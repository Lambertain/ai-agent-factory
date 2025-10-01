# Archon Quality Guardian Agent

Универсальный AI-powered агент для автоматизации контроля качества кода, code review, мониторинга метрик и интеграции с CI/CD пайплайнами.

## Возможности

### Автоматический Code Review
- AI-powered анализ кода с использованием Claude Sonnet 4
- Детекция проблем качества, безопасности, производительности
- Конкретные рекомендации с примерами исправленного кода
- Оценка severity (blocker, critical, major, minor, info)

### Мониторинг Метрик Качества
- Test coverage анализ
- Cyclomatic complexity измерение
- Maintainability index расчет
- Lines of Code статистика
- Code smells детекция

### Статический Анализ
**Python:**
- pylint, flake8, mypy
- bandit (security), safety
- radon (complexity)
- pytest-cov (coverage)

**TypeScript:**
- eslint, tsc
- snyk, npm audit (security)
- complexity-report
- jest (coverage)

### Технический Долг
- Автоматическая детекция технического долга
- Оценка времени на исправление
- Приоритизация по severity
- Отчеты и рекомендации

### CI/CD Интеграция
- GitHub Actions workflows
- GitLab CI pipelines
- Jenkins integration
- Автоматические блокировки merge при critical issues

## Установка

```bash
pip install -r requirements.txt
```

### Requirements

```txt
pydantic-ai>=0.0.14
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0

# Static Analysis Tools
pylint>=3.0.0
flake8>=6.0.0
mypy>=1.0.0
bandit>=1.7.0
safety>=2.3.0
radon>=6.0.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
```

## Быстрый старт

### 1. Настройка переменных окружения

Создайте `.env` файл:

```env
# LLM Configuration
LLM_API_KEY=your-api-key-here
LLM_MODEL=qwen2.5-coder-32b-instruct
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Quality Thresholds
TEST_COVERAGE_THRESHOLD=80.0
COMPLEXITY_THRESHOLD=10
MAINTAINABILITY_THRESHOLD=50.0

# CI/CD Integration
GITHUB_TOKEN=your-github-token
GITLAB_TOKEN=your-gitlab-token

# Archon Integration
ARCHON_API_URL=http://localhost:3737
ARCHON_PROJECT_ID=c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
```

### 2. Базовое использование

```python
from archon_quality_guardian import run_quality_guardian

async def main():
    result = await run_quality_guardian(
        user_message="Проанализируй качество кода в проекте",
        project_path="./my-project",
        language="python",
        project_type="python"
    )
    print(result)

import asyncio
asyncio.run(main())
```

### 3. Анализ конкретного файла

```python
from archon_quality_guardian import agent, QualityGuardianDependencies

deps = QualityGuardianDependencies(
    project_path="./my-project",
    language="python"
)

result = await agent.run(
    "Проанализируй файл src/main.py",
    deps=deps
)
print(result.data)
```

### 4. Получение метрик проекта

```python
result = await agent.run(
    "Покажи метрики качества проекта",
    deps=deps
)
```

### 5. Расчет технического долга

```python
result = await agent.run(
    "Рассчитай технический долг проекта",
    deps=deps
)
```

## Примеры конфигураций

### Python проект

```python
from archon_quality_guardian import QualityGuardianDependencies

deps = QualityGuardianDependencies(
    project_path="/path/to/python/project",
    project_type="python",
    language="python",
    framework="fastapi",
    test_coverage_threshold=85.0,
    complexity_threshold=10,
    enable_auto_fix=True,
    enable_ai_review=True
)
```

### TypeScript проект

```python
deps = QualityGuardianDependencies(
    project_path="/path/to/typescript/project",
    project_type="typescript",
    language="typescript",
    framework="nextjs",
    test_coverage_threshold=80.0,
    complexity_threshold=15,
    enable_auto_fix=True
)
```

### Fullstack проект

```python
deps = QualityGuardianDependencies(
    project_path="/path/to/fullstack/project",
    project_type="fullstack",
    language="python",  # или "typescript"
    test_coverage_threshold=82.0,
    enable_ai_review=True
)
```

## CI/CD Интеграция

### GitHub Actions

Создайте `.github/workflows/quality-check.yml`:

```yaml
name: Quality Check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Quality Guardian
        run: |
          pip install -r requirements.txt

      - name: Run Quality Analysis
        run: |
          python -m archon_quality_guardian.agent
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json
```

### GitLab CI

Добавьте в `.gitlab-ci.yml`:

```yaml
quality_check:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python -m archon_quality_guardian.agent
  artifacts:
    reports:
      codequality: quality-report.json
```

## Доступные инструменты агента

### analyze_code_file
Анализ качества конкретного файла

```python
"Проанализируй файл src/app.py"
```

### review_code_with_ai
AI-powered code review

```python
"Проведи AI review файла src/service.py"
```

### calculate_technical_debt
Расчет технического долга проекта

```python
"Рассчитай технический долг проекта"
```

### get_project_quality_metrics
Общие метрики качества проекта

```python
"Покажи метрики качества проекта"
```

## Архитектура

```
archon_quality_guardian/
├── agent.py                 # Главный агент
├── tools.py                 # Инструменты анализа
├── prompts.py               # Системные промпты
├── dependencies.py          # Зависимости агента
├── settings.py              # Настройки
├── knowledge/               # База знаний
│   └── archon_quality_guardian_knowledge.md
├── examples/                # Примеры конфигураций
│   ├── python_project_config.py
│   ├── typescript_project_config.py
│   └── fullstack_project_config.py
└── tests/                   # Тесты
```

## Интеграция с другими агентами

Quality Guardian может делегировать задачи другим специализированным агентам:

- **Security Audit Agent** - для глубокого security анализа
- **Performance Optimization Agent** - для оптимизации производительности
- **UI/UX Enhancement Agent** - для UI-specific проблем
- **TypeScript Architecture Agent** - для архитектурного анализа TypeScript

Делегирование происходит автоматически через Archon Task Management.

## Best Practices

### 1. Настройте пороги качества под свой проект
```python
deps.test_coverage_threshold = 85.0  # Высокие стандарты
deps.complexity_threshold = 8         # Строгий контроль сложности
```

### 2. Включите автоматические проверки в CI/CD
```yaml
- name: Quality Gate
  run: python -m archon_quality_guardian.agent
  # Fail build если critical issues
```

### 3. Регулярный мониторинг технического долга
```python
# Еженедельный отчет
result = await agent.run("Рассчитай технический долг", deps=deps)
```

### 4. AI Review для критических изменений
```python
# Перед merge важных PR
result = await agent.run(
    "Проведи детальный AI review файла auth.py",
    deps=deps
)
```

## Расширение

### Добавление новых инструментов анализа

```python
# В tools.py
async def custom_analyzer(file_path: str) -> Dict:
    # Ваш анализатор
    return results

# В agent.py
@agent.tool
async def use_custom_analyzer(ctx, file_path: str) -> str:
    results = await custom_analyzer(file_path)
    return format_results(results)
```

### Кастомизация промптов

```python
# В prompts.py
def get_custom_review_prompt(code: str) -> str:
    return f"""
    Кастомный промпт для вашего проекта:
    {code}
    """
```

## Troubleshooting

### Проблема: Инструменты анализа не найдены

Убедитесь что установлены все зависимости:
```bash
pip install pylint flake8 mypy bandit
```

### Проблема: AI review не работает

Проверьте настройки LLM:
```python
deps.enable_ai_review = True
deps.settings.llm_api_key = "your-key"
```

### Проблема: Низкая производительность

Ограничьте количество анализируемых файлов:
```python
# В tools.py, find_project_files
for file in project_files[:20]:  # Только первые 20
```

## Поддержка

- **Issues:** https://github.com/Lambertain/ai-agent-factory/issues
- **Documentation:** https://docs.lambertain.agency
- **Email:** support@lambertain.agency

## Лицензия

MIT License - см. LICENSE файл

## Автор

**Lambertain Agency** - AI Agent Factory Team

---

**Version:** 1.0.0
**Last Updated:** 2025-10-01
