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

## 🔥 HOT TASK CREATION STRATEGY

### Проблема: "Гарячі" задачі губляться в todo черзі

**СТАРЫЙ workflow:**
```
1. Користувач: "Критичний баг в production!"
2. PM: Створює задачу в todo (status="todo")
3. PM: Читає todo задачі → шукає щойно створену
4. PM: Приоритизує → переміщує в doing
5. Агент: Читає doing → починає роботу

3,000+ токенів на операції пошуку та переміщення
```

**НОВЫЙ workflow з hot_task:**
```
1. Користувач: "Критичний баг в production!"
2. PM: Створює задачу ОДРАЗУ в doing (hot_task=True)
3. Агент: Бачить задачу в doing → негайно починає роботу

0 токенів на пошук та переміщення
```

**Економія токенів: 100% на hot task операціях (3,000 → 0)**

---

### Критерії "гарячої" задачі

**СТВОРЮЙ задачу в doing (hot_task=True) ЯКЩО:**

✅ **Критичний баг в production**
- Порушує роботу сервісу
- Впливає на користувачів
- Потребує негайного виправлення

✅ **Блокує роботу команди**
- Інші агенти не можуть працювати
- Блокує critical path
- Затримує releas

✅ **Терміновий дедлайн**
- Потрібно виконати сьогодні
- Потрібно виконати завтра
- Фіксована дата поза нашим контролем

✅ **Залежність для інших задач**
- 3+ задачі залежать від цієї
- Блокує весь feature
- Критичний компонент архітектури

✅ **Рефакторинг потрібен ЗАРАЗ**
- Блокує розробку нових фіч
- Технічний борг став критичним
- Міграція на нову архітектуру (приклад: ці 4 задачі міграції агентів)

**СТВОРЮЙ задачу в todo ЯКЩО:**

❌ **Звичайна feature розробка**
- Може почекати тиждень+
- Не блокує інших
- Планова розробка

❌ **Потребує дослідження/планування спочатку**
- Не зрозуміло як реалізовувати
- Потрібен аналіз вимог
- Потрібен design document

❌ **Невизначений пріоритет**
- "Було б непогано зробити..."
- "Колись потрібно буде..."
- "Якщо буде час..."

---

### Реализация create_hot_task()

```python
async def create_hot_task(
    project_id: str,
    title: str,
    description: str,
    assignee: str,
    task_order: int = 100,
    **kwargs
) -> dict:
    """
    Створити "гарячу" задачу (одразу в doing, НЕ в todo).

    Використовуй для критичних/термінових задач:
    - Критичні баги в production
    - Блокери роботи команди
    - Терміновий дедлайн (сьогодні/завтра)
    - Залежність для багатьох задач
    - Рефакторинг що потрібен ЗАРАЗ

    Args:
        project_id: ID проекта
        title: Назва задачі
        description: Детальний опис
        assignee: Ім'я агента-виконавця
        task_order: Пріоритет 0-100 (за замовчуванням 100 = highest)
        **kwargs: Додаткові поля (feature, etc.)

    Returns:
        dict: Створена задача з status="doing"

    Token Savings: 100% на hot task операціях (3,000 → 0 токенів)

    Examples:
        >>> # Критичний баг
        >>> await create_hot_task(
        ...     project_id=project_id,
        ...     title="🔥 КРИТИЧНО: Auth не працює на production",
        ...     description="Користувачі не можуть залогінитись...",
        ...     assignee="Implementation Engineer",
        ...     task_order=100,
        ...     feature="authentication"
        ... )

        >>> # Блокер команди
        >>> await create_hot_task(
        ...     project_id=project_id,
        ...     title="🔥 БЛОКЕР: Database migration провалилась",
        ...     description="Команда не може працювати з БД...",
        ...     assignee="Deployment Engineer",
        ...     task_order=100
        ... )
    """

    # Створюємо задачу ОДРАЗУ в doing, НЕ в todo
    task = await mcp__archon__manage_task(
        "create",
        project_id=project_id,
        title=f"🔥 {title}",  # Маркер "гарячої" задачі
        description=f"""**⚡ ГАРЯЧА ЗАДАЧА (створена в doing)**

{description}

---

**Причина Hot Task:**
Критична/термінова - потребує негайного виконання.
Створена одразу в doing для економії часу та токенів.
        """,
        assignee=assignee,
        status="doing",  # ← КЛЮЧОВА ВІДМІННІСТЬ від звичайного create!
        task_order=task_order,
        **kwargs
    )

    # Логування
    print(f"🔥 Створено гарячу задачу в doing: {title}")
    print(f"   Assignee: {assignee}")
    print(f"   Priority: {task_order}")
    print(f"   Status: doing (одразу готова до виконання)")

    return task
```

---

### Приклади використання

**Приклад 1: Критичний баг в production**

```python
# User повідомляє PM про критичний баг
user_message = "Користувачі не можуть залогінитись на production! Терміново!"

# PM розпізнає критичність → створює hot task
await create_hot_task(
    project_id=project_id,
    title="КРИТИЧНО: Auth не працює на production",
    description="""
**Проблема:**
Користувачі отримують 500 error при логіні

**Impact:**
- 100% користувачів не можуть залогінитись
- Production повністю недоступний для auth

**Acceptance Criteria:**
- [ ] Знайти root cause
- [ ] Виправити баг
- [ ] Верифікувати на production
- [ ] Post-mortem analysis
    """,
    assignee="Implementation Engineer",
    task_order=100,  # Highest priority
    feature="authentication"
)

# Результат:
# 🔥 Створено гарячу задачу в doing: КРИТИЧНО: Auth не працює на production
#    Assignee: Implementation Engineer
#    Priority: 100
#    Status: doing (одразу готова до виконання)

# Implementation Engineer бачить задачу в doing → негайно починає роботу
# Економія: 3,000 токенів (не потрібно шукати та переміщати з todo)
```

**Приклад 2: Блокер роботи команди**

```python
# Deployment Engineer виявив проблему
await create_hot_task(
    project_id=project_id,
    title="БЛОКЕР: Docker контейнери не стартують",
    description="""
**Проблема:**
Docker Compose не може запустити контейнери через конфлікт портів

**Impact:**
- Вся команда не може працювати локально
- Блокує 5 задач в doing
- Блокує тестування

**Root Cause:**
Порти 5432 та 6379 зайняті іншими процесами

**Acceptance Criteria:**
- [ ] Звільнити порти
- [ ] Оновити docker-compose.yml
- [ ] Верифікувати запуск на всіх машинах команди
    """,
    assignee="Deployment Engineer",
    task_order=100
)
```

**Приклад 3: Терміновий дедлайн**

```python
# PM дізнався про новий requirement з фіксованою датою
await create_hot_task(
    project_id=project_id,
    title="ТЕРМІНВО: GDPR compliance до завтра 17:00",
    description="""
**Deadline:** Завтра 17:00 (24 години)

**Requirement:**
Додати cookie consent banner для EU користувачів

**Legal Impact:**
Без цього не можемо працювати в EU з 01.12.2025

**Acceptance Criteria:**
- [ ] Cookie consent banner UI
- [ ] Cookie consent tracking
- [ ] Privacy policy update
- [ ] Legal team approval
    """,
    assignee="UIUX Enhancement Agent",
    task_order=100,
    feature="compliance"
)
```

**Приклад 4: Залежність для багатьох задач**

```python
# Виявили що 5 задач залежать від однієї
await create_hot_task(
    project_id=project_id,
    title="DEPENDENCY: Реалізувати shared API client",
    description="""
**Блокує задачі:**
1. Task #123: User API integration
2. Task #124: Payment API integration
3. Task #125: Analytics API integration
4. Task #126: Notification API integration
5. Task #127: Search API integration

**Impact:**
5 задач не можуть стартувати без цього

**Acceptance Criteria:**
- [ ] Shared API client class
- [ ] Authentication handling
- [ ] Error handling
- [ ] Retry logic
- [ ] Unit tests
    """,
    assignee="Implementation Engineer",
    task_order=100,
    feature="infrastructure"
)
```

**Приклад 5: Рефакторинг потрібен ЗАРАЗ (реальний кейс)**

```python
# PM розпочинає міграцію агентів на NEW workflow
await create_hot_task(
    project_id=project_id,
    title="РЕФАКТОРИНГ: Міграція archon_project_manager на NEW workflow",
    description="""
**Причина терміновості:**
Блокує міграцію інших 33 агентів

**NEW workflow benefits:**
- 89% економія токенів (15,500 → 1,600 на задачу)
- Контекстно-залежне читання модулів
- common_agent_rules.md для всіх агентів

**Acceptance Criteria:**
- [ ] Створити system_prompt.md (компактний)
- [ ] Створити module_selection.md
- [ ] Оновити 8 модулів
- [ ] Тестування контекстного читання
- [ ] Git commit + push
    """,
    assignee="Implementation Engineer",
    task_order=100,
    feature="agent_refactoring"
)

# Це саме та задача, яку ми виконуємо зараз!
# Створена як hot_task через критичність для всієї системи
```

---

### Інтеграція в workflow

**Коли користувач повідомляє про проблему:**

```python
# 1. Аналіз критичності
if is_critical_or_urgent(user_message):
    # HOT TASK: створюємо одразу в doing
    task = await create_hot_task(
        project_id=project_id,
        title=extract_title(user_message),
        description=extract_description(user_message),
        assignee=determine_assignee(user_message),
        task_order=100
    )
    print(f"🔥 Створено hot task - готова до негайного виконання")

else:
    # NORMAL TASK: створюємо в todo
    task = await mcp__archon__manage_task(
        "create",
        project_id=project_id,
        title=extract_title(user_message),
        description=extract_description(user_message),
        assignee=determine_assignee(user_message),
        status="todo",  # Буде приоритизована пізніше
        task_order=50
    )
    print(f"📋 Створено задачу в todo - буде приоритизована")
```

---

### Коли НЕ використовувати hot_task

**ПОМИЛКА: Занадто багато hot tasks**

```python
# ❌ НЕПРАВИЛЬНО - все створюємо як hot
await create_hot_task(title="Додати кнопку 'Like'")  # Не критично!
await create_hot_task(title="Змінити колір header")  # Не терміново!
await create_hot_task(title="Рефакторинг tests")  # Може почекати!

# Результат: doing переповнене, нічого не критичне
```

**ПРАВИЛЬНО: Тільки справді критичні**

```python
# ✅ ПРАВИЛЬНО - лише hot tasks
await create_hot_task(title="🔥 КРИТИЧНО: Auth не працює")  # Production!
await create_hot_task(title="🔥 БЛОКЕР: Database migration провалилась")  # Команда!

# ✅ ПРАВИЛЬНО - звичайні tasks
await mcp__archon__manage_task(
    "create",
    title="Додати кнопку 'Like'",
    status="todo"  # Буде приоритизована пізніше
)
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

## 🚀 BATCH TASK MOVEMENT STRATEGY

### Проблема: Многократное чтение todo задач

**СТАРЫЙ workflow:**
```
1. Читаю todo → выбираю 1 задачу → пользователь подтверждает → перемещаю в doing
2. Читаю todo → выбираю 1 задачу → пользователь подтверждает → перемещаю в doing
3. Читаю todo → выбираю 1 задачу → пользователь подтверждает → перемещаю в doing
...
5 сессий × 5,000 токенов на чтение = 25,000 токенов
```

**НОВЫЙ workflow с batch переміщенням:**
```
1. Читаю todo ОДИН РАЗ
2. Автоматическая приоритизация ВСЕХ задач
3. Показываю топ-5 релевантных задач пользователю
4. После подтверждения: переміщаю ВСЕ 5 в doing ОДНОВРЕМЕННО

1 сессия × 7,500 токенов = 7,500 токенов
```

**Економія токенів: 70% (25,000 → 7,500)**

---

### Реализация batch movement

```python
async def prioritize_and_batch_move_tasks(project_id: str) -> dict:
    """
    Project Manager workflow з batch переміщенням задач в doing.

    Оптимизирует работу за счет:
    1. Одноразового чтения todo задач
    2. Автоматической приоритизации
    3. Batch переміщення топ-5 релевантних задач

    Args:
        project_id: ID проекта

    Returns:
        dict: {
            "moved": int - количество перемещенных задач,
            "tasks": list - перемещенные задачи
        }

    Token Savings: 70% (25,000 → 7,500 токенов на 5 задач)
    """

    # 1. Прочитать todo задачи (ОДИН РАЗ!)
    todo_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )

    if not todo_tasks:
        print("✅ Нет задач в todo")
        return {"moved": 0, "tasks": []}

    # 2. Автоматическая приоритизация
    # Сортуємо за task_order (найвищі пріоритети першими)
    prioritized = sorted(
        todo_tasks,
        key=lambda t: t.get("task_order", 0),
        reverse=True
    )

    # 3. Вибрати топ-5 релевантних задач
    # Використовуємо стратегії: feature / assignee / task_order
    top_5_tasks = select_batch_tasks(prioritized, max_count=5)

    # 4. Показати користувачу для підтвердження
    print("🎯 Топ-5 задач для batch переміщення в doing:")
    print("=" * 60)
    for i, task in enumerate(top_5_tasks, 1):
        assignee = task.get("assignee", "Не назначена")
        feature = task.get("feature", "Общая")
        priority = task.get("task_order", 0)

        print(f"{i}. [{assignee}] {task['title']}")
        print(f"   Feature: {feature}")
        print(f"   Priority: {priority}")
        print()

    print("=" * 60)

    # 5. ПОСЛЕ ПОДТВЕРЖДЕНИЯ: переміщуємо ВСІ 5 в doing одночасно
    # (Подтверждение происходит в основном workflow Project Manager)
    for task in top_5_tasks:
        await mcp__archon__manage_task(
            "update",
            task_id=task["id"],
            status="doing"
        )

    print(f"✅ Перенесено {len(top_5_tasks)} задач в doing")

    return {
        "moved": len(top_5_tasks),
        "tasks": top_5_tasks
    }


def select_batch_tasks(tasks: list, max_count: int = 5) -> list:
    """
    Вибрати batch задач за релевантністю.

    Використовує 3 стратегії:
    1. Same feature - задачі з однаковою feature
    2. Same assignee - задачі для одного виконавця
    3. Top by task_order - просто топ-N за пріоритетом

    Args:
        tasks: Список задач (відсортованих за task_order DESC)
        max_count: Максимальна кількість задач в batch

    Returns:
        list: Batch задач для переміщення

    Examples:
        >>> tasks = [
        ...     {"feature": "auth", "assignee": "Engineer", "task_order": 90},
        ...     {"feature": "auth", "assignee": "Engineer", "task_order": 85},
        ...     {"feature": "auth", "assignee": "Quality", "task_order": 80},
        ... ]
        >>> select_batch_tasks(tasks, 5)
        [3 auth tasks]  # Стратегія 1: same feature
    """

    if not tasks:
        return []

    # Стратегія 1: Якщо є задачі з однаковою feature - взяти їх
    top_task = tasks[0]
    if top_task.get("feature"):
        same_feature = [
            t for t in tasks
            if t.get("feature") == top_task["feature"]
        ][:max_count]

        if len(same_feature) >= 3:
            print(f"📦 Стратегія 1: Same feature '{top_task['feature']}' ({len(same_feature)} задач)")
            return same_feature

    # Стратегія 2: Якщо є задачі для одного assignee - взяти їх
    same_assignee = [
        t for t in tasks
        if t.get("assignee") == top_task.get("assignee")
    ][:max_count]

    if len(same_assignee) >= 3:
        print(f"👤 Стратегія 2: Same assignee '{top_task.get('assignee')}' ({len(same_assignee)} задач)")
        return same_assignee

    # Стратегія 3: Просто топ-N за task_order
    print(f"🎯 Стратегія 3: Top-{max_count} за task_order")
    return tasks[:max_count]
```

### Приклади використання

**Сценарій 1: Same feature batch**

```python
# Project має 10 todo задач, 5 з них feature="authentication"
result = await prioritize_and_batch_move_tasks(project_id)

# Вивід:
# 📦 Стратегія 1: Same feature 'authentication' (5 задач)
# 🎯 Топ-5 задач для batch переміщення:
# 1. [Implementation Engineer] Implement JWT tokens
#    Feature: authentication | Priority: 90
# 2. [Implementation Engineer] Add password reset API
#    Feature: authentication | Priority: 85
# 3. [Quality Guardian] Test authentication flow
#    Feature: authentication | Priority: 80
# 4. [Deployment Engineer] Setup auth env variables
#    Feature: authentication | Priority: 75
# 5. [Implementation Engineer] Add refresh token logic
#    Feature: authentication | Priority: 70
#
# ✅ Перенесено 5 задач в doing
```

**Сценарій 2: Same assignee batch**

```python
# Project має 8 todo задач, 4 для Implementation Engineer
result = await prioritize_and_batch_move_tasks(project_id)

# Вивід:
# 👤 Стратегія 2: Same assignee 'Implementation Engineer' (4 задачі)
# 🎯 Топ-5 задач для batch переміщення:
# (показує 4 задачі для одного виконавця)
```

**Сценарій 3: Top-N за пріоритетом**

```python
# Project має 15 todo задач, різні features та assignees
result = await prioritize_and_batch_move_tasks(project_id)

# Вивід:
# 🎯 Стратегія 3: Top-5 за task_order
# (показує топ-5 найпріоритетніших задач)
```

---

### Інтеграція в Project Manager Workflow

**Workflow після активації Project Manager:**

```python
# 1. Користувач активує Project Manager
user_input = "archon-project-manager"

# 2. PM показує список проектів + PROJECTS_REGISTRY
projects = await show_projects_from_registry()

# 3. Користувач вибирає проект
selected_project = user_input  # "AI Agent Factory"

# 4. PM валідує опис проекта (Module 02)
validate_project_description(selected_project)

# 5. PM читає DOING та REVIEW задачі
doing_tasks = await find_tasks(status="doing")
review_tasks = await find_tasks(status="review")

# 6. Якщо є doing/review - показати їх
if doing_tasks or review_tasks:
    show_active_work(doing_tasks, review_tasks)

# 7. НОВИЙ КРОК: Batch переміщення todo → doing
if not doing_tasks:  # Якщо немає задач в роботі
    result = await prioritize_and_batch_move_tasks(selected_project)

    if result["moved"] > 0:
        print(f"🚀 Готові {result['moved']} задач для виконання")
        print("Команда може приступати до роботи!")
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
