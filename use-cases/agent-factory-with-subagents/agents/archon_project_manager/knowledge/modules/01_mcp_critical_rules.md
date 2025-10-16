# Module 01: MCP Critical Rules

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Пользователь пишет "archon-project-manager"
- Работа с проектами через Archon MCP
- Создание, обновление или удаление задач
- Получение списка проектов или задач
- Любые операции с Archon MCP Server
- Ошибка "No such tool available" при вызове mcp__archon__*
- Попытка использовать bash/Python вместо MCP tools

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** archon, mcp, проекты, задачи, создать задачу, список проектов, обновить задачу, archon-project-manager

**English:** archon, mcp, projects, tasks, create task, list projects, update task, archon-project-manager

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Начало работы с Archon MCP Server
- Получена ошибка при вызове MCP инструмента
- Нужно создать/обновить/удалить проект или задачу
- Проверка правильности использования MCP tools
- Отладка проблем с подключением к Archon

---

## 🔌 КРИТИЧЕСКИ ВАЖНО: КАК ПОДКЛЮЧАТЬСЯ К ARCHON MCP

### ✅ ШАГ 1: ИСПОЛЬЗУЙ ВСТРОЕННЫЙ ИНСТРУМЕНТ (НЕ Bash, НЕ Python скрипт!)

**ЕДИНСТВЕННЫЙ ПРАВИЛЬНЫЙ СПОСОБ:**

```xml
<antml_function_calls>
<antml_invoke name="mcp__archon__find_projects">
</antml_invoke>
</antml_function_calls>
```

**ЧТО ЭТО ЗНАЧИТ:**
- Claude Code уже подключен к Archon MCP Server
- У тебя есть готовый инструмент `mcp__archon__find_projects`
- Просто вызови его через `<antml_invoke>` тег
- НЕ нужно искать пути к файлам
- НЕ нужно запускать через Bash
- НЕ нужно писать Python скрипты

**Если получил ответ `No such tool available`:**
- Немедленно повтори вызов `mcp__archon__find_projects` — первый запрос может лишь инициировать загрузку инструмента
- Если повторный вызов тоже вернул ошибку, сообщи пользователю, что Archon MCP не подключён
- Предложи перезапустить `start-archon.bat` или проверить конфиг
- НЕ переходи к Bash/Python-обходным путям

---

## ✅ ШАГ 2: ЧАСТОИСПОЛЬЗУЕМЫЕ ИНСТРУМЕНТЫ

### Получить список всех проектов:
```xml
<antml_invoke name="mcp__archon__find_projects">
</antml_invoke>
```

### Получить конкретный проект:
```xml
<antml_invoke name="mcp__archon__find_projects">
<antml_parameter name="project_id">UUID-проекта</antml_parameter>
</antml_invoke>
```

### Получить задачи проекта:
```xml
<antml_invoke name="mcp__archon__find_tasks">
<antml_parameter name="project_id">UUID-проекта</antml_parameter>
</antml_invoke>
```

### Получить задачи с фильтром:
```xml
<antml_invoke name="mcp__archon__find_tasks">
<antml_parameter name="project_id">UUID-проекта</antml_parameter>
<antml_parameter name="filter_by">status</antml_parameter>
<antml_parameter name="filter_value">todo</antml_parameter>
</antml_invoke>
```

### Получить конкретную задачу:
```xml
<antml_invoke name="mcp__archon__find_tasks">
<antml_parameter name="task_id">UUID-задачи</antml_parameter>
</antml_invoke>
```

### Создать задачу:
```xml
<antml_invoke name="mcp__archon__manage_task">
<antml_parameter name="action">create</antml_parameter>
<antml_parameter name="project_id">UUID-проекта</antml_parameter>
<antml_parameter name="title">Название задачи</antml_parameter>
<antml_parameter name="description">Описание задачи</antml_parameter>
<antml_parameter name="assignee">Имя агента</antml_parameter>
<antml_parameter name="status">todo</antml_parameter>
</antml_invoke>
```

### Обновить задачу:
```xml
<antml_invoke name="mcp__archon__manage_task">
<antml_parameter name="action">update</antml_parameter>
<antml_parameter name="task_id">UUID-задачи</antml_parameter>
<antml_parameter name="status">done</antml_parameter>
</antml_invoke>
```

### Удалить задачу:
```xml
<antml_invoke name="mcp__archon__manage_task">
<antml_parameter name="action">delete</antml_parameter>
<antml_parameter name="task_id">UUID-задачи</antml_parameter>
</antml_invoke>
```

---

## ❌ ТИПИЧНЫЕ ОШИБКИ (НЕ ДЕЛАЙ ТАК!)

### ❌ ОШИБКА 1: Поиск через Bash
```bash
# НЕПРАВИЛЬНО!
find . -name "archon*"
node D:\Automation\archon-mcp-server\build\index.js
```
**Почему неправильно:** Ты пытаешься найти файлы сервера вместо использования готового инструмента.

### ❌ ОШИБКА 2: Прямой вызов Python функций
```python
# НЕПРАВИЛЬНО!
await mcp__archon__find_projects()
```
**Почему неправильно:** Это синтаксис для Python, а ты работаешь в Claude Code через XML теги.

### ❌ ОШИБКА 3: Попытка создать клиент вручную
```python
# НЕПРАВИЛЬНО!
from mcp import Client
client = Client("archon")
await client.connect()
```
**Почему неправильно:** Клиент уже создан и подключен Claude Code автоматически.

### ❌ ОШИБКА 4: Использование asyncio обертки
```python
# НЕПРАВИЛЬНО!
import asyncio
asyncio.run(mcp__archon__find_projects())
```
**Почему неправильно:** Ты не запускаешь Python код, ты вызываешь MCP инструменты через Claude Code.

---

## ✅ ЧЕК-ЛИСТ САМОПРОВЕРКИ

Перед тем как сделать запрос к Archon, задай себе вопросы:

1. ❓ **Я использую `<antml_invoke>`?**
   - ✅ Да → Правильно!
   - ❌ Нет → Исправь на `<antml_invoke name="mcp__archon__...">`

2. ❓ **Я ищу файлы через `find` или `Glob`?**
   - ✅ Нет → Правильно!
   - ❌ Да → Удали поиск, используй прямой вызов инструмента

3. ❓ **Я запускаю команды через `Bash`?**
   - ✅ Нет → Правильно!
   - ❌ Да → Замени на `<antml_invoke>`

4. ❓ **Я пишу Python код с `await`?**
   - ✅ Нет → Правильно!
   - ❌ Да → Это не Python, используй XML теги Claude Code

5. ❓ **Название инструмента начинается с `mcp__archon__`?**
   - ✅ Да → Правильно!
   - ❌ Нет → Добавь префикс `mcp__archon__`

---

## 🎯 БЫСТРАЯ ШПАРГАЛКА

| Что нужно сделать | Инструмент | Обязательные параметры |
|-------------------|------------|------------------------|
| Список проектов | `mcp__archon__find_projects` | нет |
| Конкретный проект | `mcp__archon__find_projects` | `project_id` |
| Список задач | `mcp__archon__find_tasks` | `project_id` (рекомендуется) |
| Конкретная задача | `mcp__archon__find_tasks` | `task_id` |
| Создать задачу | `mcp__archon__manage_task` | `action="create"`, `project_id`, `title` |
| Обновить задачу | `mcp__archon__manage_task` | `action="update"`, `task_id` |
| Удалить задачу | `mcp__archon__manage_task` | `action="delete"`, `task_id` |
| Создать проект | `mcp__archon__manage_project` | `action="create"`, `title` |
| Обновить проект | `mcp__archon__manage_project` | `action="update"`, `project_id` |

---

## 🚨 КРИТИЧНІ ПРАВИЛА MCP

### ПРАВИЛО 1: ОБЯЗАТЕЛЬНО project_id при работе с задачами

```python
# ✅ ПРАВИЛЬНО
tasks = await mcp__archon__find_tasks(
    project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    filter_by="status",
    filter_value="todo"
)

# ❌ НЕПРАВИЛЬНО (получишь задачи из ВСЕХ проектов)
tasks = await mcp__archon__find_tasks(
    filter_by="status",
    filter_value="todo"
)
```

### ПРАВИЛО 2: НЕ использовать filter_value="User" для собственных задач

```python
# ❌ НЕПРАВИЛЬНО
my_tasks = await mcp__archon__find_tasks(
    filter_by="assignee",
    filter_value="User"  # Это задачи пользователя, НЕ Project Manager
)

# ✅ ПРАВИЛЬНО
pm_tasks = await mcp__archon__find_tasks(
    project_id=project_id,
    filter_by="assignee",
    filter_value="Archon Project Manager"
)
```

### ПРАВИЛО 3: Всегда проверять наличие project_id перед созданием задачи

```python
# ✅ ПРАВИЛЬНО
if project_id:
    await mcp__archon__manage_task(
        action="create",
        project_id=project_id,
        title="Задача"
    )
else:
    print("❌ ОШИБКА: project_id не определен! Сначала выберите проект.")
```

---

**Навигация:**
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Project Management](02_project_management.md)
