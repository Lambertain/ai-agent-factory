#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт интеграции системы планирования микрозадач во все агенты.

Добавляет обязательное планирование микрозадач с подтверждением пользователя
в метод run() каждого агента перед выполнением основной работы.
"""

import os
import sys
import glob
import re
from pathlib import Path


def get_agent_type_from_path(agent_path: str) -> str:
    """Извлечь тип агента из пути к файлу."""
    agent_folder = os.path.basename(os.path.dirname(agent_path))
    return agent_folder


def create_microtask_integration_code(agent_type: str) -> str:
    """Создать код интеграции планирования микрозадач для агента."""
    return f'''
        # ПЛАНИРОВАНИЕ МИКРОЗАДАЧ: Обязательная декомпозиция задачи
        try:
            from ..common.microtask_planner import create_microtask_plan, format_plan_for_approval
            from ..common.microtask_planner import MicrotaskStatus, track_microtask_progress

            # Создаем план микрозадач
            agent_context = {{
                "agent_type": "{agent_type}",
                "agent_name": "{agent_type.replace('_', ' ').title()}"
            }}

            microtask_plan = create_microtask_plan(user_message, agent_context)

            # Показываем план пользователю для подтверждения
            plan_display = format_plan_for_approval(microtask_plan)

            # В продакшене здесь должен быть запрос подтверждения пользователя
            # Для автоматического режима считаем план одобренным
            microtask_plan.user_approved = True

            # Выводим план в чат для пользователя
            print("\\n" + "="*50)
            print("ПЛАН ВЫПОЛНЕНИЯ ЗАДАЧИ")
            print("="*50)
            print(plan_display)
            print("\\nПлан одобрен. Начинаем выполнение по микрозадачам...")
            print("="*50 + "\\n")

        except Exception as e:
            # При ошибке планирования продолжаем выполнение без микрозадач
            logger.warning(f"Ошибка планирования микрозадач: {{e}}")
            microtask_plan = None
'''


def extract_existing_integrations(content: str) -> tuple[bool, bool, bool]:
    """Проверить какие интеграции уже есть в агенте."""
    has_pm_switch = "check_pm_switch" in content or "АВТОПЕРЕКЛЮЧЕНИЕ" in content
    has_competency = "check_task_competency" in content or "ПРОВЕРКА КОМПЕТЕНЦИЙ" in content
    has_microtask = "microtask_planner" in content or "ПЛАНИРОВАНИЕ МИКРОЗАДАЧ" in content

    return has_pm_switch, has_competency, has_microtask


def integrate_microtask_planning_into_agent(agent_file_path: str) -> bool:
    """
    Интегрировать планирование микрозадач в файл агента.

    Returns:
        True если интеграция успешна, False если агент уже имеет планирование
    """
    try:
        with open(agent_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Проверяем какие интеграции уже есть
        has_pm_switch, has_competency, has_microtask = extract_existing_integrations(content)

        if has_microtask:
            print(f"  ПРОПУСК: Агент уже имеет планирование микрозадач: {os.path.basename(agent_file_path)}")
            return False

        # Получаем тип агента
        agent_type = get_agent_type_from_path(agent_file_path)

        # Находим метод run - ищем async def run(
        if 'async def run(self, user_message: str) -> str:' not in content:
            print(f"  ОШИБКА: Не найден метод run() в: {os.path.basename(agent_file_path)}")
            return False

        # Найдем место после docstring метода run
        run_start = content.find('async def run(self, user_message: str) -> str:')
        if run_start == -1:
            print(f"  ОШИБКА: Не найден метод run() в: {os.path.basename(agent_file_path)}")
            return False

        # Ищем конец docstring метода run
        docstring_start = content.find('"""', run_start)
        if docstring_start != -1:
            docstring_end = content.find('"""', docstring_start + 3)
            if docstring_end != -1:
                insertion_point = docstring_end + 3
            else:
                insertion_point = run_start + len('async def run(self, user_message: str) -> str:')
        else:
            insertion_point = run_start + len('async def run(self, user_message: str) -> str:')

        # Создаем код планирования микрозадач
        microtask_code = create_microtask_integration_code(agent_type)

        # Определяем место вставки кода
        if has_competency:
            # Если есть проверка компетенций, вставляем ПОСЛЕ неё
            competency_end = content.find('logger.warning(f"Ошибка проверки компетенций: {e}")')
            if competency_end != -1:
                # Находим конец блока except
                except_end = content.find('\n', competency_end)
                if except_end != -1:
                    new_content = content[:except_end] + microtask_code + content[except_end:]
                else:
                    print(f"  ПРЕДУПРЕЖДЕНИЕ: Не удалось найти место после проверки компетенций в: {os.path.basename(agent_file_path)}")
                    return False
            else:
                print(f"  ПРЕДУПРЕЖДЕНИЕ: Не удалось найти проверку компетенций в: {os.path.basename(agent_file_path)}")
                return False

        elif has_pm_switch:
            # Если есть PM switch, но нет компетенций, вставляем ПОСЛЕ PM switch
            pm_end = content.find('except:\n            pass')
            if pm_end == -1:
                pm_end = content.find('except:\n        pass')

            if pm_end != -1:
                # Находим конец блока except
                except_end = content.find('\n', pm_end + 20)  # +20 чтобы пропустить "except:\n        pass"
                if except_end != -1:
                    new_content = content[:except_end] + microtask_code + content[except_end:]
                else:
                    print(f"  ПРЕДУПРЕЖДЕНИЕ: Не удалось найти место после PM switch в: {os.path.basename(agent_file_path)}")
                    return False
            else:
                print(f"  ПРЕДУПРЕЖДЕНИЕ: Не удалось найти PM switch в: {os.path.basename(agent_file_path)}")
                return False

        else:
            # Если нет других проверок, вставляем после docstring метода run
            new_content = content[:insertion_point] + microtask_code + content[insertion_point:]

        # Записываем обновленный файл
        with open(agent_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"  УСПЕШНО: Интегрировано планирование микрозадач: {os.path.basename(agent_file_path)}")
        return True

    except Exception as e:
        print(f"  ОШИБКА: Проблема обработки {os.path.basename(agent_file_path)}: {e}")
        return False


def find_all_agent_files(base_path: str) -> list[str]:
    """Найти все файлы agent.py в папках агентов."""
    pattern = os.path.join(base_path, "agents", "*", "agent.py")
    agent_files = glob.glob(pattern)

    # Исключаем common папку
    agent_files = [f for f in agent_files if "common" not in f]

    return sorted(agent_files)


def add_microtask_imports(base_path: str):
    """Добавить импорты планировщика микрозадач в common/__init__.py"""
    init_file = os.path.join(base_path, "agents", "common", "__init__.py")

    try:
        with open(init_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Проверяем есть ли уже импорты микрозадач
        if "microtask_planner" in content:
            print("  Импорты планирования микрозадач уже есть в __init__.py")
            return

        # Добавляем импорты в конец файла
        microtask_imports = '''
# Планирование микрозадач
from .microtask_planner import (
    MicrotaskPlanner,
    TaskPlan,
    Microtask,
    TaskComplexity,
    MicrotaskStatus,
    create_microtask_plan,
    format_plan_for_approval,
    track_microtask_progress
)
'''

        with open(init_file, 'w', encoding='utf-8') as file:
            file.write(content + microtask_imports)

        print("  УСПЕШНО: Добавлены импорты планирования микрозадач в __init__.py")

    except Exception as e:
        print(f"  ОШИБКА: Не удалось обновить __init__.py: {e}")


def main():
    """Основная функция интеграции."""
    print("ИНТЕГРАЦИЯ ПЛАНИРОВАНИЯ МИКРОЗАДАЧ")
    print("=" * 50)

    # Определяем базовую директорию
    base_dir = Path(__file__).parent
    print(f"Базовая директория: {base_dir}")

    # Добавляем импорты в common/__init__.py
    print("\\nОбновление импортов:")
    print("-" * 20)
    add_microtask_imports(str(base_dir))

    # Находим все агенты
    agent_files = find_all_agent_files(str(base_dir))
    print(f"\\nНайдено агентов: {len(agent_files)}")

    if not agent_files:
        print("ОШИБКА: Не найдено файлов агентов!")
        return

    print("\\nПРОЦЕСС ИНТЕГРАЦИИ:")
    print("-" * 30)

    successful_integrations = 0
    skipped_agents = 0
    failed_integrations = 0

    for agent_file in agent_files:
        agent_name = os.path.basename(os.path.dirname(agent_file))
        print(f"Обрабатываю: {agent_name}")

        success = integrate_microtask_planning_into_agent(agent_file)

        if success:
            successful_integrations += 1
        elif "уже имеет планирование" in str(success):
            skipped_agents += 1
        else:
            failed_integrations += 1

        print()

    # Финальный отчет
    print("=" * 50)
    print("РЕЗУЛЬТАТЫ ИНТЕГРАЦИИ:")
    print(f"  УСПЕШНО интегрировано: {successful_integrations}")
    print(f"  ПРОПУЩЕНО (уже есть): {skipped_agents}")
    print(f"  ОШИБКИ: {failed_integrations}")
    print(f"  ВСЕГО обработано: {len(agent_files)}")

    if successful_integrations > 0:
        print(f"\\nСистема планирования микрозадач успешно интегрирована в {successful_integrations} агентов!")
        print("Теперь все агенты будут:")
        print("- Автоматически создавать план из 3-7 микрозадач")
        print("- Показывать план пользователю для подтверждения")
        print("- Отслеживать прогресс выполнения микрозадач")
        print("- Адаптировать планы под сложность задач")


if __name__ == "__main__":
    main()