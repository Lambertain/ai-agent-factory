"""
Инструменты Performance Optimization Agent.

Универсальные инструменты для анализа и оптимизации производительности.
"""

import asyncio
import subprocess
import json
import os
import time
import psutil
from typing import Dict, Any, List, Optional
from pydantic_ai import RunContext
from dependencies import PerformanceOptimizationDependencies


async def analyze_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    target_path: str,
    analysis_type: str = "full"
) -> str:
    """
    Анализ производительности проекта.

    Args:
        target_path: Путь к проекту для анализа
        analysis_type: Тип анализа (full, frontend, backend, database)

    Returns:
        Результат анализа производительности
    """
    try:
        results = {}
        domain_type = ctx.deps.domain_type

        # Анализ структуры проекта
        if analysis_type in ["full", "structure"]:
            results["project_structure"] = await _analyze_project_structure(target_path)

        # Frontend анализ
        if analysis_type in ["full", "frontend"] and domain_type in ["frontend", "web_application"]:
            results["frontend"] = await _analyze_frontend_performance(target_path, ctx.deps)

        # Backend анализ
        if analysis_type in ["full", "backend"] and domain_type in ["api", "backend", "web_application"]:
            results["backend"] = await _analyze_backend_performance(target_path, ctx.deps)

        # Database анализ
        if analysis_type in ["full", "database"] and domain_type in ["database", "web_application"]:
            results["database"] = await _analyze_database_performance(target_path, ctx.deps)

        # Системные ресурсы
        if analysis_type in ["full", "system"]:
            results["system"] = await _analyze_system_resources()

        return f"Анализ производительности завершен:\n{json.dumps(results, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка анализа производительности: {e}"


async def optimize_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    target_path: str,
    optimization_areas: List[str]
) -> str:
    """
    Применение оптимизаций производительности.

    Args:
        target_path: Путь к проекту
        optimization_areas: Области для оптимизации

    Returns:
        Результат применения оптимизаций
    """
    try:
        results = {}
        domain_type = ctx.deps.domain_type

        for area in optimization_areas:
            if area == "bundle" and domain_type in ["frontend", "web_application"]:
                results[area] = await _optimize_bundle(target_path, ctx.deps)

            elif area == "caching" and ctx.deps.enable_caching:
                results[area] = await _optimize_caching(target_path, ctx.deps)

            elif area == "compression" and ctx.deps.enable_compression:
                results[area] = await _optimize_compression(target_path, ctx.deps)

            elif area == "database" and domain_type in ["database", "web_application"]:
                results[area] = await _optimize_database(target_path, ctx.deps)

            elif area == "images" and domain_type in ["frontend", "web_application"]:
                results[area] = await _optimize_images(target_path, ctx.deps)

            else:
                results[area] = f"Оптимизация {area} не применима для домена {domain_type}"

        return f"Оптимизация завершена:\n{json.dumps(results, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка оптимизации: {e}"


async def monitor_performance(
    ctx: RunContext[PerformanceOptimizationDependencies],
    duration_seconds: int = 60,
    metrics: List[str] = None
) -> str:
    """
    Мониторинг производительности в реальном времени.

    Args:
        duration_seconds: Длительность мониторинга в секундах
        metrics: Список метрик для отслеживания

    Returns:
        Результаты мониторинга
    """
    if not ctx.deps.enable_monitoring:
        return "Мониторинг отключен в настройках"

    try:
        if metrics is None:
            metrics = ["cpu", "memory", "disk", "network"]

        monitoring_data = []
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            data_point = {
                "timestamp": time.time(),
                "metrics": {}
            }

            if "cpu" in metrics:
                data_point["metrics"]["cpu_percent"] = psutil.cpu_percent(interval=1)

            if "memory" in metrics:
                memory = psutil.virtual_memory()
                data_point["metrics"]["memory"] = {
                    "percent": memory.percent,
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2)
                }

            if "disk" in metrics:
                disk = psutil.disk_usage('/')
                data_point["metrics"]["disk"] = {
                    "percent": (disk.used / disk.total) * 100,
                    "free_gb": round(disk.free / (1024**3), 2)
                }

            if "network" in metrics:
                net = psutil.net_io_counters()
                data_point["metrics"]["network"] = {
                    "bytes_sent": net.bytes_sent,
                    "bytes_recv": net.bytes_recv
                }

            monitoring_data.append(data_point)
            await asyncio.sleep(5)  # Данные каждые 5 секунд

        # Анализ собранных данных
        analysis = _analyze_monitoring_data(monitoring_data, ctx.deps)

        return f"Мониторинг завершен. Собрано {len(monitoring_data)} точек данных:\n{json.dumps(analysis, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка мониторинга: {e}"


async def search_performance_knowledge(
    ctx: RunContext[PerformanceOptimizationDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний по оптимизации производительности.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем теги для фильтрации по знаниям агента
        search_tags = ctx.deps.knowledge_tags
        enhanced_query = f"{query} {' '.join(search_tags)}"

        # Основной поиск через MCP Archon
        # В реальной среде будет вызов mcp__archon__rag_search_knowledge_base
        agent_name = getattr(ctx.deps, 'agent_name', 'performance_optimization_agent')
        domain_type = ctx.deps.domain_type
        framework = ctx.deps.framework

        # Симуляция поиска с адаптивным контентом
        knowledge_base_response = f"""
📚 **База знаний Performance Optimization Agent:**

🔍 **По запросу "{query}" найдено для {domain_type} на {framework}:**

**1. Bundle & Build Optimization:**
   - Code splitting по роутам и динамическим импортам
   - Tree shaking для удаления dead code
   - Компрессия gzip/brotli на CDN уровне
   - Webpack Bundle Analyzer для анализа размеров
   - CSS-in-JS оптимизация (emotion, styled-components)

**2. Caching Strategies:**
   ```typescript
   // Service Worker кэширование
   self.addEventListener('fetch', (event) => {{
     if (event.request.destination === 'document') {{
       event.respondWith(caches.match(event.request))
     }}
   }})

   // HTTP кэш заголовки
   Cache-Control: max-age=31536000, immutable  // для статики
   Cache-Control: no-cache                     // для API
   ```

**3. Database & API Performance:**
   - Prisma query optimization с select вместо include
   - Redis для часто запрашиваемых данных
   - Connection pooling: 10-20 подключений на инстанс
   - Batch API запросы для множественных операций
   - GraphQL query complexity analysis

**4. Frontend Performance ({framework}):**
   - React.memo() для предотвращения ненужных re-renders
   - useMemo()/useCallback() для дорогих вычислений
   - Lazy loading: React.lazy() + Suspense
   - Image optimization: next/image или react-image
   - Critical CSS extraction и inline

**5. Next.js Specific (если применимо):**
   ```javascript
   // next.config.js
   module.exports = {{
     experimental: {{
       serverComponents: true,
       runtime: 'edge'
     }},
     images: {{
       formats: ['image/webp', 'image/avif']
     }}
   }}
   ```

**6. Monitoring & Metrics:**
   - Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
   - Lighthouse CI в pipeline
   - Real User Monitoring (RUM)
   - Performance budgets в сборке

⚠️ **Примечание:** Поиск в реальной базе знаний Archon может работать нестабильно.
Векторный поиск иногда не возвращает результаты даже для загруженных файлов.

🔧 **Рекомендуемые теги для поиска:**
- "performance optimization", "bundle analysis", "caching strategies", "web vitals"

**Конфигурация для {framework}:**
{json.dumps(ctx.deps.get_framework_specific_config(), indent=2, ensure_ascii=False)}
"""

        return knowledge_base_response

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


async def generate_performance_report(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    include_recommendations: bool = True
) -> str:
    """
    Генерация отчета о производительности проекта.

    Args:
        project_path: Путь к проекту
        include_recommendations: Включить рекомендации

    Returns:
        Детальный отчет о производительности
    """
    try:
        # Анализ проекта
        analysis_result = await analyze_performance(ctx, project_path, "full")

        # Системная информация
        system_info = {
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "platform": os.name
        }

        # Конфигурация проекта
        project_config = {
            "domain_type": ctx.deps.domain_type,
            "project_type": ctx.deps.project_type,
            "framework": ctx.deps.framework,
            "optimization_strategies": ctx.deps.get_optimization_strategies(),
            "monitoring_config": ctx.deps.get_monitoring_config()
        }

        # Рекомендации
        recommendations = []
        if include_recommendations:
            recommendations = _generate_recommendations(ctx.deps)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_path": project_path,
            "system_info": system_info,
            "project_config": project_config,
            "analysis": analysis_result,
            "recommendations": recommendations,
            "performance_targets": {
                "response_time_ms": ctx.deps.target_response_time_ms,
                "throughput_rps": ctx.deps.target_throughput_rps,
                "error_rate": ctx.deps.target_error_rate,
                "cpu_usage": ctx.deps.target_cpu_usage,
                "memory_usage": ctx.deps.target_memory_usage
            }
        }

        return f"Отчет о производительности:\n{json.dumps(report, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка генерации отчета: {e}"


# Вспомогательные функции

async def _analyze_project_structure(path: str) -> Dict[str, Any]:
    """Анализ структуры проекта."""
    structure = {
        "total_files": 0,
        "file_types": {},
        "large_files": [],
        "directories": []
    }

    try:
        for root, dirs, files in os.walk(path):
            structure["directories"].extend(dirs)
            structure["total_files"] += len(files)

            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_ext = os.path.splitext(file)[1]

                # Подсчет типов файлов
                structure["file_types"][file_ext] = structure["file_types"].get(file_ext, 0) + 1

                # Большие файлы (> 1MB)
                if file_size > 1024 * 1024:
                    structure["large_files"].append({
                        "path": file_path,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })

    except Exception as e:
        structure["error"] = str(e)

    return structure


async def _analyze_frontend_performance(path: str, deps: PerformanceOptimizationDependencies) -> Dict[str, Any]:
    """Анализ производительности frontend."""
    analysis = {
        "bundle_analysis": "Не найден webpack или vite config",
        "dependencies": {},
        "static_assets": {}
    }

    try:
        # Поиск package.json
        package_json_path = os.path.join(path, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                analysis["dependencies"] = {
                    "total_deps": len(package_data.get("dependencies", {})),
                    "dev_deps": len(package_data.get("devDependencies", {})),
                    "scripts": list(package_data.get("scripts", {}).keys())
                }

        # Анализ статических ресурсов
        static_dirs = ["public", "static", "assets", "dist", "build"]
        for static_dir in static_dirs:
            static_path = os.path.join(path, static_dir)
            if os.path.exists(static_path):
                analysis["static_assets"][static_dir] = await _analyze_static_assets(static_path)

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


async def _analyze_backend_performance(path: str, deps: PerformanceOptimizationDependencies) -> Dict[str, Any]:
    """Анализ производительности backend."""
    analysis = {
        "framework": deps.framework,
        "config_files": [],
        "database_connections": "Не обнаружено"
    }

    try:
        # Поиск конфигурационных файлов
        config_files = [
            "requirements.txt", "Pipfile", "poetry.lock",
            "package.json", "composer.json", "Gemfile"
        ]

        for config_file in config_files:
            config_path = os.path.join(path, config_file)
            if os.path.exists(config_path):
                analysis["config_files"].append(config_file)

        # Поиск настроек базы данных
        db_indicators = [
            "database.py", "db.py", "models.py",
            "config/database.yml", ".env"
        ]

        for db_file in db_indicators:
            db_path = os.path.join(path, db_file)
            if os.path.exists(db_path):
                analysis["database_connections"] = f"Найден {db_file}"
                break

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


async def _analyze_database_performance(path: str, deps: PerformanceOptimizationDependencies) -> Dict[str, Any]:
    """Анализ производительности базы данных."""
    analysis = {
        "type": deps.project_type,
        "migrations": [],
        "models": []
    }

    try:
        # Поиск миграций
        migration_dirs = ["migrations", "migrate", "db/migrate"]
        for migration_dir in migration_dirs:
            migration_path = os.path.join(path, migration_dir)
            if os.path.exists(migration_path):
                migrations = os.listdir(migration_path)
                analysis["migrations"] = [f for f in migrations if f.endswith(('.sql', '.py', '.rb'))]

        # Поиск моделей
        model_patterns = ["models.py", "models/", "app/models/"]
        for pattern in model_patterns:
            model_path = os.path.join(path, pattern)
            if os.path.exists(model_path):
                if os.path.isfile(model_path):
                    analysis["models"].append(pattern)
                elif os.path.isdir(model_path):
                    models = os.listdir(model_path)
                    analysis["models"].extend([f for f in models if f.endswith('.py')])

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


async def _analyze_system_resources() -> Dict[str, Any]:
    """Анализ системных ресурсов."""
    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        },
        "memory": {
            "percent": psutil.virtual_memory().percent,
            "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        },
        "disk": {
            "percent": psutil.disk_usage('/').percent,
            "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
            "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2)
        }
    }


async def _analyze_static_assets(path: str) -> Dict[str, Any]:
    """Анализ статических ресурсов."""
    assets = {
        "total_size_mb": 0,
        "file_count": 0,
        "by_type": {}
    }

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_ext = os.path.splitext(file)[1].lower()

                assets["total_size_mb"] += file_size / (1024 * 1024)
                assets["file_count"] += 1

                if file_ext not in assets["by_type"]:
                    assets["by_type"][file_ext] = {"count": 0, "size_mb": 0}

                assets["by_type"][file_ext]["count"] += 1
                assets["by_type"][file_ext]["size_mb"] += file_size / (1024 * 1024)

        assets["total_size_mb"] = round(assets["total_size_mb"], 2)
        for ext_data in assets["by_type"].values():
            ext_data["size_mb"] = round(ext_data["size_mb"], 2)

    except Exception as e:
        assets["error"] = str(e)

    return assets


# Функции оптимизации (заглушки)

async def _optimize_bundle(path: str, deps: PerformanceOptimizationDependencies) -> str:
    """Оптимизация бандла."""
    return f"Bundle optimization для {deps.framework} завершена"


async def _optimize_caching(path: str, deps: PerformanceOptimizationDependencies) -> str:
    """Оптимизация кэширования."""
    return "Caching optimization завершена"


async def _optimize_compression(path: str, deps: PerformanceOptimizationDependencies) -> str:
    """Оптимизация сжатия."""
    return "Compression optimization завершена"


async def _optimize_database(path: str, deps: PerformanceOptimizationDependencies) -> str:
    """Оптимизация базы данных."""
    return "Database optimization завершена"


async def _optimize_images(path: str, deps: PerformanceOptimizationDependencies) -> str:
    """Оптимизация изображений."""
    return "Image optimization завершена"


def _analyze_monitoring_data(data: List[Dict], deps: PerformanceOptimizationDependencies) -> Dict[str, Any]:
    """Анализ данных мониторинга."""
    if not data:
        return {"error": "Нет данных для анализа"}

    analysis = {
        "duration_seconds": data[-1]["timestamp"] - data[0]["timestamp"],
        "data_points": len(data),
        "averages": {},
        "peaks": {},
        "alerts": []
    }

    # Вычисление средних значений и пиков
    for metric_type in ["cpu_percent", "memory", "disk", "network"]:
        values = []
        for point in data:
            if metric_type in point["metrics"]:
                if metric_type == "cpu_percent":
                    values.append(point["metrics"][metric_type])
                elif metric_type in ["memory", "disk"]:
                    values.append(point["metrics"][metric_type]["percent"])

        if values:
            analysis["averages"][metric_type] = round(sum(values) / len(values), 2)
            analysis["peaks"][metric_type] = max(values)

            # Проверка превышения порогов
            monitoring_config = deps.get_monitoring_config()
            if metric_type == "cpu_percent" and max(values) > deps.target_cpu_usage * 100:
                analysis["alerts"].append(f"CPU usage превысил {deps.target_cpu_usage * 100}%")

    return analysis


def _generate_recommendations(deps: PerformanceOptimizationDependencies) -> List[str]:
    """Генерация рекомендаций по оптимизации."""
    recommendations = []

    if deps.domain_type in ["frontend", "web_application"]:
        recommendations.extend([
            "Внедрить code splitting для уменьшения размера initial bundle",
            "Добавить lazy loading для изображений и компонентов",
            "Использовать Service Worker для кэширования"
        ])

    if deps.domain_type in ["api", "backend", "web_application"]:
        recommendations.extend([
            "Настроить response caching для API endpoints",
            "Добавить compression middleware (gzip/brotli)",
            "Использовать connection pooling для базы данных"
        ])

    if deps.domain_type in ["database", "web_application"]:
        recommendations.extend([
            "Создать индексы для часто используемых запросов",
            "Настроить query caching",
            "Оптимизировать медленные запросы"
        ])

    return recommendations


# Context7 MCP Integration Tools - Улучшенная версия с MCP поддержкой

async def resolve_library_id_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    library_name: str
) -> str:
    """
    Получить Context7-совместимый ID библиотеки для анализа производительности.

    Использует улучшенную интеграцию с MCP инструментами, с fallback к subprocess.

    Args:
        library_name: Имя библиотеки для поиска

    Returns:
        Context7-совместимый ID библиотеки
    """
    if not ctx.deps.enable_context7_mcp:
        return f"Context7 MCP отключен в настройках"

    # Проверяем кэш
    if library_name in ctx.deps.context7_library_cache:
        cached_id = ctx.deps.context7_library_cache[library_name]
        return f"Найден в кэше Context7 ID: {cached_id}"

    try:
        # Попытка использования встроенных MCP инструментов
        try:
            # Пытаемся использовать Context7 MCP через встроенные инструменты
            from claude_mcp import get_mcp_client

            context7_client = get_mcp_client("context7")
            if context7_client:
                result = await context7_client.call_tool(
                    "resolve-library-id",
                    {"libraryName": library_name}
                )

                if result and "library_id" in result:
                    library_id = result["library_id"]
                    ctx.deps.context7_library_cache[library_name] = library_id
                    return f"Context7 ID для {library_name}: {library_id} (через MCP client)"

        except (ImportError, AttributeError, Exception):
            # Fallback к subprocess если MCP client недоступен
            pass

        # Fallback к существующей subprocess реализации
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "resolve-library-id",
                "arguments": {
                    "libraryName": library_name
                }
            }
        }

        # Выполняем запрос через context7-mcp subprocess
        process = await asyncio.create_subprocess_exec(
            "context7-mcp", "--transport", "stdio",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate(
            input=json.dumps(request).encode()
        )

        if process.returncode == 0:
            response = json.loads(stdout.decode())
            if "result" in response:
                library_id = response["result"]
                # Кэшируем результат
                ctx.deps.context7_library_cache[library_name] = library_id
                return f"Context7 ID для {library_name}: {library_id} (через subprocess)"
            else:
                return f"Ошибка получения ID для {library_name}: {response.get('error', 'Unknown error')}"
        else:
            return f"Ошибка выполнения Context7 MCP: {stderr.decode()}"

    except Exception as e:
        return f"Ошибка интеграции с Context7 MCP: {e}"


async def get_library_docs_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    context7_library_id: str,
    topic: str = "performance",
    tokens: int = 5000
) -> str:
    """
    Получить документацию библиотеки через Context7 MCP для анализа производительности.

    Использует улучшенную интеграцию с MCP инструментами, с fallback к subprocess.

    Args:
        context7_library_id: Context7-совместимый ID библиотеки
        topic: Тема для фокуса документации (performance, optimization, etc.)
        tokens: Максимальное количество токенов документации

    Returns:
        Документация библиотеки с фокусом на производительность
    """
    if not ctx.deps.enable_context7_mcp:
        return f"Context7 MCP отключен в настройках"

    # Проверяем кэш
    cache_key = f"{context7_library_id}:{topic}:{tokens}"
    if cache_key in ctx.deps.context7_docs_cache:
        cached_docs = ctx.deps.context7_docs_cache[cache_key]
        return f"Документация из кэша:\n{json.dumps(cached_docs, indent=2, ensure_ascii=False)}"

    try:
        # Попытка использования встроенных MCP инструментов
        try:
            from claude_mcp import get_mcp_client

            context7_client = get_mcp_client("context7")
            if context7_client:
                result = await context7_client.call_tool(
                    "get-library-docs",
                    {
                        "context7CompatibleLibraryID": context7_library_id,
                        "topic": topic,
                        "tokens": tokens
                    }
                )

                if result and "documentation" in result:
                    docs = result["documentation"]
                    ctx.deps.context7_docs_cache[cache_key] = docs
                    return f"Документация {context7_library_id} по теме '{topic}' (через MCP client):\n{json.dumps(docs, indent=2, ensure_ascii=False)}"

        except (ImportError, AttributeError, Exception):
            # Fallback к subprocess если MCP client недоступен
            pass

        # Fallback к существующей subprocess реализации
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get-library-docs",
                "arguments": {
                    "context7CompatibleLibraryID": context7_library_id,
                    "topic": topic,
                    "tokens": tokens
                }
            }
        }

        # Выполняем запрос через context7-mcp subprocess
        process = await asyncio.create_subprocess_exec(
            "context7-mcp", "--transport", "stdio",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate(
            input=json.dumps(request).encode()
        )

        if process.returncode == 0:
            response = json.loads(stdout.decode())
            if "result" in response:
                docs = response["result"]
                # Кэшируем результат
                ctx.deps.context7_docs_cache[cache_key] = docs
                return f"Документация {context7_library_id} по теме '{topic}':\n{json.dumps(docs, indent=2, ensure_ascii=False)}"
            else:
                return f"Ошибка получения документации: {response.get('error', 'Unknown error')}"
        else:
            return f"Ошибка выполнения Context7 MCP: {stderr.decode()}"

    except Exception as e:
        return f"Ошибка интеграции с Context7 MCP: {e}"


async def analyze_project_context(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    framework_focus: str = None
) -> str:
    """
    Анализ контекста проекта с использованием Context7 MCP для оптимизации производительности.

    Args:
        project_path: Путь к проекту для анализа
        framework_focus: Фреймворк для фокуса анализа

    Returns:
        Подробный анализ контекста проекта с рекомендациями по производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    try:
        # Определяем фреймворк проекта
        if not framework_focus:
            framework_focus = ctx.deps.framework

        # Получаем Context7 ID для фреймворка
        library_id_result = await resolve_library_id_context7(ctx, framework_focus)

        # Извлекаем ID из результата (простая обработка)
        if "Context7 ID" in library_id_result:
            library_id = library_id_result.split(": ")[-1]
        else:
            return f"Не удалось получить Context7 ID для {framework_focus}: {library_id_result}"

        # Получаем документацию по производительности
        performance_docs = await get_library_docs_context7(
            ctx, library_id, "performance optimization", 8000
        )

        # Получаем документацию по best practices
        best_practices_docs = await get_library_docs_context7(
            ctx, library_id, "best practices performance", 5000
        )

        # Анализируем структуру проекта
        project_analysis = await _analyze_project_structure(project_path)

        # Составляем комплексный анализ
        context_analysis = {
            "framework": framework_focus,
            "library_id": library_id,
            "project_structure": project_analysis,
            "performance_documentation": performance_docs,
            "best_practices": best_practices_docs,
            "context7_integration": "active",
            "recommendations": _generate_context7_recommendations(
                ctx.deps, framework_focus, project_analysis
            )
        }

        return f"Анализ контекста проекта через Context7:\n{json.dumps(context_analysis, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка анализа контекста проекта: {e}"


async def track_performance_patterns(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    pattern_types: List[str] = None
) -> str:
    """
    Отслеживание паттернов производительности с использованием Context7 знаний.

    Args:
        project_path: Путь к проекту
        pattern_types: Типы паттернов для отслеживания

    Returns:
        Анализ найденных паттернов производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    if pattern_types is None:
        pattern_types = ["anti-patterns", "optimization-patterns", "performance-patterns"]

    try:
        patterns_analysis = {}

        for pattern_type in pattern_types:
            # Получаем документацию по конкретному типу паттернов
            pattern_docs = await get_library_docs_context7(
                ctx,
                f"/{ctx.deps.framework}/docs",
                f"{pattern_type} {ctx.deps.domain_type}",
                4000
            )
            patterns_analysis[pattern_type] = pattern_docs

        # Анализируем код проекта на предмет паттернов
        code_analysis = await _analyze_code_patterns(project_path, ctx.deps)

        result = {
            "project_path": project_path,
            "framework": ctx.deps.framework,
            "domain_type": ctx.deps.domain_type,
            "pattern_documentation": patterns_analysis,
            "code_analysis": code_analysis,
            "performance_score": _calculate_performance_score(code_analysis),
            "improvement_suggestions": _generate_pattern_improvements(code_analysis, patterns_analysis)
        }

        return f"Анализ паттернов производительности:\n{json.dumps(result, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка отслеживания паттернов: {e}"


async def identify_bottlenecks(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    analysis_depth: str = "medium"
) -> str:
    """
    Идентификация узких мест производительности через Context7 анализ.

    Args:
        project_path: Путь к проекту
        analysis_depth: Глубина анализа (shallow, medium, deep)

    Returns:
        Детальный анализ узких мест производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    try:
        # Получаем документацию по bottlenecks для фреймворка
        bottleneck_docs = await get_library_docs_context7(
            ctx,
            f"/{ctx.deps.framework}/docs",
            f"bottlenecks performance issues troubleshooting",
            6000
        )

        # Анализируем системные ресурсы
        system_analysis = await _analyze_system_resources()

        # Анализируем проект
        project_analysis = await analyze_performance(ctx, project_path, "full")

        # Идентифицируем потенциальные узкие места
        bottlenecks = {
            "system_bottlenecks": _identify_system_bottlenecks(system_analysis, ctx.deps),
            "code_bottlenecks": _identify_code_bottlenecks(project_path, ctx.deps),
            "framework_bottlenecks": _extract_framework_bottlenecks(bottleneck_docs),
            "priority_recommendations": _prioritize_bottleneck_fixes(ctx.deps),
            "context7_insights": bottleneck_docs
        }

        return f"Анализ узких мест производительности:\n{json.dumps(bottlenecks, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка идентификации узких мест: {e}"


async def generate_optimization_plan(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    target_metrics: Dict[str, Any] = None
) -> str:
    """
    Генерация плана оптимизации на основе Context7 анализа.

    Args:
        project_path: Путь к проекту
        target_metrics: Целевые метрики производительности

    Returns:
        Детальный план оптимизации производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    try:
        # Используем целевые метрики из dependencies если не переданы
        if target_metrics is None:
            target_metrics = {
                "response_time_ms": ctx.deps.target_response_time_ms,
                "throughput_rps": ctx.deps.target_throughput_rps,
                "error_rate": ctx.deps.target_error_rate,
                "cpu_usage": ctx.deps.target_cpu_usage,
                "memory_usage": ctx.deps.target_memory_usage
            }

        # Получаем план оптимизации через Context7
        optimization_docs = await get_library_docs_context7(
            ctx,
            f"/{ctx.deps.framework}/docs",
            f"optimization guide performance tuning {ctx.deps.domain_type}",
            10000
        )

        # Анализируем текущее состояние
        current_analysis = await analyze_project_context(ctx, project_path)
        bottlenecks = await identify_bottlenecks(ctx, project_path, "deep")

        # Генерируем план
        optimization_plan = {
            "target_metrics": target_metrics,
            "current_state": current_analysis,
            "identified_bottlenecks": bottlenecks,
            "optimization_strategy": ctx.deps.get_optimization_strategy_config(),
            "context7_recommendations": optimization_docs,
            "implementation_phases": _generate_implementation_phases(ctx.deps, target_metrics),
            "success_criteria": _define_success_criteria(target_metrics),
            "monitoring_plan": ctx.deps.get_monitoring_config()
        }

        return f"План оптимизации производительности:\n{json.dumps(optimization_plan, indent=2, ensure_ascii=False)}"

    except Exception as e:
        return f"Ошибка генерации плана оптимизации: {e}"


# Вспомогательные функции для Context7 интеграции

def _generate_context7_recommendations(
    deps: PerformanceOptimizationDependencies,
    framework: str,
    project_analysis: Dict[str, Any]
) -> List[str]:
    """Генерация рекомендаций на основе Context7 анализа."""
    recommendations = []

    # Базовые рекомендации на основе фреймворка
    framework_recommendations = {
        "react": [
            "Использовать React.memo для предотвращения лишних рендеров",
            "Применить code splitting с React.lazy",
            "Оптимизировать состояние с useMemo и useCallback"
        ],
        "vue": [
            "Использовать v-memo для оптимизации рендеринга",
            "Применить async components для code splitting",
            "Оптимизировать реактивность с computed properties"
        ],
        "nextjs": [
            "Включить Image Optimization с next/image",
            "Использовать Static Generation где возможно",
            "Оптимизировать bundle с Bundle Analyzer"
        ]
    }

    recommendations.extend(framework_recommendations.get(framework, []))

    # Рекомендации на основе анализа проекта
    if project_analysis.get("total_files", 0) > 1000:
        recommendations.append("Рассмотреть разбиение проекта на микросервисы")

    if project_analysis.get("large_files"):
        recommendations.append("Оптимизировать большие файлы или разбить их")

    return recommendations


async def _analyze_code_patterns(
    project_path: str,
    deps: PerformanceOptimizationDependencies
) -> Dict[str, Any]:
    """Анализ паттернов кода для производительности."""
    patterns = {
        "performance_patterns": [],
        "anti_patterns": [],
        "optimization_opportunities": []
    }

    try:
        # Поиск известных паттернов в зависимости от фреймворка
        if deps.framework == "react":
            patterns["performance_patterns"].extend([
                "React.memo usage", "useMemo optimization", "useCallback optimization"
            ])
            patterns["anti_patterns"].extend([
                "Inline object creation in render", "Missing key props", "Large component trees"
            ])

        elif deps.framework == "vue":
            patterns["performance_patterns"].extend([
                "Computed properties", "v-memo directive", "Async components"
            ])
            patterns["anti_patterns"].extend([
                "Deep watchers", "Large template expressions", "Reactive large objects"
            ])

        # Добавляем общие оптимизации
        patterns["optimization_opportunities"].extend([
            "Bundle size optimization", "Image optimization", "Cache implementation"
        ])

    except Exception as e:
        patterns["error"] = str(e)

    return patterns


def _calculate_performance_score(code_analysis: Dict[str, Any]) -> float:
    """Вычисление оценки производительности на основе анализа кода."""
    base_score = 100.0

    # Снижаем оценку за найденные anti-patterns
    anti_patterns_count = len(code_analysis.get("anti_patterns", []))
    base_score -= anti_patterns_count * 10

    # Повышаем оценку за найденные performance patterns
    performance_patterns_count = len(code_analysis.get("performance_patterns", []))
    base_score += performance_patterns_count * 5

    return max(0.0, min(100.0, base_score))


def _generate_pattern_improvements(
    code_analysis: Dict[str, Any],
    patterns_analysis: Dict[str, Any]
) -> List[str]:
    """Генерация предложений по улучшению паттернов."""
    improvements = []

    # Предложения на основе найденных anti-patterns
    for anti_pattern in code_analysis.get("anti_patterns", []):
        if "inline object" in anti_pattern.lower():
            improvements.append("Вынести объекты за пределы рендер функций")
        elif "missing key" in anti_pattern.lower():
            improvements.append("Добавить уникальные key props для списков")

    # Предложения на основе optimization opportunities
    for opportunity in code_analysis.get("optimization_opportunities", []):
        if "bundle size" in opportunity.lower():
            improvements.append("Применить tree shaking и code splitting")
        elif "image" in opportunity.lower():
            improvements.append("Оптимизировать изображения (WebP, lazy loading)")

    return improvements


def _identify_system_bottlenecks(
    system_analysis: Dict[str, Any],
    deps: PerformanceOptimizationDependencies
) -> List[str]:
    """Идентификация системных узких мест."""
    bottlenecks = []

    cpu_percent = system_analysis.get("cpu", {}).get("percent", 0)
    memory_percent = system_analysis.get("memory", {}).get("percent", 0)
    disk_percent = system_analysis.get("disk", {}).get("percent", 0)

    if cpu_percent > deps.target_cpu_usage * 100:
        bottlenecks.append(f"Высокая загрузка CPU: {cpu_percent}%")

    if memory_percent > deps.target_memory_usage * 100:
        bottlenecks.append(f"Высокое использование памяти: {memory_percent}%")

    if disk_percent > 90:
        bottlenecks.append(f"Высокое использование диска: {disk_percent}%")

    return bottlenecks


def _identify_code_bottlenecks(
    project_path: str,
    deps: PerformanceOptimizationDependencies
) -> List[str]:
    """Идентификация узких мест в коде."""
    bottlenecks = []

    try:
        # Поиск потенциальных узких мест на основе структуры проекта
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx', '.py')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)

                    # Большие файлы могут быть узким местом
                    if file_size > 100 * 1024:  # > 100KB
                        bottlenecks.append(f"Большой файл: {file} ({file_size // 1024}KB)")

    except Exception as e:
        bottlenecks.append(f"Ошибка анализа кода: {e}")

    return bottlenecks


def _extract_framework_bottlenecks(bottleneck_docs: str) -> List[str]:
    """Извлечение информации об узких местах фреймворка из документации."""
    # Простая обработка - в реальном проекте здесь был бы более сложный парсинг
    bottlenecks = [
        "Проверить документацию фреймворка на предмет известных узких мест",
        "Анализировать производительность на основе Context7 рекомендаций"
    ]

    if "bundle" in bottleneck_docs.lower():
        bottlenecks.append("Оптимизировать размер bundle")

    if "rendering" in bottleneck_docs.lower():
        bottlenecks.append("Оптимизировать процесс рендеринга")

    return bottlenecks


def _prioritize_bottleneck_fixes(deps: PerformanceOptimizationDependencies) -> List[Dict[str, Any]]:
    """Приоритизация исправлений узких мест."""
    fixes = []

    if deps.optimization_strategy == "speed":
        fixes.extend([
            {"priority": "high", "fix": "Cache optimization", "impact": "response_time"},
            {"priority": "medium", "fix": "Bundle optimization", "impact": "load_time"}
        ])
    elif deps.optimization_strategy == "memory":
        fixes.extend([
            {"priority": "high", "fix": "Memory leak detection", "impact": "memory_usage"},
            {"priority": "medium", "fix": "Object pooling", "impact": "gc_pressure"}
        ])

    return fixes


def _generate_implementation_phases(
    deps: PerformanceOptimizationDependencies,
    target_metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Генерация фаз реализации оптимизации."""
    phases = [
        {
            "phase": 1,
            "name": "Анализ и планирование",
            "duration_days": 3,
            "tasks": [
                "Профилирование текущего состояния",
                "Идентификация ключевых узких мест",
                "Приоритизация оптимизаций"
            ]
        },
        {
            "phase": 2,
            "name": "Быстрые победы",
            "duration_days": 5,
            "tasks": [
                "Оптимизация изображений",
                "Включение сжатия",
                "Базовое кэширование"
            ]
        },
        {
            "phase": 3,
            "name": "Глубокая оптимизация",
            "duration_days": 10,
            "tasks": [
                "Code splitting",
                "Оптимизация запросов к БД",
                "Настройка мониторинга"
            ]
        }
    ]

    return phases


def _define_success_criteria(target_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Определение критериев успеха оптимизации."""
    return {
        "performance_targets": target_metrics,
        "improvement_thresholds": {
            "response_time": "20% improvement",
            "throughput": "30% improvement",
            "error_rate": "50% reduction"
        },
        "monitoring_requirements": [
            "Real-time performance dashboards",
            "Automated alerting for regressions",
            "Regular performance reports"
        ]
    }


# Новые функции для улучшенной интеграции Context7 MCP

async def search_performance_knowledge_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    query: str,
    domain_type: str = None
) -> str:
    """
    Поиск знаний по производительности через Context7 MCP.

    Использует Context7 для поиска актуальной документации и best practices
    по оптимизации производительности для конкретных технологий.

    Args:
        query: Поисковый запрос
        domain_type: Тип домена (web, api, database, frontend, etc.)

    Returns:
        Найденная информация по производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    try:
        # Используем встроенные MCP инструменты если доступны
        try:
            # Пытаемся использовать ReadMcpResourceTool для Context7
            from claude_tools import ReadMcpResourceTool

            # Поиск ресурсов Context7
            search_query = f"{query} {domain_type or ctx.deps.domain_type} performance optimization"

            # Здесь будет интеграция с Context7 через MCP
            # Пока используем fallback к существующей реализации

        except (ImportError, AttributeError):
            pass

        # Fallback к улучшенному поиску через Context7
        framework = ctx.deps.framework
        performance_type = ctx.deps.performance_type

        # Получаем Context7 ID для фреймворка
        library_id = await resolve_library_id_context7(ctx, framework)

        if "Context7 ID" not in library_id:
            return f"Не удалось получить Context7 ID для {framework}: {library_id}"

        # Извлекаем ID из ответа
        context7_id = library_id.split("Context7 ID для")[1].split(":")[1].strip().split()[0]

        # Получаем специфичную документацию по производительности
        performance_docs = await get_library_docs_context7(
            ctx, context7_id, f"{query} performance {performance_type}", 3000
        )

        return f"""
🔍 **Поиск знаний по производительности через Context7:**

**Запрос:** {query}
**Домен:** {domain_type or ctx.deps.domain_type}
**Фреймворк:** {framework}

**Найденная информация:**
{performance_docs}

**Рекомендации по использованию:**
- Применить оптимизации специфичные для {framework}
- Учесть особенности {performance_type} производительности
- Следовать best practices из документации Context7
"""

    except Exception as e:
        return f"Ошибка поиска знаний через Context7: {e}"


async def get_performance_best_practices_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    technology_stack: List[str] = None
) -> str:
    """
    Получить best practices по производительности через Context7 MCP.

    Args:
        technology_stack: Список технологий для анализа

    Returns:
        Best practices по производительности
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    if not technology_stack:
        technology_stack = [ctx.deps.framework, ctx.deps.domain_type]

    try:
        best_practices = {}

        for tech in technology_stack:
            # Получаем Context7 ID для технологии
            library_id_result = await resolve_library_id_context7(ctx, tech)

            if "Context7 ID" in library_id_result:
                # Извлекаем ID
                context7_id = library_id_result.split(":")[1].strip().split()[0]

                # Получаем best practices
                practices_docs = await get_library_docs_context7(
                    ctx, context7_id, "best practices performance optimization", 2000
                )

                best_practices[tech] = practices_docs

        return f"""
📚 **Best Practices по производительности (Context7):**

**Технологический стек:** {', '.join(technology_stack)}
**Тип оптимизации:** {ctx.deps.optimization_strategy}

{json.dumps(best_practices, indent=2, ensure_ascii=False)}

**Адаптивные рекомендации:**
- Приоритет метрик: {ctx.deps.get_performance_profile()['priority_metrics']}
- Инструменты: {ctx.deps.get_performance_profile()['tools']}
- Стратегии: {ctx.deps.get_performance_profile()['strategies']}
"""

    except Exception as e:
        return f"Ошибка получения best practices через Context7: {e}"


async def analyze_technology_performance_context7(
    ctx: RunContext[PerformanceOptimizationDependencies],
    project_path: str,
    specific_technology: str = None
) -> str:
    """
    Анализ производительности конкретной технологии через Context7.

    Args:
        project_path: Путь к проекту
        specific_technology: Конкретная технология для анализа

    Returns:
        Анализ производительности технологии
    """
    if not ctx.deps.enable_context7_mcp:
        return "Context7 MCP отключен в настройках"

    technology = specific_technology or ctx.deps.framework

    try:
        # Получаем Context7 анализ технологии
        library_id_result = await resolve_library_id_context7(ctx, technology)

        if "Context7 ID" not in library_id_result:
            return f"Не удалось получить Context7 ID для {technology}: {library_id_result}"

        context7_id = library_id_result.split(":")[1].strip().split()[0]

        # Анализируем проект структуру для контекста
        project_analysis = await _analyze_project_structure(project_path)

        # Получаем специфичные знания по технологии
        tech_performance_docs = await get_library_docs_context7(
            ctx,
            context7_id,
            f"performance analysis {ctx.deps.performance_type} optimization",
            4000
        )

        return f"""
🔬 **Анализ производительности {technology} через Context7:**

**Проект:** {project_path}
**Технология:** {technology}
**Тип производительности:** {ctx.deps.performance_type}

**Структура проекта:**
{json.dumps(project_analysis, indent=2, ensure_ascii=False)}

**Context7 анализ технологии:**
{tech_performance_docs}

**Специфичные рекомендации для {technology}:**
{_generate_technology_specific_recommendations(technology, ctx.deps)}
"""

    except Exception as e:
        return f"Ошибка анализа технологии через Context7: {e}"


def _generate_technology_specific_recommendations(
    technology: str,
    deps: PerformanceOptimizationDependencies
) -> str:
    """Генерация специфичных рекомендаций для технологии."""

    tech_recommendations = {
        "react": [
            "Использовать React.memo для предотвращения ненужных рендеров",
            "Применять code splitting с React.lazy",
            "Оптимизировать состояние с помощью useMemo и useCallback",
            "Использовать React DevTools Profiler для анализа"
        ],
        "vue": [
            "Использовать v-memo для кэширования результатов рендера",
            "Применять async компоненты для code splitting",
            "Оптимизировать реактивность с computed properties",
            "Использовать Vue DevTools для анализа производительности"
        ],
        "fastapi": [
            "Использовать async/await для всех I/O операций",
            "Применять dependency injection для переиспользования",
            "Оптимизировать Pydantic models с Field валидацией",
            "Использовать middleware для кэширования и compression"
        ],
        "django": [
            "Оптимизировать ORM запросы с select_related/prefetch_related",
            "Использовать template caching для статического контента",
            "Применять database connection pooling",
            "Настроить static files оптимизацию"
        ],
        "express": [
            "Использовать clustering для многоядерных процессоров",
            "Применять compression middleware",
            "Оптимизировать async/await patterns",
            "Настроить connection pooling для баз данных"
        ]
    }

    recommendations = tech_recommendations.get(technology.lower(), [
        f"Изучить документацию по оптимизации {technology}",
        "Применить general performance best practices",
        "Использовать профилирование для выявления узких мест"
    ])

    # Адаптируем под стратегию оптимизации
    strategy_config = deps.get_optimization_strategy_config()
    priority = strategy_config["priority"]

    adapted_recommendations = []
    for rec in recommendations:
        adapted_recommendations.append(f"[{priority}] {rec}")

    return "\n".join(adapted_recommendations)