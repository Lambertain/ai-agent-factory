# Примеры использования Contact Registry

Этот документ содержит практические примеры использования системы контактов для агентов.

## Базовое использование

### Пример 1: Добавление контактов в README.md

```python
from common.contacts_registry import get_contacts

# Получить контакты для проекта Lazy Income AI
contacts = get_contacts("lazy_income_public")

# Генерировать секцию для README
readme_section = contacts.to_readme_section()

# Добавить в конец README.md
with open("README.md", "a", encoding="utf-8") as f:
    f.write("\n\n")
    f.write(readme_section)

print("[OK] Contacts section added to README.md")
```

**Результат в README.md:**
```markdown
## Author
**Nikita Solovey**
- Email: nikitasolovey1@gmail.com
- GitHub: [@LazyIncomeAI](https://github.com/LazyIncomeAI)
- Company: Lazy Income AI
- Website: [https://lambertain.agency](https://lambertain.agency)
- Follow: [Instagram](https://www.instagram.com/solovey_nikita) | [YouTube](https://www.youtube.com/@LazyIncome_AI) | [Telegram](https://t.me/LazyIncomeAI) | [TikTok](https://www.tiktok.com/@lazyincome_ai) | [Facebook](https://www.facebook.com/profile.php?id=61573906928624)
```

---

## Работа с клиентскими проектами

### Пример 2: Создание README для клиентского проекта (публичный репозиторий)

```python
from common.contacts_registry import update_client_profile

# Обновить профиль клиента с реальными данными
client_contacts = update_client_profile(
    profile_type="client_public",
    github_username="TechStartupInc",
    company_name="Tech Startup Inc.",
    website="https://techstartup.com"
)

# Генерировать секцию
readme_section = client_contacts.to_readme_section()

# Сохранить в README
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Tech Startup Project\n\n")
    f.write("Project description here...\n\n")
    f.write(readme_section)

print("[OK] Client project README created")
```

**Результат в README.md:**
```markdown
## Author
**Nikita Solovey**
- Email: nikitasolovey1@gmail.com
- GitHub: [@TechStartupInc](https://github.com/TechStartupInc)
- Company: Tech Startup Inc.
- Website: [https://techstartup.com](https://techstartup.com)

*Developed by Nikita Solovey | Lazy Income AI* | [https://github.com/LazyIncomeAI](https://github.com/LazyIncomeAI)
```

---

### Пример 3: Создание README для приватного клиентского проекта

```python
from common.contacts_registry import update_client_profile

# Для приватных репозиториев не показываем "Developed by"
client_contacts = update_client_profile(
    profile_type="client_private",
    github_username="ClientPrivateOrg",
    company_name="Client Private Organization"
)

readme_section = client_contacts.to_readme_section()

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Private Client Project\n\n")
    f.write("Internal documentation...\n\n")
    f.write(readme_section)
```

---

## Настройка Git Configuration

### Пример 4: Автоматическая настройка git для проекта

```python
from common.contacts_registry import get_git_config
import subprocess

# Получить git конфигурацию для профиля
git_config = get_git_config("lazy_income_public")

# Применить локально для текущего репозитория
subprocess.run(["git", "config", "user.name", git_config["user.name"]])
subprocess.run(["git", "config", "user.email", git_config["user.email"]])

print(f"[OK] Git config updated:")
print(f"  user.name: {git_config['user.name']}")
print(f"  user.email: {git_config['user.email']}")
```

**Результат:**
```bash
[OK] Git config updated:
  user.name: Nikita Solovey
  user.email: nikitasolovey1@gmail.com
```

---

## Использование в агентах

### Пример 5: Создание нового проекта агентом

```python
from pathlib import Path
from common.contacts_registry import get_contacts

def create_project_readme(project_name: str, description: str, profile: str = "lazy_income_public"):
    """
    Создать README.md для нового проекта с правильными контактами.

    Args:
        project_name: Название проекта
        description: Описание проекта
        profile: Профиль контактов
    """
    contacts = get_contacts(profile)

    readme_content = f"""# {project_name}

{description}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install {project_name.lower().replace(' ', '-')}
```

## Usage

```python
from {project_name.lower().replace(' ', '_')} import main

main()
```

## License

MIT License

{contacts.to_readme_section()}
"""

    readme_path = Path("README.md")
    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"[OK] README.md created for {project_name}")
    return readme_path


# Использование агентом
create_project_readme(
    project_name="Awesome AI Tool",
    description="An awesome automation tool powered by AI",
    profile="lazy_income_public"
)
```

---

### Пример 6: Обработка нескольких проектов

```python
from common.contacts_registry import get_contacts, update_client_profile
from pathlib import Path

def process_projects(projects: list):
    """
    Обработать несколько проектов и добавить контакты.

    Args:
        projects: Список словарей с информацией о проектах
    """
    for project in projects:
        # Определить тип профиля
        if project.get("is_client"):
            contacts = update_client_profile(
                profile_type="client_public" if project.get("public") else "client_private",
                github_username=project["github_username"],
                company_name=project["company_name"],
                website=project.get("website")
            )
        else:
            contacts = get_contacts("lazy_income_public")

        # Обновить README
        readme_path = Path(project["path"]) / "README.md"
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")

            # Удалить старую секцию контактов если есть
            if "## Author" in content:
                content = content.split("## Author")[0].rstrip()

            # Добавить новую секцию
            content += "\n\n" + contacts.to_readme_section()

            readme_path.write_text(content, encoding="utf-8")
            print(f"[OK] Updated: {readme_path}")


# Пример использования
projects = [
    {
        "path": "D:/Projects/my-automation-tool",
        "is_client": False
    },
    {
        "path": "D:/Projects/client-project",
        "is_client": True,
        "public": True,
        "github_username": "ClientCompany",
        "company_name": "Client Company Ltd.",
        "website": "https://clientcompany.com"
    },
    {
        "path": "D:/Projects/another-tool",
        "is_client": False
    }
]

process_projects(projects)
```

---

## Валидация контактов

### Пример 7: Проверка, что контакты не являются placeholders

```python
from common.contacts_registry import get_contacts

def validate_contacts(profile: str = "lazy_income_public"):
    """
    Проверить что контакты валидны и не являются placeholders.

    Args:
        profile: Профиль контактов для проверки

    Returns:
        bool: True если контакты валидны
    """
    contacts = get_contacts(profile)

    # Проверить на placeholder значения
    placeholders = [
        "[", "]", "placeholder", "your", "example",
        "todo", "replace", "changeme"
    ]

    invalid_fields = []

    for field in ["author_name", "author_email", "github_username"]:
        value = getattr(contacts, field, "")
        if any(p in value.lower() for p in placeholders):
            invalid_fields.append(field)

    if invalid_fields:
        print(f"[ERROR] Invalid fields: {', '.join(invalid_fields)}")
        return False

    print(f"[OK] Contacts validated for profile: {profile}")
    return True


# Использование
if validate_contacts("lazy_income_public"):
    print("[OK] Contacts are ready to use")
else:
    print("[ERROR] Please update contacts in contacts_registry.py")
```

---

## Тестирование

### Пример 8: Unit тесты для системы контактов

```python
import pytest
from common.contacts_registry import get_contacts, update_client_profile, get_git_config


def test_get_lazy_income_contacts():
    """Тест получения контактов Lazy Income AI."""
    contacts = get_contacts("lazy_income_public")

    assert contacts.author_name == "Nikita Solovey"
    assert contacts.author_email == "nikitasolovey1@gmail.com"
    assert contacts.github_username == "LazyIncomeAI"
    assert contacts.company == "Lazy Income AI"
    assert contacts.youtube is not None
    assert contacts.telegram is not None


def test_update_client_profile():
    """Тест обновления клиентского профиля."""
    client_contacts = update_client_profile(
        profile_type="client_public",
        github_username="TestClient",
        company_name="Test Company",
        website="https://test.com"
    )

    assert client_contacts.github_username == "TestClient"
    assert client_contacts.company == "Test Company"
    assert client_contacts.website == "https://test.com"
    assert client_contacts.developed_by == "Nikita Solovey | Lazy Income AI"


def test_readme_section_generation():
    """Тест генерации секции README."""
    contacts = get_contacts("lazy_income_public")
    readme_section = contacts.to_readme_section()

    assert "## Author" in readme_section
    assert "Nikita Solovey" in readme_section
    assert "@LazyIncomeAI" in readme_section
    assert "YouTube" in readme_section


def test_git_config():
    """Тест получения git конфигурации."""
    git_config = get_git_config("lazy_income_public")

    assert "user.name" in git_config
    assert "user.email" in git_config
    assert git_config["user.name"] == "Nikita Solovey"
    assert git_config["user.email"] == "nikitasolovey1@gmail.com"


def test_invalid_profile():
    """Тест обработки неизвестного профиля."""
    with pytest.raises(ValueError):
        get_contacts("unknown_profile")


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
```

---

## Интеграция с CI/CD

### Пример 9: Автоматическая проверка контактов в CI/CD

```yaml
# .github/workflows/validate-contacts.yml
name: Validate Contacts

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest

      - name: Run contacts validation
        run: |
          python -c "
          from common.contacts_registry import get_contacts
          contacts = get_contacts('lazy_income_public')
          assert '[' not in contacts.author_name
          assert '[' not in contacts.author_email
          print('[OK] Contacts validated')
          "

      - name: Run contact tests
        run: |
          pytest common/tests/test_contacts_registry.py
```

---

## Полезные советы

1. **Всегда используй правильный профиль**:
   - Свои проекты → `lazy_income_public`
   - Клиентские публичные → `client_public`
   - Клиентские приватные → `client_private`

2. **Проверяй контакты перед публикацией**:
   ```python
   contacts = get_contacts("lazy_income_public")
   print(contacts.to_readme_section())
   # Проверь что всё правильно перед коммитом
   ```

3. **Обновляй git config для каждого проекта**:
   ```bash
   # Локальная конфигурация для проекта
   git config user.name "Nikita Solovey"
   git config user.email "nikitasolovey1@gmail.com"
   ```

4. **Для клиентов - всегда уточняй данные**:
   - GitHub username клиента
   - Официальное название компании
   - URL сайта
   - Нужно ли указывать "Developed by"

---

## Чек-лист для агентов

При создании нового проекта, убедись что:

- [ ] Использован правильный профиль контактов
- [ ] Контакты добавлены в README.md
- [ ] Git config настроен правильно
- [ ] Нет placeholder значений
- [ ] Для клиентских проектов согласовано "Developed by"
- [ ] Все social media ссылки рабочие
- [ ] Email адрес актуален

---

**Документ создан:** 2025-10-10
**Версия:** 1.0
**Автор:** Archon Implementation Engineer
