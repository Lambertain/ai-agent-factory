# Psychology Test Generator Agent

Универсальный агент для создания научно обоснованных психологических тестов, опросников и диагностических инструментов с поддержкой психометрической валидации и адаптации под различные популяции.

## 🎯 Основные возможности

### Генерация тестов
- **Психологические домены**: тревожность, депрессия, травма, личность, стресс, отношения
- **Популяции**: дети, подростки, взрослые, пожилые, люди с особыми потребностями
- **Типы тестов**: диагностические, скрининговые, оценка прогресса, исследовательские

### Психометрическая валидация
- Анализ надежности (альфа Кронбаха)
- Конструктная валидность
- Факторный анализ
- Обнаружение предвзятостей

### Адаптация тестов
- Языковые уровни (6-й, 8-й, 10-й класс, профессиональный)
- Культурная адаптация
- Возрастные особенности
- Особые потребности

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Конфигурация
1. Скопируйте `.env.example` в `.env`
2. Заполните необходимые переменные окружения:
```bash
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### Базовое использование
```python
from psychology_test_generator import (
    psychology_test_generator_agent,
    TestGenerationRequest,
    TestGeneratorDependencies,
    load_settings
)

# Загрузка настроек
settings = load_settings()

# Создание зависимостей
deps = TestGeneratorDependencies(
    api_key=settings.llm_api_key,
    psychological_domain="anxiety",
    target_population="adults",
    test_type="assessment"
)

# Генерация теста
async def generate_anxiety_test():
    request = TestGenerationRequest(
        domain="anxiety",
        population="adults",
        purpose="screening",
        question_count=15,
        response_format="frequency"
    )

    result = await psychology_test_generator_agent.run(
        user_prompt=f"Создай тест для скрининга тревожности: {request.model_dump_json()}",
        deps=deps
    )

    return result.data

# test = asyncio.run(generate_anxiety_test())
```

## 📊 Поддерживаемые домены и популяции

### Психологические домены
- `anxiety` - Тревожные расстройства
- `depression` - Депрессивные расстройства
- `trauma` - Травматические расстройства
- `personality` - Личностные черты
- `stress` - Стресс и совладание
- `relationships` - Качество отношений
- `cognitive` - Когнитивные функции
- `behavioral` - Поведенческие паттерны
- `general` - Общая психологическая оценка

### Целевые популяции
- `children` (6-12 лет) - Упрощенная лексика, визуальные элементы
- `adolescents` (13-17 лет) - Современная лексика, цифровые форматы
- `adults` (18-64 года) - Стандартные формулировки
- `elderly` (65+ лет) - Крупный шрифт, простые технологии
- `special_needs` - Адаптированные форматы

## 🛠️ API агента

### Основные функции

#### create_psychological_test()
Создание индивидуального психологического теста
```python
test = await create_psychological_test(
    domain="depression",
    population="adults",
    question_count=18,
    response_format="frequency"
)
```

#### create_test_battery()
Создание батареи тестов для комплексной оценки
```python
battery = await create_test_battery(
    domains=["anxiety", "depression", "stress"],
    population="adults",
    assessment_type="comprehensive"
)
```

#### adapt_test_for_population()
Адаптация существующего теста под новую популяцию
```python
adapted_test = await adapt_test_for_population(
    original_test=test,
    target_population="adolescents",
    adaptation_type="full"
)
```

### Доступные инструменты

- `generate_test_questions()` - Генерация вопросов теста
- `create_scoring_system()` - Создание системы подсчета баллов
- `validate_test_content()` - Валидация содержания теста
- `analyze_psychometric_properties()` - Психометрический анализ
- `adapt_for_population()` - Адаптация под популяцию
- `search_psychology_knowledge()` - Поиск в базе знаний

## 🔧 Конфигурация

### Основные настройки
```python
# settings.py
class PsychologyTestGeneratorSettings(BaseSettings):
    # LLM настройки
    llm_model: str = "qwen2.5-coder-32b-instruct"
    llm_api_key: str = Field(..., description="API ключ")

    # Настройки тестов
    default_psychological_domain: str = "general"
    default_target_population: str = "adults"
    min_question_count: int = 5
    max_question_count: int = 100

    # Психометрические стандарты
    min_reliability_threshold: float = 0.70
    enable_automatic_validation: bool = True
```

### Доменные настройки
```python
# Получение настроек для конкретного домена
anxiety_settings = get_domain_specific_settings("anxiety")
# {
#     "preferred_response_format": "frequency",
#     "typical_question_count": 21,
#     "reliability_threshold": 0.85,
#     "specialized_subscales": ["general_anxiety", "social_anxiety", "panic", "worry"]
# }
```

### Популяционные настройки
```python
# Получение настроек для целевой популяции
children_settings = get_population_specific_settings("children")
# {
#     "language_level": "grade_6",
#     "max_question_count": 15,
#     "time_limit_minutes": 10,
#     "visual_aids_required": True
# }
```

## 🧪 Психометрические стандарты

### Надежность
- **Клинические тесты**: α ≥ 0.85
- **Исследовательские тесты**: α ≥ 0.80
- **Скрининговые тесты**: α ≥ 0.75
- **Экспериментальные тесты**: α ≥ 0.70

### Валидность
- **Содержательная**: Экспертная оценка и теоретическое обоснование
- **Конструктная**: Факторный анализ и конвергентная/дискриминантная валидность
- **Критериальная**: Корреляция с установленными методиками
- **Прогностическая**: Предсказание долгосрочных результатов

### Размер выборки
- **Пилотное исследование**: 50+ участников
- **Разработка теста**: 200+ участников
- **Валидация**: 500+ участников
- **Нормализация**: 1000+ участников

## 🌐 Интеграция с мультиагентной системой

### Связанные агенты
- **Psychology Research Agent** - Научное обоснование методик
- **Psychology Content Architect** - Архитектура психологических программ
- **Psychology Quality Guardian** - Контроль качества и этики

### Рабочий процесс
1. **Research Agent** → Научное обоснование конструкта
2. **Test Generator** → Создание тестовых вопросов
3. **Content Architect** → Интеграция в программу
4. **Quality Guardian** → Финальная валидация

### Делегирование задач
```python
# Автоматическое делегирование исследовательских задач
research_result = await delegate_to_research_agent(
    task="Анализ валидности конструкта тревожности",
    context={"domain": "anxiety", "population": "adults"}
)

# Делегирование контроля качества
quality_report = await delegate_to_quality_guardian(
    test_content=generated_test,
    validation_type="ethical_and_psychometric"
)
```

## 📋 Форматы экспорта

### Поддерживаемые форматы
- **JSON** - Структурированные данные
- **YAML** - Человекочитаемый формат
- **CSV** - Табличные данные
- **PDF** - Готовые к печати тесты
- **HTML** - Веб-версии тестов

### Пример экспорта
```python
# Экспорт в различные форматы
test_json = export_test(test, format="json")
test_pdf = export_test(test, format="pdf", include_scoring=True)
test_html = export_test(test, format="html", interactive=True)
```

## 🔒 Этические принципы

### Автоматические проверки
- **Информированное согласие** - Обязательные разделы согласия
- **Конфиденциальность** - Защита персональных данных
- **Культурная чувствительность** - Исключение предвзятостей
- **Предотвращение вреда** - Предупреждения о дистрессе

### Соответствие стандартам
- **ITC Guidelines** - Международные стандарты тестирования
- **APA Standards** - Этические принципы APA
- **GDPR/HIPAA** - Защита персональных данных

## 🧩 Примеры использования

### Создание теста на депрессию
```python
depression_test = await create_psychological_test(
    domain="depression",
    population="adults",
    question_count=18,
    response_format="frequency",
    subscales=["mood", "anhedonia", "cognitive", "somatic"]
)
```

### Адаптация теста для подростков
```python
teen_test = await adapt_test_for_population(
    original_test=adult_anxiety_test,
    target_population="adolescents",
    adaptations={
        "language_level": "grade_8",
        "contemporary_examples": True,
        "privacy_emphasis": True
    }
)
```

### Создание батареи тестов
```python
comprehensive_battery = await create_test_battery(
    domains=["anxiety", "depression", "stress", "personality"],
    population="adults",
    purpose="clinical_assessment",
    time_limit_minutes=45
)
```

## 📈 Мониторинг и аналитика

### Метрики качества
- Время генерации тестов
- Психометрические показатели
- Показатели успешности валидации
- Частота использования доменов

### Логирование
```python
import logging
logger = logging.getLogger("psychology_test_generator")
logger.info("Test generated successfully", extra={
    "domain": "anxiety",
    "population": "adults",
    "question_count": 15,
    "reliability": 0.87
})
```

## 🤝 Участие в разработке

### Структура проекта
```
psychology_test_generator/
├── agent.py              # Основной агент
├── dependencies.py       # Конфигурация зависимостей
├── tools.py              # Инструменты агента
├── prompts.py            # Системные промпты
├── settings.py           # Настройки приложения
├── knowledge/            # База знаний
│   └── psychology_test_generator_knowledge.md
├── examples/             # Примеры конфигураций
├── tests/                # Тесты
└── README.md
```

### Добавление нового домена
1. Обновите `DOMAIN_SPECIFIC_PROMPTS` в `prompts.py`
2. Добавьте настройки в `get_domain_specific_settings()`
3. Расширьте базу знаний
4. Создайте тесты для нового домена

### Добавление новой популяции
1. Обновите `POPULATION_ADAPTED_PROMPTS` в `prompts.py`
2. Добавьте настройки в `get_population_specific_settings()`
3. Создайте адаптационные правила
4. Протестируйте на целевой популяции

## 📚 Ресурсы и документация

### Психометрические ресурсы
- International Test Commission Guidelines
- American Psychological Association Standards
- Handbook of Psychological Assessment

### Научные основы
- Classical Test Theory
- Item Response Theory
- Modern psychometric methods

### Технические требования
- Python 3.8+
- pydantic-ai >= 0.0.15
- Доступ к LLM API (OpenAI, Qwen)

## 📞 Поддержка

Для вопросов и предложений:
- Создайте issue в репозитории
- Обратитесь к документации Archon
- Используйте встроенные инструменты диагностики

---

**Psychology Test Generator Agent** - часть универсальной мультиагентной системы для создания психологических программ и инструментов.