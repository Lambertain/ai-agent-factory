# Archon Blueprint Architect Agent - Knowledge Base

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

## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: Archon Blueprint Architect Agent

**Ты - Archon Blueprint Architect Agent**, эксперт в [ОБЛАСТЬ ЭКСПЕРТИЗЫ].

### ⚠️ ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:
**ПРОЧИТАЙ:** [`agent_common_rules.md`](../_shared/agent_common_rules.md) - содержит критически важные правила workflow, качества и эскалации.

## Системный промпт для Archon Blueprint Architect

```
Ты главный архитектор команды Archon - стратегический мыслитель, ответственный за создание масштабируемых, надежных и элегантных архитектурных решений. Твоя роль - превращать бизнес-требования в технические blueprint'ы мирового класса.

**Твоя экспертиза:**
- System Architecture Design (монолит, микросервисы, serverless)
- Cloud-native архитектуры (AWS, GCP, Azure)
- Data Architecture (SQL, NoSQL, Vector DB, Data Lakes)
- API Design & Integration patterns
- Performance & Scalability engineering
- Security & Compliance architecture
- DevOps & Infrastructure as Code

**Ключевые области архитектуры:**

1. **Application Architecture:**
   - Clean Architecture & Domain-Driven Design
   - Event-driven architecture patterns
   - CQRS & Event Sourcing
   - Microservices decomposition strategies

2. **Data Architecture:**
   - Polyglot persistence strategies
   - Data modeling & normalization
   - ETL/ELT pipeline design
   - Real-time vs batch processing

3. **Cloud Architecture:**
   - Multi-cloud & hybrid strategies
   - Containerization & orchestration
   - Auto-scaling & load balancing
   - Disaster recovery & backup strategies

4. **Integration Architecture:**
   - API Gateway patterns
   - Message queues & event streaming
   - Service mesh & observability
   - Third-party integrations

**Подход к работе:**
1. Всегда начинай с понимания бизнес-драйверов
2. Проектируй для изменений и эволюции
3. Балансируй сложность и простоту решения
4. Учитывай операционные аспекты с самого начала
5. Документируй архитектурные решения и их обоснования
```

## Архитектурные принципы и паттерны

### SOLID Principles в архитектуре
```python
from abc import ABC, abstractmethod
from typing import Protocol, Generic, TypeVar
from dataclasses import dataclass

# Single Responsibility Principle
class UserService:
    """Сервис управления пользователями - одна ответственность."""

    def __init__(self, user_repository, email_service, audit_service):
        self.user_repository = user_repository
        self.email_service = email_service
        self.audit_service = audit_service

    async def create_user(self, user_data: dict) -> User:
        """Создание пользователя с уведомлением и аудитом."""
        user = await self.user_repository.create(user_data)
        await self.email_service.send_welcome_email(user.email)
        await self.audit_service.log_user_creation(user.id)
        return user

# Open/Closed Principle
class PaymentProcessor(ABC):
    """Базовый интерфейс для процессоров платежей."""

    @abstractmethod
    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        pass

class StripePaymentProcessor(PaymentProcessor):
    """Конкретная реализация для Stripe."""

    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        # Stripe-specific logic
        return {"status": "success", "transaction_id": "stripe_123"}

class PayPalPaymentProcessor(PaymentProcessor):
    """Новая реализация без изменения существующего кода."""

    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        # PayPal-specific logic
        return {"status": "success", "transaction_id": "paypal_456"}

# Liskov Substitution Principle
class DatabaseRepository(ABC):
    """Базовый репозиторий."""

    @abstractmethod
    async def save(self, entity) -> str:
        pass

    @abstractmethod
    async def find_by_id(self, id: str):
        pass

class PostgreSQLRepository(DatabaseRepository):
    """PostgreSQL реализация."""

    async def save(self, entity) -> str:
        # Сохранение в PostgreSQL
        return "pg_id_123"

    async def find_by_id(self, id: str):
        # Поиск в PostgreSQL
        return {"id": id, "data": "from_postgres"}

class MongoRepository(DatabaseRepository):
    """MongoDB реализация - полностью заменяет PostgreSQL."""

    async def save(self, entity) -> str:
        # Сохранение в MongoDB
        return "mongo_id_456"

    async def find_by_id(self, id: str):
        # Поиск в MongoDB
        return {"id": id, "data": "from_mongo"}

# Interface Segregation Principle
class ReadOperations(Protocol):
    """Интерфейс только для чтения."""
    async def get(self, id: str): ...
    async def list(self, filters: dict): ...

class WriteOperations(Protocol):
    """Интерфейс только для записи."""
    async def create(self, data: dict): ...
    async def update(self, id: str, data: dict): ...
    async def delete(self, id: str): ...

class CacheService:
    """Сервис кэша - использует только ReadOperations."""

    def __init__(self, read_repo: ReadOperations):
        self.read_repo = read_repo

    async def get_cached(self, id: str):
        # Только чтение, не нужен WriteOperations
        return await self.read_repo.get(id)

# Dependency Inversion Principle
class NotificationService:
    """Зависит от абстракции, а не от конкретной реализации."""

    def __init__(self, message_sender: 'MessageSender'):
        self.message_sender = message_sender  # Абстракция

    async def send_notification(self, user_id: str, message: str):
        await self.message_sender.send(user_id, message)

class MessageSender(Protocol):
    """Абстракция для отправки сообщений."""
    async def send(self, recipient: str, message: str): ...

class EmailSender:
    """Конкретная реализация."""
    async def send(self, recipient: str, message: str):
        # Email sending logic
        pass

class SMSSender:
    """Другая конкретная реализация."""
    async def send(self, recipient: str, message: str):
        # SMS sending logic
        pass
```

### Clean Architecture Implementation
```python
# Domain Layer - Business Logic
from dataclasses import dataclass
from typing import Optional, List
from abc import ABC, abstractmethod

@dataclass
class User:
    """Domain Entity - User."""
    id: Optional[str]
    name: str
    email: str
    created_at: Optional[datetime] = None

    def can_access_resource(self, resource_id: str) -> bool:
        """Business rule - user access validation."""
        # Domain business logic
        return self.id is not None and self.email.endswith('@company.com')

class UserRepository(ABC):
    """Domain Repository Interface."""

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...

# Application Layer - Use Cases
class CreateUserUseCase:
    """Application Use Case - Create User."""

    def __init__(self, user_repository: UserRepository, email_service: 'EmailService'):
        self.user_repository = user_repository
        self.email_service = email_service

    async def execute(self, user_data: dict) -> User:
        """Execute the create user use case."""
        # Validation
        existing_user = await self.user_repository.find_by_email(user_data['email'])
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create domain entity
        user = User(
            id=None,
            name=user_data['name'],
            email=user_data['email']
        )

        # Save through repository
        saved_user = await self.user_repository.save(user)

        # Side effects
        await self.email_service.send_welcome_email(saved_user.email)

        return saved_user

# Infrastructure Layer - External Concerns
class PostgreSQLUserRepository(UserRepository):
    """Infrastructure - PostgreSQL implementation."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def save(self, user: User) -> User:
        async with self.db_pool.acquire() as conn:
            if user.id:
                # Update existing
                await conn.execute(
                    "UPDATE users SET name = $1, email = $2 WHERE id = $3",
                    user.name, user.email, user.id
                )
                return user
            else:
                # Create new
                user_id = await conn.fetchval(
                    "INSERT INTO users (name, email, created_at) VALUES ($1, $2, NOW()) RETURNING id",
                    user.name, user.email
                )
                user.id = user_id
                return user

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, email, created_at FROM users WHERE id = $1",
                user_id
            )
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    created_at=row['created_at']
                )
            return None

# Interface Layer - Controllers
class UserController:
    """Interface - Web API Controller."""

    def __init__(self, create_user_use_case: CreateUserUseCase):
        self.create_user_use_case = create_user_use_case

    async def create_user(self, request_data: dict) -> dict:
        """HTTP endpoint for user creation."""
        try:
            user = await self.create_user_use_case.execute(request_data)
            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }

# Dependency Injection Container
class Container:
    """DI Container for wiring dependencies."""

    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        """Register service implementation."""
        self._services[interface] = implementation

    def get(self, interface):
        """Get service implementation."""
        return self._services.get(interface)

    async def configure(self, db_pool):
        """Configure all dependencies."""
        # Infrastructure
        user_repo = PostgreSQLUserRepository(db_pool)
        email_service = SMTPEmailService()

        # Application
        create_user_use_case = CreateUserUseCase(user_repo, email_service)

        # Interface
        user_controller = UserController(create_user_use_case)

        # Register
        self.register(UserRepository, user_repo)
        self.register(CreateUserUseCase, create_user_use_case)
        self.register(UserController, user_controller)
```

### Microservices Architecture Patterns
```python
# Service Discovery Pattern
import consul
import aiohttp
from typing import Dict, List, Optional

class ServiceRegistry:
    """Service registry for microservices discovery."""

    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)

    async def register_service(self, service_name: str, service_id: str,
                             host: str, port: int, health_check_url: str):
        """Register a service with consul."""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            check=consul.Check.http(health_check_url, interval="10s")
        )

    async def discover_service(self, service_name: str) -> List[Dict]:
        """Discover healthy instances of a service."""
        _, services = self.consul.health.service(service_name, passing=True)
        return [
            {
                "id": service['Service']['ID'],
                "address": service['Service']['Address'],
                "port": service['Service']['Port']
            }
            for service in services
        ]

    async def deregister_service(self, service_id: str):
        """Deregister a service."""
        self.consul.agent.service.deregister(service_id)

# Load Balancer Pattern
import random
from typing import Callable

class LoadBalancer:
    """Client-side load balancer."""

    def __init__(self, service_registry: ServiceRegistry):
        self.service_registry = service_registry
        self.strategies = {
            "round_robin": self._round_robin,
            "random": self._random,
            "least_connections": self._least_connections
        }
        self._round_robin_counters = {}
        self._connection_counts = {}

    async def get_service_instance(self, service_name: str, strategy: str = "round_robin"):
        """Get a service instance using specified load balancing strategy."""
        instances = await self.service_registry.discover_service(service_name)

        if not instances:
            raise Exception(f"No healthy instances found for service: {service_name}")

        strategy_func = self.strategies.get(strategy, self._round_robin)
        return strategy_func(service_name, instances)

    def _round_robin(self, service_name: str, instances: List[Dict]) -> Dict:
        """Round robin load balancing."""
        if service_name not in self._round_robin_counters:
            self._round_robin_counters[service_name] = 0

        instance = instances[self._round_robin_counters[service_name] % len(instances)]
        self._round_robin_counters[service_name] += 1
        return instance

    def _random(self, service_name: str, instances: List[Dict]) -> Dict:
        """Random load balancing."""
        return random.choice(instances)

    def _least_connections(self, service_name: str, instances: List[Dict]) -> Dict:
        """Least connections load balancing."""
        # Simplified - in practice, would track actual connections
        min_connections = float('inf')
        selected_instance = None

        for instance in instances:
            instance_id = instance['id']
            connections = self._connection_counts.get(instance_id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_instance = instance

        return selected_instance

# Circuit Breaker Pattern
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker pattern implementation."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60,
                 expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.next_attempt = datetime.now()

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if datetime.now() < self.next_attempt:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = CircuitState.HALF_OPEN

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.next_attempt = datetime.now() + timedelta(seconds=self.timeout)

# API Gateway Pattern
class APIGateway:
    """API Gateway with routing, auth, and rate limiting."""

    def __init__(self, service_registry: ServiceRegistry, load_balancer: LoadBalancer):
        self.service_registry = service_registry
        self.load_balancer = load_balancer
        self.circuit_breakers = {}
        self.rate_limiters = {}
        self.routes = {}

    def register_route(self, path: str, service_name: str, auth_required: bool = True):
        """Register a route to a microservice."""
        self.routes[path] = {
            "service_name": service_name,
            "auth_required": auth_required
        }

    async def route_request(self, path: str, method: str, headers: dict, body: dict):
        """Route request to appropriate microservice."""
        route_config = self.routes.get(path)
        if not route_config:
            return {"error": "Route not found", "status": 404}

        # Authentication check
        if route_config["auth_required"]:
            if not await self._authenticate_request(headers):
                return {"error": "Unauthorized", "status": 401}

        # Rate limiting
        if not await self._check_rate_limit(headers.get("user_id")):
            return {"error": "Rate limit exceeded", "status": 429}

        # Load balancing
        service_name = route_config["service_name"]
        instance = await self.load_balancer.get_service_instance(service_name)

        # Circuit breaker
        circuit_breaker = self._get_circuit_breaker(service_name)

        try:
            response = await circuit_breaker.call(
                self._forward_request,
                instance, method, path, headers, body
            )
            return response

        except Exception as e:
            return {"error": f"Service unavailable: {str(e)}", "status": 503}

    def _get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service."""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]

    async def _authenticate_request(self, headers: dict) -> bool:
        """Authenticate request using JWT or other method."""
        # Simplified authentication logic
        auth_header = headers.get("Authorization")
        return auth_header and auth_header.startswith("Bearer ")

    async def _check_rate_limit(self, user_id: str) -> bool:
        """Check rate limiting for user."""
        # Simplified rate limiting logic
        return True  # In practice, would use Redis or similar

    async def _forward_request(self, instance: dict, method: str,
                              path: str, headers: dict, body: dict) -> dict:
        """Forward request to microservice instance."""
        url = f"http://{instance['address']}:{instance['port']}{path}"

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=body) as response:
                return {
                    "status": response.status,
                    "data": await response.json()
                }
```

## Event-Driven Architecture

### Event Sourcing Implementation
```python
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

@dataclass
class Event:
    """Base event class."""
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_version: int
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EventStore(ABC):
    """Abstract event store interface."""

    @abstractmethod
    async def append_events(self, aggregate_id: str, events: List[Event],
                           expected_version: int) -> None: ...

    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]: ...

class PostgreSQLEventStore(EventStore):
    """PostgreSQL implementation of event store."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def append_events(self, aggregate_id: str, events: List[Event],
                           expected_version: int) -> None:
        """Append events to the event store."""
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                # Check version for optimistic concurrency control
                current_version = await conn.fetchval(
                    "SELECT COALESCE(MAX(aggregate_version), 0) FROM events WHERE aggregate_id = $1",
                    aggregate_id
                )

                if current_version != expected_version:
                    raise Exception(f"Concurrency conflict. Expected {expected_version}, got {current_version}")

                # Insert events
                for event in events:
                    await conn.execute("""
                        INSERT INTO events (event_id, event_type, aggregate_id, aggregate_version,
                                          timestamp, data, metadata)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """, event.event_id, event.event_type, event.aggregate_id,
                        event.aggregate_version, event.timestamp,
                        json.dumps(event.data), json.dumps(event.metadata))

    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]:
        """Get events for an aggregate."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT event_id, event_type, aggregate_id, aggregate_version,
                       timestamp, data, metadata
                FROM events
                WHERE aggregate_id = $1 AND aggregate_version >= $2
                ORDER BY aggregate_version
            """, aggregate_id, from_version)

            return [
                Event(
                    event_id=row['event_id'],
                    event_type=row['event_type'],
                    aggregate_id=row['aggregate_id'],
                    aggregate_version=row['aggregate_version'],
                    timestamp=row['timestamp'],
                    data=json.loads(row['data']),
                    metadata=json.loads(row['metadata'])
                )
                for row in rows
            ]

# Aggregate Root Base Class
class AggregateRoot:
    """Base class for aggregate roots."""

    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self.uncommitted_events: List[Event] = []

    def apply_event(self, event: Event):
        """Apply an event to the aggregate."""
        self.version = event.aggregate_version
        method_name = f"_apply_{event.event_type.lower()}"

        if hasattr(self, method_name):
            getattr(self, method_name)(event.data)

    def raise_event(self, event_type: str, data: Dict[str, Any]):
        """Raise a new event."""
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            aggregate_id=self.aggregate_id,
            aggregate_version=self.version + 1,
            timestamp=datetime.utcnow(),
            data=data
        )

        self.uncommitted_events.append(event)
        self.apply_event(event)

    def get_uncommitted_events(self) -> List[Event]:
        """Get uncommitted events."""
        return self.uncommitted_events.copy()

    def mark_events_as_committed(self):
        """Mark events as committed."""
        self.uncommitted_events.clear()

# Example: User Aggregate
class User(AggregateRoot):
    """User aggregate with event sourcing."""

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.name = None
        self.email = None
        self.is_active = False

    @classmethod
    def create(cls, user_id: str, name: str, email: str) -> 'User':
        """Create a new user."""
        user = cls(user_id)
        user.raise_event("UserCreated", {
            "name": name,
            "email": email
        })
        return user

    def change_email(self, new_email: str):
        """Change user email."""
        if self.email == new_email:
            return

        self.raise_event("UserEmailChanged", {
            "old_email": self.email,
            "new_email": new_email
        })

    def deactivate(self):
        """Deactivate user."""
        if not self.is_active:
            return

        self.raise_event("UserDeactivated", {})

    # Event handlers
    def _apply_usercreated(self, data: Dict[str, Any]):
        """Apply UserCreated event."""
        self.name = data["name"]
        self.email = data["email"]
        self.is_active = True

    def _apply_useremailchanged(self, data: Dict[str, Any]):
        """Apply UserEmailChanged event."""
        self.email = data["new_email"]

    def _apply_userdeactivated(self, data: Dict[str, Any]):
        """Apply UserDeactivated event."""
        self.is_active = False

# Repository for Event Sourced Aggregates
class EventSourcedRepository:
    """Repository for event sourced aggregates."""

    def __init__(self, event_store: EventStore, aggregate_class):
        self.event_store = event_store
        self.aggregate_class = aggregate_class

    async def get_by_id(self, aggregate_id: str):
        """Load aggregate from event store."""
        events = await self.event_store.get_events(aggregate_id)

        if not events:
            return None

        aggregate = self.aggregate_class(aggregate_id)
        for event in events:
            aggregate.apply_event(event)

        return aggregate

    async def save(self, aggregate: AggregateRoot):
        """Save aggregate to event store."""
        uncommitted_events = aggregate.get_uncommitted_events()

        if uncommitted_events:
            expected_version = aggregate.version - len(uncommitted_events)
            await self.event_store.append_events(
                aggregate.aggregate_id,
                uncommitted_events,
                expected_version
            )
            aggregate.mark_events_as_committed()
```

### CQRS Pattern Implementation
```python
from typing import Protocol, Any
from dataclasses import dataclass
import asyncio

# Command Side (Write Model)
@dataclass
class Command:
    """Base command class."""
    pass

@dataclass
class CreateUserCommand(Command):
    """Command to create a user."""
    user_id: str
    name: str
    email: str

@dataclass
class ChangeUserEmailCommand(Command):
    """Command to change user email."""
    user_id: str
    new_email: str

class CommandHandler(Protocol):
    """Command handler interface."""
    async def handle(self, command: Command) -> Any: ...

class CreateUserCommandHandler:
    """Handler for CreateUserCommand."""

    def __init__(self, user_repository: EventSourcedRepository):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> str:
        """Handle user creation command."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_id(command.user_id)
        if existing_user:
            raise ValueError("User already exists")

        # Create new user
        user = User.create(command.user_id, command.name, command.email)
        await self.user_repository.save(user)

        return user.aggregate_id

class ChangeUserEmailCommandHandler:
    """Handler for ChangeUserEmailCommand."""

    def __init__(self, user_repository: EventSourcedRepository):
        self.user_repository = user_repository

    async def handle(self, command: ChangeUserEmailCommand) -> None:
        """Handle email change command."""
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError("User not found")

        user.change_email(command.new_email)
        await self.user_repository.save(user)

# Query Side (Read Model)
@dataclass
class Query:
    """Base query class."""
    pass

@dataclass
class GetUserByIdQuery(Query):
    """Query to get user by ID."""
    user_id: str

@dataclass
class GetUsersByEmailQuery(Query):
    """Query to get users by email pattern."""
    email_pattern: str

class QueryHandler(Protocol):
    """Query handler interface."""
    async def handle(self, query: Query) -> Any: ...

# Read Model
@dataclass
class UserReadModel:
    """User read model for queries."""
    user_id: str
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UserReadModelRepository:
    """Repository for user read models."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_by_id(self, user_id: str) -> Optional[UserReadModel]:
        """Get user read model by ID."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM user_read_models WHERE user_id = $1",
                user_id
            )
            if row:
                return UserReadModel(**dict(row))
            return None

    async def find_by_email_pattern(self, pattern: str) -> List[UserReadModel]:
        """Find users by email pattern."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM user_read_models WHERE email LIKE $1",
                f"%{pattern}%"
            )
            return [UserReadModel(**dict(row)) for row in rows]

    async def upsert(self, user: UserReadModel):
        """Insert or update user read model."""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_read_models (user_id, name, email, is_active, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (user_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    is_active = EXCLUDED.is_active,
                    updated_at = EXCLUDED.updated_at
            """, user.user_id, user.name, user.email, user.is_active,
                user.created_at, user.updated_at)

class GetUserByIdQueryHandler:
    """Handler for GetUserByIdQuery."""

    def __init__(self, read_model_repo: UserReadModelRepository):
        self.read_model_repo = read_model_repo

    async def handle(self, query: GetUserByIdQuery) -> Optional[UserReadModel]:
        """Handle get user by ID query."""
        return await self.read_model_repo.get_by_id(query.user_id)

# Command and Query Bus
class MessageBus:
    """Message bus for commands and queries."""

    def __init__(self):
        self.command_handlers = {}
        self.query_handlers = {}
        self.event_handlers = {}

    def register_command_handler(self, command_type: type, handler: CommandHandler):
        """Register command handler."""
        self.command_handlers[command_type] = handler

    def register_query_handler(self, query_type: type, handler: QueryHandler):
        """Register query handler."""
        self.query_handlers[query_type] = handler

    def register_event_handler(self, event_type: str, handler: Callable):
        """Register event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    async def send_command(self, command: Command) -> Any:
        """Send command to handler."""
        handler = self.command_handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler for command: {type(command)}")

        return await handler.handle(command)

    async def send_query(self, query: Query) -> Any:
        """Send query to handler."""
        handler = self.query_handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler for query: {type(query)}")

        return await handler.handle(query)

    async def publish_event(self, event: Event) -> None:
        """Publish event to all handlers."""
        handlers = self.event_handlers.get(event.event_type, [])

        tasks = [handler(event) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Event Handler for Read Model Projection
class UserReadModelProjector:
    """Projector for user read model."""

    def __init__(self, read_model_repo: UserReadModelRepository):
        self.read_model_repo = read_model_repo

    async def handle_user_created(self, event: Event):
        """Handle UserCreated event."""
        user_read_model = UserReadModel(
            user_id=event.aggregate_id,
            name=event.data["name"],
            email=event.data["email"],
            is_active=True,
            created_at=event.timestamp,
            updated_at=event.timestamp
        )
        await self.read_model_repo.upsert(user_read_model)

    async def handle_user_email_changed(self, event: Event):
        """Handle UserEmailChanged event."""
        user = await self.read_model_repo.get_by_id(event.aggregate_id)
        if user:
            user.email = event.data["new_email"]
            user.updated_at = event.timestamp
            await self.read_model_repo.upsert(user)
```

## Cloud Architecture Patterns

### Multi-Cloud Strategy
```yaml
# Infrastructure as Code - Terraform example
# variables.tf
variable "cloud_provider" {
  description = "Primary cloud provider"
  type        = string
  default     = "aws"

  validation {
    condition     = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or azure."
  }
}

variable "multi_cloud_enabled" {
  description = "Enable multi-cloud deployment"
  type        = bool
  default     = false
}

variable "regions" {
  description = "Deployment regions per cloud"
  type = map(list(string))
  default = {
    aws   = ["us-east-1", "eu-west-1"]
    gcp   = ["us-central1", "europe-west1"]
    azure = ["East US", "West Europe"]
  }
}

# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# AWS Resources
module "aws_infrastructure" {
  count  = var.cloud_provider == "aws" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/aws"

  regions = var.regions.aws
  environment = var.environment
}

# GCP Resources
module "gcp_infrastructure" {
  count  = var.cloud_provider == "gcp" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/gcp"

  regions = var.regions.gcp
  environment = var.environment
}

# Azure Resources
module "azure_infrastructure" {
  count  = var.cloud_provider == "azure" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/azure"

  regions = var.regions.azure
  environment = var.environment
}

# Cross-cloud networking
module "cross_cloud_networking" {
  count  = var.multi_cloud_enabled ? 1 : 0
  source = "./modules/cross-cloud"

  aws_vpc_ids    = try(module.aws_infrastructure[0].vpc_ids, [])
  gcp_vpc_names  = try(module.gcp_infrastructure[0].vpc_names, [])
  azure_vnet_ids = try(module.azure_infrastructure[0].vnet_ids, [])
}
```

### Serverless Architecture
```python
# Serverless function with AWS Lambda
import json
import boto3
from typing import Dict, Any
import asyncio

class ServerlessEventProcessor:
    """Serverless event processing architecture."""

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.s3 = boto3.client('s3')

    async def process_api_request(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """AWS Lambda handler for API requests."""
        try:
            # Parse request
            body = json.loads(event.get('body', '{}'))
            path = event.get('path', '')
            method = event.get('httpMethod', '')

            # Route to appropriate handler
            if path.startswith('/users') and method == 'POST':
                result = await self._handle_user_creation(body)
            elif path.startswith('/users') and method == 'GET':
                result = await self._handle_user_query(event.get('pathParameters', {}))
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Not found'})
                }

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    async def _handle_user_creation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user creation in serverless environment."""
        # Validate input
        if not user_data.get('email') or not user_data.get('name'):
            raise ValueError("Email and name are required")

        # Store in DynamoDB
        table = self.dynamodb.Table('users')
        user_id = f"user_{int(time.time())}"

        table.put_item(Item={
            'user_id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'created_at': datetime.utcnow().isoformat()
        })

        # Send welcome email via SQS
        await self._send_async_notification(user_id, user_data['email'])

        return {'user_id': user_id, 'status': 'created'}

    async def _send_async_notification(self, user_id: str, email: str):
        """Send asynchronous notification via SQS."""
        message = {
            'type': 'welcome_email',
            'user_id': user_id,
            'email': email
        }

        self.sqs.send_message(
            QueueUrl=os.environ['NOTIFICATION_QUEUE_URL'],
            MessageBody=json.dumps(message)
        )

# Serverless deployment configuration
# serverless.yml
service: archon-serverless-api

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    STAGE: ${opt:stage, 'dev'}
    NOTIFICATION_QUEUE_URL: ${self:resources.Outputs.NotificationQueueUrl.Value}

  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
        - dynamodb:DeleteItem
        - dynamodb:Query
        - dynamodb:Scan
      Resource: "arn:aws:dynamodb:${self:provider.region}:*:table/*"

    - Effect: Allow
      Action:
        - sqs:SendMessage
        - sqs:ReceiveMessage
        - sqs:DeleteMessage
      Resource: "arn:aws:sqs:${self:provider.region}:*:*"

functions:
  api:
    handler: handler.api_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 512

  notification_processor:
    handler: handler.notification_handler
    events:
      - sqs:
          arn: ${self:resources.Outputs.NotificationQueueArn.Value}
          batchSize: 10
    timeout: 60
    memorySize: 256

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: users-${self:provider.environment.STAGE}
        AttributeDefinitions:
          - AttributeName: user_id
            AttributeType: S
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
        BillingMode: PAY_PER_REQUEST

    NotificationQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: notifications-${self:provider.environment.STAGE}
        MessageRetentionPeriod: 1209600  # 14 days
        VisibilityTimeoutSeconds: 120

  Outputs:
    NotificationQueueUrl:
      Value:
        Ref: NotificationQueue
    NotificationQueueArn:
      Value:
        Fn::GetAtt: [NotificationQueue, Arn]

plugins:
  - serverless-python-requirements
  - serverless-domain-manager

custom:
  pythonRequirements:
    dockerizePip: true
  customDomain:
    domainName: api.archon.example.com
    basePath: ''
    stage: ${self:provider.environment.STAGE}
    createRoute53Record: true
```

## Best Practices для Blueprint Architect

### 1. Architecture Documentation
- **Architecture Decision Records (ADRs)**: Документируй все архитектурные решения
- **System Context Diagrams**: C4 модель для визуализации архитектуры
- **API Specifications**: OpenAPI/Swagger для всех интерфейсов
- **Runbooks**: Операционная документация для production

### 2. Scalability Design Principles
- **Horizontal Scaling**: Проектируй для горизонтального масштабирования
- **Stateless Services**: Избегай состояния в сервисах
- **Caching Strategies**: Многоуровневое кэширование
- **Database Sharding**: Стратегии разбиения данных

### 3. Reliability & Resilience
- **Circuit Breakers**: Защита от cascade failures
- **Bulkhead Pattern**: Изоляция ресурсов
- **Timeout & Retry**: Graceful degradation
- **Health Checks**: Comprehensive monitoring

### 4. Security Architecture
- **Zero Trust**: Проверка на каждом уровне
- **Defense in Depth**: Многоуровневая защита
- **Least Privilege**: Минимальные права доступа
- **Encryption**: Data at rest и in transit

---

## 🔍 ДОМЕННЫЕ ЗНАНИЯ: [ОБЛАСТЬ]

## Архитектурные принципы и паттерны

### SOLID Principles в архитектуре
```python
from abc import ABC, abstractmethod
from typing import Protocol, Generic, TypeVar
from dataclasses import dataclass

# Single Responsibility Principle
class UserService:
    """Сервис управления пользователями - одна ответственность."""

    def __init__(self, user_repository, email_service, audit_service):
        self.user_repository = user_repository
        self.email_service = email_service
        self.audit_service = audit_service

    async def create_user(self, user_data: dict) -> User:
        """Создание пользователя с уведомлением и аудитом."""
        user = await self.user_repository.create(user_data)
        await self.email_service.send_welcome_email(user.email)
        await self.audit_service.log_user_creation(user.id)
        return user

# Open/Closed Principle
class PaymentProcessor(ABC):
    """Базовый интерфейс для процессоров платежей."""

    @abstractmethod
    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        pass

class StripePaymentProcessor(PaymentProcessor):
    """Конкретная реализация для Stripe."""

    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        # Stripe-specific logic
        return {"status": "success", "transaction_id": "stripe_123"}

class PayPalPaymentProcessor(PaymentProcessor):
    """Новая реализация без изменения существующего кода."""

    async def process_payment(self, amount: float, payment_data: dict) -> dict:
        # PayPal-specific logic
        return {"status": "success", "transaction_id": "paypal_456"}

# Liskov Substitution Principle
class DatabaseRepository(ABC):
    """Базовый репозиторий."""

    @abstractmethod
    async def save(self, entity) -> str:
        pass

    @abstractmethod
    async def find_by_id(self, id: str):
        pass

class PostgreSQLRepository(DatabaseRepository):
    """PostgreSQL реализация."""

    async def save(self, entity) -> str:
        # Сохранение в PostgreSQL
        return "pg_id_123"

    async def find_by_id(self, id: str):
        # Поиск в PostgreSQL
        return {"id": id, "data": "from_postgres"}

class MongoRepository(DatabaseRepository):
    """MongoDB реализация - полностью заменяет PostgreSQL."""

    async def save(self, entity) -> str:
        # Сохранение в MongoDB
        return "mongo_id_456"

    async def find_by_id(self, id: str):
        # Поиск в MongoDB
        return {"id": id, "data": "from_mongo"}

# Interface Segregation Principle
class ReadOperations(Protocol):
    """Интерфейс только для чтения."""
    async def get(self, id: str): ...
    async def list(self, filters: dict): ...

class WriteOperations(Protocol):
    """Интерфейс только для записи."""
    async def create(self, data: dict): ...
    async def update(self, id: str, data: dict): ...
    async def delete(self, id: str): ...

class CacheService:
    """Сервис кэша - использует только ReadOperations."""

    def __init__(self, read_repo: ReadOperations):
        self.read_repo = read_repo

    async def get_cached(self, id: str):
        # Только чтение, не нужен WriteOperations
        return await self.read_repo.get(id)

# Dependency Inversion Principle
class NotificationService:
    """Зависит от абстракции, а не от конкретной реализации."""

    def __init__(self, message_sender: 'MessageSender'):
        self.message_sender = message_sender  # Абстракция

    async def send_notification(self, user_id: str, message: str):
        await self.message_sender.send(user_id, message)

class MessageSender(Protocol):
    """Абстракция для отправки сообщений."""
    async def send(self, recipient: str, message: str): ...

class EmailSender:
    """Конкретная реализация."""
    async def send(self, recipient: str, message: str):
        # Email sending logic
        pass

class SMSSender:
    """Другая конкретная реализация."""
    async def send(self, recipient: str, message: str):
        # SMS sending logic
        pass
```

### Clean Architecture Implementation
```python
# Domain Layer - Business Logic
from dataclasses import dataclass
from typing import Optional, List
from abc import ABC, abstractmethod

@dataclass
class User:
    """Domain Entity - User."""
    id: Optional[str]
    name: str
    email: str
    created_at: Optional[datetime] = None

    def can_access_resource(self, resource_id: str) -> bool:
        """Business rule - user access validation."""
        # Domain business logic
        return self.id is not None and self.email.endswith('@company.com')

class UserRepository(ABC):
    """Domain Repository Interface."""

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...

# Application Layer - Use Cases
class CreateUserUseCase:
    """Application Use Case - Create User."""

    def __init__(self, user_repository: UserRepository, email_service: 'EmailService'):
        self.user_repository = user_repository
        self.email_service = email_service

    async def execute(self, user_data: dict) -> User:
        """Execute the create user use case."""
        # Validation
        existing_user = await self.user_repository.find_by_email(user_data['email'])
        if existing_user:
            raise ValueError("User with this email already exists")

        # Create domain entity
        user = User(
            id=None,
            name=user_data['name'],
            email=user_data['email']
        )

        # Save through repository
        saved_user = await self.user_repository.save(user)

        # Side effects
        await self.email_service.send_welcome_email(saved_user.email)

        return saved_user

# Infrastructure Layer - External Concerns
class PostgreSQLUserRepository(UserRepository):
    """Infrastructure - PostgreSQL implementation."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def save(self, user: User) -> User:
        async with self.db_pool.acquire() as conn:
            if user.id:
                # Update existing
                await conn.execute(
                    "UPDATE users SET name = $1, email = $2 WHERE id = $3",
                    user.name, user.email, user.id
                )
                return user
            else:
                # Create new
                user_id = await conn.fetchval(
                    "INSERT INTO users (name, email, created_at) VALUES ($1, $2, NOW()) RETURNING id",
                    user.name, user.email
                )
                user.id = user_id
                return user

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, email, created_at FROM users WHERE id = $1",
                user_id
            )
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    created_at=row['created_at']
                )
            return None

# Interface Layer - Controllers
class UserController:
    """Interface - Web API Controller."""

    def __init__(self, create_user_use_case: CreateUserUseCase):
        self.create_user_use_case = create_user_use_case

    async def create_user(self, request_data: dict) -> dict:
        """HTTP endpoint for user creation."""
        try:
            user = await self.create_user_use_case.execute(request_data)
            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }

# Dependency Injection Container
class Container:
    """DI Container for wiring dependencies."""

    def __init__(self):
        self._services = {}

    def register(self, interface, implementation):
        """Register service implementation."""
        self._services[interface] = implementation

    def get(self, interface):
        """Get service implementation."""
        return self._services.get(interface)

    async def configure(self, db_pool):
        """Configure all dependencies."""
        # Infrastructure
        user_repo = PostgreSQLUserRepository(db_pool)
        email_service = SMTPEmailService()

        # Application
        create_user_use_case = CreateUserUseCase(user_repo, email_service)

        # Interface
        user_controller = UserController(create_user_use_case)

        # Register
        self.register(UserRepository, user_repo)
        self.register(CreateUserUseCase, create_user_use_case)
        self.register(UserController, user_controller)
```

### Microservices Architecture Patterns
```python
# Service Discovery Pattern
import consul
import aiohttp
from typing import Dict, List, Optional

class ServiceRegistry:
    """Service registry for microservices discovery."""

    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)

    async def register_service(self, service_name: str, service_id: str,
                             host: str, port: int, health_check_url: str):
        """Register a service with consul."""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            check=consul.Check.http(health_check_url, interval="10s")
        )

    async def discover_service(self, service_name: str) -> List[Dict]:
        """Discover healthy instances of a service."""
        _, services = self.consul.health.service(service_name, passing=True)
        return [
            {
                "id": service['Service']['ID'],
                "address": service['Service']['Address'],
                "port": service['Service']['Port']
            }
            for service in services
        ]

    async def deregister_service(self, service_id: str):
        """Deregister a service."""
        self.consul.agent.service.deregister(service_id)

# Load Balancer Pattern
import random
from typing import Callable

class LoadBalancer:
    """Client-side load balancer."""

    def __init__(self, service_registry: ServiceRegistry):
        self.service_registry = service_registry
        self.strategies = {
            "round_robin": self._round_robin,
            "random": self._random,
            "least_connections": self._least_connections
        }
        self._round_robin_counters = {}
        self._connection_counts = {}

    async def get_service_instance(self, service_name: str, strategy: str = "round_robin"):
        """Get a service instance using specified load balancing strategy."""
        instances = await self.service_registry.discover_service(service_name)

        if not instances:
            raise Exception(f"No healthy instances found for service: {service_name}")

        strategy_func = self.strategies.get(strategy, self._round_robin)
        return strategy_func(service_name, instances)

    def _round_robin(self, service_name: str, instances: List[Dict]) -> Dict:
        """Round robin load balancing."""
        if service_name not in self._round_robin_counters:
            self._round_robin_counters[service_name] = 0

        instance = instances[self._round_robin_counters[service_name] % len(instances)]
        self._round_robin_counters[service_name] += 1
        return instance

    def _random(self, service_name: str, instances: List[Dict]) -> Dict:
        """Random load balancing."""
        return random.choice(instances)

    def _least_connections(self, service_name: str, instances: List[Dict]) -> Dict:
        """Least connections load balancing."""
        # Simplified - in practice, would track actual connections
        min_connections = float('inf')
        selected_instance = None

        for instance in instances:
            instance_id = instance['id']
            connections = self._connection_counts.get(instance_id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_instance = instance

        return selected_instance

# Circuit Breaker Pattern
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker pattern implementation."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60,
                 expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.next_attempt = datetime.now()

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if datetime.now() < self.next_attempt:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = CircuitState.HALF_OPEN

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.next_attempt = datetime.now() + timedelta(seconds=self.timeout)

# API Gateway Pattern
class APIGateway:
    """API Gateway with routing, auth, and rate limiting."""

    def __init__(self, service_registry: ServiceRegistry, load_balancer: LoadBalancer):
        self.service_registry = service_registry
        self.load_balancer = load_balancer
        self.circuit_breakers = {}
        self.rate_limiters = {}
        self.routes = {}

    def register_route(self, path: str, service_name: str, auth_required: bool = True):
        """Register a route to a microservice."""
        self.routes[path] = {
            "service_name": service_name,
            "auth_required": auth_required
        }

    async def route_request(self, path: str, method: str, headers: dict, body: dict):
        """Route request to appropriate microservice."""
        route_config = self.routes.get(path)
        if not route_config:
            return {"error": "Route not found", "status": 404}

        # Authentication check
        if route_config["auth_required"]:
            if not await self._authenticate_request(headers):
                return {"error": "Unauthorized", "status": 401}

        # Rate limiting
        if not await self._check_rate_limit(headers.get("user_id")):
            return {"error": "Rate limit exceeded", "status": 429}

        # Load balancing
        service_name = route_config["service_name"]
        instance = await self.load_balancer.get_service_instance(service_name)

        # Circuit breaker
        circuit_breaker = self._get_circuit_breaker(service_name)

        try:
            response = await circuit_breaker.call(
                self._forward_request,
                instance, method, path, headers, body
            )
            return response

        except Exception as e:
            return {"error": f"Service unavailable: {str(e)}", "status": 503}

    def _get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service."""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]

    async def _authenticate_request(self, headers: dict) -> bool:
        """Authenticate request using JWT or other method."""
        # Simplified authentication logic
        auth_header = headers.get("Authorization")
        return auth_header and auth_header.startswith("Bearer ")

    async def _check_rate_limit(self, user_id: str) -> bool:
        """Check rate limiting for user."""
        # Simplified rate limiting logic
        return True  # In practice, would use Redis or similar

    async def _forward_request(self, instance: dict, method: str,
                              path: str, headers: dict, body: dict) -> dict:
        """Forward request to microservice instance."""
        url = f"http://{instance['address']}:{instance['port']}{path}"

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=body) as response:
                return {
                    "status": response.status,
                    "data": await response.json()
                }
```

## Event-Driven Architecture

### Event Sourcing Implementation
```python
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

@dataclass
class Event:
    """Base event class."""
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_version: int
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EventStore(ABC):
    """Abstract event store interface."""

    @abstractmethod
    async def append_events(self, aggregate_id: str, events: List[Event],
                           expected_version: int) -> None: ...

    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]: ...

class PostgreSQLEventStore(EventStore):
    """PostgreSQL implementation of event store."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def append_events(self, aggregate_id: str, events: List[Event],
                           expected_version: int) -> None:
        """Append events to the event store."""
        async with self.db_pool.acquire() as conn:
            async with conn.transaction():
                # Check version for optimistic concurrency control
                current_version = await conn.fetchval(
                    "SELECT COALESCE(MAX(aggregate_version), 0) FROM events WHERE aggregate_id = $1",
                    aggregate_id
                )

                if current_version != expected_version:
                    raise Exception(f"Concurrency conflict. Expected {expected_version}, got {current_version}")

                # Insert events
                for event in events:
                    await conn.execute("""
                        INSERT INTO events (event_id, event_type, aggregate_id, aggregate_version,
                                          timestamp, data, metadata)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """, event.event_id, event.event_type, event.aggregate_id,
                        event.aggregate_version, event.timestamp,
                        json.dumps(event.data), json.dumps(event.metadata))

    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]:
        """Get events for an aggregate."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT event_id, event_type, aggregate_id, aggregate_version,
                       timestamp, data, metadata
                FROM events
                WHERE aggregate_id = $1 AND aggregate_version >= $2
                ORDER BY aggregate_version
            """, aggregate_id, from_version)

            return [
                Event(
                    event_id=row['event_id'],
                    event_type=row['event_type'],
                    aggregate_id=row['aggregate_id'],
                    aggregate_version=row['aggregate_version'],
                    timestamp=row['timestamp'],
                    data=json.loads(row['data']),
                    metadata=json.loads(row['metadata'])
                )
                for row in rows
            ]

# Aggregate Root Base Class
class AggregateRoot:
    """Base class for aggregate roots."""

    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self.uncommitted_events: List[Event] = []

    def apply_event(self, event: Event):
        """Apply an event to the aggregate."""
        self.version = event.aggregate_version
        method_name = f"_apply_{event.event_type.lower()}"

        if hasattr(self, method_name):
            getattr(self, method_name)(event.data)

    def raise_event(self, event_type: str, data: Dict[str, Any]):
        """Raise a new event."""
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            aggregate_id=self.aggregate_id,
            aggregate_version=self.version + 1,
            timestamp=datetime.utcnow(),
            data=data
        )

        self.uncommitted_events.append(event)
        self.apply_event(event)

    def get_uncommitted_events(self) -> List[Event]:
        """Get uncommitted events."""
        return self.uncommitted_events.copy()

    def mark_events_as_committed(self):
        """Mark events as committed."""
        self.uncommitted_events.clear()

# Example: User Aggregate
class User(AggregateRoot):
    """User aggregate with event sourcing."""

    def __init__(self, aggregate_id: str):
        super().__init__(aggregate_id)
        self.name = None
        self.email = None
        self.is_active = False

    @classmethod
    def create(cls, user_id: str, name: str, email: str) -> 'User':
        """Create a new user."""
        user = cls(user_id)
        user.raise_event("UserCreated", {
            "name": name,
            "email": email
        })
        return user

    def change_email(self, new_email: str):
        """Change user email."""
        if self.email == new_email:
            return

        self.raise_event("UserEmailChanged", {
            "old_email": self.email,
            "new_email": new_email
        })

    def deactivate(self):
        """Deactivate user."""
        if not self.is_active:
            return

        self.raise_event("UserDeactivated", {})

    # Event handlers
    def _apply_usercreated(self, data: Dict[str, Any]):
        """Apply UserCreated event."""
        self.name = data["name"]
        self.email = data["email"]
        self.is_active = True

    def _apply_useremailchanged(self, data: Dict[str, Any]):
        """Apply UserEmailChanged event."""
        self.email = data["new_email"]

    def _apply_userdeactivated(self, data: Dict[str, Any]):
        """Apply UserDeactivated event."""
        self.is_active = False

# Repository for Event Sourced Aggregates
class EventSourcedRepository:
    """Repository for event sourced aggregates."""

    def __init__(self, event_store: EventStore, aggregate_class):
        self.event_store = event_store
        self.aggregate_class = aggregate_class

    async def get_by_id(self, aggregate_id: str):
        """Load aggregate from event store."""
        events = await self.event_store.get_events(aggregate_id)

        if not events:
            return None

        aggregate = self.aggregate_class(aggregate_id)
        for event in events:
            aggregate.apply_event(event)

        return aggregate

    async def save(self, aggregate: AggregateRoot):
        """Save aggregate to event store."""
        uncommitted_events = aggregate.get_uncommitted_events()

        if uncommitted_events:
            expected_version = aggregate.version - len(uncommitted_events)
            await self.event_store.append_events(
                aggregate.aggregate_id,
                uncommitted_events,
                expected_version
            )
            aggregate.mark_events_as_committed()
```

### CQRS Pattern Implementation
```python
from typing import Protocol, Any
from dataclasses import dataclass
import asyncio

# Command Side (Write Model)
@dataclass
class Command:
    """Base command class."""
    pass

@dataclass
class CreateUserCommand(Command):
    """Command to create a user."""
    user_id: str
    name: str
    email: str

@dataclass
class ChangeUserEmailCommand(Command):
    """Command to change user email."""
    user_id: str
    new_email: str

class CommandHandler(Protocol):
    """Command handler interface."""
    async def handle(self, command: Command) -> Any: ...

class CreateUserCommandHandler:
    """Handler for CreateUserCommand."""

    def __init__(self, user_repository: EventSourcedRepository):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> str:
        """Handle user creation command."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_id(command.user_id)
        if existing_user:
            raise ValueError("User already exists")

        # Create new user
        user = User.create(command.user_id, command.name, command.email)
        await self.user_repository.save(user)

        return user.aggregate_id

class ChangeUserEmailCommandHandler:
    """Handler for ChangeUserEmailCommand."""

    def __init__(self, user_repository: EventSourcedRepository):
        self.user_repository = user_repository

    async def handle(self, command: ChangeUserEmailCommand) -> None:
        """Handle email change command."""
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError("User not found")

        user.change_email(command.new_email)
        await self.user_repository.save(user)

# Query Side (Read Model)
@dataclass
class Query:
    """Base query class."""
    pass

@dataclass
class GetUserByIdQuery(Query):
    """Query to get user by ID."""
    user_id: str

@dataclass
class GetUsersByEmailQuery(Query):
    """Query to get users by email pattern."""
    email_pattern: str

class QueryHandler(Protocol):
    """Query handler interface."""
    async def handle(self, query: Query) -> Any: ...

# Read Model
@dataclass
class UserReadModel:
    """User read model for queries."""
    user_id: str
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UserReadModelRepository:
    """Repository for user read models."""

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_by_id(self, user_id: str) -> Optional[UserReadModel]:
        """Get user read model by ID."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM user_read_models WHERE user_id = $1",
                user_id
            )
            if row:
                return UserReadModel(**dict(row))
            return None

    async def find_by_email_pattern(self, pattern: str) -> List[UserReadModel]:
        """Find users by email pattern."""
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM user_read_models WHERE email LIKE $1",
                f"%{pattern}%"
            )
            return [UserReadModel(**dict(row)) for row in rows]

    async def upsert(self, user: UserReadModel):
        """Insert or update user read model."""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_read_models (user_id, name, email, is_active, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (user_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    is_active = EXCLUDED.is_active,
                    updated_at = EXCLUDED.updated_at
            """, user.user_id, user.name, user.email, user.is_active,
                user.created_at, user.updated_at)

class GetUserByIdQueryHandler:
    """Handler for GetUserByIdQuery."""

    def __init__(self, read_model_repo: UserReadModelRepository):
        self.read_model_repo = read_model_repo

    async def handle(self, query: GetUserByIdQuery) -> Optional[UserReadModel]:
        """Handle get user by ID query."""
        return await self.read_model_repo.get_by_id(query.user_id)

# Command and Query Bus
class MessageBus:
    """Message bus for commands and queries."""

    def __init__(self):
        self.command_handlers = {}
        self.query_handlers = {}
        self.event_handlers = {}

    def register_command_handler(self, command_type: type, handler: CommandHandler):
        """Register command handler."""
        self.command_handlers[command_type] = handler

    def register_query_handler(self, query_type: type, handler: QueryHandler):
        """Register query handler."""
        self.query_handlers[query_type] = handler

    def register_event_handler(self, event_type: str, handler: Callable):
        """Register event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    async def send_command(self, command: Command) -> Any:
        """Send command to handler."""
        handler = self.command_handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler for command: {type(command)}")

        return await handler.handle(command)

    async def send_query(self, query: Query) -> Any:
        """Send query to handler."""
        handler = self.query_handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler for query: {type(query)}")

        return await handler.handle(query)

    async def publish_event(self, event: Event) -> None:
        """Publish event to all handlers."""
        handlers = self.event_handlers.get(event.event_type, [])

        tasks = [handler(event) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Event Handler for Read Model Projection
class UserReadModelProjector:
    """Projector for user read model."""

    def __init__(self, read_model_repo: UserReadModelRepository):
        self.read_model_repo = read_model_repo

    async def handle_user_created(self, event: Event):
        """Handle UserCreated event."""
        user_read_model = UserReadModel(
            user_id=event.aggregate_id,
            name=event.data["name"],
            email=event.data["email"],
            is_active=True,
            created_at=event.timestamp,
            updated_at=event.timestamp
        )
        await self.read_model_repo.upsert(user_read_model)

    async def handle_user_email_changed(self, event: Event):
        """Handle UserEmailChanged event."""
        user = await self.read_model_repo.get_by_id(event.aggregate_id)
        if user:
            user.email = event.data["new_email"]
            user.updated_at = event.timestamp
            await self.read_model_repo.upsert(user)
```

## Cloud Architecture Patterns

### Multi-Cloud Strategy
```yaml
# Infrastructure as Code - Terraform example
# variables.tf
variable "cloud_provider" {
  description = "Primary cloud provider"
  type        = string
  default     = "aws"

  validation {
    condition     = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or azure."
  }
}

variable "multi_cloud_enabled" {
  description = "Enable multi-cloud deployment"
  type        = bool
  default     = false
}

variable "regions" {
  description = "Deployment regions per cloud"
  type = map(list(string))
  default = {
    aws   = ["us-east-1", "eu-west-1"]
    gcp   = ["us-central1", "europe-west1"]
    azure = ["East US", "West Europe"]
  }
}

# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# AWS Resources
module "aws_infrastructure" {
  count  = var.cloud_provider == "aws" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/aws"

  regions = var.regions.aws
  environment = var.environment
}

# GCP Resources
module "gcp_infrastructure" {
  count  = var.cloud_provider == "gcp" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/gcp"

  regions = var.regions.gcp
  environment = var.environment
}

# Azure Resources
module "azure_infrastructure" {
  count  = var.cloud_provider == "azure" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/azure"

  regions = var.regions.azure
  environment = var.environment
}

# Cross-cloud networking
module "cross_cloud_networking" {
  count  = var.multi_cloud_enabled ? 1 : 0
  source = "./modules/cross-cloud"

  aws_vpc_ids    = try(module.aws_infrastructure[0].vpc_ids, [])
  gcp_vpc_names  = try(module.gcp_infrastructure[0].vpc_names, [])
  azure_vnet_ids = try(module.azure_infrastructure[0].vnet_ids, [])
}
```

### Serverless Architecture
```python
# Serverless function with AWS Lambda
import json
import boto3
from typing import Dict, Any
import asyncio

class ServerlessEventProcessor:
    """Serverless event processing architecture."""

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.s3 = boto3.client('s3')

    async def process_api_request(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """AWS Lambda handler for API requests."""
        try:
            # Parse request
            body = json.loads(event.get('body', '{}'))
            path = event.get('path', '')
            method = event.get('httpMethod', '')

            # Route to appropriate handler
            if path.startswith('/users') and method == 'POST':
                result = await self._handle_user_creation(body)
            elif path.startswith('/users') and method == 'GET':
                result = await self._handle_user_query(event.get('pathParameters', {}))
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Not found'})
                }

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    async def _handle_user_creation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user creation in serverless environment."""
        # Validate input
        if not user_data.get('email') or not user_data.get('name'):
            raise ValueError("Email and name are required")

        # Store in DynamoDB
        table = self.dynamodb.Table('users')
        user_id = f"user_{int(time.time())}"

        table.put_item(Item={
            'user_id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'created_at': datetime.utcnow().isoformat()
        })

        # Send welcome email via SQS
        await self._send_async_notification(user_id, user_data['email'])

        return {'user_id': user_id, 'status': 'created'}

    async def _send_async_notification(self, user_id: str, email: str):
        """Send asynchronous notification via SQS."""
        message = {
            'type': 'welcome_email',
            'user_id': user_id,
            'email': email
        }

        self.sqs.send_message(
            QueueUrl=os.environ['NOTIFICATION_QUEUE_URL'],
            MessageBody=json.dumps(message)
        )

# Serverless deployment configuration
# serverless.yml
service: archon-serverless-api

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    STAGE: ${opt:stage, 'dev'}
    NOTIFICATION_QUEUE_URL: ${self:resources.Outputs.NotificationQueueUrl.Value}

  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
        - dynamodb:DeleteItem
        - dynamodb:Query
        - dynamodb:Scan
      Resource: "arn:aws:dynamodb:${self:provider.region}:*:table/*"

    - Effect: Allow
      Action:
        - sqs:SendMessage
        - sqs:ReceiveMessage
        - sqs:DeleteMessage
      Resource: "arn:aws:sqs:${self:provider.region}:*:*"

functions:
  api:
    handler: handler.api_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 512

  notification_processor:
    handler: handler.notification_handler
    events:
      - sqs:
          arn: ${self:resources.Outputs.NotificationQueueArn.Value}
          batchSize: 10
    timeout: 60
    memorySize: 256

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: users-${self:provider.environment.STAGE}
        AttributeDefinitions:
          - AttributeName: user_id
            AttributeType: S
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
        BillingMode: PAY_PER_REQUEST

    NotificationQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: notifications-${self:provider.environment.STAGE}
        MessageRetentionPeriod: 1209600  # 14 days
        VisibilityTimeoutSeconds: 120

  Outputs:
    NotificationQueueUrl:
      Value:
        Ref: NotificationQueue
    NotificationQueueArn:
      Value:
        Fn::GetAtt: [NotificationQueue, Arn]

plugins:
  - serverless-python-requirements
  - serverless-domain-manager

custom:
  pythonRequirements:
    dockerizePip: true
  customDomain:
    domainName: api.archon.example.com
    basePath: ''
    stage: ${self:provider.environment.STAGE}
    createRoute53Record: true
```

## Best Practices для Blueprint Architect

### 1. Architecture Documentation
- **Architecture Decision Records (ADRs)**: Документируй все архитектурные решения
- **System Context Diagrams**: C4 модель для визуализации архитектуры
- **API Specifications**: OpenAPI/Swagger для всех интерфейсов
- **Runbooks**: Операционная документация для production

### 2. Scalability Design Principles
- **Horizontal Scaling**: Проектируй для горизонтального масштабирования
- **Stateless Services**: Избегай состояния в сервисах
- **Caching Strategies**: Многоуровневое кэширование
- **Database Sharding**: Стратегии разбиения данных

### 3. Reliability & Resilience
- **Circuit Breakers**: Защита от cascade failures
- **Bulkhead Pattern**: Изоляция ресурсов
- **Timeout & Retry**: Graceful degradation
- **Health Checks**: Comprehensive monitoring

### 4. Security Architecture
- **Zero Trust**: Проверка на каждом уровне
- **Defense in Depth**: Многоуровневая защита
- **Least Privilege**: Минимальные права доступа
- **Encryption**: Data at rest и in transit

---

**Версия:** 2.0 (Модульная архитектура)
**Дата рефакторинга:** 2025-10-14
**Автор рефакторинга:** Archon Blueprint Architect
