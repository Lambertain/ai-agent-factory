#!/usr/bin/env python3
"""
Шаблон интеграции автопереключения на Project Manager для всех агентов.

Этот код должен быть добавлен в метод run() каждого агента.
"""

# ДОБАВИТЬ В ИМПОРТЫ:
# from ..common import check_pm_switch

# ЗАМЕНИТЬ МЕТОД run() НА ЭТОТ ШАБЛОН:

async def run(self, user_message: str) -> str:
    """
    Основной метод для обработки запросов пользователя с автопереключением.

    Args:
        user_message: Сообщение от пользователя

    Returns:
        Ответ агента
    """
    try:
        # АВТОПЕРЕКЛЮЧЕНИЕ: Проверяем команды управления
        try:
            from ..common import check_pm_switch
            pm_switch_result = await check_pm_switch(
                user_message,
                "AGENT_NAME"  # Заменить на имя конкретного агента
            )

            if pm_switch_result:
                # Команда управления обнаружена - переключаемся на PM
                print(pm_switch_result)  # Выводим результат анализа PM
                return "✅ Переключение на Project Manager выполнено. Следуйте рекомендациям выше."

        except ImportError:
            # Если модуль автопереключения недоступен, продолжаем обычную работу
            pass
        except Exception as pm_error:
            # Логируем ошибку, но не прерываем работу агента
            print(f"⚠️ Предупреждение: Ошибка автопереключения: {pm_error}")

        # Стандартная обработка запроса
        result = await self.agent.run(
            user_message,
            deps=self.dependencies
        )
        return result.data

    except Exception as e:
        error_msg = f"Ошибка выполнения запроса: {e}"
        # Логируем если logger доступен
        if hasattr(self, 'logger'):
            self.logger.error(error_msg)
        return f"Произошла ошибка при обработке запроса: {e}"


# ПРИМЕР ИНТЕГРАЦИИ ДЛЯ ANALYTICS TRACKING AGENT:

# 1. Добавить импорт в начало файла (после других импортов):
# from ..common import check_pm_switch

# 2. Заменить метод run() на версию выше, где AGENT_NAME = "Analytics Tracking Agent"

# 3. Аналогично для всех остальных агентов с соответствующими именами


# СПИСОК АГЕНТОВ ДЛЯ ИНТЕГРАЦИИ (32 агента):

AGENT_NAMES = [
    "Analytics Tracking Agent",
    "API Development Agent",
    "Community Management Agent",
    "MCP Configuration Agent",
    "NLP Content Quality Guardian Agent",
    "NLP Content Research Agent",
    "NLP Program Generator Agent",
    "NLP Psychology Test Adapter Agent",
    "Online Support Content Architect Agent",
    "Online Support Content Orchestrator Agent",
    "Online Support Quality Guardian Agent",
    "Online Support Research Agent",
    "Online Support Test Generator Agent",
    "Patternshift Test Generator Agent",
    "Payment Integration Agent",
    "Performance Optimization Agent",
    "Prisma Database Agent",
    "Psychology Content Architect Agent",
    "Psychology Content Orchestrator Agent",
    "PWA Mobile Agent",
    "Queue Worker Agent",
    "RAG Agent",
    "Security Audit Agent",
    "TypeScript Architecture Agent",
    "UI/UX Enhancement Agent",
    "Universal NLP Content Architect Agent",
    "Archon Project Manager",
    "Analysis Lead",
    "Blueprint Architect",
    "Implementation Engineer",
    "Quality Guardian",
    "Deployment Engineer"
]

# АВТОМАТИЗАЦИЯ ИНТЕГРАЦИИ:
# Можно создать скрипт, который автоматически найдет все agent.py файлы
# и добавит код автопереключения в каждый