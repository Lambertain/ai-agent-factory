"""Main agent implementation for Security Audit Agent."""

from pydantic_ai import Agent, RunContext
from typing import Any, Dict, List, Optional
import asyncio
import time
from datetime import datetime

from providers import get_llm_model
from dependencies import SecurityAuditDependencies
from prompts import get_security_system_prompt, get_dynamic_security_prompt
from tools import (
    scan_code_security,
    analyze_code_vulnerabilities,
    check_dependency_vulnerabilities,
    generate_security_report,
    break_down_to_microtasks,
    report_microtask_progress,
    delegate_task_to_agent,
    reflect_and_improve,
    check_delegation_need,
    search_agent_knowledge,
    SecurityFinding,
    VulnerabilityReport
)


# Initialize the security audit agent with universal prompt
security_agent = Agent(
    get_llm_model(),
    deps_type=SecurityAuditDependencies,
    system_prompt=get_security_system_prompt()  # Использует универсальный промпт
)

# Register security tools
security_agent.tool(scan_code_security)
security_agent.tool(analyze_code_vulnerabilities)
security_agent.tool(check_dependency_vulnerabilities)
security_agent.tool(generate_security_report)

# Register mandatory collective work tools
security_agent.tool(break_down_to_microtasks)
security_agent.tool(report_microtask_progress)
security_agent.tool(delegate_task_to_agent)
security_agent.tool(reflect_and_improve)
security_agent.tool(check_delegation_need)
security_agent.tool(search_agent_knowledge)


async def run_security_audit(
    target_path: str,
    scan_type: str = "comprehensive",
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a complete security audit on the specified target.

    Args:
        target_path: Path to file or directory to audit
        scan_type: Type of scan (quick, comprehensive, focused)
        session_id: Optional session identifier

    Returns:
        Comprehensive security audit results
    """
    start_time = time.time()

    # Initialize dependencies
    deps = SecurityAuditDependencies(session_id=session_id)
    await deps.initialize()

    try:
        # Run security scan
        result = await security_agent.run(
            f"Perform a {scan_type} security audit of: {target_path}",
            deps=deps
        )

        # Calculate scan duration
        scan_duration = time.time() - start_time

        # Process and enhance results
        audit_results = {
            "scan_summary": {
                "target": target_path,
                "scan_type": scan_type,
                "session_id": deps.session_id,
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "duration_seconds": scan_duration,
                "status": "completed"
            },
            "agent_response": result.data,
            "scan_metrics": deps.scan_metrics,
            "recommendations": _extract_recommendations(result.data),
            "next_steps": _generate_next_steps(result.data)
        }

        # Add to scan history
        deps.add_scan_result({
            "scan_id": deps.current_scan_id or "unknown",
            "target": target_path,
            "total_findings": _count_findings(result.data),
            "risk_score": _calculate_risk_score(result.data),
            "scan_duration": scan_duration
        })

        # Send notifications for critical findings
        critical_findings = _extract_critical_findings(result.data)
        if critical_findings:
            await deps.send_notification(
                severity="critical",
                title=f"Critical security findings in {target_path}",
                message=f"Found {len(critical_findings)} critical security issues",
                findings=critical_findings
            )

        return audit_results

    except Exception as e:
        return {
            "scan_summary": {
                "target": target_path,
                "scan_type": scan_type,
                "session_id": deps.session_id,
                "duration_seconds": time.time() - start_time,
                "status": "failed",
                "error": str(e)
            },
            "agent_response": f"Security audit failed: {str(e)}",
            "recommendations": ["Fix configuration issues and retry scan"],
            "next_steps": ["Review error logs", "Check scan permissions", "Verify target accessibility"]
        }

    finally:
        await deps.cleanup()


async def run_focused_scan(
    target_path: str,
    focus_areas: List[str],
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a focused security scan on specific areas.

    Args:
        target_path: Path to file or directory to audit
        focus_areas: List of areas to focus on (secrets, dependencies, code, compliance)
        session_id: Optional session identifier

    Returns:
        Focused security scan results
    """
    deps = SecurityAuditDependencies(session_id=session_id)
    await deps.initialize()

    # Set scan preferences for focused areas
    for area in focus_areas:
        deps.set_scan_preference(f"focus_{area}", True)

    try:
        prompt = f"Perform focused security analysis of {target_path} with emphasis on: {', '.join(focus_areas)}"
        result = await security_agent.run(prompt, deps=deps)

        return {
            "target": target_path,
            "focus_areas": focus_areas,
            "results": result.data,
            "session_id": deps.session_id
        }

    finally:
        await deps.cleanup()


async def analyze_security_trends(session_id: str) -> Dict[str, Any]:
    """
    Analyze security trends across multiple scans in a session.

    Args:
        session_id: Session identifier to analyze

    Returns:
        Security trend analysis
    """
    deps = SecurityAuditDependencies(session_id=session_id)
    await deps.initialize()

    try:
        if not deps.scan_history:
            return {
                "session_id": session_id,
                "message": "No scan history available for trend analysis",
                "recommendations": ["Perform multiple scans to enable trend analysis"]
            }

        # Analyze trends
        trends = _analyze_scan_trends(deps.scan_history)

        prompt = f"Analyze these security scan trends and provide insights: {trends}"
        result = await security_agent.run(prompt, deps=deps)

        return {
            "session_id": session_id,
            "scan_count": len(deps.scan_history),
            "trends": trends,
            "analysis": result.data,
            "recommendations": _extract_trend_recommendations(result.data)
        }

    finally:
        await deps.cleanup()


async def generate_compliance_report(
    target_path: str,
    frameworks: List[str],
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate compliance report for specified frameworks.

    Args:
        target_path: Path to audit for compliance
        frameworks: List of compliance frameworks (owasp, pci_dss, hipaa, gdpr)
        session_id: Optional session identifier

    Returns:
        Compliance assessment report
    """
    deps = SecurityAuditDependencies(session_id=session_id)
    await deps.initialize()

    # Enable specified compliance frameworks
    for framework in frameworks:
        deps.set_scan_preference(f"compliance_{framework}", True)

    try:
        prompt = f"Generate compliance report for {target_path} against {', '.join(frameworks)} frameworks"
        result = await security_agent.run(prompt, deps=deps)

        return {
            "target": target_path,
            "frameworks": frameworks,
            "compliance_status": _extract_compliance_status(result.data),
            "detailed_report": result.data,
            "session_id": deps.session_id
        }

    finally:
        await deps.cleanup()


async def perform_threat_modeling(
    target_path: str,
    system_description: str,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform automated threat modeling analysis.

    Args:
        target_path: Path to system/application to model
        system_description: Description of the system architecture
        session_id: Optional session identifier

    Returns:
        Threat modeling results
    """
    deps = SecurityAuditDependencies(session_id=session_id)
    await deps.initialize()

    deps.set_scan_preference("threat_modeling", True)

    try:
        prompt = f"""
        Perform threat modeling analysis for system at {target_path}.

        System Description: {system_description}

        Identify threats using STRIDE methodology and provide mitigation strategies.
        """

        result = await security_agent.run(prompt, deps=deps)

        return {
            "target": target_path,
            "system_description": system_description,
            "threat_model": result.data,
            "threats_identified": _extract_threats(result.data),
            "mitigation_strategies": _extract_mitigations(result.data),
            "session_id": deps.session_id
        }

    finally:
        await deps.cleanup()


# Helper functions

def _extract_recommendations(agent_response: str) -> List[str]:
    """Extract actionable recommendations from agent response."""
    recommendations = []

    # Simple pattern matching for recommendations
    lines = agent_response.split('\n')
    in_recommendations = False

    for line in lines:
        line = line.strip()
        if 'recommendation' in line.lower() or 'suggest' in line.lower():
            in_recommendations = True
        elif in_recommendations and line.startswith(('-', '*', '•')):
            recommendations.append(line[1:].strip())
        elif in_recommendations and line and not line.startswith((' ', '\t')):
            in_recommendations = False

    return recommendations[:10]  # Limit to top 10 recommendations


def _generate_next_steps(agent_response: str) -> List[str]:
    """Generate next steps based on agent response."""
    next_steps = [
        "Review all critical and high severity findings",
        "Prioritize fixes based on business impact",
        "Update vulnerable dependencies",
        "Implement recommended security controls",
        "Schedule follow-up security scan"
    ]

    # Add specific next steps based on response content
    if "critical" in agent_response.lower():
        next_steps.insert(0, "Address critical vulnerabilities immediately")

    if "compliance" in agent_response.lower():
        next_steps.append("Review compliance framework requirements")

    if "secret" in agent_response.lower() or "credential" in agent_response.lower():
        next_steps.append("Rotate any exposed credentials")

    return next_steps


def _count_findings(agent_response: str) -> int:
    """Count security findings in agent response."""
    # Simple heuristic to count findings
    finding_indicators = ['vulnerability', 'security issue', 'finding', 'risk']
    count = 0

    for indicator in finding_indicators:
        count += agent_response.lower().count(indicator)

    return min(count, 100)  # Cap at reasonable maximum


def _calculate_risk_score(agent_response: str) -> float:
    """Calculate overall risk score from agent response."""
    # Simple scoring based on severity mentions
    critical_count = agent_response.lower().count('critical')
    high_count = agent_response.lower().count('high')
    medium_count = agent_response.lower().count('medium')

    # Weight by severity
    score = (critical_count * 10) + (high_count * 5) + (medium_count * 2)

    # Normalize to 0-100 scale
    return min(100.0, score * 2.0)


def _extract_critical_findings(agent_response: str) -> List[Dict[str, str]]:
    """Extract critical findings from agent response."""
    findings = []

    if 'critical' in agent_response.lower():
        # Simple extraction of critical issues
        lines = agent_response.split('\n')
        for line in lines:
            if 'critical' in line.lower():
                findings.append({
                    "severity": "critical",
                    "description": line.strip(),
                    "category": "security_issue"
                })

    return findings[:5]  # Limit to top 5 critical findings


def _analyze_scan_trends(scan_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze trends in scan history."""
    if len(scan_history) < 2:
        return {"message": "Insufficient data for trend analysis"}

    # Calculate trend metrics
    recent_scans = scan_history[-5:]
    findings_trend = [scan.get("findings_count", 0) for scan in recent_scans]
    risk_trend = [scan.get("risk_score", 0) for scan in recent_scans]

    return {
        "total_scans": len(scan_history),
        "recent_scans": len(recent_scans),
        "findings_trend": findings_trend,
        "risk_trend": risk_trend,
        "average_findings": sum(findings_trend) / len(findings_trend),
        "average_risk": sum(risk_trend) / len(risk_trend),
        "trend_direction": "improving" if risk_trend[-1] < risk_trend[0] else "worsening"
    }


def _extract_trend_recommendations(agent_response: str) -> List[str]:
    """Extract trend-specific recommendations."""
    return [
        "Continue regular security scanning",
        "Track security metrics over time",
        "Focus on persistent vulnerabilities",
        "Implement continuous security monitoring"
    ]


def _extract_compliance_status(agent_response: str) -> Dict[str, str]:
    """Extract compliance status from agent response."""
    status = {}

    frameworks = ["owasp", "pci_dss", "hipaa", "gdpr"]
    for framework in frameworks:
        if framework.lower() in agent_response.lower():
            if "compliant" in agent_response.lower():
                status[framework] = "compliant"
            elif "non-compliant" in agent_response.lower():
                status[framework] = "non-compliant"
            else:
                status[framework] = "partially-compliant"

    return status


def _extract_threats(agent_response: str) -> List[str]:
    """Extract identified threats from threat modeling response."""
    threats = []

    # Look for STRIDE categories
    stride_categories = ["spoofing", "tampering", "repudiation", "information disclosure", "denial of service", "elevation of privilege"]

    for category in stride_categories:
        if category in agent_response.lower():
            threats.append(f"{category.title()} threat identified")

    return threats


def _extract_mitigations(agent_response: str) -> List[str]:
    """Extract mitigation strategies from threat modeling response."""
    mitigations = []

    # Common mitigation patterns
    mitigation_keywords = ["implement", "use", "enable", "configure", "deploy"]

    lines = agent_response.split('\n')
    for line in lines:
        for keyword in mitigation_keywords:
            if keyword in line.lower() and len(line.strip()) > 20:
                mitigations.append(line.strip())
                break

    return mitigations[:10]  # Limit to top 10 mitigations