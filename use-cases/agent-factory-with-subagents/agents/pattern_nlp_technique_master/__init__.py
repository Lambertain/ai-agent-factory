"""
Pattern NLP Technique Master Agent Package

Специализированный агент для создания модульных НЛП-техник трансформации.
Поддержка CBT, DBT, ACT и классических НЛП паттернов.
"""

from .agent import (
    agent,
    run_pattern_nlp_technique_master,
    TechniqueCreationRequest,
    TechniqueAnalysisRequest,
    ModuleGenerationRequest,
    create_cbt_technique_deps,
    create_dbt_technique_deps,
    create_act_technique_deps,
    create_classic_nlp_deps,
    create_mindfulness_deps
)

from .dependencies import (
    PatternNLPTechniqueMasterDependencies,
    create_technique_dependencies,
    create_cbt_dependencies,
    create_dbt_dependencies,
    create_act_dependencies,
    create_classic_nlp_dependencies,
    create_mindfulness_dependencies,
    NLPTechniqueType,
    TherapyModality,
    ProblemArea,
    RepresentationalSystem,
    DifficultyLevel,
    TechniqueFormat
)

from .tools import (
    search_agent_knowledge,
    create_nlp_technique,
    adapt_technique_vak,
    assess_technique_safety,
    generate_technique_variants,
    TechniqueRequest,
    TechniqueModule,
    VAKAdaptation,
    SafetyAssessment
)

from .prompts import (
    get_system_prompt,
    get_technique_creation_prompt,
    get_vak_adaptation_prompt
)

from .settings import (
    load_settings,
    get_settings
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"

__all__ = [
    # Main agent
    'agent',
    'run_pattern_nlp_technique_master',

    # Request models
    'TechniqueCreationRequest',
    'TechniqueAnalysisRequest',
    'ModuleGenerationRequest',

    # Dependencies
    'PatternNLPTechniqueMasterDependencies',
    'create_technique_dependencies',
    'create_cbt_dependencies',
    'create_dbt_dependencies',
    'create_act_dependencies',
    'create_classic_nlp_dependencies',
    'create_mindfulness_dependencies',

    # Helper functions
    'create_cbt_technique_deps',
    'create_dbt_technique_deps',
    'create_act_technique_deps',
    'create_classic_nlp_deps',
    'create_mindfulness_deps',

    # Enums
    'NLPTechniqueType',
    'TherapyModality',
    'ProblemArea',
    'RepresentationalSystem',
    'DifficultyLevel',
    'TechniqueFormat',

    # Tools
    'search_agent_knowledge',
    'create_nlp_technique',
    'adapt_technique_vak',
    'assess_technique_safety',
    'generate_technique_variants',

    # Tool models
    'TechniqueRequest',
    'TechniqueModule',
    'VAKAdaptation',
    'SafetyAssessment',

    # Prompts
    'get_system_prompt',
    'get_technique_creation_prompt',
    'get_vak_adaptation_prompt',

    # Settings
    'load_settings',
    'get_settings'
]