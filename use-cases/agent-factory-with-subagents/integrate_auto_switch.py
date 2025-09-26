#!/usr/bin/env python3
"""
Скрипт автоматической интеграции системы автопереключения во все агенты.

Добавляет функциональность автопереключения на Project Manager во все agent.py файлы.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def find_agent_files() -> List[Tuple[str, str]]:
    """
    Найти все файлы agent.py в директории агентов.

    Returns:
        Список кортежей (путь_к_файлу, имя_агента)
    """
    agents_dir = Path("D:/Automation/agent-factory/use-cases/agent-factory-with-subagents/agents")
    agent_files = []

    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "common":
            agent_file = agent_dir / "agent.py"
            if agent_file.exists():
                # Извлекаем имя агента из названия папки
                agent_name = agent_dir.name.replace('_', ' ').title() + " Agent"
                agent_files.append((str(agent_file), agent_name))

    return agent_files


def extract_agent_name_from_file(file_path: str) -> str:
    """
    Извлечь имя агента из содержимого файла.

    Args:
        file_path: Путь к файлу агента

    Returns:
        Имя агента или имя по умолчанию
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Ищем в docstring или комментариях
        patterns = [
            r'"""[\s\S]*?([A-Z][^"\n]*Agent)[\s\S]*?"""',
            r"'''[\s\S]*?([A-Z][^'\n]*Agent)[\s\S]*?'''",
            r'# ([A-Z][^\n]*Agent)',
            r'class\s+([A-Z][^\s\(]*Agent)',
            r'def\s+create_([a-z_]+)_agent'
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                agent_name = match.group(1)
                if "agent" in agent_name.lower():
                    return agent_name
                else:
                    return agent_name.replace('_', ' ').title() + " Agent"

        # Если не нашли, используем имя папки
        folder_name = Path(file_path).parent.name
        return folder_name.replace('_', ' ').title() + " Agent"

    except Exception as e:
        print(f"Ошибка извлечения имени агента из {file_path}: {e}")
        folder_name = Path(file_path).parent.name
        return folder_name.replace('_', ' ').title() + " Agent"


def has_auto_switch_integration(file_content: str) -> bool:
    """
    Проверить, уже ли интегрировано автопереключение.

    Args:
        file_content: Содержимое файла

    Returns:
        True если интеграция уже есть
    """
    indicators = [
        "check_pm_switch",
        "АВТОПЕРЕКЛЮЧЕНИЕ",
        "from ..common import",
        "pm_switch_result"
    ]

    return any(indicator in file_content for indicator in indicators)


def backup_file(file_path: str) -> str:
    """
    Создать резервную копию файла.

    Args:
        file_path: Путь к файлу

    Returns:
        Путь к backup файлу
    """
    backup_path = file_path + ".backup"

    try:
        with open(file_path, 'r', encoding='utf-8') as original:
            content = original.read()

        with open(backup_path, 'w', encoding='utf-8') as backup:
            backup.write(content)

        return backup_path
    except Exception as e:
        print(f"Ошибка создания backup для {file_path}: {e}")
        return ""


def add_import_statement(content: str) -> str:
    """
    Добавить импорт check_pm_switch если его нет.

    Args:
        content: Содержимое файла

    Returns:
        Обновленное содержимое
    """
    # Проверяем, есть ли уже импорт
    if "from ..common import" in content or "check_pm_switch" in content:
        return content

    # Ищем место для вставки импорта
    lines = content.split('\n')
    insert_index = -1

    # Ищем последний импорт из локальных модулей
    for i, line in enumerate(lines):
        if line.strip().startswith('from .') and 'import' in line:
            insert_index = i + 1
        elif line.strip().startswith('from pydantic_ai') and 'import' in line:
            insert_index = i + 1

    if insert_index == -1:
        # Ищем любые импорты
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                insert_index = i + 1

    if insert_index != -1:
        lines.insert(insert_index, "from ..common import check_pm_switch")
        return '\n'.join(lines)

    return content


def modify_run_method(content: str, agent_name: str) -> str:
    """
    Модифицировать метод run для добавления автопереключения.

    Args:
        content: Содержимое файла
        agent_name: Имя агента

    Returns:
        Обновленное содержимое
    """
    # Паттерн для поиска метода run
    run_method_pattern = r'(async\s+def\s+run\s*\([^)]*\)\s*->\s*str\s*:\s*"""[^"]*""")'

    # Новый код автопереключения
    auto_switch_code = f'''        try:
            # АВТОПЕРЕКЛЮЧЕНИЕ: Проверяем команды управления
            try:
                from ..common import check_pm_switch
                pm_switch_result = await check_pm_switch(
                    user_message,
                    "{agent_name}"
                )

                if pm_switch_result:
                    # Команда управления обнаружена - переключаемся на PM
                    print(pm_switch_result)
                    return "✅ Переключение на Project Manager выполнено. Следуйте рекомендациям выше."

            except ImportError:
                # Если модуль автопереключения недоступен, продолжаем обычную работу
                pass
            except Exception as pm_error:
                # Логируем ошибку, но не прерываем работу агента
                if hasattr(self, 'logger'):
                    self.logger.warning(f"Ошибка автопереключения: {{pm_error}}")

            # Стандартная обработка запроса'''

    # Ищем метод run и заменяем его содержимое
    def replace_run_method(match):
        method_signature = match.group(1)

        # Создаем новый метод с автопереключением
        new_method = f"""{method_signature}
{auto_switch_code}
            result = await self.agent.run(
                user_message,
                deps=self.dependencies
            )
            return result.data

        except Exception as e:
            error_msg = f"Ошибка выполнения запроса: {{e}}"
            if hasattr(self, 'logger'):
                self.logger.error(error_msg)
            return f"Произошла ошибка при обработке запроса: {{e}}\""""

        return new_method

    # Применяем замену
    modified_content = re.sub(run_method_pattern, replace_run_method, content, flags=re.DOTALL)

    # Если метод run не найден стандартным способом, попробуем другой подход
    if modified_content == content:
        # Ищем более простую сигнатуру
        simple_pattern = r'(def\s+run\s*\([^)]*\):.*?)(\n    def|\nclass|\n\n|\Z)'

        def replace_simple_run(match):
            method_content = match.group(1)
            next_part = match.group(2)

            if "АВТОПЕРЕКЛЮЧЕНИЕ" not in method_content:
                # Добавляем автопереключение в начало метода
                lines = method_content.split('\n')
                if len(lines) > 2:
                    # Вставляем код после docstring
                    docstring_end = -1
                    for i, line in enumerate(lines):
                        if '"""' in line and i > 0:
                            docstring_end = i
                            break

                    if docstring_end != -1:
                        insert_lines = auto_switch_code.split('\n')
                        for j, insert_line in enumerate(insert_lines):
                            lines.insert(docstring_end + 1 + j, insert_line)

                        return '\n'.join(lines) + next_part

            return method_content + next_part

        modified_content = re.sub(simple_pattern, replace_simple_run, content, flags=re.DOTALL)

    return modified_content


def integrate_agent(file_path: str, agent_name: str) -> bool:
    """
    Интегрировать автопереключение в конкретный агент.

    Args:
        file_path: Путь к файлу агента
        agent_name: Имя агента

    Returns:
        True если интеграция успешна
    """
    try:
        # Читаем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Проверяем, нужна ли интеграция
        if has_auto_switch_integration(content):
            print(f"✅ {agent_name}: автопереключение уже интегрировано")
            return True

        # Создаем backup
        backup_path = backup_file(file_path)
        if not backup_path:
            print(f"❌ {agent_name}: не удалось создать backup")
            return False

        print(f"📁 {agent_name}: backup создан -> {backup_path}")

        # Добавляем импорт
        content = add_import_statement(content)

        # Модифицируем метод run
        content = modify_run_method(content, agent_name)

        # Записываем обновленный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {agent_name}: автопереключение интегрировано")
        return True

    except Exception as e:
        print(f"❌ {agent_name}: ошибка интеграции - {e}")
        return False


def main():
    """Основная функция скрипта."""
    print("🔄 Начинаем интеграцию автопереключения во все агенты...")
    print("-" * 60)

    # Находим все агенты
    agent_files = find_agent_files()
    print(f"📋 Найдено {len(agent_files)} агентов")

    successful_integrations = 0
    failed_integrations = 0

    # Интегрируем каждого агента
    for file_path, default_agent_name in agent_files:
        # Извлекаем точное имя агента из файла
        agent_name = extract_agent_name_from_file(file_path)

        print(f"\n🔧 Обрабатываем: {agent_name}")
        print(f"   Файл: {file_path}")

        if integrate_agent(file_path, agent_name):
            successful_integrations += 1
        else:
            failed_integrations += 1

    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ:")
    print(f"✅ Успешно интегрировано: {successful_integrations}")
    print(f"❌ Ошибок интеграции: {failed_integrations}")
    print(f"📁 Всего агентов: {len(agent_files)}")

    if failed_integrations == 0:
        print("\n🎉 ВСЕ АГЕНТЫ УСПЕШНО ИНТЕГРИРОВАНЫ!")
        print("Теперь все агенты поддерживают автопереключение на Project Manager")
    else:
        print(f"\n⚠️ Есть проблемы с {failed_integrations} агентами")
        print("Проверьте логи выше для деталей")

    print("\n📝 Следующие шаги:")
    print("1. Протестируйте автопереключение с командами: 'продолжай', 'работай', 'дальше'")
    print("2. Обновите статус задачи в Archon")
    print("3. Проверьте работу всех агентов")


if __name__ == "__main__":
    main()