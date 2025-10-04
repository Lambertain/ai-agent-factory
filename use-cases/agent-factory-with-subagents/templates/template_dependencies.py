# -*- coding: utf-8 -*-
"""
ШАБЛОН: Зависимости для Pydantic AI агента

Этот шаблон содержит конфигурацию для агента.
Dependencies определяют контекст работы когда вы (Claude) принимаете роль эксперта.

ИСПОЛЬЗОВАНИЕ:
1. Замените [AGENT_NAME] на имя вашего агента (например, payment_integration)
2. Укажите knowledge_tags для поиска в RAG
3. Добавьте специфичные настройки для вашей области
4. Сохраните как agents/[agent_name]/dependencies.py

ВАЖНО: Это конфигурация для ВАШЕЙ работы в роли эксперта, не автономного агента.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# ============================================================================
# КОНСТАНТЫ АГЕНТА (ОБЯЗАТЕЛЬНО ЗАПОЛНИТЬ)
# ============================================================================

# 🚨 ОБЯЗАТЕЛЬНО: замените на уникальное имя вашего агента
AGENT_NAME = "[agent_name]"  # Например: "payment_integration"

# 🚨 ОБЯЗАТЕЛЬНО: укажите теги для поиска знаний роли в RAG
DEFAULT_KNOWLEDGE_TAGS = [
    "[agent_name]",           # Имя агента
    "agent-knowledge",        # Маркер знаний агента
    "pydantic-ai",            # Фреймворк
    "[domain]"                # Область экспертизы (например: payments, security, ui)
]

# Опционально: domain для фильтрации в RAG
DEFAULT_KNOWLEDGE_DOMAIN = None  # Например: "docs.stripe.com" для Payment Agent

# ID проекта AI Agent Factory в Archon (для отслеживания задач)
DEFAULT_ARCHON_PROJECT_ID = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

# ============================================================================
# КЛАСС ЗАВИСИМОСТЕЙ АГЕНТА
# Это контекст для работы в роли эксперта
# ============================================================================

@dataclass
class [AGENT_NAME_PASCAL]Dependencies:
    """
    Зависимости для работы в роли [Agent Display Name].

    Этот dataclass содержит конфигурацию и контекст для работы
    когда вы (Claude) принимаете роль этого эксперта:
    - API ключи и базовые настройки
    - Теги знаний для поиска в RAG
    - Настройки для универсальности
    - Специфичные параметры роли

    ОБЯЗАТЕЛЬНЫЕ ПОЛЯ:
    - api_key: API ключ для LLM провайдера
    - knowledge_tags: теги для поиска специализированных знаний
    """

    # ========================================================================
    # ОСНОВНЫЕ НАСТРОЙКИ (ОБЯЗАТЕЛЬНО)
    # ========================================================================

    api_key: str
    """API ключ для LLM провайдера (обязательно)."""

    project_path: str = ""
    """Путь к проекту (опционально)."""

    # ========================================================================
    # ИДЕНТИФИКАЦИЯ РОЛИ
    # ========================================================================

    agent_name: str = AGENT_NAME
    """Имя роли эксперта."""

    agent_type: str = "[agent_type]"
    """Тип экспертизы (например: payment_integration, security_audit, ui_ux)."""

    # ========================================================================
    # ЗНАНИЯ РОЛИ (для поиска в RAG)
    # ========================================================================

    knowledge_tags: List[str] = field(default_factory=lambda: DEFAULT_KNOWLEDGE_TAGS.copy())
    """Теги для поиска специализированных знаний роли в RAG."""

    knowledge_domain: Optional[str] = DEFAULT_KNOWLEDGE_DOMAIN
    """Опциональный домен для фильтрации знаний (например: docs.stripe.com)."""

    knowledge_match_count: int = 5
    """Количество результатов при поиске в базе знаний."""

    # ========================================================================
    # УНИВЕРСАЛЬНОСТЬ РОЛИ
    # Настройки для адаптации поведения под разные проекты
    # ========================================================================

    domain_type: str = "[domain]"
    """
    Тип домена для адаптации роли.
    Примеры: "payments", "security", "ui/ux", "performance", "database"
    """

    project_type: str = "universal"
    """
    Тип проекта для адаптации советов роли.
    Примеры: "e-commerce", "saas", "blog", "crm", "social-network"
    """

    framework: Optional[str] = None
    """
    Используемый фреймворк (для адаптации примеров).
    Примеры: "Next.js", "React", "Vue", "Django", "FastAPI"
    """

    # ========================================================================
    # ИНТЕГРАЦИЯ С ARCHON
    # Для отслеживания задач когда вы работаете в роли
    # ========================================================================

    archon_project_id: str = DEFAULT_ARCHON_PROJECT_ID
    """ID проекта в Archon для отслеживания задач."""

    current_task_id: Optional[str] = None
    """ID текущей задачи в Archon (если работаете над задачей)."""

    # ========================================================================
    # СПЕЦИФИЧНЫЕ ДЛЯ РОЛИ НАСТРОЙКИ
    # Добавьте здесь настройки специфичные для вашей области экспертизы
    # ========================================================================

    # ШАБЛОН: Замените на реальные настройки вашей роли
    # Примеры для разных ролей:
    #
    # Payment Expert:
    #   stripe_api_key: Optional[str] = None
    #   paypal_client_id: Optional[str] = None
    #   supported_currencies: List[str] = field(default_factory=lambda: ["USD", "EUR"])
    #
    # Security Expert:
    #   scan_depth: str = "comprehensive"  # basic, standard, comprehensive
    #   vulnerability_threshold: str = "medium"  # low, medium, high, critical
    #   compliance_standards: List[str] = field(default_factory=lambda: ["OWASP", "CWE"])
    #
    # UI/UX Expert:
    #   design_system: Optional[str] = "material"  # material, bootstrap, custom
    #   accessibility_level: str = "WCAG-AA"  # WCAG-A, WCAG-AA, WCAG-AAA
    #   target_devices: List[str] = field(default_factory=lambda: ["desktop", "mobile"])

    [agent_specific_setting]: Optional[str] = None
    """Описание специфичной настройки роли."""

    # ========================================================================
    # КОНТЕКСТ РАБОТЫ
    # ========================================================================

    session_id: Optional[str] = None
    """ID сессии для отслеживания взаимодействий."""

    user_id: Optional[str] = None
    """ID пользователя для персонализации."""

    work_context: Dict[str, Any] = field(default_factory=dict)
    """Дополнительный контекст работы в роли."""

    # ========================================================================
    # МЕТОДЫ
    # ========================================================================

    def __post_init__(self):
        """Инициализация и валидация зависимостей."""
        # Автоопределение имени роли если не указано
        if not self.agent_name or self.agent_name == AGENT_NAME:
            module_parts = self.__class__.__module__.split('.')
            if 'agents' in module_parts:
                agent_index = module_parts.index('agents')
                if agent_index + 1 < len(module_parts):
                    self.agent_name = module_parts[agent_index + 1]

        # Установка knowledge_tags по умолчанию если пусто
        if not self.knowledge_tags:
            agent_base_name = self.agent_name.replace('_agent', '') if self.agent_name else 'unknown'
            self.knowledge_tags = [
                agent_base_name,
                "agent-knowledge",
                "pydantic-ai"
            ]

        # Валидация API ключа
        if not self.api_key:
            raise ValueError("API ключ обязателен для работы в роли эксперта")

    def get_search_context(self) -> Dict[str, Any]:
        """
        Получить контекст для поиска в базе знаний.

        Returns:
            Словарь с параметрами поиска
        """
        return {
            "tags": self.knowledge_tags,
            "domain": self.knowledge_domain,
            "match_count": self.knowledge_match_count
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать зависимости в словарь для логирования.

        Returns:
            Словарь с настройками (без секретных данных)
        """
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "domain_type": self.domain_type,
            "project_type": self.project_type,
            "framework": self.framework,
            "knowledge_tags": self.knowledge_tags,
            "knowledge_domain": self.knowledge_domain,
            "session_id": self.session_id
        }


# ============================================================================
# ЭКСПОРТ
# ============================================================================

__all__ = [
    "[AGENT_NAME_PASCAL]Dependencies",
    "AGENT_NAME",
    "DEFAULT_KNOWLEDGE_TAGS",
    "DEFAULT_KNOWLEDGE_DOMAIN",
    "DEFAULT_ARCHON_PROJECT_ID"
]
