"""
Pattern Metaphor Weaver Agent
"""

import logging
from pydantic_ai import Agent
from .settings import get_llm_model
from .dependencies import PatternMetaphorWeaverDependencies
from .prompts import get_system_prompt
from .tools import *

try:
    from ..common.pydantic_ai_decorators import create_universal_pydantic_agent
    HAS_DECORATORS = True
except ImportError:
    HAS_DECORATORS = False

logger = logging.getLogger(__name__)

if HAS_DECORATORS:
    agent = create_universal_pydantic_agent(
        model=get_llm_model(),
        deps_type=PatternMetaphorWeaverDependencies,
        system_prompt=get_system_prompt,
        agent_type="pattern_metaphor_weaver",
        knowledge_tags=["pattern-metaphor-weaver", "therapeutic-metaphors", "agent-knowledge", "patternshift"],
        with_collective_tools=True,
        with_knowledge_tool=True
    )
else:
    agent = Agent(
        model=get_llm_model(),
        deps_type=PatternMetaphorWeaverDependencies,
        system_prompt=get_system_prompt
    )

agent.tool(create_therapeutic_metaphor)
agent.tool(adapt_metaphor_culturally)
agent.tool(create_isomorphic_mapping)
agent.tool(generate_story_structure)
agent.tool(create_metaphor_seed)


async def run_pattern_metaphor_weaver(
    user_message: str,
    api_key: str,
    patternshift_project_path: str = "",
    **kwargs
) -> str:
    deps = PatternMetaphorWeaverDependencies(
        api_key=api_key,
        patternshift_project_path=patternshift_project_path,
        **kwargs
    )

    try:
        result = await agent.run(user_message, deps=deps)
        return result.data
    except Exception as e:
        return f"Ошибка: {e}"


__all__ = ["agent", "run_pattern_metaphor_weaver"]
