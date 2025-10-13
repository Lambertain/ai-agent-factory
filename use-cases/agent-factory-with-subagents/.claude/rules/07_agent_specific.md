# 07. Специфіка агентів та матриця компетенцій

**📖 Детальна матриця:** Для повного списку типів помилок та правил ескалації див. `07_1_competency_matrix_detailed.md`

## 🧭 МАТРИЦЯ КОМПЕТЕНЦІЙ АГЕНТІВ (ШВИДКИЙ ОГЛЯД)

### Core Team Roles (Основні ролі):

**Analysis Lead:**
- Аналіз вимог та декомпозиція
- Створення user stories та acceptance criteria
- Дослідження та discovery
- Пріоритизація задач

**Blueprint Architect:**
- Проектування систем та архітектури
- Технічна архітектура та інтеграції
- Планування технологічного стеку
- Архітектурні рішення

**Implementation Engineer:**
- Розробка та написання коду
- Реалізація функціональності
- Виправлення багів
- Code reviews

**Quality Guardian:**
- Стратегії тестування
- Quality assurance
- Валідація deployment
- Перевірка якості коду

**Deployment Engineer:**
- Налаштування CI/CD
- Управління інфраструктурою
- Release management
- Налаштування моніторингу

### Specialized Agents (Спеціалізовані агенти):

**Security Audit Agent:**
- Компетенції: безпека, вразливості, compliance, аудит
- Делегує: UI/UX (accessibility), Performance (optimization)

**RAG Agent:**
- Компетенції: пошук інформації, семантичний аналіз
- Делегує: Implementation (реалізація), Analysis (дослідження)

**UI/UX Enhancement Agent:**
- Компетенції: дизайн, інтерфейс, accessibility, UX
- Делегує: Security (аудит), Performance (UI швидкість)

**Performance Optimization Agent:**
- Компетенції: оптимізація, швидкість, profiling
- Делегує: Database (SQL), Security (проблеми безпеки)

**TypeScript Architecture Agent:**
- Компетенції: типізація, архітектура, TypeScript
- Делегує: Implementation (код), Quality (тести)

**Prisma Database Agent:**
- Компетенції: база даних, SQL, Prisma, схеми
- Делегує: Security (безпека БД), Performance (оптимізація)

**PWA Mobile Agent:**
- Компетенції: PWA, мобільна розробка, offline
- Делегує: UI/UX (мобільний UX), Performance (швидкість)

**Next.js Optimization Agent:**
- Компетенції: Next.js, SSR, SSG, оптимізація
- Делегує: Performance, Security, UI/UX

## 🤝 ПРАВИЛА ДЕЛЕГУВАННЯ

### Коли делегувати:

**Security Audit Agent → інші агенти:**
- UI/UX вразливості → uiux_enhancement
- Продуктивність → performance_optimization
- Database безпека → prisma_database

**Performance Agent → інші агенти:**
- UI продуктивність → uiux_enhancement
- Database оптимізація → prisma_database
- Security проблеми → security_audit

**UI/UX Agent → інші агенти:**
- Accessibility аудит → security_audit
- Performance UI → performance_optimization
- TypeScript типи → typescript_architecture

**Будь-який агент → rag_agent:**
- Пошук документації
- Дослідження best practices
- Аналіз технічних рішень

### Логіка прийняття рішень:

**ПРАВИЛО:** Якщо задача торкається >1 області експертизи, ОБОВ'ЯЗКОВО делегуй відповідні частини.

```python
AGENT_ASSIGNEE_MAP = {
    "security_audit": "Security Audit Agent",
    "rag_agent": "Archon Analysis Lead",
    "uiux_enhancement": "Archon UI/UX Designer",
    "performance_optimization": "Performance Optimization Agent",
    "typescript_architecture": "Archon Blueprint Architect",
    "prisma_database": "Archon Implementation Engineer",
    "pwa_mobile": "Archon Implementation Engineer",
    "nextjs_optimization": "Archon Implementation Engineer"
}
```

## 🛠️ ОБОВ'ЯЗКОВІ ІНСТРУМЕНТИ АГЕНТІВ

**Кожен агент ПОВИНЕН мати:**

1. **search_agent_knowledge** - Пошук у базі знань агента
2. **break_down_to_microtasks** - Розбивка задачі на мікрозадачі
3. **report_microtask_progress** - Звітування про прогрес
4. **delegate_task_to_agent** - Делегування задач
5. **check_delegation_need** - Перевірка необхідності делегування
6. **reflect_and_improve** - Рефлексія та покращення

## 📚 ОБОВ'ЯЗКОВА БАЗА ЗНАНЬ

**Кожен спеціалізований агент ПОВИНЕН мати:**
- Файл знань: `agents/[agent_name]/knowledge/[agent_name]_knowledge.md`
- Системний промпт з експертизою ролі
- Приклади та best practices
- Інструкції з інтеграції з проектами

**Теги для Knowledge Base:**
- `[agent_name]` - ім'я агента
- `agent-knowledge` - маркер знань
- `pydantic-ai` - фреймворк
- `[domain]` - область експертизи
