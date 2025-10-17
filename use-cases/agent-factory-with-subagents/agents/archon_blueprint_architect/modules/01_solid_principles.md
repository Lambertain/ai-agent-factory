# SOLID Principles в архитектуре

**Навигация:** [← Назад к Knowledge Base](../knowledge/archon_blueprint_architect_knowledge.md)

---

## Обзор

SOLID - фундаментальные принципы объектно-ориентированного проектирования, критически важные для создания масштабируемых архитектур.

---

## S - Single Responsibility Principle (Принцип единственной ответственности)

**Правило:** Класс должен иметь только одну причину для изменения.

```python
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
```

**Преимущества:**
- Легче тестировать
- Проще поддерживать
- Меньше coupling между компонентами

---

## O - Open/Closed Principle (Принцип открытости/закрытости)

**Правило:** Программные сущности должны быть открыты для расширения, но закрыты для модификации.

```python
from abc import ABC, abstractmethod

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
```

**Преимущества:**
- Добавление функциональности без изменения кода
- Снижение риска breaking changes
- Поддержка полиморфизма

---

## L - Liskov Substitution Principle (Принцип подстановки Лисков)

**Правило:** Объекты подклассов должны быть взаимозаменяемы с объектами базового класса.

```python
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
```

**Преимущества:**
- Гарантия совместимости интерфейсов
- Безопасная замена реализаций
- Надежность системы

---

## I - Interface Segregation Principle (Принцип разделения интерфейса)

**Правило:** Клиенты не должны зависеть от интерфейсов, которые они не используют.

```python
from typing import Protocol

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
```

**Преимущества:**
- Минимальные зависимости
- Гибкость в реализации
- Простота в тестировании

---

## D - Dependency Inversion Principle (Принцип инверсии зависимостей)

**Правило:** Зависеть от абстракций, а не от конкретных реализаций.

```python
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

**Преимущества:**
- Слабая связанность (loose coupling)
- Простая замена реализаций
- Тестируемость через mocks

---

## Применение SOLID в архитектуре

### Уровень сервисов
- **SRP:** Один сервис = одна бизнес-ответственность
- **OCP:** Расширение через плагины/модули
- **LSP:** Совместимость версий API
- **ISP:** Разделение публичных и приватных API
- **DIP:** Зависимость от контрактов, не от реализаций

### Уровень микросервисов
- **SRP:** Bounded Context из DDD
- **OCP:** Event-driven расширения
- **LSP:** API Gateway с версионированием
- **ISP:** GraphQL для гибких интерфейсов
- **DIP:** Service Mesh для абстракции коммуникации

---

**Версия:** 1.0
**Дата создания:** 2025-10-14
**Автор:** Archon Blueprint Architect
