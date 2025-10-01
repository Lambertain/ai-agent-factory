# Pattern Integration Synthesizer Agent

**Системный интегратор программ трансформации с холистическим видением всей программы.**

Pattern Integration Synthesizer Agent специализируется на оркестрации модулей контента в целостные программы трансформации для проекта PatternShift. Агент обеспечивает синергичное взаимодействие модулей, управляет эмоциональной кривой и предвидит точки сопротивления.

---

## 🎯 Основные возможности

### 1. Оркестрация модулей
- Применение паттернов оркестрации (Progressive Intensity, Technique Sandwich, Energy Wave, Spiral Deepening)
- Оптимальная последовательность модулей для максимальной синергии
- Распределение модулей по фазам программы

### 2. Управление эмоциональной кривой
- Управление 21-дневным циклом трансформации
- Учет 5 стадий: Excitement, Resistance, Breakthrough, Integration, Mastery
- Адаптация активностей под эмоциональное состояние пользователя

### 3. Предвидение точек сопротивления
- Идентификация критических точек dropout (дни 4-7, 10-12, 16-17)
- Встроенная поддержка и стратегии митигации
- Персонализация под профиль пользователя

### 4. Оптимизация нагрузки
- Управление когнитивной и эмоциональной нагрузкой
- Соблюдение лимитов интенсивности (Light, Medium, Intensive)
- Предотвращение burnout и dropout

### 5. Анализ целостности программы
- Проверка связности всех уровней: Program → Phase → Day → Session → Activity → Module
- Создание narrative arc через всю программу
- Оптимизация coherence и синергии

---

## 📦 Установка

### Требования
- Python 3.11+
- Pydantic AI 0.0.14+
- OpenAI API key (или другой LLM провайдер)

### Установка зависимостей

```bash
cd agents/pattern_integration_synthesizer
pip install -r requirements.txt
```

### Настройка окружения

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Отредактируйте `.env` и укажите свои настройки:
```env
LLM_API_KEY=your_actual_api_key_here
PATTERNSHIFT_PROJECT_PATH=/path/to/your/patternshift/project
```

---

## 🚀 Быстрый старт

### Базовое использование

```python
from pattern_integration_synthesizer import run_pattern_integration_synthesizer
import os

# Оркестровать модули для программы
result = await run_pattern_integration_synthesizer(
    user_message="Оркеструй модули для 21-дневной программы по работе с тревогой",
    api_key=os.getenv("LLM_API_KEY"),
    patternshift_project_path="/path/to/patternshift"
)

print(result)
```

### Анализ синергии программы

```python
from pattern_integration_synthesizer import analyze_program_synergy

program_structure = {
    "program_name": "Anxiety Management Program",
    "total_days": 21,
    "target_conditions": ["anxiety", "stress"],
    "phases": [...]
}

result = await analyze_program_synergy(
    program_structure=program_structure,
    api_key=os.getenv("LLM_API_KEY")
)

print(result)
```

### Оптимизация эмоциональной кривой

```python
from pattern_integration_synthesizer import optimize_emotional_curve

result = await optimize_emotional_curve(
    program_duration_days=21,
    target_conditions=["anxiety", "stress"],
    api_key=os.getenv("LLM_API_KEY"),
    program_intensity="medium"
)

print(result)
```

### Создание последовательности модулей

```python
from pattern_integration_synthesizer import create_module_sequence

result = await create_module_sequence(
    module_ids=["psychoeducation", "breathing", "cognitive_restructuring"],
    phase_type="beginning",
    target_goals=["build awareness", "reduce anxiety"],
    api_key=os.getenv("LLM_API_KEY")
)

print(result)
```

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
pytest tests/
```

### Запуск конкретных тестов

```bash
# Тесты инструментов
pytest tests/test_tools.py

# Тесты структуры агента
pytest tests/test_agent.py

# Валидация моделей
pytest tests/test_validation.py

# Интеграционные тесты
pytest tests/test_integration.py
```

### Тестирование с покрытием

```bash
pytest tests/ --cov=. --cov-report=html
```

---

## 🛠️ Инструменты агента

### 1. orchestrate_module_sequence
Оркестровать последовательность модулей используя паттерны оркестрации.

**Параметры:**
- `module_ids`: Список ID модулей
- `phase_type`: beginning | development | integration
- `target_goals`: Целевые цели программы

**Пример:**
```python
result = await orchestrate_module_sequence(
    ctx=context,
    module_ids=["mod_1", "mod_2", "mod_3"],
    phase_type="beginning",
    target_goals=["build awareness"]
)
```

### 2. manage_emotional_curve
Управлять эмоциональной кривой на протяжении программы.

**Параметры:**
- `program_duration_days`: Длительность программы в днях
- `program_intensity`: light | medium | intensive

**Пример:**
```python
result = await manage_emotional_curve(
    ctx=context,
    program_duration_days=21,
    program_intensity="medium"
)
```

### 3. identify_resistance_points
Предвидеть точки сопротивления и встроить поддержку.

**Параметры:**
- `program`: Структура программы
- `user_profile`: Профиль пользователя (опционально)

**Пример:**
```python
result = await identify_resistance_points(
    ctx=context,
    program=program_structure,
    user_profile={"previous_dropout": True}
)
```

### 4. ensure_module_synergy
Обеспечить синергию между модулями программы.

**Параметры:**
- `module_a_id`: ID первого модуля
- `module_b_id`: ID второго модуля
- `gap_days`: Промежуток в днях между модулями

**Пример:**
```python
result = await ensure_module_synergy(
    ctx=context,
    module_a_id="cognitive_restructuring",
    module_b_id="behavioral_activation",
    gap_days=1
)
```

### 5. analyze_program_coherence
Проанализировать целостность и связность программы.

**Параметры:**
- `program_structure`: Структура программы для анализа

**Пример:**
```python
result = await analyze_program_coherence(
    ctx=context,
    program_structure=program_structure
)
```

### 6. search_agent_knowledge
Поиск в специализированной базе знаний агента через Archon RAG.

**Параметры:**
- `query`: Поисковый запрос
- `match_count`: Количество результатов

**Пример:**
```python
result = await search_agent_knowledge(
    ctx=context,
    query="orchestration patterns",
    match_count=5
)
```

---

## 📊 Ключевые паттерны оркестрации

### Progressive Intensity (Постепенная интенсификация)
**Применение:** Beginning Phase, работа с травмами, чувствительные темы
**Последовательность:** light → medium → deep
**Обоснование:** предотвращение overwhelm, постепенная адаптация

### Technique Sandwich (Сэндвич техник)
**Применение:** NLP работа, гипноз, поведенческие изменения
**Последовательность:** technique → integration → technique → integration
**Обоснование:** время на закрепление изменений между техниками

### Energy Wave (Волнообразная энергия)
**Применение:** длительные программы, ежедневные сессии
**Последовательность:** high energy → rest → high energy → reflection
**Обоснование:** предотвращение выгорания, устойчивый momentum

### Spiral Deepening (Спиральное углубление)
**Применение:** сложные темы, развитие навыков, трансформация
**Последовательность:** intro → practice → return_deeper → practice → mastery
**Обоснование:** постепенное раскрытие сложности без overwhelm

---

## 📈 Эмоциональная кривая 21-дневной программы

### Days 1-3: EXCITEMENT (Энтузиазм)
- **Энергия:** HIGH | **Мотивация:** HIGH
- **Активности:** психообразование, легкие упражнения, мотивирующий контент
- **Избегать:** слишком интенсивная работа, сложные техники

### Days 4-7: RESISTANCE (Сопротивление)
- **Энергия:** MEDIUM | **Мотивация:** DECLINING
- **🚨 КРИТИЧЕСКАЯ ТОЧКА DROPOUT** - нужна активная поддержка
- **Активности:** поддерживающий контент, quick wins, напоминание о целях

### Days 8-12: BREAKTHROUGH (Прорыв)
- **Энергия:** VARIABLE | **Мотивация:** RENEWED
- **💡 Момент для более глубокой работы**
- **Активности:** углубленные техники, consolidation, celebrating progress

### Days 13-18: INTEGRATION (Интеграция)
- **Энергия:** STABLE | **Мотивация:** HIGH
- **Фокус:** перенос в реальную жизнь
- **Активности:** real-world application, habit formation, advanced techniques

### Days 19-21: MASTERY (Мастерство)
- **Энергия:** HIGH | **Мотивация:** INTRINSIC
- **Цель:** подготовка к самостоятельному продолжению
- **Активности:** consolidation, future planning, maintenance strategies

---

## 📂 Структура проекта

```
pattern_integration_synthesizer/
├── agent.py                    # Главный агент и функции запуска
├── dependencies.py             # Зависимости и базы знаний
├── settings.py                 # Настройки и конфигурация
├── models.py                   # Pydantic модели данных
├── tools.py                    # Инструменты агента
├── prompts.py                  # Системные промпты
├── __init__.py                 # Экспорты пакета
├── requirements.txt            # Python зависимости
├── .env.example                # Шаблон переменных окружения
├── README.md                   # Эта документация
├── knowledge/                  # База знаний агента
│   └── pattern_integration_synthesizer_knowledge.md
└── tests/                      # Тесты
    ├── conftest.py             # Pytest конфигурация
    ├── test_agent.py           # Тесты структуры агента
    ├── test_tools.py           # Тесты инструментов
    ├── test_validation.py      # Тесты Pydantic моделей
    └── test_integration.py     # Интеграционные тесты
```

---

## 🔗 Интеграция с Archon Knowledge Base

### Загрузка базы знаний в Archon

1. Откройте Archon: http://localhost:3737/
2. Перейдите в **Knowledge Base** → **Upload**
3. Загрузите файл: `knowledge/pattern_integration_synthesizer_knowledge.md`
4. Добавьте теги:
   - `pattern-integration-synthesizer`
   - `orchestration`
   - `synergy`
   - `agent-knowledge`
   - `patternshift`
5. Привяжите к проекту **AI Agent Factory** → вкладка **Sources**

### Использование RAG в коде

Агент автоматически использует Archon RAG через инструмент `search_agent_knowledge`:

```python
# Поиск в базе знаний
result = await search_agent_knowledge(
    ctx=context,
    query="emotional curve resistance points",
    match_count=5
)
```

---

## 🤝 Интеграция с PatternShift

Pattern Integration Synthesizer работает с архитектурой PatternShift:

```
Program → Phase → Day → Session → Activity → Module
```

### Ответственность агента:
- Оркестрация модулей в Activities
- Распределение Activities по Sessions
- Планирование Sessions в Days
- Группировка Days в Phases
- Связность всех уровней в единую Program

### Пример структуры программы:

```python
from pattern_integration_synthesizer import Program, Phase, Day, Session, Activity

program = Program(
    program_id="prog_anxiety_21day",
    program_name="Anxiety Management Program",
    total_days=21,
    target_conditions=["anxiety", "stress"],
    overall_goals=["reduce anxiety", "build coping skills"],
    phases=[
        Phase(
            phase_type=PhaseType.BEGINNING,
            phase_name="Foundation Building",
            duration_days=7,
            phase_goals=["build awareness", "psychoeducation"],
            days=[...]
        )
    ]
)
```

---

## 📚 Примеры использования

### Пример 1: Оркестрация 21-дневной программы

```python
import os
from pattern_integration_synthesizer import run_pattern_integration_synthesizer

async def orchestrate_anxiety_program():
    result = await run_pattern_integration_synthesizer(
        user_message="""
        Оркеструй 21-дневную программу по работе с тревогой:

        Модули для Beginning Phase (Days 1-7):
        - psychoeducation_anxiety
        - breathing_basics
        - thought_awareness

        Модули для Development Phase (Days 8-14):
        - cognitive_restructuring
        - behavioral_activation
        - exposure_gentle
        - self_compassion

        Модули для Integration Phase (Days 15-21):
        - real_world_exposure
        - habit_formation
        - relapse_prevention
        - maintenance_planning
        """,
        api_key=os.getenv("LLM_API_KEY"),
        patternshift_project_path="/path/to/patternshift"
    )

    print(result)
```

### Пример 2: Анализ точек сопротивления

```python
from pattern_integration_synthesizer import (
    run_pattern_integration_synthesizer,
    identify_resistance_points
)

async def analyze_resistance():
    program = {
        "program_name": "Anxiety Program",
        "total_days": 21,
        "phases": [...]
    }

    user_profile = {
        "previous_dropout": True,
        "low_motivation": False
    }

    result = await run_pattern_integration_synthesizer(
        user_message=f"""
        Проанализируй точки сопротивления для программы:
        {program}

        Профиль пользователя:
        {user_profile}

        Предложи конкретные стратегии митигации.
        """,
        api_key=os.getenv("LLM_API_KEY")
    )

    print(result)
```

### Пример 3: Проверка синергии модулей

```python
from pattern_integration_synthesizer import run_pattern_integration_synthesizer

async def check_synergy():
    result = await run_pattern_integration_synthesizer(
        user_message="""
        Проверь синергию между модулями:
        - cognitive_restructuring (Day 5)
        - behavioral_activation (Day 6)

        Промежуток: 1 день

        Является ли это оптимальной комбинацией?
        """,
        api_key=os.getenv("LLM_API_KEY")
    )

    print(result)
```

---

## 🔧 Конфигурация

### Настройки LLM

```python
# settings.py
llm_provider: str = "openai"
llm_model: str = "gpt-4o"
llm_base_url: str = "https://api.openai.com/v1"
```

### Настройки Archon

```python
archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
archon_api_url: str = "http://localhost:3737"
```

### Настройки Knowledge Base

```python
knowledge_tags: list = [
    "pattern-integration-synthesizer",
    "orchestration",
    "synergy",
    "agent-knowledge",
    "patternshift"
]
```

---

## 📖 Лицензия

Этот агент является частью проекта AI Agent Factory и предназначен для использования в проекте PatternShift.

---

## 🤝 Поддержка

Для вопросов и поддержки:
- Проект в Archon: **AI Agent Factory** (ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a)
- База знаний: `pattern_integration_synthesizer_knowledge.md`

---

**Pattern Integration Synthesizer Agent v1.0.0**
*Системный интегратор программ трансформации*
