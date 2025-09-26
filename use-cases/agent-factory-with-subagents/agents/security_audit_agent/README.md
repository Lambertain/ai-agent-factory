# Security Audit Agent

**Universal Security Audit Agent for comprehensive security analysis across any project type**

The Security Audit Agent specializes in automated security testing, vulnerability assessment, and compliance auditing for diverse project types including web applications, APIs, mobile apps, infrastructure, and regulatory compliance systems.

## 🎯 Purpose

The agent performs comprehensive security analysis with focus on:
- **Vulnerability Assessment**: automated detection of security vulnerabilities
- **Compliance Auditing**: regulatory compliance verification (GDPR, HIPAA, PCI-DSS, SOX)
- **Infrastructure Security**: cloud and container security analysis
- **Mobile Security**: iOS and Android application security testing
- **API Security**: REST and GraphQL endpoint security validation

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
cp .env.example .env
# Configure security tools and API keys in .env
```

### CLI Usage
```bash
# Web application security audit
python -m security_audit_agent.cli audit /path/to/web/app --type web-app --compliance owasp-top10

# API security assessment
python -m security_audit_agent.cli audit /path/to/api --type api --focus authentication

# Mobile app security scan
python -m security_audit_agent.cli audit /path/to/mobile/app --type mobile --platform android

# Infrastructure security audit
python -m security_audit_agent.cli audit /path/to/terraform --type infrastructure --cloud aws

# Compliance audit
python -m security_audit_agent.cli compliance /path/to/app --frameworks gdpr,hipaa,pci-dss
```

### Python API Usage
```python
import asyncio
from security_audit_agent import run_security_audit
from security_audit_agent.dependencies import SecurityAuditDependencies

async def main():
    # Configure for your project type
    deps = SecurityAuditDependencies(
        project_type="web-app",  # or api, mobile, infrastructure, compliance
        project_path="/path/to/project",
        security_focus="owasp-top10",
        compliance_frameworks=["owasp-top10", "pci-dss"]
    )

    result = await run_security_audit(
        target_path=deps.project_path,
        scan_type="comprehensive"
    )
    print(f"Security scan complete: {result['scan_summary']['status']}")

asyncio.run(main())
```

## 🛠️ Security Tools Integration

### Static Analysis Tools
- **Bandit**: Python code security analysis
- **Semgrep**: Multi-language static analysis
- **ESLint Security**: JavaScript security linting
- **CodeQL**: Semantic code analysis

### Dynamic Analysis Tools
- **OWASP ZAP**: Web application security testing
- **Burp Suite**: Advanced security testing
- **MobSF**: Mobile security framework
- **Nuclei**: Vulnerability scanner

### Infrastructure Security
- **Trivy**: Container and IaC scanning
- **Checkov**: Infrastructure as Code security
- **Prowler**: Cloud security assessment
- **Kube-score**: Kubernetes security analysis

### Compliance Tools
- **Lynis**: System security auditing
- **OpenSCAP**: Security compliance validation
- **AWS Config**: Cloud compliance monitoring

## 📋 Project Types & Configurations

### 1. Web Application Security (`web-app`)
- **Focus Areas**: OWASP Top 10, XSS, SQL Injection, CSRF
- **Compliance**: OWASP Top 10, PCI-DSS
- **Tools**: Bandit, ZAP, Semgrep
- **Example**: [web_app_security.py](examples/web_app_security.py)

### 2. API Security (`api`)
- **Focus Areas**: Authentication, Authorization, Rate Limiting
- **Compliance**: OWASP API Top 10, PCI-DSS
- **Tools**: API fuzzing, JWT analysis, Postman security
- **Example**: [api_security.py](examples/api_security.py)

### 3. Mobile Application Security (`mobile`)
- **Focus Areas**: Data storage, Communication, Platform interaction
- **Compliance**: Mobile OWASP Top 10, GDPR
- **Tools**: MobSF, QARK, Frida
- **Example**: [mobile_app_security.py](examples/mobile_app_security.py)

### 4. Infrastructure Security (`infrastructure`)
- **Focus Areas**: Cloud misconfiguration, Container security, IaC
- **Compliance**: CIS Benchmarks, ISO27001
- **Tools**: Trivy, Checkov, Prowler
- **Example**: [infrastructure_security.py](examples/infrastructure_security.py)

### 5. Compliance Auditing (`compliance`)
- **Focus Areas**: Data protection, Access control, Audit logging
- **Compliance**: GDPR, HIPAA, PCI-DSS, SOX, ISO27001
- **Tools**: OpenSCAP, custom compliance checkers
- **Example**: [compliance_audit.py](examples/compliance_audit.py)

### 6. IoT Security (`iot`)
- **Focus Areas**: Device security, Firmware analysis, Network protocols
- **Compliance**: IoT Security Foundation guidelines
- **Tools**: Binwalk, Firmwalker, Network analyzers

### 7. Blockchain Security (`blockchain`)
- **Focus Areas**: Smart contract vulnerabilities, Consensus security
- **Compliance**: Blockchain security standards
- **Tools**: Mythril, Slither, Echidna

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Security Tools
BANDIT_CONFIG_PATH=/path/to/bandit.yaml
ZAP_API_KEY=your_zap_api_key
SEMGREP_APP_TOKEN=your_semgrep_token

# Cloud Provider APIs
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AZURE_CLIENT_ID=your_azure_client_id
GCP_SERVICE_ACCOUNT_KEY=path/to/gcp/key.json

# Vulnerability Databases
NVD_API_KEY=your_nvd_api_key
SNYK_TOKEN=your_snyk_token

# Notifications
SLACK_WEBHOOK_URL=your_slack_webhook
SMTP_SERVER=your_smtp_server
EMAIL_RECIPIENTS=security@company.com

# Compliance
PCI_DSS_LEVEL=1
HIPAA_COVERED_ENTITY=true
GDPR_DATA_CONTROLLER=true
```

### Custom Security Rules
```python
# Custom rule example
custom_rule = {
    "id": "custom-001",
    "name": "API Key Detection",
    "pattern": r"api[_-]?key['\"\s]*[:=]['\"\s]*[a-zA-Z0-9]{20,}",
    "severity": "high",
    "confidence": "medium"
}

deps.add_custom_rule(custom_rule)
```

## 🏗️ Architecture

```
security_audit_agent/
├── agent.py                    # Main security audit agent
├── dependencies.py             # Universal security dependencies
├── tools.py                    # Security scanning tools
├── prompts.py                  # Security-focused prompts
├── settings.py                 # Configuration management
├── providers.py                # LLM providers for analysis
├── cli.py                      # Command-line interface
├── examples/                   # Configuration examples
│   ├── web_app_security.py     # Web application audit
│   ├── api_security.py         # API security testing
│   ├── mobile_app_security.py  # Mobile app security
│   ├── infrastructure_security.py # Cloud/infrastructure
│   └── compliance_audit.py     # Regulatory compliance
├── knowledge/                  # Security knowledge base
│   └── security_audit_knowledge.md
├── tests/                      # Security testing framework
└── README.md                   # This documentation
```

## 🔄 Security Audit Workflow

### 1. **Discovery Phase**
- Asset identification and enumeration
- Technology stack analysis
- Attack surface mapping

### 2. **Vulnerability Assessment**
- Static code analysis
- Dynamic security testing
- Dependency vulnerability scanning
- Configuration security review

### 3. **Compliance Verification**
- Regulatory framework mapping
- Control effectiveness testing
- Gap analysis and reporting

### 4. **Threat Modeling**
- STRIDE methodology application
- Risk assessment and prioritization
- Mitigation strategy development

### 5. **Reporting & Remediation**
- Executive summary generation
- Technical findings documentation
- Remediation roadmap creation
- Continuous monitoring setup

## 📊 Security Metrics

The agent tracks comprehensive security metrics:

- **Vulnerability Metrics**: Count by severity, CVSS scores, remediation time
- **Compliance Metrics**: Framework adherence percentages, control gaps
- **Risk Metrics**: Overall risk score, business impact assessment
- **Coverage Metrics**: Code coverage, asset coverage, test coverage

## 🧪 Testing

```bash
# Run security tests
pytest tests/ -v

# Test specific security scenarios
pytest tests/test_vulnerability_detection.py
pytest tests/test_compliance_auditing.py

# Integration testing with security tools
pytest tests/test_tool_integration.py
```

## 📚 Knowledge Base Integration

The agent leverages Archon Knowledge Base for:
- **Security Patterns**: Common vulnerability patterns and fixes
- **Compliance Requirements**: Detailed regulatory requirements
- **Threat Intelligence**: Latest security threats and indicators
- **Best Practices**: Industry security best practices

### Knowledge Base Tags
- `security-audit`, `vulnerability-assessment`, `compliance`
- `owasp`, `pci-dss`, `gdpr`, `hipaa`, `iso27001`
- `web-security`, `api-security`, `mobile-security`, `cloud-security`

## 🔗 Universal Integration

The Security Audit Agent adapts to any security context:
- **CI/CD Integration**: Automated security testing in pipelines
- **SIEM Integration**: Security event correlation and analysis
- **Ticketing Systems**: Automatic vulnerability tracking
- **Compliance Platforms**: Regulatory reporting automation
- **Cloud Security**: Multi-cloud security assessment

## 📈 Continuous Security

### Automated Scanning
- **Schedule-based**: Regular security scans based on risk level
- **Event-driven**: Triggered by code changes or deployments
- **Compliance-driven**: Periodic compliance verification

### Monitoring & Alerting
- **Real-time Alerts**: Critical vulnerability notifications
- **Trend Analysis**: Security posture tracking over time
- **Compliance Dashboards**: Regulatory status monitoring

## 🤝 Integration with Other Agents

Security Audit Agent collaborates with:
- **Infrastructure Agent**: Secure infrastructure deployment
- **Code Quality Agent**: Security-focused code review
- **Compliance Agent**: Regulatory requirement validation
- **Incident Response Agent**: Security incident handling

---

**Version**: 2.0.0
**License**: MIT
**Support**: Create issues in the repository for security-related questions