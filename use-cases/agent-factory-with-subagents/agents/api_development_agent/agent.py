"""
Universal API Development Agent.

AI agent specialized in API development across multiple frameworks and domains.
Supports Express.js, NestJS, FastAPI, Django REST, ASP.NET Core, and Spring Boot.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import APIAgentDependencies
from ..common import check_pm_switch
from .prompts import get_system_prompt
from .tools import (
    search_agent_knowledge,
    generate_api_endpoint,
    generate_api_middleware,
    generate_api_documentation,
    generate_api_tests,
    validate_api_configuration,
    generate_deployment_config
)
from .settings import get_llm_model


# Create the universal API development agent
api_development_agent = Agent(
    get_llm_model(),
    deps_type=APIAgentDependencies,
    system_prompt=get_system_prompt,
    retries=2
)


# Register agent tools
@api_development_agent.tool
async def search_knowledge_base(
    ctx: RunContext[APIAgentDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Search API development knowledge base for relevant information.

    Use this tool to find patterns, examples, and best practices for API development.
    Search covers framework-specific patterns, security practices, and domain-specific considerations.

    Args:
        query: Search query (e.g., "express authentication", "fastapi validation", "nestjs guards")
        match_count: Number of results to return (default: 5)

    Returns:
        Relevant knowledge and code examples
    """
    return await search_agent_knowledge(ctx, query, match_count)


@api_development_agent.tool
async def create_api_endpoint(
    ctx: RunContext[APIAgentDependencies],
    endpoint_name: str,
    http_method: str,
    resource_type: str = "collection",
    include_auth: bool = True
) -> str:
    """
    Generate complete API endpoint code for the configured framework.

    Creates endpoint with proper routing, validation, error handling, and authentication
    based on the agent's current configuration.

    Args:
        endpoint_name: Name of the resource/endpoint (e.g., "users", "products", "orders")
        http_method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        resource_type: Type of resource ("collection", "single", "nested")
        include_auth: Whether to include authentication middleware

    Returns:
        Complete endpoint implementation code
    """
    return await generate_api_endpoint(ctx, endpoint_name, http_method, resource_type, include_auth)


@api_development_agent.tool
async def create_middleware(
    ctx: RunContext[APIAgentDependencies],
    middleware_type: str,
    custom_options: dict = None
) -> str:
    """
    Generate middleware code for the API framework.

    Creates middleware for common API concerns like authentication, CORS, rate limiting,
    logging, and validation based on the configured framework.

    Args:
        middleware_type: Type of middleware ("auth", "cors", "logging", "rate-limit", "validation", "error-handling")
        custom_options: Custom configuration options for the middleware

    Returns:
        Generated middleware implementation
    """
    return await generate_api_middleware(ctx, middleware_type, custom_options or {})


@api_development_agent.tool
async def create_api_documentation(
    ctx: RunContext[APIAgentDependencies],
    endpoints: list,
    include_examples: bool = True
) -> str:
    """
    Generate comprehensive API documentation.

    Creates documentation in the configured format (OpenAPI, Postman, etc.)
    with endpoint descriptions, request/response schemas, and examples.

    Args:
        endpoints: List of endpoint definitions to document
        include_examples: Whether to include request/response examples

    Returns:
        Generated API documentation
    """
    return await generate_api_documentation(ctx, endpoints, include_examples)


@api_development_agent.tool
async def create_endpoint_tests(
    ctx: RunContext[APIAgentDependencies],
    endpoint_name: str,
    test_types: list = None
) -> str:
    """
    Generate comprehensive test cases for API endpoints.

    Creates unit tests, integration tests, and e2e tests using the configured
    testing framework with proper setup, teardown, and assertions.

    Args:
        endpoint_name: Name of the endpoint to test
        test_types: Types of tests to generate (["unit", "integration", "e2e"])

    Returns:
        Generated test code with complete test coverage
    """
    return await generate_api_tests(ctx, endpoint_name, test_types or ["unit", "integration"])


@api_development_agent.tool
async def validate_configuration(
    ctx: RunContext[APIAgentDependencies]
) -> str:
    """
    Validate current API configuration and suggest improvements.

    Analyzes the current agent configuration for compatibility issues,
    security concerns, and optimization opportunities.

    Returns:
        Validation results with warnings, errors, and recommendations
    """
    return await validate_api_configuration(ctx)


@api_development_agent.tool
async def create_deployment_configuration(
    ctx: RunContext[APIAgentDependencies],
    deployment_type: str = "docker"
) -> str:
    """
    Generate deployment configuration files.

    Creates deployment configurations for containerization, orchestration,
    or serverless deployment based on the specified type.

    Args:
        deployment_type: Type of deployment ("docker", "kubernetes", "serverless")

    Returns:
        Generated deployment configuration files
    """
    return await generate_deployment_config(ctx, deployment_type)


@api_development_agent.tool
async def analyze_project_structure(
    ctx: RunContext[APIAgentDependencies],
    project_path: str
) -> str:
    """
    Analyze existing project structure and suggest API improvements.

    Examines the current project directory structure, identifies the framework,
    and provides recommendations for API organization and best practices.

    Args:
        project_path: Path to the project directory to analyze

    Returns:
        Analysis results with recommendations for improvement
    """
    import os
    from pathlib import Path

    try:
        project_dir = Path(project_path)
        if not project_dir.exists():
            return f"❌ Проект не найден по пути: {project_path}"

        analysis = ["📁 Анализ структуры проекта API:\n"]

        # Check for common files
        package_json = project_dir / "package.json"
        requirements_txt = project_dir / "requirements.txt"
        csproj_files = list(project_dir.glob("*.csproj"))
        pom_xml = project_dir / "pom.xml"

        # Detect framework
        detected_framework = "unknown"
        if package_json.exists():
            analysis.append("✅ Node.js проект обнаружен (package.json)")
            # Could parse package.json to detect Express/NestJS
            detected_framework = "nodejs"
        elif requirements_txt.exists():
            analysis.append("✅ Python проект обнаружен (requirements.txt)")
            detected_framework = "python"
        elif csproj_files:
            analysis.append("✅ .NET проект обнаружен (.csproj файлы)")
            detected_framework = "dotnet"
        elif pom_xml.exists():
            analysis.append("✅ Java проект обнаружен (pom.xml)")
            detected_framework = "java"

        # Check directory structure
        common_dirs = ["src", "controllers", "routes", "middleware", "models", "services", "tests"]
        for dir_name in common_dirs:
            if (project_dir / dir_name).exists():
                analysis.append(f"📂 Найдена папка: {dir_name}")

        # API-specific analysis
        api_indicators = {
            "routes": "Маршруты API",
            "controllers": "Контроллеры",
            "middleware": "Middleware",
            "models": "Модели данных",
            "schemas": "Схемы валидации",
            "services": "Бизнес-логика",
            "tests": "Тесты"
        }

        found_indicators = []
        for indicator, description in api_indicators.items():
            if (project_dir / indicator).exists():
                found_indicators.append(f"✅ {description} ({indicator}/)")

        if found_indicators:
            analysis.append("\n📋 Компоненты API:")
            analysis.extend(found_indicators)

        # Recommendations
        analysis.append(f"\n💡 Рекомендации для {detected_framework} проекта:")

        if detected_framework == "nodejs":
            analysis.extend([
                "- Рассмотрите использование TypeScript для type safety",
                "- Внедрите ESLint и Prettier для качества кода",
                "- Добавьте Swagger/OpenAPI документацию",
                "- Настройте Jest для тестирования"
            ])
        elif detected_framework == "python":
            analysis.extend([
                "- Используйте FastAPI для современного API development",
                "- Внедрите Pydantic для валидации данных",
                "- Добавьте pytest для comprehensive testing",
                "- Настройте Black и flake8 для code quality"
            ])

        # Security recommendations
        analysis.append("\n🔒 Рекомендации по безопасности:")
        analysis.extend([
            "- Внедрите rate limiting",
            "- Добавьте CORS middleware",
            "- Настройте HTTPS",
            "- Используйте environment variables для секретов"
        ])

        return "\n".join(analysis)

    except Exception as e:
        return f"❌ Ошибка анализа проекта: {e}"


# Main agent instance for export
__all__ = ["api_development_agent", "APIAgentDependencies"]