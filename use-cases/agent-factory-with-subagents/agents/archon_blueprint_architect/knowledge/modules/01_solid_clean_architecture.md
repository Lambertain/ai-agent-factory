# Module 01: SOLID Principles & Clean Architecture

**Назад к:** [Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)

---

## SOLID Principles в архитектуре
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

---

## Clean Architecture Implementation
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

---

**Навигация:**
- [← Назад к Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)
- [→ Следующий модуль: Microservices Patterns](02_microservices_patterns.md)
