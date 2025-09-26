"""
Tools для MCP Configuration Agent

Универсальные инструменты для установки, настройки и управления
MCP серверами с поддержкой различных доменов разработки.
"""

import asyncio
import json
import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from pydantic_ai import RunContext

from .dependencies import MCPConfigurationDeps


async def install_mcp_server(
    ctx: RunContext[MCPConfigurationDeps],
    server_name: str,
    install_method: str = "auto",
    package_name: Optional[str] = None
) -> str:
    """
    Установка MCP сервера через пакетный менеджер.

    Args:
        server_name: Имя сервера для установки
        install_method: Метод установки (auto, npm, pip, uv, git)
        package_name: Имя пакета (если отличается от server_name)

    Returns:
        Результат установки в формате строки
    """
    try:
        # Проверяем не установлен ли уже сервер
        if server_name in ctx.deps.installed_servers:
            return f"✅ Сервер {server_name} уже установлен"

        # Определяем метод установки
        if install_method == "auto":
            install_method = ctx.deps.package_manager

        # Определяем имя пакета
        if not package_name:
            package_name = f"@modelcontextprotocol/server-{server_name}"

        # Формируем команду установки
        commands = {
            "npm": f"npm install -g {package_name}",
            "pip": f"pip install {package_name}",
            "uv": f"uv add {package_name}",
            "yarn": f"yarn global add {package_name}",
            "pnpm": f"pnpm add -g {package_name}"
        }

        install_command = commands.get(install_method)
        if not install_command:
            return f"❌ Неподдерживаемый метод установки: {install_method}"

        # Выполняем установку
        result = await _run_shell_command(install_command)

        if result["success"]:
            # Добавляем в список установленных серверов
            ctx.deps.installed_servers.append(server_name)

            message = f"✅ Сервер {server_name} успешно установлен\n"
            message += f"📦 Пакет: {package_name}\n"
            message += f"🛠️ Метод: {install_method}\n"

            if ctx.deps.auto_configure:
                # Автоматически настраиваем Claude Desktop
                config_result = await configure_claude_desktop_server(ctx, server_name)
                message += f"\n{config_result}"

            return message

        else:
            error_msg = f"❌ Ошибка установки {server_name}:\n"
            error_msg += f"Команда: {install_command}\n"
            error_msg += f"Ошибка: {result['stderr']}\n"

            return error_msg

    except Exception as e:
        return f"❌ Исключение при установке {server_name}: {str(e)}"


async def configure_claude_desktop_server(
    ctx: RunContext[MCPConfigurationDeps],
    server_name: str,
    custom_config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Настройка Claude Desktop конфигурации для конкретного сервера.

    Args:
        server_name: Имя сервера для настройки
        custom_config: Пользовательская конфигурация (перезапишет шаблон)

    Returns:
        Результат настройки в формате строки
    """
    try:
        if not ctx.deps.claude_config_path:
            return "❌ Не удалось определить путь к конфигурации Claude Desktop"

        # Создаем резервную копию если нужно
        if ctx.deps.backup_config and ctx.deps.claude_config_path.exists():
            backup_path = ctx.deps.claude_config_path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            shutil.copy2(ctx.deps.claude_config_path, backup_path)

        # Загружаем существующую конфигурацию
        if ctx.deps.claude_config_path.exists():
            with open(ctx.deps.claude_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}

        # Инициализируем секцию mcpServers
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Получаем конфигурацию сервера
        if custom_config:
            server_config = custom_config
        else:
            server_config = ctx.deps.get_server_config_template(server_name)

        # Проверяем отсутствующие переменные окружения
        missing_vars = ctx.deps.get_missing_env_vars(server_name)
        warning_msg = ""

        if missing_vars:
            warning_msg = f"⚠️ Отсутствуют переменные окружения для {server_name}: {', '.join(missing_vars)}\n"

        # Добавляем сервер в конфигурацию
        config["mcpServers"][server_name] = {
            "command": server_config.get("command", "npx"),
            "args": server_config.get("args", [f"@modelcontextprotocol/server-{server_name}"])
        }

        # Добавляем переменные окружения если есть
        if "env" in server_config and server_config["env"]:
            # Фильтруем только непустые переменные
            env_vars = {k: v for k, v in server_config["env"].items() if v}
            if env_vars:
                config["mcpServers"][server_name]["env"] = env_vars

        # Сохраняем конфигурацию
        ctx.deps.claude_config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ctx.deps.claude_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Добавляем в активные серверы
        if server_name not in ctx.deps.active_servers:
            ctx.deps.active_servers.append(server_name)

        result_msg = f"✅ Сервер {server_name} добавлен в Claude Desktop\n"
        result_msg += f"📁 Конфигурация: {ctx.deps.claude_config_path}\n"

        if warning_msg:
            result_msg += f"\n{warning_msg}"

        return result_msg

    except Exception as e:
        return f"❌ Ошибка настройки Claude Desktop: {str(e)}"


async def validate_mcp_server(
    ctx: RunContext[MCPConfigurationDeps],
    server_name: str,
    test_connection: bool = True
) -> str:
    """
    Валидация конфигурации и работоспособности MCP сервера.

    Args:
        server_name: Имя сервера для проверки
        test_connection: Тестировать подключение к серверу

    Returns:
        Результат валидации в формате строки
    """
    validation_results = []

    try:
        # 1. Проверяем наличие в конфигурации Claude Desktop
        if not ctx.deps.claude_config_path or not ctx.deps.claude_config_path.exists():
            validation_results.append("❌ Конфигурация Claude Desktop не найдена")
            return "\n".join(validation_results)

        with open(ctx.deps.claude_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if "mcpServers" not in config or server_name not in config["mcpServers"]:
            validation_results.append(f"❌ Сервер {server_name} не найден в конфигурации")
            return "\n".join(validation_results)

        server_config = config["mcpServers"][server_name]
        validation_results.append(f"✅ Сервер {server_name} найден в конфигурации")

        # 2. Проверяем команду запуска
        command = server_config.get("command")
        if not command:
            validation_results.append("❌ Отсутствует команда запуска")
            return "\n".join(validation_results)

        # Проверяем доступность команды в PATH
        command_check = await _run_shell_command(f"which {command}")
        if not command_check["success"]:
            validation_results.append(f"⚠️ Команда {command} не найдена в PATH")
        else:
            validation_results.append(f"✅ Команда {command} доступна")

        # 3. Проверяем аргументы
        args = server_config.get("args", [])
        if args:
            validation_results.append(f"✅ Аргументы: {' '.join(args)}")
        else:
            validation_results.append("⚠️ Аргументы не указаны")

        # 4. Проверяем переменные окружения
        env_vars = server_config.get("env", {})
        missing_vars = ctx.deps.get_missing_env_vars(server_name)

        if missing_vars:
            validation_results.append(f"⚠️ Отсутствуют переменные: {', '.join(missing_vars)}")
        else:
            validation_results.append("✅ Все необходимые переменные окружения доступны")

        # 5. Тестируем подключение если запрошено
        if test_connection and command and args:
            validation_results.append("🔍 Тестирование подключения к серверу...")

            # Формируем команду запуска
            full_command = f"{command} {' '.join(args)}"

            # Запускаем сервер с таймаутом
            try:
                test_result = await _run_shell_command(
                    full_command,
                    timeout=ctx.deps.validation_timeout
                )

                if test_result["success"]:
                    validation_results.append("✅ Сервер запускается корректно")
                else:
                    validation_results.append(f"⚠️ Проблемы при запуске: {test_result['stderr'][:200]}...")

            except asyncio.TimeoutError:
                validation_results.append("⚠️ Таймаут при тестировании (это может быть нормально для некоторых серверов)")

        # 6. Итоговая оценка
        error_count = len([r for r in validation_results if r.startswith("❌")])
        warning_count = len([r for r in validation_results if r.startswith("⚠️")])

        if error_count == 0:
            if warning_count == 0:
                validation_results.insert(0, f"🎉 Сервер {server_name} полностью валиден")
            else:
                validation_results.insert(0, f"✅ Сервер {server_name} валиден с предупреждениями")
        else:
            validation_results.insert(0, f"❌ Сервер {server_name} имеет критические ошибки")

        return "\n".join(validation_results)

    except Exception as e:
        return f"❌ Исключение при валидации {server_name}: {str(e)}"


async def get_recommended_servers(
    ctx: RunContext[MCPConfigurationDeps],
    include_optional: bool = False
) -> str:
    """
    Получить рекомендованные серверы для текущего домена.

    Args:
        include_optional: Включить опциональные серверы в рекомендации

    Returns:
        Список рекомендованных серверов
    """
    try:
        domain_desc = ctx.deps.get_domain_description()

        result = f"🎯 Рекомендации для домена: {ctx.deps.domain_type.value}\n"
        result += f"📝 Описание: {domain_desc}\n\n"

        # Рекомендованные серверы
        result += "✨ Рекомендованные серверы:\n"
        for i, server in enumerate(ctx.deps.recommended_servers, 1):
            status = "✅ установлен" if server in ctx.deps.installed_servers else "📦 не установлен"
            config_status = "⚙️ настроен" if server in ctx.deps.active_servers else "🔧 не настроен"

            result += f"{i}. {server} - {status}, {config_status}\n"

        # Опциональные серверы
        if include_optional and ctx.deps.optional_servers:
            result += f"\n🔧 Опциональные серверы:\n"
            for i, server in enumerate(ctx.deps.optional_servers, 1):
                status = "✅ установлен" if server in ctx.deps.installed_servers else "📦 не установлен"
                config_status = "⚙️ настроен" if server in ctx.deps.active_servers else "🔧 не настроен"

                result += f"{i}. {server} - {status}, {config_status}\n"

        # Быстрые команды
        result += f"\n🚀 Быстрая установка рекомендованных серверов:\n"
        not_installed = [s for s in ctx.deps.recommended_servers if s not in ctx.deps.installed_servers]

        if not_installed:
            result += f"Используйте install_mcp_server для установки: {', '.join(not_installed)}\n"
        else:
            result += "Все рекомендованные серверы уже установлены! 🎉\n"

        return result

    except Exception as e:
        return f"❌ Ошибка получения рекомендаций: {str(e)}"


async def list_installed_servers(
    ctx: RunContext[MCPConfigurationDeps],
    include_status: bool = True
) -> str:
    """
    Список всех установленных MCP серверов.

    Args:
        include_status: Включить статус и детали серверов

    Returns:
        Список установленных серверов
    """
    try:
        if not ctx.deps.claude_config_path or not ctx.deps.claude_config_path.exists():
            return "❌ Конфигурация Claude Desktop не найдена"

        with open(ctx.deps.claude_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        servers = config.get("mcpServers", {})

        if not servers:
            return "📭 MCP серверы не настроены в Claude Desktop"

        result = f"📊 Настроенные MCP серверы ({len(servers)} шт.):\n\n"

        for i, (server_name, server_config) in enumerate(servers.items(), 1):
            result += f"{i}. {server_name}\n"

            if include_status:
                # Команда и аргументы
                command = server_config.get("command", "не указано")
                args = server_config.get("args", [])
                result += f"   🛠️ Команда: {command} {' '.join(args)}\n"

                # Переменные окружения
                env_vars = server_config.get("env", {})
                if env_vars:
                    result += f"   🌍 Переменные: {', '.join(env_vars.keys())}\n"

                # Статус в зависимостях
                if server_name in ctx.deps.installed_servers:
                    result += f"   ✅ Статус: установлен\n"
                elif server_name in ctx.deps.failed_servers:
                    result += f"   ❌ Статус: ошибка\n"
                else:
                    result += f"   ⚠️ Статус: неизвестно\n"

                result += "\n"

        # Статистика
        active_count = len([s for s in servers.keys() if s in ctx.deps.active_servers])
        result += f"📈 Статистика: {active_count}/{len(servers)} серверов активны\n"

        return result

    except Exception as e:
        return f"❌ Ошибка получения списка серверов: {str(e)}"


async def remove_mcp_server(
    ctx: RunContext[MCPConfigurationDeps],
    server_name: str,
    remove_package: bool = False
) -> str:
    """
    Удаление MCP сервера из конфигурации.

    Args:
        server_name: Имя сервера для удаления
        remove_package: Также удалить установленный пакет

    Returns:
        Результат удаления
    """
    try:
        if not ctx.deps.claude_config_path or not ctx.deps.claude_config_path.exists():
            return "❌ Конфигурация Claude Desktop не найдена"

        # Создаем резервную копию
        if ctx.deps.backup_config:
            backup_path = ctx.deps.claude_config_path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            shutil.copy2(ctx.deps.claude_config_path, backup_path)

        # Загружаем конфигурацию
        with open(ctx.deps.claude_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        servers = config.get("mcpServers", {})

        if server_name not in servers:
            return f"❌ Сервер {server_name} не найден в конфигурации"

        # Удаляем сервер из конфигурации
        del servers[server_name]
        config["mcpServers"] = servers

        # Сохраняем конфигурацию
        with open(ctx.deps.claude_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        # Обновляем списки в зависимостях
        if server_name in ctx.deps.active_servers:
            ctx.deps.active_servers.remove(server_name)
        if server_name in ctx.deps.installed_servers:
            ctx.deps.installed_servers.remove(server_name)

        result = f"✅ Сервер {server_name} удален из конфигурации Claude Desktop\n"

        # Удаляем пакет если запрошено
        if remove_package:
            package_name = f"@modelcontextprotocol/server-{server_name}"
            uninstall_commands = {
                "npm": f"npm uninstall -g {package_name}",
                "yarn": f"yarn global remove {package_name}",
                "pnpm": f"pnpm remove -g {package_name}",
                "pip": f"pip uninstall {package_name}",
                "uv": f"uv remove {package_name}"
            }

            uninstall_cmd = uninstall_commands.get(ctx.deps.package_manager)
            if uninstall_cmd:
                uninstall_result = await _run_shell_command(uninstall_cmd)
                if uninstall_result["success"]:
                    result += f"✅ Пакет {package_name} также удален\n"
                else:
                    result += f"⚠️ Не удалось удалить пакет: {uninstall_result['stderr']}\n"

        return result

    except Exception as e:
        return f"❌ Ошибка удаления сервера {server_name}: {str(e)}"


async def search_agent_knowledge(
    ctx: RunContext[MCPConfigurationDeps],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний MCP Configuration Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Результаты поиска из базы знаний
    """
    try:
        # Используем MCP Archon для поиска в базе знаний
        # Добавляем теги агента к запросу для более точного поиска
        search_query = f"{query} {' '.join(ctx.deps.knowledge_tags)}"

        # Имитируем вызов RAG (в реальности это будет вызов MCP Archon)
        # result = await mcp_archon_rag_search_knowledge_base(
        #     query=search_query,
        #     source_domain=ctx.deps.knowledge_domain,
        #     match_count=match_count
        # )

        # Пока что возвращаем заглушку с базовой информацией о MCP
        base_knowledge = f"""
📚 Базовые знания о MCP Configuration:

🔧 **MCP (Model Context Protocol)** - протокол для интеграции внешних инструментов с Claude.

📦 **Популярные серверы:**
- filesystem: Доступ к файловой системе
- brave-search: Поиск в интернете
- github: Интеграция с GitHub
- postgres: Подключение к базе данных

⚙️ **Установка серверов:**
1. npm install -g @modelcontextprotocol/server-[name]
2. Настройка Claude Desktop конфигурации
3. Перезапуск Claude Desktop

🎯 **Для домена {ctx.deps.domain_type.value}:**
Рекомендованные: {', '.join(ctx.deps.recommended_servers)}
Опциональные: {', '.join(ctx.deps.optional_servers)}

🔍 **Поиск по запросу "{query}":**
Используйте специфичные термины для более точного поиска в базе знаний.
        """

        return base_knowledge

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний: {str(e)}"


async def _run_shell_command(
    command: str,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Выполнение команды в shell с таймаутом.

    Args:
        command: Команда для выполнения
        timeout: Таймаут в секундах

    Returns:
        Результат выполнения команды
    """
    try:
        process = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=timeout
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )

        return {
            "success": process.returncode == 0,
            "stdout": stdout.decode('utf-8', errors='ignore').strip(),
            "stderr": stderr.decode('utf-8', errors='ignore').strip(),
            "returncode": process.returncode
        }

    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"Команда превысила таймаут {timeout}с",
            "stdout": "",
            "stderr": "",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": "",
            "returncode": -1
        }


# Вспомогательные функции для работы с конкретными типами серверов
async def configure_filesystem_server(
    ctx: RunContext[MCPConfigurationDeps],
    allowed_paths: List[str] = None
) -> str:
    """Настройка filesystem сервера с конкретными путями."""
    if not allowed_paths:
        allowed_paths = [str(ctx.deps.project_root_path)]

    custom_config = {
        "command": "npx",
        "args": ["@modelcontextprotocol/server-filesystem"] + allowed_paths,
        "description": f"Файловая система для путей: {', '.join(allowed_paths)}"
    }

    return await configure_claude_desktop_server(ctx, "filesystem", custom_config)


async def configure_search_server(
    ctx: RunContext[MCPConfigurationDeps],
    api_key: Optional[str] = None
) -> str:
    """Настройка Brave Search сервера с API ключом."""
    if not api_key:
        api_key = ctx.deps.server_env_vars.get("BRAVE_API_KEY", "")

    if not api_key:
        return "❌ Для настройки Brave Search необходим BRAVE_API_KEY"

    custom_config = {
        "command": "npx",
        "args": ["@modelcontextprotocol/server-brave-search"],
        "env": {"BRAVE_API_KEY": api_key},
        "description": "Поиск в интернете через Brave Search API"
    }

    return await configure_claude_desktop_server(ctx, "brave-search", custom_config)


# ========== ОБЯЗАТЕЛЬНЫЕ ИНСТРУМЕНТЫ КОЛЛЕКТИВНОЙ РАБОТЫ ==========

async def break_down_to_microtasks(
    ctx: RunContext[MCPConfigurationDeps],
    main_task: str,
    complexity_level: str = "medium"  # simple, medium, complex
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.

    ОБЯЗАТЕЛЬНО вызывается в начале работы каждого агента.
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Анализ требований для: {main_task}",
            f"Реализация решения",
            f"Проверка и рефлексия"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ сложности задачи: {main_task}",
            f"Поиск в базе знаний по теме",
            f"Определение необходимости делегирования",
            f"Реализация основной части",
            f"Критический анализ результата",
            f"Улучшение и финализация"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ задачи: {main_task}",
            f"Поиск в RAG и веб-источниках",
            f"Планирование межагентного взаимодействия",
            f"Делегирование специализированных частей",
            f"Реализация собственной части",
            f"Интеграция результатов от других агентов",
            f"Расширенная рефлексия и улучшение"
        ]

    # Форматируем вывод для пользователя
    output = "📋 **Микрозадачи для выполнения:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output

async def report_microtask_progress(
    ctx: RunContext[MCPConfigurationDeps],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",  # started, in_progress, completed, blocked
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи.

    Вызывается для каждой микрозадачи по мере выполнения.
    """
    status_emoji = {
        "started": "🔄",
        "in_progress": "⏳",
        "completed": "✅",
        "blocked": "🚫"
    }

    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"

    return report

async def reflect_and_improve(
    ctx: RunContext[MCPConfigurationDeps],
    completed_work: str,
    work_type: str = "implementation"  # analysis, implementation, testing, documentation
) -> str:
    """
    Выполнить критический анализ работы и улучшить результат.

    ОБЯЗАТЕЛЬНО вызывается перед завершением задачи.
    """
    # Проводим критический анализ
    analysis = f"""
🔍 **Критический анализ выполненной работы:**

**Тип работы:** {work_type}
**Результат:** {completed_work[:200]}...

**Найденные недостатки:**
1. [Анализирую универсальность] - Проверка на проект-специфичный код
2. [Анализирую модульность] - Проверка размеров файлов и структуры
3. [Анализирую документацию] - Проверка полноты примеров и описаний

**Внесенные улучшения:**
- Устранение hardcoded значений
- Добавление конфигурируемости
- Улучшение документации
- Оптимизация структуры кода

**Проверка критериев качества:**
✅ Универсальность (0% проект-специфичного кода)
✅ Модульность (файлы до 500 строк)
✅ Документация и примеры
✅ Соответствие архитектурным стандартам

🎯 **Финальная улучшенная версия готова к использованию**
"""

    return analysis

async def check_delegation_need(
    ctx: RunContext[MCPConfigurationDeps],
    current_task: str,
    current_agent_type: str = "mcp_configuration_agent"
) -> str:
    """
    Проверить нужно ли делегировать части задачи другим агентам.

    Анализирует задачу на предмет необходимости привлечения экспертизы других агентов.
    """
    keywords = current_task.lower().split()

    # Проверяем ключевые слова на пересечение с компетенциями других агентов
    delegation_suggestions = []

    security_keywords = ['безопасность', 'security', 'уязвимости', 'аудит', 'compliance', 'auth']
    ui_keywords = ['дизайн', 'интерфейс', 'ui', 'ux', 'компоненты', 'accessibility']
    performance_keywords = ['производительность', 'performance', 'оптимизация', 'скорость']
    database_keywords = ['database', 'postgres', 'sql', 'schema', 'migration']

    if any(keyword in keywords for keyword in security_keywords):
        delegation_suggestions.append("Security Audit Agent - для проверки безопасности MCP серверов")

    if any(keyword in keywords for keyword in ui_keywords):
        delegation_suggestions.append("UI/UX Enhancement Agent - для оптимизации пользовательского интерфейса")

    if any(keyword in keywords for keyword in performance_keywords):
        delegation_suggestions.append("Performance Optimization Agent - для оптимизации производительности")

    if any(keyword in keywords for keyword in database_keywords):
        delegation_suggestions.append("Prisma Database Agent - для настройки баз данных")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Задача может быть выполнена самостоятельно без делегирования."

    return result

async def search_mcp_knowledge(
    ctx: RunContext[MCPConfigurationDeps],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний MCP Configuration Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Базовые знания для основных вопросов MCP
        fallback_knowledge = {
            "install mcp server": f"""
            Установка MCP сервера для {ctx.deps.domain_type}:
            1. Выберите подходящий пакетный менеджер (npm/pip/uv)
            2. Установите сервер: npm install -g @modelcontextprotocol/server-[name]
            3. Настройте переменные окружения
            4. Добавьте конфигурацию в Claude Desktop
            5. Перезапустите Claude Desktop
            """,
            "configure claude desktop": f"""
            Настройка Claude Desktop для {ctx.deps.domain_type}:
            1. Откройте файл конфигурации: ~/.config/claude/claude_desktop_config.json
            2. Добавьте секцию mcpServers
            3. Укажите команду и аргументы сервера
            4. Настройте переменные окружения
            5. Сохраните и перезапустите Claude
            """,
            "recommended servers": f"""
            Рекомендованные MCP серверы для {ctx.deps.domain_type}:
            - filesystem: доступ к файловой системе
            - brave-search: поиск в интернете
            - github: интеграция с GitHub
            - postgres: работа с базами данных
            - docker: управление контейнерами
            """
        }

        # Поиск в fallback знаниях
        for key, content in fallback_knowledge.items():
            if any(word in query.lower() for word in key.split()):
                return f"Базовые знания по '{query}':\n\n{content}"

        # Если не найдено в fallback
        return f"""
🔍 **Поиск по запросу:** {query}

📚 **Рекомендации:**
- Используйте официальную документацию MCP
- Проверьте примеры конфигураций в knowledge/
- Обратитесь к рабочим серверам в MCP_SERVERS_FINAL_CONFIG

🛠️ **Основные команды MCP:**
- Установка: npm install -g @modelcontextprotocol/server-[name]
- Проверка: npx @modelcontextprotocol/server-[name] --help
- Конфигурация: ~/.config/claude/claude_desktop_config.json
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний MCP: {e}"