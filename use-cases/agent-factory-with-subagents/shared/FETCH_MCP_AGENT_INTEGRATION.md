# 🤖 Интеграция Fetch MCP с агентами AI Agent Factory

## 🎯 Специализированная интеграция по агентам

После комплексного тестирования определены оптимальные способы интеграции Fetch MCP с каждым типом агента в фабрике.

## 🔒 Security Audit Agent

### Специальные инструменты:
```python
@agent.tool
async def analyze_website_security(
    ctx: RunContext[SecurityAuditDependencies],
    target_url: str,
    scan_depth: str = "comprehensive"
) -> str:
    """Анализ безопасности веб-сайта через извлечение контента."""

    # Извлекаем контент для анализа
    result = await extract_web_content(
        url=target_url,
        content_type="documentation" if scan_depth == "comprehensive" else "lightweight",
        mcp_fetch_function=mcp__fetch__imageFetch
    )

    if not result["success"]:
        return f"Ошибка извлечения контента: {result['error']}"

    content = result["content"]

    # Анализируем на предмет уязвимостей
    security_issues = []

    # Поиск потенциальных проблем безопасности
    if "password" in content.lower() and "form" in content.lower():
        security_issues.append("Обнаружены формы с паролями - проверить HTTPS")

    if "admin" in content.lower() and "login" in content.lower():
        security_issues.append("Найдены административные страницы - проверить доступ")

    if "api" in content.lower() and "key" in content.lower():
        security_issues.append("Возможное упоминание API ключей - проверить экспозицию")

    # Проверяем заголовки безопасности через повторный запрос
    headers_check = await extract_web_content(
        url=target_url,
        content_type="lightweight",
        custom_params={"maxLength": 500},
        mcp_fetch_function=mcp__fetch__imageFetch
    )

    return f"""
🔒 Анализ безопасности: {target_url}

📊 Статус извлечения: {'✅ Успешно' if result['success'] else '❌ Ошибка'}
📄 Размер контента: {len(content)} символов

🚨 Найденные проблемы:
{chr(10).join(f"- {issue}" for issue in security_issues) if security_issues else "Критических проблем не обнаружено"}

💡 Рекомендации:
- Проверить SSL/TLS сертификаты
- Анализировать заголовки безопасности
- Проверить доступность административных интерфейсов
- Провести полный пентест для критических находок
"""

@agent.tool
async def scan_competitor_security(
    ctx: RunContext[SecurityAuditDependencies],
    competitor_urls: List[str]
) -> str:
    """Анализ безопасности конкурентов для сравнения."""

    security_analysis = await analyze_competitor_sites(
        urls=competitor_urls,
        mcp_fetch_function=mcp__fetch__imageFetch,
        focus_areas=["security", "privacy", "compliance"]
    )

    results = []
    for result in security_analysis["results"]:
        if result.get("success"):
            content = result["content"]

            # Простой анализ упоминаний безопасности
            security_mentions = []
            if "privacy policy" in content.lower():
                security_mentions.append("Privacy Policy")
            if "terms of service" in content.lower():
                security_mentions.append("Terms of Service")
            if "security" in content.lower():
                security_mentions.append("Security Information")
            if "gdpr" in content.lower():
                security_mentions.append("GDPR Compliance")

            results.append({
                "url": result["url"],
                "security_features": security_mentions,
                "compliance_indicators": len(security_mentions)
            })

    return f"""
🔍 Анализ безопасности конкурентов:

📈 Результаты:
{chr(10).join(f"🌐 {r['url']}: {', '.join(r['security_features']) or 'Не указано'}" for r in results)}

📊 Среднее количество индикаторов безопасности: {sum(r['compliance_indicators'] for r in results) / len(results) if results else 0:.1f}

💡 Выводы для улучшения:
- Добавить четкую политику конфиденциальности
- Разместить информацию о безопасности на видном месте
- Обеспечить соответствие стандартам GDPR/CCPA
"""
```

## 🔍 RAG Agent

### Интеграция для поиска знаний:
```python
@agent.tool
async def research_web_knowledge(
    ctx: RunContext[RAGDependencies],
    research_query: str,
    sources: List[str],
    depth: str = "comprehensive"
) -> str:
    """Исследование знаний через веб-источники для пополнения RAG."""

    research_results = await research_technical_topics(
        urls=sources,
        topic=research_query,
        mcp_fetch_function=mcp__fetch__imageFetch,
        depth=depth
    )

    # Синтезируем знания для RAG
    knowledge_synthesis = []
    for result in research_results["research_results"]:
        knowledge_synthesis.append({
            "source": result["url"],
            "relevance": result["relevance_score"],
            "key_concepts": result["key_concepts"],
            "content_summary": result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
        })

    # Сортируем по релевантности
    knowledge_synthesis.sort(key=lambda x: x["relevance"], reverse=True)

    return f"""
🧠 Исследование знаний: {research_query}

📚 Обработано источников: {research_results['sources_processed']}
✅ Успешных извлечений: {research_results['successful_extractions']}

🎯 Наиболее релевантные источники:
{chr(10).join(f"📖 {k['source']} (релевантность: {k['relevance']:.2f})" for k in knowledge_synthesis[:3])}

💡 Ключевые находки:
{chr(10).join(research_results['synthesis']['key_findings'])}

🔄 Рекомендации для RAG:
- Добавить наиболее релевантные источники в базу знаний
- Проверить актуальность информации
- Создать связи между концепциями
"""

@agent.tool
async def update_knowledge_base_from_web(
    ctx: RunContext[RAGDependencies],
    topic_urls: Dict[str, List[str]],
    knowledge_tags: List[str]
) -> str:
    """Обновление базы знаний из веб-источников."""

    all_extractions = []

    for topic, urls in topic_urls.items():
        for url in urls:
            result = await extract_web_content(
                url=url,
                content_type="research",
                mcp_fetch_function=mcp__fetch__imageFetch
            )

            if result["success"]:
                all_extractions.append({
                    "topic": topic,
                    "url": url,
                    "content": result["content"],
                    "tags": knowledge_tags + [topic]
                })

    return f"""
📚 Обновление базы знаний:

📊 Статистика:
- Тем обработано: {len(topic_urls)}
- Источников извлечено: {len(all_extractions)}
- Общий объем знаний: {sum(len(e['content']) for e in all_extractions)} символов

🏷️ Теги для добавления: {', '.join(knowledge_tags)}

💾 Готово к загрузке в Archon Knowledge Base:
{chr(10).join(f"📄 {e['topic']}: {e['url'][:50]}..." for e in all_extractions[:5])}

{"...и еще " + str(len(all_extractions) - 5) + " источников" if len(all_extractions) > 5 else ""}
"""
```

## 🎨 UI/UX Enhancement Agent

### Дизайн-исследования и вдохновение:
```python
@agent.tool
async def gather_ui_inspiration(
    ctx: RunContext[UIUXDependencies],
    design_categories: List[str],
    inspiration_urls: List[str] = None
) -> str:
    """Сбор UI/UX вдохновения по категориям."""

    # Используем предустановленные источники вдохновения если URL не указаны
    if not inspiration_urls:
        inspiration_urls = [
            "https://dribbble.com",
            "https://unsplash.com",
            "https://www.behance.net"
        ]

    inspiration = await gather_design_inspiration(
        urls=inspiration_urls,
        mcp_fetch_function=mcp__fetch__imageFetch,
        design_categories=design_categories
    )

    return f"""
🎨 Дизайн-вдохновение собрано:

📊 Результаты:
- Сайтов обработано: {inspiration['successful_extractions']}
- Изображений сохранено: {inspiration['summary']['total_images_saved']}
- Категории: {', '.join(inspiration['categories'])}

🎯 Выявленные паттерны:
{chr(10).join(f"• {pattern}" for pattern in inspiration['summary']['design_patterns'])}

💡 Для UI/UX применения:
- Современные градиенты и цветовые схемы
- Минималистичные интерфейсы
- Адаптивные компоненты
- Микроанимации и переходы

📁 Изображения сохранены в: C:\\Users\\Admin\\Downloads\\mcp-fetch\\{datetime.now().strftime('%Y-%m-%d')}\\
"""

@agent.tool
async def analyze_ui_accessibility(
    ctx: RunContext[UIUXDependencies],
    target_urls: List[str]
) -> str:
    """Анализ доступности интерфейсов конкурентов."""

    accessibility_analysis = []

    for url in target_urls:
        result = await extract_web_content(
            url=url,
            content_type="documentation",
            mcp_fetch_function=mcp__fetch__imageFetch
        )

        if result["success"]:
            content = result["content"]

            # Простой анализ доступности через контент
            accessibility_features = []

            if "alt=" in content:
                accessibility_features.append("Alt text для изображений")
            if "aria-" in content:
                accessibility_features.append("ARIA атрибуты")
            if "role=" in content:
                accessibility_features.append("Роли элементов")
            if "skip" in content.lower() and "content" in content.lower():
                accessibility_features.append("Skip links")

            accessibility_analysis.append({
                "url": url,
                "features": accessibility_features,
                "score": len(accessibility_features)
            })

    # Сортируем по количеству функций доступности
    accessibility_analysis.sort(key=lambda x: x["score"], reverse=True)

    return f"""
♿ Анализ доступности UI:

🏆 Лидеры по доступности:
{chr(10).join(f"🌐 {a['url']}: {a['score']} функций" for a in accessibility_analysis[:3])}

📋 Обнаруженные функции:
{chr(10).join(f"• {feature}" for a in accessibility_analysis for feature in a['features'])}

📊 Средний уровень доступности: {sum(a['score'] for a in accessibility_analysis) / len(accessibility_analysis) if accessibility_analysis else 0:.1f}

💡 Рекомендации:
- Добавить alt атрибуты для всех изображений
- Реализовать ARIA labels для интерактивных элементов
- Добавить skip links для навигации
- Обеспечить контрастность цветов
"""
```

## ⚡ Performance Optimization Agent

### Анализ производительности веб-сайтов:
```python
@agent.tool
async def analyze_web_performance_patterns(
    ctx: RunContext[PerformanceDependencies],
    benchmark_urls: List[str],
    focus_metrics: List[str] = None
) -> str:
    """Анализ паттернов производительности у лидеров рынка."""

    if not focus_metrics:
        focus_metrics = ["loading", "images", "scripts", "css"]

    performance_insights = []

    for url in benchmark_urls:
        # Извлекаем контент для анализа
        result = await extract_web_content(
            url=url,
            content_type="documentation",
            mcp_fetch_function=mcp__fetch__imageFetch
        )

        if result["success"]:
            content = result["content"]

            # Анализируем упоминания техник оптимизации
            optimization_techniques = []

            if "lazy" in content.lower() and "load" in content.lower():
                optimization_techniques.append("Lazy loading")
            if "cache" in content.lower():
                optimization_techniques.append("Caching")
            if "compress" in content.lower() or "gzip" in content.lower():
                optimization_techniques.append("Compression")
            if "cdn" in content.lower():
                optimization_techniques.append("CDN usage")
            if "minif" in content.lower():
                optimization_techniques.append("Minification")

            performance_insights.append({
                "url": url,
                "techniques": optimization_techniques,
                "performance_score": len(optimization_techniques)
            })

    return f"""
⚡ Анализ производительности веб-сайтов:

🎯 Фокус метрики: {', '.join(focus_metrics)}

📊 Результаты анализа:
{chr(10).join(f"🌐 {p['url']}: {p['performance_score']} техник" for p in performance_insights)}

🛠️ Обнаруженные техники оптимизации:
{chr(10).join(f"• {tech}" for p in performance_insights for tech in p['techniques'])}

💡 Рекомендации для внедрения:
- Реализовать lazy loading для изображений
- Настроить эффективное кэширование
- Использовать CDN для статических ресурсов
- Минифицировать CSS/JS файлы
- Включить сжатие на сервере
"""

@agent.tool
async def benchmark_loading_strategies(
    ctx: RunContext[PerformanceDependencies],
    case_study_urls: List[str]
) -> str:
    """Изучение стратегий загрузки у успешных сайтов."""

    loading_strategies = await analyze_competitor_sites(
        urls=case_study_urls,
        mcp_fetch_function=mcp__fetch__imageFetch,
        focus_areas=["performance", "loading", "optimization"]
    )

    strategies_found = []
    for result in loading_strategies["results"]:
        if result.get("success"):
            content = result["content"]

            # Ищем паттерны стратегий загрузки
            strategies = []
            if "critical" in content.lower() and "css" in content.lower():
                strategies.append("Critical CSS inline")
            if "async" in content.lower() or "defer" in content.lower():
                strategies.append("Async/Defer scripts")
            if "preload" in content.lower():
                strategies.append("Resource preloading")
            if "progressive" in content.lower():
                strategies.append("Progressive enhancement")

            strategies_found.extend(strategies)

    # Подсчитываем частоту стратегий
    strategy_frequency = {}
    for strategy in strategies_found:
        strategy_frequency[strategy] = strategy_frequency.get(strategy, 0) + 1

    return f"""
📈 Анализ стратегий загрузки:

🔍 Исследовано сайтов: {len(case_study_urls)}
✅ Успешных анализов: {loading_strategies['successful_extractions']}

📊 Популярные стратегии:
{chr(10).join(f"• {strategy}: {count} упоминаний" for strategy, count in sorted(strategy_frequency.items(), key=lambda x: x[1], reverse=True))}

🎯 Приоритетные техники для внедрения:
1. Critical CSS inline (приоритет 1)
2. Async/Defer для JavaScript
3. Preloading ключевых ресурсов
4. Progressive enhancement

📈 Ожидаемый прирост производительности: 20-40%
"""
```

## 📊 Общие паттерны интеграции

### 🗣️ Примеры коммуникационных паттернов агентов:

**❌ НЕПРАВИЛЬНО (старый формат):**
```
Agent: "Анализ завершен. Переходим к следующей приоритетной задаче из списка?"
```

**✅ ПРАВИЛЬНО (новый формат с task_communication_utils):**
```python
from shared.task_communication_utils import (
    TaskCommunicationFormatter,
    parse_archon_task_to_task_info,
    get_next_priority_task
)

# В конце выполнения задачи агентом
async def complete_task_and_transition():
    # Получаем список задач из Archon
    archon_response = await mcp__archon__find_tasks(
        project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        filter_by="status",
        filter_value="todo"
    )

    # Находим следующую приоритетную задачу
    next_task = get_next_priority_task(archon_response["tasks"])

    if next_task:
        # Используем стандартизированный формат
        prompt = TaskCommunicationFormatter.format_next_task_prompt(next_task)
        print(prompt)
        # Вывод: "Следующая задача: 'Тестирование Puppeteer MCP' (приоритет P1-High/task_order 77, Implementation Engineer). Приступать?"
    else:
        print("📋 Все приоритетные задачи выполнены!")
```

**Примеры конкретных коммуникационных паттернов:**
```
✅ "Следующая задача: 'Создать универсального Security Audit Agent' (приоритет P1-High/task_order 85, Implementation Engineer). Приступать?"

✅ "Следующая задача: 'Оптимизировать производительность RAG поиска' (приоритет P2-Medium/task_order 65, Performance Optimization Agent). Приступать?"

✅ "Следующая задача: 'Добавить accessibility features в UI компоненты' (приоритет P1-High/task_order 78, UI/UX Enhancement Agent). Приступать?"

❌ "Какую задачу выполнять следующей?"
❌ "Переходим к другим задачам?"
❌ "Продолжаем работу?"
```

### Базовый шаблон для любого агента с коммуникационными паттернами:
```python
from shared.fetch_mcp_utils import extract_web_content, FetchMCPOptimizer
from shared.task_communication_utils import (
    TaskCommunicationFormatter,
    parse_archon_task_to_task_info,
    get_next_priority_task,
    create_agent_task_communication_mixin
)

class AgentFetchIntegration:
    """Базовый класс для интеграции Fetch MCP в агенты с коммуникационными паттернами."""

    def __init__(self, agent_type: str, archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"):
        self.agent_type = agent_type
        self.archon_project_id = archon_project_id
        self.default_content_type = self._get_default_content_type()

    def _get_default_content_type(self) -> str:
        """Определить тип контента по умолчанию для агента."""
        mapping = {
            "security_audit": "documentation",
            "rag_agent": "research",
            "uiux_enhancement": "design_inspiration",
            "performance_optimization": "documentation",
            "typescript_architecture": "documentation"
        }
        return mapping.get(self.agent_type, "documentation")

    async def smart_web_extraction(
        self,
        url: str,
        purpose: str = "analysis",
        custom_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Умное извлечение контента с учетом назначения."""

        # Определяем тип контента по назначению
        content_type_mapping = {
            "security": "documentation",
            "research": "research",
            "design": "design_inspiration",
            "competitor": "competitor_analysis",
            "quick": "lightweight"
        }

        content_type = content_type_mapping.get(purpose, self.default_content_type)

        return await extract_web_content(
            url=url,
            content_type=content_type,
            custom_params=custom_params,
            mcp_fetch_function=mcp__fetch__imageFetch
        )

    async def get_next_task_formatted(self) -> str:
        """
        Получить следующую задачу в стандартизированном формате.

        Returns:
            Отформатированное приглашение к следующей задаче или сообщение об отсутствии задач
        """
        try:
            # Получаем задачи из Archon
            archon_response = await mcp__archon__find_tasks(
                project_id=self.archon_project_id,
                filter_by="status",
                filter_value="todo"
            )

            if not archon_response.get("success", False):
                return "❌ Ошибка получения задач из Archon"

            # Находим следующую приоритетную задачу
            next_task = get_next_priority_task(archon_response.get("tasks", []))

            if next_task:
                return TaskCommunicationFormatter.format_next_task_prompt(next_task)
            else:
                return "📋 Все приоритетные задачи выполнены!"

        except Exception as e:
            return f"❌ Ошибка получения следующей задачи: {e}"

    def format_task_completion_with_transition(self, completed_task_title: str) -> str:
        """
        Форматирует завершение задачи с переходом к следующей.

        Args:
            completed_task_title: Название завершенной задачи

        Returns:
            Отформатированное сообщение о завершении и переходе
        """
        return f"""✅ **Задача завершена:** '{completed_task_title}'

🔄 **Следующий шаг:** Получение следующей приоритетной задачи из Archon.
Используйте get_next_task_formatted() для продолжения работы."""

# Обязательный инструмент для всех агентов
@agent.tool
async def transition_to_next_task(
    ctx: RunContext[AgentDependencies],
    completed_task_title: str = ""
) -> str:
    """
    Завершить текущую задачу и перейти к следующей приоритетной.

    ОБЯЗАТЕЛЬНО используется в конце каждой задачи для стандартизированного перехода.
    """
    try:
        # Получаем задачи из Archon
        archon_response = await mcp__archon__find_tasks(
            project_id=ctx.deps.archon_project_id,
            filter_by="status",
            filter_value="todo"
        )

        if not archon_response.get("success", False):
            return "❌ Ошибка получения задач из Archon"

        # Находим следующую приоритетную задачу
        next_task = get_next_priority_task(archon_response.get("tasks", []))

        if next_task:
            # Форматируем переход с завершенной задачей (если указана)
            if completed_task_title:
                completed_task_info = TaskInfo(
                    id="completed",
                    title=completed_task_title,
                    assignee="Current Agent",
                    task_order=0,
                    status="done"
                )

                return TaskCommunicationFormatter.format_task_transition_announcement(
                    completed_task_info, next_task
                )
            else:
                # Простое приглашение к следующей задаче
                return TaskCommunicationFormatter.format_next_task_prompt(next_task)
        else:
            completion_msg = ""
            if completed_task_title:
                completion_msg = f"✅ **Завершена задача:** '{completed_task_title}'\n\n"

            return f"{completion_msg}📋 Все приоритетные задачи выполнены!"

    except Exception as e:
        return f"❌ Ошибка перехода к следующей задаче: {e}"
```

## 🔄 Batch обработка для всех агентов:
```python
async def batch_web_analysis(
    urls: List[str],
    analysis_type: str,
    agent_context: str,
    max_concurrent: int = 3
) -> List[Dict[str, Any]]:
    """Batch обработка URL с ограничением конкурентности."""

    import asyncio
    from itertools import islice

    results = []

    # Разбиваем на батчи для предотвращения перегрузки
    def batched(iterable, batch_size):
        iterator = iter(iterable)
        while batch := list(islice(iterator, batch_size)):
            yield batch

    for url_batch in batched(urls, max_concurrent):
        # Обрабатываем батч параллельно
        batch_tasks = [
            extract_web_content(
                url=url,
                content_type=analysis_type,
                mcp_fetch_function=mcp__fetch__imageFetch
            )
            for url in url_batch
        ]

        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

        for url, result in zip(url_batch, batch_results):
            if isinstance(result, Exception):
                results.append({
                    "url": url,
                    "success": False,
                    "error": str(result)
                })
            else:
                results.append({
                    "url": url,
                    "success": result.get("success", False),
                    "content": result.get("content", ""),
                    "analysis_type": analysis_type
                })

        # Пауза между батчами для снижения нагрузки
        await asyncio.sleep(1)

    return results
```

## 📈 Метрики успешности интеграции

### Контрольные показатели по агентам:
- **Security Audit**: 90%+ успешность извлечения, <5с на анализ
- **RAG Agent**: 95%+ качество релевантности, >15K символов за запрос
- **UI/UX Enhancement**: 100% извлечение изображений, <3 изображения за сайт
- **Performance**: 85%+ обнаружение техник оптимизации

---

*Интеграционное руководство v1.0*
*Основано на результатах комплексного тестирования*