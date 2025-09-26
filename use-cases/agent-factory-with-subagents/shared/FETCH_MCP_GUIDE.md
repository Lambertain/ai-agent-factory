# 🌐 Руководство по оптимизации Fetch MCP для агентов

## 📋 Результаты тестирования и оптимизации

Данное руководство основано на комплексном тестировании Fetch MCP сервера и содержит проверенные настройки для максимальной эффективности в различных сценариях использования.

## 🎯 Основные выводы тестирования

### ✅ Что работает отлично:
- **Обработка HTML → Markdown** - отличная конвертация с сохранением структуры
- **JSON извлечение** - корректная обработка API ответов с `raw=true`
- **Обработка изображений** - качественное сохранение и конвертация в base64
- **Управление размером контента** - эффективное ограничение через `maxLength`
- **Обработка ошибок** - корректные HTTP коды и информативные сообщения

### ⚠️ Ограничения:
- **404 ошибки** - некоторые URL могут быть недоступны (нормальное поведение)
- **Большие страницы** - требуют pagination через `startIndex`
- **Некоторые сайты** могут блокировать автоматические запросы

## 🔧 Оптимальные конфигурации по типам контента

### 📚 Техническая документация
```python
{
    "maxLength": 15000,
    "enableFetchImages": False,
    "raw": False
}
```
**Использование**: Документация API, туториалы, технические статьи
**Преимущества**: Максимальное извлечение текста с markdown форматированием

### 🔄 JSON API
```python
{
    "maxLength": 5000,
    "enableFetchImages": False,
    "raw": True
}
```
**Использование**: REST API ответы, структурированные данные
**Преимущества**: Сохранение оригинальной JSON структуры

### 🎨 Дизайн и UI/UX
```python
{
    "maxLength": 8000,
    "enableFetchImages": True,
    "imageMaxCount": 3,
    "imageQuality": 90,
    "imageMaxWidth": 800,
    "imageMaxHeight": 600,
    "returnBase64": False,
    "saveImages": True
}
```
**Использование**: Дизайн-вдохновение, анализ интерфейсов
**Преимущества**: Высокое качество изображений с оптимальным размером

### 🔍 Анализ конкурентов
```python
{
    "maxLength": 12000,
    "enableFetchImages": True,
    "imageMaxCount": 2,
    "imageQuality": 80,
    "returnBase64": False,
    "saveImages": True
}
```
**Использование**: Исследование конкурентных решений
**Преимущества**: Баланс между детализацией и производительностью

### 🧪 Исследования
```python
{
    "maxLength": 20000,
    "enableFetchImages": False,
    "raw": False
}
```
**Использование**: Научные статьи, обширные материалы
**Преимущества**: Максимальное извлечение текстового контента

### ⚡ Быстрое извлечение
```python
{
    "maxLength": 3000,
    "enableFetchImages": False,
    "raw": False
}
```
**Использование**: Краткие сводки, быстрая проверка
**Преимущества**: Минимальное время ответа

## 🛠️ Интеграция с агентами

### Базовая интеграция

```python
from shared.fetch_mcp_utils import extract_web_content, FetchMCPOptimizer

@agent.tool
async def research_web_content(
    ctx: RunContext[AgentDependencies],
    url: str,
    content_type: str = "documentation"
) -> str:
    """Исследовать веб-контент с оптимизированными настройками."""

    result = await extract_web_content(
        url=url,
        content_type=content_type,
        mcp_fetch_function=mcp__fetch__imageFetch
    )

    if result["success"]:
        return f"Контент из {url}:\n{result['content']}"
    else:
        return f"Ошибка извлечения: {result['error']}"
```

### Специализированные функции

```python
@agent.tool
async def analyze_competitors(
    ctx: RunContext[AgentDependencies],
    competitor_urls: List[str],
    focus_areas: List[str] = None
) -> str:
    """Анализ сайтов конкурентов."""

    analysis = await analyze_competitor_sites(
        urls=competitor_urls,
        mcp_fetch_function=mcp__fetch__imageFetch,
        focus_areas=focus_areas
    )

    return f"""
Анализ конкурентов завершен:
- Обработано сайтов: {analysis['successful_extractions']}/{analysis['total_sites']}
- Успешность: {analysis['summary']['success_rate']:.0%}
- Рекомендации: {', '.join(analysis['summary']['recommendations'])}
"""

@agent.tool
async def gather_design_inspiration(
    ctx: RunContext[AgentDependencies],
    design_urls: List[str],
    categories: List[str] = None
) -> str:
    """Сбор дизайн-вдохновения с изображениями."""

    inspiration = await gather_design_inspiration(
        urls=design_urls,
        mcp_fetch_function=mcp__fetch__imageFetch,
        design_categories=categories
    )

    return f"""
Дизайн-исследование завершено:
- Сайтов обработано: {inspiration['successful_extractions']}
- Изображений сохранено: {inspiration['summary']['total_images_saved']}
- Паттерны: {', '.join(inspiration['summary']['design_patterns'])}
"""
```

## 📊 Производительность и лимиты

### Рекомендуемые лимиты:
- **maxLength**: 3,000 - 20,000 символов в зависимости от задачи
- **imageMaxCount**: 1-3 изображения для оптимальной скорости
- **imageQuality**: 80-90 для баланса качества/размера
- **Размер изображений**: 800x600 для web-контента

### Оптимизация производительности:
1. **Используйте подходящий content_type** для автоматической оптимизации
2. **Ограничивайте imageMaxCount** для сайтов с множеством изображений
3. **Применяйте pagination** для больших страниц через `startIndex`
4. **Кэшируйте результаты** в агентах для повторных запросов

## 🔄 Обработка ошибок

### Типичные ошибки и решения:

```python
async def safe_web_extraction(url: str, content_type: str = "documentation"):
    """Безопасное извлечение с обработкой ошибок."""

    try:
        result = await extract_web_content(
            url=url,
            content_type=content_type,
            mcp_fetch_function=mcp__fetch__imageFetch
        )

        if not result["success"]:
            # Пробуем с более легкими настройками
            fallback_result = await extract_web_content(
                url=url,
                content_type="lightweight",
                mcp_fetch_function=mcp__fetch__imageFetch
            )
            return fallback_result

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Критическая ошибка: {e}",
            "fallback_suggestion": "Попробуйте другой URL или настройки"
        }
```

## 🎯 Best Practices для агентов

### 1. **Выбор правильного типа контента**
```python
# Хорошо
await extract_web_content(url, content_type="json_api")  # для API

# Плохо
await extract_web_content(url, content_type="design_inspiration")  # для API
```

### 2. **Постепенная деградация**
```python
# Сначала пробуем полную функциональность
result = await extract_web_content(url, "design_inspiration")

# При ошибке - упрощаем
if not result["success"]:
    result = await extract_web_content(url, "lightweight")
```

### 3. **Batch обработка**
```python
# Для множественных URL используйте специализированные функции
await analyze_competitor_sites(urls_list, mcp_fetch_function)

# Вместо циклов с extract_web_content
```

### 4. **Кэширование результатов**
```python
@agent.tool
async def cached_web_research(
    ctx: RunContext[AgentDependencies],
    url: str
) -> str:
    """Исследование с кэшированием."""

    # Проверяем кэш в зависимостях агента
    cache_key = f"web_content_{hash(url)}"

    if hasattr(ctx.deps, 'content_cache') and cache_key in ctx.deps.content_cache:
        return ctx.deps.content_cache[cache_key]

    # Извлекаем контент
    result = await extract_web_content(url, "documentation", mcp__fetch__imageFetch)

    # Сохраняем в кэш
    if not hasattr(ctx.deps, 'content_cache'):
        ctx.deps.content_cache = {}
    ctx.deps.content_cache[cache_key] = result["content"]

    return result["content"]
```

## 📁 Управление сохраненными изображениями

Fetch MCP автоматически сохраняет изображения в:
```
C:\Users\Admin\Downloads\mcp-fetch\YYYY-MM-DD\merged\
```

### Работа с сохраненными изображениями:
1. **Автоматическое именование**: `domain_HH-MM-SS-sssZ_index.jpg`
2. **Слияние изображений**: Несколько изображений объединяются вертикально
3. **Оптимизация размера**: Автоматическое изменение размера до заданных лимитов

## 🔮 Интеграция с другими MCP серверами

### Puppeteer + Fetch комбинация:
```python
# Сначала навигация через Puppeteer
await mcp__puppeteer__puppeteer_navigate(url)
await mcp__puppeteer__puppeteer_screenshot("page_preview")

# Затем извлечение контента через Fetch
content = await extract_web_content(url, "design_inspiration", mcp__fetch__imageFetch)
```

### RAG + Fetch для исследований:
```python
# Fetch для получения свежего контента
web_content = await extract_web_content(research_url, "research", mcp__fetch__imageFetch)

# RAG для поиска связанных знаний
related_knowledge = await mcp__archon__rag_search_knowledge_base(
    query=f"research {topic}",
    match_count=3
)
```

## 📈 Метрики успешности

### Контрольные показатели:
- **Успешность извлечения**: >85% для стандартных сайтов
- **Скорость обработки**: <10 секунд для документации (<15K символов)
- **Качество изображений**: 80-90% оригинального качества
- **Точность markdown**: >90% сохранения структуры

### Мониторинг производительности:
```python
import time

async def monitored_extraction(url: str, content_type: str):
    """Извлечение с мониторингом производительности."""

    start_time = time.time()

    result = await extract_web_content(url, content_type, mcp__fetch__imageFetch)

    duration = time.time() - start_time

    # Логирование метрик
    logger.info(f"Extraction metrics: {url}, {content_type}, {duration:.2f}s, "
                f"success: {result.get('success', False)}")

    return result
```

## 🚀 Заключение

Fetch MCP показал отличные результаты во всех тестовых сценариях. Основные преимущества:

1. **Универсальность** - работает с любыми типами веб-контента
2. **Оптимизация** - настраиваемые параметры для разных задач
3. **Надежность** - корректная обработка ошибок и fallback стратегии
4. **Интеграция** - простая интеграция с агентами через готовые утилиты

**Рекомендация**: Использовать Fetch MCP как основной инструмент для веб-исследований во всех агентах AI Agent Factory.

---

*Документ обновлен: 23 сентября 2025*
*Версия: 1.0*
*Основан на комплексном тестировании Fetch MCP сервера*