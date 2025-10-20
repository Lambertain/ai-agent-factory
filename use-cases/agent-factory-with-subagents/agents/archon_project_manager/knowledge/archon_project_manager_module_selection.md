# Archon Project Manager - Module Selection Logic

**Version:** 1.1
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Purpose:** Intelligent module selection based on task keywords and context

**Changes in v1.1 (2025-10-20):**
- Added Module 08: Quick Task Selection Protocol (CRITICAL priority)
- Renamed old Module 08 to Module 09: Agent Refactoring Check
- Updated total modules: 8 → 9
- Updated statistics: average 2.8 → 3.0 modules per task
- Updated Priority Validation: added Module 08 (70% load frequency)
- Updated all examples and best practices
- Total Knowledge: ~1,800 → ~2,100 lines

---

## 📊 Module Overview

| # | Module | Priority | Domain | Load When |
|---|--------|----------|--------|-----------|
| **01** | [MCP Critical Rules](modules/01_mcp_critical_rules.md) | 🔴 CRITICAL | Archon MCP operations | MCP, Archon API tasks |
| **02** | [Project Management](modules/02_project_management.md) | 🟡 HIGH | Project lifecycle | Project creation, planning |
| **03** | [Task Management](modules/03_task_management.md) | 🔴 CRITICAL | Task operations | Task creation, prioritization |
| **04** | [Context Recovery](modules/04_context_recovery.md) | 🟡 HIGH | Context restoration | Auto-compact, context loss |
| **05** | [Agile Methodologies](modules/05_agile_methodologies.md) | 🟢 MEDIUM | Sprint/Scrum | Sprint planning, backlog |
| **06** | [Examples Templates](modules/06_examples_templates.md) | 🟢 MEDIUM | Templates | Need examples |
| **07** | [Refactoring Workflow](modules/07_refactoring_workflow.md) | 🟡 HIGH | Agent refactoring | Token optimization |
| **08** | [Quick Task Selection](modules/08_quick_task_selection_protocol.md) | 🔴 CRITICAL | Task selection | Default PM workflow |
| **09** | [Agent Refactoring Check](modules/09_agent_refactoring_check.md) | 🟢 MEDIUM | Progress tracking | Role switching, checklist |

**Total Knowledge:** ~2,100 lines in modules + ~550 tokens system prompt

**Priority Legend:**
- 🔴 **CRITICAL** - Load frequency: 70-80% of tasks
- 🟡 **HIGH** - Load frequency: 50-60% of tasks
- 🟢 **MEDIUM** - Load frequency: 30-40% of tasks

---

## 📦 Module 01: MCP Critical Rules

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Работа с Archon MCP Server API
- Создание/обновление задач через MCP
- Получение проектов/задач из Archon
- Проблемы с MCP tools

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* mcp, archon, api, сервер, проект, задача, создать, получить, обновить

*English:* mcp, archon, api, server, project, task, create, get, update

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- mcp__archon__find_projects()
- mcp__archon__find_tasks()
- mcp__archon__manage_task()
- PROJECTS_REGISTRY.md чтение
- Token optimization через registry

**Примеры задач:**
- "Получить список задач проекта"
- "Создать новую задачу через Archon"
- "Обновить статус задачи на done"

---

## 📦 Module 02: Project Management

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Создание новых проектов
- Планирование проектов
- Управление lifecycle проекта
- Multi-project coordination

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* проект, создать проект, управление проектами, планирование, инициация, завершение

*English:* project, create project, project management, planning, initiation, completion

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Project lifecycle stages
- Multi-project coordination
- Project documentation
- Dependency management

**Примеры задач:**
- "Создать новый проект в Archon"
- "Спланировать этапы проекта"
- "Управлять несколькими проектами"

---

## 📦 Module 03: Task Management

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание задач
- Приоритизация задач
- Назначение задач агентам
- Управление task_order
- Dependency resolution

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* задача, задачи, создать задачу, приоритет, назначить, task_order, зависимости

*English:* task, tasks, create task, priority, assign, task_order, dependencies

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Intelligent task prioritization
- task_order calculation
- Dependency graph analysis
- Critical path determination
- Team workload balancing

**Примеры задач:**
- "Создать задачу для Implementation Engineer"
- "Приоритизировать задачи проекта"
- "Назначить задачи команде"

---

## 📦 Module 04: Context Recovery

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- После auto-compact (потеря контекста)
- Восстановление project_id
- Recovery protocols
- PROJECTS_REGISTRY.md usage

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* контекст, восстановление, auto-compact, потеря, registry, project_id

*English:* context, recovery, auto-compact, loss, registry, project_id

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Context loss detection
- PROJECTS_REGISTRY.md parsing
- Fallback to MCP when registry unavailable
- Project context restoration

**Примеры задач:**
- "Восстановить контекст проекта"
- "Определить активный project_id"
- "Восстановить после auto-compact"

---

## 📦 Module 05: Agile Methodologies

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Sprint planning
- Backlog grooming
- Daily standups
- Agile/Scrum processes

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* agile, scrum, спринт, бэклог, планирование спринта, daily standup

*English:* agile, scrum, sprint, backlog, sprint planning, daily standup

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Sprint creation
- Backlog prioritization
- Velocity tracking
- Burndown charts

**Примеры задач:**
- "Спланировать спринт"
- "Создать бэклог задач"
- "Провести daily standup"

---

## 📦 Module 06: Examples Templates

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Нужны примеры workflow
- Шаблоны документов
- Best practices примеры

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* пример, шаблон, примеры, template, образец

*English:* example, template, templates, sample, pattern

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Need for templates
- Example workflows
- Documentation templates

**Примеры задач:**
- "Показать пример создания задачи"
- "Нужен шаблон проектного плана"
- "Примеры workflow PM"

---

## 📦 Module 07: Refactoring Workflow

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Рефакторинг агентов
- Token optimization
- Модульная архитектура знаний
- NEW workflow migration

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* рефакторинг, оптимизация, токены, модули, workflow, миграция

*English:* refactoring, optimization, tokens, modules, workflow, migration

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- OLD → NEW workflow migration
- Token optimization strategies
- Module creation
- Context-dependent reading

**Примеры задач:**
- "Рефакторить агента на NEW workflow"
- "Оптимизировать использование токенов"
- "Создать модульную структуру знаний"

---

## 📦 Module 08: Quick Task Selection Protocol

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- При переключении в роль PM (ПО ДЕФОЛТУ)
- Выбор следующей задачи для работы
- Оптимизация токенов при выборе задач
- Приоритизация doing → review → todo

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* выбор задачи, приоритизация, doing, review, todo, переключение роли, токен-экономия, быстрый выбор

*English:* task selection, prioritization, doing, review, todo, role switching, token economy, quick selection

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- PM role activation (автоматически загружается)
- Task status filtering (doing/review/todo)
- Context preservation (70-85%+ saved)
- Minimal API calls (2-4 requests)

**Примеры задач:**
- "Выбрать следующую задачу"
- "Какая задача следующая?"
- "Что делать дальше?"

---

## 📦 Module 09: Agent Refactoring Check

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Переключение на роль любого агента (автопроверка ПЕРЕД переключением)
- Обновление прогресса рефакторинга
- Tracking agent refactoring status
- Checklist updates

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* чеклист, прогресс, рефакторинг агентов, checklist, tracking, проверка агента, нерефакторенный агент

*English:* checklist, progress, agent refactoring, tracking, agent check, non-refactored agent

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- AGENTS_REFACTORING_CHECKLIST.md reading
- Role switch validation
- Agent status check ([x] vs [ ])
- Progress tracking
- Refactoring task creation

**Примеры задач:**
- "Обновить чеклист рефакторинга"
- "Отследить прогресс миграции агентов"
- "Пометить агента как рефакторенного"
- "Проверить статус агента перед переключением"

---

## 🤖 Module Selection Function

### select_modules_for_task()

Intelligent module selection based on task keywords and context.

```python
def select_modules_for_task(task_description: str, task_title: str = "") -> list[str]:
    """
    Выбирает релевантные модули на основе анализа задачи.

    Args:
        task_description: Полное описание задачи
        task_title: Название задачи (опционально)

    Returns:
        List of module file paths to load

    Example:
        >>> select_modules_for_task("Создать задачу для Implementation Engineer")
        ["modules/01_mcp_critical_rules.md",
         "modules/03_task_management.md"]

        >>> select_modules_for_task("Восстановить контекст после auto-compact")
        ["modules/01_mcp_critical_rules.md",
         "modules/04_context_recovery.md"]
    """

    full_text = f"{task_title} {task_description}".lower()
    selected_modules = []

    # Module 01: MCP Critical Rules
    mcp_keywords = [
        "mcp", "archon", "api", "сервер", "server", "проект", "project",
        "задача", "task", "создать", "create", "получить", "get",
        "обновить", "update"
    ]
    if any(kw in full_text for kw in mcp_keywords):
        selected_modules.append("modules/01_mcp_critical_rules.md")

    # Module 02: Project Management
    project_keywords = [
        "проект", "project", "создать проект", "create project",
        "управление проектами", "project management", "планирование", "planning",
        "инициация", "initiation", "завершение", "completion"
    ]
    if any(kw in full_text for kw in project_keywords):
        selected_modules.append("modules/02_project_management.md")

    # Module 03: Task Management
    task_keywords = [
        "задача", "задачи", "task", "tasks", "создать задачу", "create task",
        "приоритет", "priority", "назначить", "assign", "task_order",
        "зависимости", "dependencies", "приоритизация", "prioritization"
    ]
    if any(kw in full_text for kw in task_keywords):
        selected_modules.append("modules/03_task_management.md")

    # Module 04: Context Recovery
    context_keywords = [
        "контекст", "context", "восстановление", "recovery", "auto-compact",
        "потеря", "loss", "registry", "project_id"
    ]
    if any(kw in full_text for kw in context_keywords):
        selected_modules.append("modules/04_context_recovery.md")

    # Module 05: Agile Methodologies
    agile_keywords = [
        "agile", "scrum", "спринт", "sprint", "бэклог", "backlog",
        "планирование спринта", "sprint planning", "daily standup"
    ]
    if any(kw in full_text for kw in agile_keywords):
        selected_modules.append("modules/05_agile_methodologies.md")

    # Module 06: Examples Templates
    example_keywords = [
        "пример", "example", "шаблон", "template", "templates",
        "образец", "sample", "pattern"
    ]
    if any(kw in full_text for kw in example_keywords):
        selected_modules.append("modules/06_examples_templates.md")

    # Module 07: Refactoring Workflow
    refactoring_keywords = [
        "рефакторинг", "refactoring", "оптимизация", "optimization",
        "токены", "tokens", "модули", "modules", "workflow", "миграция", "migration"
    ]
    if any(kw in full_text for kw in refactoring_keywords):
        selected_modules.append("modules/07_refactoring_workflow.md")

    # Module 08: Quick Task Selection Protocol
    task_selection_keywords = [
        "выбор задачи", "task selection", "приоритизация", "prioritization",
        "doing", "review", "todo", "переключение роли", "role switching",
        "токен-экономия", "token economy", "быстрый выбор", "quick selection",
        "какая задача", "what task", "что делать", "what to do"
    ]
    if any(kw in full_text for kw in task_selection_keywords):
        selected_modules.append("modules/08_quick_task_selection_protocol.md")

    # Module 09: Agent Refactoring Check
    checklist_keywords = [
        "чеклист", "checklist", "прогресс", "progress",
        "рефакторинг агентов", "agent refactoring", "tracking",
        "проверка агента", "agent check", "нерефакторенный", "non-refactored",
        "статус агента", "agent status"
    ]
    if any(kw in full_text for kw in checklist_keywords):
        selected_modules.append("modules/09_agent_refactoring_check.md")

    # Fallback: if no keywords matched, load CRITICAL modules
    if not selected_modules:
        selected_modules = [
            "modules/01_mcp_critical_rules.md",
            "modules/03_task_management.md"
        ]

    return selected_modules
```

### Usage Examples

**Example 1: Simple task creation**
```python
Task: "Создать задачу для Blueprint Architect"
Selected: ["modules/01_mcp_critical_rules.md",
           "modules/03_task_management.md"]
Result: 2 modules loaded (CRITICAL priority)
```

**Example 2: Context recovery**
```python
Task: "Восстановить контекст проекта после auto-compact"
Selected: ["modules/01_mcp_critical_rules.md",
           "modules/04_context_recovery.md"]
Result: 2 modules loaded (CRITICAL + HIGH priorities)
```

**Example 3: Agent refactoring**
```python
Task: "Рефакторить deployment_engineer на NEW workflow"
Selected: ["modules/01_mcp_critical_rules.md",
           "modules/03_task_management.md",
           "modules/07_refactoring_workflow.md",
           "modules/09_agent_refactoring_check.md"]
Result: 4 modules loaded (multi-domain task)
```

**Example 4: Task selection (PM workflow)**
```python
Task: "Выбрать следующую задачу для работы"
Selected: ["modules/01_mcp_critical_rules.md",
           "modules/03_task_management.md",
           "modules/08_quick_task_selection_protocol.md"]
Result: 3 modules loaded (default PM workflow)
```

---

## 🔄 Workflow Integration

### 8-Stage Process

```
STAGE 1: Read archon_project_manager_system_prompt.md (~550 tokens)
   ↓ File: knowledge/archon_project_manager_system_prompt.md
   ↓ Contains: Role identity + Specialization

STAGE 1.5: Read common_agent_rules.md (~1,500 tokens)
   ↓ File: agents/common_agent_rules.md
   ↓ Contains: Universal rules for ALL agents (TodoWrite, Git, Escalation, etc.)
   ↓ Applies to EVERY task execution

STAGE 2: Read task from Archon MCP
   ↓ mcp__archon__find_tasks(task_id="...")

STAGE 3: Read archon_project_manager_module_selection.md + select modules
   ↓ File: knowledge/archon_project_manager_module_selection.md
   ↓ Select 2-4 relevant modules из 9

STAGE 4: Read ONLY SELECTED modules
   ↓ Files: knowledge/modules/01-09_*.md
   ↓ Load only relevant knowledge

STAGE 5: Git Log First
   ↓ git log --oneline -10
   ↓ Project context from recent changes

STAGE 6: Read existing code (MANDATORY!)
   ↓ Grep/Glob for existing implementation
   ↓ Read for code analysis

STAGE 7: Execute task with context-dependent modules
```

---

## 📈 Expected Performance

### Module Loading Distribution

**By Task Complexity:**
- Simple tasks (2 modules): Task creation only, MCP operations
- Medium tasks (3 modules): Task + Project management, Context recovery
- Complex tasks (4-5 modules): Refactoring, Multi-project coordination

**Average:** 3.0 modules per task (из 9 available)

### Priority Validation

**Module Load Frequency (predicted):**
- 🔴 01_mcp_critical_rules: 80% of tasks
- 🔴 03_task_management: 75% of tasks
- 🔴 08_quick_task_selection_protocol: 70% of tasks (default PM workflow)
- 🟡 02_project_management: 55% of tasks
- 🟡 04_context_recovery: 50% of tasks
- 🟡 07_refactoring_workflow: 50% of tasks
- 🟢 05_agile_methodologies: 35% of tasks
- 🟢 06_examples_templates: 30% of tasks
- 🟢 09_agent_refactoring_check: 25% of tasks

---

## ✅ Best Practices

### DO:
1. **ALWAYS read system_prompt.md first** - this is role identity
2. **ALWAYS read PROJECTS_REGISTRY.md before MCP calls** - 98% token savings
3. **Use MODULE_SELECTION.md for selection** - don't guess which modules to load
4. **Load ONLY relevant modules** - not all 9 modules
5. **Check existing code (STAGE 6)** - mandatory before changes
6. **Use Git context (STAGE 5)** - for project history understanding

### DON'T:
1. **DON'T load all 9 modules** - only relevant 2-4
2. **DON'T skip MODULE_SELECTION.md** - critical for module selection
3. **DON'T guess which modules needed** - use select_modules_for_task()
4. **DON'T ignore STAGE 6** - code reading is mandatory
5. **DON'T skip Git context** - history matters
6. **DON'T skip PROJECTS_REGISTRY.md** - это критично для токен-оптимізації

---

**Version:** 1.0
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Status:** Ready for production use
