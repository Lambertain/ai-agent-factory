# Module 02: Kubernetes Orchestration

**Назад к:** [Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)

---

## 🎯 ТРИГГЕРНАЯ СИСТЕМА - Когда читать этот модуль

### Тип 1: Ключевые слова (Keywords Triggers)
**Читай этот модуль ЕСЛИ задача содержит:**
- `kubernetes`, `k8s`, `kubectl`
- `deployment`, `pod`, `service`, `ingress`
- `namespace`, `configmap`, `secret`
- `hpa`, `horizontal pod autoscaler`
- `rbac`, `service account`, `role`, `rolebinding`
- `rolling update`, `rollback`

### Тип 2: Сценарии использования (Scenario Triggers)
**Читай этот модуль КОГДА нужно:**
- Развернуть приложение в Kubernetes
- Настроить Kubernetes манифесты (Deployment, Service, Ingress)
- Создать namespace и управлять ресурсами
- Настроить автоскейлинг (HPA)
- Настроить RBAC и permissions
- Выполнить rolling update или rollback
- Настроить health probes (liveness, readiness)
- Создать Ingress для external access

### Тип 3: Технические термины (Technical Terms Triggers)
**Читай этот модуль ЕСЛИ встречаешь:**
- Kubernetes manifests (YAML)
- RollingUpdate strategy
- Liveness/Readiness probes
- Resource requests and limits
- HorizontalPodAutoscaler (HPA)
- ServiceAccount, Role, RoleBinding
- ClusterIP, NodePort, LoadBalancer
- Ingress controller (nginx)
- ConfigMap and Secret management
- Zero-downtime deployments

---

## 📋 СОДЕРЖАНИЕ МОДУЛЯ

**Основные темы:**
1. ✅ Complete Kubernetes Manifests (Namespace, ConfigMap, Secret, Deployment)
2. ✅ Service and Ingress (ClusterIP, external access, TLS)
3. ✅ HorizontalPodAutoscaler (CPU/Memory based autoscaling)
4. ✅ ServiceAccount and RBAC (permissions, least privilege)
5. ✅ Deployment Commands (apply, verify, rolling update, rollback)
6. ✅ Best Practices (resource management, health checks, security)

**Конфигурации:**
- Full Deployment manifest (replicas, strategy, probes, resources)
- Service (ClusterIP) + Ingress (nginx, TLS)
- HPA (CPU 70%, Memory 80%, scale policies)
- RBAC (ServiceAccount, Role, RoleBinding)

**Команды:**
- kubectl apply/get/describe
- Rolling update and rollback commands
- HPA management

---

## Complete Kubernetes Manifests

### Namespace and Configuration

```yaml
# ========================================
# Namespace
# ========================================
apiVersion: v1
kind: Namespace
metadata:
  name: archon-agent
  labels:
    name: archon-agent

---
# ========================================
# ConfigMap - Конфигурация приложения
# ========================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: archon-agent
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  PORT: "8000"

---
# ========================================
# Secret - Секретные данные
# ========================================
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: archon-agent
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@postgres:5432/mydb"
  LLM_API_KEY: "your-llm-api-key"
  REDIS_URL: "redis://redis:6379/0"
```

**Важно:**
- ConfigMap для неконфиденциальной конфигурации
- Secret для паролей и API ключей
- Namespace для изоляции ресурсов

---

## Deployment Configuration

```yaml
# ========================================
# Deployment - Основное приложение
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: archon-agent
  namespace: archon-agent
  labels:
    app: archon-agent
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: archon-agent
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: archon-agent
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: archon-agent-sa
      securityContext:
        fsGroup: 1000
        runAsNonRoot: true
        runAsUser: 1000

      containers:
      - name: archon-agent
        image: archon-agent:latest
        imagePullPolicy: Always

        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: LLM_API_KEY

        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: tmp
          mountPath: /tmp

      volumes:
      - name: logs
        emptyDir: {}
      - name: tmp
        emptyDir: {}
```

**Ключевые настройки:**
- ✅ RollingUpdate strategy для zero-downtime deployments
- ✅ Resource limits для стабильности
- ✅ Health probes для мониторинга
- ✅ Security context для безопасности

---

## Service and Ingress

```yaml
# ========================================
# Service - Expose приложения
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: archon-agent-service
  namespace: archon-agent
  labels:
    app: archon-agent
spec:
  type: ClusterIP
  selector:
    app: archon-agent
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: http
  sessionAffinity: None

---
# ========================================
# Ingress - Внешний доступ
# ========================================
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: archon-agent-ingress
  namespace: archon-agent
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - agent.example.com
    secretName: archon-agent-tls
  rules:
  - host: agent.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: archon-agent-service
            port:
              number: 80
```

**Важно:**
- Service для internal routing
- Ingress для external access
- TLS/SSL через cert-manager

---

## HorizontalPodAutoscaler

```yaml
# ========================================
# HorizontalPodAutoscaler - Auto-scaling
# ========================================
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: archon-agent-hpa
  namespace: archon-agent
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: archon-agent
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

**Ключевые метрики:**
- CPU utilization target: 70%
- Memory utilization target: 80%
- Scale down gradually (50% per minute)
- Scale up quickly (100% per 30s or 4 pods)

---

## ServiceAccount and RBAC

```yaml
# ========================================
# ServiceAccount
# ========================================
apiVersion: v1
kind: ServiceAccount
metadata:
  name: archon-agent-sa
  namespace: archon-agent

---
# ========================================
# Role - Permissions for ServiceAccount
# ========================================
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: archon-agent-role
  namespace: archon-agent
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

---
# ========================================
# RoleBinding - Bind Role to ServiceAccount
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

---

## Deployment Commands

### Apply Manifests

```bash
# Apply all manifests
kubectl apply -f k8s/

# Apply specific file
kubectl apply -f k8s/deployment.yaml

# Apply from directory with recursive
kubectl apply -R -f k8s/
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n archon-agent

# Check services
kubectl get svc -n archon-agent

# Check ingress
kubectl get ingress -n archon-agent

# Check HPA
kubectl get hpa -n archon-agent

# Describe deployment
kubectl describe deployment archon-agent -n archon-agent
```

### Rolling Update

```bash
# Update image
kubectl set image deployment/archon-agent \
  archon-agent=archon-agent:v2.0.0 \
  -n archon-agent

# Check rollout status
kubectl rollout status deployment/archon-agent -n archon-agent

# Rollout history
kubectl rollout history deployment/archon-agent -n archon-agent

# Rollback to previous version
kubectl rollout undo deployment/archon-agent -n archon-agent

# Rollback to specific revision
kubectl rollout undo deployment/archon-agent --to-revision=2 -n archon-agent
```

---

## Best Practices для Kubernetes

### 1. Resource Management

**Always set resource requests and limits:**
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 2. Health Checks

**Используй оба типа проб:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 3. Security

**Security best practices:**
```yaml
securityContext:
  fsGroup: 1000
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
```

### 4. Labels and Annotations

**Правильное использование:**
```yaml
labels:
  app: archon-agent
  version: v1
  environment: production
  team: archon

annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
```

### 5. ConfigMaps vs Secrets

**ConfigMaps для неконфиденциальных данных:**
```yaml
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
```

**Secrets для конфиденциальных:**
```yaml
stringData:
  DATABASE_URL: "postgresql://..."
  API_KEY: "secret-key"
```

---

**Навигация:**
- [← Предыдущий модуль: Docker & Containerization](01_docker_containerization.md)
- [↑ Назад к Deployment Engineer Knowledge Base](../deployment_engineer_knowledge.md)
- [→ Следующий модуль: CI/CD Pipelines](03_cicd_pipelines.md)
