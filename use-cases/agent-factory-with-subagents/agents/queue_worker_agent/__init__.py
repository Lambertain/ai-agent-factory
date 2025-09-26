"""
Universal Queue/Worker Management Agent for Pydantic AI.

Comprehensive AI agent for queue systems and worker management supporting multiple
queue backends (Redis, RabbitMQ, AWS SQS, Azure Service Bus, Google Cloud Tasks)
and worker architectures (Celery, RQ, Dramatiq, Huey, TaskiQ, ARQS).

Features:
- Universal queue system support (6+ queue backends)
- Multiple worker architectures (6+ worker types)
- Use case optimizations (API processing, data pipelines, email, file processing, etc.)
- Deployment flexibility (standalone, Docker, Kubernetes, serverless)
- Auto-scaling and performance optimization
- Comprehensive monitoring and alerting
- Production-ready configurations
"""

from .agent import (
    queue_worker_agent,
    get_queue_worker_agent,
    run_queue_worker_agent,
    create_queue_system,
    submit_background_task,
    check_task_progress,
    get_system_statistics,
    scale_workers,
    get_configuration_analysis,
    create_api_processing_agent,
    create_data_pipeline_agent,
    create_email_service_agent,
    create_file_processing_agent,
    create_ml_inference_agent,
    create_serverless_agent
)
from .dependencies import (
    QueueWorkerDependencies,
    QueueType,
    WorkerType,
    UseCase,
    DeploymentType,
    ScalingStrategy
)
from .settings import (
    QueueWorkerAgentSettings,
    load_settings,
    get_settings,
    get_llm_model,
    get_queue_specific_settings,
    get_worker_specific_settings,
    get_use_case_settings,
    get_deployment_settings
)
from .tools import (
    search_queue_knowledge,
    create_task_queue,
    submit_task,
    get_task_status,
    get_queue_statistics,
    manage_workers,
    validate_queue_configuration,
    TaskDefinition,
    TaskResult,
    QueueStats,
    WorkerInfo
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__license__ = "MIT"

# Supported queue systems
SUPPORTED_QUEUE_TYPES = [
    "redis",
    "rabbitmq",
    "aws_sqs",
    "azure_service_bus",
    "google_cloud_tasks",
    "celery"
]

# Supported worker types
SUPPORTED_WORKER_TYPES = [
    "celery",
    "rq",
    "dramatiq",
    "huey",
    "taskiq",
    "arqs",
    "worker_threads",
    "asyncio_workers",
    "multiprocessing"
]

# Supported use cases
SUPPORTED_USE_CASES = [
    "api_processing",
    "data_pipeline",
    "email_sending",
    "file_processing",
    "image_processing",
    "video_processing",
    "ml_inference",
    "batch_jobs",
    "cron_jobs",
    "event_processing",
    "notification_service",
    "web_scraping",
    "report_generation",
    "data_sync",
    "backup_tasks"
]

# Supported deployment types
SUPPORTED_DEPLOYMENT_TYPES = [
    "standalone",
    "distributed",
    "kubernetes",
    "docker",
    "serverless",
    "cloud_functions",
    "lambda",
    "cloud_run"
]

# Supported scaling strategies
SUPPORTED_SCALING_STRATEGIES = [
    "manual",
    "auto_cpu",
    "auto_memory",
    "auto_queue_length",
    "auto_latency",
    "kubernetes_hpa",
    "docker_swarm",
    "custom"
]

__all__ = [
    # Agent functions
    "queue_worker_agent",
    "get_queue_worker_agent",
    "run_queue_worker_agent",
    "create_queue_system",
    "submit_background_task",
    "check_task_progress",
    "get_system_statistics",
    "scale_workers",
    "get_configuration_analysis",

    # Use case specific agents
    "create_api_processing_agent",
    "create_data_pipeline_agent",
    "create_email_service_agent",
    "create_file_processing_agent",
    "create_ml_inference_agent",
    "create_serverless_agent",

    # Dependencies and enums
    "QueueWorkerDependencies",
    "QueueType",
    "WorkerType",
    "UseCase",
    "DeploymentType",
    "ScalingStrategy",

    # Settings
    "QueueWorkerAgentSettings",
    "load_settings",
    "get_settings",
    "get_llm_model",
    "get_queue_specific_settings",
    "get_worker_specific_settings",
    "get_use_case_settings",
    "get_deployment_settings",

    # Tools and models
    "search_queue_knowledge",
    "create_task_queue",
    "submit_task",
    "get_task_status",
    "get_queue_statistics",
    "manage_workers",
    "validate_queue_configuration",
    "TaskDefinition",
    "TaskResult",
    "QueueStats",
    "WorkerInfo",

    # Constants
    "SUPPORTED_QUEUE_TYPES",
    "SUPPORTED_WORKER_TYPES",
    "SUPPORTED_USE_CASES",
    "SUPPORTED_DEPLOYMENT_TYPES",
    "SUPPORTED_SCALING_STRATEGIES"
]