# Pattern VAK Adaptation Specialist Agent

Полноценный Pydantic AI агент для создания VAK адаптированного психологического контента в рамках системы PatternShift.

## 🎯 Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль специалиста по VAK адаптации

⚠️ **СПЕЦИАЛИЗАЦИЯ:** Это Pattern агент для проекта PatternShift, НЕ универсальный агент. Работает с модулями психологических программ трансформации.

## 🧠 Как использовать агента

### Активация роли согласно D:\Automation\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
🔍 Ищу промпт роли Pattern VAK Adaptation Specialist...
📁 Поиск через: Glob(**/*pattern*vak*knowledge*.md)
📖 Читаю системный промпт роли...

🎭 ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN VAK ADAPTATION SPECIALIST

Моя экспертиза:
- Сенсорные репрезентативные системы VAK
- Адаптация контента под Visual/Auditory/Kinesthetic модальности
- Работа с модульной архитектурой PatternShift

✅ Готов создавать VAK-адаптированные модули PatternShift
```

### Запрос от пользователя:

```
Прими роль Pattern VAK Adaptation Specialist и создай VAK версии модуля.
```

### Шаг 3: Работа с модулями PatternShift

После принятия роли передайте Claude базовый модуль и попросите создать VAK адаптации:

```
Вот базовый модуль PatternShift:

Название: "Техника якорения"
Тип: technique
Длительность: 15 минут
Контент: [ваш контент]

Создай три VAK версии этого модуля.
```

## 📋 Что делает агент

### Входные данные:
- Базовый модуль PatternShift любого типа (technique, meditation, exercise, hypnosis)
- Контекстная информация о целевой аудитории

### Выходные данные:
- **Visual версия** - с яркими образами и визуализациями
- **Auditory версия** - с звуковыми метафорами и ритмом
- **Kinesthetic версия** - с телесными ощущениями и движениями

## 🔧 Структура агента

```
pattern_vak_adaptation_specialist/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты VAK адаптации
├── dependencies.py             # Зависимости и типы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── validators.py               # Валидаторы безопасности
├── knowledge/
│   └── pattern_vak_adaptation_specialist_knowledge.md  # База знаний
├── examples/                   # Примеры конфигураций
├── tests/                      # Модульные тесты
└── README.md                   # Документация
```

## 🚀 Программное использование (Pydantic AI)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Быстрый старт

```python
from pattern_vak_adaptation_specialist import run_pattern_vak_adaptation_specialist

# Простой пример адаптации
result = await run_pattern_vak_adaptation_specialist(
    "Создай VAK версии медитации осознанного дыхания"
)

print(result.adapted_content)
```

### Продвинутое использование

```python
from pattern_vak_adaptation_specialist.agent import (
    VAKAdaptationRequest,
    vak_adaptation_agent
)
from pattern_vak_adaptation_specialist.dependencies import (
    PatternVAKAdaptationDependencies,
    VAKModalityType,
    AdaptationDepth
)

# Создание зависимостей
deps = PatternVAKAdaptationDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift"
)

# Создание детального запроса
request = VAKAdaptationRequest(
    content="Ваш психологический контент...",
    target_modality=VAKModalityType.VISUAL,
    adaptation_depth=AdaptationDepth.DEEP,
    create_multimodal=True,
    preserve_therapeutic_goals=True
)

# Выполнение адаптации
result = await vak_adaptation_agent.run(
    f"Обработай VAK адаптацию: {request.model_dump_json()}",
    deps=deps
)
```

## 🛠️ Доступные инструменты

### Основные инструменты

- `analyze_content_vak_modalities()` - Анализ контента на VAK модальности
- `adapt_content_to_vak_modality()` - Адаптация под целевую модальность
- `create_multimodal_variant()` - Создание мультимодального варианта
- `validate_adaptation_safety()` - Валидация безопасности
- `generate_vak_metrics()` - Генерация метрик эффективности

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## 📚 База знаний содержит:

- **Системный промпт** из PatternShift системы
- **Конкретные инструкции** работы с модулями
- **Алгоритм создания** VAK адаптаций
- **Практические примеры** адаптации техник и медитаций
- **Ссылки на контекстные файлы** PatternShift

## 🎨 Примеры использования

### Пример 1: НЛП техника

**Исходный модуль:**
```
Сядьте удобно. Вспомните момент максимальной уверенности.
Сожмите кулак, создавая связь между жестом и состоянием.
```

**Visual адаптация:**
```
Увидьте яркую картину своего триумфа.
Сфокусируйтесь на образе и сожмите кулак, создавая визуальную связь.
```

**Auditory адаптация:**
```
Услышьте внутренний голос уверенности.
Сожмите кулак в ритм этого голоса, создавая звуковую связь.
```

**Kinesthetic адаптация:**
```
Почувствуйте телесные ощущения уверенности.
Сожмите кулак, ощущая связь с внутренней силой.
```

## 🔗 Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\Automation\Development\projects\patternshift\docs\content-agents-system-prompts.md`
- `D:\Automation\Development\projects\patternshift\docs\final-kontent-architecture-complete.md`

## ⚠️ Важные принципы

- **Сохранение терапевтической сути** - эффект остается тем же
- **Адаптация только формы подачи** - структура техники не меняется
- **Культурная приемлемость** - без травмирующего контента
- **Безопасность применения** - особенно для уязвимых групп

## 🚀 Быстрый старт

1. Запросите роль: "Прими роль Pattern VAK Adaptation Specialist"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте модуль: "Создай VAK версии этого модуля: [контент]"
4. Получите три адаптированные версии

---

*Pattern VAK Adaptation Specialist Agent - создание персонализированного психологического контента через сенсорные модальности*