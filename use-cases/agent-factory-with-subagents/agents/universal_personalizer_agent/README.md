# Universal Personalizer Agent

Универсальный агент для персонализации контента и пользовательского опыта в различных доменах: психология, астрология, нумерология, бизнес и другие области. Построен на базе Pydantic AI с поддержкой многоуровневой персонализации, машинного обучения и кросс-культурной адаптации.

## 🎯 Основные возможности

- **Анализ профиля пользователя** для глубокой персонализации
- **Генерация персонализированного контента** под конкретные потребности
- **Создание правил персонализации** для автоматизации процессов
- **Адаптация контента** под культурный и языковой контекст
- **Отслеживание эффективности** персонализации в реальном времени
- **Оптимизация пользовательского опыта** через A/B тестирование
- **Коллективная работа** с другими агентами для комплексных решений

## 🌐 Универсальность

Агент разработан как полностью универсальное решение:
- ✅ **0% проект-специфичного кода** - работает с любыми проектами
- ✅ **Конфигурируемые настройки** через environment variables
- ✅ **Адаптивные промпты** под различные домены и технологии
- ✅ **Множественные примеры** конфигураций для разных областей
- ✅ **Кросс-доменная персонализация** - один агент для всех задач

## 📁 Структура проекта

```
universal_personalizer_agent/
├── agent.py                    # Основной агент с точками входа
├── dependencies.py             # Управление зависимостями и конфигурация
├── tools.py                    # Инструменты персонализации и анализа
├── prompts.py                  # Адаптивные промпты под домены
├── providers.py                # Оптимизированная система LLM моделей
├── settings.py                 # Конфигурируемые параметры
├── knowledge/                  # База знаний агента
│   └── universal_personalizer_knowledge.md
├── __init__.py                 # Инициализация пакета
├── requirements.txt            # Python зависимости
├── .env.example               # Шаблон конфигурации
└── README.md                  # Документация
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и настройте параметры:

```bash
cp .env.example .env
```

Минимальная конфигурация:
```env
# Основные настройки
LLM_API_KEY=your_api_key_here
DOMAIN_TYPE=psychology
PROJECT_TYPE=transformation_platform
PERSONALIZATION_MODE=adaptive

# LLM провайдер
LLM_PROVIDER=qwen
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 3. Базовое использование

```python
from universal_personalizer_agent import run_personalization_task

# Персонализация для психологической платформы
result = await run_personalization_task(
    message="Создай персонализированную терапевтическую программу для пользователя с тревожностью",
    domain_type="psychology",
    project_type="transformation_platform",
    personalization_mode="adaptive"
)

print(result)
```

## 🎨 Примеры конфигураций

### Психологическая терапевтическая платформа

```env
DOMAIN_TYPE=psychology
PROJECT_TYPE=transformation_platform
PERSONALIZATION_MODE=adaptive
PERSONALIZATION_DEPTH=deep
ADAPTATION_STRATEGY=dynamic
PRIVACY_PROTECTION_LEVEL=maximum
PSYCHOLOGY_PERSONALIZATION_FACTORS=personality_traits,therapeutic_goals,cultural_background,psychological_state
```

```python
result = await run_personalization_task(
    message="Создай персонализированную программу работы с тревожностью",
    domain_type="psychology",
    project_type="transformation_platform"
)
```

### Астрологический консультационный сервис

```env
DOMAIN_TYPE=astrology
PROJECT_TYPE=consultation_platform
PERSONALIZATION_MODE=hybrid
CULTURAL_ADAPTATION=true
CONTENT_ADAPTATION=comprehensive
ASTROLOGY_PERSONALIZATION_FACTORS=birth_chart_data,cultural_tradition,experience_level,spiritual_orientation
```

```python
result = await run_personalization_task(
    message="Персонализируй астрологические интерпретации под культурный контекст пользователя",
    domain_type="astrology",
    project_type="consultation_platform"
)
```

### Нумерологическая бизнес-консультация

```env
DOMAIN_TYPE=numerology
PROJECT_TYPE=business_consultancy
PERSONALIZATION_MODE=rule_based
LEARNING_APPROACH=preference_based
NUMEROLOGY_PERSONALIZATION_FACTORS=core_numbers,life_path,cultural_context,application_purpose
```

```python
result = await run_personalization_task(
    message="Создай персонализированную бизнес-стратегию на основе нумерологических данных",
    domain_type="numerology",
    project_type="business_consultancy"
)
```

### Бизнес-аналитическая платформа

```env
DOMAIN_TYPE=business
PROJECT_TYPE=analytics_platform
PERSONALIZATION_MODE=ml_driven
RECOMMENDATION_ALGORITHM=hybrid
A_B_TESTING_ENABLED=true
REAL_TIME_OPTIMIZATION=true
BUSINESS_PERSONALIZATION_FACTORS=industry_sector,company_size,role_level,business_goals
```

```python
result = await run_personalization_task(
    message="Адаптируй бизнес-рекомендации под роль и индустрию пользователя",
    domain_type="business",
    project_type="analytics_platform"
)
```

### E-commerce персонализация

```env
DOMAIN_TYPE=business
PROJECT_TYPE=ecommerce_platform
USER_SEGMENTATION=behavioral
REAL_TIME_OPTIMIZATION=true
RECOMMENDATION_ALGORITHM=collaborative
```

```python
result = await run_personalization_task(
    message="Создай персонализированные рекомендации товаров на основе поведения пользователя",
    domain_type="business",
    project_type="ecommerce_platform"
)
```

## 🔧 Основные функции

### Анализ профиля пользователя

```python
from universal_personalizer_agent import run_user_profile_analysis

result = await run_user_profile_analysis(
    user_data={
        "demographics": {"age": 25, "location": "Ukraine"},
        "behavior": {"session_duration": 30, "interaction_count": 15},
        "preferences": {"communication_style": "formal", "content_type": "visual"}
    },
    domain_type="psychology"
)
```

### Персонализация контента

```python
from universal_personalizer_agent import run_content_personalization

result = await run_content_personalization(
    base_content="Базовый психологический материал о тревожности",
    user_profile={
        "personality_type": "introvert",
        "anxiety_level": "moderate",
        "cultural_background": "eastern_european"
    },
    personalization_goals=["reduce_anxiety", "increase_self_awareness"]
)
```

### Оптимизация пользовательского опыта

```python
from universal_personalizer_agent import run_ux_optimization

result = await run_ux_optimization(
    current_interface={
        "layout": "grid",
        "colors": ["blue", "white"],
        "navigation": "sidebar"
    },
    user_feedback={
        "usability_score": 3.5,
        "satisfaction": 4.0,
        "completion_rate": 0.7
    },
    optimization_goals=["increase_engagement", "improve_accessibility"]
)
```

## 🎛️ Режимы персонализации

### Адаптивная персонализация (Adaptive)
- **Применение**: Максимальная гибкость и отзывчивость
- **Алгоритмы**: Машинное обучение, reinforcement learning
- **Идеально для**: Психологические платформы, астрологические сервисы

### Основанная на правилах (Rule-based)
- **Применение**: Четкие критерии персонализации
- **Алгоритмы**: Логические правила, деревья решений
- **Идеально для**: Нумерологические расчеты, корпоративные системы

### Управляемая ML (ML-driven)
- **Применение**: Большие данные для обучения
- **Алгоритмы**: Collaborative filtering, deep learning
- **Идеально для**: E-commerce, аналитические системы

### Гибридная (Hybrid)
- **Применение**: Комбинация различных подходов
- **Алгоритмы**: Ансамбли методов, meta-learning
- **Идеально для**: Комплексные многофункциональные системы

## 🌍 Культурная адаптация

Агент поддерживает автоматическую адаптацию под различные культуры:

```env
CULTURAL_ADAPTATION=true
PRIMARY_LANGUAGE=ukrainian
SECONDARY_LANGUAGES=polish,english
TARGET_REGIONS=ukraine,poland
```

Поддерживаемые аспекты:
- **Локализация контента** по регионам
- **Языковая адаптация** с учетом формальности
- **Культурные особенности** в астрологических и психологических подходах
- **Региональные стандарты** форматирования данных

## 🔒 Приватность и безопасность

Агент реализует принципы Privacy by Design:

```env
PRIVACY_PROTECTION_LEVEL=high
DATA_ANONYMIZATION=true
CONSENT_MANAGEMENT=true
DATA_RETENTION_DAYS=365
```

Функции безопасности:
- **Анонимизация данных** с настраиваемыми уровнями
- **Управление согласием** пользователей
- **Шифрование данных** персонализации
- **Соблюдение GDPR** и других стандартов

## 📊 Алгоритмы персонализации

### Коллаборативная фильтрация
```python
# Пример конфигурации
RECOMMENDATION_ALGORITHM=collaborative
SIMILARITY_THRESHOLD=0.7
MIN_INTERACTION_COUNT=5
```

### Контентная фильтрация
```python
# Пример конфигурации
RECOMMENDATION_ALGORITHM=content_based
CONTENT_FRESHNESS_WEIGHT=0.3
PERSONALIZATION_CONFIDENCE_THRESHOLD=0.6
```

### Гибридные рекомендации
```python
# Пример конфигурации
RECOMMENDATION_ALGORITHM=hybrid
PERSONALIZATION_WEIGHTS=relevance:0.25,engagement:0.20,satisfaction:0.20,effectiveness:0.15,accuracy:0.10,usability:0.10
```

## 🧪 A/B тестирование

```env
A_B_TESTING_ENABLED=true
REAL_TIME_OPTIMIZATION=true
```

Агент автоматически:
- Создает A/B эксперименты для новых персонализаций
- Отслеживает ключевые метрики эффективности
- Оптимизирует алгоритмы на основе результатов
- Предоставляет детальную аналитику экспериментов

## 🔄 Интеграция с другими агентами

Агент поддерживает коллективную работу:

```env
ENABLE_TASK_DELEGATION=true
DELEGATION_THRESHOLD=medium
MAX_DELEGATION_DEPTH=3
```

Возможные делегирования:
- **Security Audit Agent** - для проверки безопасности персонализации
- **RAG Agent** - для поиска специализированных знаний
- **UI/UX Enhancement Agent** - для улучшения интерфейсов
- **Performance Optimization Agent** - для оптимизации алгоритмов

## 🎯 Метрики эффективности

Агент отслеживает ключевые показатели:

- **Точность персонализации** (target: >0.7)
- **Удовлетворенность пользователей** (target: >0.85)
- **Коэффициент ошибок** (target: <0.05)
- **Время отклика** системы
- **Коэффициент конверсии** после персонализации

## 🛠️ Расширенная конфигурация

### Весовые коэффициенты
```env
PERSONALIZATION_WEIGHTS=relevance:0.25,engagement:0.20,satisfaction:0.20,effectiveness:0.15,accuracy:0.10,usability:0.10
USER_FEEDBACK_WEIGHT=0.4
BEHAVIORAL_DATA_WEIGHT=0.6
```

### Оптимизация производительности
```env
MAX_TOKENS=4096
TEMPERATURE=0.4
REQUEST_TIMEOUT=120
RETRY_ATTEMPTS=3
```

### Сегментация пользователей
```env
USER_SEGMENTATION=behavioral
SEGMENT_UPDATE_FREQUENCY=weekly
MAX_SEGMENTS_PER_USER=3
```

## 🔗 Интеграция с Archon Knowledge Base

Агент автоматически интегрируется с Archon для доступа к базе знаний:

```env
ARCHON_PROJECT_ID=c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
KNOWLEDGE_TAGS=personalization,user-experience,agent-knowledge,pydantic-ai
```

База знаний включает:
- Алгоритмы персонализации и их применение
- Доменно-специфичные практики и паттерны
- Этические принципы и требования безопасности
- Примеры успешных внедрений

## 📚 Документация и ресурсы

### Файлы знаний
- `knowledge/universal_personalizer_knowledge.md` - Полная база знаний агента

### Конфигурационные примеры
- `.env.example` - Шаблон настроек с комментариями
- Примеры для различных доменов в документации

### Зависимости
- `requirements.txt` - Все необходимые Python пакеты
- Поддержка ML библиотек: scikit-learn, surprise, implicit

## 🤝 Вклад в развитие

Агент разработан как часть AI Agent Factory и следует принципам:
- **Универсальности** - работа с любыми проектами типа
- **Модульности** - четкое разделение ответственности
- **Тестируемости** - полное покрытие unit-тестами
- **Документированности** - подробная документация всех компонентов

## 📄 Лицензия

Часть проекта AI Agent Factory. Использование в соответствии с лицензией проекта.

---

**Universal Personalizer Agent** - ваше универсальное решение для персонализации контента и пользовательского опыта в любых доменах с поддержкой машинного обучения, культурной адаптации и коллективной работы с другими агентами.