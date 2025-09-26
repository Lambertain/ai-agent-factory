"""
Universal Queue/Worker Management Agent Settings.

Configurable settings supporting multiple queue systems and deployment environments.
"""

import os
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class QueueWorkerAgentSettings(BaseSettings):
    """Universal settings for Queue/Worker Management Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== CORE LLM CONFIGURATION =====
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="LLM API key")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="LLM model name")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="LLM API base URL"
    )

    # ===== COST-OPTIMIZED MODEL CONFIGURATION =====
    # Queue architecture and complex distributed systems - Premium Qwen
    llm_architecture_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Model for queue architecture and distributed system design"
    )

    # Queue/worker implementation and configuration - Qwen Coder
    llm_implementation_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Model for queue/worker implementation and configuration"
    )

    # Documentation and deployment guides - Ultra-cheap Gemini
    llm_docs_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Model for documentation and deployment guides"
    )

    # Monitoring and debugging - Fast Qwen Coder
    llm_monitoring_model: str = Field(
        default="qwen2.5-coder-7b-instruct",
        description="Model for monitoring setup and debugging"
    )

    # Alternative API keys
    gemini_api_key: str = Field(..., description="Google Gemini API key")

    # ===== QUEUE/WORKER AGENT CONFIGURATION =====
    agent_name: str = Field(default="Queue/Worker Management Agent", description="Agent name")
    agent_version: str = Field(default="1.0.0", description="Agent version")

    # Default queue/worker settings
    default_queue_type: str = Field(default="redis", description="Default queue system")
    default_worker_type: str = Field(default="celery", description="Default worker type")
    default_use_case: str = Field(default="api_processing", description="Default use case")
    default_deployment: str = Field(default="standalone", description="Default deployment type")

    # ===== KNOWLEDGE BASE & RAG =====
    archon_url: str = Field(default="http://localhost:3737", description="Archon Knowledge Base URL")
    knowledge_base_enabled: bool = Field(default=True, description="Enable knowledge base integration")

    # Knowledge base configuration
    default_knowledge_tags: list[str] = Field(
        default_factory=lambda: ["queue-worker", "agent-knowledge", "pydantic-ai"],
        description="Default knowledge base tags"
    )

    # ===== PERFORMANCE SETTINGS =====
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout_seconds: int = Field(default=60, description="Request timeout in seconds")
    enable_caching: bool = Field(default=True, description="Enable response caching")

    # Rate limiting
    max_requests_per_minute: int = Field(default=60, description="Max requests per minute")
    max_requests_per_hour: int = Field(default=1000, description="Max requests per hour")

    # ===== DEVELOPMENT SETTINGS =====
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    enable_verbose_logging: bool = Field(default=False, description="Enable verbose logging")

    # Development features
    hot_reload: bool = Field(default=True, description="Enable hot reload")
    auto_save: bool = Field(default=True, description="Enable auto save")

    # ===== SECURITY SETTINGS =====
    enable_input_validation: bool = Field(default=True, description="Enable input validation")
    max_input_length: int = Field(default=10000, description="Maximum input length")
    sanitize_inputs: bool = Field(default=True, description="Sanitize user inputs")

    # Security defaults
    default_queue_authentication: bool = Field(default=False, description="Default queue authentication")
    default_ssl_enabled: bool = Field(default=False, description="Default SSL enablement")

    # ===== QUEUE SYSTEM DEFAULTS =====
    # Redis
    redis_default_url: str = Field(default="redis://localhost:6379/0", description="Default Redis URL")
    redis_connection_pool_size: int = Field(default=10, description="Redis connection pool size")
    redis_socket_timeout: int = Field(default=30, description="Redis socket timeout")

    # RabbitMQ
    rabbitmq_default_url: str = Field(default="amqp://guest:guest@localhost:5672//", description="Default RabbitMQ URL")
    rabbitmq_heartbeat: int = Field(default=600, description="RabbitMQ heartbeat interval")
    rabbitmq_blocked_connection_timeout: int = Field(default=300, description="RabbitMQ blocked connection timeout")

    # AWS SQS
    aws_sqs_region: str = Field(default="us-east-1", description="Default AWS SQS region")
    aws_sqs_visibility_timeout: int = Field(default=300, description="Default SQS visibility timeout")
    aws_sqs_message_retention: int = Field(default=345600, description="Default message retention (4 days)")

    # Azure Service Bus
    azure_servicebus_namespace: str = Field(default="", description="Azure Service Bus namespace")
    azure_servicebus_auth_timeout: int = Field(default=60, description="Azure Service Bus auth timeout")

    # Google Cloud Tasks
    gcp_project_id: str = Field(default="", description="Google Cloud project ID")
    gcp_location: str = Field(default="us-central1", description="Google Cloud location")
    gcp_tasks_timeout: int = Field(default=1800, description="Cloud Tasks timeout")

    # ===== WORKER SYSTEM DEFAULTS =====
    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/0", description="Default Celery broker")
    celery_result_backend: str = Field(default="redis://localhost:6379/0", description="Default Celery result backend")
    celery_worker_concurrency: int = Field(default=4, description="Default Celery worker concurrency")
    celery_task_serializer: str = Field(default="json", description="Default Celery task serializer")

    # RQ
    rq_connection_url: str = Field(default="redis://localhost:6379/0", description="Default RQ Redis connection")
    rq_default_timeout: int = Field(default=180, description="Default RQ job timeout")
    rq_worker_ttl: int = Field(default=420, description="Default RQ worker TTL")

    # Dramatiq
    dramatiq_broker_url: str = Field(default="redis://localhost:6379/0", description="Default Dramatiq broker")
    dramatiq_max_retries: int = Field(default=20, description="Default Dramatiq max retries")

    # ===== USE CASE DEFAULTS =====
    # API Processing
    api_processing_timeout: int = Field(default=30, description="API processing timeout")
    api_processing_concurrency: int = Field(default=8, description="API processing concurrency")
    api_processing_rate_limit: int = Field(default=100, description="API processing rate limit")

    # Data Pipeline
    data_pipeline_timeout: int = Field(default=1800, description="Data pipeline timeout")
    data_pipeline_concurrency: int = Field(default=4, description="Data pipeline concurrency")
    data_pipeline_batch_size: int = Field(default=100, description="Data pipeline batch size")

    # Email Sending
    email_sending_timeout: int = Field(default=60, description="Email sending timeout")
    email_sending_concurrency: int = Field(default=16, description="Email sending concurrency")
    email_sending_rate_limit: int = Field(default=1000, description="Email sending rate limit per minute")

    # File Processing
    file_processing_timeout: int = Field(default=600, description="File processing timeout")
    file_processing_concurrency: int = Field(default=2, description="File processing concurrency")

    # Image Processing
    image_processing_timeout: int = Field(default=300, description="Image processing timeout")
    image_processing_concurrency: int = Field(default=2, description="Image processing concurrency")

    # Video Processing
    video_processing_timeout: int = Field(default=3600, description="Video processing timeout")
    video_processing_concurrency: int = Field(default=1, description="Video processing concurrency")

    # ML Inference
    ml_inference_timeout: int = Field(default=120, description="ML inference timeout")
    ml_inference_concurrency: int = Field(default=4, description="ML inference concurrency")
    ml_inference_batch_size: int = Field(default=32, description="ML inference batch size")

    # ===== DEPLOYMENT DEFAULTS =====
    # Standalone
    standalone_max_workers: int = Field(default=10, description="Standalone max workers")
    standalone_monitoring: bool = Field(default=True, description="Standalone monitoring")

    # Docker
    docker_base_image: str = Field(default="python:3.9-slim", description="Default Docker base image")
    docker_health_check: bool = Field(default=True, description="Docker health check")

    # Kubernetes
    k8s_namespace: str = Field(default="default", description="Default Kubernetes namespace")
    k8s_resource_requests_cpu: str = Field(default="100m", description="Default CPU requests")
    k8s_resource_requests_memory: str = Field(default="128Mi", description="Default memory requests")
    k8s_resource_limits_cpu: str = Field(default="500m", description="Default CPU limits")
    k8s_resource_limits_memory: str = Field(default="512Mi", description="Default memory limits")

    # Serverless
    serverless_timeout: int = Field(default=900, description="Serverless function timeout")
    serverless_memory: int = Field(default=512, description="Serverless function memory MB")

    # ===== MONITORING DEFAULTS =====
    # Prometheus
    prometheus_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    prometheus_port: int = Field(default=8000, description="Prometheus metrics port")

    # Health checks
    health_check_interval: int = Field(default=30, description="Health check interval seconds")
    health_check_timeout: int = Field(default=5, description="Health check timeout seconds")

    # Alerting
    alert_webhook_url: Optional[str] = Field(default=None, description="Alert webhook URL")
    alert_on_queue_size: int = Field(default=1000, description="Alert when queue size exceeds")
    alert_on_failure_rate: float = Field(default=0.1, description="Alert when failure rate exceeds")

    # ===== TESTING CONFIGURATION =====
    enable_test_mode: bool = Field(default=True, description="Enable test mode")
    test_queue_prefix: str = Field(default="test_", description="Test queue prefix")
    test_worker_count: int = Field(default=2, description="Test worker count")

    # Testing features
    enable_queue_testing: bool = Field(default=True, description="Enable queue testing")
    test_task_timeout: int = Field(default=10, description="Test task timeout")

    # ===== ADVANCED CONFIGURATION =====
    # Experimental features
    enable_experimental_features: bool = Field(default=False, description="Enable experimental features")
    enable_auto_scaling: bool = Field(default=False, description="Enable auto-scaling")
    enable_cost_optimization: bool = Field(default=False, description="Enable cost optimization")

    # Performance optimization
    enable_performance_monitoring: bool = Field(default=True, description="Enable performance monitoring")
    enable_queue_optimization: bool = Field(default=True, description="Enable queue optimization")
    enable_worker_optimization: bool = Field(default=True, description="Enable worker optimization")

    # Integration settings
    enable_webhook_integration: bool = Field(default=True, description="Enable webhook integration")
    webhook_retry_attempts: int = Field(default=3, description="Webhook retry attempts")
    webhook_timeout: int = Field(default=30, description="Webhook timeout seconds")

    # ===== ENVIRONMENT PATHS =====
    project_root: str = Field(default=".", description="Project root directory")
    output_directory: str = Field(default="./generated", description="Output directory")
    backup_directory: str = Field(default="./backups", description="Backup directory")
    logs_directory: str = Field(default="./logs", description="Logs directory")
    config_directory: str = Field(default="./config", description="Configuration directory")


def load_settings() -> QueueWorkerAgentSettings:
    """
    Load queue/worker agent settings from environment variables and .env file.

    Returns:
        Configured QueueWorkerAgentSettings instance

    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    try:
        settings = QueueWorkerAgentSettings()

        # Validate critical settings
        if not settings.llm_api_key or settings.llm_api_key == "your_api_key_here":
            raise ValueError(
                "LLM_API_KEY is required. Please set it in your .env file or environment variables."
            )

        if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is required for cost optimization. Please set it in your .env file."
            )

        return settings

    except Exception as e:
        error_msg = f"Failed to load queue/worker agent settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nPlease ensure LLM_API_KEY is set in your .env file:"
            error_msg += "\nLLM_API_KEY=your_actual_api_key_here"
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "default") -> OpenAIModel:
    """
    Get cost-optimized LLM model based on task type.

    Args:
        task_type: Type of task (default, architecture, implementation, docs, monitoring)

    Returns:
        Configured OpenAI model instance
    """
    settings = load_settings()

    # Select model based on task type for cost optimization
    model_map = {
        "default": settings.llm_model,
        "architecture": settings.llm_architecture_model,
        "implementation": settings.llm_implementation_model,
        "docs": settings.llm_docs_model,
        "monitoring": settings.llm_monitoring_model,
    }

    model_name = model_map.get(task_type, settings.llm_model)

    # Configure provider based on model
    if model_name.startswith("gemini"):
        # Use Gemini for cost-effective tasks
        provider = OpenAIProvider(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.gemini_api_key
        )
    else:
        # Use Qwen for specialized tasks
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )

    return OpenAIModel(model_name, provider=provider)


def get_queue_specific_settings(queue_type: str) -> Dict[str, Any]:
    """
    Get queue system specific configuration settings.

    Args:
        queue_type: Queue system type

    Returns:
        Queue system specific settings dictionary
    """
    settings = load_settings()

    queue_settings = {
        "redis": {
            "connection_url": settings.redis_default_url,
            "connection_pool_size": settings.redis_connection_pool_size,
            "socket_timeout": settings.redis_socket_timeout,
            "supports_priority": True,
            "supports_delay": True,
            "supports_ttl": True,
            "supports_streams": True
        },
        "rabbitmq": {
            "connection_url": settings.rabbitmq_default_url,
            "heartbeat": settings.rabbitmq_heartbeat,
            "blocked_connection_timeout": settings.rabbitmq_blocked_connection_timeout,
            "supports_routing": True,
            "supports_durability": True,
            "supports_dead_letter": True,
            "supports_priority": True
        },
        "aws_sqs": {
            "region": settings.aws_sqs_region,
            "visibility_timeout": settings.aws_sqs_visibility_timeout,
            "message_retention": settings.aws_sqs_message_retention,
            "supports_fifo": True,
            "supports_dead_letter": True,
            "supports_delay": True,
            "managed_service": True
        },
        "azure_service_bus": {
            "namespace": settings.azure_servicebus_namespace,
            "auth_timeout": settings.azure_servicebus_auth_timeout,
            "supports_sessions": True,
            "supports_duplicate_detection": True,
            "supports_dead_letter": True,
            "managed_service": True
        },
        "google_cloud_tasks": {
            "project_id": settings.gcp_project_id,
            "location": settings.gcp_location,
            "timeout": settings.gcp_tasks_timeout,
            "supports_http_targets": True,
            "supports_rate_limiting": True,
            "managed_service": True
        },
        "celery": {
            "broker_url": settings.celery_broker_url,
            "result_backend": settings.celery_result_backend,
            "task_serializer": settings.celery_task_serializer,
            "supports_routing": True,
            "supports_periodic": True,
            "supports_canvas": True
        }
    }

    return queue_settings.get(queue_type, {})


def get_worker_specific_settings(worker_type: str) -> Dict[str, Any]:
    """
    Get worker system specific configuration settings.

    Args:
        worker_type: Worker system type

    Returns:
        Worker system specific settings dictionary
    """
    settings = load_settings()

    worker_settings = {
        "celery": {
            "default_concurrency": settings.celery_worker_concurrency,
            "broker_url": settings.celery_broker_url,
            "result_backend": settings.celery_result_backend,
            "supports_prefork": True,
            "supports_eventlet": True,
            "supports_gevent": True,
            "supports_monitoring": True
        },
        "rq": {
            "connection_url": settings.rq_connection_url,
            "default_timeout": settings.rq_default_timeout,
            "worker_ttl": settings.rq_worker_ttl,
            "supports_job_timeout": True,
            "supports_failed_queue": True,
            "simple_setup": True
        },
        "dramatiq": {
            "broker_url": settings.dramatiq_broker_url,
            "max_retries": settings.dramatiq_max_retries,
            "supports_middleware": True,
            "supports_rate_limiting": True,
            "supports_prometheus": True
        },
        "huey": {
            "supports_periodic": True,
            "supports_retry": True,
            "lightweight": True,
            "django_integration": True
        },
        "taskiq": {
            "supports_async": True,
            "supports_dependencies": True,
            "type_safe": True,
            "fastapi_integration": True
        },
        "arqs": {
            "supports_async": True,
            "redis_based": True,
            "simple_setup": True,
            "lightweight": True
        }
    }

    return worker_settings.get(worker_type, {})


def get_use_case_settings(use_case: str) -> Dict[str, Any]:
    """
    Get use case specific configuration settings.

    Args:
        use_case: Use case type

    Returns:
        Use case specific settings dictionary
    """
    settings = load_settings()

    use_case_settings = {
        "api_processing": {
            "timeout": settings.api_processing_timeout,
            "concurrency": settings.api_processing_concurrency,
            "rate_limit": settings.api_processing_rate_limit,
            "recommended_queues": ["redis", "rabbitmq"],
            "recommended_workers": ["celery", "rq"]
        },
        "data_pipeline": {
            "timeout": settings.data_pipeline_timeout,
            "concurrency": settings.data_pipeline_concurrency,
            "batch_size": settings.data_pipeline_batch_size,
            "recommended_queues": ["rabbitmq", "aws_sqs"],
            "recommended_workers": ["celery", "dramatiq"]
        },
        "email_sending": {
            "timeout": settings.email_sending_timeout,
            "concurrency": settings.email_sending_concurrency,
            "rate_limit": settings.email_sending_rate_limit,
            "recommended_queues": ["redis", "aws_sqs"],
            "recommended_workers": ["rq", "celery"]
        },
        "file_processing": {
            "timeout": settings.file_processing_timeout,
            "concurrency": settings.file_processing_concurrency,
            "recommended_queues": ["aws_sqs", "azure_service_bus"],
            "recommended_workers": ["celery", "dramatiq"]
        },
        "image_processing": {
            "timeout": settings.image_processing_timeout,
            "concurrency": settings.image_processing_concurrency,
            "cpu_intensive": True,
            "recommended_workers": ["celery", "rq"]
        },
        "video_processing": {
            "timeout": settings.video_processing_timeout,
            "concurrency": settings.video_processing_concurrency,
            "cpu_intensive": True,
            "memory_intensive": True,
            "recommended_workers": ["celery"]
        },
        "ml_inference": {
            "timeout": settings.ml_inference_timeout,
            "concurrency": settings.ml_inference_concurrency,
            "batch_size": settings.ml_inference_batch_size,
            "gpu_support": True,
            "recommended_workers": ["celery", "dramatiq"]
        }
    }

    return use_case_settings.get(use_case, {})


def get_deployment_settings(deployment_type: str) -> Dict[str, Any]:
    """
    Get deployment type specific configuration settings.

    Args:
        deployment_type: Deployment type

    Returns:
        Deployment specific settings dictionary
    """
    settings = load_settings()

    deployment_settings = {
        "standalone": {
            "max_workers": settings.standalone_max_workers,
            "monitoring": settings.standalone_monitoring,
            "simple_setup": True,
            "recommended_for": ["development", "small_scale"]
        },
        "docker": {
            "base_image": settings.docker_base_image,
            "health_check": settings.docker_health_check,
            "container_ready": True,
            "recommended_for": ["production", "ci_cd"]
        },
        "kubernetes": {
            "namespace": settings.k8s_namespace,
            "resource_requests": {
                "cpu": settings.k8s_resource_requests_cpu,
                "memory": settings.k8s_resource_requests_memory
            },
            "resource_limits": {
                "cpu": settings.k8s_resource_limits_cpu,
                "memory": settings.k8s_resource_limits_memory
            },
            "auto_scaling": True,
            "recommended_for": ["production", "enterprise"]
        },
        "serverless": {
            "timeout": settings.serverless_timeout,
            "memory": settings.serverless_memory,
            "cost_effective": True,
            "auto_scaling": True,
            "recommended_for": ["event_driven", "variable_load"]
        },
        "lambda": {
            "timeout": settings.serverless_timeout,
            "memory": settings.serverless_memory,
            "aws_native": True,
            "recommended_for": ["aws_ecosystem", "event_driven"]
        }
    }

    return deployment_settings.get(deployment_type, {})


# Convenience function to get settings
def get_settings() -> QueueWorkerAgentSettings:
    """Get queue/worker agent settings instance."""
    return load_settings()