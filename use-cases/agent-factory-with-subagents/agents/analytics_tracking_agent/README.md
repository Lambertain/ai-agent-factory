# 📊 Universal Analytics & Tracking Agent

Универсальный агент на базе Pydantic AI для настройки, оптимизации и анализа систем аналитики для любых типов проектов.

## 🎯 Основные возможности

- **Универсальная поддержка проектов**: веб-аналитика, e-commerce, SaaS, блоги, мобильные приложения
- **Множественные провайдеры**: Google Analytics 4, Mixpanel, Amplitude, Segment, Hotjar
- **Privacy-compliant tracking**: GDPR и CCPA compliance из коробки
- **Конверсионная аналитика**: воронки, сегментация, behavioral analysis
- **Автоматизированные дашборды**: custom dashboards и real-time reporting
- **Межагентное взаимодействие**: интеграция с другими агентами через Archon

## 🏗️ Архитектура

```
analytics_tracking_agent/
├── agent.py                    # Основной агент
├── dependencies.py             # Зависимости и конфигурация
├── settings.py                 # Настройки и переменные окружения
├── tools.py                    # Инструменты для работы с аналитикой
├── prompts.py                  # Адаптивные системные промпты
├── knowledge/                  # База знаний агента
│   └── analytics_tracking_knowledge.md
├── examples/                   # Примеры конфигураций
│   ├── ecommerce_config.py     # E-commerce проекты
│   ├── saas_config.py          # SaaS метрики
│   └── blog_config.py          # Блог аналитика
├── requirements.txt            # Python зависимости
├── .env.example                # Шаблон переменных окружения
└── README.md                   # Документация
```

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонируйте репозиторий
cd agents/analytics_tracking_agent

# Установите зависимости
pip install -r requirements.txt

# Скопируйте и настройте переменные окружения
cp .env.example .env
```

### 2. Конфигурация

Отредактируйте `.env` файл с вашими API ключами:

```env
# Основные настройки
LLM_API_KEY=your-llm-api-key
PROJECT_TYPE=web_analytics
TRACKING_FOCUS=conversion

# Google Analytics 4
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GA4_API_SECRET=your-ga4-api-secret

# Mixpanel (опционально)
MIXPANEL_TOKEN=your-mixpanel-token
MIXPANEL_API_KEY=your-mixpanel-api-key

# Privacy compliance
GDPR_COMPLIANCE=true
CCPA_COMPLIANCE=true
```

### 3. Использование

#### Python API

```python
from analytics_tracking_agent import create_web_analytics_agent

# Создайте агента для веб-аналитики
agent = create_web_analytics_agent()

# Настройте трекинг
response = await agent.run("Настрой Google Analytics 4 для отслеживания конверсий")
print(response)

# Создайте воронку конверсии
response = await agent.run("Создай воронку конверсии для лендинга с 4 этапами")
print(response)
```

#### Различные типы проектов

```python
from analytics_tracking_agent import (
    create_ecommerce_agent,
    create_saas_agent,
    create_blog_agent
)

# E-commerce аналитика
ecommerce_agent = create_ecommerce_agent()
await ecommerce_agent.run("Настрой Enhanced E-commerce tracking")

# SaaS метрики
saas_agent = create_saas_agent()
await saas_agent.run("Создай cohort analysis для churn prediction")

# Блог аналитика
blog_agent = create_blog_agent()
await blog_agent.run("Настрой отслеживание reading engagement")
```

#### Командная строка

```bash
# Веб-аналитика
python agent.py --project-type web_analytics --message "Настрой базовую аналитику"

# E-commerce
python agent.py --project-type ecommerce_tracking --message "Создай отчет по продажам"

# Интерактивный режим
python agent.py --project-type saas_metrics --interactive
```

## 📋 Поддерживаемые типы проектов

### 🌐 Веб-аналитика (`web_analytics`)
- Отслеживание трафика и поведения пользователей
- SEO метрики и органический поиск
- Конверсионные воронки для лендингов
- A/B тестирование и оптимизация

**Провайдеры**: Google Analytics 4, Mixpanel
**Ключевые метрики**: Sessions, Users, Bounce Rate, Avg Session Duration

### 🛒 E-commerce (`ecommerce_tracking`)
- Enhanced E-commerce tracking
- Отслеживание покупательского пути
- Cart abandonment analysis
- Customer lifetime value (CLV)

**Провайдеры**: Google Analytics 4, Mixpanel
**Ключевые метрики**: Conversion Rate, AOV, Revenue, Cart Abandonment Rate

### 🚀 SaaS метрики (`saas_metrics`)
- User activation и onboarding
- Feature usage и adoption
- Churn prediction и retention
- Subscription lifecycle tracking

**Провайдеры**: Mixpanel, Amplitude
**Ключевые метрики**: MAU, Activation Rate, Churn Rate, NRR

### 📝 Блог аналитика (`blog_analytics`)
- Content performance tracking
- Reader engagement metrics
- Social sharing analysis
- Newsletter conversion

**Провайдеры**: Google Analytics 4
**Ключевые метрики**: Unique Visitors, Engagement Rate, Newsletter Conversion

### 📱 Мобильная аналитика (`mobile_analytics`)
- In-app events tracking
- User retention analysis
- Push notification effectiveness
- Cross-platform attribution

**Провайдеры**: Mixpanel, Amplitude
**Ключевые метрики**: DAU, Session Length, Retention Rate, Push Open Rate

### 📄 Контент аналитика (`content_analytics`)
- Multimedia content tracking
- Social media integration
- Content lifecycle analysis
- Creator performance metrics

**Провайдеры**: Google Analytics 4, Mixpanel
**Ключевые метрики**: Content Engagement, Social Shares, Time on Content

## 🔧 Доступные инструменты

### Основные инструменты

- `setup_analytics_tracking()` - Настройка трекинга для различных провайдеров
- `create_conversion_funnel()` - Создание воронок конверсии
- `analyze_user_behavior()` - Анализ поведения пользователей
- `generate_analytics_report()` - Генерация отчетов и дашбордов

### Специализированные инструменты

- `optimize_tracking_performance()` - Оптимизация производительности трекинга
- `setup_privacy_compliance()` - Настройка GDPR/CCPA compliance
- `create_custom_dashboard()` - Создание кастомных дашбордов
- `validate_tracking_implementation()` - Валидация корректности настройки

### Поиск и коллаборация

- `search_analytics_knowledge()` - Поиск в базе знаний агента
- `delegate_task_to_agent()` - Делегирование задач другим агентам

## 🛡️ Privacy & Compliance

Агент поддерживает compliance из коробки:

### GDPR Compliance
- Cookie consent management
- Data anonymization
- Right to deletion
- Data portability

### CCPA Compliance
- Opt-out mechanisms
- Do not sell options
- Consumer rights support

### Техническая реализация

```javascript
// Пример GDPR-compliant трекинга
if (cookieConsentGiven) {
    gtag('config', 'GA_MEASUREMENT_ID', {
        'anonymize_ip': false,
        'allow_personalization_signals': true
    });
} else {
    gtag('config', 'GA_MEASUREMENT_ID', {
        'anonymize_ip': true,
        'allow_personalization_signals': false
    });
}
```

## 📊 Примеры использования

### E-commerce трекинг

```python
agent = create_ecommerce_agent()

# Настройка Enhanced E-commerce
await agent.run("""
Настрой Enhanced E-commerce для интернет-магазина:
- Отслеживание view_item, add_to_cart, purchase
- Cart abandonment analysis
- Customer segmentation по CLV
- Revenue attribution по каналам
""")
```

### SaaS метрики

```python
agent = create_saas_agent()

# Настройка product-led growth аналитики
await agent.run("""
Создай систему отслеживания для SaaS:
- User activation tracking (time to value)
- Feature adoption measurement
- Churn prediction модель
- Cohort analysis по месяцам регистрации
""")
```

### Блог аналитика

```python
agent = create_blog_agent()

# Настройка content performance tracking
await agent.run("""
Настрой аналитику для блога:
- Reading progress tracking (25%, 50%, 75%, 100%)
- Social sharing по платформам
- Newsletter conversion optimization
- Author performance metrics
""")
```

## 🤝 Межагентное взаимодействие

Агент автоматически интегрируется с другими агентами системы:

### Автоматическое делегирование

- **Performance issues** → Performance Optimization Agent
- **Security/Privacy аудит** → Security Audit Agent
- **UI/UX optimization** → UI/UX Enhancement Agent
- **Database оптимизация** → Prisma Database Agent

### Пример делегирования

```python
# Если запрос касается производительности
await agent.run("Оптимизируй скорость загрузки analytics скриптов")
# → Автоматически делегирует Performance Optimization Agent

# Если запрос касается UI
await agent.run("Улучши UX для cookie consent баннера")
# → Автоматически делегирует UI/UX Enhancement Agent
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Тестирование specific provider
pytest tests/test_providers.py::TestGoogleAnalytics

# Интеграционные тесты
pytest tests/test_integration.py
```

## 📚 База знаний

Агент включает обширную базу знаний с примерами:

- **Google Analytics 4**: Enhanced E-commerce, Custom Events, Audiences
- **Mixpanel**: Event Tracking, Funnel Analysis, Cohort Analysis
- **Amplitude**: User Journey, Retention Analysis, Behavioral Cohorts
- **Privacy Compliance**: GDPR/CCPA implementation patterns
- **Best Practices**: Performance optimization, data governance

### Загрузка в Archon Knowledge Base

1. Откройте Archon: http://localhost:3737/
2. Перейдите в Knowledge Base → Upload
3. Загрузите `knowledge/analytics_tracking_knowledge.md`
4. Добавьте теги: `analytics-tracking`, `agent-knowledge`, `pydantic-ai`

## 🔄 Обновления и расширения

### Добавление нового провайдера

1. Обновите `settings.py` с новыми API настройками
2. Добавьте конфигурацию в `dependencies.py`
3. Реализуйте инструменты в `tools.py`
4. Обновите базу знаний с примерами

### Новый тип проекта

1. Создайте конфигурацию в `examples/new_project_config.py`
2. Добавьте тип в `settings.py` → `get_project_config()`
3. Обновите промпты в `prompts.py`
4. Добавьте фабричную функцию в `agent.py`

## 🐛 Известные ограничения

- Некоторые функции требуют оплачиваемых планов провайдеров
- Real-time данные могут иметь задержки до 24-48 часов
- CORS настройки могут потребовать дополнительной конфигурации
- Batch API некоторых провайдеров имеют rate limits

## 📖 Дополнительные ресурсы

### Документация провайдеров
- [Google Analytics 4 Documentation](https://developers.google.com/analytics/devguides/collection/ga4)
- [Mixpanel Documentation](https://docs.mixpanel.com/)
- [Amplitude Documentation](https://docs.amplitude.com/)
- [Segment Documentation](https://docs.segmentapis.com/)

### Privacy Compliance
- [GDPR Compliance Guide](https://gdpr.eu/)
- [CCPA Compliance Guide](https://oag.ca.gov/privacy/ccpa)

## 🤝 Вклад в развитие

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

---

**Создано с помощью AI Agent Factory** 🤖