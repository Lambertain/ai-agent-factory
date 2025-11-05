# Module 08: Design System Protocol

## 🚨 КРИТИЧЕСКОЕ ПРАВИЛО: Обязательная проверка дизайн-системы

**ЭТОТ МОДУЛЬ ЧИТАЕТСЯ ПО ДЕФОЛТУ ПЕРЕД ЛЮБОЙ UI РАБОТОЙ!**

### Проблема которую решает этот модуль

UI/UX Enhancement Agent создавал РАЗНЫЕ компоненты для ОДИНАКОВЫХ задач, игнорируя существующие паттерны проекта.

**Пример:**
- Транзакции: `SmartCategorySelector` (Select + AI кнопка)
- Assets: `InlineReferenceSelect` (Select + 4 inline кнопки)
- Calendar: `CalendarReferenceSelect` (Select + Edit + Dropdown меню)

**Все три делают CRUD операции со справочниками, но выглядят по-разному!**

---

## 📋 ОБЯЗАТЕЛЬНЫЙ WORKFLOW ПЕРЕД UI ИЗМЕНЕНИЯМИ

### ЭТАП 0: Проверка дизайн-системы (КРИТИЧЕСКИ ВАЖНО!)

```python
async def check_design_system_before_ui_work(project_path: str) -> dict:
    """
    ОБЯЗАТЕЛЬНАЯ проверка дизайн-системы перед началом работы.

    Этот этап НЕЛЬЗЯ пропустить!

    Args:
        project_path: Путь к проекту

    Returns:
        dict: Информация о дизайн-системе проекта
    """

    # Список файлов дизайн-системы (в порядке приоритета)
    design_files = [
        "DESIGN_SYSTEM.md",           # Основная дизайн-система
        "UI_STYLE_GUIDE.md",          # Руководство по стилю
        "COMPONENT_ARCHITECTURE.md",  # Архитектура компонентов
        "UI_PATTERNS.md",             # UI паттерны
        ".claude/design/patterns.md", # Claude-специфичные паттерны
        ".claude/design/components.md",
        "docs/design-system.md",
        "docs/ui-guidelines.md"
    ]

    found_files = []
    for file in design_files:
        full_path = os.path.join(project_path, file)
        if os.path.exists(full_path):
            # ОБЯЗАТЕЛЬНО прочитать файл
            content = read_file(full_path)
            found_files.append({
                "path": file,
                "content": content
            })

    if not found_files:
        # Дизайн-системы НЕТ → создать её
        print("[WARNING] Дизайн-система не найдена в проекте!")
        print("[ACTION] Создаю дизайн-систему для проекта...")

        design_system = await create_design_system_for_project(project_path)
        return {
            "exists": False,
            "created": True,
            "design_system": design_system
        }

    return {
        "exists": True,
        "files": found_files,
        "patterns": extract_patterns_from_files(found_files)
    }
```

### КРИТИЧЕСКИЕ ПРАВИЛА:

1. **НЕ НАЧИНАТЬ РАБОТУ БЕЗ ПРОВЕРКИ ДИЗАЙН-СИСТЕМЫ**
   - ❌ Нельзя пропустить Этап 0
   - ❌ Нельзя начать кодить без чтения дизайн-системы
   - ✅ ВСЕГДА читать DESIGN_SYSTEM.md перед работой

2. **ЕСЛИ ДИЗАЙН-СИСТЕМЫ НЕТ → СОЗДАТЬ ЕЁ**
   - ✅ Создать микрозадачу "Создать дизайн-систему проекта"
   - ✅ Проанализировать существующие компоненты
   - ✅ Задокументировать найденные паттерны
   - ✅ ТОЛЬКО ПОСЛЕ ЭТОГО делать UI изменения

3. **ЕСЛИ ПАТТЕРН ДЛЯ ЗАДАЧИ СУЩЕСТВУЕТ → ИСПОЛЬЗОВАТЬ ЕГО**
   - ❌ НЕ создавать новый компонент
   - ✅ Использовать существующий паттерн
   - ✅ Адаптировать под конкретный случай

---

## 🏗️ Функция создания дизайн-системы

```python
async def create_design_system_for_project(project_path: str) -> dict:
    """
    Создать дизайн-систему для проекта на основе существующих компонентов.

    Workflow:
    1. Сканировать все UI компоненты в проекте
    2. Извлечь паттерны (цвета, типографика, spacing, компоненты)
    3. Задокументировать найденные паттерны в DESIGN_SYSTEM.md
    4. Добавить CRUD Select Pattern для справочников

    Args:
        project_path: Путь к проекту

    Returns:
        dict: Созданная дизайн-система
    """

    print("[STEP 1/5] Сканирование UI компонентов...")
    components = scan_ui_components(project_path)

    print("[STEP 2/5] Извлечение цветовой палитры...")
    colors = extract_color_palette(components)

    print("[STEP 3/5] Анализ типографики...")
    typography = extract_typography(components)

    print("[STEP 4/5] Извлечение spacing system...")
    spacing = extract_spacing_system(components)

    print("[STEP 5/5] Документирование компонентов...")
    component_patterns = document_component_patterns(components)

    # Создать структуру дизайн-системы
    design_system = {
        "project_name": extract_project_name(project_path),
        "version": "1.0.0",
        "created_by": "UI/UX Enhancement Agent",
        "created_at": datetime.now().isoformat(),

        "colors": colors,
        "typography": typography,
        "spacing": spacing,

        "components": component_patterns,

        "patterns": {
            "crud_operations": generate_crud_pattern(components),
            "data_display": generate_data_display_patterns(components),
            "navigation": generate_navigation_patterns(components),
            "forms": generate_form_patterns(components)
        }
    }

    # Сохранить в DESIGN_SYSTEM.md
    design_system_md = format_design_system_to_markdown(design_system)
    write_file(
        os.path.join(project_path, "DESIGN_SYSTEM.md"),
        design_system_md
    )

    print(f"[OK] Дизайн-система создана: {project_path}/DESIGN_SYSTEM.md")

    return design_system


def scan_ui_components(project_path: str) -> list[dict]:
    """Сканировать все UI компоненты в проекте."""

    # Типичные локации компонентов
    component_dirs = [
        "src/components",
        "components",
        "src/ui",
        "ui",
        "app/components",
        "src/app/components"
    ]

    components = []
    for comp_dir in component_dirs:
        full_path = os.path.join(project_path, comp_dir)
        if os.path.exists(full_path):
            # Найти все .tsx/.jsx/.vue файлы
            files = glob(f"{full_path}/**/*.{{tsx,jsx,vue}}", recursive=True)

            for file in files:
                component_code = read_file(file)
                components.append({
                    "file": file,
                    "name": extract_component_name(file),
                    "code": component_code,
                    "type": detect_component_type(component_code)
                })

    return components


def extract_color_palette(components: list[dict]) -> dict:
    """Извлечь цветовую палитру из компонентов."""

    colors = {
        "primary": set(),
        "secondary": set(),
        "accent": set(),
        "background": set(),
        "text": set(),
        "border": set(),
        "status": {
            "success": set(),
            "warning": set(),
            "error": set(),
            "info": set()
        }
    }

    # Регулярные выражения для поиска цветов
    color_patterns = [
        r'bg-(\w+-\d+)',          # bg-blue-500
        r'text-(\w+-\d+)',        # text-gray-700
        r'border-(\w+-\d+)',      # border-red-300
        r'#([0-9A-Fa-f]{6})',     # #FF5733
        r'hsl\(([^)]+)\)',        # hsl(220 13% 91%)
        r'--(\w+-?\w*)',          # --primary-500
    ]

    for component in components:
        code = component["code"]

        # Найти все цвета в коде
        for pattern in color_patterns:
            matches = re.findall(pattern, code)
            # Классифицировать цвета...

    return format_color_palette(colors)


def generate_crud_pattern(components: list[dict]) -> dict:
    """
    Генерировать CRUD Select Pattern на основе существующих компонентов.

    Поиск паттернов:
    - Select компоненты со справочниками
    - CRUD операции (Create/Update/Delete)
    - Кнопки редактирования
    - Dropdown меню
    """

    # Найти все Select компоненты с CRUD операциями
    crud_selects = []
    for component in components:
        if is_crud_select_component(component):
            crud_selects.append(component)

    if not crud_selects:
        # НЕ найдено существующих CRUD Select → предложить стандартный паттерн
        return {
            "pattern": "ReferenceSelect",
            "description": "Универсальный CRUD Select для справочников",
            "structure": """
┌────────────────────────┐  ┌──┐  ┌──┐
│ [Выбрать значение ▼]  │  │✏️│  │⋮ │ ← Dropdown: Обновить/Добавить/Удалить
└────────────────────────┘  └──┘  └──┘
            """,
            "component_name": "ReferenceSelect",
            "usage": "Использовать для: категорий, статусов, приоритетов, типов и т.д.",
            "example": """
<ReferenceSelect
  value={selectedValue}
  onChange={handleChange}
  referenceType="priority"
  onCreate={handleCreate}
  onUpdate={handleUpdate}
  onDelete={handleDelete}
/>
            """
        }

    # Проанализировать существующие CRUD Select компоненты
    primary_pattern = crud_selects[0]  # Взять первый как эталон

    return {
        "pattern": extract_pattern_name(primary_pattern),
        "description": "Найден существующий CRUD паттерн в проекте",
        "structure": extract_visual_structure(primary_pattern),
        "component_name": primary_pattern["name"],
        "file": primary_pattern["file"],
        "usage": extract_usage_examples(primary_pattern),
        "variations": [
            extract_pattern_name(comp) for comp in crud_selects[1:]
        ]
    }
```

---

## 📝 Шаблон DESIGN_SYSTEM.md

```markdown
# Design System - [Project Name]

**Version:** 1.0.0
**Created:** [Date]
**Maintained by:** UI/UX Enhancement Agent

---

## 🎨 Colors

### Primary
- **Primary 500:** \`hsl(220 90% 56%)\` - Main brand color
- **Primary 600:** \`hsl(220 90% 46%)\` - Hover state
- **Primary 700:** \`hsl(220 90% 36%)\` - Active state

### Status Colors
- **Success:** \`hsl(142 76% 36%)\` - ✅ Успешные действия
- **Warning:** \`hsl(38 92% 50%)\` - ⚠️ Предупреждения
- **Error:** \`hsl(0 72% 51%)\` - ❌ Ошибки
- **Info:** \`hsl(217 91% 60%)\` - ℹ️ Информация

---

## 📐 Typography

### Font Families
- **Sans:** Inter, system-ui, sans-serif
- **Display:** Cal Sans, Inter, sans-serif
- **Mono:** Fira Code, Menlo, monospace

### Text Sizes
- **xs:** 0.75rem (12px)
- **sm:** 0.875rem (14px)
- **base:** 1rem (16px)
- **lg:** 1.125rem (18px)
- **xl:** 1.25rem (20px)
- **2xl:** 1.5rem (24px)

---

## 🧩 Component Patterns

### CRUD Select Pattern (Reference Data)

**ВСЕ компоненты для работы со справочниками ДОЛЖНЫ использовать ЕДИНЫЙ паттерн:**

```
┌────────────────────────┐  ┌──┐  ┌──┐
│ [Выбрать значение ▼]  │  │✏️│  │⋮ │ ← Dropdown: Обновить/Добавить/Удалить
└────────────────────────┘  └──┘  └──┘
```

**Компонент:** \`<ReferenceSelect />\`

**Использовать для:** категорий, статусов, приоритетов, типов и т.д.

**❌ НЕ создавать новые компоненты для той же задачи!**
**✅ Использовать существующий паттерн!**

**Пример использования:**

\`\`\`tsx
<ReferenceSelect
  value={priority}
  onChange={setPriority}
  referenceType="priority"
  onCreate={handleCreatePriority}
  onUpdate={handleUpdatePriority}
  onDelete={handleDeletePriority}
/>
\`\`\`

---

## 🚫 Запрещенные практики

### ❌ НЕ создавать разные компоненты для одинаковых задач

**Плохо:**
- \`SmartCategorySelector\` для транзакций
- \`InlineReferenceSelect\` для assets
- \`CalendarReferenceSelect\` для календаря

**Хорошо:**
- \`ReferenceSelect\` для ВСЕХ справочников

### ❌ НЕ игнорировать существующие паттерны

Перед созданием нового компонента:
1. Прочитать DESIGN_SYSTEM.md
2. Найти существующий паттерн
3. Использовать или адаптировать его

---

## 📚 Справочник компонентов

| Компонент | Назначение | Локация |
|-----------|------------|---------|
| \`ReferenceSelect\` | CRUD операции со справочниками | \`src/components/ReferenceSelect.tsx\` |
| \`Button\` | Действия пользователя | \`src/components/ui/Button.tsx\` |
| \`Card\` | Контейнеры контента | \`src/components/ui/Card.tsx\` |

---

**Последнее обновление:** [Date]
```

---

## 🔍 Как использовать этот модуль

### Сценарий 1: Начало новой UI задачи

```python
# Шаг 1: Прочитать дизайн-систему (ОБЯЗАТЕЛЬНО!)
design_system = await check_design_system_before_ui_work(project_path)

if not design_system["exists"]:
    # Создана новая дизайн-система
    print("[INFO] Создана дизайн-система для проекта")
    print(f"[INFO] Файл: {project_path}/DESIGN_SYSTEM.md")

# Шаг 2: Найти существующий паттерн для задачи
patterns = design_system.get("patterns", {})
crud_pattern = patterns.get("crud_operations")

if crud_pattern:
    print(f"[OK] Найден существующий CRUD паттерн: {crud_pattern['component_name']}")
    print(f"[OK] Использовать компонент: {crud_pattern['file']}")
else:
    print("[WARNING] CRUD паттерн не найден, создаю новый...")
    # Создать CRUD паттерн и добавить в дизайн-систему
```

### Сценарий 2: Создание нового компонента

```python
# ЗАПРЕЩЕННЫЙ подход (БЕЗ проверки дизайн-системы):
def create_component_wrong():
    # ❌ Начинаем кодить без проверки дизайн-системы
    component_code = generate_new_component()  # Создаст дубликат!
    write_file("CalendarReferenceSelect.tsx", component_code)


# ПРАВИЛЬНЫЙ подход (С проверкой дизайн-системы):
async def create_component_correct(task_description: str):
    # ✅ Шаг 1: Проверить дизайн-систему
    design_system = await check_design_system_before_ui_work(project_path)

    # ✅ Шаг 2: Найти существующий паттерн
    existing_pattern = find_pattern_for_task(design_system, task_description)

    if existing_pattern:
        print(f"[OK] Использую существующий компонент: {existing_pattern['component_name']}")
        # Адаптировать существующий компонент
        return adapt_existing_component(existing_pattern, task_description)
    else:
        print("[INFO] Создаю новый компонент (паттерн не найден)")
        # Создать новый компонент
        new_component = create_new_component(task_description)

        # ✅ Шаг 3: Добавить новый паттерн в дизайн-систему
        await add_pattern_to_design_system(design_system, new_component)

        return new_component
```

---

## 📊 Метрики улучшения

### ДО внедрения протокола:
- ❌ 3 разных компонента для CRUD select
- ❌ Несогласованный UI
- ❌ Дублирование кода
- ❌ Сложность поддержки

### ПОСЛЕ внедрения протокола:
- ✅ 1 универсальный ReferenceSelect
- ✅ Консистентный UI
- ✅ Переиспользование кода
- ✅ Простая поддержка

---

**Version:** 1.0
**Date:** 2025-11-05
**Author:** UI/UX Enhancement Agent (Improved by Archon Team)
**Project:** AI Agent Factory - UI/UX Agent Consistency Fix

**Changes:**
- ✅ Добавлен обязательный протокол проверки дизайн-системы
- ✅ Функция create_design_system_for_project() для генерации дизайн-системы
- ✅ CRUD Select Pattern для унификации справочников
- ✅ Запрет на создание дубликатов компонентов
- ✅ Примеры правильного и неправильного подходов
