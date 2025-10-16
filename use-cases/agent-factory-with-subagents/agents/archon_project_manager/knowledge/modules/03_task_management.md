# Module 03: Task Management

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Создание новой задачи
- Обновление статуса задачи
- Приоритизация задач (task_order)
- Определение dependency graph
- Эскалация непрофильных задач
- Управление блокерами
- Переход задачи между статусами (todo/doing/review/done)
- Анализ critical path

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** задача, приоритет, task_order, зависимости, блокер, эскалация, статус задачи, критический путь

**English:** task, priority, task_order, dependencies, blocker, escalation, task status, critical path

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Нужно создать новую задачу с правильным приоритетом
- Задача заблокирована или требует эскалации
- Определение какую задачу выполнять следующей
- Анализ зависимостей между задачами
- Выбор правильного статуса после завершения работы

---

## 📋 СОЗДАНИЕ ЗАДАЧ

### Стандартная структура задачи

```python
await mcp__archon__manage_task(
    action="create",
    project_id=project_id,          # ОБЯЗАТЕЛЬНО
    title="Краткое название задачи",
    description="Детальное описание с acceptance criteria",
    assignee="Archon Project Manager",  # Имя агента
    status="todo",                   # todo/doing/review/done
    task_order=50,                   # 0-100 (выше = приоритетнее)
    feature="authentication"         # Группировка по фичам
)
```

### ПОСЛЕ создания любой задачи

```python
# ОБЯЗАТЕЛЬНО вызвать приоритизацию
await analyze_and_prioritize_tasks(project_id)
```

### ПЕРЕД началом выполнения задачи

```python
# ОБЯЗАТЕЛЬНО проверить актуальность приоритета
await validate_task_priority(task_id)
```

---

## 🎯 ИНТЕЛЛЕКТУАЛЬНАЯ ПРИОРИТИЗАЦИЯ

### Алгоритм автоматического task_order

```python
async def analyze_and_prioritize_tasks(project_id: str):
    """
    Автоматическая приоритизация всех задач проекта.

    Факторы приоритета:
    1. Блокирует ли других (highest)
    2. Критический путь проекта
    3. Количество зависимых задач
    4. Срочность (doing > review > todo)
    5. Экспертиза исполнителя
    """

    # 1. Получить ВСЕ задачи проекта
    all_tasks = await mcp__archon__find_tasks(project_id=project_id)

    # 2. Построить dependency graph
    graph = build_dependency_graph(all_tasks)

    # 3. Определить critical path
    critical_path = find_critical_path(graph)

    # 4. Вычислить приоритеты
    priorities = {}

    for task in all_tasks:
        score = 0

        # Задачи в работе = highest priority
        if task["status"] == "doing":
            score += 100

        # На ревью = high priority
        elif task["status"] == "review":
            score += 80

        # Блокирует других
        blockers = count_blocked_tasks(task, graph)
        score += blockers * 10

        # На critical path
        if task["id"] in critical_path:
            score += 30

        # Количество зависимых задач
        dependents = count_dependents(task, graph)
        score += dependents * 5

        priorities[task["id"]] = min(score, 100)  # Макс 100

    # 5. Обновить task_order для всех задач
    for task_id, priority in priorities.items():
        await mcp__archon__manage_task(
            action="update",
            task_id=task_id,
            task_order=priority
        )

    return priorities
```

### Dependency Graph Example

```
Task A (auth backend) - task_order: 90
  ↓ blocks
Task B (auth frontend) - task_order: 70
  ↓ blocks
Task C (protected routes) - task_order: 50
  ↓ blocks
Task D (user dashboard) - task_order: 30

Critical Path: A → B → C → D
```

---

## 🔄 СТАТУСЫ ЗАДАЧ И ПЕРЕХОДЫ

### Жизненный цикл задачи

```
┌──────┐
│ todo │ ← Создана, ожидает выполнения
└───┬──┘
    ↓ start work
┌───────┐
│ doing │ ← В процессе выполнения
└───┬───┘
    ↓ completed
┌────────┐
│ review │ ← Требует проверки эксперта
└───┬────┘
    ↓ approved
┌──────┐
│ done │ ← Полностью завершена
└──────┘
```

### Гибкое управление статусами

**ПОСЛЕ завершения работы, выбрать статус:**

```python
# СЦЕНАРИЙ 1: Полностью выполнена ✅
if task_completed_successfully and no_issues_found:
    status = "done"
    description = original_description + "\n\n✅ Выполнено успешно"

# СЦЕНАРИЙ 2: Требует проверки 🔍
elif task_completed_but_needs_review:
    status = "review"
    description = original_description + "\n\n🔍 На проверке у эксперта"

# СЦЕНАРИЙ 3: Нужна эскалация ⚠️
elif needs_escalation_or_help:
    status = "doing"  # Остается в работе
    description = original_description + "\n\n⚠️ ТРЕБУЕТСЯ ЭСКАЛАЦИЯ: [причина]"
    # Создать задачу для помощи
    await escalate_to_expert(task_id, reason)

# СЦЕНАРИЙ 4: Заблокирована 🚫
elif task_blocked:
    status = "doing"
    description = original_description + "\n\n🚫 БЛОКЕР: [описание]\nОжидает: [что нужно]"
```

### Таблица статусов

| Статус | Когда использовать | Приоритет |
|--------|-------------------|-----------|
| `done` | Все требования выполнены, проблем нет | - |
| `review` | Работа выполнена, нужна проверка эксперта | High |
| `doing` + эскалация | В процессе столкнулись с проблемой вне компетенции | Highest |
| `doing` + блокер | Не может быть завершена из-за внешних факторов | Highest |
| `todo` | Новая задача, ожидает начала работы | Normal |

---

## 🚨 ЭСКАЛАЦИЯ НЕПРОФИЛЬНЫХ ЗАДАЧ

### Правило эскалации

**ОБЯЗАТЕЛЬНО ЭСКАЛИРОВАТЬ ЕСЛИ:**

1. **Получил непрофильную задачу изначально**
2. **В ПРОЦЕССЕ выполнения профильной задачи** выявилась необходимость в работе вне специализации

### Алгоритм эскалации

```python
async def escalate_task(original_task_id: str, target_agent: str, reason: str):
    """
    Эскалировать задачу правильному агенту.

    Args:
        original_task_id: ID оригинальной задачи
        target_agent: Имя агента, который должен выполнить
        reason: Причина эскалации
    """

    # 1. Получить оригинальную задачу
    task = await mcp__archon__find_tasks(task_id=original_task_id)

    # 2. Создать новую задачу для правильного агента
    new_task = await mcp__archon__manage_task(
        action="create",
        project_id=task["project_id"],
        assignee=target_agent,
        title=f"⚠️ ЭСКАЛАЦИЯ: {task['title']}",
        description=f"""
Эскалировано от: {task['assignee']}
Причина: {reason}

ОРИГИНАЛЬНОЕ ОПИСАНИЕ:
{task['description']}
        """,
        feature=task.get("feature"),
        task_order=task["task_order"] + 10  # Выше приоритет
    )

    # 3. Обновить оригинальную задачу
    await mcp__archon__manage_task(
        action="update",
        task_id=original_task_id,
        status="doing",
        description=task["description"] + f"""

⚠️ ЭСКАЛИРОВАНО: {target_agent}
🔗 Новая задача: {new_task['id']}
📋 Причина: {reason}
        """
    )

    # 4. Уведомить пользователя
    print(f"⚠️ Задача эскалирована: {target_agent}")
    print(f"🔗 Новая задача ID: {new_task['id']}")

    return new_task
```

### Примеры эскалации

**Пример 1: Непрофильная задача изначально**

```
Implementation Engineer получил: "Протестируй новый API"

→ НЕ выполнять
→ escalate_task(task_id, "Quality Guardian", "Тестирование вне моей компетенции")
→ Сообщить: "Задача передана Quality Guardian для тестирования"
```

**Пример 2: Эскалация В ПРОЦЕССЕ работы**

```
Implementation Engineer работает: "Подключить QR-сканирование в бекенде"

→ Выяснил: нужен UI компонент для сканера
→ escalate_task(task_id, "UIUX Enhancement Agent", "Требуется UI компонент")
→ Продолжить: только backend логику QR-сканирования
→ Сообщить: "Создана дополнительная задача для UI компонента"
```

---

## 🔄 ПРИОРИТЕТ ЗАДАЧ В НОВОЙ СЕССИИ

### Правильный порядок выполнения

```python
async def get_next_task(my_role: str, project_id: str) -> dict:
    """
    Получить следующую задачу с ПРАВИЛЬНЫМ приоритетом.

    ПРИОРИТЕТ:
    1. doing - незавершенная работа (может блокировать других)
    2. review - требует проверки (может блокировать следующие задачи)
    3. todo - новые задачи (только когда нет doing и review)
    """

    # ПРИОРИТЕТ 1: Незавершенная работа (doing)
    doing_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="doing"
    )
    my_doing = [t for t in doing_tasks if t["assignee"] == my_role]
    if my_doing:
        task = max(my_doing, key=lambda t: t["task_order"])
        print(f"🔄 ПРИОРИТЕТ 1: Продолжаю незавершенную: {task['title']}")
        return task

    # ПРИОРИТЕТ 2: Задачи на ревью (review)
    review_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="review"
    )
    my_review = [t for t in review_tasks if t["assignee"] == my_role]
    if my_review:
        task = max(my_review, key=lambda t: t["task_order"])
        print(f"🔍 ПРИОРИТЕТ 2: Проверяю на ревью: {task['title']}")
        return task

    # ПРИОРИТЕТ 3: Новые задачи (todo)
    todo_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )
    my_todo = [t for t in todo_tasks if t["assignee"] == my_role]
    if my_todo:
        task = max(my_todo, key=lambda t: t["task_order"])
        print(f"📋 ПРИОРИТЕТ 3: Начинаю новую: {task['title']}")
        return task

    print("✅ Нет задач для выполнения")
    return None
```

### Таблица приоритетов

| Приоритет | Статус | Значение | Почему |
|-----------|--------|----------|--------|
| **1** | `doing` | Незавершенная работа | Может блокировать других |
| **2** | `review` | Требует проверки | Может блокировать следующие задачи |
| **3** | `todo` | Новые задачи | Берем только когда нет doing и review |

---

## 🎯 BEST PRACTICES

### Atomic Tasks
- Создавать задачи, выполнимые за 1-4 часа
- Если задача больше → разбить на подзадачи
- Каждая задача должна иметь четкий acceptance criteria

### Clear Descriptions
```markdown
# Хорошее описание задачи

## Цель
Что должно быть сделано и зачем

## Acceptance Criteria
- [ ] Критерий 1
- [ ] Критерий 2
- [ ] Критерий 3

## Технические детали
- Технологии: Python, FastAPI
- Файлы: src/auth.py, tests/test_auth.py
- Зависимости: Task ID 123 должна быть выполнена первой
```

### Use Features
```python
# Группировка задач по фичам
await mcp__archon__manage_task(
    action="create",
    feature="authentication",  # Все задачи auth будут связаны
    title="Implement JWT tokens"
)

await mcp__archon__manage_task(
    action="create",
    feature="authentication",
    title="Add password reset"
)
```

### Track Progress
```python
# Обновлять статус по мере работы
await mcp__archon__manage_task(
    action="update",
    task_id=task_id,
    status="doing"  # Начал работу
)

# После завершения
await mcp__archon__manage_task(
    action="update",
    task_id=task_id,
    status="done",
    description=original + "\n\n✅ Выполнено: все критерии соблюдены"
)
```

---

**Навигация:**
- [← Предыдущий модуль: Project Management](02_project_management.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Context Recovery](04_context_recovery.md)
