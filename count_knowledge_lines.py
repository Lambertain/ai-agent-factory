#!/usr/bin/env python3
"""Подсчет строк в файлах knowledge.md всех агентов."""

import os
from pathlib import Path

agents_dir = Path(r"D:\Automation\agent-factory\use-cases\agent-factory-with-subagents\agents")

# Найти все файлы knowledge.md
knowledge_files = list(agents_dir.rglob("*_knowledge.md"))

# Подсчитать строки и сгруппировать по агентам
agents_data = {}

for file_path in knowledge_files:
    # Получить имя агента из пути
    agent_name = file_path.parent.parent.name

    # Подсчитать строки
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = len(f.readlines())

    # Сохранить только самый большой файл для каждого агента (на случай дубликатов)
    if agent_name not in agents_data or lines > agents_data[agent_name]['lines']:
        agents_data[agent_name] = {
            'lines': lines,
            'file': file_path.name
        }

# Отсортировать по количеству строк (по убыванию)
sorted_agents = sorted(agents_data.items(), key=lambda x: x[1]['lines'], reverse=True)

print("=" * 80)
print("АНАЛИЗ РАЗМЕРОВ ФАЙЛОВ KNOWLEDGE.MD")
print("=" * 80)
print(f"\nВсего агентов: {len(sorted_agents)}")
print("\nАгенты отсортированы по размеру (от большего к меньшему):\n")

# Группы по размеру
group_1 = []  # >1000 строк - критично требуют модуляризации
group_2 = []  # 800-1000 строк - требуют модуляризации
group_3 = []  # 600-800 строк - граница, рекомендуется модуляризация
group_4 = []  # <600 строк - модуляризация не требуется

for agent_name, data in sorted_agents:
    lines = data['lines']

    if lines > 1000:
        group_1.append((agent_name, lines))
    elif lines >= 800:
        group_2.append((agent_name, lines))
    elif lines >= 600:
        group_3.append((agent_name, lines))
    else:
        group_4.append((agent_name, lines))

    # Статус модуляризации
    if lines > 1000:
        status = "[КРИТИЧНО - МОДУЛЯРИЗАЦИЯ ОБЯЗАТЕЛЬНА]"
    elif lines >= 800:
        status = "[ТРЕБУЕТ МОДУЛЯРИЗАЦИИ]"
    elif lines >= 600:
        status = "[РЕКОМЕНДУЕТСЯ МОДУЛЯРИЗАЦИЯ]"
    else:
        status = "[OK - модуляризация не требуется]"

    print(f"{agent_name:45} {lines:5} строк  {status}")

print("\n" + "=" * 80)
print("СТАТИСТИКА ПО ГРУППАМ")
print("=" * 80)

print(f"\nГруппа 1 (>1000 строк, КРИТИЧНО): {len(group_1)} агентов")
for agent_name, lines in group_1:
    print(f"  - {agent_name}: {lines} строк")

print(f"\nГруппа 2 (800-1000 строк, требует модуляризации): {len(group_2)} агентов")
for agent_name, lines in group_2:
    print(f"  - {agent_name}: {lines} строк")

print(f"\nГруппа 3 (600-800 строк, рекомендуется): {len(group_3)} агентов")
for agent_name, lines in group_3:
    print(f"  - {agent_name}: {lines} строк")

print(f"\nГруппа 4 (<600 строк, OK): {len(group_4)} агентов")

print("\n" + "=" * 80)
print("ИТОГО")
print("=" * 80)
print(f"Требуют модуляризации (группы 1-3): {len(group_1) + len(group_2) + len(group_3)} агентов")
print(f"Не требуют модуляризации (группа 4): {len(group_4)} агентов")
print("=" * 80)
