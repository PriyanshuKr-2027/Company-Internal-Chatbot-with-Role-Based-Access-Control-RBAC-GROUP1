# 🎯 RAG Chatbot Demo

Quick demonstration of the RAG pipeline with role-based access control.

## 🚀 Quick Start

### Option 1: Terminal-based Chatbot

```bash
# Activate your virtual environment
# On Windows:
C:\Users\10pri\Downloads\infosys\.venv\Scripts\Activate.ps1

# On Linux/Mac:
source .venv/bin/activate

# Run the terminal chatbot
python demo_chatbot.py
```

### Option 2: Web-based Chatbot (Streamlit) ⭐ RECOMMENDED

```bash
# Install streamlit if not already installed
pip install streamlit

# Run the web interface
streamlit run demo_web_chatbot.py
```

The web interface will automatically open in your browser at `http://localhost:8501`

## 🎭 Demo Roles

Try these roles to see RBAC in action:

| Role | Access |
|------|--------|
| `admin` | All documents (finance, engineering, marketing, hr, general) |
| `finance` | Finance documents + general |
| `engineering` | Engineering documents + general |
| `marketing` | Marketing documents + general |
| `hr` | HR documents + general |
| `employee` | General documents only |

## 💡 Example Questions

### For Finance Role:
- "What were the financial results for 2024?"
- "What are the vendor service expenses?"
- "Show me the quarterly financial report"
- "What was the revenue growth in 2024?"

### For Engineering Role:
- "What are the main technical components?"
- "Explain the system architecture"
- "What technologies are used?"
- "Tell me about the engineering documentation"

### For Marketing Role:
- "What are the Q4 2024 marketing highlights?"
- "What were the marketing strategies in 2024?"
- "Show me the annual marketing report"
- "What were the Q1 2024 marketing initiatives?"

### For Employee Role:
- "What is the remote work policy?"
- "What are the company benefits?"
- "Tell me about the employee handbook"
- "What are the general company policies?"

### For Admin Role:
Try any question from any department - you have access to everything!

## 📊 Features Demonstrated

✅ **Vector Embeddings** - Semantic search using sentence-transformers  
✅ **ChromaDB** - Persistent vector database with 135 document chunks  
✅ **RBAC Filtering** - Role-based access control enforced at query time  
✅ **Source Attribution** - Every answer shows source documents  
✅ **Relevance Scoring** - Results ranked by semantic similarity  

## 🔧 Technical Details

- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- **Vector Database:** ChromaDB (persistent storage)
- **Total Vectors:** 135 chunks across 4 departments
  - 39 Engineering chunks
  - 49 Marketing chunks
  - 36 Finance chunks
  - 11 General chunks
- **Search Method:** Cosine similarity with role-based filtering

## 🎥 Demo Flow for Mentor

1. **Start with Web Interface** (more impressive):
   ```bash
   streamlit run demo_web_chatbot.py
   ```

2. **Show RBAC in action**:
   - Login as `employee` → Ask about finance → Get "No results"
   - Login as `finance` → Ask same question → Get results!
   - Login as `admin` → Ask anything → Get all results

3. **Demonstrate Search Quality**:
   - Ask specific questions and show relevance scores
   - Show source attribution with exact document references
   - Highlight department filtering

4. **Show Terminal Version** (optional):
   ```bash
   python demo_chatbot.py
   ```

## 🎯 What This Demonstrates

### ✅ Completed (Milestone 1 & 2):
- Complete data pipeline (clean → chunk → embed → index)
- Vector database with 135 semantic chunks
- RBAC filtering working correctly
- Semantic search with source attribution
- Role-based access enforcement

### ⏳ Next Steps (Milestone 3):
- Add LLM integration (OpenAI/HuggingFace) for natural language generation
- Implement JWT authentication
- Add conversation history and context
- Deploy to cloud (Streamlit Cloud, Heroku, etc.)

## 🐛 Troubleshooting

**Error: "Collection not found"**
- Make sure you've run the data pipeline first:
  ```bash
  cd processing
  python run_pipeline.py
  python chunk_only.py
  python generate_embeddings.py
  python index_embeddings.py
  ```

**Error: "Module not found"**
- Activate virtual environment
- Install requirements: `pip install -r requirements.txt`

**Streamlit not working**
- Install: `pip install streamlit`
- Check if port 8501 is available

## 📞 Support

For questions or issues, contact any team member listed in README.md

---

**Made with ❤️ by the Role-Based Access Chatbot Team**
