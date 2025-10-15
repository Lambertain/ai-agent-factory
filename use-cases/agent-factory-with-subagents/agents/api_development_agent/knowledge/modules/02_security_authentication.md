# Module 02: Security & Authentication

## Паттерны безопасности и аутентификации для API

Этот модуль содержит проверенные паттерны для защиты API: JWT аутентификацию, rate limiting, и другие best practices безопасности.

---

## JWT Authentication

### Universal JWT Implementation

```python
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any

SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create JWT access token.

    Args:
        data: Payload data to encode
        expires_delta: Optional token expiry time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(user_id: int) -> str:
    """Create long-lived refresh token."""
    data = {
        "sub": user_id,
        "type": "refresh"
    }
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload

    Raises:
        Exception: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def refresh_access_token(refresh_token: str) -> str:
    """
    Generate new access token from refresh token.

    Args:
        refresh_token: Valid refresh token

    Returns:
        New access token
    """
    payload = verify_token(refresh_token)

    if payload.get("type") != "refresh":
        raise Exception("Invalid token type")

    user_id = payload.get("sub")
    new_access_token = create_access_token({"sub": user_id})

    return new_access_token
```

### Token-Based Authentication Flow

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint - returns access and refresh tokens.
    """
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.id, "email": user.email})
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/token/refresh")
async def refresh(refresh_token: str):
    """Refresh access token using refresh token."""
    try:
        new_access_token = refresh_access_token(refresh_token)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Protected route - requires valid access token."""
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        user = get_user_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

---

## Rate Limiting Patterns

### Redis-Based Rate Limiting

```python
import redis
from datetime import datetime, timedelta
from typing import Optional

class RateLimiter:
    """
    Redis-based rate limiter using sliding window algorithm.
    """

    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int = 100,
        window_seconds: int = 3600
    ):
        """
        Initialize rate limiter.

        Args:
            redis_client: Redis connection
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds (default: 1 hour)
        """
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, key: str) -> bool:
        """
        Check if request is allowed under rate limit.

        Args:
            key: Unique identifier (e.g., user_id or IP address)

        Returns:
            True if request is allowed, False otherwise
        """
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=self.window_seconds)

        # Remove old entries outside the window
        self.redis.zremrangebyscore(key, 0, window_start.timestamp())

        # Count current requests in window
        current_requests = self.redis.zcard(key)

        if current_requests >= self.max_requests:
            return False

        # Add current request
        self.redis.zadd(key, {str(current_time.timestamp()): current_time.timestamp()})
        self.redis.expire(key, self.window_seconds)

        return True

    def get_remaining_requests(self, key: str) -> int:
        """Get number of remaining allowed requests."""
        current_requests = self.redis.zcard(key)
        return max(0, self.max_requests - current_requests)

    def get_reset_time(self, key: str) -> Optional[datetime]:
        """Get time when rate limit will reset."""
        oldest_request = self.redis.zrange(key, 0, 0, withscores=True)

        if not oldest_request:
            return None

        oldest_timestamp = oldest_request[0][1]
        reset_time = datetime.fromtimestamp(oldest_timestamp) + timedelta(seconds=self.window_seconds)

        return reset_time
```

### FastAPI Rate Limiting Middleware

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
rate_limiter = RateLimiter(redis_client, max_requests=100, window_seconds=3600)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки rate limits."""

    async def dispatch(self, request: Request, call_next):
        # Extract identifier (user ID or IP address)
        client_id = request.client.host

        if hasattr(request.state, "user"):
            client_id = f"user:{request.state.user.id}"
        else:
            client_id = f"ip:{request.client.host}"

        # Check rate limit
        if not rate_limiter.is_allowed(client_id):
            reset_time = rate_limiter.get_reset_time(client_id)
            raise HTTPException(
                status_code=429,
                detail="Too many requests",
                headers={
                    "Retry-After": str(reset_time),
                    "X-RateLimit-Limit": str(rate_limiter.max_requests),
                    "X-RateLimit-Remaining": "0"
                }
            )

        response = await call_next(request)

        # Add rate limit headers
        remaining = rate_limiter.get_remaining_requests(client_id)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

app.add_middleware(RateLimitMiddleware)
```

---

## CORS Configuration

### Secure CORS Setup

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# Production CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

### Development CORS Configuration

```python
# Development only - permissive CORS
if os.getenv("ENV") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

---

## Input Validation & Sanitization

### Pydantic Validators

```python
from pydantic import BaseModel, validator, Field
import re

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: str
    password: str = Field(..., min_length=8)

    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    @validator('email')
    def validate_email(cls, v):
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
