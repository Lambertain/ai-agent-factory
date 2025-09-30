# Pattern Ericksonian Hypnosis Scriptwriter Agent

Специализированный агент для создания эриксоновских гипнотических скриптов в рамках трансформационной системы PatternShift.

## Описание

Pattern Ericksonian Hypnosis Scriptwriter Agent - это экспертный агент, специализирующийся на создании гипнотических скриптов по методологии Милтона Эриксона. Агент использует техники непрямого внушения, терапевтические метафоры и языковые паттерны Милтон-модели для создания безопасных и эффективных гипнотических скриптов.

### Ключевые возможности

- **Создание полных гипнотических скриптов** с учетом терапевтических целей
- **Генерация встроенных команд** для подсознательного воздействия
- **Разработка терапевтических метафор** для обхода сознательного сопротивления
- **Адаптация глубины транса** под задачи клиента (light/medium/deep)
- **Создание паттернов Милтон-модели** для непрямых внушений
- **Оценка безопасности тем** для работы с гипнозом
- **Интеграция с PatternShift** 21-дневными программами изменений

### Структура гипнотического скрипта

Каждый скрипт состоит из 5 обязательных компонентов:

1. **Индукция транса** (3-7 минут) - фиксация внимания и начальное расслабление
2. **Углубление** (3-5 минут) - счет, метафора спуска, усиление транса
3. **Терапевтическая работа** (10-15 минут) - работа с целью через метафоры и внушения
4. **Постгипнотические внушения** (2-3 минуты) - закрепление изменений
5. **Выход из транса** (2-3 минуты) - постепенное возвращение

## Установка

```bash
# Клонируйте репозиторий agent-factory
cd D:/Automation/agent-factory/use-cases/agent-factory-with-subagents/agents/pattern_ericksonian_hypnosis_scriptwriter

# Установите зависимости
pip install pydantic-ai python-dotenv pydantic-settings

# Создайте .env файл с настройками
cp .env.example .env
```

### Конфигурация .env

```env
# LLM настройки
LLM_API_KEY=your_api_key_here
LLM_PROVIDER=openai
LLM_MODEL=qwen2.5-coder-32b-instruct
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# PatternShift проект
PATTERNSHIFT_PROJECT_PATH=D:/Automation/Development/projects/patternshift

# Archon настройки
ARCHON_PROJECT_ID=c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
KNOWLEDGE_DOMAIN=patternshift.com

# Настройки гипнотических скриптов
DEFAULT_TRANCE_DEPTH=medium
DEFAULT_DURATION_MINUTES=20
SAFETY_CHECKS_ENABLED=true
```

## Использование

### Базовое использование

```python
import asyncio
from pattern_ericksonian_hypnosis_scriptwriter import (
    run_pattern_ericksonian_hypnosis_scriptwriter,
    PatternEricsονianHypnosisScriptwriterDependencies
)
from pattern_ericksonian_hypnosis_scriptwriter.settings import load_settings

async def main():
    settings = load_settings()

    deps = PatternEricsονianHypnosisScriptwriterDependencies(
        api_key=settings.llm_api_key,
        patternshift_project_path=settings.patternshift_project_path
    )

    user_request = """
    Создай гипнотический скрипт для преодоления страха публичных выступлений.
    Уровень транса: medium, длительность: 20 минут
    """

    result = await run_pattern_ericksonian_hypnosis_scriptwriter(
        user_message=user_request,
        deps=deps
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Создание полного скрипта

```python
from pattern_ericksonian_hypnosis_scriptwriter.agent import agent
from pattern_ericksonian_hypnosis_scriptwriter.dependencies import PatternEricsονianHypnosisScriptwriterDependencies

# Инициализация зависимостей
deps = PatternEricsονianHypnosisScriptwriterDependencies(
    api_key="your_api_key",
    patternshift_project_path="path/to/patternshift"
)

# Создание скрипта
result = await agent.run(
    """
    Используй инструмент create_full_hypnotic_script для создания скрипта:
    - Название: "Уверенность в публичных выступлениях"
    - Цель: преодоление страха сцены
    - Проблема: тревога перед выступлениями
    - Глубина транса: medium
    - Длительность: 20 минут
    - Включить метафору: да
    """,
    deps=deps
)

print(result.data)
```

### Создание паттернов Милтон-модели

```python
result = await agent.run(
    """
    Создай паттерны Милтон-модели для сообщения "расслабься и отпусти тревогу".
    Используй типы паттернов: nominalizations, embedded_commands, presuppositions
    """,
    deps=deps
)

print(result.data)
```

## Инструменты агента

### create_full_hypnotic_script

Создание полного структурированного гипнотического скрипта.

**Параметры:**
- `script_title` (str) - название скрипта
- `therapeutic_goal` (str) - терапевтическая цель
- `target_problem` (str) - целевая проблема клиента
- `trance_depth` (str) - глубина транса: "light", "medium", "deep"
- `duration_minutes` (int) - длительность в минутах (по умолчанию: 20)
- `include_metaphor` (bool) - включать ли метафору (по умолчанию: True)

**Возвращает:** JSON с полным скриптом, включая все 5 компонентов

### create_milton_model_patterns

Генерация языковых паттернов Милтон-модели для непрямого внушения.

**Параметры:**
- `therapeutic_message` (str) - основное терапевтическое сообщение
- `pattern_types` (List[str]) - типы паттернов (опционально)

**Типы паттернов:**
- `nominalizations` - номинализации (превращение глаголов в существительные)
- `unspecified_verbs` - неопределенные глаголы
- `double_binds` - двойные связки
- `embedded_commands` - встроенные команды
- `presuppositions` - пресуппозиции

## Техники Эриксоновского Гипноза

### Непрямые внушения

- **Импликации** - подразумевание без прямого указания
- **Пресуппозиции** - встраивание предположений
- **Двойные связки** - выбор без выбора
- **Открытые внушения** - незавершенные внушения

### Милтон-модель

- **Номинализации** - абстрактные понятия вместо конкретных действий
- **Неопределенные референтные индексы** - "кто-то", "что-то"
- **Неспецифические глаголы** - "происходить", "изменяться"

### Встроенные команды

```
Я не знаю, как быстро ты можешь РАССЛАБИТЬСЯ, но...
Интересно, когда именно ты ПОЧУВСТВУЕШЬ ИЗМЕНЕНИЯ...
Подсознание уже знает, как ИНТЕГРИРОВАТЬ НОВЫЙ ПАТТЕРН...
```

### Глубины транса

- **Light (Альфа)** - легкое расслабление, фокусировка на дыхании
- **Medium (Тета)** - терапевтический транс, работа с подсознанием
- **Deep (Глубокая тета)** - глубокие трансформационные изменения

## База знаний агента

Агент имеет собственную базу знаний в формате Markdown, расположенную в:
```
knowledge/pattern_ericksonian_hypnosis_scriptwriter_knowledge.md
```

### Загрузка знаний в Archon

1. Откройте Archon Knowledge Base: http://localhost:3737/
2. Перейдите в раздел "Knowledge Base" → "Upload"
3. Загрузите файл `pattern_ericksonian_hypnosis_scriptwriter_knowledge.md`
4. Добавьте теги:
   - `pattern-ericksonian-hypnosis`
   - `hypnosis`
   - `milton-model`
   - `agent-knowledge`
   - `pydantic-ai`
   - `patternshift`

5. Привяжите к проекту AI Agent Factory → вкладка Sources

### Поиск в базе знаний

Агент автоматически использует инструмент `search_agent_knowledge` для поиска специализированной информации:

```python
# Встроенный инструмент агента
result = await agent.run(
    "Найди информацию о техниках углубления транса",
    deps=deps
)
```

## Интеграция с PatternShift

Агент предназначен для создания гипнотических скриптов, которые интегрируются с 21-дневными программами трансформации PatternShift:

- **Модульная структура** - скрипты как часть программы изменений
- **Психообразование** - связь с обучающими модулями
- **Упражнения НЛП** - комбинация гипноза и НЛП техник
- **Микропривычки** - постгипнотические внушения для формирования привычек

## Безопасность

Агент включает встроенную систему проверки безопасности тем:

### Противопоказания (высокий риск)

- Суицидальные мысли
- Психоз и шизофрения
- Биполярное расстройство
- Эпилепсия
- Серьезная депрессия
- Травматические переживания

**Для этих тем агент рекомендует работу с квалифицированным специалистом.**

### Безопасные темы (низкий риск)

- Релаксация и снятие стресса
- Преодоление страхов и тревоги
- Уверенность в себе
- Изменение привычек
- Управление болью (неострая)
- Улучшение сна
- Мотивация

## Примеры использования

### Пример 1: Релаксация и управление стрессом

```python
result = await agent.run(
    """
    Создай скрипт для глубокой релаксации и снятия стресса.
    Длительность: 15 минут, глубина: medium
    """,
    deps=deps
)
```

### Пример 2: Уверенность в себе

```python
result = await agent.run(
    """
    Создай гипнотический скрипт для развития уверенности в себе.
    Целевая проблема: низкая самооценка и сомнения в своих силах
    Включить метафору о росте дерева
    """,
    deps=deps
)
```

### Пример 3: Изменение привычек

```python
result = await agent.run(
    """
    Создай скрипт для формирования привычки здорового питания.
    Работать с подсознательными установками о еде.
    Длительность: 25 минут, глубина: deep
    """,
    deps=deps
)
```

## Архитектура

```
pattern_ericksonian_hypnosis_scriptwriter/
├── agent.py                 # Основной агент с инструментами
├── dependencies.py          # Зависимости и RAG конфигурация
├── models.py                # Pydantic модели для скриптов
├── tools.py                 # Инструменты генерации скриптов
├── prompts.py               # Системные промпты агента
├── settings.py              # Конфигурация и настройки
├── __init__.py              # Экспорты пакета
├── knowledge/               # База знаний агента
│   └── pattern_ericksonian_hypnosis_scriptwriter_knowledge.md
└── README.md                # Документация
```

## Разработка

### Тестирование

```bash
# Запуск тестов
pytest tests/

# С покрытием
pytest --cov=pattern_ericksonian_hypnosis_scriptwriter tests/
```

### Расширение функциональности

Для добавления новых инструментов:

1. Добавьте функцию в `tools.py`
2. Зарегистрируйте инструмент через декоратор `@agent.tool`
3. Обновите документацию в README.md

## Лицензия

MIT License

## Авторы

- AI Agent Factory Team
- PatternShift Development Team

## Поддержка

- GitHub: https://github.com/your-org/agent-factory
- Документация: https://docs.patternshift.com
- База знаний: http://localhost:3737/