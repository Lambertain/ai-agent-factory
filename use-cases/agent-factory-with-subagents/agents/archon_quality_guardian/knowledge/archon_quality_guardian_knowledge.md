# Archon Quality Guardian Agent Knowledge Base

## Системный промпт для Archon Quality Guardian

```
Ты эксперт по контролю качества кода и автоматизации процессов Quality Assurance. Твоя миссия - обеспечить высочайшее качество кода во всех проектах через автоматизированные проверки, AI-powered code review и интеграцию с CI/CD пайплайнами.

**Твоя экспертиза:**
- Автоматический code review с использованием AI
- Мониторинг метрик качества кода (complexity, coverage, maintainability)
- Выявление технического долга и предложения по рефакторингу
- Интеграция с CI/CD пайплайнами (GitHub Actions, GitLab CI, Jenkins)
- Static code analysis (pylint, flake8, mypy, eslint, tslint)
- Security scanning (bandit, safety, snyk)
- Test coverage анализ и reporting
- Performance profiling и optimization recommendations

**Ключевые обязанности:**

1. **Pre-commit Analysis:**
   - Запуск статического анализа кода
   - Проверка типов и линтинг
   - Security сканирование
   - Auto-fixing простых проблем

2. **Pull Request Review:**
   - AI-powered code review с конкретными рекомендациями
   - Анализ сложности кода
   - Проверка соответствия архитектурным стандартам
   - Валидация test coverage

3. **Post-merge Monitoring:**
   - Отслеживание технического долга
   - Сбор метрик производительности
   - Выявление паттернов проблем
   - Рекомендации по рефакторингу

4. **Continuous Improvement:**
   - Распознавание повторяющихся проблем
   - Эволюция best practices
   - Интеграция feedback от команды
   - Автоматизация рутинных проверок

**Принципы работы:**
- Фокус на предотвращение проблем, а не только их выявление
- Автоматизация всего, что можно автоматизировать
- Предоставление конкретных, actionable рекомендаций
- Обучение команды через quality insights
- Минимизация false positives через контекстный анализ

**Интеграции:**
- GitHub Actions / GitLab CI / Jenkins
- SonarQube / CodeClimate / Codacy
- Sentry / Datadog для мониторинга
- Slack / Discord для уведомлений
- Jira / Linear для tracking технического долга
```

## Архитектура Quality Assurance System

### Компоненты системы

```
Quality Guardian Architecture:

┌─────────────────────────────────────────────────────────────┐
│                   Quality Guardian Agent                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Code       │  │   Security   │  │  Performance │     │
│  │   Analyzer   │  │   Scanner    │  │  Profiler    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   AI Code    │  │   Technical  │  │  Test        │     │
│  │   Reviewer   │  │   Debt Mgr   │  │  Coverage    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │         CI/CD Integration Layer                       │  │
│  │  (GitHub Actions, GitLab CI, Jenkins)                │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Metrics & Reporting Dashboard                 │  │
│  │  (Quality Trends, Technical Debt, Coverage)          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Workflow этапов

```python
# Этапы Quality Assurance Process

PRE_COMMIT_STAGE = {
    "static_analysis": ["pylint", "flake8", "mypy", "eslint"],
    "security_scan": ["bandit", "safety", "snyk"],
    "formatting": ["black", "prettier", "autopep8"],
    "type_checking": ["mypy", "typescript"],
    "auto_fixes": True
}

PULL_REQUEST_STAGE = {
    "ai_code_review": {
        "model": "Claude Sonnet 4",
        "focus_areas": [
            "code_quality",
            "security_issues",
            "performance_concerns",
            "maintainability",
            "test_coverage"
        ]
    },
    "complexity_analysis": {
        "cyclomatic_complexity": True,
        "cognitive_complexity": True,
        "thresholds": {
            "function": 10,
            "class": 50,
            "module": 100
        }
    },
    "architecture_compliance": {
        "patterns": ["clean_architecture", "solid_principles"],
        "anti_patterns": ["god_class", "circular_deps"]
    }
}

POST_MERGE_STAGE = {
    "technical_debt_tracking": {
        "measurement": "hours",
        "categories": ["code_smell", "duplication", "complexity"],
        "alerts": "weekly_report"
    },
    "performance_metrics": {
        "response_time": True,
        "memory_usage": True,
        "database_queries": True
    },
    "refactoring_opportunities": {
        "auto_detect": True,
        "priority_scoring": True
    }
}
```

## Code Quality Metrics

### Метрики и их значение

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class CodeQualityMetrics(BaseModel):
    """Метрики качества кода."""

    # Test Coverage
    test_coverage: float = Field(ge=0.0, le=100.0, description="Процент покрытия тестами")
    branch_coverage: float = Field(ge=0.0, le=100.0, description="Покрытие веток кода")

    # Complexity
    cyclomatic_complexity: float = Field(description="Цикломатическая сложность")
    cognitive_complexity: float = Field(description="Когнитивная сложность")

    # Maintainability
    maintainability_index: float = Field(ge=0.0, le=100.0, description="Индекс поддерживаемости")
    technical_debt_hours: float = Field(description="Технический долг в часах")

    # Security
    security_issues: List["SecurityIssue"] = Field(default_factory=list)
    vulnerability_count: int = Field(default=0)

    # Code Smells
    code_smells: List["CodeSmell"] = Field(default_factory=list)
    duplication_percentage: float = Field(ge=0.0, le=100.0)

    # Performance
    performance_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)

    # Overall
    overall_grade: str = Field(description="A, B, C, D, F")
    timestamp: datetime = Field(default_factory=datetime.now)

class SecurityIssue(BaseModel):
    """Проблема безопасности."""
    severity: str  # critical, high, medium, low
    category: str  # sql_injection, xss, etc.
    file_path: str
    line_number: int
    description: str
    recommendation: str
    cwe_id: Optional[str] = None

class CodeSmell(BaseModel):
    """Code smell."""
    type: str  # long_method, god_class, etc.
    file_path: str
    line_start: int
    line_end: int
    severity: str  # major, minor, info
    description: str
    refactoring_suggestion: str

class ReviewResult(BaseModel):
    """Результат code review."""
    issues: List["QualityIssue"]
    suggestions: List["ImprovementSuggestion"]
    auto_fixable: List["AutoFix"]
    overall_score: float = Field(ge=0.0, le=100.0)
    requires_human_review: bool
    estimated_fix_time: float  # hours

class QualityIssue(BaseModel):
    """Проблема качества."""
    severity: str  # blocker, critical, major, minor, info
    category: str
    file_path: str
    line_number: int
    message: str
    rule_id: str

class ImprovementSuggestion(BaseModel):
    """Предложение по улучшению."""
    type: str  # refactoring, optimization, security
    file_path: str
    description: str
    code_example: Optional[str] = None
    impact: str  # high, medium, low
    effort: str  # hours estimation

class AutoFix(BaseModel):
    """Автоматическое исправление."""
    file_path: str
    line_number: int
    original_code: str
    fixed_code: str
    fix_type: str
    confidence: float = Field(ge=0.0, le=1.0)
```

## AI-Powered Code Review

### Prompt Engineering для Code Review

```python
CODE_REVIEW_SYSTEM_PROMPT = """
Ты опытный senior разработчик, проводящий code review.

**Анализируй код по следующим критериям:**

1. **Code Quality:**
   - Читаемость и понятность
   - Следование принципам SOLID
   - DRY (Don't Repeat Yourself)
   - Правильное именование переменных и функций

2. **Security:**
   - Потенциальные уязвимости
   - SQL injection, XSS, CSRF
   - Правильная обработка пользовательского ввода
   - Безопасное хранение секретов

3. **Performance:**
   - Неэффективные алгоритмы
   - N+1 query проблемы
   - Memory leaks
   - Unnecessary computations

4. **Testing:**
   - Наличие тестов
   - Покрытие edge cases
   - Качество тестов

5. **Architecture:**
   - Соответствие архитектурным паттернам
   - Правильное разделение ответственностей
   - Coupling и cohesion

**Формат ответа:**
- Используй конкретные примеры из кода
- Предлагай конкретные улучшения
- Оценивай серьезность проблем (blocker, critical, major, minor, info)
- Предоставляй примеры исправленного кода где возможно
"""

def create_review_prompt(code: str, context: Dict) -> str:
    """Создать промпт для code review."""
    return f"""
# Code Review Request

## Context
- **Language:** {context.get('language')}
- **Framework:** {context.get('framework')}
- **File:** {context.get('file_path')}
- **Purpose:** {context.get('purpose')}

## Code to Review
```{context.get('language')}
{code}
```

## Previous Reviews
{context.get('previous_reviews', 'None')}

## Specific Concerns
{context.get('concerns', 'General review')}

Проведи детальный code review и предоставь структурированный feedback.
"""
```

### Интеграция с LLM

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CodeReviewDependencies:
    """Зависимости для code review."""
    project_path: str
    language: str
    framework: str
    quality_standards: Dict
    archon_project_id: str

async def perform_ai_code_review(
    code: str,
    file_path: str,
    deps: CodeReviewDependencies
) -> ReviewResult:
    """Провести AI-powered code review."""

    agent = Agent(
        model="claude-sonnet-4",
        system_prompt=CODE_REVIEW_SYSTEM_PROMPT
    )

    context = {
        "language": deps.language,
        "framework": deps.framework,
        "file_path": file_path,
        "purpose": "Code quality and security review"
    }

    prompt = create_review_prompt(code, context)

    result = await agent.run(prompt, deps=deps)

    # Parse AI response and structure it
    return parse_review_result(result.data)
```

## Static Analysis Tools Integration

### Python Tools

```python
PYTHON_QUALITY_TOOLS = {
    "linting": {
        "pylint": {
            "config": ".pylintrc",
            "threshold": 8.0,
            "rules": ["C0111", "W0612", "E1101"]
        },
        "flake8": {
            "max_line_length": 100,
            "ignore": ["E203", "W503"]
        }
    },
    "type_checking": {
        "mypy": {
            "strict": True,
            "config": "mypy.ini"
        }
    },
    "security": {
        "bandit": {
            "level": "medium",
            "confidence": "medium"
        },
        "safety": {
            "check": "dependencies"
        }
    },
    "complexity": {
        "radon": {
            "cc_threshold": 10,
            "mi_threshold": 50
        }
    },
    "coverage": {
        "pytest-cov": {
            "threshold": 80,
            "format": ["html", "xml", "term"]
        }
    }
}

async def run_python_quality_checks(file_path: str) -> Dict:
    """Запустить все проверки качества для Python."""
    results = {}

    # Pylint
    results['pylint'] = await run_command(
        f"pylint {file_path} --output-format=json"
    )

    # Flake8
    results['flake8'] = await run_command(
        f"flake8 {file_path} --format=json"
    )

    # MyPy
    results['mypy'] = await run_command(
        f"mypy {file_path} --json"
    )

    # Bandit (security)
    results['bandit'] = await run_command(
        f"bandit {file_path} -f json"
    )

    # Radon (complexity)
    results['complexity'] = await run_command(
        f"radon cc {file_path} -j"
    )

    return results
```

### TypeScript/JavaScript Tools

```python
TYPESCRIPT_QUALITY_TOOLS = {
    "linting": {
        "eslint": {
            "config": ".eslintrc.json",
            "plugins": ["@typescript-eslint", "react-hooks"]
        }
    },
    "type_checking": {
        "tsc": {
            "strict": True,
            "noImplicitAny": True
        }
    },
    "security": {
        "snyk": {
            "severity_threshold": "high"
        },
        "npm_audit": {
            "level": "moderate"
        }
    },
    "complexity": {
        "complexity-report": {
            "threshold": 10
        }
    },
    "coverage": {
        "jest": {
            "threshold": 80,
            "collectFrom": ["src/**/*.{ts,tsx}"]
        }
    }
}

async def run_typescript_quality_checks(file_path: str) -> Dict:
    """Запустить все проверки качества для TypeScript."""
    results = {}

    # ESLint
    results['eslint'] = await run_command(
        f"eslint {file_path} --format=json"
    )

    # TypeScript Compiler
    results['tsc'] = await run_command(
        "tsc --noEmit --pretty false"
    )

    # Snyk (security)
    results['snyk'] = await run_command(
        f"snyk code test {file_path} --json"
    )

    return results
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Quality Guardian Check

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  quality-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Quality Guardian
        run: |
          pip install quality-guardian

      - name: Run Quality Analysis
        run: |
          quality-guardian analyze \
            --project-path . \
            --output-format json \
            --fail-on-critical
        env:
          ARCHON_API_KEY: ${{ secrets.ARCHON_API_KEY }}
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}

      - name: Post Review Comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('quality-report.json'));

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: generateReviewComment(report)
            });

      - name: Upload Quality Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json
```

### GitLab CI Pipeline

```yaml
quality_check:
  stage: test
  image: python:3.11

  before_script:
    - pip install quality-guardian

  script:
    - quality-guardian analyze --project-path . --output-format json

  artifacts:
    reports:
      codequality: quality-report.json
    paths:
      - quality-report.json
    expire_in: 30 days

  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'
```

## Technical Debt Management

### Отслеживание технического долга

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TechnicalDebtItem(BaseModel):
    """Элемент технического долга."""
    id: str
    type: str  # code_smell, duplication, complexity, security
    severity: str  # blocker, critical, major, minor
    file_path: str
    line_start: int
    line_end: int
    description: str
    estimated_hours: float
    created_at: datetime
    resolved_at: Optional[datetime] = None
    assignee: Optional[str] = None

class TechnicalDebtReport(BaseModel):
    """Отчет по техническому долгу."""
    total_debt_hours: float
    debt_by_type: Dict[str, float]
    debt_by_severity: Dict[str, int]
    trend: str  # increasing, decreasing, stable
    top_files: List[Dict[str, float]]  # file_path -> debt_hours
    recommendations: List[str]

async def calculate_technical_debt(project_path: str) -> TechnicalDebtReport:
    """Рассчитать технический долг проекта."""

    # Собираем все проблемы
    issues = await collect_all_quality_issues(project_path)

    # Рассчитываем debt для каждой проблемы
    debt_items = []
    for issue in issues:
        debt_hours = estimate_fix_time(issue)
        debt_items.append(TechnicalDebtItem(
            id=generate_id(),
            type=issue.category,
            severity=issue.severity,
            file_path=issue.file_path,
            line_start=issue.line_number,
            line_end=issue.line_number + get_issue_span(issue),
            description=issue.message,
            estimated_hours=debt_hours,
            created_at=datetime.now()
        ))

    # Генерируем отчет
    return generate_debt_report(debt_items)
```

## Best Practices для Quality Guardian

### 1. Автоматизация
- Интегрируй все проверки в CI/CD
- Автоматически исправляй простые проблемы
- Блокируй merge при critical issues
- Автоматизируй генерацию отчетов

### 2. AI-Powered Review
- Используй Claude Sonnet 4 для сложного анализа
- Предоставляй конкретные рекомендации с примерами
- Учитывай контекст проекта и историю
- Минимизируй false positives

### 3. Metrics & Monitoring
- Отслеживай тренды качества
- Мониторь технический долг
- Измеряй эффективность команды
- Визуализируй прогресс

### 4. Team Collaboration
- Интегрируй с Slack/Discord для уведомлений
- Предоставляй weekly quality reports
- Обучай команду через insights
- Собирай feedback для улучшений

### 5. Continuous Improvement
- Анализируй повторяющиеся проблемы
- Эволюционируй правила проверок
- Автоматизируй новые паттерны
- Адаптируй под команду и проект
