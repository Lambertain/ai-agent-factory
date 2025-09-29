# Pattern VAK Adaptation Specialist Agent

Специализированный агент для адаптации психологического контента под различные сенсорные модальности (Visual, Auditory, Kinesthetic) в рамках PatternShift системы психологических трансформаций.

## 🎯 Назначение

Агент предназначен для автоматической адаптации психологических техник, медитативных практик, упражнений и других модулей PatternShift под предпочитаемые пользователем каналы восприятия информации.

### Ключевые возможности

- **VAK анализ контента** - определение доминирующих сенсорных модальностей
- **Адаптация под модальности** - трансформация контента для Visual/Auditory/Kinesthetic каналов
- **Мультимодальные варианты** - создание версий контента для всех модальностей
- **Сохранение терапевтической целостности** - адаптация с сохранением ключевого смысла
- **Травма-информированный подход** - безопасность и этичность адаптаций
- **Батчевая обработка** - эффективная обработка множественного контента

## 🏗️ Архитектура

```
pattern_vak_adaptation_specialist/
├── agent.py                      # Основной агент с Pydantic AI
├── dependencies.py               # VAK типы и зависимости
├── tools.py                      # Инструменты адаптации
├── prompts.py                    # Системные промпты
├── settings.py                   # Конфигурация агента
├── knowledge/                    # База знаний агента
│   └── pattern_vak_adaptation_specialist_knowledge.md
├── examples/                     # Примеры конфигураций
│   ├── __init__.py
│   ├── nlp_techniques_config.py
│   ├── meditation_config.py
│   └── visualization_movement_config.py
├── tests/                        # Комплексное тестирование
│   ├── conftest.py
│   ├── test_dependencies.py
│   ├── test_tools.py
│   ├── test_agent.py
│   ├── test_integration.py
│   └── test_examples.py
├── __init__.py
└── README.md
```

## 🛠️ Установка и настройка

### Требования

- Python 3.9+
- Pydantic AI
- Доступ к LLM API (Qwen, OpenAI, Gemini)
- Archon MCP Server (для интеграции с базой знаний)

### Установка зависимостей

```bash
pip install pydantic-ai python-dotenv pydantic-settings
```

### Конфигурация

Создайте файл `.env` с необходимыми переменными:

```env
# LLM Configuration
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen2.5-coder-32b-instruct

# PatternShift Configuration
PATTERN_SHIFT_BASE_PATH=/path/to/patternshift
ADAPTATION_DEPTH=moderate
ENABLE_SAFETY_VALIDATION=true
TRAUMA_INFORMED_ADAPTATIONS=true

# Archon Integration
ARCHON_PROJECT_ID=your_project_id
ENABLE_KNOWLEDGE_SEARCH=true
```

## 🚀 Использование

### Базовое использование

```python
from pattern_vak_adaptation_specialist import (
    PatternVAKAdaptationAgent,
    VAKAdaptationRequest,
    VAKModalityType,
    AdaptationDepth,
    PatternShiftModuleType,
    create_vak_adaptation_dependencies
)

# Создание зависимостей
dependencies = create_vak_adaptation_dependencies(
    api_key="your_api_key",
    adaptation_depth=AdaptationDepth.MODERATE,
    enable_safety_validation=True
)

# Инициализация агента
agent = PatternVAKAdaptationAgent(dependencies=dependencies)

# Контент для адаптации
content = {
    "title": "Техника якорения",
    "content": """
    Сядьте удобно и вспомните момент максимальной уверенности.
    Усильте это ощущение и сожмите кулак.
    Повторите несколько раз для закрепления связи.
    """,
    "module_type": PatternShiftModuleType.TECHNIQUE
}

# Создание запроса
request = VAKAdaptationRequest(
    content=content,
    target_modality=VAKModalityType.VISUAL,
    adaptation_depth=AdaptationDepth.MODERATE,
    preserve_core_message=True
)

# Выполнение адаптации
response = await agent.adapt_content(request)

if response.success:
    print(f"Адаптированный контент: {response.adapted_content}")
    print(f"Качество адаптации: {response.adaptation_quality_score}")
else:
    print(f"Ошибка: {response.error_message}")
```

### Анализ VAK модальностей

```python
# Анализ исходного контента
analysis = await agent.analyze_content(
    content=content,
    include_recommendations=True
)

print(f"Доминирующая модальность: {analysis['dominant_modality']}")
print(f"Scores: {analysis['modality_scores']}")
print(f"Найденные предикаты: {analysis['predicates_found']}")
print(f"Рекомендации: {analysis['recommendations']}")
```

### Создание мультимодальных вариантов

```python
# Создание версий для всех модальностей
variants = await agent.create_multimodal_variants(
    content=content,
    include_original=True,
    include_validation=True
)

for modality, variant in variants.items():
    print(f"\n{modality.upper()}:")
    print(f"Заголовок: {variant['title']}")
    print(f"Качество: {variant.get('validation_score', 'N/A')}")
```

### Батчевая обработка

```python
from pattern_vak_adaptation_specialist import BatchVAKAdaptationRequest

# Подготовка батча контента
content_list = [content1, content2, content3]
target_modalities = [
    VAKModalityType.VISUAL,
    VAKModalityType.AUDITORY,
    VAKModalityType.KINESTHETIC
]

batch_request = BatchVAKAdaptationRequest(
    content_list=content_list,
    target_modalities=target_modalities,
    adaptation_depth=AdaptationDepth.MODERATE
)

# Батчевая обработка
batch_response = await agent.adapt_content_batch(batch_request)

print(f"Успешных адаптаций: {batch_response.successful_adaptations}")
print(f"Неудачных: {batch_response.failed_adaptations}")
```

## 🎨 Примеры конфигураций

### Терапевтический контекст

```python
# Максимальная безопасность для терапии
therapy_deps = create_vak_adaptation_dependencies(
    api_key="your_api_key",
    adaptation_depth=AdaptationDepth.DEEP,
    trauma_informed_adaptations=True,
    preserve_therapeutic_integrity=True,
    safety_keywords=["безопасно", "комфортно", "границы"],
    therapeutic_frameworks=["trauma-informed", "person-centered"]
)

therapy_agent = PatternVAKAdaptationAgent(dependencies=therapy_deps)
```

### Коучинговый контекст

```python
# Фокус на достижениях для коучинга
coaching_deps = create_vak_adaptation_dependencies(
    api_key="your_api_key",
    adaptation_depth=AdaptationDepth.MODERATE,
    enable_multimodal=True,
    batch_adaptation_size=10,
    knowledge_tags=["coaching", "goal-achievement", "performance"]
)

coaching_agent = PatternVAKAdaptationAgent(dependencies=coaching_deps)
```

### Образовательный контекст

```python
# Быстрая адаптация для образования
education_deps = create_vak_adaptation_dependencies(
    api_key="your_api_key",
    adaptation_depth=AdaptationDepth.SURFACE,
    max_adaptation_time_seconds=15.0,
    knowledge_tags=["education", "learning-styles", "accessibility"]
)

education_agent = PatternVAKAdaptationAgent(dependencies=education_deps)
```

## 📚 Работа с примерами

Агент включает богатую библиотеку готовых примеров для различных типов контента:

```python
from pattern_vak_adaptation_specialist.examples import (
    get_example_for_module_type,
    get_all_available_examples,
    get_recommended_config_for_context,
    create_multi_modal_example_set
)

# Получение примера для конкретного типа модуля
example = get_example_for_module_type(
    module_type=PatternShiftModuleType.MEDITATION,
    modality=VAKModalityType.KINESTHETIC,
    specific_technique="breath_awareness"
)

# Просмотр всех доступных примеров
all_examples = get_all_available_examples()
print("Доступные НЛП техники:", all_examples["nlp_techniques"])
print("Доступные медитации:", all_examples["meditation_practices"])

# Рекомендуемая конфигурация для контекста
config = get_recommended_config_for_context(
    context="therapy",
    api_key="your_api_key"
)

# Создание полного набора примеров для техники
example_set = create_multi_modal_example_set(
    technique_name="anchoring",
    module_type=PatternShiftModuleType.TECHNIQUE
)
```

## 🧪 Тестирование

Проект включает комплексное тестирование:

```bash
# Запуск всех тестов
pytest tests/

# Запуск с покрытием кода
pytest tests/ --cov=pattern_vak_adaptation_specialist --cov-report=html

# Запуск конкретного модуля тестов
pytest tests/test_agent.py -v

# Запуск интеграционных тестов
pytest tests/test_integration.py -v

# Запуск только быстрых тестов
pytest tests/ -m "not slow"
```

### Структура тестов

- **test_dependencies.py** - тесты системы зависимостей и типов
- **test_tools.py** - тесты инструментов VAK адаптации
- **test_agent.py** - тесты основного агента
- **test_integration.py** - интеграционные тесты с PatternShift
- **test_examples.py** - тесты системы примеров

## 🔧 Расширение функциональности

### Добавление новых типов модулей

1. Добавьте новый тип в `PatternShiftModuleType`:

```python
class PatternShiftModuleType(Enum):
    # ... существующие типы
    NEW_MODULE = "new_module"
```

2. Создайте примеры адаптации в `examples/`:

```python
def get_new_module_example(modality: VAKModalityType) -> Dict[str, Any]:
    # Реализация примера
    pass
```

3. Обновите функцию `get_example_for_module_type` в `examples/__init__.py`

### Добавление новых сенсорных предикатов

Обновите константы в `dependencies.py`:

```python
VISUAL_PREDICATES = [
    # ... существующие предикаты
    "новый_визуальный_предикат"
]
```

### Кастомные валидаторы безопасности

```python
from pattern_vak_adaptation_specialist.tools import validate_safety_requirements

async def custom_safety_validator(content: Dict[str, Any]) -> Dict[str, Any]:
    # Ваша логика валидации
    return {
        "is_safe": True,
        "safety_score": 0.9,
        "custom_checks": ["passed"]
    }
```

## 🔍 Интеграция с Archon

Агент полностью интегрирован с Archon MCP Server для доступа к базе знаний:

```python
# Поиск в базе знаний
from pattern_vak_adaptation_specialist.tools import search_vak_knowledge_base

knowledge_results = await search_vak_knowledge_base(
    dependencies=dependencies,
    query="кинестетическая адаптация медитации",
    search_type="techniques",
    modality_filter=VAKModalityType.KINESTHETIC
)
```

### Загрузка базы знаний в Archon

1. Откройте Archon: http://localhost:3737/
2. Перейдите в Knowledge Base → Upload
3. Загрузите файл `knowledge/pattern_vak_adaptation_specialist_knowledge.md`
4. Добавьте теги: `pattern-vak-adaptation`, `agent-knowledge`, `pydantic-ai`, `psychology`
5. Привяжите к проекту PatternShift в разделе Sources

## 🛡️ Безопасность и этика

### Травма-информированный подход

Агент реализует принципы травма-информированного подхода:

- **Безопасность** - адаптации не содержат потенциально триггерных элементов
- **Выбор** - пользователь всегда может остановить или изменить процесс
- **Сотрудничество** - агент предлагает варианты, а не навязывает решения
- **Доверие** - прозрачность в работе алгоритмов адаптации

### Валидация безопасности

```python
# Автоматическая проверка безопасности
response = await agent.adapt_content(request)

if "safety_score" in response.adaptation_metadata:
    safety_score = response.adaptation_metadata["safety_score"]
    if safety_score < 0.7:
        print("⚠️ Низкий уровень безопасности адаптации")
```

### Сохранение терапевтической целостности

Агент автоматически проверяет сохранение ключевых терапевтических элементов:

- Основная цель техники
- Ключевые инструкции
- Терапевтические границы
- Этические принципы

## 📊 Мониторинг и аналитика

### Метрики качества

Агент отслеживает различные метрики:

```python
# Доступ к метрикам производительности
metadata = response.adaptation_metadata
print(f"Время обработки: {metadata['processing_time']}s")
print(f"Качество адаптации: {response.adaptation_quality_score}")
print(f"Сохранение смысла: {metadata.get('core_preservation_score', 'N/A')}")
```

### Логирование

Настройте логирование для отслеживания работы:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pattern_vak_adaptation")

# Агент автоматически логирует ключевые события
```

## 🔄 Обновления и поддержка

### Версионность

Агент использует семантическое версионирование:
- **Major** - кардинальные изменения API
- **Minor** - новая функциональность
- **Patch** - исправления и улучшения

### Обратная связь

Для улучшения агента собирается обратная связь:

```python
# Отправка обратной связи о качестве адаптации
feedback = {
    "adaptation_id": response.adaptation_id,
    "user_rating": 4.5,
    "comments": "Отличная адаптация для визуальной модальности"
}
```

## 📞 Поддержка

### Документация

- **Техническая документация** - в папке `knowledge/`
- **Примеры использования** - в папке `examples/`
- **API Reference** - автогенерируемая из docstrings

### Сообщество

- **Issues** - для багов и предложений функций
- **Discussions** - для вопросов и обсуждений
- **Wiki** - для расширенной документации

## 📄 Лицензия

Проект лицензирован под MIT License. См. файл LICENSE для подробностей.

## 🙏 Благодарности

- **PatternShift** - за основу психологических трансформаций
- **Pydantic AI** - за отличный фреймворк для агентов
- **Archon** - за систему управления проектами и базу знаний
- **Сообщество психологов** - за экспертизу в области VAK модальностей

---

*Pattern VAK Adaptation Specialist Agent - делаем психологические техники доступными для всех типов восприятия* 🧠✨