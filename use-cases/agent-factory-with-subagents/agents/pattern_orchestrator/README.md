# Pattern Orchestrator Agent

Системный архитектор и главный координатор всех 17 специализированных Pattern агентов в проекте PatternShift. Мастер-агент, управляющий полным жизненным циклом создания персонализированного психологического контента, компилирующий ENGINE_SPEC.json и делегирующий Universal агентам создание движка маршрутизации.

## Описание

Pattern Orchestrator Agent - это вершина экосистемы PatternShift. Он координирует работу 17 Pattern агентов, управляет созданием 20,700+ персонализированных модулей, компилирует спецификацию движка маршрутизации и делегирует Universal агентам техническую реализацию.

## Структура агента

Полноценный Pydantic AI агент с универсальными декораторами и специализированными инструментами оркестрации:

```
pattern_orchestrator_agent/
├── agent.py              # Основной агент с интеграциями
├── tools.py              # 9 специализированных инструментов
├── dependencies.py       # Полная архитектура PatternShift
├── prompts.py            # Системные промпты координатора
├── settings.py           # Конфигурация 17 агентов + деградации
├── workflow.py           # Orchestration + Degradation workflows
├── knowledge/
│   └── pattern_orchestrator_agent_knowledge.md
├── __init__.py           # Экспорты пакета
└── README.md
```

## Ключевые обязанности

### 1. Координация 17 Pattern Агентов

**Phase 1: Content Creation (Days 1-14)** - 6 агентов
- NLP Technique Master → 100+ НЛП техник
- Ericksonian Hypnosis Scriptwriter → 50+ гипнотических скриптов
- Exercise Architect → 80+ практических упражнений
- Microhabit Designer → 70+ микропривычек
- Metaphor Weaver → 60+ терапевтических метафор
- Gamification Architect → игровые механики
- **Выход:** ~460 базовых модулей

**Phase 2: Integration & Polish (Days 15-21)** - 4 агента
- Integration Synthesizer → интегрированные программы
- Feedback Orchestrator → системы обратной связи
- Progress Narrator → нарративы прогресса
- Transition Craftsman → плавные переходы
- **Выход:** Интегрированные программы

**Phase 3: Safety & Science (Days 22-24)** - 2 агента
- Safety Protocol → валидация безопасности
- Scientific Validator → научная обоснованность
- **Выход:** Валидированные модули

**Phase 4: Multiplier Adaptation (Days 25-35)** - 4 агента
- Gender Adaptation → ×3 (masculine, feminine, neutral)
- Age Adaptation → ×5 (5 возрастных групп)
- VAK Adaptation → ×3 (visual, audial, kinesthetic)
- Cultural Adaptation → культурная полировка
- **Выход:** 460 → 20,700 модулей (×45 multiplier)

**Phase 5: Final Assembly (Days 36-42+)** - 2 агента
- Test Architect → психографические тесты
- Pattern Orchestrator (текущий) → ENGINE_SPEC.json
- **Выход:** Движок маршрутизации + делегирование

### 2. Управление 5-уровневой системой деградации

**Level 1: Program (45 минут)**
- Полная программа трансформации
- Все модули: НЛП + Гипноз + Упражнения + Метафоры
- Глубокая проработка
- Контекст: Дома, спокойная обстановка

**Level 2: Phase (25 минут)**
- Ключевая фаза программы
- Основные модули: НЛП + Упражнение
- Фокус на практике
- Контекст: Дома или тихое место

**Level 3: Day (15 минут)**
- Дневная практика
- Одна мощная техника + микропривычка
- Практический фокус
- Контекст: Любое тихое место

**Level 4: Session (5 минут)**
- Быстрая сессия
- Экспресс-техника + микродействие
- Без подготовки
- Контекст: Где угодно

**Level 5: Emergency (1 минута)**
- Экстренная помощь
- Мгновенная техника БЕЗ подготовки
- Немедленный эффект
- Контекст: Любая экстренная ситуация

### 3. Психографическая маршрутизация

**4 измерения персонализации:**
- **Gender:** masculine | feminine | neutral
- **Age:** teens | young_adults | early_middle | middle | seniors
- **VAK:** visual | audial | kinesthetic
- **Culture:** individualistic | collectivistic | balanced

**Алгоритм:**
1. Психографическое тестирование (Test Architect)
2. Определение профиля пользователя
3. Подбор модулей из 20,700
4. Построение 5-уровневой программы
5. Адаптивная доставка

### 4. Делегирование Universal Агентам

**Для создания движка маршрутизации:**

1. **Blueprint Architect** → проектирует архитектуру движка
2. **Implementation Engineer** → реализует алгоритмы маршрутизации
3. **API Development Agent** → создает REST/GraphQL API
4. **Typescript Architecture Agent** → типизация движка
5. **Prisma Database Agent** → схемы БД для 20,700 модулей
6. **Queue Worker Agent** → фоновая обработка
7. **Quality Guardian** → тестирование движка

## Использование

### Прямой запуск агента

```python
from pattern_orchestrator_agent import (
    run_pattern_orchestrator_agent,
    PatternOrchestratorDependencies
)

# Настройка зависимостей
deps = PatternOrchestratorDependencies(
    llm_api_key="your_api_key",
    project_path="D:\\Automation\\Development\\projects\\PatternShift"
)

# Запуск с автоматическими интеграциями
result = await run_pattern_orchestrator_agent(
    user_message="Координируй Phase 4: Multiplier Adaptation",
    deps=deps
)
```

### Полный Orchestration Workflow

```python
from pattern_orchestrator_agent import run_full_orchestration_workflow

# Выполнить все 5 фаз PatternShift
result = await run_full_orchestration_workflow(deps=deps)

# Результат:
# {
#   "success": True,
#   "workflow_results": {
#     "phases_completed": [phase_1, phase_2, phase_3, phase_4, phase_5],
#     "total_duration_days": 42,
#     "final_output": {engine_creation_plan}
#   },
#   "engine_spec_path": "D:/Automation/.../ENGINE_SPEC.json",
#   "stats": {
#     "total_modules_created": 20700,
#     "pattern_agents_count": 17,
#     "universal_agents_count": 7
#   }
# }
```

### Деградация контента

```python
from pattern_orchestrator_agent import apply_content_degradation

# Деградировать программу с 45 мин до 1 мин
program_content = {
    "module_id": "confidence_program",
    "duration": 45,
    "modules": {...}
}

result = await apply_content_degradation(
    program_content=program_content,
    target_level="emergency",  # 1 минута
    deps=deps
)

# Результат: контент деградирован program → phase → day → session → emergency
```

### Emergency Mode

```python
# Emergency техника на 60 секунд
from pattern_orchestrator_agent.tools import emergency_mode_handler

emergency = await emergency_mode_handler(
    ctx=ctx,
    user_state="panic_attack",
    available_time=60,
    context="before_presentation"
)

# Вернет:
# {
#   "technique": "Grounding 5-4-3-2-1",
#   "duration": 60,
#   "instructions": [
#     "5 вещей, которые видишь",
#     "4 вещи, которые слышишь",
#     "3 вещи, которые чувствуешь",
#     "2 вещи, которые обоняешь",
#     "1 вещь на вкус"
#   ],
#   "immediate_effect": "Возврат в настоящий момент"
# }
```

## Специализированные инструменты

Агент имеет 9 мощных инструментов оркестрации:

### 1. orchestrate_agents()
Координирует работу Pattern агентов для заданной фазы
```python
orchestrate_agents(phase="phase_4", task_description="Multiplier Adaptation")
```

### 2. manage_degradation_levels()
Управляет деградацией контента между уровнями
```python
manage_degradation_levels(
    source_level="program",
    target_level="emergency",
    module_content={...}
)
```

### 3. coordinate_workflow()
Синхронизирует весь workflow PatternShift
```python
coordinate_workflow(current_stage="phase_3_completed")
```

### 4. delegate_to_pattern_agent()
Делегирует задачу Pattern агенту
```python
delegate_to_pattern_agent(
    agent_type="pattern_gender_adaptation",
    task="Адаптировать модуль под гендер",
    context={...}
)
```

### 5. manage_module_pipeline()
Управляет конвейером создания модулей
```python
manage_module_pipeline(pipeline_stage="after_vak_adaptation")
```

### 6. validate_integration()
Валидирует интеграцию всех компонентов
```python
validate_integration(components=[...])
```

### 7. compile_engine_spec()
Компилирует ENGINE_SPEC.json
```python
compile_engine_spec(
    modules_library={...},
    psychographic_tests={...}
)
```

### 8. emergency_mode_handler()
Обрабатывает emergency режим (1 мин)
```python
emergency_mode_handler(
    user_state="acute_stress",
    available_time=60
)
```

### 9. delegate_to_universal_agents()
Делегирует Universal агентам
```python
delegate_to_universal_agents(
    agent_type="blueprint_architect",
    specification={...}
)
```

## ENGINE_SPEC.json структура

```json
{
  "version": "1.0.0",
  "total_modules": 20700,
  "psychographic_dimensions": {
    "gender": ["masculine", "feminine", "neutral"],
    "age": ["teens", "young_adults", "early_middle", "middle", "seniors"],
    "vak": ["visual", "audial", "kinesthetic"],
    "culture": ["individualistic", "collectivistic", "balanced"]
  },
  "degradation_levels": {
    "program": {"duration": "45min", "modules": "all"},
    "phase": {"duration": "25min", "modules": "key"},
    "day": {"duration": "15min", "modules": "daily"},
    "session": {"duration": "5min", "modules": "express"},
    "emergency": {"duration": "1min", "modules": "critical"}
  },
  "routing_algorithm": {
    "step_1": "psychographic_testing",
    "step_2": "profile_matching",
    "step_3": "module_selection",
    "step_4": "program_assembly_5_levels",
    "step_5": "adaptive_delivery"
  },
  "api_endpoints": {
    "get_user_profile": "/api/profile",
    "get_recommended_program": "/api/program/recommend",
    "get_module": "/api/module/:id",
    "get_degraded_version": "/api/module/:id/degrade/:level",
    "track_progress": "/api/progress",
    "adaptive_feedback": "/api/feedback",
    "emergency_help": "/api/emergency"
  },
  "ready_for_engine_creation": true
}
```

## Интеграция с PatternShift

### Статистика модулей:

- **Базовые модули:** 460 (Phase 3 output)
- **После Gender:** 1,380 (×3)
- **После Age:** 6,900 (×5)
- **После VAK:** 20,700 (×3)
- **Итого множитель:** ×45

### Workflow Position:

**Phase 5: Final Assembly (Days 36-42+)**

- Получает: 20,700 адаптированных модулей + психографические тесты
- Компилирует: ENGINE_SPEC.json
- Делегирует: Universal агентам для создания движка

### Связи с агентами:

**Входные данные:**
- От всех 17 Pattern агентов (Phase 1-4)
- От Pattern Test Architect (психографические тесты)

**Выходные данные:**
- ENGINE_SPEC.json для Universal агентов
- Делегирование 7 Universal агентам
- Production-ready движок маршрутизации

## Универсальные интеграции

Агент использует полные интеграции из agent-factory:

```python
from agents.common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations
)

# Автоматически применяются:
# - PM Switch
# - Competency Check
# - Microtask Planning
# - Git Commits
# - Russian Localization
# - RAG Search
# - Collective Tools
```

## Архитектура

- **Тип:** Pattern агент (MASTER orchestrator)
- **Фреймворк:** Pydantic AI + Universal Decorators
- **Специализация:** Координация 17 агентов + компиляция движка
- **База знаний:** `knowledge/pattern_orchestrator_agent_knowledge.md`
- **НЕ публикуется в git** (локальная разработка PatternShift)
- **НЕ универсальный** (проект-специфичный)

## Принципы работы

1. **Системное мышление** - видит всю экосистему 17 агентов
2. **Координация без микроменеджмента** - доверяет специализированным агентам
3. **Качество превыше скорости** - 20,700 модулей должны быть безупречны
4. **Адаптивность** - от 45 минут до 1 минуты под любой контекст
5. **Научная обоснованность** - evidence-based подход
6. **Безопасность** - травма-информированный подход
7. **Делегирование мастерство** - Pattern агенты для контента, Universal для движка

## Статус разработки

- ✅ База знаний создана
- ✅ Pydantic AI реализация с универсальными декораторами
- ✅ Интеграция с PatternShift workflow (Phase 5)
- ✅ PatternShiftArchitecture - полная архитектура 17 агентов
- ✅ DegradationSystemArchitecture - система деградации
- ✅ 9 специализированных инструментов оркестрации
- ✅ OrchestratorWorkflow - полный жизненный цикл
- ✅ DegradationWorkflow - управление деградацией
- ⏳ Тестирование (в планах)

## Примечания

Этот агент является **вершиной экосистемы** 18 специализированных Pattern агентов проекта PatternShift. Он координирует создание 20,700+ персонализированных психологических модулей и компилирует спецификацию для движка маршрутизации, который затем создается Universal агентами.

**Конечная цель:** Production-ready система PatternShift, способная доставлять персонализированный психологический контент адаптивно от 45 минут полной программы до 1 минуты экстренной помощи.
