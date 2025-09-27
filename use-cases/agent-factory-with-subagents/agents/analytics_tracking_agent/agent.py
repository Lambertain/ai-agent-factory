# -*- coding: utf-8 -*-
"""
Универсальный Analytics & Tracking Agent
Специализируется на настройке, оптимизации и анализе систем аналитики для любых проектов
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic_ai import Agent, RunContext
from .dependencies import load_dependencies, AnalyticsTrackingDependencies
from .providers import get_llm_model
from .tools import (
    setup_analytics_tracking,
    create_conversion_funnel,
    analyze_user_behavior,
    search_analytics_knowledge,
    delegate_task_to_agent,
    generate_analytics_report,
    optimize_tracking_performance,
    setup_privacy_compliance,
    create_custom_dashboard,
    validate_tracking_implementation,
    break_down_to_microtasks,
    report_microtask_progress,
    reflect_and_improve,
    check_delegation_need
)
from .prompts import get_system_prompt, get_tool_selection_prompt

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Pydantic AI агента (прямая архитектура)
analytics_agent = Agent(
    get_llm_model(),
    deps_type=AnalyticsTrackingDependencies,
    system_prompt=get_system_prompt()
)

# Регистрируем analytics инструменты
analytics_agent.tool(setup_analytics_tracking)
analytics_agent.tool(create_conversion_funnel)
analytics_agent.tool(analyze_user_behavior)
analytics_agent.tool(search_analytics_knowledge)
analytics_agent.tool(delegate_task_to_agent)
analytics_agent.tool(generate_analytics_report)
analytics_agent.tool(optimize_tracking_performance)
analytics_agent.tool(setup_privacy_compliance)
analytics_agent.tool(create_custom_dashboard)
analytics_agent.tool(validate_tracking_implementation)

# Регистрируем обязательные инструменты коллективной работы
analytics_agent.tool(break_down_to_microtasks)
analytics_agent.tool(report_microtask_progress)
analytics_agent.tool(reflect_and_improve)
analytics_agent.tool(check_delegation_need)

async def run_analytics_audit(
    target_type: str,
    audit_scope: str = "comprehensive",
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Запустить комплексный аудит аналитики для указанной цели.

    Args:
        target_type: Тип аудита (web_analytics, ecommerce_tracking, saas_metrics)
        audit_scope: Область аудита (quick, comprehensive, focused)
        session_id: Опциональный идентификатор сессии

    Returns:
        Результаты аудита аналитики
    """
    start_time = asyncio.get_event_loop().time()

    # Инициализируем зависимости
    deps = load_dependencies()
    deps.project_type = target_type

    try:
        # Запускаем аудит аналитики
        result = await analytics_agent.run(
            f"Выполни {audit_scope} аудит аналитики для проекта типа: {target_type}",
            deps=deps
        )

        # Вычисляем время выполнения
        audit_duration = asyncio.get_event_loop().time() - start_time

        # Обрабатываем и улучшаем результаты
        audit_results = {
            "audit_summary": {
                "target_type": target_type,
                "audit_scope": audit_scope,
                "session_id": session_id,
                "start_time": start_time,
                "duration_seconds": audit_duration,
                "status": "completed"
            },
            "agent_response": result.data,
            "recommendations": _extract_analytics_recommendations(result.data),
            "next_steps": _generate_analytics_next_steps(result.data)
        }

        logger.info(f"Аудит аналитики завершен за {audit_duration:.2f} секунд")
        return audit_results

    except Exception as e:
        logger.error(f"Ошибка выполнения аудита аналитики: {e}")
        return {
            "error": str(e),
            "audit_summary": {
                "target_type": target_type,
                "status": "failed"
            }
        }

def _extract_analytics_recommendations(response: str) -> List[str]:
    """Извлечь рекомендации из ответа агента."""
    recommendations = []
    lines = response.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith(('Рекомендация:', 'Recommendation:', '✅', '💡')):
            recommendations.append(line)

    return recommendations

def _generate_analytics_next_steps(response: str) -> List[str]:
    """Сгенерировать следующие шаги на основе ответа."""
    next_steps = []

    if "Google Analytics" in response:
        next_steps.append("Настройка Google Analytics 4")
    if "конверсия" in response.lower():
        next_steps.append("Создание воронки конверсии")
    if "отслеживание" in response.lower():
        next_steps.append("Реализация пользовательского трекинга")

    return next_steps

async def run_analytics_task(user_message: str, target_type: str = "web_analytics") -> str:
    """
    Выполнить задачу аналитики с автоматическими интеграциями.

    Args:
        user_message: Сообщение от пользователя
        target_type: Тип проекта аналитики

    Returns:
        Ответ агента
    """
    # Инициализируем зависимости
    deps = load_dependencies()
    deps.project_type = target_type

    try:
        # Используем новую систему интеграций
        from ..common.pydantic_ai_integrations import run_with_integrations

        result = await run_with_integrations(
            agent=analytics_agent,
            user_message=user_message,
            deps=deps,
            agent_type="analytics_tracking_agent"
        )
        return result

    except Exception as e:
        logger.error(f"Ошибка выполнения запроса аналитики: {e}")
        return f"Произошла ошибка при обработке запроса аналитики: {e}"

def get_available_providers() -> List[str]:
    """Получить список доступных analytics провайдеров."""
    deps = load_dependencies()
    return deps.analytics_providers

def get_project_info() -> Dict[str, Any]:
    """Получить информацию о текущем проекте."""
    deps = load_dependencies()
    return {
        "project_type": deps.project_type,
        "domain_type": deps.domain_type,
        "tracking_focus": deps.tracking_focus,
        "analytics_providers": deps.analytics_providers,
        "primary_provider": deps.primary_provider,
        "key_metrics": deps.get_key_metrics(),
        "recommended_events": deps.get_recommended_events(),
        "privacy_compliant": {
            "gdpr": deps.gdpr_enabled,
            "ccpa": deps.ccpa_enabled
        }
    }


# CLI интерфейс (опциональный)
async def main():
    """Основная функция для запуска агента из командной строки."""
    import argparse

    parser = argparse.ArgumentParser(description="Universal Analytics & Tracking Agent")
    parser.add_argument("--project-type", default="web_analytics",
                       help="Тип проекта (web_analytics, ecommerce_tracking, saas_metrics, blog_analytics)")
    parser.add_argument("--message", help="Сообщение для агента")
    parser.add_argument("--interactive", action="store_true",
                       help="Запустить в интерактивном режиме")

    args = parser.parse_args()

    print(f"🎯 Analytics Agent запущен для проекта типа: {args.project_type}")
    print(f"📊 Доступные провайдеры: {', '.join(get_available_providers())}")
    print("-" * 50)

    if args.message:
        # Одноразовый режим
        response = await run_analytics_task(args.message, args.project_type)
        print(f"Ответ: {response}")

    elif args.interactive:
        # Интерактивный режим
        print("Введите 'exit' для выхода")

        while True:
            try:
                user_input = input("\n👤 Вы: ")

                if user_input.lower() in ['exit', 'quit', 'выход']:
                    break

                if user_input.strip():
                    response = await run_analytics_task(user_input, args.project_type)
                    print(f"🤖 Агент: {response}")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    else:
        # Показываем информацию о проекте
        project_info = get_project_info()
        print("📋 Информация о проекте:")
        for key, value in project_info.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())