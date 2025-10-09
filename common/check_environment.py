# -*- coding: utf-8 -*-
"""
Скрипт для перевірки налаштування середовища розробки.

Перевіряє:
- Кодування Python (stdin, stdout, stderr)
- Наявність PYTHONIOENCODING змінної
- Роботу з Unicode символами
- Налаштування Git

Author: Archon Implementation Engineer
Date: 2025-10-09
"""

import sys
import os
import platform
from pathlib import Path


def check_python_encoding():
    """Перевірити кодування Python."""
    print("[CHECK] Перевірка кодування Python...")

    stdin_enc = sys.stdin.encoding
    stdout_enc = sys.stdout.encoding
    stderr_enc = sys.stderr.encoding

    print(f"  stdin:  {stdin_enc}")
    print(f"  stdout: {stdout_enc}")
    print(f"  stderr: {stderr_enc}")

    # Перевірка що всі використовують UTF-8
    all_utf8 = all(enc and 'utf' in enc.lower()
                   for enc in [stdin_enc, stdout_enc, stderr_enc])

    if all_utf8:
        print("  [OK] Всі потоки використовують UTF-8")
        return True
    else:
        print("  [WARNING] Не всі потоки використовують UTF-8")
        return False


def check_pythonioencoding():
    """Перевірити змінну PYTHONIOENCODING."""
    print("\n[CHECK] Перевірка PYTHONIOENCODING...")

    pythonioencoding = os.environ.get('PYTHONIOENCODING')

    if pythonioencoding:
        print(f"  PYTHONIOENCODING = {pythonioencoding}")
        if 'utf' in pythonioencoding.lower():
            print("  [OK] PYTHONIOENCODING встановлена в UTF-8")
            return True
        else:
            print(f"  [WARNING] PYTHONIOENCODING = {pythonioencoding}, рекомендовано 'utf-8'")
            return False
    else:
        print("  [ERROR] PYTHONIOENCODING не встановлена")
        print("  [HELP] Встановіть змінну: setx PYTHONIOENCODING \"utf-8\"")
        return False


def test_unicode_output():
    """Тест виведення Unicode символів."""
    print("\n[CHECK] Тестування Unicode виводу...")

    try:
        # Тестові рядки
        test_strings = [
            "[OK] Українська: Привіт, світе!",
            "[OK] Русский: Привет, мир!",
            "[OK] English: Hello, world!",
            "[OK] Спецсимволи: [OK] [ERROR] [WARNING]"
        ]

        for test_str in test_strings:
            print(f"  {test_str}")

        print("  [OK] Unicode символи відображаються коректно")
        return True

    except UnicodeEncodeError as e:
        print(f"  [ERROR] Помилка кодування: {e}")
        print("  [HELP] Перевірте налаштування PYTHONIOENCODING")
        return False


def check_git_config():
    """Перевірити налаштування Git."""
    print("\n[CHECK] Перевірка налаштування Git...")

    try:
        import subprocess

        # Перевірка core.hooksPath
        result = subprocess.run(
            ['git', 'config', 'core.hooksPath'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )

        hooks_path = result.stdout.strip()

        if hooks_path:
            print(f"  core.hooksPath = {hooks_path}")
            if hooks_path == '.githooks':
                print("  [OK] Git hooks налаштовані правильно")
                return True
            else:
                print(f"  [WARNING] Очікується '.githooks', знайдено '{hooks_path}'")
                return False
        else:
            print("  [WARNING] core.hooksPath не встановлено")
            print("  [HELP] Запустіть: git config core.hooksPath .githooks")
            return False

    except Exception as e:
        print(f"  [ERROR] Не вдалося перевірити Git: {e}")
        return False


def check_platform_specific():
    """Перевірки специфічні для платформи."""
    system = platform.system()

    print(f"\n[INFO] Платформа: {system}")

    if system == "Windows":
        print("[CHECK] Windows-специфічні перевірки...")

        # Перевірка кодової сторінки консолі
        try:
            import subprocess
            result = subprocess.run(
                ['chcp'],
                capture_output=True,
                text=True,
                shell=True
            )
            print(f"  {result.stdout.strip()}")

            if '65001' in result.stdout:  # UTF-8
                print("  [OK] Консоль використовує UTF-8 (65001)")
                return True
            else:
                print("  [INFO] Консоль не використовує UTF-8")
                print("  [HELP] Виконайте: chcp 65001")
                return False
        except Exception as e:
            print(f"  [ERROR] Не вдалося перевірити кодову сторінку: {e}")
            return False

    return True


def print_summary(results):
    """Вивести підсумок перевірки."""
    print("\n" + "=" * 60)
    print("ПІДСУМОК ПЕРЕВІРКИ СЕРЕДОВИЩА")
    print("=" * 60)

    total = len(results)
    passed = sum(results.values())

    for check_name, result in results.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {check_name}")

    print("=" * 60)
    print(f"РЕЗУЛЬТАТ: {passed}/{total} перевірок пройдено")

    if passed == total:
        print("[SUCCESS] Середовище налаштоване правильно!")
        return 0
    else:
        print("[WARNING] Деякі перевірки не пройдені")
        print("[HELP] Дивіться рекомендації вище для виправлення")
        return 1


def main():
    """Головна функція."""
    print("=" * 60)
    print("ПЕРЕВІРКА СЕРЕДОВИЩА РОЗРОБКИ")
    print("=" * 60)

    results = {
        "Python кодування": check_python_encoding(),
        "PYTHONIOENCODING": check_pythonioencoding(),
        "Unicode вивід": test_unicode_output(),
        "Git налаштування": check_git_config(),
        "Платформа-специфічне": check_platform_specific()
    }

    exit_code = print_summary(results)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
