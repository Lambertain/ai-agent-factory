# Стандарти кодування для Agent Factory

## Критично важливо: UTF-8 та заборона емодзі

### Проблема

Використання Unicode емодзі в Python скриптах призводить до:
- Проблем з кодуванням при виконанні
- Помилок при читанні файлів на різних системах
- Необхідності переробляти код по 4+ рази
- Нестабільної поведінки print() функцій

### Рішення

**ОБОВ'ЯЗКОВІ ПРАВИЛА ДЛЯ PYTHON СКРИПТІВ:**

## 1. Тільки UTF-8 кодування

**Кожен Python файл повинен починатися з:**

```python
# -*- coding: utf-8 -*-
"""
Опис модуля російською мовою.
"""
```

**Правила:**
- ЗАВЖДИ додавай цей рядок на початку кожного .py файлу
- НІКОЛИ не використовуй інші кодування (cp1251, latin-1, тощо)
- Використовуй тільки UTF-8 без BOM

## 2. Заборона емодзі за замовчуванням

### Заборонено використовувати емодзі в:

```python
# НЕПРАВИЛЬНО - НЕ ВИКОРИСТОВУВАТИ В КОДІ
print("\u2705 Успішно")
print("\u274c Помилка")
print("\ud83c\udfaf Задача виконана")
logger.info("\ud83d\udd0d Пошук файлів...")
```

### Правильно - чистий текст:

```python
# ПРАВИЛЬНО - ЧИСТИЙ ТЕКСТ
print("[OK] Успішно")
print("[ERROR] Помилка")
print("[DONE] Задача виконана")
logger.info("[SEARCH] Пошук файлів...")
```

## 3. Рекомендовані текстові префікси

Замість емодзі використовуй текстові префікси:

| Емодзі | Текстова альтернатива | Коли використовувати |
|--------|----------------------|---------------------|
| \u2705 | `[OK]` або `[SUCCESS]` | Успішне виконання |
| \u274c | `[ERROR]` або `[FAIL]` | Помилка |
| \u26a0\ufe0f | `[WARNING]` або `[WARN]` | Попередження |
| \ud83d\udd0d | `[SEARCH]` або `[FIND]` | Операції пошуку |
| \ud83d\udcc1 | `[DIR]` або `[FOLDER]` | Робота з директоріями |
| \ud83d\udcc4 | `[FILE]` | Робота з файлами |
| \ud83c\udfaf | `[TARGET]` або `[GOAL]` | Цілі та таргети |
| \ud83d\udd27 | `[TOOL]` або `[CONFIG]` | Конфігурація та інструменти |
| \ud83d\ude80 | `[START]` або `[LAUNCH]` | Старт процесів |
| \ud83d\udcca | `[REPORT]` або `[STATS]` | Звіти та статистика |
| \u2139\ufe0f | `[INFO]` | Інформація |
| \ud83d\udd34 | `[CRITICAL]` | Критичні проблеми |
| \ud83d\udd35 | `[DEBUG]` | Налагодження |

## 4. Коли емодзі дозволені

Емодзі можна використовувати ТІЛЬКИ в:

### Дозволено:
- \u2705 Markdown документації (README.md, CLAUDE.md, документи знань)
- \u2705 Коментарях для розробників (не в runtime коді)
- \u2705 Коли користувач ЯВНО запросив емодзі

### Заборонено:
- \u274c У print() функціях
- \u274c У logger повідомленнях
- \u274c У error messages
- \u274c У docstrings функцій
- \u274c У назвах змінних/функцій/класів

## 5. Приклади правильного коду

### Правильний модуль:

```python
# -*- coding: utf-8 -*-
"""
Модуль для роботи з агентами.
Всі рядки в UTF-8, без емодзі в runtime коді.

Author: Archon Implementation Engineer
Date: 2025-10-09
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def process_task(task_id: str) -> bool:
    """
    Обробити задачу.

    Args:
        task_id: Ідентифікатор задачі

    Returns:
        bool: True якщо успішно, False якщо помилка

    Example:
        >>> result = process_task("task-123")
        >>> if result:
        ...     print("[OK] Задача виконана")
    """
    try:
        logger.info(f"[START] Обробка задачі {task_id}")

        # Ваша логіка тут
        result = do_something()

        if result:
            logger.info(f"[OK] Задача {task_id} виконана")
            return True
        else:
            logger.warning(f"[WARN] Задача {task_id} повернула порожній результат")
            return False

    except Exception as e:
        logger.error(f"[ERROR] Помилка при обробці задачі {task_id}: {e}")
        return False


# У print для користувача - також без емодзі
print("[INFO] Програма запущена")
print("[DONE] Всі задачі оброблені")
```

### Правильний logging:

```python
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Правильні log повідомлення
logger.debug("[DEBUG] Деталі виконання")
logger.info("[INFO] Загальна інформація")
logger.warning("[WARN] Попередження")
logger.error("[ERROR] Помилка виконання")
logger.critical("[CRITICAL] Критична помилка")
```

### Правильна обробка помилок:

```python
def safe_operation():
    """Операція з правильною обробкою помилок."""
    try:
        # Код операції
        result = risky_operation()
        print("[OK] Операція виконана успішно")
        return result

    except ValueError as e:
        print(f"[ERROR] Помилка значення: {e}")
        return None

    except Exception as e:
        print(f"[CRITICAL] Неочікувана помилка: {e}")
        raise
```

## 6. Валідація перед коммітом

### Автоматична перевірка:

```python
# Запускати перед кожним git commit
from common.script_encoding_validator import validate_directory

results = validate_directory(Path("."))
if results['invalid']:
    print("[ERROR] Знайдено проблеми з кодуванням!")
    # НЕ комітити до виправлення
```

### Командний рядок:

```bash
# Перевірка одного файлу
python common/script_encoding_validator.py my_script.py

# Перевірка директорії
python common/script_encoding_validator.py /path/to/project

# Автоматичне виправлення (попередній перегляд)
python common/script_encoding_validator.py /path/to/project --fix --dry-run

# Автоматичне виправлення (застосувати)
python common/script_encoding_validator.py /path/to/project --fix
```

## 7. Інтеграція в workflow

### Pre-commit hook:

Створи файл `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook для валідації кодування

echo "[CHECK] Перевірка кодування Python файлів..."

python common/script_encoding_validator.py .

if [ $? -ne 0 ]; then
    echo "[ERROR] Коміт заблоковано через проблеми з кодуванням"
    echo "[HELP] Виправ проблеми та спробуй знову"
    echo "[HELP] Запусти: python common/script_encoding_validator.py ."
    exit 1
fi

echo "[OK] Всі файли валідні"
exit 0
```

Зроби його виконуваним:

```bash
chmod +x .git/hooks/pre-commit
```

## 8. Виправлення існуючого коду

### Автоматичне виправлення:

```bash
# Попередній перегляд змін
python common/script_encoding_validator.py . --fix --dry-run

# Застосувати зміни
python common/script_encoding_validator.py . --fix
```

### Ручне виправлення:

1. Відкрий файл в редакторі
2. Заміни емодзі на текстові префікси згідно таблиці вище
3. Додай `# -*- coding: utf-8 -*-` на початок файлу
4. Збережи файл в UTF-8 кодуванні
5. Запусти валідатор для перевірки

## 9. Виключення з правил

Дозволено використовувати емодзі в:

- **Markdown файлах** (README.md, knowledge bases, документація)
- **Git commit messages** (для кращої читабельності історії)
- **Відповідях користувачу в чаті** (але НЕ в runtime коді)

НЕ дозволено в:

- **Production коді** (будь-який .py файл що виконується)
- **Logger повідомленнях** (все що йде в логи)
- **Error messages** (що можуть попасти в логи)

## 10. Чому це важливо

### Проблеми без цих правил:

1. **Кодування**: Різні системи можуть інтерпретувати емодзі по-різному
2. **Логи**: Емодзі в логах створюють проблеми з пошуком та аналізом
3. **Автоматизація**: Скрипти можуть зламатися через Unicode символи
4. **Переносимість**: Код може не працювати на Windows/Linux/Mac однаково
5. **Час розробки**: 4+ рази переробляти код через проблеми з емодзі

### Переваги цих правил:

1. \u2705 Стабільне кодування на всіх платформах
2. \u2705 Передбачувана поведінка print() та logger
3. \u2705 Легкий пошук в логах (grep "[ERROR]" замість grep "\u274c")
4. \u2705 Швидша розробка (менше помилок з кодуванням)
5. \u2705 Професійний вигляд коду

## 11. Налаштування середовища для Windows

### Проблема з кодуванням в Windows консолі

Windows консоль за замовчуванням використовує кодування cp1251 (кирилиця) замість UTF-8, що призводить до помилок при виведенні Unicode символів.

### Рішення: Глобальна змінна PYTHONIOENCODING

**Встановлення змінної середовища:**

```powershell
# Windows PowerShell (з правами адміністратора)
setx PYTHONIOENCODING "utf-8"

# Або додати вручну через System Properties:
# Control Panel → System → Advanced System Settings
# → Environment Variables → New (User variable)
# Variable name: PYTHONIOENCODING
# Variable value: utf-8
```

**ВАЖЛИВО:** Після встановлення змінної потрібно:
1. Закрити всі відкриті термінали (PowerShell, CMD, Git Bash)
2. Відкрити новий термінал
3. Перевірити що змінна встановлена: `echo $env:PYTHONIOENCODING` (PowerShell)

### Перевірка налаштування:

```python
# -*- coding: utf-8 -*-
"""Тест налаштування кодування."""

import sys
import os

print("[INFO] Перевірка налаштування кодування:")
print(f"  stdin:  {sys.stdin.encoding}")
print(f"  stdout: {sys.stdout.encoding}")
print(f"  stderr: {sys.stderr.encoding}")
print(f"  PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")

# Тест Unicode виводу
print("\n[TEST] Тестування Unicode символів:")
print("[OK] Українська: Привіт, світе!")
print("[OK] Русский: Привет, мир!")
print("[OK] Спецсимволи: [OK] [ERROR] [WARNING]")
```

**Очікуваний результат після налаштування:**
```
[INFO] Перевірка налаштування кодування:
  stdin:  utf-8
  stdout: utf-8
  stderr: utf-8
  PYTHONIOENCODING: utf-8

[TEST] Тестування Unicode символів:
[OK] Українська: Привіт, світе!
[OK] Русский: Привет, мир!
[OK] Спецсимволы: [OK] [ERROR] [WARNING]
```

### Альтернативні рішення:

**Варіант 1: У коді скрипта (не рекомендовано)**
```python
import sys
import io

# Переконфігурувати stdout/stderr для UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

**Варіант 2: При запуску скрипта**
```bash
# PowerShell
$env:PYTHONIOENCODING="utf-8"; python my_script.py

# CMD
set PYTHONIOENCODING=utf-8 && python my_script.py
```

**Варіант 3: В IDE (налаштування термінала)**

VSCode:
```json
// settings.json
{
    "terminal.integrated.env.windows": {
        "PYTHONIOENCODING": "utf-8"
    }
}
```

PyCharm:
```
Settings → Tools → Terminal → Environment variables
Додати: PYTHONIOENCODING=utf-8
```

Visual Studio:
```
Tools → Options → Python → Environment
Додати змінну: PYTHONIOENCODING=utf-8
```

### Автоматична діагностика середовища:

Використовуй скрипт для автоматичної перевірки налаштування:

```bash
python common/check_environment.py
```

Скрипт перевіряє:
- Python кодування (stdin, stdout, stderr)
- Наявність PYTHONIOENCODING
- Роботу з Unicode символами
- Налаштування Git hooks
- Платформа-специфічні налаштування (Windows codepage)

### Виправлення типових помилок:

**Помилка:** `UnicodeEncodeError: 'charmap' codec can't encode character`

**Причина:** Python використовує cp1251 замість UTF-8

**Рішення:**
1. Встанови PYTHONIOENCODING=utf-8 (дивись вище)
2. Перезапусти термінал
3. Перевір налаштування: `python common/check_environment.py`

## 12. Підтримка

При виникненні проблем:

1. Запусти валідатор: `python common/script_encoding_validator.py .`
2. Перевір налаштування PYTHONIOENCODING (дивись розділ 11)
3. Перевір вивід на наявність конкретних проблем
4. Виправ проблеми згідно цього гайду
5. Повтори валідацію

Для питань та покращень створюй issue в проекті.

---

**Версія:** 1.1.0
**Дата:** 2025-10-09
**Автор:** Archon Implementation Engineer
**Оновлено:** Додано розділ про PYTHONIOENCODING для Windows
