"""
Deployment Engineer Agent - специалист по DevOps, CI/CD и автоматизации развертывания.
"""

from pydantic_ai import Agent, RunContext
from .dependencies import DeploymentEngineerDependencies
from .settings import load_settings
from .tools import register_tools
from .prompts import get_system_prompt


def create_deployment_engineer_agent():
    """Создать агента Deployment Engineer."""
    settings = load_settings()

    agent = Agent(
        model=settings.llm_model,
        deps_type=DeploymentEngineerDependencies,
        system_prompt=get_system_prompt()
    )

    # Регистрация инструментов
    register_tools(agent)

    return agent


# Создание глобального экземпляра агента
deployment_engineer_agent = create_deployment_engineer_agent()


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
