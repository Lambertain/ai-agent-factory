# Шаблоны для создания Pydantic AI агентов

Эти шаблоны помогают создавать универсальные агенты для работы в ролях экспертов.

## 🎯 Что такое агент?

**Агент = Роль эксперта для Claude**

Когда вы создаёте агента, вы создаёте:
- **Системный промпт роли** — контекст для переключения в экспертизу
- **Базу знаний роли** — специализированная информация, примеры, best practices
- **Инструменты роли** — помощники для выполнения специфичных задач
- **Конфигурацию роли** — настройки для адаптации под разные проекты

**ВАЖНО**: Агенты НЕ работают автономно. Это роли, которые принимает Claude для качественной работы в специализации.

## 📁 Структура шаблонов

```
templates/
├── template_tools.py          # Инструменты для роли
├── template_dependencies.py   # Конфигурация роли
├── template_prompts.py        # Системные промпты роли
└── README.md                  # Эта документация
```

## 🚀 Как создать нового агента

### Шаг 1: Определите роль

Решите какую роль эксперта вы создаёте:
- **Security Expert** — аудит безопасности, уязвимости
- **Performance Expert** — оптимизация производительности
- **UI/UX Expert** — дизайн интерфейсов, usability
- **Payment Expert** — интеграция платёжных систем
- **Database Expert** — проектирование схем БД

### Шаг 2: Скопируйте шаблоны

```bash
# Создайте директорию агента
mkdir -p agents/[agent_name]

# Скопируйте шаблоны
cp templates/template_tools.py agents/[agent_name]/tools.py
cp templates/template_dependencies.py agents/[agent_name]/dependencies.py
cp templates/template_prompts.py agents/[agent_name]/prompts.py
```

### Шаг 3: Заполните промпты роли

В `prompts.py` замените:

```python
# ❌ БЫЛО (шаблон):
SYSTEM_PROMPT = """
Ты — [EXPERT_ROLE], специализирующийся на [DOMAIN_AREA].
...
"""

# ✅ СТАЛО (реальная роль):
SYSTEM_PROMPT = """
Ты — Security Expert, специализирующийся на аудите безопасности веб-приложений.

## 🎯 Твоя экспертиза:

**Основная специализация:**
- Поиск уязвимостей: OWASP Top 10, injection attacks
- Code review: проверка кода на security issues
- Compliance: GDPR, SOC2, PCI-DSS требования
...
"""
```

**Ключевые секции промпта:**
1. **Экспертиза** — что знает эта роль
2. **Рабочий процесс** — как работать в роли
3. **Критерии качества** — стандарты роли
4. **Доступные инструменты** — что можно использовать
5. **Частые ошибки** — что избегать

### Шаг 4: Настройте зависимости

В `dependencies.py` укажите:

```python
# Имя агента
AGENT_NAME = "security_audit"  # ✅ Конкретное имя

# Теги для RAG поиска
DEFAULT_KNOWLEDGE_TAGS = [
    "security",              # ✅ Специализация
    "agent-knowledge",       # ✅ Маркер
    "pydantic-ai",          # ✅ Фреймворк
    "security-audit"        # ✅ Специфика
]

# Специфичные настройки роли
@dataclass
class SecurityAuditDependencies:
    # ... базовые поля ...

    # ✅ Добавьте специфичные настройки
    scan_depth: str = "comprehensive"
    compliance_standards: List[str] = field(
        default_factory=lambda: ["OWASP", "CWE", "GDPR"]
    )
```

### Шаг 5: Создайте инструменты роли

В `tools.py` реализуйте специализированные инструменты:

```python
# ✅ Пример для Security Expert
async def scan_for_vulnerabilities(
    ctx: RunContext,
    code_path: str,
    scan_type: str = "full"
) -> str:
    """Сканирование кода на уязвимости."""
    # Реализация специфичная для роли
    ...

# ✅ Пример для Performance Expert
async def profile_performance(
    ctx: RunContext,
    endpoint: str,
    metrics: List[str]
) -> str:
    """Профилирование производительности."""
    # Реализация специфичная для роли
    ...
```

### Шаг 6: Создайте базу знаний

Создайте файл `agents/[agent_name]/knowledge/[agent_name]_knowledge.md`:

```markdown
# Security Expert Knowledge Base

## Системный промпт роли
[Скопируйте из prompts.py]

## Best Practices

### OWASP Top 10 Проверки
1. **Injection Attacks**
   ```typescript
   // ❌ Уязвимый код
   db.query(`SELECT * FROM users WHERE id = ${userId}`)

   // ✅ Безопасный код
   db.query('SELECT * FROM users WHERE id = ?', [userId])
   ```

### Security Headers
```typescript
export const securityHeaders = {
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Strict-Transport-Security': 'max-age=31536000'
}
```

## Примеры аудита

### Пример 1: Проверка аутентификации
[Детальный пример]

### Пример 2: Валидация input
[Детальный пример]
```

## 📋 Чеклист создания агента

- [ ] **Определена роль** — ясная специализация эксперта
- [ ] **Заполнены промпты** — системный промпт с контекстом роли
- [ ] **Настроены зависимости** — knowledge_tags, специфичные настройки
- [ ] **Созданы инструменты** — минимум 3-4 специализированных функции
- [ ] **Создана база знаний** — файл `knowledge/[agent]_knowledge.md`
- [ ] **Загружены знания в Archon** — через http://localhost:3737/
- [ ] **Добавлены примеры** — минимум 3 реальных примера в базе знаний
- [ ] **Протестирована роль** — попробуйте переключиться и работать в роли

## 🎭 Как использовать агента

### Переключение в роль

```python
from agents.security_audit.prompts import get_system_prompt
from agents.security_audit.dependencies import SecurityAuditDependencies
from agents.security_audit import tools

# 1. Создаём зависимости роли
deps = SecurityAuditDependencies(
    api_key="...",
    project_type="e-commerce",  # Адаптация под тип проекта
    framework="Next.js"          # Адаптация под фреймворк
)

# 2. Получаем промпт с учетом контекста
system_prompt = get_system_prompt(
    project_type=deps.project_type,
    framework=deps.framework
)

# 3. Создаём агента с промптом роли
agent = Agent(
    get_llm_model(),
    deps_type=SecurityAuditDependencies,
    system_prompt=system_prompt
)

# 4. Добавляем инструменты роли
@agent.tool
async def search_knowledge(ctx, query):
    return await tools.search_agent_knowledge(ctx, query)

@agent.tool
async def scan_vulnerabilities(ctx, code_path):
    return await tools.scan_for_vulnerabilities(ctx, code_path)

# 5. Работаем в роли
result = await agent.run(
    "Проверь безопасность этого API endpoint",
    deps=deps
)
```

### Поиск в базе знаний роли

Во время работы в роли используйте инструмент поиска:

```python
# Claude в роли Security Expert ищет в своей базе знаний
result = await search_agent_knowledge(
    ctx,
    query="OWASP injection prevention"
)
# Находит примеры и best practices из security_knowledge.md
```

## 🌐 Принципы универсальности

**КАЖДЫЙ агент должен быть универсальным:**

### ✅ ПРАВИЛЬНО:

```python
# Адаптируется под любой проект
@dataclass
class PaymentDependencies:
    project_type: str = "universal"  # e-commerce, saas, etc
    supported_providers: List[str] = field(
        default_factory=lambda: ["stripe", "paypal"]
    )
```

### ❌ НЕПРАВИЛЬНО:

```python
# Привязан к конкретному проекту
@dataclass
class PaymentDependencies:
    unipark_api_key: str  # ❌ Проект-специфично!
    unipark_colors: Dict  # ❌ Hardcoded!
```

## 🔧 Доступные инструменты шаблона

Каждый агент автоматически получает:

1. **search_agent_knowledge** — поиск в базе знаний роли
2. **analyze_task_as_expert** — анализ с точки зрения экспертизы
3. **apply_expert_solution** — применение best practices роли
4. **check_quality_standards** — проверка по стандартам роли

Добавьте свои специализированные инструменты!

## 📚 Примеры готовых агентов

Изучите существующие агенты как примеры:

- `agents/security_audit/` — аудит безопасности
- `agents/performance_optimization/` — оптимизация производительности
- `agents/uiux_enhancement/` — улучшение UI/UX
- `agents/prisma_database/` — проектирование БД

## 🤝 Вклад в развитие

При создании нового агента:

1. Следуйте структуре шаблонов
2. Создавайте подробную базу знаний
3. Добавьте минимум 3 реальных примера
4. Убедитесь в универсальности (0% проект-специфичного кода)
5. Загрузите знания в Archon Knowledge Base

---

**ПОМНИТЕ**: Агенты — это роли для Claude, не автономные системы.
Качественная база знаний = качественная работа в роли.
