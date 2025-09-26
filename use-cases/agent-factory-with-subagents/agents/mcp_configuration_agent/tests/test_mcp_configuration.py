"""
Тесты для MCP Configuration Agent

Набор unit и integration тестов для проверки функциональности агента
"""

import pytest
import json
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

# Импорты из агента (предполагаемые)
try:
    from ..agent import MCPConfigurationAgent
    from ..dependencies import MCPDependencies
    from ..settings import MCPSettings
    from ..tools import MCPTools
except ImportError:
    # Fallback для запуска тестов отдельно
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from agent import MCPConfigurationAgent
    from dependencies import MCPDependencies
    from settings import MCPSettings
    from tools import MCPTools


class TestMCPConfigurationAgent:
    """Тесты основного функционала MCP Configuration Agent"""

    @pytest.fixture
    def agent(self):
        """Создание экземпляра агента для тестов"""
        return MCPConfigurationAgent()

    @pytest.fixture
    def mock_project_config(self):
        """Мок конфигурации проекта"""
        return {
            "project_type": "frontend",
            "framework": "react",
            "ui_library": "shadcn",
            "testing_framework": "jest"
        }

    def test_agent_initialization(self, agent):
        """Тест инициализации агента"""
        assert agent is not None
        assert hasattr(agent, 'settings')
        assert hasattr(agent, 'dependencies')
        assert hasattr(agent, 'tools')

    def test_frontend_config_generation(self, agent, mock_project_config):
        """Тест генерации конфигурации для фронтенд проекта"""
        config = agent.generate_config(**mock_project_config)

        assert config is not None
        assert "mcpServers" in config
        assert "github" in config["mcpServers"]
        assert "shadcn" in config["mcpServers"]
        assert "puppeteer" in config["mcpServers"]

    def test_backend_config_generation(self, agent):
        """Тест генерации конфигурации для бэкенд проекта"""
        backend_config = {
            "project_type": "backend",
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql"
        }

        config = agent.generate_config(**backend_config)

        assert config is not None
        assert "mcpServers" in config
        assert "github" in config["mcpServers"]
        assert "postgresql" in config["mcpServers"]
        assert "security" in config["mcpServers"]

    def test_fullstack_config_generation(self, agent):
        """Тест генерации конфигурации для fullstack проекта"""
        fullstack_config = {
            "project_type": "fullstack",
            "frontend_framework": "react",
            "backend_language": "python",
            "backend_framework": "fastapi",
            "database": "postgresql"
        }

        config = agent.generate_config(**fullstack_config)

        assert config is not None
        assert "mcpServers" in config
        assert "github" in config["mcpServers"]
        assert "shadcn" in config["mcpServers"]
        assert "postgresql" in config["mcpServers"]
        assert "context7" in config["mcpServers"]

    def test_invalid_project_type(self, agent):
        """Тест обработки некорректного типа проекта"""
        with pytest.raises(ValueError):
            agent.generate_config(project_type="invalid_type")

    def test_config_validation(self, agent):
        """Тест валидации сгенерированной конфигурации"""
        config = agent.generate_config(
            project_type="frontend",
            framework="react"
        )

        # Проверяем структуру конфигурации
        assert isinstance(config, dict)
        assert "mcpServers" in config
        assert isinstance(config["mcpServers"], dict)

        # Проверяем обязательные серверы
        required_servers = ["github", "filesystem", "fetch"]
        for server in required_servers:
            assert server in config["mcpServers"]

    @pytest.mark.asyncio
    async def test_async_config_generation(self, agent):
        """Тест асинхронной генерации конфигурации"""
        config = await agent.generate_config_async(
            project_type="backend",
            language="python",
            framework="django"
        )

        assert config is not None
        assert "mcpServers" in config


class TestMCPDependencies:
    """Тесты управления зависимостями MCP серверов"""

    @pytest.fixture
    def dependencies(self):
        """Создание экземпляра dependencies для тестов"""
        return MCPDependencies()

    def test_check_server_availability(self, dependencies):
        """Тест проверки доступности MCP серверов"""
        # Мокируем существующий сервер
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0

            result = dependencies.check_server_availability("uvx")
            assert result is True

    def test_install_missing_dependencies(self, dependencies):
        """Тест установки недостающих зависимостей"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0

            result = dependencies.install_dependencies(["uvx"])
            assert result is True

    def test_validate_environment(self, dependencies):
        """Тест валидации окружения"""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
            result = dependencies.validate_environment(['GITHUB_TOKEN'])
            assert result is True


class TestMCPTools:
    """Тесты инструментов MCP Configuration Agent"""

    @pytest.fixture
    def tools(self):
        """Создание экземпляра tools для тестов"""
        return MCPTools()

    def test_server_health_check(self, tools):
        """Тест проверки здоровья MCP сервера"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200

            result = tools.check_server_health("localhost:8000")
            assert result is True

    def test_config_file_generation(self, tools):
        """Тест генерации файла конфигурации"""
        config_data = {
            "mcpServers": {
                "github": {
                    "command": "uvx",
                    "args": ["mcp-server-github"]
                }
            }
        }

        with patch('builtins.open', mock_open()) as mock_file:
            tools.save_config_to_file(config_data, "test_config.json")
            mock_file.assert_called_once_with("test_config.json", "w", encoding="utf-8")

    def test_template_loading(self, tools):
        """Тест загрузки шаблонов конфигурации"""
        mock_template = {
            "project_type": "frontend",
            "default_servers": ["github", "filesystem"]
        }

        with patch('json.load', return_value=mock_template):
            template = tools.load_config_template("frontend")
            assert template["project_type"] == "frontend"


class TestMCPSettings:
    """Тесты настроек MCP Configuration Agent"""

    @pytest.fixture
    def settings(self):
        """Создание экземпляра settings для тестов"""
        return MCPSettings()

    def test_default_settings_loading(self, settings):
        """Тест загрузки настроек по умолчанию"""
        assert settings.default_timeout > 0
        assert settings.max_servers > 0
        assert isinstance(settings.supported_frameworks, list)

    def test_custom_settings_override(self, settings):
        """Тест переопределения настроек"""
        custom_settings = {
            "default_timeout": 60,
            "max_servers": 20
        }

        settings.update_settings(custom_settings)
        assert settings.default_timeout == 60
        assert settings.max_servers == 20

    def test_settings_validation(self, settings):
        """Тест валидации настроек"""
        invalid_settings = {
            "default_timeout": -1,  # Некорректное значение
        }

        with pytest.raises(ValueError):
            settings.update_settings(invalid_settings)


class TestIntegration:
    """Интеграционные тесты MCP Configuration Agent"""

    @pytest.fixture
    def full_agent(self):
        """Полностью настроенный агент для интеграционных тестов"""
        agent = MCPConfigurationAgent()
        return agent

    def test_end_to_end_config_generation(self, full_agent):
        """Тест полного цикла генерации конфигурации"""
        # Генерируем конфигурацию
        config = full_agent.generate_config(
            project_type="fullstack",
            frontend_framework="react",
            backend_language="python",
            backend_framework="fastapi",
            database="postgresql"
        )

        # Проверяем результат
        assert config is not None
        assert "mcpServers" in config
        assert "project_info" in config

        # Валидируем конфигурацию
        validation_result = full_agent.validate_config(config)
        assert validation_result is True

    def test_config_export_import(self, full_agent, tmp_path):
        """Тест экспорта и импорта конфигурации"""
        # Генерируем конфигурацию
        original_config = full_agent.generate_config(
            project_type="frontend",
            framework="vue"
        )

        # Экспортируем в файл
        config_file = tmp_path / "test_config.json"
        full_agent.export_config(original_config, str(config_file))

        # Импортируем обратно
        imported_config = full_agent.import_config(str(config_file))

        # Сравниваем
        assert imported_config == original_config


# Фикстуры для mock объектов
def mock_open(mock_data=""):
    """Хелпер для мокирования файловых операций"""
    from unittest.mock import mock_open as mock_open_builtin
    return mock_open_builtin(read_data=mock_data)


# Конфигурация pytest
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Настройка тестового окружения"""
    # Установка тестовых переменных окружения
    import os
    os.environ.setdefault("GITHUB_TOKEN", "test_token")
    os.environ.setdefault("TEST_MODE", "true")

    yield

    # Очистка после тестов
    if "TEST_MODE" in os.environ:
        del os.environ["TEST_MODE"]


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__])