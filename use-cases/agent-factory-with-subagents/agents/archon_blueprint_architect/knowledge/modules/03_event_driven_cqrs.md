# Module 03: Event-Driven Architecture & CQRS

**Назад к:** [Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)

---

## Event Sourcing Implementation
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

---

## CQRS Pattern Implementation
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

---

**Навигация:**
- [← Предыдущий модуль: Microservices Patterns](02_microservices_patterns.md)
- [↑ Назад к Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)
- [→ Следующий модуль: Cloud & Serverless Architecture](04_cloud_serverless_architecture.md)
