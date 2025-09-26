"""Dependencies for Security Audit Agent."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import hashlib
import json
import asyncio
import httpx
from settings import load_security_settings, SecurityAuditSettings


@dataclass
class SecurityAuditDependencies:
    """Universal dependencies for Security Audit Agent supporting various project types."""

    # Core dependencies
    settings: Optional[SecurityAuditSettings] = None

    # Universal project configuration
    project_type: str = "web-app"  # web-app, api, mobile, infrastructure, compliance, iot, blockchain
    project_path: str = ""
    project_name: str = ""

    # Domain-specific security focus
    security_focus: str = "comprehensive"  # comprehensive, owasp-top10, privacy, authentication, infrastructure
    compliance_frameworks: List[str] = field(default_factory=list)  # ["pci-dss", "hipaa", "gdpr", "sox", "iso27001"]

    # Session context
    session_id: Optional[str] = None
    scan_history: List[Dict[str, Any]] = field(default_factory=list)
    current_scan_id: Optional[str] = None

    # Security scan configuration
    scan_preferences: Dict[str, Any] = field(default_factory=dict)
    excluded_paths: List[str] = field(default_factory=list)
    custom_rules: List[Dict[str, Any]] = field(default_factory=list)

    # Vulnerability database connections
    nvd_client: Optional[Any] = None
    safety_enabled: bool = True
    bandit_enabled: bool = True

    # Notification clients
    slack_client: Optional[Any] = None
    email_client: Optional[Any] = None

    # Performance tracking
    scan_metrics: Dict[str, Any] = field(default_factory=dict)
    cache: Dict[str, Any] = field(default_factory=dict)

    # RAG Configuration
    knowledge_tags: List[str] = field(default_factory=lambda: ["security-audit", "agent-knowledge", "pydantic-ai"])
    knowledge_domain: str | None = None
    archon_project_id: str | None = None
    archon_url: str = "http://localhost:3737"

    def __post_init__(self):
        """Initialize configuration after object creation."""
        # Setup project-specific defaults
        self._setup_project_defaults()

        # Configure compliance requirements based on project type
        self._setup_compliance_requirements()

        # Update knowledge tags based on project type and focus
        self._update_knowledge_tags()

    def _setup_project_defaults(self):
        """Set up default security scan configuration based on project type."""
        project_defaults = {
            "web-app": {
                "excluded_paths": ["node_modules", ".git", "dist", "build"],
                "scan_focus": ["xss", "sql-injection", "csrf", "authentication"],
                "compliance": ["owasp-top10", "pci-dss"],
                "priority_checks": ["input-validation", "session-management", "encryption"]
            },
            "api": {
                "excluded_paths": ["tests", "docs", ".git"],
                "scan_focus": ["api-security", "authentication", "rate-limiting", "data-exposure"],
                "compliance": ["owasp-api-top10", "pci-dss"],
                "priority_checks": ["jwt-validation", "api-keys", "cors", "rate-limits"]
            },
            "mobile": {
                "excluded_paths": ["build", "gradle", ".git"],
                "scan_focus": ["mobile-owasp", "data-storage", "communication", "platform-interaction"],
                "compliance": ["mobile-owasp-top10", "gdpr"],
                "priority_checks": ["insecure-storage", "weak-crypto", "reverse-engineering"]
            },
            "infrastructure": {
                "excluded_paths": [".terraform", ".git"],
                "scan_focus": ["cloud-security", "iac", "network", "access-control"],
                "compliance": ["cis-benchmarks", "iso27001"],
                "priority_checks": ["misconfigurations", "exposed-secrets", "public-access"]
            },
            "compliance": {
                "excluded_paths": [".git"],
                "scan_focus": ["data-protection", "privacy", "audit-logging", "access-control"],
                "compliance": ["gdpr", "hipaa", "sox", "pci-dss"],
                "priority_checks": ["data-classification", "encryption", "audit-trails"]
            },
            "iot": {
                "excluded_paths": ["firmware", ".git"],
                "scan_focus": ["device-security", "network-protocols", "firmware", "physical-security"],
                "compliance": ["iot-security-foundation"],
                "priority_checks": ["default-credentials", "firmware-updates", "secure-boot"]
            },
            "blockchain": {
                "excluded_paths": ["node_modules", ".git"],
                "scan_focus": ["smart-contracts", "consensus", "key-management", "transaction-security"],
                "compliance": ["blockchain-security-standards"],
                "priority_checks": ["reentrancy", "integer-overflow", "access-control"]
            }
        }

        if self.project_type in project_defaults:
            defaults = project_defaults[self.project_type]
            if not self.excluded_paths:
                self.excluded_paths = defaults["excluded_paths"]
            if not self.compliance_frameworks:
                self.compliance_frameworks = defaults["compliance"]
            # Update scan preferences with project-specific focus
            self.scan_preferences.update({
                "focus_areas": defaults["scan_focus"],
                "priority_checks": defaults["priority_checks"]
            })

    def _setup_compliance_requirements(self):
        """Set up compliance requirements based on selected frameworks."""
        compliance_requirements = {
            "pci-dss": {
                "required_checks": ["credit-card-detection", "encryption-in-transit", "access-logging"],
                "scan_frequency_days": 7
            },
            "hipaa": {
                "required_checks": ["phi-detection", "encryption-at-rest", "audit-logging"],
                "scan_frequency_days": 14
            },
            "gdpr": {
                "required_checks": ["pii-detection", "consent-management", "data-portability"],
                "scan_frequency_days": 30
            },
            "owasp-top10": {
                "required_checks": ["injection", "broken-auth", "sensitive-data", "xxe", "access-control"],
                "scan_frequency_days": 7
            },
            "iso27001": {
                "required_checks": ["risk-assessment", "asset-management", "incident-response"],
                "scan_frequency_days": 30
            }
        }

        for framework in self.compliance_frameworks:
            if framework in compliance_requirements:
                requirements = compliance_requirements[framework]
                self.scan_preferences.setdefault("required_checks", []).extend(requirements["required_checks"])

    def _update_knowledge_tags(self):
        """Update knowledge tags based on project configuration."""
        # Add project type specific tags
        type_tags = {
            "web-app": ["web-security", "owasp", "browser-security"],
            "api": ["api-security", "rest-security", "graphql-security"],
            "mobile": ["mobile-security", "ios-security", "android-security"],
            "infrastructure": ["cloud-security", "devops-security", "container-security"],
            "compliance": ["compliance", "regulatory", "data-protection"],
            "iot": ["iot-security", "embedded-security", "device-security"],
            "blockchain": ["blockchain-security", "smart-contract-audit", "defi-security"]
        }

        # Add focus-specific tags
        focus_tags = {
            "comprehensive": ["full-audit", "penetration-testing", "vulnerability-assessment"],
            "owasp-top10": ["owasp", "web-vulnerabilities", "application-security"],
            "privacy": ["privacy", "data-protection", "pii"],
            "authentication": ["auth-security", "identity-management", "access-control"],
            "infrastructure": ["infrastructure-security", "network-security", "cloud-security"]
        }

        if self.project_type in type_tags:
            self.knowledge_tags.extend(type_tags[self.project_type])

        if self.security_focus in focus_tags:
            self.knowledge_tags.extend(focus_tags[self.security_focus])

        # Add compliance framework tags
        for framework in self.compliance_frameworks:
            self.knowledge_tags.append(framework)

        # Remove duplicates
        self.knowledge_tags = list(set(self.knowledge_tags))

    def get_project_context(self) -> str:
        """Get project context for security analysis."""
        project_descriptions = {
            "web-app": "Web application requiring protection against OWASP Top 10 vulnerabilities",
            "api": "API service requiring authentication, rate limiting, and data protection",
            "mobile": "Mobile application with focus on secure storage and communication",
            "infrastructure": "Infrastructure and cloud resources requiring configuration security",
            "compliance": "Compliance-focused project requiring regulatory adherence",
            "iot": "IoT device/system requiring embedded and network security",
            "blockchain": "Blockchain/DeFi application requiring smart contract security"
        }

        return project_descriptions.get(self.project_type, "General security audit")

    def get_recommended_tools(self) -> List[str]:
        """Get recommended security tools for project type."""
        tools_map = {
            "web-app": ["bandit", "safety", "semgrep", "zap", "burp"],
            "api": ["bandit", "safety", "postman", "swagger-security", "api-fuzzer"],
            "mobile": ["mobsf", "qark", "needle", "frida", "apktool"],
            "infrastructure": ["trivy", "checkov", "terrascan", "prowler", "scout"],
            "compliance": ["lynis", "openscap", "chef-inspec", "aws-config"],
            "iot": ["firmwalker", "binwalk", "nmap", "wireshark"],
            "blockchain": ["mythril", "slither", "echidna", "manticore", "securify"]
        }

        return tools_map.get(self.project_type, ["bandit", "safety"])

    async def initialize(self):
        """Initialize external connections and validate configuration."""
        if not self.settings:
            self.settings = load_security_settings()

        # Generate session ID if not provided
        if not self.session_id:
            self.session_id = self._generate_session_id()

        # Initialize security tools availability
        await self._check_security_tools()

        # Initialize notification clients if configured
        await self._initialize_notifications()

        # Initialize vulnerability database connections
        await self._initialize_vulnerability_databases()

        # Set default scan preferences
        if not self.scan_preferences:
            self.scan_preferences = {
                "scan_type": self.settings.default_scan_type,
                "include_dependencies": True,
                "include_secrets": True,
                "include_compliance": True,
                "confidence_threshold": self.settings.min_confidence_level
            }

        # Initialize metrics tracking
        self.scan_metrics = {
            "total_scans": 0,
            "total_findings": 0,
            "average_scan_time": 0.0,
            "last_scan_time": None,
            "session_start_time": datetime.utcnow().isoformat()
        }

    async def cleanup(self):
        """Clean up external connections and resources."""
        # Close notification clients
        if self.slack_client:
            await self._cleanup_slack_client()

        if self.email_client:
            await self._cleanup_email_client()

        # Close vulnerability database connections
        if self.nvd_client:
            await self._cleanup_nvd_client()

        # Clear cache
        self.cache.clear()

    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat()

    def get_next_scan_date(self) -> str:
        """Get recommended next scan date based on findings."""
        # Default to weekly scans, but adjust based on risk level
        last_scan = self.scan_metrics.get("last_scan_time")
        if not last_scan:
            return (datetime.utcnow() + timedelta(days=7)).isoformat()

        # If last scan had critical findings, recommend sooner
        last_scan_findings = self._get_last_scan_findings()
        if any(f.get("severity") == "critical" for f in last_scan_findings):
            return (datetime.utcnow() + timedelta(days=1)).isoformat()
        elif any(f.get("severity") == "high" for f in last_scan_findings):
            return (datetime.utcnow() + timedelta(days=3)).isoformat()
        else:
            return (datetime.utcnow() + timedelta(days=7)).isoformat()

    def add_scan_result(self, scan_result: Dict[str, Any]):
        """Add scan result to history and update metrics."""
        self.scan_history.append({
            "timestamp": self.get_timestamp(),
            "scan_id": scan_result.get("scan_id"),
            "target": scan_result.get("target"),
            "findings_count": scan_result.get("total_findings", 0),
            "risk_score": scan_result.get("risk_score", 0.0),
            "scan_duration": scan_result.get("scan_duration", 0.0)
        })

        # Update metrics
        self.scan_metrics["total_scans"] += 1
        self.scan_metrics["total_findings"] += scan_result.get("total_findings", 0)
        self.scan_metrics["last_scan_time"] = self.get_timestamp()

        # Update average scan time
        total_duration = sum(s.get("scan_duration", 0) for s in self.scan_history)
        self.scan_metrics["average_scan_time"] = total_duration / len(self.scan_history)

        # Keep only last 100 scan results
        if len(self.scan_history) > 100:
            self.scan_history.pop(0)

    def set_scan_preference(self, key: str, value: Any):
        """Set a scan preference for the session."""
        self.scan_preferences[key] = value

    def add_custom_rule(self, rule: Dict[str, Any]):
        """Add a custom security rule."""
        self.custom_rules.append({
            "id": self._generate_rule_id(),
            "created_at": self.get_timestamp(),
            **rule
        })

    def get_scan_context(self) -> Dict[str, Any]:
        """Get current scan context for prompt generation."""
        return {
            "session_id": self.session_id,
            "total_scans": self.scan_metrics["total_scans"],
            "preferences": self.scan_preferences,
            "recent_findings": self._get_recent_findings_summary(),
            "custom_rules_count": len(self.custom_rules),
            "tools_available": {
                "bandit": self.bandit_enabled,
                "safety": self.safety_enabled,
                "nvd": bool(self.nvd_client)
            }
        }

    async def send_notification(self, severity: str, title: str, message: str, findings: List[Dict] = None):
        """Send security notification if configured."""
        try:
            # Only send notifications for high/critical findings
            if severity not in ["high", "critical"]:
                return

            notification_data = {
                "severity": severity,
                "title": title,
                "message": message,
                "timestamp": self.get_timestamp(),
                "session_id": self.session_id,
                "findings_count": len(findings) if findings else 0
            }

            # Send Slack notification
            if self.slack_client and self.settings.slack_webhook_url:
                await self._send_slack_notification(notification_data)

            # Send email notification
            if self.email_client and self.settings.email_notifications:
                await self._send_email_notification(notification_data)

        except Exception as e:
            # Don't fail the scan if notifications fail
            print(f"Failed to send notification: {e}")

    def get_compliance_requirements(self) -> Dict[str, bool]:
        """Get enabled compliance requirements."""
        return {
            "owasp_top10": self.settings.enable_owasp_top10,
            "cwe_mapping": self.settings.enable_cwe_mapping,
            "pci_dss": self.settings.enable_pci_dss,
            "hipaa": self.settings.enable_hipaa,
            "gdpr": self.settings.enable_gdpr
        }

    def should_exclude_path(self, path: str) -> bool:
        """Check if a path should be excluded from scanning."""
        path_lower = path.lower()

        # Check configured excluded directories
        for excluded_dir in self.settings.excluded_directories:
            if excluded_dir.lower() in path_lower:
                return True

        # Check custom excluded paths
        for excluded_path in self.excluded_paths:
            if excluded_path.lower() in path_lower:
                return True

        return False

    def should_exclude_file(self, filename: str) -> bool:
        """Check if a file should be excluded from scanning."""
        # Check file extensions
        for ext in self.settings.excluded_extensions:
            if filename.lower().endswith(ext.lower()):
                return True

        return False

    def get_cache_key(self, target: str, scan_type: str) -> str:
        """Generate cache key for scan results."""
        key_data = f"{target}_{scan_type}_{json.dumps(self.scan_preferences, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def cache_result(self, key: str, result: Any, ttl_minutes: int = 60):
        """Cache scan result with TTL."""
        expiry = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        self.cache[key] = {
            "data": result,
            "expiry": expiry.isoformat()
        }

    def get_cached_result(self, key: str) -> Optional[Any]:
        """Get cached result if still valid."""
        if key not in self.cache:
            return None

        cached = self.cache[key]
        expiry = datetime.fromisoformat(cached["expiry"])

        if datetime.utcnow() > expiry:
            del self.cache[key]
            return None

        return cached["data"]

    # Private helper methods

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]

    def _generate_rule_id(self) -> str:
        """Generate unique rule ID."""
        timestamp = datetime.utcnow().isoformat()
        rule_count = len(self.custom_rules)
        return hashlib.md5(f"{timestamp}_{rule_count}".encode()).hexdigest()[:8]

    async def _check_security_tools(self):
        """Check availability of security tools."""
        # Check Bandit
        try:
            import bandit
            self.bandit_enabled = True
        except ImportError:
            self.bandit_enabled = False

        # Check Safety
        try:
            import subprocess
            result = await asyncio.create_subprocess_exec(
                "safety", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            self.safety_enabled = result.returncode == 0
        except Exception:
            self.safety_enabled = False

    async def _initialize_notifications(self):
        """Initialize notification clients."""
        # Initialize Slack client
        if self.settings.slack_webhook_url:
            try:
                import aiohttp
                self.slack_client = aiohttp.ClientSession()
            except ImportError:
                self.slack_client = None

        # Initialize email client
        if self.settings.email_notifications and self.settings.smtp_server:
            try:
                import aiosmtplib
                self.email_client = aiosmtplib.SMTP(
                    hostname=self.settings.smtp_server,
                    port=self.settings.smtp_port
                )
            except ImportError:
                self.email_client = None

    async def _initialize_vulnerability_databases(self):
        """Initialize vulnerability database connections."""
        # Initialize NVD client if API key is provided
        if self.settings.nvd_api_key:
            # This would initialize a real NVD API client
            self.nvd_client = {"api_key": self.settings.nvd_api_key}

    def _get_last_scan_findings(self) -> List[Dict[str, Any]]:
        """Get findings from the last scan."""
        if not self.scan_history:
            return []

        # This would retrieve actual findings from the last scan
        # For now, return empty list
        return []

    def _get_recent_findings_summary(self) -> Dict[str, Any]:
        """Get summary of recent findings."""
        recent_scans = self.scan_history[-5:] if self.scan_history else []

        return {
            "recent_scans_count": len(recent_scans),
            "total_recent_findings": sum(s.get("findings_count", 0) for s in recent_scans),
            "average_risk_score": sum(s.get("risk_score", 0) for s in recent_scans) / len(recent_scans) if recent_scans else 0
        }

    async def _send_slack_notification(self, notification_data: Dict[str, Any]):
        """Send Slack notification."""
        if not self.slack_client:
            return

        payload = {
            "text": f"🚨 Security Alert: {notification_data['title']}",
            "attachments": [
                {
                    "color": "danger" if notification_data["severity"] == "critical" else "warning",
                    "fields": [
                        {
                            "title": "Severity",
                            "value": notification_data["severity"].upper(),
                            "short": True
                        },
                        {
                            "title": "Findings",
                            "value": str(notification_data.get("findings_count", 0)),
                            "short": True
                        },
                        {
                            "title": "Message",
                            "value": notification_data["message"],
                            "short": False
                        }
                    ]
                }
            ]
        }

        try:
            async with self.slack_client.post(self.settings.slack_webhook_url, json=payload) as response:
                if response.status != 200:
                    print(f"Slack notification failed: HTTP {response.status}")
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")

    async def _send_email_notification(self, notification_data: Dict[str, Any]):
        """Send email notification."""
        if not self.email_client or not self.settings.notification_recipients:
            return

        subject = f"Security Alert: {notification_data['title']}"
        body = f"""
Security Alert Details:

Severity: {notification_data['severity'].upper()}
Title: {notification_data['title']}
Message: {notification_data['message']}
Timestamp: {notification_data['timestamp']}
Session ID: {notification_data['session_id']}
Findings Count: {notification_data.get('findings_count', 0)}

This is an automated security notification from the Security Audit Agent.
"""

        try:
            await self.email_client.connect()
            await self.email_client.login(self.settings.smtp_username, self.settings.smtp_password)

            for recipient in self.settings.notification_recipients:
                message = f"""From: {self.settings.smtp_username}
To: {recipient}
Subject: {subject}

{body}"""

                await self.email_client.send_message(message)

            await self.email_client.quit()

        except Exception as e:
            print(f"Failed to send email notification: {e}")

    async def _cleanup_slack_client(self):
        """Clean up Slack client."""
        if self.slack_client:
            await self.slack_client.close()

    async def _cleanup_email_client(self):
        """Clean up email client."""
        if self.email_client:
            try:
                await self.email_client.quit()
            except Exception:
                pass

    async def _cleanup_nvd_client(self):
        """Clean up NVD client."""
        # Clean up NVD client if needed
        self.nvd_client = None