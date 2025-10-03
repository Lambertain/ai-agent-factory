# -*- coding: utf-8 -*-
"""
Настройки Pattern Orchestrator Agent.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Dict
import os


class PatternOrchestratorSettings(BaseSettings):
    """Настройки Pattern Orchestrator Agent."""

    # LLM настройки
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель LLM для агента"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Base URL для LLM API"
    )
    llm_api_key: str = Field(
        default="",
        description="API ключ для LLM (берется из env)"
    )

    # PatternShift пути
    patternshift_project_path: str = Field(
        default="D:\\Automation\\Development\\projects\\PatternShift",
        description="Путь к проекту PatternShift"
    )

    # 17 Pattern Agents для координации
    pattern_agents: List[str] = Field(
        default=[
            # Phase 1: Content Creation (Days 1-14)
            "pattern_nlp_technique_master",
            "pattern_ericksonian_hypnosis_scriptwriter",
            "pattern_exercise_architect",
            "pattern_microhabit_designer",
            "pattern_metaphor_weaver",
            "pattern_gamification_architect",

            # Phase 2: Integration & Polish (Days 15-21)
            "pattern_integration_synthesizer",
            "pattern_feedback_orchestrator",
            "pattern_progress_narrator",
            "pattern_transition_craftsman",

            # Phase 3: Safety & Science (Days 22-24)
            "pattern_safety_protocol",
            "pattern_scientific_validator",

            # Phase 4: Multiplier Adaptation (Days 25-35)
            "pattern_gender_adaptation",
            "pattern_age_adaptation",
            "pattern_vak_adaptation",
            "pattern_cultural_adaptation",

            # Phase 5: Final Assembly (Days 36-42)
            "pattern_test_architect"
        ],
        description="Список всех Pattern агентов для координации"
    )

    # 5-уровневая система деградации контента
    degradation_levels: Dict[str, dict] = Field(
        default={
            "program": {
                "duration_minutes": 45,
                "modules": "all",
                "description": "Полная программа трансформации"
            },
            "phase": {
                "duration_minutes": 25,
                "modules": "key",
                "description": "Ключевая фаза программы"
            },
            "day": {
                "duration_minutes": 15,
                "modules": "daily",
                "description": "Дневная практика"
            },
            "session": {
                "duration_minutes": 5,
                "modules": "express",
                "description": "Быстрая сессия"
            },
            "emergency": {
                "duration_minutes": 1,
                "modules": "critical",
                "description": "Экстренная помощь"
            }
        },
        description="5 уровней деградации контента"
    )

    # Психографические измерения
    psychographic_dimensions: Dict[str, List[str]] = Field(
        default={
            "gender": ["masculine", "feminine", "neutral"],
            "age": ["teens", "young_adults", "early_middle_age", "middle_age", "seniors"],
            "vak": ["visual", "audial", "kinesthetic"],
            "culture": ["individualistic", "collectivistic", "balanced"]
        },
        description="Психографические измерения для маршрутизации"
    )

    # Расчет множителей
    total_base_modules: int = Field(
        default=460,
        description="Базовое количество модулей после Phase 3"
    )

    gender_multiplier: int = Field(default=3, description="Множитель гендерной адаптации")
    age_multiplier: int = Field(default=5, description="Множитель возрастной адаптации")
    vak_multiplier: int = Field(default=3, description="Множитель VAK адаптации")

    # Итоговое количество модулей
    @property
    def total_adapted_modules(self) -> int:
        """Общее количество адаптированных модулей."""
        return (
            self.total_base_modules *
            self.gender_multiplier *
            self.age_multiplier *
            self.vak_multiplier
        )

    # Universal Agents для делегирования
    universal_agents_for_engine: List[str] = Field(
        default=[
            "blueprint_architect",
            "implementation_engineer",
            "api_development",
            "typescript_architecture",
            "prisma_database",
            "queue_worker",
            "quality_guardian"
        ],
        description="Universal агенты для создания движка"
    )

    # Workflow stages
    workflow_stages: Dict[str, dict] = Field(
        default={
            "phase_1": {
                "name": "Content Creation",
                "days": "1-14",
                "agents": 6,
                "output": "~460 базовых модулей"
            },
            "phase_2": {
                "name": "Integration & Polish",
                "days": "15-21",
                "agents": 4,
                "output": "Интегрированные программы"
            },
            "phase_3": {
                "name": "Safety & Science",
                "days": "22-24",
                "agents": 2,
                "output": "Валидированные модули"
            },
            "phase_4": {
                "name": "Multiplier Adaptation",
                "days": "25-35",
                "agents": 4,
                "output": "~20,700 адаптированных модулей"
            },
            "phase_5": {
                "name": "Final Assembly",
                "days": "36-42+",
                "agents": 2,
                "output": "ENGINE_SPEC.json + Движок"
            }
        },
        description="Стадии workflow"
    )

    # RAG и база знаний
    knowledge_tags: List[str] = Field(
        default=[
            "pattern-orchestrator",
            "system-architecture",
            "agent-coordination",
            "content-degradation",
            "psychographic-routing",
            "pydantic-ai",
            "patternshift"
        ],
        description="Теги для поиска знаний"
    )

    knowledge_domain: str = Field(
        default="",
        description="Домен знаний агента"
    )

    # Emergency режим
    enable_emergency_mode: bool = Field(
        default=True,
        description="Включить emergency режим (1 мин контент)"
    )

    emergency_techniques: List[str] = Field(
        default=[
            "grounding_5_4_3_2_1",
            "breathing_4_4_4",
            "power_pose_affirmation",
            "anchor_activation",
            "safe_place_visualization"
        ],
        description="Экстренные техники для 1-минутного контента"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_settings() -> PatternOrchestratorSettings:
    """
    Загрузить настройки агента из env файла.

    Returns:
        Объект настроек
    """
    settings = PatternOrchestratorSettings()

    # API ключ из переменной окружения
    if not settings.llm_api_key:
        settings.llm_api_key = os.getenv("DASHSCOPE_API_KEY", "")

    return settings


def get_llm_model():
    """
    Получить настроенную модель LLM.

    Returns:
        Настроенная модель для Pydantic AI
    """
    from pydantic_ai.models.openai import OpenAIModel

    settings = load_settings()

    return OpenAIModel(
        settings.llm_model,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
