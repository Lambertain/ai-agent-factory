#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование системы автопереключения на Project Manager.
"""

import asyncio
import sys
import os

# Добавляем путь к модулю common
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

async def test_keyword_detection():
    """Тестирует определение ключевых команд."""
    print("=== ТЕСТ ОПРЕДЕЛЕНИЯ КОМАНД ===")

    try:
        from common.keyword_detector import should_switch_to_pm, get_command_context

        test_commands = [
            "продолжай работу",
            "работай дальше",
            "следующее задание",
            "давай продолжим",
            "приоритизируй задачи",
            "статус проекта",
            "что делать дальше",
            "обычный запрос на аналитику",
            "hello world",
            "создай отчет"
        ]

        for cmd in test_commands:
            should_switch = should_switch_to_pm(cmd)
            context = get_command_context(cmd)

            print(f"Команда: '{cmd}'")
            print(f"  Переключение: {'ДА' if should_switch else 'НЕТ'}")
            print(f"  Действие: {context.get('detected_action', 'не определено')}")
            print(f"  Уверенность: {context.get('confidence', 0):.2f}")
            print()

    except Exception as e:
        print(f"Ошибка тестирования: {e}")

async def test_pm_switch():
    """Тестирует полное автопереключение."""
    print("=== ТЕСТ АВТОПЕРЕКЛЮЧЕНИЯ ===")

    try:
        from common.auto_switch import auto_switch_to_project_manager, format_switch_result

        test_commands = [
            "продолжай проект",
            "дальше работаем",
            "статус задач",
            "обычный вопрос"
        ]

        for cmd in test_commands:
            print(f"Тестируем: '{cmd}'")

            result = await auto_switch_to_project_manager(
                cmd,
                "Test Agent",
                threshold=0.7
            )

            if result.get("switched"):
                formatted = format_switch_result(result)
                print("ПЕРЕКЛЮЧЕНИЕ СРАБОТАЛО:")
                print(formatted)
            else:
                print("Переключение не требуется")

            print("-" * 40)

    except Exception as e:
        print(f"Ошибка тестирования автопереключения: {e}")

async def test_simple_check():
    """Простая проверка функции check_pm_switch."""
    print("=== ТЕСТ ПРОСТОЙ ПРОВЕРКИ ===")

    try:
        from common import check_pm_switch

        result = await check_pm_switch("продолжай работу", "Test Agent")

        if result:
            print("Переключение сработало:")
            print(result)
        else:
            print("Переключение не требуется")

    except Exception as e:
        print(f"Ошибка простой проверки: {e}")

async def main():
    """Основная функция тестирования."""
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ АВТОПЕРЕКЛЮЧЕНИЯ")
    print("=" * 50)

    await test_keyword_detection()
    await test_pm_switch()
    await test_simple_check()

    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    asyncio.run(main())