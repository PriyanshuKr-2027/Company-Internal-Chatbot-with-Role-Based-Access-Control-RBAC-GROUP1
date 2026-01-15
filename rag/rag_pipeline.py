"""Complete RAG Pipeline with RBAC"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from query.query_engine import QueryEngine
from llm.llm_engine import LLMEngine
from llm.config import OPENROUTER_API_KEY, DEFAULT_LLM_MODEL
from rag.prompt_templates import PromptTemplates
from rag.confidence_scorer import ConfidenceScorer


class RAGPipeline:
    """
    Complete RAG Pipeline Implementation
    
    Flow: User Authentication → RBAC Filtering → Semantic Search → 
          Context Augmentation → LLM Generation → Source Attribution
    """
    
    def __init__(self, 
                 vectorstore_path: str = "vectorstore/chroma",
                 api_key: Optional[str] = None,
                 model: str = DEFAULT_LLM_MODEL):
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
        
        print(f"✓ RAG Pipeline initialized with model: {model}")
    
    def query(self, 
              user_query: str,
              user_role: str = "employee",
              n_results: int = 5,
              include_citations: bool = True,
              max_tokens: int = 400) -> Dict[str, Any]:
        """
        Execute complete RAG pipeline
        
        Args:
            user_query: User's question
            user_role: User's role for RBAC (admin/finance/engineering/marketing/hr/employee)
            n_results: Number of documents to retrieve
            include_citations: Whether to include source citations
            max_tokens: Maximum tokens in LLM response
            
        Returns:
            Dict containing:
                - answer: Generated answer
                - sources: List of source documents with relevance
                - confidence: Confidence score and level
                - metadata: Query metadata
        """
        
        # Step 1: Authenticate user (role validation)
        valid_roles = ["admin", "finance", "engineering", "marketing", "hr", "employee"]
        if user_role not in valid_roles:
            return {
                "answer": "Error: Invalid user role",
                "sources": [],
                "confidence": {"score": 0, "level": "NONE"},
                "metadata": {"error": "Invalid role"}
            }
        
        # Step 2: Retrieve relevant documents with RBAC filtering
        search_results = self.query_engine.search(
            query=user_query,
            n_results=n_results,
            user_role=user_role
        )
        
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
        
        # Step 3: Calculate confidence score
        confidence = self.confidence_scorer.calculate_confidence(
            distances=distances,
            num_results=len(documents)
        )
        
        # Step 4: Format context for LLM
        context = self.prompt_templates.format_context(
            documents=documents[:3],  # Use top 3 for context
            metadatas=metadatas[:3],
            distances=distances[:3]
        )
        
        # Step 5: Build appropriate prompt based on query type
        prompt = self.prompt_templates.get_prompt_for_query(
            query=user_query,
            context=context,
            include_citations=include_citations
        )
        
        # Step 6: Generate answer with LLM
        try:
            answer = self.llm.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.5
            )
        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "confidence": confidence,
                "metadata": {
                    "query": user_query,
                    "role": user_role,
                    "error": str(e)
                }
            }
        
        # Step 7: Add confidence disclaimer if needed
        answer = self.confidence_scorer.add_confidence_disclaimer(
            answer=answer,
            confidence_level=confidence["level"]
        )
        
        # Step 8: Build source attribution
        sources = self.confidence_scorer.calculate_source_scores(
            distances=distances[:3],
            metadatas=metadatas[:3]
        )
        
        # Step 9: Return complete response
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "metadata": {
                "query": user_query,
                "role": user_role,
                "num_results": len(documents),
                "query_type": self.prompt_templates.detect_query_type(user_query)
            }
        }
    
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
