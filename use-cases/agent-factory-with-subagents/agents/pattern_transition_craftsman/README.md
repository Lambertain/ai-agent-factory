# Pattern Transition Craftsman Agent

Специализированный Pydantic AI агент для создания переходов между модулями программы трансформации PatternShift.

## Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль специалиста по созданию переходов

СПЕЦИАЛИЗАЦИЯ: Это Pattern агент для проекта PatternShift. Работает с созданием связующих элементов, обеспечением coherence и flow в терапевтическом процессе.

## Как использовать агента

### Активация роли согласно D:\\Automation\\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
Ищу промпт роли Pattern Transition Craftsman...
Поиск через: Glob(**/*pattern*transition*knowledge*.md)
Читаю системный промпт роли...

ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN TRANSITION CRAFTSMAN

Моя экспертиза:
- Создание связующих элементов между модулями
- Обеспечение coherence и flow в терапевтическом процессе
- Создание мостов между разными активностями
- Сохранение эмоционального состояния и фокуса внимания
- Подготовка mind-set для следующего модуля
- Использование якорей из предыдущих модулей
- Работа с энергетическими переходами
- Управление сменой модальностей восприятия

Готов создавать переходы между модулями
```

### Запрос от пользователя:

```
Прими роль Pattern Transition Craftsman и создай переход между модулем техники и модулем упражнения.
```

### Пример работы с созданием перехода:

После принятия роли передайте Claude запрос:

```
Создай переход между модулями:
- От: Техника переоценки (завершена, пользователь понял механизм)
- К: Упражнение применения техники
- Энергия: neutral → activating
- Использовать achievement anchor
```

## Что делает агент

### Входные данные:
- Информация о модулях (from/to)
- Тип перехода (intro_to_main, day_to_day, etc.)
- Энергетический уровень (calm, neutral, activating, building, sustaining)
- Смена модальности (visual→auditory, etc.)
- Контекст программы и история модулей

### Выходные данные:
- **Module Transitions** - переходы между модулями с элементами и якорями
- **Bridge Content** - мосты между активностями
- **Coherence Checks** - проверка связности программы
- **Micro-interventions** - терапевтические микро-интервенции
- **Flow Analysis** - анализ общего потока программы

## Структура агента

```
pattern_transition_craftsman/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты создания переходов
├── dependencies.py             # Зависимости и базы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── models.py                   # Pydantic модели данных
├── knowledge/
│   └── pattern_transition_craftsman_knowledge.md  # База знаний
├── __init__.py                 # Экспорты
└── README.md                   # Документация
```

## Программное использование (Pydantic AI)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Быстрый старт

```python
from pattern_transition_craftsman import run_pattern_transition_craftsman

# Простой пример создания перехода
result = await run_pattern_transition_craftsman(
    "Создай переход от техники переоценки к упражнению применения",
    api_key="your_api_key"
)

print(result)
```

### Продвинутое использование

```python
from pattern_transition_craftsman.agent import agent
from pattern_transition_craftsman.dependencies import PatternTransitionCraftsmanDependencies
from pattern_transition_craftsman.tools import create_module_transition

# Создание зависимостей
deps = PatternTransitionCraftsmanDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift",
    program_id="program_123"
)

# Прямой вызов инструмента создания перехода
from pydantic_ai import RunContext
result = await create_module_transition(
    ctx=RunContext(deps=deps),
    from_module={
        "id": "mod_1",
        "name": "Техника переоценки",
        "type": "technique",
        "energy_level": "neutral"
    },
    to_module={
        "id": "mod_2",
        "name": "Упражнение применения",
        "type": "exercise"
    },
    transition_type="technique_to_exercise",
    energy_shift="activating",
    use_anchors=True
)

print(result)
```

## Доступные инструменты

### Основные инструменты создания переходов

- `create_module_transition()` - Создать переход между модулями
- `create_bridge_content()` - Создать мост между активностями
- `check_program_coherence()` - Проверить связность программы
- `generate_micro_intervention()` - Сгенерировать микро-интервенцию
- `analyze_program_flow()` - Проанализировать общий flow программы
- `search_agent_knowledge()` - Поиск в базе знаний

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## База знаний содержит:

- **Системный промпт** из PatternShift системы (TRANSITION CRAFTSMAN AGENT)
- **Flow Theory** - концепция потока (Csikszentmihalyi, 1990)
- **Gestalt Theory of Closure** - принцип завершенности (Wertheimer, 1923)
- **Cognitive Load Theory** - управление когнитивной нагрузкой (Sweller, 1988)
- **Zeigarnik Effect** - эффект незавершенного действия (1927)
- **Emotional Continuity Theory** - эмоциональная непрерывность (Isen, 1984)
- **Anchoring in NLP** - якорение (Bandler & Grinder, 1979)
- **Практические паттерны** - Summary, Anticipation, Reflection, Energy Shift, Modality Shift, Anchor bridges
- **Checklist эффективного перехода**
- **Частые ошибки и решения**

## Примеры использования

### Пример 1: Создание перехода между модулями

**Исходный запрос:**
```
Создай переход:
- От: Техника переоценки (завершена)
- К: Упражнение применения
- Энергия: neutral → activating
- Тип: technique_to_exercise
```

**Результат:**
```
Переход создан успешно

ID перехода: trans_a7f3b2c1
От: Техника переоценки → К: Упражнение применения
Тип: technique_to_exercise
Энергия: activating

Текст перехода:
Отлично! Теперь, когда вы освоили технику, давайте закрепим её на практике.
Это упражнение поможет вам применить переоценку к реальной ситуации...

Элементы (2):
- energizer: Сделайте глубокий вдох... и на выдохе почувствуйте готовность действовать...
- anchor: Помните, как легко получилась техника? Эта же лёгкость с вами сейчас.

Длительность: ~95 сек
```

### Пример 2: Создание моста между активностями

**Исходный запрос:**
```
Создай мост:
- От: Визуализация ресурсного состояния
- К: Практика применения в жизни
- Anchor: emotion
- Preserve emotion: true
```

**Результат:**
```
Мост создан

ID моста: bridge_9x2k4p
От: Визуализация → К: Практика применения

Текст моста:
Отлично! Теперь, основываясь на опыте Визуализация ресурсного состояния,
мы переходим к Практика применения в жизни.

Якорь: Помните то чувство лёгкости, когда получилась техника? Вызовите его снова.

Подготовка mind-set:
Приготовьтесь к новому опыту.

Сохраняет фокус: Да
Сохраняет эмоцию: Да
```

### Пример 3: Проверка связности программы

**Исходный запрос:**
```
Проверь coherence дня 5:
Модули:
1. Утренняя медитация (complexity: 3)
2. Техника работы с убеждениями (complexity: 7)
3. Упражнение на интеграцию (complexity: 5)
```

**Результат:**
```
Проверка связности завершена

ID проверки: check_f4d8a3
Программа: program_123
День: 5

Flow Score: 0.67 / 1.00

Проблемы связности (1):
- Резкий скачок сложности между Утренняя медитация и Техника работы с убеждениями

Эмоциональная непрерывность: Да

Рекомендации (1):
- Добавить промежуточный модуль или смягчить переход
```

### Пример 4: Генерация микро-интервенции

**Исходный запрос:**
```
Создай микро-интервенцию:
Тип: reframe
Контекст: Пользователь говорит что техника не получилась
```

**Результат:**
```
Микро-интервенция создана

Тип: reframe
Контекст: Пользователь говорит что техника не получилась

Текст интервенции:
Это не неудача, это ценная информация о том, как работает ваша психика.

Терапевтический эффект: Reframe
Длительность: ~20 секунд
```

## Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\\Automation\\Development\\projects\\patternshift\\docs\\content-agents-system-prompts.md` (раздел 11: TRANSITION CRAFTSMAN AGENT)
- `D:\\Automation\\Development\\projects\\patternshift\\docs\\final-kontent-architecture-complete.md`

## Важные принципы

- **Coherence first** - связность превыше всего
- **Flow preservation** - сохранение потока программы
- **Emotional continuity** - непрерывность эмоционального опыта
- **Anchor usage** - использование якорей для преемственности
- **Brevity** - краткость переходов (30-60 сек)
- **Clarity** - ясность цели и направления
- **Therapeutic effect** - каждый переход имеет терапевтический эффект
- **Mind-set preparation** - подготовка мышления для следующего модуля

## Загрузка в Archon Knowledge Base

После создания агента загрузите файл знаний:

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_transition_craftsman_knowledge.md`
4. Добавьте теги:
   - `pattern-transition-craftsman`
   - `flow-design`
   - `coherence`
   - `agent-knowledge`
   - `patternshift`
   - `bridges`
   - `emotional-continuity`

## Быстрый старт

1. Запросите роль: "Прими роль Pattern Transition Craftsman"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте запрос: "Создай переход между [модуль A] и [модуль B]"
4. Получите готовый переход с элементами, якорями и терапевтическим эффектом

---

*Pattern Transition Craftsman Agent - создание связующих элементов и обеспечение flow в системе PatternShift*
