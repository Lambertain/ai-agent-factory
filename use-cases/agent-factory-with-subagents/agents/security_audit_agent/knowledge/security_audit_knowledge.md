# Security Audit Agent Knowledge Base

## Системный промпт для Security Audit Agent

```
Ты специализированный агент по аудиту безопасности приложений с фокусом на современные веб-технологии и практики DevSecOps.

**Твоя экспертиза:**
- OWASP Top 10 и современные угрозы безопасности
- Статический анализ кода (SAST) и динамическое тестирование (DAST)
- Анализ зависимостей и уязвимостей Supply Chain
- Container security и Kubernetes security
- API security и аутентификация/авторизация
- Infrastructure as Code (IaC) security

**Ключевые области аудита:**

1. **Code Security Analysis:**
   - Поиск уязвимостей в коде (SQL injection, XSS, CSRF)
   - Анализ конфигураций и секретов
   - Проверка криптографических реализаций
   - Code review для security best practices

2. **Infrastructure Security:**
   - Анализ Docker/Kubernetes конфигураций
   - Cloud security (AWS, Azure, GCP)
   - Network security и firewall rules
   - SSL/TLS конфигурации

3. **Application Security:**
   - OWASP Top 10 compliance
   - API security testing
   - Authentication и authorization flows
   - Session management

**Подход к работе:**
1. Автоматизированное сканирование с использованием инструментов
2. Ручная проверка критических компонентов
3. Анализ threat modeling
4. Предоставление actionable рекомендаций
5. Интеграция с CI/CD пайплайнами
```

## OWASP Top 10 2021

### A01:2021 - Broken Access Control
**Описание:** Нарушения контроля доступа, когда пользователи могут получить доступ к ресурсам или функциям, которые им не должны быть доступны.

**Примеры уязвимостей:**
- Обход проверок авторизации через изменение URL
- Elevation of privilege атаки
- CORS неправильные конфигурации
- Доступ к API без токенов

**Методы обнаружения:**
```python
# Проверка authorization middleware
def check_authorization_bypass():
    """Проверка обхода авторизации."""
    patterns = [
        r"@app\.route.*without.*auth",
        r"if.*user\.is_admin.*else.*bypass",
        r"auth.*=.*False.*default"
    ]
    return scan_code_patterns(patterns)
```

### A02:2021 - Cryptographic Failures
**Описание:** Отказы в криптографии, включая слабое шифрование, плохое управление ключами.

**Критические проверки:**
- Использование устаревших алгоритмов (MD5, SHA1, DES)
- Хранение паролей в plain text
- Слабые случайные числа
- Отсутствие шифрования чувствительных данных

**Инструменты обнаружения:**
```bash
# Поиск слабых криптографических реализаций
grep -r "MD5\|SHA1\|DES" --include="*.py" --include="*.js" .
semgrep --config=crypto src/
```

### A03:2021 - Injection
**Описание:** SQL injection, NoSQL injection, Command injection, LDAP injection.

**SQL Injection Detection:**
```python
# Паттерны для обнаружения SQL injection
sql_injection_patterns = [
    r"\.execute\(.*\+.*\)",  # String concatenation in SQL
    r"f\".*{.*}.*\".*execute",  # F-string в SQL запросах
    r"query.*=.*request\.args",  # Прямое использование user input
]

def detect_sql_injection(code_file):
    """Анализ потенциальных SQL injection уязвимостей."""
    with open(code_file, 'r') as f:
        content = f.read()

    vulnerabilities = []
    for pattern in sql_injection_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            vulnerabilities.append({
                'type': 'SQL Injection Risk',
                'line': content[:match.start()].count('\n') + 1,
                'code': match.group()
            })

    return vulnerabilities
```

## Security Scanning Tools Integration

### SAST (Static Analysis) Tools
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  sast-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Run CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: python, javascript

      - name: Run Bandit (Python)
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json

      - name: Run ESLint Security (JavaScript)
        run: |
          npm install eslint-plugin-security
          npx eslint --ext .js,.ts --format json -o eslint-security.json .
```

### DAST (Dynamic Analysis) Tools
```bash
# OWASP ZAP автоматизированное сканирование
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://your-app.com \
  -g gen.conf \
  -r zap-report.html

# Nikto web server scanner
nikto -h https://your-app.com -Format htm -output nikto-report.html

# Nuclei template-based scanning
nuclei -u https://your-app.com \
  -t nuclei-templates/ \
  -o nuclei-results.txt
```

### Container Security Scanning
```bash
# Trivy container vulnerability scanner
trivy image your-app:latest

# Aqua Security MicroScanner
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/microscanner your-app:latest

# Snyk container scanning
snyk container test your-app:latest
```

## Common Vulnerability Patterns

### Authentication & Session Management
```python
# ❌ Небезопасные практики
def login_weak():
    password = request.form['password']
    # Нет хеширования пароля
    if user.password == password:
        session['logged_in'] = True
        # Нет regeneration session ID
        return redirect('/dashboard')

# ✅ Безопасная реализация
def login_secure():
    password = request.form['password']
    if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
        session.regenerate()  # Prevent session fixation
        session['user_id'] = user.id
        session['csrf_token'] = generate_csrf_token()
        return redirect('/dashboard')
```

### API Security Patterns
```python
# ✅ Secure API implementation
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/user/<int:user_id>')
@limiter.limit("10 per minute")
@require_auth
def get_user(user_id):
    # Authorization check
    if not current_user.can_access_user(user_id):
        abort(403)

    # Input validation
    if not isinstance(user_id, int) or user_id <= 0:
        abort(400)

    user = User.query.get_or_404(user_id)
    # Sanitize output
    return jsonify(user.to_safe_dict())
```

### Secure Configuration Examples
```python
# Django secure settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Flask secure headers
from flask_talisman import Talisman

Talisman(app, {
    'force_https': True,
    'strict_transport_security': True,
    'strict_transport_security_max_age': 31536000,
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
})
```

## Infrastructure Security Checks

### Docker Security
```dockerfile
# ✅ Secure Dockerfile practices
FROM node:16-alpine AS builder
# Use specific version, not latest

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY --chown=nextjs:nodejs . .

# Use multi-stage build
FROM node:16-alpine AS runner
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy only necessary files
COPY --from=builder --chown=nextjs:nodejs /app ./

# Don't run as root
USER nextjs

# Use specific port
EXPOSE 3000
ENV PORT 3000

CMD ["npm", "start"]
```

### Kubernetes Security
```yaml
# Secure Pod Security Standards
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: your-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
      runAsNonRoot: true
    resources:
      limits:
        cpu: 500m
        memory: 512Mi
      requests:
        cpu: 100m
        memory: 128Mi
```

## Security Testing Integration

### Automated Security Tests
```python
# security_tests.py
import requests
import pytest

class TestSecurityHeaders:
    """Test security headers implementation."""

    def test_security_headers_present(self, app_url):
        """Check for essential security headers."""
        response = requests.get(app_url)
        headers = response.headers

        assert 'X-Content-Type-Options' in headers
        assert headers['X-Content-Type-Options'] == 'nosniff'

        assert 'X-Frame-Options' in headers
        assert headers['X-Frame-Options'] in ['DENY', 'SAMEORIGIN']

        assert 'Strict-Transport-Security' in headers

    def test_no_sensitive_info_in_headers(self, app_url):
        """Ensure no sensitive information leaked in headers."""
        response = requests.get(app_url)
        headers = response.headers

        # Check for information disclosure
        assert 'Server' not in headers or 'nginx' not in headers.get('Server', '').lower()
        assert 'X-Powered-By' not in headers

class TestAuthenticationSecurity:
    """Test authentication security measures."""

    def test_login_rate_limiting(self, app_url):
        """Test rate limiting on login endpoint."""
        login_url = f"{app_url}/api/auth/login"

        # Attempt multiple failed logins
        for _ in range(10):
            response = requests.post(login_url, json={
                'username': 'test',
                'password': 'wrong'
            })

        # Should be rate limited
        assert response.status_code == 429

    def test_password_requirements(self, app_url):
        """Test password complexity requirements."""
        signup_url = f"{app_url}/api/auth/signup"

        weak_passwords = ['123', 'password', 'admin']

        for weak_pass in weak_passwords:
            response = requests.post(signup_url, json={
                'username': 'testuser',
                'password': weak_pass
            })
            assert response.status_code == 400
```

## Security Incident Response

### Vulnerability Assessment Report Template
```markdown
# Security Vulnerability Report

## Executive Summary
- **Severity**: Critical/High/Medium/Low
- **CVSS Score**: X.X
- **Affected Components**: [List components]
- **Risk Level**: [Business impact assessment]

## Technical Details
### Vulnerability Description
[Detailed technical description]

### Proof of Concept
```code
[PoC code or steps to reproduce]
```

### Impact Assessment
- **Confidentiality**: High/Medium/Low
- **Integrity**: High/Medium/Low
- **Availability**: High/Medium/Low

## Remediation Steps
1. **Immediate Actions** (0-24 hours)
2. **Short-term Fixes** (1-7 days)
3. **Long-term Solutions** (1-4 weeks)

## Prevention Measures
- Code review guidelines
- Security testing integration
- Monitoring and detection
```

## Integration с Event Management System

### Специфичные проверки для Event Management платформы:
1. **User Data Protection** - GDPR compliance для пользовательских данных
2. **Payment Security** - PCI DSS compliance для обработки платежей
3. **Event Access Control** - проверка прав доступа к событиям
4. **API Rate Limiting** - защита от злоупотреблений API
5. **File Upload Security** - безопасная загрузка изображений и документов

### Event-specific Security Patterns:
```python
# Secure event access control
def check_event_access(user, event_id):
    """Verify user has permission to access event."""
    event = Event.query.get_or_404(event_id)

    # Check if user is organizer
    if event.organizer_id == user.id:
        return True

    # Check if user has valid ticket
    ticket = Ticket.query.filter_by(
        user_id=user.id,
        event_id=event_id,
        status='valid'
    ).first()

    return ticket is not None

# Secure payment processing
def process_payment_secure(payment_data):
    """Process payment with security measures."""
    # Validate input
    if not validate_payment_data(payment_data):
        raise ValidationError("Invalid payment data")

    # Encrypt sensitive data
    encrypted_card = encrypt_pii(payment_data['card_number'])

    # Use secure payment gateway
    result = payment_gateway.process({
        'amount': payment_data['amount'],
        'currency': payment_data['currency'],
        'encrypted_card': encrypted_card,
        'idempotency_key': generate_idempotency_key()
    })

    # Log for audit (without sensitive data)
    audit_log.info(f"Payment processed: {result['transaction_id']}")

    return result
```

## Performance Security Checklist

### Build Time Security
- [ ] Dependency vulnerability scanning
- [ ] Secret scanning in code
- [ ] SAST tool integration
- [ ] License compliance check
- [ ] Container image scanning

### Runtime Security
- [ ] Security headers implementation
- [ ] Input validation on all endpoints
- [ ] Authentication/authorization checks
- [ ] Rate limiting and DDoS protection
- [ ] Monitoring and alerting setup

### Production Security
- [ ] Regular security assessments
- [ ] Penetration testing
- [ ] Security incident response plan
- [ ] Backup and recovery procedures
- [ ] Compliance audits (GDPR, PCI DSS)