# Universal Domain Knowledge Extractor Agent

Универсальный агент для извлечения, структурирования и модуляризации знаний из любых доменов: психология, астрология, нумерология, бизнес и другие области.

## 🎯 Возможности

### Поддерживаемые домены
- **Психология**: Научные методики, валидированные тесты, терапевтические подходы
- **Астрология**: Системы домов, расчеты, культурные традиции
- **Нумерология**: Методы расчета, интерпретации, совместимость
- **Бизнес**: Фреймворки анализа, метрики, стратегическое планирование
- **Универсальные домены**: Адаптация под любую область знаний

### Основной функционал
- 🔍 **Извлечение знаний** из различных источников
- 🧩 **Модуляризация** для переиспользования
- 🔬 **Научная валидация** содержимого
- 🌍 **Мультиязычность** (украинский, польский, английский)
- 🎨 **Персонализация** под VAK типы и культуру

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка окружения
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

### Базовое использование
```python
from universal_domain_knowledge_extractor_agent import run_domain_knowledge_extraction

# Извлечение знаний для психологии
result = await run_domain_knowledge_extraction(
    message="Извлечь знания о депрессии и создать модули для диагностики",
    domain_type="psychology",
    project_type="transformation_platform"
)

# Извлечение знаний для астрологии
result = await run_domain_knowledge_extraction(
    message="Создать модули расчета гороскопов",
    domain_type="astrology",
    project_type="consultation_platform"
)
```

## ⚙️ Конфигурация

### Переменные окружения (.env)
```env
# Обязательные
LLM_API_KEY=your_api_key_here
DEFAULT_DOMAIN_TYPE=psychology
PRIMARY_LANGUAGE=ukrainian

# Опциональные
ARCHON_PROJECT_ID=your_project_id
KNOWLEDGE_BASE_URL=http://localhost:3737
```

### Конфигурация для разных доменов

#### Психология
```python
deps = load_dependencies(
    domain_type="psychology",
    project_type="transformation_platform"
)
# Автоматически включает научную валидацию и этические стандарты
```

#### Астрология
```python
deps = load_dependencies(
    domain_type="astrology",
    project_type="consultation_platform"
)
# Автоматически настраивает системы домов и культурные традиции
```

#### Бизнес
```python
deps = load_dependencies(
    domain_type="business",
    project_type="analytics_platform"
)
# Автоматически включает бизнес-фреймворки и метрики
```

## 🔧 API агента

### Основные инструменты

```python
# Извлечение знаний из источника
await extract_domain_knowledge(
    source_text="...",
    knowledge_type="concepts",  # concepts, methods, patterns, frameworks
    extraction_depth="comprehensive"  # surface, comprehensive, expert
)

# Анализ паттернов в знаниях
await analyze_knowledge_patterns(
    knowledge_data="...",
    pattern_type="structural"  # structural, semantic, behavioral
)

# Создание модулей знаний
await create_knowledge_modules(
    analyzed_patterns="...",
    module_type="functional"  # functional, data, presentation
)

# Поиск в базе знаний
await search_domain_knowledge(
    query="...",
    search_scope="comprehensive"  # focused, comprehensive, experimental
)

# Валидация структуры знаний
await validate_knowledge_structure(
    knowledge_modules="...",
    validation_criteria="scientific"  # basic, scientific, expert
)
```

### Коллективная работа

```python
# Разбивка на микрозадачи
await break_down_to_microtasks(
    main_task="...",
    complexity_level="medium"  # simple, medium, complex
)

# Проверка необходимости делегирования
await check_delegation_need(
    current_task="...",
    current_agent_type="domain_knowledge_extractor"
)

# Делегирование задач
await delegate_task_to_agent(
    target_agent="security_audit",
    task_title="...",
    task_description="..."
)
```

## 📁 Структура проекта

```
universal_domain_knowledge_extractor_agent/
├── agent.py                    # Основной агент
├── dependencies.py             # Зависимости и конфигурация
├── providers.py                # Провайдеры LLM моделей
├── settings.py                 # Настройки агента
├── tools.py                    # Инструменты извлечения знаний
├── prompts.py                  # Системные промпты
├── knowledge/                  # База знаний для RAG
│   └── universal_domain_knowledge_extractor_knowledge.md
├── requirements.txt            # Зависимости Python
├── .env.example               # Пример конфигурации
├── __init__.py                # Инициализация пакета
└── README.md                  # Документация
```

## 🎨 Примеры использования

### Создание психологических тестов

```python
# Извлечение знаний о депрессии
depression_knowledge = await extract_domain_knowledge(
    source_text=phq9_research_paper,
    knowledge_type="methods",
    extraction_depth="expert"
)

# Создание модулей теста
test_modules = await create_knowledge_modules(
    analyzed_patterns=depression_knowledge,
    module_type="functional"
)

# Результат: готовые модули для интеграции в PatternShift
```

### Создание астрологических расчетов

```python
# Извлечение знаний о системах домов
house_systems_knowledge = await extract_domain_knowledge(
    source_text=astrology_textbook,
    knowledge_type="frameworks",
    extraction_depth="comprehensive"
)

# Создание модулей расчета
calculation_modules = await create_knowledge_modules(
    analyzed_patterns=house_systems_knowledge,
    module_type="data"
)
```

### Создание бизнес-фреймворков

```python
# Извлечение SWOT анализа
swot_knowledge = await extract_domain_knowledge(
    source_text=business_strategy_book,
    knowledge_type="frameworks",
    extraction_depth="comprehensive"
)

# Создание применимых инструментов
business_tools = await create_knowledge_modules(
    analyzed_patterns=swot_knowledge,
    module_type="functional"
)
```

## 🔍 База знаний и RAG

### Загрузка в Archon Knowledge Base

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/universal_domain_knowledge_extractor_knowledge.md`
4. Добавьте теги: `universal-domain-knowledge-extractor`, `agent-knowledge`, `pydantic-ai`, `domain-extraction`

### Поиск через RAG

```python
# Поиск знаний по психологии
psychology_info = await search_domain_knowledge(
    query="методики диагностики депрессии",
    search_scope="comprehensive"
)

# Поиск знаний по астрологии
astrology_info = await search_domain_knowledge(
    query="системы домов плацидус",
    search_scope="focused"
)
```

## 🌍 Локализация

### Поддерживаемые языки
- **Украинский** (основной)
- **Польский**
- **Английский**

### Настройка языка
```python
deps = load_dependencies(
    domain_type="psychology",
    primary_language="ukrainian"  # ukrainian, polish, english
)
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Тестирование конкретного домена
pytest tests/test_psychology_extraction.py
pytest tests/test_astrology_extraction.py
pytest tests/test_business_extraction.py

# Тестирование с покрытием
pytest --cov=universal_domain_knowledge_extractor_agent
```

## 🤝 Интеграция с другими агентами

### Автоматическое делегирование
Агент автоматически делегирует специализированные задачи:
- **Security Audit Agent** → для проверки безопасности данных
- **RAG Agent** → для глубокого поиска информации
- **Performance Optimization Agent** → для оптимизации алгоритмов

### Пример совместной работы
```python
# При обнаружении задач безопасности
await delegate_task_to_agent(
    target_agent="security_audit",
    task_title="Аудит безопасности психологических данных",
    task_description="Проверить соответствие GDPR при обработке личных данных"
)
```

## 📊 Мониторинг и логирование

### Включение детального логирования
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SAVE_EXTRACTION_LOGS=true
```

### Просмотр логов
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Логи будут показывать:
# - Процесс извлечения знаний
# - Валидацию результатов
# - Делегирование задач
# - Ошибки и предупреждения
```

## 🛠️ Разработка и вклад

### Добавление нового домена

1. Обновите `dependencies.py`:
```python
domain_configs["new_domain"] = {
    "specific_config": "value"
}
```

2. Добавьте в `tools.py`:
```python
async def _extract_new_domain_knowledge(text, knowledge_type, config):
    # Логика извлечения для нового домена
    pass
```

3. Обновите `prompts.py`:
```python
def _get_new_domain_prompt(config):
    # Промпт для нового домена
    pass
```

### Стиль кода
- Следуйте PEP8
- Используйте type hints
- Документируйте функции
- Пишите тесты для новой функциональности

## 📝 Лицензия

AI Agent Factory - Универсальная система создания агентов

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте конфигурацию в `.env`
2. Убедитесь что загружена база знаний в Archon
3. Проверьте доступность LLM API
4. Посмотрите логи для диагностики

---

**Universal Domain Knowledge Extractor Agent** - ваш универсальный помощник для создания модульных систем знаний в любых доменах! 🚀