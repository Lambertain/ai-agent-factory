"""
Dependencies для Pattern Ericksonian Hypnosis Scriptwriter Agent
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PatternEricksonianHypnosisScriptwriterDependencies:
    """
    Зависимости для Pattern Ericksonian Hypnosis Scriptwriter Agent.
    """

    # Основные настройки
    api_key: str
    patternshift_project_path: str = ""

    # Имя агента для защиты от отсутствия знаний в RAG
    agent_name: str = "pattern_ericksonian_hypnosis_scriptwriter"

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "pattern-ericksonian-hypnosis",
        "hypnosis",
        "milton-model",
        "agent-knowledge",
        "pydantic-ai",
        "patternshift"
    ])
    knowledge_domain: str | None = "patternshift.com"
    archon_project_id: str | None = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Настройки гипнотических скриптов
    default_trance_depth: str = "medium"
    default_duration_minutes: int = 20
    safety_checks_enabled: bool = True
    metaphor_library_path: str = ""

    def __post_init__(self):
        """Инициализация конфигурации RAG."""
        if not self.knowledge_tags:
            self.knowledge_tags = [
                "pattern-ericksonian-hypnosis",
                "hypnosis",
                "agent-knowledge",
                "pydantic-ai"
            ]