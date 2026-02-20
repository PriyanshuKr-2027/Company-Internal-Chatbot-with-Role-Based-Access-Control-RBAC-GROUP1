# API Usage Examples

## Authentication Examples

### 1. Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
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
    "last_login": "2026-01-15T10:30:00"
  }
}
```

### 2. Get Current User Info

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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
  "last_login": "2026-01-15T10:30:00"
}
```

### 3. Refresh Token

```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 4. Logout

```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

---

## Chat Examples

### 1. Submit Query

```bash
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What were the Q4 2024 financial results?",
    "n_results": 5,
    "include_citations": true
  }'
```

**Response:**
```json
{
  "answer": "The financial results for Q4 2024 show significant growth across all divisions...",
  "sources": [
    {
      "rank": 1,
      "source": "quarterly_financial_report.md",
      "section": "Executive Summary",
      "relevance_score": 0.852,
      "relevance_percent": "85.2%",
      "quality": "Highly Relevant"
    },
    {
      "rank": 2,
      "source": "financial_summary.md",
      "section": "Q4 Performance",
      "relevance_score": 0.789,
      "relevance_percent": "78.9%",
      "quality": "Highly Relevant"
    }
  ],
  "confidence": {
    "score": 0.823,
    "level": "HIGH",
    "reasoning": "Multiple highly relevant documents found with consistent information"
  },
  "metadata": {
    "query": "What were the Q4 2024 financial results?",
    "role": "finance",
    "num_results": 5,
    "query_type": "factual"
  }
}
```

### 2. Get Chat History

```bash
curl -X GET "http://localhost:8000/api/chat/history?limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 15,
    "query": "What were the Q4 2024 financial results?",
    "timestamp": "2026-01-15T10:30:00"
  },
  {
    "id": 14,
    "query": "What are the company benefits?",
    "timestamp": "2026-01-15T10:25:00"
  }
]
```

---

## Python Examples

### Setup

```python
import requests

BASE_URL = "http://localhost:8000"
```

### Login

```python
def login(username: str, password: str):
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": password}
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"], data["user"]

# Usage
token, user = login("admin", "admin123")
print(f"Logged in as {user['username']} ({user['role']})")
print(f"Token: {token[:50]}...")
```

### Submit Query

```python
def query_chatbot(token: str, query: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/chat/query",
        headers=headers,
        json={"query": query}
    )
    response.raise_for_status()
    return response.json()

# Usage
token, _ = login("john_finance", "finance123")
result = query_chatbot(token, "What were the Q4 2024 financial results?")

print(f"\nAnswer: {result['answer']}")
print(f"\nConfidence: {result['confidence']['level']} ({result['confidence']['score']:.2%})")
print(f"\nSources:")
for source in result['sources']:
    print(f"  - {source['source']} ({source['relevance_percent']})")
```

### Get User Info

```python
def get_user_info(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/auth/me",
        headers=headers
    )
    response.raise_for_status()
    return response.json()

# Usage
token, _ = login("admin", "admin123")
user_info = get_user_info(token)
print(f"Username: {user_info['username']}")
print(f"Role: {user_info['role']}")
print(f"Department: {user_info['department']}")
```

### Complete Workflow

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "jane_marketing", "password": "marketing123"}
)
login_data = login_response.json()
token = login_data["access_token"]
user = login_data["user"]

print(f"✅ Logged in as {user['username']} ({user['role']})")

# 2. Query chatbot
headers = {"Authorization": f"Bearer {token}"}
query_response = requests.post(
    f"{BASE_URL}/api/chat/query",
    headers=headers,
    json={
        "query": "What were the marketing campaigns in Q4 2024?",
        "n_results": 3
    }
)
query_data = query_response.json()

print(f"\n📝 Query: {query_data['metadata']['query']}")
print(f"🤖 Answer: {query_data['answer'][:200]}...")
print(f"📊 Confidence: {query_data['confidence']['level']}")

# 3. Get chat history
history_response = requests.get(
    f"{BASE_URL}/api/chat/history?limit=5",
    headers=headers
)
history = history_response.json()

print(f"\n📚 Recent queries:")
for item in history[:3]:
    print(f"  - {item['query']}")

# 4. Refresh token
refresh_response = requests.post(
    f"{BASE_URL}/api/auth/refresh",
    headers=headers
)
new_token = refresh_response.json()["access_token"]

print(f"\n🔄 Token refreshed")

# 5. Logout
logout_response = requests.post(
    f"{BASE_URL}/api/auth/logout",
    headers=headers
)

print(f"✅ {logout_response.json()['message']}")
```

---

## JavaScript/TypeScript Examples

### Setup

```typescript
const BASE_URL = 'http://localhost:8000';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: string;
  department: string;
  is_active: boolean;
  created_at: string;
  last_login: string;
}

interface QueryResponse {
  answer: string;
  sources: Source[];
  confidence: Confidence;
  metadata: Metadata;
}
```

### Login

```typescript
async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  if (!response.ok) {
    throw new Error(`Login failed: ${response.statusText}`);
  }
  
  return await response.json();
}

// Usage
const { access_token, user } = await login('admin', 'admin123');
console.log(`Logged in as ${user.username} (${user.role})`);
```

### Submit Query

```typescript
async function queryChatbot(token: string, query: string): Promise<QueryResponse> {
  const response = await fetch(`${BASE_URL}/api/chat/query`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  });
  
  if (!response.ok) {
    throw new Error(`Query failed: ${response.statusText}`);
  }
  
  return await response.json();
}

// Usage
const result = await queryChatbot(access_token, 'What is the employee handbook?');
console.log('Answer:', result.answer);
console.log('Confidence:', result.confidence.level);
```

### Complete React Hook Example

```typescript
import { useState, useEffect } from 'react';

function useChatbot() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  
  const login = async (username: string, password: string) => {
    const response = await fetch(`${BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    setToken(data.access_token);
    setUser(data.user);
  };
  
  const query = async (question: string) => {
    if (!token) throw new Error('Not authenticated');
    
    const response = await fetch(`${BASE_URL}/api/chat/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: question })
    });
    
    return await response.json();
  };
  
  const logout = async () => {
    if (!token) return;
    
    await fetch(`${BASE_URL}/api/auth/logout`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    setToken(null);
    setUser(null);
  };
  
  return { user, login, query, logout, isAuthenticated: !!token };
}

// Usage in component
function ChatComponent() {
  const { user, login, query, logout, isAuthenticated } = useChatbot();
  const [answer, setAnswer] = useState('');
  
  const handleSubmit = async (question: string) => {
    const result = await query(question);
    setAnswer(result.answer);
  };
  
  if (!isAuthenticated) {
    return <LoginForm onLogin={login} />;
  }
  
  return (
    <div>
      <h1>Welcome, {user?.full_name}</h1>
      <ChatInterface onSubmit={handleSubmit} answer={answer} />
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## Postman Collection

```json
{
  "info": {
    "name": "Company Chatbot API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{access_token}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    },
    {
      "key": "access_token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Login",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "var jsonData = pm.response.json();",
                  "pm.collectionVariables.set('access_token', jsonData.access_token);"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"username\": \"admin\",\n  \"password\": \"admin123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": {
              "raw": "{{base_url}}/api/auth/login",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "login"]
            }
          }
        },
        {
          "name": "Get User Info",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/auth/me",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "me"]
            }
          }
        },
        {
          "name": "Refresh Token",
          "request": {
            "method": "POST",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/auth/refresh",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "refresh"]
            }
          }
        },
        {
          "name": "Logout",
          "request": {
            "method": "POST",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/auth/logout",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "logout"]
            }
          }
        }
      ]
    },
    {
      "name": "Chat",
      "item": [
        {
          "name": "Submit Query",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"query\": \"What is the employee handbook?\",\n  \"n_results\": 5,\n  \"include_citations\": true\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": {
              "raw": "{{base_url}}/api/chat/query",
              "host": ["{{base_url}}"],
              "path": ["api", "chat", "query"]
            }
          }
        },
        {
          "name": "Get Chat History",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/chat/history?limit=20",
              "host": ["{{base_url}}"],
              "path": ["api", "chat", "history"],
              "query": [
                {
                  "key": "limit",
                  "value": "20"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

---

## Error Handling Examples

### Python

```python
import requests
from requests.exceptions import HTTPError

def safe_query(token: str, query: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BASE_URL}/api/chat/query",
            headers=headers,
            json={"query": query}
        )
        response.raise_for_status()
        return response.json()
        
    except HTTPError as e:
        if e.response.status_code == 401:
            print("Authentication failed - token expired or invalid")
        elif e.response.status_code == 403:
            print("Access denied - insufficient permissions")
        else:
            print(f"HTTP error: {e.response.status_code}")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

### TypeScript

```typescript
async function safeQuery(token: string, query: string): Promise<QueryResponse | null> {
  try {
    const response = await fetch(`${BASE_URL}/api/chat/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query })
    });
    
    if (response.status === 401) {
      console.error('Authentication failed - token expired or invalid');
      return null;
    }
    
    if (response.status === 403) {
      console.error('Access denied - insufficient permissions');
      return null;
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    
    return await response.json();
    
  } catch (error) {
    console.error('Unexpected error:', error);
    return null;
  }
}
```

---

## Rate Limiting Example (If Implemented)

```python
import time
from functools import wraps

def rate_limit(max_calls: int, period: int):
    """Rate limiter decorator"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            calls[:] = [call for call in calls if call > now - period]
            
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                print(f"Rate limit reached. Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                calls[:] = []
            
            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, period=60)  # 10 calls per minute
def query_chatbot(token: str, query: str):
    # ... implementation
    pass
```
