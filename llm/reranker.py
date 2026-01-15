"""Result Reranker - Re-ranks search results using LLM for better relevance"""

from typing import List, Dict, Any
from .llm_engine import LLMEngine

class ResultReranker:
    """Re-rank search results using LLM to improve relevance"""
    
    def __init__(self, llm_engine: LLMEngine):
        """
        Initialize reranker
        
        Args:
            llm_engine: LLMEngine instance for re-ranking
        """
        self.llm = llm_engine
    
    def rerank(self, 
               query: str,
               search_results: Dict[str, Any],
               top_k: int = 3) -> Dict[str, Any]:
        """
        Re-rank search results using LLM
        
        Args:
            query: User query
            search_results: Original search results from ChromaDB
            top_k: Number of results to return after re-ranking
            
        Returns:
            Re-ranked search results
        """
        
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        ids = search_results.get("ids", [[]])[0]
        
        if not documents:
            return search_results
        
        # Build list of documents with their info
        doc_list = []
        for i, (doc, meta, dist, doc_id) in enumerate(zip(documents, metadatas, distances, ids)):
            relevance = (1 - dist) * 100
            doc_list.append({
                "index": i,
                "id": doc_id,
                "text": doc[:200] + "..." if len(doc) > 200 else doc,
                "source": meta.get("source_document", "Unknown"),
                "section": meta.get("section_title", "N/A"),
                "original_relevance": f"{relevance:.1f}%",
                "metadata": meta
            })
        
        # Create prompt for LLM to re-rank
        doc_descriptions = "\n".join([
            f"{i+1}. [{d['source']} - {d['section']}]: {d['text']}"
            for i, d in enumerate(doc_list)
        ])
        
        prompt = f"""You are an expert at ranking document relevance. 
        
User Query: "{query}"

Documents to rank:
{doc_descriptions}

Please rank these documents from most to least relevant for answering the query.
Return ONLY a comma-separated list of document numbers in order of relevance.
For example: "2,1,3" means document 2 is most relevant, then 1, then 3.

ANSWER (ONLY numbers, no explanation):"""
        
        # Get LLM ranking
        ranking_str = self.llm.generate(prompt, max_tokens=50, temperature=0.1)
        
        # Parse the ranking
        try:
            ranks = [int(x.strip()) - 1 for x in ranking_str.strip().split(",") if x.strip().isdigit()]
        except:
            # If parsing fails, return original order
            ranks = list(range(len(documents)))
        
        # Filter to top_k and reorder
        reranked_indices = [r for r in ranks if 0 <= r < len(documents)][:top_k]
        
        # Build reranked results
        reranked = {
            "documents": [[documents[i] for i in reranked_indices]],
            "metadatas": [[metadatas[i] for i in reranked_indices]],
            "distances": [[distances[i] for i in reranked_indices]],
            "ids": [[ids[i] for i in reranked_indices]] if ids else [[]],
        }
        
        return reranked
    
    def score_relevance(self, query: str, document: str) -> float:
        """
        Score relevance of a single document to a query
        
        Args:
            query: User query
            document: Document text
            
        Returns:
            Relevance score (0-100)
        """
        
        prompt = f"""Rate the relevance of the following document to the query on a scale of 0-100.

Query: "{query}"

Document: "{document[:300]}"

Respond with ONLY a number between 0-100:"""
        
        response = self.llm.generate(prompt, max_tokens=10, temperature=0.0)
        
        try:
            score = float(response.strip())
            return max(0, min(100, score))  # Clamp between 0-100
        except:
            return 50.0  # Default if parsing fails
