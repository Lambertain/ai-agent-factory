# -*- coding: utf-8 -*-
"""
Модуль планирования микрозадач для агентов.

Обеспечивает обязательное планирование задач на микрошаги
с подтверждением пользователя перед выполнением.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskComplexity(Enum):
    """Уровни сложности задач."""
    SIMPLE = "simple"      # 3-4 микрозадачи
    MEDIUM = "medium"      # 4-5 микрозадач
    COMPLEX = "complex"    # 5-7 микрозадач
    CRITICAL = "critical"  # 6-7 микрозадач с повышенным контролем


class MicrotaskStatus(Enum):
    """Статусы выполнения микрозадач."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


@dataclass
class Microtask:
    """Микрозадача в плане выполнения."""
    id: int
    title: str
    description: str
    estimated_time: str  # "5 мин", "15 мин", "30 мин"
    status: MicrotaskStatus = MicrotaskStatus.PENDING
    dependencies: List[int] = None  # ID микрозадач-зависимостей
    actual_result: str = ""
    notes: str = ""

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class TaskPlan:
    """План выполнения задачи с микрозадачами."""
    task_description: str
    complexity: TaskComplexity
    microtasks: List[Microtask]
    total_estimated_time: str
    confirmation_required: bool = True
    user_approved: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class MicrotaskPlanner:
    """Планировщик микрозадач для агентов."""

    def __init__(self):
        """Инициализация планировщика."""
        self.planning_templates = self._build_planning_templates()
        self.complexity_keywords = self._build_complexity_keywords()

    def _build_planning_templates(self) -> Dict[str, List[str]]:
        """Построить шаблоны планирования для разных типов задач."""
        return {
            "code_implementation": [
                "Анализ требований и выбор подхода",
                "Создание структуры и архитектуры",
                "Реализация основной логики",
                "Добавление обработки ошибок",
                "Создание тестов и валидация",
                "Документирование и финализация"
            ],

            "system_analysis": [
                "Сбор и анализ исходных данных",
                "Выявление ключевых компонентов",
                "Анализ взаимосвязей и зависимостей",
                "Выявление проблем и узких мест",
                "Формирование выводов и рекомендаций"
            ],

            "configuration_setup": [
                "Анализ требований к конфигурации",
                "Подготовка конфигурационных файлов",
                "Применение настроек и параметров",
                "Тестирование конфигурации",
                "Валидация и исправление ошибок"
            ],

            "data_processing": [
                "Анализ структуры и формата данных",
                "Подготовка данных и очистка",
                "Применение обработки и трансформаций",
                "Валидация результатов обработки",
                "Сохранение и экспорт результатов"
            ],

            "integration_task": [
                "Анализ интеграционных требований",
                "Настройка соединений и доступов",
                "Реализация механизмов интеграции",
                "Тестирование интеграционных потоков",
                "Обработка ошибок и резервных сценариев",
                "Мониторинг и логирование"
            ],

            "research_task": [
                "Определение направлений исследования",
                "Поиск и сбор информации",
                "Анализ и структурирование данных",
                "Формирование выводов",
                "Подготовка рекомендаций"
            ]
        }

    def _build_complexity_keywords(self) -> Dict[TaskComplexity, List[str]]:
        """Построить ключевые слова для определения сложности."""
        return {
            TaskComplexity.SIMPLE: [
                "простой", "быстрый", "базовый", "минимальный", "single",
                "простая настройка", "короткий", "trivial", "basic"
            ],

            TaskComplexity.MEDIUM: [
                "стандартный", "обычный", "средний", "moderate", "standard",
                "типичный", "нормальный", "regular", "common"
            ],

            TaskComplexity.COMPLEX: [
                "сложный", "комплексный", "многоэтапный", "complex", "comprehensive",
                "расширенный", "advanced", "sophisticated", "интегрированный",
                "архитектурный", "системный"
            ],

            TaskComplexity.CRITICAL: [
                "критический", "критичный", "важный", "critical", "crucial",
                "mission critical", "production", "безопасность", "security",
                "высокий приоритет", "urgent", "срочный"
            ]
        }

    def analyze_task_complexity(self, task_description: str) -> TaskComplexity:
        """
        Определить сложность задачи по описанию.

        Args:
            task_description: Описание задачи

        Returns:
            Уровень сложности задачи
        """
        task_lower = task_description.lower()

        # Подсчитываем совпадения ключевых слов для каждого уровня
        complexity_scores = {}

        for complexity, keywords in self.complexity_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            complexity_scores[complexity] = score

        # Если есть явные совпадения, выбираем наивысший уровень
        if any(score > 0 for score in complexity_scores.values()):
            return max(complexity_scores.keys(), key=lambda k: complexity_scores[k])

        # Эвристики по длине и содержанию задачи
        word_count = len(task_description.split())

        if word_count < 10:
            return TaskComplexity.SIMPLE
        elif word_count < 25:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.COMPLEX

    def detect_task_type(self, task_description: str) -> str:
        """
        Определить тип задачи по описанию.

        Args:
            task_description: Описание задачи

        Returns:
            Тип задачи для выбора шаблона
        """
        task_lower = task_description.lower()

        # Ключевые слова для разных типов задач
        type_keywords = {
            "code_implementation": [
                "код", "code", "реализация", "implementation", "программирование",
                "разработка", "development", "функция", "function", "метод", "class"
            ],
            "system_analysis": [
                "анализ", "analysis", "исследование", "research", "изучение",
                "рассмотрение", "evaluation", "assessment", "review"
            ],
            "configuration_setup": [
                "настройка", "configuration", "config", "setup", "установка",
                "конфигурация", "параметры", "settings", "environment"
            ],
            "data_processing": [
                "данные", "data", "обработка", "processing", "парсинг", "parsing",
                "трансформация", "transformation", "конвертация", "export", "import"
            ],
            "integration_task": [
                "интеграция", "integration", "подключение", "connection", "api",
                "webhook", "синхронизация", "sync", "импорт", "экспорт"
            ],
            "research_task": [
                "поиск", "search", "исследование", "research", "изучение", "study",
                "анализ рынка", "сравнение", "comparison", "benchmark"
            ]
        }

        # Находим тип с наибольшим количеством совпадений
        best_type = "system_analysis"  # по умолчанию
        best_score = 0

        for task_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            if score > best_score:
                best_score = score
                best_type = task_type

        return best_type

    def create_task_plan(
        self,
        task_description: str,
        agent_context: Optional[Dict[str, Any]] = None
    ) -> TaskPlan:
        """
        Создать план выполнения задачи с микрозадачами.

        Args:
            task_description: Описание задачи
            agent_context: Контекст агента (тип, экспертиза и т.д.)

        Returns:
            План выполнения с микрозадачами
        """
        complexity = self.analyze_task_complexity(task_description)
        task_type = self.detect_task_type(task_description)

        # Получаем базовый шаблон микрозадач
        template_steps = self.planning_templates.get(
            task_type,
            self.planning_templates["system_analysis"]
        )

        # Адаптируем под конкретную задачу и сложность
        microtasks = self._adapt_template_to_task(
            template_steps,
            task_description,
            complexity,
            agent_context
        )

        # Вычисляем общее время
        total_time = self._calculate_total_time(microtasks)

        return TaskPlan(
            task_description=task_description,
            complexity=complexity,
            microtasks=microtasks,
            total_estimated_time=total_time,
            confirmation_required=True
        )

    def _adapt_template_to_task(
        self,
        template_steps: List[str],
        task_description: str,
        complexity: TaskComplexity,
        agent_context: Optional[Dict[str, Any]]
    ) -> List[Microtask]:
        """Адаптировать шаблон под конкретную задачу."""
        microtasks = []

        # Определяем количество микрозадач в зависимости от сложности
        target_count = {
            TaskComplexity.SIMPLE: 3,
            TaskComplexity.MEDIUM: 4,
            TaskComplexity.COMPLEX: 6,
            TaskComplexity.CRITICAL: 7
        }[complexity]

        # Берем нужное количество шагов из шаблона
        selected_steps = template_steps[:target_count]

        # Если шагов меньше чем нужно, добавляем общие шаги
        while len(selected_steps) < target_count:
            selected_steps.append("Дополнительная проверка и валидация")

        # Создаем микрозадачи
        for i, step in enumerate(selected_steps):
            # Адаптируем описание под конкретную задачу
            adapted_title = self._adapt_step_to_context(step, task_description, agent_context)

            # Оцениваем время выполнения
            estimated_time = self._estimate_microtask_time(step, complexity)

            microtask = Microtask(
                id=i + 1,
                title=adapted_title,
                description=f"Выполнить: {adapted_title.lower()}",
                estimated_time=estimated_time
            )
            microtasks.append(microtask)

        return microtasks

    def _adapt_step_to_context(
        self,
        step: str,
        task_description: str,
        agent_context: Optional[Dict[str, Any]]
    ) -> str:
        """Адаптировать шаг под контекст задачи."""
        # Извлекаем ключевые слова из задачи
        key_words = self._extract_key_words(task_description)

        # Заменяем общие термины на конкретные
        adapted_step = step

        if key_words:
            # Подставляем ключевые слова в общие фразы
            replacements = {
                "основной логики": f"логики для {key_words[0]}",
                "данных": f"данных {key_words[0]}",
                "компонентов": f"компонентов {key_words[0]}",
                "требований": f"требований для {key_words[0]}",
                "результатов": f"результатов {key_words[0]}"
            }

            for old, new in replacements.items():
                if old in adapted_step:
                    adapted_step = adapted_step.replace(old, new)

        return adapted_step

    def _extract_key_words(self, task_description: str) -> List[str]:
        """Извлечь ключевые слова из описания задачи."""
        # Удаляем стоп-слова и извлекаем существенные термины
        stop_words = {
            'для', 'и', 'в', 'на', 'с', 'по', 'к', 'от', 'до', 'при', 'о', 'об',
            'что', 'как', 'где', 'когда', 'который', 'которая', 'которое',
            'этот', 'эта', 'это', 'тот', 'та', 'то', 'все', 'всё', 'можно', 'нужно'
        }

        words = re.findall(r'\b[а-яёa-z]+\b', task_description.lower())
        key_words = [word for word in words if len(word) > 3 and word not in stop_words]

        return key_words[:3]  # Возвращаем первые 3 ключевых слова

    def _estimate_microtask_time(self, step: str, complexity: TaskComplexity) -> str:
        """Оценить время выполнения микрозадачи."""
        base_times = {
            TaskComplexity.SIMPLE: "10 мин",
            TaskComplexity.MEDIUM: "15 мин",
            TaskComplexity.COMPLEX: "25 мин",
            TaskComplexity.CRITICAL: "30 мин"
        }

        # Корректируем время в зависимости от типа шага
        time_modifiers = {
            "анализ": 1.2,
            "реализация": 1.5,
            "тестирование": 1.3,
            "документирование": 0.8,
            "настройка": 1.1,
            "проверка": 0.9
        }

        base_time = base_times[complexity]
        base_minutes = int(base_time.split()[0])

        # Применяем модификатор времени
        for keyword, modifier in time_modifiers.items():
            if keyword in step.lower():
                base_minutes = int(base_minutes * modifier)
                break

        return f"{base_minutes} мин"

    def _calculate_total_time(self, microtasks: List[Microtask]) -> str:
        """Вычислить общее время выполнения."""
        total_minutes = 0

        for microtask in microtasks:
            time_str = microtask.estimated_time
            minutes = int(time_str.split()[0])
            total_minutes += minutes

        if total_minutes < 60:
            return f"{total_minutes} мин"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes == 0:
                return f"{hours} ч"
            else:
                return f"{hours} ч {minutes} мин"

    def format_plan_for_user(self, plan: TaskPlan) -> str:
        """
        Форматировать план для показа пользователю.

        Args:
            plan: План выполнения

        Returns:
            Форматированное описание плана
        """
        output = [
            "ПЛАН ВЫПОЛНЕНИЯ ЗАДАЧИ",
            "=" * 40,
            f"Задача: {plan.task_description}",
            f"Сложность: {plan.complexity.value}",
            f"Общее время: {plan.total_estimated_time}",
            f"Количество шагов: {len(plan.microtasks)}",
            "",
            "МИКРОЗАДАЧИ:"
        ]

        for microtask in plan.microtasks:
            status_symbol = {
                MicrotaskStatus.PENDING: "⏳",
                MicrotaskStatus.IN_PROGRESS: "🔄",
                MicrotaskStatus.COMPLETED: "✅",
                MicrotaskStatus.BLOCKED: "🚫",
                MicrotaskStatus.SKIPPED: "⏭️"
            }.get(microtask.status, "⏳")

            output.append(f"{microtask.id}. {status_symbol} {microtask.title} ({microtask.estimated_time})")
            if microtask.dependencies:
                dep_str = ", ".join(str(d) for d in microtask.dependencies)
                output.append(f"   └── Зависит от: {dep_str}")

        output.extend([
            "",
            "Хотите продолжить выполнение по этому плану? (да/нет)"
        ])

        return "\n".join(output)

    def update_microtask_status(
        self,
        plan: TaskPlan,
        microtask_id: int,
        status: MicrotaskStatus,
        result: str = "",
        notes: str = ""
    ) -> bool:
        """
        Обновить статус микрозадачи.

        Args:
            plan: План выполнения
            microtask_id: ID микрозадачи
            status: Новый статус
            result: Результат выполнения
            notes: Заметки

        Returns:
            True если обновление успешно
        """
        for microtask in plan.microtasks:
            if microtask.id == microtask_id:
                microtask.status = status
                if result:
                    microtask.actual_result = result
                if notes:
                    microtask.notes = notes
                return True
        return False

    def get_next_microtask(self, plan: TaskPlan) -> Optional[Microtask]:
        """
        Получить следующую микрозадачу для выполнения.

        Args:
            plan: План выполнения

        Returns:
            Следующая микрозадача или None если все выполнены
        """
        for microtask in plan.microtasks:
            if microtask.status == MicrotaskStatus.PENDING:
                # Проверяем зависимости
                dependencies_completed = all(
                    any(mt.id == dep_id and mt.status == MicrotaskStatus.COMPLETED
                        for mt in plan.microtasks)
                    for dep_id in microtask.dependencies
                )

                if dependencies_completed:
                    return microtask

        return None

    def format_progress_report(self, plan: TaskPlan) -> str:
        """
        Форматировать отчет о прогрессе выполнения.

        Args:
            plan: План выполнения

        Returns:
            Отчет о прогрессе
        """
        completed = sum(1 for mt in plan.microtasks if mt.status == MicrotaskStatus.COMPLETED)
        total = len(plan.microtasks)
        progress = (completed / total) * 100 if total > 0 else 0

        output = [
            f"ПРОГРЕСС ВЫПОЛНЕНИЯ: {progress:.0f}% ({completed}/{total})",
            "=" * 50
        ]

        for microtask in plan.microtasks:
            status_symbol = {
                MicrotaskStatus.PENDING: "⏳",
                MicrotaskStatus.IN_PROGRESS: "🔄",
                MicrotaskStatus.COMPLETED: "✅",
                MicrotaskStatus.BLOCKED: "🚫",
                MicrotaskStatus.SKIPPED: "⏭️"
            }.get(microtask.status, "⏳")

            line = f"{microtask.id}. {status_symbol} {microtask.title}"

            if microtask.status == MicrotaskStatus.COMPLETED and microtask.actual_result:
                line += f"\n   Результат: {microtask.actual_result[:100]}"

            if microtask.notes:
                line += f"\n   Заметки: {microtask.notes[:100]}"

            output.append(line)

        return "\n".join(output)

    def should_create_git_commit(self, plan: TaskPlan) -> bool:
        """
        Определить нужно ли создавать Git коммит на основе прогресса.

        Args:
            plan: План выполнения

        Returns:
            True если нужно создать коммит
        """
        # Создаем коммит если:
        # 1. Все микрозадачи завершены
        # 2. Завершена критическая микрозадача
        # 3. Завершено больше половины задач

        completed = [mt for mt in plan.microtasks if mt.status == MicrotaskStatus.COMPLETED]
        total = len(plan.microtasks)

        if total == 0:
            return False

        # Все задачи завершены
        if len(completed) == total:
            return True

        # Больше половины задач завершены
        if len(completed) >= total / 2:
            return True

        # Есть критические задачи с "реализация" или "implementation"
        for microtask in completed:
            if any(keyword in microtask.title.lower()
                   for keyword in ['реализация', 'implementation', 'создание', 'разработка']):
                return True

        return False


# Функции-утилиты для интеграции в агенты
def create_microtask_plan(
    task_description: str,
    agent_context: Optional[Dict[str, Any]] = None
) -> TaskPlan:
    """
    Универсальная функция создания плана микрозадач.

    Args:
        task_description: Описание задачи
        agent_context: Контекст агента

    Returns:
        План выполнения задачи
    """
    planner = MicrotaskPlanner()
    return planner.create_task_plan(task_description, agent_context)


async def auto_commit_on_microtask_completion(
    plan: TaskPlan,
    microtask_id: int,
    result: str = ""
) -> str:
    """
    Автоматический Git коммит при завершении критической микрозадачи.

    Args:
        plan: План выполнения
        microtask_id: ID завершенной микрозадачи
        result: Результат выполнения

    Returns:
        Сообщение о результате коммита
    """
    planner = MicrotaskPlanner()

    # Обновляем статус микрозадачи
    planner.update_microtask_status(plan, microtask_id, MicrotaskStatus.COMPLETED, result)

    # Проверяем нужен ли Git коммит
    if planner.should_create_git_commit(plan):
        try:
            from .git_manager import auto_commit_on_task_completion

            # Формируем описание коммита
            completed_tasks = [mt.title for mt in plan.microtasks if mt.status == MicrotaskStatus.COMPLETED]
            commit_description = f"Завершены микрозадачи: {', '.join(completed_tasks[:3])}"
            if len(completed_tasks) > 3:
                commit_description += f" и еще {len(completed_tasks) - 3}"

            # Создаем коммит
            commit_result = await auto_commit_on_task_completion(commit_description)
            return f"Микрозадача завершена. {commit_result}"

        except Exception as e:
            return f"Микрозадача завершена. Ошибка Git коммита: {e}"
    else:
        return f"Микрозадача {microtask_id} завершена: {result}"


def check_git_commit_needed(plan: TaskPlan) -> Tuple[bool, str]:
    """
    Проверить нужен ли Git коммит для текущего плана.

    Args:
        plan: План выполнения

    Returns:
        Tuple[bool, str]: (нужен_коммит, описание_причины)
    """
    planner = MicrotaskPlanner()

    if planner.should_create_git_commit(plan):
        completed = [mt for mt in plan.microtasks if mt.status == MicrotaskStatus.COMPLETED]
        total = len(plan.microtasks)

        if len(completed) == total:
            return True, "Все микрозадачи завершены"
        elif len(completed) >= total / 2:
            return True, f"Завершено {len(completed)} из {total} микрозадач (более половины)"
        else:
            critical_completed = [mt for mt in completed
                                if any(keyword in mt.title.lower()
                                     for keyword in ['реализация', 'implementation', 'создание', 'разработка'])]
            if critical_completed:
                return True, f"Завершена критическая микрозадача: {critical_completed[0].title}"

    return False, "Условия для коммита не выполнены"


def format_plan_for_approval(plan: TaskPlan) -> str:
    """
    Форматировать план для запроса одобрения у пользователя.

    Args:
        plan: План выполнения

    Returns:
        Форматированный план
    """
    planner = MicrotaskPlanner()
    return planner.format_plan_for_user(plan)


def track_microtask_progress(
    plan: TaskPlan,
    microtask_id: int,
    status: MicrotaskStatus,
    result: str = ""
) -> str:
    """
    Отследить прогресс выполнения микрозадачи.

    Args:
        plan: План выполнения
        microtask_id: ID микрозадачи
        status: Новый статус
        result: Результат выполнения

    Returns:
        Отчет о прогрессе
    """
    planner = MicrotaskPlanner()
    planner.update_microtask_status(plan, microtask_id, status, result)
    return planner.format_progress_report(plan)


# Экспорт для других модулей
__all__ = [
    'MicrotaskPlanner',
    'TaskPlan',
    'Microtask',
    'TaskComplexity',
    'MicrotaskStatus',
    'create_microtask_plan',
    'format_plan_for_approval',
    'track_microtask_progress',
    'auto_commit_on_microtask_completion',
    'check_git_commit_needed'
]