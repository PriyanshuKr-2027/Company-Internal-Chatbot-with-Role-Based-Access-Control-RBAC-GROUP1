# Backend API - Module 5 Documentation

## Overview

FastAPI backend with JWT authentication, role-based access control (RBAC), and integrated RAG pipeline for secure chatbot queries.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌──────────────┐                   │
│  │  Auth API   │    │   Chat API   │                   │
│  └─────────────┘    └──────────────┘                   │
│         │                    │                          │
│         ├────────────────────┤                          │
│         │                                               │
│  ┌──────────────────────────────┐                       │
│  │   RBAC Middleware            │                       │
│  └──────────────────────────────┘                       │
│         │                                               │
│  ┌──────────────────────────────┐                       │
│  │   Audit Middleware           │                       │
│  └──────────────────────────────┘                       │
│         │                                               │
│  ┌──────────────────────────────┐                       │
│  │   Database (SQLite)          │                       │
│  │   - Users                    │                       │
│  │   - Audit Logs               │                       │
│  └──────────────────────────────┘                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── init_users.py             # Sample user creation script
├── api/
│   ├── auth.py               # Authentication endpoints
│   └── chat.py               # Chat/RAG endpoints
├── auth/
│   ├── security.py           # JWT & password utilities
│   └── dependencies.py       # Auth dependencies
├── database/
│   ├── database.py           # SQLAlchemy models & DB config
│   └── schemas.py            # Pydantic schemas
├── middleware/
│   ├── rbac_middleware.py    # Role-based access control
│   └── audit_middleware.py   # Request audit logging
└── tests/
    └── test_auth_rbac.py     # Test suite
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create/update `.env` file:

```env
# OpenRouter API (already configured)
OPENROUTER_API_KEY=your-api-key-here

# JWT Secret (for production, use strong random key)
SECRET_KEY=your-secret-key-change-in-production

# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///./backend/chatbot.db
```

### 3. Initialize Database & Users

```bash
python backend/init_users.py
```

This creates 6 sample users:
- `admin` / `admin123` (admin role)
- `john_finance` / `finance123` (finance role)
- `jane_marketing` / `marketing123` (marketing role)
- `bob_engineering` / `engineering123` (engineering role)
- `alice_hr` / `hr123` (hr role)
- `employee` / `employee123` (employee role)

### 4. Start Server

```bash
# Development
uvicorn backend.main:app --reload --port 8000

# Production
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

#### POST `/api/auth/login`
Login with username and password

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@company.com",
    "full_name": "Admin User",
    "role": "admin",
    "department": "IT",
    "is_active": true,
    "created_at": "2026-01-15T10:00:00",
    "last_login": "2026-01-15T10:00:00"
  }
}
```

#### POST `/api/auth/logout`
Logout (requires authentication)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

#### GET `/api/auth/me`
Get current user information

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@company.com",
  "full_name": "Admin User",
  "role": "admin",
  "department": "IT",
  "is_active": true,
  "created_at": "2026-01-15T10:00:00",
  "last_login": "2026-01-15T10:00:00"
}
```

#### POST `/api/auth/refresh`
Refresh access token

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Chat (RAG Pipeline)

#### POST `/api/chat/query`
Submit query to RAG pipeline (requires authentication)

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "query": "What were the Q4 2024 financial results?",
  "n_results": 5,
  "include_citations": true
}
```

**Response:**
```json
{
  "answer": "The financial results for Q4 2024 show...",
  "sources": [
    {
      "rank": 1,
      "source": "quarterly_financial_report.md",
      "section": "Executive Summary",
      "relevance_score": 0.852,
      "relevance_percent": "85.2%",
      "quality": "Highly Relevant"
    }
  ],
  "confidence": {
    "score": 0.823,
    "level": "HIGH",
    "reasoning": "Multiple highly relevant documents found"
  },
  "metadata": {
    "query": "What were the Q4 2024 financial results?",
    "role": "finance",
    "num_results": 5,
    "query_type": "factual"
  }
}
```

#### GET `/api/chat/history`
Get user's chat history (requires authentication)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional, default: 20): Max records to return

**Response:**
```json
[
  {
    "id": 1,
    "query": "What were the Q4 2024 financial results?",
    "timestamp": "2026-01-15T10:30:00"
  }
]
```

## Role-Based Access Control (RBAC)

### Roles

| Role | Access |
|------|--------|
| **admin** | All documents and endpoints |
| **finance** | Finance department documents |
| **engineering** | Engineering department documents |
| **marketing** | Marketing department documents |
| **hr** | HR department documents |
| **employee** | General/public documents only |

### RBAC Enforcement

1. **Middleware Level**: `RBACMiddleware` checks token and role for all protected endpoints
2. **Dependency Level**: Route-specific dependencies like `require_admin`, `require_finance`
3. **RAG Pipeline Level**: Document filtering based on user role

### Example Usage

```python
from backend.auth.dependencies import require_admin, require_finance

@router.get("/admin/users", dependencies=[Depends(require_admin)])
async def get_users():
    # Only admin role can access
    pass

@router.get("/finance/reports", dependencies=[Depends(require_finance)])
async def get_reports():
    # Admin and finance roles can access
    pass
```

## Audit Logging

All API requests are logged to the database with:
- User identity (if authenticated)
- Endpoint accessed
- HTTP method
- Response status code
- IP address
- User agent
- Timestamp
- Response time

### Audit Log Model

```python
{
  "id": 1,
  "user_id": 1,
  "username": "admin",
  "action": "chat_query",
  "endpoint": "/api/chat/query",
  "method": "POST",
  "status_code": 200,
  "ip_address": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  "details": "Query: What were... | Confidence: HIGH",
  "timestamp": "2026-01-15T10:30:00"
}
```

## Testing

### Run Tests

```bash
# Run all tests
pytest backend/tests/ -v

# Run specific test class
pytest backend/tests/test_auth_rbac.py::TestAuthentication -v

# Run with coverage
pytest backend/tests/ --cov=backend --cov-report=html
```

### Test Coverage

- ✅ Authentication (login, logout, token refresh)
- ✅ RBAC enforcement
- ✅ Protected endpoint access
- ✅ Invalid credentials handling
- ✅ Token validation
- ✅ Chat query with different roles
- ✅ Audit logging

## Security Features

### 1. Password Security
- **Bcrypt hashing** with salt
- Passwords never stored in plain text
- Configurable hashing rounds

### 2. JWT Tokens
- **HS256 algorithm** (configurable)
- 1-hour expiration (configurable)
- Token refresh mechanism
- Secure token validation

### 3. RBAC
- Role-based endpoint protection
- Middleware-level enforcement
- Fine-grained permission control

### 4. Audit Trail
- Complete request logging
- User action tracking
- Security event monitoring

## Production Considerations

### 1. Environment Variables

```env
# Strong random secret key (use: openssl rand -hex 32)
SECRET_KEY=<generate-strong-random-key>

# PostgreSQL for production
DATABASE_URL=postgresql://user:password@localhost/chatbot

# CORS origins
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Database

For production, use PostgreSQL:

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/chatbot
```

### 3. HTTPS

Always use HTTPS in production:

```bash
# With SSL certificate
uvicorn backend.main:app --host 0.0.0.0 --port 443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### 4. Rate Limiting

Add rate limiting middleware (recommended):

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Module 5 Deliverables

✅ **FastAPI Backend Application** - Complete REST API with middleware support  
✅ **User Authentication & JWT** - Secure authentication with token management  
✅ **RBAC Middleware** - Role-based access control enforcement  
✅ **User Database** - SQLite with 6 sample accounts  
✅ **Audit Logging** - Comprehensive request and action logging  
✅ **Test Cases** - Authentication and authorization test suite  

**Status**: ✅ **COMPLETE - PRODUCTION READY**
