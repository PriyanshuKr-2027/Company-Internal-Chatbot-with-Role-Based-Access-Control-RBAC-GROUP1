# Backend Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Create sample users
python -m backend.init_users
```

This creates 6 sample accounts:
- `admin` / `admin123`
- `john_finance` / `finance123`
- `jane_marketing` / `marketing123`
- `bob_engineering` / `engineering123`
- `alice_hr` / `hr123`
- `employee` / `employee123`

### 3. Start Server

```powershell
# Windows PowerShell
$env:PYTHONPATH = (Get-Location).Path
uvicorn backend.main:app --reload --port 8000
```

```bash
# Linux/Mac
export PYTHONPATH=$(pwd)
uvicorn backend.main:app --reload --port 8000
```

### 4. Access API Documentation

Open your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Home**: http://localhost:8000

## 📖 Quick API Test

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    ...
  }
}
```

### Chat Query (with authentication)

```bash
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the employee handbook?"}'
```

## 🔑 Features

- ✅ JWT Authentication
- ✅ Role-Based Access Control (RBAC)
- ✅ Audit Logging
- ✅ RAG Pipeline Integration
- ✅ 6 Pre-configured User Roles
- ✅ SQLite Database
- ✅ Auto-generated API Documentation

## 📂 Project Structure

```
backend/
├── main.py                   # FastAPI app entry point
├── init_users.py            # User initialization script
├── api/
│   ├── auth.py              # Authentication endpoints
│   └── chat.py              # Chat/RAG endpoints
├── auth/
│   ├── security.py          # JWT & password utilities
│   └── dependencies.py      # Auth dependencies
├── database/
│   ├── database.py          # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── middleware/
│   ├── rbac_middleware.py   # RBAC enforcement
│   └── audit_middleware.py  # Audit logging
└── tests/
    └── test_auth_rbac.py    # Test suite
```

## 🎯 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Test Authentication**: Try logging in with different user roles
3. **Query RAG**: Test the chat endpoint with various queries
4. **Check Audit Logs**: View `backend/chatbot.db` audit_logs table
5. **Review Code**: Check the well-documented source files

## 🛠️ Troubleshooting

**Module Not Found Error:**
```bash
# Ensure PYTHONPATH is set
$env:PYTHONPATH = (Get-Location).Path  # Windows
export PYTHONPATH=$(pwd)                # Linux/Mac
```

**Database Issues:**
```bash
# Reset database
rm backend/chatbot.db
python -m backend.init_users
```

**Port Already in Use:**
```bash
# Use different port
uvicorn backend.main:app --reload --port 8001
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- Architecture diagram
- All API endpoints
- RBAC roles and permissions
- Security features
- Production deployment guide
