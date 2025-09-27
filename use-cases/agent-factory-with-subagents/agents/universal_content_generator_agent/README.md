# Universal Content Generator Agent

Универсальный агент для создания высококачественного контента любого типа и для любой аудитории. Построен на базе Pydantic AI с поддержкой SEO оптимизации, культурной адаптации, A/B тестирования и коллективной работы с другими агентами.

## 🎯 Основные возможности

- **Универсальная генерация контента** - блоги, документация, маркетинг, образование, соцсети, email
- **Адаптация под аудитории** - от новичков до экспертов, разные демографические группы
- **SEO оптимизация** - keyword research, meta-теги, структурирование, internal linking
- **Культурная локализация** - адаптация под регионы, языки, культурные особенности
- **Валидация качества** - автоматическая проверка читабельности, структуры, SEO
- **A/B тестирование вариаций** - создание множественных версий для тестирования
- **Коллективная работа** - интеграция с SEO, UI/UX, локализационными агентами

## 🌐 Универсальность

Агент разработан как полностью универсальное решение:
- ✅ **0% проект-специфичного кода** - работает с любыми проектами и доменами
- ✅ **12+ типов контента** - от блог-постов до технической документации
- ✅ **10+ доменов** - технологии, бизнес, здоровье, образование, финансы, lifestyle
- ✅ **Множественные форматы** - Markdown, HTML, plain text, JSON
- ✅ **Культурная адаптация** - поддержка 3+ языков и региональных особенностей

## 📁 Структура проекта

```
universal_content_generator_agent/
├── agent.py                    # Основной агент с точками входа
├── dependencies.py             # Управление зависимостями и конфигурация
├── tools.py                    # Инструменты создания и оптимизации контента
├── prompts.py                  # Адаптивные промпты под типы и домены
├── providers.py                # Оптимизированная система LLM моделей
├── settings.py                 # Конфигурируемые параметры
├── knowledge/                  # База знаний агента
│   └── universal_content_generator_knowledge.md
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
CONTENT_TYPE=blog_post
DOMAIN_TYPE=technology
TARGET_AUDIENCE=general

# LLM провайдер
LLM_PROVIDER=qwen
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 3. Базовое использование

```python
from universal_content_generator_agent import run_content_generation_task

# Создание блог-поста
result = await run_content_generation_task(
    message="Создай статью о современных трендах в AI",
    content_type="blog_post",
    domain_type="technology",
    target_audience="professionals",
    seo_focus=True
)

print(result)
```

## 🎨 Примеры использования

### Блог-пост для технологической компании

```python
from universal_content_generator_agent import run_blog_post_generation

result = await run_blog_post_generation(
    topic="Как внедрить AI в бизнес-процессы в 2024 году",
    keywords=["artificial intelligence", "business automation", "digital transformation"],
    target_audience="executives",
    content_style="authoritative",
    word_count=1500,
    include_seo=True
)
```

**Конфигурация:**
```env
CONTENT_TYPE=blog_post
DOMAIN_TYPE=technology
TARGET_AUDIENCE=professionals
CONTENT_STYLE=informative
SEO_OPTIMIZATION=true
CONTENT_LENGTH=medium
```

### Техническая документация API

```python
from universal_content_generator_agent import run_documentation_generation

result = await run_documentation_generation(
    documentation_type="api",
    technical_level="intermediate",
    framework="FastAPI",
    include_examples=True,
    format_style="markdown"
)
```

**Конфигурация:**
```env
CONTENT_TYPE=documentation
DOMAIN_TYPE=technology
TARGET_AUDIENCE=developers
CONTENT_STYLE=technical
SEO_OPTIMIZATION=false
CONTENT_LENGTH=comprehensive
```

### Маркетинговая email кампания

```python
from universal_content_generator_agent import run_marketing_content_generation

result = await run_marketing_content_generation(
    campaign_type="email",
    product_category="SaaS",
    marketing_goal="conversion",
    tone="professional",
    call_to_action="Start Free Trial"
)
```

**Конфигурация:**
```env
CONTENT_TYPE=email
DOMAIN_TYPE=business
TARGET_AUDIENCE=customers
CONTENT_STYLE=persuasive
CONTENT_LENGTH=short
INCLUDE_CALL_TO_ACTION=true
```

### Образовательный курс

```python
from universal_content_generator_agent import run_educational_content_generation

result = await run_educational_content_generation(
    subject="Python для анализа данных",
    education_level="beginner",
    learning_style="hands-on",
    content_format="structured",
    include_assessments=True
)
```

**Конфигурация:**
```env
CONTENT_TYPE=educational
DOMAIN_TYPE=technology
TARGET_AUDIENCE=students
CONTENT_STYLE=educational
STORYTELLING_ELEMENTS=true
CONTENT_LENGTH=long
```

### Контент для социальных сетей

```python
from universal_content_generator_agent import run_social_media_generation

result = await run_social_media_generation(
    platform="linkedin",
    content_theme="thought leadership",
    post_type="carousel",
    engagement_goal="shares",
    hashtag_strategy="moderate"
)
```

**Конфигурация:**
```env
CONTENT_TYPE=social_media
DOMAIN_TYPE=business
TARGET_AUDIENCE=professionals
CONTENT_STYLE=engaging
CREATIVITY_LEVEL=creative
CONTENT_LENGTH=short
```

## 🔧 Расширенные функции

### Валидация качества контента

```python
from universal_content_generator_agent.tools import validate_content_quality

# Проверка качества созданного контента
validation_results = await validate_content_quality(
    ctx=context,
    content=generated_content,
    quality_criteria={
        "min_words": 800,
        "keywords": ["AI", "automation", "business"],
        "required_sections": ["introduction", "conclusion"]
    }
)

print(f"Качество контента: {validation_results['quality_percentage']}%")
print(f"Рекомендации: {validation_results['recommendations']}")
```

### Генерация вариаций для A/B тестирования

```python
from universal_content_generator_agent.tools import generate_content_variations

# Создание вариаций контента
variations = await generate_content_variations(
    ctx=context,
    base_content=original_content,
    variation_types=["tone", "style", "length"],
    variation_count=3
)

print("Создано вариаций:", len(variations))
for name, content in variations.items():
    print(f"Вариация {name}: {content[:100]}...")
```

### Анализ эффективности контента

```python
from universal_content_generator_agent.tools import extract_content_insights

# Анализ контента
insights = await extract_content_insights(
    ctx=context,
    content=published_content,
    insight_types=["readability", "seo", "engagement", "structure"]
)

print(f"Читабельность: {insights['readability']['readability_score']}")
print(f"SEO score: {insights['seo']['heading_structure']['good_hierarchy']}")
print(f"Engagement score: {insights['engagement']['engagement_score']}")
```

## 🎯 Типы контента

### Поддерживаемые типы

| Тип контента | Описание | Типичная длина | SEO важность |
|--------------|----------|----------------|--------------|
| `blog_post` | Блог-посты и статьи | 800-2500 слов | Высокая |
| `documentation` | Техническая документация | 500-5000+ слов | Средняя |
| `marketing` | Маркетинговые материалы | 100-1000 слов | Высокая |
| `educational` | Образовательный контент | 1000-3000 слов | Средняя |
| `social_media` | Посты для соцсетей | 50-300 символов | Средняя |
| `email` | Email кампании | 100-500 слов | Низкая |
| `press_release` | Пресс-релизы | 300-800 слов | Средняя |
| `white_paper` | Аналитические документы | 3000-8000 слов | Высокая |
| `case_study` | Кейс-стади | 1000-2000 слов | Высокая |
| `tutorial` | Обучающие материалы | 800-2000 слов | Высокая |

### Специализация по доменам

| Домен | Особенности | Ключевые элементы |
|-------|-------------|-------------------|
| `technology` | Техническая точность, примеры кода | Code examples, latest trends |
| `business` | ROI фокус, кейс-стади | Case studies, actionable advice |
| `health` | Evidence-based, безопасность | Expert review, disclaimers |
| `education` | Learning objectives, прогрессивность | Interactive elements, assessments |
| `finance` | Регуляторные требования, точность | Risk disclaimers, compliance |
| `lifestyle` | Личный подход, визуальные элементы | Trends, personal touch |

## 🌍 Культурная адаптация

### Поддерживаемые языки и регионы

```python
# Украинский рынок
await run_content_generation_task(
    message="Створи статтю про цифрові тренди в Україні",
    language="ukrainian",
    regional_preferences="ukraine",
    cultural_adaptation=True,
    local_references=True,
    currency_format="UAH"
)

# Польский рынок
await run_content_generation_task(
    message="Utwórz artykuł o trendach e-commerce w Polsce",
    language="polish",
    regional_preferences="poland",
    cultural_adaptation=True,
    currency_format="PLN"
)

# Международный рынок
await run_content_generation_task(
    message="Create article about global AI trends",
    language="english",
    regional_preferences="global",
    cultural_adaptation=False
)
```

### Культурные особенности

**Украина:**
- Формальное обращение в B2B контенте
- Упор на инновации и digital transformation
- Wartime context awareness
- Грн валюта, DD.MM.YYYY формат

**Польша:**
- EU regulatory compliance
- Traditional business values
- Central European context
- PLN валюта, EU стандарты

**Global:**
- Универсальные примеры
- International best practices
- Neutral cultural references
- USD валюта, международные форматы

## 🔍 SEO оптимизация

### Автоматическая SEO оптимизация

```python
from universal_content_generator_agent.tools import optimize_content_seo

# SEO оптимизация контента
optimized_content = await optimize_content_seo(
    ctx=context,
    content=raw_content,
    primary_keyword="artificial intelligence",
    secondary_keywords=["AI trends", "machine learning", "automation"],
    meta_requirements={
        "meta_description_length": 155,
        "title_length": 60,
        "include_schema_markup": True
    }
)
```

### SEO элементы

- **Keyword Integration**: Естественное включение ключевых слов
- **Title Optimization**: SEO-оптимизированные заголовки
- **Meta Descriptions**: Убедительные мета-описания 150-160 символов
- **Header Structure**: Логическая иерархия H1, H2, H3
- **Internal Linking**: Предложения по внутренним ссылкам
- **Schema Markup**: Structured data для rich snippets

### SEO метрики

```python
# Проверка SEO метрик
seo_analysis = insights['seo']
print(f"Keyword density: {seo_analysis['keyword_analysis']['keyword_density']}%")
print(f"Header structure: {seo_analysis['heading_structure']['good_hierarchy']}")
print(f"Internal links: {seo_analysis['internal_links']}")
```

## 📊 Система качества

### Автоматическая валидация

```python
# Комплексная проверка качества
quality_report = await validate_content_quality(
    ctx=context,
    content=content,
    quality_criteria={
        "min_words": 800,
        "max_words": 2500,
        "keywords": ["primary keyword"],
        "required_sections": ["introduction", "conclusion"],
        "readability_target": "general",
        "seo_optimization": True
    }
)

# Результаты
print(f"Общий балл качества: {quality_report['quality_percentage']}%")
print(f"Структура: {'✅' if quality_report['well_structured'] else '❌'}")
print(f"Читабельность: {'✅' if quality_report['readability_good'] else '❌'}")
print(f"SEO оптимизация: {'✅' if quality_report.get('optimal_keyword_density') else '❌'}")
```

### Метрики качества

| Метрика | Целевое значение | Описание |
|---------|------------------|----------|
| **Quality Score** | > 70% | Общий балл качества |
| **Readability** | General level | Подходящий уровень читабельности |
| **Keyword Density** | 1-2.5% | Оптимальная плотность ключевых слов |
| **Structure Score** | > 80% | Логическая структура контента |
| **Engagement Score** | > 60% | Потенциал вовлечения аудитории |

## 🔄 Коллективная работа

### Автоматическое делегирование

Агент автоматически привлекает других специалистов:

```python
# Пример делегирования SEO задач
if complex_seo_requirements:
    await delegate_task_to_agent(
        target_agent="seo_optimization",
        task_title="Комплексная SEO оптимизация контента",
        task_description="Провести детальный SEO аудит и оптимизацию",
        priority="high"
    )

# Привлечение UI/UX эксперта для дизайна
if visual_content_needed:
    await delegate_task_to_agent(
        target_agent="uiux_enhancement",
        task_title="Создание визуального дизайна контента",
        task_description="Разработать layout и визуальные элементы"
    )
```

### Интеграции с агентами

| Агент | Когда привлекается | Результат |
|-------|-------------------|-----------|
| **SEO Specialist** | Сложная SEO оптимизация | Детальный keyword research, technical SEO |
| **UI/UX Enhancement** | Визуальный контент | Дизайн, layout, пользовательский опыт |
| **Localization Engine** | Мультиязычный контент | Профессиональная локализация |
| **Quality Validator** | Финальная проверка | Comprehensive quality assurance |
| **Performance Optimizer** | Технические требования | Оптимизация скорости, производительности |

## 🎛️ Настройки и конфигурация

### Основные параметры

```env
# Тип и домен контента
CONTENT_TYPE=blog_post                    # Тип создаваемого контента
DOMAIN_TYPE=technology                    # Предметная область
TARGET_AUDIENCE=professionals            # Целевая аудитория
CONTENT_STYLE=informative               # Стиль изложения

# Качество и стиль
QUALITY_STANDARD=high                    # Стандарт качества
READABILITY_LEVEL=general               # Уровень читабельности
CREATIVITY_LEVEL=balanced               # Уровень креативности
TONE_FORMALITY=balanced                 # Формальность тона

# SEO настройки
SEO_OPTIMIZATION=true                   # Включить SEO оптимизацию
SEO_PRIMARY_KEYWORD=                    # Основное ключевое слово
SEO_SECONDARY_KEYWORDS=                 # Дополнительные ключевые слова

# Культурная адаптация
CULTURAL_ADAPTATION=true                # Культурная адаптация
TARGET_REGION=ukraine                   # Целевой регион
PRIMARY_LANGUAGE=ukrainian              # Основной язык
LOCAL_REFERENCES=true                   # Местные ссылки
```

### Расширенная конфигурация

```env
# Структура контента
CONTENT_STRUCTURE=standard              # Структура контента
INCLUDE_INTRODUCTION=true               # Включать введение
INCLUDE_CONCLUSION=true                 # Включать заключение
INCLUDE_CALL_TO_ACTION=true            # Включать призыв к действию

# Творческие элементы
HUMOR_USAGE=minimal                     # Использование юмора
STORYTELLING_ELEMENTS=false            # Элементы storytelling
PERSONAL_ANECDOTES=false               # Личные истории
BRAND_VOICE=neutral                    # Голос бренда

# Технические параметры
OUTPUT_FORMAT=markdown                  # Формат вывода
INCLUDE_METADATA=true                  # Включать метаданные
INCLUDE_WORD_COUNT=true                # Подсчет слов
INCLUDE_READING_TIME=true              # Время чтения
```

## 🛠️ API Reference

### Основные функции

```python
# Основная функция генерации
async def run_content_generation_task(
    message: str,
    content_type: str = "blog_post",
    domain_type: str = "technology",
    target_audience: str = "general",
    content_style: str = "informative",
    content_length: str = "medium",
    language: str = "ukrainian",
    seo_focus: bool = True
) -> str

# Специализированные функции
async def run_blog_post_generation(
    topic: str,
    keywords: List[str] = None,
    target_audience: str = "general",
    content_style: str = "engaging",
    word_count: int = 800,
    include_seo: bool = True
) -> str

async def run_documentation_generation(
    documentation_type: str,
    technical_level: str = "intermediate",
    framework: str = "general",
    include_examples: bool = True,
    format_style: str = "markdown"
) -> str

async def run_marketing_content_generation(
    campaign_type: str,
    product_category: str,
    marketing_goal: str = "awareness",
    tone: str = "professional",
    call_to_action: str = None
) -> str
```

### Утилиты и инструменты

```python
# Валидация и анализ
async def validate_content_requirements(
    content: str,
    requirements: Dict[str, Any]
) -> Dict[str, bool]

async def extract_content_insights(
    content: str,
    insight_types: List[str] = None
) -> Dict[str, Any]

# Предложения и рекомендации
async def get_content_suggestions(
    content_type: str,
    domain: str,
    audience: str
) -> Dict[str, List[str]]

# Генерация вариаций
async def generate_content_variations(
    base_content: str,
    variation_types: List[str] = None,
    variation_count: int = 3
) -> Dict[str, str]
```

## 📈 Мониторинг и аналитика

### Метрики производительности

```python
# Отслеживание метрик
content_metrics = {
    "generation_time": "2.3 seconds",
    "word_count": 1247,
    "readability_score": 85,
    "seo_score": 92,
    "quality_score": 88,
    "engagement_potential": 76
}

# Анализ эффективности
performance_report = {
    "content_created": 150,
    "average_quality": 87.3,
    "seo_optimized": "98%",
    "user_satisfaction": 4.6,
    "revision_rate": "12%"
}
```

### Отчеты и аналитика

```python
# Еженедельный отчет
weekly_report = {
    "period": "2024-03-01 to 2024-03-07",
    "content_types": {
        "blog_posts": 25,
        "documentation": 8,
        "marketing": 15,
        "social_media": 42
    },
    "domains": {
        "technology": 35,
        "business": 28,
        "education": 12,
        "health": 15
    },
    "quality_metrics": {
        "average_score": 86.2,
        "seo_compliance": "96%",
        "cultural_adaptation": "89%"
    }
}
```

## 🔗 Интеграция с Archon Knowledge Base

### Автоматический поиск знаний

Агент автоматически использует базу знаний для улучшения качества:

```python
# Поиск релевантной информации
knowledge_context = await search_content_knowledge(
    ctx=context,
    query="blog post best practices technology content",
    content_category="blog_writing",
    match_count=5
)

# Интеграция найденных знаний в контент
enhanced_content = integrate_knowledge_insights(
    base_content=draft_content,
    knowledge_context=knowledge_context,
    integration_style="natural"
)
```

### База знаний агента

Файл знаний: `knowledge/universal_content_generator_knowledge.md`

**Теги для загрузки в Archon:**
- `universal-content-generator`
- `content-generation`
- `copywriting`
- `seo`
- `agent-knowledge`
- `pydantic-ai`

## 🚀 Развертывание и масштабирование

### Production настройки

```env
# Production конфигурация
QUALITY_STANDARD=premium
REQUEST_TIMEOUT=300
RETRY_ATTEMPTS=5
SAVE_CONTENT_LOGS=true
CONTENT_OUTPUT_FORMAT=json

# Мониторинг
DEBUG_MODE=false
LOG_LEVEL=INFO
PERFORMANCE_MONITORING=true
```

### Интеграция с системами

```python
# Интеграция с CMS
async def publish_to_cms(content, metadata):
    """Публикация в систему управления контентом"""
    pass

# Интеграция с email marketing
async def send_to_email_platform(content, segment):
    """Отправка в email маркетинговую платформу"""
    pass

# Интеграция с социальными сетями
async def schedule_social_posts(content, platforms, schedule):
    """Планирование постов в соцсетях"""
    pass
```

## 🤝 Вклад в развитие

Агент разработан как часть AI Agent Factory и следует принципам:
- **Универсальности** - работа с любыми проектами и доменами
- **Качества** - высокие стандарты создаваемого контента
- **Адаптивности** - гибкость под различные требования
- **Коллективности** - интеграция с другими агентами
- **Масштабируемости** - готовность к enterprise использованию

## 📄 Лицензия

Часть проекта AI Agent Factory. Использование в соответствии с лицензией проекта.

---

**Universal Content Generator Agent** - ваше универсальное решение для создания высококачественного контента любого типа с поддержкой SEO, культурной адаптации и коллективной работы с другими агентами.