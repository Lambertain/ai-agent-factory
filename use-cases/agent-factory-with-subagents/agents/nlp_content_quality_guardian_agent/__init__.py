"""
NLP Content Quality Guardian Agent - Universal Content Validation System

Мощный агент для валидации качества NLP контента и программ трансформации с использованием
методологии PatternShift 2.0, строгих стандартов безопасности и этических принципов.
Поддерживает работу в любых доменах: психология, астрология, таро, нумерология.

Author: Implementation Engineer
Version: 1.0.0
"""

from .agent import (
    create_nlp_quality_guardian_agent,
    get_nlp_quality_guardian_agent,
    validate_content_quality,
    validate_test_quality,
    validate_transformation_program,
    validate_nlp_technique_safety,
    batch_validate_content,
    get_quality_recommendations,
    quick_safety_check
)

from .dependencies import (
    NLPQualityGuardianDependencies,
    create_psychology_quality_guardian_dependencies,
    create_universal_quality_guardian_dependencies,
    create_test_quality_guardian_dependencies,
    create_nlp_technique_quality_guardian_dependencies,
    ValidationDomain,
    ContentType,
    QualityLevel,
    ValidationAspect,
    CriticalFlag,
    ValidationResult,
    ValidationCriteria
)

from .settings import (
    load_settings,
    NLPQualityGuardianSettings,
    get_domain_specific_settings,
    create_validation_settings_for_domain
)

from .providers import (
    create_model_manager,
    QualityGuardianModelManager,
    ValidationTaskType,
    get_validation_model,
    get_deep_analysis_model,
    get_safety_check_model,
    get_report_generation_model,
    get_knowledge_search_model
)

from .tools import (
    search_quality_knowledge,
    validate_content_structure,
    check_safety_and_ethics,
    validate_nlp_techniques,
    generate_quality_report,
    break_down_validation_tasks,
    delegate_validation_task
)

from .prompts import (
    create_adaptive_system_prompt,
    create_domain_specific_prompt,
    create_content_type_prompt,
    create_expert_validation_prompt
)

__version__ = "1.0.0"
__author__ = "Implementation Engineer"

__all__ = [
    # Core agent functions
    "create_nlp_quality_guardian_agent",
    "get_nlp_quality_guardian_agent",
    "validate_content_quality",
    "validate_test_quality",
    "validate_transformation_program",
    "validate_nlp_technique_safety",
    "batch_validate_content",
    "get_quality_recommendations",
    "quick_safety_check",

    # Dependencies and data models
    "NLPQualityGuardianDependencies",
    "create_psychology_quality_guardian_dependencies",
    "create_universal_quality_guardian_dependencies",
    "create_test_quality_guardian_dependencies",
    "create_nlp_technique_quality_guardian_dependencies",
    "ValidationDomain",
    "ContentType",
    "QualityLevel",
    "ValidationAspect",
    "CriticalFlag",
    "ValidationResult",
    "ValidationCriteria",

    # Settings management
    "load_settings",
    "NLPQualityGuardianSettings",
    "get_domain_specific_settings",
    "create_validation_settings_for_domain",

    # Model providers and optimization
    "create_model_manager",
    "QualityGuardianModelManager",
    "ValidationTaskType",
    "get_validation_model",
    "get_deep_analysis_model",
    "get_safety_check_model",
    "get_report_generation_model",
    "get_knowledge_search_model",

    # Validation tools
    "search_quality_knowledge",
    "validate_content_structure",
    "check_safety_and_ethics",
    "validate_nlp_techniques",
    "generate_quality_report",
    "break_down_validation_tasks",
    "delegate_validation_task",

    # Prompt management
    "create_adaptive_system_prompt",
    "create_domain_specific_prompt",
    "create_content_type_prompt",
    "create_expert_validation_prompt"
]