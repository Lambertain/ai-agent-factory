# Pattern Progress Narrator Agent

Специализированный Pydantic AI агент для создания нарративов прогресса и трансформации в рамках системы PatternShift.

## 🎯 Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль мастера сторителлинга

⚠️ **СПЕЦИАЛИЗАЦИЯ:** Это Pattern агент для проекта PatternShift, НЕ универсальный агент. Работает с нарративами прогресса, мотивацией и Hero's Journey.

## 🧠 Как использовать агента

### Активация роли согласно D:\Automation\CLAUDE.md

Агент активируется через локальный поиск промпта в репозитории:

```
🔍 Ищу промпт роли Pattern Progress Narrator...
📁 Поиск через: Glob(**/*pattern*progress*knowledge*.md)
📖 Читаю системный промпт роли...

🎭 ПЕРЕКЛЮЧЕНИЕ В РОЛЬ PATTERN PROGRESS NARRATOR

Моя экспертиза:
- Storytelling и нарративные техники (Hero's Journey)
- Мотивационная психология (Self-Determination Theory)
- Framing и reframing техники
- Метафоры трансформации
- Momentum building и поддержание
- Anticipation creation и curiosity hooks

✅ Готов создавать нарративы прогресса
```

### Запрос от пользователя:

```
Прими роль Pattern Progress Narrator и создай мотивирующее сообщение для Day 10.
```

### Пример работы с нарративом прогресса:

После принятия роли передайте Claude запрос на создание нарратива:

```
Создай нарратив прогресса для пользователя на Day 10 программы.
Данные прогресса:
- Consistency: 85%
- Completed modules: 9/10
- Engagement level: высокий
- Challenges: испытывал сложности с meditation модулем
```

## 📋 Что делает агент

### Входные данные:
- День программы (1-21)
- Метрики прогресса пользователя (consistency, engagement, completion)
- Достигнутые вехи
- Challenges и difficulties
- Персональные данные (имя, предпочтения)

### Выходные данные:
- **Progress Narratives** - мотивирующие нарративы прогресса
- **Challenge Reframes** - рефрейминг неудач в научение
- **Momentum Messages** - сообщения для поддержания импульса
- **Anticipation Builders** - создание предвкушения следующих этапов
- **Hero Journey Mapping** - mapping пользователя на путь героя

## 🔧 Структура агента

```
pattern_progress_narrator/
├── agent.py                    # Основной Pydantic AI агент
├── tools.py                    # Инструменты создания нарративов
├── dependencies.py             # Зависимости и типы данных
├── prompts.py                  # Системные промпты
├── settings.py                 # Конфигурация агента
├── models.py                   # Pydantic модели данных
├── knowledge/
│   └── pattern_progress_narrator_knowledge.md  # База знаний
├── __init__.py                 # Экспорты
└── README.md                   # Документация
```

## 🚀 Программное использование (Pydantic AI)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Быстрый старт

```python
from pattern_progress_narrator import run_pattern_progress_narrator

# Простой пример создания нарратива прогресса
result = await run_pattern_progress_narrator(
    "Создай мотивирующий нарратив для Day 15",
    api_key="your_api_key"
)

print(result)
```

### Продвинутое использование

```python
from pattern_progress_narrator.agent import agent
from pattern_progress_narrator.dependencies import PatternProgressNarratorDependencies
from pattern_progress_narrator.tools import create_progress_narrative, reframe_challenge

# Создание зависимостей
deps = PatternProgressNarratorDependencies(
    api_key="your_api_key",
    patternshift_project_path="/path/to/patternshift",
    user_name="Alex",
    day_number=10
)

# Прямой вызов инструмента создания нарратива
from pydantic_ai import RunContext
result = await create_progress_narrative(
    ctx=RunContext(deps=deps),
    narrative_type="milestone_celebration",
    day_number=10,
    progress_data={
        "metrics": [
            {"metric_name": "Consistency", "improvement_percentage": 50}
        ],
        "hero_journey_stage": "tests_allies_enemies",
        "next_action": "Continue to Day 11"
    },
    emotional_tone="celebratory"
)

print(result)
```

## 🛠️ Доступные инструменты

### Основные инструменты создания нарративов

- `create_progress_narrative()` - Создание нарратива прогресса (Hero Journey, transformation, celebration)
- `reframe_challenge()` - Рефрейминг вызовов/неудач в learning opportunities
- `generate_momentum_message()` - Генерация сообщений для поддержания импульса
- `create_anticipation_builder()` - Создание предвкушения следующих этапов
- `search_agent_knowledge()` - Поиск best practices в базе знаний

### Инструменты коллективной работы

- `break_down_to_microtasks()` - Разбивка задачи на микрозадачи
- `report_microtask_progress()` - Отчетность о прогрессе
- `reflect_and_improve()` - Рефлексия и улучшение
- `check_delegation_need()` - Проверка необходимости делегирования
- `delegate_task_to_agent()` - Делегирование задач через Archon

## 📚 База знаний содержит:

- **Системный промпт** из PatternShift системы (PROGRESS NARRATOR AGENT)
- **Hero's Journey** - структура мономифа Joseph Campbell
- **Self-Determination Theory** - автономия, компетентность, связь (Deci & Ryan)
- **Goal Progress Theory** - feedback loops и proximity effects (Carver & Scheier)
- **Small Wins Theory** - series малых побед для momentum (Weick)
- **Framing Effects** - позитивный фрейминг vs негативный (Kahneman & Tversky)
- **Narrative Identity Theory** - создание личной истории (McAdams)
- **Metaphor Theory** - терапевтические метафоры (Lakoff & Johnson)
- **Momentum Psychology** - что создает и разрушает импульс
- **Anticipation & Curiosity** - Zeigarnik effect, curiosity gap

## 🎨 Примеры использования

### Пример 1: Milestone Celebration (Day 7)

**Исходный запрос:**
```
Создай празднование вехи для завершения первой недели
День: 7
Consistency: 90%
Completed: 7/7 modules
```

**Результат:**
```
🎉 День 7: Первая Веха Позади!

Alex, ты сделал это! Целая неделя трансформации. Знаешь что это значит?

**Твой прогресс в цифрах:**
- Consistency: 90% (это выше среднего!)
- Завершено: 7 из 7 модулей

**Где ты сейчас на пути героя:**
Пересечение порога - ты официально committed к изменениям. Обычный мир позади.

**Что это значит:**
Первая неделя - самая сложная. Ты преодолел initial resistance, показал силу воли.
Статистика: 80% людей не доходят до Day 7. Ты в топ 20%. Это впечатляет.

**Впереди:**
Следующая неделя - самая интересная. Ты начнешь видеть реальные изменения в своей жизни.

Momentum теперь работает на тебя! 🚀
```

### Пример 2: Challenge Reframe (Struggle с упражнением)

**Исходный запрос:**
```
Рефреймируй: "Не смог выполнить медитацию 10 минут, отвлекался постоянно"
```

**Результат:**
```
🔄 Рефрейминг вызова

**Оригинал:** Не смог выполнить медитацию 10 минут, отвлекался постоянно

**Рефреймированная перспектива:**

1. **Признание:** Я понимаю, что не смог выполнить медитацию 10 минут, отвлекался постоянно было непросто.

2. **Нормализация:** Это нормальная часть процесса трансформации.
   Факт: 95% начинающих медитировать испытывают то же самое.
   Отвлечения - это не failure, это показатель того, как работает необученный ум.

3. **Извлечение научения:**
   Ты узнал важное: твои триггеры отвлечения, паттерны мыслей, когда focus уходит.
   Осознание отвлечения - ЭТО и есть медитация!

4. **Идентификация роста:**
   Теперь ты знаешь, что 10 минут - challenging. Значит, начнем с 3 минут и будем расти.

5. **Следующее действие:**
   Завтра: 3 минуты медитации. Focus на возвращении внимания, не на избегании отвлечений.

**Новый фрейм:**
"Не удалось медитировать" → "Я научился наблюдать свои отвлечения - это ключевой навык!"

💡 **Помни:** Мастерство приходит через практику, не через perfect execution.
```

### Пример 3: Momentum Message (Consistency падает)

**Исходный запрос:**
```
Генерируй momentum message
Consistency: 45%
Engagement: 40%
Completion: 50%
```

**Результат:**
```
💪 Время перезапустить momentum

Я вижу, было challenging последнее время (consistency: 45%).

**Хорошие новости:**
Momentum можно восстановить. Всё, что нужно - начать again.

**Почему это происходит:**
Momentum - это физический принцип. Когда останавливаешься, нужна energy чтобы начать снова.
Это нормально. Это не говорит ничего о тебе - только о physics of behavior change.

**Твой план восстановления:**
1. Выбери САМОЕ простое упражнение из программы
2. Сделай его сегодня (даже если 2 минуты)
3. Повтори завтра
4. Momentum начнет возвращаться на Day 3

**Помни:**
Ты не начинаешь с нуля. Все previous learning с тобой. Нейронные пути уже созданы.
Просто нужно активировать их снова.

**Следующий шаг:**
Прямо сейчас: открой самый короткий модуль и просто начни. Не думай, просто действуй.

Я верю в тебя. Ты уже показывал что можешь. Покажи еще раз. 💪

**Твои показатели momentum:**
- Consistency: 45% (начнем отсюда)
- Engagement: 40% (будет расти)
- Completion: 50% (половина - это старт)

Momentum level: 45% - В процессе восстановления. Один шаг сейчас = запуск!
```

### Пример 4: Anticipation Builder (Preview Day 11)

**Исходный запрос:**
```
Создай anticipation для следующего дня
Current day: 10
Upcoming: "Advanced Visualization Technique"
```

**Результат:**
```
🔮 Что тебя ждет впереди

**Следующий шаг: Day 11**
Advanced Visualization Technique - Создание будущего в уме

**Почему это важно:**
За последние 10 дней ты освоил базовые навыки. Day 11 - это level up.
Ты будешь работать с техникой, которую используют олимпийские атлеты и top performers.

**Предвкушение:**
🎯 Середина программы близко - время самых мощных трансформаций

**Интрига:**
Помнишь breathwork с Day 5 и mindfulness с Day 8?
Завтра они соединятся с visualization - и произойдет something magical.
Ты сможешь буквально "программировать" свой мозг на желаемое будущее.

Но я не буду спойлерить детали. Это нужно испытать. 😊

**Еще впереди:**
- 11 дней трансформационного путешествия
- Интеграция всех навыков в систему
- Moments инсайтов, которые изменят твое понимание себя
- Версия тебя, которая уже существует в potential - waiting to emerge

**Твой следующий move:**
Отдохни сегодня. Celebrate Day 10. Завтра тебя ждет adventure.

✨ Лучшее еще впереди!
```

## 🔗 Связь с PatternShift

Агент использует контекстную информацию из:
- `D:\Automation\Development\projects\patternshift\docs\content-agents-system-prompts.md` (раздел 9: PROGRESS NARRATOR AGENT)
- `D:\Automation\Development\projects\patternshift\docs\final-kontent-architecture-complete.md`

## ⚠️ Важные принципы

- **Show, don't tell** - показывать прогресс через конкретные примеры
- **Personalization** - использовать имя, личные детали, specific achievements
- **Emotional resonance** - matching emotional state, validation опыта
- **Action orientation** - всегда указывать следующий конкретный шаг
- **Momentum awareness** - понимание psychology импульса
- **Anticipation building** - создание curiosity и предвкушения
- **Framing mastery** - positive framing, reframing failures как learning

## 📚 Загрузка в Archon Knowledge Base

После создания агента загрузите файл знаний:

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_progress_narrator_knowledge.md`
4. Добавьте теги:
   - `pattern-progress-narrator`
   - `storytelling`
   - `motivation`
   - `hero-journey`
   - `agent-knowledge`
   - `patternshift`

## 🚀 Быстрый старт

1. Запросите роль: "Прими роль Pattern Progress Narrator"
2. Claude найдет промпт через локальный Glob поиск
3. Передайте запрос: "Создай нарратив прогресса для Day [X]"
4. Получите мотивирующий нарратив с framing достижений и next steps

---

*Pattern Progress Narrator Agent - создание трансформационных нарративов для системы PatternShift*
