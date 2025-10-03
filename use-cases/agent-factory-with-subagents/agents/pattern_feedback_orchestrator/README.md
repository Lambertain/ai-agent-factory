# Pattern Feedback Orchestrator Agent

Специализированный Pydantic AI агент для дизайна систем обратной связи в рамках системы PatternShift.

## 🎯 Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль эксперта по обратной связи

⚠️ **СПЕЦИАЛИЗАЦИЯ:** Это Pattern агент для проекта PatternShift, НЕ универсальный агент. Работает с психометрией, UX research и поведенческой аналитикой.

## 🧠 Как использовать агента

### Активация роли согласно D:\Automation\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
🔍 Ищу промпт роли Pattern Feedback Orchestrator...
📁 Поиск через: Glob(**/*pattern*feedback*knowledge*.md)
📖 Читаю системный промпт роли...

🎭 ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN FEEDBACK ORCHESTRATOR

Моя экспертиза:
- Психометрия и теория измерений (Likert, NPS, VAS)
- UX research методология и дизайн форм
- Поведенческая аналитика и engagement metrics
- Детекция кризисных состояний через паттерны ответов
- Создание триггерных правил маршрутизации
- Генерация действенных инсайтов (actionable insights)

✅ Готов проектировать системы обратной связи
```

### Запрос от пользователя:

```
Прими роль Pattern Feedback Orchestrator и создай форму обратной связи для модуля Day 5.
```

### Пример работы с формой обратной связи:

После принятия роли передайте Claude запрос на создание формы:

```
Создай форму обратной связи для модуля "Практика осознанного дыхания" Day 5.
Цель: progress_tracking
Длительность заполнения: 2 минуты
Включить детекцию кризисов: да
```

## 📋 Что делает агент

### Входные данные:
- Цель формы обратной связи (progress_tracking, satisfaction, engagement)
- Целевой модуль программы PatternShift
- Доступное время на заполнение (2-3 минуты)
- Параметры детекции кризисных состояний

### Выходные данные:
- **Форма обратной связи** - 5-7 вопросов с психометрической валидностью
- **Триггерные правила** - автоматическая маршрутизация на основе ответов
- **Детекция кризисов** - выявление паттернов риска в реальном времени
- **Actionable insights** - конкретные рекомендации по улучшению программы

## 🔧 Структура агента

```
pattern_feedback_orchestrator/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты дизайна обратной связи
├── dependencies.py             # Зависимости и типы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── models.py                   # Pydantic модели данных
├── knowledge/
│   └── pattern_feedback_orchestrator_knowledge.md  # База знаний
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
from pattern_feedback_orchestrator import run_pattern_feedback_orchestrator

# Простой пример создания формы обратной связи
result = await run_pattern_feedback_orchestrator(
    "Создай форму обратной связи для модуля Day 10",
    api_key="your_api_key"
)

print(result)
```

### Продвинутое использование

```python
from pattern_feedback_orchestrator.agent import agent
from pattern_feedback_orchestrator.dependencies import PatternFeedbackOrchestratorDependencies
from pattern_feedback_orchestrator.tools import design_feedback_form, create_trigger_rules

# Создание зависимостей
deps = PatternFeedbackOrchestratorDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift"
)

# Прямой вызов инструмента дизайна формы
from pydantic_ai import RunContext
result = await design_feedback_form(
    ctx=RunContext(deps=deps),
    purpose="satisfaction",
    target_module="Module: Day 15 - Практика благодарности",
    duration_minutes=2,
    include_crisis_detection=True
)

print(result)
```

## 🛠️ Доступные инструменты

### Основные инструменты дизайна обратной связи

- `design_feedback_form()` - Создание формы обратной связи (5-7 вопросов)
- `create_trigger_rules()` - Генерация триггерных правил маршрутизации
- `detect_crisis_patterns()` - Детекция кризисных паттернов в ответах
- `generate_actionable_insights()` - Генерация действенных инсайтов
- `search_agent_knowledge()` - Поиск best practices в базе знаний

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## 📚 База знаний содержит:

- **Системный промпт** из PatternShift системы (FEEDBACK ORCHESTRATOR AGENT)
- **Психометрия** - уровни измерения Stevens, шкалы Likert, NPS, VAS, Semantic Differential
- **Response Biases** - социальная желательность, acquiescence, extreme/central tendency
- **UX Research** - тайминг обратной связи, принципы дизайна форм, progressive disclosure
- **Behavioral Analytics** - паттерны кризисных состояний, engagement metrics
- **Триггерные правила** - low engagement, difficulty spike, crisis detection, success celebration
- **Actionable Insights Framework** - SMART критерии для действенных рекомендаций
- **Примеры форм** - end-of-day check-in, module completion feedback

## 🎨 Примеры использования

### Пример 1: End-of-Day Check-in

**Исходный запрос:**
```
Создай краткую форму обратной связи для конца дня
Модуль: Day 7
Цель: engagement + прогресс
Время: 2 минуты
```

**Результат:**
- ✅ 5 вопросов: общая оценка дня, применение техник, что помогло, уровень энергии, планы на завтра
- ✅ Likert scales + slider + open text
- ✅ Детекция низкой энергии (trigger на support)
- ✅ Therapeutic intent: рефлексия через вопросы

### Пример 2: Module Completion Feedback

**Исходный запрос:**
```
Создай форму обратной связи после завершения модуля "Техники релаксации"
Цель: satisfaction + difficulty assessment
Время: 3 минуты
Детекция кризисов: включить
```

**Результат:**
```
1. Насколько упражнение было полезным? (Likert 1-5)
2. Уровень сложности? (Slider 1-10)
3. Что вызвало затруднение? (Open text, 200 chars)
4. Как себя чувствуете сейчас? (Slider 1-10) - детекция кризиса
5. Рекомендовали бы другим? (NPS 0-10)

Триггеры:
- Score <= 2 на Q1 → supportive message (2 часа)
- Score >= 8 на Q2 → reduce difficulty (20%)
- Score <= 3 на Q4 → escalate to professional (critical)
- Score >= 9 на Q5 → celebration message
```

### Пример 3: Crisis Detection

**Исходный запрос:**
```
Проанализируй ответы на предмет кризисных паттернов
Ответы: {
  "general": 2,
  "difficulty": 9,
  "insights": "Чувствую безнадежность, не вижу смысла продолжать",
  "wellbeing": 2
}
```

**Результат:**
```
⚠️ Обнаружено 2 индикатора

1. [HIGH] Ключевые слова риска в текстовых ответах
   Уверенность: 85%
   Эскалация: ✅ Требуется
   Рекомендуемые действия:
   - Немедленная эскалация
   - Предоставить контакты кризисной помощи
   Ресурсы:
   - Телефон доверия: 8-800-2000-122
   - Психологическая помощь онлайн

2. [MEDIUM] Множественные низкие оценки
   Уверенность: 75%
   Эскалация: ❌ Не требуется
   Рекомендуемые действия:
   - Отправить поддерживающее сообщение
   - Предложить альтернативные ресурсы
```

### Пример 4: Actionable Insights

**Исходный запрос:**
```
Сгенерируй действенные инсайты из агрегированных данных
Данные: {
  "avg_satisfaction": 2.8,
  "avg_difficulty": 7.5
}
```

**Результат:**
```
💡 Сгенерировано 2 действенных инсайтов

1. **Низкая удовлетворенность**
   Действие: Пересмотреть содержание модуля
   Метрика: Повышение avg_satisfaction до >= 3.5
   Срок: Следующая итерация

2. **Слишком высокая сложность**
   Действие: Упростить упражнения, добавить промежуточные шаги
   Метрика: Снижение avg_difficulty до 5-6
   Срок: Немедленно
```

## 🔗 Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\Automation\Development\projects\patternshift\docs\content-agents-system-prompts.md` (раздел 8: FEEDBACK ORCHESTRATOR AGENT)
- `D:\Automation\Development\projects\patternshift\docs\final-kontent-architecture-complete.md`

## ⚠️ Важные принципы

- **Краткость** - формы <3 минут заполнения, максимум 5-7 вопросов
- **Минимизация social desirability** - нейтральные формулировки, нормализация "негативных" ответов
- **Психометрическая валидность** - правильные типы шкал для измеряемых конструктов
- **Терапевтический эффект** - вопросы создают рефлексию сами по себе
- **Actionability** - каждый инсайт ведет к конкретному действию
- **Crisis-aware** - детекция кризисных состояний через паттерны ответов

## 📚 Загрузка в Archon Knowledge Base

После создания агента загрузите файл знаний:

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_feedback_orchestrator_knowledge.md`
4. Добавьте теги:
   - `pattern-feedback`
   - `psychometrics`
   - `ux-research`
   - `behavioral-analytics`
   - `crisis-detection`
   - `agent-knowledge`
   - `patternshift`

## 🚀 Быстрый старт

1. Запросите роль: "Прими роль Pattern Feedback Orchestrator"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте запрос: "Создай форму обратной связи для [модуль]"
4. Получите спроектированную форму с триггерами и детекцией кризисов

---

*Pattern Feedback Orchestrator Agent - дизайн систем обратной связи с психометрической валидностью для системы PatternShift*
