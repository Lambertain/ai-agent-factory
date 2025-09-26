"""
Интеграция с системой обработки ошибок.

Этот модуль обеспечивает интеграцию оркестратора с системой обработки ошибок
для централизованного управления сбоями и восстановления.
"""

import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
import traceback

from ..core.interfaces import IErrorHandler
from ..core.types import Task, Agent, TaskResult, TaskStatus


class ErrorSeverity(Enum):
    """Уровни серьезности ошибок."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Категории ошибок."""
    NETWORK = "network"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication"
    RESOURCE = "resource"
    VALIDATION = "validation"
    AGENT_FAILURE = "agent_failure"
    DEPENDENCY = "dependency"
    UNKNOWN = "unknown"


class OrchestrationErrorHandler(IErrorHandler):
    """
    Обработчик ошибок для системы оркестрации.

    Предоставляет:
    - Классификацию ошибок по типам и серьезности
    - Стратегии повторных попыток
    - Эскалацию критических ошибок
    - Сбор метрик по ошибкам
    - Интеграцию с внешними системами уведомлений
    """

    def __init__(self):
        """Инициализация обработчика ошибок."""
        self.logger = logging.getLogger(__name__)

        # История ошибок
        self._error_history: List[Dict[str, Any]] = []

        # Статистика ошибок
        self._error_stats: Dict[str, int] = {}

        # Обработчики для разных типов ошибок
        self._error_handlers: Dict[ErrorCategory, Callable] = {}

        # Настройки повторных попыток
        self._retry_config = {
            ErrorCategory.NETWORK: {"max_retries": 3, "delays": [1, 5, 15]},
            ErrorCategory.TIMEOUT: {"max_retries": 2, "delays": [5, 30]},
            ErrorCategory.AUTHENTICATION: {"max_retries": 1, "delays": [10]},
            ErrorCategory.RESOURCE: {"max_retries": 3, "delays": [10, 60, 300]},
            ErrorCategory.VALIDATION: {"max_retries": 0, "delays": []},
            ErrorCategory.AGENT_FAILURE: {"max_retries": 2, "delays": [5, 30]},
            ErrorCategory.DEPENDENCY: {"max_retries": 3, "delays": [1, 5, 15]},
            ErrorCategory.UNKNOWN: {"max_retries": 1, "delays": [5]},
        }

        # Callbacks для уведомлений
        self._notification_callbacks: List[Callable] = []

        # Блокировка для thread-safety
        self._lock = asyncio.Lock()

        # Инициализируем стандартные обработчики
        self._init_default_handlers()

    def _init_default_handlers(self):
        """Инициализировать стандартные обработчики ошибок."""
        self._error_handlers[ErrorCategory.NETWORK] = self._handle_network_error
        self._error_handlers[ErrorCategory.TIMEOUT] = self._handle_timeout_error
        self._error_handlers[ErrorCategory.AUTHENTICATION] = self._handle_auth_error
        self._error_handlers[ErrorCategory.RESOURCE] = self._handle_resource_error
        self._error_handlers[ErrorCategory.VALIDATION] = self._handle_validation_error
        self._error_handlers[ErrorCategory.AGENT_FAILURE] = self._handle_agent_failure
        self._error_handlers[ErrorCategory.DEPENDENCY] = self._handle_dependency_error
        self._error_handlers[ErrorCategory.UNKNOWN] = self._handle_unknown_error

    async def handle_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Обработать ошибку.

        Args:
            error: Исключение
            context: Контекст ошибки

        Returns:
            True если ошибка обработана успешно
        """
        async with self._lock:
            try:
                # Классифицируем ошибку
                category = self._classify_error(error)
                severity = self._determine_severity(error, category, context)

                # Создаем запись об ошибке
                error_record = {
                    "timestamp": datetime.now(timezone.utc),
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "category": category.value,
                    "severity": severity.value,
                    "context": context.copy(),
                    "traceback": traceback.format_exc(),
                    "task_id": context.get("task_id"),
                    "agent_id": context.get("agent_id")
                }

                # Добавляем в историю
                self._error_history.append(error_record)
                self._update_error_stats(category, severity)

                # Логируем ошибку
                self._log_error(error_record)

                # Обрабатываем ошибку специфичным обработчиком
                handler = self._error_handlers.get(category, self._handle_unknown_error)
                handled = await handler(error, error_record, context)

                # Уведомляем подписчиков
                await self._notify_subscribers(error_record)

                # Эскалируем критические ошибки
                if severity == ErrorSeverity.CRITICAL:
                    await self._escalate_critical_error(error_record)

                return handled

            except Exception as handler_error:
                self.logger.error(f"Error in error handler: {handler_error}")
                return False

    async def should_retry(self, error: Exception, retry_count: int) -> bool:
        """
        Определить, следует ли повторить операцию.

        Args:
            error: Исключение
            retry_count: Текущий счетчик попыток

        Returns:
            True если следует повторить
        """
        category = self._classify_error(error)
        config = self._retry_config.get(category, {"max_retries": 0})

        max_retries = config["max_retries"]
        should_retry = retry_count < max_retries

        self.logger.debug(f"Retry decision for {category.value}: {should_retry} "
                         f"(attempt {retry_count + 1}/{max_retries + 1})")

        return should_retry

    async def get_retry_delay(self, retry_count: int) -> int:
        """
        Получить задержку перед повтором.

        Args:
            retry_count: Счетчик попыток

        Returns:
            Задержка в секундах
        """
        # Используем экспоненциальный backoff по умолчанию
        base_delay = 2 ** retry_count
        max_delay = 300  # 5 минут максимум

        delay = min(base_delay, max_delay)
        self.logger.debug(f"Retry delay for attempt {retry_count}: {delay} seconds")

        return delay

    async def escalate_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Эскалировать ошибку.

        Args:
            error: Исключение
            context: Контекст ошибки

        Returns:
            True если эскалация успешна
        """
        try:
            category = self._classify_error(error)
            severity = self._determine_severity(error, category, context)

            escalation_record = {
                "timestamp": datetime.now(timezone.utc),
                "error_type": type(error).__name__,
                "error_message": str(error),
                "category": category.value,
                "severity": severity.value,
                "context": context,
                "escalation_reason": "manual_escalation"
            }

            await self._escalate_critical_error(escalation_record)
            self.logger.info(f"Escalated error: {error}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to escalate error: {e}")
            return False

    def _classify_error(self, error: Exception) -> ErrorCategory:
        """
        Классифицировать ошибку по категории.

        Args:
            error: Исключение

        Returns:
            Категория ошибки
        """
        error_type = type(error).__name__
        error_message = str(error).lower()

        # Сетевые ошибки
        if any(keyword in error_message for keyword in
               ["connection", "network", "socket", "dns", "host"]):
            return ErrorCategory.NETWORK

        # Таймауты
        if any(keyword in error_message for keyword in
               ["timeout", "timed out", "deadline"]):
            return ErrorCategory.TIMEOUT

        # Аутентификация
        if any(keyword in error_message for keyword in
               ["auth", "unauthorized", "forbidden", "token", "credential"]):
            return ErrorCategory.AUTHENTICATION

        # Ресурсы
        if any(keyword in error_message for keyword in
               ["memory", "disk", "cpu", "resource", "quota", "limit"]):
            return ErrorCategory.RESOURCE

        # Валидация
        if any(keyword in error_message for keyword in
               ["validation", "invalid", "malformed", "schema"]):
            return ErrorCategory.VALIDATION

        # Сбой агента
        if any(keyword in error_message for keyword in
               ["agent", "worker", "executor"]):
            return ErrorCategory.AGENT_FAILURE

        # Зависимости
        if any(keyword in error_message for keyword in
               ["dependency", "requirement", "prerequisite"]):
            return ErrorCategory.DEPENDENCY

        return ErrorCategory.UNKNOWN

    def _determine_severity(self, error: Exception, category: ErrorCategory,
                          context: Dict[str, Any]) -> ErrorSeverity:
        """
        Определить серьезность ошибки.

        Args:
            error: Исключение
            category: Категория ошибки
            context: Контекст

        Returns:
            Уровень серьезности
        """
        # Критические ошибки
        if category in [ErrorCategory.AUTHENTICATION, ErrorCategory.RESOURCE]:
            return ErrorSeverity.CRITICAL

        # Проверяем контекст задачи
        task_priority = context.get("task_priority")
        if task_priority and task_priority >= 4:  # HIGH/CRITICAL priority
            return ErrorSeverity.HIGH

        # Повторные ошибки повышают серьезность
        retry_count = context.get("retry_count", 0)
        if retry_count > 2:
            return ErrorSeverity.HIGH

        # Сетевые и таймауты - средняя серьезность
        if category in [ErrorCategory.NETWORK, ErrorCategory.TIMEOUT]:
            return ErrorSeverity.MEDIUM

        # Остальные - низкая серьезность
        return ErrorSeverity.LOW

    async def _handle_network_error(self, error: Exception, error_record: Dict[str, Any],
                                  context: Dict[str, Any]) -> bool:
        """Обработать сетевую ошибку."""
        self.logger.warning(f"Network error: {error}")
        # Можно добавить логику проверки сетевого соединения
        return True

    async def _handle_timeout_error(self, error: Exception, error_record: Dict[str, Any],
                                  context: Dict[str, Any]) -> bool:
        """Обработать ошибку таймаута."""
        self.logger.warning(f"Timeout error: {error}")
        # Можно добавить логику увеличения таймаутов
        return True

    async def _handle_auth_error(self, error: Exception, error_record: Dict[str, Any],
                               context: Dict[str, Any]) -> bool:
        """Обработать ошибку аутентификации."""
        self.logger.error(f"Authentication error: {error}")
        # Можно добавить логику обновления токенов
        return True

    async def _handle_resource_error(self, error: Exception, error_record: Dict[str, Any],
                                   context: Dict[str, Any]) -> bool:
        """Обработать ошибку ресурсов."""
        self.logger.error(f"Resource error: {error}")
        # Можно добавить логику освобождения ресурсов
        return True

    async def _handle_validation_error(self, error: Exception, error_record: Dict[str, Any],
                                     context: Dict[str, Any]) -> bool:
        """Обработать ошибку валидации."""
        self.logger.error(f"Validation error: {error}")
        # Ошибки валидации обычно не требуют повторных попыток
        return False

    async def _handle_agent_failure(self, error: Exception, error_record: Dict[str, Any],
                                  context: Dict[str, Any]) -> bool:
        """Обработать сбой агента."""
        self.logger.error(f"Agent failure: {error}")
        agent_id = context.get("agent_id")
        if agent_id:
            # Можно добавить логику перезапуска агента
            self.logger.info(f"Agent {agent_id} marked for restart")
        return True

    async def _handle_dependency_error(self, error: Exception, error_record: Dict[str, Any],
                                     context: Dict[str, Any]) -> bool:
        """Обработать ошибку зависимостей."""
        self.logger.warning(f"Dependency error: {error}")
        return True

    async def _handle_unknown_error(self, error: Exception, error_record: Dict[str, Any],
                                  context: Dict[str, Any]) -> bool:
        """Обработать неизвестную ошибку."""
        self.logger.error(f"Unknown error: {error}")
        return True

    def _update_error_stats(self, category: ErrorCategory, severity: ErrorSeverity):
        """Обновить статистику ошибок."""
        category_key = f"category_{category.value}"
        severity_key = f"severity_{severity.value}"

        self._error_stats[category_key] = self._error_stats.get(category_key, 0) + 1
        self._error_stats[severity_key] = self._error_stats.get(severity_key, 0) + 1
        self._error_stats["total"] = self._error_stats.get("total", 0) + 1

    def _log_error(self, error_record: Dict[str, Any]):
        """Логировать ошибку."""
        severity = error_record["severity"]
        category = error_record["category"]
        message = error_record["error_message"]
        task_id = error_record.get("task_id", "unknown")

        log_message = f"[{category.upper()}] Task {task_id}: {message}"

        if severity == "critical":
            self.logger.critical(log_message)
        elif severity == "high":
            self.logger.error(log_message)
        elif severity == "medium":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)

    async def _notify_subscribers(self, error_record: Dict[str, Any]):
        """Уведомить подписчиков об ошибке."""
        for callback in self._notification_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(error_record)
                else:
                    callback(error_record)
            except Exception as e:
                self.logger.error(f"Error in notification callback: {e}")

    async def _escalate_critical_error(self, error_record: Dict[str, Any]):
        """Эскалировать критическую ошибку."""
        self.logger.critical(f"CRITICAL ERROR ESCALATION: {error_record}")

        # Здесь можно добавить интеграцию с внешними системами:
        # - Отправка email/SMS уведомлений
        # - Создание тикетов в системе мониторинга
        # - Вызов webhook-ов
        # - Уведомление в Slack/Teams

    async def add_notification_callback(self, callback: Callable):
        """
        Добавить callback для уведомлений об ошибках.

        Args:
            callback: Функция обратного вызова
        """
        self._notification_callbacks.append(callback)

    async def get_error_statistics(self) -> Dict[str, Any]:
        """
        Получить статистику ошибок.

        Returns:
            Словарь со статистикой
        """
        async with self._lock:
            recent_errors = [
                error for error in self._error_history
                if (datetime.now(timezone.utc) - error["timestamp"]).total_seconds() < 3600
            ]

            return {
                "total_errors": len(self._error_history),
                "recent_errors_1h": len(recent_errors),
                "error_stats": self._error_stats.copy(),
                "error_rate_per_hour": len(recent_errors),
                "most_common_category": self._get_most_common_category(),
                "most_common_severity": self._get_most_common_severity()
            }

    def _get_most_common_category(self) -> str:
        """Получить наиболее частую категорию ошибок."""
        category_stats = {k: v for k, v in self._error_stats.items() if k.startswith("category_")}
        if not category_stats:
            return "unknown"

        return max(category_stats, key=category_stats.get).replace("category_", "")

    def _get_most_common_severity(self) -> str:
        """Получить наиболее частый уровень серьезности."""
        severity_stats = {k: v for k, v in self._error_stats.items() if k.startswith("severity_")}
        if not severity_stats:
            return "low"

        return max(severity_stats, key=severity_stats.get).replace("severity_", "")

    async def cleanup_old_errors(self, days: int = 7):
        """
        Очистить старые записи об ошибках.

        Args:
            days: Количество дней для хранения
        """
        async with self._lock:
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)

            original_count = len(self._error_history)
            self._error_history = [
                error for error in self._error_history
                if error["timestamp"] > cutoff_time
            ]

            cleaned_count = original_count - len(self._error_history)
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old error records")

    async def update_retry_config(self, category: ErrorCategory, config: Dict[str, Any]):
        """
        Обновить конфигурацию повторных попыток.

        Args:
            category: Категория ошибки
            config: Новая конфигурация
        """
        self._retry_config[category] = config
        self.logger.info(f"Updated retry config for {category.value}: {config}")