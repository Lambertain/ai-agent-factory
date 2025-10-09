# -*- coding: utf-8 -*-
"""
Тести для валідатора кодування скриптів.

Тестує всі функції модуля script_encoding_validator:
- Перевірку кодування файлів
- Виявлення емодзі
- Валідацію скриптів
- Автоматичне виправлення

Author: Archon Implementation Engineer
Date: 2025-10-09
"""

import pytest
import tempfile
from pathlib import Path
from common.script_encoding_validator import (
    check_file_encoding,
    find_emojis_in_code,
    check_encoding_declaration,
    validate_script,
    validate_directory,
    fix_file_emojis,
    fix_directory_emojis,
    EMOJI_REPLACEMENTS,
)


class TestCheckFileEncoding:
    """Тести для функції check_file_encoding."""

    def test_valid_utf8_file(self):
        """Тест: файл з коректним UTF-8 кодуванням."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("# Тестовий файл з українським текстом\n")
            f.write("print('Привіт світ')\n")
            temp_path = Path(f.name)

        try:
            is_utf8, encoding = check_file_encoding(temp_path)
            assert is_utf8 is True
            assert encoding == "utf-8"
        finally:
            temp_path.unlink()

    def test_file_with_emoji(self):
        """Тест: файл з емодзі (але все ще UTF-8)."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\u2705 Success')\n")
            temp_path = Path(f.name)

        try:
            is_utf8, encoding = check_file_encoding(temp_path)
            # Файл все ще UTF-8, просто містить емодзі
            assert is_utf8 is True
            assert encoding == "utf-8"
        finally:
            temp_path.unlink()


class TestFindEmojisInCode:
    """Тести для функції find_emojis_in_code."""

    def test_no_emojis(self):
        """Тест: файл без емодзі."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('[OK] Success')\n")
            f.write("logger.info('[INFO] Processing')\n")
            temp_path = Path(f.name)

        try:
            emojis = find_emojis_in_code(temp_path)
            assert len(emojis) == 0
        finally:
            temp_path.unlink()

    def test_with_emojis(self):
        """Тест: файл з емодзі."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\u2705 Success')\n")  # Рядок 2
            f.write("print('Normal line')\n")  # Рядок 3
            f.write("logger.info('\u274c Error')\n")  # Рядок 4
            temp_path = Path(f.name)

        try:
            emojis = find_emojis_in_code(temp_path)
            assert len(emojis) == 2
            # Перевіряємо номери рядків
            line_numbers = [line_num for line_num, _ in emojis]
            assert 2 in line_numbers
            assert 4 in line_numbers
        finally:
            temp_path.unlink()

    def test_multiple_emojis_per_line(self):
        """Тест: кілька емодзі в одному рядку."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("print('\u2705 Success \ud83c\udfaf Target \ud83d\ude80 Launch')\n")
            temp_path = Path(f.name)

        try:
            emojis = find_emojis_in_code(temp_path)
            # Рядок з кількома емодзі все одно рахується як 1 проблемний рядок
            assert len(emojis) == 1
            assert '\u2705' in emojis[0][1]  # Перевіряємо що емодзі є в вмісті
        finally:
            temp_path.unlink()


class TestCheckEncodingDeclaration:
    """Тести для функції check_encoding_declaration."""

    def test_has_declaration(self):
        """Тест: файл з декларацією кодування."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('test')\n")
            temp_path = Path(f.name)

        try:
            has_declaration = check_encoding_declaration(temp_path)
            assert has_declaration is True
        finally:
            temp_path.unlink()

    def test_no_declaration(self):
        """Тест: файл без декларації кодування."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("print('test')\n")
            temp_path = Path(f.name)

        try:
            has_declaration = check_encoding_declaration(temp_path)
            assert has_declaration is False
        finally:
            temp_path.unlink()

    def test_declaration_on_second_line(self):
        """Тест: декларація на другому рядку (теж валідно)."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('test')\n")
            temp_path = Path(f.name)

        try:
            has_declaration = check_encoding_declaration(temp_path)
            assert has_declaration is True
        finally:
            temp_path.unlink()


class TestValidateScript:
    """Тести для функції validate_script."""

    def test_valid_script(self):
        """Тест: повністю валідний скрипт."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("\"\"\"\n")
            f.write("Тестовий модуль.\n")
            f.write("\"\"\"\n")
            f.write("print('[OK] Success')\n")
            temp_path = Path(f.name)

        try:
            is_valid, issues = validate_script(temp_path)
            assert is_valid is True
            assert len(issues) == 0
        finally:
            temp_path.unlink()

    def test_script_with_emojis(self):
        """Тест: скрипт з емодзі."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\u2705 Success')\n")
            temp_path = Path(f.name)

        try:
            is_valid, issues = validate_script(temp_path)
            assert is_valid is False
            assert len(issues) > 0
            # Перевіряємо що є повідомлення про емодзі
            assert any("[ERROR]" in issue and "емодзі" in issue for issue in issues)
        finally:
            temp_path.unlink()

    def test_script_without_declaration(self):
        """Тест: скрипт без декларації кодування."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("print('[OK] Success')\n")
            temp_path = Path(f.name)

        try:
            is_valid, issues = validate_script(temp_path)
            assert is_valid is False
            # Має бути попередження про відсутність декларації
            assert any("[WARNING]" in issue for issue in issues)
        finally:
            temp_path.unlink()


class TestValidateDirectory:
    """Тести для функції validate_directory."""

    def test_empty_directory(self):
        """Тест: порожня директорія."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            results = validate_directory(temp_path)

            assert results['total'] == 0
            assert len(results['valid']) == 0
            assert len(results['invalid']) == 0

    def test_directory_with_valid_files(self):
        """Тест: директорія з валідними файлами."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Створюємо 3 валідних файли
            for i in range(3):
                file_path = temp_path / f"test{i}.py"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# -*- coding: utf-8 -*-\n")
                    f.write(f"print('[OK] Test {i}')\n")

            results = validate_directory(temp_path, recursive=False)

            assert results['total'] == 3
            assert len(results['valid']) == 3
            assert len(results['invalid']) == 0

    def test_directory_with_invalid_files(self):
        """Тест: директорія з невалідними файлами."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Валідний файл
            valid_path = temp_path / "valid.py"
            with open(valid_path, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("print('[OK] Valid')\n")

            # Невалідний файл (емодзі)
            invalid_path = temp_path / "invalid.py"
            with open(invalid_path, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("print('\u2705 Invalid')\n")

            results = validate_directory(temp_path, recursive=False)

            assert results['total'] == 2
            assert len(results['valid']) == 1
            assert len(results['invalid']) == 1


class TestFixFileEmojis:
    """Тести для функції fix_file_emojis."""

    def test_fix_known_emojis(self):
        """Тест: заміна відомих емодзі."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\u2705 Success')\n")
            f.write("print('\u274c Error')\n")
            temp_path = Path(f.name)

        try:
            # Спочатку dry-run
            changed = fix_file_emojis(temp_path, dry_run=True)
            assert changed is True

            # Застосувати зміни
            changed = fix_file_emojis(temp_path, dry_run=False)
            assert changed is True

            # Перевірити що емодзі замінено
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '[OK]' in content
                assert '[ERROR]' in content
                assert '\u2705' not in content
                assert '\u274c' not in content

        finally:
            temp_path.unlink()

    def test_fix_unknown_emojis(self):
        """Тест: заміна невідомих емодзі на [EMOJI]."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\ud83e\udd84 Unicorn')\n")  # Невідомий емодзі
            temp_path = Path(f.name)

        try:
            changed = fix_file_emojis(temp_path, dry_run=False)
            assert changed is True

            # Перевірити що емодзі замінено
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '[EMOJI]' in content
                assert '\ud83e\udd84' not in content

        finally:
            temp_path.unlink()

    def test_no_changes_needed(self):
        """Тест: файл без емодзі не потребує змін."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('[OK] Success')\n")
            temp_path = Path(f.name)

        try:
            changed = fix_file_emojis(temp_path, dry_run=False)
            assert changed is False
        finally:
            temp_path.unlink()


class TestFixDirectoryEmojis:
    """Тести для функції fix_directory_emojis."""

    def test_fix_directory_with_emojis(self):
        """Тест: виправлення емодзі в директорії."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Створюємо 3 файли з емодзі
            for i in range(3):
                file_path = temp_path / f"test{i}.py"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# -*- coding: utf-8 -*-\n")
                    f.write(f"print('\u2705 Test {i}')\n")

            # Виправляємо всі файли
            fixed_count = fix_directory_emojis(temp_path, dry_run=False)
            assert fixed_count == 3

            # Перевіряємо що всі файли виправлено
            for i in range(3):
                file_path = temp_path / f"test{i}.py"
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert '[OK]' in content
                    assert '\u2705' not in content

    def test_fix_directory_dry_run(self):
        """Тест: dry-run режим для директорії."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Створюємо файл з емодзі
            file_path = temp_path / "test.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("print('\u2705 Success')\n")

            # Dry-run не повинен змінювати файли
            fixed_count = fix_directory_emojis(temp_path, dry_run=True)
            assert fixed_count == 1

            # Перевіряємо що файл не змінився
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '\u2705' in content  # Емодзі все ще є

    def test_fix_directory_no_changes(self):
        """Тест: директорія без емодзі."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Створюємо файл без емодзі
            file_path = temp_path / "test.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("print('[OK] Success')\n")

            # Немає файлів для виправлення
            fixed_count = fix_directory_emojis(temp_path, dry_run=False)
            assert fixed_count == 0

    def test_fix_directory_recursive(self):
        """Тест: рекурсивне виправлення вкладених директорій."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Створюємо вкладену структуру
            subdir = temp_path / "subdir"
            subdir.mkdir()

            # Файл в корені
            (temp_path / "root.py").write_text("# -*- coding: utf-8 -*-\nprint('\u2705 Root')\n", encoding='utf-8')

            # Файл у підпапці
            (subdir / "nested.py").write_text("# -*- coding: utf-8 -*-\nprint('\u274c Nested')\n", encoding='utf-8')

            # Виправляємо рекурсивно
            fixed_count = fix_directory_emojis(temp_path, dry_run=False)
            assert fixed_count == 2

            # Перевіряємо обидва файли
            assert '[OK]' in (temp_path / "root.py").read_text(encoding='utf-8')
            assert '[ERROR]' in (subdir / "nested.py").read_text(encoding='utf-8')


class TestEmojiReplacements:
    """Тести для словника EMOJI_REPLACEMENTS."""

    def test_replacements_dict_exists(self):
        """Тест: словник замін існує."""
        assert EMOJI_REPLACEMENTS is not None
        assert len(EMOJI_REPLACEMENTS) > 0

    def test_common_emojis_present(self):
        """Тест: основні емодзі присутні в словнику."""
        assert '\u2705' in EMOJI_REPLACEMENTS  # OK
        assert '\u274c' in EMOJI_REPLACEMENTS  # ERROR
        assert '\u26a0\ufe0f' in EMOJI_REPLACEMENTS or '\u26a0' in EMOJI_REPLACEMENTS  # WARNING

    def test_replacements_are_brackets(self):
        """Тест: всі заміни у форматі [TEXT]."""
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            assert replacement.startswith('[')
            assert replacement.endswith(']')
            # Всередині квадратних дужок тільки великі літери та цифри
            inner = replacement[1:-1]
            assert inner.isupper() or inner.isdigit()


# Інтеграційні тести
class TestIntegration:
    """Інтеграційні тести для повного workflow."""

    def test_full_workflow_validation_and_fix(self):
        """Тест: повний цикл - валідація → виправлення → повторна валідація."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write("print('\u2705 Success')\n")
            f.write("print('\u274c Error')\n")
            temp_path = Path(f.name)

        try:
            # Крок 1: Валідація (має знайти проблеми)
            is_valid, issues = validate_script(temp_path)
            assert is_valid is False
            assert len(issues) > 0

            # Крок 2: Виправлення
            fixed = fix_file_emojis(temp_path, dry_run=False)
            assert fixed is True

            # Крок 3: Повторна валідація (має бути валідним)
            is_valid, issues = validate_script(temp_path)
            assert is_valid is True
            assert len(issues) == 0

        finally:
            temp_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
