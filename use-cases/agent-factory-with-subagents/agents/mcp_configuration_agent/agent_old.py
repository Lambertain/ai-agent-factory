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
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Импорт реальной конфигурации MCP серверов
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
from MCP_SERVERS_FINAL_CONFIG import WORKING_MCP_SERVERS, get_mcp_config_for_agent

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

class MCPConfigurationAgent:
    """
    Универсальный MCP Configuration Agent

    Основные функции:
    - install_mcp_server() - установка MCP сервера
    - configure_claude_desktop() - настройка Claude Desktop
    - validate_server_config() - валидация конфигурации
    - manage_server_lifecycle() - управление жизненным циклом
    - get_recommended_servers() - рекомендации по стеку
    """

    def __init__(self, config_domain: str = "general", project_type: str = "web"):
        self.name = "MCP Configuration Agent"
        self.version = "2.0.0"
        self.config_domain = config_domain
        self.project_type = project_type

        # Путь к конфигурации Claude Desktop
        self.claude_config_path = self._get_claude_config_path()

        # Универсальные конфигурации для разных стеков
        self.domain_configurations = {
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

    def _get_claude_config_path(self) -> Path:
        """Получить путь к конфигурации Claude Desktop."""
        if sys.platform == "win32":
            return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        elif sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return Path.home() / ".config" / "claude" / "claude_desktop_config.json"

    async def install_mcp_server(self, server_name: str, install_method: str = "auto") -> Dict[str, Any]:
        """
        Установка MCP сервера через соответствующий пакетный менеджер.

        Args:
            server_name: Имя сервера для установки
            install_method: Метод установки (auto, npm, pip, uv, git)

        Returns:
            dict: Результат установки
        """
        print(f"🔧 {self.name}: Устанавливаю MCP сервер {server_name}")

        # Загружаем конфигурации доступных серверов
        available_servers = self._load_available_servers()

        if server_name not in available_servers:
            return {
                "success": False,
                "error": f"Сервер {server_name} не найден в доступных конфигурациях",
                "available": list(available_servers.keys())
            }

        server_config = available_servers[server_name]

        try:
            # Определяем метод установки
            if install_method == "auto":
                install_method = server_config.get("package_manager", "npm")

            # Выполняем установку
            install_command = server_config.get("install_command")
            if not install_command:
                # Генерируем команду установки по умолчанию
                package_name = server_config.get("package", server_name)
                if install_method == "npm":
                    install_command = f"npm install -g {package_name}"
                elif install_method == "pip":
                    install_command = f"pip install {package_name}"
                elif install_method == "uv":
                    install_command = f"uv add {package_name}"

            if install_command:
                result = await self._run_command(install_command)
                if result["success"]:
                    print(f"✅ {server_name} успешно установлен")
                    return {
                        "success": True,
                        "server_name": server_name,
                        "install_method": install_method,
                        "command": install_command
                    }
                else:
                    print(f"❌ Ошибка установки {server_name}: {result['error']}")
                    return {
                        "success": False,
                        "error": result["error"],
                        "command": install_command
                    }
            else:
                return {
                    "success": False,
                    "error": f"Не удалось определить команду установки для {server_name}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Исключение при установке {server_name}: {str(e)}"
            }

    async def configure_claude_desktop(self, servers_config: Dict[str, MCPServerConfig]) -> Dict[str, Any]:
        """
        Настройка Claude Desktop конфигурации с MCP серверами.

        Args:
            servers_config: Словарь конфигураций серверов

        Returns:
            dict: Результат конфигурации
        """
        print(f"⚙️ {self.name}: Настраиваю Claude Desktop конфигурацию")

        try:
            # Загружаем существующую конфигурацию или создаем новую
            if self.claude_config_path.exists():
                with open(self.claude_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}

            # Убеждаемся что секция mcpServers существует
            if "mcpServers" not in config:
                config["mcpServers"] = {}

            # Добавляем новые серверы
            for server_name, server_config in servers_config.items():
                mcp_config = {
                    "command": server_config.command,
                    "args": server_config.args
                }

                if server_config.env:
                    mcp_config["env"] = server_config.env

                config["mcpServers"][server_name] = mcp_config
                print(f"✅ Добавлен сервер: {server_name}")

            # Сохраняем конфигурацию
            self.claude_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.claude_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"💾 Конфигурация сохранена: {self.claude_config_path}")

            return {
                "success": True,
                "config_path": str(self.claude_config_path),
                "servers_added": list(servers_config.keys()),
                "total_servers": len(config["mcpServers"])
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка конфигурации Claude Desktop: {str(e)}"
            }

    async def validate_server_config(self, server_config: MCPServerConfig) -> Dict[str, Any]:
        """
        Валидация конфигурации MCP сервера.

        Args:
            server_config: Конфигурация сервера для проверки

        Returns:
            dict: Результат валидации
        """
        print(f"🔍 Валидация конфигурации сервера: {server_config.name}")

        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # Проверка обязательных полей
        if not server_config.name:
            validation_results["errors"].append("Отсутствует имя сервера")
            validation_results["valid"] = False

        if not server_config.command:
            validation_results["errors"].append("Отсутствует команда запуска")
            validation_results["valid"] = False

        # Проверка команды на существование
        try:
            result = await self._run_command(f"which {server_config.command}")
            if not result["success"]:
                validation_results["warnings"].append(f"Команда {server_config.command} не найдена в PATH")
        except Exception:
            validation_results["warnings"].append(f"Не удалось проверить команду {server_config.command}")

        # Проверка аргументов
        if server_config.args:
            for arg in server_config.args:
                if not isinstance(arg, str):
                    validation_results["errors"].append(f"Аргумент должен быть строкой: {arg}")
                    validation_results["valid"] = False

        # Проверка переменных окружения
        if server_config.env:
            for key, value in server_config.env.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    validation_results["errors"].append(f"Переменная окружения должна быть строкой: {key}={value}")
                    validation_results["valid"] = False

        return validation_results

    def get_recommended_servers_for_domain(self, domain: str) -> Dict[str, Any]:
        """
        Получение рекомендованных серверов для домена.

        Args:
            domain: Домен разработки (frontend, backend, fullstack, ai, security)

        Returns:
            dict: Список рекомендованных серверов
        """
        if domain not in self.domain_configurations:
            return {
                "error": f"Неподдерживаемый домен: {domain}",
                "available_domains": list(self.domain_configurations.keys())
            }

        config = self.domain_configurations[domain]
        return {
            "domain": domain,
            "description": config["description"],
            "recommended": config["recommended"],
            "optional": config["optional"]
        }

    def _load_available_servers(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка доступных MCP серверов из реальной конфигурации."""
        try:
            # Используем реальную конфигурацию рабочих MCP серверов
            servers_config = {}

            for server_name, server_status in WORKING_MCP_SERVERS.items():
                if server_status.status == "connected":
                    # Конвертируем в формат для установки
                    command_parts = server_status.command.split()
                    if command_parts[0] == "npx":
                        package = command_parts[-1] if len(command_parts) > 1 else server_name
                        servers_config[server_name] = {
                            "package": package,
                            "command": command_parts[0],
                            "args": command_parts[1:],
                            "package_manager": "npm",
                            "description": server_status.description,
                            "status": "working",
                            "functions_count": len(server_status.functions)
                        }
                    elif server_status.command.startswith("http://"):
                        # HTTP сервер (Archon)
                        servers_config[server_name] = {
                            "type": "http",
                            "url": server_status.command,
                            "description": server_status.description,
                            "status": "working",
                            "functions_count": len(server_status.functions)
                        }

            print(f"✅ Загружено {len(servers_config)} рабочих MCP серверов")
            return servers_config

        except Exception as e:
            print(f"⚠️ Ошибка загрузки реальной конфигурации: {e}")
            return self._get_default_servers()

    def _get_default_servers(self) -> Dict[str, Dict[str, Any]]:
        """Базовые MCP серверы из официальной документации."""
        return {
            "filesystem": {
                "package": "@modelcontextprotocol/server-filesystem",
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"],
                "package_manager": "npm",
                "description": "Доступ к файловой системе"
            },
            "brave-search": {
                "package": "@modelcontextprotocol/server-brave-search",
                "command": "npx",
                "args": ["@modelcontextprotocol/server-brave-search"],
                "package_manager": "npm",
                "description": "Поиск в интернете через Brave Search",
                "env_required": ["BRAVE_API_KEY"]
            },
            "postgres": {
                "package": "@modelcontextprotocol/server-postgres",
                "command": "npx",
                "args": ["@modelcontextprotocol/server-postgres"],
                "package_manager": "npm",
                "description": "Подключение к PostgreSQL базе данных",
                "env_required": ["POSTGRES_CONNECTION_STRING"]
            },
            "github": {
                "package": "@modelcontextprotocol/server-github",
                "command": "npx",
                "args": ["@modelcontextprotocol/server-github"],
                "package_manager": "npm",
                "description": "Интеграция с GitHub API",
                "env_required": ["GITHUB_PERSONAL_ACCESS_TOKEN"]
            }
        }

    async def _run_command(self, command: str) -> Dict[str, Any]:
        """Выполнение команды в subprocess."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            return {
                "success": process.returncode == 0,
                "stdout": stdout.decode('utf-8', errors='ignore').strip(),
                "stderr": stderr.decode('utf-8', errors='ignore').strip(),
                "returncode": process.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "returncode": -1
            }

    async def create_server_from_template(self, server_name: str, template_type: str = "python") -> Dict[str, Any]:
        """
        Создание нового MCP сервера из шаблона.

        Args:
            server_name: Имя нового сервера
            template_type: Тип шаблона (python, typescript, etc.)

        Returns:
            dict: Результат создания
        """
        print(f"🛠️ Создание MCP сервера {server_name} из шаблона {template_type}")

        try:
            if template_type == "python":
                # Используем официальный Python шаблон
                command = f"npx @modelcontextprotocol/create-server {server_name} --template python"
            elif template_type == "typescript":
                command = f"npx @modelcontextprotocol/create-server {server_name} --template typescript"
            else:
                return {
                    "success": False,
                    "error": f"Неподдерживаемый тип шаблона: {template_type}"
                }

            result = await self._run_command(command)

            if result["success"]:
                print(f"✅ Сервер {server_name} создан успешно")
                return {
                    "success": True,
                    "server_name": server_name,
                    "template_type": template_type,
                    "path": f"./{server_name}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Ошибка создания сервера: {result['stderr']}",
                    "command": command
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Исключение при создании сервера: {str(e)}"
            }

# Пример использования
async def main():
    """Демонстрация работы MCP Configuration Agent"""
    agent = MCPConfigurationAgent(config_domain="fullstack", project_type="web")

    print("🚀 MCP Configuration Agent - Демонстрация возможностей\n")

    # 1. Получить рекомендации для fullstack разработки
    print("1. Рекомендации для fullstack разработки:")
    recommendations = agent.get_recommended_servers_for_domain("fullstack")
    print(f"Рекомендованные серверы: {recommendations['recommended']}")

    # 2. Установить рекомендованный сервер
    print("\n2. Установка рекомендованного сервера:")
    install_result = await agent.install_mcp_server("brave-search")
    print(f"Результат установки: {install_result}")

    # 3. Валидация конфигурации
    print("\n3. Валидация конфигурации сервера:")
    test_config = MCPServerConfig(
        name="test-server",
        command="npx",
        args=["@modelcontextprotocol/server-filesystem", "/tmp"],
        description="Тестовый сервер"
    )
    validation = await agent.validate_server_config(test_config)
    print(f"Валидация: {validation}")

if __name__ == "__main__":
    asyncio.run(main())