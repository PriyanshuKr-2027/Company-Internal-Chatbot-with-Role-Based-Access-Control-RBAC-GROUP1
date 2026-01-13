"""Query Engine with Semantic Search + RBAC"""

import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class QueryEngine:
    """Semantic search with RBAC filtering"""
    
    def __init__(self, vectorstore_path: str = "../vectorstore/chroma"):
        self.client = chromadb.Client(
            Settings(
                persist_directory=vectorstore_path,
                anonymized_telemetry=False
            )
        )
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="company_documents",
            metadata={"description": "Company internal docs with RBAC metadata"}
        )
    
    def search(self, query: str, n_results: int = 5, user_role: str = "employee"):
        """Search documents with RBAC filtering"""
        # Encode query
        query_embedding = self.model.encode(query).tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Filter by role
        # TODO: Implement RBAC filtering here
        return results
