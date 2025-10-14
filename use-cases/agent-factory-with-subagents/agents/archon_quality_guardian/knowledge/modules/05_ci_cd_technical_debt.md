# Module 05: CI/CD Integration & Technical Debt Management

**Назад к:** [Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)

---

## CI/CD Integration

### GitHub Actions Quality Pipeline

```yaml
# .github/workflows/quality-check.yml
name: Quality Check

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  python-quality:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pylint flake8 mypy bandit black isort pytest pytest-cov

      - name: Code Formatting Check (Black)
        run: black --check .

      - name: Import Sorting Check (isort)
        run: isort --check-only .

      - name: Linting (Pylint)
        run: |
          pylint $(git ls-files '*.py') --fail-under=8.0

      - name: Style Check (Flake8)
        run: flake8 . --count --max-line-length=100 --statistics

      - name: Type Checking (Mypy)
        run: mypy . --strict

      - name: Security Scan (Bandit)
        run: bandit -r . -ll

      - name: Run Tests with Coverage
        run: |
          pytest --cov=. --cov-report=xml --cov-report=term

      - name: Upload Coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  typescript-quality:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[ts]') || github.event_name == 'pull_request'

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Linting (ESLint)
        run: npm run lint

      - name: Type Checking (TSC)
        run: npx tsc --noEmit

      - name: Security Audit (Snyk)
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Tests
        run: npm test -- --coverage

  ai-code-review:
    runs-on: ubuntu-latest
    needs: [python-quality, typescript-quality]
    if: github.event_name == 'pull_request'

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for diff

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install AI Review dependencies
        run: |
          pip install pydantic-ai anthropic

      - name: Run AI Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          python scripts/ai_code_review.py --pr $PR_NUMBER

      - name: Post Review Comments
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const comments = JSON.parse(fs.readFileSync('review_comments.json'));

            for (const comment of comments) {
              await github.rest.pulls.createReviewComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.issue.number,
                body: comment.body,
                path: comment.path,
                line: comment.line
              });
            }

  quality-gate:
    runs-on: ubuntu-latest
    needs: [python-quality, typescript-quality, ai-code-review]
    if: always()

    steps:
      - name: Check Quality Gate
        run: |
          if [ "${{ needs.python-quality.result }}" == "failure" ] || \
             [ "${{ needs.typescript-quality.result }}" == "failure" ]; then
            echo "Quality gate failed!"
            exit 1
          fi

          echo "Quality gate passed!"
```

---

### GitLab CI Quality Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - quality
  - test
  - review

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  NPM_CONFIG_CACHE: "$CI_PROJECT_DIR/.npm"

cache:
  paths:
    - .cache/pip
    - .npm

python-quality:
  stage: quality
  image: python:3.11
  before_script:
    - pip install pylint flake8 mypy bandit black isort
  script:
    - black --check .
    - isort --check-only .
    - pylint $(git ls-files '*.py') --fail-under=8.0 --output-format=colorized
    - flake8 . --count --max-line-length=100 --statistics
    - mypy . --strict
    - bandit -r . -ll -f json -o bandit-report.json
  artifacts:
    reports:
      codequality: bandit-report.json
    when: always
  allow_failure: false

typescript-quality:
  stage: quality
  image: node:18
  before_script:
    - npm ci
  script:
    - npm run lint
    - npx tsc --noEmit
    - npx snyk test --severity-threshold=high
  only:
    changes:
      - "**/*.ts"
      - "**/*.tsx"
      - package.json
  allow_failure: false

unit-tests:
  stage: test
  image: python:3.11
  before_script:
    - pip install pytest pytest-cov
  script:
    - pytest --cov=. --cov-report=xml --cov-report=term --cov-fail-under=80
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

ai-code-review:
  stage: review
  image: python:3.11
  before_script:
    - pip install pydantic-ai anthropic
  script:
    - python scripts/ai_code_review.py --mr $CI_MERGE_REQUEST_IID
  only:
    - merge_requests
  when: manual
  allow_failure: true
```

---

## Technical Debt Management

### TechnicalDebt Tracking Model

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class TechnicalDebtItem(BaseModel):
    """Элемент технического долга."""

    id: str = Field(description="Уникальный идентификатор")
    title: str = Field(description="Краткое описание проблемы")
    description: str = Field(description="Детальное описание")

    # Location
    file_path: str = Field(description="Путь к файлу")
    line_start: int = Field(description="Начальная строка")
    line_end: Optional[int] = Field(default=None, description="Конечная строка")

    # Classification
    category: Literal[
        "code_smell",
        "outdated_dependency",
        "missing_tests",
        "poor_architecture",
        "security_debt",
        "performance_debt",
        "documentation_debt"
    ]

    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Серьезность долга"
    )

    # Impact
    impact_areas: List[str] = Field(
        default_factory=list,
        description="Области влияния (maintainability, security, performance)"
    )

    estimated_fix_hours: float = Field(
        description="Оценка времени на исправление"
    )

    compound_interest_factor: float = Field(
        default=1.1,
        description="Фактор роста долга со временем (monthly)"
    )

    # Tracking
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    # Priority
    priority_score: float = Field(
        default=0.0,
        description="Вычисляемый приоритет (0-100)"
    )

    def calculate_priority(self) -> float:
        """Рассчитать приоритет на основе severity, impact, age."""

        # Severity weight (40%)
        severity_scores = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25
        }
        severity_weight = severity_scores[self.severity] * 0.4

        # Impact weight (30%)
        impact_weight = len(self.impact_areas) * 10 * 0.3

        # Age weight (20%)
        age_days = (datetime.now() - self.created_at).days
        age_weight = min(age_days / 90 * 100, 100) * 0.2  # Max 90 days

        # Estimated effort weight (10%) - меньше = выше приоритет (quick wins)
        effort_weight = max(0, 100 - self.estimated_fix_hours * 5) * 0.1

        self.priority_score = severity_weight + impact_weight + age_weight + effort_weight
        return self.priority_score

    def calculate_current_cost(self) -> float:
        """Рассчитать текущую стоимость долга с учетом compound interest."""

        months_elapsed = (datetime.now() - self.created_at).days / 30
        current_cost = self.estimated_fix_hours * (self.compound_interest_factor ** months_elapsed)

        return current_cost

class TechnicalDebtReport(BaseModel):
    """Отчет о техническом долге проекта."""

    project_name: str
    items: List[TechnicalDebtItem] = Field(default_factory=list)

    # Summary
    total_items: int = 0
    total_estimated_hours: float = 0.0
    total_current_cost_hours: float = 0.0

    # Breakdown by category
    by_category: Dict[str, int] = Field(default_factory=dict)

    # Breakdown by severity
    by_severity: Dict[str, int] = Field(default_factory=dict)

    # Top priority items
    top_priority_items: List[TechnicalDebtItem] = Field(default_factory=list)

    generated_at: datetime = Field(default_factory=datetime.now)

    def calculate_summary(self):
        """Рассчитать summary метрики."""

        self.total_items = len(self.items)
        self.total_estimated_hours = sum(item.estimated_fix_hours for item in self.items)
        self.total_current_cost_hours = sum(item.calculate_current_cost() for item in self.items)

        # Category breakdown
        self.by_category = {}
        for item in self.items:
            self.by_category[item.category] = self.by_category.get(item.category, 0) + 1

        # Severity breakdown
        self.by_severity = {}
        for item in self.items:
            self.by_severity[item.severity] = self.by_severity.get(item.severity, 0) + 1

        # Top priority (top 10)
        sorted_items = sorted(self.items, key=lambda x: x.calculate_priority(), reverse=True)
        self.top_priority_items = sorted_items[:10]

    def to_markdown(self) -> str:
        """Генерация markdown отчета."""

        self.calculate_summary()

        report = f"""# Technical Debt Report: {self.project_name}

## Summary
- **Total Items:** {self.total_items}
- **Estimated Fix Time:** {self.total_estimated_hours:.1f} hours
- **Current Cost (with interest):** {self.total_current_cost_hours:.1f} hours
- **Cost Increase:** {((self.total_current_cost_hours / self.total_estimated_hours - 1) * 100):.1f}%

## Breakdown by Category
"""
        for category, count in sorted(self.by_category.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category}:** {count} items\n"

        report += "\n## Breakdown by Severity\n"
        for severity, count in sorted(self.by_severity.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{severity}:** {count} items\n"

        report += "\n## Top 10 Priority Items\n"
        for i, item in enumerate(self.top_priority_items, 1):
            report += f"""
### {i}. {item.title} [Priority: {item.priority_score:.1f}]
- **File:** {item.file_path}:{item.line_start}
- **Severity:** {item.severity}
- **Category:** {item.category}
- **Estimated Fix:** {item.estimated_fix_hours:.1f}h
- **Current Cost:** {item.calculate_current_cost():.1f}h
- **Description:** {item.description}
"""

        return report
```

---

### Technical Debt Detector

```python
class TechnicalDebtDetector:
    """Автоматическое обнаружение технического долга."""

    def __init__(self):
        self.debt_items: List[TechnicalDebtItem] = []

    async def scan_project(self, project_path: str) -> TechnicalDebtReport:
        """Сканирование проекта на технический долг."""

        # 1. Code smells из static analysis
        code_smell_items = await self._detect_code_smells(project_path)
        self.debt_items.extend(code_smell_items)

        # 2. Outdated dependencies
        dependency_items = await self._detect_outdated_dependencies(project_path)
        self.debt_items.extend(dependency_items)

        # 3. Missing tests
        test_items = await self._detect_missing_tests(project_path)
        self.debt_items.extend(test_items)

        # 4. Security debt
        security_items = await self._detect_security_debt(project_path)
        self.debt_items.extend(security_items)

        # 5. TODO/FIXME comments
        todo_items = await self._detect_todo_comments(project_path)
        self.debt_items.extend(todo_items)

        # Генерация отчета
        report = TechnicalDebtReport(
            project_name=Path(project_path).name,
            items=self.debt_items
        )
        report.calculate_summary()

        return report

    async def _detect_code_smells(self, project_path: str) -> List[TechnicalDebtItem]:
        """Обнаружение code smells."""
        items = []

        # Запуск pylint
        result = await run_pylint([project_path], PythonAnalysisConfig())

        for issue in result.issues:
            if issue["type"] in ["refactor", "convention"]:
                items.append(TechnicalDebtItem(
                    id=f"smell_{hash(issue['message'])}",
                    title=f"Code Smell: {issue['symbol']}",
                    description=issue["message"],
                    file_path=issue["path"],
                    line_start=issue["line"],
                    category="code_smell",
                    severity="medium",
                    impact_areas=["maintainability"],
                    estimated_fix_hours=1.0
                ))

        return items

    async def _detect_outdated_dependencies(self, project_path: str) -> List[TechnicalDebtItem]:
        """Обнаружение устаревших зависимостей."""
        items = []

        # Python dependencies (pip-outdated)
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            outdated = json.loads(result.stdout)

            for pkg in outdated:
                items.append(TechnicalDebtItem(
                    id=f"dep_{pkg['name']}",
                    title=f"Outdated: {pkg['name']}",
                    description=f"Current: {pkg['version']}, Latest: {pkg['latest_version']}",
                    file_path="requirements.txt",
                    line_start=1,
                    category="outdated_dependency",
                    severity="low",
                    impact_areas=["security", "performance"],
                    estimated_fix_hours=0.5
                ))

        return items

    async def _detect_missing_tests(self, project_path: str) -> List[TechnicalDebtItem]:
        """Обнаружение файлов без тестов."""
        items = []

        # Найти все .py файлы
        py_files = list(Path(project_path).rglob("*.py"))

        for py_file in py_files:
            if "test" not in str(py_file) and "venv" not in str(py_file):
                # Проверить есть ли соответствующий тест файл
                test_file = self._find_test_file(py_file)

                if not test_file or not test_file.exists():
                    # Оценка по размеру файла
                    lines = len(py_file.read_text().splitlines())
                    estimated_hours = lines / 50  # 50 lines = 1 hour tests

                    items.append(TechnicalDebtItem(
                        id=f"test_{py_file.stem}",
                        title=f"Missing tests: {py_file.name}",
                        description=f"No test coverage found for {py_file}",
                        file_path=str(py_file),
                        line_start=1,
                        category="missing_tests",
                        severity="high",
                        impact_areas=["reliability", "maintainability"],
                        estimated_fix_hours=estimated_hours
                    ))

        return items

    async def _detect_security_debt(self, project_path: str) -> List[TechnicalDebtItem]:
        """Обнаружение security debt."""
        items = []

        # Запуск bandit
        result = await run_bandit([project_path], PythonAnalysisConfig())

        for issue in result.issues:
            items.append(TechnicalDebtItem(
                id=f"sec_{issue['test_id']}_{issue['line_number']}",
                title=f"Security: {issue['issue_text']}",
                description=issue["issue_text"],
                file_path=issue["filename"],
                line_start=issue["line_number"],
                category="security_debt",
                severity=issue["issue_severity"].lower(),
                impact_areas=["security"],
                estimated_fix_hours=2.0
            ))

        return items

    async def _detect_todo_comments(self, project_path: str) -> List[TechnicalDebtItem]:
        """Обнаружение TODO/FIXME комментариев."""
        items = []

        py_files = list(Path(project_path).rglob("*.py"))

        for py_file in py_files:
            if "venv" in str(py_file):
                continue

            content = py_file.read_text()

            for i, line in enumerate(content.splitlines(), 1):
                if "TODO" in line or "FIXME" in line:
                    items.append(TechnicalDebtItem(
                        id=f"todo_{py_file.stem}_{i}",
                        title=f"TODO: {line.strip()}",
                        description=line.strip(),
                        file_path=str(py_file),
                        line_start=i,
                        category="documentation_debt",
                        severity="low",
                        impact_areas=["maintainability"],
                        estimated_fix_hours=0.5
                    ))

        return items

    def _find_test_file(self, source_file: Path) -> Optional[Path]:
        """Найти соответствующий тестовый файл."""
        test_patterns = [
            source_file.parent / f"test_{source_file.name}",
            source_file.parent / "tests" / f"test_{source_file.name}",
            source_file.parent.parent / "tests" / f"test_{source_file.name}"
        ]

        for pattern in test_patterns:
            if pattern.exists():
                return pattern

        return None
```

---

## Best Practices для CI/CD Quality

### 1. Fail Fast принцип

```yaml
# Запускать быстрые проверки первыми
stages:
  - lint       # 30s - быстро
  - typecheck  # 1min
  - test       # 3min
  - security   # 5min
  - review     # 10min (manual)
```

### 2. Caching для скорости

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - .npm
    - node_modules/
```

### 3. Parallel execution

```yaml
# Запускать Python и TypeScript проверки параллельно
python-quality:
  stage: quality
  # ...

typescript-quality:
  stage: quality
  # ... (параллельно с python)
```

### 4. Quality metrics tracking

```python
# Отправка метрик в monitoring
async def track_quality_metrics(report: QualityReport):
    """Отправка метрик качества в Prometheus/Datadog."""

    metrics = {
        "quality_score": report.metrics.overall_grade,
        "test_coverage": report.metrics.test_coverage,
        "security_issues": report.metrics.vulnerability_count,
        "technical_debt_hours": report.metrics.technical_debt_hours
    }

    # Push to monitoring system
    await push_metrics(metrics)
```

---

**Навигация:**
- [← Предыдущий модуль: Static Analysis Integration](04_static_analysis_integration.md)
- [↑ Назад к Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)
