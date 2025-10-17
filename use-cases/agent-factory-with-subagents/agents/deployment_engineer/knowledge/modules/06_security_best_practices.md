# Module 06: Security & Best Practices

**Назад к:** [Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)

---

## 🎯 ТРИГГЕРНАЯ СИСТЕМА - Когда читать этот модуль

### Тип 1: Ключевые слова (Keywords Triggers)
**Читай этот модуль ЕСЛИ задача содержит:**
- `security`, `hardening`, `secure`, `vulnerability`
- `rbac`, `role`, `rolebinding`, `service account`
- `network policy`, `ingress`, `egress`
- `secrets`, `sealed secrets`, `external secrets`
- `tls`, `ssl`, `certificate`, `cert-manager`
- `trivy`, `scanning`, `vulnerability scanning`
- `compliance`, `audit`, `cis benchmark`
- `pod security`, `security context`

### Тип 2: Сценарии использования (Scenario Triggers)
**Читай этот модуль КОГДА нужно:**
- Настроить Network Policies для ограничения трафика
- Зашифровать Kubernetes secrets (SealedSecrets)
- Настроить TLS/SSL для приложения (Cert-Manager)
- Провести vulnerability scanning (Trivy)
- Настроить RBAC с минимальными правами (least privilege)
- Настроить Pod Security Standards (restricted)
- Создать Security Context для контейнеров
- Настроить External Secrets Operator (AWS Secrets Manager)
- Провести CIS Kubernetes Benchmark аудит
- Настроить runtime security (Falco)
- Подписать Docker образы (Cosign)
- Создать Pre-Deployment Security Checklist

### Тип 3: Технические термины (Technical Terms Triggers)
**Читай этот модуль ЕСЛИ встречаешь:**
- NetworkPolicy (ingress/egress rules, podSelector)
- SealedSecrets (kubeseal encryption)
- External Secrets Operator (AWS Secrets Manager integration)
- Pod Security Standards (restricted, baseline, privileged)
- Security Context (runAsNonRoot, readOnlyRootFilesystem, allowPrivilegeEscalation)
- Trivy vulnerability scanning (HIGH, CRITICAL severities)
- Cert-Manager (ClusterIssuer, Certificate, Let's Encrypt)
- RBAC least privilege (Role, RoleBinding)
- CIS Kubernetes Benchmark (kube-bench)
- Falco runtime security (custom rules)
- Cosign image signing/verification
- Defense in Depth strategy
- Zero Trust Security principles

---

## 📋 СОДЕРЖАНИЕ МОДУЛЯ

**Основные темы:**
1. ✅ Security Hardening (Network Policies для ограничения трафика)
2. ✅ Secrets Management (SealedSecrets, External Secrets Operator)
3. ✅ Pod Security Standards (restricted policy, Security Context)
4. ✅ TLS/SSL Configuration (Cert-Manager, Let's Encrypt)
5. ✅ Vulnerability Scanning (Trivy для Docker и Kubernetes)
6. ✅ RBAC Best Practices (least privilege, audit logging)
7. ✅ Image Security (Cosign signing/verification)
8. ✅ Compliance and Auditing (CIS Kubernetes Benchmark, Falco)
9. ✅ Security Checklist (Pre-Deployment Checklist)
10. ✅ Best Practices Summary (Defense in Depth, Zero Trust, Security Automation)

**Конфигурации:**
- Network Policies (ingress/egress restrictions, DNS, external HTTPS)
- SealedSecrets (encrypted secrets для git)
- External Secrets Operator (AWS Secrets Manager)
- Pod Security Context (runAsNonRoot, readOnlyRootFilesystem, capabilities drop)
- Cert-Manager (ClusterIssuer для Let's Encrypt)
- RBAC Roles (минимальные permissions)
- Falco Rules (unauthorized processes, sensitive file access)

**Инструменты:**
- Trivy (vulnerability scanning)
- kubeseal (SealedSecrets encryption)
- Cert-Manager (automated TLS/SSL)
- kube-bench (CIS Benchmark)
- Falco (runtime security)
- Cosign (image signing)

---

## Security Hardening

### Kubernetes Network Policies

```yaml
# ========================================
# Network Policy - Restrict Ingress Traffic
# ========================================
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: archon-agent-netpol
  namespace: archon-agent
spec:
  podSelector:
    matchLabels:
      app: archon-agent
  policyTypes:
    - Ingress
    - Egress

  # Разрешить входящий трафик только от ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8000

  # Разрешить исходящий трафик
  egress:
    # Доступ к базе данных
    - to:
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432

    # Доступ к Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379

    # DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
        - podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53

    # External HTTPS
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 443
```

---

## Secrets Management

### Sealed Secrets for Kubernetes

```yaml
# ========================================
# SealedSecret - Encrypted Secret
# ========================================
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: archon-agent
spec:
  encryptedData:
    DATABASE_URL: AgBX8f9...encrypted...
    LLM_API_KEY: AgCY3k2...encrypted...
    REDIS_URL: AgDZ7m1...encrypted...
```

**Команды для создания SealedSecret:**
```bash
# Установка kubeseal
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-0.24.0-linux-amd64.tar.gz
tar xfz kubeseal-0.24.0-linux-amd64.tar.gz
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

# Создание обычного secret
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=LLM_API_KEY="sk-..." \
  --dry-run=client -o yaml > secret.yaml

# Шифрование secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Применение зашифрованного secret
kubectl apply -f sealed-secret.yaml
```

### External Secrets Operator

```yaml
# ========================================
# SecretStore - AWS Secrets Manager
# ========================================
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: archon-agent
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: archon-agent-sa

---
# ========================================
# ExternalSecret - Ссылка на AWS Secret
# ========================================
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: archon-agent
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore

  target:
    name: app-secrets
    creationPolicy: Owner

  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: archon/database/url
    - secretKey: LLM_API_KEY
      remoteRef:
        key: archon/llm/api-key
```

---

## Pod Security Standards

### Pod Security Policy (Deprecated) → Pod Security Standards

```yaml
# ========================================
# Namespace с Pod Security Standards
# ========================================
apiVersion: v1
kind: Namespace
metadata:
  name: archon-agent
  labels:
    # Enforce restricted policy
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Restricted Policy Requirements:**
- Запрет запуска контейнеров с root
- Обязательная изоляция capabilities
- Запрет hostPath volumes
- Запрет hostNetwork, hostPID, hostIPC
- Read-only root filesystem

### Security Context Best Practices

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      # Pod-level security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: app:latest

        # Container-level security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
              - ALL
            add:
              - NET_BIND_SERVICE

        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

---

## TLS/SSL Configuration

### Cert-Manager for Automatic Certificates

```yaml
# ========================================
# ClusterIssuer - Let's Encrypt Production
# ========================================
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx

---
# ========================================
# Certificate - Автоматический SSL
# ========================================
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: archon-agent-tls
  namespace: archon-agent
spec:
  secretName: archon-agent-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: agent.example.com
  dnsNames:
    - agent.example.com
    - www.agent.example.com
```

---

## Vulnerability Scanning

### Trivy Container Scanning

```bash
# ========================================
# Сканирование Docker образа
# ========================================
trivy image --severity HIGH,CRITICAL archon-agent:latest

# Сканирование с выводом в JSON
trivy image --format json --output results.json archon-agent:latest

# Сканирование Kubernetes кластера
trivy k8s --report summary cluster

# Сканирование конкретного namespace
trivy k8s --report summary namespace archon-agent

# Сканирование с игнорированием unfixed vulnerabilities
trivy image --ignore-unfixed archon-agent:latest
```

### Automated Scanning in CI/CD

```yaml
# GitHub Actions - Trivy Scan
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'archon-agent:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload Trivy results to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'

# Fail build on critical vulnerabilities
- name: Fail on critical vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'archon-agent:${{ github.sha }}'
    exit-code: '1'
    severity: 'CRITICAL'
```

---

## RBAC Best Practices

### Least Privilege Principle

```yaml
# ========================================
# Role - Минимальные разрешения
# ========================================
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: archon-agent-role
  namespace: archon-agent
rules:
# Только чтение ConfigMaps и Secrets
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]

# Только чтение информации о Pods
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

# Только чтение Services
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list"]

---
# ========================================
# RoleBinding
# ========================================
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: archon-agent-rolebinding
  namespace: archon-agent
subjects:
- kind: ServiceAccount
  name: archon-agent-sa
  namespace: archon-agent
roleRef:
  kind: Role
  name: archon-agent-role
  apiGroup: rbac.authorization.k8s.io
```

### Audit Logging

```yaml
# ========================================
# Audit Policy
# ========================================
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  # Логировать все запросы на метаданные
  - level: RequestResponse
    resources:
    - group: ""
      resources: ["secrets", "configmaps"]

  # Логировать изменения RBAC
  - level: RequestResponse
    verbs: ["create", "update", "patch", "delete"]
    resources:
    - group: "rbac.authorization.k8s.io"

  # Не логировать чтение статуса
  - level: None
    verbs: ["get", "list", "watch"]
    resources:
    - group: ""
      resources: ["events"]
```

---

## Image Security

### Image Signing and Verification

```bash
# ========================================
# Cosign - Подпись образов
# ========================================

# Генерация ключей
cosign generate-key-pair

# Подпись образа
cosign sign --key cosign.key archon-agent:latest

# Верификация образа
cosign verify --key cosign.pub archon-agent:latest
```

### Image Policy Webhook

```yaml
# ========================================
# ImagePolicy - Принудительная проверка подписей
# ========================================
apiVersion: v1
kind: AdmissionConfiguration
plugins:
- name: ImagePolicyWebhook
  configuration:
    imagePolicy:
      kubeConfigFile: /etc/kubernetes/imagepolicy/kubeconfig
      allowTTL: 50
      denyTTL: 50
      retryBackoff: 500
      defaultAllow: false
```

---

## Compliance and Auditing

### CIS Kubernetes Benchmark

```bash
# ========================================
# kube-bench - CIS Benchmark Scanning
# ========================================

# Запуск на master node
kube-bench master

# Запуск на worker node
kube-bench node

# Вывод в JSON
kube-bench --json

# Проверка конкретной секции
kube-bench --section 1.2
```

### Falco - Runtime Security

```yaml
# ========================================
# Falco Rules - Custom Security Rules
# ========================================
- rule: Unauthorized Process in Container
  desc: Detect unauthorized processes running in container
  condition: >
    spawned_process and
    container and
    not proc.name in (authorized_processes)
  output: >
    Unauthorized process started in container
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING

- rule: Sensitive File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    fd.name in (sensitive_files) and
    not proc.name in (authorized_readers)
  output: >
    Sensitive file accessed
    (user=%user.name file=%fd.name proc=%proc.name)
  priority: CRITICAL
```

---

## Security Checklist

### Pre-Deployment Checklist

```markdown
## Docker Security
- [ ] Multi-stage builds используются
- [ ] Образы не содержат секретов
- [ ] Используется non-root пользователь
- [ ] Образ прошел vulnerability scanning
- [ ] Включен health check

## Kubernetes Security
- [ ] RBAC настроен с минимальными правами
- [ ] Network Policies применены
- [ ] Pod Security Standards enforced
- [ ] Secrets не в plain text
- [ ] Resource limits установлены

## Application Security
- [ ] TLS/SSL включен
- [ ] Аутентификация настроена
- [ ] Логирование включено
- [ ] Rate limiting настроен
- [ ] Input validation реализована

## Monitoring & Alerting
- [ ] Prometheus собирает метрики
- [ ] Алерты настроены
- [ ] Логи централизованы
- [ ] Audit logging включен
- [ ] SLI/SLO определены
```

---

## Best Practices Summary

### 1. Defense in Depth

**Многослойная защита:**
- Network layer (Network Policies)
- Pod layer (Security Context)
- Container layer (Non-root, Read-only FS)
- Application layer (Authentication, Authorization)

### 2. Zero Trust Security

**Принципы Zero Trust:**
- Verify explicitly
- Use least privilege access
- Assume breach

### 3. Security Automation

**Автоматизация безопасности:**
- Automated vulnerability scanning
- Policy-as-Code enforcement
- Continuous compliance monitoring
- Automated secret rotation

---

**Навигация:**
- [← Предыдущий модуль: Monitoring & Observability](05_monitoring_observability.md)
- [↑ Назад к Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)
