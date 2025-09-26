"""
Serverless Configuration Example for Queue/Worker Management Agent.

Serverless configuration optimized for AWS Lambda, Google Cloud Functions,
Azure Functions, Vercel Functions, and other serverless environments.
"""

from ..dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType, ScalingStrategy

# Serverless Configuration
serverless_config = QueueWorkerDependencies(
    # LLM Configuration
    api_key="your_api_key_here",

    # Project Configuration
    project_path="/path/to/serverless/project",
    project_name="Serverless Queue Processing",

    # Queue Configuration - Cloud-native queues for serverless
    queue_type=QueueType.AWS_SQS,
    queue_connection_url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",

    # Worker Configuration - AsyncIO for serverless efficiency
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,  # Limited in serverless environments

    # Use Case Optimization
    use_case=UseCase.API_PROCESSING,
    domain_type="serverless",

    # Performance Settings
    max_queue_size=10000,
    retry_attempts=3,
    task_timeout=15,  # Serverless timeout limitations

    # Deployment Configuration
    deployment_type=DeploymentType.SERVERLESS,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,

    # Serverless-specific optimizations
    enable_cold_start_optimization=True,
    enable_connection_pooling=True,
    enable_lambda_warmer=True,

    # Monitoring optimized for serverless
    enable_metrics=True,
    enable_xray_tracing=True
)

# Alternative configurations for different serverless scenarios

# AWS Lambda Configuration
aws_lambda_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.AWS_SQS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.API_PROCESSING,
    domain_type="aws_lambda",
    deployment_type=DeploymentType.LAMBDA,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    max_queue_size=5000,
    task_timeout=15,  # Lambda max timeout (15 minutes)
    enable_lambda_layers=True,
    enable_vpc_support=True,
    enable_dead_letter_queue=True
)

# Google Cloud Functions Configuration
gcp_functions_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.GOOGLE_CLOUD_TASKS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.EVENT_PROCESSING,
    domain_type="gcp_functions",
    deployment_type=DeploymentType.CLOUD_FUNCTIONS,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=3000,
    task_timeout=9,  # Cloud Functions timeout (9 minutes)
    enable_pubsub_integration=True,
    enable_cloud_logging=True
)

# Azure Functions Configuration
azure_functions_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.AZURE_SERVICE_BUS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.API_PROCESSING,
    domain_type="azure_functions",
    deployment_type=DeploymentType.CLOUD_FUNCTIONS,
    scaling_strategy=ScalingStrategy.AUTO_CPU,
    max_queue_size=4000,
    task_timeout=10,  # Azure Functions timeout
    enable_app_insights=True,
    enable_cosmos_integration=True
)

# Vercel Functions Configuration
vercel_functions_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,  # External Redis for Vercel
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.API_PROCESSING,
    domain_type="vercel",
    deployment_type=DeploymentType.SERVERLESS,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=1000,
    task_timeout=5,  # Vercel Edge timeout (5 seconds)
    enable_edge_runtime=True,
    enable_vercel_analytics=True
)

# Netlify Functions Configuration
netlify_functions_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.API_PROCESSING,
    domain_type="netlify",
    deployment_type=DeploymentType.SERVERLESS,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=800,
    task_timeout=10,  # Netlify Functions timeout
    enable_background_functions=True,
    enable_netlify_analytics=True
)

# Cloudflare Workers Configuration
cloudflare_workers_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,  # External queue for Workers
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=1,
    use_case=UseCase.API_PROCESSING,
    domain_type="cloudflare_workers",
    deployment_type=DeploymentType.SERVERLESS,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=500,
    task_timeout=1,  # Workers very short timeout
    enable_durable_objects=True,
    enable_kv_storage=True
)

# Serverless Container Configuration (Cloud Run, Container Instances)
serverless_container_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.GOOGLE_CLOUD_TASKS,
    worker_type=WorkerType.CELERY,  # Can use more complex workers
    worker_concurrency=2,
    use_case=UseCase.DATA_PIPELINE,
    domain_type="serverless_container",
    deployment_type=DeploymentType.CLOUD_RUN,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=8000,
    task_timeout=60,  # Longer timeout for containers
    enable_container_optimization=True,
    enable_autoscaling=True
)

# Example usage configurations
EXAMPLE_CONFIGS = {
    "serverless": serverless_config,
    "aws_lambda": aws_lambda_config,
    "gcp_functions": gcp_functions_config,
    "azure_functions": azure_functions_config,
    "vercel": vercel_functions_config,
    "netlify": netlify_functions_config,
    "cloudflare_workers": cloudflare_workers_config,
    "serverless_container": serverless_container_config
}

def get_serverless_config(config_name: str = "serverless") -> QueueWorkerDependencies:
    """
    Get predefined serverless configuration.

    Args:
        config_name: Name of configuration to use

    Returns:
        QueueWorkerDependencies: Configuration for the specified serverless platform
    """
    if config_name not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(EXAMPLE_CONFIGS.keys())}")

    return EXAMPLE_CONFIGS[config_name]

# Usage examples:
if __name__ == "__main__":
    # Standard serverless setup
    config = get_serverless_config("serverless")
    print(f"Queue: {config.queue_type}, Worker: {config.worker_type}")

    # AWS Lambda for image processing
    image_lambda_config = get_serverless_config("aws_lambda")
    image_lambda_config.use_case = UseCase.IMAGE_PROCESSING
    image_lambda_config.project_name = "Serverless Image Processing"

    # Vercel API for SaaS product
    saas_vercel_config = get_serverless_config("vercel")
    saas_vercel_config.domain_type = "saas_api"
    saas_vercel_config.project_name = "SaaS API Backend"

    # Google Cloud Functions for IoT data
    iot_gcp_config = get_serverless_config("gcp_functions")
    iot_gcp_config.use_case = UseCase.EVENT_PROCESSING
    iot_gcp_config.domain_type = "iot_data"
    iot_gcp_config.project_name = "IoT Data Processing"