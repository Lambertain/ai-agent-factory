# 06. Стандарти кодування

## 🐍 PYTHON CODING STANDARDS

### Загальні принципи:

- ✅ **Використовуй Python** як основну мову
- ✅ **Слідуй PEP8** - стандарт стилю Python
- ✅ **Type hints** - обов'язкова типізація
- ✅ **Format з black** - автоформатування коду
- ✅ **Pydantic** для валідації даних
- ✅ **FastAPI** для API
- ✅ **SQLAlchemy/SQLModel** для ORM (якщо потрібно)

### Docstrings:

**Пиши docstrings для КОЖНОЇ функції** у стилі Google:

```python
def example_function(param1: str, param2: int) -> str:
    """
    Короткий опис функції.

    Детальний опис що робить функція, як вона працює
    та які має особливості.

    Args:
        param1 (str): Опис першого параметра.
        param2 (int): Опис другого параметра.

    Returns:
        str: Опис того що повертає функція.

    Raises:
        ValueError: Опис умови коли виникає помилка.

    Examples:
        >>> example_function("test", 42)
        "result"
    """
    pass
```

### Type Hints:

**ЗАВЖДИ використовуй типізацію:**

```python
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class AgentDependencies:
    """Залежності агента з підтримкою RAG."""

    api_key: str
    project_path: str = ""
    agent_name: str = ""
    knowledge_tags: List[str] = field(default_factory=list)
    knowledge_domain: Optional[str] = None
```

## 💻 ПРАВИЛА КОДУВАННЯ

### 1️⃣ ЗАБОРОНЕНО ВИКОРИСТОВУВАТИ:

**❌ НІКОЛИ не використовуй смайли/емодзі в Python скриптах або production коді**
**❌ НІКОЛИ не використовуй Unicode символи в коді**
**❌ НІКОЛИ не використовуй емодзі в print() функціях скриптів**

**ПРАВИЛЬНО:**
```python
# Добре - звичайний текст
print("Task completed successfully")
logger.info("Processing started")
```

**НЕПРАВИЛЬНО:**
```python
# Погано - емодзі в коді
print("✅ Task completed")  # ❌
logger.info("🎯 Processing started")  # ❌
```

### 2️⃣ КОДУВАННЯ:

**✅ ЗАВЖДИ використовуй UTF-8 кодування, НЕ Unicode символи в коді**
**✅ ВСІ коментарі та рядки в коді повинні бути російською мовою в UTF-8**

```python
# -*- coding: utf-8 -*-
"""
Модуль для работы с агентами Pydantic AI.

Этот модуль содержит основную логику агента и его инструменты.
"""
```

### 3️⃣ ІНКРЕМЕНТАЛЬНІ ЗМІНИ:

**НІКОЛИ не редагувати великі секції файлів за раз!**

- ✅ Максимум 50 рядків за одне редагування
- ✅ Завжди робити маленькі інкрементальні зміни
- ✅ Тестувати кожну зміну перед наступною

### 4️⃣ ORGANIZATION КО:

**Чіткі, узгоджені імпорти:**
- Віддавай перевагу відносним імпортам всередині пакетів
- Групуй імпорти: стандартна бібліотека → сторонні → локальні
- Сортуй імпорти алфавітно в групах

```python
# Стандартна бібліотека
import os
import sys
from typing import List, Optional

# Сторонні бібліотеки
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field

# Локальні модулі
from .settings import load_settings
from .tools import search_tool
```

## 🔧 ENVIRONMENT VARIABLES

**✅ Використовуй python-dotenv та load_env() для змінних оточення**

```python
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    """Налаштування додатка з підтримкою змінних оточення."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct")

def load_settings() -> Settings:
    """Завантажити налаштування та перевірити наявність змінних."""
    load_dotenv()
    return Settings()
```

## 🧪 TESTING STANDARDS

### Pytest Unit Tests:

**ЗАВЖДИ створюй Pytest unit tests для нових фіч:**

```python
import pytest
from your_module import your_function

def test_your_function_expected_use():
    """Тест очікуваного використання."""
    result = your_function("input")
    assert result == "expected_output"

def test_your_function_edge_case():
    """Тест крайнього випадку."""
    result = your_function("")
    assert result is None

def test_your_function_failure_case():
    """Тест сценарію помилки."""
    with pytest.raises(ValueError):
        your_function(None)
```

**Структура тестів:**
```
/tests
├── test_agent.py         # Тести агента
├── test_tools.py         # Тести інструментів
├── test_integration.py   # Інтеграційні тести
├── test_validation.py    # Тести валідації
└── conftest.py           # Pytest конфігурація
```

**Мінімальне покриття для кожної функції:**
- 1 тест для очікуваного використання
- 1 edge case тест
- 1 failure case тест

## 📝 КОМЕНТАРІ ТА ДОКУМЕНТАЦІЯ

### Правила коментарів:

**✅ Коментуй незрозумілий код**
**✅ Додавай inline `# Причина:` коментарі для складної логіки**
**✅ Пояснюй ЧОМУ, а не ЩО**

```python
# Причина: Використовуємо batch processing для економії API викликів
# та зменшення затримки на 50%
results = await batch_process(items)

# Причина: Gemini Batch API надає 50% знижку на вартість
if settings.gemini_use_batch_api:
    provider = GeminiBatchProvider()
```

### Оновлення README:

**Оновлюй README.md коли:**
- Додаються нові фічі
- Змінюються залежності
- Модифікуються кроки налаштування

## 🚫 ЩО УНИКАТИ

**НІКОЛИ не:**
- ❌ Вигадувай бібліотеки або функції
- ❌ Використовуй неперевірені Python пакети
- ❌ Видаляй або перезаписуй існуючий код без інструкції
- ❌ Створюй файли без перевірки чи вони існують
