# Pattern Age Adaptation Agent

Специализированный агент для адаптации психологического контента под возрастные особенности когнитивного, эмоционального и социального развития в проекте PatternShift.

## Описание

Pattern Age Adaptation Agent - это эксперт по возрастной психологии развития и адаптации контента. Агент создает возрастно-адаптированные версии психологических техник и программ трансформации с учетом задач развития по Эриксону, когнитивных способностей и жизненного опыта разных возрастных групп.

## Структура агента

Полноценный Pydantic AI агент с универсальными декораторами и специализированными инструментами:

```
pattern_age_adaptation_agent/
├── agent.py              # Основной агент с интеграциями
├── tools.py              # Специализированные инструменты
├── dependencies.py       # Зависимости + PatternAgeToUniversalBridge
├── prompts.py            # Системные промпты
├── settings.py           # Конфигурация агента
├── workflow.py           # PatternShift workflow (Step 4.2)
├── knowledge/
│   └── pattern_age_adaptation_agent_knowledge.md
├── __init__.py           # Экспорты пакета
└── README.md
```

## Возрастные группы

### 1. Teens (14-18 лет) - Подростки
**Задача развития:** Identity Formation (формирование идентичности)

- Язык: Энергичный, близкий к молодежному
- Примеры: Школа, друзья, социальные сети
- Метафоры: Открытие себя, квест, становление
- Формат: Короткие сессии (15-20 мин), геймификация

### 2. Young Adults (19-25 лет) - Молодые взрослые
**Задача развития:** Intimacy vs Isolation (близость vs изоляция)

- Язык: Современный, динамичный, профессиональный
- Примеры: Карьера, отношения, саморазвитие, путешествия
- Метафоры: Строительство фундамента, восхождение
- Формат: Практичность, быстрые результаты (25-30 мин)

### 3. Early Middle Age (26-35 лет) - Ранний средний возраст
**Задача развития:** Generativity Beginning (начало продуктивности)

- Язык: Деловой, четкий, теплый
- Примеры: Work-life balance, семья, карьерный рост
- Метафоры: Баланс, мастерство, создание наследия
- Формат: Системный подход, долгосрочные стратегии (30-35 мин)

### 4. Middle Age (36-50 лет) - Средний возраст
**Задача развития:** Generativity Peak (пик продуктивности)

- Язык: Зрелый, содержательный, глубокий
- Примеры: Наставничество, смысл жизни, переоценка ценностей
- Метафоры: Созревание, мудрость, передача опыта
- Формат: Глубинная работа, рефлексия (35-45 мин)

### 5. Seniors (50+ лет) - Старший возраст
**Задача развития:** Integrity vs Despair (целостность vs отчаяние)

- Язык: Уважительный, глубокий, мудрый
- Примеры: Жизненный опыт, наследие, принятие
- Метафоры: Осень жизни, мудрость, интеграция
- Формат: Созерцательный подход, связь с опытом (20-60 мин)

## Использование

### Прямой запуск агента

```python
from pattern_age_adaptation_agent import (
    run_pattern_age_agent,
    PatternAgeAdaptationDependencies
)

# Настройка зависимостей
deps = PatternAgeAdaptationDependencies(
    llm_api_key="your_api_key",
    project_path="D:\\Automation\\Development\\projects\\PatternShift"
)

# Запуск агента с автоматическими интеграциями
result = await run_pattern_age_agent(
    user_message="Адаптируй модуль под возрастные версии",
    deps=deps
)
```

### Workflow для пакетной обработки

```python
from pattern_age_adaptation_agent import run_age_adaptation_workflow

# Обработка гендерно-адаптированных модулей
gender_modules = [
    {
        "module_id": "nlp_001_masculine",
        "gender_version": "masculine",
        "content": {...},
        "module_type": "nlp_technique"
    },
    # ... еще 2 гендерные версии
]

result = await run_age_adaptation_workflow(
    modules=gender_modules,
    module_type="nlp_technique",
    deps=deps
)

# Результат:
# {
#   "success": True,
#   "adapted_modules": [...],  # 5 возрастных версий каждого
#   "output_path": "adapted_modules/age/",
#   "stats": {
#     "input_modules_processed": 3,
#     "output_modules_created": 15,
#     "multiplication_factor": 5
#   }
# }
```

### Специализированные инструменты

Агент имеет 7 основных инструментов:

```python
# 1. Анализ возрастных аспектов
analyze_age_patterns(module_content: Dict) -> AgeAnalysisResult

# 2. Адаптация для подростков (14-18)
adapt_for_teens(module_content: Dict, module_id: str) -> AgeAdaptedModule

# 3. Адаптация для молодых взрослых (19-25)
adapt_for_young_adults(module_content: Dict, module_id: str) -> AgeAdaptedModule

# 4. Адаптация для раннего среднего возраста (26-35)
adapt_for_early_middle_age(module_content: Dict, module_id: str) -> AgeAdaptedModule

# 5. Адаптация для среднего возраста (36-50)
adapt_for_middle_age(module_content: Dict, module_id: str) -> AgeAdaptedModule

# 6. Адаптация для старшего возраста (50+)
adapt_for_seniors(module_content: Dict, module_id: str) -> AgeAdaptedModule

# 7. Валидация соответствия задачам развития
validate_developmental_tasks(adapted_module_json: str) -> ValidationResult
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

**Шаг 4.2 (Дни 29-32): Возрастная адаптация**

- **Входные данные:** Гендерно-адаптированные модули от Pattern Gender Adaptation Agent (3 версии)
- **Выходные данные:** 5 возрастных версий каждого модуля (teens, young_adults, early_middle_age, middle_age, seniors)
- **Следующий агент:** Pattern VAK Adaptation Specialist (Шаг 4.3)
- **Умножение модулей:** 3 гендерных × 5 возрастных = 15 модулей на 1 базовый

### Связи с другими агентами

**Pattern агенты (создание контента):**
- **Pattern Gender Adaptation** → создает гендерные версии (предыдущий)
- **Pattern Age Adaptation** → создает возрастные версии (текущий)
- **Pattern VAK Adaptation** → адаптирует под сенсорные каналы (следующий)
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

### PatternAgeToUniversalBridge

Агент включает архитектурную документацию взаимодействия:

```python
from pattern_age_adaptation_agent import PatternAgeToUniversalBridge

# Получить позицию в workflow
position = PatternAgeToUniversalBridge.get_workflow_position()

# Получить статистику адаптации
stats = PatternAgeToUniversalBridge.get_age_adaptation_stats(base_modules_count=100)
# Для 100 базовых модулей:
# - Входные модули (после Gender): 300 (100 × 3)
# - Выходные модули (после Age): 1500 (100 × 3 × 5)
# - Множитель: 15x
```

### Архитектура

- **Тип:** Pattern агент (UPGRADE версия Pydantic AI агента)
- **Фреймворк:** Pydantic AI + Universal Decorators
- **Специализация:** Возрастная адаптация психологического контента
- **База знаний:** `knowledge/pattern_age_adaptation_agent_knowledge.md`
- **НЕ публикуется в git** (локальная разработка PatternShift)
- **НЕ универсальный** (проект-специфичный)

## Принципы работы

1. **Уважай каждый возраст** - каждый этап жизни ценен и важен
2. **Избегай возрастизма** - никаких стереотипов "слишком молод/стар"
3. **Учитывай развитие** - соответствуй задачам развития по Эриксону
4. **Адаптируй когнитивно** - сложность соответствует возрасту
5. **Резонируй эмоционально** - примеры и метафоры актуальны для возраста
6. **Мотивируй правильно** - используй релевантные драйверы

## Научная база

### Теории развития:

1. **Erikson - Психосоциальное развитие**
   - 8 стадий развития на протяжении жизни
   - Кризисы и задачи каждой стадии

2. **Piaget - Когнитивное развитие**
   - Стадии развития мышления
   - Формальные операции у подростков

3. **Vygotsky - Социокультурная теория**
   - Зона ближайшего развития
   - Роль культуры и социума

4. **Baltes - Lifespan Development**
   - Развитие на протяжении всей жизни
   - Gains and losses на каждом этапе

### Современные исследования:

- Нейропластичность в разных возрастах
- Developmental tasks и well-being
- Успешное старение (Successful Aging)
- Позитивное развитие подростков (Positive Youth Development)

## Пример адаптации

### НЛП техника "Рефрейминг" - адаптация под возраст:

**Teens (14-18):**
```
Смени угол зрения! Та ситуация, которая бесит - можно посмотреть на нее по-другому.
Как в игре сменить камеру, чтобы увидеть скрытые детали.

Пример: "Родители достали с контролем" → "Родители заботятся обо мне"
```

**Young Adults (19-25):**
```
Рефрейминг - смена перспективы на ситуацию для получения новых возможностей.
Как в проекте: та же задача, но другой подход = другой результат.

Пример: "Работа рутинная" → "Развиваю навыки, которые откроют новые двери"
```

**Middle Age (36-50):**
```
Рефрейминг - мудрость видеть множество граней реальности.
Используя жизненный опыт, мы находим смысл даже в сложных ситуациях.

Пример: "Карьера не достигла потолка" → "Могу передать опыт следующему поколению"
```

**Seniors (50+):**
```
Рефрейминг интегрирует опыт жизни в новое понимание.
То, что казалось неудачей, становится важным уроком на пути мудрости.

Пример: "Упущенные возможности" → "Каждый выбор привел меня к сегодняшней мудрости"
```

## Статус разработки

- ✅ База знаний создана
- ✅ Pydantic AI реализация с универсальными декораторами
- ✅ Интеграция с PatternShift workflow (Step 4.2)
- ✅ PatternAgeToUniversalBridge архитектура
- ✅ Специализированные инструменты (7 tools)
- ✅ Workflow для пакетной обработки
- ⏳ Тестирование (в планах)

## Примечания

Этот агент является частью экосистемы 18 специализированных Pattern агентов проекта PatternShift и работает под управлением Pattern Orchestrator Agent.

Все адаптации выполняются с учетом теорий развития (Эриксон, Пиаже, Выготский, Бальтес) и современных исследований возрастной психологии.
