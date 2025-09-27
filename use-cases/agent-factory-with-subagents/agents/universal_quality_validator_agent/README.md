# Universal Quality Validator Agent

Универсальный агент для комплексной валидации и контроля качества различных типов проектов с поддержкой множественных стандартов, автоматизированных проверок и детальной отчетности.

## 🎯 Основные возможности

- **Комплексная валидация качества** - код, безопасность, производительность, соответствие стандартам
- **Универсальная архитектура** - поддержка различных доменов (веб, мобильные, API, финтех, здравоохранение)
- **Адаптивные стандарты** - ISO 9001, Agile, CMMI, IEEE 830, кастомные стандарты
- **AI-powered анализ** - интеллектуальные рекомендации и автоматическое выявление проблем
- **Детальная отчетность** - структурированные отчеты с метриками и рекомендациями
- **Гибкие уровни валидации** - от базового до enterprise уровня

## 🏗️ Архитектура

```
universal_quality_validator_agent/
├── agent.py              # Основной агент
├── dependencies.py       # Конфигурация зависимостей
├── tools.py             # Инструменты валидации
├── prompts.py           # Адаптивные системные промпты
├── settings.py          # Настройки и конфигурация
├── providers.py         # Провайдеры AI моделей
├── requirements.txt     # Зависимости Python
├── .env.example        # Шаблон переменных окружения
└── README.md           # Документация
```

## 🚀 Быстрый старт

### 1. Установка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

### 2. Конфигурация

Основные переменные в `.env`:

```env
# Домен проекта
QUALITY_VALIDATOR_PROJECT_DOMAIN=web_development

# Стандарт качества
QUALITY_VALIDATOR_QUALITY_STANDARD=iso_9001

# Уровень валидации
QUALITY_VALIDATOR_VALIDATION_LEVEL=standard

# AI модели
LLM_API_KEY=your_api_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Базовое использование

```python
from universal_quality_validator_agent import (
    universal_quality_validator_agent,
    QualityValidatorDependencies,
    ProjectDomain,
    QualityStandard,
    ValidationLevel
)

# Создание зависимостей
deps = QualityValidatorDependencies(
    project_domain=ProjectDomain.WEB_DEVELOPMENT,
    quality_standard=QualityStandard.ISO_9001,
    validation_level=ValidationLevel.STANDARD,
    project_path="/path/to/your/project"
)

# Запуск валидации
result = await universal_quality_validator_agent.run(
    "Проведи комплексную валидацию качества проекта",
    deps=deps
)

print(result.data)
```

## 🌐 Поддерживаемые домены

### Web Development
- HTML5, CSS3, JavaScript валидация
- Responsive design и accessibility
- SEO оптимизация
- Performance budget анализ
- Веб-безопасность (XSS, CSRF, CSP)

### Mobile Development
- Platform-specific guidelines (iOS/Android)
- Performance на мобильных устройствах
- Battery optimization
- Memory management
- App Store compliance

### API Services
- REST/GraphQL best practices
- API documentation quality
- Rate limiting и authentication
- Response time анализ
- API security стандарты

### Fintech
- PCI-DSS compliance
- Financial regulations
- Enhanced security requirements
- Fraud detection patterns
- Audit trail validation

### Healthcare
- HIPAA compliance
- Medical device standards (IEC 62304)
- Patient data security
- Clinical workflow validation
- Regulatory compliance (FDA, CE)

## ⚙️ Уровни валидации

### Basic
- Основные проверки качества кода
- Критичные проблемы безопасности
- Базовое функциональное тестирование
- Простые метрики производительности

### Standard
- Комплексный анализ кода и архитектуры
- Полная проверка безопасности
- Автоматизированное тестирование
- Детальные метрики производительности
- Проверка соответствия стандартам

### Comprehensive
- Глубокий архитектурный анализ
- Расширенные security тесты
- Performance profiling
- Compliance audit
- Полная документация и отчетность

### Enterprise
- Enterprise architecture validation
- Multi-environment testing
- Scalability и reliability анализ
- Regulatory compliance
- Risk assessment и mitigation
- Continuous monitoring setup

## 🛠️ Инструменты валидации

### Качество кода
- Статический анализ (flake8, pylint, mypy)
- Code complexity метрики (radon, mccabe)
- Code style проверки (black, isort)
- Documentation coverage (pydocstyle)

### Безопасность
- Vulnerability scanning (bandit, semgrep)
- Dependency analysis (safety, pip-audit)
- Security headers validation
- Authentication/authorization проверки

### Производительность
- Load testing и benchmarking
- Memory profiling
- Database query optimization
- Caching strategy analysis

### Соответствие стандартам
- Regulatory compliance проверки
- Industry best practices
- Internal policies validation
- Audit trail analysis

## 📊 Отчетность

### Executive Summary
- Общий балл качества
- Ключевые findings
- Критичные проблемы
- High-level рекомендации

### Technical Report
- Детальный анализ по категориям
- Метрики и KPI
- Списки проблем с приоритетами
- Технические рекомендации

### Improvement Roadmap
- Поэтапный план улучшений
- Временные рамки
- Ресурсные требования
- Метрики успеха

## 🤖 AI-powered возможности

### Интеллектуальный анализ
- Автоматическое выявление архитектурных проблем
- Semantic code analysis
- Pattern recognition в коде
- Predictive quality scoring

### Оптимизация моделей
- **Qwen 2.5 Coder** для анализа кода
- **Qwen 2.5-72B** для security audit
- **Gemini 2.5 Flash** для документации
- **Автоматический выбор** оптимальной модели

### Умные рекомендации
- Контекстуальные улучшения
- Best practices для конкретного домена
- Приоритизация исправлений
- Effort estimation

## 🔧 Конфигурация под различные проекты

### React/Next.js проект
```python
deps = QualityValidatorDependencies(
    project_domain=ProjectDomain.WEB_DEVELOPMENT,
    quality_standard=QualityStandard.AGILE,
    validation_level=ValidationLevel.STANDARD,
    custom_rules={
        "check_react_patterns": True,
        "validate_nextjs_performance": True,
        "seo_optimization": True
    }
)
```

### Python API проект
```python
deps = QualityValidatorDependencies(
    project_domain=ProjectDomain.API_SERVICES,
    quality_standard=QualityStandard.ISO_9001,
    validation_level=ValidationLevel.COMPREHENSIVE,
    custom_rules={
        "validate_openapi": True,
        "check_rate_limiting": True,
        "security_headers": True
    }
)
```

### Финтех приложение
```python
deps = QualityValidatorDependencies(
    project_domain=ProjectDomain.FINTECH,
    quality_standard=QualityStandard.CMMI,
    validation_level=ValidationLevel.ENTERPRISE,
    custom_rules={
        "pci_compliance": True,
        "fraud_detection": True,
        "audit_logging": True
    }
)
```

## 📈 Метрики и KPI

### Качество кода
- **Code Quality Score** (0-100)
- **Technical Debt Ratio**
- **Cyclomatic Complexity**
- **Test Coverage %**
- **Documentation Coverage %**

### Безопасность
- **Security Score** (0-100)
- **Vulnerability Count** (Critical/High/Medium/Low)
- **Security Headers Coverage**
- **Dependency Risk Score**

### Производительность
- **Performance Score** (0-100)
- **Response Time P95/P99**
- **Memory Usage**
- **CPU Utilization**
- **Database Query Performance**

### Соответствие
- **Compliance Score** (0-100)
- **Standards Adherence %**
- **Policy Violations Count**
- **Audit Readiness Score**

## 🔌 Интеграции

### Внешние инструменты
- **SonarQube** - централизованный анализ качества
- **JIRA** - автоматическое создание issues
- **Slack/Teams** - уведомления команды
- **GitHub/GitLab** - интеграция с CI/CD

### CI/CD интеграция
```yaml
# GitHub Actions example
- name: Quality Validation
  run: |
    python -m universal_quality_validator_agent \
      --project-path . \
      --validation-level comprehensive \
      --output-format json
```

## 🎯 Примеры использования

### 1. Быстрая проверка качества
```python
result = await universal_quality_validator_agent.run(
    "Проведи быструю проверку качества кода",
    deps=QualityValidatorDependencies(
        validation_level=ValidationLevel.BASIC,
        project_path="./src"
    )
)
```

### 2. Полный security audit
```python
result = await universal_quality_validator_agent.run(
    "Выполни полный аудит безопасности с проверкой всех уязвимостей",
    deps=QualityValidatorDependencies(
        project_domain=ProjectDomain.FINTECH,
        validation_level=ValidationLevel.ENTERPRISE,
        custom_rules={"deep_security_scan": True}
    )
)
```

### 3. Performance анализ
```python
result = await universal_quality_validator_agent.run(
    "Проанализируй производительность и найди узкие места",
    deps=QualityValidatorDependencies(
        validation_level=ValidationLevel.COMPREHENSIVE,
        custom_rules={"performance_profiling": True}
    )
)
```

## 🤝 Интеграция с другими агентами

Quality Validator может работать совместно с другими агентами:

- **Security Audit Agent** - для глубокого анализа безопасности
- **Performance Optimization Agent** - для оптимизации производительности
- **Prisma Database Agent** - для валидации схем БД
- **UI/UX Enhancement Agent** - для проверки интерфейсов

## 📚 API Reference

### Основные функции

#### `run_quality_validation()`
Комплексная валидация качества проекта

**Параметры:**
- `project_path` (str) - путь к проекту
- `validation_scope` (str) - область валидации
- `environment` (str) - среда выполнения
- `quality_standard` (str) - стандарт качества
- `custom_rules` (dict) - пользовательские правила

#### `validate_specific_component()`
Валидация конкретного компонента

**Параметры:**
- `component_path` (str) - путь к компоненту
- `component_type` (str) - тип компонента
- `validation_types` (list) - типы валидации
- `strict_mode` (bool) - строгий режим

#### `continuous_quality_monitoring()`
Непрерывный мониторинг качества

**Параметры:**
- `project_path` (str) - путь к проекту
- `monitoring_interval` (int) - интервал мониторинга
- `alert_thresholds` (dict) - пороги уведомлений

## 🚨 Устранение неполадок

### Распространенные проблемы

1. **Отсутствие API ключей**
   ```
   ValueError: API key not found in environment: LLM_API_KEY
   ```
   **Решение:** Убедитесь, что все необходимые API ключи указаны в `.env`

2. **Проблемы с правами доступа**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   **Решение:** Проверьте права доступа к анализируемым файлам

3. **Превышение лимитов AI моделей**
   ```
   RateLimitError: Rate limit exceeded
   ```
   **Решение:** Используйте более дешевые модели или настройте rate limiting

### Отладка

Включите подробный режим:
```env
DEBUG=true
VERBOSE=true
LOG_LEVEL=DEBUG
```

## 📄 Лицензия

Этот проект разработан в рамках AI Agent Factory и предназначен для универсального использования в различных типах проектов.

## 🤝 Вклад в проект

Агент разработан для максимальной универсальности и может быть адаптирован под любые проекты. Для предложений по улучшению создавайте issues в репозитории AI Agent Factory.

## 📞 Поддержка

Для получения поддержки обращайтесь к документации AI Agent Factory или создавайте issues с детальным описанием проблемы.