"""FastAPI Backend Application - Main Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import auth, chat
from backend.middleware.rbac_middleware import RBACMiddleware
from backend.middleware.audit_middleware import AuditMiddleware
from backend.database.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Company Internal Chatbot API",
    description="Secure chatbot API with RBAC and RAG pipeline",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(AuditMiddleware)
app.add_middleware(RBACMiddleware)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Company Internal Chatbot API",
        "version": "1.0.0",
        "status": "operational"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "rag_pipeline": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
