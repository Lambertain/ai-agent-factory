# Pattern Gamification Architect Agent - Knowledge Base

## 📚 Общие правила для всех агентов

**ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:** Прочитай [Общие правила агентов](../_shared/agent_common_rules.md)

Все агенты следуют единым правилам workflow, качества и взаимодействия. Общие правила содержат:
- ✅ Переключение в роль (обязательно)
- ✅ Workflow и приоритизация
- ✅ Управление задачами (Archon + TodoWrite)
- ✅ Git интеграция и стандарты кодирования
- ✅ Post-Task Checklist (последний пункт каждой задачи)
- ✅ Протоколы анализа проблем и эскалации
- ✅ Заборона ярликів та токен-економії

---

## 🎭 СИСТЕМНЫЙ ПРОМПТ РОЛИ: Pattern Gamification Architect Agent

**Ты - Pattern Gamification Architect Agent**, эксперт в [ОБЛАСТЬ ЭКСПЕРТИЗЫ].

### ⚠️ ОБЯЗАТЕЛЬНО ПЕРЕД НАЧАЛОМ РАБОТЫ:
**ПРОЧИТАЙ:** [`agent_common_rules.md`](../_shared/agent_common_rules.md) - содержит критически важные правила workflow, качества и эскалации.

## Системный промпт

Ты - эксперт по геймификации с глубоким пониманием поведенческой психологии, game design и мотивационных систем.

Ты знаешь как превратить терапевтический процесс в engaging journey без потери серьезности. Твои системы достижений meaningful и связаны с реальными изменениями. Ты мастерски балансируешь между внешней и внутренней мотивацией.

Ты понимаешь разные типы игроков (Bartle taxonomy: Achievers, Explorers, Socializers, Killers) и создаешь multiple paths to success. Твои механики простые но addictive в позитивном смысле.

Ты знаешь как использовать социальные элементы без создания негативного сравнения. Твоя геймификация поддерживает терапевтические цели, а не отвлекает от них. Ты мастер создания epic meaning в процессе личной трансформации.

---

## 1. Self-Determination Theory (SDT) - Основа мотивации

**Deci & Ryan, 1985 - Теория самоопределения**

### Три базовые психологические потребности:

#### 1.1 Autonomy (Автономия)
- **Определение:** Чувство выбора и контроля над своими действиями
- **В геймификации:**
  - Множественные пути к цели
  - Выбор челленджей
  - Кастомизация опыта
  - Opt-in социальные функции

#### 1.2 Competence (Компетентность)
- **Определение:** Чувство мастерства и эффективности
- **В геймификации:**
  - Постепенное увеличение сложности
  - Четкая обратная связь о прогрессе
  - Достижения за мастерство
  - Уровни и progression

#### 1.3 Relatedness (Связанность)
- **Определение:** Чувство принадлежности и связи с другими
- **В геймификации:**
  - Опциональные социальные функции
  - Sharing достижений
  - Community challenges
  - Peer support (но не сравнение)

### Применение в PatternShift:
```
Autonomy: Пользователь выбирает когда и как выполнять модули
Competence: Система badges показывает рост мастерства
Relatedness: Опция поделиться инсайтами с комьюнити
```

---

## 2. Flow Theory - Оптимальное состояние вовлеченности

**Csikszentmihalyi, 1990 - Теория потока**

### Условия для Flow:
1. **Clear Goals** - Ясные цели на каждом этапе
2. **Immediate Feedback** - Мгновенная обратная связь
3. **Challenge-Skill Balance** - Баланс сложности и навыков

### Flow Channel:
```
Сложность
    ^
    |     ANXIETY
    |        /
    |       /  FLOW CHANNEL
    |      / /
    |     / /
    | APATHY
    +-------------> Навыки
```

### В геймификации PatternShift:
- **День 1-3:** Легкие задачи (tutorial) - building skills
- **День 4-7:** Постепенное усложнение - entering flow
- **День 8-14:** Peak challenge matching skills - optimal flow
- **День 15-21:** Mastery level challenges - flow maintenance

**Ключ:** Адаптивная сложность под текущий уровень пользователя

---

## 3. Bartle's Player Types - Типология игроков

**Bartle, 1996 - Таксономия игроков**

### 4 основных типа:

#### 3.1 Achievers (Достигаторы) - 10-15% пользователей
**Мотивация:** Достижение целей, accumulation, status
**Предпочитают:**
- Points и scores
- Badges и trophies
- Levels и progression
- Leaderboards (осторожно!)
- Clear milestones

**Для них создаем:**
```python
{
  "points_system": "Accumulation of transformation points",
  "badges": "Tiered achievements (bronze, silver, gold)",
  "levels": "Clear progression path 1-5",
  "milestones": "Visible checkpoints every 3 days"
}
```

#### 3.2 Explorers (Исследователи) - 10% пользователей
**Мотивация:** Discovery, knowledge, hidden content
**Предпочитают:**
- Unlockable content
- Easter eggs
- Bonus materials
- Deep dives
- Secrets

**Для них создаем:**
```python
{
  "unlocks": "Advanced techniques after mastery",
  "bonus_content": "Hidden insights for curious",
  "discovery_paths": "Alternative ways to complete",
  "deep_content": "Extended theory for interested"
}
```

#### 3.3 Socializers (Социализаторы) - 80% пользователей
**Мотивация:** Connection, sharing, relationships
**Предпочитают:**
- Sharing mechanisms
- Community features
- Co-op challenges
- Social recognition

**Для них создаем (opt-in):**
```python
{
  "sharing": "Share insights (but not compare)",
  "community": "Support groups (moderated)",
  "recognition": "From peers, not ranking",
  "co-op": "Partner challenges (optional)"
}
```

#### 3.4 Killers (Конкуренты) - 1% пользователей
**Мотивация:** Competition, domination, winning
**Предпочитают:**
- PvP elements
- Rankings
- Competitive challenges

**Осторожно в терапии!**
- НЕ создаем публичных rankings
- Если competition - только vs self (beat your best)
- Фокус на personal bests, не на beating others

### Multiple Paths Strategy:
Создаем систему где КАЖДЫЙ тип игрока находит свой path to success:
- Achievers → Points & Badges path
- Explorers → Discovery & Unlock path
- Socializers → Community & Sharing path
- Killers → Self-competition & Mastery path

---

## 4. Operant Conditioning - Системы подкрепления

**Skinner, 1953 - Оперантное обусловливание**

### Типы подкрепления:

#### 4.1 Fixed Ratio (FR)
- Награда после фиксированного числа действий
- Пример: "Каждые 5 выполненных упражнений = badge"
- **Плюсы:** Предсказуемость, ясность
- **Минусы:** Может быть скучным

#### 4.2 Variable Ratio (VR)
- Награда после переменного числа действий
- Пример: "Случайные bonus points за insights"
- **Плюсы:** Наиболее addictive
- **Минусы:** Может казаться несправедливым
- **⚠️ ОСТОРОЖНО:** Не злоупотреблять в терапии!

#### 4.3 Fixed Interval (FI)
- Награда через фиксированные промежутки времени
- Пример: "Daily rewards за логин"
- **Плюсы:** Создает routine
- **Минусы:** Activity spike перед наградой

#### 4.4 Variable Interval (VI)
- Награда через переменные промежутки
- Пример: "Surprise bonus content"
- **Плюсы:** Поддерживает постоянную активность
- **Минусы:** Непредсказуемость

### Рекомендация для PatternShift:
**Комбинируем:**
- **FR** для основных достижений (предсказуемость)
- **FI** для daily routines (consistency)
- **VR/VI осторожно** для surprise bonuses (excitement)

**НИКОГДА не делаем награды манипулятивными!**

---

## 5. Yerkes-Dodson Law - Оптимальное давление

**Yerkes & Dodson, 1908**

### Закон:
```
Performance = f(Arousal)

Но: Too little arousal → Boredom
     Optimal arousal → Peak performance
     Too much arousal → Anxiety
```

### В геймификации:
- **Слишком легко:** Boring, no engagement
- **Оптимально:** Challenging but achievable
- **Слишком сложно:** Frustrating, quit

### Применение:
```python
difficulty_curve = {
    "week_1": "Tutorial - очень легко",
    "week_2": "Building momentum - умеренно",
    "week_3": "Peak challenge - сложно но achievable"
}

# Адаптивная сложность:
if user_struggling:
    offer_easier_path()
if user_bored:
    offer_bonus_challenge()
```

---

## 6. Goal-Setting Theory - Теория постановки целей

**Locke & Latham, 1990**

### Характеристики эффективных целей (SMART):

#### S - Specific (Конкретные)
- ❌ "Будь лучше"
- ✅ "Выполни технику рефрейминга 3 раза эту неделю"

#### M - Measurable (Измеримые)
- Progress bars
- Point systems
- Completion percentages

#### A - Achievable (Достижимые)
- Не слишком легко, не слишком сложно
- Учитывать текущий уровень

#### R - Relevant (Релевантные)
- Связаны с терапевтическими целями
- Meaningful для пользователя

#### T - Time-bound (Ограниченные во времени)
- Daily goals
- Weekly milestones
- 21-day completion

### В геймификации:
```python
daily_goal = {
    "specific": "Complete today's NLP technique module",
    "measurable": "100% completion = 50 points",
    "achievable": "15-20 minutes required",
    "relevant": "Advances transformation goal",
    "time_bound": "Today (24 hours)"
}
```

---

## 7. Progress Bar Effect - Психология завершенности

**Kivetz et al., 2006 - Goal-Gradient Hypothesis**

### Феномен:
Чем ближе к завершению, тем сильнее мотивация завершить.

### Эффект endowed progress:
Если дать "стартовый бонус" - люди более мотивированы завершить.

**Пример:**
- ❌ "Пройдите 10 модулей для badge"
- ✅ "Пройдите еще 8 модулей (2 уже зачтены как welcome bonus!)"

### Применение:
```python
# Progress bars everywhere!
program_progress = "Day 5 of 21 (24% complete)"
weekly_progress = "4 of 7 days completed this week"
technique_mastery = "2 of 3 perfect executions (66%)"

# Endowed progress:
"You've already earned 50 points (welcome bonus)!
 Earn 50 more to unlock next level!"
```

### Визуальные паттерны:
```
[=========>           ] 40%  ← Clear, motivating
[■■■■■■■■■□□□□□□□□□□□] 9/20 ← Concrete
Day 7/21 ⭐⭐⭐⭐⭐⭐⭐     ← Celebratory
```

---

## 8. Loss Aversion - Избегание потерь

**Kahneman & Tversky, 1979 - Prospect Theory**

### Принцип:
Люди сильнее мотивированы избежать потери, чем получить приобретение.

### ⚠️ ОСТОРОЖНО в терапии!

#### НЕ делаем:
- ❌ "Вы потеряли 3-дневную серию!"
- ❌ "Отнимаем points за пропуск"
- ❌ "Streak reset to zero"

#### Делаем правильно:
- ✅ "Ваша серия: 7 дней. Продолжайте сегодня?"
- ✅ "Bonus points for maintaining streak!"
- ✅ "Grace period: you have 24h to keep streak"

### Позитивное фрейминг:
```python
# Вместо punishment используем positive framing:
missed_day_message = """
Мы заметили что вы пропустили вчера.
Это нормально - жизнь бывает непредсказуемой.

Хорошая новость: ваши 50 points сохранены!
Сегодня отличный день чтобы продолжить.
Готовы?
"""
```

---

## 9. Zeigarnik Effect - Эффект незавершенности

**Zeigarnik, 1927**

### Феномен:
Незавершенные задачи лучше запоминаются и создают психологическое напряжение к завершению.

### В геймификации:
```python
# Показываем незавершенное:
"Today's progress: 2 of 3 modules completed ⚪⚪⚫"

# Создаем open loops:
"Tomorrow unlocks: Advanced Reframing Technique 🔒"

# Cliffhangers между днями:
"Great progress today!
 Tomorrow we'll discover how this connects to..."
```

### Но осторожно:
- НЕ создавать тревогу
- Всегда давать closure option
- Balance между anticipation и stress

---

## 10. Social Proof - Социальное доказательство

**Cialdini, 1984 - Influence**

### Принцип:
Люди смотрят на действия других чтобы определить правильное поведение.

### Безопасное применение:
```python
# ДА:
"Join 10,000+ people on transformation journey"
"Most popular technique this week: Reframing"
"Sarah shared: 'This exercise changed my perspective'"

# НЕТ:
"You're in bottom 10% of users"  # Негативное сравнение!
"John has 500 more points than you"  # Harmful competition!
```

### Community без сравнения:
- Показываем collective achievements
- Sharing insights (opt-in)
- Peer support
- НО: никогда публичных rankings

---

## 11. Peak-End Rule - Правило пика-конца

**Kahneman, 1993**

### Принцип:
Люди судят опыт по:
1. Самому интенсивному моменту (peak)
2. Финальному моменту (end)

### В 21-дневной программе:
```python
peak_moments = [
    "Day 7: First major achievement badge",
    "Day 14: Breakthrough insight celebration",
    "Day 21: Epic transformation completion"
]

end_experience = {
    "celebration": "Massive congratulations",
    "review": "Look how far you've come",
    "gift": "Bonus content unlock",
    "continuation": "What's next pathway"
}
```

### Design peaks intentionally:
- Week 1 peak: "First week warrior" badge
- Week 2 peak: Major technique mastery
- Week 3 peak: Integration breakthrough
- Final peak: Epic completion ceremony

---

## 12. Практические паттерны геймификации

### 12.1 Points System Design

**Earning points:**
```python
points = {
    "module_complete": 50,
    "exercise_done": 25,
    "insight_recorded": 40,
    "technique_mastery": 100,
    "daily_login": 10,
    "consistency_bonus": 20,  # 3+ days in row
    "perfect_day": 150  # All activities
}
```

**Point redemption (optional):**
- Unlock bonus content
- Customize experience
- Access advanced techniques

### 12.2 Badge System Design

**Типы badges:**
```python
badges = {
    "completion": ["First step", "Week 1 done", "Halfway", "Complete"],
    "consistency": ["3-day streak", "Week streak", "21-day warrior"],
    "mastery": ["Technique master", "Insight seeker", "Reflection pro"],
    "breakthrough": ["First aha", "Pattern breaker", "Transformer"],
    "special": ["Night owl", "Early bird", "Weekend warrior"]
}
```

**Rarity levels:**
- Common (80%): Everyone can get
- Rare (40%): Require effort
- Epic (10%): Significant achievement
- Legendary (1%): Exceptional completion

### 12.3 Level System Design

**5-level progression:**
```python
levels = [
    {
        "level": 1,
        "name": "Awakening",
        "points_required": 0,
        "unlocks": ["Basic techniques"],
        "meaning": "Beginning awareness"
    },
    {
        "level": 2,
        "name": "Seeker",
        "points_required": 500,
        "unlocks": ["Intermediate techniques"],
        "meaning": "Active exploration"
    },
    {
        "level": 3,
        "name": "Practitioner",
        "points_required": 1200,
        "unlocks": ["Advanced techniques"],
        "meaning": "Regular practice"
    },
    {
        "level": 4,
        "name": "Adept",
        "points_required": 2500,
        "unlocks": ["Master techniques", "Bonus content"],
        "meaning": "Deep integration"
    },
    {
        "level": 5,
        "name": "Transformed",
        "points_required": 5000,
        "unlocks": ["All content", "Mentor pathway"],
        "meaning": "Complete transformation"
    }
]
```

### 12.4 Quest System Design

**Daily quests:**
```python
daily_quest = {
    "title": "Today's Transformation",
    "tasks": [
        "Complete main module",
        "Do practice exercise",
        "Record one insight"
    ],
    "reward": "150 points + daily badge"
}
```

**Weekly quests:**
```python
weekly_quest = {
    "title": "Week of Growth",
    "tasks": [
        "Complete 5 of 7 daily quests",
        "Master one new technique",
        "Maintain 3-day streak"
    ],
    "reward": "500 points + rare badge"
}
```

**Epic quest (21-day):**
```python
epic_quest = {
    "title": "Transformation Journey",
    "chapters": [
        "Week 1: Foundation",
        "Week 2: Development",
        "Week 3: Integration"
    ],
    "reward": "Legendary badge + Certificate + Bonus program"
}
```

### 12.5 Feedback Loop Design

**Immediate feedback:**
- Points появляются instantly
- Animation при badge unlock
- Progress bar updates live
- Celebration micro-animations

**Delayed feedback:**
- Weekly summary email
- Progress reports at milestones
- Reflection prompts with data

**Periodic feedback:**
- Daily recap notification
- Weekly achievement digest
- Monthly transformation report

---

## 13. Anti-Patterns и что избегать

### 13.1 Dark Patterns - НИКОГДА!

❌ **Forced Social:**
- Не требовать sharing для progress
- Все социальное - opt-in

❌ **FOMO (Fear of Missing Out):**
- Не "Limited time only!" на критическом контенте
- Не "Others are ahead of you!"

❌ **Punitive Mechanics:**
- Не отнимать points
- Не reset progress агрессивно
- Не shame за пропуски

❌ **Pay-to-Win:**
- Не давать преимуществ за деньги
- Все могут достичь всего

❌ **Addictive Manipulation:**
- Не abuse Variable Ratio schedules
- Не создавать compulsive checking
- Баланс engagement и wellbeing

### 13.2 Harmful Competition

❌ **Public Rankings:**
```python
# НЕ ДЕЛАТЬ:
leaderboard = {
    "1. John - 5000 points",
    "2. Sarah - 4800 points",
    "...",
    "847. You - 200 points"  # Демотивирующе!
}
```

✅ **Personal Progress:**
```python
# ПРАВИЛЬНО:
personal_stats = {
    "Your progress": "Level 2 (500 points)",
    "This week": "+250 points (great!)",
    "Your best": "Perfect day on Day 5",
    "Community": "Part of 10k+ transformers"
}
```

### 13.3 Overwhelming Complexity

❌ Слишком много механик одновременно
❌ Сложные правила earning points
❌ Непонятные критерии badges

✅ Простота:
- 1-2 основные механики
- Ясные правила
- Интуитивный progress

---

## 14. Balancing Strategies

### 14.1 Difficulty Curve

```python
difficulty_progression = {
    "Days 1-3": {
        "challenge": "Tutorial level",
        "success_rate_target": "95%",
        "rewards": "Frequent, encouraging"
    },
    "Days 4-7": {
        "challenge": "Easy",
        "success_rate_target": "85%",
        "rewards": "Regular, building confidence"
    },
    "Days 8-14": {
        "challenge": "Medium",
        "success_rate_target": "70%",
        "rewards": "Substantial for effort"
    },
    "Days 15-20": {
        "challenge": "Hard",
        "success_rate_target": "60%",
        "rewards": "Significant achievements"
    },
    "Day 21": {
        "challenge": "Integration",
        "success_rate_target": "80%",
        "rewards": "Epic celebration"
    }
}
```

### 14.2 Reward Pacing

**Frequency:**
- Early (Days 1-7): Частые небольшие награды
- Middle (Days 8-14): Реже но больше
- Late (Days 15-21): Крупные за вехи

**Value:**
```python
reward_value = {
    "common_task": 25-50 points,
    "significant_task": 100-150 points,
    "major_milestone": 250-500 points,
    "epic_achievement": 1000+ points
}
```

### 14.3 Economy Balance

**Total points available:**
- Минимальное прохождение: ~1,500 points
- Среднее прохождение: ~3,000 points
- Полное прохождение: ~5,000+ points

**Level requirements:**
- Level 2: Достижимо за Week 1
- Level 3: Достижимо за Week 2
- Level 4-5: Требуют полного engagement

---

## 15. Measurement & Iteration

### Ключевые метрики:

**Engagement:**
- Daily Active Users (DAU)
- Session length
- Feature usage rates
- Return rate

**Progress:**
- Completion rates по дням
- Drop-off points
- Time to milestones
- Achievement unlock rates

**Satisfaction:**
- User ratings
- NPS score
- Feedback sentiment
- Feature requests

### A/B Testing Ideas:
```python
tests = [
    "Points value: 25 vs 50 за упражнение",
    "Badge rarity: 3 vs 4 уровня",
    "Feedback timing: immediate vs delayed",
    "Social features: opt-in vs opt-out"
]
```

### Итерация:
1. Launch MVP gamification
2. Collect data 2-4 weeks
3. Identify drop-off points
4. Test improvements
5. Roll out winners
6. Repeat

---

## Заключение

Геймификация терапевтического процесса - это искусство баланса между:
- **Engagement** и **Wellbeing**
- **Extrinsic rewards** и **Intrinsic motivation**
- **Challenge** и **Achievability**
- **Social** и **Personal**
- **Fun** и **Therapeutic depth**

Ключ успеха: ВСЕГДА поддерживай терапевтические цели, никогда не жертвуй ими ради engagement metrics.

Геймификация - это инструмент усиления трансформации, не замена самой трансформации.


---

## 🔍 ДОМЕННЫЕ ЗНАНИЯ: [ОБЛАСТЬ]

#### 1.1 Autonomy (Автономия)
#### 1.2 Competence (Компетентность)
#### 1.3 Relatedness (Связанность)
#### 3.1 Achievers (Достигаторы) - 10-15% пользователей
```python
#### 3.2 Explorers (Исследователи) - 10% пользователей
```python
#### 3.3 Socializers (Социализаторы) - 80% пользователей
```python
#### 3.4 Killers (Конкуренты) - 1% пользователей
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python
```python

---

**Версия:** 2.0 (Модульная архитектура)
**Дата рефакторинга:** 2025-10-14
**Автор рефакторинга:** Archon Blueprint Architect
