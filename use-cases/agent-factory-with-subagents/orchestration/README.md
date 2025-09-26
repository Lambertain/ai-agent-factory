# 🤖 Система интеллектуальной оркестрации субагентов

Система интеллектуальной оркестрации субагентов предоставляет комплексное решение для координации, планирования и управления выполнением задач между множественными ИИ-агентами.

## 🚀 Основные возможности

### 📋 Умное управление задачами
- **Приоритетная очередь задач** с динамическим назначением приоритетов
- **Планировщик задач** с поддержкой временного планирования
- **Система зависимостей** для сложных рабочих процессов
- **Автоматическая эскалация** приоритетов с течением времени

### ⚖️ Интеллектуальная балансировка нагрузки
- **Множественные стратегии** балансировки (round-robin, least-loaded, capability-based)
- **Адаптивное распределение** на основе производительности агентов
- **Динамическое перебалансирование** при изменении нагрузки
- **Учет возможностей агентов** при назначении задач

### 🔄 Гибкое выполнение
- **Параллельное выполнение** независимых задач
- **Последовательное выполнение** с зависимостями
- **Конвейерное выполнение** (pipeline) для сложных процессов
- **Условное выполнение** на основе результатов

### 📊 Мониторинг и аналитика
- **Реальное время мониторинга** состояния системы
- **Подробные метрики** производительности
- **Система событий** для интеграции с внешними системами
- **Аналитика ошибок** и автоматическое восстановление

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────────┐
│                    AgentOrchestrator                            │
│                  (Центральный координатор)                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌────▼────┐   ┌────▼────┐
│ Queue │    │Scheduler│   │Balancer │
│Manager│    │ Manager │   │ Manager │
└───────┘    └─────────┘   └─────────┘
    │             │             │
┌───▼─────────────▼─────────────▼───┐
│        Execution Engine           │
│     (Параллельное выполнение)     │
└───────────────────────────────────┘
```

### Основные компоненты

1. **AgentOrchestrator** - Центральный координатор системы
2. **PriorityTaskQueue** - Очередь задач с приоритетами
3. **SmartTaskScheduler** - Планировщик с поддержкой зависимостей
4. **TaskDependencyManager** - Управление зависимостями между задачами
5. **SmartLoadBalancer** - Интеллектуальный балансировщик нагрузки
6. **SmartPriorityManager** - Менеджер динамических приоритетов
7. **ParallelExecutionEngine** - Движок параллельного выполнения

## 📦 Установка и настройка

### Требования
- Python 3.8+
- asyncio
- pydantic
- dataclasses (встроенные)

### Быстрый старт

```python
import asyncio
from orchestration import AgentOrchestrator, Task, Agent, TaskPriority, OrchestrationConfig

async def main():
    # Создаем конфигурацию
    config = OrchestrationConfig(
        max_concurrent_tasks=5,
        max_queue_size=100,
        enable_parallel_execution=True,
        enable_load_balancing=True
    )

    # Инициализируем оркестратор
    orchestrator = AgentOrchestrator(config)
    await orchestrator.start()

    try:
        # Регистрируем агента
        agent = Agent(
            id="my-agent-1",
            name="My First Agent",
            type="data-processor",
            capabilities=["processing", "analysis"],
            max_concurrent_tasks=3
        )
        await orchestrator.register_agent(agent)

        # Создаем и отправляем задачу
        task = Task(
            id="my-task-1",
            name="Process Data",
            priority=TaskPriority.HIGH,
            agent_type="data-processor",
            input_data={"file": "data.csv"},
            estimated_duration=30
        )

        task_id = await orchestrator.submit_task(task)
        print(f"Задача {task_id} отправлена!")

        # Мониторим выполнение
        status = await orchestrator.get_task_status(task_id)
        print(f"Статус задачи: {status}")

    finally:
        await orchestrator.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

## 📋 Примеры использования

### Простое создание и выполнение задач

```python
# Создание задачи
task = Task(
    id="analysis-task-001",
    name="Анализ данных продаж",
    description="Провести анализ данных продаж за последний квартал",
    priority=TaskPriority.HIGH,
    agent_type="data-analyst",
    input_data={
        "data_source": "sales_q4_2024.csv",
        "analysis_type": "trend_analysis",
        "output_format": "pdf_report"
    },
    estimated_duration=1800,  # 30 минут
    timeout=3600  # 1 час таймаут
)

# Отправка задачи
task_id = await orchestrator.submit_task(task)
```

### Работа с зависимостями

```python
# Создаем связанные задачи
tasks = [
    Task(id="collect-data", name="Сбор данных", agent_type="collector"),
    Task(id="process-data", name="Обработка данных", agent_type="processor"),
    Task(id="generate-report", name="Генерация отчета", agent_type="reporter")
]

# Устанавливаем зависимости
await orchestrator.dependency_manager.add_dependency("process-data", "collect-data")
await orchestrator.dependency_manager.add_dependency("generate-report", "process-data")

# Отправляем задачи (они выполнятся в правильном порядке)
for task in tasks:
    await orchestrator.submit_task(task)
```

### Управление приоритетами

```python
# Создание задачи с динамическими приоритетами
task = Task(
    id="urgent-analysis",
    name="Срочный анализ",
    priority=TaskPriority.NORMAL,
    agent_type="analyst",
    context={
        "deadline": "2024-12-31T23:59:59Z",  # Дедлайн для автоэскалации
        "business_value": "high",
        "department": "finance"
    }
)

# Ручное повышение приоритета
await orchestrator.priority_manager.escalate_priority(
    task.id,
    "Запрос от руководства"
)
```

### Балансировка нагрузки

```python
# Регистрация нескольких агентов одного типа
for i in range(3):
    agent = Agent(
        id=f"worker-{i}",
        name=f"Worker {i}",
        type="worker",
        capabilities=["processing"],
        max_concurrent_tasks=2,
        success_rate=0.95 + i * 0.01  # Разная производительность
    )
    await orchestrator.register_agent(agent)

# Система автоматически распределит задачи между агентами
tasks = [Task(id=f"task-{i}", agent_type="worker") for i in range(10)]
task_ids = await orchestrator.submit_tasks(tasks)
```

## 🔧 Конфигурация

### OrchestrationConfig

```python
config = OrchestrationConfig(
    max_concurrent_tasks=10,           # Максимум одновременных задач
    max_queue_size=1000,               # Размер очереди задач
    default_task_timeout=300,          # Таймаут по умолчанию (5 мин)
    retry_delays=[1, 5, 15],          # Задержки между попытками
    enable_parallel_execution=True,    # Включить параллельное выполнение
    enable_load_balancing=True,        # Включить балансировку нагрузки
    monitoring_interval=30,            # Интервал мониторинга (сек)
    cleanup_completed_tasks_after=3600 # Очистка завершенных задач (1 час)
)
```

### Настройка приоритетов

```python
# Добавление пользовательского правила приоритета
from orchestration.managers.priority_manager import PriorityRule, PriorityFactor

def business_value_calculator(task: Task) -> float:
    business_value = task.context.get("business_value", "low")
    values = {"low": 0.0, "medium": 1.0, "high": 2.0, "critical": 3.0}
    return values.get(business_value, 0.0)

rule = PriorityRule(
    factor=PriorityFactor.BUSINESS_VALUE,
    weight=0.3,
    calculator=business_value_calculator
)

await orchestrator.priority_manager.add_priority_rule(rule)
```

## 📊 Мониторинг и метрики

### Получение статуса системы

```python
status = await orchestrator.get_system_status()

print(f"Активных агентов: {status['orchestrator']['registered_agents']}")
print(f"Задач в очереди: {status['task_queue']['total_tasks']}")
print(f"Выполняется задач: {status['execution']['active_executions']}")
print(f"Успешных выполнений: {status['metrics']['tasks_completed']}")
print(f"Неудачных выполнений: {status['metrics']['tasks_failed']}")
```

### Подписка на события

```python
async def task_completed_handler(event):
    print(f"Задача {event.data['task_id']} завершена агентом {event.data['agent_id']}")

await orchestrator.subscribe_to_events("task.completed", task_completed_handler)
```

### Метрики производительности

```python
# Статистика очереди
queue_stats = await orchestrator.task_queue.get_queue_stats()
print(f"Утилизация очереди: {queue_stats['queue_utilization']:.1f}%")
print(f"Среднее время ожидания: {queue_stats['average_wait_time']:.1f} сек")

# Статистика планировщика
scheduler_stats = await orchestrator.scheduler.get_scheduler_stats()
print(f"Коэффициент успешности: {scheduler_stats['task_success_rate']:.2%}")

# Статистика балансировщика
balancer_stats = await orchestrator.load_balancer.get_balancer_stats()
print(f"Назначений задач: {balancer_stats['total_assignments']}")
```

## 🛠️ Продвинутые возможности

### Создание планов выполнения

```python
# Создание плана для группы задач
execution_plan = await orchestrator.create_execution_plan(tasks)

print(f"План содержит {len(execution_plan.parallel_groups)} этапов")
print(f"Оценочное время выполнения: {execution_plan.estimated_total_time} сек")

# Выполнение плана
results = await orchestrator.execute_plan(execution_plan)
```

### Обработка ошибок

```python
from orchestration.integrations.error_handler import OrchestrationErrorHandler

# Интеграция обработчика ошибок
error_handler = OrchestrationErrorHandler()

async def error_notification(error_record):
    if error_record["severity"] == "critical":
        # Отправить уведомление администратору
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {error_record['error_message']}")

await error_handler.add_notification_callback(error_notification)
```

### Кастомные стратегии балансировки

```python
async def custom_balancing_strategy(agents: List[Agent], task: Task) -> Agent:
    \"\"\"Пользовательская стратегия балансировки.\"\"\"
    # Выбираем агента с наименьшей нагрузкой и подходящими возможностями
    suitable_agents = [
        agent for agent in agents
        if task.agent_type in agent.capabilities
    ]

    if not suitable_agents:
        return None

    return min(suitable_agents, key=lambda a: a.current_load)

# Использование стратегии в балансировщике
orchestrator.load_balancer._apply_strategy = custom_balancing_strategy
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Запуск всех тестов
python -m pytest orchestration/tests/ -v

# Запуск конкретного теста
python -m pytest orchestration/tests/test_orchestrator.py::TestAgentOrchestrator::test_task_submission -v

# Запуск с покрытием кода
python -m pytest orchestration/tests/ --cov=orchestration --cov-report=html
```

### Пример теста

```python
async def test_custom_orchestration():
    orchestrator = AgentOrchestrator()
    await orchestrator.start()

    try:
        # Тестовая логика
        agent = Agent(id="test-agent", type="test", capabilities=["test"])
        await orchestrator.register_agent(agent)

        task = Task(id="test-task", agent_type="test")
        task_id = await orchestrator.submit_task(task)

        assert task_id == "test-task"

    finally:
        await orchestrator.shutdown()
```

## 🔗 Интеграция с существующими системами

### Интеграция с логированием

```python
import logging

# Настройка логирования для системы оркестрации
logging.getLogger("orchestration").setLevel(logging.INFO)

# Добавление пользовательских логгеров
logger = logging.getLogger("my_app.orchestration")
logger.info("Система оркестрации инициализирована")
```

### Интеграция с метриками

```python
# Экспорт метрик в Prometheus (пример)
async def export_metrics():
    status = await orchestrator.get_system_status()

    # Отправка метрик во внешнюю систему
    metrics = {
        "orchestrator_active_tasks": status["execution"]["active_executions"],
        "orchestrator_queue_size": status["task_queue"]["total_tasks"],
        "orchestrator_success_rate": status["execution"]["success_rate"]
    }

    # Интеграция с вашей системой метрик
    send_to_prometheus(metrics)
```

## 🐛 Отладка и устранение неполадок

### Включение детального логирования

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Отладочные логи для конкретных компонентов
logging.getLogger("orchestration.schedulers").setLevel(logging.DEBUG)
logging.getLogger("orchestration.balancers").setLevel(logging.DEBUG)
```

### Проверка состояния компонентов

```python
# Диагностика системы
async def diagnose_system():
    status = await orchestrator.get_system_status()

    print("=== ДИАГНОСТИКА СИСТЕМЫ ===")
    print(f"Оркестратор запущен: {status['orchestrator']['is_running']}")
    print(f"Время работы: {status['orchestrator']['uptime_seconds']} сек")
    print(f"Зарегистрированных агентов: {status['orchestrator']['registered_agents']}")

    # Проверка очереди
    queue_size = status['task_queue']['total_tasks']
    if queue_size > 100:
        print("⚠️ ВНИМАНИЕ: Очередь задач переполнена")

    # Проверка производительности
    success_rate = status['execution']['success_rate']
    if success_rate < 0.9:
        print("⚠️ ВНИМАНИЕ: Низкий коэффициент успешности")
```

### Частые проблемы и решения

**Проблема**: Задачи не выполняются
- Проверьте, зарегистрированы ли агенты: `await orchestrator.get_available_agents()`
- Убедитесь, что типы агентов соответствуют типам задач
- Проверьте статус агентов (IDLE/BUSY/ERROR)

**Проблема**: Медленное выполнение
- Увеличьте `max_concurrent_tasks` в конфигурации
- Проверьте балансировку нагрузки
- Оптимизируйте алгоритмы агентов

**Проблема**: Ошибки зависимостей
- Проверьте циклические зависимости: `await dependency_manager.detect_circular_dependencies(tasks)`
- Убедитесь, что все зависимые задачи существуют

## 📝 API Reference

### AgentOrchestrator

#### Основные методы
- `start()` - Запуск оркестратора
- `shutdown()` - Остановка оркестратора
- `submit_task(task)` - Отправка задачи
- `submit_tasks(tasks)` - Отправка нескольких задач
- `get_task_status(task_id)` - Получение статуса задачи
- `cancel_task(task_id)` - Отмена задачи
- `register_agent(agent)` - Регистрация агента
- `unregister_agent(agent_id)` - Отмена регистрации агента
- `get_system_status()` - Получение статуса системы

### Task

#### Основные поля
- `id` - Уникальный идентификатор
- `name` - Название задачи
- `priority` - Приоритет (LOW, NORMAL, HIGH, URGENT, CRITICAL)
- `agent_type` - Тип требуемого агента
- `input_data` - Входные данные
- `estimated_duration` - Оценочное время выполнения
- `timeout` - Таймаут выполнения
- `context` - Дополнительный контекст

### Agent

#### Основные поля
- `id` - Уникальный идентификатор
- `name` - Название агента
- `type` - Тип агента
- `capabilities` - Список возможностей
- `supported_tasks` - Поддерживаемые типы задач
- `max_concurrent_tasks` - Максимум одновременных задач
- `status` - Статус (IDLE, BUSY, ERROR, UNAVAILABLE)

## 🤝 Вклад в развитие

Мы приветствуем вклад в развитие системы оркестрации! Пожалуйста:

1. Создайте fork репозитория
2. Создайте ветку для вашей функции
3. Добавьте тесты для новой функциональности
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для деталей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте документацию и примеры
2. Изучите секцию "Отладка и устранение неполадок"
3. Создайте issue в репозитории с подробным описанием проблемы
4. Приложите логи и конфигурацию системы

---

**Система интеллектуальной оркестрации субагентов** - мощный инструмент для координации ИИ-агентов в сложных рабочих процессах. Используйте её для создания эффективных, масштабируемых и надежных систем автоматизации! 🚀