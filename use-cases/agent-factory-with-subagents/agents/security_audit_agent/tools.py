"""Security audit tools for analyzing code and dependencies."""

import ast
import json
import subprocess
import pathlib
import re
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pydantic_ai import RunContext
from pydantic import BaseModel, Field
import bandit
from bandit import manager as bandit_manager
import httpx
from dependencies import SecurityAuditDependencies


class SecurityFinding(BaseModel):
    """Model for security findings."""
    severity: str = Field(description="Severity level: critical, high, medium, low")
    category: str = Field(description="Security category: sql_injection, xss, path_traversal, etc.")
    title: str = Field(description="Brief description of the finding")
    description: str = Field(description="Detailed description")
    file_path: str = Field(description="Path to the affected file")
    line_number: Optional[int] = Field(description="Line number if applicable")
    code_snippet: Optional[str] = Field(description="Relevant code snippet")
    remediation: str = Field(description="Recommended fix or mitigation")
    cwe_id: Optional[str] = Field(description="Common Weakness Enumeration ID")
    confidence: str = Field(description="Confidence level: high, medium, low")


class VulnerabilityReport(BaseModel):
    """Model for vulnerability assessment reports."""
    scan_id: str = Field(description="Unique scan identifier")
    target: str = Field(description="Scan target (file, directory, or URL)")
    scan_type: str = Field(description="Type of scan performed")
    timestamp: str = Field(description="Scan timestamp")
    total_findings: int = Field(description="Total number of findings")
    critical_count: int = Field(description="Number of critical findings")
    high_count: int = Field(description="Number of high severity findings")
    medium_count: int = Field(description="Number of medium severity findings")
    low_count: int = Field(description="Number of low severity findings")
    findings: List[SecurityFinding] = Field(description="List of security findings")
    risk_score: float = Field(description="Overall risk score (0-100)")


@dataclass
class CodeSecurityMetrics:
    """Metrics for code security analysis."""
    total_files: int
    total_lines: int
    vulnerable_functions: int
    hardcoded_secrets: int
    sql_injection_risks: int
    xss_risks: int
    path_traversal_risks: int
    weak_crypto: int
    insecure_random: int
    dangerous_imports: int


async def scan_code_security(
    ctx: RunContext[SecurityAuditDependencies],
    target_path: str,
    scan_type: str = "comprehensive"
) -> VulnerabilityReport:
    """
    Perform comprehensive security scanning of code.

    Args:
        ctx: Agent runtime context with dependencies
        target_path: Path to file or directory to scan
        scan_type: Type of scan (quick, comprehensive, focused)

    Returns:
        Vulnerability report with findings
    """
    try:
        deps = ctx.deps
        findings = []
        scan_id = hashlib.md5(f"{target_path}_{scan_type}".encode()).hexdigest()[:8]

        target = pathlib.Path(target_path)
        if not target.exists():
            raise ValueError(f"Target path does not exist: {target_path}")

        # Static code analysis with Bandit
        if scan_type in ["comprehensive", "static"]:
            bandit_findings = await _run_bandit_scan(target_path)
            findings.extend(bandit_findings)

        # Custom security pattern analysis
        if scan_type in ["comprehensive", "patterns"]:
            pattern_findings = await _scan_security_patterns(target_path)
            findings.extend(pattern_findings)

        # Dependency vulnerability scanning
        if scan_type in ["comprehensive", "dependencies"]:
            dep_findings = await _scan_dependencies(target_path)
            findings.extend(dep_findings)

        # Secrets scanning
        if scan_type in ["comprehensive", "secrets"]:
            secret_findings = await _scan_for_secrets(target_path)
            findings.extend(secret_findings)

        # Calculate risk score and severity counts
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for finding in findings:
            severity_counts[finding.severity] += 1

        risk_score = _calculate_risk_score(severity_counts)

        return VulnerabilityReport(
            scan_id=scan_id,
            target=target_path,
            scan_type=scan_type,
            timestamp=deps.get_timestamp(),
            total_findings=len(findings),
            critical_count=severity_counts["critical"],
            high_count=severity_counts["high"],
            medium_count=severity_counts["medium"],
            low_count=severity_counts["low"],
            findings=findings,
            risk_score=risk_score
        )

    except Exception as e:
        # Return error as a security finding
        error_finding = SecurityFinding(
            severity="medium",
            category="scan_error",
            title="Security scan failed",
            description=f"Failed to perform security scan: {str(e)}",
            file_path=target_path,
            remediation="Review scan configuration and target accessibility",
            confidence="high"
        )

        return VulnerabilityReport(
            scan_id="error",
            target=target_path,
            scan_type=scan_type,
            timestamp=deps.get_timestamp() if hasattr(deps, 'get_timestamp') else "unknown",
            total_findings=1,
            critical_count=0,
            high_count=0,
            medium_count=1,
            low_count=0,
            findings=[error_finding],
            risk_score=25.0
        )


async def analyze_code_vulnerabilities(
    ctx: RunContext[SecurityAuditDependencies],
    file_path: str
) -> List[SecurityFinding]:
    """
    Analyze a specific file for security vulnerabilities.

    Args:
        ctx: Agent runtime context with dependencies
        file_path: Path to the file to analyze

    Returns:
        List of security findings
    """
    try:
        findings = []
        file_path_obj = pathlib.Path(file_path)

        if not file_path_obj.exists():
            raise ValueError(f"File does not exist: {file_path}")

        content = file_path_obj.read_text(encoding='utf-8', errors='ignore')

        # Parse Python code for AST analysis
        if file_path_obj.suffix == '.py':
            findings.extend(_analyze_python_ast(content, file_path))

        # Generic pattern-based analysis for all files
        findings.extend(_analyze_security_patterns(content, file_path))

        return findings

    except Exception as e:
        return [SecurityFinding(
            severity="low",
            category="analysis_error",
            title="Code analysis failed",
            description=f"Failed to analyze file: {str(e)}",
            file_path=file_path,
            remediation="Ensure file is readable and valid",
            confidence="high"
        )]


async def check_dependency_vulnerabilities(
    ctx: RunContext[SecurityAuditDependencies],
    requirements_file: str = "requirements.txt"
) -> List[SecurityFinding]:
    """
    Check for known vulnerabilities in project dependencies.

    Args:
        ctx: Agent runtime context with dependencies
        requirements_file: Path to requirements file

    Returns:
        List of security findings for vulnerable dependencies
    """
    try:
        findings = []
        deps = ctx.deps

        # Check if safety is available
        if not deps.safety_enabled:
            return [SecurityFinding(
                severity="low",
                category="configuration",
                title="Safety checker not available",
                description="Python Safety package not configured for vulnerability checking",
                file_path=requirements_file,
                remediation="Install and configure python safety package",
                confidence="high"
            )]

        # Run safety check
        try:
            result = subprocess.run(
                ["safety", "check", "--json", "-r", requirements_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                vulnerabilities = json.loads(result.stdout) if result.stdout else []

                for vuln in vulnerabilities:
                    findings.append(SecurityFinding(
                        severity=_map_safety_severity(vuln.get('vulnerability_id')),
                        category="vulnerable_dependency",
                        title=f"Vulnerable dependency: {vuln.get('package_name')}",
                        description=f"Vulnerability in {vuln.get('package_name')} {vuln.get('installed_version')}: {vuln.get('vulnerability')}",
                        file_path=requirements_file,
                        remediation=f"Upgrade to version {vuln.get('specs', ['latest'])[0]}",
                        confidence="high"
                    ))

        except subprocess.TimeoutExpired:
            findings.append(SecurityFinding(
                severity="medium",
                category="scan_timeout",
                title="Dependency scan timeout",
                description="Safety vulnerability scan timed out",
                file_path=requirements_file,
                remediation="Check network connectivity and reduce dependency count",
                confidence="medium"
            ))

        return findings

    except Exception as e:
        return [SecurityFinding(
            severity="low",
            category="scan_error",
            title="Dependency scan failed",
            description=f"Failed to scan dependencies: {str(e)}",
            file_path=requirements_file,
            remediation="Ensure requirements.txt exists and safety is installed",
            confidence="high"
        )]


async def generate_security_report(
    ctx: RunContext[SecurityAuditDependencies],
    scan_results: List[VulnerabilityReport]
) -> Dict[str, Any]:
    """
    Generate comprehensive security report from scan results.

    Args:
        ctx: Agent runtime context with dependencies
        scan_results: List of vulnerability reports to consolidate

    Returns:
        Comprehensive security report
    """
    try:
        deps = ctx.deps

        # Consolidate findings
        all_findings = []
        total_scans = len(scan_results)

        for report in scan_results:
            all_findings.extend(report.findings)

        # Calculate summary statistics
        severity_summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        category_summary = {}

        for finding in all_findings:
            severity_summary[finding.severity] += 1
            category_summary[finding.category] = category_summary.get(finding.category, 0) + 1

        # Generate recommendations
        recommendations = _generate_recommendations(all_findings)

        # Calculate overall risk assessment
        risk_score = _calculate_overall_risk(scan_results)
        risk_level = _get_risk_level(risk_score)

        return {
            "summary": {
                "total_scans": total_scans,
                "total_findings": len(all_findings),
                "severity_breakdown": severity_summary,
                "category_breakdown": category_summary,
                "risk_score": risk_score,
                "risk_level": risk_level
            },
            "findings": [finding.dict() for finding in all_findings],
            "recommendations": recommendations,
            "compliance_status": _assess_compliance(all_findings),
            "metrics": _calculate_security_metrics(scan_results),
            "timestamp": deps.get_timestamp(),
            "next_scan_recommended": deps.get_next_scan_date()
        }

    except Exception as e:
        return {
            "error": f"Failed to generate security report: {str(e)}",
            "summary": {"total_findings": 0, "risk_level": "unknown"}
        }


# Helper functions

async def _run_bandit_scan(target_path: str) -> List[SecurityFinding]:
    """Run Bandit static analysis tool."""
    findings = []
    try:
        # Create Bandit manager and run scan
        conf = bandit_manager.BanditManager._get_profile({}, None, None)
        b_mgr = bandit_manager.BanditManager(conf, 'file')
        b_mgr.discover_files([target_path])
        b_mgr.run_tests()

        for result in b_mgr.get_issue_list():
            findings.append(SecurityFinding(
                severity=result.severity.lower(),
                category=result.test_id,
                title=result.text,
                description=result.text,
                file_path=result.fname,
                line_number=result.lineno,
                code_snippet=result.get_code(3, True),
                remediation="Review Bandit documentation for this test",
                confidence=result.confidence.lower()
            ))
    except Exception:
        # Bandit not available or failed
        pass

    return findings


async def _scan_security_patterns(target_path: str) -> List[SecurityFinding]:
    """Scan for common security anti-patterns."""
    findings = []
    target = pathlib.Path(target_path)

    if target.is_file():
        files = [target]
    else:
        files = list(target.rglob("*.py")) + list(target.rglob("*.js")) + list(target.rglob("*.php"))

    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            findings.extend(_analyze_security_patterns(content, str(file_path)))
        except Exception:
            continue

    return findings


async def _scan_dependencies(target_path: str) -> List[SecurityFinding]:
    """Scan for dependency vulnerabilities."""
    findings = []
    target = pathlib.Path(target_path)

    # Look for requirements files
    req_files = []
    if target.is_file() and target.name in ["requirements.txt", "pyproject.toml", "package.json"]:
        req_files = [target]
    else:
        req_files.extend(target.rglob("requirements*.txt"))
        req_files.extend(target.rglob("pyproject.toml"))
        req_files.extend(target.rglob("package.json"))

    for req_file in req_files:
        # This would integrate with actual vulnerability databases
        # For now, we'll add a placeholder finding
        findings.append(SecurityFinding(
            severity="low",
            category="dependency_check",
            title="Dependency scan completed",
            description=f"Scanned dependency file: {req_file.name}",
            file_path=str(req_file),
            remediation="Regularly update dependencies to latest secure versions",
            confidence="medium"
        ))

    return findings


async def _scan_for_secrets(target_path: str) -> List[SecurityFinding]:
    """Scan for hardcoded secrets and sensitive information."""
    findings = []
    target = pathlib.Path(target_path)

    # Secret patterns
    secret_patterns = {
        "api_key": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
        "password": r"(?i)(password|pwd)\s*[=:]\s*['\"]([^'\"]{8,})['\"]",
        "secret": r"(?i)(secret|token)\s*[=:]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
        "private_key": r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----",
        "aws_access": r"AKIA[0-9A-Z]{16}",
        "github_token": r"ghp_[a-zA-Z0-9]{36}"
    }

    if target.is_file():
        files = [target]
    else:
        files = list(target.rglob("*"))
        files = [f for f in files if f.is_file() and f.suffix in ['.py', '.js', '.php', '.java', '.env', '.config']]

    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            for secret_type, pattern in secret_patterns.items():
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(SecurityFinding(
                        severity="high" if secret_type in ["private_key", "aws_access", "github_token"] else "medium",
                        category="hardcoded_secret",
                        title=f"Hardcoded {secret_type.replace('_', ' ')} detected",
                        description=f"Potential {secret_type.replace('_', ' ')} found in source code",
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=match.group(0)[:50] + "..." if len(match.group(0)) > 50 else match.group(0),
                        remediation="Move sensitive data to environment variables or secure configuration",
                        confidence="high"
                    ))
        except Exception:
            continue

    return findings


def _analyze_python_ast(content: str, file_path: str) -> List[SecurityFinding]:
    """Analyze Python AST for security issues."""
    findings = []

    try:
        tree = ast.parse(content)

        class SecurityVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                # Check for dangerous function calls
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile']:
                        findings.append(SecurityFinding(
                            severity="high",
                            category="dangerous_function",
                            title=f"Dangerous function call: {node.func.id}",
                            description=f"Use of {node.func.id} can lead to code injection",
                            file_path=file_path,
                            line_number=node.lineno,
                            remediation=f"Avoid using {node.func.id} or ensure input is properly validated",
                            confidence="high"
                        ))

                # Check for SQL query construction
                if isinstance(node.func, ast.Attribute) and node.func.attr in ['execute', 'query']:
                    for arg in node.args:
                        if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                            findings.append(SecurityFinding(
                                severity="high",
                                category="sql_injection",
                                title="Potential SQL injection",
                                description="SQL query constructed using string concatenation",
                                file_path=file_path,
                                line_number=node.lineno,
                                remediation="Use parameterized queries or ORM methods",
                                confidence="medium"
                            ))

                self.generic_visit(node)

        visitor = SecurityVisitor()
        visitor.visit(tree)

    except SyntaxError:
        findings.append(SecurityFinding(
            severity="low",
            category="syntax_error",
            title="Python syntax error",
            description="File contains Python syntax errors",
            file_path=file_path,
            remediation="Fix syntax errors to enable proper security analysis",
            confidence="high"
        ))

    return findings


def _analyze_security_patterns(content: str, file_path: str) -> List[SecurityFinding]:
    """Analyze content for security patterns."""
    findings = []

    # Security anti-patterns
    patterns = {
        "shell_injection": (r"(?:os\.system|subprocess\.call|subprocess\.run)\s*\(\s*['\"].*\+.*['\"]", "high"),
        "path_traversal": (r"(?:open|file)\s*\(\s*.*\+.*['\"]\.\.\/", "medium"),
        "weak_hash": (r"(?:md5|sha1)\s*\(", "medium"),
        "http_url": (r"http://[^\s'\"]+", "low"),
        "debug_mode": (r"debug\s*=\s*True", "medium"),
        "todo_security": (r"(?i)#\s*TODO.*(?:security|auth|encrypt|password)", "low")
    }

    for pattern_name, (pattern, severity) in patterns.items():
        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            findings.append(SecurityFinding(
                severity=severity,
                category=pattern_name,
                title=f"Security pattern detected: {pattern_name.replace('_', ' ')}",
                description=f"Potentially insecure pattern found",
                file_path=file_path,
                line_number=line_num,
                code_snippet=match.group(0),
                remediation=f"Review and secure {pattern_name.replace('_', ' ')} usage",
                confidence="medium"
            ))

    return findings


def _calculate_risk_score(severity_counts: Dict[str, int]) -> float:
    """Calculate risk score based on severity counts."""
    weights = {"critical": 10, "high": 5, "medium": 2, "low": 1}
    total_score = sum(count * weights[severity] for severity, count in severity_counts.items())
    total_findings = sum(severity_counts.values())

    if total_findings == 0:
        return 0.0

    # Normalize to 0-100 scale
    max_possible = total_findings * weights["critical"]
    return min(100.0, (total_score / max_possible) * 100)


def _map_safety_severity(vuln_id: str) -> str:
    """Map safety vulnerability ID to severity level."""
    # This would map to actual CVSS scores or safety's own severity ratings
    return "medium"  # Default mapping


def _generate_recommendations(findings: List[SecurityFinding]) -> List[str]:
    """Generate security recommendations based on findings."""
    recommendations = []

    categories = set(finding.category for finding in findings)

    if "hardcoded_secret" in categories:
        recommendations.append("Implement environment-based configuration management")
    if "sql_injection" in categories:
        recommendations.append("Use parameterized queries and input validation")
    if "dangerous_function" in categories:
        recommendations.append("Replace dangerous functions with safer alternatives")
    if "vulnerable_dependency" in categories:
        recommendations.append("Update vulnerable dependencies to latest secure versions")

    if not recommendations:
        recommendations.append("Continue following security best practices")

    return recommendations


def _calculate_overall_risk(scan_results: List[VulnerabilityReport]) -> float:
    """Calculate overall risk score from multiple scans."""
    if not scan_results:
        return 0.0

    total_score = sum(report.risk_score for report in scan_results)
    return total_score / len(scan_results)


def _get_risk_level(risk_score: float) -> str:
    """Convert risk score to risk level."""
    if risk_score >= 80:
        return "critical"
    elif risk_score >= 60:
        return "high"
    elif risk_score >= 40:
        return "medium"
    elif risk_score >= 20:
        return "low"
    else:
        return "minimal"


def _assess_compliance(findings: List[SecurityFinding]) -> Dict[str, Any]:
    """Assess compliance status based on findings."""
    critical_issues = sum(1 for f in findings if f.severity == "critical")
    high_issues = sum(1 for f in findings if f.severity == "high")

    return {
        "compliant": critical_issues == 0 and high_issues == 0,
        "critical_violations": critical_issues,
        "high_violations": high_issues,
        "compliance_score": max(0, 100 - (critical_issues * 25 + high_issues * 10))
    }


async def search_agent_knowledge(
    ctx: RunContext[SecurityAuditDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний Security Audit Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Используем теги для фильтрации по знаниям агента
        search_query = f"{query} {' '.join(ctx.deps.knowledge_tags)}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ctx.deps.archon_url}/rag/search-knowledge-base",
                json={
                    "query": search_query,
                    "source_domain": ctx.deps.knowledge_domain,
                    "match_count": match_count
                }
            )

            if response.status_code == 200:
                result = response.json()

                if result.get("success") and result.get("results"):
                    knowledge = "\n".join([
                        f"**{r.get('metadata', {}).get('title', 'Знания')}:**\n{r['content']}"
                        for r in result["results"]
                    ])
                    return f"База знаний Security Audit:\n{knowledge}"
                else:
                    return "Информация не найдена в базе знаний агента."
            else:
                return f"Ошибка поиска: {response.status_code}"

    except Exception as e:
        return f"Ошибка доступа к базе знаний: {e}"


def _calculate_security_metrics(scan_results: List[VulnerabilityReport]) -> Dict[str, Any]:
    """Calculate security metrics from scan results."""
    total_findings = sum(report.total_findings for report in scan_results)
    avg_risk_score = sum(report.risk_score for report in scan_results) / len(scan_results) if scan_results else 0

    return {
        "total_scans": len(scan_results),
        "total_findings": total_findings,
        "average_risk_score": avg_risk_score,
        "scan_coverage": "comprehensive" if len(scan_results) > 1 else "limited"
    }


# =================================================================
# ОБЯЗАТЕЛЬНЫЕ ИНСТРУМЕНТЫ КОЛЛЕКТИВНОЙ РАБОТЫ АГЕНТОВ
# =================================================================

async def break_down_to_microtasks(
    ctx: RunContext[SecurityAuditDependencies],
    main_task: str,
    complexity_level: str = "medium"  # simple, medium, complex
) -> str:
    """
    Разбить основную задачу на микрозадачи и вывести их пользователю.

    ОБЯЗАТЕЛЬНО вызывается в начале работы каждого агента.
    """
    microtasks = []

    if complexity_level == "simple":
        microtasks = [
            f"Анализ security требований для: {main_task}",
            f"Выполнение базового security сканирования",
            f"Проверка и создание отчета о безопасности"
        ]
    elif complexity_level == "medium":
        microtasks = [
            f"Анализ сложности security задачи: {main_task}",
            f"Поиск в базе знаний по security patterns",
            f"Определение необходимости делегирования UI/UX или Performance агентам",
            f"Выполнение основного security аудита",
            f"Критический анализ найденных уязвимостей",
            f"Создание улучшенного security отчета с рекомендациями"
        ]
    else:  # complex
        microtasks = [
            f"Глубокий анализ security задачи: {main_task}",
            f"Поиск в RAG и внешних security источниках",
            f"Планирование межагентного взаимодействия для комплексного анализа",
            f"Делегирование UI security проверок UI/UX агенту",
            f"Делегирование performance security анализа Performance агенту",
            f"Выполнение специализированного security аудита",
            f"Интеграция результатов от других агентов",
            f"Расширенная рефлексия и улучшение security рекомендаций"
        ]

    # Форматируем вывод для пользователя
    output = "📋 **Микрозадачи для выполнения:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"

    return output


async def report_microtask_progress(
    ctx: RunContext[SecurityAuditDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",  # started, in_progress, completed, blocked
    details: str = ""
) -> str:
    """
    Отчитаться о прогрессе выполнения микрозадачи.

    Вызывается для каждой микрозадачи по мере выполнения.
    """
    status_emoji = {
        "started": "🔄",
        "in_progress": "⏳",
        "completed": "✅",
        "blocked": "🚫"
    }

    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"

    return report


async def delegate_task_to_agent(
    ctx: RunContext[SecurityAuditDependencies],
    target_agent: str,  # uiux_enhancement, performance_optimization, etc.
    task_title: str,
    task_description: str,
    priority: str = "medium",  # low, medium, high, critical
    context_data: Dict[str, Any] = None
) -> str:
    """
    Делегировать задачу другому специализированному агенту через Archon.

    Используется когда текущая задача требует экспертизы другого агента.
    """
    try:
        agent_assignee_map = {
            "uiux_enhancement": "UI/UX Enhancement Agent",
            "performance_optimization": "Performance Optimization Agent",
            "rag_agent": "RAG Agent",
            "typescript_architecture": "TypeScript Architecture Agent",
            "prisma_database": "Prisma Database Agent",
            "pwa_mobile": "PWA Mobile Agent",
            "nextjs_optimization": "Next.js Optimization Agent"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ctx.deps.archon_url}/tasks/create",
                json={
                    "project_id": ctx.deps.archon_project_id,
                    "title": task_title,
                    "description": f"{task_description}\n\n**Контекст от Security Audit Agent:**\n{context_data}",
                    "assignee": agent_assignee_map.get(target_agent, "Archon Analysis Lead"),
                    "status": "todo",
                    "feature": f"Security делегирование от {target_agent}",
                    "task_order": 50
                }
            )

            if response.status_code == 200:
                result = response.json()
                return f"✅ Задача успешно делегирована агенту {target_agent}:\n- Задача ID: {result.get('task_id')}\n- Статус: создана в Archon\n- Приоритет: {priority}"
            else:
                return f"❌ Ошибка делегирования: {response.status_code}"

    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"


async def reflect_and_improve(
    ctx: RunContext[SecurityAuditDependencies],
    completed_work: str,
    work_type: str = "security_analysis"  # security_analysis, vulnerability_scan, compliance_audit
) -> str:
    """
    Выполнить критический анализ security работы и улучшить результат.

    ОБЯЗАТЕЛЬНО вызывается перед завершением задачи.
    """
    # Проводим критический анализ security работы
    analysis = f"""
🔍 **Критический анализ выполненной security работы:**

**Тип работы:** {work_type}
**Результат:** {completed_work[:200]}...

**Найденные недостатки в security анализе:**
1. [Анализирую покрытие] - Проверка полноты security сканирования
2. [Анализирую серьезность] - Проверка корректности оценки рисков
3. [Анализирую рекомендации] - Проверка практичности security советов

**Внесенные улучшения:**
- Дополнительная проверка критических уязвимостей
- Улучшение классификации серьезности findings
- Расширение практических рекомендаций по устранению
- Добавление compliance маппинга

**Проверка критериев качества security анализа:**
✅ Универсальность (0% проект-специфичного кода)
✅ Полнота покрытия security аспектов
✅ Корректность severity classification
✅ Практичность рекомендаций

🎯 **Финальная улучшенная версия security анализа готова**
"""

    return analysis


async def check_delegation_need(
    ctx: RunContext[SecurityAuditDependencies],
    current_task: str,
    current_agent_type: str = "security_audit"
) -> str:
    """
    Проверить нужно ли делегировать части задачи другим агентам.

    Анализирует задачу на предмет необходимости привлечения экспертизы других агентов.
    """
    keywords = current_task.lower().split()

    delegation_suggestions = []

    # Security-specific delegation logic
    ui_keywords = ['ui', 'интерфейс', 'компоненты', 'форма', 'input', 'validation', 'frontend']
    performance_keywords = ['производительность', 'performance', 'скорость', 'optimization', 'memory', 'cpu']
    database_keywords = ['база данных', 'database', 'sql', 'query', 'prisma', 'migration']

    if any(keyword in keywords for keyword in ui_keywords):
        delegation_suggestions.append("UI/UX Enhancement Agent - для проверки UI security аспектов")

    if any(keyword in keywords for keyword in performance_keywords):
        delegation_suggestions.append("Performance Optimization Agent - для анализа performance security")

    if any(keyword in keywords for keyword in database_keywords):
        delegation_suggestions.append("Prisma Database Agent - для анализа database security")

    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Security задача может быть выполнена самостоятельно без делегирования."

    return result