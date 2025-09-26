#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт интеграции системы проверки компетенций во все агенты.

Добавляет проверку компетенций и автоматическое делегирование задач
в метод run() каждого агента.
"""

import os
import sys
import glob
import re
from pathlib import Path


def get_agent_type_from_path(agent_path: str) -> str:
    """Извлечь тип агента из пути к файлу."""
    # Извлекаем имя папки агента
    agent_folder = os.path.basename(os.path.dirname(agent_path))
    return agent_folder


def create_competency_check_code(agent_type: str) -> str:
    """Создать код проверки компетенций для агента."""
    return f'''
        # ПРОВЕРКА КОМПЕТЕНЦИЙ: Анализируем задачу перед выполнением
        try:
            from ..common import check_task_competency, should_delegate_task

            # Проверяем компетенцию для выполнения задачи
            should_delegate, suggested_agent, reason = should_delegate_task(
                user_message, "{agent_type}", threshold=0.7
            )

            if should_delegate and suggested_agent:
                # Делегируем задачу соответствующему агенту через Archon
                delegation_message = f"""
🤝 ДЕЛЕГИРОВАНИЕ ЗАДАЧИ

Причина: {{reason}}

Рекомендованный агент: {{suggested_agent}}

Исходная задача: {{user_message}}

Для выполнения этой задачи рекомендуется обратиться к агенту {{suggested_agent}},
который лучше подходит для данного типа работы.

Если это срочно, создайте задачу в Archon:
- Проект: AI Agent Factory (c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
- Assignee: {{suggested_agent}}
- Описание: {{user_message}}
"""
                return delegation_message
        except Exception as e:
            # При ошибке проверки компетенций продолжаем выполнение
            logger.warning(f"Ошибка проверки компетенций: {{e}}")
'''


def extract_existing_checks(content: str) -> tuple[bool, bool]:
    """Проверить какие проверки уже есть в агенте."""
    has_pm_switch = "check_pm_switch" in content or "АВТОПЕРЕКЛЮЧЕНИЕ" in content
    has_competency = "check_task_competency" in content or "ПРОВЕРКА КОМПЕТЕНЦИЙ" in content

    return has_pm_switch, has_competency


def integrate_competency_check_into_agent(agent_file_path: str) -> bool:
    """
    Интегрировать проверку компетенций в файл агента.

    Returns:
        True если интеграция успешна, False если агент уже имеет проверку
    """
    try:
        with open(agent_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Проверяем какие проверки уже есть
        has_pm_switch, has_competency = extract_existing_checks(content)

        if has_competency:
            print(f"  ⚠️  Агент уже имеет проверку компетенций: {os.path.basename(agent_file_path)}")
            return False

        # Получаем тип агента
        agent_type = get_agent_type_from_path(agent_file_path)

        # Находим метод run
        run_method_pattern = r'(async def run\(self, user_message: str\) -> str:\s*"""[^"]*"""\s*)'
        run_match = re.search(run_method_pattern, content, re.DOTALL)

        if not run_match:
            print(f"  ❌ Не найден метод run() в: {os.path.basename(agent_file_path)}")
            return False

        # Создаем код проверки компетенций
        competency_code = create_competency_check_code(agent_type)

        # Вставляем проверку компетенций
        if has_pm_switch:
            # Если есть PM switch, вставляем ПОСЛЕ него
            pm_pattern = r'(# АВТОПЕРЕКЛЮЧЕНИЕ:.*?except:\s*pass\s*)'
            pm_match = re.search(pm_pattern, content, re.DOTALL)
            if pm_match:
                # Вставляем после PM проверки
                new_content = content.replace(
                    pm_match.group(1),
                    pm_match.group(1) + competency_code
                )
            else:
                # Если паттерн не найден, ищем альтернативный
                alt_pattern = r'(pm_switch_result = await check_pm_switch.*?\n)'
                alt_match = re.search(alt_pattern, content, re.DOTALL)
                if alt_match:
                    new_content = content.replace(
                        alt_match.group(1),
                        alt_match.group(1) + competency_code
                    )
                else:
                    print(f"  ⚠️  Не удалось найти место для вставки в: {os.path.basename(agent_file_path)}")
                    return False
        else:
            # Если нет PM switch, вставляем в начало метода run
            new_content = content.replace(
                run_match.group(1),
                run_match.group(1) + competency_code
            )

        # Записываем обновленный файл
        with open(agent_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"  ✅ Интегрирована проверка компетенций: {os.path.basename(agent_file_path)}")
        return True

    except Exception as e:
        print(f"  ❌ Ошибка обработки {os.path.basename(agent_file_path)}: {e}")
        return False


def find_all_agent_files(base_path: str) -> list[str]:
    """Найти все файлы agent.py в папках агентов."""
    pattern = os.path.join(base_path, "agents", "*", "agent.py")
    agent_files = glob.glob(pattern)

    # Исключаем common папку
    agent_files = [f for f in agent_files if "common" not in f]

    return sorted(agent_files)


def main():
    """Основная функция интеграции."""
    print("🔍 ИНТЕГРАЦИЯ СИСТЕМЫ ПРОВЕРКИ КОМПЕТЕНЦИЙ")
    print("=" * 50)

    # Определяем базовую директорию
    base_dir = Path(__file__).parent
    print(f"Базовая директория: {base_dir}")

    # Находим все агенты
    agent_files = find_all_agent_files(str(base_dir))
    print(f"Найдено агентов: {len(agent_files)}")

    if not agent_files:
        print("❌ Не найдено файлов агентов!")
        return

    print("\n🛠️  ПРОЦЕСС ИНТЕГРАЦИИ:")
    print("-" * 30)

    successful_integrations = 0
    skipped_agents = 0
    failed_integrations = 0

    for agent_file in agent_files:
        agent_name = os.path.basename(os.path.dirname(agent_file))
        print(f"📁 Обрабатываю: {agent_name}")

        success = integrate_competency_check_into_agent(agent_file)

        if success:
            successful_integrations += 1
        elif "уже имеет проверку" in str(success):
            skipped_agents += 1
        else:
            failed_integrations += 1

        print()

    # Финальный отчет
    print("=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ИНТЕГРАЦИИ:")
    print(f"  ✅ Успешно интегрировано: {successful_integrations}")
    print(f"  ⚠️  Пропущено (уже есть): {skipped_agents}")
    print(f"  ❌ Ошибки: {failed_integrations}")
    print(f"  📈 Всего обработано: {len(agent_files)}")

    if successful_integrations > 0:
        print(f"\n🎉 Система проверки компетенций успешно интегрирована в {successful_integrations} агентов!")
        print("Теперь все агенты будут:")
        print("- Проверять свои компетенции перед выполнением задач")
        print("- Автоматически делегировать задачи соответствующим специалистам")
        print("- Рекомендовать создание задач в Archon для правильных агентов")


if __name__ == "__main__":
    main()