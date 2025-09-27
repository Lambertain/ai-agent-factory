"""
Настройки для Universal Quality Validator Agent.
Конфигурация для различных доменов, стандартов качества и уровней валидации.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from enum import Enum
import os

from .dependencies import QualityStandard, ValidationLevel, ProjectDomain


class QualityValidatorSettings(BaseSettings):
    """Настройки Universal Quality Validator Agent с поддержкой переменных окружения."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="QUALITY_VALIDATOR_"
    )

    # Основные настройки
    project_domain: ProjectDomain = Field(
        default=ProjectDomain.WEB_DEVELOPMENT,
        description="Домен проекта для адаптации валидации"
    )
    quality_standard: QualityStandard = Field(
        default=QualityStandard.ISO_9001,
        description="Стандарт качества для применения"
    )
    validation_level: ValidationLevel = Field(
        default=ValidationLevel.STANDARD,
        description="Уровень детализации валидации"
    )

    # Пути и директории
    project_path: str = Field(
        default="",
        description="Путь к анализируемому проекту"
    )
    reports_output_dir: str = Field(
        default="./quality_reports",
        description="Директория для сохранения отчетов"
    )
    temp_dir: str = Field(
        default="./temp",
        description="Временная директория для промежуточных файлов"
    )

    # Пороги качества
    minimum_code_quality_score: float = Field(
        default=0.8,
        description="Минимальный порог качества кода",
        ge=0.0,
        le=1.0
    )
    minimum_security_score: float = Field(
        default=0.9,
        description="Минимальный порог безопасности",
        ge=0.0,
        le=1.0
    )
    minimum_performance_score: float = Field(
        default=0.7,
        description="Минимальный порог производительности",
        ge=0.0,
        le=1.0
    )
    minimum_test_coverage: float = Field(
        default=0.8,
        description="Минимальный порог покрытия тестами",
        ge=0.0,
        le=1.0
    )

    # Настройки инструментов
    enable_static_analysis: bool = Field(
        default=True,
        description="Включить статический анализ кода"
    )
    enable_security_scan: bool = Field(
        default=True,
        description="Включить сканирование безопасности"
    )
    enable_performance_tests: bool = Field(
        default=True,
        description="Включить тесты производительности"
    )
    enable_dependency_check: bool = Field(
        default=True,
        description="Включить проверку зависимостей"
    )

    # Внешние инструменты
    sonar_url: Optional[str] = Field(
        default=None,
        description="URL SonarQube сервера"
    )
    sonar_token: Optional[str] = Field(
        default=None,
        description="Токен для SonarQube"
    )

    # Уведомления
    notification_channels: List[str] = Field(
        default_factory=list,
        description="Каналы уведомлений (email, slack, teams)"
    )
    alert_on_critical_issues: bool = Field(
        default=True,
        description="Отправлять уведомления о критичных проблемах"
    )

    # Расширенные настройки для разных доменов
    domain_specific_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Специфичные настройки для доменов"
    )

    # AI и ML настройки
    ai_model_provider: str = Field(
        default="openai",
        description="Провайдер AI модели для анализа"
    )
    ai_model_name: str = Field(
        default="gpt-4",
        description="Название AI модели"
    )
    enable_ai_recommendations: bool = Field(
        default=True,
        description="Включить AI рекомендации"
    )

    def __post_init__(self):
        """Инициализация дополнительных настроек после создания."""
        if not self.domain_specific_config:
            self.domain_specific_config = self._get_default_domain_config()

    def _get_default_domain_config(self) -> Dict[str, Any]:
        """Получить конфигурацию по умолчанию для различных доменов."""
        return {
            "web_development": {
                "check_accessibility": True,
                "validate_seo": True,
                "performance_budget": {
                    "first_contentful_paint": 1.5,
                    "largest_contentful_paint": 2.5,
                    "cumulative_layout_shift": 0.1
                },
                "security_headers": [
                    "Content-Security-Policy",
                    "X-Frame-Options",
                    "X-Content-Type-Options"
                ]
            },
            "mobile_development": {
                "battery_optimization": True,
                "memory_limits": {
                    "max_heap_size": "128MB",
                    "image_cache_size": "50MB"
                },
                "platform_compliance": {
                    "ios_app_store": True,
                    "google_play": True
                }
            },
            "api_services": {
                "validate_openapi": True,
                "rate_limiting": True,
                "response_time_sla": 200,  # ms
                "api_versioning": True,
                "security_standards": ["OAuth2", "JWT"]
            },
            "fintech": {
                "pci_compliance": True,
                "encryption_standards": ["AES-256", "RSA-2048"],
                "audit_logging": True,
                "fraud_detection": True,
                "regulatory_compliance": ["PCI-DSS", "SOX", "GDPR"]
            },
            "healthcare": {
                "hipaa_compliance": True,
                "data_encryption": "AES-256",
                "access_controls": "RBAC",
                "audit_trails": True,
                "medical_device_standards": ["IEC 62304", "ISO 14971"]
            }
        }

    def get_domain_config(self, domain: str = None) -> Dict[str, Any]:
        """Получить конфигурацию для конкретного домена."""
        if domain is None:
            domain = self.project_domain.value

        return self.domain_specific_config.get(domain, {})

    def get_quality_thresholds(self) -> Dict[str, float]:
        """Получить пороги качества для текущих настроек."""
        base_thresholds = {
            "code_quality": self.minimum_code_quality_score,
            "security": self.minimum_security_score,
            "performance": self.minimum_performance_score,
            "test_coverage": self.minimum_test_coverage
        }

        # Адаптация порогов под уровень валидации
        if self.validation_level == ValidationLevel.BASIC:
            # Для базового уровня пороги ниже
            for key in base_thresholds:
                base_thresholds[key] *= 0.8
        elif self.validation_level == ValidationLevel.ENTERPRISE:
            # Для enterprise уровня пороги выше
            for key in base_thresholds:
                base_thresholds[key] = min(1.0, base_thresholds[key] * 1.1)

        return base_thresholds

    def get_enabled_validations(self) -> List[str]:
        """Получить список включенных типов валидации."""
        validations = []

        if self.enable_static_analysis:
            validations.append("code_quality")
        if self.enable_security_scan:
            validations.append("security")
        if self.enable_performance_tests:
            validations.append("performance")
        if self.enable_dependency_check:
            validations.append("dependencies")

        # Всегда включена валидация документации и compliance
        validations.extend(["documentation", "compliance"])

        return validations


def load_settings() -> QualityValidatorSettings:
    """Загрузить настройки с проверкой переменных окружения."""
    load_dotenv()

    try:
        return QualityValidatorSettings()
    except Exception as e:
        # Fallback к настройкам по умолчанию
        print(f"Предупреждение: Не удалось загрузить некоторые настройки: {e}")
        return QualityValidatorSettings()


def get_domain_specific_settings(domain: ProjectDomain) -> Dict[str, Any]:
    """Получить специфичные настройки для домена."""
    settings = load_settings()
    return settings.get_domain_config(domain.value)


def get_validation_config(
    domain: ProjectDomain,
    standard: QualityStandard,
    level: ValidationLevel
) -> Dict[str, Any]:
    """Получить полную конфигурацию валидации для указанных параметров."""
    settings = load_settings()
    settings.project_domain = domain
    settings.quality_standard = standard
    settings.validation_level = level

    return {
        "domain_config": settings.get_domain_config(),
        "quality_thresholds": settings.get_quality_thresholds(),
        "enabled_validations": settings.get_enabled_validations(),
        "settings": settings
    }