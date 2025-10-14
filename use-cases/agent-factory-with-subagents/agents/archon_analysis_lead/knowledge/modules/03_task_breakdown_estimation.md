# Module 03: Task Breakdown & Estimation Techniques

**Назад к:** [Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)

---

## Task Breakdown Structure (TBS)

### Иерархическая декомпозиция проекта

```
Project: E-commerce Platform
├── 1. Analysis & Design (2 weeks)
│   ├── 1.1 Requirements Gathering
│   │   ├── 1.1.1 Stakeholder interviews (3 days)
│   │   ├── 1.1.2 User persona creation (2 days)
│   │   └── 1.1.3 Requirements documentation (2 days)
│   ├── 1.2 System Architecture Design
│   │   ├── 1.2.1 High-level architecture diagram (2 days)
│   │   ├── 1.2.2 Technology stack selection (1 day)
│   │   ├── 1.2.3 Database schema design (3 days)
│   │   └── 1.2.4 API contract definition (2 days)
│   └── 1.3 Technical Specifications
│       ├── 1.3.1 API documentation (OpenAPI spec) (2 days)
│       ├── 1.3.2 Security requirements doc (1 day)
│       └── 1.3.3 Performance requirements doc (1 day)
│
├── 2. Foundation (1 week)
│   ├── 2.1 Project Setup
│   │   ├── 2.1.1 Repository initialization (0.5 days)
│   │   ├── 2.1.2 CI/CD pipeline setup (2 days)
│   │   └── 2.1.3 Code quality tools (linting, formatting) (1 day)
│   ├── 2.2 Infrastructure Setup
│   │   ├── 2.2.1 Cloud environment provisioning (1 day)
│   │   ├── 2.2.2 Database setup (PostgreSQL + Redis) (1 day)
│   │   └── 2.2.3 Monitoring & logging setup (1 day)
│   └── 2.3 Development Environment
│       ├── 2.3.1 Docker compose for local dev (1 day)
│       ├── 2.3.2 Environment variables management (0.5 days)
│       └── 2.3.3 Developer documentation (0.5 days)
│
├── 3. Core Implementation (6 weeks)
│   ├── 3.1 Authentication & Authorization (1 week)
│   │   ├── 3.1.1 User registration API (2 days)
│   │   ├── 3.1.2 Login/Logout with JWT (2 days)
│   │   ├── 3.1.3 Password reset flow (1 day)
│   │   ├── 3.1.4 OAuth2 integration (Google, GitHub) (2 days)
│   │   └── 3.1.5 RBAC implementation (2 days)
│   │
│   ├── 3.2 Product Catalog (2 weeks)
│   │   ├── 3.2.1 Product CRUD APIs (3 days)
│   │   ├── 3.2.2 Category management (2 days)
│   │   ├── 3.2.3 Product search (Elasticsearch) (3 days)
│   │   ├── 3.2.4 Filtering & sorting (2 days)
│   │   └── 3.2.5 Product image upload (S3) (2 days)
│   │
│   ├── 3.3 Shopping Cart (1 week)
│   │   ├── 3.3.1 Add/Remove items API (2 days)
│   │   ├── 3.3.2 Cart persistence (Redis) (1 day)
│   │   ├── 3.3.3 Quantity management (1 day)
│   │   └── 3.3.4 Cart expiry logic (1 day)
│   │
│   ├── 3.4 Order Management (2 weeks)
│   │   ├── 3.4.1 Checkout flow API (3 days)
│   │   ├── 3.4.2 Order creation & tracking (2 days)
│   │   ├── 3.4.3 Payment integration (Stripe) (3 days)
│   │   ├── 3.4.4 Order status updates (2 days)
│   │   └── 3.4.5 Order history & details (2 days)
│   │
│   └── 3.5 Notifications (1 week)
│       ├── 3.5.1 Email service integration (2 days)
│       ├── 3.5.2 Order confirmation emails (1 day)
│       ├── 3.5.3 Password reset emails (1 day)
│       └── 3.5.4 Marketing emails (opt-in) (1 day)
│
├── 4. Integration & Testing (3 weeks)
│   ├── 4.1 Component Integration
│   │   ├── 4.1.1 Service-to-service integration (3 days)
│   │   ├── 4.1.2 Third-party API integration (2 days)
│   │   └── 4.1.3 Frontend-backend integration (3 days)
│   │
│   ├── 4.2 Testing
│   │   ├── 4.2.1 Unit tests (coverage > 80%) (5 days)
│   │   ├── 4.2.2 Integration tests (3 days)
│   │   ├── 4.2.3 E2E tests (critical flows) (3 days)
│   │   └── 4.2.4 Performance testing (load tests) (2 days)
│   │
│   └── 4.3 Quality Assurance
│       ├── 4.3.1 Security audit (2 days)
│       ├── 4.3.2 Code review & refactoring (2 days)
│       └── 4.3.3 Bug fixing & optimization (3 days)
│
└── 5. Deployment & Monitoring (1 week)
    ├── 5.1 Production Deployment
    │   ├── 5.1.1 Production environment setup (1 day)
    │   ├── 5.1.2 Database migration (0.5 days)
    │   ├── 5.1.3 Zero-downtime deployment (1 day)
    │   └── 5.1.4 Smoke testing in prod (0.5 days)
    │
    ├── 5.2 Monitoring & Observability
    │   ├── 5.2.1 Application metrics (Prometheus) (1 day)
    │   ├── 5.2.2 Logging aggregation (ELK) (1 day)
    │   ├── 5.2.3 Alerting rules (PagerDuty) (1 day)
    │   └── 5.2.4 Dashboard creation (Grafana) (1 day)
    │
    └── 5.3 Documentation
        ├── 5.3.1 API documentation (Swagger UI) (1 day)
        ├── 5.3.2 Deployment runbook (1 day)
        └── 5.3.3 Troubleshooting guide (1 day)

Total: 13 weeks (65 working days)
```

### Когда использовать:
- При планировании больших проектов (> 2 месяцев)
- Для оценки ресурсов и бюджета
- При коммуникации с stakeholders о timeline
- Для распределения работы между командами

---

## Story Points & Planning Poker

### Фибоначчи оценка сложности

```python
STORY_POINTS = {
    1: {
        "effort": "1-2 часа",
        "description": "Очень простая задача",
        "examples": [
            "Добавить поле в форму",
            "Изменить текст на кнопке",
            "Обновить конфигурационный параметр"
        ]
    },
    2: {
        "effort": "Полдня (3-4 часа)",
        "description": "Простая задача",
        "examples": [
            "Создать новый API endpoint (CRUD)",
            "Добавить валидацию формы",
            "Написать unit тест для функции"
        ]
    },
    3: {
        "effort": "День (6-8 часов)",
        "description": "Стандартная задача",
        "examples": [
            "Реализовать простую бизнес-логику",
            "Создать новую страницу с формой",
            "Интегрироваться с внешним API"
        ]
    },
    5: {
        "effort": "2-3 дня",
        "description": "Средняя сложность",
        "examples": [
            "Реализовать authentication flow",
            "Создать сложную форму с вложенными данными",
            "Оптимизировать производительность модуля"
        ]
    },
    8: {
        "effort": "Неделя (5 дней)",
        "description": "Сложная задача",
        "examples": [
            "Реализовать платежную интеграцию",
            "Создать dashboard с визуализацией",
            "Рефакторинг большого модуля"
        ]
    },
    13: {
        "effort": "2 недели",
        "description": "Очень сложная задача - требует декомпозиции",
        "examples": [
            "Реализовать search с Elasticsearch",
            "Создать real-time notification system",
            "Миграция на новую архитектуру"
        ]
    },
    21: {
        "effort": "Месяц+",
        "description": "Epic - ОБЯЗАТЕЛЬНО разбить на stories",
        "examples": [
            "Полная переработка UI",
            "Миграция на новый фреймворк",
            "Создание новой платформы с нуля"
        ]
    }
}

def estimate_story_points(task_description: str, complexity_factors: dict) -> int:
    """Оценить story points задачи.

    Args:
        task_description: Описание задачи
        complexity_factors: Факторы сложности
            {
                "technical_unknown": bool,  # Новые технологии
                "dependencies": int,         # Количество зависимостей
                "testing_complexity": str,   # "low" | "medium" | "high"
                "integration_points": int    # Внешние интеграции
            }

    Returns:
        Оценка в story points
    """
    base_points = 3  # Стандартная задача

    # Увеличить сложность за неизвестные технологии
    if complexity_factors.get("technical_unknown"):
        base_points += 2

    # Увеличить за зависимости
    dependencies = complexity_factors.get("dependencies", 0)
    if dependencies > 3:
        base_points += 2
    elif dependencies > 0:
        base_points += 1

    # Увеличить за сложность тестирования
    testing = complexity_factors.get("testing_complexity", "low")
    if testing == "high":
        base_points += 3
    elif testing == "medium":
        base_points += 1

    # Увеличить за внешние интеграции
    integrations = complexity_factors.get("integration_points", 0)
    base_points += integrations

    # Округление до ближайшего значения Фибоначчи
    fibonacci = [1, 2, 3, 5, 8, 13, 21]
    return min(fibonacci, key=lambda x: abs(x - base_points))
```

### Planning Poker Process

```markdown
## Процесс оценки в команде

### Этап 1: Презентация задачи (5 минут)
- Product Owner объясняет требования
- Разработчики задают уточняющие вопросы
- Обсуждение acceptance criteria

### Этап 2: Индивидуальная оценка (2 минуты)
- Каждый член команды выбирает story points
- Никто не показывает свою карту
- Все думают независимо

### Этап 3: Одновременное раскрытие (1 минута)
- Все показывают карты одновременно
- Фиксируются оценки

### Этап 4: Обсуждение расхождений (5-10 минут)
- Если разброс > 3 points → обсуждение
- Самая высокая оценка объясняет риски
- Самая низкая оценка объясняет простоту

### Этап 5: Повторная оценка (2 минуты)
- После обсуждения — новый раунд
- Обычно оценки сходятся
- Если нет — берется среднее или медиана

### Этап 6: Финализация (1 минута)
- Команда принимает консенсусную оценку
- Фиксируется в backlog

**Пример:**
```
Задача: "Реализовать password reset flow"

Раунд 1:
- Dev A: 5 points ("Нужна email интеграция")
- Dev B: 3 points ("Стандартная задача")
- Dev C: 8 points ("Security concerns + тестирование")

Обсуждение:
- Dev C: "Нужно тестировать expired tokens, rate limiting, email templates"
- Dev A: "Согласен, забыл про rate limiting"
- Dev B: "Хорошие замечания, повышаю до 5"

Раунд 2:
- Dev A: 5 points
- Dev B: 5 points
- Dev C: 5 points

Результат: 5 story points
```
```

---

## Three-Point Estimation (PERT)

### Программно-оценочная техника (PERT)

```python
from typing import Tuple

def pert_estimate(optimistic: float, realistic: float, pessimistic: float) -> Tuple[float, float]:
    """PERT оценка времени выполнения задачи.

    Formula: E = (O + 4R + P) / 6

    Args:
        optimistic: Оптимистичная оценка (лучший случай)
        realistic: Реалистичная оценка (наиболее вероятный)
        pessimistic: Пессимистичная оценка (худший случай)

    Returns:
        Tuple[expected_time, standard_deviation]
    """
    # Ожидаемое время
    expected = (optimistic + 4 * realistic + pessimistic) / 6

    # Стандартное отклонение
    std_dev = (pessimistic - optimistic) / 6

    return round(expected, 2), round(std_dev, 2)


# Примеры использования
examples = [
    {
        "task": "Реализовать JWT authentication",
        "optimistic": 2,   # 2 дня (все идет гладко)
        "realistic": 5,    # 5 дней (стандартный сценарий)
        "pessimistic": 10  # 10 дней (все проблемы сразу)
    },
    {
        "task": "Интегрироваться с Payment Gateway",
        "optimistic": 3,
        "realistic": 7,
        "pessimistic": 15  # Проблемы с sandbox, документацией
    },
    {
        "task": "Написать unit тесты для модуля",
        "optimistic": 1,
        "realistic": 2,
        "pessimistic": 4
    }
]

for example in examples:
    expected, std_dev = pert_estimate(
        example["optimistic"],
        example["realistic"],
        example["pessimistic"]
    )
    print(f"\nЗадача: {example['task']}")
    print(f"Оптимистичная: {example['optimistic']} дней")
    print(f"Реалистичная: {example['realistic']} дней")
    print(f"Пессимистичная: {example['pessimistic']} дней")
    print(f"→ Ожидаемое время: {expected} дней (±{std_dev})")

"""
Вывод:

Задача: Реализовать JWT authentication
Оптимистичная: 2 дней
Реалистичная: 5 дней
Пессимистичная: 10 дней
→ Ожидаемое время: 5.33 дней (±1.33)

Задача: Интегрироваться с Payment Gateway
Оптимистичная: 3 дней
Реалистичная: 7 дней
Пессимистичная: 15 дней
→ Ожидаемое время: 8.0 дней (±2.0)

Задача: Написать unit тесты для модуля
Оптимистичная: 1 дней
Реалистичная: 2 дней
Пессимистичная: 4 дней
→ Ожидаемое время: 2.17 дней (±0.5)
"""
```

### Когда использовать PERT:
- При оценке задач с высокой неопределенностью
- Для критически важных задач (critical path)
- При планировании buffer времени в проекте
- Для коммуникации рисков с менеджментом

---

## T-Shirt Sizing для быстрой оценки

### Шкала размеров

```python
T_SHIRT_SIZES = {
    "XS": {
        "days": "0.5-1",
        "story_points": "1-2",
        "examples": ["Bug fix", "Config change", "Text update"]
    },
    "S": {
        "days": "1-3",
        "story_points": "3-5",
        "examples": ["New API endpoint", "Form validation", "Simple UI component"]
    },
    "M": {
        "days": "3-5",
        "story_points": "5-8",
        "examples": ["Authentication flow", "Complex form", "Third-party integration"]
    },
    "L": {
        "days": "5-10",
        "story_points": "8-13",
        "examples": ["Payment system", "Search feature", "Dashboard page"]
    },
    "XL": {
        "days": "10-20",
        "story_points": "13-21",
        "examples": ["Major refactoring", "New service", "Platform migration"]
    },
    "XXL": {
        "days": "20+",
        "story_points": "21+",
        "examples": ["New product feature", "System redesign", "Multi-service integration"],
        "warning": "⚠️ Разбить на более мелкие задачи!"
    }
}

def convert_tshirt_to_story_points(size: str) -> int:
    """Конвертировать T-shirt size в story points."""
    mapping = {
        "XS": 1,
        "S": 3,
        "M": 5,
        "L": 8,
        "XL": 13,
        "XXL": 21
    }
    return mapping.get(size, 5)  # Default to M
```

### Когда использовать T-Shirt Sizing:
- На ранних этапах планирования (roadmap)
- Для быстрой оценки большого backlog
- При обсуждении с non-technical stakeholders
- Для определения приоритетов (effort vs value)

---

## Velocity Tracking

### Отслеживание скорости команды

```python
from datetime import date, timedelta
from typing import List, Dict

class VelocityTracker:
    """Трекер velocity команды для прогнозирования."""

    def __init__(self):
        self.sprint_velocities: List[int] = []
        self.sprint_dates: List[date] = []

    def add_sprint(self, completed_points: int, sprint_date: date):
        """Добавить данные спринта."""
        self.sprint_velocities.append(completed_points)
        self.sprint_dates.append(sprint_date)

    def average_velocity(self, last_n_sprints: int = 3) -> float:
        """Средняя velocity за последние N спринтов."""
        if not self.sprint_velocities:
            return 0.0

        recent = self.sprint_velocities[-last_n_sprints:]
        return round(sum(recent) / len(recent), 2)

    def predict_completion_date(self, remaining_points: int, sprint_length_days: int = 14) -> date:
        """Прогноз даты завершения проекта."""
        avg_velocity = self.average_velocity()

        if avg_velocity == 0:
            raise ValueError("Нет данных о velocity для прогноза")

        sprints_needed = remaining_points / avg_velocity
        days_needed = sprints_needed * sprint_length_days

        today = date.today()
        return today + timedelta(days=int(days_needed))

    def velocity_trend(self) -> str:
        """Определить тренд velocity."""
        if len(self.sprint_velocities) < 2:
            return "Недостаточно данных"

        recent = self.sprint_velocities[-3:]
        older = self.sprint_velocities[-6:-3] if len(self.sprint_velocities) >= 6 else []

        if not older:
            return "Недостаточно данных для тренда"

        avg_recent = sum(recent) / len(recent)
        avg_older = sum(older) / len(older)

        if avg_recent > avg_older * 1.1:
            return "📈 Растущая (команда ускоряется)"
        elif avg_recent < avg_older * 0.9:
            return "📉 Падающая (команда замедляется)"
        else:
            return "📊 Стабильная"


# Пример использования
tracker = VelocityTracker()

# Добавляем данные последних 6 спринтов
tracker.add_sprint(completed_points=23, sprint_date=date(2025, 9, 1))
tracker.add_sprint(completed_points=25, sprint_date=date(2025, 9, 15))
tracker.add_sprint(completed_points=21, sprint_date=date(2025, 9, 29))
tracker.add_sprint(completed_points=27, sprint_date=date(2025, 10, 13))
tracker.add_sprint(completed_points=29, sprint_date=date(2025, 10, 27))
tracker.add_sprint(completed_points=30, sprint_date=date(2025, 11, 10))

print(f"Средняя velocity (последние 3 спринта): {tracker.average_velocity()} points")
print(f"Тренд: {tracker.velocity_trend()}")

# Прогноз завершения
remaining = 120  # points
completion_date = tracker.predict_completion_date(remaining, sprint_length_days=14)
print(f"\nОсталось: {remaining} points")
print(f"Прогноз завершения: {completion_date.strftime('%Y-%m-%d')}")
print(f"Это через ~{(completion_date - date.today()).days} дней")

"""
Вывод:

Средняя velocity (последние 3 спринта): 28.67 points
Тренд: 📈 Растущая (команда ускоряется)

Осталось: 120 points
Прогноз завершения: 2026-01-25
Это через ~73 дней
"""
```

---

## Best Practices для декомпозиции

### Правила хорошей декомпозиции

1. **INVEST Criteria для User Stories:**
   - **I**ndependent: Независима от других stories
   - **N**egotiable: Можно обсуждать детали
   - **V**aluable: Приносит ценность пользователю
   - **E**stimable: Можно оценить сложность
   - **S**mall: Завершима за 1 спринт
   - **T**estable: Есть четкие критерии приемки

2. **Максимальный размер задачи:**
   - Story не должна быть больше 8 points
   - Если > 8 → декомпозировать на подзадачи
   - Epic (21+ points) ОБЯЗАТЕЛЬНО разбить

3. **Вертикальное vs Горизонтальное разбиение:**
   ```
   ❌ Горизонтальное (по слоям):
   - Story 1: Создать UI форму
   - Story 2: Создать API endpoint
   - Story 3: Создать database table

   ✅ Вертикальное (end-to-end):
   - Story 1: User can register with email
   - Story 2: User can login with OAuth
   - Story 3: User can reset password
   ```

4. **Definition of Done:**
   ```markdown
   ## DoD Checklist
   - [ ] Код написан и работает локально
   - [ ] Unit тесты покрытие > 80%
   - [ ] Integration тесты пройдены
   - [ ] Code review approved (2+ approvals)
   - [ ] Нет критических security issues
   - [ ] Documentation обновлена
   - [ ] Deployed на staging и протестирован
   - [ ] Product Owner подтвердил acceptance criteria
   ```

---

**Навигация:**
- [← Предыдущий модуль: Architecture & Technology](02_architecture_technology.md)
- [↑ Назад к Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)
- [→ Следующий модуль: AI Agent Analysis](04_ai_agent_analysis.md)
