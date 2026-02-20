"""Answer Generator - Generates answers from RAG search results"""

from typing import List, Dict, Any
from .llm_engine import LLMEngine

class AnswerGenerator:
    """Generate answers from search results using LLM + RAG"""
    
    def __init__(self, llm_engine: LLMEngine):
        """
        Initialize answer generator
        
        Args:
            llm_engine: LLMEngine instance for generating answers
        """
        self.llm = llm_engine
    
    def generate_answer(self, 
                       query: str, 
                       search_results: Dict[str, Any],
                       max_tokens: int = 300) -> Dict[str, str]:
        """
        Generate an answer based on search results
        
        Args:
            query: User query
            search_results: Results from semantic search (from ChromaDB)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict with answer and sources
        """
        
        # Extract documents and metadata
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        
        if not documents:
            return {
                "answer": "No relevant documents found to answer your query.",
                "sources": []
            }
        
        # Build context from top results
        context_parts = []
        sources = []
        
        for i, (doc, meta, dist) in enumerate(zip(documents[:3], metadatas[:3], distances[:3]), 1):
            relevance = (1 - dist) * 100
            context_parts.append(f"[Source {i}] {doc}")
            sources.append({
                "rank": i,
                "source": meta.get("source_document", "Unknown"),
                "section": meta.get("section_title", "N/A"),
                "relevance": f"{relevance:.1f}%"
            })
        
        context = "\n\n".join(context_parts)
        
        # Create prompt for LLM
        prompt = f"""Based on the following documents, answer the user's query.
        
User Query: {query}

Context from documents:
{context}

Please provide a clear, concise answer based on the documents above. If the answer is not in the documents, say so clearly."""
        
        # Generate answer
        answer = self.llm.generate(prompt, max_tokens=max_tokens, temperature=0.5)
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def generate_with_explanation(self,
                                 query: str,
                                 search_results: Dict[str, Any],
                                 max_tokens: int = 400) -> Dict[str, str]:
        """
        Generate answer with step-by-step explanation
        
        Args:
            query: User query
            search_results: Results from semantic search
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict with answer, explanation, and sources
        """
        
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        
        if not documents:
            return {
                "answer": "No relevant documents found.",
                "explanation": "No relevant information available.",
                "sources": []
            }
        
        context_parts = []
        sources = []
        
        for i, (doc, meta, dist) in enumerate(zip(documents[:3], metadatas[:3], distances[:3]), 1):
            relevance = (1 - dist) * 100
            context_parts.append(f"[Ref {i}] {doc}")
            sources.append({
                "rank": i,
                "source": meta.get("source_document", "Unknown"),
                "section": meta.get("section_title", "N/A"),
                "relevance": f"{relevance:.1f}%"
            })
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""Based on the documents provided, answer the user's query with a clear explanation.

User Query: {query}

Available Documents:
{context}

Please provide:
1. A clear, direct answer to the query
2. Step-by-step explanation of how you arrived at this answer
3. Key facts from the documents that support your answer

Format your response clearly with sections."""
        
        response = self.llm.generate(prompt, max_tokens=max_tokens, temperature=0.5)
        
        return {
            "answer": response,
            "explanation": "See answer above for detailed explanation",
            "sources": sources
        }
