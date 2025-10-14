# Module 01: QA Architecture & Process

**Назад к:** [Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)

---

## 🔄 ОБЯЗАТЕЛЬНАЯ СИСТЕМА КОНТРОЛЯ КАЧЕСТВА

**КАЖДЫЙ АУДИТ ПРОХОДИТ 3 ЭТАПА:**

### ЭТАП 1: АУДИТ

**Действия:**
1. Получить запрос на аудит кода/агента/проекта
2. Провести детальную проверку по чек-листу:
   - Соответствие архитектуре
   - Размеры файлов (<500 строк)
   - Наличие обязательных файлов (workflow.py, knowledge/, README.md)
   - Качество кода и документации
   - Тесты и валидация
3. Сформировать детальный отчет с найденными проблемами
4. Перейти к ЭТАПУ 2

**Выход:** Список проблем с приоритизацией

---

### ЭТАП 2: СОЗДАНИЕ ЗАДАЧ

**Действия:**
1. Для КАЖДОЙ проблемы из аудита создать задачу в Archon
2. Использовать шаблон:
   ```
   Название: [Компонент]: [Проблема]
   Описание:
   - Что не так
   - Путь к файлу
   - Референс к правильному примеру
   - Критерии завершения
   Приоритет: P1-Critical/P2-High/P3-Medium
   Исполнитель: [роль]
   ```
3. Назначить на правильного исполнителя:
   - Архитектурные проблемы → Blueprint Architect
   - Проблемы кода → Implementation Engineer
   - Проблемы документации → Analysis Lead
   - DevOps проблемы → Deployment Engineer

**Выход:** Набор задач в Archon с назначенными исполнителями

---

### ЭТАП 3: РЕАЛИЗАЦИЯ ИСПРАВЛЕНИЙ

**Действия:**
1. Исполнители получают задачи из Archon
2. Каждый исполнитель работает над своими задачами
3. Quality Guardian проверяет выполненные исправления
4. При необходимости создает follow-up задачи
5. После всех исправлений - финальный аудит

**Выход:** Проект соответствует стандартам качества

---

## Архитектура Quality Guardian

```
┌─────────────────────────────────────────────────────────────┐
│                    Quality Guardian Agent                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │  Code Review  │  │    Static     │  │   Performance   │ │
│  │    Module     │  │   Analysis    │  │    Testing      │ │
│  └───────┬───────┘  └───────┬───────┘  └────────┬────────┘ │
│          │                  │                     │          │
│          └──────────────────┴─────────────────────┘          │
│                             │                                │
│                   ┌─────────▼──────────┐                    │
│                   │  Quality Metrics   │                    │
│                   │    Aggregator      │                    │
│                   └─────────┬──────────┘                    │
│                             │                                │
│          ┌──────────────────┼──────────────────┐            │
│          │                  │                  │            │
│  ┌───────▼───────┐  ┌──────▼──────┐  ┌────────▼────────┐  │
│  │   Archon MCP  │  │   Reports   │  │  CI/CD Pipeline │  │
│  │  Integration  │  │  Generator  │  │   Integration   │  │
│  └───────────────┘  └─────────────┘  └─────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Основные компоненты:

1. **Code Review Module:**
   - AI-powered review с Claude Sonnet 4
   - Статический анализ кода
   - Проверка соответствия стандартам

2. **Static Analysis:**
   - Интеграция с pylint, flake8, mypy, bandit
   - Интеграция с eslint, tsc, snyk для TypeScript
   - Автоматическое обнаружение code smells

3. **Performance Testing:**
   - Load testing и stress testing
   - Профилирование производительности
   - Мониторинг метрик

4. **Quality Metrics Aggregator:**
   - Сбор и агрегация всех метрик
   - Расчет общей оценки качества
   - Трекинг технического долга

5. **Archon MCP Integration:**
   - Создание задач для исправлений
   - Трекинг прогресса
   - Приоритизация проблем

6. **Reports Generator:**
   - Автоматическая генерация отчетов
   - Dashboard с метриками
   - Trend analysis

7. **CI/CD Pipeline Integration:**
   - GitHub Actions integration
   - GitLab CI integration
   - Автоматические проверки качества

---

## Workflow стадии качества

### PRE_COMMIT_STAGE: Проверки перед коммитом

```python
PRE_COMMIT_STAGE = {
    "stage_name": "Pre-Commit",
    "checks": [
        {
            "name": "Code Formatting",
            "tools": ["black", "isort", "prettier"],
            "blocking": True,
            "auto_fix": True
        },
        {
            "name": "Type Checking",
            "tools": ["mypy", "tsc"],
            "blocking": True,
            "auto_fix": False
        },
        {
            "name": "Linting",
            "tools": ["pylint", "flake8", "eslint"],
            "blocking": True,
            "auto_fix": True
        },
        {
            "name": "Security Scan",
            "tools": ["bandit", "snyk"],
            "blocking": True,
            "auto_fix": False
        },
        {
            "name": "Unit Tests",
            "tools": ["pytest", "jest"],
            "blocking": True,
            "auto_fix": False,
            "min_coverage": 80
        }
    ],
    "execution": "local",
    "max_duration_seconds": 60
}
```

**Цель:** Блокировать коммит если есть критические проблемы

**Когда срабатывает:** При попытке сделать git commit

**Действия при проблемах:**
- Auto-fix для форматирования (black, prettier)
- Блокировка коммита при ошибках типизации
- Блокировка при security issues
- Блокировка при падении тестов

---

### PULL_REQUEST_STAGE: Проверки при создании PR

```python
PULL_REQUEST_STAGE = {
    "stage_name": "Pull Request",
    "checks": [
        {
            "name": "AI Code Review",
            "tool": "claude-sonnet-4",
            "blocking": False,
            "creates_comments": True
        },
        {
            "name": "Integration Tests",
            "tools": ["pytest", "jest"],
            "blocking": True,
            "auto_fix": False
        },
        {
            "name": "E2E Tests",
            "tools": ["playwright", "cypress"],
            "blocking": False,
            "auto_fix": False
        },
        {
            "name": "Performance Tests",
            "tools": ["locust", "k6"],
            "blocking": False,
            "auto_fix": False,
            "thresholds": {
                "p95_latency_ms": 500,
                "error_rate_percent": 1
            }
        },
        {
            "name": "Security Audit",
            "tools": ["snyk", "trivy"],
            "blocking": True,
            "auto_fix": False
        },
        {
            "name": "Code Coverage",
            "tools": ["coverage", "jest-coverage"],
            "blocking": True,
            "auto_fix": False,
            "min_coverage": 80,
            "min_branch_coverage": 75
        }
    ],
    "execution": "ci_cd",
    "max_duration_seconds": 600,
    "parallel_execution": True
}
```

**Цель:** Комплексная проверка перед мержем

**Когда срабатывает:** При создании или обновлении Pull Request

**Действия при проблемах:**
- AI review оставляет комментарии с предложениями
- Блокировка мержа при падении integration tests
- Блокировка при security vulnerabilities
- Warning при недостаточном покрытии

---

### POST_MERGE_STAGE: Проверки после мержа

```python
POST_MERGE_STAGE = {
    "stage_name": "Post-Merge",
    "checks": [
        {
            "name": "Smoke Tests",
            "tools": ["pytest", "jest"],
            "blocking": False,
            "auto_rollback": True
        },
        {
            "name": "Performance Monitoring",
            "tools": ["prometheus", "datadog"],
            "blocking": False,
            "auto_rollback": True,
            "alerts": [
                {
                    "metric": "p95_latency",
                    "threshold": 1000,
                    "unit": "ms"
                },
                {
                    "metric": "error_rate",
                    "threshold": 5,
                    "unit": "percent"
                }
            ]
        },
        {
            "name": "Deployment Verification",
            "tools": ["kubectl", "docker"],
            "blocking": False,
            "auto_rollback": True
        }
    ],
    "execution": "production",
    "max_duration_seconds": 300,
    "rollback_on_failure": True
}
```

**Цель:** Мониторинг production после деплоя

**Когда срабатывает:** После мержа в main/master branch

**Действия при проблемах:**
- Автоматический rollback при критических ошибках
- Alerts в Slack/PagerDuty
- Создание incident task в Archon

---

## Best Practices для QA процесса

### 1. Автоматизация над ручными проверками
- Автоматизируй все что можно автоматизировать
- Используй pre-commit hooks для быстрого feedback loop
- CI/CD должен быть максимально быстрым (<10 минут)

### 2. Fail Fast принцип
- Самые быстрые проверки первыми
- Блокируй рано если есть критические проблемы
- Не трать время на E2E если unit tests падают

### 3. Измеримые метрики
- Каждая проверка должна давать численный результат
- Трекай метрики во времени
- Устанавливай конкретные пороги (80% coverage, 0 security issues)

### 4. Continuous Improvement
- Регулярно review false positives
- Добавляй новые проверки по мере роста проекта
- Настраивай пороги на основе данных

---

**Навигация:**
- [↑ Назад к Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)
- [→ Следующий модуль: Metrics & Quality Models](02_metrics_quality_models.md)
