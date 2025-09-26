"""
Universal Queue/Worker Management Agent Dependencies.

Configurable dependencies supporting multiple queue systems and worker architectures.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from decimal import Decimal
from enum import Enum


class QueueType(str, Enum):
    """Supported queue types."""
    REDIS = "redis"
    RABBITMQ = "rabbitmq"
    AWS_SQS = "aws_sqs"
    AZURE_SERVICE_BUS = "azure_service_bus"
    GOOGLE_CLOUD_TASKS = "google_cloud_tasks"
    CELERY = "celery"
    RQUEUE = "rqueue"
    SIDEKIQ = "sidekiq"
    BULL = "bull"
    BEE_QUEUE = "bee_queue"


class WorkerType(str, Enum):
    """Supported worker types."""
    CELERY = "celery"
    RQ = "rq"
    DRAMATIQ = "dramatiq"
    HUEY = "huey"
    TASKIQ = "taskiq"
    ARQS = "arqs"
    WORKER_THREADS = "worker_threads"
    ASYNCIO_WORKERS = "asyncio_workers"
    MULTIPROCESSING = "multiprocessing"


class ScalingStrategy(str, Enum):
    """Worker scaling strategies."""
    MANUAL = "manual"
    AUTO_CPU = "auto_cpu"
    AUTO_MEMORY = "auto_memory"
    AUTO_QUEUE_LENGTH = "auto_queue_length"
    AUTO_LATENCY = "auto_latency"
    KUBERNETES_HPA = "kubernetes_hpa"
    DOCKER_SWARM = "docker_swarm"
    CUSTOM = "custom"


class DeploymentType(str, Enum):
    """Deployment environments."""
    STANDALONE = "standalone"
    DISTRIBUTED = "distributed"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"
    SERVERLESS = "serverless"
    CLOUD_FUNCTIONS = "cloud_functions"
    LAMBDA = "lambda"
    CLOUD_RUN = "cloud_run"


class UseCase(str, Enum):
    """Common use cases for queue/worker systems."""
    API_PROCESSING = "api_processing"
    DATA_PIPELINE = "data_pipeline"
    EMAIL_SENDING = "email_sending"
    FILE_PROCESSING = "file_processing"
    IMAGE_PROCESSING = "image_processing"
    VIDEO_PROCESSING = "video_processing"
    ML_INFERENCE = "ml_inference"
    BATCH_JOBS = "batch_jobs"
    CRON_JOBS = "cron_jobs"
    EVENT_PROCESSING = "event_processing"
    NOTIFICATION_SERVICE = "notification_service"
    WEB_SCRAPING = "web_scraping"
    REPORT_GENERATION = "report_generation"
    DATA_SYNC = "data_sync"
    BACKUP_TASKS = "backup_tasks"


@dataclass
class QueueWorkerDependencies:
    """Universal dependencies for Queue/Worker Management Agent."""

    # Core settings
    api_key: str
    project_path: str = ""
    project_name: str = ""

    # Queue system configuration
    queue_type: QueueType = QueueType.REDIS
    queue_connection_url: str = "redis://localhost:6379/0"
    queue_name_prefix: str = "tasks"

    # Worker configuration
    worker_type: WorkerType = WorkerType.CELERY
    worker_concurrency: int = 4
    worker_prefetch_multiplier: int = 1
    worker_max_tasks_per_child: int = 1000

    # Use case and domain
    use_case: UseCase = UseCase.API_PROCESSING
    domain_type: str = "general"  # general, web, data, ml, media, etc.

    # Architecture and deployment
    deployment_type: DeploymentType = DeploymentType.STANDALONE
    scaling_strategy: ScalingStrategy = ScalingStrategy.MANUAL
    distributed_workers: bool = False

    # Queue configuration
    queue_durability: bool = True
    queue_persistence: bool = True
    queue_ttl_seconds: Optional[int] = 3600  # 1 hour default
    max_queue_size: Optional[int] = None

    # Task configuration
    task_timeout_seconds: int = 300  # 5 minutes default
    task_retry_attempts: int = 3
    task_retry_delay_seconds: int = 60
    task_priority_levels: int = 3  # low, normal, high

    # Performance settings
    enable_task_compression: bool = False
    enable_result_backend: bool = True
    result_expires_seconds: int = 86400  # 24 hours
    task_serializer: str = "json"  # json, pickle, msgpack
    result_serializer: str = "json"

    # Monitoring and observability
    monitoring_enabled: bool = True
    metrics_backend: str = "prometheus"  # prometheus, statsd, custom
    enable_task_tracking: bool = True
    enable_worker_monitoring: bool = True
    enable_queue_monitoring: bool = True

    # Failure handling
    dead_letter_queue: bool = True
    max_retries_before_dlq: int = 5
    enable_failure_notifications: bool = True
    failure_notification_webhook: Optional[str] = None

    # Security
    enable_authentication: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    enable_ssl: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None

    # Rate limiting
    enable_rate_limiting: bool = False
    max_tasks_per_second: Optional[int] = None
    max_tasks_per_minute: Optional[int] = None
    rate_limit_window_seconds: int = 60

    # Scheduling
    enable_periodic_tasks: bool = False
    scheduler_timezone: str = "UTC"
    enable_cron_tasks: bool = False

    # Worker pool configuration
    worker_pool_type: str = "threads"  # threads, processes, eventlet, gevent
    min_workers: int = 1
    max_workers: int = 10
    worker_spawn_delay_seconds: float = 1.0

    # Queue priorities and routing
    enable_task_routing: bool = False
    routing_key_strategy: str = "hash"  # hash, round_robin, priority, custom
    queue_routing_config: Dict[str, str] = field(default_factory=dict)

    # Health checks and heartbeats
    worker_heartbeat_interval: int = 30  # seconds
    health_check_endpoint: bool = True
    health_check_path: str = "/health"

    # Logging and debugging
    log_level: str = "INFO"
    enable_task_logging: bool = True
    log_task_args: bool = False  # Security consideration
    log_task_results: bool = False

    # Framework integration
    framework_type: str = "universal"  # fastapi, django, flask, express, spring, etc.
    integration_middleware: List[str] = field(default_factory=list)

    # Cloud provider specific settings
    cloud_provider: Optional[str] = None  # aws, azure, gcp
    cloud_region: Optional[str] = None
    cloud_credentials_path: Optional[str] = None

    # Docker/Kubernetes settings
    container_image: Optional[str] = None
    kubernetes_namespace: str = "default"
    resource_requests: Dict[str, str] = field(default_factory=lambda: {"cpu": "100m", "memory": "128Mi"})
    resource_limits: Dict[str, str] = field(default_factory=lambda: {"cpu": "500m", "memory": "512Mi"})

    # Advanced features
    enable_message_deduplication: bool = False
    enable_exactly_once_delivery: bool = False
    enable_message_ordering: bool = False
    enable_batch_processing: bool = False
    batch_size: int = 10
    batch_timeout_seconds: int = 5

    # Development settings
    debug_mode: bool = False
    enable_hot_reload: bool = False
    development_mode: bool = False

    # Backup and recovery
    enable_task_backup: bool = False
    backup_interval_hours: int = 24
    backup_retention_days: int = 7

    # Cost optimization
    enable_worker_auto_shutdown: bool = False
    idle_worker_timeout_minutes: int = 10
    cost_optimization_enabled: bool = False

    # RAG and knowledge integration
    knowledge_tags: List[str] = field(default_factory=lambda: ["queue-worker", "agent-knowledge", "pydantic-ai"])
    knowledge_domain: Optional[str] = None
    archon_project_id: Optional[str] = None

    # Session management
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    # Advanced configuration
    advanced_config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization configuration."""
        # Auto-configure based on queue type
        self._configure_queue_defaults()

        # Auto-configure based on worker type
        self._configure_worker_defaults()

        # Auto-configure based on use case
        self._configure_use_case_optimizations()

        # Auto-configure based on deployment type
        self._configure_deployment_optimizations()

        # Set knowledge domain based on queue/worker type
        if not self.knowledge_domain:
            domain_map = {
                QueueType.REDIS: "redis.io",
                QueueType.RABBITMQ: "rabbitmq.com",
                QueueType.CELERY: "docs.celeryproject.org",
                QueueType.AWS_SQS: "docs.aws.amazon.com/sqs",
                QueueType.AZURE_SERVICE_BUS: "docs.microsoft.com/azure/service-bus"
            }
            self.knowledge_domain = domain_map.get(self.queue_type, "queue-worker.universal.com")

    def _configure_queue_defaults(self):
        """Configure queue-specific default settings."""
        queue_configs = {
            QueueType.REDIS: {
                "queue_connection_url": "redis://localhost:6379/0",
                "queue_durability": False,  # Redis is in-memory by default
                "task_serializer": "json",
                "result_serializer": "json"
            },
            QueueType.RABBITMQ: {
                "queue_connection_url": "amqp://guest:guest@localhost:5672//",
                "queue_durability": True,
                "queue_persistence": True,
                "task_serializer": "json",
                "enable_task_routing": True
            },
            QueueType.AWS_SQS: {
                "queue_durability": True,
                "queue_persistence": True,
                "cloud_provider": "aws",
                "enable_message_deduplication": True,
                "task_timeout_seconds": 900  # SQS max visibility timeout
            },
            QueueType.AZURE_SERVICE_BUS: {
                "queue_durability": True,
                "queue_persistence": True,
                "cloud_provider": "azure",
                "enable_message_ordering": True,
                "enable_exactly_once_delivery": True
            },
            QueueType.GOOGLE_CLOUD_TASKS: {
                "queue_durability": True,
                "cloud_provider": "gcp",
                "task_timeout_seconds": 1800,  # Cloud Tasks max
                "enable_rate_limiting": True
            },
            QueueType.CELERY: {
                "worker_type": WorkerType.CELERY,
                "enable_result_backend": True,
                "enable_periodic_tasks": True,
                "task_serializer": "json"
            }
        }

        config = queue_configs.get(self.queue_type, {})
        for key, value in config.items():
            if hasattr(self, key) and getattr(self, key) == getattr(QueueWorkerDependencies, key, None):
                setattr(self, key, value)

    def _configure_worker_defaults(self):
        """Configure worker-specific default settings."""
        worker_configs = {
            WorkerType.CELERY: {
                "worker_pool_type": "threads",
                "enable_periodic_tasks": True,
                "enable_task_tracking": True,
                "worker_heartbeat_interval": 30
            },
            WorkerType.RQ: {
                "queue_type": QueueType.REDIS,
                "worker_pool_type": "processes",
                "task_timeout_seconds": 180,
                "enable_result_backend": True
            },
            WorkerType.DRAMATIQ: {
                "worker_pool_type": "threads",
                "enable_rate_limiting": True,
                "enable_task_tracking": True,
                "task_serializer": "json"
            },
            WorkerType.HUEY: {
                "enable_periodic_tasks": True,
                "enable_result_backend": True,
                "worker_pool_type": "threads"
            },
            WorkerType.TASKIQ: {
                "worker_pool_type": "asyncio",
                "task_serializer": "json",
                "enable_task_tracking": True
            },
            WorkerType.ARQS: {
                "worker_pool_type": "asyncio",
                "queue_type": QueueType.REDIS,
                "task_serializer": "json"
            }
        }

        config = worker_configs.get(self.worker_type, {})
        for key, value in config.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Only override if current value is default
                if (isinstance(current_value, str) and current_value in ["universal", "general"]) or \
                   (isinstance(current_value, bool) and not current_value):
                    setattr(self, key, value)

    def _configure_use_case_optimizations(self):
        """Configure optimizations based on use case."""
        use_case_configs = {
            UseCase.API_PROCESSING: {
                "task_timeout_seconds": 30,
                "worker_concurrency": 8,
                "enable_rate_limiting": True,
                "max_tasks_per_second": 100
            },
            UseCase.DATA_PIPELINE: {
                "task_timeout_seconds": 1800,  # 30 minutes
                "worker_concurrency": 4,
                "enable_batch_processing": True,
                "batch_size": 100,
                "worker_pool_type": "processes"
            },
            UseCase.EMAIL_SENDING: {
                "task_timeout_seconds": 60,
                "worker_concurrency": 16,
                "enable_rate_limiting": True,
                "max_tasks_per_minute": 1000,
                "task_retry_attempts": 5
            },
            UseCase.FILE_PROCESSING: {
                "task_timeout_seconds": 600,  # 10 minutes
                "worker_concurrency": 2,
                "worker_pool_type": "processes",
                "enable_task_compression": True
            },
            UseCase.IMAGE_PROCESSING: {
                "task_timeout_seconds": 300,
                "worker_concurrency": 2,
                "worker_pool_type": "processes",
                "resource_requests": {"cpu": "500m", "memory": "1Gi"},
                "resource_limits": {"cpu": "2", "memory": "4Gi"}
            },
            UseCase.VIDEO_PROCESSING: {
                "task_timeout_seconds": 3600,  # 1 hour
                "worker_concurrency": 1,
                "worker_pool_type": "processes",
                "resource_requests": {"cpu": "1", "memory": "2Gi"},
                "resource_limits": {"cpu": "4", "memory": "8Gi"}
            },
            UseCase.ML_INFERENCE: {
                "task_timeout_seconds": 120,
                "worker_concurrency": 4,
                "enable_batch_processing": True,
                "batch_size": 32,
                "resource_requests": {"cpu": "1", "memory": "2Gi"}
            },
            UseCase.BATCH_JOBS: {
                "task_timeout_seconds": 7200,  # 2 hours
                "worker_concurrency": 1,
                "enable_periodic_tasks": True,
                "worker_pool_type": "processes"
            },
            UseCase.EVENT_PROCESSING: {
                "task_timeout_seconds": 10,
                "worker_concurrency": 16,
                "enable_exactly_once_delivery": True,
                "max_tasks_per_second": 1000
            },
            UseCase.WEB_SCRAPING: {
                "task_timeout_seconds": 180,
                "worker_concurrency": 8,
                "enable_rate_limiting": True,
                "max_tasks_per_second": 10,
                "task_retry_attempts": 5
            }
        }

        config = use_case_configs.get(self.use_case, {})
        for key, value in config.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Apply use case optimizations
                if isinstance(value, (int, float)) and value > current_value:
                    setattr(self, key, value)
                elif isinstance(value, bool) and value:
                    setattr(self, key, value)
                elif isinstance(value, str) and current_value in ["universal", "general"]:
                    setattr(self, key, value)
                elif isinstance(value, dict):
                    setattr(self, key, value)

    def _configure_deployment_optimizations(self):
        """Configure optimizations based on deployment type."""
        deployment_configs = {
            DeploymentType.KUBERNETES: {
                "health_check_endpoint": True,
                "monitoring_enabled": True,
                "enable_worker_monitoring": True,
                "scaling_strategy": ScalingStrategy.KUBERNETES_HPA
            },
            DeploymentType.DOCKER: {
                "health_check_endpoint": True,
                "container_image": "python:3.9-slim",
                "monitoring_enabled": True
            },
            DeploymentType.SERVERLESS: {
                "task_timeout_seconds": 900,  # 15 minutes max for most serverless
                "enable_worker_auto_shutdown": True,
                "cost_optimization_enabled": True,
                "worker_concurrency": 1
            },
            DeploymentType.CLOUD_FUNCTIONS: {
                "task_timeout_seconds": 540,  # 9 minutes for Cloud Functions
                "worker_concurrency": 1,
                "enable_worker_auto_shutdown": True,
                "cost_optimization_enabled": True
            },
            DeploymentType.LAMBDA: {
                "task_timeout_seconds": 900,  # 15 minutes for Lambda
                "worker_concurrency": 1,
                "cloud_provider": "aws",
                "cost_optimization_enabled": True
            },
            DeploymentType.DISTRIBUTED: {
                "distributed_workers": True,
                "enable_worker_monitoring": True,
                "monitoring_enabled": True,
                "scaling_strategy": ScalingStrategy.AUTO_QUEUE_LENGTH
            }
        }

        config = deployment_configs.get(self.deployment_type, {})
        for key, value in config.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Apply deployment optimizations
                if isinstance(value, bool) and value:
                    setattr(self, key, value)
                elif isinstance(value, (int, float)):
                    setattr(self, key, value)
                elif isinstance(value, str) and current_value in ["manual", "general", "universal"]:
                    setattr(self, key, value)

    def get_queue_config(self) -> Dict[str, Any]:
        """Get queue-specific configuration."""
        return {
            "queue_type": self.queue_type,
            "connection_url": self.queue_connection_url,
            "durability": self.queue_durability,
            "persistence": self.queue_persistence,
            "ttl_seconds": self.queue_ttl_seconds,
            "max_size": self.max_queue_size,
            "routing_enabled": self.enable_task_routing,
            "dead_letter_queue": self.dead_letter_queue,
            **self.advanced_config.get("queue", {})
        }

    def get_worker_config(self) -> Dict[str, Any]:
        """Get worker-specific configuration."""
        return {
            "worker_type": self.worker_type,
            "concurrency": self.worker_concurrency,
            "pool_type": self.worker_pool_type,
            "prefetch_multiplier": self.worker_prefetch_multiplier,
            "max_tasks_per_child": self.worker_max_tasks_per_child,
            "heartbeat_interval": self.worker_heartbeat_interval,
            "min_workers": self.min_workers,
            "max_workers": self.max_workers,
            **self.advanced_config.get("worker", {})
        }

    def get_task_config(self) -> Dict[str, Any]:
        """Get task processing configuration."""
        return {
            "timeout_seconds": self.task_timeout_seconds,
            "retry_attempts": self.task_retry_attempts,
            "retry_delay_seconds": self.task_retry_delay_seconds,
            "priority_levels": self.task_priority_levels,
            "serializer": self.task_serializer,
            "compression": self.enable_task_compression,
            "tracking": self.enable_task_tracking,
            **self.advanced_config.get("task", {})
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring and observability configuration."""
        return {
            "enabled": self.monitoring_enabled,
            "metrics_backend": self.metrics_backend,
            "worker_monitoring": self.enable_worker_monitoring,
            "queue_monitoring": self.enable_queue_monitoring,
            "task_tracking": self.enable_task_tracking,
            "health_check_endpoint": self.health_check_endpoint,
            "health_check_path": self.health_check_path,
            **self.advanced_config.get("monitoring", {})
        }

    def get_deployment_config(self) -> Dict[str, Any]:
        """Get deployment-specific configuration."""
        return {
            "deployment_type": self.deployment_type,
            "scaling_strategy": self.scaling_strategy,
            "distributed_workers": self.distributed_workers,
            "cloud_provider": self.cloud_provider,
            "cloud_region": self.cloud_region,
            "container_image": self.container_image,
            "kubernetes_namespace": self.kubernetes_namespace,
            "resource_requests": self.resource_requests,
            "resource_limits": self.resource_limits,
            **self.advanced_config.get("deployment", {})
        }

    def validate_configuration(self) -> List[str]:
        """Validate queue/worker configuration and return warnings/errors."""
        issues = []

        # Validate queue type and worker type compatibility
        if self.queue_type == QueueType.REDIS and self.worker_type not in [WorkerType.CELERY, WorkerType.RQ, WorkerType.ARQS]:
            issues.append(f"Worker type {self.worker_type} may not be compatible with Redis queue")

        # Validate timeout settings
        if self.task_timeout_seconds <= 0:
            issues.append("Task timeout must be positive")

        if self.task_retry_delay_seconds <= 0:
            issues.append("Retry delay must be positive")

        # Validate worker concurrency
        if self.worker_concurrency <= 0:
            issues.append("Worker concurrency must be positive")

        if self.worker_concurrency > 100:
            issues.append("High worker concurrency may cause resource issues")

        # Validate deployment specific settings
        if self.deployment_type == DeploymentType.SERVERLESS and self.task_timeout_seconds > 900:
            issues.append("Task timeout too high for serverless deployment (max 15 minutes)")

        if self.deployment_type == DeploymentType.LAMBDA and self.task_timeout_seconds > 900:
            issues.append("Task timeout too high for AWS Lambda (max 15 minutes)")

        # Validate scaling configuration
        if self.scaling_strategy != ScalingStrategy.MANUAL and not self.monitoring_enabled:
            issues.append("Auto-scaling requires monitoring to be enabled")

        # Validate cloud provider settings
        if self.cloud_provider and not self.cloud_region:
            issues.append("Cloud region must be specified when using cloud provider")

        # Validate resource limits
        if self.deployment_type == DeploymentType.KUBERNETES:
            cpu_request = self.resource_requests.get("cpu", "0")
            cpu_limit = self.resource_limits.get("cpu", "0")
            if cpu_request and cpu_limit and cpu_request > cpu_limit:
                issues.append("CPU request cannot be higher than CPU limit")

        return issues

    def get_supported_features(self) -> Dict[str, bool]:
        """Get supported features based on configuration."""
        features = {
            "periodic_tasks": self.enable_periodic_tasks,
            "task_routing": self.enable_task_routing,
            "rate_limiting": self.enable_rate_limiting,
            "batch_processing": self.enable_batch_processing,
            "dead_letter_queue": self.dead_letter_queue,
            "result_backend": self.enable_result_backend,
            "monitoring": self.monitoring_enabled,
            "auto_scaling": self.scaling_strategy != ScalingStrategy.MANUAL,
            "distributed": self.distributed_workers,
            "compression": self.enable_task_compression,
            "deduplication": self.enable_message_deduplication,
            "exactly_once": self.enable_exactly_once_delivery,
            "message_ordering": self.enable_message_ordering,
            "ssl": self.enable_ssl,
            "authentication": self.enable_authentication
        }

        return features