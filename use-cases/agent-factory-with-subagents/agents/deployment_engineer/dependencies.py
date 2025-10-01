"""
Deployment Engineer Dependencies - зависимости для агента.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class DeploymentEngineerDependencies:
    """Зависимости для Deployment Engineer агента."""

    # Основные настройки
    api_key: str
    project_path: str = ""
    agent_name: str = "deployment_engineer"

    # Cloud platform configuration
    cloud_provider: str = "aws"  # aws, gcp, azure, digitalocean
    cloud_region: str = "us-east-1"
    cloud_credentials: Optional[Dict[str, str]] = None

    # Kubernetes configuration
    kube_config_path: Optional[str] = None
    kube_namespace: str = "default"
    kube_context: Optional[str] = None

    # Docker configuration
    docker_registry: str = "ghcr.io"
    docker_registry_credentials: Optional[Dict[str, str]] = None

    # CI/CD configuration
    cicd_platform: str = "github_actions"  # github_actions, gitlab_ci, jenkins
    cicd_config_path: str = ".github/workflows"

    # Monitoring configuration
    monitoring_enabled: bool = True
    prometheus_url: Optional[str] = None
    grafana_url: Optional[str] = None

    # Infrastructure as Code
    terraform_backend: str = "s3"
    terraform_state_bucket: Optional[str] = None

    # RAG конфигурация для базы знаний
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "deployment",
        "devops",
        "ci-cd",
        "kubernetes",
        "docker",
        "agent-knowledge"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory

    # Deployment settings
    deployment_strategy: str = "rolling"  # rolling, blue-green, canary
    max_unavailable: int = 0
    max_surge: int = 1

    # Auto-scaling configuration
    min_replicas: int = 3
    max_replicas: int = 10
    target_cpu_utilization: int = 70
    target_memory_utilization: int = 80

    def __post_init__(self):
        """Инициализация зависимостей."""
        # Установка cloud credentials по умолчанию
        if not self.cloud_credentials:
            self.cloud_credentials = {}

        # Установка Docker registry credentials
        if not self.docker_registry_credentials:
            self.docker_registry_credentials = {}
