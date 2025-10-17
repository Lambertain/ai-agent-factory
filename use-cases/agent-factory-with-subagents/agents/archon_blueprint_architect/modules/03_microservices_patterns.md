# Microservices Architecture Patterns

**Навигация:** [← Назад к Knowledge Base](../knowledge/archon_blueprint_architect_knowledge.md)

---

## Обзор

Паттерны микросервисной архитектуры для построения распределенных систем с высокой доступностью и масштабируемостью.

---

## Service Discovery Pattern

### Проблема
Микросервисы динамически создаются/удаляются. Как найти актуальный адрес сервиса?

### Решение: Service Registry

```python
import consul
from typing import Dict, List

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
```

**Преимущества:**
- Автоматическое обнаружение сервисов
- Health checks из коробки
- Динамическая конфигурация

---

## Load Balancer Pattern

### Client-Side Load Balancing

```python
import random
from typing import Callable, List, Dict

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
        min_connections = float('inf')
        selected_instance = None

        for instance in instances:
            instance_id = instance['id']
            connections = self._connection_counts.get(instance_id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_instance = instance

        return selected_instance
```

**Стратегии:**
- **Round Robin:** Равномерное распределение
- **Random:** Случайный выбор
- **Least Connections:** Минимальная нагрузка

---

## Circuit Breaker Pattern

### Проблема
Сбойный сервис может вызвать cascade failure во всей системе.

### Решение: Circuit Breaker

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable

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
```

**Состояния:**
- **CLOSED:** Нормальная работа
- **OPEN:** Блокировка запросов
- **HALF_OPEN:** Тестовая попытка восстановления

---

## API Gateway Pattern

### Unified Entry Point

```python
import aiohttp

class APIGateway:
    """API Gateway with routing, auth, and rate limiting."""

    def __init__(self, service_registry: ServiceRegistry, load_balancer: LoadBalancer):
        self.service_registry = service_registry
        self.load_balancer = load_balancer
        self.circuit_breakers = {}
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
        auth_header = headers.get("Authorization")
        return auth_header and auth_header.startswith("Bearer ")

    async def _check_rate_limit(self, user_id: str) -> bool:
        """Check rate limiting for user."""
        # In practice, would use Redis or similar
        return True

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

**Функции API Gateway:**
- Routing и маршрутизация
- Authentication & Authorization
- Rate limiting
- Load balancing
- Circuit breaking
- Protocol translation

---

## Best Practices

### 1. Service Mesh
- Istio/Linkerd для управления трафиком
- Автоматический retry и timeout
- Observability из коробки

### 2. Saga Pattern
- Распределенные транзакции
- Choreography vs Orchestration
- Компенсирующие транзакции

### 3. Event-Driven Communication
- Asynchronous messaging
- Event sourcing для истории
- CQRS для разделения write/read

---

**Версия:** 1.0
**Дата создания:** 2025-10-14
**Автор:** Archon Blueprint Architect
