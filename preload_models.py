#!/usr/bin/env python3
"""
Preload ML models to cache them locally before application starts.
This prevents timeout errors on first request.

Run this script once: python preload_models.py
"""

import os
import sys
from pathlib import Path

# Set environment variables for longer timeouts
os.environ["HF_HUB_READ_TIMEOUT"] = "300"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "300"
os.environ["TRANSFORMERS_OFFLINE"] = "0"

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def preload_sentence_transformer():
    """Preload sentence-transformers embedding model"""
    print("📥 Preloading Sentence Transformer (all-MiniLM-L6-v2)...")
    try:
        from sentence_transformers import SentenceTransformer
        
        cache_folder = os.path.expanduser("~/.cache/sentence-transformers")
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=cache_folder
        )
        print("✅ Sentence Transformer loaded successfully!")
        
        # Test encoding
        test_embedding = model.encode("test query", normalize_embeddings=True)
        print(f"✅ Model encoding test passed! Embedding dimension: {len(test_embedding)}")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Failed to preload Sentence Transformer: {e}")
        return False

def preload_chromadb():
    """Initialize ChromaDB collection"""
    print("\n📥 Initializing ChromaDB...")
    try:
        import chromadb
        
        client = chromadb.PersistentClient(path="vectorstore/chroma")
        collection = client.get_or_create_collection(
            name="company_documents",
            metadata={"description": "Company internal docs with RBAC metadata"}
        )
        
        count = collection.count()
        print(f"✅ ChromaDB initialized! Documents in collection: {count}")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Failed to initialize ChromaDB: {e}")
        return False

def test_llm_connection():
    """Test OpenRouter API connection"""
    print("\n📥 Testing OpenRouter API connection...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("⚠️ Warning: OPENROUTER_API_KEY not set in .env file")
            return False
        
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        # Test with minimal request
        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": "Hi"}
            ],
            "temperature": 0.7,
            "max_tokens": 10,
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ OpenRouter API connection successful!")
            return True
        else:
            print(f"⚠️ Warning: OpenRouter API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Warning: Failed to test OpenRouter API: {e}")
        return False

def main():
    """Main preload function"""
    print("=" * 50)
    print("🚀 ML Models Preloader")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 3
    
    # Preload Sentence Transformer
    if preload_sentence_transformer():
        success_count += 1
    
    # Initialize ChromaDB
    if preload_chromadb():
        success_count += 1
    
    # Test LLM connection
    if test_llm_connection():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Preload Complete: {success_count}/{total_tasks} tasks successful")
    print("=" * 50)
    print("\n🎯 You can now start the application:")
    print("   Backend: uvicorn backend.main:app --port 8000")
    print("   Frontend: streamlit run \"demo preview/demo_web_chatbot.py\"")
    print("=" * 50)

if __name__ == "__main__":
    main()
