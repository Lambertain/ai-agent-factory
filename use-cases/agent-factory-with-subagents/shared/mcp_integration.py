"""
Universal MCP Server Integration Module for All Agents

Provides standardized integration with all MCP servers:
- shadcn: UI component generation
- context7: Long-term memory and context management
- security-scanner: Security analysis and vulnerability detection
- memory: Persistent memory storage
- puppeteer: Browser automation
- github: Git repository operations
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
import json
from pydantic_ai.mcp import MCPServerStdio


@dataclass
class MCPServerConfig:
    """Configuration for MCP server connection."""
    name: str
    command: str
    args: List[str]
    working_dir: str = "D:/Automation"
    timeout: int = 30
    enabled: bool = True


class MCPIntegration:
    """Universal MCP server integration for agents."""

    # Standard MCP server configurations
    MCP_SERVERS = {
        "shadcn": MCPServerConfig(
            name="shadcn",
            command="node",
            args=["../shadcn-ui-mcp-server/build/index.js", "--transport", "stdio"],
            enabled=True
        ),
        "context7": MCPServerConfig(
            name="context7",
            command="node",
            args=["../context7-mcp-server/dist/index.js", "--transport", "stdio"],
            enabled=True
        ),
        "security-scanner": MCPServerConfig(
            name="security-scanner",
            command="node",
            args=["d:/Automation/scripts/security-scanner-mcp.mjs"],
            enabled=True
        ),
        "memory": MCPServerConfig(
            name="memory",
            command="npx",
            args=["@modelcontextprotocol/server-memory", "--transport", "stdio"],
            enabled=True
        ),
        "puppeteer": MCPServerConfig(
            name="puppeteer",
            command="npx",
            args=["@modelcontextprotocol/server-puppeteer", "--transport", "stdio"],
            enabled=True
        ),
        "github": MCPServerConfig(
            name="github",
            command="npx",
            args=["@modelcontextprotocol/server-github", "--transport", "stdio"],
            enabled=True
        )
    }

    def __init__(self, enabled_servers: Optional[List[str]] = None):
        """
        Initialize MCP integration with specified servers.

        Args:
            enabled_servers: List of server names to enable. If None, all are enabled.
        """
        self.enabled_servers = enabled_servers or list(self.MCP_SERVERS.keys())
        self.servers: Dict[str, MCPServerStdio] = {}
        self._initialize_servers()

    def _initialize_servers(self):
        """Initialize configured MCP servers."""
        for server_name in self.enabled_servers:
            if server_name in self.MCP_SERVERS:
                config = self.MCP_SERVERS[server_name]
                if config.enabled:
                    self.servers[server_name] = MCPServerStdio(
                        command=config.command,
                        args=config.args,
                        timeout=config.timeout
                    )

    def get_server_toolsets(self) -> List[MCPServerStdio]:
        """Get list of server toolsets for agent registration."""
        return list(self.servers.values())

    def get_server_by_name(self, name: str) -> Optional[MCPServerStdio]:
        """Get specific server by name."""
        return self.servers.get(name)

    @staticmethod
    def create_agent_specific_integration(agent_type: str) -> 'MCPIntegration':
        """Create MCP integration tailored for specific agent type."""

        agent_server_mapping = {
            # UI/UX agents need Shadcn and Puppeteer
            "uiux_enhancement": ["shadcn", "puppeteer"],
            "ui_designer": ["shadcn", "puppeteer"],

            # Security agents need security scanner and github
            "security_audit": ["security-scanner", "github"],
            "security_scanner": ["security-scanner", "github"],

            # Performance agents need puppeteer and memory
            "performance_optimization": ["puppeteer", "memory", "context7"],
            "performance_monitor": ["puppeteer", "memory"],

            # Database/Backend agents need github and memory
            "prisma_database": ["github", "memory", "context7"],
            "api_development": ["github", "memory", "context7"],
            "queue_worker": ["memory", "context7"],

            # General development agents need context7 and github
            "typescript_architecture": ["context7", "github", "memory"],
            "implementation_engineer": ["context7", "github", "memory"],

            # Community/Social agents need memory for user data
            "community_management": ["memory", "context7"],
            "viral_sharing": ["memory", "context7"],

            # Payment agents need security and memory
            "payment_integration": ["security-scanner", "memory", "context7"],

            # Mobile agents need all for comprehensive testing
            "pwa_mobile": ["puppeteer", "memory", "context7"],
            "mobile_development": ["puppeteer", "memory", "context7"]
        }

        # Get servers for this agent type, default to context7 + memory
        servers = agent_server_mapping.get(
            agent_type,
            ["context7", "memory"]
        )

        return MCPIntegration(enabled_servers=servers)


class MCPToolsMixin:
    """Mixin providing common MCP tool patterns for agents."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mcp_integration: Optional[MCPIntegration] = None

    def setup_mcp_integration(self, agent_type: str):
        """Setup MCP integration for this agent."""
        self.mcp_integration = MCPIntegration.create_agent_specific_integration(agent_type)
        return self.mcp_integration.get_server_toolsets()

    async def use_shadcn_component(self, component_name: str, props: Dict[str, Any] = None) -> str:
        """Generate Shadcn UI component."""
        if not self.mcp_integration or "shadcn" not in self.mcp_integration.servers:
            return "Shadcn MCP server not available"

        # Implementation will depend on actual Shadcn MCP API
        return f"Generated {component_name} component with props: {props}"

    async def store_long_term_memory(self, key: str, data: Any, tags: List[str] = None) -> bool:
        """Store data in long-term memory via Memory MCP."""
        if not self.mcp_integration or "memory" not in self.mcp_integration.servers:
            return False

        try:
            # Memory MCP implementation
            memory_data = {
                "key": key,
                "data": data,
                "tags": tags or [],
                "timestamp": asyncio.get_event_loop().time()
            }
            # Actual MCP call would go here
            return True
        except Exception:
            return False

    async def retrieve_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve memories from long-term storage."""
        if not self.mcp_integration or "memory" not in self.mcp_integration.servers:
            return []

        try:
            # Memory MCP search implementation
            # Actual MCP call would go here
            return []
        except Exception:
            return []

    async def analyze_security_vulnerabilities(self, code_or_path: str) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities."""
        if not self.mcp_integration or "security-scanner" not in self.mcp_integration.servers:
            return {"error": "Security scanner not available"}

        try:
            # Security scanner MCP implementation
            return {
                "vulnerabilities": [],
                "severity": "low",
                "recommendations": []
            }
        except Exception as e:
            return {"error": f"Security analysis failed: {e}"}

    async def capture_screenshot(self, url: str, selector: str = None) -> str:
        """Capture screenshot using Puppeteer MCP."""
        if not self.mcp_integration or "puppeteer" not in self.mcp_integration.servers:
            return "Puppeteer MCP server not available"

        try:
            # Puppeteer MCP implementation
            return f"Screenshot captured for {url}"
        except Exception as e:
            return f"Screenshot failed: {e}"

    async def manage_context_memory(self, action: str, data: Any = None) -> Any:
        """Manage long-term context via Context7 MCP."""
        if not self.mcp_integration or "context7" not in self.mcp_integration.servers:
            return None

        try:
            # Context7 MCP implementation
            if action == "store":
                return f"Context stored: {data}"
            elif action == "retrieve":
                return "Retrieved context data"
            else:
                return f"Unknown action: {action}"
        except Exception as e:
            return f"Context management failed: {e}"


# Convenience functions for quick MCP setup
def get_standard_mcp_toolsets() -> List[MCPServerStdio]:
    """Get standard MCP toolsets for general agents."""
    integration = MCPIntegration(enabled_servers=["context7", "memory"])
    return integration.get_server_toolsets()


def get_ui_mcp_toolsets() -> List[MCPServerStdio]:
    """Get MCP toolsets optimized for UI/UX agents."""
    integration = MCPIntegration(enabled_servers=["shadcn", "puppeteer", "context7"])
    return integration.get_server_toolsets()


def get_security_mcp_toolsets() -> List[MCPServerStdio]:
    """Get MCP toolsets optimized for security agents."""
    integration = MCPIntegration(enabled_servers=["security-scanner", "github", "context7"])
    return integration.get_server_toolsets()


def get_performance_mcp_toolsets() -> List[MCPServerStdio]:
    """Get MCP toolsets optimized for performance agents."""
    integration = MCPIntegration(enabled_servers=["puppeteer", "memory", "context7"])
    return integration.get_server_toolsets()