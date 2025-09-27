# Universal Opportunity Analyzer Agent

Универсальный агент для анализа возможностей и болевых точек в любых доменах: психология, астрология, нумерология, бизнес и другие области.

## 🎯 Возможности

### Поддерживаемые домены
- **Психология**: Диагностические платформы, терапевтические решения, образовательные программы
- **Астрология**: Консультационные сервисы, расчетные системы, мобильные приложения
- **Нумерология**: Сервисы расчетов, именование, бизнес-консультации
- **Бизнес**: Стратегический анализ, рыночные исследования, конкурентная разведка
- **Универсальные домены**: Адаптация под любую область деятельности

### Основной функционал
- 🔍 **Анализ возможностей** в конкретных рыночных сегментах
- 🎯 **Выявление болевых точек** целевой аудитории
- 📊 **Оценка рыночного потенциала** и конкурентной среды
- 🏆 **Расчет скоринга возможностей** для приоритизации
- 🌍 **Мультиязычность** (украинский, польский, английский)
- 🤝 **Коллективная работа** с другими агентами через делегирование

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
from universal_opportunity_analyzer_agent import run_opportunity_analysis

# Анализ возможностей для психологии
result = await run_opportunity_analysis(
    message="Проанализируй возможности создания платформы онлайн-диагностики депрессии для украинской аудитории",
    domain_type="psychology",
    project_type="transformation_platform"
)

# Анализ возможностей для астрологии
result = await run_opportunity_analysis(
    message="Оцени потенциал мобильного приложения персональных гороскопов с AI",
    domain_type="astrology",
    project_type="consultation_platform"
)
```

## ⚙️ Конфигурация

### Переменные окружения (.env)
```env
# Обязательные
LLM_API_KEY=your_api_key_here
DOMAIN_TYPE=psychology
PRIMARY_LANGUAGE=ukrainian

# Опциональные
ARCHON_PROJECT_ID=your_project_id
ANALYSIS_DEPTH=comprehensive
MARKET_SCOPE=regional
```

### Конфигурация для разных доменов

#### Психология
```python
deps = create_domain_config(
    domain_type="psychology",
    project_type="transformation_platform",
    analysis_depth="deep"
)
# Автоматически включает научную валидацию и этические стандарты
```

#### Астрология
```python
deps = create_domain_config(
    domain_type="astrology",
    project_type="consultation_platform",
    analysis_depth="comprehensive"
)
# Автоматически настраивает культурную чувствительность и точность расчетов
```

#### Бизнес
```python
deps = create_domain_config(
    domain_type="business",
    project_type="analytics_platform",
    analysis_depth="comprehensive"
)
# Автоматически включает ROI анализ и конкурентную разведку
```

## 🔧 API агента

### Основные инструменты

```python
# Анализ возможностей в домене
await analyze_domain_opportunities(
    market_segment="online_therapy",
    analysis_type="comprehensive",
    time_frame="current"
)

# Выявление болевых точек
await identify_pain_points(
    target_audience="young_adults_with_anxiety",
    research_depth="comprehensive"
)

# Оценка рыночного потенциала
await evaluate_market_potential(
    opportunity_type="ai_diagnostic_platform",
    geographic_scope="regional"
)

# Анализ конкурентной среды
await assess_competition_landscape(
    opportunity_area="mental_health_apps",
    analysis_depth="comprehensive"
)

# Расчет скоринга возможностей
await calculate_opportunity_score(
    opportunity_data="market_analysis_results",
    scoring_model="comprehensive"
)

# Поиск паттернов через RAG
await search_opportunity_patterns(
    query="successful mental health startups",
    pattern_type="market_trends"
)
```

### Коллективная работа

```python
# Разбивка на микрозадачи
await break_down_to_microtasks(
    main_task="Анализ возможностей создания астрологического сервиса",
    complexity_level="medium"
)

# Проверка необходимости делегирования
await check_delegation_need(
    current_task="Анализ безопасности психологических данных",
    current_agent_type="opportunity_analyzer"
)

# Делегирование задач
await delegate_task_to_agent(
    target_agent="security_audit",
    task_title="Аудит безопасности диагностической платформы",
    task_description="Проверить соответствие GDPR при обработке психологических данных"
)
```

## 📁 Структура проекта

```
universal_opportunity_analyzer_agent/
├── agent.py                    # Основной агент
├── dependencies.py             # Зависимости и конфигурация
├── providers.py                # Провайдеры LLM моделей с оптимизацией стоимости
├── settings.py                 # Настройки агента
├── tools.py                    # Инструменты анализа возможностей
├── prompts.py                  # Системные промпты
├── knowledge/                  # База знаний для RAG
│   └── universal_opportunity_analyzer_knowledge.md
├── requirements.txt            # Зависимости Python
├── .env.example               # Пример конфигурации
├── __init__.py                # Инициализация пакета
└── README.md                  # Документация
```

## 🎨 Примеры использования

### Анализ возможностей в психологии

```python
# Анализ рынка психологической диагностики
psychology_analysis = await analyze_domain_opportunities(
    market_segment="online_psychological_assessment",
    analysis_type="comprehensive",
    time_frame="current"
)

# Выявление болевых точек
pain_points = await identify_pain_points(
    target_audience="adults_with_depression",
    research_depth="comprehensive"
)

# Результат: комплексный анализ с рекомендациями
```

### Анализ возможностей в астрологии

```python
# Анализ рынка астрологических приложений
astrology_analysis = await analyze_domain_opportunities(
    market_segment="personalized_horoscope_apps",
    analysis_type="comprehensive",
    time_frame="current"
)

# Оценка конкурентной среды
competition = await assess_competition_landscape(
    opportunity_area="astrology_mobile_apps",
    analysis_depth="comprehensive"
)
```

### Анализ бизнес-возможностей

```python
# Анализ возможностей SaaS платформы
business_analysis = await analyze_domain_opportunities(
    market_segment="small_business_automation",
    analysis_type="comprehensive",
    time_frame="medium_term"
)

# Расчет скоринга возможностей
scoring = await calculate_opportunity_score(
    opportunity_data=business_analysis,
    scoring_model="comprehensive"
)
```

## 🔍 База знаний и RAG

### Загрузка в Archon Knowledge Base

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/universal_opportunity_analyzer_knowledge.md`
4. Добавьте теги: `universal-opportunity-analyzer`, `agent-knowledge`, `pydantic-ai`, `market-analysis`

### Поиск через RAG

```python
# Поиск паттернов возможностей
patterns = await search_opportunity_patterns(
    query="successful fintech startups Ukraine",
    pattern_type="market_trends"
)

# Поиск знаний по домену
domain_info = await search_opportunity_patterns(
    query="psychology platform market analysis",
    pattern_type="domain_insights"
)
```

## 🌍 Локализация

### Поддерживаемые языки
- **Украинский** (основной)
- **Польский**
- **Английский**

### Настройка языка
```python
deps = create_domain_config(
    domain_type="psychology",
    primary_language="ukrainian"  # ukrainian, polish, english
)
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Тестирование конкретного домена
pytest tests/test_psychology_analysis.py
pytest tests/test_astrology_analysis.py
pytest tests/test_business_analysis.py

# Тестирование с покрытием
pytest --cov=universal_opportunity_analyzer_agent
```

## 🤝 Интеграция с другими агентами

### Автоматическое делегирование
Агент автоматически делегирует специализированные задачи:
- **Security Audit Agent** → для анализа безопасности данных
- **RAG Agent** → для глубокого рыночного исследования
- **UI/UX Enhancement Agent** → для анализа пользовательского опыта
- **Performance Optimization Agent** → для оценки технических требований

### Пример совместной работы
```python
# При обнаружении задач безопасности
await delegate_task_to_agent(
    target_agent="security_audit",
    task_title="Аудит безопасности платформы ментального здоровья",
    task_description="Проверить соответствие HIPAA и GDPR при обработке медицинских данных"
)
```

## 📊 Мониторинг и логирование

### Включение детального логирования
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SAVE_ANALYSIS_LOGS=true
```

### Просмотр логов
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Логи будут показывать:
# - Процесс анализа возможностей
# - Результаты скоринга
# - Делегирование задач
# - Ошибки и предупреждения
```

## 🛠️ Разработка и вклад

### Добавление нового домена

1. Обновите `dependencies.py`:
```python
domain_configs["new_domain"] = {
    "pain_points_focus": ["specific", "pain", "points"],
    "opportunity_types": ["relevant", "opportunities"],
    "validation_criteria": {"domain": "specific"}
}
```

2. Добавьте в `tools.py`:
```python
async def _analyze_new_domain_opportunities(domain, segment, config):
    # Логика анализа для нового домена
    pass
```

3. Обновите `prompts.py`:
```python
def _get_domain_expertise(domain_type: str) -> str:
    domain_expertises["new_domain"] = """
    Экспертиза для нового домена...
    """
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

**Universal Opportunity Analyzer Agent** - ваш универсальный помощник для выявления и анализа возможностей в любых доменах! 🚀