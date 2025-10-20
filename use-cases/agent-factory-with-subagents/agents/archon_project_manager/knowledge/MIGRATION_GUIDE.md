# Archon Project Manager - Migration Guide

**Alternative Title:** Module Selection & NEW Workflow Migration Guide
**Version:** 1.0
**Date:** 2025-10-20
**Author:** Archon Implementation Engineer
**Purpose:** OLD → NEW workflow migration instructions + Module selection logic

---

## 📊 Module Overview

| # | Module | Priority | Lines | Domain | Load When |
|---|--------|----------|-------|--------|-----------|
| **01** | [MCP Critical Rules](modules/01_mcp_critical_rules.md) | 🔴 CRITICAL | ~250 | Archon MCP operations | MCP, Archon API tasks |
| **02** | [Project Management](modules/02_project_management.md) | 🟡 HIGH | ~220 | Project lifecycle | Project creation, planning |
| **03** | [Task Management](modules/03_task_management.md) | 🔴 CRITICAL | ~300 | Task operations | Task creation, prioritization |
| **04** | [Context Recovery](modules/04_context_recovery.md) | 🟡 HIGH | ~200 | Context restoration | Auto-compact, context loss |
| **05** | [Agile Methodologies](modules/05_agile_methodologies.md) | 🟢 MEDIUM | ~180 | Sprint/Scrum | Sprint planning, backlog |
| **06** | [Examples Templates](modules/06_examples_templates.md) | 🟢 MEDIUM | ~150 | Templates | Need examples |
| **07** | [Refactoring Workflow](modules/07_refactoring_workflow.md) | 🟡 HIGH | ~350 | Agent refactoring | Token optimization |
| **08** | [Agent Refactoring Check](modules/08_agent_refactoring_check.md) | 🟢 MEDIUM | ~150 | Progress tracking | Checklist updates |

**Total Knowledge:** ~1,800 lines in modules + ~550 tokens system prompt

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

## 📦 Module 08: Agent Refactoring Check

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Обновление прогресса рефакторинга
- Tracking agent refactoring status
- Checklist updates

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* чеклист, прогресс, рефакторинг агентов, checklist, tracking

*English:* checklist, progress, agent refactoring, tracking

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- AGENTS_REFACTORING_CHECKLIST.md updates
- Progress tracking
- Status updates (OLD/NEW)

**Примеры задач:**
- "Обновить чеклист рефакторинга"
- "Отследить прогресс миграции агентов"
- "Пометить агента как рефакторенного"

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

    # Module 08: Agent Refactoring Check
    checklist_keywords = [
        "чеклист", "checklist", "прогресс", "progress",
        "рефакторинг агентов", "agent refactoring", "tracking"
    ]
    if any(kw in full_text for kw in checklist_keywords):
        selected_modules.append("modules/08_agent_refactoring_check.md")

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
           "modules/08_agent_refactoring_check.md"]
Result: 4 modules loaded (multi-domain task)
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
   ↓ Select 2-4 relevant modules из 8

STAGE 4: Read ONLY SELECTED modules
   ↓ Files: knowledge/modules/01-08_*.md
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

**Average:** 2.8 modules per task (из 8 available)

### Priority Validation

**Module Load Frequency (predicted):**
- 🔴 01_mcp_critical_rules: 80% of tasks
- 🔴 03_task_management: 75% of tasks
- 🟡 02_project_management: 55% of tasks
- 🟡 04_context_recovery: 50% of tasks
- 🟡 07_refactoring_workflow: 50% of tasks
- 🟢 05_agile_methodologies: 35% of tasks
- 🟢 06_examples_templates: 30% of tasks
- 🟢 08_agent_refactoring_check: 25% of tasks

---

## ✅ Best Practices

### DO:
1. **ALWAYS read system_prompt.md first** - this is role identity
2. **ALWAYS read PROJECTS_REGISTRY.md before MCP calls** - 98% token savings
3. **Use MODULE_SELECTION.md for selection** - don't guess which modules to load
4. **Load ONLY relevant modules** - not all 8 modules
5. **Check existing code (STAGE 6)** - mandatory before changes
6. **Use Git context (STAGE 5)** - for project history understanding

### DON'T:
1. **DON'T load all 8 modules** - only relevant 2-4
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
