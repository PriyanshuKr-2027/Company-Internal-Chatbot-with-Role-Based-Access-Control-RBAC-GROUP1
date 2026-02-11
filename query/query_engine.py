"""Query Engine with Semantic Search + RBAC"""

import re
import os
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
            # Set environment variable for longer timeout
            os.environ["HF_HUB_READ_TIMEOUT"] = "120"
            os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120"
            
            try:
                _model_cache = SentenceTransformer(
                    "sentence-transformers/all-MiniLM-L6-v2",
                    cache_folder=os.path.expanduser("~/.cache/sentence-transformers")
                )
            except Exception as e:
                print(f"Warning: Failed to load model from HuggingFace: {e}")
                print("Attempting to load from local cache or offline mode...")
                # Try offline mode
                os.environ["TRANSFORMERS_OFFLINE"] = "1"
                _model_cache = SentenceTransformer(
                    "sentence-transformers/all-MiniLM-L6-v2",
                    cache_folder=os.path.expanduser("~/.cache/sentence-transformers")
                )
        
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
    
    def search_by_department(self, department: str, user_role: str = "employee") -> dict:
        """
        Search employees by department using metadata filtering (exact match)
        
        Args:
            department: Department name (e.g., 'Finance', 'Engineering')
            user_role: User's role for RBAC
            
        Returns:
            Results filtered by department
        """
        # Map role to correct ChromaDB filter key
        if user_role == "employee":
            role_key = "role_general"
        else:
            role_key = f"role_{user_role}"
        
        # Build combined where filter: HR access + exact department match
        where_filter = {
            "$and": [
                {role_key: True},
                {"employee_dept": department}
            ]
        }
        
        # Get all results without limiting (will manually paginate if needed)
        results = self.collection.query(
            query_embeddings=None,
            n_results=100,
            where=where_filter
        )
        
        return results
    
    def search_by_role(self, role: str, user_role: str = "employee") -> dict:
        """
        Search employees by job role using metadata filtering (exact match)
        
        Args:
            role: Job role (e.g., 'Manager', 'Developer')
            user_role: User's role for RBAC
            
        Returns:
            Results filtered by job role
        """
        if user_role == "employee":
            role_key = "role_general"
        else:
            role_key = f"role_{user_role}"
        
        where_filter = {
            "$and": [
                {role_key: True},
                {"employee_role": role}
            ]
        }
        
        results = self.collection.query(
            query_embeddings=None,
            n_results=100,
            where=where_filter
        )
        
        return results
