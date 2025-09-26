# -*- coding: utf-8 -*-
"""
Универсальные декораторы для Pydantic AI агентов

Предоставляет декораторы для автоматического добавления интеграций
ко всем Pydantic AI агентам без изменения их кода.
"""

import functools
import asyncio
import logging
from typing import Any, Callable, Dict, Optional, TypeVar, Awaitable
from pydantic_ai import Agent, RunContext

from .pydantic_ai_integrations import PydanticAIIntegration

logger = logging.getLogger(__name__)

T = TypeVar('T')

# Глобальная система интеграций
_integration_system = PydanticAIIntegration()

def with_integrations(
    agent_type: str = "unknown",
    enable_pm_switch: bool = True,
    enable_competency_check: bool = True,
    enable_microtask_planning: bool = True,
    enable_git_commits: bool = True,
    enable_russian_localization: bool = True
):
    """
    Декоратор для автоматического добавления интеграций к Pydantic AI агентам.

    Args:
        agent_type: Тип агента для интеграций
        enable_pm_switch: Включить переключение на Project Manager
        enable_competency_check: Включить проверку компетенций
        enable_microtask_planning: Включить планирование микрозадач
        enable_git_commits: Включить автоматические Git коммиты
        enable_russian_localization: Включить русскую локализацию

    Returns:
        Декорированная функция с интеграциями
    """
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                # Выполняем pre-run интеграции
                if len(args) >= 1:
                    user_message = str(args[0])

                    pre_result = await _integration_system.apply_pre_run_integrations(
                        agent_name=func.__name__,
                        user_message=user_message,
                        agent_type=agent_type
                    )

                    if pre_result:
                        return pre_result

                # Выполняем основную функцию
                result = await func(*args, **kwargs)

                # Выполняем post-run интеграции
                if len(args) >= 1:
                    user_message = str(args[0])

                    enhanced_result = await _integration_system.apply_post_run_integrations(
                        agent_name=func.__name__,
                        user_message=user_message,
                        result=str(result),
                        agent_type=agent_type
                    )

                    return enhanced_result

                return result

            except Exception as e:
                logger.error(f"Ошибка в интеграциях для {func.__name__}: {e}")
                # В случае ошибки интеграций выполняем основную функцию
                return await func(*args, **kwargs)

        return wrapper
    return decorator

def with_collective_work_tools(agent: Agent) -> Agent:
    """
    Декоратор для автоматического добавления обязательных инструментов коллективной работы.

    Args:
        agent: Pydantic AI агент

    Returns:
        Агент с добавленными инструментами коллективной работы
    """
    from .collective_work_tools import (
        break_down_to_microtasks,
        report_microtask_progress,
        reflect_and_improve,
        check_delegation_need
    )

    # Добавляем обязательные инструменты коллективной работы
    agent.tool(break_down_to_microtasks)
    agent.tool(report_microtask_progress)
    agent.tool(reflect_and_improve)
    agent.tool(check_delegation_need)

    logger.info(f"Добавлены обязательные инструменты коллективной работы для агента {agent.__class__.__name__}")

    return agent

def with_knowledge_search(agent: Agent, knowledge_tags: list = None, knowledge_domain: str = None) -> Agent:
    """
    Декоратор для добавления инструмента поиска в базе знаний.

    Args:
        agent: Pydantic AI агент
        knowledge_tags: Теги для фильтрации знаний
        knowledge_domain: Домен знаний

    Returns:
        Агент с добавленным инструментом поиска знаний
    """
    @agent.tool
    async def search_agent_knowledge(
        ctx: RunContext,
        query: str,
        match_count: int = 5
    ) -> str:
        """
        Поиск в специализированной базе знаний агента.

        Args:
            query: Поисковый запрос
            match_count: Количество результатов

        Returns:
            Найденная информация из базы знаний
        """
        try:
            # Используем Archon RAG для поиска
            from ..common.archon_integrations import search_knowledge_base

            result = await search_knowledge_base(
                query=query,
                tags=knowledge_tags,
                domain=knowledge_domain,
                match_count=match_count
            )

            return result

        except Exception as e:
            return f"Ошибка поиска в базе знаний: {e}"

    logger.info(f"Добавлен инструмент поиска знаний для агента {agent.__class__.__name__}")

    return agent

def create_universal_pydantic_agent(
    model,
    deps_type,
    system_prompt: str,
    agent_type: str = "unknown",
    knowledge_tags: list = None,
    knowledge_domain: str = None,
    with_collective_tools: bool = True,
    with_knowledge_tool: bool = True
) -> Agent:
    """
    Универсальная фабрика для создания Pydantic AI агентов со всеми интеграциями.

    Args:
        model: LLM модель
        deps_type: Тип зависимостей
        system_prompt: Системный промпт
        agent_type: Тип агента
        knowledge_tags: Теги знаний
        knowledge_domain: Домен знаний
        with_collective_tools: Добавить инструменты коллективной работы
        with_knowledge_tool: Добавить инструмент поиска знаний

    Returns:
        Полностью сконфигурированный Pydantic AI агент
    """
    # Создаем базовый агент
    agent = Agent(
        model=model,
        deps_type=deps_type,
        system_prompt=system_prompt
    )

    # Добавляем обязательные инструменты коллективной работы
    if with_collective_tools:
        agent = with_collective_work_tools(agent)

    # Добавляем инструмент поиска знаний
    if with_knowledge_tool:
        agent = with_knowledge_search(
            agent=agent,
            knowledge_tags=knowledge_tags,
            knowledge_domain=knowledge_domain
        )

    logger.info(f"Создан универсальный Pydantic AI агент типа: {agent_type}")

    return agent

class AgentRegistry:
    """Реестр агентов для централизованного управления."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.agent_configs: Dict[str, Dict] = {}

    def register_agent(
        self,
        name: str,
        agent: Agent,
        agent_type: str = "unknown",
        knowledge_tags: list = None,
        knowledge_domain: str = None
    ):
        """Зарегистрировать агента в реестре."""
        self.agents[name] = agent
        self.agent_configs[name] = {
            "agent_type": agent_type,
            "knowledge_tags": knowledge_tags or [],
            "knowledge_domain": knowledge_domain
        }

        logger.info(f"Агент {name} зарегистрирован в реестре")

    def get_agent(self, name: str) -> Optional[Agent]:
        """Получить агента по имени."""
        return self.agents.get(name)

    def get_agent_config(self, name: str) -> Optional[Dict]:
        """Получить конфигурацию агента."""
        return self.agent_configs.get(name)

    def list_agents(self) -> list:
        """Получить список всех зарегистрированных агентов."""
        return list(self.agents.keys())

    async def run_agent_with_integrations(
        self,
        agent_name: str,
        user_message: str,
        deps: Any
    ) -> str:
        """Запустить агента с полными интеграциями."""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Агент {agent_name} не найден в реестре")

        config = self.get_agent_config(agent_name)
        agent_type = config.get("agent_type", "unknown")

        # Используем систему интеграций
        return await _integration_system.run_with_integrations(
            agent=agent,
            user_message=user_message,
            deps=deps,
            agent_type=agent_type
        )

# Глобальный реестр агентов
global_agent_registry = AgentRegistry()

# Экспортируемые функции для удобства
def register_agent(name: str, agent: Agent, **kwargs):
    """Быстрая регистрация агента в глобальном реестре."""
    global_agent_registry.register_agent(name, agent, **kwargs)

def get_agent(name: str) -> Optional[Agent]:
    """Быстрое получение агента из глобального реестра."""
    return global_agent_registry.get_agent(name)

async def run_registered_agent(agent_name: str, user_message: str, deps: Any) -> str:
    """Быстрый запуск зарегистрированного агента с интеграциями."""
    return await global_agent_registry.run_agent_with_integrations(
        agent_name=agent_name,
        user_message=user_message,
        deps=deps
    )