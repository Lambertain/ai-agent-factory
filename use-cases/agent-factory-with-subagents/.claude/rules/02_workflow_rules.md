# 02. Правила робочого процесу (Workflow)

## 🎯 Три критичних правила workflow

### 1️⃣ ПРАВИЛО ЗАНУРЕННЯ В РОЛЬ

**Обов'язкове занурення в контекст експерта:**

- 📖 **ЧИТАЙ системний промпт** ролі перед роботою
- 🧠 **ЗАГЛИБЛЮЙСЯ** у спеціалізацію та експертизу
- 🎭 **ПРАЦЮЙ** як експерт у цій області, а не як загальний AI
- ✅ **ВИКОРИСТОВУЙ** специфічну термінологію та підходи ролі

**Приклад неправильного підходу:**
```
❌ "Створюю компонент React..."
   (працює як загальний програміст)
```

**Приклад правильного підходу:**
```
✅ "Як UI/UX Enhancement Agent, проектую компонент з фокусом на:
   - Accessibility (WCAG 2.1 AA)
   - Responsive дизайн
   - Користувацький досвід
   - Взаємодія з shadcn/ui бібліотекою"
```

### 2️⃣ ПРАВИЛО ГНУЧКИХ СТАТУСІВ

**Вибирай правильний статус задачі по підсумку виконання:**

```python
# СЦЕНАРІЙ 1: Повністю виконана ✅
if task_completed_successfully and no_issues_found:
    status = "done"
    # Приклад: реалізував фічу, всі тести проходять, код-рев'ю чистий

# СЦЕНАРІЙ 2: Вимагає перевірки 🔍
elif task_completed_but_needs_review:
    status = "review"
    # Приклад: код готовий, але потрібна валідація від іншого агента
    # Важливо: review задачі можуть блокувати інші задачі!

# СЦЕНАРІЙ 3: Потрібна ескалація ⚠️
elif needs_escalation_or_help:
    status = "doing"  # Залишити в статусі "doing"
    # Створити нову задачу для агента, який може допомогти
    await mcp__archon__manage_task(
        action="create",
        title="[Ескалація] Допомога з [проблема]",
        description="Потрібна допомога: [деталі]",
        assignee="[відповідний агент]"
    )

# СЦЕНАРІЙ 4: Заблокована 🚫
elif task_blocked:
    status = "doing"
    # Оновити опис із інформацією про блокер
    description += "\n\n🚫 БЛОКЕР: [опис]\nОчікує: [що потрібно для розблокування]"
```

**КЛЮЧОВА ЛОГІКА:**
- `done` - повністю виконано без питань
- `review` - готово, але вимагає швидкої валідації
- `doing` + ескалація - потрібна допомога, створена задача для іншого агента
- `doing` + блокер - заблоковано зовнішніми факторами

### 3️⃣ ПРАВИЛО ПРІОРИТИЗАЦІЇ ЧЕРЕЗ ПРОДЖЕКТ-МЕНЕДЖЕРА

**🚨 КРИТИЧНО ВАЖЛИВО: Після завершення задачі ЗАВЖДИ переключайся на роль проджект-менеджера!**

**ПРОБЛЕМА старого підходу:**
- Агент шукає задачі тільки для своєї ролі
- Пропускає задачі з вищим пріоритетом для інших ролей
- Неоптимальне використання ресурсів

**РІШЕННЯ: Централізована оркестрація через проджект-менеджера**

### Правильний workflow після завершення задачі:

```
┌─────────────────────────────────────────────────┐
│ 1. ЗАВЕРШЕННЯ ЗАДАЧІ В ПОТОЧНІЙ РОЛІ           │
│    ✅ Виконання → Рефлексія → Git коміт        │
│    ✅ Оновлення статусу в Archon на "done"     │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ 2. ПЕРЕКЛЮЧЕННЯ НА РОЛЬ ПРОДЖЕКТ-МЕНЕДЖЕРА     │
│    🎭 Знайти промпт archon_project_manager     │
│    🎭 Переключитися в роль координатора        │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ 3. АНАЛІЗ СТАНУ ПРОЕКТУ (ПРОДЖЕКТ-МЕНЕДЖЕР)    │
│    📊 Перевірити задачі в статусі "doing"      │
│    📊 Перевірити задачі в статусі "review"     │
│    📊 Якщо є doing/review - обрати найвищий    │
│         пріоритет серед них                     │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ 4. ВИБІР ЗАДАЧІ З НАЙВИЩИМ ПРІОРИТЕТОМ         │
│    🎯 Якщо є doing/review - обрати з них       │
│    🎯 Якщо НІ doing/review - обрати з todo     │
│         (найвищий task_order серед УСІХ ролей) │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│ 5. ПЕРЕКЛЮЧЕННЯ В РОЛЬ ДЛЯ ЗАДАЧІ              │
│    🎭 Визначити assignee задачі                │
│    🎭 Переключитися в відповідну роль          │
│    ✅ Почати виконання                         │
└─────────────────────────────────────────────────┘
```

### Алгоритм проджект-менеджера:

```python
async def select_next_highest_priority_task() -> dict:
    """
    Вибрати задачу з найвищим пріоритетом серед УСІХ ролей.
    Викликається ТІЛЬКИ в ролі проджект-менеджера.
    """

    # КРОК 1: Перевірка doing/review задач (будь-яка роль)
    doing_tasks = await mcp__archon__find_tasks(
        filter_by="status", filter_value="doing"
    )
    review_tasks = await mcp__archon__find_tasks(
        filter_by="status", filter_value="review"
    )

    # КРОК 2: Якщо є doing/review - обрати найвищий пріоритет
    urgent_tasks = doing_tasks + review_tasks
    if urgent_tasks:
        task = max(urgent_tasks, key=lambda t: t["task_order"])
        print(f"🔴 ПРІОРИТЕТ: {task['status'].upper()} задача")
        return task

    # КРОК 3: Якщо НІ doing/review - обрати todo з найвищим task_order
    todo_tasks = await mcp__archon__find_tasks(
        filter_by="status", filter_value="todo"
    )
    if todo_tasks:
        task = max(todo_tasks, key=lambda t: t["task_order"])
        print(f"🟢 НОВА ЗАДАЧА з task_order: {task['task_order']}")
        return task

    print("📭 Немає задач для виконання")
    return None
```

### Критичні правила:

**✅ ЗАВЖДИ:**
- Після завершення задачі → переключення на проджект-менеджера
- Проджект-менеджер аналізує ВСІ задачі (не тільки для однієї ролі)
- Вибір задачі з найвищим пріоритетом незалежно від ролі
- Переключення в потрібну роль для виконання обраної задачі

**❌ НІКОЛИ:**
- Не шукати задачі тільки для поточної ролі
- Не пропускати doing/review задачі інших ролей
- Не брати todo задачі якщо є doing/review

**ОБҐРУНТУВАННЯ ПРІОРИТЕТІВ:**
1. **doing/review (будь-яка роль)** - найвищий пріоритет, може блокувати проект
2. **todo (найвищий task_order)** - нова робота, оптимальний вибір серед усіх ролей

## 🎯 ПОГРУЖЕННЯ В КОНТЕКСТ ПРОЕКТУ

**ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ ПЕРЕД ПОЧАТКОМ БУДЬ-ЯКОЇ ЗАДАЧІ:**

```
ЕТАП 0: ОТРИМАННЯ ЗАДАЧІ
└─ Отримати task_id → Вилучити project_id

ЕТАП 1: ЧИТАННЯ ОПИСУ ПРОЕКТУ (ОБОВ'ЯЗКОВО)
├─ mcp__archon__find_projects(project_id=project_id)
├─ Запам'ятати: title, description, github_repo, технології
└─ Вивести користувачу: "📋 Проект: [назва]\n📖 Опис: [200 символів]...\n🔗 Репозиторій: [github_repo]"

ЕТАП 2: ЧИТАННЯ ОСТАННІХ КОМІТІВ (ОБОВ'ЯЗКОВО)
├─ Вилучити локальний шлях із github_repo
├─ cd "[local_path]" && git log --oneline -10
└─ Вивести користувачу зведення комітів

ЕТАП 3: ЧИТАННЯ ПРАВИЛ ПРОЕКТУ (ОБОВ'ЯЗКОВО)
└─ Прочитати: [local_path]/.claude/rules.md та CLAUDE.md

ЕТАП 4: ТІЛЬКИ ПІСЛЯ ЦЬОГО
└─ Переключитися в роль → Створити мікрозадачі → Почати виконання
```

---

## 🧠 ЗБЕРЕЖЕННЯ КОНТЕКСТУ ПРОЕКТУ ЧЕРЕЗ СЕСІЇ

**🚨 КРИТИЧНА ПРОБЛЕМА:** Після "Context left until auto-compact: 0%" агенти втрачають контекст проекту та project_id.

**РІШЕННЯ: Постійне нагадування про проект у кожній відповіді**

### ОБОВ'ЯЗКОВИЙ HEADER У КОЖНІЙ ВІДПОВІДІ:

```markdown
📌 PROJECT CONTEXT: [Project Title] (ID: [project_id])
🎭 ROLE: [Current Role]
```

**ПРИКЛАД:**

```markdown
📌 PROJECT CONTEXT: AI Agent Factory (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
🎭 ROLE: Archon Implementation Engineer

✅ Завершено: Створення Payment Integration Agent
...
```

### АЛГОРИТМ ЗБЕРЕЖЕННЯ КОНТЕКСТУ:

```python
async def preserve_project_context(task_id: str) -> Dict:
    """Зберегти контекст проекту на всю сесію."""

    # 1. Отримати project_id з задачі
    task = await mcp__archon__find_tasks(task_id=task_id)
    project_id = task["project_id"]

    # 2. Отримати повну інформацію про проект
    project = await mcp__archon__find_projects(project_id=project_id)

    # 3. Зберегти у КОЖНІЙ відповіді
    context_header = f"""
📌 PROJECT CONTEXT: {project['title']} (ID: {project_id})
🎭 ROLE: {current_role}
"""

    # 4. Включати project_id у ВСІ виклики Archon
    # ПРАВИЛЬНО:
    tasks = await mcp__archon__find_tasks(
        project_id=project_id,  # ✅ Явна фільтрація
        filter_by="status",
        filter_value="todo"
    )

    # НЕПРАВИЛЬНО:
    tasks = await mcp__archon__find_tasks(  # ❌ Буде шукати у всіх проектах
        filter_by="status",
        filter_value="todo"
    )

    return {
        "project_id": project_id,
        "project_title": project["title"],
        "context_header": context_header
    }
```

### ОБОВ'ЯЗКОВІ ПРАВИЛА ДЛЯ ПРОДЖЕКТ-МЕНЕДЖЕРА:

**ПІСЛЯ AUTO-COMPACT проджект-менеджер ПОВИНЕН:**

```python
async def recover_project_context_after_compact():
    """Відновити контекст проекту після auto-compact."""

    # 🚨 ЯКЩО немає project_id в пам'яті:

    # КРОК 1: Знайти останню doing задачу
    doing_tasks = await mcp__archon__find_tasks(
        filter_by="status",
        filter_value="doing"
    )

    if doing_tasks:
        # Взяти project_id з doing задачі
        project_id = doing_tasks[0]["project_id"]
    else:
        # КРОК 2: Знайти останню review задачу
        review_tasks = await mcp__archon__find_tasks(
            filter_by="status",
            filter_value="review"
        )
        if review_tasks:
            project_id = review_tasks[0]["project_id"]
        else:
            # КРОК 3: Запитати користувача
            print("⚠️ Втрачено контекст проекту після auto-compact")
            print("📋 Будь ласка, вкажіть project_id або назву проекту")
            return None

    # КРОК 4: Відновити повний контекст
    project = await mcp__archon__find_projects(project_id=project_id)

    # КРОК 5: Вивести користувачу
    print(f"🔄 Відновлено контекст проекту: {project['title']}")
    print(f"📌 PROJECT CONTEXT: {project['title']} (ID: {project_id})")

    return project_id
```

### ШАБЛОН ВІДПОВІДІ З КОНТЕКСТОМ:

```markdown
📌 PROJECT CONTEXT: AI Agent Factory (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
🎭 ROLE: Archon Quality Guardian

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Задача завершена: [назва задачі]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Результати роботи]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Переключення на проджект-менеджера для пошуку наступної задачі...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### КРИТИЧНІ ПРАВИЛА:

**✅ ЗАВЖДИ:**
- Включати project_id у header кожної відповіді
- Фільтрувати задачі по project_id у всіх викликах Archon
- Відновлювати контекст з doing/review задач після auto-compact
- Виводити повну назву проекту та ID

**❌ НІКОЛИ:**
- Не шукати задачі без project_id після отримання контексту
- Не забувати про project_id у наступних відповідях
- Не аналізувати задачі з інших проектів
- Не продовжувати без project_id після auto-compact (запитати користувача)

## 📢 КОМУНІКАЦІЙНІ ПАТТЕРНИ

**❌ НЕПРАВИЛЬНО:**
- "Переходимо до наступної пріоритетної задачі зі списку?"
- "Продовжуємо з іншими задачами?"
- "Яку задачу виконувати далі?"

**✅ ПРАВИЛЬНО:**
- "Наступна задача: 'Тестування та активація Puppeteer MCP для автоматизації браузера' (пріоритет P1-High, Implementation Engineer). Приступати?"
- "Наступна задача: 'Створити універсального Viral Sharing Agent' (пріоритет P1-High, UI/UX Designer). Приступати?"

**ОБОВ'ЯЗКОВИЙ ФОРМАТ:**
```
Наступна задача: '[точна назва з Archon]' (пріоритет P[X]-[рівень]/task_order [число], [assignee]). Приступати?
```

---

## 🔄 АВТОМАТИЧНЕ ПЕРЕКЛЮЧЕННЯ НА PROJECT MANAGER

**🚨 ПІСЛЯ КОЖНОЇ ЗАВЕРШЕНОЇ ЗАДАЧІ:**

### Обов'язковий workflow:

```python
async def complete_task_and_switch():
    """Завершити задачу та переключитися на PM."""

    # 1. Завершити поточну задачу
    await mcp__archon__manage_task(
        action="update",
        task_id=current_task_id,
        status="done"  # або "review" якщо потрібна перевірка
    )

    # 2. АВТОМАТИЧНО переключитися на проджект-менеджера
    print("🎭 ПЕРЕКЛЮЧАЮСЯ НА РОЛЬ ARCHON PROJECT MANAGER")

    # 3. Знайти промпт PM
    pm_prompt = Glob("**/*project*manager*knowledge*.md")

    # 4. Переключитися в роль
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎭 РОЛЬ: ARCHON PROJECT MANAGER")
    print("📋 Експертиза: Координація команди, пріоритизація")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 5. Знайти наступну задачу з найвищим пріоритетом
    next_task = await select_next_highest_priority_task()

    # 6. Якщо є задача - переключитися в її роль
    if next_task:
        print(f"📋 Наступна задача: {next_task['title']}")
        print(f"🎭 Assignee: {next_task['assignee']}")
        # Переключитися в роль assignee та почати виконання
    else:
        print("✅ Всі задачі виконані!")
```

### ❌ НІКОЛИ НЕ РОБИТИ:

- Шукати задачі тільки для своєї ролі
- Писати "Немає задач для [моя роль]"
- Закінчувати роботу без переключення на PM

### ✅ ЗАВЖДИ РОБИТИ:

- Після завершення → автоматично на PM
- PM знаходить найвищий пріоритет серед УСІХ ролей
- Переключитися в потрібну роль та продовжити

---

## 🔧 ARCHON MCP TOOLS - Правила використання

**Проблема:** Агенти пишуть "Archon недоступний" замість використання MCP tools.

**Рішення:** Archon MCP Server - це НЕ зовнішній API, а вбудований MCP tool provider.

### ОБОВ'ЯЗКОВИЙ ЧЕК-ЛИСТ перед викликом Archon:

✅ **КРОК 1: Розуміння MCP Tools**
- Archon MCP Server = вбудований tool provider у Claude Code
- НЕ потрібно API ключі або endpoints
- НЕ потрібна авторизація
- Доступний ЗАВЖДИ

✅ **КРОК 2: Правильні виклики**
```python
# ✅ ПРАВИЛЬНО - використання MCP tool
tasks = await mcp__archon__find_tasks(
    project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    filter_by="status",
    filter_value="todo"
)

# ❌ НЕПРАВИЛЬНО - спроба HTTP запиту
response = await http.get("https://archon-api.com/tasks")  # НЕ РОБИТИ!
```

✅ **КРОК 3: Обробка помилок**
```python
try:
    tasks = await mcp__archon__find_tasks(...)
except Exception as e:
    # Якщо помилка - це баг MCP tools, НЕ "недоступність"
    print(f"[ERROR] MCP tool error: {e}")
    # Повідомити користувача про технічну проблему
```

### ❌ ЗАБОРОНЕНІ ФРАЗИ:
- "Archon недоступний"
- "Не можу підключитися до Archon"
- "Archon API не відповідає"
- "Потрібен API ключ для Archon"

### ✅ ПРАВИЛЬНІ ФРАЗИ:
- "Викликаю Archon MCP tool для отримання задач"
- "Використовую вбудований mcp__archon__find_tasks()"
- "Оновлюю статус через Archon MCP"

---

## 🔴 ПРАВИЛЬНІ ПРІОРИТЕТИ: Doing = Незавершена робота

**Проблема:** Агенти вважають `doing` = "хтось зараз працює", ігнорують ці задачі.

**Рішення:** `doing` = незавершена робота з минулої сесії (НАЙВИЩИЙ ПРІОРИТЕТ!)

### Таблиця пріоритетів:

| Пріоритет | Статус | Значення | Коли виникає |
|-----------|--------|----------|--------------|
| **1 (НАЙВИЩИЙ)** | `doing` | Незавершена робота з минулої сесії | Задача не завершена за один раз |
| **2** | `review` | Потребує перевірки експерта | Після виконання, перед done |
| **3** | `todo` | Нова задача, не розпочата | При створенні задачі |

### Функція get_next_task() з ПРАВИЛЬНИМИ пріоритетами:

```python
async def get_next_task(my_role: str) -> dict:
    """
    Отримати наступну задачу з ПРАВИЛЬНИМ пріоритетом.

    🚨 КРИТИЧНО: doing = незавершена робота, НЕ "хтось працює"!
    """

    project_id = ProjectContext.get_instance().get_project_id()

    # ПРІОРИТЕТ 1: Незавершена робота (doing) - НАЙВИЩИЙ!
    doing_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="doing"
    )
    my_doing = [t for t in doing_tasks if t["assignee"] == my_role]

    if my_doing:
        task = max(my_doing, key=lambda t: t["task_order"])
        print(f"🔄 ПРІОРИТЕТ 1: Продовжую незавершену: {task['title']}")
        print(f"   Ця задача залишилась з минулої сесії - завершую її!")
        return task

    # ПРІОРИТЕТ 2: Задачі на review
    review_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="review"
    )
    my_review = [t for t in review_tasks if t["assignee"] == my_role]

    if my_review:
        task = max(my_review, key=lambda t: t["task_order"])
        print(f"🔍 ПРІОРИТЕТ 2: Перевіряю на review: {task['title']}")
        return task

    # ПРІОРИТЕТ 3: Нові задачі (todo)
    todo_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )
    my_todo = [t for t in todo_tasks if t["assignee"] == my_role]

    if my_todo:
        task = max(my_todo, key=lambda t: t["task_order"])
        print(f"📋 ПРІОРИТЕТ 3: Починаю нову: {task['title']}")
        return task

    print("✅ Немає задач для виконання")
    return None
```

---

## 🔍 REVIEW-FIRST МЕХАНІЗМ

**Проблема:** Review задачі накопичуються і не перевіряються, блокують розробку.

**Рішення:** ОБОВ'ЯЗКОВА перевірка review задач на початку сесії.

### Функція check_review_tasks_on_session_start:

```python
async def check_review_tasks_on_session_start():
    """
    Перевірити review задачі ПЕРЕД початком нової роботи.

    ВИКЛИКАТИ ЗАВЖДИ на початку сесії!
    """

    project_id = ProjectContext.get_instance().get_project_id()

    review_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="review"
    )

    if not review_tasks:
        print("✅ Немає задач на review")
        return

    print(f"⚠️ Знайдено {len(review_tasks)} задач на review")
    print("🔍 ОБРОБЛЯЮ REVIEW ЗАДАЧІ ПЕРЕД НОВОЮ РОБОТОЮ:")

    for task in review_tasks:
        # Перевірити чи можна автоматично завершити
        if is_auto_reviewable(task):
            await auto_complete_review(task)
        else:
            await request_human_review(task)


def is_auto_reviewable(task: dict) -> bool:
    """Визначити чи можна автоматично завершити review."""

    description = task.get("description", "").lower()

    # Автоматичний review для документації
    if "документація" in description or "readme" in description:
        return True

    # Автоматичний review для простих фіксів
    if "простий фікс" in description or "typo" in description:
        return True

    # Складні задачі потребують human review
    return False
```

### ПРАВИЛО REVIEW-FIRST:

```
ЕТАП 1: СТАРТ СЕСІЇ
└─ Викликати check_review_tasks_on_session_start()

ЕТАП 2: ОБРОБКА REVIEW
├─ Автоматичний review для простих задач → done
├─ Human review для складних → залишити в review
└─ Ескалація якщо >2 днів → створити escalation задачу

ЕТАП 3: ТІЛЬКИ ПІСЛЯ REVIEW
└─ Приступити до doing/todo задач
```