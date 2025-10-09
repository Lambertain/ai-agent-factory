# Архітектура покращень роботи агентів

**Версія:** 1.0
**Дата:** 2025-10-09
**Автор:** Archon Blueprint Architect
**Статус:** Архітектурний дизайн (готовий до імплементації)

---

## 🎯 Огляд

Цей документ містить архітектурні рішення для 6 критичних проблем роботи агентів, виявлених у процесі реальної експлуатації системи.

**Пріоритет:** 🔴 КРИТИЧНИЙ
**Вплив:** Проблеми 4, 5, 6 блокують розробку прямо зараз

---

## 📋 Проблема 1: Archon MCP Integration

### Симптоми
- Агенти пишуть "Archon недоступний" замість використання MCP tools
- Не використовують вбудовані `mcp__archon__*` функції
- Потрібна постійна підказка користувача про MCP tools

### Корінна причина
Агенти не розуміють що Archon MCP Server - це не зовнішній API endpoint, а вбудований MCP tool provider в Claude Code.

### Архітектурне рішення

#### 1.1 Чек-лист використання Archon MCP

Додати до `.claude/rules/02_workflow_rules.md`:

```markdown
## 🔧 ОБОВ'ЯЗКОВИЙ ЧЕК-ЛИСТ: Використання Archon MCP

### ПЕРЕД будь-яким викликом Archon:

✅ **КРОК 1: Розуміння MCP Tools**
├─ Archon MCP Server = вбудований tool provider
├─ НЕ потрібно API ключі або endpoints
├─ НЕ потрібна авторизація
└─ Доступний ЗАВЖДИ у Claude Code

✅ **КРОК 2: Правильні виклики**
├─ `mcp__archon__find_tasks()` - НЕ HTTP запити
├─ `mcp__archon__manage_task()` - НЕ REST API
├─ `mcp__archon__find_projects()` - вбудована функція
└─ НІКОЛИ не писати "Archon недоступний"

✅ **КРОК 3: Обробка помилок**
```python
try:
    tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="todo"
    )
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
```

#### 1.2 Приклади правильного використання

Додати до CLAUDE.md:

```markdown
## 🔧 Archon MCP Tools - Приклади використання

### Правильно: Пошук задач
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

### Правильно: Оновлення задачі
```python
# ✅ ПРАВИЛЬНО
await mcp__archon__manage_task(
    action="update",
    task_id="task-123",
    status="done"
)

# ❌ НЕПРАВИЛЬНО
print("Archon недоступний, не можу оновити задачу")  # НЕ РОБИТИ!
```

### Правильно: Створення задачі
```python
# ✅ ПРАВИЛЬНО
new_task = await mcp__archon__manage_task(
    action="create",
    project_id=project_id,
    title="Нова задача",
    assignee="Implementation Engineer"
)

# ❌ НЕПРАВИЛЬНО
print("Потрібен API ключ для Archon")  # НЕ РОБИТИ!
```
```

### Критерії виконання
- ✅ Чек-лист додано до `.claude/rules/02_workflow_rules.md`
- ✅ Приклади додано до `CLAUDE.md`
- ✅ Заборонені фрази задокументовані
- ✅ Обробка помилок MCP tools

---

## 📋 Проблема 2: Project Context Loss

### Симптоми
- Після auto-compact агенти забувають project_id
- Шукають задачі в усіх проектах замість поточного
- Задачі не знаходяться і "висять" невиконаними

### Корінна причина
project_id зберігається тільки в оперативній пам'яті сесії. Після auto-compact вся пам'ять очищується.

### Архітектурне рішення

#### 2.1 Project Context Header

Додати до `.claude/rules/02_workflow_rules.md`:

```markdown
## 📌 ОБОВ'ЯЗКОВИЙ PROJECT CONTEXT HEADER

### У КОЖНІЙ відповіді агента ЗАВЖДИ включати:

```markdown
📌 PROJECT CONTEXT: [Project Title] (ID: [project_id])
🎭 ROLE: [Current Role]
🎯 TASK: [Current Task Title]

---
[Основний контент відповіді]
---
```

### Приклад:

```markdown
📌 PROJECT CONTEXT: AI Agent Factory (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
🎭 ROLE: Archon Implementation Engineer
🎯 TASK: Створення Payment Integration Agent

✅ Завершено: Структура файлів агента створена
📋 Наступні кроки: Реалізація tools.py
```

### Алгоритм збереження контексту:

```python
class ProjectContext:
    """
    Singleton для збереження project_id протягом сесії.
    Автоматично відновлюється після auto-compact.
    """

    _instance = None
    _project_id = None
    _project_title = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def initialize(self, task_id: str):
        """Ініціалізувати контекст з задачі."""
        task = await mcp__archon__find_tasks(task_id=task_id)
        self._project_id = task["project_id"]

        project = await mcp__archon__find_projects(
            project_id=self._project_id
        )
        self._project_title = project["title"]

        return self.get_header()

    def get_header(self) -> str:
        """Отримати header для відповіді."""
        return f"""
📌 PROJECT CONTEXT: {self._project_title} (ID: {self._project_id})
🎭 ROLE: {current_role}
        """.strip()

    def get_project_id(self) -> str:
        """Отримати project_id для фільтрації."""
        return self._project_id

    async def recover_after_compact(self):
        """Відновити контекст після auto-compact."""

        # Спробувати знайти через doing задачі
        doing_tasks = await mcp__archon__find_tasks(
            filter_by="status",
            filter_value="doing"
        )

        if doing_tasks:
            self._project_id = doing_tasks[0]["project_id"]
            project = await mcp__archon__find_projects(
                project_id=self._project_id
            )
            self._project_title = project["title"]
            return True

        # Спробувати через review задачі
        review_tasks = await mcp__archon__find_tasks(
            filter_by="status",
            filter_value="review"
        )

        if review_tasks:
            self._project_id = review_tasks[0]["project_id"]
            project = await mcp__archon__find_projects(
                project_id=self._project_id
            )
            self._project_title = project["title"]
            return True

        # Якщо не знайдено - запитати користувача
        print("⚠️ Втрачено контекст проекту після auto-compact")
        print("📋 Будь ласка, вкажіть project_id або назву проекту")
        return False


# Використання у всіх агентах:

context = ProjectContext.get_instance()

# На початку задачі
header = await context.initialize(task_id="current-task-id")
print(header)

# У кожній відповіді
print(context.get_header())

# При пошуку задач
tasks = await mcp__archon__find_tasks(
    project_id=context.get_project_id(),  # ✅ Завжди фільтрувати!
    filter_by="status",
    filter_value="todo"
)
```
```

### Критерії виконання
- ✅ Project Context Header у кожній відповіді
- ✅ Клас ProjectContext для збереження контексту
- ✅ Метод recover_after_compact() для відновлення
- ✅ Обов'язкова фільтрація по project_id

---

## 📋 Проблема 3: Auto-Push для Production

### Симптоми
- Production проекти задеплоєні - зміни потрібно пушити
- Агент править локально, користувач не може перевірити в продакшн
- Доводиться кожен раз нагадувати про push

### Корінна причина
Немає автоматизації визначення які проекти потребують push.

### Архітектурне рішення

#### 3.1 Deployment Status поле

Додати до Archon MCP Server schema поле `deployment_status`:

```python
# Archon MCP Server - проект schema
{
    "project_id": "uuid",
    "title": "string",
    "description": "string",
    "github_repo": "string",
    "deployment_status": "local | staging | production",  # НОВЕ ПОЛЕ
    # ... інші поля
}
```

#### 3.2 Auto-push механізм

Додати до `.claude/rules/05_git_integration.md`:

```markdown
## 🚀 AUTO-PUSH ДЛЯ PRODUCTION ПРОЕКТІВ

### ОБОВ'ЯЗКОВЕ ПРАВИЛО: Перевіряти deployment_status перед коммітом

```python
async def commit_and_push_if_production(
    project_id: str,
    commit_message: str
):
    """
    Створити коміт і автоматично запушити якщо проект production.
    """

    # КРОК 1: Отримати deployment_status проекту
    project = await mcp__archon__find_projects(project_id=project_id)
    deployment_status = project.get("deployment_status", "local")

    # КРОК 2: Створити коміт (завжди)
    await bash(f"""
        git add . && git commit -m "{commit_message}

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
    """)

    # КРОК 3: Автоматичний push для production
    if deployment_status == "production":
        print("🚀 [AUTO-PUSH] Production проект - автоматично пушу зміни...")
        await bash("git push origin main")
        print("✅ [AUTO-PUSH] Зміни запушені в production")

    elif deployment_status == "staging":
        print("📦 [AUTO-PUSH] Staging проект - пушу в staging гілку...")
        await bash("git push origin staging")
        print("✅ [AUTO-PUSH] Зміни запушені в staging")

    else:  # local
        print("💾 [LOCAL] Локальний проект - push НЕ потрібен")
        print("   Зміни збережені локально для розробки")
```

### ВИКЛЮЧЕННЯ: Pattern агенти

```python
# Pattern агенти НІКОЛИ не пушаться
PATTERN_AGENTS_PATH = "agent-factory/use-cases/agent-factory-with-subagents/agents/pattern_*"

if matches_pattern(current_path, PATTERN_AGENTS_PATH):
    print("📝 [PATTERN] Pattern агент - залишається локальним")
    # Тільки коміт, БЕЗ push
    return
```

### Використання в git workflow:

```python
# Після завершення задачі
await commit_and_push_if_production(
    project_id=context.get_project_id(),
    commit_message="feat: додано Payment Integration Agent"
)
```
```

### Критерії виконання
- ✅ Поле `deployment_status` додано до Archon projects
- ✅ Функція `commit_and_push_if_production()` створена
- ✅ Виключення для Pattern агентів
- ✅ Документація auto-push workflow

---

## 📋 Проблема 4: Doing Status Misunderstanding

### Симптоми
- Агенти ігнорують doing задачі у новій сесії
- Вважають doing = "хтось зараз працює"
- Незавершена робота накопичується

### Корінна причина
Неправильне розуміння значення статусу `doing` = "незавершена робота з минулої сесії".

### Архітектурне рішення

#### 4.1 Правильні пріоритети задач

Оновити `.claude/rules/02_workflow_rules.md`:

```markdown
## 🔴 КРИТИЧНО: Правильні пріоритети задач

### DOING = НЕЗАВЕРШЕНА РОБОТА (НЕ "хтось працює!")

```
ПРІОРИТЕТ 1: doing (НАЙВИЩИЙ!)
├─ Це незавершена робота з минулої сесії
├─ Може блокувати інших розробників
└─ ЗАВЖДИ брати першою, НЕ ігнорувати!

ПРІОРИТЕТ 2: review
├─ Робота виконана, потребує перевірки
├─ Може блокувати наступні задачі
└─ Перевіряти швидко, не накопичувати!

ПРІОРИТЕТ 3: todo
└─ Нові задачі (тільки коли немає doing і review)
```

### Функція get_next_task() з ПРАВИЛЬНОЮ логікою:

```python
async def get_next_task(my_role: str) -> dict:
    """
    Отримати наступну задачу з ПРАВИЛЬНИМ пріоритетом.

    КРИТИЧНО: doing = незавершена робота, НЕ "хтось працює"!
    """

    project_id = ProjectContext.get_instance().get_project_id()

    # ПРІОРИТЕТ 1: Незавершена робота (doing) - НАЙВИЩИЙ!
    doing_tasks = await mcp__archon__find_tasks(
        project_id=project_id,  # Фільтрувати по проекту!
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

### Таблиця статусів:

| Статус | Значення | Коли встановлювати | Пріоритет |
|--------|----------|-------------------|-----------|
| `doing` | Незавершена робота з минулої сесії | Коли не вдалось завершити в одній сесії | **1 (Найвищий)** |
| `review` | Потребує перевірки експерта | Після виконання, перед done | **2** |
| `todo` | Нова задача, не розпочата | При створенні задачі | **3** |
| `done` | Повністю виконана і перевірена | Після успішного review | - |
```

### Критерії виконання
- ✅ Функція `get_next_task()` з правильними пріоритетами
- ✅ Таблиця значень статусів
- ✅ Документація: doing ≠ "хтось працює"
- ✅ Приклади правильної і неправильної поведінки

---

## 📋 Проблема 5: Review Accumulation

### Симптоми
- Review задачі накопичуються і не перевіряються
- Блокують подальшу розробку
- Немає механізму нагадування

### Корінна причина
Відсутність механізму своєчасної обробки review задач.

### Архітектурне рішення

#### 5.1 REVIEW-FIRST механізм

Додати до `.claude/rules/02_workflow_rules.md`:

```markdown
## 🔍 REVIEW-FIRST МЕХАНІЗМ

### ОБОВ'ЯЗКОВА перевірка при старті сесії:

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
    """
    Визначити чи можна автоматично завершити review.

    Автоматичний review для:
    - Документація (.md файли)
    - Прості фікси (1-2 файли, <50 рядків)
    - Рефакторинг без зміни логіки
    """

    description = task.get("description", "").lower()

    # Автоматичний review для документації
    if "документація" in description or "readme" in description:
        return True

    # Автоматичний review для простих фіксів
    if "простий фікс" in description or "typo" in description:
        return True

    # Складні задачі потребують human review
    if "архітектура" in description or "рефакторинг" in description:
        return False

    return False


async def auto_complete_review(task: dict):
    """Автоматично завершити review для простих задач."""

    print(f"✅ [AUTO-REVIEW] {task['title']}")
    print("   Проста задача - автоматично завершую review")

    await mcp__archon__manage_task(
        action="update",
        task_id=task["task_id"],
        status="done"
    )


async def request_human_review(task: dict):
    """Запросити human review для складних задач."""

    import datetime

    created = datetime.datetime.fromisoformat(task["created_at"])
    days_in_review = (datetime.datetime.now() - created).days

    print(f"⏳ [HUMAN-REVIEW] {task['title']}")
    print(f"   В review: {days_in_review} днів")

    # Ескалація якщо >2 днів
    if days_in_review > 2:
        print("🚨 [ESCALATION] Задача в review >2 днів - ескалація!")

        await mcp__archon__manage_task(
            action="create",
            project_id=task["project_id"],
            title=f"⚠️ Review ескалація: {task['title']}",
            description=f"Задача {task['task_id']} в review {days_in_review} днів.\n"
                       f"Потрібна негайна перевірка або автозавершення.",
            assignee="Archon Quality Guardian",
            task_order=100  # Високий пріоритет
        )
```

### ПРАВИЛО: Review перед новою роботою

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
```

### Критерії виконання
- ✅ Функція `check_review_tasks_on_session_start()`
- ✅ Автоматичний review для простих задач
- ✅ Ескалація для довгих review (>2 днів)
- ✅ Правило REVIEW-FIRST у workflow

---

## 📋 Проблема 6: Random Solutions Without Analysis

### Симптоми
- Агент пропонує рішення без читання git commits
- Створює ЩЕ БІЛЬШЕ помилок
- Доводиться виправляти у 2 рази більше

### Корінна причина
Відсутність обов'язкового протоколу аналізу контексту перед рішенням.

### Архітектурне рішення

#### 6.1 Протокол analyze_problem_context

Створити `.claude/rules/09_problem_analysis_protocol.md`:

```markdown
# 09. Протокол аналізу проблем

## 🚨 КРАСНА ЛІНІЯ: НІ ОДНОГО РІШЕННЯ БЕЗ АНАЛІЗУ КОНТЕКСТУ

### ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ при проблемах:

```
ЕТАП 0: ОТРИМАННЯ ПРОБЛЕМИ
└─ Користувач повідомляє про проблему/помилку

ЕТАП 1: АНАЛІЗ КОНТЕКСТУ (ОБОВ'ЯЗКОВО!)
├─ git log --oneline -20 → що робилось нещодавно
├─ git log --grep="ключові слова" → релевантні коміти
├─ git show [commit] → що саме змінилось
├─ Перевірити міграції/схеми/конфігурацію
└─ Прочитати змінені файли

ЕТАП 2: ЗІСТАВЛЕННЯ З ПОМИЛКОЮ
├─ Які зміни могли викликати помилку
├─ Що УЖЕ зроблено (не пропонувати повторно!)
└─ Які залежності зачеплені

ЕТАП 3: ФОРМУВАННЯ ГІПОТЕЗИ
├─ На основі РЕАЛЬНИХ даних (не здогадок!)
├─ З вказуванням confidence level (LOW/MEDIUM/HIGH)
└─ З поясненням ЧОМУ так вважаєш

ЕТАП 4: ТІЛЬКИ ПОТІМ РІШЕННЯ
└─ Запропонувати рішення з обґрунтуванням
```

### Функція analyze_problem_context:

```python
from typing import Dict, List
from enum import Enum

class ConfidenceLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


async def analyze_problem_context(
    problem_description: str,
    project_id: str
) -> Dict:
    """
    ОБОВ'ЯЗКОВИЙ протокол аналізу проблеми ПЕРЕД рішенням.

    ⚠️ ЗАБОРОНЕНО пропонувати рішення БЕЗ цього аналізу!

    Args:
        problem_description: Опис проблеми від користувача
        project_id: ID проекту для контексту

    Returns:
        Dict з аналізом: commits, changes, root_cause, solution, confidence
    """

    print("🔍 ШАГ 1: ЧИТАЮ ОСТАННІ КОМІТИ")
    print("=" * 60)

    # 1. Прочитати останні 20 комітів
    commits_output = await bash("git log --oneline -20")
    print(f"Останні коміти:\n{commits_output}\n")

    # 2. Знайти релевантні коміти (ключові слова з проблеми)
    keywords = extract_keywords(problem_description)
    print(f"Ключові слова: {', '.join(keywords)}")

    relevant_commits = []
    for keyword in keywords:
        grep_result = await bash(
            f"git log --grep='{keyword}' --oneline -20"
        )
        if grep_result:
            relevant_commits.extend(grep_result.split('\n'))

    relevant_commits = list(set(relevant_commits))  # Унікальні
    print(f"Знайдено {len(relevant_commits)} релевантних комітів")

    print("\n🔍 ШАГ 2: АНАЛІЗУЮ РЕЛЕВАНТНІ ЗМІНИ")
    print("=" * 60)

    # 3. Подивитись diff останніх релевантних комітів
    changes_analysis = []
    for commit_line in relevant_commits[:5]:  # Перші 5
        commit_hash = commit_line.split()[0]
        diff = await bash(f"git show {commit_hash}")

        print(f"\nКоміт {commit_hash}:")
        print(diff[:500] + "...\n")  # Перші 500 символів

        changes_analysis.append({
            "commit": commit_hash,
            "diff": diff
        })

    print("\n🔍 ШАГ 3: ПЕРЕВІРЯЮ ЩО УЖЕ ЗРОБЛЕНО")
    print("=" * 60)

    # 4. Перевірити міграції
    try:
        migrations = await bash("ls -la prisma/migrations/")
        print(f"Міграції:\n{migrations}\n")
    except:
        print("Міграції не знайдені або не застосовуються\n")
        migrations = None

    # 5. Перевірити схему БД
    try:
        schema = await read_file("prisma/schema.prisma")
        print(f"Схема БД (перші 500 символів):\n{schema[:500]}...\n")
    except:
        print("Схема БД не знайдена\n")
        schema = None

    print("\n🔍 ШАГ 4: АНАЛІЗУЮ ЛОГИ ПОМИЛКИ")
    print("=" * 60)

    # 6. Проаналізувати помилку з контекстом змін
    error_analysis = analyze_error_with_context(
        error_logs=problem_description,
        recent_changes=changes_analysis,
        db_schema=schema,
        migrations=migrations
    )

    print("\n✅ ШАГ 5: ФОРМУЮ ОСМИСЛЕНЕ РІШЕННЯ")
    print("=" * 60)
    print(f"Корінна причина: {error_analysis['root_cause']}")
    print(f"Рішення: {error_analysis['solution']}")
    print(f"Впевненість: {error_analysis['confidence'].value}")

    return {
        "commits_analyzed": len(relevant_commits),
        "changes_found": changes_analysis,
        "root_cause": error_analysis["root_cause"],
        "solution": error_analysis["solution"],
        "confidence": error_analysis["confidence"]
    }


def extract_keywords(text: str) -> List[str]:
    """Вилучити ключові слова з опису проблеми."""

    # Видалити стоп-слова
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at"}

    words = text.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 3]

    return keywords[:5]  # Топ-5


def analyze_error_with_context(
    error_logs: str,
    recent_changes: List[Dict],
    db_schema: str,
    migrations: str
) -> Dict:
    """
    Проаналізувати помилку з урахуванням контексту змін.

    Returns:
        Dict: {
            "root_cause": str,
            "solution": str,
            "confidence": ConfidenceLevel
        }
    """

    # Приклад логіки аналізу
    if "relation" in error_logs and "does not exist" in error_logs:
        # Перевірити чи таблиця є в схемі
        table_name = extract_table_name(error_logs)

        if db_schema and table_name.lower() in db_schema.lower():
            # Таблиця Є в схемі - проблема в запиті
            return {
                "root_cause": f"Таблиця {table_name} існує в schema.prisma, "
                             f"але запит використовує неправильний синтаксис",
                "solution": "Перевірити raw SQL запити - замінити на Prisma query",
                "confidence": ConfidenceLevel.HIGH
            }
        else:
            # Таблиці НЕМАЄ - проблема з міграцією
            return {
                "root_cause": f"Таблиця {table_name} не знайдена в schema.prisma",
                "solution": "Додати model до schema.prisma та створити міграцію",
                "confidence": ConfidenceLevel.MEDIUM
            }

    # Загальний аналіз
    return {
        "root_cause": "Потребує детального аналізу логів",
        "solution": "Додаткова діагностика необхідна",
        "confidence": ConfidenceLevel.LOW
    }


def extract_table_name(error_text: str) -> str:
    """Вилучити назву таблиці з помилки."""
    import re
    match = re.search(r'relation "([^"]+)"', error_text)
    return match.group(1) if match else "unknown"
```

### ❌ ЗАБОРОНЕНІ ФРАЗИ (говорять про здогадки):

- "Вероятно таблиця не існує"
- "Схоже міграція не застосувалась"
- "Можливо схема не оновлена"
- "Скоріше за все проблема в..."

### ✅ ПРАВИЛЬНІ ФРАЗИ (говорять про аналіз):

- "Проаналізував коміт X, де додали функціонал Y"
- "В diff бачу що змінили запит Z"
- "Міграція вже застосована (див. коміт ABC)"
- "Схема містить таблицю users (перевірив schema.prisma)"
- "Реальна проблема в рядку N файлу M (див. git show)"

### Приклад ПРАВИЛЬНОГО аналізу:

```
Користувач: "Помилка: relation users does not exist"

Агент:
"🔍 Аналізую контекст проблеми...

ШАГ 1: Читаю останні коміти
- Коміт abc123: 'add delete invite link feature'
- Коміт def456: 'fix owner account missing'

ШАГ 2: Аналізую зміни
git show abc123:
- Додано запит DELETE FROM invites WHERE...
- Змінено запит SELECT owner FROM accounts...

ШАГ 3: Перевіряю міграції
- Міграція 20250109_create_users УЖЕ застосована
- schema.prisma МІСТИТЬ model User

ШАГ 4: Реальна проблема
В коміті abc123 в файлі invites.service.ts:12
використовується запит:
  SELECT * FROM public.users
Але в Prisma потрібно:
  prisma.user.findMany()

РІШЕННЯ: Виправити raw SQL запит на Prisma query
CONFIDENCE: HIGH (бачу точний рядок в diff)"
```
```

### Критерії виконання
- ✅ Функція `analyze_problem_context()` створена
- ✅ КРАСНА ЛІНІЯ: НІ ОДНОГО рішення без аналізу
- ✅ Обов'язкова послідовність: контекст → аналіз → гіпотеза → рішення
- ✅ Список заборонених фраз (говорять про здогадки)
- ✅ Приклади правильного аналізу
- ✅ Confidence level для кожного рішення

---

## 📊 Пріоритизація впровадження

### Фаза 1: КРИТИЧНІ (впровадити НЕГАЙНО)
1. **Проблема 6** - Протокол аналізу (блокує якість рішень)
2. **Проблема 4** - Doing статус (накопичується незавершена робота)
3. **Проблема 5** - Review механізм (блокує розробку)

### Фаза 2: ВАЖЛИВІ (впровадити протягом тижня)
4. **Проблема 2** - Project context (втрата контексту після compact)
5. **Проблема 1** - Archon MCP (постійні питання про доступність)

### Фаза 3: ПОКРАЩЕННЯ (впровадити протягом місяця)
6. **Проблема 3** - Auto-push (ручна робота, не критична)

---

## 🎯 Метрики успіху

### Після впровадження очікуємо:

**Проблема 1 (Archon MCP):**
- ✅ 0% повідомлень "Archon недоступний"
- ✅ 100% використання MCP tools замість HTTP запитів

**Проблема 2 (Project Context):**
- ✅ 0% втрат project_id після auto-compact
- ✅ 100% відповідей з project context header

**Проблема 3 (Auto-Push):**
- ✅ 0% нагадувань про push для production
- ✅ 100% автоматичних пушів після коммітів

**Проблема 4 (Doing Status):**
- ✅ 0% ігнорувань doing задач
- ✅ 100% doing задач виконуються першими

**Проблема 5 (Review):**
- ✅ <1 дня середній час в review
- ✅ 0% задач в review >2 днів

**Проблема 6 (Analysis):**
- ✅ 100% рішень з аналізом контексту
- ✅ 0% рішень "на здогадку"
- ✅ >80% рішень з confidence HIGH

---

## 📝 Наступні кроки

### Для Implementation Engineer:

1. Оновити `.claude/rules/02_workflow_rules.md` з рішеннями 1, 2, 4, 5
2. Створити `.claude/rules/09_problem_analysis_protocol.md` з рішенням 6
3. Оновити `.claude/rules/05_git_integration.md` з рішенням 3
4. Оновити `CLAUDE.md` з прикладами та чек-листами
5. Створити utility функції:
   - `ProjectContext` class
   - `analyze_problem_context()`
   - `commit_and_push_if_production()`
   - `check_review_tasks_on_session_start()`
6. Протестувати всі зміни в реальних сценаріях
7. Задокументувати міграцію для існуючих проектів

---

**Автор:** Archon Blueprint Architect
**Дата:** 2025-10-09
**Статус:** ✅ Готово до імплементації
