# Module 05: Agile Methodologies

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Sprint planning (планирование спринта)
- Daily standup (ежедневная синхронизация)
- Backlog grooming (приоритизация бэклога)
- Sprint retrospective (ретроспектива спринта)
- Sprint report (отчет по спринту)
- Определение sprint goals
- Velocity tracking (отслеживание скорости)

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** спринт, sprint planning, daily standup, backlog, retrospective, sprint report, velocity, agile, scrum

**English:** sprint, sprint planning, daily standup, backlog grooming, retrospective, sprint report, velocity, agile, scrum

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Начало нового спринта
- Ежедневные синхронизации команды
- Завершение спринта и планирование следующего
- Анализ продуктивности команды
- Оптимизация процессов разработки

---

## 🏃 AGILE FRAMEWORK ДЛЯ ARCHON

### Адаптация Scrum для мультиагентной команды

```
SPRINT CYCLE (2 недели):

День 1: Sprint Planning
├─ Определить sprint goal
├─ Выбрать задачи из backlog
├─ Декомпозировать на подзадачи
└─ Распределить между агентами

День 2-13: Daily Standups
├─ Что сделано вчера
├─ Что планируется сегодня
├─ Есть ли блокеры
└─ Приоритизация задач

День 14: Sprint Review + Retrospective
├─ Демо выполненных задач
├─ Анализ velocity
├─ Обсуждение улучшений
└─ Planning следующего спринта
```

---

## 📋 SPRINT PLANNING

### Workflow планирования спринта

```python
async def conduct_sprint_planning(project_id: str, sprint_number: int):
    """
    Провести sprint planning для проекта.

    Args:
        project_id: UUID проекта
        sprint_number: Номер спринта

    Returns:
        dict: Sprint plan с целями и задачами
    """

    print(f"🏃 SPRINT PLANNING: Sprint #{sprint_number}")
    print("━" * 50)

    # ЭТАП 1: Определить sprint goal
    sprint_goal = define_sprint_goal(project_id)
    print(f"\n🎯 Sprint Goal: {sprint_goal}")

    # ЭТАП 2: Получить backlog
    backlog = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )
    print(f"\n📋 Backlog: {len(backlog)} задач")

    # ЭТАП 3: Приоритизировать задачи
    prioritized = await analyze_and_prioritize_tasks(project_id)

    # ЭТАП 4: Выбрать задачи для спринта (по capacity)
    sprint_capacity = calculate_team_capacity()
    selected_tasks = select_sprint_tasks(prioritized, sprint_capacity)

    print(f"\n✅ Выбрано для спринта: {len(selected_tasks)} задач")

    # ЭТАП 5: Распределить между агентами
    for task in selected_tasks:
        agent = assign_task_to_agent(task)
        await mcp__archon__manage_task(
            action="update",
            task_id=task["id"],
            assignee=agent,
            feature=f"Sprint-{sprint_number}"
        )

    # ЭТАП 6: Создать sprint report
    sprint_plan = {
        "sprint_number": sprint_number,
        "goal": sprint_goal,
        "start_date": today(),
        "end_date": today() + timedelta(days=14),
        "tasks": selected_tasks,
        "capacity": sprint_capacity
    }

    return sprint_plan
```

### Sprint Goal Definition

```python
def define_sprint_goal(project_id: str) -> str:
    """
    Определить цель спринта на основе приоритетов.

    Примеры sprint goals:
    - "Завершить аутентификацию и авторизацию"
    - "Реализовать основные CRUD операции"
    - "Подготовить MVP к демо"
    - "Исправить критические баги production"
    """

    # Анализ высокоприоритетных задач
    top_tasks = get_top_priority_tasks(project_id, limit=5)

    # Определить общую тему
    common_theme = extract_common_theme(top_tasks)

    # Сформулировать SMART цель
    sprint_goal = f"Реализовать {common_theme} с высоким качеством"

    return sprint_goal
```

---

## 🗣️ DAILY STANDUP

### Структура ежедневной синхронизации

```python
async def conduct_daily_standup(project_id: str):
    """
    Провести daily standup для команды.

    Returns:
        dict: Отчет о прогрессе и блокерах
    """

    print("🗣️ DAILY STANDUP")
    print("━" * 50)

    # Получить всех агентов проекта
    agents = get_project_agents(project_id)

    standup_report = {
        "date": today(),
        "completed": [],
        "in_progress": [],
        "planned": [],
        "blockers": []
    }

    for agent in agents:
        print(f"\n👤 {agent}")

        # ЧТО СДЕЛАНО ВЧЕРА
        completed = await mcp__archon__find_tasks(
            project_id=project_id,
            filter_by="assignee",
            filter_value=agent
        )
        completed = [t for t in completed if t["status"] == "done" and is_yesterday(t["updated_at"])]
        standup_report["completed"].extend(completed)
        print(f"✅ Завершено: {len(completed)} задач")

        # ЧТО В РАБОТЕ
        in_progress = await mcp__archon__find_tasks(
            project_id=project_id,
            filter_by="assignee",
            filter_value=agent
        )
        in_progress = [t for t in in_progress if t["status"] == "doing"]
        standup_report["in_progress"].extend(in_progress)
        print(f"🔄 В работе: {len(in_progress)} задач")

        # ЧТО ПЛАНИРУЕТСЯ
        planned = await mcp__archon__find_tasks(
            project_id=project_id,
            filter_by="assignee",
            filter_value=agent
        )
        planned = [t for t in planned if t["status"] == "todo"]
        planned = sorted(planned, key=lambda t: t["task_order"], reverse=True)[:3]
        standup_report["planned"].extend(planned)
        print(f"📋 Планируется: {len(planned)} задач")

        # БЛОКЕРЫ
        blockers = [t for t in in_progress if "БЛОКЕР" in t.get("description", "")]
        standup_report["blockers"].extend(blockers)
        if blockers:
            print(f"🚫 БЛОКЕРЫ: {len(blockers)}")
            for blocker in blockers:
                print(f"   - {blocker['title']}")

    # ПРИОРИТИЗАЦИЯ на сегодня
    await analyze_and_prioritize_tasks(project_id)

    return standup_report
```

### Шаблон daily standup ответа

```markdown
🗣️ DAILY STANDUP - 2025-10-16
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Analysis Lead
✅ Вчера: Завершен анализ требований к API (#123)
🔄 Сегодня: Декомпозиция задач по аутентификации (#125)
📋 Планируется: Создание документации архитектуры (#127)

👤 Implementation Engineer
✅ Вчера: Реализован JWT token handler (#134)
🔄 Сегодня: Интеграция с database (#135)
🚫 БЛОКЕР: Нужны миграции БД от Blueprint Architect

👤 Quality Guardian
✅ Вчера: Написаны тесты для auth module (#140)
🔄 Сегодня: Code review PR#12
📋 Планируется: E2E тестирование авторизации (#142)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 ПРИОРИТЕТ СЕГОДНЯ: Разблокировать Implementation Engineer
→ Blueprint Architect должен создать миграции БД первым
```

---

## 📊 BACKLOG GROOMING

### Регулярная приоритизация backlog

```python
async def conduct_backlog_grooming(project_id: str):
    """
    Провести grooming session для backlog.

    Цели:
    - Приоритизировать задачи
    - Оценить сложность
    - Разбить большие задачи
    - Удалить устаревшие
    """

    print("📊 BACKLOG GROOMING")
    print("━" * 50)

    # Получить весь backlog
    backlog = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )

    grooming_results = {
        "prioritized": 0,
        "split": 0,
        "archived": 0,
        "clarified": 0
    }

    for task in backlog:
        # 1. Проверить актуальность
        if is_outdated(task):
            await archive_task(task["id"])
            grooming_results["archived"] += 1
            continue

        # 2. Проверить описание
        if needs_clarification(task):
            await clarify_task_requirements(task["id"])
            grooming_results["clarified"] += 1

        # 3. Проверить размер
        if is_too_large(task):
            subtasks = split_task(task)
            for subtask in subtasks:
                await mcp__archon__manage_task(
                    action="create",
                    project_id=project_id,
                    **subtask
                )
            grooming_results["split"] += 1

        # 4. Приоритизировать
        await mcp__archon__manage_task(
            action="update",
            task_id=task["id"],
            task_order=calculate_priority(task)
        )
        grooming_results["prioritized"] += 1

    print(f"\n✅ Grooming завершен:")
    print(f"   Приоритизировано: {grooming_results['prioritized']}")
    print(f"   Разбито: {grooming_results['split']}")
    print(f"   Архивировано: {grooming_results['archived']}")
    print(f"   Уточнено: {grooming_results['clarified']}")

    return grooming_results
```

---

## 🔄 SPRINT RETROSPECTIVE

### Анализ и улучшения после спринта

```python
async def conduct_sprint_retrospective(project_id: str, sprint_number: int):
    """
    Провести ретроспективу спринта.

    Returns:
        dict: Insights и action items
    """

    print(f"🔄 SPRINT RETROSPECTIVE: Sprint #{sprint_number}")
    print("━" * 50)

    # Получить задачи спринта
    sprint_tasks = await get_sprint_tasks(project_id, sprint_number)

    # Анализ выполнения
    completed = [t for t in sprint_tasks if t["status"] == "done"]
    incomplete = [t for t in sprint_tasks if t["status"] != "done"]

    completion_rate = len(completed) / len(sprint_tasks) * 100

    print(f"\n📊 МЕТРИКИ:")
    print(f"   Завершено: {len(completed)}/{len(sprint_tasks)} ({completion_rate:.1f}%)")
    print(f"   Velocity: {calculate_velocity(completed)} story points")

    # Что хорошо (Keep)
    keeps = analyze_what_went_well(sprint_tasks)
    print(f"\n✅ ЧТО ХОРОШО:")
    for keep in keeps:
        print(f"   • {keep}")

    # Что не хорошо (Problems)
    problems = analyze_problems(sprint_tasks)
    print(f"\n⚠️ ПРОБЛЕМЫ:")
    for problem in problems:
        print(f"   • {problem}")

    # Что улучшить (Actions)
    actions = generate_action_items(problems)
    print(f"\n🎯 ACTION ITEMS:")
    for i, action in enumerate(actions, 1):
        print(f"   {i}. {action}")
        # Создать задачи для action items
        await mcp__archon__manage_task(
            action="create",
            project_id=project_id,
            title=f"[PROCESS] {action}",
            assignee="Archon Project Manager",
            task_order=90  # High priority
        )

    retrospective = {
        "sprint": sprint_number,
        "completion_rate": completion_rate,
        "velocity": calculate_velocity(completed),
        "keeps": keeps,
        "problems": problems,
        "actions": actions
    }

    return retrospective
```

---

## 📈 VELOCITY TRACKING

### Отслеживание продуктивности команды

```python
def calculate_team_velocity(project_id: str, sprints_count: int = 3):
    """
    Вычислить среднюю velocity команды за последние спринты.

    Args:
        project_id: UUID проекта
        sprints_count: Количество спринтов для анализа

    Returns:
        float: Средняя velocity (story points per sprint)
    """

    velocities = []

    for sprint in range(1, sprints_count + 1):
        sprint_tasks = get_sprint_tasks(project_id, sprint)
        completed = [t for t in sprint_tasks if t["status"] == "done"]
        velocity = sum(t.get("story_points", 1) for t in completed)
        velocities.append(velocity)

    average_velocity = sum(velocities) / len(velocities)

    print(f"📈 VELOCITY ANALYSIS:")
    print(f"   Last {sprints_count} sprints: {velocities}")
    print(f"   Average: {average_velocity:.1f} story points/sprint")

    return average_velocity
```

---

## 📋 SPRINT REPORT

### Автоматический отчет по спринту

```python
async def generate_sprint_report(project_id: str, sprint_number: int):
    """
    Создать подробный отчет по спринту.

    Returns:
        str: Markdown отчет
    """

    sprint_tasks = await get_sprint_tasks(project_id, sprint_number)
    completed = [t for t in sprint_tasks if t["status"] == "done"]
    in_progress = [t for t in sprint_tasks if t["status"] == "doing"]
    incomplete = [t for t in sprint_tasks if t["status"] == "todo"]

    report = f"""
# Sprint #{sprint_number} Report

**Дата:** {today()}
**Проект:** {get_project_name(project_id)}

## 📊 Итоги

- **Завершено:** {len(completed)}/{len(sprint_tasks)} задач ({len(completed)/len(sprint_tasks)*100:.1f}%)
- **В работе:** {len(in_progress)} задач
- **Не начато:** {len(incomplete)} задач
- **Velocity:** {calculate_velocity(completed)} story points

## ✅ Завершенные задачи

{format_tasks_list(completed)}

## 🔄 Задачи в работе (carry over)

{format_tasks_list(in_progress)}

## 📋 Незавершенные задачи

{format_tasks_list(incomplete)}

## 🎯 Достижения

- Реализовано {len([t for t in completed if t.get("feature") == "authentication"])} задач по аутентификации
- Закрыто {len([t for t in completed if "bug" in t.get("title", "").lower()])} багов
- Code coverage: {get_coverage_percentage()}%

## ⚠️ Блокеры и проблемы

{list_sprint_blockers(sprint_tasks)}

## 📈 Следующий спринт

**Приоритеты:**
1. Завершить задачи в работе (carry over)
2. Реализовать [следующая фича]
3. Исправить критические баги

**Capacity:** {calculate_team_capacity()} story points
"""

    return report
```

---

## 🎯 BEST PRACTICES

### Agile принципы для Archon

1. **Регулярные синхронизации** - Daily standups предотвращают блокеры
2. **Короткие итерации** - Спринты 2 недели для быстрой адаптации
3. **Приоритизация** - Всегда работать над самым важным
4. **Ретроспективы** - Постоянное улучшение процессов
5. **Прозрачность** - Все видят прогресс и проблемы

### Адаптация для AI команды

```python
# Агенты работают асинхронно - важна координация
async def coordinate_agents():
    """Координировать работу агентов в спринте."""

    # 1. Определить зависимости задач
    dependency_graph = build_dependency_graph()

    # 2. Запустить независимые задачи параллельно
    independent_tasks = find_independent_tasks(dependency_graph)
    await asyncio.gather(*[execute_task(t) for t in independent_tasks])

    # 3. После завершения - запустить зависимые
    dependent_tasks = find_dependent_tasks(dependency_graph)
    await execute_dependent_tasks(dependent_tasks)
```

---

**Навигация:**
- [← Предыдущий модуль: Context Recovery](04_context_recovery.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Examples & Templates](06_examples_templates.md)
