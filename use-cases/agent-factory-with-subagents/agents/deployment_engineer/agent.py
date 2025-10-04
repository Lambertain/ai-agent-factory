"""
Deployment Engineer Agent - специалист по DevOps, CI/CD и автоматизации развертывания.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import DeploymentEngineerDependencies
from .settings import load_settings
from .tools import register_tools
from .prompts import get_system_prompt
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)


# Create universal deployment engineer agent with decorators
deployment_engineer_agent = create_universal_pydantic_agent(
    model=load_settings().llm_model,
    deps_type=DeploymentEngineerDependencies,
    system_prompt=get_system_prompt(),
    agent_type="deployment_engineer",
    knowledge_tags=["deployment", "devops", "ci-cd", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="devops.deployment.com",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Register agent in global registry
register_agent("deployment_engineer", deployment_engineer_agent, agent_type="deployment_engineer")

# Регистрация deployment-specific инструментов
register_tools(deployment_engineer_agent)

# Collective work tools and knowledge search now added automatically via decorators


async def run_deployment_engineer_task(
    user_message: str,
    deps: DeploymentEngineerDependencies
) -> str:
    """
    Запустить Deployment Engineer агента для выполнения задачи.

    Args:
        user_message: Задача от пользователя
        deps: Зависимости агента

    Returns:
        Результат выполнения задачи
    """
    result = await deployment_engineer_agent.run(user_message, deps=deps)
    return result.data
