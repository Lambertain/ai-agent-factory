"""
Валідація статусу задачі Archon перед git коммітом.

Автоматично перевіряє що задача має правильний статус перед комітом:
- Блокує коміт якщо задача в статусі "todo" (робота не почата)
- Блокує коміт якщо задача в статусі "doing" (робота не завершена)
- Дозволяє коміт якщо задача в статусі "done" або "review"

Graceful degradation: якщо Archon MCP недоступний - пропускає перевірку з warning.

Usage:
    python validate_task_status_before_commit.py <commit_message_file>

Pre-commit hook:
    .git/hooks/pre-commit -> викликає цей скрипт автоматично
"""

import re
import sys
from typing import Optional, Tuple


def extract_task_id_from_commit(commit_message: str) -> Optional[str]:
    """
    Витягти Task ID з повідомлення коміту.

    Підтримувані формати:
    - [TASK_ID: abc123...]
    - Task ID: abc123...
    - task_id: abc123...

    Args:
        commit_message: Текст повідомлення коміту

    Returns:
        Task ID або None якщо не знайдено

    Examples:
        >>> extract_task_id_from_commit("[TASK_ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349]")
        'e7cb2e05-21fe-450e-af2c-25ac1b6b8349'
        >>> extract_task_id_from_commit("Task ID: e7cb2e05-21fe-450e-af2c-25ac1b6b8349")
        'e7cb2e05-21fe-450e-af2c-25ac1b6b8349'
        >>> extract_task_id_from_commit("Regular commit without task ID")
        None
    """
    # Pattern 1: [TASK_ID: ...]
    match = re.search(r'\[TASK_ID:\s*([a-f0-9-]{36})\]', commit_message, re.IGNORECASE)
    if match:
        return match.group(1)

    # Pattern 2: Task ID: ...
    match = re.search(r'Task\s+ID:\s*([a-f0-9-]{36})', commit_message, re.IGNORECASE)
    if match:
        return match.group(1)

    return None


def check_task_status_in_archon_sync(task_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Перевірити статус задачі в Archon MCP Server (синхронна версія).

    Використовує синхронний HTTP запит до локального Archon MCP Server.

    Args:
        task_id: UUID задачі

    Returns:
        Tuple[status, error]: (статус задачі, помилка) або (None, error_message)

    Examples:
        >>> check_task_status_in_archon_sync("e7cb2e05-21fe-450e-af2c-25ac1b6b8349")
        ('done', None)
        >>> check_task_status_in_archon_sync("invalid-id")
        (None, 'Task not found in Archon')
    """
    try:
        import json
        import http.client

        # Підключення до локального Archon MCP Server
        conn = http.client.HTTPConnection('localhost', 3000)

        # Формуємо запит до Archon API
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({
            "jsonrpc": "2.0",
            "method": "find_tasks",
            "params": {"task_id": task_id},
            "id": 1
        })

        conn.request('POST', '/api/mcp', body, headers)
        response = conn.getresponse()
        data = response.read().decode()

        if response.status != 200:
            return None, f"Archon MCP Server error: HTTP {response.status}"

        result = json.loads(data)

        if 'error' in result:
            return None, f"Archon MCP error: {result['error'].get('message', 'Unknown error')}"

        task_data = result.get('result')
        if not task_data:
            return None, f"Task {task_id} not found in Archon"

        status = task_data.get('status')
        return status, None

    except ImportError:
        return None, "Required modules not available (graceful degradation)"
    except Exception as e:
        return None, f"Error connecting to Archon MCP: {str(e)}"


def validate_commit_message(commit_message_file: str) -> int:
    """
    Основна функція валідації коміту.

    Args:
        commit_message_file: Шлях до файлу з повідомленням коміту

    Returns:
        0 - коміт дозволено
        1 - коміт заблоковано

    Examples:
        >>> validate_commit_message("/tmp/commit_msg_with_done_task.txt")
        0
        >>> validate_commit_message("/tmp/commit_msg_with_doing_task.txt")
        1
    """
    with open(commit_message_file, 'r', encoding='utf-8') as f:
        commit_message = f.read()

    task_id = extract_task_id_from_commit(commit_message)

    if not task_id:
        print("[OK] No Task ID found in commit message - skipping validation")
        return 0

    print(f"[INFO] Found Task ID: {task_id}")
    print("[INFO] Checking task status in Archon MCP...")

    status, error = check_task_status_in_archon_sync(task_id)

    if error:
        print(f"[WARNING] {error}")
        print("[WARNING] Skipping validation (graceful degradation)")
        return 0

    print(f"[INFO] Task status: {status}")

    if status in ["done", "review"]:
        print("[OK] Task status is valid for commit")
        return 0

    elif status == "todo":
        print("\n" + "="*70)
        print("[ERROR] COMMIT BLOCKED - Task status is 'todo'")
        print("="*70)
        print("\nPROBLEM:")
        print("  Task status is 'todo', which means work hasn't started yet.")
        print("  You MUST update status to 'doing' before making commits.\n")
        print("SOLUTION:")
        print("  1. Update task status to 'doing' in Archon MCP:")
        print(f"     mcp__archon__manage_task(action='update', task_id='{task_id}', status='doing')\n")
        print("  2. After that, retry your commit:")
        print("     git commit\n")
        print("RED LINE #1 VIOLATED:")
        print("  .claude/rules/02_workflow_rules.md -> 'ЧЕРВОНА ЛІНІЯ #1'")
        print("  Work without 'doing' status is FORBIDDEN!\n")
        print("="*70)
        return 1

    elif status == "doing":
        print("\n" + "="*70)
        print("[ERROR] COMMIT BLOCKED - Task status is 'doing'")
        print("="*70)
        print("\nPROBLEM:")
        print("  Task status is 'doing', which means work is not finished yet.")
        print("  You MUST update status to 'done' or 'review' before committing.\n")
        print("SOLUTION:")
        print("  1. If work is complete without issues:")
        print(f"     mcp__archon__manage_task(action='update', task_id='{task_id}', status='done')\n")
        print("  2. If work needs expert review:")
        print(f"     mcp__archon__manage_task(action='update', task_id='{task_id}', status='review')\n")
        print("  3. After updating status, retry your commit:")
        print("     git commit\n")
        print("RED LINE #2 VIOLATED:")
        print("  .claude/rules/02_workflow_rules.md -> 'ЧЕРВОНА ЛІНІЯ #2'")
        print("  Git commit without 'done'/'review' status is FORBIDDEN!\n")
        print("="*70)
        return 1

    else:
        print(f"[WARNING] Unknown status '{status}' - allowing commit")
        return 0


def main():
    """
    Main entry point для використання як pre-commit hook.

    Usage:
        python validate_task_status_before_commit.py .git/COMMIT_EDITMSG

    Returns:
        Exits with code 0 (allow commit) or 1 (block commit)
    """
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python validate_task_status_before_commit.py <commit_message_file>")
        sys.exit(1)

    commit_message_file = sys.argv[1]
    exit_code = validate_commit_message(commit_message_file)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
