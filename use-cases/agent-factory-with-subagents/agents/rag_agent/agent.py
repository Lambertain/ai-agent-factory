"""Main agent implementation for Semantic Search."""

from pydantic_ai import Agent, RunContext
from typing import Any

from .providers import get_llm_model
from .dependencies import RAGAgentDependencies
from .prompts import MAIN_SYSTEM_PROMPT
from .tools import semantic_search, hybrid_search
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)


# Create universal RAG agent with decorators
search_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=RAGAgentDependencies,
    system_prompt=MAIN_SYSTEM_PROMPT,
    agent_type="rag_agent",
    knowledge_tags=["rag", "semantic-search", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="rag.semantic-search.com",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Register agent in global registry
register_agent("rag_agent", search_agent, agent_type="rag_agent")

# Register RAG-specific tools
search_agent.tool(semantic_search)
search_agent.tool(hybrid_search)

# Collective work tools and knowledge search now added automatically via decorators
