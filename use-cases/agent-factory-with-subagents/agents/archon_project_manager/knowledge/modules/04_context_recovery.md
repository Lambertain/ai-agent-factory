# Module 04: Context Recovery

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- После auto-compact сессии
- Потеря контекста о текущем проекте
- Потеря project_id в новой сессии
- Запуск агента после длительной паузы
- Ошибка "project_id не определен"
- Пользователь начинает работу без указания проекта
- Новая сессия с нулевым контекстом

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** auto-compact, втрата контексту, восстановить контекст, project_id втрачено, новая сессия, PROJECTS_REGISTRY

**English:** auto-compact, lost context, recover context, project_id lost, new session, PROJECTS_REGISTRY

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Начало новой сессии с агентом
- После прерывания работы и возобновления
- Когда нужно восстановить информацию о проекте
- Когда потерян контекст о текущей работе

---

## 🚨 ПРОБЛЕМА: Потеря контекста после auto-compact

### Что происходит при auto-compact?

```
Сессия 1: Работаем с проектом "AI Agent Factory" (project_id: c75ef8...)
│
├─ Создано 10 задач
├─ Обсуждены приоритеты
├─ Начата работа над задачей #3
│
└─ AUTO-COMPACT TRIGGERED (токены закончились)
    ↓
Сессия 2: 🚨 ВСЯ ИНФОРМАЦИЯ ПОТЕРЯНА
│
├─ ❌ Не помним project_id
├─ ❌ Не помним какой проект активный
├─ ❌ Не помним над чем работали
└─ ❌ Не помним контекст задач
```

### Последствия потери контекста:

1. **Путаница с проектами** - может работать с неправильным проектом
2. **Дублирование работы** - может начать задачу заново
3. **Потеря приоритетов** - не помнит что было важно
4. **Неправильное назначение задач** - может назначить на неправильного агента

---

## 🛡️ РЕШЕНИЕ: Трёхуровневая система сохранения контекста

### УРОВЕНЬ 1: Header каждой ответа (Основная защита)

**ОБЯЗАТЕЛЬНО в начале КАЖДОЙ ответи Project Manager:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PROJECT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Активний проект: AI Agent Factory
📋 Project ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
📈 Задачі в роботі: 3 | Review: 2 | Todo: 15
⏰ Останнє оновлення: 2025-10-16 14:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Почему это работает:**
- Project_id ВСЕГДА видим в последнем сообщении
- После auto-compact и summarization это сохранится
- Легко скопировать для следующих запросов

### УРОВЕНЬ 2: PROJECTS_REGISTRY.md (Локальный кеш)

**Файл:** `D:\Automation\agent-factory\...\archon_project_manager\knowledge\PROJECTS_REGISTRY.md`

**Структура:**

```markdown
# Реестр проектов Archon

**Последнее обновление:** 2025-10-16 14:30
**Версия:** 1.0

## Активные проекты

### 🔥 AI Agent Factory (ОСНОВНОЙ)
- **Project ID:** c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
- **Приоритет:** HIGHEST
- **Статус:** In active development
- **Локальный путь:** D:\Automation\agent-factory
- **Git:** https://github.com/nikitasolovey/ai-agent-factory
- **Tech Stack:** Python, Pydantic AI, FastAPI
- **Задач:** doing: 3, review: 2, todo: 15
- **Последняя работа:** Рефакторинг Project Manager (2025-10-16)

### 📊 PatternShift
- **Project ID:** [UUID]
- **Приоритет:** MEDIUM
- **Статус:** Early development
- **Локальный путь:** D:\Automation\Development\projects\patternshift
- **Tech Stack:** Python, FastAPI, PostgreSQL, Claude API
- **Описание:** Трансформационная программа для психологов

## Архивные проекты

[Список завершенных проектов]

## Быстрый доступ

| Проект | ID (первые 8 символов) | Активность |
|--------|------------------------|------------|
| AI Agent Factory | c75ef8e3 | 🔥 Сейчас |
| PatternShift | [UUID] | ⏸️ Пауза |
```

**Автоматическое обновление:**

```python
async def update_projects_registry():
    """Автоматически обновлять PROJECTS_REGISTRY.md после изменений."""

    # 1. Получить все проекты
    projects = await mcp__archon__find_projects()

    # 2. Для каждого проекта получить статистику задач
    for project in projects:
        stats = await get_project_task_stats(project["id"])
        project["stats"] = stats

    # 3. Обновить файл PROJECTS_REGISTRY.md
    registry_content = format_registry(projects)
    write_file("PROJECTS_REGISTRY.md", registry_content)
```

### УРОВЕНЬ 3: Auto-recovery функция

**Вызывать в начале КАЖДОЙ новой сессии:**

```python
async def recover_project_context_after_compact():
    """
    Восстановить контекст проекта после auto-compact.

    Returns:
        str: project_id активного проекта
    """

    print("🔄 Восстанавливаю контекст после auto-compact...")

    # ШАГО 1: Попытка восстановить из PROJECTS_REGISTRY.md
    try:
        registry = read_file("PROJECTS_REGISTRY.md")
        active_project = extract_active_project(registry)
        if active_project:
            print(f"✅ Контекст восстановлен из реестра")
            print(f"🎯 Активний проект: {active_project['name']}")
            print(f"📋 Project ID: {active_project['id']}")
            return active_project["id"]
    except FileNotFoundError:
        print("⚠️ PROJECTS_REGISTRY.md не найден")

    # ШАГО 2: Получить список проектов из Archon
    projects = await mcp__archon__find_projects()

    # ШАГО 3: Определить последний активный проект
    # (по последним изменениям в задачах)
    active_project_id = None
    latest_activity = None

    for project in projects:
        # Получить последние задачи проекта
        tasks = await mcp__archon__find_tasks(
            project_id=project["id"],
            filter_by="status",
            filter_value="doing"
        )

        if tasks:
            # Проект с задачами в работе = активный
            active_project_id = project["id"]
            print(f"🔍 Найден активный проект: {project['title']}")
            print(f"📋 Задач в работе: {len(tasks)}")
            break

    # ШАГО 4: Если не найден - спросить пользователя
    if not active_project_id:
        print("\n🚨 НЕ УДАЛОСЬ ВОССТАНОВИТЬ КОНТЕКСТ АВТОМАТИЧЕСКИ")
        print("\n📋 Доступные проекты:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project['title']}")

        print("\n🎯 С каким проектом работаем?")
        # Ожидать ответ пользователя

    return active_project_id
```

---

## 🔄 WORKFLOW ВОССТАНОВЛЕНИЯ КОНТЕКСТА

### Начало новой сессии (после auto-compact)

```
┌──────────────────────────────────────────────┐
│ ШАГ 1: Проверить наличие контекста           │
│ ↓ Есть ли project_id в памяти?               │
└──────────────────────────────────────────────┘
              ↓ НЕТ
┌──────────────────────────────────────────────┐
│ ШАГ 2: Восстановить из PROJECTS_REGISTRY.md  │
│ ↓ Найти запись об активном проекте           │
└──────────────────────────────────────────────┘
              ↓ Найдено
┌──────────────────────────────────────────────┐
│ ШАГ 3: Валидировать через Archon MCP         │
│ ↓ Проверить что проект существует            │
└──────────────────────────────────────────────┘
              ↓ Валидно
┌──────────────────────────────────────────────┐
│ ШАГ 4: Восстановить полный контекст          │
│ ├─ Прочитать описание проекта                │
│ ├─ Получить статус задач (doing/review/todo) │
│ ├─ Определить приоритеты                     │
│ └─ Показать PROJECT CONTEXT header           │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ ШАГ 5: Готов к работе                        │
│ ↓ Контекст восстановлен, можно продолжать    │
└──────────────────────────────────────────────┘
```

### Если автоматическое восстановление не удалось

```python
# КРИТИЧЕСКИ ВАЖНО: НЕ ПРЕДПОЛАГАТЬ ПОСЛЕДНИЙ ПРОЕКТ

# ❌ НЕПРАВИЛЬНО
project_id = "последний из предыдущей сессии"  # Предположение!

# ✅ ПРАВИЛЬНО
print("🚨 НЕ УДАЛОСЬ ВОССТАНОВИТЬ КОНТЕКСТ")
print("🎯 Пожалуйста, укажите с каким проектом работаем:")
project_id = await ask_user_for_project()
```

---

## 📋 ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА CONTEXT RECOVERY

### Правило 1: НИКОГДА не предполагать последний проект

```python
# ❌ ЗАПРЕЩЕНО
# "Продолжаем работу с AI Agent Factory"
# (БЕЗ уточнения у пользователя)

# ✅ ПРАВИЛЬНО
print("🎯 С каким проектом работаем?")
# Показать список → получить выбор
```

### Правило 2: PROJECT CONTEXT header в КАЖДОМ ответе

```python
# ОБЯЗАТЕЛЬНО начинать каждый ответ с:
print_project_context_header(project_id)

# Даже если кажется очевидным - всегда показывать
```

### Правило 3: Обновлять PROJECTS_REGISTRY.md после каждого изменения

```python
# После создания задачи
await mcp__archon__manage_task("create", ...)
await update_projects_registry()  # Обновить реестр

# После изменения статуса
await mcp__archon__manage_task("update", ...)
await update_projects_registry()  # Обновить реестр
```

### Правило 4: Валидация project_id перед КАЖДОЙ операцией

```python
async def ensure_project_context(project_id: str = None):
    """Убедиться что project_id определен."""

    if not project_id:
        project_id = await recover_project_context_after_compact()

    if not project_id:
        raise ValueError("❌ ОШИБКА: project_id не определен!")

    return project_id
```

---

## 🔍 ДИАГНОСТИКА ПРОБЛЕМ С КОНТЕКСТОМ

### Симптомы потери контекста:

1. **"Над каким проектом работаем?"** - агент не помнит проект
2. **Задачи из разных проектов** - путаница в задачах
3. **Повторные вопросы** - агент задает уже отвеченные вопросы
4. **Неправильные назначения** - задачи назначаются не тем агентам

### Чек-лист диагностики:

```
□ Есть ли PROJECT CONTEXT header в последнем ответе?
□ Существует ли PROJECTS_REGISTRY.md?
□ Обновлялся ли реестр недавно?
□ Может ли агент получить проекты через Archon MCP?
□ Валидна ли связь с Archon MCP Server?
```

---

## 🎯 BEST PRACTICES

### Проактивное сохранение контекста

```python
# Начало работы
project_id = await ensure_project_context()
print_project_context_header(project_id)

# Во время работы
await update_projects_registry()  # После каждого изменения

# Перед завершением
await save_session_state(project_id, current_task_id)
```

### Защита от множественных восстановлений

```python
# Кеширование project_id в сессии
_session_project_id = None

async def get_project_id():
    global _session_project_id

    if _session_project_id:
        return _session_project_id

    _session_project_id = await recover_project_context_after_compact()
    return _session_project_id
```

---

**Навигация:**
- [← Предыдущий модуль: Task Management](03_task_management.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Agile Methodologies](05_agile_methodologies.md)
