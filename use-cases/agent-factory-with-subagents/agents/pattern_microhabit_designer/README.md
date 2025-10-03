# Pattern Microhabit Designer Agent

Специализированный Pydantic AI агент для создания микро-привычек и habit chains в рамках системы PatternShift.

## 🎯 Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль поведенческого дизайнера

⚠️ **СПЕЦИАЛИЗАЦИЯ:** Это Pattern агент для проекта PatternShift, НЕ универсальный агент. Работает с поведенческим дизайном и формированием привычек.

## 🧠 Как использовать агента

### Активация роли согласно D:\Automation\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
🔍 Ищу промпт роли Pattern Microhabit Designer...
📁 Поиск через: Glob(**/*pattern*microhabit*knowledge*.md)
📖 Читаю системный промпт роли...

🎭 ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN MICROHABIT DESIGNER

Моя экспертиза:
- Поведенческая экономика и нейробиология привычек
- Декомпозиция целей на атомарные действия
- Дизайн триггеров и вознаграждений
- Создание habit chains с domino effect
- Интеграция с программами трансформации PatternShift

✅ Готов создавать микро-привычки
```

### Запрос от пользователя:

```
Прими роль Pattern Microhabit Designer и создай микро-привычку для медитации.
```

### Пример работы с привычкой:

После принятия роли передайте Claude запрос на создание микро-привычки:

```
Создай микро-привычку на основе цели "медитировать каждый день".
Существующие рутины: чистка зубов утром, утренний кофе, поездка на работу
Доступное время: 2 минуты
```

## 📋 Что делает агент

### Входные данные:
- Цель поведенческого изменения
- Существующие рутины пользователя (для habit stacking)
- Доступное время
- Контекст пользователя (мотивация, барьеры)

### Выходные данные:
- **Микро-привычка** - конкретное действие <2 минут
- **Триггеры** - привязка к существующим рутинам
- **Вознаграждения** - immediate rewards для закрепления
- **Habit Chains** - цепочки усиливающих друг друга привычек
- **Анализ барьеров** - что может помешать и как устранить

## 🔧 Структура агента

```
pattern_microhabit_designer/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты дизайна привычек
├── dependencies.py             # Зависимости и типы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── models.py                   # Pydantic модели данных
├── knowledge/
│   └── pattern_microhabit_designer_knowledge.md  # База знаний
├── __init__.py                 # Экспорты
└── README.md                   # Документация
```

## 🚀 Программное использование (Pydantic AI)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Быстрый старт

```python
from pattern_microhabit_designer import run_pattern_microhabit_designer

# Простой пример создания микро-привычки
result = await run_pattern_microhabit_designer(
    "Создай микро-привычку для утренней медитации",
    api_key="your_api_key"
)

print(result)
```

### Продвинутое использование

```python
from pattern_microhabit_designer.agent import agent
from pattern_microhabit_designer.dependencies import PatternMicrohabitDesignerDependencies
from pattern_microhabit_designer.tools import design_microhabit, create_habit_chain

# Создание зависимостей
deps = PatternMicrohabitDesignerDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift"
)

# Прямой вызов инструмента дизайна привычки
from pydantic_ai import RunContext
result = await design_microhabit(
    ctx=RunContext(deps=deps),
    goal_description="Стать более осознанным",
    target_behavior="медитировать",
    existing_routines=["чистить зубы", "варить кофе"],
    available_time_seconds=120,
    difficulty_preference="micro"
)

print(result)
```

## 🛠️ Доступные инструменты

### Основные инструменты дизайна привычек

- `design_microhabit()` - Создание микро-привычки под цель
- `create_habit_chain()` - Построение цепочки привычек (domino effect)
- `identify_triggers_rewards()` - Подбор триггеров и вознаграждений
- `generate_module_variants()` - Адаптация под VAK/age/culture
- `search_agent_knowledge()` - Поиск best practices в базе знаний

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## 📚 База знаний содержит:

- **Системный промпт** из PatternShift системы (MICROHABIT DESIGNER AGENT)
- **Habit Loop** - модель Cue-Routine-Reward (Charles Duhigg)
- **Implementation Intentions** - "When X, I will Y" формат (Gollwitzer)
- **Atomic Habits** - принципы James Clear
- **Tiny Habits** - модель B=MAP (BJ Fogg)
- **Behavioral Economics** - поведенческая экономика
- **Примеры успешных микро-привычек** с разбором
- **Ссылки на контекстные файлы** PatternShift

## 🎨 Примеры использования

### Пример 1: Привычка чтения

**Исходный запрос:**
```
Создай микро-привычку для чтения книг
Существующие рутины: ложиться спать в 23:00
Доступное время: 2 минуты
```

**Результат:**
- ✅ Микро-привычка: "После того как лягу в кровать, я прочитаю 1 страницу"
- ✅ Триггер: лечь в кровать
- ✅ Friction removed: книга на тумбочке
- ✅ Celebration: "Я читатель!"
- ✅ Success probability: 0.92

### Пример 2: Утренняя Habit Chain

**Исходный запрос:**
```
Создай цепочку утренних привычек для энергичного старта дня
Якорь: встать с кровати
Целевые привычки: гидратация, дыхание, намерение, движение
Время: 5 минут
```

**Результат:**
```
1. Встаю с кровати → Выпиваю стакан воды (30 сек)
2. Выпиваю воду → Делаю 3 глубоких вдоха (30 сек)
3. Делаю вдохи → Записываю 1 намерение (60 сек)
4. Записываю → Делаю 5 приседаний (30 сек)
5. Приседания → Улыбаюсь "Yes!" (10 сек)
```

Cumulative impact: 0.88

### Пример 3: VAK адаптация

**Исходный запрос:**
```
Создай варианты микро-привычки "благодарность" для VAK типов
```

**Результат:**
- **Visual**: визуальный дневник благодарности с картинками
- **Auditory**: проговорить вслух 3 благодарности
- **Kinesthetic**: написать рукой в блокнот

## 🔗 Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\Automation\Development\projects\patternshift\docs\content-agents-system-prompts.md` (раздел 6: MICROHABIT DESIGNER AGENT)
- `D:\Automation\Development\projects\patternshift\docs\final-kontent-architecture-complete.md`

## ⚠️ Важные принципы

- **The 2-Minute Rule** - каждая привычка <2 минут
- **Friction reduction** - устранить все барьеры
- **Habit stacking** - привязка к существующим рутинам
- **Immediate rewards** - мгновенное вознаграждение
- **Celebration** - празднование малых побед критично
- **Domino effect** - цепочки усиливают эффект

## 📚 Загрузка в Archon Knowledge Base

После создания агента загрузите файл знаний:

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_microhabit_designer_knowledge.md`
4. Добавьте теги:
   - `pattern-microhabit`
   - `behavior-design`
   - `habits`
   - `agent-knowledge`
   - `patternshift`

## 🚀 Быстрый старт

1. Запросите роль: "Прими роль Pattern Microhabit Designer"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте запрос: "Создай микро-привычку для [цель]"
4. Получите спроектированную микро-привычку с триггерами и вознаграждениями

---

*Pattern Microhabit Designer Agent - создание эффективных микро-привычек с научной основой для системы PatternShift*
