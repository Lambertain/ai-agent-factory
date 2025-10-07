# Система контроля качества Quality Guardian

## Быстрый старт

### Как запросить аудит

**Для агента или проекта:**

```
Мне нужен quality audit для [название агента/проекта]
```

**Примеры:**
- "Мне нужен quality audit для payment_integration_agent"
- "Проведи аудит quality для проекта PatternShift"
- "Проверь качество кода в agents/uiux_enhancement_agent"

---

## Трехэтапная система контроля

### ЭТАП 1: АУДИТ

**Quality Guardian проводит:**

1. Проверку по чек-листу (`checklists/audit_checklist.md`)
2. Анализ соответствия стандартам
3. Выявление проблем всех уровней
4. Формирование детального отчета

**Результат:** Список проблем с приоритизацией (P1-Critical, P2-High, P3-Medium)

---

### ЭТАП 2: СОЗДАНИЕ ЗАДАЧ

**Quality Guardian автоматически:**

1. Создает задачу в Archon для КАЖДОЙ проблемы
2. Использует шаблон из `templates/task_template.md`
3. Назначает на правильного исполнителя:
   - Implementation Engineer - код
   - Blueprint Architect - архитектура
   - Quality Guardian - тесты
4. Устанавливает приоритет (task_order)

**Результат:** Задачи в Archon готовы к выполнению

---

### ЭТАП 3: КОНТРОЛЬ РЕАЛИЗАЦИИ

**Quality Guardian мониторит:**

1. Выполнение созданных задач
2. Проводит code review после выполнения
3. Валидирует исправления
4. Закрывает задачи только после проверки

**Результат:** Гарантированное качество исправлений

---

## Категории проверок

### 1. Архитектура
- Размеры файлов (<500 строк)
- Наличие обязательных файлов
- Структура проекта
- Модульность

### 2. Код
- UTF-8 кодировка (без Unicode символов)
- Комментарии на русском
- Type hints
- Docstrings

### 3. Документация
- README актуален
- Knowledge base заполнена
- Примеры использования
- Integration guides

### 4. Тесты
- Наличие тестов
- Coverage >80%
- Edge cases
- Failure cases

### 5. Интеграция
- Archon интеграция
- Инструменты агента
- Dependencies
- Prompts

### 6. Качество
- Отсутствие технического долга
- Модульность
- Single responsibility
- Performance

### 7. Безопасность
- Нет hardcoded секретов
- Input validation
- Error handling
- Secure logging

---

## Уровни приоритета

### P1-Critical (task_order: 90-100)
**Блокирующие проблемы:**
- Отсутствие обязательных файлов
- Критические ошибки в коде
- Security уязвимости
- Блокирует работу других агентов

**Время реакции:** Немедленно

### P2-High (task_order: 60-89)
**Важные проблемы:**
- Превышение лимита строк
- Отсутствие тестов
- Плохая документация
- Code smells

**Время реакции:** В течение дня

### P3-Medium (task_order: 30-59)
**Улучшения:**
- Оптимизация кода
- Дополнительные тесты
- Улучшение комментариев
- Refactoring

**Время реакции:** В течение недели

---

## Примеры использования

### Пример 1: Аудит нового агента

```
User: Мне нужен quality audit для payment_integration_agent

Quality Guardian:
1. Проводит аудит по чек-листу
2. Находит 5 проблем:
   - P1-Critical: Отсутствует workflow.py
   - P2-High: Превышен лимит строк в agent.py (650 строк)
   - P2-High: Нет тестов
   - P3-Medium: Неполная документация
   - P3-Medium: Отсутствуют примеры
3. Создает 5 задач в Archon
4. Назначает на соответствующих агентов
5. Уведомляет Project Manager о переприоритизации
```

### Пример 2: Периодический аудит проекта

```
User: Проведи weekly quality audit для AI Agent Factory

Quality Guardian:
1. Анализирует все агенты проекта
2. Формирует сводный отчет
3. Создает задачи для найденных проблем
4. Генерирует quality metrics dashboard
5. Отправляет weekly report команде
```

---

## Интеграция с существующими процессами

### После создания нового агента

```python
# Автоматический вызов Quality Guardian
after_agent_creation():
    quality_guardian.audit(agent_name)
    quality_guardian.create_tasks_from_audit()
    project_manager.prioritize_tasks()
```

### В CI/CD пайплайне

```yaml
# GitHub Actions
- name: Quality Check
  run: quality-guardian audit --project-path . --create-tasks
```

### Периодический мониторинг

```python
# Еженедельный аудит
@schedule(weekly)
def weekly_quality_audit():
    quality_guardian.audit_project()
    quality_guardian.generate_report()
    quality_guardian.notify_team()
```

---

## Файлы системы

```
agents/archon_quality_guardian/
├── knowledge/
│   └── archon_quality_guardian_knowledge.md  # Системный промпт с 3 этапами
├── checklists/
│   └── audit_checklist.md                     # Чек-лист аудита
├── templates/
│   └── task_template.md                       # Шаблон задач
└── QUALITY_CONTROL_SYSTEM.md                  # Этот файл
```

---

## Best Practices

### Для Quality Guardian:
1. Всегда следовать трем этапам
2. Не пропускать создание задач
3. Проводить ревью перед закрытием
4. Документировать все находки

### Для Implementation Engineer:
1. Обращаться к шаблону задач
2. Следовать критериям завершения
3. Запрашивать ревью у Quality Guardian
4. Обновлять документацию

### Для Project Manager:
1. Переприоритизировать после создания задач
2. Мониторить критические проблемы
3. Балансировать нагрузку команды
4. Отслеживать качественные метрики

---

## Метрики качества

**Отслеживаем:**
- Количество критических проблем
- Среднее время исправления
- Trend качества кода (improving/declining)
- Test coverage по проекту
- Technical debt в часах

**Цели:**
- P1-Critical: 0
- P2-High: <5
- Test coverage: >80%
- Technical debt: <40 часов

---

## FAQ

**Q: Как часто проводить аудит?**
A: Рекомендуется:
- После создания нового агента - сразу
- Еженедельный аудит проекта
- После major changes
- По запросу Project Manager

**Q: Что делать если найдено много проблем?**
A: Quality Guardian создаст задачи, Project Manager переприоритизирует, команда работает по приоритетам.

**Q: Можно ли пропустить создание задач?**
A: Нет, это обязательный этап. Задачи обеспечивают:
- Прозрачность
- Отслеживание
- Accountability
- Integration с Archon

---

**Версия:** 1.0
**Дата создания:** 2025-10-07
**Автор:** Archon Quality Guardian
