"""
Universal Queue/Worker Management Agent for Pydantic AI.

Comprehensive AI agent for queue systems and worker management supporting multiple
queue backends and deployment architectures with adaptive configuration.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from pydantic_ai import Agent, RunContext

from .dependencies import QueueWorkerDependencies, QueueType, WorkerType, UseCase, DeploymentType
from ..common import check_pm_switch
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .prompts import get_system_prompt
from .settings import get_llm_model
from .tools import (
    create_task_queue,
    submit_task,
    get_task_status,
    get_queue_statistics,
    manage_workers,
    validate_queue_configuration
)

logger = logging.getLogger(__name__)

# Create universal queue worker agent with decorators
queue_worker_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=QueueWorkerDependencies,
    system_prompt=lambda deps: get_system_prompt(deps),
    agent_type="queue_worker",
    knowledge_tags=["queue", "worker", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="queue-worker.universal.com",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Register agent in global registry
register_agent("queue_worker", queue_worker_agent, agent_type="queue_worker")

# Register queue-specific tools
queue_worker_agent.tool(create_task_queue)
queue_worker_agent.tool(submit_task)
queue_worker_agent.tool(get_task_status)
queue_worker_agent.tool(get_queue_statistics)
queue_worker_agent.tool(manage_workers)
queue_worker_agent.tool(validate_queue_configuration)

# Collective work tools and knowledge search now added automatically via decorators


async def run_queue_worker_agent(
    user_input: str,
    deps: Optional[QueueWorkerDependencies] = None,
    **kwargs
) -> str:
    """
    Run queue/worker management agent with user input.

    Args:
        user_input: User query or request for queue/worker management
        deps: Queue/worker agent dependencies
        **kwargs: Additional arguments for agent execution

    Returns:
        Agent response with queue/worker management guidance
    """
    try:
        if deps is None:
            deps = QueueWorkerDependencies(
                api_key="demo",
                project_path="",
                project_name="Queue Worker Management Project"
            )

        # Run agent with user input
        result = await queue_worker_agent.run(user_input, deps=deps)

        logger.info(f"Queue/worker management request completed: {user_input[:100]}...")
        return result.data

    except Exception as e:
        logger.error(f"Queue/worker management agent error: {e}")
        return f"Ошибка выполнения агента управления очередями: {e}"


async def create_queue_system(
    queue_name: str,
    deps: QueueWorkerDependencies,
    max_size: Optional[int] = None,
    ttl_seconds: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create queue system through the agent.

    Args:
        queue_name: Name of the queue to create
        deps: Queue/worker agent dependencies
        max_size: Maximum queue size
        ttl_seconds: Time to live for messages
        **kwargs: Additional queue parameters

    Returns:
        Queue creation result
    """
    try:
        # Create queue through agent tools
        with queue_worker_agent.override(deps=deps):
            queue_result = await create_task_queue(
                ctx=RunContext(deps=deps, retry=0),
                queue_name=queue_name,
                max_size=max_size,
                ttl_seconds=ttl_seconds,
                **kwargs
            )

        logger.info(f"Queue created: {queue_result.get('queue_name')}")
        return queue_result

    except Exception as e:
        logger.error(f"Queue creation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_type": str(deps.queue_type)
        }


async def submit_background_task(
    task_name: str,
    task_function: str,
    deps: QueueWorkerDependencies,
    args: Optional[list] = None,
    kwargs: Optional[dict] = None,
    priority: int = 2,
    delay_seconds: Optional[int] = None,
    **options
) -> Dict[str, Any]:
    """
    Submit background task through the agent.

    Args:
        task_name: Human-readable task name
        task_function: Function to execute
        deps: Queue/worker agent dependencies
        args: Positional arguments
        kwargs: Keyword arguments
        priority: Task priority (1=low, 2=normal, 3=high)
        delay_seconds: Delay before execution
        **options: Additional task options

    Returns:
        Task submission result
    """
    try:
        # Submit task through agent tools
        with queue_worker_agent.override(deps=deps):
            task_result = await submit_task(
                ctx=RunContext(deps=deps, retry=0),
                task_name=task_name,
                task_function=task_function,
                args=args,
                kwargs=kwargs,
                priority=priority,
                delay_seconds=delay_seconds,
                **options
            )

        logger.info(f"Task submitted: {task_result.get('task_id')}")
        return task_result

    except Exception as e:
        logger.error(f"Task submission error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_system": str(deps.queue_type)
        }


async def check_task_progress(
    task_id: str,
    deps: QueueWorkerDependencies
) -> Dict[str, Any]:
    """
    Check task progress through the agent.

    Args:
        task_id: Task identifier
        deps: Queue/worker agent dependencies

    Returns:
        Task status information
    """
    try:
        # Check task status through agent tools
        with queue_worker_agent.override(deps=deps):
            status_result = await get_task_status(
                ctx=RunContext(deps=deps, retry=0),
                task_id=task_id
            )

        logger.info(f"Task status checked: {task_id}")
        return status_result

    except Exception as e:
        logger.error(f"Task status check error: {e}")
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id,
            "queue_system": str(deps.queue_type)
        }


async def get_system_statistics(
    deps: QueueWorkerDependencies,
    queue_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get queue system statistics through the agent.

    Args:
        deps: Queue/worker agent dependencies
        queue_name: Optional queue name to get statistics for

    Returns:
        System statistics and metrics
    """
    try:
        # Get statistics through agent tools
        with queue_worker_agent.override(deps=deps):
            stats_result = await get_queue_statistics(
                ctx=RunContext(deps=deps, retry=0),
                queue_name=queue_name
            )

        logger.info(f"Statistics retrieved for {deps.queue_type}")
        return stats_result

    except Exception as e:
        logger.error(f"Statistics retrieval error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_system": str(deps.queue_type)
        }


async def scale_workers(
    worker_count: int,
    deps: QueueWorkerDependencies,
    queue_names: Optional[list] = None
) -> Dict[str, Any]:
    """
    Scale workers through the agent.

    Args:
        worker_count: Target number of workers
        deps: Queue/worker agent dependencies
        queue_names: Optional list of queue names for workers

    Returns:
        Worker scaling result
    """
    try:
        # Scale workers through agent tools
        with queue_worker_agent.override(deps=deps):
            scaling_result = await manage_workers(
                ctx=RunContext(deps=deps, retry=0),
                action="scale",
                worker_count=worker_count,
                queue_names=queue_names
            )

        logger.info(f"Workers scaled to {worker_count}")
        return scaling_result

    except Exception as e:
        logger.error(f"Worker scaling error: {e}")
        return {
            "success": False,
            "error": str(e),
            "worker_type": str(deps.worker_type)
        }


async def get_configuration_analysis(
    deps: QueueWorkerDependencies
) -> Dict[str, Any]:
    """
    Get comprehensive configuration analysis.

    Args:
        deps: Queue/worker agent dependencies

    Returns:
        Configuration analysis and recommendations
    """
    try:
        # Validate configuration through agent tools
        with queue_worker_agent.override(deps=deps):
            analysis_result = await validate_queue_configuration(
                ctx=RunContext(deps=deps, retry=0)
            )

        logger.info(f"Configuration analyzed for {deps.queue_type}/{deps.worker_type}")
        return analysis_result

    except Exception as e:
        logger.error(f"Configuration analysis error: {e}")
        return {
            "success": False,
            "error": str(e),
            "queue_type": str(deps.queue_type),
            "worker_type": str(deps.worker_type)
        }


# Convenience functions for different use cases

def create_api_processing_deps(
    api_key: str,
    queue_type: QueueType = QueueType.REDIS,
    worker_type: WorkerType = WorkerType.CELERY,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for API processing."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=worker_type,
        use_case=UseCase.API_PROCESSING,
        task_timeout_seconds=30,
        worker_concurrency=8,
        enable_rate_limiting=True,
        max_tasks_per_second=100,
        **kwargs
    )


def create_data_pipeline_deps(
    api_key: str,
    queue_type: QueueType = QueueType.RABBITMQ,
    worker_type: WorkerType = WorkerType.CELERY,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for data pipelines."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=worker_type,
        use_case=UseCase.DATA_PIPELINE,
        task_timeout_seconds=1800,  # 30 minutes
        worker_concurrency=4,
        enable_batch_processing=True,
        batch_size=100,
        worker_pool_type="processes",
        **kwargs
    )


def create_email_service_deps(
    api_key: str,
    queue_type: QueueType = QueueType.REDIS,
    worker_type: WorkerType = WorkerType.RQ,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for email sending."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=worker_type,
        use_case=UseCase.EMAIL_SENDING,
        task_timeout_seconds=60,
        worker_concurrency=16,
        enable_rate_limiting=True,
        max_tasks_per_minute=1000,
        task_retry_attempts=5,
        **kwargs
    )


def create_file_processing_deps(
    api_key: str,
    queue_type: QueueType = QueueType.AWS_SQS,
    worker_type: WorkerType = WorkerType.CELERY,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for file processing."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=worker_type,
        use_case=UseCase.FILE_PROCESSING,
        task_timeout_seconds=600,  # 10 minutes
        worker_concurrency=2,
        worker_pool_type="processes",
        enable_task_compression=True,
        cloud_provider="aws",
        **kwargs
    )


def create_ml_inference_deps(
    api_key: str,
    queue_type: QueueType = QueueType.REDIS,
    worker_type: WorkerType = WorkerType.CELERY,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for ML inference."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=worker_type,
        use_case=UseCase.ML_INFERENCE,
        task_timeout_seconds=120,
        worker_concurrency=4,
        enable_batch_processing=True,
        batch_size=32,
        resource_requests={"cpu": "1", "memory": "2Gi"},
        resource_limits={"cpu": "4", "memory": "8Gi"},
        **kwargs
    )


def create_serverless_deps(
    api_key: str,
    queue_type: QueueType = QueueType.AWS_SQS,
    deployment_type: DeploymentType = DeploymentType.LAMBDA,
    project_path: str = "",
    **kwargs
) -> QueueWorkerDependencies:
    """Create dependencies optimized for serverless deployment."""
    return QueueWorkerDependencies(
        api_key=api_key,
        project_path=project_path,
        queue_type=queue_type,
        worker_type=WorkerType.WORKER_THREADS,
        deployment_type=deployment_type,
        use_case=UseCase.API_PROCESSING,
        task_timeout_seconds=900,  # 15 minutes max for serverless
        worker_concurrency=1,
        enable_worker_auto_shutdown=True,
        cost_optimization_enabled=True,
        cloud_provider="aws",
        **kwargs
    )


# Main execution function
async def main():
    """
    Main execution function for testing the queue/worker management agent.
    """
    # Create test dependencies
    deps = QueueWorkerDependencies(
        api_key="test_api_key",
        project_path="/path/to/project",
        project_name="Test Queue Worker Project",
        queue_type=QueueType.REDIS,
        worker_type=WorkerType.CELERY,
        use_case=UseCase.API_PROCESSING
    )

    # Test queries
    test_queries = [
        "Как настроить Redis очередь для API обработки?",
        "Создать Celery worker'ы для обработки задач",
        "Реализовать мониторинг производительности очереди",
        "Настроить автоскейлинг worker'ов",
        "Добавить обработку ошибок и retry логику"
    ]

    print(f"🔄 Тестирование Queue/Worker Management Agent ({deps.queue_type} + {deps.worker_type})")
    print("=" * 80)

    for query in test_queries:
        print(f"\n💬 Запрос: {query}")
        print("-" * 40)

        try:
            response = await run_queue_worker_agent(query, deps)
            print(f"🤖 Ответ: {response[:200]}...")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    # Test queue creation
    print(f"\n📋 Тестирование создания очереди...")
    queue_result = await create_queue_system(
        queue_name="test_queue",
        deps=deps,
        max_size=1000
    )
    print(f"Результат: {queue_result}")

    # Test task submission
    print(f"\n📤 Тестирование отправки задачи...")
    task_result = await submit_background_task(
        task_name="Test Task",
        task_function="process_data",
        deps=deps,
        args=[1, 2, 3],
        kwargs={"timeout": 30}
    )
    print(f"Результат: {task_result}")

    # Test configuration analysis
    print(f"\n⚙️ Тестирование анализа конфигурации...")
    config_result = await get_configuration_analysis(deps)
    print(f"Конфигурация валидна: {config_result.get('configuration_valid')}")
    print(f"Performance score: {config_result.get('performance_score')}")
    print(f"Рекомендации: {len(config_result.get('recommendations', {}).get('scalability', []))}")

    # Test system statistics
    print(f"\n📊 Тестирование статистики системы...")
    stats_result = await get_system_statistics(deps)
    if stats_result.get("success"):
        stats = stats_result.get("statistics", {})
        print(f"Pending tasks: {stats.get('pending_tasks')}")
        print(f"Worker count: {stats.get('worker_count')}")
        print(f"Throughput: {stats.get('throughput_per_minute')} tasks/min")


if __name__ == "__main__":
    asyncio.run(main())