# Psychology Content Orchestrator Agent

Агент-оркестратор для координации полного пайплайна создания психологических тестов и программ трансформации. Управляет всеми специализированными агентами в экосистеме психологического контента.

## Описание

Psychology Content Orchestrator Agent является центральным координатором проектов создания психологических тестов. Он управляет сложными workflow, координирует работу специализированных агентов и обеспечивает высокое качество итоговых продуктов.

### 🎯 Ключевые возможности

- **Полная оркестрация** всего пайплайна создания психологических тестов
- **Координация агентов** с умной системой делегирования задач
- **Управление качеством** через многоуровневые качественные гейты
- **Мониторинг прогресса** и детальная отчетность
- **Гибкие workflow** от простых до экспертных конфигураций

## Команда агентов

Оркестратор координирует работу следующих специализированных агентов:

### 🔍 Psychology Research Agent
- Глубокое исследование психологических тем
- Анализ клинических шкал и референсов
- Изучение целевых аудиторий и культурных особенностей

### 🏗️ Psychology Content Architect
- Создание тестов по методологии PatternShift
- 4-уровневая система: Research → Draft → Analysis → Finalization
- VAK и возрастные адаптации

### ⚙️ Psychology Test Generator
- Генерация конкретных экземпляров тестов
- Адаптация под различные сценарии использования
- Создание множественных вариантов

### 🛡️ Psychology Quality Guardian
- Валидация соответствия методологии PatternShift
- Проверка клинической точности
- Контроль качества всех deliverables

### 🎯 Psychology Transformation Planner
- Создание программ трансформации и интервенций
- Планирование поведенческих изменений
- Индивидуальные планы развития

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

3. Убедитесь в доступности Archon MCP Server для координации агентов.

## Использование

### Полная оркестрация проекта

```python
from psychology_content_orchestrator import create_complete_psychology_project

# Создание полного проекта психологических тестов
result = await create_complete_psychology_project(
    project_name="Stress Management Test Suite",
    project_description="Comprehensive stress assessment and management tools",
    test_topics=["stress", "burnout", "work_anxiety"],
    target_audience="working_professionals",
    complexity_level="advanced"
)

print(f"Проект создан: {result['project']['project_info']['name']}")
print(f"Агенты задействованы: {len(result['metadata']['agents_used'])}")
print(f"Deliverables: {result['project']['deliverables']}")
```

### Координация существующего проекта

```python
from psychology_content_orchestrator import coordinate_existing_project

# Координация работы с существующим проектом
coordination = await coordinate_existing_project(
    project_id="existing-project-123",
    coordination_type="quality_check",
    specific_agents=["psychology_quality_guardian", "psychology_content_architect"]
)

print(f"Координация завершена: {coordination['coordination_type']}")
print(f"Агенты: {coordination['agents_involved']}")
```

### Оркестрация контроля качества

```python
from psychology_content_orchestrator import quality_orchestration

# Комплексная проверка качества
quality_check = await quality_orchestration(
    test_data=my_test_data,
    quality_level="comprehensive"
)

print(f"Оценка качества: {quality_check['compliance_score']}")
print(f"Рекомендации: {quality_check['recommendations']}")
```

## Конфигурация

### Уровни сложности

| Уровень | Описание | Агенты | Качественные гейты |
|---------|----------|--------|-------------------|
| `simple` | Базовая оркестрация | 2 агента | Основные проверки |
| `standard` | Стандартный пайплайн | 4 агента | Расширенные проверки |
| `advanced` | Продвинутая координация | 5 агентов | Строгие гейты |
| `expert` | Экспертная оркестрация | 5+ агентов | Исчерпывающие проверки |

### Типы оркестрации

| Тип | Описание | Применение |
|-----|----------|------------|
| `full_pipeline` | Полный пайплайн | Новые проекты |
| `targeted` | Целевая координация | Конкретные задачи |
| `quality_focused` | Фокус на качество | Валидация и улучшение |

### Workflow режимы

| Режим | Описание | Преимущества |
|-------|----------|--------------|
| `sequential` | Последовательное выполнение | Надежность, простота |
| `parallel` | Параллельное выполнение | Скорость, эффективность |
| `conditional` | Условное выполнение | Гибкость, адаптивность |

## Качественные гейты

### PatternShift Compliance (порог: 0.85)
- ✅ 4-уровневая методология
- ✅ VAK адаптации
- ✅ Возрастные адаптации
- ✅ Минимум 15 вопросов

### Clinical Accuracy (порог: 0.90)
- ✅ Соответствие DSM-5/ICD-11
- ✅ Корректность клинических референсов
- ✅ Валидность симптоматики
- ✅ Этические стандарты

### VAK Adaptations (порог: 0.80)
- ✅ Визуальные адаптации
- ✅ Аудиальные адаптации
- ✅ Кинестетические адаптации

### Language Quality (порог: 0.85)
- ✅ Качество целевого языка
- ✅ Культурная адаптация
- ✅ Разговорный стиль
- ✅ Эмоциональная поддержка

## Архитектура

```
psychology_content_orchestrator/
├── agent.py              # Основной агент-оркестратор
├── dependencies.py       # Конфигурация агентов и workflow
├── tools.py             # Инструменты оркестрации и координации
├── prompts.py           # Системные промпты для оркестрации
├── settings.py          # Настройки и конфигурации
├── requirements.txt     # Зависимости Python
├── .env.example        # Пример переменных окружения
└── README.md           # Документация
```

## Инструменты оркестрации

### Основные инструменты
- `orchestrate_test_creation()` - Полная оркестрация создания тестов
- `coordinate_agent_workflow()` - Координация workflow агентов
- `manage_test_lifecycle()` - Управление жизненным циклом тестов
- `validate_final_output()` - Финальная валидация проекта
- `track_project_progress()` - Отслеживание прогресса
- `delegate_to_specialist()` - Делегирование специализированным агентам

### Workflow паттерны
- **Sequential**: Последовательное выполнение агентов
- **Parallel**: Параллельная координация совместимых агентов
- **Conditional**: Условное выполнение на основе результатов

## Мониторинг и отчетность

### Отслеживание прогресса
- Статус выполнения задач по агентам
- Метрики качества на каждом этапе
- Время выполнения и эффективность
- Выявление блокеров и проблем

### Типы отчетов
- `per_task`: Отчет по каждой задаче
- `per_stage`: Отчет по этапам
- `final_only`: Только финальный отчет

### Логирование
- Детальное логирование всех операций
- Трекинг межагентного взаимодействия
- Анализ производительности
- Архив решений и их обоснований

## Интеграция с Archon

Полная интеграция с Archon Project Management System:

- **Проект ID**: `c75ef8e3-6f4d-4da2-9e81-8d38d04a341a` (AI Agent Factory)
- **Создание задач** для каждого агента
- **Отслеживание статуса** выполнения
- **RAG поиск** знаний для агентов
- **Координация зависимостей** между задачами

## Примеры конфигураций

### Простой проект (2 агента)
```python
SIMPLE_CONFIG = {
    "complexity_level": "simple",
    "orchestration_level": "targeted",
    "agents": ["content_architect", "quality_guardian"],
    "parallel_execution": False
}
```

### Стандартный проект (4 агента)
```python
STANDARD_CONFIG = {
    "complexity_level": "standard",
    "orchestration_level": "full_pipeline",
    "agents": ["content_architect", "test_generator", "quality_guardian", "transformation_planner"],
    "parallel_execution": True
}
```

### Экспертный проект (5+ агентов)
```python
EXPERT_CONFIG = {
    "complexity_level": "expert",
    "orchestration_level": "full_pipeline",
    "agents": ["research_agent", "content_architect", "test_generator", "quality_guardian", "transformation_planner"],
    "parallel_execution": True,
    "quality_thresholds": {"patternshift": 0.95, "clinical": 0.98}
}
```

## Лучшие практики

### Планирование проекта
1. **Определите сложность** на основе требований
2. **Выберите подходящих агентов** для задач
3. **Настройте качественные гейты** согласно стандартам
4. **Планируйте зависимости** между этапами

### Координация агентов
1. **Используйте параллельное выполнение** для независимых задач
2. **Контролируйте качество** на каждом этапе
3. **Документируйте решения** и их обоснования
4. **Мониторьте прогресс** в реальном времени

### Управление качеством
1. **Не пропускайте гейты качества** ради скорости
2. **Валидируйте результаты** перед передачей следующему агенту
3. **Требуйте исправления недостатков** перед продолжением
4. **Ведите архив проверок** для аудита

## Поддержка

Для вопросов и предложений используйте:
- Archon Project Management System
- Проект: AI Agent Factory
- ID: c75ef8e3-6f4d-4da2-9e81-8d38d04a341a

## Лицензия

Создан в рамках проекта AI Agent Factory и следует принципам открытой разработки.