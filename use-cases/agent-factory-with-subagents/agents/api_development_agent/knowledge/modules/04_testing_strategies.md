# Module 04: Testing Strategies

## Comprehensive API Testing Patterns

Этот модуль содержит паттерны для тестирования API: unit tests, integration tests, end-to-end tests, и security tests.

---

## Unit Testing with Pytest

### FastAPI Test Setup

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user():
    """Test user data."""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "TestPass123!"
    }
```

### Comprehensive Test Examples

```python
class TestUserAPI:
    """Test user-related API endpoints."""

    def test_create_user_success(self, client, test_user):
        """Test successful user creation."""
        response = client.post("/users/", json=test_user)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["full_name"] == test_user["full_name"]
        assert "password" not in data  # Password should not be returned
        assert "id" in data

    def test_create_user_invalid_email(self, client, test_user):
        """Test user creation with invalid email."""
        invalid_data = test_user.copy()
        invalid_data["email"] = "invalid-email"

        response = client.post("/users/", json=invalid_data)

        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["loc"]

    def test_create_user_weak_password(self, client, test_user):
        """Test user creation with weak password."""
        weak_data = test_user.copy()
        weak_data["password"] = "weak"

        response = client.post("/users/", json=weak_data)

        assert response.status_code == 422

    def test_create_user_duplicate_email(self, client, test_user):
        """Test duplicate user creation."""
        # Create first user
        client.post("/users/", json=test_user)

        # Try to create duplicate
        response = client.post("/users/", json=test_user)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_get_user_unauthorized(self, client):
        """Test getting user without authentication."""
        response = client.get("/users/1")

        assert response.status_code == 401

    def test_get_user_with_auth(self, client, test_user):
        """Test getting user with valid token."""
        # Create user
        create_response = client.post("/users/", json=test_user)
        user_id = create_response.json()["id"]

        # Login to get token
        login_response = client.post("/token", data={
            "username": test_user["email"],
            "password": test_user["password"]
        })
        token = login_response.json()["access_token"]

        # Get user with token
        response = client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["email"] == test_user["email"]
```

---

## Integration Testing

### Testing with Mocks

```python
from unittest.mock import patch, MagicMock
import pytest

@pytest.fixture
def mock_email_service():
    """Mock email service."""
    with patch('app.services.email.send_email') as mock:
        yield mock

class TestUserIntegration:
    """Integration tests with external services mocked."""

    def test_create_user_sends_welcome_email(self, client, test_user, mock_email_service):
        """Test that user creation triggers welcome email."""
        response = client.post("/users/", json=test_user)

        assert response.status_code == 201
        mock_email_service.assert_called_once()

        # Verify email parameters
        call_args = mock_email_service.call_args
        assert call_args[0][0] == test_user["email"]
        assert "Welcome" in call_args[0][1]  # Subject
        assert test_user["full_name"] in call_args[0][2]  # Body

    @patch('app.services.payment.process_payment')
    def test_payment_integration(self, mock_payment, client):
        """Test payment processing integration."""
        mock_payment.return_value = {"status": "success", "transaction_id": "txn_123"}

        payment_data = {
            "amount": 99.99,
            "currency": "USD",
            "card_token": "tok_test"
        }

        response = client.post("/payments/", json=payment_data)

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_payment.assert_called_once()
```

---

## Rate Limiting Tests

### Testing Rate Limits

```python
class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_rate_limit_enforcement(self, client, test_user):
        """Test that rate limiting is enforced."""
        # Exceed rate limit (100 requests per hour)
        for i in range(101):
            response = client.post("/users/", json=test_user)

        # Last request should be rate limited
        assert response.status_code == 429
        assert "Too many requests" in response.json()["detail"]

    def test_rate_limit_headers(self, client):
        """Test rate limit headers are present."""
        response = client.get("/health")

        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers

    def test_rate_limit_reset_after_window(self, client, test_user):
        """Test rate limit resets after time window."""
        import time

        # Hit rate limit
        for i in range(100):
            client.post("/users/", json=test_user)

        # Wait for window to reset (in real tests, use time mocking)
        time.sleep(3601)  # 1 hour + 1 second

        # Should be able to make requests again
        response = client.post("/users/", json=test_user)
        assert response.status_code != 429
```

---

## Security Testing

### Authentication Tests

```python
class TestAuthentication:
    """Test authentication and authorization."""

    def test_invalid_token(self, client):
        """Test request with invalid token."""
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    def test_expired_token(self, client, test_user):
        """Test request with expired token."""
        # Create expired token
        import jwt
        from datetime import datetime, timedelta

        expired_token = jwt.encode(
            {"sub": 1, "exp": datetime.utcnow() - timedelta(hours=1)},
            "secret",
            algorithm="HS256"
        )

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )

        assert response.status_code == 401

    def test_sql_injection_protection(self, client):
        """Test SQL injection protection."""
        # Try SQL injection in query parameter
        response = client.get("/users?email=admin' OR '1'='1")

        # Should not return unauthorized data
        assert response.status_code in [400, 404]

    def test_xss_protection(self, client):
        """Test XSS protection."""
        xss_payload = {
            "email": "test@example.com",
            "full_name": "<script>alert('XSS')</script>",
            "password": "TestPass123!"
        }

        response = client.post("/users/", json=xss_payload)

        # Should sanitize or reject
        if response.status_code == 201:
            data = response.json()
            assert "<script>" not in data["full_name"]
```

---

## End-to-End Testing

### Complete User Flow Test

```python
class TestUserFlowE2E:
    """End-to-end tests for complete user flows."""

    def test_complete_user_lifecycle(self, client):
        """Test complete user lifecycle: register → login → update → delete."""

        # 1. Register new user
        user_data = {
            "email": "e2e@example.com",
            "full_name": "E2E Test User",
            "password": "E2EPass123!"
        }

        register_response = client.post("/users/", json=user_data)
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]

        # 2. Login
        login_response = client.post("/token", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Get user profile
        profile_response = client.get("/users/me", headers=headers)
        assert profile_response.status_code == 200
        assert profile_response.json()["email"] == user_data["email"]

        # 4. Update profile
        update_data = {"full_name": "Updated Name"}
        update_response = client.patch(
            f"/users/{user_id}",
            json=update_data,
            headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["full_name"] == "Updated Name"

        # 5. Delete account
        delete_response = client.delete(f"/users/{user_id}", headers=headers)
        assert delete_response.status_code == 204

        # 6. Verify deletion
        get_response = client.get(f"/users/{user_id}", headers=headers)
        assert get_response.status_code == 404
```

---

## Performance Testing

### Load Testing Pattern

```python
import asyncio
import aiohttp
import time

async def make_request(session, url):
    """Make single async request."""
    async with session.get(url) as response:
        return await response.json()

async def load_test(url, num_requests):
    """Run load test with concurrent requests."""
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, url) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Completed {num_requests} requests in {duration:.2f} seconds")
    print(f"Requests per second: {num_requests / duration:.2f}")

    return responses

# Run load test
asyncio.run(load_test("http://localhost:8000/health", 1000))
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
