"""
Data Pipeline Configuration Example for Queue/Worker Management Agent.

Batch processing configuration optimized for ETL operations, data transformation,
analytics processing, and large-scale data synchronization.
"""

from ..dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType, ScalingStrategy

# Data Pipeline Configuration
data_pipeline_config = QueueWorkerDependencies(
    # LLM Configuration
    api_key="your_api_key_here",

    # Project Configuration
    project_path="/path/to/data/project",
    project_name="Enterprise Data Pipeline",

    # Queue Configuration - RabbitMQ for reliable batch processing
    queue_type=QueueType.RABBITMQ,
    queue_connection_url="amqp://guest:guest@localhost:5672//",

    # Worker Configuration - Celery for complex workflows
    worker_type=WorkerType.CELERY,
    worker_concurrency=4,  # Lower concurrency for resource-intensive tasks

    # Use Case Optimization
    use_case=UseCase.DATA_PIPELINE,
    domain_type="data_processing",

    # Performance Settings
    max_queue_size=50000,
    retry_attempts=5,  # Higher retry for data reliability
    task_timeout=1800,  # 30 minutes for complex data processing

    # Deployment Configuration
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,

    # Data pipeline specific optimizations
    enable_batch_processing=True,
    enable_data_validation=True,
    enable_checkpoint_recovery=True,

    # Monitoring for data quality
    enable_metrics=True,
    enable_data_lineage=True,
    alert_on_data_quality=True
)

# Alternative configurations for different data scenarios

# ETL Processing (Extract, Transform, Load)
etl_processing_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,
    worker_type=WorkerType.CELERY,
    worker_concurrency=6,
    use_case=UseCase.DATA_PIPELINE,
    domain_type="etl_processing",
    deployment_type=DeploymentType.STANDALONE,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=25000,
    task_timeout=3600,  # 1 hour for ETL jobs
    enable_workflow_orchestration=True,
    enable_data_partitioning=True
)

# Real-time Stream Processing (Kafka, Kinesis)
stream_processing_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,  # Fast processing for streams
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=8,
    use_case=UseCase.DATA_PIPELINE,
    domain_type="stream_processing",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    max_queue_size=100000,
    task_timeout=30,  # Short timeout for stream processing
    enable_stream_windowing=True,
    enable_backpressure_handling=True
)

# Big Data Analytics (Spark, Hadoop ecosystem)
big_data_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,
    worker_type=WorkerType.CELERY,
    worker_concurrency=2,  # Very resource-intensive
    use_case=UseCase.DATA_PIPELINE,
    domain_type="big_data_analytics",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_CPU,
    max_queue_size=10000,
    task_timeout=7200,  # 2 hours for big data jobs
    enable_distributed_processing=True,
    enable_resource_management=True
)

# Machine Learning Pipeline
ml_pipeline_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,
    worker_concurrency=3,
    use_case=UseCase.ML_INFERENCE,
    domain_type="ml_pipeline",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=5000,
    task_timeout=1200,  # 20 minutes for ML training
    enable_model_versioning=True,
    enable_experiment_tracking=True,
    enable_gpu_support=True
)

# Data Warehouse Sync (Snowflake, BigQuery, Redshift)
warehouse_sync_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.AWS_SQS,  # Cloud-native for warehouse sync
    worker_type=WorkerType.DRAMATIQ,
    worker_concurrency=4,
    use_case=UseCase.DATA_SYNC,
    domain_type="data_warehouse",
    deployment_type=DeploymentType.CLOUD_FUNCTIONS,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    max_queue_size=20000,
    task_timeout=600,  # 10 minutes for warehouse operations
    enable_incremental_sync=True,
    enable_schema_evolution=True
)

# IoT Data Processing
iot_processing_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.AZURE_SERVICE_BUS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=12,
    use_case=UseCase.EVENT_PROCESSING,
    domain_type="iot_data",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=500000,  # Very high volume
    task_timeout=10,  # Fast IoT processing
    enable_time_series_optimization=True,
    enable_anomaly_detection=True
)

# Example usage configurations
EXAMPLE_CONFIGS = {
    "data_pipeline": data_pipeline_config,
    "etl_processing": etl_processing_config,
    "stream_processing": stream_processing_config,
    "big_data": big_data_config,
    "ml_pipeline": ml_pipeline_config,
    "warehouse_sync": warehouse_sync_config,
    "iot_processing": iot_processing_config
}

def get_data_config(config_name: str = "data_pipeline") -> QueueWorkerDependencies:
    """
    Get predefined data pipeline configuration.

    Args:
        config_name: Name of configuration to use

    Returns:
        QueueWorkerDependencies: Configuration for the specified data use case
    """
    if config_name not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(EXAMPLE_CONFIGS.keys())}")

    return EXAMPLE_CONFIGS[config_name]

# Usage examples:
if __name__ == "__main__":
    # Standard data pipeline
    config = get_data_config("data_pipeline")
    print(f"Queue: {config.queue_type}, Worker: {config.worker_type}")

    # E-commerce analytics pipeline
    analytics_config = get_data_config("big_data")
    analytics_config.domain_type = "ecommerce_analytics"
    analytics_config.project_name = "E-commerce Analytics Pipeline"

    # Financial data processing
    fintech_config = get_data_config("stream_processing")
    fintech_config.domain_type = "financial_data"
    fintech_config.project_name = "Financial Data Stream Processing"

    # Healthcare data pipeline
    healthcare_config = get_data_config("etl_processing")
    healthcare_config.domain_type = "healthcare"
    healthcare_config.project_name = "Healthcare Data ETL"