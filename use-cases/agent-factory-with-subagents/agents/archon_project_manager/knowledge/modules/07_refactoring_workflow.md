# Module 07: Refactoring Workflow

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Создание новых knowledge base модулей
- Рефакторинг существующих агентов
- Оптимизация токенов базы знаний
- Валидация модульной архитектуры
- Применение best practices к документации
- Создание систем триггеров
- Миграция с монолитных к модульным knowledge bases

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** рефакторинг, оптимизация токенов, модульная архитектура, знания агента, триггеры загрузки, чек-лист

**English:** refactoring, token optimization, modular architecture, agent knowledge, loading triggers, checklist

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Планируешь рефакторинг knowledge base любого агента
- Нужно создать новый агент с оптимизированной структурой
- Задача: "оптимизировать токены агента"
- Задача: "сделать модульную архитектуру знаний"
- Нужно создать триггеры для интеллектуальной загрузки модулей

---

## 📋 ЧЕКЛИСТ РЕФАКТОРИНГА AGENT KNOWLEDGE BASE

### ЭТАП 1: Инвентаризация и анализ

```python
async def analyze_current_knowledge_base(agent_name: str):
    """
    Провести полный анализ текущей базы знаний агента.

    Returns:
        dict: Статистика и рекомендации
    """

    # 1. Измерить текущее состояние
    current_file = f"{agent_name}_knowledge.md"
    total_lines = count_lines(current_file)
    estimated_tokens = total_lines * 30  # Приблизительная оценка

    print(f"📊 ТЕКУЩЕЕ СОСТОЯНИЕ: {agent_name}")
    print(f"📄 Строк: {total_lines}")
    print(f"🔢 Токенов (оценка): {estimated_tokens}")

    # 2. Составить список ВСЕХ правил
    all_rules = extract_all_rules(current_file)
    print(f"📋 Правил всего: {len(all_rules)}")

    # 3. Категоризировать правила
    categories = categorize_rules(all_rules)
    for category, count in categories.items():
        print(f"  - {category}: {count} правил")

    # 4. Определить частоту использования
    usage_frequency = analyze_usage_frequency(categories)
    print(f"\n🔥 ТОП-5 категорий по частоте использования:")
    for i, (category, frequency) in enumerate(usage_frequency[:5], 1):
        print(f"  {i}. {category}: {frequency}%")

    # 5. Рекомендации по модулям
    recommended_modules = recommend_module_structure(categories, usage_frequency)
    print(f"\n💡 Рекомендуется создать {len(recommended_modules)} модулей")

    return {
        "total_lines": total_lines,
        "estimated_tokens": estimated_tokens,
        "total_rules": len(all_rules),
        "categories": categories,
        "top_categories": usage_frequency[:5],
        "recommended_modules": recommended_modules
    }
```

### ЭТАП 2: Создание ultra-compact core

**Цель:** Сократить основной файл до 150-300 строк

```markdown
# [Agent Name] - Knowledge Base

**Версия:** 2.0
**Дата:** [YYYY-MM-DD]

## 🔥 TOP-10 КРИТИЧНЫХ ПРАВИЛ (для 90% задач)

### 1. [Самое важное правило]
[Краткое описание с примером кода]

### 2. [Второе по важности]
[Краткое описание с примером кода]

[... 8 more critical rules ...]

## 📖 MODULE INDEX

| Модуль | Приоритет | Домен | Когда читать | Строк |
|--------|-----------|-------|--------------|-------|
| [01](modules/01_...) | 🔴 | [Domain] | [Trigger] | ~200 |
| [02](modules/02_...) | 🟡 | [Domain] | [Trigger] | ~200 |
[...]

**Легенда приоритетов:**
- 🔴 CRITICAL - читай ВСЕГДА
- 🟡 HIGH - читай часто
- 🟢 MEDIUM - читай по необходимости
```

### ЭТАП 3: Создание модулей с триггерами

**Стандартная структура модуля:**

```markdown
# Module [NN]: [Module Name]

**Версия:** 1.0
**Дата:** [YYYY-MM-DD]
**Автор:** [Agent Role]

**Назад к:** [Main Knowledge Base](../[agent]_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- [Техническая ситуация 1] (например: "Ошибка 'No such tool available'")
- [Техническая ситуация 2]
- [Техническая ситуация 3]
- [Операция X требует знаний из модуля]

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** [слово1], [слово2], [слово3], ...

**English:** [word1], [word2], [word3], ...

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- [Простое описание ситуации 1]
- [Простое описание ситуации 2]
- [Простое описание ситуации 3]

---

## [ОСНОВНОЕ СОДЕРЖАНИЕ МОДУЛЯ]

[Правила, примеры кода, best practices для данного домена]

---

**Навигация:**
- [← Предыдущий модуль: [Name]](0[N-1]_[name].md)
- [↑ Назад к [Agent] Knowledge Base](../[agent]_knowledge.md)
- [→ Следующий модуль: [Name]](0[N+1]_[name].md)
```

### ЭТАП 4: Валидация полноты

```python
async def validate_refactoring_completeness(agent_name: str):
    """
    Проверить что ВСЕ правила сохранены после рефакторинга.

    Returns:
        bool: True если все правила сохранены
    """

    # 1. Извлечь правила из OLD файла
    old_file = f"{agent_name}_knowledge_OLD_[date].md"
    old_rules = extract_all_rules(old_file)

    # 2. Извлечь правила из НОВЫХ файлов (core + modules)
    core_file = f"{agent_name}_knowledge.md"
    core_rules = extract_all_rules(core_file)

    module_rules = []
    for module_file in glob("modules/*.md"):
        module_rules.extend(extract_all_rules(module_file))

    new_rules = core_rules + module_rules

    # 3. Сравнить
    print(f"📊 ВАЛИДАЦИЯ ПОЛНОТЫ ПРАВИЛ")
    print(f"📄 Было правил: {len(old_rules)}")
    print(f"📄 Стало правил: {len(new_rules)}")

    if len(new_rules) < len(old_rules):
        missing = set(old_rules) - set(new_rules)
        print(f"❌ ПОТЕРЯНО ПРАВИЛ: {len(missing)}")
        for rule in missing:
            print(f"  - {rule}")
        return False

    print(f"✅ ВСЕ ПРАВИЛА СОХРАНЕНЫ!")
    return True
```

### ЭТАП 5: Валидация триггеров

**Цель:** Проверить что каждый модуль имеет достаточно триггеров для автоматической загрузки.

```python
async def validate_trigger_system(agent_name: str):
    """
    Валидировать систему триггеров для всех модулей.

    Returns:
        dict: Результаты валидации по каждому модулю
    """

    results = {}

    for module_file in glob("modules/*.md"):
        module_name = extract_module_name(module_file)

        # 1. Проверить наличие трёх типов триггеров
        has_technical = check_section_exists(module_file, "ТЕХНИЧЕСКИЕ ТРИГГЕРЫ")
        has_keywords = check_section_exists(module_file, "КЛЮЧЕВЫЕ СЛОВА")
        has_context = check_section_exists(module_file, "КОГДА ЧИТАТЬ")

        # 2. Проверить количество триггеров
        technical_count = count_trigger_items(module_file, "ТЕХНИЧЕСКИЕ ТРИГГЕРЫ")
        keyword_count = count_keywords(module_file)
        context_count = count_trigger_items(module_file, "КОГДА ЧИТАТЬ")

        # 3. Оценка качества
        quality_score = 0
        if has_technical and technical_count >= 3:
            quality_score += 40
        if has_keywords and keyword_count >= 5:
            quality_score += 30
        if has_context and context_count >= 3:
            quality_score += 30

        results[module_name] = {
            "has_all_sections": has_technical and has_keywords and has_context,
            "technical_triggers": technical_count,
            "keywords": keyword_count,
            "context_triggers": context_count,
            "quality_score": quality_score,
            "status": "✅ ОТЛИЧНО" if quality_score >= 90 else "⚠️ ТРЕБУЕТ ДОРАБОТКИ"
        }

    # 4. Вывод результатов
    print(f"📊 ВАЛИДАЦИЯ СИСТЕМЫ ТРИГГЕРОВ")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for module, stats in results.items():
        print(f"\n{module}:")
        print(f"  Технические триггеры: {stats['technical_triggers']}")
        print(f"  Ключевые слова: {stats['keywords']}")
        print(f"  Контекстные триггеры: {stats['context_triggers']}")
        print(f"  Качество: {stats['quality_score']}/100 - {stats['status']}")

    return results
```

---

## 🎯 BEST PRACTICES МОДУЛЬНОЙ АРХИТЕКТУРЫ

### Размеры модулей

```
РЕКОМЕНДУЕМЫЕ РАЗМЕРЫ:
├─ Core file: 150-300 строк
├─ Critical modules (🔴): 200-300 строк
├─ High priority (🟡): 150-250 строк
└─ Medium priority (🟢): 100-200 строк

МАКСИМАЛЬНЫЕ РАЗМЕРЫ:
├─ Core file: 400 строк
└─ Любой модуль: 500 строк
```

### Три уровня триггеров (ОБЯЗАТЕЛЬНО)

1. **ТЕХНИЧЕСКИЕ ТРИГГЕРЫ** - Для экспертов и автоматических систем
   - Конкретные ошибки (например: `"Ошибка 'No such tool available'"`)
   - Технические операции (например: `"Создание проекта с обязательными полями"`)
   - API вызовы (например: `"mcp__archon__find_projects() failed"`)

2. **КЛЮЧЕВЫЕ СЛОВА** - Для автоматического поиска
   - Русские + English версии
   - Минимум 5-10 слов
   - Покрывают основной домен модуля

3. **КОНТЕКСТ** - Для пользователя простым языком
   - "Когда нужно..." описания
   - Понятные ситуации из практики
   - Без технических терминов

### Навигация между модулями

```markdown
**Навигация:**
- [← Предыдущий модуль: Task Management](03_task_management.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Context Recovery](05_context_recovery.md)
```

---

## 📊 МЕТРИКИ УСПЕШНОЙ ОПТИМИЗАЦИИ

### Целевые показатели:

```
✅ УСПЕШНЫЙ РЕФАКТОРИНГ:
├─ Сохранность правил: 100% (ничего не потеряно)
├─ Количество модулей: 5-10 (оптимально 7)
├─ Core file: ≤300 строк
├─ Каждый модуль: ≤500 строк
└─ Триггеры: 3 типа в каждом модуле

📊 ПРИМЕРЫ УСПЕШНЫХ РЕФАКТОРИНГОВ:
├─ Blueprint Architect: 1693 → 280 строк
└─ Project Manager: 1135 → 280 строк
```

### Формула расчёта оптимизации:

```python
def calculate_optimization_percentage(old_lines: int, new_core_lines: int) -> float:
    """
    Вычислить процент оптимизации core файла.

    Args:
        old_lines: Количество строк в старом монолитном файле
        new_core_lines: Количество строк в новом core файле

    Returns:
        float: Процент оптимизации
    """
    reduction = old_lines - new_core_lines
    optimization_percent = (reduction / old_lines) * 100
    return round(optimization_percent, 1)

# Пример:
optimization = calculate_optimization_percentage(1135, 280)
# → 75.3%
```

---

## 🔄 MIGRATION GUIDE TEMPLATE

**При создании рефакторинга обязательно создать MIGRATION_GUIDE.md:**

```markdown
# Migration Guide: [Agent Name] Knowledge Base

**Версия:** OLD → 2.0
**Дата:** [YYYY-MM-DD]
**Автор:** [Agent Role]

## 📊 Что изменилось

### Метрики:
- **Было:** [N] строк
- **Стало:** [K] строк (core file)

### Структура:
- **Было:** 1 монолитный файл
- **Стало:** 1 core + [N] модулей

## 📖 Соответствие старого → нового

| Старый раздел | Новое расположение |
|--------------|-------------------|
| [Old Section 1] | Core: Section [N] |
| [Old Section 2] | Module 01: [Name] |
| [Old Section 3] | Module 02: [Name] |
[...]

## 🎯 Как использовать новую структуру

1. **Всегда начинай с core файла** - содержит ТОП-10 правил
2. **Читай модули по триггерам** - система автоматически подскажет
3. **Используй навигацию** - каждый модуль содержит ссылки

## ⚠️ Критические изменения

- [Список изменений требующих внимания]
- [Breaking changes если есть]

## ✅ Чек-лист миграции

- [ ] Прочитать core file
- [ ] Ознакомиться с MODULE INDEX
- [ ] Прочитать Module 01 (критичный)
- [ ] По необходимости загружать остальные модули

## 📞 Поддержка

При возникновении вопросов обращайтесь к [Agent Role] или читайте
Module 07: Refactoring Workflow для деталей процесса.
```

---

**Навигация:**
- [← Предыдущий модуль: Examples & Templates](06_examples_templates.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
