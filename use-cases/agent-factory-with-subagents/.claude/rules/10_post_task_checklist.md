# 10. Post-Task Checklist - Обов'язковий останній пункт TodoWrite

## 🚨 КРИТИЧНО ВАЖЛИВО: ОБОВ'ЯЗКОВИЙ ОСТАННІЙ ПУНКТ

**КОЖНА ЗАДАЧА ПОВИННА ЗАВЕРШУВАТИСЯ ОСТАННІМ ПУНКТОМ TodoWrite:**

```
N. Виконати Post-Task Checklist (.claude/rules/10_post_task_checklist.md)
```

**ЦЕЙ ПУНКТ ОБОВ'ЯЗКОВИЙ ДЛЯ ВСІХ ЗАДАЧ БЕЗ ВИКЛЮЧЕНЬ!**

---

## 📋 POST-TASK CHECKLIST - Що робити після завершення задачі

**Коли ти досягаєш останнього пункту TodoWrite, виконуй ЦЕЙ чек-лист:**

### ✅ КРОК 0: Оновлення статусу задачі в Archon (ОБОВ'ЯЗКОВО!)

**🚨 ЦЕ ПЕРШИЙ КРОК - ВИКОНУЄТЬСЯ ПЕРЕД УСІМА ІНШИМИ!**

**ПРОБЛЕМА:** Агенти забувають оновлювати статус задачі після завершення роботи, через що задачі залишаються в статусі "doing" навіть після виконання.

**РІШЕННЯ:** Обов'язкове оновлення статусу задачі В КІНЦІ роботи.

#### 📊 ТАБЛИЦЯ ВИБОРУ СТАТУСУ:

| Ситуація | Статус | Коли використовувати |
|----------|--------|---------------------|
| ✅ **Виконано БЕЗ проблем** | `done` | Всі вимоги виконані, тести пройдені, код готовий |
| 🔍 **Потребує перевірки** | `review` | Робота виконана, але потрібен code review експерта |
| ⚠️ **Потрібна ескалація** | `doing` + створити задачу | Столкнувся з проблемою вне компетенції |
| 🚫 **Заблокована** | `doing` + опис блокера | Не може бути завершена через зовнішні фактори |

#### ✅ ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ:

```python
# КРОК 0.1: Перевірити поточний статус задачі
task = await mcp__archon__find_tasks(task_id=current_task_id)
current_status = task['status']
print(f"[КРОК 0/5] Поточний статус задачі: {current_status}")

# КРОК 0.2: Вибрати новий статус на основі результату
if work_completed_successfully and no_issues:
    new_status = "done"
    print("✅ Задача виконана БЕЗ проблем → статус 'done'")

elif work_completed_but_needs_expert_review:
    new_status = "review"
    print("🔍 Задача виконана, потребує перевірки → статус 'review'")

elif encountered_issue_outside_expertise:
    new_status = "doing"  # Залишається в doing
    print("⚠️ Потрібна ескалація → залишаю 'doing' + створюю задачу експерту")
    # Створити задачу для експерта
    await mcp__archon__manage_task(
        action="create",
        assignee="Відповідний_Експерт",
        title=f"⚠️ ЕСКАЛАЦІЯ: {опис_проблеми}",
        description=f"Деталі: {деталі_проблеми}"
    )

elif task_blocked_by_external_factor:
    new_status = "doing"  # Залишається в doing
    print("🚫 Задача заблокована → залишаю 'doing' + опис блокера")
    # Оновити description з блокером
    updated_description = f"{original_description}\n\n🚫 БЛОКЕР: {опис_блокера}\nОчікує: {що_потрібно}"

# КРОК 0.3: ОБОВ'ЯЗКОВО оновити статус в Archon
await mcp__archon__manage_task(
    action="update",
    task_id=current_task_id,
    status=new_status
)
print(f"✅ Статус задачі оновлено: '{current_status}' → '{new_status}'")
```

#### ❌ ПРИКЛАДИ НЕПРАВИЛЬНОГО:

**ПОМИЛКА #1: Забув оновити статус на "done"**
```python
# ❌ ЗАБОРОНЕНО - завершив роботу, але не змінив статус
print("✅ Код написано, тести пройдені, коміт зроблено")
print("Тепер виконаю Post-Task Checklist...")
# СТОП! Задача залишиться в статусі "doing"!
```

**ПОМИЛКА #2: Не перевірив результат перед вибором статусу**
```python
# ❌ ЗАБОРОНЕНО - автоматично ставить "done" без перевірки
await mcp__archon__manage_task("update", task_id=id, status="done")
# А якщо є проблеми? Якщо потрібна перевірка?
```

**ПОМИЛКА #3: Проігнорував проблему замість ескалації**
```python
# ❌ ЗАБОРОНЕНО - знайшов TypeScript помилки (поза компетенцією), але поставив "done"
print("Є TypeScript помилки, але це не критично...")
await mcp__archon__manage_task("update", task_id=id, status="done")
# СТОП! Треба створити задачу для TypeScript експерта!
```

#### ✅ ПРИКЛАД ПРАВИЛЬНОГО:

```python
# ✅ ПРАВИЛЬНО - перевірив результат, вибрав правильний статус
task_id = "e7cb2e05-21fe-450e-af2c-25ac1b6b8349"

# Перевірка результату
tests_passed = True
no_errors = True
no_external_issues = True

# Вибір статусу
if tests_passed and no_errors and no_external_issues:
    new_status = "done"
    print("✅ Всі критерії виконані → статус 'done'")
else:
    new_status = "review"
    print("🔍 Потребує перевірки → статус 'review'")

# Оновлення в Archon
await mcp__archon__manage_task(
    action="update",
    task_id=task_id,
    status=new_status
)
print(f"✅ Статус задачі оновлено на '{new_status}'")

# ТІЛЬКИ ПІСЛЯ цього продовжити до КРОК 1
```

#### 🔗 ЗВ'ЯЗОК З ЧЕРВОНИМИ ЛІНІЯМИ:

Цей розділ реалізує кінцевий етап **ЧЕРВОНОЇ ЛІНІЇ #2** з системи захисту:

**ЧЕРВОНА ЛІНІЯ #2:** "Git коміт без статусу 'done'"
- **ДО КОМІТУ:** Статус повинен бути оновлений на "doing" (це ПЕРШИЙ пункт TodoWrite)
- **ПІСЛЯ КОМІТУ:** Статус повинен бути оновлений на "done" або "review" (ЦЕЙ КРОК!)

**Детальна інформація про ЧЕРВОНІ ЛІНІЇ:**
→ `.claude/rules/02_workflow_rules.md` → розділ "🔴 ЧЕРВОНІ ЛІНІЇ: Оновлення статусів задач"

#### 🚨 ДІЯ ПРИ ПОРУШЕННІ:

**ЯКЩО агент забув оновити статус задачі:**

```
1. НЕГАЙНО ЗУПИНИТИСЯ
   ↓
2. Повернутися до КРОК 0
   ↓
3. Вибрати правильний статус (done/review/doing)
   ↓
4. Оновити статус в Archon
   ↓
5. ТІЛЬКИ ПІСЛЯ - продовжити до КРОК 1
```

---

### ✅ КРОК 1: Освіження пам'яті (Memory Refresh)

**Прочитай `.claude/rules/refresh_protocol.md` для повного алгоритму**

**Коротко:**
- Якщо виконав 5+ мікрозадач → освіжи пам'ять правил
- Перечитай ключові розділи відповідно до типу задачі
- Переконайся що не забув жодних критичних правил

**Файл для читання:** `.claude/rules/refresh_protocol.md`

---

### ✅ КРОК 2: Перевірка білда та Git операцій (ОБОВ'ЯЗКОВО!)

**🚨 КРИТИЧНЕ ПРАВИЛО: BUILD → COMMIT → PUSH**

**ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ:**

1. **Запустити білд проекту:**
   - Python: `python -m pytest` або `python -m unittest discover`
   - Node.js: `npm run build` або `npm test`
   - Go: `go build ./... && go test ./...`

2. **Перевірити результат білда:**
   - ✅ Білд успішний → продовжити до git commit
   - ❌ Білд провалився → ЗУПИНИТИСЬ, виправити помилки, повторити білд

3. **Git коміт (тільки після успішного білда!):**
   - `git add .`
   - `git commit -m "feat: опис змін"`

4. **🚨 Git push НЕГАЙНО після коміту (для ВСІХ проектів з git!):**
   - `git push origin main`

**Для Production проектів:**
- Прочитай `.claude/rules/05_git_integration.md` → розділ "ОБОВ'ЯЗКОВИЙ PUSH ДЛЯ PRODUCTION ПРОЕКТІВ"
- Push КРИТИЧНО ВАЖЛИВИЙ для production проектів!

**Файл для читання:** `.claude/rules/05_git_integration.md` (рядки 63-227)

---

### ✅ КРОК 3: SELF-CHECK АБО ПЕРЕКЛЮЧЕННЯ НА PROJECT MANAGER

**🚨 ЦЕ НАЙВАЖЛИВІШИЙ КРОК - НЕ ПРОПУСКАЙ!**

**НОВИЙ ОПТИМІЗОВАНИЙ WORKFLOW:**

```
КРОК 3A: ПЕРЕВІРКА ВЛАСНИХ ЗАДАЧ (СПОЧАТКУ!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Визначити поточну роль агента:
   current_role = "Implementation Engineer"  # або інша роль

2️⃣ Перевірити чи є doing задачі для МОЄЇ ролі:
   my_doing = await mcp__archon__find_tasks(
       project_id=project_id,
       filter_by="status",
       filter_value="doing"
   )
   # Фільтруємо: тільки де assignee == current_role

3️⃣ Перевірити чи є review задачі для МОЄЇ ролі:
   my_review = await mcp__archon__find_tasks(
       project_id=project_id,
       filter_by="status",
       filter_value="review"
   )
   # Фільтруємо: тільки де assignee == current_role

4️⃣ ЯКЩО є задачі для мене (doing або review):
   ✅ Вибрати задачу з найвищим task_order
   ✅ Показати користувачу: "Знайдено N задач для [роль]"
   ✅ Почати виконання БЕЗ переключення ролі
   ✅ RETURN - НЕ йти до КРОКУ 3B!

КРОК 3B: ПЕРЕКЛЮЧЕННЯ НА PM (тільки якщо немає своїх задач)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ Якщо НЕ знайдено задач для моєї ролі:
   📭 Показати: "Немає задач для [роль]"
   🔄 Переходимо до переключення на Project Manager

6️⃣ Знайти промпт Project Manager:
   Glob("**/*project*manager*knowledge*.md")

7️⃣ Прочитати промпт роли

8️⃣ ПЕРЕКЛЮЧИТИСЯ В РОЛЬ PROJECT MANAGER
   (показати користувачу шаблон переключення)

9️⃣ Створити мікрозадачі для PM роботи (TodoWrite TOOL):
   - Перевірити doing/review задачі в Archon (серед УСІХ ролей)
   - Перевірити todo задачі в Archon
   - Вибрати задачу з найвищим пріоритетом серед УСІХ ролей
   - Переключитися в роль для цієї задачі

🔟 Виконати мікрозадачі PM:
   - Проаналізувати ВСІ задачі проекту (не тільки для однієї ролі!)
   - Вибрати задачу з найвищим пріоритетом серед УСІХ ролей
   - Переключитися в відповідну роль
   - Почати виконання нової задачі
```

**💡 КЛЮЧОВА ІДЕЯ:**
- Агент спочатку перевіряє СВОЇ doing/review
- Тільки якщо у нього немає роботи → переключається на PM
- PM шукає серед УСІХ ролей (це його робота)

**Детальні правила переключення:**
- **Файл:** `.claude/rules/02_workflow_rules.md` (рядки 69-406)
- **Розділи:**
  - "Правило пріоритизації через проджект-менеджера" (рядки 69-172)
  - "Автоматичне переключення на PROJECT MANAGER" (рядки 354-406)

---

### ✅ КРОК 4: Збереження контексту проекту

**ОБОВ'ЯЗКОВО включай у КОЖНУ відповідь після переключення на PM:**

```markdown
📌 PROJECT CONTEXT: [Project Title] (ID: [project_id])
🎭 ROLE: Archon Project Manager
```

**Детальні правила:** `.claude/rules/02_workflow_rules.md` (рядки 199-335)

---

## 🎯 АЛГОРИТМ ВИКОНАННЯ ОСТАННЬОГО ПУНКТУ TodoWrite

**Коли досягаєш пункту "Виконати Post-Task Checklist":**

```python
# ПСЕВДОКОД для розуміння послідовності

async def execute_post_task_checklist():
    """Виконати Post-Task Checklist після завершення задачі."""

    # КРОК 1: Освіження пам'яті
    print("[КРОК 1/4] Освіження пам'яті...")
    if microtasks_count >= 5:
        await read_file(".claude/rules/refresh_protocol.md")
        await refresh_relevant_rules()

    # КРОК 2: Git операції для production
    print("[КРОК 2/4] Перевірка Git операцій...")
    if project_deployment_status == "production":
        await read_file(".claude/rules/05_git_integration.md")
        await check_and_push_if_needed()

    # КРОК 3A: SELF-CHECK - ПЕРЕВІРКА ВЛАСНИХ ЗАДАЧ (НОВИЙ!)
    print("[КРОК 3A/5] 🔍 Перевіряю власні doing/review задачі...")

    current_role = get_current_agent_role()  # e.g., "Implementation Engineer"
    project_id = get_project_id_from_context()

    # 3A.1 Шукаємо doing задачі для ПОТОЧНОЇ ролі
    my_doing_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="doing"
    )
    # Фільтруємо тільки свої задачі
    my_doing = [t for t in my_doing_tasks if t.get("assignee") == current_role]

    # 3A.2 Шукаємо review задачі для ПОТОЧНОЇ ролі
    my_review_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="review"
    )
    # Фільтруємо тільки свої задачі
    my_review = [t for t in my_review_tasks if t.get("assignee") == current_role]

    # 3A.3 Якщо є СВОЇ задачі - продовжуємо БЕЗ переключення
    my_tasks = my_doing + my_review
    if my_tasks:
        next_task = max(my_tasks, key=lambda t: t.get("task_order", 0))

        print(f"✅ Знайдено {len(my_tasks)} задач для {current_role}")
        print(f"📋 Наступна задача: {next_task['title']}")
        print(f"🎯 Status: {next_task['status']}")
        print(f"⚡ Priority (task_order): {next_task.get('task_order', 0)}")
        print(f"\n🔄 Продовжую роботу БЕЗ переключення ролі")

        # Оновлюємо статус на doing якщо це review
        if next_task['status'] == 'review':
            await mcp__archon__manage_task(
                "update",
                task_id=next_task["id"],
                status="doing"
            )

        # Починаємо виконання ОДРАЗУ
        await start_task_execution(next_task)
        return  # КРИТИЧНО: не переключаємось на PM

    # КРОК 3B: ПЕРЕКЛЮЧЕННЯ НА PM (тільки якщо немає своїх задач)
    print(f"📭 Немає задач для {current_role}")
    print("[КРОК 3B/5] 🚨 ПЕРЕКЛЮЧЕННЯ НА PROJECT MANAGER...")

    # 3B.1 Знайти промпт PM
    pm_knowledge = await Glob("**/*project*manager*knowledge*.md")
    pm_prompt = await Read(pm_knowledge[0])

    # 3B.2 ПОКАЗАТИ ПЕРЕКЛЮЧЕННЯ КОРИСТУВАЧУ
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ ARCHON PROJECT MANAGER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя експертиза:
• Управління lifecycle проектів
• Координація мультиагентної команди
• Планування ресурсів та часових рамок
• Risk management і mitigation стратегії

✅ Готов виконати задачу в ролі експерта Project Manager

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

    # 3B.3 Створити мікрозадачі для PM роботи (TodoWrite TOOL!)
    await TodoWrite([
        {"content": "Перевірити doing/review задачі проекту (УСІХ ролей)", "status": "pending"},
        {"content": "Перевірити todo задачі проекту", "status": "pending"},
        {"content": "Вибрати задачу з найвищим пріоритетом серед УСІХ ролей", "status": "pending"},
        {"content": "Переключитися в роль для обраної задачі", "status": "pending"},
        {"content": "Почати виконання нової задачі", "status": "pending"}
    ])

    # 3B.4 Виконати PM мікрозадачі (пошук серед УСІХ ролей)
    # Перевірити doing/review (ПРІОРИТЕТ 1-2) серед УСІХ assignees
    doing_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="doing"
    )
    review_tasks = await mcp__archon__find_tasks(
        project_id=project_id,
        filter_by="status",
        filter_value="review"
    )

    # Вибрати найвищий пріоритет серед УСІХ задач (всіх ролей)
    urgent_tasks = doing_tasks + review_tasks
    if urgent_tasks:
        next_task = max(urgent_tasks, key=lambda t: t.get("task_order", 0))
    else:
        # Якщо немає doing/review - взяти todo
        todo_tasks = await mcp__archon__find_tasks(
            project_id=project_id,
            filter_by="status",
            filter_value="todo"
        )
        if todo_tasks:
            next_task = max(todo_tasks, key=lambda t: t.get("task_order", 0))
        else:
            print("✅ Всі задачі виконані!")
            return

    # КРОК 4: Збереження контексту (виконується в PM ролі)
    print("[КРОК 4/5] Збереження контексту проекту...")
    print(f"📌 PROJECT CONTEXT: {project_title} (ID: {project_id})")
    print(f"🎭 ROLE: Archon Project Manager")
    print(f"\n📋 Наступна задача: {next_task['title']}")
    print(f"🎯 Assignee: {next_task['assignee']}")

    # КРОК 5: Переключитися в роль assignee та почати виконання
    print("[КРОК 5/5] Переключення в роль для виконання задачі...")
    await switch_to_role(next_task['assignee'])
    await start_task_execution(next_task)
```

---

## ❌ ЗАБОРОНЕНІ ПАТТЕРНИ

**НІКОЛИ НЕ РОБИТИ:**

```python
# ❌ НЕПРАВИЛЬНО - НЕ перевірити власні задачі перед PM
print("✅ Задача завершена!")
# Одразу переключаюсь на PM...
await switch_to_pm()
# СТОП! Спочатку треба перевірити чи є СВОЇ doing/review!

# ❌ НЕПРАВИЛЬНО - пропустити self-check (КРОК 3A)
# Агент одразу йде в PM, навіть якщо у нього є свої задачі
await execute_post_task_checklist()
# ... але в execute_post_task_checklist() пропускає КРОК 3A
# СТОП! КРОК 3A ОБОВ'ЯЗКОВИЙ!

# ❌ НЕПРАВИЛЬНО - закінчити без Post-Task Checklist
await mcp__archon__manage_task("update", task_id=id, status="done")
return "Задача виконана!"
# СТОП! Після done ЗАВЖДИ виконати Post-Task Checklist!

# ❌ НЕПРАВИЛЬНО - PM шукає тільки для однієї ролі
# У КРОЦІ 3B PM шукає тільки для Implementation Engineer
pm_tasks = [t for t in all_tasks if t["assignee"] == "Implementation Engineer"]
# СТОП! PM повинен шукати серед УСІХ ролей!
```

**✅ ПРАВИЛЬНО:**

```python
# ✅ ПРАВИЛЬНО - повний workflow з self-check
await mcp__archon__manage_task("update", task_id=id, status="done")

# ОБОВ'ЯЗКОВО виконати Post-Task Checklist
await execute_post_task_checklist()

# Де execute_post_task_checklist() виконує:
# 1. КРОК 1: Освіження пам'яті
# 2. КРОК 2: Git операції
# 3. КРОК 3A: Self-check (перевірка СВОЇХ doing/review)
#    → Якщо є свої задачі → продовжити БЕЗ PM
# 4. КРОК 3B: Переключення на PM (якщо немає своїх задач)
#    → PM шукає серед УСІХ ролей
# 5. КРОК 4: Збереження контексту
# 6. КРОК 5: Виконання наступної задачі
```

---

## 🔄 ТАБЛИЦЯ ПРІОРИТЕТІВ ЗАДАЧ (для PM)

| Пріоритет | Статус | Значення | Чому важливо |
|-----------|--------|----------|--------------|
| **1 (НАЙВИЩИЙ)** | `doing` | Незавершена робота з минулої сесії | Може блокувати інших |
| **2** | `review` | Потребує перевірки експерта | Може блокувати наступні задачі |
| **3** | `todo` | Нова задача з найвищим task_order | Береться тільки якщо немає doing/review |

**PM ЗАВЖДИ шукає серед УСІХ ролей, не тільки для однієї!**

---

## 📊 ШАБЛОН ПОВІДОМЛЕННЯ ПІСЛЯ ПЕРЕКЛЮЧЕННЯ НА PM

**ОБОВ'ЯЗКОВИЙ ФОРМАТ після переключення на PM:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Задача завершена: [Назва задачі]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 PROJECT CONTEXT: [Project Name] (ID: [project_id])
🎭 ROLE: Archon Project Manager

🔄 Аналізую стан проекту для вибору наступної задачі...

[Результати аналізу doing/review/todo задач]

📋 Наступна задача: "[Точна назва з Archon]"
   (пріоритет: task_order [число], assignee: [роль])

🎭 Переключаюся в роль [assignee] для виконання...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 КРИТИЧНІ ПРАВИЛА ДЛЯ ЗАПАМ'ЯТОВУВАННЯ

**ЦІ ПРАВИЛА НІКОЛИ НЕ ПОРУШУЮТЬСЯ:**

1. **КОЖНА ЗАДАЧА ЗАВЕРШУЄТЬСЯ ОСТАННІМ ПУНКТОМ:** "Виконати Post-Task Checklist"
2. **Post-Task Checklist ЗАВЖДИ включає КРОК 3A (self-check)** перед PM
3. **КРОК 3A: Агент СПОЧАТКУ перевіряє СВОЇ doing/review задачі**
4. **КРОК 3B: Тільки якщо немає своїх задач → переключення на PM**
5. **PM шукає задачі серед УСІХ ролей, не тільки для однієї**
6. **Пріоритет: doing > review > todo (за task_order)**
7. **Після вибору задачі PM переключається в роль assignee**
8. **Новий цикл починається з переключення в роль → TodoWrite → виконання**

---

## 📚 ФАЙЛИ ДЛЯ ОБОВ'ЯЗКОВОГО ЧИТАННЯ

**При виконанні Post-Task Checklist читай:**

1. **`.claude/rules/refresh_protocol.md`**
   - Коли: Якщо виконав 5+ мікрозадач
   - Що: Алгоритм освіження пам'яті правил

2. **`.claude/rules/05_git_integration.md` (рядки 63-221)**
   - Коли: Завжди перед завершенням
   - Що: Production push правила, git workflow

3. **`.claude/rules/02_workflow_rules.md` (рядки 69-406)**
   - Коли: ЗАВЖДИ перед переключенням на PM
   - Що: Правила пріоритизації, переключення ролей, збереження контексту

4. **Промпт Project Manager: `agents/archon_project_manager/knowledge/*.md`**
   - Коли: При переключенні на PM
   - Що: Системний промпт, експертиза, обов'язки PM

---

## 🚀 ШВИДКИЙ СТАРТ - Останній пункт TodoWrite

**ШАБЛОН для копіювання в TodoWrite:**

```json
{
  "content": "Виконати Post-Task Checklist (.claude/rules/10_post_task_checklist.md) [TASK_ID: {task_id}]",
  "status": "pending",
  "activeForm": "Виконую Post-Task Checklist"
}
```

**🚨 КРИТИЧНО ВАЖЛИВО:**
- **ЗАВЖДИ вказуй TASK_ID** в останньому пункті TodoWrite!
- Формат: `[TASK_ID: task-uuid-here]`
- Це дозволяє агенту пам'ятати яку задачу треба оновити в Archon

**Приклад:**
```
N. Виконати Post-Task Checklist (.claude/rules/10_post_task_checklist.md) [TASK_ID: 3a7f8b9c-1d2e-3f4g-5h6i-7j8k9l0m1n2o]
```

**Цей пункт ОБОВ'ЯЗКОВИЙ для КОЖНОЇ задачі без виключень!**

---

## 🎓 НАВЧАЛЬНІ СЦЕНАРІЇ

### Сценарій 1: Агент БЕЗ власних задач (переключення на PM)

```
1. Отримав задачу "Створити Payment Agent"
2. Переключився в роль Implementation Engineer
3. Створив TodoWrite з мікрозадачами:
   - Проаналізувати вимоги
   - Створити структуру файлів
   - Реалізувати функціонал
   - Написати тести
   - Рефлексія та покращення
   - Git коміт
   - Оновити статус в Archon
   - ✅ Виконати Post-Task Checklist <-- ОСТАННІЙ ПУНКТ!

4. Виконав всі мікрозадачі

5. Досяг останнього пункту "Виконати Post-Task Checklist":
   ✅ Крок 1: Освіжив пам'ять (виконав 8 мікрозадач)
   ✅ Крок 2: Перевірив git (проект не production, пропустив push)
   ✅ Крок 3A: SELF-CHECK (НОВИЙ!)
      - Перевірив doing для Implementation Engineer: 0 задач
      - Перевірив review для Implementation Engineer: 0 задач
      - 📭 Немає задач для моєї ролі
      - → Переходжу до КРОКУ 3B (PM)
   ✅ Крок 3B: ПЕРЕКЛЮЧИВСЯ НА PM
      - Знайшов промпт PM
      - Показав переключення користувачу
      - Створив мікрозадачі для PM роботи (TodoWrite!)
      - Проаналізував doing серед УСІХ ролей (0 задач)
      - Проаналізував review серед УСІХ ролей (1 задача!)
      - Вибрав review задачу для Quality Guardian
      - Переключився в роль Quality Guardian
   ✅ Крок 4: Зберіг контекст проекту
   ✅ Крок 5: Виконання наступної задачі

6. Почав виконання review задачі в ролі Quality Guardian
```

### Сценарій 1A: Агент З власними задачами (БЕЗ PM)

```
1. Отримав задачу "Створити API endpoint /payments"
2. Переключився в роль Implementation Engineer
3. Виконав задачу, створив коміт
4. Досяг останнього пункту "Виконати Post-Task Checklist":
   ✅ Крок 1: Освіжив пам'ять
   ✅ Крок 2: Перевірив git
   ✅ Крок 3A: SELF-CHECK
      - Перевірив doing для Implementation Engineer: 2 задачі!
        * "Додати валідацію платежів" (task_order: 90)
        * "Написати тести для /payments" (task_order: 85)
      - ✅ Знайдено 2 задачі для Implementation Engineer
      - 📋 Наступна задача: "Додати валідацію платежів" (пріоритет: 90)
      - 🔄 Продовжую роботу БЕЗ переключення ролі
      - ⏭️ КРОК 3B ПРОПУЩЕНО (не треба PM)

5. ОДРАЗУ почав виконання "Додати валідацію платежів"
   (БЕЗ переключення на PM - економія часу та токенів!)
```

### Сценарій 2: Production проект + відсутність власних задач

```
1. Завершив задачу "Виправити баг авторизації" (production проект)
2. Оновив статус в Archon:
   await mcp__archon__manage_task("update", task_id=id, status="done")
   ✅ Задача позначена як done

3. Останній пункт TodoWrite: "Виконати Post-Task Checklist"

4. Виконую Post-Task Checklist:
   ✅ Крок 1: Освіжив пам'ять
      - Прочитав останні 10 commits
      - Зрозумів контекст проекту

   ✅ Крок 2: PRODUCTION ПРОЕКТ!
      - Прочитав .claude/rules/05_git_integration.md
      - Перевірив непушнуті коміти: 1 коміт
      - 🚨 ОБОВ'ЯЗКОВО виконав: git push origin main
      - ✅ Код синхронізовано з production!

   ✅ Крок 3A: SELF-CHECK
      - Поточна роль: Implementation Engineer
      - Перевірив doing для Implementation Engineer: 0 задач
      - Перевірив review для Implementation Engineer: 0 задач
      - 📭 Немає задач для Implementation Engineer
      - ⏭️ Переходжу до КРОКУ 3B

   ✅ Крок 3B: ПЕРЕКЛЮЧЕННЯ НА PM (оскільки немає своїх задач)
      - Знайшов промпт PM
      - Переключився на роль Project Manager
      - Створив мікрозадачі для PM workflow

   ✅ Крок 4: Зберіг контекст
      - Project ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a

5. PM почав роботу:
   - Перевірив doing серед УСІХ ролей: 1 задача
   - Перевірив review серед УСІХ ролей: 0 задач
   - Знайшов задачу: "Додати unit тести для API" (assignee: Quality Guardian)
   - Переключився на роль Quality Guardian
   - Почав виконання...
```

---

**ВЕРСІЯ:** 1.0
**ДАТА СТВОРЕННЯ:** 2025-10-10
**АВТОР:** Archon Project Manager

**🚨 ЦЕ КРИТИЧНО ВАЖЛИВИЙ ДОКУМЕНТ - ЗАВЖДИ ВИКОНУЙ POST-TASK CHECKLIST!**
