# 02a. Управління контекстом проекту (Project Context Management)

## 🚨 КРИТИЧНА ПРОБЛЕМА: Втрата project_id після auto-compact

**Проблема:** Після "Context left until auto-compact: 0%" агенти втрачають контекст проекту та project_id.

**Наслідки:**
- Проджект-менеджер показує задачі з УСІХ проектів замість поточного
- Агенти не можуть фільтрувати задачі по project_id
- Втрата контексту про те, над яким проектом працюємо

**Рішення:** Триступенева система збереження та відновлення контексту

---

## 📌 РІВЕНЬ 1: ОБОВ'ЯЗКОВИЙ HEADER У КОЖНІЙ ВІДПОВІДІ

**🚨 ПРАВИЛО:** КОЖНА відповідь агента ПОВИННА починатися з цього header'а:

```markdown
📌 PROJECT CONTEXT: [Project Title] (ID: [project_id])
🎭 ROLE: [Current Role]
```

**ЧОМУ ЦЕ КРИТИЧНО:**
- Після auto-compact Claude втрачає project_id з пам'яті
- Header нагадує агенту про контекст проекту в КОЖНІЙ відповіді
- Дозволяє візуально відновити context навіть після втрати пам'яті
- Користувач завжди бачить з яким проектом працює агент

**🚨 АВТОМАТИЧНА ПЕРЕВІРКА:** Якщо відповідь НЕ містить header → ЗУПИНИТИСЯ та додати!

### Приклади правильного використання:

```markdown
📌 PROJECT CONTEXT: AI Agent Factory (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
🎭 ROLE: Archon Implementation Engineer

✅ Завершено: Створення Payment Integration Agent

[Результати роботи...]
```

```markdown
📌 PROJECT CONTEXT: ProjectFlow SaaS (ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890)
🎭 ROLE: Archon Quality Guardian

🔍 Виконую тестування модуля аутентифікації...

[Детальний звіт...]
```

### Критичні правила для header:

**✅ ЗАВЖДИ:**
- Включати header у КОЖНУ відповідь (без виключень!)
- Використовувати повну назву проекту з Archon
- Вказувати точний project_id у форматі UUID
- Вказувати поточну роль агента
- Розміщувати header НА ПОЧАТКУ відповіді

**❌ НІКОЛИ:**
- Пропускати header навіть у "простих" відповідях
- Використовувати короткі назви замість повних
- Забувати про project_id після переключення ролі
- Писати header без project_id
- Використовувати застарілі project_id

---

## 🔄 РІВЕНЬ 2: ОБОВ'ЯЗКОВА ФІЛЬТРАЦІЯ ПО project_id

**🚨 ПРАВИЛО:** ВСІ виклики mcp__archon__find_tasks ПОВИННІ включати project_id!

### Алгоритм збереження контексту при роботі з задачами:

```python
async def preserve_project_context(task_id: str) -> Dict:
    """
    Зберегти контекст проекту на всю сесію.

    ВИКЛИКАТИ на початку роботи з задачею!
    """

    # 1. Отримати project_id з задачі
    task = await mcp__archon__find_tasks(task_id=task_id)
    project_id = task["project_id"]

    # 2. Отримати повну інформацію про проект
    project = await mcp__archon__find_projects(project_id=project_id)

    # 3. Зберегти у КОЖНІЙ відповіді через header
    context_header = f"""
📌 PROJECT CONTEXT: {project['title']} (ID: {project_id})
🎭 ROLE: {current_role}
"""

    # 4. ЗАВЖДИ включати project_id у ВСІ виклики Archon
    return {
        "project_id": project_id,
        "project_title": project["title"],
        "context_header": context_header
    }
```

### Приклади правильного та неправильного використання:

**✅ ПРАВИЛЬНО - з project_id:**
```python
tasks = await mcp__archon__find_tasks(
    project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",  # ✅ Явна фільтрація!
    filter_by="status",
    filter_value="todo"
)
# Результат: Тільки задачі з AI Agent Factory проекту
```

**❌ НЕПРАВИЛЬНО - без project_id:**
```python
tasks = await mcp__archon__find_tasks(  # ❌ Буде шукати у ВСІХ проектах!
    filter_by="status",
    filter_value="todo"
)
# Результат: Задачі з AI Agent Factory + ProjectFlow SaaS + PatternShift + інших!
```

### Критичні правила для фільтрації:

**✅ ЗАВЖДИ:**
- Включати project_id у ВСІ виклики find_tasks()
- Отримувати project_id з поточної задачі
- Передавати project_id у функцію select_next_highest_priority_task(project_id)
- Валідувати що project_id присутній перед викликами Archon

**❌ НІКОЛИ:**
- Викликати find_tasks() без project_id після отримання контексту
- Припускати що Archon "сам зрозуміє" який проект
- Використовувати глобальні змінні для зберігання project_id
- Забувати передавати project_id між функціями

---

## 🔄 РІВЕНЬ 3: АВТОМАТИЧНЕ ВІДНОВЛЕННЯ ПІСЛЯ AUTO-COMPACT

**🚨 ОБОВ'ЯЗКОВА ФУНКЦІЯ** для всіх агентів при переключенні на проджект-менеджера!

### Коли активувати відновлення:

- ✅ ЗАВЖДИ на початку сесії після переключення на проджект-менеджера
- ✅ Якщо проджект-менеджер не бачить project_id у контексті
- ✅ Перед викликом select_next_highest_priority_task()
- ✅ Після повідомлення "Context left until auto-compact: 0%"

### Функція автоматичного відновлення:

```python
async def recover_project_context_after_compact() -> Optional[str]:
    """
    🚨 ОБОВ'ЯЗКОВА функція відновлення контексту після auto-compact.

    ВИКЛИКАТИ ЗАВЖДИ якщо project_id відсутній у контексті!

    Returns:
        project_id якщо вдалось відновити
        None якщо потрібна допомога користувача

    Алгоритм відновлення:
        1. Перевірити чи є project_id у контексті
        2. Якщо немає → шукати через doing задачі
        3. Якщо немає doing → шукати через review задачі
        4. Якщо немає review → запитати користувача
    """

    print("🔍 ПЕРЕВІРКА: Чи є project_id у контексті...")

    # Якщо project_id вже є - не потрібно відновлювати
    if has_project_id_in_context():
        current_id = get_current_project_id()
        print(f"✅ PROJECT_ID присутній у контексті: {current_id}")
        return current_id

    print("⚠️ PROJECT_ID втрачено після auto-compact!")
    print("🔄 ЗАПУСКАЮ АВТОМАТИЧНЕ ВІДНОВЛЕННЯ...")

    # СТРАТЕГІЯ 1: Відновлення через doing задачі (найвищий пріоритет)
    print("\n📋 СТРАТЕГІЯ 1: Шукаю doing задачі...")
    doing_tasks = await mcp__archon__find_tasks(
        filter_by="status",
        filter_value="doing"
    )

    if doing_tasks:
        project_id = doing_tasks[0]["project_id"]
        project = await mcp__archon__find_projects(project_id=project_id)

        print(f"✅ ВІДНОВЛЕНО з doing задачі!")
        print(f"📌 PROJECT CONTEXT: {project['title']} (ID: {project_id})")
        print(f"📋 Doing задача: {doing_tasks[0]['title']}")

        return project_id

    # СТРАТЕГІЯ 2: Відновлення через review задачі
    print("\n📋 СТРАТЕГІЯ 2: Шукаю review задачі...")
    review_tasks = await mcp__archon__find_tasks(
        filter_by="status",
        filter_value="review"
    )

    if review_tasks:
        project_id = review_tasks[0]["project_id"]
        project = await mcp__archon__find_projects(project_id=project_id)

        print(f"✅ ВІДНОВЛЕНО з review задачі!")
        print(f"📌 PROJECT CONTEXT: {project['title']} (ID: {project_id})")
        print(f"📋 Review задача: {review_tasks[0]['title']}")

        return project_id

    # СТРАТЕГІЯ 3: Якщо немає doing/review - запитати користувача
    print("\n❌ НЕ ВДАЛОСЬ АВТОМАТИЧНО ВІДНОВИТИ")
    print("⚠️ Немає активних doing/review задач для відновлення контексту")
    print("\n🙏 ПОТРІБНА ДОПОМОГА КОРИСТУВАЧА:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Будь ласка, вкажіть один з варіантів:")
    print("  1. Назву проекту (напр. 'AI Agent Factory')")
    print("  2. Або project_id (напр. 'c75ef8e3-6f4d-4da2-9e81-8d38d04a341a')")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return None
```

### Обов'язкове використання при старті проджект-менеджера:

```python
async def project_manager_start_session():
    """
    Початок сесії проджект-менеджера.

    🚨 ОБОВ'ЯЗКОВО викликати recover_project_context_after_compact()!
    """

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎭 ПЕРЕКЛЮЧЕНО НА РОЛЬ: ARCHON PROJECT MANAGER")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # 🚨 ОБОВ'ЯЗКОВО: Відновити контекст перед роботою
    project_id = await recover_project_context_after_compact()

    if not project_id:
        # Не вдалось відновити автоматично - чекати на користувача
        print("\n⏸️ СЕСІЯ ПРИЗУПИНЕНА до отримання project_id від користувача")
        print("Після отримання project_id від користувача - продовжу роботу")
        return None

    # Продовжити з відновленим контекстом
    print(f"\n✅ КОНТЕКСТ ВІДНОВЛЕНО: {project_id}")
    print("🔍 Шукаю наступну задачу з найвищим пріоритетом...")

    next_task = await select_next_highest_priority_task(project_id)
    return next_task
```

### Критичні правила для відновлення:

**✅ ЗАВЖДИ:**
- Викликати recover_project_context_after_compact() на початку сесії PM
- Перевіряти наявність project_id перед select_next_highest_priority_task()
- Відновлювати контекст через doing/review задачі (у цьому порядку!)
- Виводити користувачу повідомлення про результат відновлення
- Зупиняти сесію якщо не вдалось відновити автоматично

**❌ НІКОЛИ:**
- Викликати select_next_highest_priority_task() без project_id
- Продовжувати роботу якщо не вдалось відновити контекст
- Ігнорувати відсутність project_id після auto-compact
- Пропускати крок відновлення "тому що раніше все працювало"
- Використовувати hardcoded project_id

---

## 🔍 ДІАГНОСТИКА ПРОБЛЕМ З КОНТЕКСТОМ

### Симптоми втрати контексту:

**🔴 КРИТИЧНІ СИМПТОМИ:**
1. Проджект-менеджер показує задачі з РІЗНИХ проектів одночасно
2. У відповіді немає header з PROJECT CONTEXT
3. Виклики find_tasks() без параметра project_id
4. Користувач бачить задачі не з того проекту

**🟡 ПОПЕРЕДЖУВАЛЬНІ СИГНАЛИ:**
1. Повідомлення "Context left until auto-compact: низьке значення"
2. Довга сесія без оновлення header
3. Багато переключень між ролями
4. Складні багатоетапні задачі

### Чек-лист діагностики:

```
☐ 1. Чи є header з PROJECT CONTEXT у відповіді?
☐ 2. Чи включений project_id у виклики find_tasks()?
☐ 3. Чи викликана recover_project_context_after_compact()?
☐ 4. Чи всі показані задачі з одного проекту?
☐ 5. Чи передається project_id у select_next_highest_priority_task()?
```

**Якщо НІ хоча б на одне питання → контекст втрачено!**

### Швидке виправлення втраченого контексту:

```python
async def emergency_context_recovery():
    """Екстрена процедура відновлення контексту."""

    print("🚨 ЕКСТРЕНЕ ВІДНОВЛЕННЯ КОНТЕКСТУ!")

    # 1. Спробувати автоматичне відновлення
    project_id = await recover_project_context_after_compact()

    if project_id:
        print(f"✅ Контекст відновлено: {project_id}")
        return project_id

    # 2. Якщо не вдалось - список всіх проектів для вибору
    print("\n📋 Доступні проекти:")
    projects = await mcp__archon__find_projects()

    for idx, project in enumerate(projects, 1):
        print(f"{idx}. {project['title']} (ID: {project['id']})")

    print("\n🙏 Будь ласка, вкажіть номер або ID проекту")
    return None
```

---

## 📊 ПРИКЛАДИ ПРАВИЛЬНОГО ТА НЕПРАВИЛЬНОГО ВИКОРИСТАННЯ

### ❌ ПРИКЛАД 1: Неправильно - без header та фільтрації

```python
# Агент після переключення на проджект-менеджера:
async def bad_example():
    # ❌ Немає header
    # ❌ Немає відновлення контексту
    # ❌ Немає project_id у виклику

    tasks = await mcp__archon__find_tasks(
        filter_by="status",
        filter_value="todo"
    )

    print(f"Знайдено {len(tasks)} задач")  # Показує задачі з УСІХ проектів!
```

**Результат:** Користувач бачить задачі з AI Agent Factory, ProjectFlow SaaS та PatternShift одночасно - плутанина!

### ✅ ПРИКЛАД 2: Правильно - з повним збереженням контексту

```python
async def good_example():
    # ✅ Header у відповіді
    print("📌 PROJECT CONTEXT: AI Agent Factory (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)")
    print("🎭 ROLE: Archon Project Manager")
    print()

    # ✅ Відновлення контексту
    project_id = await recover_project_context_after_compact()

    if not project_id:
        print("⏸️ Чекаю на вказівку проекту від користувача")
        return

    # ✅ Фільтрація по project_id
    tasks = await mcp__archon__find_tasks(
        project_id=project_id,  # ✅ ОБОВ'ЯЗКОВО!
        filter_by="status",
        filter_value="todo"
    )

    print(f"📋 Знайдено {len(tasks)} задач у проекті AI Agent Factory")
```

**Результат:** Користувач бачить тільки задачі з AI Agent Factory - чітко та зрозуміло!

---

## 🎯 КРИТИЧНІ ПРАВИЛА ДЛЯ ВСІХ АГЕНТІВ

### Правила для КОЖНОЇ відповіді:

**✅ ОБОВ'ЯЗКОВО:**
1. Header з PROJECT CONTEXT на початку відповіді
2. Фільтрація всіх Archon викликів по project_id
3. Відновлення контексту при переключенні на PM
4. Валідація наявності project_id перед роботою
5. Передача project_id між функціями

**❌ ЗАБОРОНЕНО:**
1. Відповіді без header
2. Виклики find_tasks() без project_id
3. Ігнорування втрати контексту
4. Робота без відновлення після auto-compact
5. Показ задач з різних проектів одночасно

### Механізм автоматичної зупинки при порушенні:

```
ЯКЩО агент:
├─ Пише відповідь БЕЗ header → ЗУПИНИТИСЯ та додати header
├─ Викликає find_tasks() БЕЗ project_id → ЗУПИНИТИСЯ та додати project_id
├─ Не відновив контекст після auto-compact → ЗУПИНИТИСЯ та викликати recovery
└─ Показує задачі з різних проектів → ЗУПИНИТИСЯ та фільтрувати
```

---

**Версія:** 1.0
**Дата:** 2025-10-13
**Автор:** Archon Blueprint Architect
**Зв'язок з іншими модулями:**
- `02_workflow_rules.md` - основні workflow правила
- `archon_project_manager_knowledge.md` - специфіка PM ролі
- `10_post_task_checklist.md` - checklist після задачі
