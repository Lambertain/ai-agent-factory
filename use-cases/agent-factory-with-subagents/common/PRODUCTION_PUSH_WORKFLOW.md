# Production Push Workflow - Примеры использования

Этот документ содержит практические примеры интеграции Production Push Reminder в workflow агентов.

## Проблема которую решаем

**Проблема:** Агенты делают изменения в production проектах локально и забывают запушить → код в репозитории и production расходятся

**Решение:** ОБЯЗАТЕЛЬНЫЙ пункт в TodoWrite для production проектов + функции напоминания из git_utils

---

## Пример 1: Базовое использование в задаче

```python
from common.git_utils import create_commit_with_check, check_production_status
import os
import subprocess

# В конце выполнения задачи

# Получить информацию о проекте через Archon MCP
project = await mcp__archon__find_projects(project_id=context.get_project_id())

# Создать коммит с автоматической проверкой
result = await create_commit_with_check(
    project_info=project,
    local_repo_path=os.getcwd(),
    commit_message="feat: добавлен Payment Integration Agent"
)

# Вывести результат
print(f"[OK] Commit created: {result['commit_hash'][:8]}")
print(f"[STATUS] Deployment: {result['deployment_status']}")

# Если production и есть непушнутые коммиты → ПОКАЗАТЬ НАПОМИНАНИЕ
if result["needs_push"]:
    print(result["reminder_message"])

    # ОБЯЗАТЕЛЬНО выполнить push для production
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

**Результат для production проекта:**
```
[OK] Commit created: abc12345
[STATUS] Deployment: production

[PRODUCTION] Проект имеет 3 непушнутых коммитов!

ОБЯЗАТЕЛЬНО выполнить:
   git push origin main

НЕ ЗАВЕРШАЙ задачу без push!

[OK] Changes pushed to production!
```

**Результат для local проекта:**
```
[OK] Commit created: def67890
[STATUS] Deployment: local
[LOCAL] Проект не требует обязательного push
```

---

## Пример 2: Проверка статуса перед началом задачи

```python
from common.git_utils import check_production_status
import os

# Перед началом задачи проверить статус проекта

project = await mcp__archon__find_projects(project_id=task["project_id"])

status = await check_production_status(
    project_info=project,
    local_repo_path=os.getcwd()
)

print(f"[INFO] {status['status_message']}")

# Если production - добавить обязательный пункт в TodoWrite
if status["is_production"]:
    print("[INFO] Production проект - обязательный push после коммита!")

    todos = [
        {"content": "Выполнить основную задачу", "status": "pending"},
        {"content": "Рефлексия и критический анализ", "status": "pending"},
        {"content": "Git коммит с описом изменений", "status": "pending"},
        {"content": "ОБЯЗАТЕЛЬНО: Git push для синхронизации production", "status": "pending"}
    ]
else:
    todos = [
        {"content": "Выполнить основную задачу", "status": "pending"},
        {"content": "Рефлексия и критический анализ", "status": "pending"},
        {"content": "Git коммит с описом изменений", "status": "pending"}
    ]

await TodoWrite(todos)
```

**Вывод:**
```
[INFO] [PRODUCTION] 3 коммитов требуют push
[INFO] Production проект - обязательный push после коммита!
```

---

## Пример 3: Напоминание перед завершением задачи

```python
from common.git_utils import remind_to_push
import os
import subprocess

# В самом конце выполнения задачи

project = await mcp__archon__find_projects(project_id=task["project_id"])

# Проверить нужен ли push
reminder = await remind_to_push(
    project_info=project,
    local_repo_path=os.getcwd()
)

if reminder["should_remind"]:
    print(reminder["reminder_message"])

    # ОБЯЗАТЕЛЬНО запушить перед завершением
    push_result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=os.getcwd(),
        capture_output=True,
        text=True
    )

    if push_result.returncode == 0:
        print("[OK] All changes synced to production!")
    else:
        print(f"[ERROR] Push failed: {push_result.stderr}")
else:
    print(reminder["reminder_message"])
```

**Результат:**
```
[PRODUCTION] Проект имеет 1 непушнутых коммитов!

ОБЯЗАТЕЛЬНО выполнить:
   git push origin main

НЕ ЗАВЕРШАЙ задачу без push!

[OK] All changes synced to production!
```

---

## Пример 4: Полный workflow задачи с Production Push

```python
async def execute_task(task_id: str):
    """Полный workflow выполнения задачи с Production Push."""

    from common.git_utils import check_production_status, create_commit_with_check
    import os
    import subprocess

    # 1. Получить задачу из Archon
    task = await mcp__archon__find_tasks(task_id=task_id)
    project = await mcp__archon__find_projects(project_id=task["project_id"])

    # 2. Проверить статус проекта
    status = await check_production_status(project, os.getcwd())
    print(f"[INFO] {status['status_message']}")

    # 3. Создать микрозадачи с учетом production статуса
    if status["is_production"]:
        await TodoWrite([
            {"content": "Выполнить основную работу", "status": "in_progress"},
            {"content": "Рефлексия и анализ", "status": "pending"},
            {"content": "Git коммит с описанием", "status": "pending"},
            {"content": "ОБЯЗАТЕЛЬНО: Git push для production", "status": "pending"},
            {"content": "Обновить статус в Archon", "status": "pending"}
        ])
    else:
        await TodoWrite([
            {"content": "Выполнить основную работу", "status": "in_progress"},
            {"content": "Рефлексия и анализ", "status": "pending"},
            {"content": "Git коммит с описанием", "status": "pending"},
            {"content": "Обновить статус в Archon", "status": "pending"}
        ])

    # 4. Выполнить основную работу
    # ... (код выполнения задачи)

    # 5. Рефлексия
    await TodoWrite([
        {"content": "Выполнить основную работу", "status": "completed"},
        {"content": "Рефлексия и анализ", "status": "in_progress"},
        # ...
    ])

    # Провести рефлексию...
    improvements = analyze_and_improve()

    # 6. Git коммит с автоматической проверкой
    await TodoWrite([
        {"content": "Выполнить основную работу", "status": "completed"},
        {"content": "Рефлексия и анализ", "status": "completed"},
        {"content": "Git коммит с описанием", "status": "in_progress"},
        # ...
    ])

    result = await create_commit_with_check(
        project_info=project,
        local_repo_path=os.getcwd(),
        commit_message=f"feat: {task['title']}\n\n{improvements}"
    )

    print(f"[OK] Commit: {result['commit_hash'][:8]}")

    # 7. Если production - ОБЯЗАТЕЛЬНО push
    if result["needs_push"]:
        await TodoWrite([
            {"content": "Выполнить основную работу", "status": "completed"},
            {"content": "Рефлексия и анализ", "status": "completed"},
            {"content": "Git коммит с описанием", "status": "completed"},
            {"content": "ОБЯЗАТЕЛЬНО: Git push для production", "status": "in_progress"},
            {"content": "Обновить статус в Archon", "status": "pending"}
        ])

        print(result["reminder_message"])

        # ВЫПОЛНИТЬ PUSH
        push_result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )

        if push_result.returncode == 0:
            print("[OK] Pushed to production!")
        else:
            print(f"[ERROR] Push failed: {push_result.stderr}")
            return  # НЕ завершать задачу если push провалился

    # 8. Обновить статус в Archon
    await mcp__archon__manage_task(
        action="update",
        task_id=task_id,
        status="done"
    )

    # 9. Вывести итоги
    print("\n[OK] Задача завершена:")
    print(f"   Title: {task['title']}")
    print(f"   Commit: {result['commit_hash'][:8]}")
    print(f"   Deployment: {result['deployment_status']}")

    if status["is_production"]:
        print("   Push: [OK] Synced with production")
```

---

## Пример 5: Определение deployment_status для разных проектов

```python
from common.git_utils import check_production_status

# Production проект
project1 = {"description": "Production AI Agent Factory", "title": "AI Factory"}
status1 = await check_production_status(project1, "/path/to/repo")
print(f"Production: {status1['is_production']}")  # True
print(f"Needs push: {status1['needs_push']}")     # True if unpushed commits

# Staging проект
project2 = {"description": "Staging environment for testing", "title": "Test App"}
status2 = await check_production_status(project2, "/path/to/repo")
print(f"Production: {status2['is_production']}")  # False

# Local проект
project3 = {"description": "Development playground", "title": "My Experiments"}
status3 = await check_production_status(project3, "/path/to/repo")
print(f"Production: {status3['is_production']}")  # False
```

---

## Пример 6: Обработка ошибок git push

```python
from common.git_utils import create_commit_with_check
import subprocess
import logging

logger = logging.getLogger(__name__)

try:
    result = await create_commit_with_check(
        project_info=project,
        local_repo_path=os.getcwd(),
        commit_message="feat: new feature"
    )

    if not result["commit_created"]:
        logger.error("Failed to create commit")
        logger.error(f"Reason: {result['reminder_message']}")
        # Обработать ошибку
        return

    # Если production - пытаемся push с retry
    if result["needs_push"]:
        max_retries = 3
        for attempt in range(max_retries):
            push_result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=os.getcwd(),
                capture_output=True,
                text=True
            )

            if push_result.returncode == 0:
                print(f"[OK] Pushed to production (attempt {attempt + 1})")
                break
            else:
                logger.warning(f"Push attempt {attempt + 1} failed: {push_result.stderr}")

                if attempt == max_retries - 1:
                    logger.error("All push attempts failed!")
                    # Уведомить пользователя
                    print("[ERROR] Cannot sync to production - manual push required")
                    print(f"Error: {push_result.stderr}")

except Exception as e:
    logger.error(f"Git operation failed: {e}")
    # Fallback: попробовать вручную или сообщить пользователю
```

---

## Чек-лист для агентов

При использовании Production Push Reminder убедись что:

- [ ] Проверил deployment_status проекта перед началом задачи
- [ ] Добавил обязательный пункт "Git push" в TodoWrite для production
- [ ] Использовал `create_commit_with_check()` вместо обычного `git commit`
- [ ] Проверил `result["needs_push"]` после коммита
- [ ] Выполнил `git push` если `needs_push == True`
- [ ] Убедился что push прошел успешно перед завершением задачи
- [ ] НЕ завершил задачу в Archon пока не запушил production изменения
- [ ] Логировал события push для аудита

---

## Интеграция с микрозадачами TodoWrite

```python
# Микрозадачи для production агента:

# ШАГ 1: Проверить статус в начале
status = await check_production_status(project, os.getcwd())

# ШАГ 2: Создать TodoWrite с учетом статуса
if status["is_production"]:
    todos = [
        {"content": "Реализовать новую функциональность", "status": "in_progress"},
        {"content": "Написать unit тесты", "status": "pending"},
        {"content": "Обновить документацию", "status": "pending"},
        {"content": "Рефлексия: критический анализ", "status": "pending"},
        {"content": "Git коммит с описанием", "status": "pending"},
        {"content": "ОБЯЗАТЕЛЬНО: Git push для production", "status": "pending"}  # ← ПОСЛЕДНИЙ ШАГ
    ]
else:
    # Для non-production убрать обязательный push
    todos = [
        {"content": "Реализовать новую функциональность", "status": "in_progress"},
        {"content": "Написать unit тесты", "status": "pending"},
        {"content": "Обновить документацию", "status": "pending"},
        {"content": "Рефлексия: критический анализ", "status": "pending"},
        {"content": "Git коммит с описанием", "status": "pending"}
    ]

# Выполнение всех микрозадач...

# Последняя микрозадача - git push (только для production)
if status["is_production"]:
    await TodoWrite([
        {"content": "Реализовать новую функциональность", "status": "completed"},
        {"content": "Написать unit тесты", "status": "completed"},
        {"content": "Обновить документацию", "status": "completed"},
        {"content": "Рефлексия: критический анализ", "status": "completed"},
        {"content": "Git коммит с описанием", "status": "completed"},
        {"content": "ОБЯЗАТЕЛЬНО: Git push для production", "status": "in_progress"}
    ])

    # Создать коммит и проверить
    result = await create_commit_with_check(
        project_info=project,
        local_repo_path=os.getcwd(),
        commit_message="""feat: реализована новая функциональность

Файлы созданы:
- new_feature.py
- tests/test_new_feature.py

Документация обновлена:
- README.md
- docs/usage.md

Все тесты проходят успешно."""
    )

    # Если есть напоминание - выполнить push
    if result["needs_push"]:
        print(result["reminder_message"])

        push_result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )

        if push_result.returncode == 0:
            print("[OK] Production synced!")
        else:
            print(f"[ERROR] {push_result.stderr}")

    # Завершить последнюю микрозадачу
    await TodoWrite([
        {"content": "Реализовать новую функциональность", "status": "completed"},
        {"content": "Написать unit тесты", "status": "completed"},
        {"content": "Обновить документацию", "status": "completed"},
        {"content": "Рефлексия: критический анализ", "status": "completed"},
        {"content": "Git коммит с описанием", "status": "completed"},
        {"content": "ОБЯЗАТЕЛЬНО: Git push для production", "status": "completed"}
    ])
```

---

## Логирование Production Push событий

```python
import logging
from common.git_utils import create_commit_with_check

# Настроить логгер
logger = logging.getLogger("production_push_audit")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("production_push_audit.log")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Выполнить Production Push с логированием
result = await create_commit_with_check(
    project_info=project,
    local_repo_path=os.getcwd(),
    commit_message="feat: critical production fix"
)

# Аудит лог
if result["needs_push"]:
    logger.info(f"PRODUCTION-PUSH-REQUIRED: Project {project['id']}")
    logger.info(f"  Commit: {result['commit_hash']}")
    logger.info(f"  Unpushed: {result.get('unpushed_count', 'unknown')}")

    # Выполнить push
    push_result = subprocess.run(...)

    if push_result.returncode == 0:
        logger.info(f"PRODUCTION-PUSH-SUCCESS: Project {project['id']} synced")
    else:
        logger.error(f"PRODUCTION-PUSH-FAILED: {push_result.stderr}")
else:
    logger.info(f"LOCAL-COMMIT: Project {project['id']} committed locally")
    logger.info(f"  Reason: {result['reminder_message']}")
```

**Лог файл:**
```
[2025-10-10 12:34:56] INFO: PRODUCTION-PUSH-REQUIRED: Project abc-123
[2025-10-10 12:34:56] INFO:   Commit: 1a2b3c4d
[2025-10-10 12:34:56] INFO:   Unpushed: 3
[2025-10-10 12:34:57] INFO: PRODUCTION-PUSH-SUCCESS: Project abc-123 synced
```

---

**Документ создан:** 2025-10-10
**Версия:** 2.0 (Production Push Reminder)
**Автор:** Archon Implementation Engineer
