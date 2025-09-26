"""
Пример базового использования системы оркестрации субагентов.

Этот файл демонстрирует, как использовать систему оркестрации
для координации работы субагентов в реальных сценариях.
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import List

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Импорт компонентов системы
from orchestration import (
    AgentOrchestrator, Task, Agent, TaskPriority, AgentStatus,
    OrchestrationConfig, TaskDependency
)


async def basic_orchestration_example():
    """
    Пример базовой оркестрации.

    Демонстрирует:
    - Создание и настройку оркестратора
    - Регистрацию агентов
    - Отправку задач
    - Мониторинг выполнения
    """
    print("🚀 Запуск примера базовой оркестрации...")

    # Конфигурация системы
    config = OrchestrationConfig(
        max_concurrent_tasks=3,
        max_queue_size=50,
        default_task_timeout=60,
        enable_parallel_execution=True,
        enable_load_balancing=True
    )

    # Создаем и запускаем оркестратор
    orchestrator = AgentOrchestrator(config)
    await orchestrator.start()

    try:
        # Регистрируем агентов
        agents = await register_sample_agents(orchestrator)
        print(f"✅ Зарегистрировано {len(agents)} агентов")

        # Создаем и отправляем задачи
        tasks = await create_and_submit_tasks(orchestrator)
        print(f"📝 Отправлено {len(tasks)} задач")

        # Мониторим выполнение
        await monitor_execution(orchestrator, tasks)

    finally:
        # Корректно завершаем работу
        await orchestrator.shutdown()
        print("🛑 Оркестратор остановлен")


async def register_sample_agents(orchestrator: AgentOrchestrator) -> List[Agent]:
    """Регистрация образцовых агентов."""
    agents = [
        Agent(
            id="data-processor-1",
            name="Data Processing Agent",
            type="data-processor",
            description="Обработка данных и аналитика",
            capabilities=["data-processing", "analytics", "csv", "json"],
            supported_tasks=["process-data", "analyze-data", "transform-data"],
            max_concurrent_tasks=2
        ),
        Agent(
            id="web-scraper-1",
            name="Web Scraping Agent",
            type="web-scraper",
            description="Сбор данных из веб-источников",
            capabilities=["web-scraping", "http-requests", "html-parsing"],
            supported_tasks=["scrape-website", "download-content", "extract-data"],
            max_concurrent_tasks=3
        ),
        Agent(
            id="api-client-1",
            name="API Client Agent",
            type="api-client",
            description="Взаимодействие с внешними API",
            capabilities=["api-calls", "rest", "json", "authentication"],
            supported_tasks=["api-request", "data-sync", "webhook"],
            max_concurrent_tasks=4
        )
    ]

    # Регистрируем всех агентов
    for agent in agents:
        await orchestrator.register_agent(agent)

    return agents


async def create_and_submit_tasks(orchestrator: AgentOrchestrator) -> List[str]:
    """Создание и отправка задач."""
    tasks = [
        Task(
            id="task-001",
            name="Сбор данных с веб-сайта",
            description="Собрать последние новости с tech-сайтов",
            priority=TaskPriority.HIGH,
            agent_type="web-scraper",
            input_data={
                "urls": ["https://techcrunch.com", "https://arstechnica.com"],
                "selectors": ["article", ".news-item"]
            },
            estimated_duration=30,
            context={"department": "research"}
        ),
        Task(
            id="task-002",
            name="Обработка собранных данных",
            description="Анализ и очистка собранных новостей",
            priority=TaskPriority.NORMAL,
            agent_type="data-processor",
            input_data={
                "data_source": "task-001-output",
                "operations": ["clean", "deduplicate", "sentiment_analysis"]
            },
            estimated_duration=45,
            context={"depends_on": "task-001"}
        ),
        Task(
            id="task-003",
            name="Синхронизация с внешним API",
            description="Отправка обработанных данных в CRM",
            priority=TaskPriority.NORMAL,
            agent_type="api-client",
            input_data={
                "api_endpoint": "https://api.example.com/data",
                "method": "POST",
                "auth_type": "bearer"
            },
            estimated_duration=15,
            context={"depends_on": "task-002"}
        ),
        Task(
            id="task-004",
            name="Бэкап данных",
            description="Создание резервной копии обработанных данных",
            priority=TaskPriority.LOW,
            agent_type="data-processor",
            input_data={
                "backup_location": "/backup/daily/",
                "compression": "gzip"
            },
            estimated_duration=20
        ),
        Task(
            id="task-005",
            name="Генерация отчета",
            description="Создание сводного отчета о выполненной работе",
            priority=TaskPriority.NORMAL,
            agent_type="data-processor",
            input_data={
                "report_type": "summary",
                "format": "pdf",
                "include_charts": True
            },
            estimated_duration=25,
            context={"depends_on": "task-002,task-003"}
        )
    ]

    # Отправляем задачи
    task_ids = []
    for task in tasks:
        task_id = await orchestrator.submit_task(task)
        task_ids.append(task_id)

    return task_ids


async def monitor_execution(orchestrator: AgentOrchestrator, task_ids: List[str]):
    """Мониторинг выполнения задач."""
    print("\n📊 Мониторинг выполнения задач...")

    monitoring_duration = 30  # секунд
    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < monitoring_duration:
        # Получаем статус системы
        system_status = await orchestrator.get_system_status()

        print(f"\n⏰ Время: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🔄 Активных задач: {system_status['execution']['active_executions']}")
        print(f"✅ Завершенных задач: {system_status['metrics']['tasks_completed']}")
        print(f"❌ Неудачных задач: {system_status['metrics']['tasks_failed']}")

        # Проверяем статус каждой задачи
        for task_id in task_ids:
            status = await orchestrator.get_task_status(task_id)
            if status:
                print(f"   📋 {task_id}: {status}")

        # Проверяем очередь задач
        queue_stats = system_status.get('task_queue', {})
        if queue_stats:
            print(f"📥 В очереди: {queue_stats.get('total_tasks', 0)}")

        await asyncio.sleep(5)

    print("\n✨ Мониторинг завершен")


async def dependency_example():
    """
    Пример работы с зависимостями между задачами.

    Демонстрирует:
    - Создание задач с зависимостями
    - Автоматическое разрешение порядка выполнения
    - Условное выполнение
    """
    print("\n🔗 Пример работы с зависимостями...")

    config = OrchestrationConfig(max_concurrent_tasks=2)
    orchestrator = AgentOrchestrator(config)
    await orchestrator.start()

    try:
        # Регистрируем универсального агента
        universal_agent = Agent(
            id="universal-agent",
            name="Universal Agent",
            type="universal",
            capabilities=["any"],
            supported_tasks=["any"],
            max_concurrent_tasks=5
        )
        await orchestrator.register_agent(universal_agent)

        # Создаем задачи с зависимостями
        tasks_with_deps = [
            Task(
                id="step-1",
                name="Инициализация",
                priority=TaskPriority.HIGH,
                agent_type="universal"
            ),
            Task(
                id="step-2",
                name="Загрузка данных",
                priority=TaskPriority.NORMAL,
                agent_type="universal"
            ),
            Task(
                id="step-3",
                name="Обработка данных",
                priority=TaskPriority.NORMAL,
                agent_type="universal"
            ),
            Task(
                id="step-4",
                name="Сохранение результатов",
                priority=TaskPriority.HIGH,
                agent_type="universal"
            )
        ]

        # Устанавливаем зависимости
        # step-2 зависит от step-1
        await orchestrator.dependency_manager.add_dependency("step-2", "step-1")
        # step-3 зависит от step-2
        await orchestrator.dependency_manager.add_dependency("step-3", "step-2")
        # step-4 зависит от step-3
        await orchestrator.dependency_manager.add_dependency("step-4", "step-3")

        # Создаем план выполнения
        execution_plan = await orchestrator.create_execution_plan(tasks_with_deps)
        print(f"📋 План выполнения создан с {len(execution_plan.parallel_groups)} группами")

        # Отправляем задачи (они будут выполнены в правильном порядке)
        for task in tasks_with_deps:
            await orchestrator.submit_task(task)

        # Мониторим выполнение
        await asyncio.sleep(10)

        system_status = await orchestrator.get_system_status()
        print(f"✅ Система обработала зависимости. Статус: {system_status['orchestrator']['is_running']}")

    finally:
        await orchestrator.shutdown()


async def load_balancing_example():
    """
    Пример балансировки нагрузки между агентами.

    Демонстрирует:
    - Регистрация нескольких агентов одного типа
    - Автоматическое распределение задач
    - Мониторинг нагрузки
    """
    print("\n⚖️ Пример балансировки нагрузки...")

    config = OrchestrationConfig(
        max_concurrent_tasks=10,
        enable_load_balancing=True
    )
    orchestrator = AgentOrchestrator(config)
    await orchestrator.start()

    try:
        # Регистрируем несколько агентов одного типа
        for i in range(3):
            agent = Agent(
                id=f"worker-{i+1}",
                name=f"Worker Agent {i+1}",
                type="worker",
                capabilities=["processing"],
                supported_tasks=["work-task"],
                max_concurrent_tasks=2
            )
            await orchestrator.register_agent(agent)

        # Создаем много задач для демонстрации балансировки
        tasks = []
        for i in range(10):
            task = Task(
                id=f"work-task-{i+1}",
                name=f"Work Task {i+1}",
                agent_type="worker",
                priority=TaskPriority.NORMAL,
                estimated_duration=5
            )
            tasks.append(task)

        # Отправляем все задачи
        task_ids = await orchestrator.submit_tasks(tasks)
        print(f"📤 Отправлено {len(task_ids)} задач для балансировки")

        # Мониторим распределение нагрузки
        for _ in range(5):
            await asyncio.sleep(2)

            # Получаем статистику балансировщика
            system_status = await orchestrator.get_system_status()
            balancer_stats = system_status.get('load_balancer', {})

            print(f"⚖️ Статистика балансировщика: {balancer_stats.get('total_assignments', 0)} назначений")

    finally:
        await orchestrator.shutdown()


async def main():
    """Главная функция для запуска примеров."""
    print("🎯 Демонстрация системы оркестрации субагентов")
    print("=" * 50)

    try:
        # Базовый пример
        await basic_orchestration_example()

        # Пример с зависимостями
        await dependency_example()

        # Пример балансировки нагрузки
        await load_balancing_example()

        print("\n🎉 Все примеры выполнены успешно!")

    except Exception as e:
        print(f"❌ Ошибка при выполнении примеров: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Запуск примеров
    asyncio.run(main())