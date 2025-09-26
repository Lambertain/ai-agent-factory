#!/usr/bin/env python3
"""
MCP Configuration Agent - Универсальное управление MCP серверами

Универсальный агент для установки, настройки и управления MCP серверов
для различных проектов и технологических стеков.

Ключевые возможности:
- Установка MCP серверов через npm/pip/uv
- Автоматическая настройка Claude Desktop конфигурации
- Управление жизненным циклом серверов
- Поддержка различных транспортов (STDIO, HTTP)
- Валидация и тестирование серверов
- Универсальные конфигурации для разных доменов

Технологии: Python, subprocess, JSON, MCP Protocol
Интеграция: Claude Desktop, MCP Servers, Package Managers
"""

import asyncio
import json
import os
import subprocess
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from pydantic_ai import Agent, RunContext
from .dependencies import MCPConfigurationDeps
from .providers import get_llm_model
from .tools import (
    install_mcp_server,
    configure_claude_desktop,
    validate_server_config,
    get_recommended_servers_for_domain,
    create_server_from_template,
    break_down_to_microtasks,
    report_microtask_progress,
    reflect_and_improve,
    check_delegation_need,
    search_mcp_knowledge
)
from .prompts import get_mcp_system_prompt

# Импорт реальной конфигурации MCP серверов
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
from MCP_SERVERS_FINAL_CONFIG import WORKING_MCP_SERVERS, get_mcp_config_for_agent

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Pydantic AI агента (прямая архитектура)
mcp_agent = Agent(
    get_llm_model(),
    deps_type=MCPConfigurationDeps,
    system_prompt=get_mcp_system_prompt()
)

# Регистрируем MCP инструменты
mcp_agent.tool(install_mcp_server)
mcp_agent.tool(configure_claude_desktop)
mcp_agent.tool(validate_server_config)
mcp_agent.tool(get_recommended_servers_for_domain)
mcp_agent.tool(create_server_from_template)
mcp_agent.tool(search_mcp_knowledge)

# Регистрируем обязательные инструменты коллективной работы
mcp_agent.tool(break_down_to_microtasks)
mcp_agent.tool(report_microtask_progress)
mcp_agent.tool(reflect_and_improve)
mcp_agent.tool(check_delegation_need)


@dataclass
class MCPServerConfig:
    """Конфигурация MCP сервера."""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str] = None
    transport: str = "stdio"  # stdio или http
    description: str = ""
    install_command: Optional[str] = None
    package_manager: str = "npm"  # npm, pip, uv, git


async def run_mcp_configuration(
    task_description: str,
    domain: str = "general",
    project_type: str = "web",
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Выполнить задачу конфигурации MCP сервера.

    Args:
        task_description: Описание задачи конфигурации
        domain: Домен разработки (frontend, backend, fullstack, ai, security)
        project_type: Тип проекта (web, mobile, desktop, etc.)
        session_id: Идентификатор сессии

    Returns:
        Результаты конфигурации
    """
    start_time = asyncio.get_event_loop().time()

    # Инициализируем зависимости
    deps = MCPConfigurationDeps()
    deps.domain_type = domain
    deps.project_type = project_type

    try:
        # Запускаем задачу через прямую Pydantic AI архитектуру
        result = await mcp_agent.run(
            task_description,
            deps=deps
        )

        # Вычисляем время выполнения
        config_duration = asyncio.get_event_loop().time() - start_time

        # Обрабатываем и улучшаем результаты
        config_results = {
            "configuration_summary": {
                "task": task_description,
                "domain": domain,
                "project_type": project_type,
                "session_id": session_id,
                "start_time": start_time,
                "duration_seconds": config_duration,
                "status": "completed"
            },
            "agent_response": result.data,
            "recommendations": _extract_mcp_recommendations(result.data),
            "next_steps": _generate_mcp_next_steps(result.data)
        }

        logger.info(f"MCP конфигурация завершена за {config_duration:.2f} секунд")
        return config_results

    except Exception as e:
        logger.error(f"Ошибка выполнения MCP конфигурации: {e}")
        return {
            "error": str(e),
            "configuration_summary": {
                "task": task_description,
                "status": "failed"
            }
        }

def _extract_mcp_recommendations(response: str) -> List[str]:
    """Извлечь рекомендации из ответа агента."""
    recommendations = []
    lines = response.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith(('Рекомендация:', 'Recommendation:', '✅', '💡')):
            recommendations.append(line)

    return recommendations

def _generate_mcp_next_steps(response: str) -> List[str]:
    """Сгенерировать следующие шаги на основе ответа."""
    next_steps = []

    if "install" in response.lower():
        next_steps.append("Установка рекомендованных MCP серверов")
    if "configure" in response.lower():
        next_steps.append("Настройка Claude Desktop конфигурации")
    if "validate" in response.lower():
        next_steps.append("Валидация установленных серверов")
    if "test" in response.lower():
        next_steps.append("Тестирование MCP подключений")

    return next_steps

async def run_mcp_task(user_message: str, domain: str = "general") -> str:
    """
    Выполнить задачу MCP с автоматическими интеграциями.

    Args:
        user_message: Сообщение от пользователя
        domain: Домен разработки

    Returns:
        Ответ агента
    """
    # Инициализируем зависимости
    deps = MCPConfigurationDeps()
    deps.domain_type = domain

    try:
        # Используем новую систему интеграций
        from ..common.pydantic_ai_integrations import run_with_integrations

        result = await run_with_integrations(
            agent=mcp_agent,
            user_message=user_message,
            deps=deps,
            agent_type="mcp_configuration_agent"
        )
        return result

    except Exception as e:
        logger.error(f"Ошибка выполнения MCP задачи: {e}")
        return f"Произошла ошибка при обработке MCP запроса: {e}"

# Универсальные конфигурации для разных стеков (перенесены в модуль)
DOMAIN_CONFIGURATIONS = {
    "frontend": {
        "recommended": ["brave-search", "github", "filesystem"],
        "optional": ["figma", "linear", "slack"],
        "description": "Frontend разработка (React, Vue, Angular)"
    },
    "backend": {
        "recommended": ["postgres", "github", "filesystem"],
        "optional": ["docker", "kubernetes", "redis"],
        "description": "Backend разработка (API, микросервисы)"
    },
    "fullstack": {
        "recommended": ["postgres", "github", "filesystem", "brave-search"],
        "optional": ["docker", "slack", "linear"],
        "description": "Полнофункциональная разработка"
    },
    "ai": {
        "recommended": ["brave-search", "github", "filesystem"],
        "optional": ["postgres", "vector-db", "jupyter"],
        "description": "AI/ML разработка"
    },
    "security": {
        "recommended": ["github", "filesystem"],
        "optional": ["kubernetes", "docker", "slack"],
        "description": "Security аудит и тестирование"
    }
}

def _get_claude_config_path() -> Path:
    """Получить путь к конфигурации Claude Desktop."""
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "claude" / "claude_desktop_config.json"


# CLI интерфейс (опциональный)
async def main():
    """Основная функция для запуска агента из командной строки."""
    import argparse

    parser = argparse.ArgumentParser(description="Universal MCP Configuration Agent")
    parser.add_argument("--domain", default="general",
                       help="Домен разработки (frontend, backend, fullstack, ai, security)")
    parser.add_argument("--message", help="Сообщение для агента")
    parser.add_argument("--interactive", action="store_true",
                       help="Запустить в интерактивном режиме")

    args = parser.parse_args()

    print(f"🔧 MCP Configuration Agent запущен для домена: {args.domain}")
    print(f"📋 Доступные конфигурации: {', '.join(DOMAIN_CONFIGURATIONS.keys())}")
    print("-" * 50)

    if args.message:
        # Одноразовый режим
        response = await run_mcp_task(args.message, args.domain)
        print(f"Ответ: {response}")

    elif args.interactive:
        # Интерактивный режим
        print("Введите 'exit' для выхода")

        while True:
            try:
                user_input = input("\n👤 Вы: ")

                if user_input.lower() in ['exit', 'quit', 'выход']:
                    break

                if user_input.strip():
                    response = await run_mcp_task(user_input, args.domain)
                    print(f"🤖 Агент: {response}")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    else:
        # Показываем информацию о домене
        domain_info = DOMAIN_CONFIGURATIONS.get(args.domain, {})
        print("📋 Информация о домене:")
        print(f"  Описание: {domain_info.get('description', 'Общие настройки')}")
        print(f"  Рекомендованные серверы: {', '.join(domain_info.get('recommended', []))}")
        print(f"  Опциональные серверы: {', '.join(domain_info.get('optional', []))}")


if __name__ == "__main__":
    asyncio.run(main())