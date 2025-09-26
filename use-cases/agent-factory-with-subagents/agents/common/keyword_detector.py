#!/usr/bin/env python3
"""
Модуль определения ключевых команд для автоматического переключения на Project Manager.

Определяет команды пользователя, требующие анализа задач и переприоритизации.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CommandPattern:
    """Паттерн команды для определения."""

    keywords: List[str]
    action: str
    confidence: float
    context_required: bool = False


class KeywordDetector:
    """Детектор ключевых команд для переключения на Project Manager."""

    def __init__(self):
        """Инициализация детектора с паттернами команд."""
        self.patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> List[CommandPattern]:
        """
        Инициализация паттернов команд.

        Returns:
            Список паттернов для определения команд.
        """
        return [
            # Команды продолжения работы
            CommandPattern(
                keywords=["продолжай", "продолжи", "продолжить", "продолжаем"],
                action="continue_work",
                confidence=0.95
            ),
            CommandPattern(
                keywords=["работай", "работаем", "поработай", "работать"],
                action="continue_work",
                confidence=0.9
            ),
            CommandPattern(
                keywords=["дальше", "далее", "следующее", "следующий", "следующая"],
                action="next_task",
                confidence=0.9
            ),
            CommandPattern(
                keywords=["давай", "давайте", "начинай", "начинаем", "приступай"],
                action="start_work",
                confidence=0.85
            ),

            # Команды управления задачами
            CommandPattern(
                keywords=["задача", "задачу", "задачи", "таск", "таски"],
                action="task_management",
                confidence=0.8,
                context_required=True
            ),
            CommandPattern(
                keywords=["приоритет", "приоритеты", "приоритизация", "важность"],
                action="prioritize",
                confidence=0.9
            ),
            CommandPattern(
                keywords=["план", "планирование", "распланируй", "спланируй"],
                action="planning",
                confidence=0.85
            ),

            # Команды статуса и прогресса
            CommandPattern(
                keywords=["статус", "прогресс", "готовность", "состояние"],
                action="status_check",
                confidence=0.85
            ),
            CommandPattern(
                keywords=["что делать", "что дальше", "какая задача", "что сейчас"],
                action="next_task",
                confidence=0.9
            ),

            # Команды делегирования
            CommandPattern(
                keywords=["делегируй", "назначь", "передай", "распредели"],
                action="delegate",
                confidence=0.9
            ),
            CommandPattern(
                keywords=["команда", "команде", "агентам", "субагентам"],
                action="team_management",
                confidence=0.75,
                context_required=True
            ),

            # Команды анализа и решений
            CommandPattern(
                keywords=["анализируй", "проанализируй", "изучи", "исследуй"],
                action="analyze",
                confidence=0.85
            ),
            CommandPattern(
                keywords=["решение", "решить", "реши", "решай"],
                action="solve",
                confidence=0.8,
                context_required=True
            ),

            # Команды завершения и отчетности
            CommandPattern(
                keywords=["завершай", "заверши", "закончи", "финализируй"],
                action="finalize",
                confidence=0.85
            ),
            CommandPattern(
                keywords=["отчет", "отчитайся", "доложи", "рапорт"],
                action="report",
                confidence=0.9
            )
        ]

    def detect_command(self, text: str) -> Tuple[Optional[str], float]:
        """
        Определить команду в тексте.

        Args:
            text: Текст для анализа

        Returns:
            Кортеж (действие, уверенность) или (None, 0.0)
        """
        text_lower = text.lower().strip()

        # Проверка каждого паттерна
        best_match = None
        best_confidence = 0.0

        for pattern in self.patterns:
            for keyword in pattern.keywords:
                if keyword in text_lower:
                    # Учитываем позицию ключевого слова
                    position_factor = self._calculate_position_factor(text_lower, keyword)
                    adjusted_confidence = pattern.confidence * position_factor

                    # Учитываем контекст если требуется
                    if pattern.context_required:
                        context_factor = self._analyze_context(text_lower, keyword)
                        adjusted_confidence *= context_factor

                    if adjusted_confidence > best_confidence:
                        best_confidence = adjusted_confidence
                        best_match = pattern.action

        return (best_match, best_confidence)

    def _calculate_position_factor(self, text: str, keyword: str) -> float:
        """
        Рассчитать фактор позиции ключевого слова.

        Args:
            text: Текст для анализа
            keyword: Ключевое слово

        Returns:
            Фактор позиции (0.0-1.0)
        """
        position = text.find(keyword)
        text_length = len(text)

        if position == -1:
            return 0.0

        # Слово в начале текста имеет больший вес
        if position < text_length * 0.3:
            return 1.0
        elif position < text_length * 0.6:
            return 0.9
        else:
            return 0.8

    def _analyze_context(self, text: str, keyword: str) -> float:
        """
        Анализировать контекст вокруг ключевого слова.

        Args:
            text: Текст для анализа
            keyword: Ключевое слово

        Returns:
            Фактор контекста (0.0-1.0)
        """
        # Проверяем наличие дополнительных индикаторов
        indicators = {
            "archon": 0.2,
            "проект": 0.15,
            "менеджер": 0.15,
            "управление": 0.1,
            "координация": 0.1,
            "агент": 0.1,
            "субагент": 0.1,
            "делегир": 0.1
        }

        context_score = 0.5  # Базовый счет

        for indicator, weight in indicators.items():
            if indicator in text:
                context_score += weight

        return min(context_score, 1.0)

    def should_switch_to_project_manager(
        self,
        text: str,
        threshold: float = 0.7
    ) -> bool:
        """
        Определить, нужно ли переключиться на Project Manager.

        Args:
            text: Текст команды пользователя
            threshold: Порог уверенности для переключения

        Returns:
            True если нужно переключиться
        """
        action, confidence = self.detect_command(text)

        # Список действий, требующих Project Manager
        pm_actions = {
            "continue_work", "next_task", "start_work",
            "prioritize", "planning", "delegate",
            "team_management", "status_check"
        }

        if action in pm_actions and confidence >= threshold:
            return True

        # Проверка прямых упоминаний
        direct_mentions = [
            "project manager", "проджект менеджер",
            "менеджер проекта", "pm", "пм"
        ]

        text_lower = text.lower()
        for mention in direct_mentions:
            if mention in text_lower:
                return True

        return False

    def extract_task_context(self, text: str) -> Dict[str, any]:
        """
        Извлечь контекст задачи из текста.

        Args:
            text: Текст для анализа

        Returns:
            Словарь с контекстом задачи
        """
        context = {
            "has_urgency": False,
            "has_priority": False,
            "mentioned_agents": [],
            "task_type": None,
            "requires_planning": False
        }

        text_lower = text.lower()

        # Проверка срочности
        urgency_words = ["срочно", "быстро", "немедленно", "сейчас", "asap"]
        context["has_urgency"] = any(word in text_lower for word in urgency_words)

        # Проверка приоритета
        priority_words = ["важно", "критично", "приоритет", "первоочередно"]
        context["has_priority"] = any(word in text_lower for word in priority_words)

        # Поиск упоминаний агентов
        agent_patterns = [
            "analysis lead", "анализ",
            "blueprint architect", "архитектор",
            "implementation engineer", "разработчик",
            "quality guardian", "тестировщик",
            "deployment engineer", "девопс"
        ]

        for pattern in agent_patterns:
            if pattern in text_lower:
                context["mentioned_agents"].append(pattern)

        # Определение типа задачи
        if "анализ" in text_lower or "исследов" in text_lower:
            context["task_type"] = "analysis"
        elif "разработ" in text_lower or "создай" in text_lower:
            context["task_type"] = "development"
        elif "тест" in text_lower or "провер" in text_lower:
            context["task_type"] = "testing"
        elif "развертыв" in text_lower or "deploy" in text_lower:
            context["task_type"] = "deployment"

        # Проверка необходимости планирования
        planning_words = ["план", "этап", "шаг", "последовательность"]
        context["requires_planning"] = any(word in text_lower for word in planning_words)

        return context


# Глобальный экземпляр детектора
detector = KeywordDetector()


def should_switch_to_pm(text: str, threshold: float = 0.7) -> bool:
    """
    Упрощенная функция для проверки необходимости переключения.

    Args:
        text: Текст команды
        threshold: Порог уверенности

    Returns:
        True если нужно переключиться на Project Manager
    """
    return detector.should_switch_to_project_manager(text, threshold)


def get_command_context(text: str) -> Dict[str, any]:
    """
    Получить контекст команды.

    Args:
        text: Текст команды

    Returns:
        Контекст команды
    """
    action, confidence = detector.detect_command(text)
    context = detector.extract_task_context(text)
    context["detected_action"] = action
    context["confidence"] = confidence
    return context