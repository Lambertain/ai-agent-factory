# 🛡️ NLP Content Quality Guardian Agent

Универсальный агент для валидации качества NLP контента и программ трансформации с использованием методологии PatternShift 2.0, строгих стандартов безопасности и этических принципов.

## ✨ Ключевые особенности

### 🎯 Универсальная валидация
- **Любые домены**: психология, астрология, таро, нумерология, e-commerce, SaaS, блоги, CRM
- **Любые типы контента**: тесты, программы трансформации, NLP техники, базы знаний
- **Адаптивные критерии**: автоматическая настройка под специфику домена

### 🔬 4-этапный процесс валидации
1. **🔍 Immersion** - глубокое изучение контента и понимание контекста
2. **📝 Draft** - создание детального отчета о найденных проблемах
3. **🎯 Analysis** - критический анализ влияния проблем на пользователя
4. **⚡ Improvement** - конкретные рекомендации по улучшению

### 🛡️ Строгие стандарты безопасности
- **Критические флаги**: автоматическое выявление потенциально вредного контента
- **Этическая валидация**: проверка соответствия профессиональным стандартам
- **Возрастная адекватность**: адаптация под целевую аудиторию
- **Культурная чувствительность**: учет ментальности и традиций

### 💰 Оптимизация затрат
- **Умная маршрутизация**: автоматический выбор оптимальной модели для задачи
- **Batch API Gemini**: 50% скидка при батчевой обработке
- **Контекстное кэширование**: снижение затрат на повторные запросы
- **Адаптивное сжатие**: оптимизация контекста для больших документов

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать агента
git clone <repository-url>
cd nlp_content_quality_guardian_agent

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env с вашими API ключами
```

### Базовое использование

```python
from nlp_content_quality_guardian_agent import validate_content_quality

# Валидация контента
result = await validate_content_quality(
    content="Ваш контент для валидации...",
    content_type="transformation_program",
    validation_domain="psychology",
    deep_analysis=True
)

print(result)  # Детальный отчет о качестве
```

## 📋 Типы валидации

### 🧠 Психологический контент

```python
from nlp_content_quality_guardian_agent import validate_test_quality

# Валидация психологического теста
result = await validate_test_quality(
    test_content="""
    # Тест на уровень стресса
    1. Как часто вы чувствуете усталость?
    а) Почти никогда
    б) Иногда
    в) Часто
    г) Постоянно
    """,
    domain="psychology",
    min_questions=15
)
```

### 🔄 Программы трансформации PatternShift

```python
from nlp_content_quality_guardian_agent import validate_transformation_program

# Валидация программы трансформации
result = await validate_transformation_program(
    program_content="""
    # Программа "Путь к гармонии" - 56 дней

    ## Этап 1: Кризис (21 день)
    День 1: Осознание текущего состояния
    - Визуальное упражнение: карта эмоций
    - Аудио-медитация на принятие
    - Кинестетическая практика заземления
    """,
    domain="psychology",
    check_vak_adaptation=True
)
```

### 🎯 NLP техники

```python
from nlp_content_quality_guardian_agent import validate_nlp_technique_safety

# Валидация безопасности NLP техники
result = await validate_nlp_technique_safety(
    technique_content="""
    # Техника рефрейминга для тревожности

    ## Описание
    Помогает изменить восприятие тревожных ситуаций

    ## Инструкции
    1. Определите тревожную мысль
    2. Найдите альтернативную интерпретацию
    3. Закрепите новое восприятие

    ## Противопоказания
    Не рекомендуется при острых расстройствах
    """,
    technique_type="reframing",
    target_audience="adults"
)
```

## 🌐 Универсальные конфигурации

### Примеры для разных доменов

```python
from nlp_content_quality_guardian_agent.examples import (
    create_psychology_validation_config,
    create_ecommerce_validation_config,
    create_astrology_validation_config
)

# Психологический контент с повышенными требованиями
psychology_config = create_psychology_validation_config("your-api-key")

# E-commerce с этическими проверками
ecommerce_config = create_ecommerce_validation_config("your-api-key")

# Астрологический контент с культурной чувствительностью
astrology_config = create_astrology_validation_config("your-api-key")
```

### Поддерживаемые домены

| Домен | Специфика | Требования |
|-------|-----------|------------|
| **Psychology** | Научная обоснованность | Evidence-based, этика, безопасность |
| **Astrology** | Символическая система | Культурное уважение, избегание фатализма |
| **Tarot** | Интерпретативная гибкость | Этичные чтения, уважение границ |
| **Numerology** | Математическая точность | Прозрачные вычисления, балансированность |
| **E-commerce** | Коммерческая этика | Честность, защита потребителей |
| **SaaS** | Техническая точность | API документация, безопасность |
| **Blog/CMS** | Контентные стандарты | Фактчекинг, SEO, читабельность |
| **CRM** | Приватность данных | GDPR, согласие, этика коммуникаций |

## 🛠️ Расширенные возможности

### Батчевая валидация

```python
from nlp_content_quality_guardian_agent import batch_validate_content

content_list = [
    {
        "id": "test_1",
        "content": "Контент 1...",
        "content_type": "test",
        "domain": "psychology"
    },
    {
        "id": "program_1",
        "content": "Контент 2...",
        "content_type": "transformation_program",
        "domain": "psychology"
    }
]

results = await batch_validate_content(
    content_list=content_list,
    optimize_costs=True
)
```

### Извлечение рекомендаций

```python
from nlp_content_quality_guardian_agent import get_quality_recommendations

recommendations = await get_quality_recommendations(
    validation_result=validation_output,
    priority_level="high"
)

print(recommendations)
# Структурированные рекомендации по приоритетам
```

### Быстрая проверка безопасности

```python
from nlp_content_quality_guardian_agent import quick_safety_check

is_safe = await quick_safety_check(
    content="Ваш контент...",
    target_audience="adults"
)

if not is_safe:
    print("⚠️ Контент требует дополнительной проверки")
```

## ⚙️ Конфигурация

### Основные настройки (.env)

```env
# API ключи
LLM_API_KEY=your_qwen_api_key
GEMINI_API_KEY=your_gemini_key

# Модели для разных задач
LLM_VALIDATION_MODEL=qwen2.5-72b-instruct      # Сложный анализ
LLM_SAFETY_MODEL=qwen2.5-coder-32b-instruct    # Проверка безопасности
LLM_REPORTING_MODEL=gemini-2.5-flash-lite      # Генерация отчетов

# Пороги качества
EXCELLENCE_THRESHOLD=90.0
GOOD_THRESHOLD=70.0
ACCEPTABLE_THRESHOLD=50.0

# PatternShift методология
MIN_TEST_QUESTIONS=15
REQUIRE_VAK_PERSONALIZATION=true
REQUIRE_THREE_LEVEL_STRUCTURE=true

# Безопасность
STRICT_SAFETY_MODE=true
AUTO_FLAG_MANIPULATION=true
AUTO_FLAG_PSEUDOSCIENCE=true
```

### Программная конфигурация

```python
from nlp_content_quality_guardian_agent import (
    create_psychology_quality_guardian_dependencies,
    NLPQualityGuardianSettings
)

# Создание зависимостей для психологии
dependencies = create_psychology_quality_guardian_dependencies(
    api_key="your-key",
    min_acceptable_score=85.0,  # Повышенные требования
    enable_deep_analysis=True,
    enable_safety_scanning=True
)

# Кастомные настройки
settings = NLPQualityGuardianSettings(
    llm_api_key="your-key",
    excellence_threshold=90.0,
    enable_cultural_validation=True,
    max_content_length=200000
)
```

## 📊 Система оценки

### Уровни качества

| Уровень | Балл | Описание | Действие |
|---------|------|----------|----------|
| 🟢 **ОТЛИЧНО** | 90-100% | Готово к публикации | Можно использовать без изменений |
| 🟡 **ХОРОШО** | 70-89% | Незначительные доработки | Минимальные правки |
| 🟠 **ТРЕБУЕТ УЛУЧШЕНИЯ** | 50-69% | Существенные правки | Значительная переработка |
| 🔴 **НЕПРИЕМЛЕМО** | <50% | Полная переработка | Создание заново |

### Критические флаги

- 🚨 **POTENTIALLY_HARMFUL** - потенциально вредные техники
- 🚨 **MANIPULATIVE_CONTENT** - манипулятивные элементы
- 🚨 **UNETHICAL_PRACTICE** - нарушение этических принципов
- 🚨 **PSEUDOSCIENTIFIC_CLAIM** - псевдонаучные утверждения
- 🚨 **LEGAL_VIOLATION** - возможное нарушение законодательства
- 🚨 **AGE_INAPPROPRIATE** - неподходящий для возраста контент

## 🔄 Интеграция с другими агентами

### Делегирование задач

```python
# В tools.py агента
await delegate_validation_task(
    ctx=ctx,
    target_agent="security_audit",
    task_title="Проверка критических уязвимостей",
    task_description="Найдены потенциально опасные элементы",
    content_sample=problematic_content,
    priority="high"
)
```

### Поддерживаемые агенты для делегирования

- **Security Audit Agent** - критические проблемы безопасности
- **NLP Content Research Agent** - поиск научных обоснований
- **Psychology Content Architect** - сложные психологические вопросы
- **Archon Analysis Lead** - системный анализ проблем

## 📈 Оптимизация производительности

### Стратегия выбора моделей

```python
# Автоматическая оптимизация затрат
model_manager = create_model_manager(settings)

# Разные модели для разных задач:
# - Qwen 72B для сложного анализа качества
# - Qwen Coder 32B для проверки безопасности
# - Gemini Flash Lite для генерации отчетов (в 10 раз дешевле!)

optimization_plan = model_manager.optimize_validation_pipeline(
    validation_tasks=[
        ValidationTaskType.DEEP_ANALYSIS,
        ValidationTaskType.SAFETY_CHECK,
        ValidationTaskType.REPORT_GENERATION
    ],
    content_length=50000
)
```

### Batch обработка

```python
# 50% скидка с Gemini Batch API
batch_plan = model_manager.create_batch_validation_plan(
    validation_requests=content_list
)

print(f"Оптимизации: {batch_plan['optimization_applied']}")
# ["Gemini Batch API для 10 запросов", "Кэширование контекста Qwen"]
```

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/ -v

# Тесты с покрытием
pytest --cov=nlp_content_quality_guardian_agent tests/

# Интеграционные тесты
pytest tests/integration/ -v
```

## 🎛️ Мониторинг и отладка

### Детальное логирование

```python
# В .env
LOG_LEVEL=DEBUG
ENABLE_DETAILED_LOGGING=true
TRACK_VALIDATION_METRICS=true

# Мониторинг производительности
ENABLE_PERFORMANCE_TRACKING=true
MAX_VALIDATION_TIME_SECONDS=300
```

### Метрики валидации

```python
from nlp_content_quality_guardian_agent.providers import create_model_manager

model_manager = create_model_manager()
stats = model_manager.get_model_performance_stats()

print(f"Самая эффективная модель: {stats['cost_efficiency_ranking'][0]}")
print(f"Самая производительная: {stats['performance_ranking'][0]}")
```

## 🤝 Участие в разработке

### Структура проекта

```
nlp_content_quality_guardian_agent/
├── agent.py                 # Основной агент
├── dependencies.py          # Зависимости и модели данных
├── tools.py                # Инструменты валидации
├── prompts.py              # Адаптивные промпты
├── settings.py             # Конфигурация и настройки
├── providers.py            # Провайдеры моделей и оптимизация
├── examples/               # Конфигурации для разных доменов
│   ├── psychology_validation_config.py
│   ├── universal_validation_config.py
│   └── spiritual_domains_config.py
├── knowledge/              # База знаний агента
│   └── nlp_content_quality_guardian_agent_knowledge.md
├── requirements.txt        # Зависимости Python
├── .env.example           # Пример настроек
└── README.md              # Документация
```

### Добавление нового домена

1. Создать конфигурацию в `examples/`
2. Добавить специфичные критерии валидации
3. Обновить промпты в `prompts.py`
4. Добавить тесты для нового домена

## 📚 База знаний

Агент использует обширную базу знаний (`knowledge/nlp_content_quality_guardian_agent_knowledge.md`):

- **Методология PatternShift 2.0** - трехуровневая система, VAK адаптация
- **NLP техники** - раппорт, рефрейминг, якорение, субмодальности
- **Эриксоновские паттерны** - трюизмы, пресуппозиции, встроенные команды
- **Критерии безопасности** - этические принципы, возрастная адекватность
- **Мультиязычные стандарты** - культурная адаптация, корректность перевода

### Загрузка в Archon Knowledge Base

```bash
# После создания агента загрузите базу знаний:
# 1. Откройте http://localhost:3737/
# 2. Knowledge Base → Upload
# 3. Загрузите nlp_content_quality_guardian_agent_knowledge.md
# 4. Теги: nlp-quality, patternshift, content-validation, agent-knowledge
```

## 🔧 Поиск проблем

### Частые проблемы

**Q: Ошибка "API key not found"**
```bash
# Проверьте .env файл
cat .env | grep API_KEY

# Убедитесь что .env загружается
python -c "from nlp_content_quality_guardian_agent import load_settings; print(load_settings())"
```

**Q: Низкое качество валидации**
```python
# Включите глубокий анализ
result = await validate_content_quality(
    content=your_content,
    deep_analysis=True,  # Использует более мощные модели
    validation_domain="psychology"  # Специфичные критерии
)
```

**Q: Высокие затраты на API**
```python
# Оптимизируйте через batch обработку
results = await batch_validate_content(
    content_list=content_list,
    optimize_costs=True  # Автоматическая оптимизация
)
```

**Q: RAG поиск работает нестабильно**
```python
# Агент включает fallback механизмы и диагностику проблем поиска
# Проверьте статус Archon Knowledge Base: http://localhost:3737/
```

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE) файл для деталей.

## 🙏 Благодарности

- **PatternShift 2.0 методология** - за комплексный подход к трансформации
- **Эриксоновский гипноз** - за этические принципы косвенного воздействия
- **NLP сообщество** - за стандарты безопасности и эффективности техник
- **Archon Project** - за платформу знаний и управления задачами

---

🛡️ **NLP Content Quality Guardian Agent** - ваш надежный страж качества и безопасности NLP контента!

*Генерировано с использованием [Claude Code](https://claude.ai/code)*