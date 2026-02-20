"""
Streamlit Web-based RAG Chatbot Demo with Backend Integration
Run with: streamlit run demo_web_chatbot.py

Requirements:
1. Backend server must be running: uvicorn backend.main:app --reload --port 8000
2. Set PYTHONPATH environment variable to project root
"""

import streamlit as st
import sys
import requests
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Backend API configuration
API_BASE_URL = "http://localhost:8000"
API_AUTH_LOGIN = f"{API_BASE_URL}/api/auth/login"
API_AUTH_LOGOUT = f"{API_BASE_URL}/api/auth/logout"
API_AUTH_ME = f"{API_BASE_URL}/api/auth/me"
API_CHAT_QUERY = f"{API_BASE_URL}/api/chat/query"

# Page config
st.set_page_config(
    page_title="Company Internal Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Sample user credentials (from backend)
SAMPLE_USERS = {
    "admin": {"password": "admin123", "full_name": "Admin User", "department": "IT"},
    "john_finance": {"password": "finance123", "full_name": "John Finance", "department": "Finance"},
    "jane_marketing": {"password": "marketing123", "full_name": "Jane Marketing", "department": "Marketing"},
    "bob_engineering": {"password": "engineering123", "full_name": "Bob Engineering", "department": "Engineering"},
    "alice_hr": {"password": "hr123", "full_name": "Alice HR", "department": "Human Resources"},
    "employee": {"password": "employee123", "full_name": "Employee User", "department": "General"}
}

def check_backend_health():
    """Check if backend server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def login_user(username: str, password: str):
    """Login user via backend API"""
    try:
        response = requests.post(
            API_AUTH_LOGIN,
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "token": data["access_token"],
                "user": data["user"]
            }
        else:
            return {
                "success": False,
                "error": response.json().get("detail", "Login failed")
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Connection error: {str(e)}"
        }

def logout_user(token: str):
    """Logout user via backend API"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(API_AUTH_LOGOUT, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def query_chatbot(token: str, query: str, n_results: int = 5):
    """Query chatbot via backend API"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            API_CHAT_QUERY,
            headers=headers,
            json={
                "query": query,
                "n_results": n_results,
                "include_citations": True
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "error": response.json().get("detail", "Query failed")
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Connection error: {str(e)}"
        }

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'backend_status' not in st.session_state:
    st.session_state.backend_status = check_backend_health()

# Sidebar - Login
with st.sidebar:
    st.title("🔐 Authentication")
    
    # Backend status
    if st.session_state.backend_status:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Offline")
        st.caption("Start backend: `uvicorn backend.main:app --reload`")
    
    st.divider()
    
    if not st.session_state.token:
        # Login form
        st.subheader("Login")
        
        # Quick select sample users
        sample_user = st.selectbox(
            "Quick Select Sample User:",
            options=[""] + list(SAMPLE_USERS.keys()),
            format_func=lambda x: "Choose a user..." if x == "" else f"{x} ({SAMPLE_USERS[x]['department']})" if x else ""
        )
        
        # Manual input
        username = st.text_input("Username", value=sample_user if sample_user else "")
        password = st.text_input(
            "Password", 
            type="password",
            value=SAMPLE_USERS[sample_user]["password"] if sample_user and sample_user in SAMPLE_USERS else ""
        )
        
        if st.button("Login", type="primary", disabled=not st.session_state.backend_status):
            if username and password:
                with st.spinner("Logging in..."):
                    result = login_user(username, password)
                    
                    if result["success"]:
                        st.session_state.token = result["token"]
                        st.session_state.user = result["user"]
                        st.session_state.messages = []
                        st.success(f"✅ Welcome, {result['user']['full_name']}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
            else:
                st.warning("Please enter username and password")
        
        # Sample credentials info
        with st.expander("📋 Sample Credentials"):
            st.caption("**Available Test Accounts:**")
            for user, info in SAMPLE_USERS.items():
                st.text(f"{user} / {info['password']}")
                st.caption(f"  └─ {info['full_name']} ({info['department']})")
    
    else:
        # User info when logged in
        user = st.session_state.user
        st.success(f"**Logged in as:**")
        st.write(f"👤 {user['full_name']}")
        st.write(f"🎭 Role: `{user['role']}`")
        st.write(f"🏢 Dept: {user['department']}")
        st.caption(f"Last login: {user.get('last_login', 'N/A')[:19]}")
        
        if st.button("Logout", type="secondary"):
            logout_user(st.session_state.token)
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()

# Main content
st.title("🤖 Company Internal Chatbot")
st.caption("RAG-powered chatbot with JWT Authentication & Role-Based Access Control")

if not st.session_state.token:
    st.info("👈 Please login to start chatting")
    
    # Backend status check
    if not st.session_state.backend_status:
        st.warning("⚠️ Backend server is not running. Please start it first:")
        st.code("""
# Set PYTHONPATH and start backend
$env:PYTHONPATH = (Get-Location).Path
uvicorn backend.main:app --reload --port 8000
        """, language="powershell")
    
    # Demo information
    st.divider()
    st.subheader("📚 Knowledge Base")
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
    st.subheader("✨ Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔐 Security:**
        - JWT token-based authentication
        - Bcrypt password hashing
        - Role-based access control (RBAC)
        - Complete audit logging
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI Capabilities:**
        - RAG with ChromaDB vector store
        - Mistral 7B LLM integration
        - 4-level confidence scoring
        - Source attribution
        """)
    
    st.divider()
    st.subheader("🎯 Sample Queries by Role")
    st.markdown("""
    - **Admin:** Full access to all documents
    - **Finance:** "What were the Q4 2024 financial results?"
    - **Engineering:** "What are the main technical components?"
    - **Marketing:** "What are the marketing campaign highlights?"
    - **HR:** "What are the employee benefits?"
    - **Employee:** "What is the remote work policy?"
    """)

else:
    # Chat interface for logged-in users
    user = st.session_state.user
    
    # Display user context
    st.info(f"💬 Chatting as **{user['full_name']}** ({user['role']} role)")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "metadata" in message:
                with st.expander("📊 Query Details"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Confidence", message["metadata"]["confidence"]["level"])
                    with col2:
                        st.metric("Score", f"{message['metadata']['confidence']['score']:.1%}")
                    with col3:
                        st.metric("Sources", len(message["metadata"].get("sources", [])))
            
            if "sources" in message:
                with st.expander("📚 View Sources"):
                    for source in message["sources"]:
                        st.markdown(f"""
                        **Source {source['rank']}** - {source['quality']}
                        - **Document:** {source['source']}
                        - **Section:** {source['section']}
                        - **Relevance:** {source['relevance_percent']}
                        """)
                        st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about company documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Query backend
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching knowledge base..."):
                result = query_chatbot(st.session_state.token, prompt)
                
                if result["success"]:
                    data = result["data"]
                    
                    # Display answer
                    st.markdown(data["answer"])
                    
                    # Display confidence badge
                    confidence = data["confidence"]
                    confidence_color = {
                        "VERY_HIGH": "🟢",
                        "HIGH": "🟡",
                        "MEDIUM": "🟠",
                        "LOW": "🔴"
                    }.get(confidence["level"], "⚪")
                    
                    st.caption(f"{confidence_color} **Confidence:** {confidence['level']} ({confidence['score']:.1%})")
                    st.caption(f"💡 {confidence['reasoning']}")
                    
                    # Save assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                        "sources": data.get("sources", []),
                        "metadata": data
                    })
                    
                    # Display sources
                    if data.get("sources"):
                        with st.expander(f"📚 View {len(data['sources'])} Sources"):
                            for source in data["sources"]:
                                quality_emoji = {
                                    "Highly Relevant": "🟢",
                                    "Relevant": "🟡",
                                    "Somewhat Relevant": "🟠",
                                    "Marginally Relevant": "🔴"
                                }.get(source["quality"], "⚪")
                                
                                st.markdown(f"""
                                {quality_emoji} **Source {source['rank']}** - {source['quality']}
                                - **Document:** `{source['source']}`
                                - **Section:** {source['section']}
                                - **Relevance:** {source['relevance_percent']} (Score: {source['relevance_score']:.3f})
                                """)
                                st.divider()
                else:
                    error_msg = f"❌ Error: {result['error']}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    
                    # Check if token expired
                    if "token" in result["error"].lower() or "unauthorized" in result["error"].lower():
                        st.warning("Your session may have expired. Please login again.")
                        if st.button("Logout and Re-login"):
                            st.session_state.token = None
                            st.session_state.user = None
                            st.session_state.messages = []
                            st.rerun()

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🤖 Powered by Mistral 7B")
with col2:
    st.caption("🔒 Secured with JWT + RBAC")
with col3:
    st.caption("📊 ChromaDB Vector Store")
