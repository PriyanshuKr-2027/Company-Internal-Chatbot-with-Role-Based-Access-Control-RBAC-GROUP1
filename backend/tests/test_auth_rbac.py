"""Test suite for authentication and RBAC"""

import pytest
from fastapi.testclient import TestClient as FastAPITestClient
from backend.main import app
from backend.database.database import SessionLocal, init_db, User
from backend.auth.security import get_password_hash


@pytest.fixture
def client():
    """Create test client"""
    return FastAPITestClient(app)


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == 401
    
    def test_get_current_user_info(self, client):
        """Test getting current user information"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Get user info
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "admin"
    
    def test_get_user_info_without_token(self, client):
        """Test getting user info without authentication"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # Forbidden
    
    def test_logout(self, client):
        """Test logout endpoint"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "Successfully logged out" in response.json()["message"]
    
    def test_token_refresh(self, client):
        """Test token refresh endpoint"""
        # Login first
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestRBAC:
    """Test role-based access control"""
    
    def get_token(self, client, username: str, password: str) -> str:
        """Helper to get auth token"""
        response = client.post(
            "/api/auth/login",
            json={"username": username, "password": password}
        )
        return response.json()["access_token"]
    
    def test_finance_user_access(self, client):
        """Test finance user can access chat"""
        token = self.get_token(client, "john_finance", "finance123")
        
        response = client.post(
            "/api/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "What are the financial results?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data
    
    def test_marketing_user_access(self, client):
        """Test marketing user can access chat"""
        token = self.get_token(client, "jane_marketing", "marketing123")
        
        response = client.post(
            "/api/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "What were the marketing campaigns?"}
        )
        assert response.status_code == 200
    
    def test_employee_user_access(self, client):
        """Test employee user can access chat"""
        token = self.get_token(client, "employee", "employee123")
        
        response = client.post(
            "/api/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "What are the company policies?"}
        )
        assert response.status_code == 200
    
    def test_unauthenticated_access_denied(self, client):
        """Test unauthenticated access is denied"""
        response = client.post(
            "/api/chat/query",
            json={"query": "Test query"}
        )
        assert response.status_code == 403  # Forbidden (no auth header)
    
    def test_invalid_token_access_denied(self, client):
        """Test invalid token is rejected"""
        response = client.post(
            "/api/chat/query",
            headers={"Authorization": "Bearer invalid_token"},
            json={"query": "Test query"}
        )
        assert response.status_code == 401  # Unauthorized
    
    def test_chat_history_access(self, client):
        """Test user can access their chat history"""
        token = self.get_token(client, "admin", "admin123")
        
        # Make a query first
        client.post(
            "/api/chat/query",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Test query for history"}
        )
        
        # Get history
        response = client.get(
            "/api/chat/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestAuditLogging:
    """Test audit logging functionality"""
    
    def test_login_creates_audit_log(self, client):
        """Test that login creates audit log entry"""
        # Successful login
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        
        # Check audit log was created (would need database access to verify)
        # This is a placeholder for actual database verification
    
    def test_failed_login_creates_audit_log(self, client):
        """Test that failed login creates audit log entry"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        
        # Check audit log was created
        # This is a placeholder for actual database verification


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
