# Common Utilities for Agent Factory

Спільні утиліти та інструменти для всіх агентів фабрики.

## Модулі

### Script Encoding Validator

Валідатор кодування та стилю Python скриптів. Забезпечує чистий UTF-8 без емодзі.

**Основні функції:**

- `check_file_encoding(file_path)` - Перевірка UTF-8 кодування файлу
- `find_emojis_in_code(file_path)` - Знаходження емодзі в коді
- `check_encoding_declaration(file_path)` - Перевірка декларації кодування
- `validate_script(file_path)` - Повна валідація скрипта
- `validate_directory(directory, recursive=True)` - Валідація директорії
- `fix_file_emojis(file_path, dry_run=True)` - Автоматичне виправлення емодзі
- `fix_directory_emojis(directory, dry_run=True)` - Виправлення емодзі в директорії

**Використання в коді:**

```python
from common.script_encoding_validator import (
    validate_script,
    validate_directory,
    fix_file_emojis,
)

# Валідація одного файлу
is_valid, issues = validate_script(Path("my_script.py"))
if not is_valid:
    for issue in issues:
        print(issue)

# Валідація директорії
results = validate_directory(Path("my_project"))
print(f"Валідних: {len(results['valid'])}/{results['total']}")

# Автоматичне виправлення
fixed = fix_file_emojis(Path("my_script.py"), dry_run=False)
if fixed:
    print("Файл виправлено")
```

**Використання через командний рядок:**

```bash
# Валідація одного файлу
python -m common.script_encoding_validator my_script.py

# Валідація директорії (рекурсивно)
python -m common.script_encoding_validator /path/to/project

# Валідація директорії (без рекурсії)
python -m common.script_encoding_validator /path/to/project --no-recursive

# Автоматичне виправлення (попередній перегляд)
python -m common.script_encoding_validator /path/to/project --fix --dry-run

# Автоматичне виправлення (застосувати зміни)
python -m common.script_encoding_validator /path/to/project --fix

# Показати версію
python -m common.script_encoding_validator --version
```

**Словник замін емодзі:**

```python
from common.script_encoding_validator import EMOJI_REPLACEMENTS

# Доступні заміни:
# ✅ → [OK]
# ❌ → [ERROR]
# ⚠️ → [WARNING]
# 🔍 → [SEARCH]
# 📁 → [DIR]
# 📄 → [FILE]
# 🎯 → [TARGET]
# 🔧 → [TOOL]
# 🚀 → [START]
# 📊 → [REPORT]
# і багато інших...
```

## Інтеграція в workflow

### Pre-commit hook

Створіть файл `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook для валідації кодування

echo "[CHECK] Перевірка кодування Python файлів..."

python -m common.script_encoding_validator .

if [ $? -ne 0 ]; then
    echo "[ERROR] Коміт заблоковано через проблеми з кодуванням"
    echo "[HELP] Виправ проблеми та спробуй знову"
    echo "[HELP] Запусти: python -m common.script_encoding_validator . --fix"
    exit 1
fi

echo "[OK] Всі файли валідні"
exit 0
```

Зробіть його виконуваним:

```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions

Додайте перевірку в `.github/workflows/test.yml`:

```yaml
- name: Validate encoding
  run: |
    python -m common.script_encoding_validator .
```

### Використання в pytest

```python
import pytest
from pathlib import Path
from common.script_encoding_validator import validate_directory

def test_all_files_have_valid_encoding():
    """Перевірити що всі Python файли мають валідне кодування."""
    results = validate_directory(Path("."))

    if results['invalid']:
        pytest.fail(
            f"Знайдено {len(results['invalid'])} файлів з проблемами кодування"
        )
```

## Стандарти кодування

Детальні стандарти кодування для Agent Factory:

**Документація:** [CODING_STANDARDS.md](../CODING_STANDARDS.md)

**Основні правила:**

1. Всі Python файли повинні мати `# -*- coding: utf-8 -*-` на початку
2. Заборонено використовувати емодзі в Python коді
3. Використовувати текстові префікси замість емодзі: `[OK]`, `[ERROR]`, `[WARNING]`
4. Емодзі дозволені тільки в Markdown документації

## Тестування

Запуск тестів валідатора:

```bash
# Всі тести
pytest tests/test_script_encoding_validator.py -v

# Конкретний клас тестів
pytest tests/test_script_encoding_validator.py::TestValidateScript -v

# Конкретний тест
pytest tests/test_script_encoding_validator.py::TestValidateScript::test_valid_script -v
```

**Покриття тестами:**

- 8 класів тестів
- 25+ тестових сценаріїв
- Покриття всіх публічних функцій
- Інтеграційні тести повного workflow

## Підтримка

При виникненні проблем:

1. Запустіть валідатор: `python -m common.script_encoding_validator .`
2. Перевірте вивід на наявність конкретних проблем
3. Виправте проблеми згідно [CODING_STANDARDS.md](../CODING_STANDARDS.md)
4. Повторіть валідацію

Для автоматичного виправлення:

```bash
# Попередній перегляд
python -m common.script_encoding_validator . --fix --dry-run

# Застосувати зміни
python -m common.script_encoding_validator . --fix
```

## Версія

**Поточна версія:** 1.0.0

Перевірити версію:

```bash
python -m common.script_encoding_validator --version
```

---

**Автор:** Archon Implementation Engineer
**Дата:** 2025-10-09
