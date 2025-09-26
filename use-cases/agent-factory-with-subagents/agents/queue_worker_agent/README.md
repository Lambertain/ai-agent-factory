# Universal Queue/Worker Management Agent for Pydantic AI

A comprehensive AI agent for designing, configuring, and optimizing queue systems and worker architectures. Supports 6+ queue backends, 9+ worker types, and 15+ use cases with universal adaptability.

## 🚀 Features

### Universal Queue System Support
- **Redis** - High performance, low latency
- **RabbitMQ** - Enterprise reliability, complex routing
- **AWS SQS** - Cloud-native, auto-scaling
- **Azure Service Bus** - Enterprise integration
- **Google Cloud Tasks** - Serverless-first approach
- **Celery** - Distributed task processing

### Multiple Worker Architectures
- **Celery** - Full-featured distributed system
- **RQ** - Simple and reliable Python queues
- **Dramatiq** - Modern Python task processing
- **Huey** - Lightweight task scheduler
- **TaskiQ** - Async-first Python framework
- **ARQS** - Redis-based async workers
- **AsyncIO Workers** - High-concurrency processing
- **Multiprocessing** - CPU-intensive tasks

### Optimized Use Cases
- **API Processing** - High-throughput request handling
- **Data Pipeline** - ETL operations and batch processing
- **Email Sending** - Bulk emails and transactional messaging
- **File Processing** - Upload, conversion, transformation
- **Image Processing** - Computer vision and manipulation
- **Video Processing** - Encoding and analysis
- **ML Inference** - Batch prediction and real-time serving
- **Event Processing** - Webhooks and stream processing
- **Notification Service** - Multi-channel notifications

### Deployment Flexibility
- **Standalone** - Single-server deployment
- **Docker** - Containerized deployment
- **Kubernetes** - Orchestrated scaling
- **Serverless** - AWS Lambda, Google Cloud Functions
- **Cloud Functions** - Azure Functions, Vercel, Netlify

## 📦 Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Environment Configuration
Copy the example environment file and configure:
```bash
cp .env.example .env
# Edit .env with your settings
```

## 🔧 Quick Start

### Basic Usage
```python
from queue_worker_agent import get_queue_worker_agent
from queue_worker_agent.examples import get_api_config

# Get API processing configuration
config = get_api_config("api_processing")

# Create the agent
agent = get_queue_worker_agent(config)

# Use the agent
result = await agent.run("Design a high-performance API processing queue system")
```

### Create Queue System
```python
from queue_worker_agent import create_queue_system

# Create Redis-based API processing system
queue_config = {
    "queue_type": "redis",
    "worker_type": "celery",
    "use_case": "api_processing",
    "deployment": "kubernetes"
}

result = await create_queue_system(
    name="api-processing-queue",
    **queue_config
)
```

### Submit Background Tasks
```python
from queue_worker_agent import submit_background_task

# Submit task to queue
task_result = await submit_background_task(
    task_name="process_api_request",
    task_data={"user_id": 123, "action": "update_profile"},
    priority="high"
)
```

## 📋 Configuration Examples

### API Processing Configuration
```python
from queue_worker_agent.examples import get_api_config

# High-volume API processing
config = get_api_config("high_volume_api")
config.domain_type = "ecommerce"
config.project_name = "E-commerce API Backend"
```

### Data Pipeline Configuration
```python
from queue_worker_agent.examples import get_data_config

# ETL processing pipeline
config = get_data_config("etl_processing")
config.domain_type = "analytics"
config.project_name = "Data Analytics Pipeline"
```

### Email Service Configuration
```python
from queue_worker_agent.examples import get_email_config

# Newsletter service
config = get_email_config("newsletter")
config.domain_type = "marketing"
config.project_name = "Email Marketing Platform"
```

### Serverless Configuration
```python
from queue_worker_agent.examples import get_serverless_config

# AWS Lambda processing
config = get_serverless_config("aws_lambda")
config.use_case = "image_processing"
config.project_name = "Serverless Image Processing"
```

### ML Inference Configuration
```python
from queue_worker_agent.examples import get_ml_config

# Real-time inference
config = get_ml_config("realtime")
config.domain_type = "recommendation_engine"
config.project_name = "Product Recommendation Service"
```

## 🛠️ Advanced Features

### Auto-scaling Configuration
```python
config = QueueWorkerDependencies(
    scaling_strategy=ScalingStrategy.AUTO_QUEUE_LENGTH,
    enable_auto_scaling=True,
    scale_up_threshold=1000,      # Queue length threshold
    scale_down_threshold=100,
    max_workers=20,
    min_workers=2
)
```

### Performance Optimization
```python
config = QueueWorkerDependencies(
    enable_connection_pooling=True,
    enable_result_caching=True,
    enable_batch_processing=True,
    batch_size=100,
    connection_pool_size=20
)
```

### Monitoring and Alerting
```python
config = QueueWorkerDependencies(
    enable_metrics=True,
    enable_prometheus=True,
    alert_on_queue_size=5000,
    alert_on_failure_rate=0.05,
    alert_webhook_url="https://alerts.example.com/webhook"
)
```

### Fault Tolerance
```python
config = QueueWorkerDependencies(
    enable_circuit_breaker=True,
    enable_dead_letter_queue=True,
    retry_attempts=5,
    retry_backoff="exponential",
    enable_graceful_shutdown=True
)
```

## 🔍 Domain-Specific Examples

### E-commerce Platform
```python
# High-volume order processing
ecommerce_config = get_api_config("high_volume_api")
ecommerce_config.domain_type = "ecommerce"
ecommerce_config.max_queue_size = 50000
ecommerce_config.enable_priority_queues = True
```

### SaaS Product
```python
# Multi-tenant background processing
saas_config = get_api_config("api_processing")
saas_config.domain_type = "saas_platform"
saas_config.enable_tenant_isolation = True
saas_config.enable_usage_tracking = True
```

### Healthcare System
```python
# HIPAA-compliant processing
healthcare_config = get_data_config("etl_processing")
healthcare_config.domain_type = "healthcare"
healthcare_config.enable_encryption = True
healthcare_config.enable_audit_logging = True
```

### Financial Services
```python
# Real-time fraud detection
fintech_config = get_ml_config("realtime")
fintech_config.domain_type = "fraud_detection"
fintech_config.task_timeout = 5  # Ultra-fast processing
fintech_config.enable_priority_queues = True
```

### IoT Data Processing
```python
# High-volume sensor data
iot_config = get_data_config("stream_processing")
iot_config.domain_type = "iot_platform"
iot_config.max_queue_size = 1000000
iot_config.enable_time_series_optimization = True
```

## 📊 Monitoring

### Built-in Metrics
- Queue length and processing rate
- Worker utilization and performance
- Error rates and failure patterns
- Latency and throughput statistics
- Resource usage (CPU, memory, network)

### Integration Options
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **ElasticSearch/Kibana** - Log analysis
- **DataDog** - APM and monitoring
- **New Relic** - Performance monitoring

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=queue_worker_agent

# Run specific test categories
pytest tests/test_tools.py
pytest tests/test_integration.py
```

### Load Testing
```bash
# Enable load testing mode
export LOAD_TEST_ENABLED=true
export LOAD_TEST_WORKERS=10
export LOAD_TEST_TASKS_PER_SECOND=100

python -m queue_worker_agent.tools.load_test
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t queue-worker-agent .

# Run with Redis
docker-compose up -d
```

### Kubernetes Deployment
```bash
# Apply configurations
kubectl apply -f k8s/

# Scale workers
kubectl scale deployment queue-workers --replicas=10
```

### Serverless Deployment
```bash
# Deploy to AWS Lambda
serverless deploy

# Deploy to Google Cloud Functions
gcloud functions deploy queue-processor --runtime python39
```

## 🔒 Security

### Best Practices
- Input validation and sanitization
- Rate limiting and DDoS protection
- Authentication and authorization
- Encryption in transit and at rest
- Audit logging and compliance

### Configuration
```python
config = QueueWorkerDependencies(
    enable_input_validation=True,
    enable_rate_limiting=True,
    enable_authentication=True,
    enable_encryption=True,
    enable_audit_logging=True
)
```

## 📚 Knowledge Base

The agent includes a comprehensive knowledge base for queue/worker management:
- Queue system selection criteria
- Worker architecture patterns
- Performance optimization techniques
- Scaling strategies and patterns
- Monitoring and alerting best practices
- Troubleshooting guides

Load the knowledge base into Archon:
```
File: knowledge/queue_worker_agent_knowledge.md
Tags: queue-worker, agent-knowledge, pydantic-ai, distributed-systems
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- Documentation: [Link to docs]
- Issues: [Link to issues]
- Discussions: [Link to discussions]
- Knowledge Base: `knowledge/queue_worker_agent_knowledge.md`

---

## 🔗 Related Agents

This agent works well with other universal agents:
- **API Development Agent** - For API design and implementation
- **Database Management Agent** - For data persistence
- **Monitoring Agent** - For observability and alerting
- **Deployment Agent** - For CI/CD and infrastructure

Built with ❤️ using Pydantic AI framework.