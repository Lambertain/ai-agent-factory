# Module 03: AI-Powered Code Review

**Назад к:** [Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)

---

## AI Code Review с Claude Sonnet 4

### System Prompt для code review

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
```

---

## Интеграция с Pydantic AI

### AICodeReviewer агент

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import List, Literal

class CodeReviewComment(BaseModel):
    """Комментарий code review."""

    file_path: str = Field(description="Путь к файлу")
    line_number: int = Field(description="Номер строки")

    severity: Literal["blocker", "critical", "major", "minor", "info"] = Field(
        description="Уровень серьезности"
    )
    category: Literal[
        "code_quality", "security", "performance", "testing", "architecture"
    ] = Field(description="Категория проблемы")

    issue: str = Field(description="Описание проблемы")
    suggestion: str = Field(description="Предложение по исправлению")
    example_code: str | None = Field(default=None, description="Пример исправленного кода")

class CodeReviewResult(BaseModel):
    """Результат code review."""

    comments: List[CodeReviewComment] = Field(default_factory=list)
    overall_assessment: str = Field(description="Общая оценка")
    approval_status: Literal["approved", "needs_changes", "rejected"] = Field(
        description="Статус approve/reject"
    )
    estimated_fix_time_hours: float = Field(
        description="Оценка времени на исправление всех проблем"
    )

# Создание AI Code Reviewer
code_reviewer = Agent(
    model='anthropic:claude-sonnet-4-20250514',
    result_type=CodeReviewResult,
    system_prompt=CODE_REVIEW_SYSTEM_PROMPT
)

@code_reviewer.tool
async def analyze_file_complexity(ctx: RunContext, file_path: str) -> Dict:
    """Получить метрики сложности файла."""
    # Интеграция с radon или другими инструментами
    return {
        "cyclomatic_complexity": 8.5,
        "cognitive_complexity": 12,
        "lines_of_code": 250
    }

@code_reviewer.tool
async def search_similar_code(ctx: RunContext, code_snippet: str) -> List[str]:
    """Найти похожий код (для обнаружения дубликатов)."""
    # Интеграция с vector search
    return ["path/to/similar1.py", "path/to/similar2.py"]

@code_reviewer.tool
async def check_security_patterns(ctx: RunContext, code: str) -> List[Dict]:
    """Проверить security patterns."""
    # Интеграция с bandit/semgrep
    return [
        {"type": "hardcoded_password", "line": 42, "severity": "high"}
    ]
```

---

## Использование AI Code Reviewer

### Для Pull Request

```python
async def review_pull_request(pr_number: int, repo_path: str) -> CodeReviewResult:
    """Провести AI review pull request."""

    # 1. Получить diff из PR
    diff = await get_pr_diff(pr_number, repo_path)

    # 2. Извлечь измененные файлы
    changed_files = parse_diff_files(diff)

    # 3. Для каждого файла собрать контекст
    review_context = []
    for file in changed_files:
        file_content = await read_file(file.path)

        review_context.append({
            "file_path": file.path,
            "changes": file.diff,
            "full_content": file_content,
            "language": detect_language(file.path)
        })

    # 4. Сформировать prompt
    review_prompt = f"""
Проведи code review для Pull Request #{pr_number}.

Измененные файлы:
{format_changed_files(changed_files)}

Для каждого файла проанализируй:
1. Качество кода
2. Security issues
3. Performance implications
4. Testing coverage
5. Architectural concerns

Provide specific, actionable feedback.
"""

    # 5. Запустить AI review
    result = await code_reviewer.run(review_prompt)

    return result.data


# Использование
async def main():
    review = await review_pull_request(pr_number=123, repo_path=".")

    # Вывод комментариев
    for comment in review.comments:
        print(f"\n[{comment.severity.upper()}] {comment.file_path}:{comment.line_number}")
        print(f"Category: {comment.category}")
        print(f"Issue: {comment.issue}")
        print(f"Suggestion: {comment.suggestion}")

        if comment.example_code:
            print(f"Example:\n{comment.example_code}")

    # Общий вердикт
    print(f"\nOverall: {review.overall_assessment}")
    print(f"Status: {review.approval_status}")
    print(f"Estimated fix time: {review.estimated_fix_time_hours} hours")
```

---

### Для отдельного файла

```python
async def review_file(file_path: str) -> CodeReviewResult:
    """Провести review одного файла."""

    # Читаем файл
    with open(file_path, 'r') as f:
        code = f.read()

    # Prompt для single file review
    prompt = f"""
Проведи детальный code review файла: {file_path}

Код:
```
{code}
```

Проанализируй:
1. Code quality and readability
2. Potential bugs
3. Security vulnerabilities
4. Performance issues
5. Testing needs
6. Architectural patterns

Provide line-specific feedback with concrete suggestions.
"""

    result = await code_reviewer.run(prompt)
    return result.data


# Использование
review = await review_file("src/api/users.py")

# Фильтрация critical issues
critical = [c for c in review.comments if c.severity in ["blocker", "critical"]]
if critical:
    print(f"Found {len(critical)} critical issues that must be fixed!")
```

---

## Advanced Code Review Patterns

### Pattern 1: Контекстный review с историей

```python
async def contextual_code_review(
    file_path: str,
    include_history: bool = True,
    include_tests: bool = True
) -> CodeReviewResult:
    """Code review с дополнительным контекстом."""

    # Основной код
    with open(file_path, 'r') as f:
        current_code = f.read()

    # Контекст
    context_parts = [f"Current code:\n```\n{current_code}\n```"]

    # Git история
    if include_history:
        history = await get_file_git_history(file_path, limit=5)
        context_parts.append(f"\nRecent changes:\n{history}")

    # Связанные тесты
    if include_tests:
        test_file = find_test_file(file_path)
        if test_file:
            with open(test_file, 'r') as f:
                test_code = f.read()
            context_parts.append(f"\nTest file:\n```\n{test_code}\n```")

    # Зависимости
    dependencies = analyze_imports(current_code)
    context_parts.append(f"\nDependencies: {', '.join(dependencies)}")

    # AI review с полным контекстом
    prompt = "\n\n".join(context_parts)
    prompt += "\n\nProvide comprehensive code review considering all context."

    result = await code_reviewer.run(prompt)
    return result.data
```

---

### Pattern 2: Incremental review (только diff)

```python
async def incremental_code_review(
    file_path: str,
    old_version: str,
    new_version: str
) -> CodeReviewResult:
    """Review только изменений между версиями."""

    import difflib

    # Генерация unified diff
    old_lines = old_version.splitlines(keepends=True)
    new_lines = new_version.splitlines(keepends=True)

    diff = ''.join(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"{file_path} (before)",
        tofile=f"{file_path} (after)"
    ))

    prompt = f"""
Review only the changes in this diff:

{diff}

Focus on:
1. Do the changes introduce bugs?
2. Are there security implications?
3. Do the changes follow best practices?
4. Are tests needed for these changes?

Provide feedback only for the changed lines.
"""

    result = await code_reviewer.run(prompt)
    return result.data
```

---

### Pattern 3: Review с автоматическими fixes

```python
from typing import Tuple

async def review_with_autofix(file_path: str) -> Tuple[CodeReviewResult, str]:
    """Review с предложенными автофиксами."""

    with open(file_path, 'r') as f:
        original_code = f.read()

    prompt = f"""
Review this code and provide:
1. List of all issues found
2. For each fixable issue, provide the EXACT fixed code

Code:
```python
{original_code}
```

For formatting, style, and simple issues - provide complete fixed version.
For complex issues - provide detailed explanation.
"""

    result = await code_reviewer.run(prompt)

    # Извлечение fixed code из комментариев
    fixed_code = original_code
    for comment in result.data.comments:
        if comment.example_code and comment.severity in ["minor", "info"]:
            # Применить автофикс
            fixed_code = apply_fix(fixed_code, comment)

    return result.data, fixed_code


def apply_fix(code: str, comment: CodeReviewComment) -> str:
    """Применить fix к коду."""
    lines = code.splitlines()

    if comment.example_code:
        # Замена строки на fixed version
        lines[comment.line_number - 1] = comment.example_code

    return '\n'.join(lines)
```

---

## Best Practices для AI Code Review

### 1. Используй structured output (Pydantic models)

**Плохо:**
```python
# Free-form text output
result = await agent.run("Review this code")
# Получаем неструктурированный текст
```

**Хорошо:**
```python
# Structured output с Pydantic
code_reviewer = Agent(
    model='anthropic:claude-sonnet-4-20250514',
    result_type=CodeReviewResult  # ← Pydantic model
)
result = await code_reviewer.run("Review this code")
# Получаем структурированный CodeReviewResult
```

---

### 2. Предоставляй достаточный контекст

**Плохо:**
```python
# Только код без контекста
prompt = f"Review: {code}"
```

**Хорошо:**
```python
# Код + контекст + цели
prompt = f"""
File: {file_path}
Language: {language}
Purpose: {module_purpose}

Code:
{code}

Related files: {related_files}
Dependencies: {dependencies}

Review for: production readiness, security, performance.
"""
```

---

### 3. Фильтруй и приоритизируй комментарии

```python
def prioritize_comments(comments: List[CodeReviewComment]) -> Dict[str, List]:
    """Группировка комментариев по приоритету."""

    return {
        "must_fix": [
            c for c in comments
            if c.severity in ["blocker", "critical"]
        ],
        "should_fix": [
            c for c in comments
            if c.severity == "major"
        ],
        "nice_to_have": [
            c for c in comments
            if c.severity in ["minor", "info"]
        ]
    }

# Использование
prioritized = prioritize_comments(review.comments)

# Сначала показываем must_fix
for comment in prioritized["must_fix"]:
    print(f"🚨 MUST FIX: {comment.issue}")
```

---

### 4. Интеграция с CI/CD

```python
async def ci_code_review_gate(pr_number: int) -> bool:
    """CI gate на основе AI review."""

    review = await review_pull_request(pr_number)

    # Блокируем merge если есть blocker/critical issues
    blockers = [
        c for c in review.comments
        if c.severity in ["blocker", "critical"]
    ]

    if blockers:
        # Оставить комментарии в PR
        await post_review_comments(pr_number, blockers)

        # Блокировать merge
        return False

    # Warnings для major issues
    major_issues = [c for c in review.comments if c.severity == "major"]
    if major_issues:
        await post_review_comments(pr_number, major_issues)
        # Не блокируем, но предупреждаем

    return True
```

---

### 5. Continuous Learning

```python
class ReviewFeedback(BaseModel):
    """Feedback на AI review."""

    comment_id: str
    was_helpful: bool
    actual_issue: bool
    feedback_text: str

async def collect_review_feedback(
    review_id: str,
    feedback: ReviewFeedback
):
    """Сбор обратной связи для улучшения AI review."""

    # Сохранение в базу
    await db.save_feedback(review_id, feedback)

    # Если много false positives для определенной категории
    false_positives = await db.get_false_positives_count(
        category=feedback.category
    )

    if false_positives > 10:
        # Обновить prompt для этой категории
        await update_review_prompt(category=feedback.category)
```

---

**Навигация:**
- [← Предыдущий модуль: Metrics & Quality Models](02_metrics_quality_models.md)
- [↑ Назад к Quality Guardian Knowledge Base](../archon_quality_guardian_knowledge.md)
- [→ Следующий модуль: Static Analysis Integration](04_static_analysis_integration.md)
