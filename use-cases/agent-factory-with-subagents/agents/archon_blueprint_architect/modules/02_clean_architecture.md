# Clean Architecture Implementation

**Навигация:** [← Назад к Knowledge Base](../knowledge/archon_blueprint_architect_knowledge.md)

---

## Обзор

Clean Architecture (Чистая Архитектура) - подход к проектированию систем с независимыми слоями, где бизнес-логика изолирована от внешних деталей.

---

## Принципы Clean Architecture

### Dependency Rule
**Зависимости направлены внутрь:**
```
Interface → Application → Domain
Infrastructure → Application → Domain
```

**Правило:** Внутренние слои НЕ знают о внешних.

---

## Слои Clean Architecture

### 1. Domain Layer - Бизнес-логика

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """Domain Entity - User."""
    id: Optional[str]
    name: str
    email: str
    created_at: Optional[datetime] = None

    def can_access_resource(self, resource_id: str) -> bool:
        """Business rule - user access validation."""
        return self.id is not None and self.email.endswith('@company.com')
```

**Характеристики Domain Layer:**
- Не зависит от внешних библиотек
- Содержит бизнес-правила
- Определяет интерфейсы репозиториев

### 2. Application Layer - Use Cases

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    """Domain Repository Interface."""

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

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
```

**Характеристики Application Layer:**
- Оркестрирует бизнес-логику
- Не зависит от деталей реализации
- Использует интерфейсы, определенные в Domain

### 3. Infrastructure Layer - Внешние детали

```python
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
```

**Характеристики Infrastructure Layer:**
- Реализует интерфейсы из Domain
- Содержит специфику БД, frameworks, API
- Легко заменяема

### 4. Interface Layer - Controllers

```python
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
```

**Характеристики Interface Layer:**
- Адаптирует внешний мир к Application
- HTTP/gRPC/CLI controllers
- DTO для маппинга данных

---

## Dependency Injection Container

```python
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

## Преимущества Clean Architecture

### 1. Независимость от фреймворков
- Легко сменить FastAPI на Django
- Легко сменить SQLAlchemy на raw SQL

### 2. Тестируемость
- Domain и Application тестируются без БД
- Моки для внешних сервисов

### 3. Независимость от UI
- Одна бизнес-логика для Web, Mobile, CLI

### 4. Независимость от БД
- Смена PostgreSQL на MongoDB без изменения бизнес-логики

### 5. Независимость от внешних сервисов
- Легко заменить Email provider

---

## Практические рекомендации

### Структура проекта
```
project/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   └── repositories/
├── application/
│   ├── use_cases/
│   ├── services/
│   └── dto/
├── infrastructure/
│   ├── database/
│   ├── external_apis/
│   └── messaging/
└── interface/
    ├── http/
    ├── cli/
    └── graphql/
```

### Best Practices
- **Entities** содержат только бизнес-логику
- **Use Cases** оркестрируют Entities
- **Controllers** тонкие, только маршрутизация
- **Repositories** абстрактные в Domain, конкретные в Infrastructure

---

**Версия:** 1.0
**Дата создания:** 2025-10-14
**Автор:** Archon Blueprint Architect
