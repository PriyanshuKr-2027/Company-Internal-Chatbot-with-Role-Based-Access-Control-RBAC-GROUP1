"""
Terminal-based RAG Chatbot Demo
Demonstrates semantic search with RBAC filtering
"""

import sys
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class SimpleRAGChatbot:
    """Simple RAG chatbot with RBAC"""
    
    def __init__(self):
        vectorstore_path = project_root / "vectorstore" / "chroma"
        
        print("🔄 Loading vector database...")
        self.client = chromadb.PersistentClient(path=str(vectorstore_path))
        self.collection = self.client.get_collection(name="company_documents")
        
        print("🔄 Loading embedding model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Role hierarchy
        self.role_permissions = {
            "admin": ["admin", "finance", "engineering", "hr", "marketing", "employee"],
            "finance": ["finance", "employee"],
            "engineering": ["engineering", "employee"],
            "hr": ["hr", "employee"],
            "marketing": ["marketing", "employee"],
            "employee": ["employee"]
        }
        
        print("✅ Chatbot ready!\n")

    @staticmethod
    def normalize_query(query: str) -> str:
        """Light normalization to reduce noise from user input."""
        query = query.strip().lower()
        query = re.sub(r"\s+", " ", query)
        return query
    
    def search_documents(self, query: str, user_role: str, top_k: int = 5):
        """Search documents with RBAC filtering"""
        
        normalized = self.normalize_query(query)
        query_embedding = self.model.encode(normalized).tolist()
        
        # Get role-specific filter
        role_key = f"role_{user_role}"
        
        # Search with role filter
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={role_key: True}  # Filter by role
        )
        
        return results
    
    def format_response(self, results):
        """Format search results for display"""
        if not results['documents'] or not results['documents'][0]:
            return "❌ No relevant documents found for your role."
        
        response = "\n" + "="*80 + "\n"
        response += "📚 SEARCH RESULTS\n"
        response += "="*80 + "\n\n"
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ), 1):
            relevance = (1 - distance) * 100  # Convert distance to relevance %
            
            response += f"📄 Result {i} (Relevance: {relevance:.1f}%)\n"
            response += f"   Source: {metadata.get('source_document', 'Unknown')}\n"
            response += f"   Section: {metadata.get('section_title', 'N/A')}\n"
            response += f"   Department: {metadata.get('department', 'N/A')}\n"
            response += f"\n   Content:\n   {doc[:300]}{'...' if len(doc) > 300 else ''}\n"
            response += "-" * 80 + "\n\n"
        
        return response
    
    def chat(self):
        """Interactive chat loop"""
        
        print("="*80)
        print("🤖 COMPANY INTERNAL CHATBOT - RAG DEMO")
        print("="*80)
        print("\nAvailable roles: admin, finance, engineering, marketing, hr, employee")
        print("Commands: 'quit' to exit, 'role' to change role\n")
        
        # Select role
        user_role = input("👤 Select your role: ").strip().lower()
        while user_role not in self.role_permissions:
            print("❌ Invalid role. Please choose from: admin, finance, engineering, marketing, hr, employee")
            user_role = input("👤 Select your role: ").strip().lower()
        
        print(f"\n✅ Logged in as: {user_role}")
        print(f"📋 You have access to: {', '.join(self.role_permissions[user_role])}\n")
        
        while True:
            print("-" * 80)
            query = input("\n💬 Your question (or 'quit'/'role'): ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'role':
                user_role = input("\n👤 Select new role: ").strip().lower()
                while user_role not in self.role_permissions:
                    print("❌ Invalid role.")
                    user_role = input("👤 Select your role: ").strip().lower()
                print(f"✅ Logged in as: {user_role}")
                print(f"📋 You have access to: {', '.join(self.role_permissions[user_role])}\n")
                continue
            
            print("\n🔍 Searching...")
            
            try:
                results = self.search_documents(query, user_role)
                response = self.format_response(results)
                print(response)
                
                # Simple answer generation (without LLM for now)
                if results['documents'] and results['documents'][0]:
                    print("💡 ANSWER (based on top result):")
                    print("-" * 80)
                    print(results['documents'][0][0][:500] + "...")
                    print("-" * 80)
                
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    try:
        chatbot = SimpleRAGChatbot()
        chatbot.chat()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error initializing chatbot: {str(e)}")
        import traceback
        traceback.print_exc()
