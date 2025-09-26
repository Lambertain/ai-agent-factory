"""
Dependencies для MCP Configuration Agent

Зависимости для универсального управления MCP серверами с поддержкой
различных технологических стеков и доменов разработки.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

from .settings import (
    MCPAgentSettings,
    DomainType,
    ProjectType,
    load_settings
)


@dataclass
class MCPConfigurationDeps:
    """
    Зависимости для MCP Configuration Agent.

    Поддерживает универсальную конфигурацию для различных доменов
    и типов проектов с адаптивными настройками.
    """

    # Основные настройки
    domain_type: DomainType = DomainType.GENERAL
    project_type: ProjectType = ProjectType.WEB_APPLICATION

    # Пути конфигурации
    config_base_path: Path = field(default_factory=lambda: Path.home())
    claude_config_path: Optional[Path] = None
    project_root_path: Path = field(default_factory=Path.cwd)

    # MCP серверы
    installed_servers: List[str] = field(default_factory=list)
    active_servers: List[str] = field(default_factory=list)
    failed_servers: List[str] = field(default_factory=list)

    # Настройки установки
    package_manager: str = "npm"  # npm, pip, uv, git
    auto_configure: bool = True
    validate_after_install: bool = True
    backup_config: bool = True

    # RAG и база знаний
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "mcp-configuration", "agent-knowledge", "mcp-servers", "claude-desktop"
    ])
    knowledge_domain: Optional[str] = "docs.anthropic.com"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Адаптивные конфигурации по домену
    recommended_servers: List[str] = field(default_factory=list)
    optional_servers: List[str] = field(default_factory=list)

    # Переменные окружения для серверов
    server_env_vars: Dict[str, str] = field(default_factory=dict)

    # Настройки валидации
    validation_timeout: int = 30
    retry_attempts: int = 3

    def __post_init__(self):
        """Инициализация зависимостей с адаптивными настройками."""
        # Определяем путь к конфигурации Claude Desktop
        if not self.claude_config_path:
            self.claude_config_path = self._get_claude_config_path()

        # Настраиваем рекомендованные серверы по домену
        self._configure_domain_recommendations()

        # Загружаем переменные окружения для серверов
        self._load_server_env_vars()

        # Обновляем теги знаний для специфичного домена
        self._update_knowledge_tags()

    def _get_claude_config_path(self) -> Path:
        """Определить путь к конфигурации Claude Desktop для текущей ОС."""
        import sys

        if sys.platform == "win32":
            return self.config_base_path / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        elif sys.platform == "darwin":
            return self.config_base_path / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return self.config_base_path / ".config" / "claude" / "claude_desktop_config.json"

    def _configure_domain_recommendations(self):
        """Настроить рекомендованные серверы по домену."""
        domain_configs = {
            DomainType.FRONTEND: {
                "recommended": ["filesystem", "brave-search", "github"],
                "optional": ["figma", "linear", "slack"]
            },
            DomainType.BACKEND: {
                "recommended": ["postgres", "github", "filesystem"],
                "optional": ["docker", "kubernetes", "redis"]
            },
            DomainType.FULLSTACK: {
                "recommended": ["postgres", "github", "filesystem", "brave-search"],
                "optional": ["docker", "slack", "linear"]
            },
            DomainType.AI_ML: {
                "recommended": ["brave-search", "github", "filesystem"],
                "optional": ["postgres", "jupyter", "python-execution"]
            },
            DomainType.SECURITY: {
                "recommended": ["github", "filesystem"],
                "optional": ["kubernetes", "docker", "security-scanner"]
            },
            DomainType.MOBILE: {
                "recommended": ["github", "filesystem", "brave-search"],
                "optional": ["firebase", "app-store-connect"]
            },
            DomainType.DEVOPS: {
                "recommended": ["kubernetes", "docker", "github", "filesystem"],
                "optional": ["terraform", "ansible", "monitoring"]
            },
            DomainType.DATA_SCIENCE: {
                "recommended": ["postgres", "python-execution", "filesystem", "brave-search"],
                "optional": ["jupyter", "bigquery", "s3"]
            },
            DomainType.GENERAL: {
                "recommended": ["filesystem", "brave-search", "github"],
                "optional": ["postgres", "slack"]
            }
        }

        config = domain_configs.get(self.domain_type, domain_configs[DomainType.GENERAL])
        self.recommended_servers = config["recommended"]
        self.optional_servers = config["optional"]

    def _load_server_env_vars(self):
        """Загрузить переменные окружения для MCP серверов."""
        # Стандартные переменные для популярных серверов
        env_mappings = {
            "brave-search": ["BRAVE_API_KEY"],
            "github": ["GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN"],
            "postgres": ["POSTGRES_CONNECTION_STRING", "DATABASE_URL"],
            "slack": ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN"],
            "linear": ["LINEAR_API_KEY"],
            "figma": ["FIGMA_ACCESS_TOKEN"],
            "kubernetes": ["KUBECONFIG", "K8S_CLUSTER_URL"],
            "docker": ["DOCKER_HOST"],
            "jupyter": ["JUPYTER_TOKEN"],
            "firebase": ["FIREBASE_PROJECT_ID", "GOOGLE_APPLICATION_CREDENTIALS"]
        }

        # Загружаем только доступные переменные
        for server, env_vars in env_mappings.items():
            for env_var in env_vars:
                value = os.getenv(env_var)
                if value:
                    self.server_env_vars[env_var] = value
                    break  # Берем первую доступную переменную

    def _update_knowledge_tags(self):
        """Обновить теги знаний для специфичного домена."""
        domain_tags = {
            DomainType.FRONTEND: ["frontend", "react", "vue", "angular"],
            DomainType.BACKEND: ["backend", "api", "microservices", "database"],
            DomainType.FULLSTACK: ["fullstack", "web-development"],
            DomainType.AI_ML: ["ai", "ml", "machine-learning", "llm"],
            DomainType.SECURITY: ["security", "audit", "compliance"],
            DomainType.MOBILE: ["mobile", "ios", "android", "react-native"],
            DomainType.DEVOPS: ["devops", "ci-cd", "kubernetes", "docker"],
            DomainType.DATA_SCIENCE: ["data-science", "analytics", "jupyter"],
            DomainType.GENERAL: ["general", "development"]
        }

        specific_tags = domain_tags.get(self.domain_type, [])
        self.knowledge_tags.extend(specific_tags)

    def get_server_config_template(self, server_name: str) -> Dict[str, Any]:
        """
        Получить шаблон конфигурации для конкретного сервера.

        Args:
            server_name: Имя MCP сервера

        Returns:
            Шаблон конфигурации сервера
        """
        templates = {
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", str(self.project_root_path)],
                "description": "Доступ к файловой системе проекта"
            },
            "brave-search": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": self.server_env_vars.get("BRAVE_API_KEY", "")},
                "description": "Поиск в интернете через Brave Search"
            },
            "github": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": self.server_env_vars.get("GITHUB_PERSONAL_ACCESS_TOKEN", "")},
                "description": "Интеграция с GitHub API"
            },
            "postgres": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-postgres"],
                "env": {"POSTGRES_CONNECTION_STRING": self.server_env_vars.get("POSTGRES_CONNECTION_STRING", "")},
                "description": "Подключение к PostgreSQL базе данных"
            }
        }

        return templates.get(server_name, {
            "command": "npx",
            "args": [f"@modelcontextprotocol/server-{server_name}"],
            "description": f"MCP сервер {server_name}"
        })

    def is_server_configured(self, server_name: str) -> bool:
        """Проверить настроен ли сервер."""
        return server_name in self.active_servers

    def get_missing_env_vars(self, server_name: str) -> List[str]:
        """Получить список отсутствующих переменных окружения для сервера."""
        required_vars = {
            "brave-search": ["BRAVE_API_KEY"],
            "github": ["GITHUB_PERSONAL_ACCESS_TOKEN"],
            "postgres": ["POSTGRES_CONNECTION_STRING"],
            "slack": ["SLACK_BOT_TOKEN"],
            "linear": ["LINEAR_API_KEY"],
            "figma": ["FIGMA_ACCESS_TOKEN"]
        }

        server_vars = required_vars.get(server_name, [])
        return [var for var in server_vars if var not in self.server_env_vars]

    def get_domain_description(self) -> str:
        """Получить описание текущего домена."""
        descriptions = {
            DomainType.FRONTEND: "Frontend разработка (React, Vue, Angular)",
            DomainType.BACKEND: "Backend разработка (API, микросервисы)",
            DomainType.FULLSTACK: "Полнофункциональная веб-разработка",
            DomainType.AI_ML: "AI/ML разработка и исследования",
            DomainType.SECURITY: "Security аудит и тестирование",
            DomainType.MOBILE: "Мобильная разработка",
            DomainType.DEVOPS: "DevOps и инфраструктура",
            DomainType.DATA_SCIENCE: "Data Science и аналитика",
            DomainType.GENERAL: "Общая разработка"
        }

        return descriptions.get(self.domain_type, "Универсальная разработка")


def create_mcp_deps(
    domain_type: DomainType = DomainType.GENERAL,
    project_type: ProjectType = ProjectType.WEB_APPLICATION,
    project_root: Optional[Path] = None,
    **kwargs
) -> MCPConfigurationDeps:
    """
    Создать зависимости для MCP Configuration Agent с настройками.

    Args:
        domain_type: Тип домена разработки
        project_type: Тип проекта
        project_root: Корневая папка проекта
        **kwargs: Дополнительные параметры

    Returns:
        Настроенные зависимости агента
    """
    # Загружаем основные настройки
    settings = load_settings()

    # Определяем корневую папку проекта
    if not project_root:
        project_root = Path.cwd()

    return MCPConfigurationDeps(
        domain_type=domain_type,
        project_type=project_type,
        project_root_path=project_root,
        package_manager=settings.package_manager,
        auto_configure=settings.auto_configure,
        validate_after_install=settings.validate_after_install,
        backup_config=settings.backup_config,
        validation_timeout=settings.validation_timeout,
        retry_attempts=settings.retry_attempts,
        **kwargs
    )


def create_domain_specific_deps(domain: str, project_path: Optional[str] = None) -> MCPConfigurationDeps:
    """
    Создать зависимости для конкретного домена разработки.

    Args:
        domain: Строковое название домена (frontend, backend, ai, etc.)
        project_path: Путь к проекту

    Returns:
        Зависимости настроенные для домена
    """
    # Маппинг строковых названий на енумы
    domain_mapping = {
        "frontend": DomainType.FRONTEND,
        "backend": DomainType.BACKEND,
        "fullstack": DomainType.FULLSTACK,
        "ai": DomainType.AI_ML,
        "ml": DomainType.AI_ML,
        "security": DomainType.SECURITY,
        "mobile": DomainType.MOBILE,
        "devops": DomainType.DEVOPS,
        "data": DomainType.DATA_SCIENCE,
        "general": DomainType.GENERAL
    }

    domain_type = domain_mapping.get(domain.lower(), DomainType.GENERAL)
    project_root = Path(project_path) if project_path else None

    return create_mcp_deps(
        domain_type=domain_type,
        project_root=project_root
    )


# Быстрые конфигурации для популярных случаев
def create_frontend_deps(project_path: Optional[str] = None) -> MCPConfigurationDeps:
    """Создать зависимости для frontend разработки."""
    return create_domain_specific_deps("frontend", project_path)


def create_backend_deps(project_path: Optional[str] = None) -> MCPConfigurationDeps:
    """Создать зависимости для backend разработки."""
    return create_domain_specific_deps("backend", project_path)


def create_fullstack_deps(project_path: Optional[str] = None) -> MCPConfigurationDeps:
    """Создать зависимости для fullstack разработки."""
    return create_domain_specific_deps("fullstack", project_path)


def create_ai_deps(project_path: Optional[str] = None) -> MCPConfigurationDeps:
    """Создать зависимости для AI/ML разработки."""
    return create_domain_specific_deps("ai", project_path)


# Примеры использования
EXAMPLE_DEPS = {
    "frontend_react": create_frontend_deps(),
    "backend_api": create_backend_deps(),
    "fullstack_webapp": create_fullstack_deps(),
    "ai_research": create_ai_deps()
}