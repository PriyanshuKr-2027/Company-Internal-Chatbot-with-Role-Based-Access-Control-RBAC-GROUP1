"""Query Engine with Semantic Search + RBAC"""

import re
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer

# Global model cache for faster subsequent queries
_model_cache: Optional[SentenceTransformer] = None

class QueryEngine:
    """Semantic search with RBAC filtering - Optimized for low latency"""
    
    def __init__(self, vectorstore_path: str = "../vectorstore/chroma"):
        global _model_cache
        
        # Use PersistentClient for better connection pooling
        self.client = chromadb.PersistentClient(
            path=vectorstore_path
        )
        
        # Use cached model to avoid cold start on every instance
        if _model_cache is None:
            _model_cache = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.model = _model_cache
        
        self.collection = self.client.get_or_create_collection(
            name="company_documents",
            metadata={"description": "Company internal docs with RBAC metadata"}
        )
    
    def normalize_query(self, query: str) -> str:
        """Lightly normalize user input to reduce noise."""
        query = query.strip().lower()
        query = re.sub(r"\s+", " ", query)
        return query

    def search(self, query: str, n_results: int = 5, user_role: str = "employee"):
        """Search documents with RBAC filtering - Optimized with normalized embeddings"""
        normalized = self.normalize_query(query)
        
        # Use normalize_embeddings=True for better cosine similarity performance
        query_embedding = self.model.encode(normalized, normalize_embeddings=True).tolist()
        
        # Map role to correct ChromaDB filter key
        if user_role == "employee":
            role_key = "role_general"  # Employee role uses role_general flag
        else:
            role_key = f"role_{user_role}"
        
        # Build RBAC where filter
        where_filter = {role_key: True}
        
        # Search in ChromaDB with RBAC filtering at query time
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        return results
