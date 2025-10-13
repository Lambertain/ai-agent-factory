# 05. Git інтеграція

## 📋 ОБОВ'ЯЗКОВЕ ПРАВИЛО GIT КОММІТІВ

**Кожна виконана задача ПОВИННА завершуватися git коммітом!**

### Коли створювати коммі:

- ✅ **Після завершення КОЖНОЇ основної задачі**
- ✅ **Після рефлексії та покращень**
- ✅ **ПЕРЕД оновленням статусу задачі в Archon на "done"**
- ❌ **НЕ створювати пусті коммі** якщо змін немає

### Формат коммітів:

**Структура повідомлення:**
```
[тип]: [короткий опис]

[детальний опис змін]

[створені/змінені файли]

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Типи коммітів:**
- `feat`: нова функціональність
- `fix`: виправлення бага
- `refactor`: рефакторинг коду
- `docs`: зміни в документації
- `test`: додавання або зміна тестів
- `chore`: технічні зміни (залежності, конфігурація)

### Приклад коммиту:

```bash
git add .
git commit -m "$(cat <<'EOF'
refactor: модульна архітектура правил агентів

Розділив монолітний CLAUDE.md на 7 модульних файлів для покращення запам'ятовування правил агентами:

Створені файли:
- .claude/rules/01_role_switching.md - правила переключення ролей
- .claude/rules/02_workflow_rules.md - правила робочого процесу
- .claude/rules/03_task_management.md - управління задачами
- .claude/rules/04_quality_standards.md - стандарти якості
- .claude/rules/05_git_integration.md - git інтеграція
- .claude/rules/06_coding_standards.md - стандарти кодування
- .claude/rules/07_agent_specific.md - специфіка агентів
- .claude/rules/refresh_protocol.md - протокол освіження пам'яті

Очікуваний результат: 80%+ покращення дотримання правил агентами.

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 🚨 КРИТИЧНЕ ПРАВИЛО: PUSH НЕГАЙНО ПІСЛЯ КОЖНОГО КОМІТУ

**ДЛЯ ВСІХ ПРОЕКТІВ З GIT РЕПОЗИТОРІЄМ!**

### ❌ СТАРЕ ПРАВИЛО (СКАСОВАНО):
```
❌ Кожні 5 коммітів - пуш в удаленний репозиторій
```

### ✅ НОВЕ ПРАВИЛО (ОБОВ'ЯЗКОВЕ З 2025-10-13):

**КОЖЕН КОМІТ = НЕГАЙНИЙ PUSH**

```bash
# ПОСЛІДОВНІСТЬ ОПЕРАЦІЙ:
1. git add .
2. git commit -m "feat: опис змін"
3. 🚨 НЕГАЙНО: git push origin main
```

### Чому це критично важливо:

**Проблема старого підходу:**
- ❌ Агенти накопичують локальні коммі → забувають пушити
- ❌ Remote репозиторій застарілий → інші не бачать змін
- ❌ Конфлікти при паралельній розробці
- ❌ Втрата даних при збоях системи

**Переваги нового підходу:**
- ✅ Remote завжди актуальний
- ✅ Прозорість для команди
- ✅ Захист від втрати даних
- ✅ Краща колаборація

---

## 🔨 ОБОВ'ЯЗКОВА ПЕРЕВІРКА БІЛДА ПЕРЕД PUSH

**НІКОЛИ НЕ ПУШИТИ БЕЗ ПЕРЕВІРКИ БІЛДА!**

### Золоте правило:

```
BUILD → COMMIT → PUSH
(якщо білд провалився → ВИПРАВИТИ → BUILD → COMMIT → PUSH)
```

### 🚨 КРИТИЧНИЙ WORKFLOW:

#### КРОК 1: Запустити білд проекту

**Python проекти:**
```bash
# Варіант 1: Pytest
python -m pytest

# Варіант 2: Unittest
python -m unittest discover

# Варіант 3: Lint + Tests
black . && flake8 . && python -m pytest
```

**Node.js/TypeScript проекти:**
```bash
# Next.js
npm run build

# React/Vue/Angular
npm run build

# З тестами
npm run build && npm test
```

**Go проекти:**
```bash
# Білд всіх пакетів
go build ./...

# З тестами
go build ./... && go test ./...
```

#### КРОК 2: Перевірити результат

**✅ БІЛД УСПІШНИЙ:**
```bash
# Можна продовжувати
git add .
git commit -m "feat: опис"
git push origin main
```

**❌ БІЛД ПРОВАЛИВСЯ:**
```bash
# ЗУПИНИСЬ! НЕ КОММІ! НЕ ПУШ!
# 1. Виправ помилки
# 2. Знову запусти білд
# 3. Тільки після успішного білда → commit → push
```

### Приклад повного workflow:

```bash
# Python проект
python -m pytest  # КРОК 1: Білд
if [ $? -eq 0 ]; then
    echo "[OK] Tests passed"
    git add .
    git commit -m "feat: додана нова функціональність"
    git push origin main  # 🚨 НЕГАЙНИЙ PUSH
else
    echo "[ERROR] Tests failed - FIX BEFORE COMMIT!"
    exit 1
fi

# Node.js проект
npm run build  # КРОК 1: Білд
if [ $? -eq 0 ]; then
    echo "[OK] Build successful"
    git add .
    git commit -m "feat: оновлено UI компонент"
    git push origin main  # 🚨 НЕГАЙНИЙ PUSH
else
    echo "[ERROR] Build failed - FIX BEFORE COMMIT!"
    exit 1
fi
```

### 📋 Чек-лист перед push:

- [ ] ✅ Білд успішний (без помилок)
- [ ] ✅ Всі тести пройдені
- [ ] ✅ Код відформатований (black, prettier, gofmt)
- [ ] ✅ Lint перевірка успішна
- [ ] ✅ Git коміт створено
- [ ] 🚨 **Git push виконано НЕГАЙНО**

### ⚠️ Що робити при помилках:

**Сценарій 1: Помилки білда**
```
1. Прочитати вивід помилки
2. Виправити код
3. Знову запустити білд
4. Якщо успішно → commit → push
```

**Сценарій 2: Проваленні тести**
```
1. Визначити причину провалу
2. Виправити код або тести
3. Знову запустити тести
4. Якщо пройшли → commit → push
```

**Сценарій 3: Lint помилки**
```
1. Запустити автоформатування (black, prettier)
2. Виправити решту вручну
3. Знову запустити lint
4. Якщо чисто → commit → push
```

---

### ОБОВ'ЯЗКОВИЙ PUSH ДЛЯ PRODUCTION ПРОЕКТІВ

**Production проекти ЗАВЖДИ вимагають синхронізації з remote репозиторієм!**

### КРИТИЧНЕ ПРАВИЛО: НЕ ЗАБУВАЙ PUSH

**Проблема:** Агенти роблять зміни в production проектах локально і забувають запушити → код в репозиторії та production розходяться

**Рішення:** ОБОВ'ЯЗКОВИЙ пункт в TodoWrite для production проектів

### Визначення deployment_status:

**Production проекти** (ОБОВ'ЯЗКОВИЙ push після КОЖНОГО комміту):
- Description містить: "production", "prod", "deployed", "live"
- ПРИКЛАД: "Production AI Agent Factory", "Deployed web app"

**Staging проекти** (рекомендований push):
- Description містить: "staging", "stage", "pre-production"
- ПРИКЛАД: "Staging environment for testing"

**Local проекти** (опціональний push):
- Всі інші проекти
- ПРИКЛАД: "Development playground"

### ОБОВ'ЯЗКОВЕ ПРАВИЛО: Структура TodoWrite для production

**Якщо проект production → ЗАВЖДИ додавай останній пункт:**

```python
from common.git_utils import check_production_status

# Перевірити чи це production проект
status = await check_production_status(project_info, local_repo_path)

if status["is_production"]:
    # ОБОВ'ЯЗКОВО додай останній пункт TodoWrite
    todos = [
        {"content": "Виконати основну задачу", "status": "pending"},
        {"content": "Рефлексія та покращення", "status": "pending"},
        {"content": "Git коммит з описом змін", "status": "pending"},
        {"content": "ОБОВ'ЯЗКОВО: Git push для синхронізації production", "status": "pending"}
    ]
```

### Використання git_utils для нагадування:

```python
from common.git_utils import create_commit_with_check

# Створити коммит з автоматичною перевіркою
result = await create_commit_with_check(
    project_info={"description": "Production AI Agent Factory"},
    local_repo_path="/path/to/repo",
    commit_message="feat: додана нова функціональність"
)

print(f"[OK] Commit: {result['commit_hash'][:8]}")
print(f"[STATUS] Deployment: {result['deployment_status']}")

# Якщо production і є непушнуті комміти → ПОКАЗАТИ НАГАДУВАННЯ
if result["needs_push"]:
    print(result["reminder_message"])
    # ВИКОНАТИ PUSH:
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)
```

### Приклад workflow для production проекту:

```python
# 1. В початку задачі - перевірити статус проекту
from common.git_utils import check_production_status
import os

project = await mcp__archon__find_projects(project_id=task["project_id"])
status = await check_production_status(project, os.getcwd())

print(f"[INFO] Deployment status: {status['status_message']}")

# 2. Створити TodoWrite з обов'язковим push якщо production
if status["is_production"]:
    todos = [
        {"content": "Виконати задачу", "status": "pending"},
        {"content": "Рефлексія", "status": "pending"},
        {"content": "Git commit", "status": "pending"},
        {"content": "ОБОВ'ЯЗКОВО: Git push для production", "status": "pending"}
    ]
else:
    todos = [
        {"content": "Виконати задачу", "status": "pending"},
        {"content": "Рефлексія", "status": "pending"},
        {"content": "Git commit", "status": "pending"}
    ]

# 3. В кінці задачі - створити коммит і перевірити
from common.git_utils import create_commit_with_check

result = await create_commit_with_check(
    project_info=project,
    local_repo_path=os.getcwd(),
    commit_message="feat: реалізовано нову функціональність"
)

# 4. Якщо production - ОБОВ'ЯЗКОВО push
if result["needs_push"]:
    print(result["reminder_message"])

    # ВИКОНАТИ PUSH
    import subprocess
    push_result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=os.getcwd(),
        capture_output=True,
        text=True
    )

    if push_result.returncode == 0:
        print("[OK] Changes pushed to production!")
    else:
        print(f"[ERROR] Push failed: {push_result.stderr}")
```

### Функції git_utils для роботи з production:

**1. `remind_to_push()` - нагадати про push**
```python
result = await remind_to_push(project_info, local_repo_path)
# Повертає: should_remind, unpushed_count, reminder_message
```

**2. `check_production_status()` - перевірити статус**
```python
status = await check_production_status(project_info, local_repo_path)
# Повертає: is_production, unpushed_count, needs_push
```

**3. `create_commit_with_check()` - коммит + перевірка**
```python
result = await create_commit_with_check(
    project_info, local_repo_path, commit_message
)
# Повертає: commit_hash, needs_push, reminder_message
```

### Безпечний manual push (для non-production):

Якщо потрібно вручну запушити зміни:

```bash
# ЗАВЖДИ перевіряти статус перед push
git status

# Переконатися що всі зміни закоммічені
git log origin/main..HEAD --oneline

# Push з перевіркою
git push origin main
```

## ⚠️ ВАЖЛИВІ ПРАВИЛА GIT:

### НІКОЛИ НЕ:

- ❌ Використовувати `git commit --amend` без явного запиту користувача
- ❌ Робити `git push --force` на main/master
- ❌ Пропускати hooks (`--no-verify`)
- ❌ Видаляти або перезаписувати існуючий код без інструкції
- ❌ Коммітити файли з секретами (.env, credentials.json)

### ЗАВЖДИ:

- ✅ Перевіряти `git status` перед коммітом
- ✅ Переглядати зміни через `git diff`
- ✅ Писати змістовні повідомлення коммітів
- ✅ Слідувати стилю коммітів репозиторію (`git log --oneline -5`)
- ✅ Використовувати HEREDOC для багаторядкових повідомлень

## 📝 ШАБЛОН ДЛЯ КОММІТІВ

**Використовуй цей шаблон для кожного коммиту:**

```bash
git add [файли]

git commit -m "$(cat <<'EOF'
[тип]: [стислий опис (до 50 символів)]

[Детальний опис що було зроблено]

[Створені файли:]
- file1.md
- file2.py

[Змінені файли:]
- existing_file.md

[Причина змін:]
[Опис чому були внесені зміни]

[Очікуваний результат:]
[Опис покращень]

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 🎯 ФІНАЛЬНИЙ КРОК КОЖНОЇ ЗАДАЧІ

**ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ (ОНОВЛЕНА 2025-10-13):**

```
1. Виконання задачі
2. Рефлексія та покращення
3. 🔨 БІЛД-ПЕРЕВІРКА (pytest/npm build/go build)
4. ✅ GIT КОМІТ з описом змін (якщо білд успішний)
5. 🚨 GIT PUSH НЕГАЙНО ПІСЛЯ КОМІТУ (для всіх проектів з git)
6. Оновлення статусу в Archon на "done"
```

**НІКОЛИ НЕ ПРОПУСКАЙ:**
- ❌ БІЛД-ПЕРЕВІРКУ перед коммітом
- ❌ GIT КОМІТ після білда
- ❌ GIT PUSH після коміту

**ЗАВЖДИ РОБИТИ В ТАКІЙ ПОСЛІДОВНОСТІ:**
```
BUILD → COMMIT → PUSH → ARCHON UPDATE
```
