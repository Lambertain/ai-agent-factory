"""
Universal API Development Agent Tools.

Comprehensive toolkit for API development across multiple frameworks.
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from pydantic_ai import RunContext
from .dependencies import APIAgentDependencies


async def search_agent_knowledge(
    ctx: RunContext[APIAgentDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Search API development knowledge base for relevant information.

    Args:
        ctx: Agent run context with dependencies
        query: Search query for API development topics
        match_count: Number of results to return

    Returns:
        Relevant API development knowledge and patterns
    """
    try:
        # Use knowledge tags for filtering
        search_tags = " ".join(ctx.deps.knowledge_tags)
        enhanced_query = f"{query} {search_tags} {ctx.deps.framework_type} {ctx.deps.domain_type}"

        # Simulate MCP Archon search (would be actual MCP call in production)
        knowledge_results = await _simulate_knowledge_search(enhanced_query, match_count)

        if knowledge_results:
            formatted_results = []
            for result in knowledge_results:
                formatted_results.append(f"**{result['title']}:**\n{result['content']}")

            return f"📚 База знаний API Development:\n" + "\n\n".join(formatted_results)
        else:
            return "Информация не найдена в базе знаний агента."

    except Exception as e:
        return f"Ошибка доступа к базе знаний: {e}"


async def generate_api_endpoint(
    ctx: RunContext[APIAgentDependencies],
    endpoint_name: str,
    http_method: str,
    resource_type: str,
    include_auth: bool = True
) -> str:
    """
    Generate API endpoint code based on framework and configuration.

    Args:
        ctx: Agent run context with dependencies
        endpoint_name: Name of the endpoint (e.g., 'users', 'products')
        http_method: HTTP method (GET, POST, PUT, DELETE, PATCH)
        resource_type: Type of resource (single, collection, nested)
        include_auth: Whether to include authentication

    Returns:
        Generated endpoint code for the configured framework
    """
    framework = ctx.deps.framework_type
    auth_strategy = ctx.deps.auth_strategy if include_auth else "none"

    endpoint_generators = {
        "express": _generate_express_endpoint,
        "nestjs": _generate_nestjs_endpoint,
        "fastapi": _generate_fastapi_endpoint,
        "django-rest": _generate_django_rest_endpoint,
        "aspnet-core": _generate_aspnet_endpoint,
        "spring-boot": _generate_spring_boot_endpoint
    }

    generator = endpoint_generators.get(framework, _generate_generic_endpoint)

    return await generator(
        endpoint_name=endpoint_name,
        http_method=http_method,
        resource_type=resource_type,
        auth_strategy=auth_strategy,
        deps=ctx.deps
    )


async def generate_api_middleware(
    ctx: RunContext[APIAgentDependencies],
    middleware_type: str,
    custom_options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate middleware code for the API framework.

    Args:
        ctx: Agent run context with dependencies
        middleware_type: Type of middleware (auth, cors, logging, rate-limit, validation)
        custom_options: Custom configuration options

    Returns:
        Generated middleware code
    """
    framework = ctx.deps.framework_type
    options = custom_options or {}

    middleware_generators = {
        "express": _generate_express_middleware,
        "nestjs": _generate_nestjs_middleware,
        "fastapi": _generate_fastapi_middleware,
        "django-rest": _generate_django_rest_middleware,
        "aspnet-core": _generate_aspnet_middleware,
        "spring-boot": _generate_spring_boot_middleware
    }

    generator = middleware_generators.get(framework, _generate_generic_middleware)

    return await generator(
        middleware_type=middleware_type,
        options=options,
        deps=ctx.deps
    )


async def generate_api_documentation(
    ctx: RunContext[APIAgentDependencies],
    endpoints: List[Dict[str, Any]],
    include_examples: bool = True
) -> str:
    """
    Generate API documentation based on the configured documentation type.

    Args:
        ctx: Agent run context with dependencies
        endpoints: List of endpoint definitions
        include_examples: Whether to include request/response examples

    Returns:
        Generated API documentation
    """
    doc_type = ctx.deps.documentation_type

    if doc_type == "openapi":
        return await _generate_openapi_docs(endpoints, ctx.deps, include_examples)
    elif doc_type == "postman":
        return await _generate_postman_collection(endpoints, ctx.deps)
    elif doc_type == "insomnia":
        return await _generate_insomnia_collection(endpoints, ctx.deps)
    else:
        return await _generate_markdown_docs(endpoints, ctx.deps, include_examples)


async def generate_api_tests(
    ctx: RunContext[APIAgentDependencies],
    endpoint_name: str,
    test_types: List[str] = None
) -> str:
    """
    Generate test cases for API endpoints.

    Args:
        ctx: Agent run context with dependencies
        endpoint_name: Name of the endpoint to test
        test_types: Types of tests (unit, integration, e2e)

    Returns:
        Generated test code
    """
    if test_types is None:
        test_types = ["unit", "integration"]

    framework = ctx.deps.framework_type
    testing_framework = ctx.deps.testing_framework

    test_generators = {
        "jest": _generate_jest_tests,
        "pytest": _generate_pytest_tests,
        "mocha": _generate_mocha_tests,
        "xunit": _generate_xunit_tests,
        "junit": _generate_junit_tests,
        "rspec": _generate_rspec_tests
    }

    generator = test_generators.get(testing_framework, _generate_generic_tests)

    return await generator(
        endpoint_name=endpoint_name,
        test_types=test_types,
        framework=framework,
        deps=ctx.deps
    )


async def validate_api_configuration(
    ctx: RunContext[APIAgentDependencies]
) -> str:
    """
    Validate the API configuration and suggest improvements.

    Args:
        ctx: Agent run context with dependencies

    Returns:
        Validation results and recommendations
    """
    deps = ctx.deps
    validation_results = []

    # Framework compatibility checks
    if deps.framework_type == "express" and not deps.typescript_enabled:
        validation_results.append("⚠️ Рекомендуется использовать TypeScript с Express для better type safety")

    if deps.framework_type == "nestjs" and not deps.typescript_enabled:
        validation_results.append("❌ NestJS требует TypeScript для корректной работы")

    # Security configuration checks
    security_config = deps.get_security_config()

    if deps.domain_type in ["fintech", "healthcare"] and security_config["auth_strategy"] == "basic":
        validation_results.append("⚠️ Для финтех/здравоохранения рекомендуется OAuth2 или JWT")

    if security_config["cors_enabled"] and deps.environment == "production":
        validation_results.append("⚠️ Убедитесь что CORS настроен правильно для production")

    # Performance checks
    perf_config = deps.get_performance_config()

    if deps.domain_type == "gaming" and perf_config["caching_strategy"] == "memory":
        validation_results.append("⚠️ Для игровых API рекомендуется Redis кэширование")

    if not perf_config["rate_limiting"] and deps.domain_type in ["social", "gaming"]:
        validation_results.append("❌ Rate limiting критично для социальных/игровых платформ")

    # Database configuration
    if deps.orm_framework == "auto":
        validation_results.append("ℹ️ ORM будет выбран автоматически на основе фреймворка")

    if not validation_results:
        validation_results.append("✅ Конфигурация API выглядит корректно")

    return "🔍 Результаты валидации конфигурации:\n" + "\n".join(validation_results)


async def generate_deployment_config(
    ctx: RunContext[APIAgentDependencies],
    deployment_type: str = "docker"
) -> str:
    """
    Generate deployment configuration files.

    Args:
        ctx: Agent run context with dependencies
        deployment_type: Type of deployment (docker, kubernetes, serverless)

    Returns:
        Generated deployment configuration
    """
    if deployment_type == "docker":
        return await _generate_dockerfile(ctx.deps)
    elif deployment_type == "kubernetes":
        return await _generate_k8s_manifests(ctx.deps)
    elif deployment_type == "serverless":
        return await _generate_serverless_config(ctx.deps)
    else:
        return "Неподдерживаемый тип развертывания"


# Helper functions for code generation

async def _simulate_knowledge_search(query: str, match_count: int) -> List[Dict[str, Any]]:
    """Simulate knowledge base search (would be actual MCP call in production)."""
    # Mock results based on query
    mock_results = [
        {
            "title": "API Security Best Practices",
            "content": "Always validate input, use HTTPS, implement proper authentication..."
        },
        {
            "title": "RESTful API Design Principles",
            "content": "Use proper HTTP methods, meaningful URLs, consistent response formats..."
        },
        {
            "title": "Error Handling Patterns",
            "content": "Implement centralized error handling, use proper HTTP status codes..."
        }
    ]
    return mock_results[:match_count]


async def _generate_express_endpoint(
    endpoint_name: str,
    http_method: str,
    resource_type: str,
    auth_strategy: str,
    deps: APIAgentDependencies
) -> str:
    """Generate Express.js endpoint code."""
    auth_middleware = ""
    if auth_strategy == "jwt":
        auth_middleware = ", authenticateJWT"
    elif auth_strategy == "basic":
        auth_middleware = ", authenticateBasic"

    method = http_method.lower()
    route = f"/{endpoint_name}" if resource_type == "collection" else f"/{endpoint_name}/:id"

    return f"""
// Express.js {http_method} endpoint for {endpoint_name}
app.{method}('{route}'{auth_middleware}, async (req, res, next) => {{
    try {{
        // Validate request
        const validationResult = validateRequest(req);
        if (!validationResult.isValid) {{
            return res.status(400).json({{
                error: 'Validation failed',
                details: validationResult.errors
            }});
        }}

        // Business logic
        const result = await {endpoint_name}Service.{method}({
            'get': 'req.params.id ? req.params.id : req.query',
            'post': 'req.body',
            'put': 'req.params.id, req.body',
            'delete': 'req.params.id',
            'patch': 'req.params.id, req.body'
        }[method]);

        // Response
        res.status({
            'get': '200',
            'post': '201',
            'put': '200',
            'delete': '204',
            'patch': '200'
        }[method]).json(result);

    }} catch (error) {{
        next(error);
    }}
}});

// {endpoint_name} service example
const {endpoint_name}Service = {{
    async {method}(params) {{
        // Database operation using {deps.orm_framework}
        // Implementation depends on your data layer
        return {{ message: '{http_method} {endpoint_name} successful' }};
    }}
}};
"""


async def _generate_nestjs_endpoint(
    endpoint_name: str,
    http_method: str,
    resource_type: str,
    auth_strategy: str,
    deps: APIAgentDependencies
) -> str:
    """Generate NestJS endpoint code."""
    auth_decorator = ""
    if auth_strategy == "jwt":
        auth_decorator = "@UseGuards(JwtAuthGuard)\n  "
    elif auth_strategy == "basic":
        auth_decorator = "@UseGuards(BasicAuthGuard)\n  "

    method_decorator = f"@{http_method.title()}()"
    if resource_type == "single":
        method_decorator = f"@{http_method.title()}(':id')"

    return f"""
// NestJS controller for {endpoint_name}
@Controller('{endpoint_name}')
export class {endpoint_name.title()}Controller {{
  constructor(private readonly {endpoint_name}Service: {endpoint_name.title()}Service) {{}}

  {auth_decorator}@{http_method.title()}({'' if resource_type == 'collection' else '\':id\''})
  async {method.lower()}({
      'get': '@Param(\'id\') id?: string, @Query() query?: any' if resource_type == 'single' else '@Query() query: any',
      'post': '@Body() createDto: Create{endpoint_name.title()}Dto',
      'put': '@Param(\'id\') id: string, @Body() updateDto: Update{endpoint_name.title()}Dto',
      'delete': '@Param(\'id\') id: string',
      'patch': '@Param(\'id\') id: string, @Body() patchDto: Partial<Update{endpoint_name.title()}Dto>'
  }.get(http_method.lower(), '@Body() body: any')}) {{
    return this.{endpoint_name}Service.{http_method.lower()}({
        'get': 'id || query',
        'post': 'createDto',
        'put': 'id, updateDto',
        'delete': 'id',
        'patch': 'id, patchDto'
    }.get(http_method.lower(), 'body')});
  }}
}}

// Service implementation
@Injectable()
export class {endpoint_name.title()}Service {{
  async {http_method.lower()}(params: any) {{
    // Business logic using {deps.orm_framework}
    return {{ message: '{http_method} {endpoint_name} successful' }};
  }}
}}
"""


async def _generate_fastapi_endpoint(
    endpoint_name: str,
    http_method: str,
    resource_type: str,
    auth_strategy: str,
    deps: APIAgentDependencies
) -> str:
    """Generate FastAPI endpoint code."""
    auth_dependency = ""
    if auth_strategy == "jwt":
        auth_dependency = ", current_user: User = Depends(get_current_user)"
    elif auth_strategy == "basic":
        auth_dependency = ", credentials: HTTPBasicCredentials = Depends(security)"

    path = f"/{endpoint_name}" if resource_type == "collection" else f"/{endpoint_name}/{{item_id}}"
    method = http_method.lower()

    return f"""
# FastAPI endpoint for {endpoint_name}
@app.{method}("{path}")
async def {method}_{endpoint_name}({
    'get': 'item_id: int = None, skip: int = 0, limit: int = 100' if resource_type == 'single' else 'skip: int = 0, limit: int = 100',
    'post': f'{endpoint_name}_data: {endpoint_name.title()}Create',
    'put': f'item_id: int, {endpoint_name}_data: {endpoint_name.title()}Update',
    'delete': 'item_id: int',
    'patch': f'item_id: int, {endpoint_name}_data: {endpoint_name.title()}Patch'
}.get(method, f'{endpoint_name}_data: dict')}{auth_dependency}):
    \"\"\"
    {http_method} operation for {endpoint_name} resource.
    \"\"\"
    try:
        result = await {endpoint_name}_service.{method}({
            'get': 'item_id, skip, limit' if resource_type == 'single' else 'skip, limit',
            'post': f'{endpoint_name}_data',
            'put': f'item_id, {endpoint_name}_data',
            'delete': 'item_id',
            'patch': f'item_id, {endpoint_name}_data'
        }.get(method, f'{endpoint_name}_data'))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic models
class {endpoint_name.title()}Base(BaseModel):
    name: str
    description: Optional[str] = None

class {endpoint_name.title()}Create({endpoint_name.title()}Base):
    pass

class {endpoint_name.title()}Update({endpoint_name.title()}Base):
    pass

class {endpoint_name.title()}Patch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
"""


async def _generate_generic_endpoint(
    endpoint_name: str,
    http_method: str,
    resource_type: str,
    auth_strategy: str,
    deps: APIAgentDependencies
) -> str:
    """Generate generic API endpoint pseudo-code."""
    return f"""
// Generic {http_method} endpoint for {endpoint_name}
// Framework: {deps.framework_type}
// Auth: {auth_strategy}
// Resource type: {resource_type}

endpoint {http_method} /{endpoint_name}:
  - validate authentication ({auth_strategy})
  - validate request data
  - execute business logic
  - return response with appropriate status code
  - handle errors gracefully
"""


# Additional helper functions would be implemented similarly for other frameworks
async def _generate_django_rest_endpoint(endpoint_name: str, http_method: str, resource_type: str, auth_strategy: str, deps: APIAgentDependencies) -> str:
    """Generate Django REST Framework endpoint code."""
    return "# Django REST Framework endpoint code would be generated here"

async def _generate_aspnet_endpoint(endpoint_name: str, http_method: str, resource_type: str, auth_strategy: str, deps: APIAgentDependencies) -> str:
    """Generate ASP.NET Core endpoint code."""
    return "// ASP.NET Core endpoint code would be generated here"

async def _generate_spring_boot_endpoint(endpoint_name: str, http_method: str, resource_type: str, auth_strategy: str, deps: APIAgentDependencies) -> str:
    """Generate Spring Boot endpoint code."""
    return "// Spring Boot endpoint code would be generated here"

# Middleware generators
async def _generate_express_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate Express middleware."""
    return "// Express middleware code would be generated here"

async def _generate_nestjs_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate NestJS middleware."""
    return "// NestJS middleware code would be generated here"

async def _generate_fastapi_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate FastAPI middleware."""
    return "# FastAPI middleware code would be generated here"

async def _generate_django_rest_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate Django REST middleware."""
    return "# Django REST middleware code would be generated here"

async def _generate_aspnet_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate ASP.NET middleware."""
    return "// ASP.NET middleware code would be generated here"

async def _generate_spring_boot_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate Spring Boot middleware."""
    return "// Spring Boot middleware code would be generated here"

async def _generate_generic_middleware(middleware_type: str, options: Dict[str, Any], deps: APIAgentDependencies) -> str:
    """Generate generic middleware."""
    return f"// Generic {middleware_type} middleware for {deps.framework_type}"

# Documentation generators
async def _generate_openapi_docs(endpoints: List[Dict[str, Any]], deps: APIAgentDependencies, include_examples: bool) -> str:
    """Generate OpenAPI documentation."""
    return "# OpenAPI documentation would be generated here"

async def _generate_postman_collection(endpoints: List[Dict[str, Any]], deps: APIAgentDependencies) -> str:
    """Generate Postman collection."""
    return "# Postman collection would be generated here"

async def _generate_insomnia_collection(endpoints: List[Dict[str, Any]], deps: APIAgentDependencies) -> str:
    """Generate Insomnia collection."""
    return "# Insomnia collection would be generated here"

async def _generate_markdown_docs(endpoints: List[Dict[str, Any]], deps: APIAgentDependencies, include_examples: bool) -> str:
    """Generate Markdown documentation."""
    return "# Markdown documentation would be generated here"

# Test generators
async def _generate_jest_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate Jest tests."""
    return "// Jest tests would be generated here"

async def _generate_pytest_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate pytest tests."""
    return "# pytest tests would be generated here"

async def _generate_mocha_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate Mocha tests."""
    return "// Mocha tests would be generated here"

async def _generate_xunit_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate xUnit tests."""
    return "// xUnit tests would be generated here"

async def _generate_junit_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate JUnit tests."""
    return "// JUnit tests would be generated here"

async def _generate_rspec_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate RSpec tests."""
    return "# RSpec tests would be generated here"

async def _generate_generic_tests(endpoint_name: str, test_types: List[str], framework: str, deps: APIAgentDependencies) -> str:
    """Generate generic tests."""
    return f"# Generic tests for {endpoint_name} using {deps.testing_framework}"

# Deployment configuration generators
async def _generate_dockerfile(deps: APIAgentDependencies) -> str:
    """Generate Dockerfile for API deployment."""
    return "# Dockerfile would be generated here"

async def _generate_k8s_manifests(deps: APIAgentDependencies) -> str:
    """Generate Kubernetes manifests."""
    return "# Kubernetes manifests would be generated here"

async def _generate_serverless_config(deps: APIAgentDependencies) -> str:
    """Generate serverless configuration."""
    return "# Serverless configuration would be generated here"