"""
Git utilities для напоминания агентам о push в production проектах.

Этот модуль предоставляет функции для проверки непушнутых коммитов
и напоминания агентам о необходимости синхронизации с remote репозиторием.
"""

import subprocess
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


async def remind_to_push(
    project_info: Optional[Dict],
    local_repo_path: str,
    show_warning: bool = True
) -> Dict[str, any]:
    """
    Напомнить агенту о необходимости push для production проекта.

    Проверяет deployment_status проекта и количество непушнутых коммитов.
    Если проект production и есть непушнутые коммиты - возвращает предупреждение.

    Args:
        project_info: Информация о проекте (title, description, github_repo)
        local_repo_path: Путь к локальному репозиторию
        show_warning: Показывать ли предупреждение в логах

    Returns:
        Dict: {
            "should_remind": bool,
            "unpushed_count": int,
            "deployment_status": str,
            "reminder_message": str
        }

    Examples:
        >>> # Production проект с непушнутыми коммитами
        >>> project = {"description": "Production AI Agent Factory"}
        >>> result = await remind_to_push(project, "/path/to/repo")
        >>> if result["should_remind"]:
        ...     print(result["reminder_message"])

        🚨 КРИТИЧНО: PRODUCTION проект имеет 3 непушнутых коммитов!

        ⚠️ ОБЯЗАТЕЛЬНО выполнить:
           git push origin main

        ❌ НЕ ЗАВЕРШАЙ задачу без push!
    """

    # Проверка 1: Определить deployment_status
    deployment_status = _detect_deployment_status(project_info)

    # Если не production - не напоминать
    if deployment_status != "production":
        return {
            "should_remind": False,
            "unpushed_count": 0,
            "deployment_status": deployment_status,
            "reminder_message": f"[{deployment_status.upper()}] Проект не требует обязательного push"
        }

    # Проверка 2: Подсчитать непушнутые коммиты
    try:
        unpushed_count = _count_unpushed_commits(local_repo_path)
    except Exception as e:
        logger.error(f"Ошибка при подсчете коммитов: {e}")
        return {
            "should_remind": False,
            "unpushed_count": 0,
            "deployment_status": deployment_status,
            "reminder_message": f"[ERROR] Не удалось проверить коммиты: {str(e)}"
        }

    # Проверка 3: Есть ли непушнутые коммиты?
    if unpushed_count > 0:
        reminder = f"""
[PRODUCTION] Проект имеет {unpushed_count} непушнутых коммитов!

ОБЯЗАТЕЛЬНО выполнить:
   git push origin main

НЕ ЗАВЕРШАЙ задачу без push!
"""

        if show_warning:
            logger.warning(reminder)

        return {
            "should_remind": True,
            "unpushed_count": unpushed_count,
            "deployment_status": "production",
            "reminder_message": reminder.strip()
        }

    # Все коммиты запушены
    return {
        "should_remind": False,
        "unpushed_count": 0,
        "deployment_status": "production",
        "reminder_message": "[OK] Все коммиты запушены в production"
    }


async def check_production_status(
    project_info: Optional[Dict],
    local_repo_path: str
) -> Dict[str, any]:
    """
    Проверить статус production проекта и вернуть полную информацию.

    Используется агентами для понимания нужно ли синхронизировать код.

    Args:
        project_info: Информация о проекте
        local_repo_path: Путь к локальному репозиторию

    Returns:
        Dict: {
            "is_production": bool,
            "unpushed_count": int,
            "needs_push": bool,
            "status_message": str
        }

    Examples:
        >>> status = await check_production_status(project, "/path/to/repo")
        >>> print(f"Production: {status['is_production']}")
        >>> print(f"Unpushed: {status['unpushed_count']}")
        >>> if status['needs_push']:
        ...     print("ТРЕБУЕТСЯ PUSH!")
    """

    deployment_status = _detect_deployment_status(project_info)
    is_production = deployment_status == "production"

    if not is_production:
        return {
            "is_production": False,
            "unpushed_count": 0,
            "needs_push": False,
            "status_message": f"[{deployment_status.upper()}] Проект не production"
        }

    try:
        unpushed_count = _count_unpushed_commits(local_repo_path)
    except Exception as e:
        logger.error(f"Ошибка проверки коммитов: {e}")
        return {
            "is_production": True,
            "unpushed_count": 0,
            "needs_push": False,
            "status_message": f"[ERROR] {str(e)}"
        }

    needs_push = unpushed_count > 0

    if needs_push:
        status_message = f"[PRODUCTION] {unpushed_count} коммитов требуют push"
    else:
        status_message = "[PRODUCTION] Все коммиты синхронизированы"

    return {
        "is_production": True,
        "unpushed_count": unpushed_count,
        "needs_push": needs_push,
        "status_message": status_message
    }


def _detect_deployment_status(project_info: Optional[Dict]) -> str:
    """
    Определить deployment_status проекта из description.

    Ключевые слова для определения статуса:
    - production: "production", "prod", "deployed", "live"
    - staging: "staging", "stage", "pre-production"
    - local: всё остальное (по умолчанию)

    Args:
        project_info: Словарь с информацией о проекте

    Returns:
        str: "production", "staging" или "local"
    """
    if not project_info:
        return "local"

    description = project_info.get("description", "").lower()
    title = project_info.get("title", "").lower()

    # Объединяем для поиска ключевых слов
    text = f"{description} {title}"

    # Проверка на staging (ПЕРВЫМ, чтобы "pre-production" не попал в production!)
    staging_keywords = ["staging", "stage", "pre-production", "preprod"]
    if any(keyword in text for keyword in staging_keywords):
        return "staging"

    # Проверка на production (ВТОРЫМ, после staging)
    production_keywords = ["production", "prod", "deployed", "live"]
    if any(keyword in text for keyword in production_keywords):
        return "production"

    # По умолчанию - local
    return "local"


def _count_unpushed_commits(repo_path: str) -> int:
    """
    Подсчитать количество непушнутых коммитов в локальном репозитории.

    Использует команду: git rev-list @{u}..HEAD --count

    Args:
        repo_path: Путь к git репозиторию

    Returns:
        int: Количество непушнутых коммитов

    Raises:
        subprocess.CalledProcessError: Если команда git не выполнилась
        ValueError: Если upstream branch не настроен
    """
    try:
        # Проверить что upstream branch настроен
        check_upstream = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "@{u}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )

        if check_upstream.returncode != 0:
            # Upstream не настроен
            logger.warning(f"No upstream branch configured for {repo_path}")
            return 0

        # Подсчитать непушнутые коммиты
        result = subprocess.run(
            ["git", "rev-list", "@{u}..HEAD", "--count"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        count = int(result.stdout.strip())
        return count

    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e.stderr}")
        raise
    except ValueError as e:
        logger.error(f"Failed to parse commit count: {e}")
        return 0


async def create_commit_with_check(
    project_info: Optional[Dict],
    local_repo_path: str,
    commit_message: str,
    remind_about_push: bool = True
) -> Dict[str, any]:
    """
    Создать коммит и проверить нужен ли push для production проекта.

    Это основная функция для интеграции в git workflow агентов.
    После создания коммита проверяет статус проекта и напоминает о push.

    Args:
        project_info: Информация о проекте (для определения deployment_status)
        local_repo_path: Путь к локальному репозиторию
        commit_message: Сообщение коммита
        remind_about_push: Показывать ли напоминание о push

    Returns:
        Dict с результатами:
            - commit_created: bool
            - commit_hash: str (если успешно)
            - deployment_status: str (production/staging/local)
            - needs_push: bool
            - reminder_message: str

    Examples:
        >>> result = await create_commit_with_check(
        ...     project_info={"description": "Production AI Factory"},
        ...     local_repo_path="/path/to/repo",
        ...     commit_message="feat: add new feature"
        ... )
        >>> print(f"Commit: {result['commit_hash'][:8]}")
        >>> if result['needs_push']:
        ...     print(result['reminder_message'])
    """

    result = {
        "commit_created": False,
        "commit_hash": None,
        "deployment_status": "local",
        "needs_push": False,
        "reminder_message": ""
    }

    # Определить deployment_status
    result["deployment_status"] = _detect_deployment_status(project_info)

    try:
        # ШАГО 1: Создать коммит
        logger.info(f"[GIT] Creating commit: {commit_message[:50]}...")

        # Добавить изменения
        subprocess.run(
            ["git", "add", "."],
            cwd=local_repo_path,
            check=True,
            capture_output=True
        )

        # Создать коммит с правильным форматом
        full_commit_message = f"""{commit_message}

Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""

        commit_result = subprocess.run(
            ["git", "commit", "-m", full_commit_message],
            cwd=local_repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        # Получить hash коммита
        hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=local_repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        result["commit_created"] = True
        result["commit_hash"] = hash_result.stdout.strip()

        logger.info(f"[OK] Commit created: {result['commit_hash'][:8]}")

        # ШАГО 2: Проверить нужен ли push для production
        if remind_about_push:
            reminder_result = await remind_to_push(
                project_info=project_info,
                local_repo_path=local_repo_path,
                show_warning=True
            )

            result["needs_push"] = reminder_result["should_remind"]
            result["reminder_message"] = reminder_result["reminder_message"]

        return result

    except subprocess.CalledProcessError as e:
        logger.error(f"[ERROR] Git operation failed: {e.stderr}")
        result["reminder_message"] = f"[ERROR] {e.stderr}"
        return result


# Примеры использования в агентах
USAGE_EXAMPLES = """
# Пример 1: Проверка перед завершением задачи

from common.git_utils import remind_to_push

# В конце выполнения задачи проверить статус
result = await remind_to_push(
    project_info={"description": "Production AI Agent Factory"},
    local_repo_path="/path/to/repo"
)

if result["should_remind"]:
    print(result["reminder_message"])
    # ОБЯЗАТЕЛЬНО запушить перед завершением
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)

# Пример 2: Создание коммита с автоматической проверкой

from common.git_utils import create_commit_with_check

result = await create_commit_with_check(
    project_info=project,
    local_repo_path="/path/to/repo",
    commit_message="feat: добавлен Payment Integration Agent"
)

print(f"[OK] Commit: {result['commit_hash'][:8]}")
print(f"[STATUS] Deployment: {result['deployment_status']}")

if result['needs_push']:
    print(result['reminder_message'])
    # ОБЯЗАТЕЛЬНО выполнить push для production
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)

# Пример 3: Проверка статуса production проекта

from common.git_utils import check_production_status

status = await check_production_status(project, "/path/to/repo")

if status['is_production'] and status['needs_push']:
    print(f"ВНИМАНИЕ: {status['unpushed_count']} коммитов ждут push!")
    print("Выполни: git push origin main")
"""
