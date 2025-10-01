# Pattern Scientific Validator Agent

Специализированный Pydantic AI агент для научной валидации психологических техник в программах трансформации PatternShift.

## Назначение

Этот агент предназначен для:
1. **Программное использование** - полноценный Pydantic AI агент с инструментами и API
2. **Принятие роли экспертом** - Claude может принимать роль эксперта по научной валидации

СПЕЦИАЛИЗАЦИЯ: Это Pattern агент для проекта PatternShift. Обеспечивает evidence-based practice и безопасность всех психологических техник.

## Как использовать агента

### Активация роли

```
Прими роль Pattern Scientific Validator и проведи валидацию модуля cognitive restructuring.
```

## Что делает агент

### Входные данные:
- Описание модуля PatternShift
- Список техник
- Содержание модуля
- Целевые состояния (depression, anxiety, etc.)

### Выходные данные:
- **TechniqueValidation** - оценка доказательности каждой техники
- **SafetyCheck** - оценка безопасности для самопомощи
- **EthicalReview** - этическая проверка
- **EffectivenessMetrics** - метрики измерения эффективности
- **ValidationReport** - полный отчет с рекомендациями

## Примеры использования

### Пример 1: Валидация CBT техники

**Запрос:**
```
Провалидируй технику "Cognitive Restructuring" для модуля работы с негативными мыслями.
```

**Результат:**
```
✅ Technique Validation: Cognitive Restructuring

**Evidence Level:** Meta-analysis
**Validation Status:** Validated

**Supporting Research:**
- Hofmann et al. (2012): Effect size d=0.75 (large) - N=16,000+
- Butler et al. (2006): Effect size d=0.80 (large) - N=9,138

**Theoretical Foundation:**
Cognitive Behavioral Therapy - хорошо валидирован в множественных мета-анализах

**Safety Rating:** Safe
**Contraindications:**
- Активный психоз
- Severe суицидальная ideation

**Target Conditions:**
- Depression (эффективно)
- Anxiety (эффективно)
- Negative thinking patterns (эффективно)

**Self-Help Adaptation:**
Эффективность в самопомощи: d=0.60 (medium) - на 20% ниже чем с терапевтом, но значимый эффект

**Recommendations:**
- Добавить concrete examples для каждого шага
- Включить worksheet для structured practice
- Предоставить guided process audio
```

### Пример 2: Валидация NLP техники

**Запрос:**
```
Провалидируй технику "NLP Reframing" для модуля переосмысления проблем.
```

**Результат:**
```
⚠️ Technique Validation: NLP Reframing

**Evidence Level:** Expert opinion
**Validation Status:** Validated (с оговорками)

**Supporting Research:**
- Нет direct RCT для NLP reframing
- Theoretical overlap с CBT cognitive restructuring (validated)

**Theoretical Foundation:**
Механизм overlap с CBT cognitive restructuring (мета-анализы поддерживают CBT)

**Safety Rating:** Safe

**Required Disclosure:**
"Эта техника имеет ограниченную прямую научную поддержку. Механизм похож на cognitive restructuring из Cognitive Behavioral Therapy (validated), но специфическая эффективность NLP reframing не доказана в RCT."

**Recommendations:**
1. Добавить disclosure об ограниченной evidence base
2. Упомянуть validated альтернативу (CBT cognitive restructuring)
3. Снизить claims - заменить "доказано работает" на "может помочь"
4. Добавить "Индивидуальные результаты могут vary"

**After Revisions:** Можно использовать с appropriate disclaimers
```

### Пример 3: Safety Check модуля

**Запрос:**
```
Проведи safety check для модуля "Deep Emotional Processing".
```

**Результат:**
```
⚠️ Safety Check: Deep Emotional Processing Module

**Overall Safety Rating:** Requires Professional Supervision

**Potential Risks:**
- Интенсивная эмоциональная работа без надзора
- Риск overwhelming emotions
- Возможность re-traumatization для trauma survivors

**Contraindications:**
- Severe trauma / PTSD (требуется профессиональный надзор)
- Активный психоз
- Активные суицидальные мысли
- Recent traumatic event (менее 3 месяцев)

**Risk Mitigation Strategies:**
1. Добавить grounding techniques перед intensive work
2. Предоставить clear stopping rules
3. Включить emergency contacts
4. Рекомендовать начинать с gentle version
5. Требовать professional consultation для trauma history

**Warning Signs для немедленной остановки:**
- Усиление суицидальных мыслей
- Появление диссоциативных симптомов
- Uncontrollable emotional distress
- Flashbacks или intrusive memories

**Emergency Protocol:**
"Если вы испытываете любой из warning signs - немедленно прекратите упражнение и обратитесь:
- Crisis Hotline: [номер]
- Therapist: [как найти]
- Emergency Room: при acute distress"

**Recommendation:** Модуль требует значительной revision для безопасного self-help использования. Рассмотрите gentler alternative approaches.
```

### Пример 4: Ethical Review модуля

**Запрос:**
```
Проведи ethical review модуля "21-Day Transformation Guarantee".
```

**Результат:**
```
❌ Ethical Review: 21-Day Transformation Guarantee

**Ethical Approval:** NO - требуется revision

**Ethical Concerns:**
1. **Overclaiming efficacy** - "Guarantee" нарушает принцип честности
2. **Informed consent inadequate** - не раскрыты limitations и realistic expectations
3. **Autonomy questionable** - использует "must" вместо "can"

**Principle Assessment:**
- **Autonomy:** ⚠️ Questionable - coercive language detected
- **Beneficence:** ❌ Violated - overclaiming harm через unrealistic expectations
- **Non-Maleficence:** ⚠️ Concern - риск disappointment и self-blame
- **Justice:** ✅ OK - доступно для всех

**Required Changes:**
1. **Убрать "Guarantee"** - заменить на "21-Day Transformation Program"
2. **Добавить Realistic Expectations:** "Большинство людей замечают изменения, но индивидуальные результаты vary. Некоторым может потребоваться дольше."
3. **Добавить Limitations Disclosure:** "Эта программа не замена профессиональной терапии. При серьезных симптомах обратитесь к специалисту."
4. **Изменить язык:** "Must" → "Can", "Обязан" → "Может"
5. **Добавить Right to Stop:** "Вы можете прекратить программу в любой момент без негативных последствий"

**After Revisions:** Может получить ethical approval
```

### Пример 5: Полная валидация модуля

**Запрос:**
```
Провалидируй полностью модуль "Mindfulness for Anxiety Management".

Модуль включает:
- Mindfulness meditation (10 минут ежедневно)
- Body scan technique
- Mindful breathing exercises
- Integration в повседневную жизнь

Целевые состояния: Anxiety, stress
```

**Результат:**
```
✅ Full Validation Report: Mindfulness for Anxiety Management

## 1. Technique Validations

### Mindfulness Meditation
- **Evidence Level:** Meta-analysis
- **Effect Size:** d=0.55 (medium) - Khoury et al. (2013), N=12,145
- **Validation Status:** Validated
- **Safety:** Safe для большинства

### Body Scan
- **Evidence Level:** RCT
- **Effect Size:** d=0.50 (medium)
- **Validation Status:** Validated
- **Safety:** Safe

### Mindful Breathing
- **Evidence Level:** Meta-analysis (part of MBSR protocol)
- **Validation Status:** Validated
- **Safety:** Safe

## 2. Safety Check
- **Overall Safety Rating:** Safe
- **Contraindications:**
  - Активный psychosis (intensive mindfulness может ухудшить)
  - Recent severe trauma (может быть overwhelming)
- **Warning Signs:**
  - Усиление anxiety (paradoxical effect у некоторых)
  - Диссоциативные симптомы
  - Distressing thoughts увеличиваются

## 3. Ethical Review
- **Autonomy:** ✅ Respected
- **Beneficence:** ✅ Yes - evidence-based approach
- **Non-Maleficence:** ✅ Yes - safe with warnings
- **Justice:** ✅ Yes - accessible
- **Ethical Approval:** YES

## 4. Effectiveness Metrics
- **Primary Outcome:** Снижение anxiety symptoms
- **Measurement:** GAD-7 (Generalized Anxiety Disorder-7)
- **Expected Effect:** Medium (d=0.55)
- **Time to Effect:** 4-8 недель регулярной практики

**Success Indicators:**
- Снижение GAD-7 score на 20-30%
- Улучшение ability to manage anxious thoughts
- Increased present-moment awareness

## 5. Overall Assessment
- **Validation Status:** ✅ VALIDATED
- **Evidence Level:** Meta-analysis
- **Safety Rating:** Safe (с contraindications)

## 6. Recommendations for Enhancement

**Minor Enhancements:**
1. Добавить guided audio для каждой практики
2. Включить troubleshooting guide для common difficulties
3. Предоставить shorter versions (5 минут) для начинающих
4. Добавить progress tracking worksheet

**Required Additions:**
1. Clear informed consent с:
   - Realistic expectations
   - Contraindications
   - Warning signs
   - When to seek professional help

2. Safety section с:
   - Что делать при paradoxical anxiety increase
   - Grounding techniques если overwhelmed
   - Emergency contacts

**Approval Notes:**
Модуль хорошо обоснован научно и безопасен для самопомощи. После добавления recommended enhancements - готов к использованию в PatternShift программе.
```

### Пример 6: Adaptation Validation

**Запрос:**
```
Оцени адаптацию техники "Exposure Therapy" для самопомощи.

Оригинал: Gradual exposure с терапевтом, 12-16 сессий
Адаптация: Gentle self-paced exposure exercises, без direct confrontation
```

**Результат:**
```
✅ Adaptation Validation: Exposure Therapy → Gentle Exposure

## Original Protocol
- Therapist-guided systematic desensitization
- Hierarchy of feared situations (0-100 SUDS)
- Prolonged exposure до снижения anxiety
- 12-16 weekly sessions

## Adapted Protocol
- Self-paced gentle exposure
- User creates own hierarchy
- Short exposures (5-10 минут)
- Optional - можно skip если too overwhelming

## Fidelity Assessment
**Fidelity Maintained:** ✅ YES (70%+)

**Key Elements Preserved:**
1. ✅ Hierarchy creation
2. ✅ Gradual exposure principle
3. ✅ Repeated practice
4. ⚠️ Prolonged exposure (modified - shorter duration)
5. ⚠️ Anxiety habituation tracking (simplified)

**Modifications Made:**
- Shortened exposure duration (safe modification)
- Added "escape option" (safety modification)
- Self-paced vs. therapist-paced (acceptable for self-help)
- Removed intense exposures (critical safety modification)

## Expected Efficacy Change
**Original Effect Size:** d=1.0+ (very large)
**Expected Self-Help Effect Size:** d=0.50-0.60 (medium)

**Explanation:**
- ~40% снижение efficacy из-за:
  - Отсутствие therapist guidance
  - Shorter exposure duration
  - Self-selection bias (пропуск challenging exposures)
- НО это acceptable trade-off для безопасности

## Safety Improvements
**Removed Risks:**
- ✅ Removed prolonged intense exposure (риск overwhelming)
- ✅ Removed direct traumatic memory work (риск re-traumatization)
- ✅ Added escape option (safety)

**Added Safeguards:**
- Clear stopping rules
- Grounding techniques
- When to seek professional help

## Validation Decision
**Status:** ✅ VALIDATED with modifications

**Rationale:**
- Core mechanism (gradual exposure) preserved
- Safety significantly improved
- Efficacy reduced but still meaningful (d=0.5-0.6)
- Appropriate for self-help context

**Required Additions:**
1. Clear disclaimer: "Это gentle версия exposure therapy. Для complex phobias или PTSD рекомендуется работа с терапевтом."
2. Guidance когда техника недостаточна (no improvement после 4-6 недель)
3. Alternative: Professional referral resources
```

## База знаний содержит:

- **Hierarchy of Evidence** - 6 уровней доказательности (мета-анализы → теоретическое обоснование)
- **Evidence-Based Approaches** - CBT (Hofmann et al., 2012: d=0.75), Mindfulness (Khoury et al., 2013: d=0.55), ACT (A-Tjak et al., 2015: d=0.42)
- **Limited Evidence Techniques** - NLP и как их валидировать через overlap с validated methods
- **Safety Protocols** - Contraindications (психоз, trauma, суицидальные мысли), warning signs, safe practices
- **Ethical Guidelines** - 4 принципа биоэтики (Autonomy, Beneficence, Non-Maleficence, Justice)
- **Adaptation Standards** - Fidelity, Safety, Accessibility principles
- **Effectiveness Metrics** - Validated measures (PHQ-9, GAD-7, WEMWBS), Cohen's d interpretation
- **Practical Workflow** - 6-шаговый процесс валидации
- **Example Reports** - Validated и Needs Revision примеры

## Важные принципы

- **Evidence-Based but Not Blocking** - поддержка инноваций с теоретическим обоснованием
- **Safety First** - безопасность превыше эффективности
- **Transparency about Limitations** - честность об ограничениях доказательной базы
- **Ethical Practice** - соблюдение 4 принципов биоэтики
- **Adaptation for Self-Help** - понимание что self-help имеет меньший effect size (20-30% снижение)
- **Supportive but Rigorous** - помощь создателям с сохранением высоких стандартов

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Обязательные переменные:
- `OPENAI_API_KEY` - API ключ OpenAI

### 3. Запуск тестов

```bash
# Установка pytest (если еще не установлен)
pip install pytest pytest-asyncio

# Запуск всех тестов
pytest tests/ -v

# Запуск конкретного теста
pytest tests/test_agent.py -v

# Запуск с покрытием кода
pytest tests/ --cov=. --cov-report=html
```

**Структура тестов:**
- `tests/test_agent.py` - тесты основного агента
- `tests/test_tools.py` - тесты всех 6 инструментов
- `tests/test_integration.py` - интеграционные тесты
- `tests/test_validation.py` - тесты Pydantic моделей
- `tests/conftest.py` - общие fixtures для тестов
- `tests/VALIDATION_REPORT.md` - отчет о валидации агента

### 4. Программное использование

```python
import asyncio
from pattern_scientific_validator import run_pattern_scientific_validator

async def main():
    module_data = {
        "module_id": "module_001",
        "module_name": "Cognitive Restructuring Module",
        "techniques": ["cognitive_restructuring", "thought_challenging"],
        "content": "Модуль для работы с негативными мыслями...",
        "target_conditions": ["depression", "anxiety"]
    }

    report = await run_pattern_scientific_validator(
        module_data=module_data,
        api_key="your-api-key",
        verbose=True
    )

    print(f"Validation Status: {report.overall_validation_status}")
    print(f"Safety Rating: {report.overall_safety_rating}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Загрузка в Archon Knowledge Base

1. Откройте Archon: http://localhost:3737/
2. Knowledge Base → Upload
3. Загрузите: `knowledge/pattern_scientific_validator_knowledge.md`
4. Добавьте теги:
   - `pattern-scientific-validator`
   - `evidence-based`
   - `research`
   - `agent-knowledge`
   - `patternshift`

---

## Структура проекта

```
pattern_scientific_validator/
├── agent.py                 # Основной Pydantic AI агент
├── dependencies.py          # Зависимости с RAG и базами данных
├── tools.py                 # 6 специализированных инструментов
├── prompts.py               # Системный промпт агента
├── models.py                # Pydantic модели для типизации
├── settings.py              # Конфигурация и настройки
├── __init__.py              # Python package exports
├── requirements.txt         # Python зависимости
├── .env.example             # Шаблон переменных окружения
├── knowledge/               # База знаний агента
│   └── pattern_scientific_validator_knowledge.md
└── tests/                   # Полный набор тестов
    ├── conftest.py          # Pytest конфигурация
    ├── test_agent.py        # Тесты агента (7 тестов)
    ├── test_tools.py        # Тесты инструментов (13 тестов)
    ├── test_integration.py  # Интеграционные тесты (6 тестов)
    ├── test_validation.py   # Тесты моделей (14 тестов)
    └── VALIDATION_REPORT.md # Отчет валидации
```

## Версия
1.0.0 - Production Ready

---

*Pattern Scientific Validator Agent - обеспечение научной обоснованности и безопасности программ PatternShift*
