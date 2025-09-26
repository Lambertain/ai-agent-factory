"""
Universal API Development Agent for Pydantic AI.

A comprehensive AI agent for developing APIs across multiple frameworks and domains.
Supports Express.js, NestJS, FastAPI, Django REST, ASP.NET Core, and Spring Boot
with domain-specific optimizations for e-commerce, fintech, healthcare, and more.
"""

from .agent import api_development_agent
from .dependencies import APIAgentDependencies
from .settings import get_llm_model, get_settings, APIAgentSettings

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__license__ = "MIT"

__all__ = [
    "api_development_agent",
    "APIAgentDependencies",
    "get_llm_model",
    "get_settings",
    "APIAgentSettings"
]