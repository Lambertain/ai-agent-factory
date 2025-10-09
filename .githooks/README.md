# Git Hooks для Agent Factory

Цей каталог містить готові Git hooks для автоматичної валідації коду.

## Встановлення

### Варіант 1: Налаштувати Git для використання .githooks (рекомендовано)

```bash
cd D:\Automation\agent-factory
git config core.hooksPath .githooks
```

Це налаштує Git на використання hooks з цього каталогу для всіх майбутніх комітів.

### Варіант 2: Скопіювати hook вручну

```bash
# Windows PowerShell
Copy-Item .githooks\pre-commit .git\hooks\pre-commit

# Linux/Mac
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Доступні Hooks

### pre-commit

Валідує кодування Python файлів перед кожним комітом.

**Що перевіряється:**
- UTF-8 кодування
- Відсутність BOM (Byte Order Mark)
- Відсутність емодзі в Python коді
- Наявність декларації кодування

**Що робити при помилці:**

Якщо hook заблокував коміт, виправте проблеми одним з способів:

1. **Автоматичне виправлення** (рекомендовано):
   ```bash
   python common/script_encoding_validator.py . --fix
   ```

2. **Попередній перегляд змін**:
   ```bash
   python common/script_encoding_validator.py . --fix --dry-run
   ```

3. **Ручне виправлення** згідно [CODING_STANDARDS.md](../CODING_STANDARDS.md)

Після виправлення повторіть `git commit`.

## Тимчасове відключення hook

Якщо потрібно зробити коміт без валідації (НЕ рекомендовано):

```bash
git commit --no-verify -m "your message"
```

**Увага:** Використовуйте --no-verify тільки в екстрених випадках!

## Додавання нових hooks

1. Створіть файл hook в `.githooks/`
2. Зробіть його виконуваним (Linux/Mac): `chmod +x .githooks/your-hook`
3. Оновіть цей README.md з описом нового hook

## Тестування hook

Перевірте що hook працює коректно:

```bash
# Створіть тестовий файл з емодзі
echo "print('✅ test')" > test_emoji.py

# Спробуйте закомітити
git add test_emoji.py
git commit -m "test"

# Hook має заблокувати коміт
# Якщо так - hook працює правильно

# Видаліть тестовий файл
git rm test_emoji.py
```

## Додаткова інформація

- [CODING_STANDARDS.md](../CODING_STANDARDS.md) - Повні стандарти кодування
- [common/README.md](../common/README.md) - Документація валідатора
- [common/script_encoding_validator.py](../common/script_encoding_validator.py) - Код валідатора

---

**Версія:** 1.0.0
**Дата:** 2025-10-09
**Автор:** Archon Implementation Engineer
