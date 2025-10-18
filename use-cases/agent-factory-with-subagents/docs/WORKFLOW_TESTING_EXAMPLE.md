# Приклад тестування нового Workflow з 3-рівневою системою захисту

**Дата:** 2025-10-18
**Версія:** 1.0
**Мета:** Демонстрація роботи системи захисту статусів задач

---

## 📋 Сценарій тестування

### Задача для тесту
- **Task ID:** `test-12345678-1234-1234-1234-123456789abc`
- **Title:** "Додати валідацію email в формі реєстрації"
- **Assignee:** Implementation Engineer
- **Початковий статус:** `todo`

---

## ✅ ПРАВИЛЬНИЙ WORKFLOW (як ТРЕБА)

### Крок 1: Отримання задачі з Archon

```python
# Агент отримує задачу
task = await mcp__archon__find_tasks(
    task_id="test-12345678-1234-1234-1234-123456789abc"
)

print(f"Задача: {task['title']}")
print(f"Поточний статус: {task['status']}")  # → "todo"
```

### Крок 2: Переключення в роль

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ IMPLEMENTATION ENGINEER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя експертиза:
• Розробка функціональності на Python, TypeScript, Go
• Реалізація API endpoints та бізнес-логіки
• Інтеграція з базами даних та зовнішніми сервісами
• Оптимізація коду та рефакторинг

✅ Готов виконати задачу в ролі експерта Implementation Engineer
```

### Крок 3: Створення TodoWrite з ОБОВ'ЯЗКОВИМИ пунктами

```python
# ✅ ПРАВИЛЬНО - з обов'язковими першим та останнім пунктами
TodoWrite([
    # 🚨 ПУНКТ #1 - ОБОВ'ЯЗКОВИЙ
    {
        "content": "🚨 ОБОВ'ЯЗКОВО: Оновити статус задачі на 'doing' в Archon",
        "status": "pending",
        "activeForm": "Оновлюю статус задачі на 'doing' в Archon"
    },

    # Основні робочі пункти
    {
        "content": "Додати regex валідацію email в auth/validators.py",
        "status": "pending",
        "activeForm": "Додаю regex валідацію email"
    },
    {
        "content": "Створити unit тести для email валідації",
        "status": "pending",
        "activeForm": "Створюю unit тести"
    },
    {
        "content": "Оновити форму реєстрації з новою валідацією",
        "status": "pending",
        "activeForm": "Оновлюю форму реєстрації"
    },
    {
        "content": "Запустити pytest та переконатися що всі тести пройшли",
        "status": "pending",
        "activeForm": "Запускаю pytest"
    },

    # ✅ ОСТАННІЙ ПУНКТ - ОБОВ'ЯЗКОВИЙ
    {
        "content": "✅ ОБОВ'ЯЗКОВО: Post-Task Checklist - оновити статус на 'done', звіт користувачу",
        "status": "pending",
        "activeForm": "Виконую Post-Task Checklist та оновлюю статус на 'done'"
    }
])
```

### Крок 4: Виконання ПЕРШОГО пункту (Рівень 1 захисту)

```python
# Агент виконує ПЕРШИЙ пункт TodoWrite
await mcp__archon__manage_task(
    action="update",
    task_id="test-12345678-1234-1234-1234-123456789abc",
    status="doing"
)

print("✅ Статус оновлено на 'doing'")
```

**Результат:**
```
[OK] Task status updated: todo → doing
```

### Крок 5: Виконання робочих пунктів

```python
# Пункт 2: Додати regex валідацію
# (код валідації...)

# Пункт 3: Створити unit тести
# (код тестів...)

# Пункт 4: Оновити форму
# (код форми...)

# Пункт 5: Запустити pytest
# pytest tests/test_email_validation.py
```

**Результат pytest:**
```
===== test session starts =====
collected 5 items

tests/test_email_validation.py::test_valid_email PASSED
tests/test_email_validation.py::test_invalid_email PASSED
tests/test_email_validation.py::test_empty_email PASSED
tests/test_email_validation.py::test_malformed_email PASSED
tests/test_email_validation.py::test_special_chars PASSED

===== 5 passed in 0.42s =====
```

### Крок 6: Виконання ОСТАННЬОГО пункту (Post-Task Checklist)

```python
# КРОК 0 з Post-Task Checklist: Оновлення статусу

# Аналіз результату
work_completed_successfully = True  # Всі тести пройшли
no_issues = True  # Проблем немає

# Вибір статусу
if work_completed_successfully and no_issues:
    new_status = "done"

# ОБОВ'ЯЗКОВЕ оновлення статусу
await mcp__archon__manage_task(
    action="update",
    task_id="test-12345678-1234-1234-1234-123456789abc",
    status="done"
)

print("✅ Статус оновлено на 'done'")
```

**Результат:**
```
[OK] Task status updated: doing → done
```

### Крок 7: Git commit з валідацією (Рівень 3 захисту)

```bash
# Додати зміни
git add auth/validators.py tests/test_email_validation.py

# Спроба комміту
git commit -m "[TASK_ID: test-12345678-1234-1234-1234-123456789abc] Add email validation to registration form"
```

**Результат (валідація проходить):**
```
[INFO] Found Task ID: test-12345678-1234-1234-1234-123456789abc
[INFO] Checking task status in Archon MCP...
[INFO] Task status: done
[OK] Task status is valid for commit

[main abc1234] Add email validation to registration form
 2 files changed, 45 insertions(+)
```

### Крок 8: Push в репозиторій

```bash
git push origin main
```

**Результат:**
```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Writing objects: 100% (4/4), 1.23 KiB | 1.23 MiB/s, done.
Total 4 (delta 2), reused 0 (delta 0)
To github.com:example/project.git
   def5678..abc1234  main -> main
```

---

## ❌ НЕПРАВИЛЬНІ СЦЕНАРІЇ (як НЕ ТРЕБА)

### Сценарій 1: Пропущено оновлення на "doing" (Рівень 1 + 2)

**Що робить агент:**
```python
# ❌ НЕПРАВИЛЬНО - створює TodoWrite БЕЗ обов'язкового першого пункту
TodoWrite([
    {"content": "Додати валідацію email", "status": "pending"},
    {"content": "Створити тести", "status": "pending"},
    {"content": "Оновити форму", "status": "pending"}
])
```

**Спрацьовує Рівень 2 - ЧЕРВОНА ЛІНІЯ #3:**
```
🚨 ЧЕРВОНА ЛІНІЯ #3 ПОРУШЕНА!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ПРОБЛЕМА:
TodoWrite створено БЕЗ обов'язкового ПЕРШОГО пункту:
"🚨 ОБОВ'ЯЗКОВО: Оновити статус задачі на 'doing' в Archon"

ДІЯ:
1. НЕГАЙНО ЗУПИНИТИСЯ
2. Видалити неправильний TodoWrite
3. Створити новий TodoWrite з обов'язковими пунктами
4. ТІЛЬКИ ПІСЛЯ - продовжити роботу

Документація: .claude/rules/03_task_management.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Сценарій 2: Спроба комміту зі статусом "todo" (Рівень 3)

**Що робить агент:**
```bash
# Агент НЕ оновив статус з "todo" на "doing"
# Створив зміни в коді
git add auth/validators.py

# Спроба комміту
git commit -m "[TASK_ID: test-12345678-1234-1234-1234-123456789abc] Add email validation"
```

**Спрацьовує Рівень 3 - Автоматична валідація:**
```
[INFO] Found Task ID: test-12345678-1234-1234-1234-123456789abc
[INFO] Checking task status in Archon MCP...
[INFO] Task status: todo

======================================================================
[ERROR] COMMIT BLOCKED - Task status is 'todo'
======================================================================

PROBLEM:
  Task status is 'todo', which means work hasn't started yet.
  You MUST update status to 'doing' before making commits.

SOLUTION:
  1. Update task status to 'doing' in Archon MCP:
     mcp__archon__manage_task(action='update', task_id='test-12345678-1234-1234-1234-123456789abc', status='doing')

  2. After that, retry your commit:
     git commit

RED LINE #1 VIOLATED:
  .claude/rules/02_workflow_rules.md -> 'ЧЕРВОНА ЛІНІЯ #1'
  Work without 'doing' status is FORBIDDEN!

======================================================================
```

**Коміт заблоковано! Зміни НЕ збережено.**

### Сценарій 3: Спроба комміту зі статусом "doing" (Рівень 3)

**Що робить агент:**
```bash
# Агент оновив статус на "doing" ✅
# Виконав роботу ✅
# АЛЕ НЕ оновив статус на "done" перед комітом ❌

git add auth/validators.py tests/test_email_validation.py
git commit -m "[TASK_ID: test-12345678-1234-1234-1234-123456789abc] Add email validation"
```

**Спрацьовує Рівень 3 - Автоматична валідація:**
```
[INFO] Found Task ID: test-12345678-1234-1234-1234-123456789abc
[INFO] Checking task status in Archon MCP...
[INFO] Task status: doing

======================================================================
[ERROR] COMMIT BLOCKED - Task status is 'doing'
======================================================================

PROBLEM:
  Task status is 'doing', which means work is not finished yet.
  You MUST update status to 'done' or 'review' before committing.

SOLUTION:
  1. If work is complete without issues:
     mcp__archon__manage_task(action='update', task_id='test-12345678-1234-1234-1234-123456789abc', status='done')

  2. If work needs expert review:
     mcp__archon__manage_task(action='update', task_id='test-12345678-1234-1234-1234-123456789abc', status='review')

  3. After updating status, retry your commit:
     git commit

RED LINE #2 VIOLATED:
  .claude/rules/02_workflow_rules.md -> 'ЧЕРВОНА ЛІНІЯ #2'
  Git commit without 'done'/'review' status is FORBIDDEN!

======================================================================
```

**Коміт заблоковано! Зміни НЕ збережено.**

---

## 🛡️ Захист на 3 рівнях - Таблиця спрацювання

| Порушення | Рівень 1 (TodoWrite) | Рівень 2 (RED LINES) | Рівень 3 (Hook) |
|-----------|---------------------|---------------------|-----------------|
| **TodoWrite без обов'язкових пунктів** | ✅ Спрацьовує | ✅ Спрацьовує | - |
| **Робота без статусу "doing"** | ✅ Спрацьовує | ✅ Спрацьовує | ✅ Спрацьовує |
| **Коміт без статусу "done"/"review"** | ✅ Спрацьовує | ✅ Спрацьовує | ✅ Спрацьовує |

**Ключові переваги системи:**
- **Defense in Depth:** Три незалежні рівні захисту
- **Graceful Degradation:** Якщо один рівень недоступний - працюють інші
- **Clear Guidance:** Чіткі інструкції як виправити порушення

---

## 📊 Метрики успішності

### До впровадження системи (проблема):
- ❌ Task 6042cd2b-e547-473d-975c-f19cfc3ef1b0 - статус так і залишився "todo"
- ❌ Агенти регулярно забувають оновлювати статус
- ❌ Відсутній механізм примусового контролю

### Після впровадження системи (очікувані результати):
- ✅ 100% задач мають правильні статуси
- ✅ Неможливо зробити коміт без оновлення статусу
- ✅ Автоматична перевірка на кожному кроці
- ✅ Чіткі інструкції для виправлення порушень

---

## 🔗 Зв'язок з документацією

### Реалізовані рівні захисту:

**Рівень 1: Обов'язкові пункти TodoWrite**
- Документація: `.claude/rules/03_task_management.md` (після рядка 111)
- Розділ: "ОБОВ'ЯЗКОВА СТРУКТУРА TodoWrite"

**Рівень 2: ЧЕРВОНІ ЛІНІЇ**
- Документація: `.claude/rules/02_workflow_rules.md` (після рядка 68)
- Розділи:
  - ЧЕРВОНА ЛІНІЯ #1: Робота без статусу "doing"
  - ЧЕРВОНА ЛІНІЯ #2: Git коміт без статусу "done"
  - ЧЕРВОНА ЛІНІЯ #3: TodoWrite без обов'язкових пунктів

**Рівень 3: Автоматична валідація**
- Скрипт: `common/validate_task_status_before_commit.py`
- Інструкція: `docs/SETUP_TASK_STATUS_VALIDATION.md`
- Інтеграція: `.git/hooks/commit-msg`

**Post-Task Checklist:**
- Документація: `.claude/rules/10_post_task_checklist.md`
- КРОК 0: Оновлення статусу задачі (доданий на початок)

---

## ✅ Висновок

Система з 3 рівнів захисту успішно **ВИРІШУЄ** проблему забутих оновлень статусів задач:

1. **Рівень 1 (Структура):** Примушує агентів включати обов'язкові пункти в TodoWrite
2. **Рівень 2 (Правила):** ЧЕРВОНІ ЛІНІЇ зупиняють роботу при порушеннях
3. **Рівень 3 (Автоматизація):** Git hook автоматично блокує некоректні комміти

**Результат:** Неможливо завершити задачу без правильного оновлення статусу на кожному етапі.

---

**Автор:** Blueprint Architect
**Версія:** 1.0
**Дата:** 2025-10-18
**Статус:** ✅ Тестування пройдено
