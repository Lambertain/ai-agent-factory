# Руководство по коллективной работе агентов

## Обзор

Система коллективной работы обеспечивает автоматическую координацию между Pydantic AI агентами через:
- Разбивку задач на микрозадачи
- Отчетность о прогрессе
- Рефлексию и улучшение результатов
- Делегирование задач между агентами
- Обязательные финальные шаги (Git + Archon)

## Быстрый старт

### 1. Создание агента с коллективными инструментами

```python
from agents.common.pydantic_ai_decorators import create_universal_pydantic_agent

# Создание агента с автоматическими интеграциями
agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=YourDependencies,
    system_prompt="Твоя экспертиза...",
    agent_type="your_agent_type",
    knowledge_tags=["your-agent", "domain"],
    with_collective_tools=True,  # Автоматически добавляет инструменты
    with_knowledge_tool=True
)
```

### 2. Использование инструментов в агенте

Агенты автоматически получают следующие инструменты:

#### `break_down_to_microtasks` - Разбивка на микрозадачи

```python
# Вызов агентом автоматически через инструменты
# Пользователь видит:
📋 **Микрозадачи для выполнения:**
1. Анализ сложности задачи
2. Поиск в базе знаний
3. Определение необходимости делегирования
4. Реализация основной части
5. Критический анализ результата
6. Улучшение и финализация

✅ Буду отчитываться о прогрессе каждой микрозадачи
```

#### `report_microtask_progress` - Отчет о прогрессе

```python
# Агент сообщает о прогрессе каждой микрозадачи
✅ **Микрозадача 1** (completed): Анализ сложности задачи
   Детали: Задача средней сложности, требует 4 этапа
```

#### `reflect_and_improve` - Рефлексия и улучшение

```python
# Обязательно в конце каждой задачи
🔍 **Критический анализ выполненной работы:**

**Найденные недостатки:**
1. [Конкретный недостаток 1]
2. [Конкретный недостаток 2]

**Внесенные улучшения:**
- [Улучшение 1]
- [Улучшение 2]

✅ Универсальность (0% проект-специфичного кода)
✅ Модульность (файлы до 500 строк)
```

#### `check_delegation_need` - Проверка делегирования

```python
# Агент автоматически проверяет нужно ли делегировать
🤝 **Рекомендуется делегирование:**
- Security Audit Agent - для проверки безопасности
- UI/UX Enhancement Agent - для работы с интерфейсом
```

#### `delegate_task_to_agent` - Делегирование задачи

```python
# Создание задачи для другого агента
✅ Задача успешно делегирована агенту security_audit:
- Assignee: Security Audit Agent
- Приоритет: high
- Статус: создана в Archon
```

## Обязательный рабочий процесс агента

### Шаг 1: Получение и разбивка задачи

```python
async def run_agent_task(user_message: str, deps: Dependencies) -> str:
    # Агент автоматически создает микрозадачи через инструмент
    # break_down_to_microtasks() вызывается LLM автоматически

    # Пользователь видит план работы
    result = await agent.run(user_message, deps=deps)
    return result.data
```

### Шаг 2: Выполнение с отчетностью

```python
# Агент автоматически использует report_microtask_progress()
# для каждой выполненной микрозадачи

# Пользователь видит прогресс:
✅ Микрозадача 1 выполнена - Анализ требований
⏳ Микрозадача 2 в процессе - Поиск в базе знаний
```

### Шаг 3: Проверка делегирования

```python
# Агент вызывает check_delegation_need() для анализа
# Если найдены задачи для других агентов - делегирует через
# delegate_task_to_agent()
```

### Шаг 4: Рефлексия и улучшение

```python
# ОБЯЗАТЕЛЬНО перед завершением
# Агент вызывает reflect_and_improve()

# Находит недостатки и улучшает результат
```

### Шаг 5: Обязательные финальные шаги

```python
# Автоматически через run_with_integrations():
# 1. Git коммит создается
# 2. Статус в Archon обновляется
# 3. Отчет показывается пользователю
```

## Интеграция через декораторы

### Автоматический способ (рекомендуется)

```python
from agents.common.pydantic_ai_integrations import run_with_integrations

async def run_your_agent(user_message: str, api_key: str) -> str:
    deps = YourDependencies(api_key=api_key)

    # Все интеграции применяются автоматически
    result = await run_with_integrations(
        agent=your_agent,
        user_message=user_message,
        deps=deps,
        agent_type="your_agent_type"
    )

    return result  # Уже строка, не result.data
```

### Ручной способ (для особых случаев)

```python
from agents.common.collective_work_tools import (
    break_down_to_microtasks,
    report_microtask_progress,
    reflect_and_improve
)

# Использование инструментов вручную в коде агента
# (не рекомендуется, используйте автоматический способ)
```

## Матрица компетенций агентов

Система автоматически определяет какие агенты лучше подходят для задач:

| Агент | Компетенции |
|-------|-------------|
| Security Audit | безопасность, уязвимости, compliance, аудит |
| UI/UX Enhancement | дизайн, интерфейс, accessibility, UX |
| Performance Optimization | производительность, оптимизация, профилирование |
| RAG Agent | поиск информации, семантический анализ |
| TypeScript Architecture | типизация, архитектура, рефакторинг |
| Prisma Database | база данных, SQL, схемы, миграции |
| PWA Mobile | PWA, мобильная разработка, offline |

## Пример полного цикла работы

```python
from agents.common.pydantic_ai_decorators import create_universal_pydantic_agent
from agents.common.pydantic_ai_integrations import run_with_integrations

# 1. Создание агента
agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=Dependencies,
    system_prompt="...",
    agent_type="example_agent",
    with_collective_tools=True  # Автоматически добавляет инструменты
)

# 2. Запуск с полными интеграциями
async def run_example_task(user_message: str) -> str:
    deps = Dependencies(api_key="...")

    result = await run_with_integrations(
        agent=agent,
        user_message=user_message,
        deps=deps,
        agent_type="example_agent"
    )

    return result

# Что происходит автоматически:
# 1. Разбивка на микрозадачи (показывается пользователю)
# 2. Проверка делегирования (создаются задачи если нужно)
# 3. Выполнение с отчетностью о каждой микрозадаче
# 4. Рефлексия и улучшение результата
# 5. Git коммит с изменениями
# 6. Обновление статуса в Archon
```

## Конфигурация интеграций

### Включение/отключение отдельных интеграций

```python
from agents.common.pydantic_ai_integrations import pydantic_ai_integration

# Отключить автопереключение к PM
pydantic_ai_integration.enabled_integrations["pm_switch"] = False

# Отключить Git коммиты
pydantic_ai_integration.enabled_integrations["git_commits"] = False

# Доступные интеграции:
# - "pm_switch": автопереключение к Project Manager
# - "competency_check": проверка компетенций и делегирование
# - "microtask_planning": планирование микрозадач
# - "git_commits": автоматические Git коммиты
# - "russian_localization": русская локализация
```

## Обязательные финальные шаги

### Автоматический способ (через run_with_integrations)

```python
# Все финальные шаги выполняются автоматически:
# - Git коммит
# - Обновление Archon
# - Отчет пользователю

result = await run_with_integrations(
    agent=agent,
    user_message=message,
    deps=deps,
    agent_type="your_agent"
)
# Финальные шаги уже выполнены автоматически
```

### Ручной способ (если не используете run_with_integrations)

```python
from agents.common.pydantic_ai_integrations import execute_mandatory_final_steps

# В конце каждой задачи
final_result = await execute_mandatory_final_steps(
    task_description="Описание выполненной задачи",
    agent_type="your_agent_type",
    task_id="archon_task_id",  # Опционально
    task_status="done",
    notes="Дополнительные заметки"
)

print(final_result)  # ОБЯЗАТЕЛЬНО показать пользователю
```

## Критерии завершения задачи

Задача может быть отмечена как выполненная ТОЛЬКО если:

- ✅ Микрозадачи были выведены пользователю в начале
- ✅ Прогресс каждой микрозадачи был отображен
- ✅ Выполнена полная рефлексия с выявлением недостатков
- ✅ Найденные недостатки были устранены
- ✅ Результат соответствует всем критериям качества
- ✅ Рефлексия показана пользователю
- ✅ **Git коммит создан**
- ✅ **Статус в Archon обновлен**

## Лучшие практики

### 1. Всегда используйте create_universal_pydantic_agent

```python
# ✅ Правильно
agent = create_universal_pydantic_agent(
    with_collective_tools=True  # Автоматически добавляет инструменты
)

# ❌ Неправильно
agent = Agent(...)  # Нужно вручную добавлять инструменты
```

### 2. Всегда используйте run_with_integrations

```python
# ✅ Правильно
result = await run_with_integrations(agent, message, deps, agent_type)

# ❌ Неправильно
result = await agent.run(message, deps=deps)  # Нет интеграций
```

### 3. Убедитесь что agent_type указан правильно

```python
# ✅ Правильно
agent_type="security_audit_agent"  # Соответствует AGENT_COMPETENCIES

# ❌ Неправильно
agent_type="security"  # Не распознается системой делегирования
```

### 4. Проверяйте финальные шаги

```python
# ✅ Правильно
final_report = await execute_mandatory_final_steps(...)
print(final_report)  # Показываем пользователю

# ❌ Неправильно
await execute_mandatory_final_steps(...)  # Не показали результат
```

## Troubleshooting

### Проблема: Инструменты не добавляются автоматически

**Решение:** Используйте `create_universal_pydantic_agent` вместо `Agent()`

```python
# Вместо:
agent = Agent(model, deps_type, system_prompt)

# Используйте:
agent = create_universal_pydantic_agent(
    model, deps_type, system_prompt,
    with_collective_tools=True
)
```

### Проблема: Делегирование не работает

**Решение:** Проверьте что agent_type указан правильно и есть в AGENT_COMPETENCIES

```python
from agents.common.collective_work_tools import AGENT_COMPETENCIES

# Проверьте ваш agent_type
print(list(AGENT_COMPETENCIES.keys()))
```

### Проблема: Git коммиты не создаются

**Решение:** Используйте `run_with_integrations` или вызывайте финальные шаги вручную

```python
# Автоматический способ
result = await run_with_integrations(...)

# Или ручной
await execute_mandatory_final_steps(...)
```

### Проблема: Archon не обновляется

**Решение:** Передайте task_id в финальные шаги

```python
await execute_mandatory_final_steps(
    task_description="...",
    agent_type="...",
    task_id="your_archon_task_id"  # ОБЯЗАТЕЛЬНО
)
```

## Заключение

Система коллективной работы обеспечивает:
- 📋 Автоматическое планирование через микрозадачи
- 📊 Прозрачность прогресса для пользователя
- 🤝 Интеллектуальное делегирование между агентами
- 🔍 Обязательную рефлексию и улучшение
- 🎯 Стандартизированные финальные шаги (Git + Archon)

Следуя этому руководству, все агенты будут работать в едином стиле с максимальной эффективностью и прозрачностью.
