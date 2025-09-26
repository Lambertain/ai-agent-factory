"""
MCP Configuration Agent

Универсальный агент для управления MCP серверами с поддержкой
различных технологических стеков и доменов разработки.

Основные возможности:
- Установка и настройка MCP серверов для различных доменов
- Автоматическая конфигурация Claude Desktop
- Валидация и тестирование серверов
- Рекомендации по оптимальному набору инструментов
- Управление жизненным циклом серверов

Поддерживаемые домены:
- Frontend (React, Vue, Angular)
- Backend (API, микросервисы)
- Fullstack (полнофункциональные приложения)
- AI/ML (машинное обучение)
- Security (аудит и тестирование)
- Mobile (мобильная разработка)
- DevOps (инфраструктура)
- Data Science (аналитика)

Примеры использования:
- Настройка полного стека для React приложения
- Конфигурация серверов для ML исследований
- Автоматическая установка инструментов для backend API
- Валидация существующих конфигураций
"""

from .agent import MCPConfigurationAgent
from .dependencies import (
    MCPConfigurationDeps,
    create_mcp_deps,
    create_domain_specific_deps,
    create_frontend_deps,
    create_backend_deps,
    create_fullstack_deps,
    create_ai_deps,
    EXAMPLE_DEPS
)
from .tools import (
    install_mcp_server,
    configure_claude_desktop_server,
    validate_mcp_server,
    get_recommended_servers,
    list_installed_servers,
    remove_mcp_server,
    search_agent_knowledge,
    configure_filesystem_server,
    configure_search_server
)
from .prompts import (
    MAIN_SYSTEM_PROMPT,
    PROJECT_ANALYSIS_PROMPT,
    VALIDATION_PROMPT,
    TROUBLESHOOTING_PROMPT,
    DOMAIN_SPECIFIC_PROMPTS,
    get_adaptive_system_prompt,
    get_validation_checklist,
    get_troubleshooting_guide,
    TASK_PROMPTS
)
from .settings import (
    MCPAgentSettings,
    DomainType,
    ProjectType,
    PackageManager,
    load_settings,
    get_domain_config,
    get_server_config,
    create_adaptive_config,
    get_recommended_package_manager,
    validate_env_vars,
    create_env_template,
    DOMAIN_CONFIGURATIONS,
    MCP_SERVER_CONFIGS,
    EXAMPLE_CONFIGS
)

# Версия агента
__version__ = "2.0.0"

# Метаданные агента
__agent_info__ = {
    "name": "MCP Configuration Agent",
    "version": __version__,
    "description": "Универсальный агент для управления MCP серверами с поддержкой различных доменов разработки",
    "domain": "mcp, configuration, claude-desktop",
    "framework": "Python",
    "capabilities": [
        "Установка MCP серверов через npm/pip/uv",
        "Автоматическая настройка Claude Desktop",
        "Валидация конфигураций серверов",
        "Рекомендации по доменам",
        "Управление жизненным циклом серверов",
        "Поддержка множественных пакетных менеджеров",
        "Резервное копирование конфигураций",
        "Диагностика и устранение проблем"
    ],
    "supported_domains": [
        "frontend", "backend", "fullstack", "ai_ml",
        "security", "mobile", "devops", "data_science", "general"
    ],
    "supported_package_managers": ["npm", "yarn", "pnpm", "pip", "uv", "conda"],
    "supported_servers": [
        "filesystem", "brave-search", "github", "postgres",
        "slack", "linear", "figma", "docker", "kubernetes"
    ],
    "integration": ["Claude Desktop", "MCP Protocol", "Package Managers"]
}

# Экспорт основных компонентов
__all__ = [
    # Основной класс агента
    "MCPConfigurationAgent",

    # Зависимости и фабричные функции
    "MCPConfigurationDeps",
    "create_mcp_deps",
    "create_domain_specific_deps",
    "create_frontend_deps",
    "create_backend_deps",
    "create_fullstack_deps",
    "create_ai_deps",
    "EXAMPLE_DEPS",

    # Инструменты
    "install_mcp_server",
    "configure_claude_desktop_server",
    "validate_mcp_server",
    "get_recommended_servers",
    "list_installed_servers",
    "remove_mcp_server",
    "search_agent_knowledge",
    "configure_filesystem_server",
    "configure_search_server",

    # Промпты и системные сообщения
    "MAIN_SYSTEM_PROMPT",
    "PROJECT_ANALYSIS_PROMPT",
    "VALIDATION_PROMPT",
    "TROUBLESHOOTING_PROMPT",
    "DOMAIN_SPECIFIC_PROMPTS",
    "get_adaptive_system_prompt",
    "get_validation_checklist",
    "get_troubleshooting_guide",
    "TASK_PROMPTS",

    # Настройки и конфигурации
    "MCPAgentSettings",
    "DomainType",
    "ProjectType",
    "PackageManager",
    "load_settings",
    "get_domain_config",
    "get_server_config",
    "create_adaptive_config",
    "get_recommended_package_manager",
    "validate_env_vars",
    "create_env_template",
    "DOMAIN_CONFIGURATIONS",
    "MCP_SERVER_CONFIGS",
    "EXAMPLE_CONFIGS",

    # Метаданные
    "__version__",
    "__agent_info__"
]


def get_agent_info():
    """Возвращает информацию о агенте."""
    return __agent_info__


def print_agent_capabilities():
    """Выводит возможности агента."""
    info = __agent_info__

    print(f"\n⚙️ {info['name']} v{info['version']}")
    print(f"📝 {info['description']}")
    print(f"🔧 Framework: {info['framework']}")

    print(f"\n✨ Основные возможности:")
    for capability in info['capabilities']:
        print(f"  • {capability}")

    print(f"\n🎯 Поддерживаемые домены:")
    for domain in info['supported_domains']:
        print(f"  • {domain}")

    print(f"\n📦 Поддерживаемые пакетные менеджеры:")
    for pm in info['supported_package_managers']:
        print(f"  • {pm}")

    print(f"\n🔧 Поддерживаемые MCP серверы:")
    for server in info['supported_servers']:
        print(f"  • {server}")


def create_quick_config(
    domain: str = "general",
    project_type: str = "web_application",
    package_manager: str = "npm"
) -> dict:
    """
    Создает быструю конфигурацию для агента.

    Args:
        domain: Домен разработки
        project_type: Тип проекта
        package_manager: Пакетный менеджер

    Returns:
        Словарь конфигурации
    """
    # Маппинг строковых значений в енумы
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

    project_mapping = {
        "web": ProjectType.WEB_APPLICATION,
        "web_application": ProjectType.WEB_APPLICATION,
        "api": ProjectType.API_SERVICE,
        "api_service": ProjectType.API_SERVICE,
        "mobile": ProjectType.MOBILE_APP,
        "mobile_app": ProjectType.MOBILE_APP,
        "desktop": ProjectType.DESKTOP_APP,
        "desktop_app": ProjectType.DESKTOP_APP,
        "ml": ProjectType.ML_PROJECT,
        "ml_project": ProjectType.ML_PROJECT,
        "data": ProjectType.DATA_PIPELINE,
        "data_pipeline": ProjectType.DATA_PIPELINE,
        "microservice": ProjectType.MICROSERVICE,
        "library": ProjectType.LIBRARY,
        "cli": ProjectType.CLI_TOOL,
        "cli_tool": ProjectType.CLI_TOOL,
        "research": ProjectType.RESEARCH
    }

    pm_mapping = {
        "npm": PackageManager.NPM,
        "yarn": PackageManager.YARN,
        "pnpm": PackageManager.PNPM,
        "pip": PackageManager.PIP,
        "uv": PackageManager.UV,
        "conda": PackageManager.CONDA
    }

    domain_enum = domain_mapping.get(domain.lower(), DomainType.GENERAL)
    project_enum = project_mapping.get(project_type.lower(), ProjectType.WEB_APPLICATION)
    pm_enum = pm_mapping.get(package_manager.lower(), PackageManager.NPM)

    config = create_adaptive_config(domain_enum, project_enum)
    config["package_manager"] = pm_enum

    return config


# Примеры быстрого создания конфигураций
QUICK_CONFIGS = {
    "frontend_react": create_quick_config("frontend", "web_application", "npm"),
    "backend_fastapi": create_quick_config("backend", "api_service", "pip"),
    "fullstack_nextjs": create_quick_config("fullstack", "web_application", "npm"),
    "ai_research": create_quick_config("ai", "ml_project", "pip"),
    "mobile_reactnative": create_quick_config("mobile", "mobile_app", "npm"),
    "devops_kubernetes": create_quick_config("devops", "microservice", "pip"),
    "data_jupyter": create_quick_config("data", "data_pipeline", "conda"),
    "security_audit": create_quick_config("security", "cli_tool", "pip")
}


async def quick_setup(domain: str, project_path: str = None) -> MCPConfigurationAgent:
    """
    Быстрая настройка MCP Configuration Agent для домена.

    Args:
        domain: Домен разработки (frontend, backend, ai, etc.)
        project_path: Путь к проекту

    Returns:
        Настроенный агент
    """
    config = create_quick_config(domain)

    if project_path:
        from pathlib import Path
        config["project_root_path"] = Path(project_path)

    # Создаем зависимости на основе конфигурации
    deps = create_domain_specific_deps(domain, project_path)

    # Создаем агент
    agent = MCPConfigurationAgent(
        config_domain=domain,
        project_type=config.get("project_type", "web_application")
    )

    return agent


def get_domain_info(domain: str) -> dict:
    """
    Получить информацию о конкретном домене.

    Args:
        domain: Название домена

    Returns:
        Информация о домене
    """
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

    domain_enum = domain_mapping.get(domain.lower())
    if not domain_enum:
        return {"error": f"Неподдерживаемый домен: {domain}"}

    config = get_domain_config(domain_enum)
    return {
        "domain": domain_enum.value,
        "description": config["description"],
        "recommended_servers": config["recommended_servers"],
        "optional_servers": config["optional_servers"],
        "required_env_vars": config.get("required_env_vars", []),
        "filesystem_paths": config.get("filesystem_paths", []),
        "package_managers": [pm.value for pm in config.get("package_managers", [])]
    }


if __name__ == "__main__":
    print_agent_capabilities()

    print(f"\n📋 Доступные быстрые конфигурации:")
    for name, config in QUICK_CONFIGS.items():
        domain_desc = get_domain_config(config['domain_type'])['description']
        print(f"  • {name}: {domain_desc}")

    print(f"\n🎯 Информация о доменах:")
    for domain in ["frontend", "backend", "ai", "security", "mobile"]:
        info = get_domain_info(domain)
        if "error" not in info:
            print(f"  • {domain}: {info['description']}")
            print(f"    Рекомендованные серверы: {', '.join(info['recommended_servers'])}")