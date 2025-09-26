"""Model providers for Security Audit Agent."""

from typing import Optional
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from settings import load_security_settings


def get_llm_model(model_choice: Optional[str] = None) -> OpenAIModel:
    """
    Get LLM model configuration for security analysis.
    Supports any OpenAI-compatible API provider.

    Args:
        model_choice: Optional override for model choice

    Returns:
        Configured OpenAI-compatible model
    """
    settings = load_security_settings()

    llm_choice = model_choice or settings.llm_model
    base_url = settings.llm_base_url
    api_key = settings.llm_api_key

    # Create provider based on configuration
    provider = OpenAIProvider(base_url=base_url, api_key=api_key)

    return OpenAIModel(llm_choice, provider=provider)


def get_security_analysis_model() -> OpenAIModel:
    """
    Get model optimized for security analysis tasks.

    Returns:
        Configured model for security analysis
    """
    settings = load_security_settings()

    # Use a more capable model for complex security analysis
    model_name = settings.llm_model
    if "gpt-4" not in model_name.lower() and "claude" not in model_name.lower():
        # Recommend more capable model for security analysis
        print("Warning: Consider using GPT-4 or Claude for better security analysis accuracy")

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(model_name, provider=provider)


def get_code_review_model() -> OpenAIModel:
    """
    Get model optimized for code review and vulnerability detection.

    Returns:
        Configured model for code review
    """
    settings = load_security_settings()

    # For code review, we might want to use a specialized model
    # or adjust parameters for better code understanding
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


def get_threat_modeling_model() -> OpenAIModel:
    """
    Get model optimized for threat modeling and risk assessment.

    Returns:
        Configured model for threat modeling
    """
    settings = load_security_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


def get_compliance_model() -> OpenAIModel:
    """
    Get model optimized for compliance checking and reporting.

    Returns:
        Configured model for compliance analysis
    """
    settings = load_security_settings()

    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(settings.llm_model, provider=provider)


def get_model_info() -> dict:
    """
    Get information about current model configuration.

    Returns:
        Dictionary with model configuration info
    """
    settings = load_security_settings()

    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "capabilities": {
            "security_analysis": True,
            "code_review": True,
            "threat_modeling": settings.enable_threat_modeling,
            "compliance_checking": any([
                settings.enable_owasp_top10,
                settings.enable_pci_dss,
                settings.enable_hipaa,
                settings.enable_gdpr
            ])
        }
    }


def validate_llm_configuration() -> bool:
    """
    Validate that LLM configuration is properly set for security analysis.

    Returns:
        True if configuration is valid
    """
    try:
        # Check if we can create a model instance
        model = get_llm_model()

        # Additional validation for security use case
        settings = load_security_settings()

        if not settings.llm_api_key:
            print("Error: LLM API key not configured")
            return False

        if not settings.llm_base_url:
            print("Error: LLM base URL not configured")
            return False

        # Warn about model capabilities
        if "gpt-3.5" in settings.llm_model.lower():
            print("Warning: GPT-3.5 may have limitations for complex security analysis")

        return True

    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False


def get_recommended_model_settings() -> dict:
    """
    Get recommended model settings for security analysis tasks.

    Returns:
        Dictionary with recommended settings
    """
    return {
        "temperature": 0.1,  # Low temperature for consistent security analysis
        "max_tokens": 4000,  # Allow for detailed security reports
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "recommended_models": [
            "gpt-4",
            "gpt-4-turbo",
            "claude-3-sonnet",
            "claude-3-opus"
        ],
        "model_features": {
            "code_understanding": "Essential for vulnerability detection",
            "reasoning": "Important for threat modeling",
            "consistency": "Critical for reliable security assessments",
            "context_length": "Needed for analyzing large codebases"
        }
    }