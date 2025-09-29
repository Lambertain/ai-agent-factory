# Система Культурного Профилирования PatternShift

## Обзор

Система культурного профилирования для Pattern Cultural Adaptation Expert Agent решает критически важную задачу определения культурной идентичности пользователей **независимо от их географического местоположения**.

### Ключевая проблема
Пользователь может:
- Быть французом по культуре, но проживать в Индии
- Сохранять украинские традиции, живя в США
- Иметь смешанную культурную идентичность

**Геолокация НЕ определяет культурную принадлежность!**

## Архитектура системы

```
🎭 CULTURAL PROFILING SYSTEM
├── 📋 Registration Questionnaire (registration_questionnaire.json)
├── 🧠 Cultural Profiler (cultural_profiling.py)
├── 🎯 Auto Assignment (auto_culture_assignment.py)
├── 🔧 Integration Tools (tools.py)
└── 💡 Usage Example (usage_example.py)
```

## Основные компоненты

### 1. Анкета Регистрации (registration_questionnaire.json)

**Особенности:**
- 7+ вопросов на 2 языках (RU/EN)
- Различные типы вопросов: выбор, рейтинг, множественный выбор
- Взвешенная система оценки
- Учет уровня уверенности пользователя

**Ключевые вопросы:**
1. **Прямая культурная идентификация** - "С какой культурой вы себя отождествляете?"
2. **Религиозная принадлежность** - учитывает духовные традиции
3. **Языковые предпочтения** - язык психологических материалов
4. **Семейные традиции** - влияние на восприятие изменений
5. **Стиль коммуникации** - как подавать информацию
6. **Предпочтения метафор** - какие образы резонируют
7. **Культурные ценности** - рейтинг приоритетов

### 2. Культурный Профайлер (cultural_profiling.py)

```python
# Создание профайлера
profiler = PatternShiftCulturalProfiler()

# Получение вопросов
questions = profiler.get_cultural_questions("ru")

# Анализ ответов
result = profiler.analyze_cultural_profile(responses)
```

**Возможности:**
- Взвешенный анализ ответов
- Учет уверенности пользователя
- Определение альтернативных культур
- Генерация дополнительных вопросов

### 3. Автоматическое Назначение (auto_culture_assignment.py)

```python
# Автоматическое назначение
assignment = auto_assign_culture_from_registration(responses)

# Результат содержит:
# - assigned_culture: PatternShiftCulture
# - confidence_score: float (0.0-1.0)
# - requires_confirmation: bool
# - alternative_suggestions: List[Tuple]
```

**Уровни уверенности:**
- **VERY_HIGH (0.9+)** - автоматическое назначение
- **HIGH (0.8-0.89)** - рекомендованное назначение
- **MEDIUM (0.6-0.79)** - требует подтверждения
- **LOW (0.4-0.59)** - показать варианты
- **VERY_LOW (<0.4)** - дополнительные вопросы

### 4. Поддерживаемые Культуры

**20 европейских культур:**
- **Славянские:** Украинская, Русская, Польская, Чешская, Словацкая, Болгарская, Хорватская, Сербская, Словенская
- **Германские:** Немецкая, Английская
- **Романские:** Французская, Итальянская, Испанская
- **Балтийские:** Литовская, Латышская, Эстонская
- **Другие:** Венгерская, Румынская

**Религиозные контексты:**
- ☦️ **Православный** (Украинская, Русская, Сербская, Болгарская)
- ✝️ **Католический** (Польская, Итальянская, Французская, Испанская)
- ⛪ **Протестантский** (Немецкая, Английская)
- 🔬 **Светский** (Английская, Французская)
- 🤝 **Смешанный** (Немецкая)

## Интеграция с Pattern Cultural Adaptation Expert Agent

### Новые инструменты агента:

```python
# Обработка регистрации
await process_user_registration(ctx, UserRegistrationData(...))

# Получение анкеты
await get_registration_questionnaire(ctx, language="ru")

# Обновление профиля
await update_user_cultural_profile(ctx, CulturalProfileUpdateRequest(...))

# Валидация назначения
await validate_cultural_assignment(ctx, culture, feedback)
```

### Workflow использования:

1. **Регистрация пользователя:**
   ```python
   questionnaire = await get_registration_questionnaire(ctx, "ru")
   # Пользователь заполняет анкету
   ```

2. **Автоматическое профилирование:**
   ```python
   result = await process_user_registration(ctx, responses)
   # Система определяет культуру и религию
   ```

3. **Адаптация контента:**
   ```python
   adapted = await adapt_content_culturally(ctx, content, target_culture)
   # Контент адаптируется под профиль
   ```

4. **Валидация и корректировка:**
   ```python
   validation = await validate_cultural_assignment(ctx, culture, feedback)
   # Система учитывает обратную связь
   ```

## Примеры использования

### Сценарий 1: Французский эмигрант в Индии

```python
responses = [
    {"question_id": "direct_culture", "selected_option_id": "french", "confidence_level": 8},
    {"question_id": "language_preference", "selected_option_id": "french", "confidence_level": 9},
    {"question_id": "religious_affiliation", "selected_option_id": "catholic", "confidence_level": 7}
]

result = auto_assign_culture_from_registration(responses)
# Результат: FRENCH culture, CATHOLIC religion, confidence: 85%
```

### Сценарий 2: Смешанная культурная идентичность

```python
# Основная польская, вторичная итальянская культура
mixed_profile = create_mixed_cultural_profile(
    PatternShiftCulture.POLISH,
    PatternShiftCulture.ITALIAN,
    {"living_location": "usa"}
)
```

### Сценарий 3: Низкая уверенность - дополнительные вопросы

```python
# При confidence < 0.6 система генерирует дополнительные вопросы:
follow_up = [
    "В какой культурной среде вы выросли?",
    "На каком языке говорили в вашей семье?",
    "Какие культурные праздники для вас важны?"
]
```

## Адаптация контента

### Примеры культурно-адаптированного контента:

**Украинская культура:**
```
Стрес - як ріка навесні, що шукає обхідний шлях навколо каменів.
Метафори: домашнє вогнище, дуб-віковий, родинні традиції
```

**Французская культура:**
```
Le stress comme la pression dans une cocotte-minute parisienne.
Métaphores: art-thérapie, discussions philosophiques, cafés parisiens
```

**Английская культура:**
```
Stress like system optimization - debug the issues systematically.
Метафоры: project management, personal KPIs, individual achievements
```

## Валидация и обратная связь

### Система валидации включает:

1. **Автоматическая валидация:**
   - Проверка культурной безопасности
   - Религиозная корректность
   - Языковая уместность

2. **Валидация пользователем:**
   - Оценка удовлетворенности (1-10)
   - Комментарии и предложения
   - Указание конкретных проблем

3. **Корректировка системы:**
   - Обновление весов вопросов
   - Улучшение алгоритмов назначения
   - Добавление новых метафор

## Технические детали

### Файловая структура:
```
pattern_cultural_adaptation_expert/
├── cultural_profiling.py           # Основная логика профилирования
├── auto_culture_assignment.py      # Автоматическое назначение культуры
├── registration_questionnaire.json # JSON шаблон анкеты
├── tools.py                       # Инструменты агента (обновлены)
├── agent.py                       # Основной агент (обновлен)
├── usage_example.py              # Демонстрация всех возможностей
└── CULTURAL_PROFILING_README.md   # Документация (этот файл)
```

### Зависимости:
```python
from dependencies import (
    PatternShiftCulture,
    PatternShiftReligion,
    PatternShiftCulturalProfile
)
```

## Расширение системы

### Добавление новой культуры:

1. **Обновить enum:**
   ```python
   class PatternShiftCulture(Enum):
       # ... существующие ...
       NEW_CULTURE = "new_culture"
   ```

2. **Добавить профиль:**
   ```python
   PATTERNSHIFT_CULTURAL_PROFILES[PatternShiftCulture.NEW_CULTURE] = Profile(...)
   ```

3. **Обновить анкету:**
   ```json
   {"id": "new_culture", "text_ru": "Новая культура", "culture": "NEW_CULTURE"}
   ```

4. **Добавить метафоры:**
   ```python
   # В adapt_metaphors_culturally и generate_cultural_examples
   ```

### Добавление нового типа вопроса:

1. **Обновить CulturalQuestionType:**
   ```python
   class CulturalQuestionType(Enum):
       NEW_TYPE = "new_type"
   ```

2. **Добавить обработку в профайлер:**
   ```python
   # В analyze_cultural_profile()
   ```

## Лучшие практики

### При создании вопросов:
- ✅ Культурно нейтральная формулировка
- ✅ Понятные варианты ответов
- ✅ Учет различных уровней образования
- ❌ Стереотипы или обобщения
- ❌ Политически окрашенные формулировки

### При адаптации контента:
- ✅ Сохранение терапевтической эффективности
- ✅ Использование культурно релевантных метафор
- ✅ Избегание чувствительных тем
- ❌ Прямой перевод без адаптации
- ❌ Использование непонятных культурных референсов

## Поддержка и развитие

**Мониторинг системы:**
- Отслеживание точности назначений
- Анализ обратной связи пользователей
- Выявление паттернов ошибок
- Постоянное улучшение алгоритмов

**Планы развития:**
- Поддержка неевропейских культур
- Интеграция с системами аналитики
- Машинное обучение для улучшения точности
- API для внешних интеграций

---

## 🎯 Заключение

Система культурного профилирования PatternShift обеспечивает:

1. **Точное определение** культурной идентичности независимо от геолокации
2. **Автоматическое назначение** с возможностью ручной корректировки
3. **Высокое качество** адаптации психологического контента
4. **Культурную безопасность** и уважение к традициям
5. **Масштабируемость** на новые культуры и языки

**Результат:** Каждый пользователь получает персонализированную программу PatternShift, адаптированную под его уникальную культурную идентичность, а не место проживания.

---

*Разработано для Pattern Cultural Adaptation Expert Agent*
*PatternShift - 21-дневная программа психологической трансформации*