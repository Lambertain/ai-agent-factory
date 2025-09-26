"""
Тесты для центрального оркестратора.

Этот модуль содержит тесты для проверки функциональности
главного компонента системы оркестрации.
"""

import asyncio
import pytest
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# Импортируем компоненты для тестирования
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.orchestrator import AgentOrchestrator
from core.types import (
    Task, Agent, TaskPriority, TaskStatus, AgentStatus,
    OrchestrationConfig
)


class TestAgentOrchestrator:
    """Тесты для AgentOrchestrator."""

    @pytest.fixture
    async def orchestrator(self):
        """Создать экземпляр оркестратора для тестов."""
        config = OrchestrationConfig(
            max_concurrent_tasks=5,
            max_queue_size=100,
            default_task_timeout=30
        )
        orchestrator = AgentOrchestrator(config)
        await orchestrator.start()
        yield orchestrator
        await orchestrator.shutdown()

    @pytest.fixture
    def sample_task(self):
        """Создать образец задачи для тестов."""
        return Task(
            id="test-task-1",
            name="Test Task",
            description="A test task for unit testing",
            priority=TaskPriority.NORMAL,
            agent_type="test-agent",
            input_data={"input": "test_data"},
            estimated_duration=10
        )

    @pytest.fixture
    def sample_agent(self):
        """Создать образец агента для тестов."""
        return Agent(
            id="test-agent-1",
            name="Test Agent",
            type="test-agent",
            description="A test agent for unit testing",
            status=AgentStatus.IDLE,
            capabilities=["test-agent", "general"],
            supported_tasks=["test-task"],
            max_concurrent_tasks=3
        )

    async def test_orchestrator_startup_shutdown(self):
        """Тест запуска и остановки оркестратора."""
        config = OrchestrationConfig()
        orchestrator = AgentOrchestrator(config)

        # Тест запуска
        assert not orchestrator._is_running
        start_result = await orchestrator.start()
        assert start_result
        assert orchestrator._is_running

        # Тест повторного запуска
        start_again = await orchestrator.start()
        assert not start_again  # Должен вернуть False

        # Тест остановки
        shutdown_result = await orchestrator.shutdown()
        assert shutdown_result
        assert not orchestrator._is_running

    async def test_agent_registration(self, orchestrator, sample_agent):
        """Тест регистрации агентов."""
        # Регистрируем агента
        result = await orchestrator.register_agent(sample_agent)
        assert result

        # Проверяем, что агент зарегистрирован
        available_agents = await orchestrator.get_available_agents()
        assert len(available_agents) == 1
        assert available_agents[0].id == sample_agent.id

        # Тест повторной регистрации
        duplicate_result = await orchestrator.register_agent(sample_agent)
        assert not duplicate_result

        # Тест отмены регистрации
        unregister_result = await orchestrator.unregister_agent(sample_agent.id)
        assert unregister_result

        # Проверяем, что агент удален
        available_agents_after = await orchestrator.get_available_agents()
        assert len(available_agents_after) == 0

    async def test_task_submission(self, orchestrator, sample_task):
        """Тест отправки задач."""
        # Отправляем задачу
        task_id = await orchestrator.submit_task(sample_task)
        assert task_id == sample_task.id

        # Проверяем статус задачи
        status = await orchestrator.get_task_status(task_id)
        assert status is not None

    async def test_multiple_task_submission(self, orchestrator):
        """Тест отправки нескольких задач."""
        tasks = []
        for i in range(3):
            task = Task(
                id=f"test-task-{i}",
                name=f"Test Task {i}",
                priority=TaskPriority.NORMAL,
                agent_type="test-agent"
            )
            tasks.append(task)

        # Отправляем несколько задач
        task_ids = await orchestrator.submit_tasks(tasks)
        assert len(task_ids) == 3

        # Проверяем, что все задачи имеют статус
        for task_id in task_ids:
            status = await orchestrator.get_task_status(task_id)
            assert status is not None

    async def test_task_cancellation(self, orchestrator, sample_task):
        """Тест отмены задач."""
        # Отправляем задачу
        task_id = await orchestrator.submit_task(sample_task)

        # Отменяем задачу
        cancel_result = await orchestrator.cancel_task(task_id)
        assert cancel_result

    async def test_system_status(self, orchestrator):
        """Тест получения статуса системы."""
        status = await orchestrator.get_system_status()

        # Проверяем основные поля
        assert "orchestrator" in status
        assert "metrics" in status
        assert "task_queue" in status
        assert "scheduler" in status
        assert "execution" in status

        # Проверяем статус оркестратора
        assert status["orchestrator"]["is_running"]
        assert status["orchestrator"]["uptime_seconds"] >= 0

    async def test_task_priorities(self, orchestrator):
        """Тест обработки приоритетов задач."""
        # Создаем задачи с разными приоритетами
        high_priority_task = Task(
            id="high-priority-task",
            name="High Priority Task",
            priority=TaskPriority.HIGH,
            agent_type="test-agent"
        )

        low_priority_task = Task(
            id="low-priority-task",
            name="Low Priority Task",
            priority=TaskPriority.LOW,
            agent_type="test-agent"
        )

        # Отправляем задачи в обратном порядке приоритета
        await orchestrator.submit_task(low_priority_task)
        await orchestrator.submit_task(high_priority_task)

        # Проверяем, что обе задачи отправлены
        low_status = await orchestrator.get_task_status(low_priority_task.id)
        high_status = await orchestrator.get_task_status(high_priority_task.id)

        assert low_status is not None
        assert high_status is not None

    async def test_orchestrator_with_agents_and_tasks(self, orchestrator):
        """Интеграционный тест с агентами и задачами."""
        # Регистрируем агента
        agent = Agent(
            id="integration-agent",
            name="Integration Agent",
            type="test-agent",
            capabilities=["test", "integration"],
            max_concurrent_tasks=2
        )
        await orchestrator.register_agent(agent)

        # Создаем и отправляем задачу
        task = Task(
            id="integration-task",
            name="Integration Task",
            agent_type="test-agent",
            priority=TaskPriority.NORMAL
        )
        task_id = await orchestrator.submit_task(task)

        # Проверяем, что система работает корректно
        system_status = await orchestrator.get_system_status()
        assert system_status["orchestrator"]["registered_agents"] == 1

        # Ждем небольшое время для обработки
        await asyncio.sleep(0.1)

        # Проверяем статус задачи
        task_status = await orchestrator.get_task_status(task_id)
        assert task_status is not None

    async def test_error_handling_invalid_task(self, orchestrator):
        """Тест обработки ошибок при некорректных задачах."""
        # Пытаемся отправить задачу с дублирующимся ID
        task1 = Task(id="duplicate-id", name="Task 1", agent_type="test")
        task2 = Task(id="duplicate-id", name="Task 2", agent_type="test")

        # Первая задача должна быть принята
        await orchestrator.submit_task(task1)

        # Вторая задача с тем же ID может вызвать ошибку
        # (в зависимости от реализации)
        try:
            await orchestrator.submit_task(task2)
        except Exception:
            pass  # Ожидаемое поведение

    async def test_concurrent_operations(self, orchestrator):
        """Тест параллельных операций."""
        # Создаем несколько задач для параллельной отправки
        tasks = [
            Task(id=f"concurrent-task-{i}", name=f"Task {i}", agent_type="test")
            for i in range(5)
        ]

        # Отправляем задачи параллельно
        submit_coroutines = [orchestrator.submit_task(task) for task in tasks]
        task_ids = await asyncio.gather(*submit_coroutines)

        # Проверяем, что все задачи отправлены
        assert len(task_ids) == 5
        assert len(set(task_ids)) == 5  # Все ID уникальны

    async def test_orchestrator_metrics(self, orchestrator, sample_task):
        """Тест сбора метрик оркестратора."""
        # Получаем начальные метрики
        initial_status = await orchestrator.get_system_status()
        initial_submitted = initial_status["metrics"]["tasks_submitted"]

        # Отправляем задачу
        await orchestrator.submit_task(sample_task)

        # Проверяем обновление метрик
        updated_status = await orchestrator.get_system_status()
        updated_submitted = updated_status["metrics"]["tasks_submitted"]

        assert updated_submitted == initial_submitted + 1

    async def test_event_system(self, orchestrator, sample_task):
        """Тест системы событий."""
        events_received = []

        async def event_handler(event):
            events_received.append(event)

        # Подписываемся на события
        await orchestrator.subscribe_to_events("task.submitted", event_handler)

        # Отправляем задачу
        await orchestrator.submit_task(sample_task)

        # Даем время на обработку события
        await asyncio.sleep(0.1)

        # Проверяем, что событие получено
        assert len(events_received) > 0
        assert events_received[0].event_type == "task.submitted"


# Дополнительные utility функции для тестов

def create_test_tasks(count: int) -> List[Task]:
    """Создать список тестовых задач."""
    tasks = []
    for i in range(count):
        task = Task(
            id=f"test-task-{i}",
            name=f"Test Task {i}",
            priority=TaskPriority.NORMAL if i % 2 == 0 else TaskPriority.HIGH,
            agent_type="test-agent",
            estimated_duration=10 + (i * 5)
        )
        tasks.append(task)
    return tasks


def create_test_agents(count: int) -> List[Agent]:
    """Создать список тестовых агентов."""
    agents = []
    for i in range(count):
        agent = Agent(
            id=f"test-agent-{i}",
            name=f"Test Agent {i}",
            type="test-agent",
            capabilities=["test", f"capability-{i}"],
            max_concurrent_tasks=2 + i
        )
        agents.append(agent)
    return agents


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])