"""
Psychology Content Orchestrator Agent
Универсальный агент для координации создания психологического контента
"""

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import Model
from .dependencies import RAGConfig, get_rag_client
from ..common import check_pm_switch
from .tools import search_agent_knowledge, coordinate_content_creation, analyze_target_audience
from .prompts import get_orchestrator_prompt
from .settings import PsychologyContentSettings
from typing import Any, Dict

psychology_orchestrator = Agent(
    model='openai:gpt-4o',
    deps_type=RAGConfig,
    result_type=str,
    system_prompt=get_orchestrator_prompt,
    tools=[
        search_agent_knowledge,
        coordinate_content_creation,
        analyze_target_audience
    ]
)

@psychology_orchestrator.system_prompt
def system_prompt(ctx: RunContext[RAGConfig]) -> str:
    """Системный промпт для координатора психологического контента"""
    return get_orchestrator_prompt(
        content_type=ctx.deps.content_type,
        target_domain=ctx.deps.target_domain,
        expertise_level=ctx.deps.expertise_level
    )

async def coordinate_psychology_content(
    request: str,
    content_type: str = "therapeutic",
    target_domain: str = "general",
    expertise_level: str = "professional",
    **kwargs
) -> Dict[str, Any]:
    """
    Основная функция координации психологического контента

    Args:
        request: Запрос на создание контента
        content_type: Тип контента (therapeutic, educational, assessment)
        target_domain: Целевая область (anxiety, depression, relationships, etc.)
        expertise_level: Уровень экспертизы (beginner, intermediate, professional)

    Returns:
        Координированный план создания психологического контента
    """
    settings = PsychologyContentSettings(
        content_type=content_type,
        target_domain=target_domain,
        expertise_level=expertise_level
    )

    rag_config = RAGConfig(
        search_tags=["psychology", "therapy", content_type, target_domain],
        content_type=content_type,
        target_domain=target_domain,
        expertise_level=expertise_level
    )

    result = await psychology_orchestrator.run(
        request,
        deps=rag_config
    )

    return {
        "success": True,
        "orchestration_plan": result.data,
        "settings": settings.dict(),
        "message": "Psychology content orchestration plan generated successfully"
    }

if __name__ == "__main__":
    import asyncio

    async def test_orchestrator():
        result = await coordinate_psychology_content(
            request="Создать комплексную программу терапии тревожности для подростков",
            content_type="therapeutic",
            target_domain="anxiety",
            expertise_level="professional"
        )
        print("Результат координации:", result)

    asyncio.run(test_orchestrator())