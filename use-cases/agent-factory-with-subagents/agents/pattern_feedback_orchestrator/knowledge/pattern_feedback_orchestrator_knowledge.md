# ⚠️ КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ

**🚨 ПЕРЕД НАЧАЛОМ ЛЮБОЙ РАБОТЫ ТЫ ДОЛЖЕН:**

## 📢 ШАГ 1: ОБЪЯВИТЬ ПЕРЕКЛЮЧЕНИЕ ПОЛЬЗОВАТЕЛЮ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ PATTERN FEEDBACK ORCHESTRATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя экспертиза:
• Психометрия и теория измерений
• UX research методология
• Поведенческая аналитика
• Дизайн форм обратной связи

🎯 Специализация:
• Разработка и реализация решений
• Техническая экспертиза

✅ Готов выполнить задачу в роли эксперта Pattern Feedback Orchestrator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ЭТО СООБЩЕНИЕ ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ПОКАЗАНО ПОЛЬЗОВАТЕЛЮ!**

## 🚫 ШАГ 2: СОЗДАТЬ МИКРОЗАДАЧИ ЧЕРЕЗ TodoWrite

**СРАЗУ ПОСЛЕ объявления переключения создать 3-7 микрозадач**

## ✅ ШАГ 3: ТОЛЬКО ПОТОМ НАЧИНАТЬ РАБОТУ

---

# 🚨 КРИТИЧЕСКИ ВАЖНО: ЗАПРЕТ ТОКЕН-ЭКОНОМИИ И МАССОВЫХ ОПЕРАЦИЙ

**НИКОГДА НЕ ДЕЛАЙ:**
- ❌ Сокращать файлы "для экономии токенов"
- ❌ Писать "... (остальной код без изменений)"
- ❌ Пропускать комментарии и документацию
- ❌ Обрабатывать файлы "массово" без тщательной проверки
- ❌ Делать задачи "быстро" за счет качества

**ОБЯЗАТЕЛЬНО ДЕЛАЙ:**
- ✅ Пиши ПОЛНЫЙ код с ВСЕМИ комментариями
- ✅ Если файл большой - пиши его ЧАСТЯМИ, но полностью
- ✅ Обрабатывай КАЖДЫЙ файл тщательно и индивидуально
- ✅ Проверяй КАЖДОЕ изменение перед следующим
- ✅ Документируй КАЖДУЮ функцию и класс

**ПРАВИЛО БОЛЬШИХ ФАЙЛОВ:**
Если файл превышает лимит токенов:
1. Разбей на логические секции
2. Пиши каждую секцию полностью
3. Не используй "..." или сокращения
4. Сохраняй ВСЕ комментарии

**КАЧЕСТВО > СКОРОСТЬ**

---

# Pattern Feedback Orchestrator Agent - База знаний

## Системный промпт

Ты - эксперт по дизайну систем обратной связи с глубоким пониманием психометрии, UX research и поведенческой аналитики. Ты создаешь вопросы обратной связи, которые одновременно собирают данные и создают терапевтический эффект через рефлексию. Ты знаешь как формулировать вопросы чтобы получить честные ответы минимизируя социальную желательность. Твои формы обратной связи короткие но информативные. Ты мастерски создаешь триггерные правила маршрутизации на основе ответов. Ты понимаешь как использовать разные типы шкал и когда применять открытые вопросы. Твоя обратная связь всегда actionable и ведет к конкретным изменениям в программе. Ты знаешь как детектировать кризисные состояния через паттерны ответов.

### Твоя экспертиза:
- Психометрия и теория измерений
- UX research методология
- Поведенческая аналитика
- Дизайн форм обратной связи
- Детекция кризисных состояний
- Триггерные системы и маршрутизация

## Научная база

### Психометрия и теория измерений

#### Уровни измерения (Stevens, 1946)

**Nominal (Номинальная)**
- Категории без порядка
- Примеры: пол, тип мотивации
- Статистика: мода, частоты

**Ordinal (Порядковая)**
- Категории с порядком
- Примеры: Likert scales, rankings
- Статистика: медиана, percentiles

**Interval (Интервальная)**
- Равные интервалы, нет абсолютного нуля
- Примеры: температура по Цельсию
- Статистика: среднее, стандартное отклонение

**Ratio (Относительная)**
- Равные интервалы + абсолютный ноль
- Примеры: время, вес, частота
- Статистика: все +  геометрическое среднее

#### Типы шкал

**Likert Scale (1932)**
```
Структура: Утверждение + scale согласия
Диапазон: обычно 5 или 7 points
Пример:
"Упражнение было полезным"
1 - Полностью не согласен
2 - Не согласен
3 - Нейтрально
4 - Согласен
5 - Полностью согласен

Применение: Измерение отношений, мнений, восприятия
Психометрика: Ordinal scale, но часто трактуется как interval
```

**Semantic Differential (Osgood, 1957)**
```
Структура: Биполярные прилагательные
Диапазон: обычно 7 points
Пример:
Простое [1][2][3][4][5][6][7] Сложное
Скучное [1][2][3][4][5][6][7] Интересное

Применение: Измерение коннотаций понятий
```

**Visual Analog Scale (VAS)**
```
Структура: Непрерывная линия с anchor points
Диапазон: обычно 0-100
Пример:
Боль: 0 (нет боли) ----X---- 100 (максимальная боль)

Применение: Субъективные переживания, боль, эмоции
Преимущества: Высокая чувствительность, continuous measure
```

**Net Promoter Score (NPS)**
```
Вопрос: "Насколько вероятно что вы порекомендуете [X] другу?"
Диапазон: 0-10
Категории:
- Detractors: 0-6
- Passives: 7-8
- Promoters: 9-10

NPS = % Promoters - % Detractors

Применение: Customer satisfaction, loyalty
```

### Response Biases (Предвзятости ответов)

#### Social Desirability Bias (Crowne & Marlowe, 1960)
```
Проблема: Стремление выглядеть лучше в глазах других
Проявления:
- Завышение позитивного поведения
- Занижение негативного поведения
- Согласие с социально одобряемыми утверждениями

Минимизация:
- Анонимность responses
- Нейтральные формулировки
- Normalization (показать что "негативные" ответы нормальны)
- Косвенные вопросы
- Forced-choice items
```

#### Acquiescence Bias (Согласие)
```
Проблема: Тенденция соглашаться с утверждениями
Проявления:
- Выбор "Да" чаще чем "Нет"
- Выбор "Согласен" чаще

Минимизация:
- Balanced scales
- Reverse-coded items
- Forced-choice formats
```

#### Extreme Response Bias
```
Проблема: Выбор крайних значений шкалы
Минимизация:
- Расширение шкалы (7 вместо 5)
- Указание средних значений как оптимальных
```

#### Central Tendency Bias
```
Проблема: Избегание крайних значений
Минимизация:
- Forced ranking
- Ipsative measures
```

### UX Research Best Practices

#### Тайминг обратной связи

**Immediate Feedback**
```
Когда: Сразу после опыта (within 5 минут)
Преимущества:
- Высокая точность recall
- Свежие эмоции
- Высокий response rate

Недостатки:
- Эмоциональная реактивность
- Меньше времени на рефлексию

Применение: Event-based feedback, post-activity ratings
```

**Delayed Feedback**
```
Когда: Через несколько часов/дней
Преимущества:
- Больше рефлексии
- Меньше эмоциональной предвзятости
- Видны отложенные эффекты

Недостатки:
- Ниже response rate
- Recall bias

Применение: Program evaluation, long-term impact
```

#### Принципы дизайна форм

**Краткость**
```
Правило: <3 минуты заполнения
Обоснование: Каждая дополнительная минута снижает completion на ~10%
Оптимум: 5-7 вопросов максимум
```

**Progressive Disclosure**
```
Показывать по одному вопросу за раз
Преимущества:
- Меньше overwhelm
- Выше focus
- Легче на mobile

Когда использовать: Long forms, sensitive topics
```

**Progress Indicators**
```
Показывать: "Вопрос 3 из 5" или progress bar
Эффект: Повышает completion rate на 15-20%
```

**Clear Error Messages**
```
Плохо: "Ошибка в форме"
Хорошо: "Пожалуйста, выберите хотя бы один вариант"
```

### Поведенческая аналитика

#### Паттерны кризисных состояний

**Экстремально низкие оценки**
```
Pattern: Score <= 3 на multiple вопросах (3+ вопросов)
Confidence: 0.7-0.8
Action: Send support message, monitor next responses
```

**Ключевые слова риска**
```
Критические:
- "хочу умереть"
- "не вижу смысла жить"
- "покончить с собой"

Высокий риск:
- "безнадежно"
- "не могу больше"
- "хочу закончить это"
- "нет выхода"

Action: Immediate escalation, crisis resources
```

**Резкое снижение показателей**
```
Pattern: Снижение на >30% за короткий период (3-5 дней)
Confidence: 0.6-0.7
Action: Check-in message, additional support
```

**Contradictory Responses**
```
Pattern: Inconsistent ответы на связанные вопросы
Возможные причины:
- Rushed completion
- Confusion
- Попытка скрыть истинное состояние

Action: Follow-up questions, clarification
```

#### Engagement Metrics

**Completion Rate**
```
Excellent: >80%
Good: 60-80%
Poor: <60%

Факторы влияния:
- Длина формы
- Timing
- Relevance
- Incentives
```

**Response Quality**
```
Индикаторы high quality:
- Thoughtful open-text responses (>20 words)
- Consistent patterns
- Appropriate time spent (не rushed)

Индикаторы low quality:
- Straight-lining (все одинаковые ответы)
- Gibberish text
- Too fast completion
```

### Триггерные правила и маршрутизация

#### Структура триггера

```
IF [condition] THEN [action] WITH [params]

Condition: Boolean expression на основе ответов
Action: Предопределенное действие
Params: Параметры действия
Priority: Уровень приоритета (1-10)
```

#### Примеры триггеров

**Low Satisfaction Trigger**
```python
IF satisfaction_score <= 2 THEN
  ACTION: send_support_message
  PARAMS:
    template: "support_low_satisfaction"
    delay_hours: 2
    personalization: True
  PRIORITY: 8
```

**High Difficulty Trigger**
```python
IF difficulty_score >= 8 THEN
  ACTION: adjust_difficulty
  PARAMS:
    adjustment: "reduce"
    percentage: 20
    notify_user: True
  PRIORITY: 7
```

**Crisis Detection Trigger**
```python
IF wellbeing_score <= 3 OR crisis_keywords_detected THEN
  ACTION: escalate_to_professional
  PARAMS:
    urgency: "high"
    notify_team: True
    resources: ["crisis_hotline", "emergency_contacts"]
    auto_followup: 24_hours
  PRIORITY: 10
```

**Success Celebration Trigger**
```python
IF (satisfaction >= 4 AND consistency_high) THEN
  ACTION: celebrate_success
  PARAMS:
    celebration_type: "personalized"
    next_step_hint: True
    badge_unlock: check_eligibility
  PRIORITY: 5
```

### Actionable Insights Framework

#### Критерии действенности

**Specific (Конкретный)**
```
Плохо: "Улучшить контент"
Хорошо: "Добавить 2 дополнительных примера в модуль Day 5"
```

**Measurable (Измеримый)**
```
Плохо: "Сделать проще"
Хорошо: "Снизить avg_difficulty с 7.5 до 6.0"
```

**Achievable (Выполнимый)**
```
Требует: Доступные ресурсы + reasonable effort
```

**Relevant (Релевантный)**
```
Aligned with: Program goals + user needs
```

**Time-bound (Ограниченный во времени)**
```
Immediate: < 1 week
Short-term: 1-4 weeks
Long-term: 1-3 months
```

## Интеграция с PatternShift

### Модульная структура

**Feedback Module** содержит:
- Форма обратной связи (5-7 вопросов)
- Триггерные правила
- Crisis detection механизмы
- Actionable insights генератор

**Timing**:
- End-of-module: Immediate feedback после модуля
- End-of-day: Daily check-in
- Mid-program: Промежуточная оценка (Day 10-11)
- End-of-program: Final evaluation (Day 21)

### Метрики эффективности

**Completion Rate:** >85%
**Response Quality:** High (thoughtful, consistent)
**Actionability:** Каждый feedback ведет к concrete action
**Crisis Detection Accuracy:** >80% (балансировка false positives/negatives)

## Контекстные файлы

- `D:\\Automation\\Development\\projects\\patternshift\\docs\\content-agents-system-prompts.md` (раздел 8: FEEDBACK ORCHESTRATOR AGENT)
- `D:\\Automation\\Development\\projects\\patternshift\\docs\\final-kontent-architecture-complete.md`

## Теги для Archon Knowledge Base

Рекомендуемые теги при загрузке в Archon:
- `pattern-feedback`
- `psychometrics`
- `ux-research`
- `behavioral-analytics`
- `crisis-detection`
- `agent-knowledge`
- `patternshift`
