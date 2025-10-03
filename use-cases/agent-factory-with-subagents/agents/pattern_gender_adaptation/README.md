# Pattern Gender Adaptation Agent

Специализированный агент для адаптации психологического контента под гендерно-специфичные особенности восприятия в проекте PatternShift.

## Описание

Pattern Gender Adaptation Agent - это эксперт по гендерной психологии и социальной адаптации контента. Агент адаптирует психологические техники и программы трансформации под маскулинные, фемининные и небинарные паттерны восприятия, мотивации и коммуникации.

## Ключевые возможности

- ✅ Адаптация контента для маскулинной аудитории
- ✅ Адаптация контента для фемининной аудитории
- ✅ Создание инклюзивных нейтральных версий
- ✅ Избегание токсичных гендерных стереотипов
- ✅ Учет современных исследований гендерной психологии
- ✅ Интеграция с системой PatternShift

## Экспертиза агента

### Гендерные паттерны

**Маскулинные:**
- Ориентация на решение и достижение
- Предпочтение конкретных действий
- Метафоры конкуренции и преодоления

**Фемининные:**
- Ориентация на отношения и эмоции
- Предпочтение процессного подхода
- Метафоры роста и гармонии

**Небинарные:**
- Индивидуальный баланс качеств
- Гибкость в коммуникации
- Избегание жестких рамок

### Примеры адаптации

**Аффирмация "Я достоин любви":**

- *Маскулинная:* "Я заслужил уважение и признание"
- *Фемининная:* "Я открыта для любви и заботы"
- *Нейтральная:* "Я ценю себя и принимаю любовь"

## Структура агента

Полноценный Pydantic AI агент с универсальными декораторами и специализированными инструментами:

```
pattern_gender_adaptation_agent/
├── agent.py              # Основной агент с интеграциями
├── tools.py              # Специализированные инструменты
├── dependencies.py       # Зависимости + PatternToUniversalBridge
├── prompts.py            # Системные промпты
├── settings.py           # Конфигурация агента
├── workflow.py           # PatternShift workflow (Step 4.1)
├── knowledge/
│   └── pattern_gender_adaptation_agent_knowledge.md
├── __init__.py           # Экспорты пакета
└── README.md
```

## Использование

### Прямой запуск агента

```python
from pattern_gender_adaptation_agent import (
    run_pattern_gender_agent,
    PatternGenderAdaptationDependencies
)

# Настройка зависимостей
deps = PatternGenderAdaptationDependencies(
    llm_api_key="your_api_key",
    project_path="D:\\Automation\\Development\\projects\\PatternShift"
)

# Запуск агента с автоматическими интеграциями
result = await run_pattern_gender_agent(
    user_message="Адаптируй модуль под гендерные версии",
    deps=deps
)
```

### Workflow для пакетной обработки

```python
from pattern_gender_adaptation_agent import run_gender_adaptation_workflow

# Обработка модулей
modules = [
    {"module_id": "nlp_001", "content": {...}, "module_type": "nlp_technique"},
    {"module_id": "hyp_001", "content": {...}, "module_type": "hypnosis_script"}
]

result = await run_gender_adaptation_workflow(
    modules=modules,
    module_type="nlp_technique",
    deps=deps
)

# Результат:
# {
#   "success": True,
#   "adapted_modules": [...],  # 3 версии каждого модуля
#   "output_path": "adapted_modules/gender/",
#   "stats": {
#     "input_modules_processed": 2,
#     "output_modules_created": 6,
#     "multiplication_factor": 3
#   }
# }
```

### Специализированные инструменты

Агент имеет 5 основных инструментов:

```python
# 1. Анализ гендерных паттернов
analyze_gender_patterns(module_content: Dict) -> GenderAnalysisResult

# 2. Адаптация для маскулинной аудитории
adapt_for_masculine(module_content: Dict, module_id: str) -> AdaptedModule

# 3. Адаптация для фемининной аудитории
adapt_for_feminine(module_content: Dict, module_id: str) -> AdaptedModule

# 4. Создание нейтральной версии
create_neutral_version(module_content: Dict, module_id: str) -> AdaptedModule

# 5. Валидация на стереотипы
validate_stereotypes(adapted_module_json: str) -> ValidationResult
```

### Универсальные интеграции

Агент использует полные интеграции из agent-factory:

```python
from agents.common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations
)

# Автоматически применяются:
# - PM Switch - переключение к Project Manager
# - Competency Check - проверка компетенций и делегирование
# - Microtask Planning - планирование микрозадач
# - Git Commits - автоматические коммиты
# - Russian Localization - русская локализация
# - RAG Search - поиск в базе знаний через search_agent_knowledge()
# - Collective Tools - break_down_to_microtasks, reflect_and_improve и т.д.
```

## Интеграция с PatternShift

### Workflow Position

**Шаг 4.1 (Дни 25-28): Гендерная адаптация**

- **Входные данные:** ВСЕ базовые модули после Фазы 2 (НЛП, гипноз, упражнения, и т.д.)
- **Выходные данные:** 3 версии каждого модуля (masculine, feminine, neutral)
- **Следующий агент:** Pattern Age Adaptation Agent (Шаг 4.2)

### Связи с другими агентами

**Pattern агенты (создание контента):**
- **Pattern Integration Synthesizer** → создает базовые модули
- **Pattern Gender Adaptation** → адаптирует под гендер (текущий)
- **Pattern Age Adaptation** → адаптирует под возраст
- **Pattern VAK Adaptation** → адаптирует под сенсорные каналы
- **Pattern Cultural Adaptation** → полирует под культуру
- **Pattern Orchestrator** → компилирует ENGINE_SPEC.json

**Universal агенты (создание движка):**
- **Blueprint Architect** → проектирует архитектуру движка
- **Implementation Engineer** → реализует алгоритмы маршрутизации
- **API Development Agent** → создает API endpoints
- **Typescript Architecture Agent** → типизация движка
- **Prisma Database Agent** → схемы БД для модулей
- **Queue Worker Agent** → фоновая обработка
- **Quality Guardian** → тестирование движка

### PatternToUniversalBridge

Агент включает архитектурную документацию взаимодействия:

```python
from pattern_gender_adaptation_agent import PatternToUniversalBridge

# Получить workflow создания движка
workflow = PatternToUniversalBridge.get_engine_workflow()

# Фаза 1: Pattern агенты создают контент
# Фаза 2: Pattern Orchestrator компилирует спецификацию
# Фаза 3: Blueprint Architect проектирует движок
# Фаза 4: Universal агенты реализуют движок
# Фаза 5: Quality Guardian валидирует
```

### Архитектура

- **Тип:** Pattern агент (UPGRADE версия Pydantic AI агента)
- **Фреймворк:** Pydantic AI + Universal Decorators
- **Специализация:** Гендерная адаптация психологического контента
- **База знаний:** `knowledge/pattern_gender_adaptation_agent_knowledge.md`
- **НЕ публикуется в git** (локальная разработка PatternShift)
- **НЕ универсальный** (проект-специфичный)

## Принципы работы

1. **Не абсолютизировать** - гендер как тенденция, не закон
2. **Учитывать контекст** - культура и возраст важнее
3. **Давать выбор** - пользователь выбирает стиль
4. **Избегать стереотипов** - постоянная проверка
5. **Быть инклюзивным** - весь спектр идентичности

## Источники знаний

- Gilligan, C. "In a Different Voice"
- Tannen, D. "You Just Don't Understand"
- Baron-Cohen, S. "The Essential Difference"
- APA Guidelines (2018)
- Gender-sensitive therapy research

## Статус разработки

- ✅ База знаний создана
- ✅ Pydantic AI реализация с универсальными декораторами
- ✅ Интеграция с PatternShift workflow (Step 4.1)
- ✅ PatternToUniversalBridge архитектура
- ✅ Специализированные инструменты (5 tools)
- ✅ Workflow для пакетной обработки
- ⏳ Тестирование (в планах)

## Примечания

Этот агент является частью экосистемы 18 специализированных Pattern агентов проекта PatternShift и работает под управлением Pattern Orchestrator Agent.

Все адаптации выполняются с учетом современных исследований гендерной психологии и принципов инклюзивности.
