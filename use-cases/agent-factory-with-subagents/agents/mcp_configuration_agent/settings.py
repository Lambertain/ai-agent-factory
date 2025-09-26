"""
Settings для MCP Configuration Agent

Конфигурация и настройки для универсального управления MCP серверами
с поддержкой различных доменов и типов проектов.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class DomainType(str, Enum):
    """Типы доменов разработки для MCP серверов."""
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    AI_ML = "ai_ml"
    SECURITY = "security"
    MOBILE = "mobile"
    DEVOPS = "devops"
    DATA_SCIENCE = "data_science"
    GENERAL = "general"


class ProjectType(str, Enum):
    """Типы проектов для конфигурации MCP."""
    WEB_APPLICATION = "web_application"
    API_SERVICE = "api_service"
    MOBILE_APP = "mobile_app"
    DESKTOP_APP = "desktop_app"
    ML_PROJECT = "ml_project"
    DATA_PIPELINE = "data_pipeline"
    MICROSERVICE = "microservice"
    LIBRARY = "library"
    CLI_TOOL = "cli_tool"
    RESEARCH = "research"


class PackageManager(str, Enum):
    """Поддерживаемые пакетные менеджеры."""
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"
    PIP = "pip"
    UV = "uv"
    CONDA = "conda"


class MCPAgentSettings(BaseSettings):
    """Основные настройки MCP Configuration Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # === УНИВЕРСАЛЬНАЯ КОНФИГУРАЦИЯ ===
    domain_type: DomainType = Field(
        default=DomainType.GENERAL,
        description="Тип домена разработки"
    )
    project_type: ProjectType = Field(
        default=ProjectType.WEB_APPLICATION,
        description="Тип проекта"
    )
    package_manager: PackageManager = Field(
        default=PackageManager.NPM,
        description="Предпочитаемый пакетный менеджер"
    )

    # === ПУТИ И КОНФИГУРАЦИЯ ===
    project_root: str = Field(
        default_factory=lambda: str(Path.cwd()),
        description="Корневая папка проекта"
    )
    claude_config_path: Optional[str] = Field(
        default=None,
        description="Путь к конфигурации Claude Desktop (авто-определение)"
    )
    backup_directory: str = Field(
        default_factory=lambda: str(Path.home() / ".mcp_agent_backups"),
        description="Папка для резервных копий"
    )

    # === НАСТРОЙКИ УСТАНОВКИ ===
    auto_install: bool = Field(
        default=True,
        description="Автоматическая установка рекомендованных серверов"
    )
    auto_configure: bool = Field(
        default=True,
        description="Автоматическая настройка Claude Desktop"
    )
    validate_after_install: bool = Field(
        default=True,
        description="Валидировать серверы после установки"
    )
    backup_config: bool = Field(
        default=True,
        description="Создавать резервные копии конфигураций"
    )

    # === НАСТРОЙКИ ВАЛИДАЦИИ ===
    validation_timeout: int = Field(
        default=30,
        description="Таймаут валидации в секундах",
        ge=5, le=300
    )
    retry_attempts: int = Field(
        default=3,
        description="Количество попыток при ошибках",
        ge=1, le=10
    )
    test_connection: bool = Field(
        default=True,
        description="Тестировать подключение при валидации"
    )

    # === MCP СЕРВЕРЫ ===
    default_servers: List[str] = Field(
        default_factory=lambda: ["filesystem", "brave-search", "github"],
        description="Серверы по умолчанию для установки"
    )
    excluded_servers: List[str] = Field(
        default_factory=list,
        description="Исключенные серверы (не устанавливать автоматически)"
    )

    # === ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===
    # API ключи для различных сервисов
    brave_api_key: Optional[str] = Field(
        default=None,
        description="API ключ Brave Search"
    )
    github_token: Optional[str] = Field(
        default=None,
        description="GitHub Personal Access Token"
    )
    postgres_connection: Optional[str] = Field(
        default=None,
        description="PostgreSQL connection string"
    )
    slack_bot_token: Optional[str] = Field(
        default=None,
        description="Slack Bot Token"
    )
    linear_api_key: Optional[str] = Field(
        default=None,
        description="Linear API Key"
    )
    figma_access_token: Optional[str] = Field(
        default=None,
        description="Figma Access Token"
    )

    # === RAG И БАЗА ЗНАНИЙ ===
    knowledge_tags: List[str] = Field(
        default_factory=lambda: [
            "mcp-configuration",
            "agent-knowledge",
            "claude-desktop",
            "mcp-servers"
        ],
        description="Теги для поиска знаний в RAG"
    )
    knowledge_domain: Optional[str] = Field(
        default="docs.anthropic.com",
        description="Домен источника знаний"
    )
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта в Archon"
    )

    # === БЕЗОПАСНОСТЬ ===
    max_concurrent_installs: int = Field(
        default=3,
        description="Максимальное количество одновременных установок",
        ge=1, le=10
    )
    secure_env_handling: bool = Field(
        default=True,
        description="Безопасная обработка переменных окружения"
    )
    validate_certificates: bool = Field(
        default=True,
        description="Валидировать SSL сертификаты при загрузках"
    )


# === КОНФИГУРАЦИИ ДЛЯ РАЗЛИЧНЫХ ДОМЕНОВ ===

DOMAIN_CONFIGURATIONS = {
    DomainType.FRONTEND: {
        "description": "Frontend разработка (React, Vue, Angular)",
        "recommended_servers": ["filesystem", "brave-search", "github"],
        "optional_servers": ["figma", "linear", "slack"],
        "required_env_vars": [],
        "filesystem_paths": ["src/", "public/", "components/", "assets/"],
        "package_managers": [PackageManager.NPM, PackageManager.YARN, PackageManager.PNPM]
    },
    DomainType.BACKEND: {
        "description": "Backend разработка (API, микросервисы)",
        "recommended_servers": ["postgres", "github", "filesystem"],
        "optional_servers": ["docker", "kubernetes", "redis", "slack"],
        "required_env_vars": ["POSTGRES_CONNECTION"],
        "filesystem_paths": ["src/", "api/", "migrations/", "config/"],
        "package_managers": [PackageManager.NPM, PackageManager.PIP, PackageManager.UV]
    },
    DomainType.FULLSTACK: {
        "description": "Полнофункциональная веб-разработка",
        "recommended_servers": ["postgres", "github", "filesystem", "brave-search"],
        "optional_servers": ["docker", "slack", "linear", "figma"],
        "required_env_vars": ["POSTGRES_CONNECTION"],
        "filesystem_paths": ["src/", "api/", "public/", "components/"],
        "package_managers": [PackageManager.NPM, PackageManager.YARN]
    },
    DomainType.AI_ML: {
        "description": "AI/ML разработка и исследования",
        "recommended_servers": ["brave-search", "github", "filesystem"],
        "optional_servers": ["postgres", "jupyter", "python-execution"],
        "required_env_vars": [],
        "filesystem_paths": ["data/", "models/", "notebooks/", "src/"],
        "package_managers": [PackageManager.PIP, PackageManager.UV, PackageManager.CONDA]
    },
    DomainType.SECURITY: {
        "description": "Security аудит и тестирование",
        "recommended_servers": ["github", "filesystem"],
        "optional_servers": ["kubernetes", "docker", "security-scanner"],
        "required_env_vars": [],
        "filesystem_paths": ["scripts/", "reports/", "configs/"],
        "package_managers": [PackageManager.PIP, PackageManager.NPM]
    },
    DomainType.MOBILE: {
        "description": "Мобильная разработка",
        "recommended_servers": ["github", "filesystem", "brave-search"],
        "optional_servers": ["firebase", "app-store-connect"],
        "required_env_vars": [],
        "filesystem_paths": ["src/", "assets/", "android/", "ios/"],
        "package_managers": [PackageManager.NPM, PackageManager.YARN]
    },
    DomainType.DEVOPS: {
        "description": "DevOps и инфраструктура",
        "recommended_servers": ["kubernetes", "docker", "github", "filesystem"],
        "optional_servers": ["terraform", "ansible", "monitoring"],
        "required_env_vars": [],
        "filesystem_paths": ["infrastructure/", "deployments/", "configs/"],
        "package_managers": [PackageManager.PIP, PackageManager.NPM]
    },
    DomainType.DATA_SCIENCE: {
        "description": "Data Science и аналитика",
        "recommended_servers": ["postgres", "python-execution", "filesystem", "brave-search"],
        "optional_servers": ["jupyter", "bigquery", "s3"],
        "required_env_vars": ["POSTGRES_CONNECTION"],
        "filesystem_paths": ["data/", "notebooks/", "reports/", "models/"],
        "package_managers": [PackageManager.PIP, PackageManager.CONDA, PackageManager.UV]
    },
    DomainType.GENERAL: {
        "description": "Универсальная разработка",
        "recommended_servers": ["filesystem", "brave-search", "github"],
        "optional_servers": ["postgres", "slack"],
        "required_env_vars": [],
        "filesystem_paths": ["src/", "docs/"],
        "package_managers": [PackageManager.NPM, PackageManager.PIP]
    }
}


# === КОНФИГУРАЦИИ МСР СЕРВЕРОВ ===

MCP_SERVER_CONFIGS = {
    "filesystem": {
        "package": "@modelcontextprotocol/server-filesystem",
        "command": "npx",
        "description": "Доступ к файловой системе",
        "env_vars": [],
        "install_command": "npm install -g @modelcontextprotocol/server-filesystem",
        "validation_test": "filesystem_test"
    },
    "brave-search": {
        "package": "@modelcontextprotocol/server-brave-search",
        "command": "npx",
        "description": "Поиск в интернете через Brave Search",
        "env_vars": ["BRAVE_API_KEY"],
        "install_command": "npm install -g @modelcontextprotocol/server-brave-search",
        "validation_test": "search_test"
    },
    "github": {
        "package": "@modelcontextprotocol/server-github",
        "command": "npx",
        "description": "Интеграция с GitHub API",
        "env_vars": ["GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN"],
        "install_command": "npm install -g @modelcontextprotocol/server-github",
        "validation_test": "github_test"
    },
    "postgres": {
        "package": "@modelcontextprotocol/server-postgres",
        "command": "npx",
        "description": "Подключение к PostgreSQL",
        "env_vars": ["POSTGRES_CONNECTION_STRING", "DATABASE_URL"],
        "install_command": "npm install -g @modelcontextprotocol/server-postgres",
        "validation_test": "postgres_test"
    },
    "slack": {
        "package": "@modelcontextprotocol/server-slack",
        "command": "npx",
        "description": "Интеграция со Slack",
        "env_vars": ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN"],
        "install_command": "npm install -g @modelcontextprotocol/server-slack",
        "validation_test": "slack_test"
    }
}


def load_settings() -> MCPAgentSettings:
    """Загружает настройки агента с проверкой окружения."""
    try:
        return MCPAgentSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        raise ValueError(error_msg) from e


def get_domain_config(domain_type: DomainType) -> Dict[str, Any]:
    """Получает конфигурацию для конкретного домена."""
    return DOMAIN_CONFIGURATIONS.get(domain_type, DOMAIN_CONFIGURATIONS[DomainType.GENERAL])


def get_server_config(server_name: str) -> Dict[str, Any]:
    """Получает конфигурацию для конкретного MCP сервера."""
    return MCP_SERVER_CONFIGS.get(server_name, {})


def create_adaptive_config(
    domain_type: DomainType,
    project_type: ProjectType,
    project_root: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Создает адаптивную конфигурацию на основе домена и типа проекта.

    Args:
        domain_type: Тип домена разработки
        project_type: Тип проекта
        project_root: Корневая папка проекта

    Returns:
        Адаптивная конфигурация
    """
    # Базовая конфигурация
    config = {
        "domain_type": domain_type,
        "project_type": project_type,
        "project_root_path": project_root or Path.cwd()
    }

    # Добавляем конфигурацию домена
    domain_config = get_domain_config(domain_type)
    config.update(domain_config)

    # Адаптируем под тип проекта
    if project_type == ProjectType.API_SERVICE:
        config["recommended_servers"].extend(["postgres"])
        config["filesystem_paths"] = ["api/", "schemas/", "tests/"]
    elif project_type == ProjectType.ML_PROJECT:
        config["recommended_servers"].extend(["jupyter", "python-execution"])
        config["filesystem_paths"] = ["data/", "models/", "experiments/"]
    elif project_type == ProjectType.MOBILE_APP:
        config["recommended_servers"].extend(["firebase"])
        config["filesystem_paths"] = ["src/", "assets/", "platform/"]

    return config


def get_recommended_package_manager(domain_type: DomainType) -> PackageManager:
    """Получает рекомендованный пакетный менеджер для домена."""
    recommendations = {
        DomainType.FRONTEND: PackageManager.NPM,
        DomainType.BACKEND: PackageManager.NPM,
        DomainType.FULLSTACK: PackageManager.NPM,
        DomainType.AI_ML: PackageManager.PIP,
        DomainType.SECURITY: PackageManager.PIP,
        DomainType.MOBILE: PackageManager.NPM,
        DomainType.DEVOPS: PackageManager.PIP,
        DomainType.DATA_SCIENCE: PackageManager.PIP,
        DomainType.GENERAL: PackageManager.NPM
    }
    return recommendations.get(domain_type, PackageManager.NPM)


def validate_env_vars(required_vars: List[str]) -> Dict[str, bool]:
    """Проверяет наличие необходимых переменных окружения."""
    return {var: os.getenv(var) is not None for var in required_vars}


def create_env_template(domain_type: DomainType) -> str:
    """Создает шаблон .env файла для домена."""
    domain_config = get_domain_config(domain_type)
    required_vars = domain_config.get("required_env_vars", [])

    # Добавляем общие переменные
    all_vars = [
        "# MCP Configuration Agent - Environment Variables",
        "",
        "# === ОБЩИЕ НАСТРОЙКИ ===",
        "# CLAUDE_DESKTOP_CONFIG_PATH=/path/to/claude_desktop_config.json",
        "",
        "# === API КЛЮЧИ ===",
        "# BRAVE_API_KEY=your_brave_api_key_here",
        "# GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here",
        "# GITHUB_TOKEN=your_github_token_here",
        ""
    ]

    # Добавляем специфичные для домена переменные
    if "POSTGRES_CONNECTION" in required_vars:
        all_vars.extend([
            "# === DATABASE ===",
            "# POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost:5432/dbname",
            "# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname",
            ""
        ])

    if domain_type in [DomainType.FULLSTACK, DomainType.BACKEND]:
        all_vars.extend([
            "# === ДОПОЛНИТЕЛЬНЫЕ СЕРВИСЫ ===",
            "# SLACK_BOT_TOKEN=xoxb-your-bot-token",
            "# LINEAR_API_KEY=your_linear_api_key",
            ""
        ])

    all_vars.extend([
        "# === НАСТРОЙКИ АГЕНТА ===",
        f"# DOMAIN_TYPE={domain_type.value}",
        "# AUTO_CONFIGURE=true",
        "# BACKUP_CONFIG=true",
        "# VALIDATION_TIMEOUT=30"
    ])

    return "\n".join(all_vars)


# === ПРИМЕРЫ КОНФИГУРАЦИЙ ===

EXAMPLE_CONFIGS = {
    "frontend_react": create_adaptive_config(
        DomainType.FRONTEND,
        ProjectType.WEB_APPLICATION
    ),
    "backend_api": create_adaptive_config(
        DomainType.BACKEND,
        ProjectType.API_SERVICE
    ),
    "fullstack_webapp": create_adaptive_config(
        DomainType.FULLSTACK,
        ProjectType.WEB_APPLICATION
    ),
    "ai_research": create_adaptive_config(
        DomainType.AI_ML,
        ProjectType.ML_PROJECT
    ),
    "mobile_app": create_adaptive_config(
        DomainType.MOBILE,
        ProjectType.MOBILE_APP
    ),
    "devops_infrastructure": create_adaptive_config(
        DomainType.DEVOPS,
        ProjectType.MICROSERVICE
    )
}


if __name__ == "__main__":
    # Демонстрация конфигураций
    settings = load_settings()
    print(f"Базовые настройки: {settings.domain_type} / {settings.project_type}")

    for name, config in EXAMPLE_CONFIGS.items():
        print(f"\n{name}:")
        print(f"  - Домен: {config['domain_type']}")
        print(f"  - Тип: {config['project_type']}")
        print(f"  - Рекомендованные серверы: {', '.join(config['recommended_servers'])}")
        print(f"  - Файловые пути: {', '.join(config['filesystem_paths'])}")