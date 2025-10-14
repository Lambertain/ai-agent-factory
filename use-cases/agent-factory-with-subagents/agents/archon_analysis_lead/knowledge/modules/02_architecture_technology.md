# Module 02: Architecture & Technology Analysis

**Назад к:** [Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)

---

## System Architecture Analysis Framework

### Структура архитектурного анализа

```python
class ArchitecturalAnalysis:
    """Структура для архитектурного анализа системы."""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.components = []
        self.integrations = []
        self.non_functional_requirements = {}

    def analyze_requirements(self, requirements: List[str]) -> Dict:
        """Анализ требований для архитектурных решений."""
        analysis = {
            "functional_requirements": [],
            "non_functional_requirements": {},
            "constraints": [],
            "assumptions": []
        }

        for req in requirements:
            # Классификация требований
            if self.is_performance_requirement(req):
                analysis["non_functional_requirements"]["performance"] = req
            elif self.is_security_requirement(req):
                analysis["non_functional_requirements"]["security"] = req
            elif self.is_scalability_requirement(req):
                analysis["non_functional_requirements"]["scalability"] = req
            else:
                analysis["functional_requirements"].append(req)

        return analysis

    def design_system_architecture(self, requirements: Dict) -> Dict:
        """Проектирование архитектуры на основе требований."""
        architecture = {
            "layers": self.define_layers(requirements),
            "components": self.identify_components(requirements),
            "data_flow": self.design_data_flow(requirements),
            "integration_points": self.identify_integrations(requirements),
            "technology_stack": self.recommend_technologies(requirements)
        }
        return architecture

    @staticmethod
    def is_performance_requirement(req: str) -> bool:
        """Определить требование производительности."""
        keywords = ["latency", "throughput", "response time", "RPS", "ms"]
        return any(keyword in req.lower() for keyword in keywords)

    @staticmethod
    def is_security_requirement(req: str) -> bool:
        """Определить требование безопасности."""
        keywords = ["auth", "encryption", "security", "pci", "gdpr", "compliance"]
        return any(keyword in req.lower() for keyword in keywords)

    @staticmethod
    def is_scalability_requirement(req: str) -> bool:
        """Определить требование масштабируемости."""
        keywords = ["scale", "concurrent", "users", "load", "capacity"]
        return any(keyword in req.lower() for keyword in keywords)

    def define_layers(self, requirements: Dict) -> List[str]:
        """Определить архитектурные слои."""
        base_layers = [
            "Presentation Layer (UI/API)",
            "Application Layer (Business Logic)",
            "Domain Layer (Core Entities)",
            "Infrastructure Layer (DB, External Services)"
        ]

        # Добавить дополнительные слои по требованиям
        if any("event" in str(req).lower() for req in requirements.get("functional_requirements", [])):
            base_layers.append("Event Processing Layer")

        if requirements.get("non_functional_requirements", {}).get("security"):
            base_layers.insert(0, "Security Layer (Auth, Authorization)")

        return base_layers

    def identify_components(self, requirements: Dict) -> Dict[str, List[str]]:
        """Идентифицировать компоненты системы."""
        components = {
            "Core Services": [],
            "Supporting Services": [],
            "External Integrations": []
        }

        # Анализ требований для идентификации компонентов
        for req in requirements.get("functional_requirements", []):
            if "user" in req.lower():
                components["Core Services"].append("User Service")
            if "payment" in req.lower():
                components["Core Services"].append("Payment Service")
            if "notification" in req.lower():
                components["Supporting Services"].append("Notification Service")
            if "analytics" in req.lower():
                components["Supporting Services"].append("Analytics Service")

        return components

    def design_data_flow(self, requirements: Dict) -> Dict:
        """Спроектировать потоки данных."""
        return {
            "synchronous_flows": ["User → API → Service → Database"],
            "asynchronous_flows": ["Service → Message Queue → Worker → Database"],
            "data_consistency": "Strong consistency" if "transaction" in str(requirements).lower() else "Eventual consistency"
        }

    def identify_integrations(self, requirements: Dict) -> List[str]:
        """Идентифицировать точки интеграции."""
        integrations = []

        if "payment" in str(requirements).lower():
            integrations.append("Payment Gateway (Stripe/PayPal)")
        if "email" in str(requirements).lower():
            integrations.append("Email Service (SendGrid/SES)")
        if "analytics" in str(requirements).lower():
            integrations.append("Analytics Platform (Mixpanel/Amplitude)")

        return integrations

    def recommend_technologies(self, requirements: Dict) -> Dict[str, str]:
        """Рекомендовать технологический стек."""
        tech_stack = {
            "Backend": "Python FastAPI / Node.js Express",
            "Database": "PostgreSQL (relational) / MongoDB (document)",
            "Cache": "Redis",
            "Message Queue": "RabbitMQ / AWS SQS",
            "API Gateway": "Kong / AWS API Gateway",
            "Monitoring": "Prometheus + Grafana",
            "Logging": "ELK Stack (Elasticsearch, Logstash, Kibana)"
        }

        # Адаптация на основе NFR
        perf = requirements.get("non_functional_requirements", {}).get("performance")
        if perf and "high throughput" in str(perf).lower():
            tech_stack["Message Queue"] = "Apache Kafka"
            tech_stack["Database"] = "PostgreSQL with Read Replicas"

        return tech_stack
```

### Когда использовать:
- При проектировании новых систем с нуля
- При миграции монолитных приложений на микросервисы
- При анализе архитектуры существующей системы
- При подготовке технических спецификаций для команды

---

## Technology Stack Analysis

### Критерии выбора технологий

```yaml
# Фреймворк оценки технологий

Technology Selection Criteria:

  Backend Framework:
    Performance:
      - Latency: < 100ms (P95)
      - Throughput: > 1000 RPS
      - Memory footprint: Efficient memory usage

    Scalability:
      - Horizontal scaling: Native support
      - Load balancing: Built-in or easy integration
      - Auto-scaling: Cloud-native capabilities

    Ecosystem:
      - Library ecosystem: Rich and mature
      - Community support: Active community
      - Documentation: Comprehensive docs

    Team Expertise:
      - Current knowledge: Existing team skills
      - Learning curve: Time to productivity
      - Hiring availability: Market availability

    Long-term Support:
      - Maintenance: Active maintenance
      - Security updates: Regular patches
      - Backward compatibility: Stable API

  Database:
    Data Model:
      - Relational: ACID transactions, complex queries
      - Document: Flexible schema, nested data
      - Key-Value: High performance, simple queries
      - Graph: Relationship-heavy data

    ACID Requirements:
      - Strong consistency: Financial transactions
      - Eventual consistency: Social media, analytics
      - No consistency: Caching, session storage

    Scalability:
      - Read/Write patterns: Read-heavy vs Write-heavy
      - Sharding: Horizontal partitioning support
      - Replication: Master-slave, multi-master

    Backup & Recovery:
      - RTO (Recovery Time Objective): Target downtime
      - RPO (Recovery Point Objective): Acceptable data loss
      - Backup strategy: Full, incremental, continuous

  Frontend:
    User Experience:
      - Responsive: Mobile-first design
      - Accessible: WCAG 2.1 compliance
      - Offline support: Service workers, PWA

    Performance:
      - Bundle size: < 250KB initial load
      - Loading speed: < 3s First Contentful Paint
      - Runtime performance: 60 FPS animations

    SEO Requirements:
      - Server-side rendering: SEO-critical pages
      - Static generation: Marketing pages
      - Client-side rendering: Interactive apps

    Browser Support:
      - Modern browsers: Chrome, Firefox, Safari, Edge
      - Legacy support: IE11 (if required)
      - Mobile browsers: iOS Safari, Chrome Mobile
```

---

## Technology Decision Matrix

### Матрица принятия решений

```python
class TechnologyDecisionMatrix:
    """Матрица для выбора технологий."""

    def __init__(self):
        self.criteria = {
            "performance": 0.25,
            "scalability": 0.20,
            "cost": 0.15,
            "team_expertise": 0.20,
            "ecosystem": 0.10,
            "maintainability": 0.10
        }

    def evaluate_technology(self, tech_name: str, scores: Dict[str, int]) -> float:
        """Оценить технологию по критериям.

        Args:
            tech_name: Название технологии
            scores: Оценки по каждому критерию (1-10)

        Returns:
            Итоговая взвешенная оценка
        """
        weighted_score = 0.0

        for criterion, weight in self.criteria.items():
            score = scores.get(criterion, 0)
            weighted_score += score * weight

        return round(weighted_score, 2)

    def compare_technologies(self, options: Dict[str, Dict[str, int]]) -> Dict[str, float]:
        """Сравнить несколько технологий.

        Args:
            options: Словарь {название_технологии: {критерий: оценка}}

        Returns:
            Отсортированный словарь с итоговыми оценками
        """
        results = {}

        for tech_name, scores in options.items():
            results[tech_name] = self.evaluate_technology(tech_name, scores)

        # Сортировка по убыванию оценки
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


# Пример использования
matrix = TechnologyDecisionMatrix()

options = {
    "FastAPI (Python)": {
        "performance": 8,
        "scalability": 9,
        "cost": 9,  # Open-source
        "team_expertise": 9,  # Team knows Python
        "ecosystem": 8,
        "maintainability": 9
    },
    "Express.js (Node)": {
        "performance": 7,
        "scalability": 8,
        "cost": 9,
        "team_expertise": 6,  # Team learning Node
        "ecosystem": 9,
        "maintainability": 7
    },
    "Spring Boot (Java)": {
        "performance": 9,
        "scalability": 9,
        "cost": 9,
        "team_expertise": 4,  # Team doesn't know Java
        "ecosystem": 10,
        "maintainability": 8
    }
}

results = matrix.compare_technologies(options)
# Результат: {"FastAPI (Python)": 8.55, "Spring Boot (Java)": 8.25, "Express.js (Node)": 7.45}
```

---

## Architecture Decision Records (ADR)

### Шаблон ADR

```markdown
# ADR-001: Выбор базы данных для User Service

**Статус:** Принято

**Контекст:**
Нам нужна база данных для User Service, которая будет хранить:
- Профили пользователей (10M+ записей)
- Сессии пользователей (высокая частота записи/чтения)
- Настройки и предпочтения пользователей

**Требования:**
- ACID транзакции для критических операций
- Масштабирование до 100K concurrent users
- Latency < 50ms для чтения профиля
- Поддержка сложных запросов (JOIN, агрегация)

**Рассмотренные варианты:**

### Вариант 1: PostgreSQL
**Плюсы:**
- ✅ Полная ACID поддержка
- ✅ Отличная производительность для чтения
- ✅ Богатые возможности запросов (JOIN, CTE, Window Functions)
- ✅ Проверенная надежность и стабильность
- ✅ Команда имеет опыт работы

**Минусы:**
- ❌ Вертикальное масштабирование ограничено
- ❌ Требует настройки read replicas для scale-out

### Вариант 2: MongoDB
**Плюсы:**
- ✅ Гибкая схема данных
- ✅ Легкое горизонтальное масштабирование
- ✅ Высокая производительность на write-heavy нагрузках

**Минусы:**
- ❌ Eventual consistency по умолчанию
- ❌ Сложные JOIN операции требуют application-level логики
- ❌ Меньше опыта в команде

### Вариант 3: Cassandra
**Плюсы:**
- ✅ Линейное масштабирование на write операциях
- ✅ Высокая доступность (multi-datacenter replication)

**Минусы:**
- ❌ Нет ACID транзакций
- ❌ Сложность в поддержке и operational overhead
- ❌ Нет опыта в команде

**Решение:** PostgreSQL

**Обоснование:**
1. **ACID критично** для операций с профилями пользователей
2. **Богатые запросы** необходимы для analytics и reporting
3. **Команда имеет опыт** - быстрый time-to-market
4. **Масштабирование решается** через read replicas + connection pooling
5. **Proven track record** в аналогичных проектах

**Последствия:**
- ✅ Быстрая разработка благодаря знакомой технологии
- ✅ Надежность и consistency из коробки
- ⚠️ Потребуется настройка репликации для масштабирования
- ⚠️ Мониторинг производительности запросов (slow query log)

**Дата:** 2025-10-14
**Автор:** Analysis Lead
**Reviewers:** Blueprint Architect, DBA Team
```

---

## Performance Requirements Analysis

### NFR Template

```yaml
# Non-Functional Requirements (NFR)

Performance:
  Response Time:
    - API endpoints: P95 < 200ms, P99 < 500ms
    - Database queries: P95 < 50ms
    - External API calls: P95 < 1000ms (with timeout)

  Throughput:
    - Read operations: 10,000 RPS
    - Write operations: 2,000 RPS
    - Concurrent users: 50,000

  Resource Utilization:
    - CPU: < 70% average, < 90% peak
    - Memory: < 80% of allocated
    - Disk I/O: < 70% IOPS capacity

Scalability:
  Horizontal Scaling:
    - Auto-scaling triggers: CPU > 75% for 5 minutes
    - Scale-out: Add 2 instances per trigger
    - Scale-in: Remove 1 instance when CPU < 30% for 10 minutes

  Data Partitioning:
    - Strategy: Sharding by user_id hash
    - Shard count: 16 initial shards
    - Rebalancing: Automatic when shard > 100GB

Availability:
  Uptime: 99.9% (8.76 hours downtime/year)

  Recovery Objectives:
    - RTO (Recovery Time): < 5 minutes
    - RPO (Recovery Point): < 1 minute data loss

  Redundancy:
    - Multi-AZ deployment (3 availability zones)
    - Active-passive database replicas
    - Cross-region backup every 6 hours

Security:
  Authentication:
    - OAuth2 / JWT tokens
    - Token expiry: 1 hour (access), 7 days (refresh)
    - MFA for admin accounts

  Authorization:
    - RBAC (Role-Based Access Control)
    - API rate limiting: 100 req/min per user

  Data Protection:
    - Encryption at rest: AES-256
    - Encryption in transit: TLS 1.3
    - PII data masking in logs

Monitoring:
  Metrics:
    - Application: Request rate, error rate, latency
    - Infrastructure: CPU, memory, disk, network
    - Business: Active users, transactions, revenue

  Alerting:
    - Error rate > 1% → Page on-call engineer
    - Latency P95 > 500ms → Slack notification
    - Uptime < 99.9% → Escalate to manager

  Logging:
    - Structured logs (JSON format)
    - Retention: 30 days in hot storage, 1 year in cold
    - Log aggregation: ELK Stack
```

---

**Навигация:**
- [← Предыдущий модуль: Requirements Analysis](01_requirements_analysis.md)
- [↑ Назад к Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)
- [→ Следующий модуль: Task Breakdown & Estimation](03_task_breakdown_estimation.md)
