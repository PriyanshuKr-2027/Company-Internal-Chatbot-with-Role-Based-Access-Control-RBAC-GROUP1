"""
Run the FastAPI backend server
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    from backend.main import app
    
    print("🚀 Starting Company Internal Chatbot API...")
    print("📍 Server running at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🔧 Alternative docs: http://127.0.0.1:8000/redoc")
    print("\n✅ Press Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
