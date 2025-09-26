# -*- coding: utf-8 -*-
"""
Упрощенный скрипт интеграции автопереключения.
"""

import os
import re
from pathlib import Path

def find_agent_files():
    """Найти все файлы agent.py."""
    agents_dir = Path("agents")
    agent_files = []

    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "common":
            agent_file = agent_dir / "agent.py"
            if agent_file.exists():
                agent_name = agent_dir.name.replace('_', ' ').title() + " Agent"
                agent_files.append((str(agent_file), agent_name))

    return agent_files

def has_auto_switch(content):
    """Проверить наличие автопереключения."""
    return "check_pm_switch" in content or "АВТОПЕРЕКЛЮЧЕНИЕ" in content

def add_import(content):
    """Добавить импорт."""
    if "from ..common import" in content:
        return content

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('from .') and 'import' in line:
            lines.insert(i + 1, "from ..common import check_pm_switch")
            break

    return '\n'.join(lines)

def main():
    """Основная функция."""
    print("Начинаем интеграцию автопереключения...")

    agent_files = find_agent_files()
    print(f"Найдено {len(agent_files)} агентов")

    success = 0

    for file_path, agent_name in agent_files:
        try:
            print(f"Обрабатываем: {agent_name}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if has_auto_switch(content):
                print(f"  Уже интегрировано: {agent_name}")
                success += 1
                continue

            # Создаем backup
            backup_path = file_path + ".backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Добавляем импорт
            content = add_import(content)

            # Простое добавление проверки в метод run
            run_pattern = r'(async def run\([^)]*\).*?:.*?""".*?""")'
            if re.search(run_pattern, content, re.DOTALL):
                check_code = '''
        # АВТОПЕРЕКЛЮЧЕНИЕ: Проверяем команды управления
        try:
            from ..common import check_pm_switch
            pm_switch_result = await check_pm_switch(user_message, "AGENT_NAME")
            if pm_switch_result:
                return pm_switch_result
        except:
            pass

        '''
                check_code = check_code.replace("AGENT_NAME", agent_name)

                # Вставляем код после docstring метода run
                content = re.sub(
                    r'(async def run\([^)]*\).*?:.*?""".*?""")\s*\n',
                    r'\1\n' + check_code,
                    content,
                    flags=re.DOTALL
                )

            # Записываем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  Интегрировано: {agent_name}")
            success += 1

        except Exception as e:
            print(f"  Ошибка: {agent_name} - {e}")

    print(f"Готово! Интегрировано: {success} агентов")

if __name__ == "__main__":
    main()