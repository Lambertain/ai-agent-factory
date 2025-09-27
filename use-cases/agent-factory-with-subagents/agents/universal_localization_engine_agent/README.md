# Universal Localization Engine Agent

Универсальный агент для автоматизации процессов локализации и интернационализации (i18n/l10n) различных типов проектов с поддержкой 20+ языков и культурной адаптации.

## Возможности

### 🌍 Универсальная поддержка проектов
- **Веб-приложения**: React, Vue, Angular, Svelte, HTML/JS
- **Мобильные приложения**: iOS, Android, React Native, Flutter, Xamarin
- **Десктопные приложения**: Electron, WPF, Qt, GTK, Cocoa
- **API и документация**: OpenAPI, REST, GraphQL, Markdown
- **Игры**: Unity, Unreal Engine, Godot
- **Документация**: Wiki, Confluence, Git-репозитории

### 🔤 Расширенная языковая поддержка
- **20+ языков**: Английский, испанский, французский, немецкий, русский, китайский, японский, корейский, арабский, хинди и другие
- **Региональные варианты**: en-US vs en-GB, es-ES vs es-MX
- **RTL поддержка**: Арабский, иврит, персидский
- **Сложные письменности**: Китайские иероглифы, японская хирагана/катакана

### 🎯 Умные уровни качества
- **Basic**: Быстрый автоматический перевод для черновиков
- **Standard**: Улучшенный перевод с терминологическими проверками
- **Professional**: Профессиональный перевод с лингвистическим контролем
- **Native**: Перевод носителя языка с полной культурной адаптацией

### 🛠 Автоматизированные процессы
- **Извлечение контента**: Автоматическое обнаружение переводимых строк
- **Пакетный перевод**: Оптимизированная обработка больших объемов
- **Контроль качества**: Многоуровневая валидация переводов
- **UI совместимость**: Проверка отображения в интерфейсе
- **Культурная адаптация**: Адаптация под местные особенности

## Быстрый старт

### Базовое использование

```python
from pydantic_ai import Agent
from universal_localization_engine_agent.agent import universal_localization_engine_agent

# Основная локализация
result = await universal_localization_engine_agent.run(
    "Переведи веб-приложение с английского на испанский",
    source_language="en",
    target_languages=["es"],
    project_type="web",
    translation_quality="professional"
)
```

### Расширенная конфигурация

```python
# Мультиязычная локализация с культурной адаптацией
result = await universal_localization_engine_agent.run(
    "Локализуй мобильное приложение для европейских рынков",
    source_language="en",
    target_languages=["es", "fr", "de", "it"],
    project_type="mobile",
    translation_quality="native",
    enable_cultural_adaptation=True,
    enable_ui_validation=True
)
```

### Извлечение переводимого контента

```python
from universal_localization_engine_agent.tools import extract_translatable_content

# Извлечение из проекта
content = await extract_translatable_content(
    ctx,
    project_path="/path/to/project",
    extraction_config={
        "file_patterns": ["*.js", "*.tsx", "*.vue"],
        "exclude_patterns": ["node_modules/**", "dist/**"],
        "extract_comments": True
    }
)
```

### Пакетный перевод

```python
from universal_localization_engine_agent.tools import translate_content_batch

# Перевод большого объема контента
translations = await translate_content_batch(
    ctx,
    content_items=[
        {"key": "welcome", "text": "Welcome to our app"},
        {"key": "login", "text": "Login to continue"},
        {"key": "signup", "text": "Create new account"}
    ],
    target_languages=["es", "fr", "de"],
    translation_quality="professional",
    batch_size=100
)
```

## Архитектура

### Основные компоненты

```
Universal Localization Engine Agent
├── Content Extractor      # Извлечение переводимого контента
├── Translation Engine      # Ядро системы перевода
├── Quality Validator       # Контроль качества переводов
├── Cultural Adapter        # Культурная адаптация
├── UI Validator           # Проверка интерфейса
├── Workflow Orchestrator  # Управление процессами
└── Cost Optimizer         # Оптимизация затрат
```

### Поддерживаемые форматы

#### Веб-разработка
- **JSON**: Стандартные файлы локализации
- **YAML**: Конфигурационные файлы
- **Properties**: Java-стиль локализации
- **gettext**: .po/.pot файлы

#### Мобильная разработка
- **iOS**: .strings, .stringsdict, Localizable.strings
- **Android**: strings.xml, arrays.xml, plurals.xml
- **React Native**: JSON, JS/TS модули
- **Flutter**: .arb файлы
- **Xamarin**: .resx файлы

#### Игровая разработка
- **Unity**: Asset файлы, ScriptableObjects
- **Unreal Engine**: .uasset локализационные файлы
- **Godot**: .csv файлы переводов

## Конфигурация

### Настройка для проекта

```python
from universal_localization_engine_agent.settings import LocalizationEngineConfig

config = LocalizationEngineConfig()

# Языковые настройки
config.general.default_source_language = "en"
config.general.supported_target_languages = ["es", "fr", "de", "zh", "ja"]

# Настройки качества
config.general.default_quality_level = "professional"
config.general.enable_cultural_adaptation = True

# Технические настройки
config.general.max_concurrent_translations = 10
config.general.translation_batch_size = 200
```

### Настройка для типа проекта

```python
# Веб-проект
web_config = config.get_project_config("web")
web_config["file_patterns"] = ["*.js", "*.tsx", "*.vue"]
web_config["ui_length_limits"] = {"button": 20, "title": 50}

# Мобильный проект
mobile_config = config.get_project_config("mobile")
mobile_config["platforms"] = ["ios", "android"]
mobile_config["screen_size_considerations"] = True
```

## Интеграция

### CI/CD интеграция

```yaml
# GitHub Actions
name: Localization Pipeline
on:
  push:
    paths: ['src/**', 'locales/**']

jobs:
  localize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Extract translatable content
        run: |
          python -m universal_localization_engine_agent.cli extract \
            --project-path . \
            --output locales/source.json

      - name: Translate content
        run: |
          python -m universal_localization_engine_agent.cli translate \
            --source locales/source.json \
            --target-languages es,fr,de \
            --quality professional

      - name: Validate translations
        run: |
          python -m universal_localization_engine_agent.cli validate \
            --locales-path locales/ \
            --check-ui-compatibility
```

### API интеграция

```python
from fastapi import FastAPI
from universal_localization_engine_agent.api import create_localization_api

app = FastAPI()

# Добавление API эндпоинтов локализации
localization_api = create_localization_api()
app.include_router(localization_api, prefix="/api/v1/localization")

# Доступные эндпоинты:
# POST /api/v1/localization/extract
# POST /api/v1/localization/translate
# POST /api/v1/localization/validate
# GET /api/v1/localization/status
```

## Продвинутые возможности

### Культурная адаптация

```python
# Автоматическая адаптация для рынков
cultural_adaptation = await universal_localization_engine_agent.run(
    "Адаптируй интерфейс электронной коммерции под азиатские рынки",
    target_languages=["zh", "ja", "ko"],
    cultural_settings={
        "adapt_colors": True,        # Культурное значение цветов
        "adapt_imagery": True,       # Подходящие изображения
        "adapt_layout": True,        # RTL/LTR адаптация
        "adapt_currency": True,      # Местные валюты
        "adapt_dates": True          # Форматы дат
    }
)
```

### Терминологическое управление

```python
from universal_localization_engine_agent.tools import manage_terminology

# Создание глоссария
terminology = await manage_terminology(
    ctx,
    action="create_glossary",
    domain="ecommerce",
    terms={
        "checkout": {"es": "finalizar compra", "fr": "valider commande"},
        "cart": {"es": "carrito", "fr": "panier"},
        "wishlist": {"es": "lista de deseos", "fr": "liste de souhaits"}
    }
)
```

### Автоматическое тестирование UI

```python
from universal_localization_engine_agent.tools import validate_ui_compatibility

# Проверка совместимости интерфейса
ui_validation = await validate_ui_compatibility(
    ctx,
    project_path="/path/to/project",
    locales=["es", "fr", "de"],
    test_scenarios=[
        "button_text_overflow",
        "menu_item_length",
        "form_label_display",
        "responsive_layout"
    ]
)
```

## Оптимизация производительности

### Кэширование переводов

```python
# Настройка кэширования
config.cost_optimization.caching_settings.update({
    "enable_translation_cache": True,
    "cache_duration_days": 30,
    "cache_similarity_threshold": 0.95,
    "enable_fuzzy_matching": True
})
```

### Пакетная обработка

```python
# Оптимизированная пакетная обработка
config.cost_optimization.batch_processing.update({
    "enable_batching": True,
    "optimal_batch_size": 200,
    "batch_timeout_minutes": 15,
    "parallel_processing": True
})
```

## Мониторинг и аналитика

### Метрики качества

```python
from universal_localization_engine_agent.analytics import LocalizationMetrics

metrics = LocalizationMetrics()

# Отслеживание качества
quality_report = await metrics.generate_quality_report(
    project_path="/path/to/project",
    time_period="last_30_days",
    include_metrics=[
        "translation_accuracy",
        "cultural_appropriateness",
        "ui_compatibility",
        "user_satisfaction"
    ]
)
```

### Отчеты по производительности

```python
# Отчет по производительности
performance_report = await metrics.generate_performance_report(
    include_metrics=[
        "words_per_day",
        "cost_per_word",
        "time_to_market",
        "automation_rate"
    ]
)
```

## Лучшие практики

### 1. Планирование локализации
- Проектируйте интерфейс с учетом будущей локализации
- Используйте псевдолокализацию для раннего тестирования
- Планируйте расширение текста (немецкий +30%, китайский -30%)

### 2. Качество контента
- Добавляйте контекстные комментарии к переводимым строкам
- Создавайте глоссарии для единообразия терминологии
- Разрабатывайте стилевые руководства для каждого языка

### 3. Технические аспекты
- Используйте UTF-8 кодировку везде
- Применяйте последовательный формат плейсхолдеров
- Правильно обрабатывайте множественные формы
- Поддерживайте RTL языки

### 4. Автоматизация
- Интегрируйте локализацию в CI/CD пайплайн
- Автоматизируйте извлечение и обновление переводов
- Настройте автоматическое тестирование локализованных версий

## Устранение неполадок

### Распространенные проблемы

**Проблема**: Сломанная разметка после перевода
```bash
# Включите валидацию HTML/XML
python -m universal_localization_engine_agent.cli validate \
  --check-markup-integrity \
  --fix-broken-tags
```

**Проблема**: Переполнение UI элементов
```bash
# Проверьте длину текста
python -m universal_localization_engine_agent.cli validate \
  --check-ui-length-limits \
  --adaptive-truncation
```

**Проблема**: Неправильное отображение символов
```bash
# Проверьте кодировку и шрифты
python -m universal_localization_engine_agent.cli validate \
  --check-encoding \
  --check-font-support
```

## Поддержка

- **Документация**: [knowledge/universal_localization_engine_knowledge.md](knowledge/universal_localization_engine_knowledge.md)
- **Примеры**: [examples/](examples/)
- **API Reference**: [docs/api.md](docs/api.md)

## Лицензия

MIT License - см. [LICENSE](LICENSE) файл для деталей.