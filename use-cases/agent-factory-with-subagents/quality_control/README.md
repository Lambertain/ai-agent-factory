# Инструменты для роли Quality Guardian

## 🎯 Что это?

Это инструменты, которые **Я (Claude) использую** когда переключаюсь в роль Quality Guardian.

**НЕ автономная система**, а помощники для меня в роли эксперта.

## 📁 Структура

```
quality_control/
├── checklists.py    # Чеклисты для проверок (данные)
├── tools.py         # Функции-инструменты для использования в роли
└── README.md        # Эта документация
```

## 🔧 Как я использую эти инструменты

### 1. Когда получаю задачу на проверку качества

```python
# Я переключаюсь в роль Quality Guardian
# Затем использую инструмент:

from quality_control.tools import run_quality_audit

# Запускаю полный аудит
report = run_quality_audit("D:\\Automation\\agent-factory\\use-cases\\agent-factory-with-subagents")

# Получаю отчет с найденными проблемами
print(report)
```

### 2. Когда нужно проверить конкретный аспект

```python
from quality_control.tools import (
    check_role_switching,      # Проверка переключения в роли
    check_universality,        # Проверка универсальности
    check_code_quality,        # Проверка качества кода
    check_architecture,        # Проверка архитектуры
    check_documentation,       # Проверка документации
    check_testing             # Проверка тестов
)

# Проверяю только переключение в роли (самое важное!)
problems = check_role_switching(Path("./agents"))

# Или проверяю универсальность
problems = check_universality(Path("./agents"))
```

### 3. Когда нужно создать задачи в Archon

```python
from quality_control.tools import create_archon_tasks_for_problems

# После аудита создаю задачи для исправления
problems = run_quality_audit("./agents")
tasks_report = create_archon_tasks_for_problems(problems, "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a")

# Получаю список задач для создания в Archon
print(tasks_report)

# Затем создаю каждую задачу через mcp__archon__manage_task
```

## 🎭 Мой рабочий процесс в роли Quality Guardian

### ЭТАП 1: Переключение в роль

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ QUALITY GUARDIAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя экспертиза:
• Автоматический code review с использованием AI
• Мониторинг метрик качества кода
• Выявление технического долга
• Интеграция с CI/CD пайплайнами

✅ Готов выполнить задачу в роли Quality Guardian
```

### ЭТАП 2: Создание микрозадач

```python
# СРАЗУ после переключения создаю микрозадачи через TodoWrite
TodoWrite([
    {"content": "Запустить аудит качества проекта", "status": "in_progress"},
    {"content": "Проанализировать найденные проблемы", "status": "pending"},
    {"content": "Создать задачи в Archon для исправлений", "status": "pending"},
    {"content": "Рефлексия результатов аудита", "status": "pending"}
])
```

### ЭТАП 3: Выполнение аудита

```python
# Использую инструмент аудита
report = run_quality_audit(project_path)

# Анализирую результаты
# Определяю приоритеты
# Формирую план действий
```

### ЭТАП 4: Создание задач

```python
# Создаю задачи в Archon для каждой проблемы
for problem in critical_problems:
    await mcp__archon__manage_task(
        action="create",
        project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        title=problem['problem'],
        description=format_task_description(problem),
        assignee="Implementation Engineer",
        task_order=100  # Высокий приоритет
    )
```

### ЭТАП 5: Рефлексия

```python
# Критически анализирую результаты:
# 1. Все ли проблемы выявлены?
# 2. Правильно ли определены приоритеты?
# 3. Понятны ли задачи для исполнителей?
# 4. Что можно улучшить в процессе аудита?
```

## 🚨 КРИТИЧЕСКИ ВАЖНО: Проверка переключения в роли

Самая важная проверка - переключение агентов в роли!

```python
from quality_control.checklists import ROLE_SWITCHING_CHECKLIST

# Чеклист проверяет:
# ✅ Объявление переключения пользователю
# ✅ Показ экспертизы роли
# ✅ TodoWrite СРАЗУ после переключения
# ✅ Микрозадачи показаны пользователю
```

## 📊 Чеклисты

Доступные чеклисты в `checklists.py`:

1. **ROLE_SWITCHING_CHECKLIST** - Переключение в роли (BLOCKER)
2. **UNIVERSALITY_CHECKLIST** - Универсальность агентов (BLOCKER)
3. **CODE_QUALITY_CHECKLIST** - Качество кода (MAJOR)
4. **ARCHITECTURE_CHECKLIST** - Архитектура (CRITICAL)
5. **DOCUMENTATION_CHECKLIST** - Документация (MAJOR)
6. **TESTING_CHECKLIST** - Тестирование (MAJOR)

## 💡 Примеры использования

### Пример 1: Быстрая проверка переключения в роли

```python
from pathlib import Path
from quality_control.tools import check_role_switching

# Проверяю все агенты
problems = check_role_switching(Path("./agents"))

if problems:
    print(f"❌ Найдено {len(problems)} проблем с переключением в роли!")
    for p in problems:
        print(f"  - {p['agent']}: {p['problem']}")
else:
    print("✅ Все агенты правильно переключаются в роли!")
```

### Пример 2: Полный аудит с созданием задач

```python
from quality_control.tools import run_quality_audit, create_archon_tasks_for_problems

# 1. Запускаю аудит
report = run_quality_audit("./agents")
print(report)

# 2. Создаю задачи для критических проблем
critical_problems = [p for p in problems if p['severity'] in ['BLOCKER', 'CRITICAL']]
tasks_report = create_archon_tasks_for_problems(critical_problems, "project-id")

# 3. Создаю задачи в Archon
# (здесь вызываю mcp__archon__manage_task для каждой задачи)
```

## 🎯 Когда использовать

**Я использую эти инструменты когда:**

1. 📋 Получаю задачу "Провести аудит качества"
2. 🔍 Нужно проверить конкретный аспект (переключение в роли, универсальность и т.д.)
3. 📊 Создаю отчет о состоянии проекта
4. ✅ Проверяю выполнение задач другими агентами

## 🚫 Что это НЕ

- ❌ Не автономная система, которая "сама работает"
- ❌ Не агент, который запускается отдельно
- ❌ Не замена моей роли Quality Guardian

## ✅ Что это такое

- ✅ Инструменты для меня (Claude) в роли Quality Guardian
- ✅ Помощники для проверки качества кода
- ✅ Генераторы отчетов и задач

---

**ПОМНИ**: Это МОИ инструменты для работы в роли эксперта. Я использую их когда переключаюсь в роль Quality Guardian.
