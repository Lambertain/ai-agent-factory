"""
Настройки для Pattern Scientific Validator Agent.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LLMSettings(BaseModel):
    """Настройки LLM для агента."""

    model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Модель Claude для валидации"
    )
    temperature: float = Field(
        default=0.2,
        description="Температура для точных научных оценок"
    )
    max_tokens: int = Field(
        default=8000,
        description="Максимальное количество токенов для ответа"
    )


class AgentSettings(BaseModel):
    """Настройки агента."""

    llm: LLMSettings = Field(default_factory=LLMSettings)
    agent_name: str = "Pattern Scientific Validator"
    agent_version: str = "1.0.0"

    # RAG настройки
    use_archon_rag: bool = True
    archon_match_count: int = 5

    # Настройки валидации
    minimum_evidence_level: str = "expert_opinion"  # Минимальный уровень для одобрения
    require_safety_check: bool = True
    require_ethical_review: bool = True

    # Настройки отчетности
    include_limitations: bool = True
    include_research_citations: bool = True
    verbose_reports: bool = True


__all__ = ["LLMSettings", "AgentSettings"]
