# Module 02: Metrics & Quality Models

**Назад к:** [Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)

---

## Pydantic Models для метрик качества

### CodeQualityMetrics: Основные метрики качества кода

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

    def calculate_overall_grade(self) -> str:
        """Рассчитать общую оценку на основе всех метрик."""
        score = 0.0

        # Test Coverage (30% веса)
        score += (self.test_coverage / 100) * 30

        # Maintainability (25% веса)
        score += (self.maintainability_index / 100) * 25

        # Complexity (20% веса)
        complexity_score = max(0, 100 - self.cyclomatic_complexity * 2)
        score += (complexity_score / 100) * 20

        # Security (15% веса)
        security_score = 100 if self.vulnerability_count == 0 else max(0, 100 - self.vulnerability_count * 10)
        score += (security_score / 100) * 15

        # Code Smells (10% веса)
        smell_score = max(0, 100 - len(self.code_smells) * 5)
        score += (smell_score / 100) * 10

        # Преобразование в grade
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
```

**Ключевые характеристики:**
- **Weighted scoring** - разные метрики имеют разный вес
- **Test Coverage** - 30% (самый важный фактор)
- **Maintainability** - 25% (долгосрочная поддержка)
- **Complexity** - 20% (читаемость и понимание)
- **Security** - 15% (критично для production)
- **Code Smells** - 10% (качество кода)

---

### SecurityIssue: Модель проблем безопасности

```python
from enum import Enum

class SecuritySeverity(str, Enum):
    """Уровень серьезности security проблемы."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class SecurityIssue(BaseModel):
    """Проблема безопасности в коде."""

    id: str = Field(description="Уникальный идентификатор проблемы")
    severity: SecuritySeverity = Field(description="Уровень серьезности")
    category: str = Field(description="Категория (SQL Injection, XSS, etc)")

    title: str = Field(description="Краткое описание проблемы")
    description: str = Field(description="Детальное описание")

    file_path: str = Field(description="Путь к файлу")
    line_number: int = Field(description="Номер строки")

    cwe_id: Optional[str] = Field(default=None, description="CWE ID (Common Weakness Enumeration)")
    cve_id: Optional[str] = Field(default=None, description="CVE ID если применимо")

    remediation: str = Field(description="Как исправить")
    references: List[str] = Field(default_factory=list, description="Ссылки на документацию")

    detected_by: str = Field(description="Инструмент обнаружения (bandit, snyk, etc)")
    detected_at: datetime = Field(default_factory=datetime.now)

    @property
    def is_critical(self) -> bool:
        """Является ли проблема критической."""
        return self.severity in [SecuritySeverity.CRITICAL, SecuritySeverity.HIGH]

    @property
    def risk_score(self) -> int:
        """Оценка риска от 0 до 100."""
        severity_scores = {
            SecuritySeverity.CRITICAL: 100,
            SecuritySeverity.HIGH: 75,
            SecuritySeverity.MEDIUM: 50,
            SecuritySeverity.LOW: 25,
            SecuritySeverity.INFO: 10
        }
        return severity_scores[self.severity]
```

**Когда использовать:**
- При обнаружении security vulnerabilities через bandit, snyk
- При manual security audit
- При анализе dependency vulnerabilities

**Примеры проблем:**
- SQL Injection (CWE-89)
- XSS (CWE-79)
- Hardcoded credentials (CWE-798)
- Path Traversal (CWE-22)
- Insecure Deserialization (CWE-502)

---

### CodeSmell: Модель code smells

```python
class CodeSmellType(str, Enum):
    """Типы code smells."""
    LONG_METHOD = "long_method"
    LARGE_CLASS = "large_class"
    DUPLICATE_CODE = "duplicate_code"
    LONG_PARAMETER_LIST = "long_parameter_list"
    DEAD_CODE = "dead_code"
    SPECULATIVE_GENERALITY = "speculative_generality"
    FEATURE_ENVY = "feature_envy"
    INAPPROPRIATE_INTIMACY = "inappropriate_intimacy"
    DATA_CLUMPS = "data_clumps"
    PRIMITIVE_OBSESSION = "primitive_obsession"
    SWITCH_STATEMENTS = "switch_statements"
    PARALLEL_INHERITANCE = "parallel_inheritance"
    LAZY_CLASS = "lazy_class"
    MIDDLE_MAN = "middle_man"

class CodeSmell(BaseModel):
    """Code smell в коде."""

    type: CodeSmellType = Field(description="Тип code smell")
    severity: str = Field(description="minor, major, critical")

    file_path: str = Field(description="Путь к файлу")
    line_start: int = Field(description="Начальная строка")
    line_end: int = Field(description="Конечная строка")

    description: str = Field(description="Описание проблемы")
    suggestion: str = Field(description="Предложение по исправлению")

    metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Метрики (lines_of_code, complexity, etc)"
    )

    detected_by: str = Field(description="Инструмент обнаружения")
    detected_at: datetime = Field(default_factory=datetime.now)

    @property
    def estimated_refactoring_hours(self) -> float:
        """Оценка времени на рефакторинг."""
        # Базовая оценка по типу smell
        base_hours = {
            CodeSmellType.LONG_METHOD: 2.0,
            CodeSmellType.LARGE_CLASS: 4.0,
            CodeSmellType.DUPLICATE_CODE: 1.5,
            CodeSmellType.LONG_PARAMETER_LIST: 1.0,
            CodeSmellType.DEAD_CODE: 0.5,
            CodeSmellType.FEATURE_ENVY: 3.0,
            CodeSmellType.DATA_CLUMPS: 2.0,
        }

        base = base_hours.get(self.type, 1.0)

        # Корректировка на severity
        severity_multipliers = {
            "minor": 0.5,
            "major": 1.0,
            "critical": 2.0
        }

        return base * severity_multipliers.get(self.severity, 1.0)
```

**Когда использовать:**
- При статическом анализе с pylint, flake8
- При manual code review
- При расчете технического долга

**Примеры обнаружения:**
```python
# LONG_METHOD - функция > 50 строк
def process_user_data(user_id, data, options):  # 150 lines
    # ... слишком много логики
    pass

# DUPLICATE_CODE - повторяющиеся блоки
def validate_email(email):
    if not email or '@' not in email:  # Дубликат
        return False
    return True

def validate_user_email(user):
    if not user.email or '@' not in user.email:  # Дубликат
        return False
    return True

# LONG_PARAMETER_LIST - > 5 параметров
def create_user(name, email, password, age, country, city, phone, address):
    pass
```

---

### QualityReport: Агрегированный отчет о качестве

```python
class QualityReport(BaseModel):
    """Полный отчет о качестве проекта/PR."""

    # Metadata
    project_name: str
    commit_sha: Optional[str] = None
    pull_request_id: Optional[int] = None
    branch: str = "main"

    # Metrics
    metrics: CodeQualityMetrics

    # Issues breakdown
    total_issues: int = 0
    critical_issues: int = 0
    high_priority_issues: int = 0
    medium_priority_issues: int = 0
    low_priority_issues: int = 0

    # Files analyzed
    files_analyzed: int = 0
    lines_of_code: int = 0

    # Time
    analysis_duration_seconds: float = 0.0
    generated_at: datetime = Field(default_factory=datetime.now)

    # Comparison with previous
    previous_grade: Optional[str] = None
    grade_delta: Optional[str] = None  # "+1" or "-1"

    # Recommendations
    recommendations: List[str] = Field(default_factory=list)

    def add_recommendation(self, condition: bool, message: str):
        """Добавить рекомендацию если условие выполнено."""
        if condition:
            self.recommendations.append(message)

    def generate_recommendations(self):
        """Генерация рекомендаций на основе метрик."""
        self.recommendations.clear()

        # Test Coverage
        if self.metrics.test_coverage < 80:
            self.add_recommendation(
                True,
                f"Увеличить покрытие тестами до 80% (сейчас {self.metrics.test_coverage:.1f}%)"
            )

        # Security
        if self.metrics.vulnerability_count > 0:
            self.add_recommendation(
                True,
                f"Исправить {self.metrics.vulnerability_count} security vulnerabilities"
            )

        # Complexity
        if self.metrics.cyclomatic_complexity > 10:
            self.add_recommendation(
                True,
                "Упростить сложную логику (complexity > 10)"
            )

        # Code Smells
        critical_smells = [s for s in self.metrics.code_smells if s.severity == "critical"]
        if critical_smells:
            self.add_recommendation(
                True,
                f"Рефакторинг {len(critical_smells)} критических code smells"
            )

        # Technical Debt
        if self.metrics.technical_debt_hours > 40:
            self.add_recommendation(
                True,
                f"Выделить время на погашение технического долга ({self.metrics.technical_debt_hours:.1f} часов)"
            )

    def to_markdown(self) -> str:
        """Генерация markdown отчета."""
        self.generate_recommendations()

        report = f"""# Quality Report: {self.project_name}

## Overall Grade: {self.metrics.overall_grade}
{f"Previous: {self.previous_grade} ({self.grade_delta})" if self.previous_grade else ""}

## Key Metrics
- **Test Coverage:** {self.metrics.test_coverage:.1f}%
- **Maintainability Index:** {self.metrics.maintainability_index:.1f}/100
- **Cyclomatic Complexity:** {self.metrics.cyclomatic_complexity:.1f}
- **Security Issues:** {self.metrics.vulnerability_count}
- **Code Smells:** {len(self.metrics.code_smells)}
- **Technical Debt:** {self.metrics.technical_debt_hours:.1f} hours

## Issues Breakdown
- Critical: {self.critical_issues}
- High: {self.high_priority_issues}
- Medium: {self.medium_priority_issues}
- Low: {self.low_priority_issues}

## Analysis Details
- Files Analyzed: {self.files_analyzed}
- Lines of Code: {self.lines_of_code}
- Analysis Duration: {self.analysis_duration_seconds:.2f}s

## Recommendations
"""
        for i, rec in enumerate(self.recommendations, 1):
            report += f"{i}. {rec}\n"

        return report
```

**Использование:**
```python
# Создание отчета
report = QualityReport(
    project_name="MyProject",
    commit_sha="abc123",
    branch="feature/new-api",
    metrics=metrics,
    files_analyzed=150,
    lines_of_code=12500
)

# Генерация рекомендаций
report.generate_recommendations()

# Экспорт в markdown
markdown = report.to_markdown()

# Сохранение
with open("quality_report.md", "w") as f:
    f.write(markdown)
```

---

## Best Practices для работы с метриками

### 1. Определение порогов качества

```python
QUALITY_THRESHOLDS = {
    "test_coverage": {
        "excellent": 90.0,
        "good": 80.0,
        "acceptable": 70.0,
        "poor": 60.0
    },
    "maintainability_index": {
        "excellent": 85.0,
        "good": 75.0,
        "acceptable": 65.0,
        "poor": 50.0
    },
    "cyclomatic_complexity": {
        "excellent": 5.0,
        "good": 10.0,
        "acceptable": 15.0,
        "poor": 20.0
    },
    "security_vulnerabilities": {
        "excellent": 0,
        "good": 0,
        "acceptable": 1,
        "poor": 5
    }
}

def evaluate_metric(value: float, metric_name: str) -> str:
    """Оценка метрики по порогам."""
    thresholds = QUALITY_THRESHOLDS[metric_name]

    if value >= thresholds["excellent"]:
        return "excellent"
    elif value >= thresholds["good"]:
        return "good"
    elif value >= thresholds["acceptable"]:
        return "acceptable"
    else:
        return "poor"
```

### 2. Трекинг метрик во времени

```python
class MetricsHistory(BaseModel):
    """История метрик проекта."""

    project_name: str
    metrics: List[CodeQualityMetrics] = Field(default_factory=list)

    def add_snapshot(self, metrics: CodeQualityMetrics):
        """Добавить снимок метрик."""
        self.metrics.append(metrics)

    def get_trend(self, metric_name: str) -> str:
        """Получить тренд метрики (improving, stable, declining)."""
        if len(self.metrics) < 2:
            return "stable"

        recent = [getattr(m, metric_name) for m in self.metrics[-5:]]

        if all(recent[i] >= recent[i-1] for i in range(1, len(recent))):
            return "improving"
        elif all(recent[i] <= recent[i-1] for i in range(1, len(recent))):
            return "declining"
        else:
            return "stable"
```

### 3. Автоматическая генерация action items

```python
def generate_action_items(report: QualityReport) -> List[Dict]:
    """Генерация задач для улучшения качества."""
    actions = []

    # Critical security issues
    critical_security = [
        issue for issue in report.metrics.security_issues
        if issue.is_critical
    ]
    for issue in critical_security:
        actions.append({
            "priority": "P1-Critical",
            "title": f"Fix Security: {issue.title}",
            "description": issue.description,
            "assignee": "Implementation Engineer",
            "file": issue.file_path,
            "line": issue.line_number
        })

    # Low test coverage
    if report.metrics.test_coverage < 80:
        actions.append({
            "priority": "P2-High",
            "title": "Increase Test Coverage",
            "description": f"Current: {report.metrics.test_coverage:.1f}%, Target: 80%",
            "assignee": "Quality Guardian"
        })

    # Critical code smells
    critical_smells = [
        smell for smell in report.metrics.code_smells
        if smell.severity == "critical"
    ]
    for smell in critical_smells:
        actions.append({
            "priority": "P2-High",
            "title": f"Refactor: {smell.type.value}",
            "description": smell.description,
            "assignee": "Implementation Engineer",
            "file": smell.file_path,
            "estimated_hours": smell.estimated_refactoring_hours
        })

    return actions
```

---

**Навигация:**
- [← Предыдущий модуль: QA Architecture & Process](01_qa_architecture_process.md)
- [↑ Назад к Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)
- [→ Следующий модуль: AI-Powered Code Review](03_ai_powered_code_review.md)
