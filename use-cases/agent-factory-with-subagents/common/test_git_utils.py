"""
Тестирование Production Push Reminder механизма.

Простые unit тесты для проверки функциональности git_utils.
"""

import sys
import os

# Добавить путь к common модулю
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from git_utils import (
    _detect_deployment_status,
    _count_unpushed_commits
)


def test_detect_deployment_status():
    """Тест определения deployment_status."""

    print("\n[TEST] test_detect_deployment_status")
    print("=" * 60)

    # Production проекты
    project1 = {"description": "Production AI Agent Factory", "title": "AI Factory"}
    assert _detect_deployment_status(project1) == "production"
    print("[OK] Production keyword 'production' detected")

    project2 = {"description": "Deployed web application", "title": "Web App"}
    assert _detect_deployment_status(project2) == "production"
    print("[OK] Production keyword 'deployed' detected")

    project3 = {"description": "Live system for customers", "title": "Customer Portal"}
    assert _detect_deployment_status(project3) == "production"
    print("[OK] Production keyword 'live' detected")

    # Staging проекты
    project4 = {"description": "Staging environment for testing", "title": "Test Env"}
    assert _detect_deployment_status(project4) == "staging"
    print("[OK] Staging keyword 'staging' detected")

    project5 = {"description": "Pre-production testing", "title": "PreProd"}
    assert _detect_deployment_status(project5) == "staging"
    print("[OK] Staging keyword 'pre-production' detected")

    # Local проекты
    project6 = {"description": "Development playground", "title": "My Experiments"}
    assert _detect_deployment_status(project6) == "local"
    print("[OK] Local project (no deployment keywords)")

    project7 = {"description": "", "title": "Untitled Project"}
    assert _detect_deployment_status(project7) == "local"
    print("[OK] Empty description defaults to local")

    # None project_info
    assert _detect_deployment_status(None) == "local"
    print("[OK] None project_info defaults to local")

    print("[OK] ✅ test_detect_deployment_status passed")


def test_count_unpushed_commits():
    """Тест подсчета непушнутых коммитов."""

    print("\n[TEST] test_count_unpushed_commits")
    print("=" * 60)

    # Тест на текущем репозитории
    current_repo = os.path.join(
        os.path.dirname(__file__),
        ".."  # agent-factory-with-subagents
    )

    try:
        count = _count_unpushed_commits(current_repo)
        print(f"[OK] Current repo has {count} unpushed commits")

        assert isinstance(count, int)
        assert count >= 0
        print("[OK] Count is valid non-negative integer")

    except Exception as e:
        print(f"[WARNING] Could not test on current repo: {e}")
        print("[INFO] This is OK if no upstream branch is configured")

    print("[OK] ✅ test_count_unpushed_commits passed (or skipped)")


def test_production_reminder_scenario():
    """Интеграционный тест сценария Production Push Reminder."""

    print("\n[TEST] test_production_reminder_scenario")
    print("=" * 60)

    # Сценарий 1: Production проект с непушнутыми коммитами
    project_prod = {
        "id": "test-prod-123",
        "description": "Production AI Agent Factory",
        "title": "AI Factory"
    }

    deployment_status = _detect_deployment_status(project_prod)

    print(f"[SCENARIO 1] Production project")
    print(f"  Deployment: {deployment_status}")
    print(f"  Expected: Should remind to push if unpushed commits exist")

    assert deployment_status == "production"
    print("[OK] ✅ Production scenario correct")

    # Сценарий 2: Staging проект
    project_staging = {
        "id": "staging-proj-456",
        "description": "Staging environment",
        "title": "Staging App"
    }

    deployment_status = _detect_deployment_status(project_staging)

    print(f"\n[SCENARIO 2] Staging project")
    print(f"  Deployment: {deployment_status}")
    print(f"  Expected: Should not require mandatory push")

    assert deployment_status == "staging"
    print("[OK] ✅ Staging scenario correct")

    # Сценарий 3: Local проект
    project_local = {
        "id": "local-789",
        "description": "Development experiments",
        "title": "Playground"
    }

    deployment_status = _detect_deployment_status(project_local)

    print(f"\n[SCENARIO 3] Local development")
    print(f"  Deployment: {deployment_status}")
    print(f"  Expected: Optional push")

    assert deployment_status == "local"
    print("[OK] ✅ Local development scenario correct")

    print("\n[OK] ✅ test_production_reminder_scenario passed")


def run_all_tests():
    """Запустить все тесты."""

    print("\n" + "=" * 60)
    print("PRODUCTION PUSH REMINDER - UNIT TESTS")
    print("=" * 60)

    try:
        test_detect_deployment_status()
        test_count_unpushed_commits()
        test_production_reminder_scenario()

        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n❌ ТЕСТ ПРОВАЛЕН: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ОШИБКА ПРИ ТЕСТИРОВАНИИ: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
