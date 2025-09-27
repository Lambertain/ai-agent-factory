# Universal Media Orchestrator Agent

Универсальный агент для оркестрации, обработки и оптимизации медиа-контента всех типов. Поддерживает изображения, видео, аудио, анимации, презентации и композиции с автоматической адаптацией под различные платформы и требования.

## 🎯 Основные возможности

### 🎨 Мультиформатная обработка
- **Изображения**: JPEG, PNG, WebP, AVIF, SVG, HEIC, TIFF, BMP
- **Видео**: MP4, WebM, AVI, MOV, MKV с кодеками H.264, H.265, VP9, AV1
- **Аудио**: MP3, WAV, FLAC, AAC, OGG, M4A с профессиональной обработкой
- **Анимации**: GIF, WebP, APNG, Lottie, CSS animations
- **Презентации**: PowerPoint, PDF, HTML5, интерактивные медиа
- **Композиции**: коллажи, слайд-шоу, мультимедийные проекты

### 🚀 Интеллектуальная оркестрация
- Автоматическое планирование оптимальных пайплайнов обработки
- Параллельное выполнение независимых операций
- Batch processing для массовой обработки
- Интеллектуальное кэширование результатов
- Адаптивная маршрутизация задач между инструментами

### 🌐 Платформенная адаптация
- **Веб**: responsive design, progressive loading, SEO optimization
- **Мобильные**: touch-friendly, battery optimization, сетевая эффективность
- **Социальные сети**: platform-specific форматы, aspect ratios
- **Печать**: высокое DPI, CMYK, ICC профили, bleed areas
- **Вещание**: broadcast standards, HDR, professional codecs

### 🤖 AI-powered возможности
- Автоматическая генерация и улучшение медиа-контента
- Интеллектуальная стилизация и художественная обработка
- Адаптивная цветокоррекция и тональная настройка
- Создание engaging контента для социальных платформ
- Автоматическое удаление фона и объектов

## 📁 Структура проекта

```
universal_media_orchestrator_agent/
├── agent.py                    # Основной агент с entry points
├── dependencies.py             # Универсальные зависимости
├── tools.py                    # Инструменты медиа-обработки
├── prompts.py                  # Адаптивные системные промпты
├── providers.py                # Оптимизированная система моделей
├── settings.py                 # Универсальная конфигурация
├── knowledge/                  # База знаний агента
│   └── universal_media_orchestrator_knowledge.md
├── __init__.py                 # Инициализация пакета
└── README.md                   # Документация (этот файл)
```

## 🚀 Быстрый старт

### Установка и настройка

1. **Установите зависимости**:
```bash
pip install pydantic-ai python-dotenv pydantic-settings
```

2. **Настройте переменные окружения** (создайте файл `.env`):
```env
# Основные API ключи
MEDIA_ORCHESTRATOR_LLM_API_KEY=your_qwen_api_key
MEDIA_ORCHESTRATOR_GEMINI_API_KEY=your_gemini_api_key
MEDIA_ORCHESTRATOR_ANTHROPIC_API_KEY=your_claude_api_key  # опционально

# Пути проекта
MEDIA_ORCHESTRATOR_PROJECT_PATH=/path/to/your/project
MEDIA_ORCHESTRATOR_MEDIA_ASSETS_PATH=assets/media
MEDIA_ORCHESTRATOR_OUTPUT_PATH=output/media

# Конфигурация проекта
MEDIA_ORCHESTRATOR_PROJECT_TYPE=ecommerce  # или blog, portfolio, corporate
MEDIA_ORCHESTRATOR_DOMAIN_TYPE=web         # или mobile, social, print
```

3. **Базовое использование**:
```python
from universal_media_orchestrator_agent import (
    run_media_orchestration_task,
    run_image_processing,
    run_video_processing
)

# Универсальная оркестрация медиа
result = await run_media_orchestration_task(
    message="Оптимизируй эти изображения для веб-сайта",
    media_type="image",
    processing_mode="optimize",
    target_platform="web",
    quality_level="high"
)

# Специализированная обработка изображений
image_result = await run_image_processing(
    image_path="input/product_photo.jpg",
    operations=["resize", "enhance", "optimize"],
    target_size=(1200, 800),
    platform_optimization="ecommerce"
)
```

## 📖 Примеры использования по доменам

### 💼 E-commerce проект

```python
# Конфигурация для интернет-магазина
from universal_media_orchestrator_agent.dependencies import MediaOrchestratorDependencies

ecommerce_deps = MediaOrchestratorDependencies(
    api_key="your_api_key",
    project_path="/path/to/shop",
    media_type="image",
    processing_mode="optimize",
    target_platform="web",
    quality_level="high",
    project_type="ecommerce",
    domain_type="web",

    # E-commerce специфичные настройки
    enable_ai_generation=True,
    enable_effects=True,
    enable_watermarks=True,
    product_catalog_optimization=True
)

# Обработка изображений товаров
result = await run_image_processing(
    image_path="products/smartphone.jpg",
    operations=["background_removal", "resize", "enhance", "watermark"],
    target_size=(800, 800),
    target_format="webp",
    platform_optimization="ecommerce"
)
```

### 📱 Социальные сети

```python
# Создание контента для социальных платформ
result = await run_media_composition(
    media_assets=[
        {"type": "image", "path": "photo1.jpg"},
        {"type": "text", "content": "Новый продукт!"},
        {"type": "logo", "path": "brand_logo.png"}
    ],
    composition_type="social_post",
    layout_style="instagram_story",
    output_dimensions=(1080, 1920)
)

# Оптимизация для множественных платформ
multi_platform_result = await run_platform_optimization(
    media_path="content/announcement.mp4",
    target_platforms=["instagram", "youtube", "tiktok"],
    optimization_goals=["engagement", "quality", "compatibility"]
)
```

### 🏢 Корпоративные презентации

```python
# Профессиональная обработка для бизнеса
corporate_result = await run_media_orchestration_task(
    message="Подготовь медиа-контент для корпоративной презентации",
    media_type="presentation",
    processing_mode="optimize",
    target_platform="presentation",
    quality_level="premium",
    enable_ai_generation=False,  # Консервативный подход
    enable_effects=True
)
```

### 🎨 Творческие проекты

```python
# AI-генерация креативного контента
creative_result = await run_media_generation(
    generation_type="image",
    prompt="Футуристический городской пейзаж в стиле cyberpunk",
    style="artistic",
    dimensions={"width": 1920, "height": 1080},
    quality_preset="premium"
)
```

## 🛠️ Детальное API

### Основные функции

#### `run_media_orchestration_task()`
Главная функция для универсальной оркестрации медиа-контента.

```python
async def run_media_orchestration_task(
    message: str,                    # Описание задачи
    media_type: str = "image",       # image, video, audio, animation, presentation
    processing_mode: str = "optimize", # optimize, transform, generate, composite
    target_platform: str = "web",    # web, mobile, social, print, presentation
    quality_level: str = "high",     # low, medium, high, premium
    output_format: str = "auto",     # auto или конкретный формат
    enable_ai_generation: bool = True,
    enable_effects: bool = True
) -> str
```

#### `run_image_processing()`
Специализированная обработка изображений.

```python
async def run_image_processing(
    image_path: str,                 # Путь к изображению
    operations: List[str] = None,    # resize, crop, filter, enhance, etc.
    target_size: Tuple[int, int] = None,
    target_format: str = "auto",
    quality: int = 85,
    platform_optimization: str = None
) -> Dict[str, Any]
```

#### `run_video_processing()`
Специализированная обработка видео.

```python
async def run_video_processing(
    video_path: str,
    editing_operations: Dict[str, Any] = None,
    target_resolution: str = "1080p",
    target_fps: int = 30,
    target_codec: str = "h264",
    platform_optimization: str = None
) -> Dict[str, Any]
```

### Системные функции

#### `analyze_media_requirements()`
Анализ требований к медиа для проекта.

```python
async def analyze_media_requirements(
    project_type: str,               # Тип проекта
    target_audience: str,            # Целевая аудитория
    platforms: List[str]             # Целевые платформы
) -> Dict[str, Any]
```

#### `create_media_strategy()`
Создание стратегии медиа-контента.

```python
async def create_media_strategy(
    content_goals: List[str],        # Цели контента
    budget_level: str = "medium",    # low, medium, high
    timeline: str = "standard"       # rush, standard, extended
) -> Dict[str, Any]
```

## ⚙️ Конфигурация

### Переменные окружения

Агент поддерживает обширную конфигурацию через переменные окружения с префиксом `MEDIA_ORCHESTRATOR_`:

```env
# API конфигурация
MEDIA_ORCHESTRATOR_LLM_API_KEY=your_key
MEDIA_ORCHESTRATOR_GEMINI_API_KEY=your_key
MEDIA_ORCHESTRATOR_ANTHROPIC_API_KEY=your_key

# Пути и структура
MEDIA_ORCHESTRATOR_PROJECT_PATH=/project/path
MEDIA_ORCHESTRATOR_MEDIA_ASSETS_PATH=assets/media
MEDIA_ORCHESTRATOR_OUTPUT_PATH=output/media

# Качество и производительность
MEDIA_ORCHESTRATOR_DEFAULT_IMAGE_QUALITY=85
MEDIA_ORCHESTRATOR_MAX_PARALLEL_TASKS=4
MEDIA_ORCHESTRATOR_ENABLE_CACHING=true

# Домен-специфичные настройки
MEDIA_ORCHESTRATOR_PROJECT_TYPE=ecommerce
MEDIA_ORCHESTRATOR_DOMAIN_TYPE=web
MEDIA_ORCHESTRATOR_BRAND_COLORS=["#ff0000", "#00ff00"]

# AI и генерация
MEDIA_ORCHESTRATOR_ENABLE_AI_GENERATION=true
MEDIA_ORCHESTRATOR_DEFAULT_AI_STYLE=realistic

# Безопасность
MEDIA_ORCHESTRATOR_REMOVE_EXIF_DATA=true
MEDIA_ORCHESTRATOR_PRIVACY_MODE=false
```

### Профили обработки

Агент включает предустановленные профили для различных сценариев:

```python
from universal_media_orchestrator_agent.settings import get_processing_profile

# Доступные профили
profiles = [
    "web_optimization",      # Оптимизация для веб-сайтов
    "social_media",         # Контент для социальных сетей
    "professional_print",   # Профессиональная печать
    "quick_preview"         # Быстрый просмотр
]

# Использование профиля
profile = get_processing_profile("web_optimization")
```

## 🤖 AI Модели и производительность

### Автоматический выбор моделей

Агент автоматически выбирает оптимальную модель на основе:

- **Типа медиа**: изображения, видео, аудио
- **Сложности задачи**: простая, средняя, сложная, премиум
- **Режима обработки**: оптимизация, генерация, анализ
- **Приоритетов**: качество vs стоимость

```python
from universal_media_orchestrator_agent.providers import get_model_for_media_task

# Автоматический выбор модели
model = get_model_for_media_task(
    media_type="image",
    complexity="complex",
    processing_mode="generate"
)

# Выбор по приоритетам
cost_optimized = get_llm_model(model_type="cost_optimized")
quality_optimized = get_llm_model(model_type="quality_optimized")
balanced = get_llm_model(model_type="balanced")
```

### Поддерживаемые модели

| Модель | Назначение | Стоимость | Производительность |
|--------|------------|-----------|-------------------|
| Claude Opus Vision | Анализ изображений | $$$ | ⭐⭐⭐⭐⭐ |
| Qwen Coder 32B | AI-генерация | $$ | ⭐⭐⭐⭐ |
| Qwen Coder 14B | Техническая обработка | $ | ⭐⭐⭐ |
| Gemini Flash | Быстрая обработка | $ | ⭐⭐⭐ |
| Gemini Thinking | Анализ и планирование | $$ | ⭐⭐⭐⭐ |

## 🔗 Интеграции

### Archon Integration

Агент полностью интегрирован с Archon Knowledge Base:

```python
# Поиск в базе знаний
knowledge = await search_media_knowledge(
    ctx=context,
    query="image optimization best practices",
    media_type="image"
)

# Создание задач в Archon
task = await create_archon_task(
    title="Оптимизация медиа для каталога",
    description="Batch обработка 500+ изображений товаров",
    assignee="Media Orchestrator Agent"
)
```

### Коллективное решение задач

Агент автоматически делегирует специализированные задачи:

```python
# Автоматическое делегирование
if task_requires_ui_expertise(task):
    await delegate_to_agent("UI/UX Enhancement Agent", task_details)

if task_requires_performance_analysis(task):
    await delegate_to_agent("Performance Optimization Agent", task_details)
```

## 📊 Мониторинг и отчетность

### Логирование операций

```python
# Настройка логирования
MEDIA_ORCHESTRATOR_LOG_LEVEL=INFO
MEDIA_ORCHESTRATOR_ENABLE_DETAILED_LOGGING=true
MEDIA_ORCHESTRATOR_GENERATE_PROCESSING_REPORTS=true
```

### Метрики производительности

Агент автоматически отслеживает:
- Время обработки каждого файла
- Качество сжатия и оптимизации
- Использование ресурсов (память, CPU)
- Соответствие целевым платформам
- Экономия трафика и места

## 🔒 Безопасность и конфиденциальность

### Защита данных

- **Автоматическое удаление EXIF**: GPS, metadata, camera info
- **Privacy mode**: дополнительная защита sensitive данных
- **Face blurring**: автоматическое размытие лиц при необходимости
- **Watermarking**: защита авторских прав

### Валидация файлов

- Проверка на malicious контент
- Sandboxing пользовательских файлов
- Валидация форматов и размеров
- Аудит всех операций

## 🧪 Тестирование

### Запуск тестов

```bash
# Установка тестовых зависимостей
pip install pytest pytest-asyncio

# Запуск всех тестов
pytest universal_media_orchestrator_agent/tests/

# Тесты конкретного компонента
pytest universal_media_orchestrator_agent/tests/test_image_processing.py
```

### Тестовые данные

Агент включает набор тестовых медиа-файлов для валидации:
- Различные форматы изображений
- Видео с разными кодеками
- Аудио файлы различного качества
- Презентации и анимации

## 🤝 Вклад в развитие

### Архитектура расширений

Агент спроектирован для легкого расширения:

```python
# Добавление нового инструмента
@media_orchestrator_agent.tool
async def custom_media_tool(
    ctx: RunContext[MediaOrchestratorDependencies],
    custom_param: str
) -> str:
    """Пользовательский инструмент медиа-обработки."""
    # Ваша логика
    return result

# Добавление нового формата
def register_custom_format(format_name: str, processor: callable):
    CUSTOM_PROCESSORS[format_name] = processor
```

### Добавление поддержки платформ

```python
# Новые платформенные оптимизации
PLATFORM_CONFIGS["new_platform"] = {
    "formats": ["custom_format"],
    "max_size": (2048, 2048),
    "quality": 90,
    "special_requirements": {...}
}
```

## 📋 Roadmap

### Ближайшие функции
- [ ] Поддержка 3D-моделей и VR контента
- [ ] Интеграция с популярными CMS (WordPress, Drupal)
- [ ] Real-time обработка видео потоков
- [ ] Blockchain watermarking для NFT

### Долгосрочные планы
- [ ] Интеграция с AR/VR платформами
- [ ] Machine learning для предсказания тенденций
- [ ] Автоматический A/B тест медиа-контента
- [ ] Поддержка holographic displays

## 📄 Лицензия

MIT License - см. LICENSE файл для деталей.

## 🆘 Поддержка

- **Документация**: [Knowledge Base](knowledge/universal_media_orchestrator_knowledge.md)
- **Issues**: Создайте issue в репозитории для багов и предложений
- **Discussions**: Обсуждение функций и best practices

---

**Universal Media Orchestrator Agent** - ваш универсальный помощник для профессиональной работы с медиа-контентом любых типов и форматов! 🎨🚀