# Api Development Agent - Knowledge Base

## 📚 Общие правила для всех агентов

**ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:** Прочитай [Общие правила агентов](../_shared/agent_common_rules.md)

Все агенты следуют единым правилам workflow, качества и взаимодействия. Общие правила содержат:
- ✅ Переключение в роль (обязательно)
- ✅ Workflow и приоритизация
- ✅ Управление задачами (Archon + TodoWrite)
- ✅ Git интеграция и стандарты кодирования
- ✅ Post-Task Checklist (последний пункт каждой задачи)
- ✅ Протоколы анализа проблем и эскалации
- ✅ Заборона ярликів та токен-економії

---

## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: Api Development Agent

**Ты - Api Development Agent**, эксперт в [ОБЛАСТЬ ЭКСПЕРТИЗЫ].

### ⚠️ ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:
**ПРОЧИТАЙ:** [`agent_common_rules.md`](../_shared/agent_common_rules.md) - содержит критически важные правила workflow, качества и эскалации.

## Системный промпт для API Development Agent

```
Ты специализированный агент по разработке API с экспертизой в современных фреймворках и best practices.

**Твоя экспертиза:**
- REST и GraphQL API дизайн и архитектура
- Множественные фреймворки: Express.js, NestJS, FastAPI, Django REST, ASP.NET Core, Spring Boot
- Authentication и authorization паттерны (JWT, OAuth2, Basic, API Keys)
- Performance optimization и caching стратегии
- API security best practices и compliance requirements
- Documentation generation (OpenAPI/Swagger, Postman)
- Testing strategies (unit, integration, e2e, security tests)
- Deployment и containerization для production

**Ключевые области экспертизы:**

1. **Framework-Agnostic API Design:**
   - RESTful принципы и resource-based URLs
   - HTTP methods и status codes
   - API versioning стратегии
   - Error handling best practices
   - Request/response optimization

2. **Universal Security Patterns:**
   - Authentication strategies для всех фреймворков
   - Authorization и RBAC implementation
   - Input validation и sanitization
   - Rate limiting и DDoS protection
   - CORS configuration

3. **Performance Optimization:**
   - Caching strategies (Redis, Memory, CDN)
   - Database query optimization
   - Response compression
   - Load balancing patterns
   - Monitoring и metrics

4. **Domain-Specific Optimizations:**
   - E-commerce: product catalogs, shopping carts, payments
   - Fintech: compliance, fraud detection, audit trails
   - Healthcare: HIPAA compliance, HL7 FHIR, PHI protection
   - Social Media: real-time features, content moderation, scalability
   - Enterprise: SSO, RBAC, audit logging, compliance

**Принципы работы:**
1. Всегда следуй framework-specific best practices
2. Применяй security-first подход
3. Оптимизируй для производительности и масштабируемости
4. Предоставляй полный, production-ready код
5. Включай comprehensive testing
6. Генерируй documentation
7. Следуй принципам clean code и SOLID
```

## Framework-Specific Patterns

### Express.js Best Practices

#### Middleware Architecture
```javascript
// Security middleware stack
app.use(helmet()); // Security headers
app.use(cors(corsOptions)); // CORS configuration
app.use(compression()); // Response compression
app.use(morgan('combined')); // Request logging
app.use(rateLimit(rateLimitOptions)); // Rate limiting
app.use(express.json({ limit: '10mb' })); // Body parsing
app.use(express.urlencoded({ extended: true }));

// Authentication middleware
const authenticateJWT = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (authHeader) {
    const token = authHeader.split(' ')[1];
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
      if (err) return res.sendStatus(403);
      req.user = user;
      next();
    });
  } else {
    res.sendStatus(401);
  }
};
```

#### Error Handling
```javascript
// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);

  // Default error response
  let error = {
    message: 'Internal Server Error',
    status: 500
  };

  // Handle specific error types
  if (err.name === 'ValidationError') {
    error.message = err.message;
    error.status = 400;
  } else if (err.name === 'UnauthorizedError') {
    error.message = 'Unauthorized';
    error.status = 401;
  }

  res.status(error.status).json({ error: error.message });
});
```

### NestJS Architecture Patterns

#### Dependency Injection
```typescript
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private readonly jwtService: JwtService,
  ) {}

  async createUser(createUserDto: CreateUserDto): Promise<User> {
    const user = this.userRepository.create(createUserDto);
    return this.userRepository.save(user);
  }
}

@Controller('users')
@UseGuards(JwtAuthGuard)
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  @UsePipes(new ValidationPipe())
  async create(@Body() createUserDto: CreateUserDto) {
    return this.userService.createUser(createUserDto);
  }
}
```

#### Guards and Interceptors
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const method = request.method;
    const url = request.url;

    console.log(`${method} ${url}`);

    return next.handle().pipe(
      tap(() => console.log(`${method} ${url} - Completed`)),
    );
  }
}
```

### FastAPI Patterns

#### Pydantic Models and Validation
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

#### Dependency Injection
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/users/", response_model=User)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await user_service.create_user(db, user)
```

## Security Patterns

### JWT Authentication
```python
# Universal JWT implementation
import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
```

### Rate Limiting Patterns
```python
# Redis-based rate limiting
import redis
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, redis_client, max_requests=100, window_seconds=3600):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, key: str) -> bool:
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=self.window_seconds)

        # Remove old entries
        self.redis.zremrangebyscore(key, 0, window_start.timestamp())

        # Count current requests
        current_requests = self.redis.zcard(key)

        if current_requests >= self.max_requests:
            return False

        # Add current request
        self.redis.zadd(key, {str(current_time.timestamp()): current_time.timestamp()})
        self.redis.expire(key, self.window_seconds)

        return True
```

## Performance Optimization

### Caching Strategies
```python
# Multi-level caching
import redis
from functools import wraps

def cache_result(expiry=3600, cache_key_prefix="api"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{cache_key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            redis_client.setex(
                cache_key,
                expiry,
                json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator

@cache_result(expiry=1800)
async def get_user_profile(user_id: int):
    # Expensive database operation
    return await db.fetch_user_with_details(user_id)
```

### Database Query Optimization
```python
# Efficient database patterns
from sqlalchemy.orm import selectinload, joinedload

# Eager loading to prevent N+1 queries
def get_users_with_posts():
    return session.query(User).options(
        selectinload(User.posts).selectinload(Post.comments)
    ).all()

# Pagination with cursor-based approach
def paginate_posts(cursor=None, limit=20):
    query = session.query(Post).order_by(Post.created_at.desc())

    if cursor:
        query = query.filter(Post.created_at < cursor)

    posts = query.limit(limit + 1).all()

    has_next = len(posts) > limit
    if has_next:
        posts = posts[:-1]

    next_cursor = posts[-1].created_at if posts and has_next else None

    return {
        "data": posts,
        "pagination": {
            "next_cursor": next_cursor,
            "has_next": has_next
        }
    }
```

## Testing Patterns

### API Testing Strategies
```python
# Comprehensive test patterns
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

class TestUserAPI:
    def setup_method(self):
        self.client = TestClient(app)
        self.test_user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "TestPass123"
        }

    def test_create_user_success(self):
        response = self.client.post("/users/", json=self.test_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == self.test_user_data["email"]
        assert "password" not in data

    def test_create_user_invalid_email(self):
        invalid_data = self.test_user_data.copy()
        invalid_data["email"] = "invalid-email"

        response = self.client.post("/users/", json=invalid_data)
        assert response.status_code == 422

    def test_create_user_weak_password(self):
        weak_data = self.test_user_data.copy()
        weak_data["password"] = "weak"

        response = self.client.post("/users/", json=weak_data)
        assert response.status_code == 422

    @patch('user_service.send_welcome_email')
    def test_create_user_email_integration(self, mock_email):
        response = self.client.post("/users/", json=self.test_user_data)
        assert response.status_code == 201
        mock_email.assert_called_once()

    def test_get_user_unauthorized(self):
        response = self.client.get("/users/1")
        assert response.status_code == 401

    def test_rate_limiting(self):
        # Test rate limiting
        for i in range(101):  # Exceed rate limit
            response = self.client.post("/users/", json=self.test_user_data)

        assert response.status_code == 429
```

## Domain-Specific Patterns

### E-commerce API Patterns
```python
# Shopping cart management
class ShoppingCartService:
    def __init__(self, redis_client, db_session):
        self.redis = redis_client
        self.db = db_session

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int):
        # Validate product availability
        product = await self.db.get_product(product_id)
        if not product or product.stock < quantity:
            raise HTTPException(400, "Product not available")

        # Update cart in Redis
        cart_key = f"cart:{user_id}"
        cart_item = {
            "product_id": product_id,
            "quantity": quantity,
            "price": float(product.price),
            "added_at": datetime.utcnow().isoformat()
        }

        self.redis.hset(cart_key, product_id, json.dumps(cart_item))
        self.redis.expire(cart_key, 3600 * 24)  # 24 hours

        return {"success": True, "cart_total": await self.get_cart_total(user_id)}

    async def calculate_total(self, user_id: int, tax_rate=0.08, shipping=0):
        cart_items = await self.get_cart_items(user_id)
        subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
        tax = subtotal * tax_rate
        total = subtotal + tax + shipping

        return {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "total": total
        }
```

### Fintech Security Patterns
```python
# PCI DSS compliant payment processing
class PaymentProcessor:
    def __init__(self, encryption_service):
        self.encryption = encryption_service

    async def process_payment(self, payment_data):
        # Validate and sanitize input
        validated_data = self.validate_payment_data(payment_data)

        # Encrypt sensitive data
        encrypted_card = self.encryption.encrypt_card_data(
            validated_data["card_number"]
        )

        # Create audit trail
        audit_entry = {
            "transaction_id": str(uuid.uuid4()),
            "user_id": validated_data["user_id"],
            "amount": validated_data["amount"],
            "timestamp": datetime.utcnow(),
            "ip_address": self.get_client_ip(),
            "encrypted_card_last4": encrypted_card[-4:]
        }

        await self.create_audit_log(audit_entry)

        # Process with payment gateway
        try:
            result = await self.payment_gateway.charge(
                amount=validated_data["amount"],
                card_token=encrypted_card,
                metadata=audit_entry
            )

            return result
        except PaymentException as e:
            await self.log_payment_failure(audit_entry, str(e))
            raise
```

### Healthcare HIPAA Compliance
```python
# HIPAA-compliant patient data handling
class PatientDataService:
    def __init__(self, encryption_service, audit_service):
        self.encryption = encryption_service
        self.audit = audit_service

    async def get_patient_record(self, patient_id: int, requesting_user: User):
        # Check authorization
        if not self.can_access_patient_data(requesting_user, patient_id):
            await self.audit.log_unauthorized_access(requesting_user.id, patient_id)
            raise HTTPException(403, "Access denied")

        # Log authorized access
        await self.audit.log_phi_access(
            user_id=requesting_user.id,
            patient_id=patient_id,
            access_type="read",
            timestamp=datetime.utcnow()
        )

        # Retrieve and decrypt PHI
        encrypted_record = await self.db.get_patient_record(patient_id)
        decrypted_record = self.encryption.decrypt_phi(encrypted_record)

        # Apply minimum necessary principle
        filtered_record = self.filter_phi_by_role(
            decrypted_record,
            requesting_user.role
        )

        return filtered_record

    def can_access_patient_data(self, user: User, patient_id: int) -> bool:
        # Check role-based access
        if user.role in ["doctor", "nurse"]:
            # Check if user is assigned to patient
            return self.db.check_patient_assignment(user.id, patient_id)
        elif user.role == "admin":
            return True
        else:
            return False
```

## Deployment and DevOps

### Docker Configuration
```dockerfile
# Multi-stage production build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS runtime
WORKDIR /app

# Security: Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --chown=nextjs:nodejs . .

# Security hardening
RUN apk add --no-cache dumb-init
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
```

### Kubernetes Configuration
```yaml
# Production-ready Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: api:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## API Documentation Standards

### OpenAPI 3.0 Best Practices
```yaml
openapi: 3.0.3
info:
  title: Universal API
  description: |
    Comprehensive API for [domain] applications.

    ## Authentication
    This API uses JWT Bearer token authentication.

    ## Rate Limiting
    Requests are limited to 1000 per hour per user.

  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      required:
        - id
        - email
        - full_name
      properties:
        id:
          type: integer
          example: 1
        email:
          type: string
          format: email
          example: "user@example.com"
        full_name:
          type: string
          example: "John Doe"
        created_at:
          type: string
          format: date-time

    Error:
      type: object
      required:
        - message
      properties:
        message:
          type: string
          example: "Invalid request"
        code:
          type: string
          example: "VALIDATION_ERROR"
        details:
          type: object

paths:
  /users:
    get:
      summary: List users
      description: Retrieve a paginated list of users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    type: object
                    properties:
                      page:
                        type: integer
                      limit:
                        type: integer
                      total:
                        type: integer
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

## Performance Monitoring

### Metrics Collection
```python
# Prometheus metrics integration
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

def monitor_performance(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.url.path

        try:
            response = await func(request, *args, **kwargs)
            status = response.status_code
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=500).inc()
            raise
        finally:
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)

    return wrapper

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

This knowledge base provides comprehensive patterns and best practices for universal API development across multiple frameworks and domains.

---

## 🔍 ДОМЕННЫЕ ЗНАНИЯ: [ОБЛАСТЬ]

```javascript
```javascript
```typescript
```typescript
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python

---

**Версия:** 2.0 (Модульная архитектура)
**Дата рефакторинга:** 2025-10-14
**Автор рефакторинга:** Archon Blueprint Architect
