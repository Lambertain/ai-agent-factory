"""
Зависимости для Universal Quality Validator Agent.
Конфигурация для универсального агента контроля качества различных типов проектов.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum


class QualityStandard(Enum):
    """Стандарты качества"""
    ISO_9001 = "iso_9001"
    IEEE_830 = "ieee_830"
    CMMI = "cmmi"
    AGILE = "agile"
    CUSTOM = "custom"


class ValidationLevel(Enum):
    """Уровни валидации"""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    ENTERPRISE = "enterprise"


class ProjectDomain(Enum):
    """Домены проектов"""
    WEB_DEVELOPMENT = "web_development"
    MOBILE_DEVELOPMENT = "mobile_development"
    DESKTOP_APPLICATIONS = "desktop_applications"
    API_SERVICES = "api_services"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    BLOCKCHAIN = "blockchain"
    GAMING = "gaming"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    IOT = "iot"
    DEVOPS = "devops"
    SECURITY = "security"


@dataclass
class QualityMetrics:
    """Метрики качества"""
    code_coverage: float = 0.8
    test_pass_rate: float = 1.0
    performance_threshold: float = 0.95
    security_score: float = 0.9
    maintainability_index: float = 0.8
    complexity_threshold: int = 10
    duplication_threshold: float = 0.05
    documentation_coverage: float = 0.7


@dataclass
class CodeQualityRules:
    """Правила качества кода"""
    max_function_length: int = 50
    max_class_length: int = 500
    max_file_length: int = 1000
    max_line_length: int = 120
    max_complexity: int = 10
    min_test_coverage: float = 0.8
    max_duplication: float = 0.05
    enforce_naming_conventions: bool = True
    require_documentation: bool = True
    enforce_type_hints: bool = True


@dataclass
class SecurityValidation:
    """Настройки валидации безопасности"""
    scan_vulnerabilities: bool = True
    check_dependencies: bool = True
    validate_authentication: bool = True
    check_authorization: bool = True
    verify_data_encryption: bool = True
    audit_api_security: bool = True
    check_input_validation: bool = True
    verify_output_encoding: bool = True
    validate_session_management: bool = True
    check_error_handling: bool = True


@dataclass
class PerformanceValidation:
    """Настройки валидации производительности"""
    load_testing: bool = True
    stress_testing: bool = True
    memory_usage_check: bool = True
    cpu_usage_check: bool = True
    response_time_check: bool = True
    throughput_check: bool = True
    scalability_check: bool = True
    database_performance: bool = True
    api_performance: bool = True
    frontend_performance: bool = True


@dataclass
class ComplianceValidation:
    """Настройки валидации соответствия"""
    gdpr_compliance: bool = False
    hipaa_compliance: bool = False
    pci_dss_compliance: bool = False
    sox_compliance: bool = False
    iso_27001_compliance: bool = False
    accessibility_compliance: bool = True
    wcag_level: str = "AA"
    browser_compatibility: bool = True
    mobile_responsiveness: bool = True


@dataclass
class TestingConfiguration:
    """Конфигурация тестирования"""
    unit_tests: bool = True
    integration_tests: bool = True
    e2e_tests: bool = True
    api_tests: bool = True
    performance_tests: bool = True
    security_tests: bool = True
    usability_tests: bool = False
    compatibility_tests: bool = True
    regression_tests: bool = True
    smoke_tests: bool = True


@dataclass
class DocumentationValidation:
    """Настройки валидации документации"""
    check_api_docs: bool = True
    validate_readme: bool = True
    check_code_comments: bool = True
    verify_architecture_docs: bool = True
    validate_user_guides: bool = True
    check_changelog: bool = True
    verify_deployment_docs: bool = True
    validate_troubleshooting: bool = True
    check_examples: bool = True
    verify_links: bool = True


@dataclass
class QualityGates:
    """Качественные ворота для различных стадий"""
    commit_gates: Dict[str, Any] = field(default_factory=lambda: {
        "code_formatting": True,
        "basic_tests": True,
        "linting": True,
        "type_checking": True
    })

    pr_gates: Dict[str, Any] = field(default_factory=lambda: {
        "code_review": True,
        "test_coverage": 0.8,
        "security_scan": True,
        "documentation_update": True,
        "no_breaking_changes": True
    })

    staging_gates: Dict[str, Any] = field(default_factory=lambda: {
        "integration_tests": True,
        "performance_tests": True,
        "security_scan": True,
        "api_documentation": True,
        "load_testing": True
    })

    production_gates: Dict[str, Any] = field(default_factory=lambda: {
        "all_tests_pass": True,
        "security_approved": True,
        "performance_approved": True,
        "compliance_verified": True,
        "rollback_plan": True
    })


@dataclass
class AutomationSettings:
    """Настройки автоматизации"""
    auto_fix_enabled: bool = True
    auto_format_code: bool = True
    auto_update_dependencies: bool = False
    auto_generate_tests: bool = False
    auto_generate_docs: bool = True
    auto_security_patches: bool = False
    continuous_monitoring: bool = True
    real_time_validation: bool = True


@dataclass
class ReportingSettings:
    """Настройки отчетности"""
    generate_html_reports: bool = True
    generate_json_reports: bool = True
    generate_pdf_reports: bool = False
    include_trends: bool = True
    include_recommendations: bool = True
    include_detailed_metrics: bool = True
    notification_channels: List[str] = field(default_factory=lambda: ["email", "slack"])
    report_schedule: str = "daily"


@dataclass
class IntegrationSettings:
    """Настройки интеграций"""
    git_integration: bool = True
    ci_cd_integration: bool = True
    issue_tracker_integration: bool = True
    code_review_integration: bool = True
    monitoring_integration: bool = True
    notification_integration: bool = True
    artifact_storage_integration: bool = True
    deployment_integration: bool = True


@dataclass
class QualityValidatorDependencies:
    """Основные зависимости агента валидации качества"""

    # Основные настройки
    project_domain: ProjectDomain = ProjectDomain.WEB_DEVELOPMENT
    quality_standard: QualityStandard = QualityStandard.AGILE
    validation_level: ValidationLevel = ValidationLevel.STANDARD

    # Коллективные настройки
    agent_name: str = "universal_quality_validator"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "quality-validation", "agent-knowledge", "pydantic-ai", "code-quality"
    ])
    knowledge_domain: str = "docs.quality-standards.org"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Конфигурации валидации
    quality_metrics: QualityMetrics = field(default_factory=QualityMetrics)
    code_quality_rules: CodeQualityRules = field(default_factory=CodeQualityRules)
    security_validation: SecurityValidation = field(default_factory=SecurityValidation)
    performance_validation: PerformanceValidation = field(default_factory=PerformanceValidation)
    compliance_validation: ComplianceValidation = field(default_factory=ComplianceValidation)
    testing_configuration: TestingConfiguration = field(default_factory=TestingConfiguration)
    documentation_validation: DocumentationValidation = field(default_factory=DocumentationValidation)

    # Качественные ворота и автоматизация
    quality_gates: QualityGates = field(default_factory=QualityGates)
    automation_settings: AutomationSettings = field(default_factory=AutomationSettings)
    reporting_settings: ReportingSettings = field(default_factory=ReportingSettings)
    integration_settings: IntegrationSettings = field(default_factory=IntegrationSettings)

    # Дополнительные настройки
    custom_rules: Dict[str, Any] = field(default_factory=dict)
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*/node_modules/*", "*/venv/*", "*/build/*", "*/dist/*", "*/.git/*"
    ])
    include_patterns: List[str] = field(default_factory=lambda: [
        "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.java", "*.go", "*.rb", "*.php"
    ])

    # Пороговые значения для критичности
    critical_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "security_score": 0.9,
        "test_coverage": 0.8,
        "performance_score": 0.9,
        "maintainability": 0.7,
        "code_complexity": 15
    })

    # Конфигурация для различных сред
    environment_configs: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "development": {
            "validation_level": "basic",
            "auto_fix": True,
            "strict_rules": False
        },
        "staging": {
            "validation_level": "comprehensive",
            "auto_fix": False,
            "strict_rules": True
        },
        "production": {
            "validation_level": "enterprise",
            "auto_fix": False,
            "strict_rules": True,
            "require_approval": True
        }
    })

    def get_environment_config(self, environment: str) -> Dict[str, Any]:
        """Получение конфигурации для конкретной среды"""
        return self.environment_configs.get(environment, self.environment_configs["development"])

    def get_domain_specific_rules(self) -> Dict[str, Any]:
        """Получение специфичных для домена правил"""
        domain_rules = {
            ProjectDomain.FINTECH: {
                "security_validation": {"extra_strict": True},
                "compliance_validation": {"pci_dss_compliance": True},
                "testing_configuration": {"security_tests": True, "compliance_tests": True}
            },
            ProjectDomain.HEALTHCARE: {
                "compliance_validation": {"hipaa_compliance": True, "gdpr_compliance": True},
                "security_validation": {"data_encryption": True, "audit_trails": True},
                "documentation_validation": {"regulatory_docs": True}
            },
            ProjectDomain.GAMING: {
                "performance_validation": {"fps_testing": True, "memory_optimization": True},
                "testing_configuration": {"performance_tests": True, "usability_tests": True}
            },
            ProjectDomain.API_SERVICES: {
                "documentation_validation": {"api_docs": True, "swagger_validation": True},
                "testing_configuration": {"api_tests": True, "load_tests": True},
                "security_validation": {"api_security": True, "rate_limiting": True}
            }
        }
        return domain_rules.get(self.project_domain, {})

    def is_critical_issue(self, metric_name: str, value: float) -> bool:
        """Проверка критичности проблемы"""
        threshold = self.critical_thresholds.get(metric_name)
        if threshold is None:
            return False

        # Для некоторых метрик низкие значения критичны, для других - высокие
        critical_low_metrics = ["test_coverage", "security_score", "performance_score", "maintainability"]
        if metric_name in critical_low_metrics:
            return value < threshold
        else:
            return value > threshold

    def should_delegate(self, task_keywords: List[str], current_agent_type: str = "quality_validation") -> Optional[str]:
        """Определить нужно ли делегировать задачу и кому."""
        from .tools import AGENT_COMPETENCIES

        if not self.enable_task_delegation:
            return None

        for agent_type, competencies in AGENT_COMPETENCIES.items():
            if agent_type != current_agent_type:
                overlap = set(task_keywords) & set(competencies)
                if len(overlap) >= 2:  # Значительное пересечение компетенций
                    return agent_type
        return None