# Universal NLP Content Architect Agent 🧠✨

Универсальный агент для создания контента с интеграцией NLP/Эриксоновских техник для любых доменов: психология, астрология, таро, нумерология, коучинг, велнес.

## 🌟 Ключевые особенности

### 🎯 Универсальность
- **Поддержка 6+ доменов**: психология, астрология, таро, нумерология, коучинг, велнес
- **Адаптивные конфигурации** под каждый домен
- **Мультиязычность**: украинский, русский, английский
- **Гибкие настройки** через переменные окружения

### 🧠 NLP/Эриксоновская интеграция
- **Эриксоновские паттерны**: трюизмы, презумпции, встроенные команды, терапевтические метафоры
- **NLP техники**: рефрейминг, якорение, раппорт, мета-программы, субмодальности
- **VAK адаптации**: визуальные, аудиальные, кинестетические варианты
- **Трансформационные программы**: 3-фазовая методология изменений

### 🔄 5-этапная методология
1. **Research** - исследование темы и домена
2. **Draft** - создание черновика контента
3. **Reflection** - анализ и улучшение
4. **Final** - финализация контента
5. **Analytics** - создание аналитики и рекомендаций

## 🚀 Быстрый старт

### Установка

```bash
# 1. Перейдите в директорию агента
cd agents/universal_nlp_content_architect/

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Настройте переменные окружения
cp .env.example .env
# Отредактируйте .env с вашими API ключами
```

### Базовое использование

```python
from universal_nlp_content_architect import create_nlp_content

# Создание психологического теста
result = await create_nlp_content(
    content_topic="Тест на уровень тревожности",
    domain_type="psychology",
    target_language="ukrainian",
    content_count=16,
    transformation_days=21
)

# Создание астрологического контента
result = await create_nlp_content(
    content_topic="Анализ натальной карты",
    domain_type="astrology",
    target_language="ukrainian",
    content_count=12
)

# Создание коучингового контента
result = await create_nlp_content(
    content_topic="Программа достижения целей",
    domain_type="coaching",
    content_type="transformation_program",
    transformation_days=30
)
```

### Быстрое создание с дефолтными настройками

```python
from universal_nlp_content_architect import quick_create_nlp_content

# Создание с минимальными настройками
result = await quick_create_nlp_content(
    topic="Медитация для начинающих",
    domain="wellness",
    language="ukrainian"
)
```

## 🔧 Конфигурация

### Поддерживаемые домены

| Домен | Описание | Особенности |
|-------|----------|-------------|
| `psychology` | Психология | Научная база, терапевтическая этика, безопасность |
| `astrology` | Астрология | Символические интерпретации, эмпауэрмент, свободная воля |
| `tarot` | Таро | Интуитивные чтения, архетипические образы, личная сила |
| `numerology` | Нумерология | Математическая точность, балансные интерпретации |
| `coaching` | Коучинг | Ориентация на результат, профессиональные границы |
| `wellness` | Велнес/медитация | Холистический подход, безопасность, модификации |

### Типы контента

| Тип | Описание | Применение |
|-----|----------|-----------|
| `diagnostic_test` | Диагностический тест | Психологические тесты, оценки |
| `transformation_program` | Программа трансформации | 21-дневные программы изменений |
| `guidance_system` | Система наставничества | Пошаговые руководства |
| `assessment_tool` | Инструмент оценки | Анализ и измерение прогресса |
| `meditation_program` | Программа медитации | Медитативные практики |

### Переменные окружения

```env
# Основные настройки
LLM_API_KEY=your_api_key_here
LLM_MODEL=qwen2.5-coder-32b-instruct
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# NLP настройки
DEFAULT_DOMAIN=psychology
DEFAULT_LANGUAGE=ukrainian
DEFAULT_COMPLEXITY=intermediate

# Archon интеграция
ARCHON_PROJECT_ID=your_project_id
ENABLE_ARCHON_RAG=true
```

## 📚 Примеры конфигураций

Агент включает готовые конфигурации для всех поддерживаемых доменов:

### Психология (`examples/psychology_nlp_config.py`)
```python
from examples.psychology_nlp_config import create_psychology_nlp_config

config = create_psychology_nlp_config("your-api-key")
# Включает: депрессивные тесты, программы работы с тревогой, VAK адаптации
```

### Астрология (`examples/astrology_nlp_config.py`)
```python
from examples.astrology_nlp_config import create_astrology_nlp_config

config = create_astrology_nlp_config("your-api-key")
# Включает: анализ натальной карты, астро-коучинг, планетарные NLP соответствия
```

### Таро (`examples/tarot_nlp_config.py`)
```python
from examples.tarot_nlp_config import create_tarot_nlp_config

config = create_tarot_nlp_config("your-api-key")
# Включает: расклады карт, символические интерпретации, эмпауэрмент фокус
```

### Нумерология (`examples/numerology_nlp_config.py`)
```python
from examples.numerology_nlp_config import create_numerology_nlp_config

config = create_numerology_nlp_config("your-api-key")
# Включает: расчет жизненного пути, совместимость, бизнес-нумерология
```

### Коучинг (`examples/coaching_nlp_config.py`)
```python
from examples.coaching_nlp_config import create_coaching_nlp_config

config = create_coaching_nlp_config("your-api-key")
# Включает: GROW модель, лайф-коучинг, бизнес-коучинг, велнес-коучинг
```

### Велнес (`examples/wellness_nlp_config.py`)
```python
from examples.wellness_nlp_config import create_wellness_nlp_config

config = create_wellness_nlp_config("your-api-key")
# Включает: программы медитации, энергетическое исцеление, чакры, холистический велнес
```

## 🛠️ Архитектура

### Основные компоненты

```
universal_nlp_content_architect/
├── agent.py                    # Главный агент
├── dependencies.py             # Конфигурация зависимостей
├── settings.py                 # Настройки и конфигурации
├── tools.py                    # 5-этапные инструменты
├── prompts.py                  # Системные промпты
├── knowledge/                  # База знаний
├── examples/                   # Примеры конфигураций
│   ├── psychology_nlp_config.py
│   ├── astrology_nlp_config.py
│   ├── tarot_nlp_config.py
│   ├── numerology_nlp_config.py
│   ├── coaching_nlp_config.py
│   └── wellness_nlp_config.py
├── requirements.txt
├── .env.example
└── README.md
```

### Ключевые классы

#### `UniversalNLPDependencies`
```python
@dataclass
class UniversalNLPDependencies:
    api_key: str
    domain_type: DomainType = "psychology"
    content_type: ContentType = "diagnostic_test"
    target_language: str = "ukrainian"
    nlp_methodology: NLPMethodology = "ericksonian_full"
    complexity_level: ComplexityLevel = "intermediate"
    transformation_days: int = 21
    # ... другие поля
```

#### `UniversalNLPSettings`
```python
class UniversalNLPSettings(BaseSettings):
    domain_type: DomainType = "psychology"
    content_type: ContentType = "diagnostic_test"
    target_language: str = "ukrainian"
    content_count: int = Field(default=16, ge=15)
    complexity_level: ComplexityLevel = "intermediate"
    transformation_days: int = 21
    # ... NLP и безопасность настройки
```

### 5-этапные инструменты

1. **`research_domain_topic`** - исследование темы с использованием RAG
2. **`create_content_draft`** - создание черновика с NLP интеграцией
3. **`reflect_and_improve_content`** - анализ и улучшение контента
4. **`finalize_nlp_content`** - финализация с VAK адаптациями
5. **`create_analytics_report`** - создание аналитики и рекомендаций

## 🎨 NLP/Эриксоновские техники

### Основные NLP техники
- **Рефрейминг контекста и содержания**
- **Якорение ресурсных состояний**
- **Построение раппорта**
- **Работа с мета-программами**
- **Субмодальности**
- **Терапия временной линии**

### Эриксоновские паттерны
- **Трюизмы** - общеизвестные истины
- **Презумпции** - предположения в языке
- **Встроенные команды** - скрытые директивы
- **Терапевтические метафоры** - исцеляющие образы
- **Принцип утилизации** - использование всего как ресурс

### VAK адаптации
- **Визуальные** - образы, цвета, картины
- **Аудиальные** - звуки, ритмы, мелодии
- **Кинестетические** - ощущения, движения, энергии

## 🔍 Интеграция с Archon RAG

Агент автоматически интегрируется с Archon Knowledge Base:

```python
# Автоматический поиск знаний в процессе работы
@agent.tool
async def search_nlp_knowledge(
    ctx: RunContext[UniversalNLPDependencies],
    query: str,
    domain_filter: str = None
) -> str:
    """Поиск в базе знаний NLP техник через Archon RAG."""
    # Использует mcp__archon__rag_search_knowledge_base
```

### Загрузка базы знаний

1. Откройте Archon: http://localhost:3737/
2. Перейдите в Knowledge Base → Upload
3. Загрузите `knowledge/universal_nlp_content_architect_knowledge.md`
4. Добавьте теги: `universal-nlp`, `agent-knowledge`, `pydantic-ai`, `ericksonian-nlp`

## 📈 Примеры результатов

### Психологический тест с NLP
```json
{
  "content_type": "diagnostic_test",
  "domain": "psychology",
  "title": "Тест на уровень стрессоустойчивости",
  "questions": [
    {
      "id": 1,
      "text": "Когда вы сталкиваетесь с неожиданным вызовом, первая реакция обычно (трюизм):",
      "nlp_techniques": ["truism", "embedded_command"],
      "vak_adaptations": {
        "visual": "...видите возможности в ситуации",
        "auditory": "...слышите внутренний голос поддержки",
        "kinesthetic": "...чувствуете прилив энергии"
      }
    }
  ],
  "interpretation_framework": {
    "empowerment_focus": true,
    "ericksonian_reframes": ["Стресс как компас потребностей"],
    "resource_oriented": true
  }
}
```

### Астрологическая интерпретация с NLP
```json
{
  "content_type": "guidance_system",
  "domain": "astrology",
  "title": "Солнце в Овне: активация личной силы",
  "interpretation": {
    "traditional": "Солнце в Овне означает лидерство и инициативу",
    "nlp_enhanced": "Солнце в Овне **активирует** природные лидерские качества и **направляет** к смелым начинаниям (встроенные команды)",
    "empowerment_message": "Ваша природная смелость - дар миру",
    "ericksonian_patterns": [
      "Как планеты движутся по орбитам (трюизм), так и ваши таланты **раскрываются** в нужное время (презумпция + команда)"
    ]
  }
}
```

## 🛡️ Безопасность и этика

### По доменам
- **Психология**: избежание диагнозов, фокус на ресурсах, профессиональные референсы
- **Астрология**: избежание фатализма, поощрение свободной воли, эмпауэрмент
- **Таро**: избежание абсолютных предсказаний, поощрение личной силы
- **Нумерология**: прозрачность расчетов, сбалансированные интерпретации
- **Коучинг**: профессиональные границы, фокус на целях клиента
- **Велнес**: уважение ограничений, опции модификаций, медицинские границы

### Общие принципы
- Дисклеймеры "для развлечения"
- Не замена профессиональной помощи
- Поощрение личной ответственности
- Поддерживающий, эмпауэрмент-ориентированный подход

## 🔧 Расширение и кастомизация

### Добавление нового домена

1. Создайте файл `examples/new_domain_nlp_config.py`
2. Определите специфичные NLP техники для домена
3. Добавьте VAK адаптации
4. Обновите `DomainType` в `settings.py`
5. Добавьте в `SUPPORTED_DOMAINS` в `__init__.py`

### Добавление новых NLP техник

1. Расширьте `nlp_techniques` в конфигурации домена
2. Добавьте эриксоновские паттерны в `ericksonian` секцию
3. Обновите промпты в `prompts.py`
4. Добавьте примеры в базу знаний

## 🤝 Содействие

Вклады приветствуются! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для фичи
3. Добавьте тесты для новой функциональности
4. Убедитесь, что все тесты проходят
5. Отправьте пул-реквест

## 📝 Лицензия

MIT License - см. LICENSE файл для деталей.

## 🙋‍♂️ Поддержка

Для вопросов и поддержки:
- Создайте issue в репозитории
- Проверьте документацию в `knowledge/` папке
- Используйте примеры в `examples/` папке

---

**Универсальный NLP агент - мощный инструмент для создания трансформационного контента в любой области с научно обоснованными NLP и Эриксоновскими техниками.** ✨🧠