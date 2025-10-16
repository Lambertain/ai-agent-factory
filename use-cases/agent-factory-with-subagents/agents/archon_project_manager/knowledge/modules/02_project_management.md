# Module 02: Project Management

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Создание нового проекта
- Обновление описания проекта
- Валидация полноты информации о проекте
- Настройка project structure
- Определение tech stack проекта
- Заполнение local_repo_path и git_repo
- Интерактивный диалог с пользователем о проекте

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** создать проект, новый проект, описание проекта, tech stack, git репозиторий, локальный путь, валидация проекта

**English:** create project, new project, project description, tech stack, git repository, local path, project validation

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Пользователь хочет создать новый проект
- Project Manager обнаружил неполное описание проекта
- Нужно заполнить обязательные поля проекта
- Настройка структуры и архитектуры нового проекта

---

## 🏗️ АВТОМАТИЧЕСКАЯ ВАЛИДАЦИЯ ОПИСАНИЯ ПРОЕКТА

### Workflow проверки описания

При выборе проекта Project Manager автоматически проверяет полноту описания проекта.

**Обязательные поля для валидации:**

1. **description** - что делает проект, цели, ключевые функции (минимум 50 символов)
2. **tech_stack** - язык программирования, фреймворки, библиотеки, база данных
3. **local_repo_path** - полный путь на диске (например: D:\\Automation\\Development\\projects\\patternshift)
4. **git_repo** - URL GitHub/GitLab репозитория

---

## 📋 ПРИМЕР ИНТЕРАКТИВНОГО ДИАЛОГА

### Сценарий 1: Описание неполное

```
User: archon-project-manager

PM: [Показывает список проектов]

User: PatternShift

PM: [Проверяет описание проекта через ProjectDescriptionValidator]

PM: ⚠️ Описание проекта НЕПОЛНОЕ!

Недостающие или некорректные поля:
  1. description (слишком короткое: минимум 50 символов)
  2. local_repo_path
  3. git_repo

Предлагаю заполнить недостающие поля сейчас. Это займет 2-3 минуты.
Продолжить? (да/нет)

User: да

PM:
--- DESCRIPTION ---
Описание проекта:
Что делает проект? Каковы его цели и ключевые функции?
(минимум 50 символов)

User: Трансформационная программа для психологов, использующая NLP и эриксоновский
гипноз для создания персонализированных программ изменений

PM: ✓ Описание принято

--- TECH_STACK ---
Технологический стек проекта:
Какой язык программирования, фреймворки, библиотеки используются?
Какая база данных?

User: Python, FastAPI, Pydantic AI, PostgreSQL, Claude API

PM: ✓ Tech stack принят

--- LOCAL_REPO_PATH ---
Локальный путь к репозиторию:
Полный путь на диске (например: D:\Automation\Development\projects\patternshift)

User: D:\Automation\Development\projects\patternshift

PM: ✓ Путь принят

--- GIT_REPO ---
URL Git репозитория:
GitHub или GitLab URL (например: https://github.com/username/repo)

User: https://github.com/username/patternshift

PM: ✓ Git URL принят

PM: [Обновляет проект через mcp__archon__manage_project("update", ...)]

✅ Описание проекта обновлено! Все обязательные поля заполнены.
Переходим к анализу задач...
```

### Сценарий 2: Описание полное

```
User: archon-project-manager

PM: [Показывает список проектов]

User: AI Agent Factory

PM: [Проверяет описание - все поля заполнены]

✅ Описание проекта полное. Продолжаем работу.

[Анализирует задачи проекта...]
```

---

## 🔧 ТЕХНИЧЕСКАЯ РЕАЛИЗАЦИЯ

### Использование ProjectDescriptionValidator

```python
from agents.common.project_description_validator import ProjectDescriptionValidator

# 1. Получить данные проекта
project_data = await mcp__archon__find_projects(project_id="selected_project_id")

# 2. Валидировать описание
is_complete, missing_fields = ProjectDescriptionValidator.validate_project_description(project_data)

# 3. Если неполное - интерактивный диалог
if not is_complete:
    # Показать отчет
    report = ProjectDescriptionValidator.format_validation_report(is_complete, missing_fields)
    print(report)

    # Сгенерировать промпты
    prompts = ProjectDescriptionValidator.generate_interactive_prompts(missing_fields)

    # Собрать ответы пользователя
    updated_data = {}
    for field, prompt in prompts.items():
        print(f"\n--- {field.upper()} ---")
        print(prompt)
        user_input = input()
        updated_data[field] = user_input

    # Обновить проект
    await mcp__archon__manage_project(
        action="update",
        project_id=project_id,
        **updated_data
    )

# 4. Продолжить работу с проектом
```

---

## 📐 PROJECT STRUCTURE TEMPLATE

### Project Creation Checklist

```
□ Define project scope and objectives
□ Identify stakeholders and requirements
□ Create project in Archon system
□ Set up team roles and permissions
□ Establish communication channels
□ Define success criteria and KPIs
□ Create initial task breakdown
□ Set timeline and milestones
□ Fill out all mandatory fields:
  - description (50+ символов)
  - tech_stack (полный стек)
  - local_repo_path (локальный путь)
  - git_repo (GitHub/GitLab URL)
```

### Создание нового проекта

```python
# Создать проект через MCP
await mcp__archon__manage_project(
    action="create",
    title="Project Name",
    description="Detailed description (50+ characters)",
    tech_stack="Python, FastAPI, PostgreSQL",
    local_repo_path="D:\\Automation\\Development\\projects\\projectname",
    git_repo="https://github.com/username/projectname"
)
```

---

## ✅ ПРЕИМУЩЕСТВА АВТОМАТИЧЕСКОЙ ВАЛИДАЦИИ

### Качество данных:
- Гарантирует полноту информации о проекте
- Предотвращает работу с неполными данными
- Стандартизирует описания проектов

### User Experience:
- Интерактивный диалог вместо блокировки
- Понятные промпты для каждого поля
- Валидация в реальном времени

### Эффективность:
- Однократное заполнение при создании проекта
- Автоматическая проверка при каждом запуске
- Экономия времени команды

### Интеграция:
- Бесшовно встроено в workflow Project Manager
- Использует существующие Archon MCP tools
- Модульная архитектура (ProjectDescriptionValidator)

---

## 🎯 BEST PRACTICES

### Clear Requirements:
- Well-defined scope
- Measurable objectives
- Acceptance criteria
- Success metrics

### Effective Communication:
- Regular updates
- Transparent reporting
- Stakeholder engagement
- Team collaboration

### Quality Focus:
- Continuous testing
- Code reviews
- Performance monitoring
- Security assessments

---

**Навигация:**
- [← Предыдущий модуль: MCP Critical Rules](01_mcp_critical_rules.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Task Management](03_task_management.md)
