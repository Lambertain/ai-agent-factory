"""
Deployment Engineer Settings - настройки для агента.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class DeploymentEngineerSettings(BaseSettings):
    """Настройки Deployment Engineer агента."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Модель для кодирования и DevOps"
    )
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Cloud Platform Settings
    aws_access_key_id: str = Field(default="", description="AWS Access Key")
    aws_secret_access_key: str = Field(default="", description="AWS Secret Key")
    gcp_project_id: str = Field(default="", description="GCP Project ID")
    azure_subscription_id: str = Field(default="", description="Azure Subscription ID")

    # Kubernetes Settings
    kube_config_path: str = Field(
        default="~/.kube/config",
        description="Путь к kubeconfig"
    )
    kube_default_namespace: str = Field(
        default="default",
        description="Namespace по умолчанию"
    )

    # Docker Settings
    docker_registry: str = Field(
        default="ghcr.io",
        description="Docker registry"
    )
    docker_username: str = Field(default="", description="Docker username")
    docker_password: str = Field(default="", description="Docker password")

    # Monitoring Settings
    prometheus_url: str = Field(
        default="http://localhost:9090",
        description="Prometheus URL"
    )
    grafana_url: str = Field(
        default="http://localhost:3000",
        description="Grafana URL"
    )
    alertmanager_url: str = Field(
        default="http://localhost:9093",
        description="Alertmanager URL"
    )

    # Terraform Settings
    terraform_backend: str = Field(
        default="s3",
        description="Terraform backend type"
    )
    terraform_state_bucket: str = Field(
        default="",
        description="S3 bucket для Terraform state"
    )
    terraform_state_region: str = Field(
        default="us-east-1",
        description="AWS регион для Terraform state"
    )

    # Deployment Settings
    default_deployment_strategy: str = Field(
        default="rolling",
        description="Стратегия развертывания по умолчанию"
    )
    default_min_replicas: int = Field(
        default=3,
        description="Минимальное количество реплик"
    )
    default_max_replicas: int = Field(
        default=10,
        description="Максимальное количество реплик"
    )


def load_settings() -> DeploymentEngineerSettings:
    """Загрузить настройки агента."""
    load_dotenv()

    try:
        settings = DeploymentEngineerSettings()

        # Создание модели LLM
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )

        llm_model = OpenAIModel(settings.llm_model, provider=provider)

        # Добавляем модель в settings
        settings.llm_model = llm_model

        return settings
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e
