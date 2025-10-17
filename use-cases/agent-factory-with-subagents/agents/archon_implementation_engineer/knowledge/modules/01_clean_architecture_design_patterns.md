# Module 01: Clean Architecture & Design Patterns

**Версия:** 1.0
**Дата:** 2025-10-17
**Автор:** Archon Implementation Engineer

**Назад к:** [Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Создание Domain/Application/Infrastructure layers для AI агента
- Реализация Repository Pattern с Generic типами для data access
- Настройка Dependency Injection Container для управления зависимостями
- Применение SOLID principles к AI agents
- Разработка Clean Architecture structure для Pydantic AI
- Необходимость разделить бизнес-логику от технической реализации

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** чистая архитектура, SOLID, repository pattern, dependency injection, слои приложения, use case, domain logic, infrastructure layer, application layer, maintainability

**English:** clean architecture, SOLID, repository pattern, dependency injection, application layers, use case, domain logic, infrastructure layer, application layer, maintainability

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Разрабатываешь AI агента с бизнес-логикой
- Требуется высокая тестируемость кода
- Долгосрочная maintainability критична
- Нужно изолировать внешние зависимости (database, API, MCP)
- Создаешь production-ready агента для команды
- Планируешь масштабирование проекта

---

## Clean Architecture for AI Agents

### Структура Pydantic AI агента по Clean Architecture

```python
from typing import Protocol, Dict, Any, List
from pydantic_ai import Agent, RunContext
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Domain Layer - Business Logic
class AgentUseCase(ABC):
    """Абстрактный use case для агента."""

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить бизнес-логику агента."""
        pass

class ProcessUserQueryUseCase(AgentUseCase):
    """Use case для обработки пользовательских запросов."""

    def __init__(self, knowledge_service, validation_service):
        self.knowledge_service = knowledge_service
        self.validation_service = validation_service

    async def execute(self, query: str) -> Dict[str, Any]:
        # Валидация входных данных
        validated_query = await self.validation_service.validate(query)

        # Поиск релевантной информации
        context = await self.knowledge_service.search(validated_query)

        # Формирование ответа
        return {
            "query": validated_query,
            "context": context,
            "status": "success"
        }

# Application Layer - Agent Implementation
@dataclass
class AgentDependencies:
    """Зависимости агента."""
    knowledge_service: 'KnowledgeService'
    validation_service: 'ValidationService'
    settings: 'AgentSettings'

def create_agent(deps: AgentDependencies) -> Agent:
    """Factory для создания агента."""

    agent = Agent(
        model=deps.settings.model,
        deps_type=AgentDependencies,
        system_prompt=deps.settings.system_prompt
    )

    @agent.tool
    async def search_knowledge(ctx: RunContext[AgentDependencies], query: str) -> str:
        """Поиск в базе знаний."""
        use_case = ProcessUserQueryUseCase(
            ctx.deps.knowledge_service,
            ctx.deps.validation_service
        )
        result = await use_case.execute(query)
        return result

    return agent

# Infrastructure Layer - External Services
class KnowledgeService:
    """Сервис для работы с базой знаний."""

    def __init__(self, vector_db, embedding_model):
        self.vector_db = vector_db
        self.embedding_model = embedding_model

    async def search(self, query: str) -> List[Dict]:
        embedding = await self.embedding_model.encode(query)
        results = await self.vector_db.similarity_search(embedding)
        return results
```

### Когда использовать Clean Architecture:
- При разработке AI агентов с сложной бизнес-логикой
- Когда требуется тестируемость и maintainability
- Для проектов с долгосрочной поддержкой
- При необходимости изолировать внешние зависимости

---

## Repository Pattern для Data Access

### Абстрактный репозиторий с Generic типами

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
import asyncpg
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class Repository(ABC, Generic[T]):
    """Абстрактный репозиторий для CRUD операций."""

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Создать новую запись."""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        """Получить запись по ID."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Обновить существующую запись."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Удалить запись по ID."""
        pass

    @abstractmethod
    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Получить список записей с пагинацией."""
        pass

class PostgreSQLRepository(Repository[T]):
    """Реализация репозитория для PostgreSQL."""

    def __init__(self, pool: asyncpg.Pool, table_name: str, model_class):
        self.pool = pool
        self.table_name = table_name
        self.model_class = model_class

    async def create(self, entity: T) -> T:
        async with self.pool.acquire() as conn:
            data = entity.model_dump(exclude_none=True)
            columns = ', '.join(data.keys())
            placeholders = ', '.join(f'${i+1}' for i in range(len(data)))

            query = f"""
                INSERT INTO {self.table_name} ({columns})
                VALUES ({placeholders})
                RETURNING *
            """

            row = await conn.fetchrow(query, *data.values())
            return self.model_class(**dict(row))

    async def get_by_id(self, id: str) -> Optional[T]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                f"SELECT * FROM {self.table_name} WHERE id = $1", id
            )
            return self.model_class(**dict(row)) if row else None

    async def update(self, entity: T) -> T:
        async with self.pool.acquire() as conn:
            data = entity.model_dump(exclude_none=True)
            set_clause = ', '.join(f"{k} = ${i+1}" for i, k in enumerate(data.keys()))

            query = f"""
                UPDATE {self.table_name}
                SET {set_clause}
                WHERE id = ${len(data) + 1}
                RETURNING *
            """

            row = await conn.fetchrow(query, *data.values(), entity.id)
            return self.model_class(**dict(row))

    async def delete(self, id: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                f"DELETE FROM {self.table_name} WHERE id = $1", id
            )
            return result == "DELETE 1"

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT * FROM {self.table_name} LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [self.model_class(**dict(row)) for row in rows]
```

### Пример использования: User Service

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    """Модель пользователя."""
    id: Optional[str] = None
    name: str
    email: EmailStr
    is_active: bool = True

class UserRepository(PostgreSQLRepository[User]):
    """Репозиторий пользователей."""

    def __init__(self, pool: asyncpg.Pool):
        super().__init__(pool, "users", User)

    async def find_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                f"SELECT * FROM {self.table_name} WHERE email = $1", email
            )
            return self.model_class(**dict(row)) if row else None

class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, name: str, email: str) -> User:
        """Создать нового пользователя."""
        # Проверка существования
        existing = await self.user_repo.find_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")

        # Создание пользователя
        user = User(name=name, email=email)
        return await self.user_repo.create(user)

    async def get_user(self, user_id: str) -> Optional[User]:
        """Получить пользователя по ID."""
        return await self.user_repo.get_by_id(user_id)

    async def deactivate_user(self, user_id: str) -> bool:
        """Деактивировать пользователя."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        await self.user_repo.update(user)
        return True
```

---

## Dependency Injection Pattern

### Container для управления зависимостями

```python
from typing import Dict, Type, Callable, Any
from dataclasses import dataclass

class DependencyContainer:
    """Контейнер для Dependency Injection."""

    def __init__(self):
        self._services: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}

    def register(self, interface: Type, factory: Callable, singleton: bool = False):
        """Регистрация сервиса."""
        self._services[interface] = factory
        if singleton:
            # Создаем singleton при регистрации
            self._singletons[interface] = factory()

    def resolve(self, interface: Type) -> Any:
        """Получение экземпляра сервиса."""
        # Проверяем singleton кэш
        if interface in self._singletons:
            return self._singletons[interface]

        # Создаем новый экземпляр
        if interface not in self._services:
            raise ValueError(f"Service {interface} not registered")

        factory = self._services[interface]
        return factory()

# Пример использования
@dataclass
class AppConfiguration:
    """Конфигурация приложения."""
    database_url: str
    redis_url: str
    llm_api_key: str

def create_container(config: AppConfiguration) -> DependencyContainer:
    """Создание и настройка DI контейнера."""
    container = DependencyContainer()

    # Регистрация конфигурации как singleton
    container.register(
        AppConfiguration,
        lambda: config,
        singleton=True
    )

    # Регистрация database pool
    container.register(
        asyncpg.Pool,
        lambda: asyncpg.create_pool(config.database_url),
        singleton=True
    )

    # Регистрация репозиториев
    container.register(
        UserRepository,
        lambda: UserRepository(container.resolve(asyncpg.Pool))
    )

    # Регистрация сервисов
    container.register(
        UserService,
        lambda: UserService(container.resolve(UserRepository))
    )

    return container

# Usage
async def main():
    config = AppConfiguration(
        database_url="postgresql://...",
        redis_url="redis://...",
        llm_api_key="sk-..."
    )

    container = create_container(config)

    # Получение сервиса из контейнера
    user_service = container.resolve(UserService)
    user = await user_service.create_user("John", "john@example.com")
```

---

## SOLID Principles в AI Agents

### Single Responsibility Principle (SRP)

```python
# ❌ Плохо: класс делает слишком много
class BadAgent:
    def process_query(self, query):
        # Валидация
        # Поиск в БД
        # Генерация ответа
        # Логирование
        # Метрики
        pass

# ✅ Хорошо: разделение ответственности
class QueryValidator:
    """Отвечает только за валидацию."""
    def validate(self, query: str) -> bool:
        # Логика валидации
        pass

class KnowledgeSearcher:
    """Отвечает только за поиск."""
    def search(self, query: str) -> List[Dict]:
        # Логика поиска
        pass

class ResponseGenerator:
    """Отвечает только за генерацию ответов."""
    def generate(self, context: List[Dict]) -> str:
        # Логика генерации
        pass

class AgentOrchestrator:
    """Координирует работу компонентов."""
    def __init__(self, validator, searcher, generator):
        self.validator = validator
        self.searcher = searcher
        self.generator = generator

    async def process_query(self, query: str) -> str:
        if not self.validator.validate(query):
            raise ValueError("Invalid query")

        context = await self.searcher.search(query)
        response = await self.generator.generate(context)
        return response
```

### Open/Closed Principle (OCP)

```python
from abc import ABC, abstractmethod

# Базовый интерфейс
class LLMProvider(ABC):
    """Абстрактный провайдер LLM."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

# Реализации открыты для расширения
class OpenAIProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        # OpenAI специфичная логика
        pass

class AnthropicProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        # Anthropic специфичная логика
        pass

# Агент закрыт для модификации, но открыт для расширения
class MultiProviderAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, query: str) -> str:
        # Работает с любым провайдером
        return await self.provider.generate(query)
```

---

**Навигация:**
- [↑ Назад к Implementation Engineer Knowledge Base](../archon_implementation_engineer_knowledge.md)
- [→ Следующий модуль: Performance Optimization](02_performance_optimization.md)
