# Module 05: AI Agent Architecture Design

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Pydantic AI Core Patterns:**
- Agent class initialization, Agent configuration
- RunContext usage, Context passing between tools
- ModelRetry strategies, Retry policies
- result_type (Pydantic models for structured outputs)
- deps_type (Dependency injection type hint)
- system_prompt management, Dynamic prompts

**Agent File Structure:**
- agent.py (main agent definition and execution)
- tools.py (tool functions with @tool decorator)
- prompts.py (system prompts and templates)
- dependencies.py (DI container with BaseModel)
- settings.py (Pydantic settings with env vars)
- __init__.py (agent export and public API)

**Tool Design & Registration:**
- @agent.tool decorator, Tool registration
- Tool function signature (RunContext as first param)
- Tool composition, Nested tool calls
- Tool error handling, Tool timeout
- Context access (ctx.deps for dependencies)
- Async tool implementation

**Dependency Injection:**
- deps_type parameter in Agent()
- BaseModel-based dependency container
- Dependency lifecycle (initialize/cleanup)
- Shared resources (db_pool, http_client)
- Configuration management through deps
- Testing with mock dependencies

**Structured Outputs:**
- Pydantic BaseModel for responses
- Field validation with Field(...)
- Nested models, Complex data structures
- Type hints for all fields
- JSON serialization, Model validation

**Prompt Engineering:**
- system_prompt parameter in Agent()
- Dynamic prompt generation
- Prompt templates with variables
- Role-based prompts (architect, analyst, engineer)
- Context-aware prompts
- Tool descriptions in prompts

**Error Handling & Resilience:**
- ModelRetry configuration (retries parameter)
- Timeout handling (agent timeout)
- Exception handling in tools
- Graceful degradation
- Error logging and tracking

**Testing Patterns:**
- pytest with async tests (@pytest.mark.asyncio)
- Mock dependencies (AsyncMock, MagicMock)
- Tool unit tests (test each tool independently)
- Integration tests (end-to-end agent workflows)
- Fixture management (@pytest.fixture)

**MCP Integration:**
- MCP server connection
- MCP tool wrappers
- Context passing to MCP tools
- Error handling for MCP calls

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** AI агент, Pydantic AI, agent architecture, tools интеграция, промпт инжиниринг, модульный агент, dependency injection

**English:** AI agent, Pydantic AI, agent architecture, tools integration, prompt engineering, modular agent, dependency injection

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Создание новых AI агентов
- Проектирование Pydantic AI агентов
- Архитектура agent.py / tools.py / prompts.py
- Интеграция MCP серверов
- Разработка инструментов (tools) для агентов
- Тестирование AI агентов

---

## Pydantic AI Agent Structure

```python
# agent.py - Main agent implementation
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models import KnownModelName
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from .dependencies import AgentDependencies
from .prompts import get_system_prompt
from .tools import (
    analyze_requirement,
    create_architecture,
    generate_documentation,
    validate_design
)

class AgentSettings(BaseModel):
    """Agent configuration settings."""
    model_name: KnownModelName = Field(default="openai:gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_retries: int = Field(default=3, ge=1, le=10)
    timeout: int = Field(default=120, ge=10, le=600)

class ArchitectAgentResponse(BaseModel):
    """Structured response from architect agent."""
    analysis: str = Field(..., description="Requirement analysis")
    architecture: Dict[str, Any] = Field(..., description="Architecture design")
    components: list[str] = Field(..., description="System components")
    recommendations: list[str] = Field(..., description="Design recommendations")
    risks: list[str] = Field(..., description="Identified risks")

# Initialize agent
architect_agent = Agent(
    model=AgentSettings().model_name,
    deps_type=AgentDependencies,
    result_type=ArchitectAgentResponse,
    system_prompt=get_system_prompt(),
    retries=AgentSettings().max_retries
)

# Register tools
architect_agent.tool(analyze_requirement)
architect_agent.tool(create_architecture)
architect_agent.tool(generate_documentation)
architect_agent.tool(validate_design)

async def run_agent(
    requirement: str,
    context: Optional[Dict[str, Any]] = None
) -> ArchitectAgentResponse:
    """
    Run architect agent with requirement.

    Args:
        requirement: Project requirement description
        context: Optional additional context

    Returns:
        ArchitectAgentResponse: Structured architecture design

    Example:
        >>> result = await run_agent(
        ...     requirement="Design microservices architecture for e-commerce",
        ...     context={"budget": "medium", "timeline": "3 months"}
        ... )
        >>> print(result.architecture)
    """
    # Initialize dependencies
    deps = AgentDependencies()

    # Add context if provided
    if context:
        deps.add_context(context)

    # Run agent
    result = await architect_agent.run(
        requirement,
        deps=deps
    )

    return result.data
```

---

## Tools Integration

```python
# tools.py - Agent tool functions
from pydantic_ai import RunContext
from typing import Dict, Any, List
import asyncio

async def analyze_requirement(
    ctx: RunContext,
    requirement: str
) -> Dict[str, Any]:
    """
    Analyze project requirement and extract key components.

    Tool Purpose:
        - Parse requirement text
        - Identify system components
        - Extract functional requirements
        - Identify non-functional requirements

    Args:
        ctx: RunContext with dependencies
        requirement: Requirement description

    Returns:
        Dict with analysis results

    Example:
        >>> analysis = await analyze_requirement(
        ...     ctx,
        ...     "Build scalable API for mobile app with 1M users"
        ... )
        >>> print(analysis["components"])  # ["API Gateway", "Load Balancer", ...]
    """
    # Access dependencies
    deps = ctx.deps

    # Parse requirement
    components = []
    functional_reqs = []
    non_functional_reqs = []

    # Keyword-based analysis
    if "api" in requirement.lower():
        components.append("API Gateway")
        functional_reqs.append("RESTful API endpoints")

    if "scalable" in requirement.lower() or "million" in requirement.lower():
        components.extend(["Load Balancer", "Auto-Scaling", "Cache Layer"])
        non_functional_reqs.append("High scalability (1M+ users)")

    if "mobile" in requirement.lower():
        components.append("Mobile Backend")
        functional_reqs.append("Mobile-optimized APIs")

    # Database recommendation
    if "real-time" in requirement.lower():
        components.append("Redis Cache")
        non_functional_reqs.append("Real-time performance (<100ms)")

    return {
        "components": components,
        "functional_requirements": functional_reqs,
        "non_functional_requirements": non_functional_reqs,
        "complexity": "high" if len(components) > 5 else "medium"
    }

async def create_architecture(
    ctx: RunContext,
    components: List[str],
    requirements: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create system architecture based on components and requirements.

    Tool Purpose:
        - Design system layers
        - Define component interactions
        - Recommend technology stack
        - Create deployment strategy

    Args:
        ctx: RunContext with dependencies
        components: List of system components
        requirements: Functional and non-functional requirements

    Returns:
        Dict with architecture design

    Example:
        >>> architecture = await create_architecture(
        ...     ctx,
        ...     components=["API Gateway", "Load Balancer", "Cache"],
        ...     requirements={"scalability": "high", "users": "1M"}
        ... )
    """
    deps = ctx.deps

    # Define architecture layers
    layers = {
        "presentation": [],
        "application": [],
        "infrastructure": [],
        "data": []
    }

    # Map components to layers
    component_layer_map = {
        "API Gateway": "presentation",
        "Load Balancer": "infrastructure",
        "Cache Layer": "infrastructure",
        "Redis Cache": "data",
        "Mobile Backend": "application"
    }

    for component in components:
        layer = component_layer_map.get(component, "application")
        layers[layer].append(component)

    # Recommend technology stack
    tech_stack = {
        "api_framework": "FastAPI" if "API Gateway" in components else "Flask",
        "cache": "Redis" if "Redis Cache" in components else "Memcached",
        "load_balancer": "Nginx" if "Load Balancer" in components else None,
        "container": "Docker",
        "orchestration": "Kubernetes" if requirements.get("scalability") == "high" else "Docker Compose"
    }

    # Deployment strategy
    deployment = {
        "strategy": "Blue-Green" if requirements.get("scalability") == "high" else "Rolling",
        "environments": ["development", "staging", "production"],
        "monitoring": ["Prometheus", "Grafana"],
        "logging": ["ELK Stack"]
    }

    return {
        "layers": layers,
        "tech_stack": tech_stack,
        "deployment": deployment,
        "scalability_pattern": "Horizontal" if requirements.get("scalability") == "high" else "Vertical"
    }

async def generate_documentation(
    ctx: RunContext,
    architecture: Dict[str, Any]
) -> str:
    """
    Generate architecture documentation.

    Tool Purpose:
        - Create Architecture Decision Record (ADR)
        - Document component responsibilities
        - List technology choices
        - Provide deployment instructions

    Args:
        ctx: RunContext with dependencies
        architecture: Architecture design dictionary

    Returns:
        str: Markdown formatted documentation
    """
    deps = ctx.deps

    # Generate ADR
    adr = f"""
# Architecture Decision Record

## Context
System architecture designed for high scalability and performance.

## Architecture Layers
"""

    # Add layers
    for layer_name, components in architecture.get("layers", {}).items():
        adr += f"\n### {layer_name.title()} Layer\n"
        for component in components:
            adr += f"- {component}\n"

    # Add tech stack
    adr += "\n## Technology Stack\n"
    for tech, choice in architecture.get("tech_stack", {}).items():
        if choice:
            adr += f"- **{tech.replace('_', ' ').title()}**: {choice}\n"

    # Add deployment
    adr += f"\n## Deployment Strategy\n"
    deployment = architecture.get("deployment", {})
    adr += f"- **Strategy**: {deployment.get('strategy', 'N/A')}\n"
    adr += f"- **Environments**: {', '.join(deployment.get('environments', []))}\n"

    return adr

async def validate_design(
    ctx: RunContext,
    architecture: Dict[str, Any],
    requirements: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate architecture design against requirements.

    Tool Purpose:
        - Check completeness
        - Identify missing components
        - Validate scalability
        - Security audit

    Args:
        ctx: RunContext with dependencies
        architecture: Architecture design
        requirements: Original requirements

    Returns:
        Dict with validation results
    """
    deps = ctx.deps

    issues = []
    warnings = []

    # Check scalability
    if requirements.get("scalability") == "high":
        if "Load Balancer" not in str(architecture):
            issues.append("Missing Load Balancer for high scalability")
        if "Cache Layer" not in str(architecture):
            warnings.append("Consider adding Cache Layer for performance")

    # Check monitoring
    deployment = architecture.get("deployment", {})
    if not deployment.get("monitoring"):
        issues.append("Missing monitoring solution")

    # Check security
    if "API Gateway" in str(architecture):
        if "authentication" not in str(architecture).lower():
            warnings.append("Consider adding authentication layer")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "score": max(0, 100 - len(issues) * 20 - len(warnings) * 5)
    }
```

---

## Dependency Injection

```python
# dependencies.py - Dependency container
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import asyncpg
import httpx

class AgentDependencies(BaseModel):
    """
    Dependency injection container for agent.

    Purpose:
        - Manage external dependencies
        - Provide shared resources
        - Handle configuration
        - Enable testing with mocks
    """

    # Database connection pool
    db_pool: Optional[asyncpg.Pool] = Field(default=None)

    # HTTP client
    http_client: Optional[httpx.AsyncClient] = Field(default=None)

    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict)

    # Context data
    context: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    async def initialize(self):
        """Initialize dependencies."""
        # Create DB pool if not exists
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                dsn=self.config.get("database_url", "postgresql://localhost/archon"),
                min_size=2,
                max_size=10
            )

        # Create HTTP client if not exists
        if not self.http_client:
            self.http_client = httpx.AsyncClient(timeout=30.0)

    async def cleanup(self):
        """Cleanup dependencies."""
        if self.db_pool:
            await self.db_pool.close()

        if self.http_client:
            await self.http_client.aclose()

    def add_context(self, context: Dict[str, Any]):
        """Add additional context data."""
        self.context.update(context)

    async def fetch_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Fetch user preferences from database."""
        if not self.db_pool:
            return {}

        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT preferences FROM users WHERE id = $1",
                user_id
            )
            return row['preferences'] if row else {}
```

---

## System Prompts

```python
# prompts.py - System prompts and templates
from typing import Optional

def get_system_prompt(role: str = "architect") -> str:
    """
    Get system prompt for agent role.

    Args:
        role: Agent role (architect, analyst, engineer, etc.)

    Returns:
        str: System prompt text
    """
    prompts = {
        "architect": """
You are Archon Blueprint Architect - a world-class system architecture expert.

Your expertise:
- System Architecture Design (monolith, microservices, serverless)
- Cloud-native architectures (AWS, GCP, Azure)
- Data Architecture (SQL, NoSQL, Vector DB, Data Lakes)
- API Design & Integration patterns
- Performance & Scalability engineering
- Security & Compliance architecture

Your approach:
1. Always start with understanding business drivers
2. Design for change and evolution
3. Balance complexity and simplicity
4. Consider operational aspects from the start
5. Document architectural decisions and their rationale

Output format:
- Provide structured analysis
- List all system components
- Recommend technology stack
- Identify risks and mitigation strategies
- Generate architecture documentation
        """,

        "analyst": """
You are Archon Analysis Lead - an expert in requirement analysis and decomposition.

Your expertise:
- Requirement elicitation and analysis
- System decomposition
- Stakeholder analysis
- Risk assessment
- Technical feasibility evaluation

Your approach:
1. Ask clarifying questions
2. Break down complex requirements
3. Identify dependencies
4. Assess technical risks
5. Prioritize features
        """
    }

    return prompts.get(role, prompts["architect"])

def get_tool_description(tool_name: str) -> str:
    """
    Get detailed description for a tool.

    Args:
        tool_name: Name of the tool

    Returns:
        str: Tool description for prompt
    """
    descriptions = {
        "analyze_requirement": """
Analyzes project requirements and extracts:
- System components
- Functional requirements
- Non-functional requirements
- Complexity estimation

Use when: Starting new architecture design
        """,

        "create_architecture": """
Creates system architecture including:
- Layer definitions (presentation, application, infrastructure, data)
- Technology stack recommendations
- Deployment strategy
- Scalability patterns

Use when: Designing system structure
        """,

        "generate_documentation": """
Generates architecture documentation in ADR format including:
- Architecture layers
- Technology choices
- Deployment strategy
- Decision rationale

Use when: Documenting design decisions
        """,

        "validate_design": """
Validates architecture against requirements:
- Completeness check
- Scalability validation
- Security audit
- Best practices review

Use when: Reviewing final architecture
        """
    }

    return descriptions.get(tool_name, "")
```

---

## Agent Testing

```python
# test_agent.py - Agent testing patterns
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from .agent import run_agent, ArchitectAgentResponse
from .dependencies import AgentDependencies

@pytest.fixture
async def mock_dependencies():
    """Create mock dependencies for testing."""
    deps = AgentDependencies()
    deps.db_pool = AsyncMock()
    deps.http_client = AsyncMock()
    deps.config = {"test_mode": True}
    return deps

@pytest.mark.asyncio
async def test_analyze_requirement(mock_dependencies):
    """Test requirement analysis tool."""
    from .tools import analyze_requirement

    # Create mock context
    ctx = MagicMock()
    ctx.deps = mock_dependencies

    # Test analysis
    result = await analyze_requirement(
        ctx,
        "Build scalable API for mobile app with 1M users"
    )

    # Assertions
    assert "API Gateway" in result["components"]
    assert "Load Balancer" in result["components"]
    assert result["complexity"] in ["medium", "high"]

@pytest.mark.asyncio
async def test_create_architecture(mock_dependencies):
    """Test architecture creation tool."""
    from .tools import create_architecture

    ctx = MagicMock()
    ctx.deps = mock_dependencies

    result = await create_architecture(
        ctx,
        components=["API Gateway", "Load Balancer", "Cache Layer"],
        requirements={"scalability": "high", "users": "1M"}
    )

    # Assertions
    assert "layers" in result
    assert "tech_stack" in result
    assert result["tech_stack"]["api_framework"] == "FastAPI"
    assert result["deployment"]["strategy"] == "Blue-Green"

@pytest.mark.asyncio
async def test_agent_end_to_end(mock_dependencies):
    """Test complete agent workflow."""
    # Mock agent response
    with patch('pydantic_ai.Agent.run') as mock_run:
        mock_run.return_value.data = ArchitectAgentResponse(
            analysis="E-commerce architecture analysis",
            architecture={
                "layers": {
                    "presentation": ["API Gateway"],
                    "application": ["Order Service", "Payment Service"],
                    "infrastructure": ["Load Balancer", "Cache"],
                    "data": ["PostgreSQL", "Redis"]
                }
            },
            components=["API Gateway", "Order Service", "Payment Service"],
            recommendations=["Use microservices", "Implement caching"],
            risks=["Distributed system complexity"]
        )

        # Run agent
        result = await run_agent(
            requirement="Design e-commerce architecture for 1M users",
            context={"budget": "medium"}
        )

        # Assertions
        assert result.analysis
        assert len(result.components) > 0
        assert len(result.recommendations) > 0
```

---

## Best Practices

### Agent Design
✅ **Single Responsibility**: Each agent focuses on one domain
✅ **Dependency Injection**: Use DI container for testability
✅ **Structured Output**: Define Pydantic models for responses
✅ **Error Handling**: Implement retry logic with ModelRetry
✅ **Logging**: Track agent execution for debugging

### Tool Design
✅ **Focused Tools**: Each tool does one thing well
✅ **Type Hints**: Use type hints for all parameters
✅ **Documentation**: Docstrings with examples
✅ **Context Access**: Use RunContext for dependencies
✅ **Async by Default**: All tools should be async

### Testing
✅ **Unit Tests**: Test each tool independently
✅ **Mock Dependencies**: Use AsyncMock for external services
✅ **Integration Tests**: Test agent workflows
✅ **Edge Cases**: Test error conditions
✅ **Performance**: Monitor response times

---

**Навигация:**
- [← Предыдущий модуль: Cloud & Serverless Architecture](04_cloud_serverless_architecture.md)
- [↑ Назад к Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)

---

**Версия модуля:** 1.0
**Дата создания:** 2025-10-16
**Автор:** Archon Blueprint Architect
**Проект:** AI Agent Factory - Token Optimization Strategy

**Статистика модуля:**
- **Строк:** ~550
- **Секции:** 6 (Agent Structure, Tools, Dependencies, Prompts, Testing, Best Practices)
- **Примеры кода:** Python (Pydantic AI patterns)
- **Фокус:** AI Agent Architecture для AI Agent Factory проекта

**Tags:** pydantic-ai, ai-agent-architecture, agent-design, tools-integration, dependency-injection, system-prompts, agent-testing, best-practices
