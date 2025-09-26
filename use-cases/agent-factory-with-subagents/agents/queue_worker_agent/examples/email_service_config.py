"""
Email Service Configuration Example for Queue/Worker Management Agent.

Email processing configuration optimized for bulk email sending,
newsletter distribution, transactional emails, and notification services.
"""

from ..dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType, ScalingStrategy

# Email Service Configuration
email_service_config = QueueWorkerDependencies(
    # LLM Configuration
    api_key="your_api_key_here",

    # Project Configuration
    project_path="/path/to/email/project",
    project_name="Enterprise Email Service",

    # Queue Configuration - Redis for email queue management
    queue_type=QueueType.REDIS,
    queue_connection_url="redis://localhost:6379/1",  # Separate DB for emails

    # Worker Configuration - Celery for email reliability
    worker_type=WorkerType.CELERY,
    worker_concurrency=16,  # High concurrency for email sending

    # Use Case Optimization
    use_case=UseCase.EMAIL_SENDING,
    domain_type="email_service",

    # Performance Settings
    max_queue_size=100000,  # Large queue for bulk emails
    retry_attempts=3,
    task_timeout=60,  # 1 minute for email sending

    # Deployment Configuration
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,

    # Email-specific optimizations
    enable_rate_limiting=True,
    enable_bounce_handling=True,
    enable_delivery_tracking=True,
    enable_template_caching=True,

    # Monitoring
    enable_metrics=True,
    alert_on_bounce_rate=0.05,
    alert_on_queue_size=50000
)

# Alternative configurations for different email scenarios

# Transactional Email Service (order confirmations, password resets)
transactional_email_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,  # Simpler for transactional
    worker_concurrency=8,
    use_case=UseCase.EMAIL_SENDING,
    domain_type="transactional_email",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.AUTO_LATENCY,
    max_queue_size=20000,
    task_timeout=30,  # Fast delivery for transactional
    enable_priority_queues=True,  # High priority for transactional
    enable_real_time_tracking=True
)

# Newsletter and Marketing Emails
newsletter_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,  # Reliable for large campaigns
    worker_type=WorkerType.CELERY,
    worker_concurrency=20,
    use_case=UseCase.EMAIL_SENDING,
    domain_type="newsletter",
    deployment_type=DeploymentType.STANDALONE,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=500000,  # Very large for campaigns
    task_timeout=120,
    enable_campaign_scheduling=True,
    enable_a_b_testing=True,
    enable_segmentation=True
)

# Notification Service (alerts, updates, reminders)
notification_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.DRAMATIQ,
    worker_concurrency=12,
    use_case=UseCase.NOTIFICATION_SERVICE,
    domain_type="notifications",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.AUTO_CPU,
    max_queue_size=50000,
    task_timeout=45,
    enable_multi_channel=True,  # Email, SMS, push notifications
    enable_preference_management=True,
    enable_throttling=True
)

# E-commerce Email Service
ecommerce_email_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.CELERY,
    worker_concurrency=14,
    use_case=UseCase.EMAIL_SENDING,
    domain_type="ecommerce",
    deployment_type=DeploymentType.DOCKER,
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    max_queue_size=75000,
    task_timeout=90,
    enable_abandoned_cart_recovery=True,
    enable_order_tracking=True,
    enable_personalization=True
)

# SaaS Product Email Service
saas_email_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.REDIS,
    worker_type=WorkerType.RQ,
    worker_concurrency=10,
    use_case=UseCase.EMAIL_SENDING,
    domain_type="saas_product",
    deployment_type=DeploymentType.CLOUD_FUNCTIONS,
    scaling_strategy=ScalingStrategy.AUTO_MEMORY,
    max_queue_size=30000,
    task_timeout=60,
    enable_user_onboarding=True,
    enable_feature_announcements=True,
    enable_usage_analytics=True
)

# Healthcare Email Service (HIPAA compliant)
healthcare_email_config = QueueWorkerDependencies(
    api_key="your_api_key_here",
    queue_type=QueueType.RABBITMQ,  # Secure and reliable
    worker_type=WorkerType.CELERY,
    worker_concurrency=6,  # Lower for security processing
    use_case=UseCase.EMAIL_SENDING,
    domain_type="healthcare",
    deployment_type=DeploymentType.KUBERNETES,
    scaling_strategy=ScalingStrategy.MANUAL,
    max_queue_size=15000,
    task_timeout=120,
    enable_encryption=True,
    enable_audit_logging=True,
    enable_consent_management=True
)

# Example usage configurations
EXAMPLE_CONFIGS = {
    "email_service": email_service_config,
    "transactional": transactional_email_config,
    "newsletter": newsletter_config,
    "notifications": notification_config,
    "ecommerce": ecommerce_email_config,
    "saas": saas_email_config,
    "healthcare": healthcare_email_config
}

def get_email_config(config_name: str = "email_service") -> QueueWorkerDependencies:
    """
    Get predefined email service configuration.

    Args:
        config_name: Name of configuration to use

    Returns:
        QueueWorkerDependencies: Configuration for the specified email use case
    """
    if config_name not in EXAMPLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(EXAMPLE_CONFIGS.keys())}")

    return EXAMPLE_CONFIGS[config_name]

# Usage examples:
if __name__ == "__main__":
    # Standard email service
    config = get_email_config("email_service")
    print(f"Queue: {config.queue_type}, Worker: {config.worker_type}")

    # E-commerce abandoned cart emails
    cart_config = get_email_config("ecommerce")
    cart_config.project_name = "Abandoned Cart Recovery Service"

    # SaaS onboarding emails
    onboarding_config = get_email_config("saas")
    onboarding_config.project_name = "User Onboarding Email Sequence"

    # Emergency alert notifications
    alert_config = get_email_config("notifications")
    alert_config.project_name = "Emergency Alert System"
    alert_config.enable_priority_queues = True