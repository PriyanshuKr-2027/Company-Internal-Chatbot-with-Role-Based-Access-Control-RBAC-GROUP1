"""LLM-Powered RAG Chatbot with Answer Generation and Re-ranking"""

import sys
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import chromadb
from sentence_transformers import SentenceTransformer
from llm.llm_engine import LLMEngine
from llm.answer_generator import AnswerGenerator
from llm.reranker import ResultReranker
from llm.config import OPENROUTER_API_KEY, DEFAULT_LLM_MODEL, FEATURES

class LLMPoweredChatbot:
    """RAG Chatbot with LLM-powered answer generation"""
    
    def __init__(self, vectorstore_path: str = "./vectorstore/chroma"):
        """Initialize LLM-powered chatbot"""
        
        print("🔄 Initializing LLM-Powered Chatbot...")
        
        # Initialize vector database
        print("  Loading vector database...")
        self.client = chromadb.PersistentClient(path=vectorstore_path)
        self.collection = self.client.get_collection(name="company_documents")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize LLM components
        if FEATURES["enable_llm"]:
            try:
                print("  Initializing LLM engine...")
                self.llm = LLMEngine(api_key=OPENROUTER_API_KEY, model=DEFAULT_LLM_MODEL)
                
                if FEATURES["enable_answer_generation"]:
                    self.answer_gen = AnswerGenerator(self.llm)
                    print("  ✓ Answer generator ready")
                else:
                    self.answer_gen = None
                
                if FEATURES["enable_reranking"]:
                    self.reranker = ResultReranker(self.llm)
                    print("  ✓ Result reranker ready")
                else:
                    self.reranker = None
                    
            except Exception as e:
                print(f"  ⚠️  LLM initialization failed: {e}")
                self.llm = None
                self.answer_gen = None
                self.reranker = None
        else:
            self.llm = None
            self.answer_gen = None
            self.reranker = None
        
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
        """Normalize user input"""
        query = query.strip().lower()
        query = re.sub(r"\s+", " ", query)
        return query
    
    def search_documents(self, query: str, user_role: str, top_k: int = 5):
        """Search with semantic search"""
        normalized = self.normalize_query(query)
        query_embedding = self.model.encode(normalized, normalize_embeddings=True).tolist()
        
        # Map role to ChromaDB filter
        if user_role == "employee":
            role_key = "role_general"
        else:
            role_key = f"role_{user_role}"
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={role_key: True}
        )
        
        return results
    
    def process_query(self, query: str, user_role: str, use_llm: bool = True):
        """Process query and generate answer"""
        
        # Step 1: Semantic search
        print(f"\n🔍 Searching for relevant documents...")
        search_results = self.search_documents(query, user_role, top_k=5)
        
        if not search_results["documents"][0]:
            return {
                "answer": "No relevant documents found for your query.",
                "sources": [],
                "method": "semantic_search"
            }
        
        print(f"✓ Found {len(search_results['documents'][0])} documents")
        
        # Step 2: Re-rank results if LLM available
        if use_llm and self.reranker and FEATURES["enable_reranking"]:
            print(f"🔄 Re-ranking results for better relevance...")
            try:
                search_results = self.reranker.rerank(query, search_results, top_k=3)
                print(f"✓ Results re-ranked")
            except Exception as e:
                print(f"⚠️  Re-ranking failed: {e}. Using original ranking.")
        
        # Step 3: Generate answer with LLM if available
        if use_llm and self.answer_gen and FEATURES["enable_answer_generation"]:
            print(f"✨ Generating answer with LLM...")
            try:
                result = self.answer_gen.generate_answer(query, search_results, max_tokens=300)
                result["method"] = "llm_generated"
                print(f"✓ Answer generated")
                return result
            except Exception as e:
                print(f"⚠️  LLM generation failed: {e}. Using document excerpts.")
        
        # Fallback: Return document excerpts
        return self._format_search_results(search_results)
    
    def _format_search_results(self, search_results):
        """Format search results as fallback"""
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        
        if not documents:
            return {
                "answer": "No relevant information found.",
                "sources": [],
                "method": "semantic_search"
            }
        
        # Combine top 2 documents as answer
        answer_parts = []
        sources = []
        
        for i, (doc, meta, dist) in enumerate(zip(documents[:2], metadatas[:2], distances[:2]), 1):
            relevance = (1 - dist) * 100
            answer_parts.append(doc)
            sources.append({
                "rank": i,
                "source": meta.get("source_document", "Unknown"),
                "section": meta.get("section_title", "N/A"),
                "relevance": f"{relevance:.1f}%"
            })
        
        return {
            "answer": "\n\n".join(answer_parts),
            "sources": sources,
            "method": "semantic_search"
        }
    
    def interactive_chat(self):
        """Start interactive chat session"""
        print("\n" + "=" * 80)
        print("COMPANY INTERNAL CHATBOT - INTERACTIVE MODE")
        print("=" * 80)
        
        # Role selection
        print("\nAvailable roles:")
        for i, role in enumerate(self.role_permissions.keys(), 1):
            print(f"  {i}. {role.capitalize()}")
        
        role_input = input("\nSelect your role (1-6): ").strip()
        roles = list(self.role_permissions.keys())
        
        try:
            user_role = roles[int(role_input) - 1]
            print(f"\n✓ Logged in as: {user_role}")
        except (ValueError, IndexError):
            user_role = "employee"
            print(f"Using default role: employee")
        
        print("\n" + "=" * 80)
        print("Type your question or 'quit' to exit")
        print("=" * 80)
        
        while True:
            query = input("\n🤔 Your question: ").strip()
            
            if query.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                print("Please enter a question.")
                continue
            
            result = self.process_query(query, user_role, use_llm=True)
            
            print("\n" + "=" * 80)
            print("📝 ANSWER")
            print("=" * 80)
            print(result["answer"][:500] + "..." if len(result["answer"]) > 500 else result["answer"])
            
            print("\n📚 SOURCES")
            print("=" * 80)
            for source in result["sources"]:
                print(f"  [{source['rank']}] {source['source']} - {source['section']}")
                print(f"      Relevance: {source['relevance']}")
            
            print(f"\n⚙️  Method: {result['method']}")

if __name__ == "__main__":
    try:
        chatbot = LLMPoweredChatbot()
        chatbot.interactive_chat()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
