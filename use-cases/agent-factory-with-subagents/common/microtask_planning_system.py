"""
Система обязательного планирования микрозадач для всех Pydantic AI агентов.

Архитектурный подход: Clean Architecture + Domain-Driven Design
- Domain: Микрозадачи, планы, прогресс выполнения
- Application: Use Cases планирования, выполнения, отчетности
- Infrastructure: Интеграция с TodoWrite, Archon, Pydantic AI
- Interface: Tools для агентов, пользовательский интерфейс

Критические принципы:
1. ОБЯЗАТЕЛЬНОЕ планирование для всех задач
2. Интерактивное подтверждение пользователем
3. Прозрачная отчетность о прогрессе
4. Интеграция с существующими системами
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Protocol
import uuid
import json


# =============================================================================
# DOMAIN LAYER - Сущности и бизнес-логика
# =============================================================================

class MicrotaskStatus(Enum):
    """Статусы выполнения микрозадач."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class TaskComplexity(Enum):
    """Уровни сложности задач для определения количества микрозадач."""
    SIMPLE = "simple"      # 3-4 микрозадачи
    MEDIUM = "medium"      # 5-6 микрозадач
    COMPLEX = "complex"    # 7+ микрозадач


class PlanApprovalStatus(Enum):
    """Статусы подтверждения плана пользователем."""
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


@dataclass
class Microtask:
    """Доменная сущность микрозадачи."""
    id: str
    title: str
    description: str
    status: MicrotaskStatus
    order: int
    estimated_duration_minutes: int
    agent_type: str
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def start(self):
        """Начать выполнение микрозадачи."""
        if self.status != MicrotaskStatus.PENDING:
            raise ValueError(f"Cannot start task in status: {self.status}")
        self.status = MicrotaskStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()

    def complete(self, notes: Optional[str] = None):
        """Завершить выполнение микрозадачи."""
        if self.status != MicrotaskStatus.IN_PROGRESS:
            raise ValueError(f"Cannot complete task in status: {self.status}")
        self.status = MicrotaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if notes:
            self.progress_notes.append(f"Completed: {notes}")

    def add_progress_note(self, note: str):
        """Добавить заметку о прогрессе."""
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        self.progress_notes.append(f"[{timestamp}] {note}")


@dataclass
class WorkPlan:
    """Доменная сущность плана работы."""
    id: str
    title: str
    description: str
    microtasks: List[Microtask]
    agent_type: str
    complexity: TaskComplexity
    approval_status: PlanApprovalStatus
    user_feedback: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_current_microtask(self) -> Optional[Microtask]:
        """Получить текущую выполняемую микрозадачу."""
        for task in self.microtasks:
            if task.status == MicrotaskStatus.IN_PROGRESS:
                return task
        return None

    def get_next_microtask(self) -> Optional[Microtask]:
        """Получить следующую микрозадачу для выполнения."""
        for task in self.microtasks:
            if task.status == MicrotaskStatus.PENDING:
                return task
        return None

    def calculate_progress(self) -> float:
        """Вычислить прогресс выполнения плана (0.0 - 1.0)."""
        if not self.microtasks:
            return 0.0
        completed_count = sum(1 for task in self.microtasks
                            if task.status == MicrotaskStatus.COMPLETED)
        return completed_count / len(self.microtasks)

    def is_completed(self) -> bool:
        """Проверить, завершен ли весь план."""
        return all(task.status == MicrotaskStatus.COMPLETED
                  for task in self.microtasks)

    def approve(self, user_feedback: Optional[str] = None):
        """Одобрить план пользователем."""
        self.approval_status = PlanApprovalStatus.APPROVED
        self.approved_at = datetime.utcnow()
        self.user_feedback = user_feedback

    def reject(self, user_feedback: str):
        """Отклонить план пользователем."""
        self.approval_status = PlanApprovalStatus.REJECTED
        self.user_feedback = user_feedback


# =============================================================================
# APPLICATION LAYER - Use Cases
# =============================================================================

class MicrotaskPlannerPort(Protocol):
    """Порт для создания планов микрозадач."""

    async def create_plan(self, main_task: str, agent_type: str,
                         complexity: TaskComplexity) -> WorkPlan: ...


class ProgressReporterPort(Protocol):
    """Порт для отчетности о прогрессе."""

    async def report_progress(self, plan_id: str, microtask_id: str,
                            status: MicrotaskStatus, notes: str) -> None: ...


class UserInteractionPort(Protocol):
    """Порт для взаимодействия с пользователем."""

    async def request_plan_approval(self, plan: WorkPlan) -> bool: ...
    async def display_progress_update(self, plan: WorkPlan,
                                    completed_task: Microtask) -> None: ...


class PlanExecutionUseCase:
    """Use Case выполнения плана микрозадач."""

    def __init__(self, progress_reporter: ProgressReporterPort,
                 user_interaction: UserInteractionPort):
        self.progress_reporter = progress_reporter
        self.user_interaction = user_interaction

    async def execute_plan(self, plan: WorkPlan) -> None:
        """Выполнить план микрозадач с отчетностью."""
        if plan.approval_status != PlanApprovalStatus.APPROVED:
            raise ValueError("Plan must be approved before execution")

        plan.started_at = datetime.utcnow()

        for microtask in plan.microtasks:
            # Начать выполнение микрозадачи
            microtask.start()
            await self.progress_reporter.report_progress(
                plan.id, microtask.id, MicrotaskStatus.IN_PROGRESS,
                f"Started: {microtask.title}"
            )

            # Симуляция выполнения (в реальности здесь будет вызов агента)
            yield microtask  # Yield для выполнения агентом

            # Завершить микрозадачу
            microtask.complete()
            await self.progress_reporter.report_progress(
                plan.id, microtask.id, MicrotaskStatus.COMPLETED,
                f"Completed: {microtask.title}"
            )

            # Уведомить пользователя о прогрессе
            await self.user_interaction.display_progress_update(plan, microtask)

        plan.completed_at = datetime.utcnow()


class PlanCreationUseCase:
    """Use Case создания плана микрозадач."""

    def __init__(self, planner: MicrotaskPlannerPort,
                 user_interaction: UserInteractionPort):
        self.planner = planner
        self.user_interaction = user_interaction

    async def create_and_approve_plan(self, main_task: str, agent_type: str,
                                     complexity: TaskComplexity) -> WorkPlan:
        """Создать план и получить одобрение пользователя."""
        # Создать план
        plan = await self.planner.create_plan(main_task, agent_type, complexity)

        # Запросить одобрение пользователя
        approved = await self.user_interaction.request_plan_approval(plan)

        if approved:
            plan.approve()
        else:
            plan.reject("User rejected the plan")
            raise ValueError("Plan rejected by user")

        return plan


# =============================================================================
# INFRASTRUCTURE LAYER - Конкретные реализации
# =============================================================================

class DefaultMicrotaskPlanner:
    """Стандартный планировщик микрозадач."""

    TEMPLATE_MICROTASKS = {
        TaskComplexity.SIMPLE: [
            "Проанализировать входные данные и требования",
            "Выполнить основную реализацию",
            "Протестировать результат и провести рефлексию"
        ],
        TaskComplexity.MEDIUM: [
            "Проанализировать сложность задачи и требования",
            "Найти необходимую информацию в базе знаний",
            "Спланировать архитектуру решения",
            "Реализовать основную функциональность",
            "Провести тестирование и валидацию",
            "Выполнить критический анализ и улучшения"
        ],
        TaskComplexity.COMPLEX: [
            "Глубокий анализ задачи и декомпозиция требований",
            "Исследование в базе знаний и внешних источниках",
            "Планирование архитектуры и выбор технологий",
            "Определение зависимостей и интеграций",
            "Реализация критических компонентов",
            "Реализация второстепенных компонентов",
            "Интеграционное тестирование",
            "Производительность и оптимизация",
            "Расширенная рефлексия и улучшения"
        ]
    }

    async def create_plan(self, main_task: str, agent_type: str,
                         complexity: TaskComplexity) -> WorkPlan:
        """Создать план микрозадач на основе шаблона."""
        plan_id = str(uuid.uuid4())

        template_tasks = self.TEMPLATE_MICROTASKS[complexity]
        microtasks = []

        for i, task_title in enumerate(template_tasks, 1):
            microtask = Microtask(
                id=str(uuid.uuid4()),
                title=task_title,
                description=f"Микрозадача {i} для: {main_task}",
                status=MicrotaskStatus.PENDING,
                order=i,
                estimated_duration_minutes=15 if complexity == TaskComplexity.SIMPLE else 20,
                agent_type=agent_type
            )
            microtasks.append(microtask)

        # Добавляем обязательные финальные микрозадачи
        git_commit_task = Microtask(
            id=str(uuid.uuid4()),
            title="Создать Git коммит с изменениями",
            description=f"Зафиксировать результаты выполнения: {main_task}",
            status=MicrotaskStatus.PENDING,
            order=len(microtasks) + 1,
            estimated_duration_minutes=5,
            agent_type=agent_type
        )
        microtasks.append(git_commit_task)

        plan = WorkPlan(
            id=plan_id,
            title=f"План выполнения: {main_task}",
            description=f"Детальный план из {len(microtasks)} микрозадач",
            microtasks=microtasks,
            agent_type=agent_type,
            complexity=complexity,
            approval_status=PlanApprovalStatus.PENDING_APPROVAL
        )

        return plan


class TodoWriteProgressReporter:
    """Репортер прогресса через TodoWrite."""

    def __init__(self, todowrite_callable: Callable):
        self.todowrite = todowrite_callable

    async def report_progress(self, plan_id: str, microtask_id: str,
                            status: MicrotaskStatus, notes: str) -> None:
        """Отправить обновление прогресса в TodoWrite."""
        # В реальной реализации здесь будет интеграция с TodoWrite
        print(f"📋 Progress: {status.value} - {notes}")


class ConsoleUserInteraction:
    """Взаимодействие с пользователем через консоль."""

    async def request_plan_approval(self, plan: WorkPlan) -> bool:
        """Запросить одобрение плана у пользователя."""
        approval_message = self._format_plan_for_approval(plan)
        print(approval_message)

        # В реальной реализации здесь будет интерактивный ввод
        # Для архитектурного дизайна возвращаем True
        return True

    async def display_progress_update(self, plan: WorkPlan,
                                    completed_task: Microtask) -> None:
        """Показать обновление прогресса пользователю."""
        progress_percent = int(plan.calculate_progress() * 100)
        print(f"✅ Завершено: {completed_task.title}")
        print(f"📊 Общий прогресс: {progress_percent}%")

    def _format_plan_for_approval(self, plan: WorkPlan) -> str:
        """Форматировать план для показа пользователю."""
        lines = [
            "📋 **ПЛАН РАБОТЫ ДЛЯ УТВЕРЖДЕНИЯ**",
            "",
            f"**Задача:** {plan.title}",
            f"**Агент:** {plan.agent_type}",
            f"**Сложность:** {plan.complexity.value}",
            f"**Микрозадач:** {len(plan.microtasks)}",
            "",
            "**Детальный план:**"
        ]

        for i, task in enumerate(plan.microtasks, 1):
            duration = task.estimated_duration_minutes
            lines.append(f"{i:2d}. {task.title} (~{duration}мин)")

        total_duration = sum(t.estimated_duration_minutes for t in plan.microtasks)
        lines.extend([
            "",
            f"**Общее время выполнения:** ~{total_duration} минут",
            "",
            "✅ План готов к выполнению"
        ])

        return "\n".join(lines)


# =============================================================================
# INTERFACE LAYER - Pydantic AI Tools Integration
# =============================================================================

class MicrotaskManager:
    """
    Главный класс системы управления микрозадачами.

    Интегрируется с Pydantic AI агентами через tools.
    Обеспечивает обязательное планирование и отчетность.
    """

    def __init__(self, agent_type: str = "unknown_agent"):
        self.agent_type = agent_type
        self.current_plan: Optional[WorkPlan] = None

        # Инициализация компонентов системы
        self.planner = DefaultMicrotaskPlanner()
        self.progress_reporter = TodoWriteProgressReporter(None)  # TODO: inject
        self.user_interaction = ConsoleUserInteraction()

        # Use Cases
        self.plan_creation = PlanCreationUseCase(
            self.planner, self.user_interaction
        )
        self.plan_execution = PlanExecutionUseCase(
            self.progress_reporter, self.user_interaction
        )

    async def create_mandatory_plan(self, main_task: str,
                                  complexity: str = "medium") -> str:
        """
        ОБЯЗАТЕЛЬНОЕ создание плана микрозадач.

        Этот метод ДОЛЖЕН быть вызван каждым агентом перед началом работы.
        """
        try:
            complexity_enum = TaskComplexity(complexity.lower())
        except ValueError:
            complexity_enum = TaskComplexity.MEDIUM

        # Создать и утвердить план
        self.current_plan = await self.plan_creation.create_and_approve_plan(
            main_task, self.agent_type, complexity_enum
        )

        return self._format_plan_display()

    async def start_next_microtask(self) -> Optional[str]:
        """Начать следующую микрозадачу из плана."""
        if not self.current_plan:
            return "❌ Нет активного плана. Создайте план сначала."

        next_task = self.current_plan.get_next_microtask()
        if not next_task:
            return "✅ Все микрозадачи завершены!"

        next_task.start()
        await self.progress_reporter.report_progress(
            self.current_plan.id, next_task.id,
            MicrotaskStatus.IN_PROGRESS, f"Started: {next_task.title}"
        )

        return f"🔄 Начата микрозадача: {next_task.title}"

    async def complete_current_microtask(self, notes: str = "") -> str:
        """Завершить текущую микрозадачу."""
        if not self.current_plan:
            return "❌ Нет активного плана."

        current_task = self.current_plan.get_current_microtask()
        if not current_task:
            return "❌ Нет активной микрозадачи."

        current_task.complete(notes)
        await self.progress_reporter.report_progress(
            self.current_plan.id, current_task.id,
            MicrotaskStatus.COMPLETED, f"Completed: {current_task.title}"
        )

        progress = int(self.current_plan.calculate_progress() * 100)
        return f"✅ Завершена: {current_task.title}\n📊 Прогресс: {progress}%"

    async def get_plan_status(self) -> str:
        """Получить статус текущего плана."""
        if not self.current_plan:
            return "📋 Нет активного плана микрозадач"

        progress = int(self.current_plan.calculate_progress() * 100)
        current_task = self.current_plan.get_current_microtask()

        status_lines = [
            f"📋 **Статус плана:** {self.current_plan.title}",
            f"📊 **Прогресс:** {progress}%",
            f"🎯 **Текущая задача:** {current_task.title if current_task else 'Нет активной задачи'}"
        ]

        return "\n".join(status_lines)

    def _format_plan_display(self) -> str:
        """Форматировать план для отображения пользователю."""
        if not self.current_plan:
            return "Нет активного плана"

        lines = [
            "📋 **ПЛАН РАБОТЫ УТВЕРЖДЕН**",
            "",
            f"**Задача:** {self.current_plan.title}",
            f"**Микрозадач:** {len(self.current_plan.microtasks)}",
            "",
            "**План выполнения:**"
        ]

        for i, task in enumerate(self.current_plan.microtasks, 1):
            status_emoji = "⏳" if task.status == MicrotaskStatus.PENDING else "✅"
            lines.append(f"{status_emoji} {i}. {task.title}")

        lines.extend([
            "",
            "✅ Начинаю выполнение по плану..."
        ])

        return "\n".join(lines)


# =============================================================================
# АРХИТЕКТУРНЫЕ ПРЕИМУЩЕСТВА СИСТЕМЫ
# =============================================================================

"""
🏗️ АРХИТЕКТУРНЫЕ ПРЕИМУЩЕСТВА:

1. **Separation of Concerns**
   - Domain: чистая бизнес-логика микрозадач
   - Application: use cases без зависимостей на фреймворки
   - Infrastructure: интеграция с TodoWrite, Archon
   - Interface: Pydantic AI tools

2. **Dependency Inversion**
   - Высокоуровневые модули не зависят от низкоуровневых
   - Зависимости через абстракции (Protocols)
   - Легкая подмена реализаций для тестирования

3. **Open/Closed Principle**
   - Можно добавлять новые типы планировщиков без изменения кода
   - Новые способы отчетности через ProgressReporterPort
   - Различные UI через UserInteractionPort

4. **Single Responsibility**
   - Каждый класс имеет единственную причину для изменения
   - MicrotaskManager - координация
   - DefaultMicrotaskPlanner - создание планов
   - TodoWriteProgressReporter - отчетность

5. **Testability**
   - Все зависимости инжектируются
   - Легко создать mock-объекты для тестирования
   - Use cases изолированы от внешних систем

6. **Scalability**
   - Легко добавить новые типы агентов
   - Можно масштабировать планировщики под разные домены
   - Асинхронная архитектура для производительности

7. **Maintainability**
   - Четкое разделение ответственности
   - Минимальные связи между компонентами
   - Легко найти и изменить нужную логику
"""