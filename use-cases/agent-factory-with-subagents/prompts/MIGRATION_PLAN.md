# 📋 План миграции агентов на универсальный системный промпт

Пошаговый план миграции всех существующих агентов на использование универсального системного промпта.

## 🎯 Цели миграции

- **Стандартизация**: Единообразное поведение всех агентов
- **Универсальность**: Устранение проект-специфичных привязок
- **Качество**: Внедрение обязательной рефлексии и улучшений
- **Совместимость**: Обеспечение межагентного взаимодействия

## 📊 Анализ текущего состояния

### Агенты требующие миграции:

1. **Security Audit Agent** - частично универсален
2. **RAG Agent** - требует улучшения промпта
3. **Next.js Optimization Agent** - мигрирован ✅
4. **TypeScript Architecture Agent** - мигрирован ✅
5. **Prisma Database Agent** - мигрирован ✅
6. **PWA Mobile Agent** - универсален ✅
7. **Performance Optimization Agent** - требует проверки
8. **UI/UX Enhancement Agent** - требует миграции
9. **Payment Integration Agent** - требует миграции
10. **Queue Worker Agent** - требует миграции

## 🚀 Поэтапная миграция

### Фаза 1: Критические агенты (1-2 дня)

#### Security Audit Agent
**Приоритет**: ВЫСОКИЙ
**Статус**: В процессе

```python
# Текущая конфигурация
config = UniversalPromptConfig(
    agent_name="security_audit_agent",
    specialization="кибербезопасности и аудита безопасности",
    domain_type="web_application",
    project_type="universal"
)
```

**Задачи миграции**:
- [ ] Замена текущего промпта на универсальный
- [ ] Добавление обязательных инструментов коллективной работы
- [ ] Интеграция с RAG системой
- [ ] Валидация универсальности

#### RAG Agent
**Приоритет**: ВЫСОКИЙ
**Статус**: Требует работы

```python
# Планируемая конфигурация
config = UniversalPromptConfig(
    agent_name="rag_agent",
    specialization="семантического поиска и работы с базами знаний",
    domain_type="general",
    project_type="universal",
    enable_delegation=False  # RAG обычно не делегирует
)
```

**Задачи миграции**:
- [ ] Обновление системного промпта
- [ ] Улучшение поисковых алгоритмов
- [ ] Добавление универсальных паттернов поиска
- [ ] Интеграция с коллективной системой

### Фаза 2: Функциональные агенты (2-3 дня)

#### Performance Optimization Agent
```python
config = UniversalPromptConfig(
    agent_name="performance_optimization_agent",
    specialization="оптимизации производительности",
    domain_type="web",
    project_type="universal"
)
```

#### UI/UX Enhancement Agent
```python
config = UniversalPromptConfig(
    agent_name="uiux_enhancement_agent",
    specialization="дизайна пользовательских интерфейсов и UX",
    domain_type="web",
    project_type="universal"
)
```

#### Payment Integration Agent
```python
config = UniversalPromptConfig(
    agent_name="payment_integration_agent",
    specialization="интеграции платежных систем",
    domain_type="ecommerce",
    project_type="universal"
)
```

#### Queue Worker Agent
```python
config = UniversalPromptConfig(
    agent_name="queue_worker_agent",
    specialization="системам очередей и фоновых задач",
    domain_type="backend",
    project_type="universal"
)
```

### Фаза 3: Специализированные агенты (1-2 дня)

#### API Development Agent
```python
config = UniversalPromptConfig(
    agent_name="api_development_agent",
    specialization="разработке API и backend сервисов",
    domain_type="backend",
    project_type="universal"
)
```

#### MCP Configuration Agent
```python
config = UniversalPromptConfig(
    agent_name="mcp_configuration_agent",
    specialization="управлению MCP серверами",
    domain_type="devops",
    project_type="universal"
)
```

## 🛠️ Процедура миграции агента

### Шаг 1: Анализ текущего состояния
```python
# Валидация текущего промпта
from prompts.universal_system_prompt import validate_prompt_universality

current_prompt = read_current_prompt("agents/{agent_name}/prompts.py")
validation = validate_prompt_universality(current_prompt)

print(f"Текущая оценка: {validation['score']}/100")
print(f"Проблемы: {validation['issues']}")
```

### Шаг 2: Создание конфигурации
```python
# Определение специализации агента
specialization = determine_agent_specialization(agent_name)
domain_type = analyze_target_domain(agent_name)
project_type = "universal"  # Всегда универсальный

config = UniversalPromptConfig(
    agent_name=agent_name,
    specialization=specialization,
    domain_type=domain_type,
    project_type=project_type
)
```

### Шаг 3: Генерация нового промпта
```python
from prompts.universal_system_prompt import get_universal_system_prompt

new_prompt = get_universal_system_prompt(config)

# Валидация нового промпта
new_validation = validate_prompt_universality(new_prompt)
assert new_validation['is_universal'], f"Проблемы: {new_validation['issues']}"
```

### Шаг 4: Обновление файлов агента
```python
# Обновление prompts.py
update_prompts_file(f"agents/{agent_name}/prompts.py", new_prompt)

# Добавление обязательных инструментов
add_universal_tools(f"agents/{agent_name}/tools.py")

# Обновление dependencies
add_universal_dependencies(f"agents/{agent_name}/dependencies.py")
```

### Шаг 5: Валидация и тестирование
```python
# Финальная проверка
final_validation = validate_agent_universality(agent_name)
run_agent_tests(agent_name)
test_agent_integration(agent_name)
```

## 📋 Чек-лист миграции

### Для каждого агента:

#### Подготовка
- [ ] Анализ текущего промпта агента
- [ ] Определение специализации и домена
- [ ] Создание конфигурации UniversalPromptConfig
- [ ] Валидация планируемых изменений

#### Реализация
- [ ] Замена системного промпта на универсальный
- [ ] Добавление обязательных инструментов:
  - [ ] `break_down_to_microtasks()`
  - [ ] `report_microtask_progress()`
  - [ ] `delegate_task_to_agent()`
  - [ ] `reflect_and_improve()`
  - [ ] `search_agent_knowledge()`
- [ ] Обновление dependencies.py с универсальными полями
- [ ] Создание примеров конфигураций в examples/
- [ ] Обновление README.md агента

#### Валидация
- [ ] Проверка универсальности промпта (≥80/100)
- [ ] Тестирование на различных конфигурациях
- [ ] Проверка межагентного взаимодействия
- [ ] Валидация отсутствия проект-специфичного кода
- [ ] Тестирование RAG интеграции

#### Документация
- [ ] Обновление документации агента
- [ ] Создание примеров использования
- [ ] Документирование изменений в CHANGELOG
- [ ] Обновление общей документации проекта

## 🎯 Критерии успешной миграции

### Технические критерии:
- ✅ Оценка универсальности ≥80/100
- ✅ 0% проект-специфичных упоминаний
- ✅ Наличие всех обязательных инструментов
- ✅ Работающая RAG интеграция
- ✅ Примеры для ≥3 различных доменов

### Функциональные критерии:
- ✅ Агент сохраняет свою экспертизу
- ✅ Качество решений не ухудшается
- ✅ Добавлена возможность делегирования
- ✅ Работает цикл рефлексии и улучшений
- ✅ Интеграция с другими агентами

### Качественные критерии:
- ✅ Улучшена модульность кода
- ✅ Документация актуализирована
- ✅ Тесты покрывают новую функциональность
- ✅ Производительность не ухудшилась

## 🚨 Риски и меры по снижению

### Возможные риски:
1. **Потеря специфичной экспертизы**
   - Митигация: Тщательное тестирование на реальных задачах
   - Контроль: Сравнение качества до/после миграции

2. **Нарушение существующих интеграций**
   - Митигация: Постепенная миграция с тестированием
   - Контроль: Regression тесты для всех интеграций

3. **Снижение производительности**
   - Митигация: Профилирование и оптимизация
   - Контроль: Бенчмарки производительности

4. **Сложность адаптации для разработчиков**
   - Митигация: Подробная документация и примеры
   - Контроль: Обучающие материалы и поддержка

### Планы откатов:
- Сохранение старых версий промптов
- Возможность быстрого переключения
- Мониторинг качества работы агентов
- Система алертов при деградации

## 📅 Временной план

### Неделя 1: Подготовка и критические агенты
- **День 1-2**: Создание универсального промпта ✅
- **День 3-4**: Миграция Security Audit Agent
- **День 5-6**: Миграция RAG Agent
- **День 7**: Тестирование и валидация

### Неделя 2: Функциональные агенты
- **День 1-2**: Performance Optimization Agent
- **День 3-4**: UI/UX Enhancement Agent
- **День 5-6**: Payment Integration Agent
- **День 7**: Queue Worker Agent

### Неделя 3: Специализированные агенты и финализация
- **День 1-2**: API Development Agent
- **День 3-4**: MCP Configuration Agent
- **День 5-6**: Интеграционное тестирование
- **День 7**: Документация и релиз

## 🎉 Ожидаемые результаты

### После завершения миграции:

#### Для разработчиков:
- Единообразный API всех агентов
- Предсказуемое поведение и интерфейсы
- Упрощенное создание новых агентов
- Стандартизированная документация

#### Для пользователей:
- Консистентный пользовательский опыт
- Улучшенное качество решений
- Автоматическое межагентное взаимодействие
- Адаптивность под любые проекты

#### Для системы в целом:
- Масштабируемая архитектура агентов
- Централизованное управление качеством
- Упрощенное тестирование и валидация
- Основа для будущего развития

---

**Успешная миграция означает**: Каждый агент работает универсально, взаимодействует с другими агентами, обеспечивает высокое качество решений и может быть использован в любом проекте без изменений.