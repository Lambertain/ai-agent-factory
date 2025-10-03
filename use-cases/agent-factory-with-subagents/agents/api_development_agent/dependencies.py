"""
Universal API Development Agent Dependencies.

Configurable dependencies supporting multiple frameworks and domain types.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


@dataclass
class APIAgentDependencies:
    """Universal dependencies for API Development Agent."""

    # Core API settings
    api_key: str
    agent_name: str = "api_development"  # For RAG protection
    project_path: str = ""
    project_name: str = ""

    # Universal API configuration
    framework_type: str = "express"  # express, nestjs, fastapi, django-rest, aspnet-core, spring-boot
    api_type: str = "rest"  # rest, graphql, grpc, websocket
    domain_type: str = "general"  # general, ecommerce, fintech, healthcare, gaming, social, enterprise

    # API architecture patterns
    architecture_pattern: str = "mvc"  # mvc, clean-architecture, hexagonal, microservices, serverless
    auth_strategy: str = "jwt"  # jwt, oauth2, basic, api-key, session, none
    data_validation: str = "schema"  # schema, decorator, middleware, custom

    # Performance and scaling
    caching_strategy: str = "memory"  # memory, redis, memcached, none
    rate_limiting: bool = True
    cors_enabled: bool = True
    compression_enabled: bool = True

    # Documentation and testing
    documentation_type: str = "openapi"  # openapi, postman, insomnia, custom, none
    testing_framework: str = "jest"  # jest, pytest, mocha, xunit, rspec
    api_versioning: str = "header"  # header, url, query, accept-header, none

    # Database and storage configuration
    database_type: str = "postgresql"  # postgresql, mysql, mongodb, sqlite, redis, none
    orm_framework: str = "auto"  # auto, prisma, typeorm, sequelize, mongoose, sqlalchemy, hibernate

    # Development environment
    typescript_enabled: bool = True
    hot_reload: bool = True
    environment: str = "development"  # development, staging, production

    # API specific features
    middleware_stack: List[str] = field(default_factory=lambda: ["cors", "helmet", "compression", "logging"])
    error_handling: str = "centralized"  # centralized, distributed, custom
    request_logging: bool = True
    health_checks: bool = True
    metrics_enabled: bool = True

    # Security configuration
    security_headers: bool = True
    input_sanitization: bool = True
    sql_injection_protection: bool = True
    xss_protection: bool = True

    # API business logic configuration
    business_logic_patterns: List[str] = field(default_factory=lambda: ["service-layer", "repository-pattern"])
    validation_strategy: str = "request-response"  # request-only, response-only, request-response, none
    serialization_format: str = "json"  # json, xml, protobuf, msgpack

    # Framework-specific advanced settings
    advanced_config: Dict[str, Any] = field(default_factory=dict)

    # RAG and knowledge integration
    knowledge_tags: List[str] = field(default_factory=lambda: ["api-development", "agent-knowledge", "pydantic-ai"])
    knowledge_domain: Optional[str] = None
    archon_project_id: Optional[str] = None

    # Session management
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization configuration."""
        # Auto-configure framework-specific settings
        self._configure_framework_defaults()
        self._set_domain_optimizations()

        # Set knowledge domain based on framework
        if not self.knowledge_domain:
            framework_domains = {
                "express": "docs.expressjs.com",
                "nestjs": "docs.nestjs.com",
                "fastapi": "fastapi.tiangolo.com",
                "django-rest": "django-rest-framework.org",
                "aspnet-core": "docs.microsoft.com/aspnet",
                "spring-boot": "spring.io/projects/spring-boot"
            }
            self.knowledge_domain = framework_domains.get(self.framework_type, "api.development.com")

    def _configure_framework_defaults(self):
        """Configure framework-specific default settings."""
        framework_configs = {
            "express": {
                "typescript_enabled": True,
                "testing_framework": "jest",
                "orm_framework": "prisma"
            },
            "nestjs": {
                "typescript_enabled": True,
                "testing_framework": "jest",
                "orm_framework": "typeorm",
                "architecture_pattern": "clean-architecture"
            },
            "fastapi": {
                "typescript_enabled": False,
                "testing_framework": "pytest",
                "orm_framework": "sqlalchemy",
                "documentation_type": "openapi"
            },
            "django-rest": {
                "typescript_enabled": False,
                "testing_framework": "pytest",
                "orm_framework": "django-orm",
                "architecture_pattern": "mvc"
            },
            "aspnet-core": {
                "typescript_enabled": False,
                "testing_framework": "xunit",
                "orm_framework": "entity-framework"
            },
            "spring-boot": {
                "typescript_enabled": False,
                "testing_framework": "junit",
                "orm_framework": "hibernate"
            }
        }

        config = framework_configs.get(self.framework_type, {})
        for key, value in config.items():
            if not hasattr(self, key) or getattr(self, key) == "auto":
                setattr(self, key, value)

    def _set_domain_optimizations(self):
        """Set domain-specific optimizations."""
        domain_configs = {
            "ecommerce": {
                "caching_strategy": "redis",
                "rate_limiting": True,
                "metrics_enabled": True,
                "security_headers": True
            },
            "fintech": {
                "security_headers": True,
                "input_sanitization": True,
                "request_logging": True,
                "auth_strategy": "oauth2"
            },
            "healthcare": {
                "security_headers": True,
                "input_sanitization": True,
                "sql_injection_protection": True,
                "auth_strategy": "oauth2"
            },
            "gaming": {
                "caching_strategy": "redis",
                "rate_limiting": True,
                "api_type": "websocket"
            },
            "social": {
                "rate_limiting": True,
                "caching_strategy": "redis",
                "api_versioning": "header"
            },
            "enterprise": {
                "security_headers": True,
                "metrics_enabled": True,
                "health_checks": True,
                "documentation_type": "openapi"
            }
        }

        config = domain_configs.get(self.domain_type, {})
        for key, value in config.items():
            if getattr(self, key, None) is None or getattr(self, key) == "auto":
                setattr(self, key, value)

    def get_framework_config(self) -> Dict[str, Any]:
        """Get framework-specific configuration."""
        return {
            "framework_type": self.framework_type,
            "api_type": self.api_type,
            "architecture_pattern": self.architecture_pattern,
            "typescript_enabled": self.typescript_enabled,
            "orm_framework": self.orm_framework,
            "testing_framework": self.testing_framework,
            **self.advanced_config
        }

    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration for the API."""
        return {
            "auth_strategy": self.auth_strategy,
            "security_headers": self.security_headers,
            "input_sanitization": self.input_sanitization,
            "sql_injection_protection": self.sql_injection_protection,
            "xss_protection": self.xss_protection,
            "cors_enabled": self.cors_enabled,
            "rate_limiting": self.rate_limiting
        }

    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance optimization configuration."""
        return {
            "caching_strategy": self.caching_strategy,
            "compression_enabled": self.compression_enabled,
            "rate_limiting": self.rate_limiting,
            "metrics_enabled": self.metrics_enabled,
            "health_checks": self.health_checks
        }