# Enhanced Validation System для AI Agent Factory

Комплексная система валидации и обработки входных данных с улучшенными возможностями проверки, нормализации и обработки ошибок.

## Основные компоненты

### 1. Расширенные валидаторы (`validators.py`)

Набор специализированных Pydantic валидаторов для различных типов данных:

- **EmailValidator** - валидация email адресов с нормализацией
- **URLValidator** - валидация URL с поддержкой схем и доменов
- **PhoneValidator** - международная валидация номеров телефонов
- **TextValidator** - валидация текста с фильтрацией контента
- **NumericValidator** - валидация чисел с проверкой диапазонов
- **DateTimeValidator** - валидация дат и времени с часовыми поясами

#### Специализированные валидаторы для агентов:

- **SearchRequestValidator** - валидация поисковых запросов
- **DocumentValidator** - валидация документов
- **ChunkValidator** - валидация фрагментов документов
- **SessionValidator** - валидация сессий
- **MessageValidator** - валидация сообщений
- **ToolCallValidator** - валидация вызовов инструментов

### 2. JSON схемы и регулярные выражения (`schemas.py`)

Обширная коллекция схем и паттернов для валидации:

```python
# Использование регулярных выражений
from validation.schemas import REGEX_PATTERNS

email_pattern = REGEX_PATTERNS['email_basic']
url_pattern = REGEX_PATTERNS['url_http']

# Проверка безопасности
contains_threats, threats = contains_security_threats(user_input)
```

### 3. Автоматическая нормализация данных (`normalizers.py`)

Система для очистки и стандартизации данных:

```python
from validation.normalizers import DataNormalizer

normalizer = DataNormalizer(
    strict_mode=False,
    auto_fix_errors=True
)

# Автоматическая нормализация
normalized_email = normalizer.normalize_email("  USER@EXAMPLE.COM  ")
# Результат: "user@example.com"

normalized_url = normalizer.normalize_url("example.com")
# Результат: "https://example.com"

# Пакетная нормализация
data_batch = [
    {"email": "USER@EXAMPLE.COM", "age": "25"},
    {"email": "test@test.com", "age": "30"}
]

field_types = {"email": "email", "age": "numeric"}
normalized_batch = normalizer.batch_normalize(data_batch, field_types)
```

### 4. Проверка типов и границ (`type_checker.py`)

Продвинутая система проверки типов с ограничениями:

```python
from validation.type_checker import TypeChecker, RangeConstraint

checker = TypeChecker(auto_convert=True)
constraint = RangeConstraint(min_value=0, max_value=100)

is_valid, converted_value, errors = checker.check_type(
    value="42.5",
    expected_type=float,
    constraints=[constraint]
)
```

### 5. Обработка ошибок (`error_handler.py`)

Комплексная система обработки ошибок валидации с детальными сообщениями:

```python
from validation.error_handler import ValidationErrorHandler
from pydantic import ValidationError

handler = ValidationErrorHandler(
    include_suggestions=True,
    localization='ru'
)

try:
    # Ваша валидация
    model = SomeModel(**data)
except ValidationError as e:
    report = handler.handle_pydantic_error(e, original_data=data)

    # Форматирование для пользователя
    user_message = handler.format_validation_report(report, "user_friendly")
    print(user_message)
```

## Быстрый старт

### Установка зависимостей

```bash
pip install -r validation/requirements.txt
```

### Базовое использование

```python
# Импорт основных компонентов
from validation import (
    EmailValidator, URLValidator, DataNormalizer,
    ValidationErrorHandler, quick_normalize_text
)

# Простая валидация email
try:
    email_validator = EmailValidator(email="user@example.com")
    print(f"Валидный email: {email_validator.email}")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")

# Быстрая нормализация текста
clean_text = quick_normalize_text("  <p>Hello World</p>  ")
print(f"Очищенный текст: {clean_text}")

# Валидация поискового запроса
search_validator = SearchRequestValidator(
    query="поиск документов по ИИ",
    search_type="semantic",
    limit=20
)
```

### Интеграция с агентами

```python
from validation import AgentInputValidator, DataNormalizer

# Валидация входных данных агента
def validate_agent_input(data):
    normalizer = DataNormalizer()

    # Нормализация данных
    normalized_data = normalizer.normalize_data(data)

    # Валидация через специальный валидатор
    validator = AgentInputValidator(
        input_data=normalized_data,
        required_fields=["query", "session_id"],
        optional_fields=["filters", "limit"]
    )

    return validator.input_data

# Использование в агенте
def process_agent_request(raw_input):
    try:
        validated_input = validate_agent_input(raw_input)
        # Обработка валидных данных
        return process_request(validated_input)
    except ValidationError as e:
        handler = ValidationErrorHandler()
        report = handler.handle_pydantic_error(e)
        return {"error": report.to_dict()}
```

## Продвинутые возможности

### Пользовательские валидаторы

```python
from validation.type_checker import ValidationConstraint

class CustomConstraint(ValidationConstraint):
    def validate(self, value):
        # Ваша логика валидации
        return len(str(value)) > 5

    def get_error_message(self, value):
        return f"Значение должно быть длиннее 5 символов, получено: {len(str(value))}"
```

### Безопасность

```python
from validation.schemas import contains_security_threats

user_input = "<script>alert('xss')</script>"
is_threat, threat_types = contains_security_threats(user_input)

if is_threat:
    print(f"Обнаружены угрозы: {threat_types}")
    # ['xss']
```

### Многоязычность

```python
# Русская локализация
ru_handler = ValidationErrorHandler(localization='ru')

# Английская локализация
en_handler = ValidationErrorHandler(localization='en')
```

### Производительность

```python
# Пакетная обработка для высокой производительности
normalizer = DataNormalizer()

large_dataset = [
    {"email": f"user{i}@example.com", "age": str(20 + i)}
    for i in range(10000)
]

field_types = {"email": "email", "age": "numeric"}
normalized_data = normalizer.batch_normalize(large_dataset, field_types)
```

## Тестирование

Запуск тестов:

```bash
# Все тесты
pytest validation/tests/

# Только быстрые тесты
pytest validation/tests/ -m "not slow"

# Тесты безопасности
pytest validation/tests/ -m "security"

# С покрытием кода
pytest validation/tests/ --cov=validation
```

## Примеры использования

### Валидация документов

```python
from validation import DocumentValidator

document = DocumentValidator(
    title="Исследование в области ИИ",
    content="Содержимое исследования...",
    source="https://example.com/research.pdf"
)

print(f"Валидный документ: {document.title}")
```

### Валидация фрагментов

```python
from validation import ChunkValidator

chunk = ChunkValidator(
    content="Фрагмент документа с важной информацией",
    chunk_index=0,
    token_count=8,
    embedding=[0.1] * 1536  # OpenAI embedding
)
```

### Обработка ошибок в агентах

```python
def agent_error_handler(validation_error, context=None):
    handler = ValidationErrorHandler(
        include_suggestions=True,
        localization='ru'
    )

    report = handler.handle_pydantic_error(
        validation_error,
        context=context
    )

    return {
        "success": False,
        "errors": [error.to_dict() for error in report.errors],
        "suggestions": [
            suggestion
            for error in report.errors
            for suggestion in error.suggestions
        ]
    }
```

## Архитектура

### Структура модулей

```
validation/
├── __init__.py           # Основные экспорты
├── validators.py         # Pydantic валидаторы
├── schemas.py           # JSON схемы и regex паттерны
├── normalizers.py       # Система нормализации данных
├── type_checker.py      # Проверка типов и ограничений
├── error_handler.py     # Обработка ошибок
├── requirements.txt     # Зависимости
├── README.md           # Документация
└── tests/              # Тесты
    ├── __init__.py
    ├── conftest.py     # Конфигурация pytest
    ├── test_validators.py
    ├── test_normalizers.py
    └── test_error_handler.py
```

### Принципы проектирования

1. **Модульность** - каждый компонент независим и переиспользуем
2. **Расширяемость** - легко добавлять новые валидаторы и правила
3. **Производительность** - оптимизация для больших объемов данных
4. **Безопасность** - защита от инъекций и XSS атак
5. **Локализация** - поддержка множественных языков
6. **Детальная диагностика** - подробные сообщения об ошибках

## Интеграция с AI Agent Factory

Система валидации интегрируется со всеми компонентами фабрики агентов:

1. **Входные данные агентов** - валидация запросов пользователей
2. **Инструменты агентов** - валидация параметров инструментов
3. **База знаний** - валидация документов и фрагментов
4. **Сессии** - валидация данных сессий и сообщений
5. **Конфигурация** - валидация настроек агентов

### Производительность и масштабируемость

- Поддержка пакетной обработки
- Оптимизированные регулярные выражения
- Кэширование результатов валидации
- Асинхронная обработка (при необходимости)

## Заключение

Система Enhanced Validation обеспечивает надежную, производительную и расширяемую валидацию данных для AI Agent Factory. Она включает в себя современные подходы к обработке ошибок, автоматической нормализации данных и обеспечению безопасности.

Для получения дополнительной информации обратитесь к документации отдельных модулей или изучите примеры в тестах.