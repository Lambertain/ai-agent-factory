# Module 04: Static Analysis Integration

**Назад к:** [Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)

---

## Python Static Analysis Tools

### Configuration класс для Python инструментов

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from pathlib import Path
import subprocess
import json

class PythonAnalysisConfig(BaseModel):
    """Конфигурация Python static analysis."""

    # Pylint
    pylint_enabled: bool = True
    pylint_rcfile: Optional[str] = None
    pylint_min_score: float = 8.0

    # Flake8
    flake8_enabled: bool = True
    flake8_max_line_length: int = 100
    flake8_ignore: List[str] = Field(default_factory=lambda: ["E203", "W503"])

    # Mypy
    mypy_enabled: bool = True
    mypy_strict: bool = True
    mypy_ignore_missing_imports: bool = False

    # Bandit (security)
    bandit_enabled: bool = True
    bandit_severity_level: str = "medium"  # low, medium, high

    # Black (formatter check)
    black_enabled: bool = True
    black_line_length: int = 100

    # isort (import sorting)
    isort_enabled: bool = True

class PythonAnalysisResult(BaseModel):
    """Результат Python static analysis."""

    tool: str = Field(description="Название инструмента")
    success: bool = Field(description="Прошла ли проверка")
    score: Optional[float] = Field(default=None, description="Оценка (для pylint)")

    issues: List[Dict] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    execution_time_seconds: float = 0.0
```

---

### Pylint Integration

```python
import subprocess
import json
from typing import List

async def run_pylint(
    file_paths: List[str],
    config: PythonAnalysisConfig
) -> PythonAnalysisResult:
    """Запуск Pylint анализа."""

    cmd = ["pylint", "--output-format=json"]

    if config.pylint_rcfile:
        cmd.extend(["--rcfile", config.pylint_rcfile])

    cmd.extend(file_paths)

    # Запуск
    import time
    start = time.time()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    execution_time = time.time() - start

    # Парсинг JSON output
    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        issues = []

    # Извлечение score из stderr
    score = extract_pylint_score(result.stderr)

    # Группировка по severity
    errors = [i for i in issues if i["type"] == "error"]
    warnings = [i for i in issues if i["type"] == "warning"]

    return PythonAnalysisResult(
        tool="pylint",
        success=score >= config.pylint_min_score if score else False,
        score=score,
        issues=issues,
        errors=[f"{e['path']}:{e['line']} - {e['message']}" for e in errors],
        warnings=[f"{w['path']}:{w['line']} - {w['message']}" for w in warnings],
        execution_time_seconds=execution_time
    )


def extract_pylint_score(stderr: str) -> Optional[float]:
    """Извлечь score из Pylint stderr."""
    import re

    match = re.search(r"Your code has been rated at ([\d.]+)/10", stderr)
    if match:
        return float(match.group(1))
    return None
```

**Пример .pylintrc:**
```ini
[MASTER]
ignore=venv,__pycache__,.git
jobs=4

[MESSAGES CONTROL]
disable=C0111,  # missing-docstring (слишком шумно)
        C0103,  # invalid-name
        R0903   # too-few-public-methods

[FORMAT]
max-line-length=100
indent-string='    '

[DESIGN]
max-args=7
max-locals=20
max-returns=6
max-branches=15
max-statements=60
```

---

### Flake8 Integration

```python
async def run_flake8(
    file_paths: List[str],
    config: PythonAnalysisConfig
) -> PythonAnalysisResult:
    """Запуск Flake8 анализа."""

    cmd = [
        "flake8",
        f"--max-line-length={config.flake8_max_line_length}",
        f"--ignore={','.join(config.flake8_ignore)}"
    ]
    cmd.extend(file_paths)

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start

    # Парсинг output
    issues = []
    for line in result.stdout.splitlines():
        if line.strip():
            # Формат: path:line:col: error_code message
            parts = line.split(':', 3)
            if len(parts) >= 4:
                issues.append({
                    "path": parts[0],
                    "line": int(parts[1]),
                    "column": int(parts[2]),
                    "message": parts[3].strip()
                })

    return PythonAnalysisResult(
        tool="flake8",
        success=len(issues) == 0,
        issues=issues,
        errors=[f"{i['path']}:{i['line']} - {i['message']}" for i in issues],
        execution_time_seconds=execution_time
    )
```

**Пример .flake8:**
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    build,
    dist

per-file-ignores =
    __init__.py:F401  # Игнорировать unused imports в __init__.py
```

---

### Mypy Integration

```python
async def run_mypy(
    file_paths: List[str],
    config: PythonAnalysisConfig
) -> PythonAnalysisResult:
    """Запуск Mypy type checking."""

    cmd = ["mypy", "--show-error-codes", "--pretty"]

    if config.mypy_strict:
        cmd.append("--strict")

    if config.mypy_ignore_missing_imports:
        cmd.append("--ignore-missing-imports")

    cmd.extend(file_paths)

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start

    # Парсинг output
    issues = []
    for line in result.stdout.splitlines():
        if ": error:" in line or ": note:" in line:
            issues.append({"message": line.strip()})

    errors = [i for i in issues if ": error:" in i["message"]]

    return PythonAnalysisResult(
        tool="mypy",
        success=len(errors) == 0,
        issues=issues,
        errors=[i["message"] for i in errors],
        execution_time_seconds=execution_time
    )
```

**Пример mypy.ini:**
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True

[mypy-tests.*]
disallow_untyped_defs = False
```

---

### Bandit Integration (Security)

```python
async def run_bandit(
    file_paths: List[str],
    config: PythonAnalysisConfig
) -> PythonAnalysisResult:
    """Запуск Bandit security scan."""

    cmd = [
        "bandit",
        "-f", "json",
        "-ll",  # Only low severity and above
        "-r"    # Recursive
    ]
    cmd.extend(file_paths)

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start

    # Парсинг JSON
    try:
        data = json.loads(result.stdout)
        issues = data.get("results", [])
    except json.JSONDecodeError:
        issues = []

    # Фильтрация по severity
    severity_map = {"low": 1, "medium": 2, "high": 3}
    min_severity = severity_map.get(config.bandit_severity_level, 2)

    filtered_issues = [
        i for i in issues
        if severity_map.get(i["issue_severity"].lower(), 0) >= min_severity
    ]

    # Группировка
    errors = [i for i in filtered_issues if i["issue_severity"].lower() == "high"]

    return PythonAnalysisResult(
        tool="bandit",
        success=len(errors) == 0,
        issues=filtered_issues,
        errors=[
            f"{i['filename']}:{i['line_number']} - {i['issue_text']} (CWE-{i.get('cwe', {}).get('id', 'N/A')})"
            for i in errors
        ],
        execution_time_seconds=execution_time
    )
```

**Пример .bandit:**
```yaml
exclude_dirs:
  - /venv/
  - /tests/
  - /.git/

tests:
  - B101  # assert_used
  - B601  # paramiko_calls
  - B602  # shell_injection

skips:
  - B404  # import_subprocess (too noisy)
  - B603  # subprocess_without_shell_equals_true
```

---

## TypeScript Static Analysis Tools

### Configuration для TypeScript

```python
class TypeScriptAnalysisConfig(BaseModel):
    """Конфигурация TypeScript static analysis."""

    # ESLint
    eslint_enabled: bool = True
    eslint_config_path: Optional[str] = None
    eslint_fix: bool = False

    # TypeScript Compiler
    tsc_enabled: bool = True
    tsc_strict: bool = True
    tsc_config_path: Optional[str] = "tsconfig.json"

    # Snyk (security)
    snyk_enabled: bool = True
    snyk_severity_threshold: str = "medium"  # low, medium, high

class TypeScriptAnalysisResult(BaseModel):
    """Результат TypeScript static analysis."""

    tool: str
    success: bool
    issues: List[Dict] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    execution_time_seconds: float = 0.0
```

---

### ESLint Integration

```python
async def run_eslint(
    file_paths: List[str],
    config: TypeScriptAnalysisConfig
) -> TypeScriptAnalysisResult:
    """Запуск ESLint анализа."""

    cmd = ["npx", "eslint", "--format=json"]

    if config.eslint_config_path:
        cmd.extend(["--config", config.eslint_config_path])

    if config.eslint_fix:
        cmd.append("--fix")

    cmd.extend(file_paths)

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    execution_time = time.time() - start

    # Парсинг JSON output
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = []

    # Извлечение всех issues
    all_issues = []
    errors = []
    warnings = []

    for file_result in data:
        for message in file_result.get("messages", []):
            issue = {
                "file": file_result["filePath"],
                "line": message["line"],
                "column": message["column"],
                "severity": message["severity"],  # 1=warning, 2=error
                "message": message["message"],
                "ruleId": message.get("ruleId")
            }
            all_issues.append(issue)

            formatted = f"{issue['file']}:{issue['line']}:{issue['column']} - {issue['message']} ({issue['ruleId']})"

            if message["severity"] == 2:
                errors.append(formatted)
            else:
                warnings.append(formatted)

    return TypeScriptAnalysisResult(
        tool="eslint",
        success=len(errors) == 0,
        issues=all_issues,
        errors=errors,
        warnings=warnings,
        execution_time_seconds=execution_time
    )
```

**Пример .eslintrc.json:**
```json
{
  "parser": "@typescript-eslint/parser",
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "no-console": "warn",
    "eqeqeq": "error",
    "curly": "error"
  }
}
```

---

### TypeScript Compiler Integration

```python
async def run_tsc(
    project_path: str,
    config: TypeScriptAnalysisConfig
) -> TypeScriptAnalysisResult:
    """Запуск TypeScript compiler check."""

    cmd = ["npx", "tsc", "--noEmit"]

    if config.tsc_config_path:
        cmd.extend(["--project", config.tsc_config_path])

    start = time.time()
    result = subprocess.run(
        cmd,
        cwd=project_path,
        capture_output=True,
        text=True
    )
    execution_time = time.time() - start

    # Парсинг output
    issues = []
    errors = []

    for line in result.stdout.splitlines():
        if " error TS" in line:
            issues.append({"message": line.strip()})
            errors.append(line.strip())

    return TypeScriptAnalysisResult(
        tool="tsc",
        success=len(errors) == 0,
        issues=issues,
        errors=errors,
        execution_time_seconds=execution_time
    )
```

**Пример tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,

    // Strict checks
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

### Snyk Integration (Security для TypeScript)

```python
async def run_snyk(
    project_path: str,
    config: TypeScriptAnalysisConfig
) -> TypeScriptAnalysisResult:
    """Запуск Snyk security scan."""

    cmd = [
        "npx", "snyk", "test",
        "--json",
        f"--severity-threshold={config.snyk_severity_threshold}"
    ]

    start = time.time()
    result = subprocess.run(
        cmd,
        cwd=project_path,
        capture_output=True,
        text=True
    )
    execution_time = time.time() - start

    # Парсинг JSON
    try:
        data = json.loads(result.stdout)
        vulnerabilities = data.get("vulnerabilities", [])
    except json.JSONDecodeError:
        vulnerabilities = []

    # Группировка по severity
    errors = [
        v for v in vulnerabilities
        if v["severity"] in ["high", "critical"]
    ]

    return TypeScriptAnalysisResult(
        tool="snyk",
        success=len(errors) == 0,
        issues=vulnerabilities,
        errors=[
            f"{v['packageName']}@{v['version']} - {v['title']} (Severity: {v['severity']})"
            for v in errors
        ],
        execution_time_seconds=execution_time
    )
```

---

## Unified Analysis Runner

### Запуск всех инструментов

```python
from typing import List, Dict

class ProjectAnalysisResult(BaseModel):
    """Агрегированный результат всех static analysis инструментов."""

    python_results: List[PythonAnalysisResult] = Field(default_factory=list)
    typescript_results: List[TypeScriptAnalysisResult] = Field(default_factory=list)

    total_issues: int = 0
    total_errors: int = 0
    total_warnings: int = 0

    overall_success: bool = True
    execution_time_seconds: float = 0.0

async def run_full_static_analysis(
    project_path: str,
    python_config: PythonAnalysisConfig,
    typescript_config: TypeScriptAnalysisConfig
) -> ProjectAnalysisResult:
    """Запуск полного static analysis проекта."""

    import asyncio

    result = ProjectAnalysisResult()
    start = time.time()

    # 1. Найти все Python файлы
    python_files = list(Path(project_path).rglob("*.py"))
    python_files = [str(f) for f in python_files if "venv" not in str(f)]

    # 2. Найти все TypeScript файлы
    ts_files = list(Path(project_path).rglob("*.ts"))
    ts_files = [str(f) for f in ts_files if "node_modules" not in str(f)]

    # 3. Запуск Python инструментов параллельно
    if python_files:
        python_tasks = []

        if python_config.pylint_enabled:
            python_tasks.append(run_pylint(python_files, python_config))

        if python_config.flake8_enabled:
            python_tasks.append(run_flake8(python_files, python_config))

        if python_config.mypy_enabled:
            python_tasks.append(run_mypy(python_files, python_config))

        if python_config.bandit_enabled:
            python_tasks.append(run_bandit(python_files, python_config))

        result.python_results = await asyncio.gather(*python_tasks)

    # 4. Запуск TypeScript инструментов параллельно
    if ts_files:
        ts_tasks = []

        if typescript_config.eslint_enabled:
            ts_tasks.append(run_eslint(ts_files, typescript_config))

        if typescript_config.tsc_enabled:
            ts_tasks.append(run_tsc(project_path, typescript_config))

        if typescript_config.snyk_enabled:
            ts_tasks.append(run_snyk(project_path, typescript_config))

        result.typescript_results = await asyncio.gather(*ts_tasks)

    # 5. Агрегация результатов
    all_results = result.python_results + result.typescript_results

    result.total_errors = sum(len(r.errors) for r in all_results)
    result.total_warnings = sum(len(r.warnings) for r in all_results)
    result.total_issues = sum(len(r.issues) for r in all_results)

    result.overall_success = all(r.success for r in all_results)
    result.execution_time_seconds = time.time() - start

    return result


# Использование
async def main():
    python_config = PythonAnalysisConfig(
        pylint_min_score=8.0,
        flake8_max_line_length=100,
        mypy_strict=True,
        bandit_severity_level="medium"
    )

    typescript_config = TypeScriptAnalysisConfig(
        eslint_enabled=True,
        tsc_strict=True,
        snyk_severity_threshold="high"
    )

    result = await run_full_static_analysis(
        project_path=".",
        python_config=python_config,
        typescript_config=typescript_config
    )

    # Отчет
    print(f"Overall Success: {result.overall_success}")
    print(f"Total Issues: {result.total_issues}")
    print(f"Errors: {result.total_errors}")
    print(f"Warnings: {result.total_warnings}")
    print(f"Execution Time: {result.execution_time_seconds:.2f}s")

    # Детали по инструментам
    for tool_result in result.python_results + result.typescript_results:
        print(f"\n{tool_result.tool}:")
        print(f"  Success: {tool_result.success}")
        print(f"  Issues: {len(tool_result.issues)}")

        if tool_result.errors:
            print(f"  Errors:")
            for error in tool_result.errors[:5]:  # Первые 5
                print(f"    - {error}")
```

---

**Навигация:**
- [← Предыдущий модуль: AI-Powered Code Review](03_ai_powered_code_review.md)
- [↑ Назад к Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)
- [→ Следующий модуль: CI/CD & Technical Debt](05_ci_cd_technical_debt.md)
