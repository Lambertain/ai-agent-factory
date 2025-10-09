# -*- coding: utf-8 -*-
"""
Валідатор кодування та стилю Python скриптів.
Забезпечує чистий UTF-8 без емодзі за замовчуванням.

Цей модуль перевіряє Python файли на:
- Правильність UTF-8 кодування
- Наявність емодзі в коді
- Наявність декларації кодування

Author: Archon Implementation Engineer
Date: 2025-10-09
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

# Regex для виявлення емодзі (всі Unicode блоки емодзі)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # емоції
    "\U0001F300-\U0001F5FF"  # символи та піктограми
    "\U0001F680-\U0001F6FF"  # транспорт
    "\U0001F1E0-\U0001F1FF"  # прапори
    "\U00002702-\U000027B0"  # допоміжні символи
    "\U000024C2-\U0001F251"  # додаткові символи
    "]+",
    flags=re.UNICODE
)

# Рекомендовані заміни емодзі на текстові альтернативи
EMOJI_REPLACEMENTS = {
    "\u2705": "[OK]",
    "\u274c": "[ERROR]",
    "\u26a0\ufe0f": "[WARNING]",
    "\u26a0": "[WARNING]",
    "\ud83d\udd0d": "[SEARCH]",
    "\ud83d\udcc1": "[DIR]",
    "\ud83d\udcc4": "[FILE]",
    "\ud83c\udfaf": "[TARGET]",
    "\ud83d\udd27": "[TOOL]",
    "\ud83d\ude80": "[START]",
    "\ud83d\udcca": "[REPORT]",
    "\ud83d\udcc5": "[DATE]",
    "\ud83d\udd52": "[TIME]",
    "\u2139\ufe0f": "[INFO]",
    "\u2139": "[INFO]",
    "\ud83d\udd34": "[CRITICAL]",
    "\ud83d\udd35": "[DEBUG]",
}


def check_file_encoding(file_path: Path) -> Tuple[bool, str]:
    """
    Перевірити кодування файлу.

    Спробує прочитати файл як UTF-8. Якщо не вдається, спробує визначити
    фактичне кодування за допомогою chardet.

    Args:
        file_path: Шлях до файлу для перевірки

    Returns:
        Tuple[bool, str]: (чи є файл UTF-8, виявлене кодування)
            - True, "utf-8" якщо файл коректний UTF-8
            - False, "detected_encoding" якщо файл використовує інше кодування

    Example:
        >>> is_utf8, encoding = check_file_encoding(Path("script.py"))
        >>> if not is_utf8:
        ...     print(f"Файл використовує {encoding} замість UTF-8")
    """
    try:
        # Спроба прочитати як UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True, "utf-8"
    except UnicodeDecodeError:
        # Якщо не вдалося, визначаємо реальне кодування
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                detected_encoding = result.get('encoding', 'unknown')
                return False, detected_encoding
        except ImportError:
            # Якщо chardet не встановлено, повертаємо "unknown"
            return False, "unknown (chardet не встановлено)"
        except Exception as e:
            return False, f"error: {str(e)}"


def check_bom(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Перевірити наявність BOM (Byte Order Mark) у файлі.

    Args:
        file_path: Шлях до файлу для перевірки

    Returns:
        Tuple[bool, Optional[str]]: (чи є BOM, тип BOM якщо є)
            - False, None якщо BOM відсутній
            - True, "UTF-8 BOM" якщо присутній UTF-8 BOM
            - True, "UTF-16 LE BOM" якщо присутній UTF-16 LE BOM
            - True, "UTF-16 BE BOM" якщо присутній UTF-16 BE BOM

    Example:
        >>> has_bom, bom_type = check_bom(Path("script.py"))
        >>> if has_bom:
        ...     print(f"Файл містить {bom_type}")
    """
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(4)

        # Перевірка різних типів BOM
        if first_bytes.startswith(b'\xef\xbb\xbf'):
            return True, "UTF-8 BOM"
        elif first_bytes.startswith(b'\xff\xfe'):
            return True, "UTF-16 LE BOM"
        elif first_bytes.startswith(b'\xfe\xff'):
            return True, "UTF-16 BE BOM"

        return False, None

    except Exception as e:
        print(f"[ERROR] Помилка перевірки BOM {file_path}: {e}")
        return False, None


def remove_bom(file_path: Path, dry_run: bool = True) -> bool:
    """
    Видалити BOM (Byte Order Mark) з файлу.

    Args:
        file_path: Шлях до файлу
        dry_run: Якщо True, тільки показати що буде змінено (не зберігати)

    Returns:
        bool: True якщо BOM було видалено, False якщо BOM не було

    Example:
        >>> # Попередній перегляд
        >>> if remove_bom(Path("script.py"), dry_run=True):
        ...     # Застосувати зміни
        ...     remove_bom(Path("script.py"), dry_run=False)
    """
    has_bom, bom_type = check_bom(file_path)

    if not has_bom:
        return False

    try:
        # Читаємо файл як бінарні дані
        with open(file_path, 'rb') as f:
            content = f.read()

        # Видаляємо BOM в залежності від типу
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]  # UTF-8 BOM - 3 байти
        elif content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):
            content = content[2:]  # UTF-16 BOM - 2 байти

        if not dry_run:
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"[OK] Видалено {bom_type}: {file_path}")
        else:
            print(f"[DRY-RUN] Буде видалено {bom_type}: {file_path}")

        return True

    except Exception as e:
        print(f"[ERROR] Помилка видалення BOM {file_path}: {e}")
        return False


def find_emojis_in_code(file_path: Path) -> List[Tuple[int, str]]:
    """
    Знайти всі емодзі в Python коді.

    Сканує файл рядок за рядком і виявляє наявність емодзі символів.

    Args:
        file_path: Шлях до Python файлу

    Returns:
        List[Tuple[int, str]]: Список кортежів (номер_рядка, вміст_рядка) з емодзі
            - Номер рядка починається з 1
            - Вміст рядка - це повний рядок без пробілів на початку та кінці

    Example:
        >>> emojis = find_emojis_in_code(Path("script.py"))
        >>> for line_num, line_content in emojis:
        ...     print(f"Рядок {line_num}: {line_content}")
    """
    emojis_found = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if EMOJI_PATTERN.search(line):
                    emojis_found.append((line_num, line.strip()))
    except UnicodeDecodeError:
        print(f"[WARN] Не вдалося прочитати {file_path} як UTF-8")
    except Exception as e:
        print(f"[ERROR] Помилка читання файлу {file_path}: {e}")

    return emojis_found


def check_encoding_declaration(file_path: Path) -> bool:
    """
    Перевірити наявність декларації кодування в файлі.

    Перевіряє перші 3 рядки файлу на наявність рядка з 'coding' та 'utf-8'.

    Args:
        file_path: Шлях до Python файлу

    Returns:
        bool: True якщо декларація кодування присутня, False якщо ні

    Example:
        >>> has_declaration = check_encoding_declaration(Path("script.py"))
        >>> if not has_declaration:
        ...     print("Рекомендується додати: # -*- coding: utf-8 -*-")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = [f.readline() for _ in range(3)]
            has_declaration = any(
                'coding' in line and 'utf-8' in line
                for line in first_lines
            )
            return has_declaration
    except Exception:
        return False


def validate_script(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Повна валідація Python скрипта.

    Виконує комплексну перевірку:
    1. Кодування UTF-8
    2. Наявність BOM (Byte Order Mark)
    3. Наявність емодзі в коді
    4. Наявність декларації кодування

    Args:
        file_path: Шлях до Python файлу

    Returns:
        Tuple[bool, List[str]]: (чи є файл валідним, список проблем)
            - True, [] якщо всі перевірки пройшли
            - False, ["проблема 1", "проблема 2", ...] якщо є проблеми

    Example:
        >>> is_valid, issues = validate_script(Path("script.py"))
        >>> if not is_valid:
        ...     for issue in issues:
        ...         print(issue)
    """
    issues = []

    # Перевірка 1: Кодування UTF-8
    is_utf8, encoding = check_file_encoding(file_path)
    if not is_utf8:
        issues.append(f"[ERROR] Неправильне кодування: {encoding} (потрібно UTF-8)")

    # Перевірка 2: Наявність BOM
    has_bom, bom_type = check_bom(file_path)
    if has_bom:
        issues.append(f"[WARNING] Файл містить {bom_type}, рекомендується UTF-8 без BOM")

    # Перевірка 3: Наявність емодзі
    emojis = find_emojis_in_code(file_path)
    if emojis:
        issues.append(f"[ERROR] Знайдено {len(emojis)} емодзі в коді:")
        # Показуємо перші 5 емодзі
        for line_num, line_content in emojis[:5]:
            issues.append(f"   Рядок {line_num}: {line_content}")
        if len(emojis) > 5:
            issues.append(f"   ... та ще {len(emojis) - 5} емодзі")

    # Перевірка 4: Наявність декларації кодування
    has_declaration = check_encoding_declaration(file_path)
    if not has_declaration:
        issues.append("[WARNING] Рекомендується додати: # -*- coding: utf-8 -*- на початок файлу")

    return len(issues) == 0, issues


def validate_directory(directory: Path, recursive: bool = True) -> Dict[str, Any]:
    """
    Валідація всіх Python файлів у директорії.

    Рекурсивно (або не рекурсивно) сканує директорію та перевіряє всі .py файли.

    Args:
        directory: Шлях до директорії
        recursive: Якщо True, сканувати підпапки рекурсивно

    Returns:
        Dict[str, Any]: Результати валідації:
            {
                'valid': [список валідних файлів],
                'invalid': {файл: [список_проблем]},
                'total': загальна_кількість_файлів
            }

    Example:
        >>> results = validate_directory(Path("/project"))
        >>> print(f"Валідних: {len(results['valid'])}/{results['total']}")
    """
    results = {
        'valid': [],
        'invalid': {},
        'total': 0
    }

    pattern = "**/*.py" if recursive else "*.py"

    for py_file in directory.glob(pattern):
        results['total'] += 1
        is_valid, issues = validate_script(py_file)

        if is_valid:
            results['valid'].append(str(py_file))
        else:
            results['invalid'][str(py_file)] = issues

    return results


def print_validation_report(results: Dict[str, Any]) -> None:
    """
    Вивести звіт про валідацію у консоль.

    Форматований вивід результатів валідації з кольорами та зручною структурою.

    Args:
        results: Результати валідації з validate_directory()

    Example:
        >>> results = validate_directory(Path("/project"))
        >>> print_validation_report(results)
    """
    print("=" * 70)
    print("[REPORT] ЗВІТ ВАЛІДАЦІЇ КОДУВАННЯ СКРИПТІВ")
    print("=" * 70)
    print(f"\n[OK] Валідних файлів: {len(results['valid'])}")
    print(f"[ERROR] Невалідних файлів: {len(results['invalid'])}")
    print(f"[INFO] Всього перевірено: {results['total']}")

    if results['invalid']:
        print("\n" + "=" * 70)
        print("ПРОБЛЕМНІ ФАЙЛИ:")
        print("=" * 70)

        for file_path, issues in results['invalid'].items():
            print(f"\n[FILE] {file_path}")
            for issue in issues:
                print(f"  {issue}")


def fix_file_emojis(file_path: Path, dry_run: bool = True) -> bool:
    """
    Замінити емодзі у файлі на текстові альтернативи.

    Автоматично виправляє емодзі, замінюючи їх на читабельні текстові префікси.

    Args:
        file_path: Шлях до файлу
        dry_run: Якщо True, тільки показати що буде змінено (не зберігати)

    Returns:
        bool: True якщо були зміни, False якщо змін не було

    Example:
        >>> # Спочатку перегляд змін
        >>> changed = fix_file_emojis(Path("script.py"), dry_run=True)
        >>> # Потім застосування
        >>> if changed:
        ...     fix_file_emojis(Path("script.py"), dry_run=False)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Замінюємо відомі емодзі
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)

        # Видаляємо решту емодзі
        content = EMOJI_PATTERN.sub('[EMOJI]', content)

        if content != original_content:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] Виправлено: {file_path}")
            else:
                print(f"[DRY-RUN] Буде виправлено: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"[ERROR] Помилка обробки {file_path}: {e}")
        return False


def fix_directory_emojis(directory: Path, dry_run: bool = True) -> int:
    """
    Виправити емодзі у всіх Python файлах директорії.

    Args:
        directory: Шлях до директорії
        dry_run: Якщо True, тільки показати що буде змінено

    Returns:
        int: Кількість виправлених файлів

    Example:
        >>> # Попередній перегляд
        >>> count = fix_directory_emojis(Path("/project"), dry_run=True)
        >>> print(f"Буде виправлено {count} файлів")
        >>> # Застосування змін
        >>> count = fix_directory_emojis(Path("/project"), dry_run=False)
    """
    fixed_count = 0

    for py_file in directory.glob("**/*.py"):
        if fix_file_emojis(py_file, dry_run=dry_run):
            fixed_count += 1

    return fixed_count


def main():
    """
    Головна функція командного рядка.

    Приклади використання:
        python script_encoding_validator.py /path/to/file.py
        python script_encoding_validator.py /path/to/directory
        python script_encoding_validator.py /path/to/directory --fix
        python script_encoding_validator.py /path/to/directory --fix --dry-run
        python script_encoding_validator.py --version
    """
    parser = argparse.ArgumentParser(
        description="Валідатор кодування та емодзі в Python скриптах"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        'path',
        type=str,
        nargs='?',
        default='.',
        help='Шлях до файлу або директорії (за замовчуванням: поточна директорія)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Автоматично виправити емодзі'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Режим попереднього перегляду (не зберігати зміни)'
    )
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Не сканувати підпапки рекурсивно'
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"[ERROR] Шлях не існує: {path}")
        sys.exit(1)

    # Режим виправлення
    if args.fix:
        if path.is_file():
            fixed = fix_file_emojis(path, dry_run=args.dry_run)
            if fixed:
                mode = "Буде виправлено" if args.dry_run else "Виправлено"
                print(f"[OK] {mode}: {path}")
            else:
                print(f"[INFO] Немає змін: {path}")
        else:
            mode = "Буде виправлено" if args.dry_run else "Виправлено"
            print(f"[INFO] Сканування файлів для виправлення...")
            fixed_count = fix_directory_emojis(path, dry_run=args.dry_run)
            print(f"[DONE] {mode} файлів: {fixed_count}")

        sys.exit(0)

    # Режим валідації
    if path.is_file():
        is_valid, issues = validate_script(path)
        if is_valid:
            print(f"[OK] {path} - валідний")
            sys.exit(0)
        else:
            print(f"[ERROR] {path} - проблеми:")
            for issue in issues:
                print(f"  {issue}")
            sys.exit(1)
    else:
        results = validate_directory(path, recursive=not args.no_recursive)
        print_validation_report(results)

        # Код виходу: 0 якщо всі файли валідні, 1 якщо є проблеми
        sys.exit(0 if not results['invalid'] else 1)


if __name__ == "__main__":
    main()
