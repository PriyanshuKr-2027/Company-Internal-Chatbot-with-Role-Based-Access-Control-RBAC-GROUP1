"""
Streamlit Web-based RAG Chatbot Demo
Run with: streamlit run demo_web_chatbot.py
"""

import streamlit as st
import sys
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import chromadb
from sentence_transformers import SentenceTransformer

# Page config
st.set_page_config(
    page_title="Company Internal Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Role permissions
ROLE_PERMISSIONS = {
    "admin": ["admin", "finance", "engineering", "hr", "marketing", "employee"],
    "finance": ["finance", "employee"],
    "engineering": ["engineering", "employee"],
    "hr": ["hr", "employee"],
    "marketing": ["marketing", "employee"],
    "employee": ["employee"]
}

@st.cache_resource
def load_chatbot():
    """Load vector database and model (cached)"""
    vectorstore_path = project_root / "vectorstore" / "chroma"
    
    client = chromadb.PersistentClient(path=str(vectorstore_path))
    collection = client.get_collection(name="company_documents")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    return collection, model

def normalize_query(query: str) -> str:
    """Lightly normalize user input before embedding."""
    query = query.strip().lower()
    query = re.sub(r"\s+", " ", query)
    return query

def search_documents(collection, model, query: str, user_role: str, top_k: int = 5):
    """Search documents with RBAC filtering"""
    normalized = normalize_query(query)
    query_embedding = model.encode(normalized).tolist()
    role_key = f"role_{user_role}"
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={role_key: True}
    )
    
    return results

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Sidebar - Login
with st.sidebar:
    st.title("🔐 Login")
    
    selected_role = st.selectbox(
        "Select your role:",
        options=[""] + list(ROLE_PERMISSIONS.keys()),
        format_func=lambda x: "Choose a role..." if x == "" else x.capitalize()
    )
    
    if st.button("Login") and selected_role:
        st.session_state.user_role = selected_role
        st.session_state.messages = []
        st.success(f"✅ Logged in as: {selected_role}")
        st.rerun()
    
    if st.session_state.user_role:
        st.divider()
        st.write(f"**Current Role:** {st.session_state.user_role.capitalize()}")
        st.write(f"**Access to:** {', '.join(ROLE_PERMISSIONS[st.session_state.user_role])}")
        
        if st.button("Logout"):
            st.session_state.user_role = None
            st.session_state.messages = []
            st.rerun()

# Main content
st.title("🤖 Company Internal Chatbot")
st.caption("RAG-powered chatbot with Role-Based Access Control")

if not st.session_state.user_role:
    st.info("👈 Please login with your role to start chatting")
    
    # Demo information
    st.divider()
    st.subheader("📚 Available Documents")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Engineering", "39 chunks", "🔧")
    with col2:
        st.metric("Marketing", "49 chunks", "📈")
    with col3:
        st.metric("Finance", "36 chunks", "💰")
    with col4:
        st.metric("General", "11 chunks", "📄")
    
    st.divider()
    st.subheader("🎯 Try asking:")
    st.markdown("""
    - **Engineering:** "What are the main technical components?"
    - **Finance:** "What were the financial results for 2024?"
    - **Marketing:** "What are the Q4 marketing highlights?"
    - **General:** "What is the company's remote work policy?"
    """)

else:
    # Load chatbot
    try:
        collection, model = load_chatbot()
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("📚 View Sources"):
                        st.json(message["sources"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Search and respond
            with st.chat_message("assistant"):
                with st.spinner("Searching documents..."):
                    results = search_documents(
                        collection, 
                        model, 
                        prompt, 
                        st.session_state.user_role
                    )
                    
                    if results['documents'] and results['documents'][0]:
                        # Display answer
                        answer = results['documents'][0][0][:500] + "..."
                        st.markdown(f"**Answer based on relevant documents:**\n\n{answer}")
                        
                        # Display sources
                        sources = []
                        for i, (doc, metadata, distance) in enumerate(zip(
                            results['documents'][0][:3],
                            results['metadatas'][0][:3],
                            results['distances'][0][:3]
                        ), 1):
                            relevance = (1 - distance) * 100
                            sources.append({
                                "rank": i,
                                "source": metadata.get('source_document'),
                                "section": metadata.get('section_title'),
                                "department": metadata.get('department'),
                                "relevance": f"{relevance:.1f}%",
                                "preview": doc[:200] + "..."
                            })
                        
                        with st.expander("📚 View Sources"):
                            for source in sources:
                                st.markdown(f"""
                                **Source {source['rank']}** (Relevance: {source['relevance']})
                                - **Document:** {source['source']}
                                - **Section:** {source['section']}
                                - **Department:** {source['department']}
                                
                                *Preview:* {source['preview']}
                                """)
                                st.divider()
                        
                        # Save assistant response
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Answer based on relevant documents:**\n\n{answer}",
                            "sources": sources
                        })
                    else:
                        no_results = "❌ No relevant documents found for your role and query."
                        st.warning(no_results)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": no_results
                        })
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
