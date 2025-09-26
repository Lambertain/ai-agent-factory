"""
Enhanced Base Agent Dependencies with MCP Integration

Universal base dependencies for all agents with built-in MCP server support.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path

from mcp_integration import MCPIntegration, MCPToolsMixin


@dataclass
class UniversalAgentDependencies:
    """
    Universal base dependencies for all agents with MCP integration.

    This class provides a standard foundation that all agents should inherit from.
    """

    # Core agent settings
    api_key: str
    agent_name: str = ""
    agent_type: str = ""

    # Project configuration (universal adaptability)
    project_path: str = ""
    domain_type: str = ""  # e.g., "web", "mobile", "api", "database"
    project_type: str = ""  # e.g., "e-commerce", "saas", "blog", "crm"
    framework: str = ""     # e.g., "nextjs", "react", "fastapi", "django"

    # MCP Integration settings
    enable_mcp_integration: bool = True
    custom_mcp_servers: List[str] = field(default_factory=list)
    mcp_working_dir: str = "D:/Automation"

    # RAG and Knowledge Base
    knowledge_tags: List[str] = field(default_factory=list)
    knowledge_domain: str = ""
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Performance and Scaling
    max_concurrent_operations: int = 10
    cache_ttl_seconds: int = 300
    batch_processing_size: int = 100
    rate_limit_per_minute: int = 60

    # Multi-language and Cultural Support
    primary_language: str = "en"
    supported_languages: List[str] = field(default_factory=lambda: ["en"])
    timezone: str = "UTC"
    cultural_adaptation_enabled: bool = False

    # Integration Settings
    enable_github_integration: bool = False
    enable_security_scanning: bool = False
    enable_ui_automation: bool = False
    enable_performance_monitoring: bool = False
    enable_long_term_memory: bool = True

    # Development Environment
    debug_mode: bool = False
    verbose_logging: bool = False
    testing_mode: bool = False

    # Notification and Reporting
    alert_webhook_url: str = ""
    daily_report_enabled: bool = False
    error_reporting_enabled: bool = True

    def __post_init__(self):
        """Initialize agent-specific configurations."""

        # Auto-set agent name if not provided
        if not self.agent_name and self.agent_type:
            self.agent_name = f"{self.agent_type}_agent"

        # Set default knowledge tags
        if not self.knowledge_tags and self.agent_type:
            self.knowledge_tags = [
                self.agent_type.replace("_", "-"),
                "agent-knowledge",
                "pydantic-ai"
            ]

        # Set domain-specific knowledge domain
        if not self.knowledge_domain and self.domain_type:
            domain_mapping = {
                "web": "web-development",
                "mobile": "mobile-development",
                "api": "api-development",
                "database": "database-management",
                "security": "security-audit",
                "performance": "performance-optimization",
                "ui": "ui-ux-design"
            }
            self.knowledge_domain = domain_mapping.get(self.domain_type, self.domain_type)

    def get_mcp_integration(self) -> Optional[MCPIntegration]:
        """Get MCP integration instance for this agent."""
        if not self.enable_mcp_integration:
            return None

        if self.custom_mcp_servers:
            return MCPIntegration(enabled_servers=self.custom_mcp_servers)
        else:
            return MCPIntegration.create_agent_specific_integration(self.agent_type)

    def get_required_mcp_servers(self) -> List[str]:
        """Get list of MCP servers required for this agent type."""
        server_requirements = {
            "uiux_enhancement": ["shadcn", "puppeteer"],
            "security_audit": ["security-scanner", "github"],
            "performance_optimization": ["puppeteer", "memory", "context7"],
            "prisma_database": ["github", "memory", "context7"],
            "api_development": ["github", "memory", "context7"],
            "typescript_architecture": ["context7", "github", "memory"],
            "community_management": ["memory", "context7"],
            "payment_integration": ["security-scanner", "memory", "context7"],
            "pwa_mobile": ["puppeteer", "memory", "context7"]
        }

        return server_requirements.get(self.agent_type, ["context7", "memory"])

    def validate_configuration(self) -> List[str]:
        """Validate agent configuration and return list of issues."""
        issues = []

        if not self.api_key:
            issues.append("API key is required")

        if not self.agent_type:
            issues.append("Agent type must be specified")

        if self.enable_mcp_integration and not self.mcp_working_dir:
            issues.append("MCP working directory must be specified when MCP is enabled")

        if self.project_path and not Path(self.project_path).exists():
            issues.append(f"Project path does not exist: {self.project_path}")

        return issues

    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment configuration for agent deployment."""
        return {
            "AGENT_NAME": self.agent_name,
            "AGENT_TYPE": self.agent_type,
            "PROJECT_PATH": self.project_path,
            "DOMAIN_TYPE": self.domain_type,
            "PROJECT_TYPE": self.project_type,
            "FRAMEWORK": self.framework,
            "PRIMARY_LANGUAGE": self.primary_language,
            "TIMEZONE": self.timezone,
            "DEBUG_MODE": str(self.debug_mode).lower(),
            "MCP_WORKING_DIR": self.mcp_working_dir,
            "ENABLE_MCP": str(self.enable_mcp_integration).lower(),
            "ARCHON_PROJECT_ID": self.archon_project_id
        }

    def create_specialized_config(self, specialization: str) -> 'UniversalAgentDependencies':
        """Create a specialized configuration for specific use cases."""

        specialization_configs = {
            "e-commerce": {
                "domain_type": "web",
                "project_type": "e-commerce",
                "framework": "nextjs",
                "enable_security_scanning": True,
                "enable_performance_monitoring": True
            },
            "saas-platform": {
                "domain_type": "web",
                "project_type": "saas",
                "framework": "react",
                "enable_github_integration": True,
                "enable_long_term_memory": True
            },
            "mobile-app": {
                "domain_type": "mobile",
                "project_type": "app",
                "framework": "react-native",
                "enable_ui_automation": True,
                "enable_performance_monitoring": True
            },
            "api-service": {
                "domain_type": "api",
                "project_type": "microservice",
                "framework": "fastapi",
                "enable_security_scanning": True,
                "enable_github_integration": True
            }
        }

        config = specialization_configs.get(specialization, {})

        # Create a copy with specialized settings
        new_deps = UniversalAgentDependencies(
            api_key=self.api_key,
            agent_name=self.agent_name,
            agent_type=self.agent_type,
            **config
        )

        return new_deps


# Convenience factory functions for common agent configurations
def create_ui_agent_dependencies(api_key: str, project_path: str = "") -> UniversalAgentDependencies:
    """Create dependencies for UI/UX agents."""
    return UniversalAgentDependencies(
        api_key=api_key,
        agent_type="uiux_enhancement",
        project_path=project_path,
        domain_type="ui",
        enable_ui_automation=True,
        enable_performance_monitoring=True,
        custom_mcp_servers=["shadcn", "puppeteer", "context7"]
    )


def create_security_agent_dependencies(api_key: str, project_path: str = "") -> UniversalAgentDependencies:
    """Create dependencies for security agents."""
    return UniversalAgentDependencies(
        api_key=api_key,
        agent_type="security_audit",
        project_path=project_path,
        domain_type="security",
        enable_security_scanning=True,
        enable_github_integration=True,
        custom_mcp_servers=["security-scanner", "github", "context7"]
    )


def create_performance_agent_dependencies(api_key: str, project_path: str = "") -> UniversalAgentDependencies:
    """Create dependencies for performance agents."""
    return UniversalAgentDependencies(
        api_key=api_key,
        agent_type="performance_optimization",
        project_path=project_path,
        domain_type="performance",
        enable_performance_monitoring=True,
        enable_ui_automation=True,
        custom_mcp_servers=["puppeteer", "memory", "context7"]
    )


def create_database_agent_dependencies(api_key: str, project_path: str = "") -> UniversalAgentDependencies:
    """Create dependencies for database agents."""
    return UniversalAgentDependencies(
        api_key=api_key,
        agent_type="prisma_database",
        project_path=project_path,
        domain_type="database",
        enable_github_integration=True,
        enable_long_term_memory=True,
        custom_mcp_servers=["github", "memory", "context7"]
    )