# 🌐 Универсальный системный промпт для агентов

Централизованная система промптов, обеспечивающая стандартизированное поведение, универсальность и качество всех агентов в AI Agent Factory.

## 🎯 Назначение

Универсальный системный промпт решает ключевые проблемы разработки агентов:

- **Стандартизация**: Единообразное поведение всех агентов
- **Универсальность**: Запрет на привязку к конкретным проектам
- **Качество**: Обязательная рефлексия и улучшение результатов
- **Коллективность**: Автоматическое межагентное взаимодействие
- **Масштабируемость**: Легкое создание новых агентов

## 🚀 Быстрый старт

### Базовое использование

```python
from prompts.universal_system_prompt import get_universal_system_prompt, UniversalPromptConfig

# Конфигурация для Security Audit Agent
config = UniversalPromptConfig(
    agent_name="security_audit_agent",
    specialization="кибербезопасности и аудита безопасности",
    domain_type="web_application",
    project_type="enterprise"
)

# Получение промпта
system_prompt = get_universal_system_prompt(config)

# Использование в Pydantic AI агенте
from pydantic_ai import Agent

agent = Agent(
    model="qwen2.5-coder-32b-instruct",
    system_prompt=system_prompt,
    deps_type=YourDependencies
)
```

### Упрощенное использование

```python
from prompts.universal_system_prompt import get_agent_specific_prompt

# Автоматическая конфигурация для известных типов агентов
prompt = get_agent_specific_prompt("rag_agent", domain="healthcare")
```

## 🛠️ Конфигурация

### UniversalPromptConfig

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|-----------|
| `agent_name` | str | - | Имя агента (обязательно) |
| `specialization` | str | - | Область экспертизы (обязательно) |
| `domain_type` | str | "general" | Тип домена (web, mobile, desktop, etc.) |
| `project_type` | str | "universal" | Тип проекта (saas, ecommerce, enterprise, etc.) |
| `framework` | str | "pydantic-ai" | Используемый фреймворк |
| `enable_rag` | bool | True | Включить RAG инструкции |
| `enable_delegation` | bool | True | Включить делегирование задач |
| `enable_reflection` | bool | True | Включить обязательную рефлексию |

### Поддерживаемые типы агентов

```python
AGENT_SPECIALIZATIONS = {
    "security_audit": "кибербезопасности и аудита безопасности",
    "rag_agent": "семантического поиска и работы с базами знаний",
    "uiux_enhancement": "дизайна пользовательских интерфейсов и UX",
    "performance_optimization": "оптимизации производительности",
    "typescript_architecture": "архитектуре TypeScript проектов",
    "prisma_database": "проектированию баз данных и Prisma ORM",
    "pwa_mobile": "Progressive Web Apps и мобильной разработке",
    "nextjs_optimization": "оптимизации Next.js приложений",
    # ... и другие
}
```

## 🌐 Принципы универсальности

### ❌ Что ЗАПРЕЩЕНО:

- Упоминания конкретных проектов (UniPark, PatternShift, etc.)
- Hardcoded значения (цвета, порты, URL)
- Проект-специфичные настройки
- Неконфигурируемые зависимости

### ✅ Что ОБЯЗАТЕЛЬНО:

- Адаптация под любой domain_type
- Конфигурируемые параметры
- Примеры для ≥3 различных доменов
- Универсальные паттерны решения задач

## 🤝 Коллективная работа агентов

Промпт автоматически включает инструкции для:

### 1. Планирование задач
- Автоматическая декомпозиция на микрозадачи
- Анализ необходимости делегирования
- Планирование межагентного взаимодействия

### 2. Выполнение с отчетностью
- Отчеты о прогрессе каждой микрозадачи
- Визуализация процесса для пользователя
- Координация между агентами

### 3. Обязательная рефлексия
- Критический анализ результатов
- Выявление и устранение недостатков
- Улучшение качества перед завершением

## 🔍 RAG интеграция

Промпт автоматически настраивает:

### Поисковые стратегии
- Специфичные термины для области экспертизы
- Комбинирование по domain_type и project_type
- Поиск универсальных паттернов
- Валидация актуальности информации

### Теги для поиска
```python
# Автоматически генерируемые теги
tags = [
    config.agent_name.replace('_', '-'),
    "agent-knowledge",
    config.framework,
    config.specialization.replace(' ', '-'),
    "universal-patterns"
]
```

## 📋 Валидация универсальности

Встроенная система проверки промптов:

```python
from prompts.universal_system_prompt import validate_prompt_universality

# Проверка промпта на универсальность
validation = validate_prompt_universality(your_prompt)

print(f"Оценка универсальности: {validation['score']}/100")
print(f"Универсален: {validation['is_universal']}")

if validation['issues']:
    print("Найденные проблемы:")
    for issue in validation['issues']:
        print(f"- {issue}")
```

### Критерии валидации

- **Проект-специфичные упоминания**: -20 баллов за каждое
- **Hardcoded значения**: -15 баллов за каждое
- **Отсутствие универсальных элементов**: -10 баллов за каждое
- **Минимальный порог**: 80/100 для признания универсальным

## 🛠️ Интеграция в существующие агенты

### Миграция с текущих промптов

1. **Анализ текущего промпта**:
```python
# Проверьте текущий промпт
current_validation = validate_prompt_universality(current_prompt)
```

2. **Создание конфигурации**:
```python
# Настройте конфигурацию под ваш агент
config = UniversalPromptConfig(
    agent_name="your_agent_name",
    specialization="ваша_область_экспертизы",
    domain_type="определите_домен",
    project_type="определите_тип_проекта"
)
```

3. **Генерация нового промпта**:
```python
# Получите универсальный промпт
new_prompt = get_universal_system_prompt(config)
```

4. **Тестирование**:
```python
# Проверьте качество нового промпта
new_validation = validate_prompt_universality(new_prompt)
assert new_validation['is_universal'], "Промпт должен быть универсальным"
```

### Кастомизация для специфичных нужд

```python
# Базовый промпт
config = UniversalPromptConfig(
    agent_name="custom_agent",
    specialization="ваша_экспертиза"
)

base_prompt = get_universal_system_prompt(config)

# Добавление специфичных инструкций
custom_instructions = """
## ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ

### Ваши специфичные инструкции:
- Особые требования к вашему агенту
- Дополнительные инструменты
- Специфичные паттерны работы
"""

final_prompt = base_prompt + custom_instructions

# Валидация финального промпта
validation = validate_prompt_universality(final_prompt)
```

## 📚 Примеры реальных конфигураций

### Security Audit Agent

```python
config = UniversalPromptConfig(
    agent_name="security_audit_agent",
    specialization="кибербезопасности и аудита безопасности",
    domain_type="web_application",
    project_type="enterprise",
    enable_rag=True,
    enable_delegation=True
)
```

### UI/UX Enhancement Agent

```python
config = UniversalPromptConfig(
    agent_name="uiux_enhancement_agent",
    specialization="дизайна пользовательских интерфейсов и UX",
    domain_type="web",
    project_type="saas",
    framework="react"
)
```

### RAG Agent

```python
config = UniversalPromptConfig(
    agent_name="rag_agent",
    specialization="семантического поиска и работы с базами знаний",
    domain_type="general",
    project_type="universal",
    enable_delegation=False  # RAG агент обычно не делегирует
)
```

## 🔧 Разработка новых агентов

### Шаблон создания агента

```python
# 1. Определите специализацию
SPECIALIZATION = "ваша_область_экспертизы"

# 2. Создайте конфигурацию
config = UniversalPromptConfig(
    agent_name="new_agent_name",
    specialization=SPECIALIZATION,
    domain_type="подходящий_домен",
    project_type="целевой_тип_проекта"
)

# 3. Получите промпт
system_prompt = get_universal_system_prompt(config)

# 4. Создайте агента
from pydantic_ai import Agent

agent = Agent(
    model="qwen2.5-coder-32b-instruct",
    system_prompt=system_prompt,
    deps_type=YourDependencies
)

# 5. Добавьте обязательные инструменты
@agent.tool
async def search_agent_knowledge(ctx, query: str) -> str:
    """Поиск в базе знаний агента."""
    # Реализация поиска...

@agent.tool
async def break_down_to_microtasks(ctx, task: str) -> str:
    """Разбивка задачи на микрозадачи."""
    # Реализация декомпозиции...

# 6. Валидация
validation = validate_prompt_universality(system_prompt)
assert validation['is_universal'], f"Проблемы: {validation['issues']}"
```

## 🎯 Критерии качества

### Обязательные элементы промпта

- ✅ Принципы универсальности
- ✅ Специализация агента
- ✅ Коллективное решение задач
- ✅ RAG интеграция
- ✅ Обязательная рефлексия
- ✅ Стандарты качества
- ✅ Критерии завершения

### Структура качественного промпта

1. **Заголовок и роль** (кто вы)
2. **Принципы универсальности** (как работать)
3. **Экспертиза** (что знаете)
4. **Коллективная работа** (как взаимодействовать)
5. **Инструменты** (что использовать)
6. **Рефлексия** (как улучшаться)
7. **Стандарты** (к чему стремиться)
8. **Финальная проверка** (как завершать)

## 🚀 Roadmap развития

### Версия 1.0 (текущая)
- ✅ Базовая универсальность
- ✅ Коллективное решение задач
- ✅ RAG интеграция
- ✅ Система рефлексии

### Версия 1.1 (планируется)
- 🔄 Адаптивные промпты на основе контекста
- 🔄 Автоматическая оптимизация под домен
- 🔄 Интеграция с системой метрик качества
- 🔄 Персонализация под предпочтения пользователя

### Версия 2.0 (будущее)
- 🚀 Самообучающиеся промпты
- 🚀 Динамическая генерация инструкций
- 🚀 Мультимодальная поддержка
- 🚀 Кроссплатформенная совместимость

## 🤝 Вклад в развитие

Для улучшения универсального промпта:

1. **Тестируйте** на различных типах задач
2. **Документируйте** найденные проблемы
3. **Предлагайте** улучшения через Archon
4. **Валидируйте** новые конфигурации
5. **Делитесь** успешными паттернами

---

**Цель**: Каждый агент, созданный с универсальным промптом, должен работать в любом проекте, адаптироваться под любые требования и демонстрировать высочайшее качество решений.

**Принцип**: "Создай один раз - используй везде"