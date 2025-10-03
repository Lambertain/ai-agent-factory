# Pattern Cultural Adaptation Expert Agent

Специализированный агент для культурной адаптации психологических интервенций с учетом культурных особенностей, религиозных контекстов и языковых нюансов.

## 🌍 Поддерживаемые культуры

- **Украинская** - православный контекст, коллективистские ценности, высокий контекст коммуникации
- **Польская** - католический контекст, традиционные ценности, прямая коммуникация
- **Английская** - светский контекст, индивидуалистские ценности, низкий контекст коммуникации
- **Немецкая** - светский контекст, структурированные ценности, прямая коммуникация
- **Универсальная** - межкультурные принципы, адаптивный подход

## 🛠 Основные возможности

### Анализ культурного контекста
- Выявление культурно-специфичных элементов
- Определение потенциальных проблем адаптации
- Анализ чувствительных тем и табу
- Оценка коммуникационного стиля

### Адаптация контента
- Замена метафор на культурно-релевантные
- Локализация примеров и историй
- Адаптация стиля коммуникации
- Учет религиозных и социальных особенностей

### Валидация приемлемости
- Проверка культурной чувствительности
- Оценка религиозной корректности
- Контроль избегания стереотипов
- Валидация инклюзивности

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка переменных окружения

```bash
# Скопируйте файл примера
cp .env.example .env

# Отредактируйте .env файл, добавив ваш API ключ
CULTURAL_ADAPTATION_LLM_API_KEY=your_api_key_here
```

### Тестирование

Запуск всех тестов:
```bash
cd tests/
pytest -v
```

Запуск конкретной группы тестов:
```bash
pytest tests/test_agent.py -v              # Тесты основного агента
pytest tests/test_tools.py -v              # Тесты инструментов
pytest tests/test_cultural_configs.py -v   # Тесты конфигураций
pytest tests/test_dependencies.py -v       # Тесты зависимостей
```

Запуск с покрытием кода:
```bash
pytest --cov=. --cov-report=html
```

### Базовое использование

```python
from pattern_cultural_adaptation_expert import (
    run_pattern_cultural_adaptation_expert,
    analyze_content_for_culture,
    adapt_content_for_culture
)

# Анализ контента для украинской культуры
result = await analyze_content_for_culture(
    content="Преодоление стресса через медитацию",
    target_culture="ukrainian"
)

# Адаптация контента для польской культуры
adapted = await adapt_content_for_culture(
    content="Техника релаксации",
    target_culture="polish",
    adaptation_type="moderate"
)

# Полнофункциональный запуск агента
response = await run_pattern_cultural_adaptation_expert(
    user_message="Адаптируй НЛП-технику для украинской аудитории",
    target_culture="ukrainian"
)
```

## 📋 Типы адаптации

### Поверхностная (shallow)
- Замена очевидно проблематичных элементов
- Базовая адаптация терминологии
- Учет основных культурных табу

### Умеренная (moderate)
- Сбалансированная адаптация метафор и примеров
- Адаптация стиля коммуникации
- Учет религиозных контекстов

### Глубокая (deep)
- Полная реконструкция под культурное мировоззрение
- Интеграция традиционных практик
- Создание культурно-специфичных версий

## 🔧 Конфигурация

### Настройка целевой культуры

```python
from pattern_cultural_adaptation_expert import create_cultural_adaptation_dependencies, CultureType

# Создание зависимостей для украинской культуры
deps = create_cultural_adaptation_dependencies(
    api_key="your_api_key",
    target_culture=CultureType.UKRAINIAN,
    domain_type="psychology",
    adaptation_depth="moderate"
)
```

### Предустановленные конфигурации доменов

#### Терапевтический домен
```python
from examples.therapy_config import (
    create_therapy_config,
    THERAPY_UKRAINIAN_CONFIG,
    get_therapy_examples
)

# Быстрое создание терапевтической конфигурации
deps = create_therapy_config("your_api_key", "ukrainian")

# Использование готовой конфигурации
config = THERAPY_UKRAINIAN_CONFIG
print(f"Культурный фокус: {config['cultural_focus']}")
print(f"Стиль коммуникации: {config['communication_style']}")

# Получение примеров терапевтических техник
examples = get_therapy_examples()
print(examples["anxiety_treatment"]["ukrainian"])
```

#### Образовательный домен
```python
from examples.education_config import (
    create_education_config,
    EDUCATION_ENGLISH_CONFIG,
    get_education_examples
)

# Создание образовательной конфигурации
deps = create_education_config("your_api_key", "english")

# Примеры образовательных программ
examples = get_education_examples()
print(examples["psychology_course"]["english"])
```

#### Корпоративный домен
```python
from examples.corporate_config import (
    create_corporate_config,
    CORPORATE_POLISH_CONFIG,
    get_corporate_examples
)

# Создание корпоративной конфигурации
deps = create_corporate_config("your_api_key", "polish")

# Примеры корпоративных программ
examples = get_corporate_examples()
print(examples["leadership_development"]["polish"])
```

## 🛠 Инструменты агента

### search_agent_knowledge
Поиск в базе знаний агента по культурной адаптации

### analyze_cultural_context
Анализ культурного контекста контента

### adapt_content_culturally
Адаптация контента под культурные особенности

### validate_cultural_appropriateness
Валидация культурной приемлемости

### adapt_metaphors_culturally
Специализированная адаптация метафор

### generate_cultural_examples
Генерация культурно-релевантных примеров

## 📊 Примеры использования

### Анализ чувствительных тем

```python
from pattern_cultural_adaptation_expert.tools import CulturalAnalysisRequest

request = CulturalAnalysisRequest(
    content="Работа с семейными конфликтами",
    target_culture="polish",
    sensitivity_level="high"
)

result = await analyze_cultural_context(ctx, request)
```

### Адаптация метафор

```python
from pattern_cultural_adaptation_expert.tools import MetaphorAdaptationRequest

request = MetaphorAdaptationRequest(
    original_metaphors=["строительство моста", "корни дерева"],
    target_culture="ukrainian",
    context="therapy",
    emotional_tone="supportive"
)

result = await adapt_metaphors_culturally(ctx, request)
```

### Валидация адаптации

```python
from pattern_cultural_adaptation_expert.tools import CulturalValidationRequest

request = CulturalValidationRequest(
    adapted_content="Адаптированный текст...",
    target_culture="english",
    validation_criteria=["cultural_sensitivity", "religious_appropriateness"]
)

result = await validate_cultural_appropriateness(ctx, request)
```

## 🌐 Культурные профили

### Украинская культура
- **Ценности**: стойкость, семья, свобода, достоинство
- **Метафоры**: поле, дуб, река, домашний очаг
- **Чувствительные темы**: война, оккупация, национальная идентичность
- **Стиль**: эмоциональный, высокий контекст

### Польская культура
- **Ценности**: традиция, вера, солидарность, гордость
- **Метафоры**: католические образы, исторические события
- **Чувствительные темы**: религиозные нормы, национальная гордость
- **Стиль**: формальный, уважительный

### Английская культура
- **Ценности**: индивидуализм, достижения, инновации
- **Метафоры**: светские, универсальные
- **Чувствительные темы**: политика, расовые отношения
- **Стиль**: прямой, низкий контекст

## 📈 Мониторинг и метрики

Агент отслеживает:
- Качество адаптации
- Культурную приемлемость
- Эффективность адаптации
- Пользовательскую удовлетворенность

## 🔒 Безопасность и этика

- Избегание культурных стереотипов
- Уважение к религиозным убеждениям
- Защита чувствительной информации
- Соблюдение GDPR

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/

# Тестирование с покрытием
pytest tests/ --cov=pattern_cultural_adaptation_expert
```

## 📚 Документация

Подробная документация доступна в папке `knowledge/`:
- `pattern_cultural_adaptation_expert_knowledge.md` - база знаний агента

## 🤝 Вклад в развитие

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Отправьте pull request

## 📄 Лицензия

MIT License

## 🔗 Связанные проекты

- [AI Agent Factory](../../) - фабрика для создания специализированных агентов
- Универсальная интеграция с любыми проектами психологических интервенций
- Поддержка различных фреймворков культурной адаптации