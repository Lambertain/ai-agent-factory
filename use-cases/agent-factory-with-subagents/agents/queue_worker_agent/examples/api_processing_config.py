"""
API Processing Configuration Example for Queue/Worker Management Agent.

High-performance queue configuration optimized for REST API request processing,
webhook handling, and real-time data synchronization.
"""

from ..dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType, ScalingStrategy

# API Processing Configuration
api_processing_config = QueueWorkerDependencies(
    # LLM Configuration
    api_key="your_api_key_here",

    # Project Configuration
    project_path="/path/to/api/project",
    project_name="High-Performance API Backend",

    # Queue Configuration - Redis for low latency
    queue_type=QueueType.REDIS,
    queue_connection_url="redis://localhost:6379/0",

    # Worker Configuration - Celery for reliability
    worker_type=WorkerType.CELERY,
    worker_concurrency=8,  # High concurrency for API requests

    # Use Case Optimization
    use_case=UseCase.API_PROCESSING,
    domain_type="api_backend",

    # Performance Settings
    max_queue_size=10000,
    retry_attempts=3,
    task_timeout=30,  # Short timeout for API requests

    # Deployment Configuration
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,

    # API-specific optimizations
    enable_priority_queues=True,
    enable_result_caching=True,
    enable_rate_limiting=True,

    # Monitoring
    enable_metrics=True,
    alert_on_queue_size=1000,
    alert_on_failure_rate=0.05
)

# Alternative configurations for different API scenarios

# High-Volume API Processing (e-commerce, social media)
high_volume_api_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.CELERY,
    worker_concurrency=16,
    use_case=UseCase.API_PROCESSING,
    domain_type="high_volume_api",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_CPU,
    max_queue_size=50000,
    task_timeout=15,
    enable_auto_scaling=True
)

# Real-time API Processing (chat, gaming, IoT)
realtime_api_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,  # RQ for simplicity in real-time
    worker_concurrency=4,
    use_case=UseCase.API_PROCESSING,
    domain_type="realtime_api",
    deployment_type=DeploymentType.STANDALONE,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=5000,
    task_timeout=5,  # Very short timeout
    enable_priority_queues=True
)

# Webhook Processing (GitHub, Stripe, third-party integrations)
webhook_processing_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,  # Reliable delivery for webhooks
    worker_type=WorkerType.CELERY,
    worker_concurrency=6,
    use_case=UseCase.EVENT_PROCESSING,
    domain_type="webhook_processing",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=20000,
    task_timeout=60,
    retry_attempts=5,  # High retry for webhook reliability
    enable_dlq=True  # Dead letter queue for failed webhooks
)

# Microservices API Gateway
microservices_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.DRAMATIQ,
    worker_concurrency=12,
    use_case=UseCase.API_PROCESSING,
    domain_type="microservices",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.KUBERNETES_HPA,
    max_queue_size=15000,
    task_timeout=45,
    enable_circuit_breaker=True,
    enable_load_balancing=True
)

# Serverless API Processing (AWS Lambda, Vercel, Netlify)
serverless_api_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.AWS_SQS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=2,  # Limited in serverless
    use_case=UseCase.API_PROCESSING,
    domain_type="serverless_api",
    deployment_type=DeploymentType.SERVERLESS,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=1000,
    task_timeout=10,  # Short timeout for serverless
    enable_cold_start_optimization=True
)

# Example usage configurations
EXAMPLE_CONFIGS = {
    "api_processing": api_processing_config,
    "high_volume_api": high_volume_api_config,
    "realtime_api": realtime_api_config,
    "webhook_processing": webhook_processing_config,
    "microservices": microservices_config,
    "serverless_api": serverless_api_config
}

def get_api_config(config_name: str = "api_processing") -> QueueWorkerDependencies:
    """
    Get predefined API processing configuration.

    Args:
        config_name: Name of configuration to use

    Returns:
        QueueWorkerDependencies: Configuration for the specified API use case
    """
    if config_name not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(EXAMPLE_CONFIGS.keys())}")

    return EXAMPLE_CONFIGS[config_name]

# Usage examples:
if __name__ == "__main__":
    # Standard API processing
    config = get_api_config("api_processing")
    print(f"Queue: {config.queue_type}, Worker: {config.worker_type}")

    # High-volume e-commerce API
    ecommerce_config = get_api_config("high_volume_api")
    ecommerce_config.domain_type = "ecommerce"
    ecommerce_config.project_name = "E-commerce API"

    # Real-time chat API
    chat_config = get_api_config("realtime_api")
    chat_config.domain_type = "chat_api"
    chat_config.project_name = "Real-time Chat Service"