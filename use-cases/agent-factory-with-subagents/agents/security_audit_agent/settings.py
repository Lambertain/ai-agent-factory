"""Settings configuration for Security Audit Agent."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables from .env file
load_dotenv()


class SecurityAuditSettings(BaseSettings):
    """Security audit agent settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration (OpenAI-compatible)
    llm_provider: str = Field(
        default="openai",
        description="LLM provider (openai, anthropic, gemini, ollama, etc.)"
    )

    llm_api_key: str = Field(
        ...,
        description="API key for the LLM provider"
    )

    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Model to use for security analysis and reporting"
    )

    llm_base_url: Optional[str] = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API (for OpenAI-compatible providers)"
    )

    # Security Scan Configuration
    default_scan_type: str = Field(
        default="comprehensive",
        description="Default scan type: quick, comprehensive, focused"
    )

    max_file_size_mb: int = Field(
        default=10,
        description="Maximum file size to scan in MB"
    )

    max_scan_depth: int = Field(
        default=5,
        description="Maximum directory depth for recursive scans"
    )

    excluded_extensions: List[str] = Field(
        default=[".log", ".tmp", ".cache", ".git", ".pyc", ".pyo"],
        description="File extensions to exclude from scanning"
    )

    excluded_directories: List[str] = Field(
        default=["node_modules", ".git", "__pycache__", ".venv", "venv", "build", "dist"],
        description="Directories to exclude from scanning"
    )

    # Vulnerability Database Configuration
    nvd_api_key: Optional[str] = Field(
        default=None,
        description="NIST NVD API key for vulnerability data"
    )

    safety_enabled: bool = Field(
        default=True,
        description="Enable Python Safety vulnerability checking"
    )

    bandit_enabled: bool = Field(
        default=True,
        description="Enable Bandit static analysis"
    )

    # Report Configuration
    max_findings_per_category: int = Field(
        default=50,
        description="Maximum findings to report per category"
    )

    min_confidence_level: str = Field(
        default="medium",
        description="Minimum confidence level for findings: low, medium, high"
    )

    include_code_snippets: bool = Field(
        default=True,
        description="Include code snippets in findings"
    )

    max_snippet_lines: int = Field(
        default=5,
        description="Maximum lines to include in code snippets"
    )

    # Severity Thresholds
    critical_severity_threshold: int = Field(
        default=9,
        description="CVSS score threshold for critical severity (9-10)"
    )

    high_severity_threshold: int = Field(
        default=7,
        description="CVSS score threshold for high severity (7-8.9)"
    )

    medium_severity_threshold: int = Field(
        default=4,
        description="CVSS score threshold for medium severity (4-6.9)"
    )

    # Performance Configuration
    scan_timeout_seconds: int = Field(
        default=300,
        description="Timeout for individual scans in seconds"
    )

    parallel_scans: bool = Field(
        default=True,
        description="Enable parallel scanning for better performance"
    )

    max_concurrent_scans: int = Field(
        default=4,
        description="Maximum number of concurrent scans"
    )

    # Compliance Framework Configuration
    enable_owasp_top10: bool = Field(
        default=True,
        description="Enable OWASP Top 10 compliance checking"
    )

    enable_cwe_mapping: bool = Field(
        default=True,
        description="Enable CWE (Common Weakness Enumeration) mapping"
    )

    enable_pci_dss: bool = Field(
        default=False,
        description="Enable PCI DSS compliance checking"
    )

    enable_hipaa: bool = Field(
        default=False,
        description="Enable HIPAA compliance checking"
    )

    enable_gdpr: bool = Field(
        default=False,
        description="Enable GDPR compliance checking"
    )

    # Notification Configuration
    slack_webhook_url: Optional[str] = Field(
        default=None,
        description="Slack webhook URL for security notifications"
    )

    email_notifications: bool = Field(
        default=False,
        description="Enable email notifications for critical findings"
    )

    smtp_server: Optional[str] = Field(
        default=None,
        description="SMTP server for email notifications"
    )

    smtp_port: int = Field(
        default=587,
        description="SMTP server port"
    )

    smtp_username: Optional[str] = Field(
        default=None,
        description="SMTP username"
    )

    smtp_password: Optional[str] = Field(
        default=None,
        description="SMTP password"
    )

    notification_recipients: List[str] = Field(
        default=[],
        description="Email addresses for security notifications"
    )

    # Advanced Security Features
    enable_threat_modeling: bool = Field(
        default=True,
        description="Enable automated threat modeling"
    )

    enable_penetration_testing: bool = Field(
        default=False,
        description="Enable basic penetration testing capabilities"
    )

    enable_compliance_tracking: bool = Field(
        default=True,
        description="Enable compliance status tracking"
    )

    enable_security_metrics: bool = Field(
        default=True,
        description="Enable security metrics collection"
    )

    # Database Configuration (for storing scan results)
    database_url: Optional[str] = Field(
        default=None,
        description="Database URL for storing scan results (optional)"
    )

    enable_result_storage: bool = Field(
        default=False,
        description="Enable persistent storage of scan results"
    )

    result_retention_days: int = Field(
        default=90,
        description="Number of days to retain scan results"
    )


def load_security_settings() -> SecurityAuditSettings:
    """Load security audit settings with proper error handling."""
    try:
        return SecurityAuditSettings()
    except Exception as e:
        error_msg = f"Failed to load security audit settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file"
        raise ValueError(error_msg) from e


def validate_security_configuration(settings: SecurityAuditSettings) -> List[str]:
    """
    Validate security configuration and return list of warnings/errors.

    Args:
        settings: Security audit settings to validate

    Returns:
        List of validation messages
    """
    warnings = []

    # Check critical settings
    if not settings.llm_api_key:
        warnings.append("LLM API key not configured - agent will not function")

    # Check security tool availability
    if settings.bandit_enabled:
        try:
            import bandit
        except ImportError:
            warnings.append("Bandit not installed - static analysis will be limited")

    if settings.safety_enabled:
        import subprocess
        try:
            subprocess.run(["safety", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("Safety not installed - dependency vulnerability checking disabled")

    # Check notification configuration
    if settings.email_notifications and not all([settings.smtp_server, settings.smtp_username, settings.smtp_password]):
        warnings.append("Email notifications enabled but SMTP not fully configured")

    if settings.slack_webhook_url and not settings.slack_webhook_url.startswith("https://hooks.slack.com"):
        warnings.append("Invalid Slack webhook URL format")

    # Check compliance configuration
    compliance_features = [
        settings.enable_owasp_top10,
        settings.enable_pci_dss,
        settings.enable_hipaa,
        settings.enable_gdpr
    ]

    if not any(compliance_features):
        warnings.append("No compliance frameworks enabled - consider enabling at least OWASP Top 10")

    # Check performance settings
    if settings.max_concurrent_scans > 8:
        warnings.append("High concurrent scan count may impact system performance")

    if settings.scan_timeout_seconds < 60:
        warnings.append("Short scan timeout may cause incomplete scans")

    # Check file size limits
    if settings.max_file_size_mb > 50:
        warnings.append("Large file size limit may cause memory issues")

    return warnings


def get_security_config_summary(settings: SecurityAuditSettings) -> dict:
    """
    Get a summary of current security configuration.

    Args:
        settings: Security audit settings

    Returns:
        Configuration summary dictionary
    """
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "default_scan_type": settings.default_scan_type,
        "security_tools": {
            "bandit_enabled": settings.bandit_enabled,
            "safety_enabled": settings.safety_enabled,
            "threat_modeling": settings.enable_threat_modeling,
            "penetration_testing": settings.enable_penetration_testing
        },
        "compliance_frameworks": {
            "owasp_top10": settings.enable_owasp_top10,
            "cwe_mapping": settings.enable_cwe_mapping,
            "pci_dss": settings.enable_pci_dss,
            "hipaa": settings.enable_hipaa,
            "gdpr": settings.enable_gdpr
        },
        "notifications": {
            "email_enabled": settings.email_notifications,
            "slack_enabled": bool(settings.slack_webhook_url),
            "recipients_count": len(settings.notification_recipients)
        },
        "performance": {
            "parallel_scans": settings.parallel_scans,
            "max_concurrent": settings.max_concurrent_scans,
            "timeout_seconds": settings.scan_timeout_seconds
        },
        "data_retention": {
            "result_storage": settings.enable_result_storage,
            "retention_days": settings.result_retention_days
        }
    }