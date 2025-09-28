"""
Pattern Cultural Adaptation Expert Agent Package.

Специализированный агент для культурной адаптации психологических интервенций.
Поддержка украинской, польской, английской и других культур.
"""

from .agent import (
    agent,
    run_pattern_cultural_adaptation_expert,
    analyze_content_for_culture,
    adapt_content_for_culture,
    validate_cultural_content
)

from .dependencies import (
    PatternCulturalAdaptationExpertDependencies,
    create_cultural_adaptation_dependencies,
    CultureType,
    ReligiousContext,
    CommunicationStyle,
    ValueSystem,
    CulturalProfile,
    AdaptationSettings,
    UKRAINIAN_CONFIG,
    POLISH_CONFIG,
    ENGLISH_CONFIG,
    UNIVERSAL_CONFIG
)

from .tools import (
    search_agent_knowledge,
    analyze_cultural_context,
    adapt_content_culturally,
    validate_cultural_appropriateness,
    adapt_metaphors_culturally,
    generate_cultural_examples,
    CulturalAnalysisRequest,
    AdaptationRequest,
    CulturalValidationRequest,
    MetaphorAdaptationRequest
)

from .prompts import (
    get_system_prompt,
    get_analysis_prompt,
    get_adaptation_prompt,
    get_validation_prompt,
    get_metaphor_adaptation_prompt,
    get_cultural_examples_prompt
)

from .settings import (
    load_settings,
    get_settings,
    PatternCulturalAdaptationExpertSettings,
    configure_for_environment
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"

__all__ = [
    # Main agent
    'agent',
    'run_pattern_cultural_adaptation_expert',

    # Convenience functions
    'analyze_content_for_culture',
    'adapt_content_for_culture',
    'validate_cultural_content',

    # Dependencies
    'PatternCulturalAdaptationExpertDependencies',
    'create_cultural_adaptation_dependencies',

    # Enums and types
    'CultureType',
    'ReligiousContext',
    'CommunicationStyle',
    'ValueSystem',
    'CulturalProfile',
    'AdaptationSettings',

    # Predefined configs
    'UKRAINIAN_CONFIG',
    'POLISH_CONFIG',
    'ENGLISH_CONFIG',
    'UNIVERSAL_CONFIG',

    # Tools
    'search_agent_knowledge',
    'analyze_cultural_context',
    'adapt_content_culturally',
    'validate_cultural_appropriateness',
    'adapt_metaphors_culturally',
    'generate_cultural_examples',

    # Tool models
    'CulturalAnalysisRequest',
    'AdaptationRequest',
    'CulturalValidationRequest',
    'MetaphorAdaptationRequest',

    # Prompts
    'get_system_prompt',
    'get_analysis_prompt',
    'get_adaptation_prompt',
    'get_validation_prompt',
    'get_metaphor_adaptation_prompt',
    'get_cultural_examples_prompt',

    # Settings
    'load_settings',
    'get_settings',
    'PatternCulturalAdaptationExpertSettings',
    'configure_for_environment'
]