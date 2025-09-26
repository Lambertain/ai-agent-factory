"""
API Development Agent Settings and Configuration.

Centralized configuration management for the universal API development agent.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class APIAgentSettings(BaseSettings):
    """Settings for the API Development Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for LLM provider")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="LLM model name")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Base URL for LLM API"
    )

    # Cost-optimized model configuration for different tasks
    llm_coding_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Model for code generation")
    llm_analysis_model: str = Field(default="qwen2.5-72b-instruct", description="Model for analysis tasks")
    llm_docs_model: str = Field(default="gemini-2.5-flash-lite", description="Model for documentation")

    # Gemini configuration for cost-effective tasks
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")

    # Agent-specific settings
    agent_name: str = Field(default="API Development Agent", description="Agent display name")
    agent_version: str = Field(default="1.0.0", description="Agent version")

    # RAG and Knowledge Base settings
    archon_url: str = Field(default="http://localhost:3737", description="Archon Knowledge Base URL")
    knowledge_base_enabled: bool = Field(default=True, description="Enable knowledge base integration")

    # Default API development settings
    default_framework: str = Field(default="express", description="Default API framework")
    default_domain: str = Field(default="general", description="Default domain type")
    default_language: str = Field(default="typescript", description="Default programming language")

    # Performance settings
    max_retries: int = Field(default=3, description="Maximum number of retries for LLM calls")
    timeout_seconds: int = Field(default=60, description="Timeout for LLM calls in seconds")
    enable_caching: bool = Field(default=True, description="Enable response caching")

    # Development settings
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Security settings
    enable_input_validation: bool = Field(default=True, description="Enable input validation")
    max_input_length: int = Field(default=10000, description="Maximum input length")

    # API generation settings
    include_tests: bool = Field(default=True, description="Include test generation by default")
    include_docs: bool = Field(default=True, description="Include documentation generation by default")
    include_security: bool = Field(default=True, description="Include security patterns by default")


def load_settings() -> APIAgentSettings:
    """
    Load and validate agent settings.

    Returns:
        Configured settings instance

    Raises:
        ValueError: If required settings are missing or invalid
    """
    load_dotenv()

    try:
        settings = APIAgentSettings()

        # Validate required settings
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY is required. Please set it in your .env file.")

        return settings

    except Exception as e:
        error_msg = f"Failed to load API agent settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nPlease ensure LLM_API_KEY is set in your .env file."
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "coding") -> OpenAIModel:
    """
    Get the appropriate LLM model based on task type.

    Args:
        task_type: Type of task ("coding", "analysis", "docs")

    Returns:
        Configured LLM model
    """
    settings = load_settings()

    # Select model based on task type for cost optimization
    model_mapping = {
        "coding": settings.llm_coding_model,
        "analysis": settings.llm_analysis_model,
        "docs": settings.llm_docs_model,
        "default": settings.llm_model
    }

    model_name = model_mapping.get(task_type, settings.llm_model)

    # Configure provider
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )

    return OpenAIModel(model_name, provider=provider)


def get_framework_defaults(framework: str) -> dict:
    """
    Get default configuration for a specific framework.

    Args:
        framework: Framework name (express, nestjs, fastapi, etc.)

    Returns:
        Default configuration dictionary
    """
    defaults = {
        "express": {
            "language": "typescript",
            "testing_framework": "jest",
            "orm": "prisma",
            "auth_default": "jwt",
            "documentation": "openapi"
        },
        "nestjs": {
            "language": "typescript",
            "testing_framework": "jest",
            "orm": "typeorm",
            "auth_default": "jwt",
            "documentation": "openapi"
        },
        "fastapi": {
            "language": "python",
            "testing_framework": "pytest",
            "orm": "sqlalchemy",
            "auth_default": "oauth2",
            "documentation": "openapi"
        },
        "django-rest": {
            "language": "python",
            "testing_framework": "pytest",
            "orm": "django-orm",
            "auth_default": "django-auth",
            "documentation": "openapi"
        },
        "aspnet-core": {
            "language": "csharp",
            "testing_framework": "xunit",
            "orm": "entity-framework",
            "auth_default": "identity",
            "documentation": "openapi"
        },
        "spring-boot": {
            "language": "java",
            "testing_framework": "junit",
            "orm": "hibernate",
            "auth_default": "spring-security",
            "documentation": "openapi"
        }
    }

    return defaults.get(framework, {
        "language": "typescript",
        "testing_framework": "jest",
        "orm": "auto",
        "auth_default": "jwt",
        "documentation": "openapi"
    })


def get_domain_defaults(domain: str) -> dict:
    """
    Get default configuration for a specific domain.

    Args:
        domain: Domain type (ecommerce, fintech, healthcare, etc.)

    Returns:
        Domain-specific configuration dictionary
    """
    defaults = {
        "ecommerce": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "redis",
            "security_level": "standard",
            "monitoring": True
        },
        "fintech": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "redis",
            "security_level": "high",
            "monitoring": True,
            "audit_logging": True
        },
        "healthcare": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "memory",
            "security_level": "high",
            "monitoring": True,
            "audit_logging": True,
            "data_encryption": True
        },
        "gaming": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "redis",
            "security_level": "standard",
            "monitoring": True,
            "real_time": True
        },
        "social": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "redis",
            "security_level": "standard",
            "monitoring": True,
            "content_moderation": True
        },
        "enterprise": {
            "auth_required": True,
            "rate_limiting": True,
            "caching": "redis",
            "security_level": "high",
            "monitoring": True,
            "audit_logging": True,
            "compliance": True
        }
    }

    return defaults.get(domain, {
        "auth_required": True,
        "rate_limiting": False,
        "caching": "memory",
        "security_level": "standard",
        "monitoring": False
    })


def validate_framework_compatibility(framework: str, language: str) -> bool:
    """
    Validate framework and language compatibility.

    Args:
        framework: Framework name
        language: Programming language

    Returns:
        True if compatible, False otherwise
    """
    compatibility_matrix = {
        "express": ["javascript", "typescript"],
        "nestjs": ["typescript"],
        "fastapi": ["python"],
        "django-rest": ["python"],
        "aspnet-core": ["csharp"],
        "spring-boot": ["java", "kotlin"]
    }

    compatible_languages = compatibility_matrix.get(framework, [])
    return language.lower() in [lang.lower() for lang in compatible_languages]


# Global settings instance
_settings: Optional[APIAgentSettings] = None


def get_settings() -> APIAgentSettings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings