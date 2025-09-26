"""
LLM provider configuration for Community Management Agent.
"""

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from .settings import load_settings


def get_llm_model():
    """
    Configure and return LLM model for Community Management Agent.

    Returns:
        Configured LLM model instance
    """
    settings = load_settings()

    # Configure provider
    if settings.llm_base_url:
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
    else:
        provider = OpenAIProvider(
            api_key=settings.llm_api_key
        )

    # Return model instance
    return OpenAIModel(
        model_name=settings.llm_model,
        provider=provider
    )