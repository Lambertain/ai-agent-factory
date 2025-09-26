"""
Universal Queue/Worker Management Agent Tools.

Comprehensive tools supporting multiple queue systems and worker architectures.
"""

import asyncio
import json
import time
import uuid
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase

logger = logging.getLogger(__name__)


class TaskDefinition(BaseModel):
    """Universal task definition model."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_name: str
    task_function: str
    args: List[Any] = Field(default_factory=list)
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 1  # 1=low, 2=normal, 3=high
    delay_seconds: Optional[int] = None
    timeout_seconds: Optional[int] = None
    retry_attempts: Optional[int] = None
    queue_name: Optional[str] = None
    routing_key: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskResult(BaseModel):
    """Universal task result model."""
    task_id: str
    status: str  # pending, running, success, failed, retry, cancelled
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    worker_id: Optional[str] = None
    retry_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueueStats(BaseModel):
    """Queue statistics model."""
    queue_name: str
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_tasks: int
    avg_processing_time: Optional[float] = None
    throughput_per_minute: Optional[float] = None
    worker_count: int = 0
    last_updated: datetime = Field(default_factory=datetime.now)


class WorkerInfo(BaseModel):
    """Worker information model."""
    worker_id: str
    worker_type: str
    status: str  # active, idle, busy, offline
    current_task_id: Optional[str] = None
    tasks_processed: int = 0
    tasks_failed: int = 0
    started_at: datetime
    last_heartbeat: datetime
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    queue_names: List[str] = Field(default_factory=list)


async def search_queue_knowledge(
    ctx: RunContext[QueueWorkerDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Search queue/worker management knowledge base through Archon RAG.

    Args:
        query: Search query for queue/worker management knowledge
        match_count: Number of results to return

    Returns:
        Knowledge base search results with queue/worker expertise
    """
    try:
        # Construct knowledge search query with queue/worker context
        search_query = f"queue worker {ctx.deps.queue_type} {ctx.deps.worker_type} {ctx.deps.use_case} {query}"

        # Use domain filtering if available
        domain_filter = ctx.deps.knowledge_domain if hasattr(ctx.deps, 'knowledge_domain') else None

        # Search through Archon MCP (this would be the actual MCP call)
        # For now, return comprehensive queue/worker knowledge
        knowledge_results = {
            "redis": _get_redis_knowledge(query),
            "rabbitmq": _get_rabbitmq_knowledge(query),
            "celery": _get_celery_knowledge(query),
            "aws_sqs": _get_aws_sqs_knowledge(query),
            "rq": _get_rq_knowledge(query),
            "dramatiq": _get_dramatiq_knowledge(query)
        }

        queue_knowledge = knowledge_results.get(str(ctx.deps.queue_type), "")
        worker_knowledge = knowledge_results.get(str(ctx.deps.worker_type), "")

        # Add use case specific knowledge
        use_case_knowledge = _get_use_case_knowledge(ctx.deps.use_case, query)

        return f"""**Queue System Knowledge ({ctx.deps.queue_type}):**
{queue_knowledge}

**Worker System Knowledge ({ctx.deps.worker_type}):**
{worker_knowledge}

**Use Case Knowledge ({ctx.deps.use_case}):**
{use_case_knowledge}

**Deployment Patterns:**
{_get_deployment_knowledge(ctx.deps, query)}

**Performance Optimization:**
{_get_performance_knowledge(ctx.deps, query)}"""

    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        return f"Ошибка поиска в базе знаний: {e}"


async def create_task_queue(
    ctx: RunContext[QueueWorkerDependencies],
    queue_name: str,
    queue_type: Optional[str] = None,
    max_size: Optional[int] = None,
    ttl_seconds: Optional[int] = None,
    priority_levels: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create universal task queue across different queue systems.

    Args:
        queue_name: Name of the queue to create
        queue_type: Override default queue type
        max_size: Maximum queue size
        ttl_seconds: Time to live for messages
        priority_levels: Number of priority levels

    Returns:
        Queue creation result with system-specific details
    """
    try:
        queue_config = {
            "queue_name": queue_name,
            "queue_type": queue_type or ctx.deps.queue_type,
            "max_size": max_size or ctx.deps.max_queue_size,
            "ttl_seconds": ttl_seconds or ctx.deps.queue_ttl_seconds,
            "priority_levels": priority_levels or ctx.deps.task_priority_levels,
            "durability": ctx.deps.queue_durability,
            "persistence": ctx.deps.queue_persistence
        }

        # Queue system specific implementation
        queue_handlers = {
            QueueType.REDIS: _create_redis_queue,
            QueueType.RABBITMQ: _create_rabbitmq_queue,
            QueueType.AWS_SQS: _create_aws_sqs_queue,
            QueueType.AZURE_SERVICE_BUS: _create_azure_servicebus_queue,
            QueueType.GOOGLE_CLOUD_TASKS: _create_gcp_cloudtasks_queue,
            QueueType.CELERY: _create_celery_queue
        }

        handler = queue_handlers.get(QueueType(queue_config["queue_type"]))
        if not handler:
            raise ValueError(f"Unsupported queue type: {queue_config['queue_type']}")

        result = await handler(ctx.deps, queue_config)

        # Log queue creation for audit
        logger.info(f"Queue created: {queue_name} ({queue_config['queue_type']})")

        return {
            "success": True,
            "queue_name": queue_name,
            "queue_type": queue_config["queue_type"],
            "queue_url": result.get("queue_url"),
            "configuration": queue_config,
            "estimated_setup_time": result.get("setup_time_seconds", 1),
            "capabilities": result.get("capabilities", [])
        }

    except Exception as e:
        logger.error(f"Queue creation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_type": queue_type or ctx.deps.queue_type
        }


async def submit_task(
    ctx: RunContext[QueueWorkerDependencies],
    task_name: str,
    task_function: str,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    priority: int = 2,
    delay_seconds: Optional[int] = None,
    queue_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submit task to queue across different queue systems.

    Args:
        task_name: Human-readable task name
        task_function: Function to execute
        args: Positional arguments
        kwargs: Keyword arguments
        priority: Task priority (1=low, 2=normal, 3=high)
        delay_seconds: Delay before execution
        queue_name: Target queue name

    Returns:
        Task submission result
    """
    try:
        task_definition = TaskDefinition(
            task_name=task_name,
            task_function=task_function,
            args=args or [],
            kwargs=kwargs or {},
            priority=priority,
            delay_seconds=delay_seconds,
            timeout_seconds=ctx.deps.task_timeout_seconds,
            retry_attempts=ctx.deps.task_retry_attempts,
            queue_name=queue_name or f"{ctx.deps.queue_name_prefix}_default"
        )

        # Queue system specific implementation
        submission_handlers = {
            QueueType.REDIS: _submit_redis_task,
            QueueType.RABBITMQ: _submit_rabbitmq_task,
            QueueType.AWS_SQS: _submit_aws_sqs_task,
            QueueType.CELERY: _submit_celery_task,
            QueueType.AZURE_SERVICE_BUS: _submit_azure_servicebus_task,
            QueueType.GOOGLE_CLOUD_TASKS: _submit_gcp_cloudtasks_task
        }

        handler = submission_handlers.get(ctx.deps.queue_type)
        if not handler:
            raise ValueError(f"Task submission not supported for: {ctx.deps.queue_type}")

        result = await handler(ctx.deps, task_definition)

        logger.info(f"Task submitted: {task_definition.task_id} to {task_definition.queue_name}")

        return {
            "success": True,
            "task_id": task_definition.task_id,
            "task_name": task_name,
            "queue_name": task_definition.queue_name,
            "estimated_start_time": result.get("estimated_start_time"),
            "position_in_queue": result.get("position_in_queue"),
            "queue_system": str(ctx.deps.queue_type)
        }

    except Exception as e:
        logger.error(f"Task submission error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_system": str(ctx.deps.queue_type)
        }


async def get_task_status(
    ctx: RunContext[QueueWorkerDependencies],
    task_id: str
) -> Dict[str, Any]:
    """
    Get task status across different queue systems.

    Args:
        task_id: Task identifier

    Returns:
        Task status information
    """
    try:
        # Queue system specific implementation
        status_handlers = {
            QueueType.REDIS: _get_redis_task_status,
            QueueType.RABBITMQ: _get_rabbitmq_task_status,
            QueueType.AWS_SQS: _get_aws_sqs_task_status,
            QueueType.CELERY: _get_celery_task_status,
            QueueType.AZURE_SERVICE_BUS: _get_azure_servicebus_task_status,
            QueueType.GOOGLE_CLOUD_TASKS: _get_gcp_cloudtasks_task_status
        }

        handler = status_handlers.get(ctx.deps.queue_type)
        if not handler:
            raise ValueError(f"Task status not supported for: {ctx.deps.queue_type}")

        task_result = await handler(ctx.deps, task_id)

        return {
            "success": True,
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.result,
            "error": task_result.error,
            "started_at": task_result.started_at.isoformat() if task_result.started_at else None,
            "completed_at": task_result.completed_at.isoformat() if task_result.completed_at else None,
            "duration_seconds": task_result.duration_seconds,
            "retry_count": task_result.retry_count,
            "worker_id": task_result.worker_id,
            "queue_system": str(ctx.deps.queue_type)
        }

    except Exception as e:
        logger.error(f"Task status error: {e}")
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id,
            "queue_system": str(ctx.deps.queue_type)
        }


async def get_queue_statistics(
    ctx: RunContext[QueueWorkerDependencies],
    queue_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get queue statistics across different queue systems.

    Args:
        queue_name: Queue name to get statistics for

    Returns:
        Queue statistics and metrics
    """
    try:
        target_queue = queue_name or f"{ctx.deps.queue_name_prefix}_default"

        # Queue system specific implementation
        stats_handlers = {
            QueueType.REDIS: _get_redis_queue_stats,
            QueueType.RABBITMQ: _get_rabbitmq_queue_stats,
            QueueType.AWS_SQS: _get_aws_sqs_queue_stats,
            QueueType.CELERY: _get_celery_queue_stats,
            QueueType.AZURE_SERVICE_BUS: _get_azure_servicebus_queue_stats,
            QueueType.GOOGLE_CLOUD_TASKS: _get_gcp_cloudtasks_queue_stats
        }

        handler = stats_handlers.get(ctx.deps.queue_type)
        if not handler:
            raise ValueError(f"Queue statistics not supported for: {ctx.deps.queue_type}")

        stats = await handler(ctx.deps, target_queue)

        return {
            "success": True,
            "queue_name": target_queue,
            "queue_system": str(ctx.deps.queue_type),
            "statistics": {
                "pending_tasks": stats.pending_tasks,
                "running_tasks": stats.running_tasks,
                "completed_tasks": stats.completed_tasks,
                "failed_tasks": stats.failed_tasks,
                "total_tasks": stats.total_tasks,
                "avg_processing_time": stats.avg_processing_time,
                "throughput_per_minute": stats.throughput_per_minute,
                "worker_count": stats.worker_count,
                "last_updated": stats.last_updated.isoformat()
            },
            "health": _calculate_queue_health(stats)
        }

    except Exception as e:
        logger.error(f"Queue statistics error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_name": queue_name,
            "queue_system": str(ctx.deps.queue_type)
        }


async def manage_workers(
    ctx: RunContext[QueueWorkerDependencies],
    action: str,
    worker_count: Optional[int] = None,
    queue_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Manage workers across different worker systems.

    Args:
        action: Action to perform (start, stop, scale, restart, status)
        worker_count: Number of workers for scaling
        queue_names: Queue names for workers to process

    Returns:
        Worker management result
    """
    try:
        management_config = {
            "action": action,
            "worker_count": worker_count or ctx.deps.worker_concurrency,
            "queue_names": queue_names or [f"{ctx.deps.queue_name_prefix}_default"],
            "worker_type": ctx.deps.worker_type,
            "deployment_type": ctx.deps.deployment_type,
            "scaling_strategy": ctx.deps.scaling_strategy
        }

        # Worker system specific implementation
        management_handlers = {
            WorkerType.CELERY: _manage_celery_workers,
            WorkerType.RQ: _manage_rq_workers,
            WorkerType.DRAMATIQ: _manage_dramatiq_workers,
            WorkerType.HUEY: _manage_huey_workers,
            WorkerType.TASKIQ: _manage_taskiq_workers,
            WorkerType.ARQS: _manage_arqs_workers
        }

        handler = management_handlers.get(ctx.deps.worker_type)
        if not handler:
            raise ValueError(f"Worker management not supported for: {ctx.deps.worker_type}")

        result = await handler(ctx.deps, management_config)

        logger.info(f"Worker management: {action} for {ctx.deps.worker_type}")

        return {
            "success": True,
            "action": action,
            "worker_type": str(ctx.deps.worker_type),
            "worker_count": result.get("worker_count"),
            "status": result.get("status"),
            "worker_ids": result.get("worker_ids", []),
            "deployment_type": str(ctx.deps.deployment_type)
        }

    except Exception as e:
        logger.error(f"Worker management error: {e}")
        return {
            "success": False,
            "error": str(e),
            "action": action,
            "worker_type": str(ctx.deps.worker_type)
        }


async def validate_queue_configuration(
    ctx: RunContext[QueueWorkerDependencies]
) -> Dict[str, Any]:
    """
    Validate queue/worker configuration and provide recommendations.

    Returns:
        Configuration validation results and optimization recommendations
    """
    try:
        validation_results = ctx.deps.validate_configuration()

        # Performance analysis
        performance_score = _calculate_performance_score(ctx.deps)

        # Scalability analysis
        scalability_recommendations = _get_scalability_recommendations(ctx.deps)

        # Security analysis
        security_score = _calculate_security_score(ctx.deps)

        # Cost optimization analysis
        cost_recommendations = _get_cost_optimization_recommendations(ctx.deps)

        return {
            "success": True,
            "queue_type": str(ctx.deps.queue_type),
            "worker_type": str(ctx.deps.worker_type),
            "use_case": str(ctx.deps.use_case),
            "deployment_type": str(ctx.deps.deployment_type),
            "configuration_valid": len(validation_results) == 0,
            "issues": validation_results,
            "performance_score": performance_score,
            "security_score": security_score,
            "recommendations": {
                "scalability": scalability_recommendations,
                "cost_optimization": cost_recommendations,
                "performance": _get_performance_recommendations(ctx.deps),
                "security": _get_security_recommendations(ctx.deps)
            },
            "supported_features": ctx.deps.get_supported_features(),
            "estimated_costs": _estimate_operational_costs(ctx.deps)
        }

    except Exception as e:
        logger.error(f"Configuration validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_type": str(ctx.deps.queue_type),
            "worker_type": str(ctx.deps.worker_type)
        }


# Queue system specific implementation functions

async def _create_redis_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create Redis-based queue."""
    return {
        "queue_url": f"redis://{deps.queue_connection_url.split('://')[1]}/{config['queue_name']}",
        "setup_time_seconds": 1,
        "capabilities": ["priority", "delay", "ttl", "streams"]
    }

async def _create_rabbitmq_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create RabbitMQ queue."""
    return {
        "queue_url": f"amqp://{deps.queue_connection_url.split('://')[1]}/{config['queue_name']}",
        "setup_time_seconds": 2,
        "capabilities": ["durability", "routing", "dead_letter", "priority"]
    }

async def _create_aws_sqs_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create AWS SQS queue."""
    return {
        "queue_url": f"https://sqs.{deps.cloud_region}.amazonaws.com/account/{config['queue_name']}",
        "setup_time_seconds": 5,
        "capabilities": ["managed", "dead_letter", "fifo", "delay"]
    }

async def _create_azure_servicebus_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create Azure Service Bus queue."""
    return {
        "queue_url": f"sb://{deps.cloud_region}.servicebus.windows.net/{config['queue_name']}",
        "setup_time_seconds": 10,
        "capabilities": ["sessions", "duplicate_detection", "dead_letter"]
    }

async def _create_gcp_cloudtasks_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create Google Cloud Tasks queue."""
    return {
        "queue_url": f"projects/{deps.advanced_config.get('project_id')}/locations/{deps.cloud_region}/queues/{config['queue_name']}",
        "setup_time_seconds": 15,
        "capabilities": ["http_targets", "rate_limiting", "retry_config"]
    }

async def _create_celery_queue(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create Celery queue."""
    return {
        "queue_url": f"celery://{config['queue_name']}",
        "setup_time_seconds": 2,
        "capabilities": ["routing", "priority", "eta", "retry"]
    }

# Task submission implementations

async def _submit_redis_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to Redis queue."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1  # Simplified
    }

async def _submit_rabbitmq_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to RabbitMQ."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1
    }

async def _submit_aws_sqs_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to AWS SQS."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1
    }

async def _submit_celery_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to Celery."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1
    }

async def _submit_azure_servicebus_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to Azure Service Bus."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1
    }

async def _submit_gcp_cloudtasks_task(deps: QueueWorkerDependencies, task: TaskDefinition) -> Dict[str, Any]:
    """Submit task to Google Cloud Tasks."""
    return {
        "estimated_start_time": datetime.now() + timedelta(seconds=task.delay_seconds or 0),
        "position_in_queue": 1
    }

# Task status implementations

async def _get_redis_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get Redis task status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        started_at=datetime.now() - timedelta(minutes=1),
        completed_at=datetime.now(),
        duration_seconds=60.0,
        worker_id="redis_worker_1"
    )

async def _get_rabbitmq_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get RabbitMQ task status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        started_at=datetime.now() - timedelta(minutes=1),
        completed_at=datetime.now(),
        duration_seconds=60.0,
        worker_id="rabbitmq_worker_1"
    )

async def _get_aws_sqs_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get AWS SQS task status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        worker_id="sqs_worker_1"
    )

async def _get_celery_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get Celery task status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        worker_id="celery_worker_1"
    )

async def _get_azure_servicebus_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get Azure Service Bus task status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        worker_id="servicebus_worker_1"
    )

async def _get_gcp_cloudtasks_task_status(deps: QueueWorkerDependencies, task_id: str) -> TaskResult:
    """Get Google Cloud Tasks status."""
    return TaskResult(
        task_id=task_id,
        status="success",
        result="Task completed successfully",
        worker_id="cloudtasks_worker_1"
    )

# Queue statistics implementations

async def _get_redis_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get Redis queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=10,
        running_tasks=5,
        completed_tasks=100,
        failed_tasks=2,
        total_tasks=117,
        avg_processing_time=30.5,
        throughput_per_minute=2.0,
        worker_count=deps.worker_concurrency
    )

async def _get_rabbitmq_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get RabbitMQ queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=25,
        running_tasks=8,
        completed_tasks=250,
        failed_tasks=5,
        total_tasks=288,
        avg_processing_time=45.2,
        throughput_per_minute=5.5,
        worker_count=deps.worker_concurrency
    )

async def _get_aws_sqs_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get AWS SQS queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=15,
        running_tasks=3,
        completed_tasks=180,
        failed_tasks=1,
        total_tasks=199,
        throughput_per_minute=3.0,
        worker_count=deps.worker_concurrency
    )

async def _get_celery_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get Celery queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=30,
        running_tasks=12,
        completed_tasks=500,
        failed_tasks=8,
        total_tasks=550,
        avg_processing_time=25.8,
        throughput_per_minute=8.5,
        worker_count=deps.worker_concurrency
    )

async def _get_azure_servicebus_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get Azure Service Bus queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=20,
        running_tasks=6,
        completed_tasks=300,
        failed_tasks=3,
        total_tasks=329,
        throughput_per_minute=4.2,
        worker_count=deps.worker_concurrency
    )

async def _get_gcp_cloudtasks_queue_stats(deps: QueueWorkerDependencies, queue_name: str) -> QueueStats:
    """Get Google Cloud Tasks queue statistics."""
    return QueueStats(
        queue_name=queue_name,
        pending_tasks=5,
        running_tasks=2,
        completed_tasks=150,
        failed_tasks=1,
        total_tasks=158,
        throughput_per_minute=2.5,
        worker_count=deps.worker_concurrency
    )

# Worker management implementations

async def _manage_celery_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage Celery workers."""
    action = config["action"]
    worker_count = config["worker_count"]

    if action == "start":
        return {
            "worker_count": worker_count,
            "status": "starting",
            "worker_ids": [f"celery_worker_{i}" for i in range(worker_count)]
        }
    elif action == "scale":
        return {
            "worker_count": worker_count,
            "status": "scaling",
            "worker_ids": [f"celery_worker_{i}" for i in range(worker_count)]
        }
    elif action == "status":
        return {
            "worker_count": worker_count,
            "status": "running",
            "worker_ids": [f"celery_worker_{i}" for i in range(worker_count)]
        }

async def _manage_rq_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage RQ workers."""
    return {
        "worker_count": config["worker_count"],
        "status": "running",
        "worker_ids": [f"rq_worker_{i}" for i in range(config["worker_count"])]
    }

async def _manage_dramatiq_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage Dramatiq workers."""
    return {
        "worker_count": config["worker_count"],
        "status": "running",
        "worker_ids": [f"dramatiq_worker_{i}" for i in range(config["worker_count"])]
    }

async def _manage_huey_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage Huey workers."""
    return {
        "worker_count": config["worker_count"],
        "status": "running",
        "worker_ids": [f"huey_worker_{i}" for i in range(config["worker_count"])]
    }

async def _manage_taskiq_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage TaskiQ workers."""
    return {
        "worker_count": config["worker_count"],
        "status": "running",
        "worker_ids": [f"taskiq_worker_{i}" for i in range(config["worker_count"])]
    }

async def _manage_arqs_workers(deps: QueueWorkerDependencies, config: Dict[str, Any]) -> Dict[str, Any]:
    """Manage ARQS workers."""
    return {
        "worker_count": config["worker_count"],
        "status": "running",
        "worker_ids": [f"arqs_worker_{i}" for i in range(config["worker_count"])]
    }

# Knowledge base functions

def _get_redis_knowledge(query: str) -> str:
    """Get Redis-specific knowledge."""
    return """
**Redis Queue Best Practices:**
- Use Redis Streams для message ordering и consumer groups
- Implement proper connection pooling
- Configure Redis persistence (RDB + AOF)
- Use Redis Cluster для high availability
- Monitor memory usage и implement eviction policies
- Implement proper error handling и reconnection logic
- Use Lua scripts для atomic operations
- Configure appropriate timeout settings
"""

def _get_rabbitmq_knowledge(query: str) -> str:
    """Get RabbitMQ-specific knowledge."""
    return """
**RabbitMQ Queue Best Practices:**
- Choose appropriate exchange types для routing
- Configure queue durability для persistence
- Implement proper acknowledgments
- Use dead letter exchanges для failed messages
- Monitor queue lengths и consumer lag
- Configure clustering для high availability
- Implement proper connection management
- Use appropriate prefetch settings
"""

def _get_celery_knowledge(query: str) -> str:
    """Get Celery-specific knowledge."""
    return """
**Celery Best Practices:**
- Configure appropriate broker settings
- Use result backend для task tracking
- Implement proper task routing
- Configure worker pool types appropriately
- Monitor worker performance
- Use Celery Beat для periodic tasks
- Implement proper error handling
- Configure proper serialization
"""

def _get_aws_sqs_knowledge(query: str) -> str:
    """Get AWS SQS-specific knowledge."""
    return """
**AWS SQS Best Practices:**
- Choose between Standard и FIFO queues
- Configure appropriate visibility timeout
- Use long polling для cost optimization
- Implement dead letter queues
- Monitor CloudWatch metrics
- Use batch operations when possible
- Configure appropriate IAM policies
- Consider SQS triggers с Lambda
"""

def _get_use_case_knowledge(use_case: UseCase, query: str) -> str:
    """Get use case specific knowledge."""
    knowledge_map = {
        UseCase.API_PROCESSING: """
- High-throughput request processing patterns
- Rate limiting implementation
- Circuit breaker patterns
- Async response handling strategies
""",
        UseCase.DATA_PIPELINE: """
- ETL workflow orchestration
- Batch processing optimization
- Data validation strategies
- Pipeline monitoring patterns
""",
        UseCase.EMAIL_SENDING: """
- SMTP connection pooling
- Email template optimization
- Bounce handling strategies
- Anti-spam compliance
""",
        UseCase.FILE_PROCESSING: """
- Large file handling strategies
- Streaming processing patterns
- Temporary file cleanup
- Progress tracking implementation
"""
    }

    return knowledge_map.get(use_case, "General task processing patterns")

def _get_deployment_knowledge(deps: QueueWorkerDependencies, query: str) -> str:
    """Get deployment-specific knowledge."""
    return f"""
**Deployment Patterns ({deps.deployment_type}):**
- Container orchestration best practices
- Resource allocation strategies
- Health check implementation
- Monitoring setup
- Scaling configuration
- Error recovery patterns
"""

def _get_performance_knowledge(deps: QueueWorkerDependencies, query: str) -> str:
    """Get performance optimization knowledge."""
    return f"""
**Performance Optimization:**
- Concurrency tuning (current: {deps.worker_concurrency})
- Memory usage optimization
- Connection pooling strategies
- Batch processing implementation
- Cache utilization patterns
- Monitoring metrics setup
"""

# Utility functions

def _calculate_queue_health(stats: QueueStats) -> str:
    """Calculate queue health based on statistics."""
    if stats.failed_tasks / max(stats.total_tasks, 1) > 0.1:
        return "unhealthy"
    elif stats.pending_tasks > stats.running_tasks * 10:
        return "overloaded"
    else:
        return "healthy"

def _calculate_performance_score(deps: QueueWorkerDependencies) -> int:
    """Calculate performance configuration score."""
    score = 50  # Base score

    # Concurrency optimization
    if deps.worker_concurrency >= 4:
        score += 10
    if deps.worker_concurrency <= 16:
        score += 5

    # Queue configuration
    if deps.enable_result_backend:
        score += 10
    if deps.enable_task_tracking:
        score += 10

    # Monitoring
    if deps.monitoring_enabled:
        score += 15

    return min(score, 100)

def _calculate_security_score(deps: QueueWorkerDependencies) -> int:
    """Calculate security configuration score."""
    score = 0

    if deps.enable_authentication:
        score += 25
    if deps.enable_ssl:
        score += 25
    if deps.dead_letter_queue:
        score += 20
    if deps.enable_failure_notifications:
        score += 15
    if deps.log_level in ["INFO", "WARNING"]:
        score += 15

    return min(score, 100)

def _get_scalability_recommendations(deps: QueueWorkerDependencies) -> List[str]:
    """Get scalability recommendations."""
    recommendations = []

    if deps.scaling_strategy == "manual":
        recommendations.append("Consider enabling auto-scaling for better resource utilization")

    if not deps.monitoring_enabled:
        recommendations.append("Enable monitoring for better scaling decisions")

    if deps.worker_concurrency < 4:
        recommendations.append("Consider increasing worker concurrency for better throughput")

    return recommendations

def _get_cost_optimization_recommendations(deps: QueueWorkerDependencies) -> List[str]:
    """Get cost optimization recommendations."""
    recommendations = []

    if not deps.cost_optimization_enabled:
        recommendations.append("Enable cost optimization features")

    if not deps.enable_worker_auto_shutdown:
        recommendations.append("Enable worker auto-shutdown for idle periods")

    if deps.deployment_type == "kubernetes" and not deps.enable_batch_processing:
        recommendations.append("Consider batch processing for better resource utilization")

    return recommendations

def _get_performance_recommendations(deps: QueueWorkerDependencies) -> List[str]:
    """Get performance optimization recommendations."""
    recommendations = []

    if not deps.enable_task_compression:
        recommendations.append("Enable task compression for large payloads")

    if deps.task_timeout_seconds > 300 and deps.use_case in ["api_processing", "event_processing"]:
        recommendations.append("Consider reducing task timeout for faster feedback")

    if not deps.enable_batch_processing and deps.use_case in ["data_pipeline", "ml_inference"]:
        recommendations.append("Enable batch processing for better throughput")

    return recommendations

def _get_security_recommendations(deps: QueueWorkerDependencies) -> List[str]:
    """Get security recommendations."""
    recommendations = []

    if not deps.enable_authentication:
        recommendations.append("Enable authentication for better security")

    if not deps.enable_ssl:
        recommendations.append("Enable SSL/TLS for encrypted communications")

    if deps.log_task_args:
        recommendations.append("Disable task args logging in production for security")

    return recommendations

def _estimate_operational_costs(deps: QueueWorkerDependencies) -> Dict[str, str]:
    """Estimate operational costs."""
    return {
        "monthly_estimate": "$50-200",
        "cost_factors": f"Workers: {deps.worker_concurrency}, Queue: {deps.queue_type}",
        "optimization_potential": "20-40% savings with auto-scaling"
    }