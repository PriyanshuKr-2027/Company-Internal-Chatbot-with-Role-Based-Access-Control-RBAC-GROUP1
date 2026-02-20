"""
ChromaDB Client Module
Handles interactions with the ChromaDB vector database
"""

import chromadb
from chromadb.config import Settings
import os
from pathlib import Path


class ChromaClient:
    """
    Client for managing ChromaDB vector store operations
    """
    
    def __init__(self, persist_directory: str = None):
        """
        Initialize ChromaDB client
        
        Args:
            persist_directory: Path to persist ChromaDB data (default: ./vectorstore/chroma)
        """
        if persist_directory is None:
            base_path = Path(__file__).parent.parent
            persist_directory = str(base_path / "vectorstore" / "chroma")
        
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self.persist_directory = persist_directory
    
    def get_or_create_collection(self, collection_name: str = "company_docs"):
        """
        Get or create a collection in ChromaDB
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            ChromaDB collection object
        """
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, collection_name: str, documents: list, embeddings: list, 
                     metadatas: list, ids: list):
        """
        Add documents to a collection
        
        Args:
            collection_name: Name of the collection
            documents: List of document texts
            embeddings: List of embedding vectors
            metadatas: List of metadata dictionaries
            ids: List of unique IDs
        """
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def query_documents(self, collection_name: str, query_embeddings: list, 
                       n_results: int = 5, where: dict = None):
        """
        Query documents from a collection
        
        Args:
            collection_name: Name of the collection
            query_embeddings: List of query embedding vectors
            n_results: Number of results to return
            where: Metadata filter dictionary
            
        Returns:
            Query results from ChromaDB
        """
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )
    
    def reset_database(self):
        """
        Reset the entire database (use with caution)
        """
        self.client.reset()
    
    def delete_collection(self, collection_name: str):
        """
        Delete a specific collection
        
        Args:
            collection_name: Name of the collection to delete
        """
        try:
            self.client.delete_collection(name=collection_name)
        except Exception as e:
            print(f"Error deleting collection {collection_name}: {e}")
    
    def list_collections(self):
        """
        List all collections in the database
        
        Returns:
            List of collection objects
        """
        return self.client.list_collections()
