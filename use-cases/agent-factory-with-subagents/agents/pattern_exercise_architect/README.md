# Pattern Exercise Architect Agent

Специализированный Pydantic AI агент для создания трансформационных упражнений в рамках системы PatternShift.

## 🎯 Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль создателя трансформационных упражнений

⚠️ **СПЕЦИАЛИЗАЦИЯ:** Это Pattern агент для проекта PatternShift, НЕ универсальный агент. Работает с трансформационными упражнениями и воплощённым обучением.

## 🧠 Как использовать агента

### Активация роли согласно D:\\Automation\\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
🔍 Ищу промпт роли Pattern Exercise Architect...
📁 Поиск через: Glob(**/*pattern*exercise*knowledge*.md)
📖 Читаю системный промпт роли...

🎭 ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN EXERCISE ARCHITECT

Моя экспертиза:
- Embodied cognition (воплощённое познание)
- Experiential learning cycles (Колба, Honey-Mumford)
- Multi-sensory integration (VAK + emotional + social channels)
- NLP techniques applied to exercise design
- Progressive complexity design
- Self-check mechanisms

✅ Готов создавать трансформационные упражнения
```

### Запрос от пользователя:

```
Прими роль Pattern Exercise Architect и создай упражнение для интеграции техники рефрейминга.
```

### Пример работы с упражнением:

После принятия роли передайте Claude запрос на создание упражнения:

```
Создай трансформационное упражнение на основе НЛП техники "рефрейминг".
Целевая аудитория: взрослые 30-50 лет
Длительность: 15 минут
Основной канал: cognitive + emotional
```

## 📋 Что делает агент

### Входные данные:
- Цель трансформации (что пользователь хочет изменить)
- НЛП техника для интеграции (опционально)
- Целевой уровень сложности (beginner/intermediate/advanced/expert)
- Длительность упражнения
- Основной канал научения (cognitive/emotional/somatic/social)
- Контекст выполнения (home/work/public)

### Выходные данные:
- **Трансформационное упражнение** - с пошаговыми инструкциями
- **Критерии выполнения** - наблюдаемые признаки и самопроверка
- **Варианты упражнения** - адаптации под VAK/возраст/сложность
- **Интеграция в жизнь** - как применить изменения в реальности
- **Механизм самопроверки** - как пользователь поймёт что выполнил правильно

## 🔧 Структура агента

```
pattern_exercise_architect/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты дизайна упражнений
├── dependencies.py             # Зависимости и типы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── models.py                   # Pydantic модели данных
├── knowledge/
│   └── pattern_exercise_architect_knowledge.md  # База знаний
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
from pattern_exercise_architect import run_pattern_exercise_architect

# Простой пример создания упражнения
result = await run_pattern_exercise_architect(
    "Создай упражнение для интеграции техники рефрейминга",
    api_key="your_api_key"
)

print(result)
```

### Продвинутое использование

```python
from pattern_exercise_architect.agent import agent
from pattern_exercise_architect.dependencies import PatternExerciseArchitectDependencies
from pattern_exercise_architect.tools import design_transformational_exercise

# Создание зависимостей
deps = PatternExerciseArchitectDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift"
)

# Прямой вызов инструмента дизайна упражнения
from pydantic_ai import RunContext
result = await design_transformational_exercise(
    ctx=RunContext(deps=deps),
    goal_description="Научиться видеть ситуации с разных сторон",
    nlp_technique="рефрейминг",
    target_difficulty="intermediate",
    duration_minutes=15,
    primary_channel="cognitive",
    context="home"
)

print(result)
```

## 🛠️ Доступные инструменты

### Основные инструменты дизайна упражнений

- `design_transformational_exercise()` - Создание трансформационного упражнения
- `create_exercise_variants()` - Создание вариантов под VAK/age/difficulty
- `design_self_check_criteria()` - Разработка критериев самопроверки
- `adapt_nlp_technique_to_exercise()` - Адаптация НЛП техники в формат упражнения
- `search_agent_knowledge()` - Поиск best practices в базе знаний

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## 📚 База знаний содержит:

- **Системный промпт** из PatternShift системы (EXERCISE ARCHITECT AGENT)
- **Embodied Cognition** - воплощённое познание (теория)
- **Experiential Learning** - цикл Колба
- **Multi-Channel Learning** - cognitive, emotional, somatic, social
- **Self-Directed Learning** - принципы андрагогики (Knowles)
- **Типы упражнений** - NLP Integration, Embodiment, Integration, Reflection
- **Принципы дизайна** - Progressive complexity, Multi-channel engagement, Self-check
- **Примеры упражнений** с полной структурой и критериями
- **Ссылки на контекстные файлы** PatternShift

## 🎨 Примеры использования

### Пример 1: Упражнение на рефрейминг

**Исходный запрос:**
```
Создай упражнение для интеграции техники рефрейминга контекста.
Длительность: 15 минут
Сложность: intermediate
```

**Результат:**
- ✅ Упражнение "Рефрейминг контекста" создано
- ✅ 3 шага: Выбор ситуации → Применение техники → Интеграция
- ✅ Критерии: ≥3 альтернативных интерпретации, улучшение эмоционального состояния
- ✅ Механизм самопроверки через вопросы
- ✅ Якорение для закрепления

### Пример 2: Embodiment упражнение

**Исходный запрос:**
```
Создай embodiment упражнение для калибровки эмоций через тело.
Длительность: 20 минут
Основной канал: somatic
```

**Результат:**
```
1. Body Scan (5 мин) → осознанность тела
2. Эмоциональные якоря (10 мин) → телесные маркеры эмоций
3. Практическое применение (5 мин) → распознавание в реальной ситуации

Критерии:
- Идентифицированы телесные маркеры ≥3 эмоций
- Распознана эмоция через тело
- Готовность применять в жизни
```

### Пример 3: VAK адаптация

**Исходный запрос:**
```
Создай варианты упражнения "Постановка намерения" для VAK типов
```

**Результат:**
- **Visual**: визуальная доска намерений, ментальные образы
- **Auditory**: вербализация намерения, аффирмации вслух
- **Kinesthetic**: написание от руки, физическое действие-символ

## 🔗 Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\\Automation\\Development\\projects\\patternshift\\docs\\content-agents-system-prompts.md` (раздел 7: EXERCISE ARCHITECT AGENT)
- `D:\\Automation\\Development\\projects\\patternshift\\docs\\final-kontent-architecture-complete.md`

## ⚠️ Важные принципы

- **Embodiment** - каждое упражнение задействует тело, не только ум
- **Multi-channel** - задействование cognitive + emotional + somatic + social
- **Progressive complexity** - от простого (Days 1-7) к сложному (Days 15-21+)
- **Self-check** - механизмы самопроверки критичны для автономности
- **Integration** - упражнения должны переносить изменения в жизнь
- **Experiential** - обучение через опыт, не через теорию

## 📚 Загрузка в Archon Knowledge Base

После создания агента загрузите файл знаний:

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_exercise_architect_knowledge.md`
4. Добавьте теги:
   - `pattern-exercise`
   - `transformational-exercises`
   - `nlp-techniques`
   - `embodiment`
   - `agent-knowledge`
   - `patternshift`

## 🚀 Быстрый старт

1. Запросите роль: "Прими роль Pattern Exercise Architect"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте запрос: "Создай упражнение для [цель]"
4. Получите спроектированное трансформационное упражнение с критериями выполнения

---

*Pattern Exercise Architect Agent - создание трансформационных упражнений с научной основой для системы PatternShift*
