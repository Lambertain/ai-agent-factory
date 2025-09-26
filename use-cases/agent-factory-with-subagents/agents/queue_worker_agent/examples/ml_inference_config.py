"""
ML Inference Configuration Example for Queue/Worker Management Agent.

Machine learning inference configuration optimized for model serving,
batch prediction, real-time inference, and GPU-accelerated processing.
"""

from ..dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType, ScalingStrategy

# ML Inference Configuration
ml_inference_config = QueueWorkerDependencies(
    # LLM Configuration
    api_key="your_api_key_here",

    # Project Configuration
    project_path="/path/to/ml/project",
    project_name="ML Inference Service",

    # Queue Configuration - Redis for fast inference requests
    queue_type=QueueType.REDIS,
    queue_connection_url="redis://localhost:6379/2",  # Separate DB for ML

    # Worker Configuration - Celery for ML pipeline management
    worker_type=WorkerType.CELERY,
    worker_concurrency=4,  # GPU-limited concurrency

    # Use Case Optimization
    use_case=UseCase.ML_INFERENCE,
    domain_type="ml_inference",

    # Performance Settings
    max_queue_size=20000,
    retry_attempts=2,  # Lower retry for ML tasks
    task_timeout=120,  # 2 minutes for inference

    # Deployment Configuration
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,

    # ML-specific optimizations
    enable_gpu_support=True,
    enable_model_caching=True,
    enable_batch_inference=True,
    enable_model_versioning=True,

    # Monitoring for ML
    enable_metrics=True,
    enable_inference_tracking=True,
    alert_on_model_drift=True
)

# Alternative configurations for different ML scenarios

# Real-time Inference (chat bots, recommendation engines)
realtime_inference_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,  # Simpler for real-time
    worker_concurrency=8,
    use_case=UseCase.ML_INFERENCE,
    domain_type="realtime_inference",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=5000,
    task_timeout=5,  # Very fast inference
    enable_model_warming=True,
    enable_edge_caching=True,
    enable_a_b_testing=True
)

# Batch Prediction (large datasets, overnight processing)
batch_prediction_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,  # Reliable for large batches
    worker_type=WorkerType.CELERY,
    worker_concurrency=2,  # Resource-intensive batch jobs
    use_case=UseCase.ML_INFERENCE,
    domain_type="batch_prediction",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_CPU,
    max_queue_size=50000,
    task_timeout=3600,  # 1 hour for large batches
    enable_distributed_processing=True,
    enable_checkpoint_recovery=True,
    enable_result_aggregation=True
)

# Computer Vision Inference (image/video processing)
computer_vision_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.DRAMATIQ,
    worker_concurrency=3,  # GPU memory limited
    use_case=UseCase.IMAGE_PROCESSING,
    domain_type="computer_vision",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=15000,
    task_timeout=300,  # 5 minutes for vision tasks
    enable_gpu_optimization=True,
    enable_image_preprocessing=True,
    enable_result_visualization=True
)

# NLP Inference (text processing, sentiment analysis)
nlp_inference_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,
    worker_concurrency=6,
    use_case=UseCase.ML_INFERENCE,
    domain_type="nlp_inference",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    max_queue_size=25000,
    task_timeout=60,  # 1 minute for NLP
    enable_text_preprocessing=True,
    enable_language_detection=True,
    enable_entity_extraction=True
)

# Time Series Forecasting
time_series_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,
    worker_type=WorkerType.CELERY,
    worker_concurrency=3,
    use_case=UseCase.ML_INFERENCE,
    domain_type="time_series",
    deployment_type=DeploymentType.STANDALONE,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=10000,
    task_timeout=600,  # 10 minutes for forecasting
    enable_data_validation=True,
    enable_trend_analysis=True,
    enable_seasonality_detection=True
)

# Edge ML Inference (IoT devices, mobile)
edge_inference_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.ASYNCIO_WORKERS,
    worker_concurrency=4,
    use_case=UseCase.ML_INFERENCE,
    domain_type="edge_inference",
    deployment_type=DeploymentType.STANDALONE,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=2000,
    task_timeout=10,  # Very fast for edge
    enable_model_quantization=True,
    enable_lightweight_models=True,
    enable_offline_inference=True
)

# Federated Learning Coordination
federated_learning_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,
    worker_type=WorkerType.CELERY,
    worker_concurrency=2,
    use_case=UseCase.ML_INFERENCE,
    domain_type="federated_learning",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=5000,
    task_timeout=1800,  # 30 minutes for FL rounds
    enable_secure_aggregation=True,
    enable_differential_privacy=True,
    enable_client_selection=True
)

# Example usage configurations
EXAMPLE_CONFIGS = {
    "ml_inference": ml_inference_config,
    "realtime": realtime_inference_config,
    "batch_prediction": batch_prediction_config,
    "computer_vision": computer_vision_config,
    "nlp": nlp_inference_config,
    "time_series": time_series_config,
    "edge": edge_inference_config,
    "federated_learning": federated_learning_config
}

def get_ml_config(config_name: str = "ml_inference") -> QueueWorkerDependencies:
    """
    Get predefined ML inference configuration.

    Args:
        config_name: Name of configuration to use

    Returns:
        QueueWorkerDependencies: Configuration for the specified ML use case
    """
    if config_name not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(EXAMPLE_CONFIGS.keys())}")

    return EXAMPLE_CONFIGS[config_name]

# Usage examples:
if __name__ == "__main__":
    # Standard ML inference
    config = get_ml_config("ml_inference")
    print(f"Queue: {config.queue_type}, Worker: {config.worker_type}")

    # E-commerce recommendation engine
    recommendation_config = get_ml_config("realtime")
    recommendation_config.domain_type = "ecommerce_recommendations"
    recommendation_config.project_name = "Product Recommendation Engine"

    # Healthcare image analysis
    medical_cv_config = get_ml_config("computer_vision")
    medical_cv_config.domain_type = "medical_imaging"
    medical_cv_config.project_name = "Medical Image Analysis"

    # Financial fraud detection
    fraud_config = get_ml_config("realtime")
    fraud_config.domain_type = "fraud_detection"
    fraud_config.project_name = "Real-time Fraud Detection"

    # Social media sentiment analysis
    sentiment_config = get_ml_config("nlp")
    sentiment_config.domain_type = "social_media_analytics"
    sentiment_config.project_name = "Social Media Sentiment Analysis"