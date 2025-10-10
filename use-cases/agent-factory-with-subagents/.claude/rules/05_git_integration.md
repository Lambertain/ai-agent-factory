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

## 🚨 ОБОВ'ЯЗКОВИЙ PUSH ДЛЯ PRODUCTION ПРОЕКТІВ

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

**ОБОВ'ЯЗКОВА ПОСЛІДОВНІСТЬ:**

```
1. Виконання задачі
2. Рефлексія та покращення
3. ✅ GIT КОМІТ з описом змін
4. Оновлення статусу в Archon на "done"
```

**НІКОЛИ НЕ ПРОПУСКАЙ ГІТ КОМІТ!**
