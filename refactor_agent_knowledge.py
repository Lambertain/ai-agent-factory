#!/usr/bin/env python3
"""
ИСПРАВЛЕННЫЙ Script для рефакторинга agent knowledge файлов V3.

Преобразует монолитные knowledge файлы в модульную структуру:
- Удаляет дублирующиеся общие правила (~130 строк)
- Чётко разделяет системный промпт и доменные знания
- Создаёт backup оригинала
- Валидирует результаты перед записью
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional


# Ключевые паттерны для идентификации секций
COMMON_RULES_MARKERS = [
    "КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ",
    "КРИТИЧЕСКИ ВАЖНО: ЗАПРЕТ ТОКЕН-ЭКОНОМИИ",
    "ОБОВ'ЯЗКОВІ ФІНАЛЬНІ ПУНКТИ TodoWrite",
    "ОБОВ'ЯЗКОВЕ ПРАВИЛО: НЕГАЙНЕ СТВОРЕННЯ ЗАДАЧІ",
    "критическое правило - никогда не работать как claude code"
]

SYSTEM_PROMPT_MARKERS = [
    "Системный промпт",
    "системный промпт роли",
    "экспертиза охватывает",
    "Ты специализированный AI-агент"
]

# Маркеры НАЧАЛА доменных знаний (где ЗАКАНЧИВАЕТСЯ системный промпт)
DOMAIN_START_MARKERS = [
    "## Ключевые паттерны",
    "## Специфичные для домена",
    "## Архитектурные принципы",
    "## Доменные знания",
    "## Методологии анализа требований",
    "## Архитектурный анализ",
    "## Декомпозиция задач",
    "## Паттерны анализа",
    "## Принципы проектирования",
    "## Методологии и подходы",
    "## Технические детали",
    "## Реализация",
    "## Практические примеры",
    "## Мультиагентные паттерны работы",
    "## Универсальные Performance Optimization Patterns"
]


def find_agent_knowledge_files(agents_dir: Path, group_filter: str = "all") -> list[Path]:
    """
    Найти все knowledge файлы агентов с фильтрацией по группам.

    Args:
        agents_dir: Путь к директории agents
        group_filter: Фильтр по группам агентов
            - "all": все агенты (по умолчанию)
            - "archon": только Archon агенты (5 шт)
            - "specialized": только специализированные агенты (13 шт)
            - "pattern": только Pattern агенты (18 шт)

    Returns:
        list[Path]: Список путей к knowledge файлам
    """
    # Определить списки агентов по группам
    ARCHON_AGENTS = [
        "archon_analysis_lead",
        "archon_blueprint_architect",
        "archon_implementation_engineer",
        "archon_quality_guardian",
        "deployment_engineer"
    ]

    PATTERN_AGENTS_PREFIX = "pattern_"

    knowledge_files = []

    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        # Пропустить _shared директорию
        if agent_dir.name == "_shared":
            continue

        agent_name = agent_dir.name

        # Применить фильтр по группам
        if group_filter == "archon":
            if agent_name not in ARCHON_AGENTS:
                continue
        elif group_filter == "pattern":
            if not agent_name.startswith(PATTERN_AGENTS_PREFIX):
                continue
        elif group_filter == "specialized":
            # Специализированные = не Archon и не Pattern
            if agent_name in ARCHON_AGENTS or agent_name.startswith(PATTERN_AGENTS_PREFIX):
                continue
        # Для "all" обрабатываем все агенты

        # Найти knowledge файл в knowledge/ поддиректории
        knowledge_dir = agent_dir / "knowledge"
        if knowledge_dir.exists():
            for file in knowledge_dir.iterdir():
                # Пропустить backup файлы
                if file.suffix == ".md" and "knowledge" in file.stem and "backup" not in file.stem:
                    knowledge_files.append(file)

    return sorted(knowledge_files)


def extract_agent_name(file_path: Path) -> str:
    """
    Извлечь название агента из пути файла.

    Args:
        file_path: Путь к knowledge файлу

    Returns:
        str: Название агента
    """
    # Пример: .../payment_integration_agent/knowledge/payment_integration_knowledge.md
    agent_dir_name = file_path.parent.parent.name

    # Конвертировать payment_integration_agent -> Payment Integration Agent
    name = agent_dir_name.replace("_agent", "").replace("_", " ").title()
    return f"{name} Agent"


def count_lines_with_common_rules(content: str) -> int:
    """
    Подсчитать количество строк с общими правилами.

    Args:
        content: Содержимое файла

    Returns:
        int: Количество строк с общими правилами
    """
    lines = content.split('\n')
    common_rules_lines = 0
    in_common_section = False

    for line in lines:
        # Проверить начало секции общих правил
        for marker in COMMON_RULES_MARKERS:
            if marker.lower() in line.lower():
                in_common_section = True
                break

        # Проверить конец секции (начало системного промпта)
        for marker in SYSTEM_PROMPT_MARKERS:
            if marker.lower() in line.lower() and in_common_section:
                in_common_section = False
                break

        if in_common_section:
            common_rules_lines += 1

    return common_rules_lines


def extract_system_prompt(content: str, agent_name: str) -> str:
    """
    Извлечь ТОЛЬКО системный промпт роли (БЕЗ доменных знаний).

    Args:
        content: Содержимое файла
        agent_name: Название агента

    Returns:
        str: Системный промпт БЕЗ доменных знаний
    """
    lines = content.split('\n')
    prompt_lines = []
    in_prompt_section = False

    for line in lines:
        # Начало системного промпта
        if not in_prompt_section:
            for marker in SYSTEM_PROMPT_MARKERS:
                if marker.lower() in line.lower():
                    in_prompt_section = True
                    break

        # Если в секции промпта - проверяем не начались ли доменные знания
        if in_prompt_section:
            # ОСТАНОВИТЬСЯ если начались доменные знания
            is_domain_start = False
            for domain_marker in DOMAIN_START_MARKERS:
                if domain_marker in line:
                    is_domain_start = True
                    break

            if is_domain_start:
                # Доменные знания начались - прекращаем извлечение промпта
                break

            # Добавляем строку в промпт
            prompt_lines.append(line)

    if prompt_lines:
        return '\n'.join(prompt_lines)

    # Если не найден, вернуть заглушку
    return f"""## Системный промпт

Ты специализированный AI-агент {agent_name} с экспертизой в [ОБЛАСТЬ].

### Экспертиза охватывает:
- [Компетенция 1]
- [Компетенция 2]
- [Компетенция 3]
"""


def extract_domain_knowledge(content: str) -> str:
    """
    Извлечь ТОЛЬКО доменные знания (БЕЗ системного промпта и общих правил).

    Args:
        content: Содержимое файла

    Returns:
        str: Доменные знания
    """
    lines = content.split('\n')
    domain_lines = []
    in_domain_section = False

    for line in lines:
        # Проверить начало доменных знаний
        if not in_domain_section:
            for marker in DOMAIN_START_MARKERS:
                if marker in line:
                    in_domain_section = True
                    break

        # Если в секции доменных знаний - добавляем строку
        if in_domain_section:
            # Проверить конец доменных знаний (footer)
            if "**Версия:**" in line or "**Дата рефакторинга:**" in line:
                break

            domain_lines.append(line)

    return '\n'.join(domain_lines) if domain_lines else "[Доменные знания для извлечения из оригинального файла]"


def validate_extracted_content(system_prompt: str, domain_knowledge: str, agent_name: str) -> Tuple[bool, str]:
    """
    Валидировать извлечённый контент перед генерацией.

    Args:
        system_prompt: Системный промпт
        domain_knowledge: Доменные знания
        agent_name: Название агента

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    errors = []

    # Проверка 1: Системный промпт не пустой
    if len(system_prompt.strip()) < 50:
        errors.append("Системный промпт слишком короткий")

    # Проверка 2: Доменные знания не являются placeholder
    if "[Доменные знания для извлечения" in domain_knowledge:
        errors.append("Доменные знания не извлечены (placeholder)")

    # Проверка 3: Нет дубликации секций в системном промпте
    domain_markers_in_prompt = sum(1 for marker in DOMAIN_START_MARKERS if marker in system_prompt)
    if domain_markers_in_prompt > 0:
        errors.append(f"Системный промпт содержит {domain_markers_in_prompt} маркеров доменных знаний (возможна дубликация)")

    # Проверка 4: Доменные знания содержат реальный контент
    if len(domain_knowledge.strip()) < 100:
        errors.append("Доменные знания слишком короткие")

    # Проверка 5: Нет пустых code blocks
    empty_code_blocks = domain_knowledge.count('```python\n```') + domain_knowledge.count('```javascript\n```')
    if empty_code_blocks > 0:
        errors.append(f"Найдено {empty_code_blocks} пустых code blocks")

    if errors:
        return False, f"[{agent_name}] ВАЛИДАЦИЯ ПРОВАЛЕНА: " + "; ".join(errors)

    return True, "OK"


def create_backup(file_path: Path) -> Path:
    """
    Создать backup оригинального файла.

    Args:
        file_path: Путь к оригинальному файлу

    Returns:
        Path: Путь к backup файлу
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".backup_{timestamp}.md")
    shutil.copy2(file_path, backup_path)

    print(f"  [BACKUP] {backup_path.name}")
    return backup_path


def generate_refactored_content(
    agent_name: str,
    system_prompt: str,
    domain_knowledge: str
) -> str:
    """
    Генерировать новый content на основе template.

    Args:
        agent_name: Название агента
        system_prompt: Системный промпт (БЕЗ доменных знаний)
        domain_knowledge: Доменные знания (БЕЗ системного промпта)

    Returns:
        str: Новый content
    """
    template = f"""# {agent_name} - Knowledge Base

## 📚 Общие правила для всех агентов

**ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:** Прочитай [Общие правила агентов](../_shared/agent_common_rules.md)

Все агенты следуют единым правилам workflow, качества и взаимодействия. Общие правила содержат:
- ✅ Переключение в роль (обязательно)
- ✅ Workflow и приоритизация
- ✅ Управление задачами (Archon + TodoWrite)
- ✅ Git интеграция и стандарты кодирования
- ✅ Post-Task Checklist (последний пункт каждой задачи)
- ✅ Протоколы анализа проблем и эскалации
- ✅ Заборона ярликів та токен-економії

---

## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: {agent_name}

**Ты - {agent_name}**, эксперт в [ОБЛАСТЬ ЭКСПЕРТИЗЫ].

### ⚠️ ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:
**ПРОЧИТАЙ:** [`agent_common_rules.md`](../_shared/agent_common_rules.md) - содержит критически важные правила workflow, качества и эскалации.

{system_prompt}

---

## 🔍 ДОМЕННЫЕ ЗНАНИЯ: [ОБЛАСТЬ]

{domain_knowledge}

---

**Версия:** 2.0 (Модульная архитектура)
**Дата рефакторинга:** {datetime.now().strftime("%Y-%m-%d")}
**Автор рефакторинга:** Archon Blueprint Architect
"""
    return template


def refactor_agent_knowledge(
    file_path: Path,
    dry_run: bool = False
) -> Tuple[bool, str]:
    """
    Рефакторить один knowledge файл агента.

    Args:
        file_path: Путь к knowledge файлу
        dry_run: Если True, только показать изменения без записи

    Returns:
        Tuple[bool, str]: (success, message)
    """
    agent_name = extract_agent_name(file_path)

    # Прочитать оригинальный файл
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, f"[ERROR] Не удалось прочитать файл: {e}"

    # Анализ
    original_lines = original_content.count('\n')
    common_rules_lines = count_lines_with_common_rules(original_content)

    print(f"\n[PROCESSING] {agent_name}")
    print(f"  Оригинал: {original_lines} строк")
    print(f"  Общие правила (дубликаты): ~{common_rules_lines} строк")

    # Извлечь компоненты
    system_prompt = extract_system_prompt(original_content, agent_name)
    domain_knowledge = extract_domain_knowledge(original_content)

    # Валидация извлечённого контента
    is_valid, validation_msg = validate_extracted_content(system_prompt, domain_knowledge, agent_name)

    if not is_valid:
        print(f"  [VALIDATION FAILED] {validation_msg}")
        return False, validation_msg

    print(f"  [VALIDATION OK] Системный промпт: {len(system_prompt)} символов, Доменные знания: {len(domain_knowledge)} символов")

    # Генерировать новый content
    new_content = generate_refactored_content(
        agent_name=agent_name,
        system_prompt=system_prompt,
        domain_knowledge=domain_knowledge
    )

    new_lines = new_content.count('\n')

    print(f"  Новый файл: {new_lines} строк")
    print(f"  Удалено дубликатов: ~{common_rules_lines} строк общих правил")

    if dry_run:
        print(f"  [DRY RUN] Изменения НЕ применены")
        return True, "Dry run successful"

    # Создать backup
    backup_path = create_backup(file_path)

    # Записать новый content
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [SUCCESS] Файл обновлён")
        return True, f"Refactored successfully"

    except Exception as e:
        # Восстановить из backup при ошибке
        shutil.copy2(backup_path, file_path)
        return False, f"[ERROR] Ошибка записи: {e} (восстановлено из backup)"


def main():
    """Главная функция скрипта."""
    # Настройки
    PROJECT_ROOT = Path(__file__).parent
    AGENTS_DIR = PROJECT_ROOT / "use-cases" / "agent-factory-with-subagents" / "agents"

    # ПОЭТАПНАЯ ОБРАБОТКА ПО ГРУППАМ
    GROUP_FILTER = "archon"  # Изменить для других групп: "specialized", "pattern", "all"
    DRY_RUN = False  # PRODUCTION MODE - реальный рефакторинг

    print("=" * 70)
    print("AGENT KNOWLEDGE REFACTORING SCRIPT V3 (FIXED)")
    print("=" * 70)
    print(f"Директория агентов: {AGENTS_DIR}")
    print(f"Группа обработки: {GROUP_FILTER.upper()}")
    print(f"Режим: {'DRY RUN (без изменений)' if DRY_RUN else 'PRODUCTION (с изменениями)'}")
    print("=" * 70)

    # Показать описание групп
    group_descriptions = {
        "archon": "Archon агенты (5 шт) - Core team, универсальные агенты",
        "specialized": "Специализированные агенты (13 шт) - Доменные эксперты",
        "pattern": "Pattern агенты (18 шт) - PatternShift-специфичные, последовательный workflow",
        "all": "ВСЕ агенты (37 шт) - Использовать только после успешной обработки всех групп"
    }
    print(f"\n[INFO] {group_descriptions.get(GROUP_FILTER, 'Неизвестная группа')}")

    # Найти knowledge файлы для выбранной группы
    knowledge_files = find_agent_knowledge_files(AGENTS_DIR, group_filter=GROUP_FILTER)
    print(f"[INFO] Найдено {len(knowledge_files)} knowledge файлов для группы '{GROUP_FILTER}'")

    if not knowledge_files:
        print(f"[ERROR] Knowledge файлы для группы '{GROUP_FILTER}' не найдены!")
        return

    # Показать список агентов
    print(f"\n[AGENTS] Будут обработаны:")
    for i, file_path in enumerate(knowledge_files, 1):
        agent_name = extract_agent_name(file_path)
        print(f"  {i}. {agent_name}")

    # Рефакторить каждый файл
    success_count = 0
    failed_count = 0

    for file_path in knowledge_files:
        success, message = refactor_agent_knowledge(file_path, dry_run=DRY_RUN)

        if success:
            success_count += 1
        else:
            failed_count += 1
            print(f"  [FAILED] {message}")

    # Итоговая статистика
    print("\n" + "=" * 70)
    print(f"РЕЗУЛЬТАТЫ РЕФАКТОРИНГА - ГРУППА '{GROUP_FILTER.UPPER()}'")
    print("=" * 70)
    print(f"Успешно: {success_count}/{len(knowledge_files)}")
    print(f"Ошибки: {failed_count}/{len(knowledge_files)}")

    if success_count > 0:
        print(f"\n[SUCCESS] Модульная архитектура применена к {success_count} агентам группы '{GROUP_FILTER}'!")
        print(f"[INFO] Backup файлы созданы для всех изменённых агентов")

        # Рекомендации по следующим шагам
        next_steps = {
            "archon": "specialized",
            "specialized": "pattern",
            "pattern": "all"
        }
        if GROUP_FILTER in next_steps:
            print(f"\n[NEXT] Следующая группа: '{next_steps[GROUP_FILTER]}'")
            print(f"[NEXT] Измените GROUP_FILTER = \"{next_steps[GROUP_FILTER]}\" и запустите снова")

        if not DRY_RUN:
            print(f"\n[GIT] Следующий шаг: git commit + push для группы '{GROUP_FILTER}'")


if __name__ == "__main__":
    main()
