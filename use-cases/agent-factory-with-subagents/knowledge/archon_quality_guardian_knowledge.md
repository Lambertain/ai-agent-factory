# Archon Quality Guardian Knowledge Base

## Системный промпт для Archon Quality Guardian

```
Ты главный страж качества команды Archon - специалист по обеспечению высочайших стандартов качества кода, тестирования и production-ready решений. Твоя миссия - гарантировать безупречность каждого продукта.

**Твоя экспертиза:**
- Comprehensive testing strategies (Unit, Integration, E2E, Performance)
- Code review и static analysis
- Quality assurance процессы и метрики
- Test automation и CI/CD integration
- Performance testing и optimization
- Security testing и vulnerability assessment
- Documentation quality и completeness

**Ключевые области качества:**

1. **Testing Excellence:**
   - Pytest, Jest, Playwright для автоматизации
   - Test-driven development (TDD) practices
   - Behavior-driven development (BDD)
   - Property-based testing и fuzzing

2. **Code Quality Assurance:**
   - Static analysis (mypy, ESLint, SonarQube)
   - Code coverage analysis
   - Code complexity metrics
   - Architectural compliance checking

3. **Performance & Reliability:**
   - Load testing с k6, Artillery, JMeter
   - Memory profiling и leak detection
   - Chaos engineering principles
   - SLA/SLO monitoring

4. **Security Quality:**
   - SAST/DAST security scanning
   - Dependency vulnerability scanning
   - Penetration testing coordination
   - Secure code review practices

**Подход к работе:**
1. Quality-first mindset - качество закладывается с начала
2. Автоматизация всех повторяющихся проверок
3. Измеримые метрики качества (95%+ coverage, 0 critical issues)
4. Непрерывное улучшение процессов
5. Обучение команды best practices
```

## Testing Strategies & Frameworks

### Comprehensive Testing Pyramid
```python
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic_ai.models.test import TestModel
from pydantic_ai import Agent, RunContext
import hypothesis
from hypothesis import strategies as st
import time

class TestingFramework:
    """Комплексный фреймворк для тестирования."""

    # Unit Tests (Base of pyramid - 70%)
    class UnitTests:
        """Unit тесты для отдельных компонентов."""

        @pytest.fixture
        def mock_dependencies(self):
            """Мокание зависимостей для изоляции."""
            return {
                'database': AsyncMock(),
                'cache': AsyncMock(),
                'external_api': AsyncMock(),
                'logger': MagicMock()
            }

        @pytest.mark.asyncio
        async def test_agent_tool_functionality(self, mock_dependencies):
            """Тест функциональности инструмента агента."""
            from your_app.tools import search_knowledge

            # Arrange
            mock_context = MagicMock()
            mock_context.deps = mock_dependencies['database']
            mock_dependencies['database'].search.return_value = [
                {"content": "test result", "score": 0.95}
            ]

            # Act
            result = await search_knowledge(mock_context, "test query")

            # Assert
            assert "test result" in result
            mock_dependencies['database'].search.assert_called_once_with("test query")

        @hypothesis.given(st.text(min_size=1, max_size=100))
        def test_input_validation_property_based(self, input_text):
            """Property-based тестирование валидации входных данных."""
            from your_app.validation import validate_input

            # Property: валидация должна либо пройти, либо выбросить исключение
            try:
                result = validate_input(input_text)
                assert isinstance(result, str)
                assert len(result) > 0
            except ValueError as e:
                assert str(e)  # Ошибка должна иметь описание

    # Integration Tests (Middle of pyramid - 20%)
    class IntegrationTests:
        """Интеграционные тесты для взаимодействия компонентов."""

        @pytest.mark.integration
        @pytest.mark.asyncio
        async def test_agent_with_real_database(self, test_database):
            """Тест агента с реальной базой данных."""
            from your_app.agent import create_agent
            from your_app.dependencies import AgentDependencies

            # Используем тестовую базу данных
            deps = AgentDependencies(database_url=test_database.url)
            await deps.initialize()

            try:
                agent = create_agent(deps)
                result = await agent.run("Find information about testing", deps=deps)

                assert result.data is not None
                assert isinstance(result.data, str)
                assert len(result.data) > 0

            finally:
                await deps.cleanup()

        @pytest.mark.integration
        async def test_external_api_integration(self):
            """Тест интеграции с внешними API."""
            import aiohttp

            async with aiohttp.ClientSession() as session:
                # Тест с реальным API endpoint
                response = await session.get("https://api.external-service.com/health")
                assert response.status == 200

                data = await response.json()
                assert "status" in data
                assert data["status"] == "healthy"

    # E2E Tests (Top of pyramid - 10%)
    class EndToEndTests:
        """End-to-end тесты полных пользовательских сценариев."""

        @pytest.mark.e2e
        @pytest.mark.asyncio
        async def test_complete_user_workflow(self, test_client):
            """Тест полного пользовательского workflow."""
            # 1. Пользователь отправляет запрос
            response = await test_client.post("/api/agent/query", json={
                "query": "Analyze the latest market trends",
                "user_id": "test_user_123"
            })

            assert response.status_code == 200
            data = response.json()

            # 2. Проверяем структуру ответа
            assert "response" in data
            assert "metadata" in data
            assert data["metadata"]["status"] == "success"

            # 3. Проверяем сохранение в истории
            history_response = await test_client.get(
                "/api/user/test_user_123/history"
            )
            assert history_response.status_code == 200
            history = history_response.json()
            assert len(history["queries"]) > 0

        @pytest.mark.e2e
        async def test_error_handling_workflow(self, test_client):
            """Тест обработки ошибок в полном workflow."""
            # Отправляем некорректный запрос
            response = await test_client.post("/api/agent/query", json={
                "query": "",  # Пустой запрос
                "user_id": "test_user_123"
            })

            assert response.status_code == 400
            data = response.json()
            assert "error" in data
            assert "validation" in data["error"]["type"]
```

### Performance Testing Framework
```python
import asyncio
import time
import psutil
import os
from typing import List, Dict, Any
import pytest
from concurrent.futures import ThreadPoolExecutor

class PerformanceTestSuite:
    """Комплексное тестирование производительности."""

    @pytest.mark.performance
    async def test_response_time_sla(self, test_agent):
        """Тест соответствия SLA по времени ответа."""
        agent, deps = test_agent

        response_times = []

        # Выполняем 100 запросов
        for i in range(100):
            start_time = time.time()
            await agent.run(f"Test query {i}", deps=deps)
            end_time = time.time()

            response_times.append(end_time - start_time)

        # Анализ результатов
        avg_response_time = sum(response_times) / len(response_times)
        p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]
        p99_response_time = sorted(response_times)[int(0.99 * len(response_times))]

        # SLA требования
        assert avg_response_time < 1.0, f"Average response time {avg_response_time:.2f}s exceeds 1s SLA"
        assert p95_response_time < 2.0, f"95th percentile {p95_response_time:.2f}s exceeds 2s SLA"
        assert p99_response_time < 5.0, f"99th percentile {p99_response_time:.2f}s exceeds 5s SLA"

    @pytest.mark.performance
    async def test_concurrent_load_handling(self, test_agent):
        """Тест обработки конкурентной нагрузки."""
        agent, deps = test_agent

        async def single_request(request_id: int):
            """Одиночный запрос с уникальным ID."""
            return await agent.run(f"Concurrent request {request_id}", deps=deps)

        # Тест с различными уровнями конкурентности
        concurrency_levels = [10, 50, 100, 200]

        for concurrency in concurrency_levels:
            start_time = time.time()

            # Создаем конкурентные задачи
            tasks = [single_request(i) for i in range(concurrency)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = time.time()
            total_time = end_time - start_time

            # Анализ результатов
            successful_requests = sum(1 for r in results if not isinstance(r, Exception))
            error_rate = (concurrency - successful_requests) / concurrency * 100
            throughput = successful_requests / total_time

            print(f"Concurrency: {concurrency}, Success Rate: {successful_requests}/{concurrency}, "
                  f"Error Rate: {error_rate:.1f}%, Throughput: {throughput:.1f} req/s")

            # Проверки качества
            assert error_rate < 5.0, f"Error rate {error_rate:.1f}% too high for concurrency {concurrency}"
            assert throughput > concurrency * 0.5, f"Throughput {throughput:.1f} too low for concurrency {concurrency}"

    @pytest.mark.performance
    async def test_memory_usage_stability(self, test_agent):
        """Тест стабильности использования памяти."""
        agent, deps = test_agent

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        memory_measurements = [initial_memory]

        # Выполняем 1000 запросов с измерением памяти
        for i in range(1000):
            await agent.run(f"Memory test query {i}", deps=deps)

            if i % 100 == 0:  # Измеряем каждые 100 запросов
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_measurements.append(current_memory)

        # Анализ утечек памяти
        memory_growth = memory_measurements[-1] - memory_measurements[0]
        max_memory = max(memory_measurements)

        print(f"Memory usage: Initial: {initial_memory:.1f}MB, "
              f"Final: {memory_measurements[-1]:.1f}MB, "
              f"Growth: {memory_growth:.1f}MB, Max: {max_memory:.1f}MB")

        # Проверки
        assert memory_growth < 100, f"Memory growth {memory_growth:.1f}MB indicates memory leak"
        assert max_memory < initial_memory + 200, f"Peak memory usage {max_memory:.1f}MB too high"

    @pytest.mark.performance
    async def test_database_query_performance(self, test_database):
        """Тест производительности запросов к базе данных."""
        from your_app.database import DatabaseService

        db_service = DatabaseService(test_database.url)
        await db_service.initialize()

        try:
            # Тест простых запросов
            start_time = time.time()
            for i in range(100):
                await db_service.get_user_by_id(f"user_{i}")
            simple_query_time = (time.time() - start_time) / 100

            # Тест сложных запросов
            start_time = time.time()
            for i in range(10):
                await db_service.get_user_analytics(f"user_{i}")
            complex_query_time = (time.time() - start_time) / 10

            print(f"DB Performance: Simple queries: {simple_query_time*1000:.1f}ms, "
                  f"Complex queries: {complex_query_time*1000:.1f}ms")

            # SLA проверки
            assert simple_query_time < 0.01, f"Simple query time {simple_query_time*1000:.1f}ms exceeds 10ms SLA"
            assert complex_query_time < 0.1, f"Complex query time {complex_query_time*1000:.1f}ms exceeds 100ms SLA"

        finally:
            await db_service.cleanup()
```

## Code Quality Analysis

### Static Analysis & Code Metrics
```python
import ast
import subprocess
import json
from typing import Dict, List, Any
from pathlib import Path

class CodeQualityAnalyzer:
    """Анализатор качества кода."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def run_mypy_analysis(self) -> Dict[str, Any]:
        """Запуск mypy для проверки типов."""
        result = subprocess.run([
            "mypy", "--json-report", "/tmp/mypy-report",
            str(self.project_path)
        ], capture_output=True, text=True)

        # Анализ результатов
        error_count = result.stdout.count('"severity": "error"')
        warning_count = result.stdout.count('"severity": "warning"')

        return {
            "tool": "mypy",
            "errors": error_count,
            "warnings": warning_count,
            "status": "passed" if error_count == 0 else "failed",
            "details": result.stdout
        }

    def run_pylint_analysis(self) -> Dict[str, Any]:
        """Запуск pylint для анализа качества кода."""
        result = subprocess.run([
            "pylint", "--output-format=json",
            str(self.project_path)
        ], capture_output=True, text=True)

        try:
            pylint_data = json.loads(result.stdout)

            # Группировка по типам сообщений
            messages_by_type = {}
            for message in pylint_data:
                msg_type = message.get("type", "unknown")
                if msg_type not in messages_by_type:
                    messages_by_type[msg_type] = 0
                messages_by_type[msg_type] += 1

            return {
                "tool": "pylint",
                "messages": messages_by_type,
                "total_issues": len(pylint_data),
                "status": "passed" if len(pylint_data) == 0 else "review_needed",
                "details": pylint_data[:10]  # Первые 10 для примера
            }
        except json.JSONDecodeError:
            return {
                "tool": "pylint",
                "status": "error",
                "error": "Could not parse pylint output"
            }

    def analyze_code_complexity(self) -> Dict[str, Any]:
        """Анализ сложности кода."""
        complexity_data = []

        for py_file in self.project_path.rglob("*.py"):
            if "test_" in py_file.name or py_file.name.startswith("test_"):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                file_complexity = self._calculate_cyclomatic_complexity(tree)
                complexity_data.append({
                    "file": str(py_file.relative_to(self.project_path)),
                    "complexity": file_complexity
                })
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")

        # Статистика сложности
        complexities = [item["complexity"] for item in complexity_data]
        avg_complexity = sum(complexities) / len(complexities) if complexities else 0
        max_complexity = max(complexities) if complexities else 0

        return {
            "tool": "complexity_analyzer",
            "average_complexity": avg_complexity,
            "max_complexity": max_complexity,
            "files_analyzed": len(complexity_data),
            "high_complexity_files": [
                item for item in complexity_data if item["complexity"] > 10
            ],
            "status": "passed" if max_complexity <= 15 else "review_needed"
        }

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Вычисление цикломатической сложности."""
        complexity = 1  # Базовая сложность

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1

        return complexity

    def run_security_scan(self) -> Dict[str, Any]:
        """Запуск сканирования безопасности с bandit."""
        result = subprocess.run([
            "bandit", "-r", str(self.project_path),
            "-f", "json", "-o", "/tmp/bandit-report.json"
        ], capture_output=True, text=True)

        try:
            with open("/tmp/bandit-report.json", 'r') as f:
                bandit_data = json.load(f)

            # Группировка по уровням серьезности
            severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
            for result in bandit_data.get("results", []):
                severity = result.get("issue_severity", "UNKNOWN")
                if severity in severity_counts:
                    severity_counts[severity] += 1

            return {
                "tool": "bandit",
                "severity_counts": severity_counts,
                "total_issues": len(bandit_data.get("results", [])),
                "critical_issues": severity_counts["HIGH"],
                "status": "passed" if severity_counts["HIGH"] == 0 else "failed"
            }
        except Exception as e:
            return {
                "tool": "bandit",
                "status": "error",
                "error": str(e)
            }

    def analyze_test_coverage(self) -> Dict[str, Any]:
        """Анализ покрытия тестами."""
        # Запуск pytest с coverage
        result = subprocess.run([
            "pytest", "--cov=.", "--cov-report=json:/tmp/coverage.json",
            str(self.project_path / "tests")
        ], capture_output=True, text=True)

        try:
            with open("/tmp/coverage.json", 'r') as f:
                coverage_data = json.load(f)

            total_coverage = coverage_data["totals"]["percent_covered"]

            # Файлы с низким покрытием
            low_coverage_files = []
            for filename, file_data in coverage_data["files"].items():
                if file_data["summary"]["percent_covered"] < 80:
                    low_coverage_files.append({
                        "file": filename,
                        "coverage": file_data["summary"]["percent_covered"]
                    })

            return {
                "tool": "coverage",
                "total_coverage": total_coverage,
                "line_coverage": coverage_data["totals"]["percent_covered_display"],
                "low_coverage_files": low_coverage_files,
                "status": "passed" if total_coverage >= 80 else "review_needed"
            }
        except Exception as e:
            return {
                "tool": "coverage",
                "status": "error",
                "error": str(e)
            }

    def generate_quality_report(self) -> Dict[str, Any]:
        """Генерация комплексного отчета о качестве."""
        return {
            "timestamp": time.time(),
            "project_path": str(self.project_path),
            "analyses": {
                "type_checking": self.run_mypy_analysis(),
                "code_quality": self.run_pylint_analysis(),
                "complexity": self.analyze_code_complexity(),
                "security": self.run_security_scan(),
                "test_coverage": self.analyze_test_coverage()
            }
        }
```

### Automated Code Review
```python
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path

class AutomatedCodeReviewer:
    """Автоматизированный код ревьюер."""

    def __init__(self):
        self.review_rules = {
            "naming_conventions": self._check_naming_conventions,
            "function_length": self._check_function_length,
            "import_organization": self._check_import_organization,
            "documentation": self._check_documentation,
            "error_handling": self._check_error_handling,
            "performance_patterns": self._check_performance_patterns
        }

    def review_file(self, file_path: Path) -> Dict[str, Any]:
        """Ревью одного файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []
        suggestions = []

        for rule_name, rule_func in self.review_rules.items():
            rule_issues, rule_suggestions = rule_func(content, file_path)
            issues.extend(rule_issues)
            suggestions.extend(rule_suggestions)

        return {
            "file": str(file_path),
            "issues": issues,
            "suggestions": suggestions,
            "score": self._calculate_file_score(issues)
        }

    def _check_naming_conventions(self, content: str, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Проверка соглашений именования."""
        issues = []
        suggestions = []

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Проверка классов (должны быть в PascalCase)
            class_match = re.search(r'class\s+([a-z_][a-zA-Z0-9_]*)', line)
            if class_match:
                class_name = class_match.group(1)
                if not class_name[0].isupper():
                    issues.append({
                        "type": "naming_convention",
                        "severity": "medium",
                        "line": i,
                        "message": f"Class '{class_name}' should be in PascalCase",
                        "suggestion": f"Rename to '{self._to_pascal_case(class_name)}'"
                    })

            # Проверка функций (должны быть в snake_case)
            func_match = re.search(r'def\s+([A-Z][a-zA-Z0-9_]*)', line)
            if func_match:
                func_name = func_match.group(1)
                issues.append({
                    "type": "naming_convention",
                    "severity": "medium",
                    "line": i,
                    "message": f"Function '{func_name}' should be in snake_case",
                    "suggestion": f"Rename to '{self._to_snake_case(func_name)}'"
                })

        return issues, suggestions

    def _check_function_length(self, content: str, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Проверка длины функций."""
        issues = []
        suggestions = []

        lines = content.split('\n')
        in_function = False
        function_start = 0
        function_name = ""

        for i, line in enumerate(lines, 1):
            if re.match(r'\s*def\s+', line):
                in_function = True
                function_start = i
                function_name = re.search(r'def\s+(\w+)', line).group(1)
            elif in_function and not line.startswith(' ') and not line.startswith('\t') and line.strip():
                # Конец функции
                function_length = i - function_start
                if function_length > 50:
                    issues.append({
                        "type": "function_length",
                        "severity": "high" if function_length > 100 else "medium",
                        "line": function_start,
                        "message": f"Function '{function_name}' is too long ({function_length} lines)",
                        "suggestion": "Consider breaking this function into smaller functions"
                    })
                in_function = False

        return issues, suggestions

    def _check_documentation(self, content: str, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Проверка документации."""
        issues = []
        suggestions = []

        # Проверка docstrings для функций
        function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        functions = re.finditer(function_pattern, content)

        for func_match in functions:
            func_name = func_match.group(1)
            func_start = func_match.start()

            # Поиск docstring после функции
            remaining_content = content[func_match.end():]
            docstring_match = re.search(r'^\s*""".*?"""', remaining_content, re.DOTALL | re.MULTILINE)

            if not docstring_match and not func_name.startswith('_'):
                line_num = content[:func_start].count('\n') + 1
                issues.append({
                    "type": "documentation",
                    "severity": "medium",
                    "line": line_num,
                    "message": f"Public function '{func_name}' lacks docstring",
                    "suggestion": "Add a descriptive docstring explaining the function's purpose"
                })

        return issues, suggestions

    def _check_error_handling(self, content: str, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Проверка обработки ошибок."""
        issues = []
        suggestions = []

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Bare except clauses
            if re.search(r'except\s*:', line):
                issues.append({
                    "type": "error_handling",
                    "severity": "high",
                    "line": i,
                    "message": "Bare 'except:' clause catches all exceptions",
                    "suggestion": "Specify the exception type or use 'except Exception:'"
                })

            # Exception без логирования
            if 'except' in line and 'pass' in lines[i] if i < len(lines) else False:
                issues.append({
                    "type": "error_handling",
                    "severity": "medium",
                    "line": i,
                    "message": "Exception silently ignored",
                    "suggestion": "Add logging or proper error handling"
                })

        return issues, suggestions

    def _calculate_file_score(self, issues: List[Dict]) -> float:
        """Вычисление оценки файла."""
        score = 100.0

        for issue in issues:
            if issue["severity"] == "high":
                score -= 10
            elif issue["severity"] == "medium":
                score -= 5
            elif issue["severity"] == "low":
                score -= 2

        return max(0.0, score)

    def _to_pascal_case(self, snake_str: str) -> str:
        """Конвертация в PascalCase."""
        return ''.join(word.capitalize() for word in snake_str.split('_'))

    def _to_snake_case(self, pascal_str: str) -> str:
        """Конвертация в snake_case."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str).lower()
```

## Quality Metrics & Monitoring

### Comprehensive Quality Dashboard
```python
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd

class QualityMetricsCollector:
    """Сборщик метрик качества."""

    def __init__(self, db_path: str = "quality_metrics.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация базы данных метрик."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                project_name TEXT,
                metric_type TEXT,
                metric_name TEXT,
                metric_value REAL,
                metadata TEXT
            )
        """)

        conn.commit()
        conn.close()

    def record_metric(self, project: str, metric_type: str, name: str, value: float, metadata: Dict = None):
        """Запись метрики качества."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO quality_metrics (project_name, metric_type, metric_name, metric_value, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (project, metric_type, name, value, json.dumps(metadata or {})))

        conn.commit()
        conn.close()

    def collect_test_metrics(self, test_results: Dict) -> None:
        """Сбор метрик тестирования."""
        project = test_results.get("project", "unknown")

        # Основные метрики
        self.record_metric(project, "testing", "total_tests", test_results.get("total", 0))
        self.record_metric(project, "testing", "passed_tests", test_results.get("passed", 0))
        self.record_metric(project, "testing", "failed_tests", test_results.get("failed", 0))
        self.record_metric(project, "testing", "test_coverage", test_results.get("coverage", 0))

        # Производительность тестов
        if "duration" in test_results:
            self.record_metric(project, "testing", "test_duration", test_results["duration"])

        # Качество тестов
        pass_rate = (test_results.get("passed", 0) / test_results.get("total", 1)) * 100
        self.record_metric(project, "testing", "pass_rate", pass_rate)

    def collect_code_quality_metrics(self, analysis_results: Dict) -> None:
        """Сбор метрик качества кода."""
        project = analysis_results.get("project", "unknown")

        for analysis_type, results in analysis_results.get("analyses", {}).items():
            if analysis_type == "complexity":
                self.record_metric(project, "code_quality", "avg_complexity",
                                 results.get("average_complexity", 0))
                self.record_metric(project, "code_quality", "max_complexity",
                                 results.get("max_complexity", 0))

            elif analysis_type == "security":
                critical_issues = results.get("critical_issues", 0)
                self.record_metric(project, "security", "critical_issues", critical_issues)

            elif analysis_type == "test_coverage":
                coverage = results.get("total_coverage", 0)
                self.record_metric(project, "coverage", "line_coverage", coverage)

    def generate_quality_report(self, project: str, days: int = 30) -> Dict[str, Any]:
        """Генерация отчета о качестве."""
        conn = sqlite3.connect(self.db_path)

        # Запрос данных за последние N дней
        query = """
            SELECT metric_type, metric_name, metric_value, timestamp
            FROM quality_metrics
            WHERE project_name = ? AND timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        """.format(days)

        df = pd.read_sql_query(query, conn, params=(project,))
        conn.close()

        if df.empty:
            return {"error": "No data found for the specified period"}

        # Группировка по типам метрик
        report = {
            "project": project,
            "period_days": days,
            "generated_at": datetime.now().isoformat(),
            "metrics": {}
        }

        for metric_type in df['metric_type'].unique():
            type_data = df[df['metric_type'] == metric_type]

            metrics_summary = {}
            for metric_name in type_data['metric_name'].unique():
                metric_data = type_data[type_data['metric_name'] == metric_name]

                metrics_summary[metric_name] = {
                    "current_value": metric_data.iloc[0]['metric_value'],
                    "average": metric_data['metric_value'].mean(),
                    "min": metric_data['metric_value'].min(),
                    "max": metric_data['metric_value'].max(),
                    "trend": self._calculate_trend(metric_data['metric_value'].tolist()),
                    "data_points": len(metric_data)
                }

            report["metrics"][metric_type] = metrics_summary

        return report

    def _calculate_trend(self, values: List[float]) -> str:
        """Вычисление тренда метрики."""
        if len(values) < 2:
            return "insufficient_data"

        recent_avg = sum(values[:len(values)//2]) / len(values[:len(values)//2])
        older_avg = sum(values[len(values)//2:]) / len(values[len(values)//2:])

        if recent_avg > older_avg * 1.05:
            return "improving"
        elif recent_avg < older_avg * 0.95:
            return "declining"
        else:
            return "stable"

    def generate_quality_charts(self, project: str, output_dir: str = "quality_charts"):
        """Генерация графиков качества."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        conn = sqlite3.connect(self.db_path)

        # График покрытия тестами
        coverage_query = """
            SELECT DATE(timestamp) as date, metric_value as coverage
            FROM quality_metrics
            WHERE project_name = ? AND metric_name = 'line_coverage'
            ORDER BY timestamp
        """

        coverage_df = pd.read_sql_query(coverage_query, conn, params=(project,))

        if not coverage_df.empty:
            plt.figure(figsize=(12, 6))
            plt.plot(pd.to_datetime(coverage_df['date']), coverage_df['coverage'])
            plt.title(f'Test Coverage Trend - {project}')
            plt.xlabel('Date')
            plt.ylabel('Coverage %')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/coverage_trend.png')
            plt.close()

        # График сложности кода
        complexity_query = """
            SELECT DATE(timestamp) as date, metric_value as complexity
            FROM quality_metrics
            WHERE project_name = ? AND metric_name = 'avg_complexity'
            ORDER BY timestamp
        """

        complexity_df = pd.read_sql_query(complexity_query, conn, params=(project,))

        if not complexity_df.empty:
            plt.figure(figsize=(12, 6))
            plt.plot(pd.to_datetime(complexity_df['date']), complexity_df['complexity'])
            plt.title(f'Code Complexity Trend - {project}')
            plt.xlabel('Date')
            plt.ylabel('Average Complexity')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/complexity_trend.png')
            plt.close()

        conn.close()
```

## Quality Gates & CI/CD Integration

### Quality Gates Configuration
```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality-gate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install poetry
        poetry install

    # Unit Tests
    - name: Run Unit Tests
      run: |
        poetry run pytest tests/unit --cov=. --cov-report=xml

    # Code Quality Checks
    - name: Type Checking (MyPy)
      run: |
        poetry run mypy .

    - name: Code Quality (Pylint)
      run: |
        poetry run pylint src/

    - name: Security Scan (Bandit)
      run: |
        poetry run bandit -r src/

    # Performance Tests
    - name: Performance Tests
      run: |
        poetry run pytest tests/performance -v

    # Quality Gate Evaluation
    - name: Evaluate Quality Gate
      run: |
        poetry run python scripts/quality_gate.py

    # Upload Results
    - name: Upload Coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

    - name: Quality Gate Status
      if: failure()
      run: |
        echo "Quality gate failed! Check the logs above."
        exit 1
```

### Quality Gate Script
```python
#!/usr/bin/env python3
"""
Quality Gate evaluation script.
Checks if all quality metrics meet the required thresholds.
"""

import json
import sys
import subprocess
from typing import Dict, Any, Tuple

class QualityGate:
    """Quality Gate checker."""

    def __init__(self):
        self.thresholds = {
            "test_coverage": 80.0,          # Минимум 80% покрытие
            "test_pass_rate": 100.0,        # 100% прохождение тестов
            "max_complexity": 15,           # Максимальная сложность
            "critical_security": 0,         # 0 критических уязвимостей
            "high_security": 3,             # Максимум 3 высоких уязвимости
            "type_errors": 0,               # 0 ошибок типизации
            "performance_p95": 2000,        # P95 < 2 секунд
        }

    def check_test_coverage(self) -> Tuple[bool, str]:
        """Проверка покрытия тестами."""
        try:
            result = subprocess.run([
                "coverage", "json", "--pretty-print"
            ], capture_output=True, text=True)

            coverage_data = json.loads(result.stdout)
            total_coverage = coverage_data["totals"]["percent_covered"]

            passed = total_coverage >= self.thresholds["test_coverage"]
            message = f"Test coverage: {total_coverage:.1f}% (threshold: {self.thresholds['test_coverage']}%)"

            return passed, message
        except Exception as e:
            return False, f"Failed to check test coverage: {e}"

    def check_type_errors(self) -> Tuple[bool, str]:
        """Проверка ошибок типизации."""
        try:
            result = subprocess.run([
                "mypy", "--json-report", "/tmp/mypy-report", "."
            ], capture_output=True, text=True)

            error_count = result.stdout.count('"severity": "error"')
            passed = error_count <= self.thresholds["type_errors"]
            message = f"Type errors: {error_count} (threshold: {self.thresholds['type_errors']})"

            return passed, message
        except Exception as e:
            return False, f"Failed to check type errors: {e}"

    def check_security_issues(self) -> Tuple[bool, str]:
        """Проверка уязвимостей безопасности."""
        try:
            result = subprocess.run([
                "bandit", "-r", ".", "-f", "json"
            ], capture_output=True, text=True)

            if result.stdout:
                bandit_data = json.loads(result.stdout)
                results = bandit_data.get("results", [])

                critical_count = sum(1 for r in results if r.get("issue_severity") == "HIGH")
                high_count = sum(1 for r in results if r.get("issue_severity") == "MEDIUM")

                critical_passed = critical_count <= self.thresholds["critical_security"]
                high_passed = high_count <= self.thresholds["high_security"]

                passed = critical_passed and high_passed
                message = f"Security issues: {critical_count} critical, {high_count} high"

                return passed, message
            else:
                return True, "No security issues found"
        except Exception as e:
            return False, f"Failed to check security issues: {e}"

    def check_performance(self) -> Tuple[bool, str]:
        """Проверка производительности."""
        try:
            # Запуск performance тестов
            result = subprocess.run([
                "pytest", "tests/performance", "--json-report", "--json-report-file=/tmp/performance.json"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return True, "Performance tests passed"
            else:
                return False, "Performance tests failed"
        except Exception as e:
            return False, f"Failed to check performance: {e}"

    def evaluate(self) -> bool:
        """Оценка всех качественных метрик."""
        checks = [
            ("Test Coverage", self.check_test_coverage),
            ("Type Checking", self.check_type_errors),
            ("Security", self.check_security_issues),
            ("Performance", self.check_performance),
        ]

        all_passed = True
        print("🔍 Quality Gate Evaluation")
        print("=" * 50)

        for check_name, check_func in checks:
            passed, message = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{check_name}: {status} - {message}")

            if not passed:
                all_passed = False

        print("=" * 50)

        if all_passed:
            print("🎉 Quality Gate: PASSED")
            return True
        else:
            print("💥 Quality Gate: FAILED")
            return False

if __name__ == "__main__":
    gate = QualityGate()
    success = gate.evaluate()
    sys.exit(0 if success else 1)
```

## Best Practices для Quality Guardian

### 1. Testing Strategy
- **Test Pyramid**: 70% unit, 20% integration, 10% e2e
- **Coverage Target**: Минимум 80%, стремление к 95%
- **Performance SLA**: P95 < 2s, P99 < 5s
- **Flaky Tests**: Немедленное исправление нестабильных тестов

### 2. Code Quality Standards
- **Zero Tolerance**: Критические security issues
- **Type Safety**: 100% type coverage для Python
- **Complexity**: Максимум 15 cyclomatic complexity
- **Documentation**: Docstrings для всех публичных API

### 3. Review Process
- **Automated First**: Автоматические проверки перед human review
- **Blocking Issues**: Quality gate блокирует merge
- **Continuous Monitoring**: Постоянный мониторинг качества
- **Feedback Loop**: Быстрая обратная связь разработчикам

### 4. Quality Metrics Tracking
- **Daily Monitoring**: Ежедневные отчеты качества
- **Trend Analysis**: Отслеживание трендов качества
- **Team Training**: Обучение команды лучшим практикам
- **Process Improvement**: Постоянное улучшение процессов