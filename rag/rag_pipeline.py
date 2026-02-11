"""Complete RAG Pipeline with RBAC"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from query.query_engine import QueryEngine
from llm.llm_engine import LLMEngine
from llm.config import OPENROUTER_API_KEY, DEFAULT_LLM_MODEL
from llm.reranker import ResultReranker
from rag.prompt_templates import PromptTemplates
from rag.confidence_scorer import ConfidenceScorer
from rag.cache_manager import get_cache_manager
from rag.hybrid_generator import create_hybrid_generator


class RAGPipeline:
    """
    Complete RAG Pipeline Implementation with caching
    
    Flow: Cache Check → User Authentication → RBAC Filtering → Semantic Search → 
          Context Augmentation → LLM Generation → Source Attribution
    """
    
    def __init__(self, 
                 vectorstore_path: str = "vectorstore/chroma",
                 api_key: Optional[str] = None,
                 model: str = "google/gemma-3n-e2b-it:free"):
        """
        Initialize RAG Pipeline
        
        Args:
            vectorstore_path: Path to ChromaDB vector store
            api_key: OpenRouter API key (defaults to env variable)
            model: LLM model to use
        """
        # Initialize components
        self.query_engine = QueryEngine(vectorstore_path)
        
        # Initialize LLM
        api_key = api_key or OPENROUTER_API_KEY
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment or parameters")
        
        self.llm = LLMEngine(api_key=api_key, model=model)
        
        # Initialize utilities
        self.prompt_templates = PromptTemplates()
        self.confidence_scorer = ConfidenceScorer()
        self.cache = get_cache_manager()
        self.hybrid_generator = create_hybrid_generator(self.llm, self.query_engine)
        self.reranker = ResultReranker(self.llm)
        
        print(f"✓ RAG Pipeline initialized with model: {model}")
    
    def _handle_conversational_query(self, query: str) -> Optional[str]:
        """
        Detect and respond to conversational queries (greetings, small talk)
        
        Args:
            query: User's query
            
        Returns:
            Response string if conversational, None if it's a real query
        """
        query_lower = query.lower().strip()
        
        # Simple greetings
        greetings = ["hi", "hello", "hey", "hiya", "greetings", "good morning", 
                    "good afternoon", "good evening", "howdy"]
        if query_lower in greetings:
            return "Hello! I'm your company assistant. I can help you find information about engineering, finance, marketing, HR, and general company policies. What would you like to know?"
        
        # Thanks/appreciation
        thanks = ["thanks", "thank you", "thx", "ty", "appreciate it"]
        if query_lower in thanks:
            return "You're welcome! Let me know if you need anything else."
        
        # How are you
        if any(phrase in query_lower for phrase in ["how are you", "how's it going", "what's up"]):
            return "I'm doing great, thank you for asking! I'm here to help you find information. What can I assist you with today?"
        
        # Goodbye
        goodbye = ["bye", "goodbye", "see you", "later", "exit", "quit"]
        if query_lower in goodbye:
            return "Goodbye! Feel free to come back anytime you need assistance."
        
        # Very short queries (likely conversational)
        if len(query_lower) <= 3 and query_lower not in ["who", "why", "how"]:
            return "I'm here to help! Please ask me a question about engineering, finance, marketing, HR, or general company information."
        
        return None
    
    def query(self, 
              user_query: str,
              user_role: str = "employee",
              n_results: int = 5,
              include_citations: bool = True,
              max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Execute complete RAG pipeline with caching
        
        Args:
            user_query: User's question
            user_role: User's role for RBAC (admin/finance/engineering/marketing/hr/employee)
            n_results: Number of documents to retrieve (default: 3 for speed)
            include_citations: Whether to include source citations
            max_tokens: Maximum tokens in LLM response (default: 300 for speed)
            
        Returns:
            Dict containing:
                - answer: Generated answer
                - sources: List of source documents with relevance
                - confidence: Confidence score and level
                - metadata: Query metadata
                - response_time: Time taken to generate response
        """
        
        start_time = time.time()
        
        # Step 0: Handle conversational queries (greetings, small talk)
        conversational_response = self._handle_conversational_query(user_query)
        if conversational_response:
            return {
                "answer": conversational_response,
                "sources": [],
                "confidence": {
                    "score": 1.0,
                    "level": "HIGH",
                    "reasoning": "Conversational response"
                },
                "metadata": {
                    "query": user_query,
                    "role": user_role,
                    "query_type": "conversational",
                    "response_time": f"{(time.time() - start_time):.2f}s",
                    "from_cache": False
                }
            }
        
        # Step 1: Check cache first (for same query + role + n_results)
        cached_result = self.cache.get(user_query, user_role, n_results)
        if cached_result:
            cached_result["metadata"]["from_cache"] = True
            cached_result["metadata"]["response_time"] = f"{(time.time() - start_time):.2f}s"
            return cached_result
        
        # Step 1: Authenticate user (role validation)
        valid_roles = ["admin", "finance", "engineering", "marketing", "hr", "employee"]
        if user_role not in valid_roles:
            return {
                "answer": "Error: Invalid user role",
                "sources": [],
                "confidence": {"score": 0, "level": "NONE"},
                "metadata": {"error": "Invalid role"}
            }
        
        # Step 1b: Check if HR query and user has access (only admin/hr can see employee data)
        query_type = self.prompt_templates.detect_query_type(user_query)
        is_hr_query = query_type == 'hr'
        is_aggregation = self.prompt_templates.is_hr_aggregation_query(user_query) if is_hr_query else False
        
        if is_hr_query and user_role not in ["admin", "hr"]:
            return {
                "answer": "You don't have access to employee data. Please contact your HR department.",
                "sources": [],
                "confidence": {
                    "score": 0.0,
                    "level": "NONE",
                    "reasoning": "Access restricted to HR/Admin only"
                },
                "metadata": {
                    "query": user_query,
                    "role": user_role,
                    "error": "Access denied"
                }
            }
        
        # Step 2: Retrieve relevant documents with RBAC filtering
        # For HR queries about total employees, fetch more results
        if is_hr_query and is_aggregation:
            # Aggregation queries need all matching employees
            search_results = self.query_engine.search(
                query=user_query,
                n_results=100,  # Get more results for counting
                user_role=user_role
            )
        else:
            search_results = self.query_engine.search(
                query=user_query,
                n_results=n_results,
                user_role=user_role
            )
        
        # Step 2b: Re-rank results for better relevance (LLM-based filtering)
        # Skip re-ranking for now due to timeout issues - will implement async version later
        # try:
        #     search_results = self.reranker.rerank(
        #         query=user_query,
        #         search_results=search_results,
        #         top_k=3  # Keep only top 3 most relevant
        #     )
        # except Exception as e:
        #     print(f"Note: Re-ranking skipped due to: {str(e)}")
        
        # Extract results
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        
        # Handle no results
        if not documents:
            return {
                "answer": f"No documents accessible to role '{user_role}' were found for this query.",
                "sources": [],
                "confidence": {
                    "score": 0.0,
                    "level": "NONE",
                    "reasoning": "No relevant documents found"
                },
                "metadata": {
                    "query": user_query,
                    "role": user_role,
                    "num_results": 0,
                    "query_type": self.prompt_templates.detect_query_type(user_query)
                }
            }
        
        # Step 3: Calculate confidence score (use HR-specific thresholds for employee queries)
        confidence = self.confidence_scorer.calculate_confidence(
            distances=distances,
            num_results=len(documents),
            is_hr_query=is_hr_query
        )
        
        # Step 4: Format context for LLM (use top 3-4 documents for better context)
        context = self.prompt_templates.format_context(
            documents=documents[:4],
            metadatas=metadatas[:4],
            distances=distances[:4]
        )
        
        # Step 5: Build appropriate prompt based on query type
        prompt = self.prompt_templates.get_prompt_for_query(
            query=user_query,
            context=context,
            include_citations=include_citations
        )
        
        # Step 6: Generate answer using HYBRID approach (extract + minimal LLM)
        try:
            answer = self.hybrid_generator.generate_answer(
                user_query=user_query,
                documents=documents[:5],
                metadatas=metadatas[:5],
                user_role=user_role,
                is_hr_query=is_hr_query,
                is_aggregation=is_aggregation
            )
        except Exception as e:
            result = {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "confidence": confidence,
                "metadata": {
                    "query": user_query,
                    "role": user_role,
                    "error": str(e),
                    "response_time": f"{(time.time() - start_time):.2f}s",
                    "from_cache": False
                }
            }
            self.cache.set(user_query, user_role, n_results, result)
            return result
        
        # Step 7: Add confidence disclaimer if needed
        answer = self.confidence_scorer.add_confidence_disclaimer(
            answer=answer,
            confidence_level=confidence["level"]
        )
        
        # Step 8: Build source attribution
        sources = self.confidence_scorer.calculate_source_scores(
            distances=distances[:4],
            metadatas=metadatas[:4]
        )
        
        # Step 9: Return complete response with caching
        result = {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "metadata": {
                "query": user_query,
                "role": user_role,
                "num_results": len(documents),
                "query_type": self.prompt_templates.detect_query_type(user_query),
                "response_time": f"{(time.time() - start_time):.2f}s",
                "from_cache": False
            }
        }
        
        # Cache the result for future queries
        self.cache.set(user_query, user_role, n_results, result)
        
        return result
    
    def query_simple(self, user_query: str, user_role: str = "employee") -> str:
        """
        Simplified query interface - returns just the answer
        
        Args:
            user_query: User's question
            user_role: User's role
            
        Returns:
            Answer string
        """
        result = self.query(user_query, user_role)
        return result["answer"]
    
    def query_with_sources(self, user_query: str, user_role: str = "employee") -> str:
        """
        Query with formatted sources appended
        
        Args:
            user_query: User's question
            user_role: User's role
            
        Returns:
            Answer with sources formatted as text
        """
        result = self.query(user_query, user_role)
        
        response = result["answer"]
        
        if result["sources"]:
            response += "\n\n📚 Sources:"
            for source in result["sources"]:
                response += f"\n  [{source['rank']}] {source['source']} - {source['section']} ({source['relevance_percent']}, {source['quality']})"
        
        response += f"\n\n🎯 Confidence: {result['confidence']['level']} ({result['confidence']['score']:.1%})"
        
        return response
