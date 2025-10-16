# Module 06: Examples & Templates

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Project Manager Knowledge Base](../archon_project_manager_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Когда ОБЯЗАТЕЛЬНО читать этот модуль:**
- Нужен шаблон коммуникации
- Создание project kickoff message
- Status update для stakeholders
- Priority notification для команды
- Sprint report formatting
- Template для типичной задачи

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** шаблон, template, пример, образец, kickoff, status update, project report

**English:** template, example, sample, kickoff, status update, project report, communication

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Начало нового проекта (kickoff)
- Регулярные отчеты о статусе
- Уведомление команды об изменениях
- Формальная коммуникация со stakeholders

---

## 📋 PROJECT KICKOFF MESSAGE

### Шаблон запуска нового проекта

```markdown
🚀 **НОВЫЙ ПРОЕКТ СОЗДАН: [Project Name]**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **PROJECT INFORMATION**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project ID:** [UUID]
**Created:** [Date]
**Owner:** [Project Owner Name]

**Scope:**
[Brief 2-3 sentence description of what the project aims to achieve]

**Tech Stack:**
- Language: [Primary programming language]
- Framework: [Main framework]
- Database: [Database system]
- Infrastructure: [Cloud provider, CI/CD]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 **TEAM COMPOSITION**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Analysis Lead:** Requirements & Research
- **Blueprint Architect:** Architecture & Design
- **Implementation Engineer:** Development & Coding
- **Quality Guardian:** Testing & QA
- **Deployment Engineer:** DevOps & Release

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 **TIMELINE**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Start Date:** [YYYY-MM-DD]
**Target Completion:** [YYYY-MM-DD]
**Duration:** [X weeks/months]

**Major Milestones:**
1. [Milestone 1] - [Date]
2. [Milestone 2] - [Date]
3. [Milestone 3] - [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **OBJECTIVES & DELIVERABLES**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Key Deliverables:**
- [ ] [Deliverable 1 with clear acceptance criteria]
- [ ] [Deliverable 2 with clear acceptance criteria]
- [ ] [Deliverable 3 with clear acceptance criteria]

**Success Criteria:**
- [Measurable metric 1]
- [Measurable metric 2]
- [Measurable metric 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 **NEXT STEPS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Immediate Actions:**
1. [Action 1] - Assigned to: [Agent Name]
2. [Action 2] - Assigned to: [Agent Name]
3. [Action 3] - Assigned to: [Agent Name]

**Team:**
Пожалуйста, ознакомьтесь с requirements и подтвердите готовность к работе.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Пример реального kickoff

```
🚀 **НОВЫЙ ПРОЕКТ СОЗДАН: Payment Integration System**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **PROJECT INFORMATION**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project ID:** 7a8b9c0d-4e5f-1a2b-3c4d-5e6f7a8b9c0d
**Created:** 2025-10-16
**Owner:** Archon Team

**Scope:**
Universal payment integration system supporting Stripe, PayPal, and other providers.
Includes subscription management, webhook handling, and fraud detection.

**Tech Stack:**
- Language: Python 3.11+
- Framework: FastAPI, Pydantic AI
- Database: PostgreSQL + Redis
- Infrastructure: Docker, GitHub Actions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 **TEAM COMPOSITION**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Analysis Lead:** Requirements & API Research
- **Blueprint Architect:** Payment Architecture Design
- **Implementation Engineer:** Core Development
- **Quality Guardian:** Security & Testing
- **Deployment Engineer:** CI/CD & Monitoring

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 **TIMELINE**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Start Date:** 2025-10-16
**Target Completion:** 2025-11-15
**Duration:** 4 weeks

**Major Milestones:**
1. Stripe Integration - 2025-10-23
2. PayPal Integration - 2025-10-30
3. Subscription System - 2025-11-06
4. Production Ready - 2025-11-15

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **OBJECTIVES & DELIVERABLES**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Key Deliverables:**
- [ ] Stripe API integration with test coverage >90%
- [ ] PayPal REST API integration
- [ ] Webhook handling system with retry logic
- [ ] Subscription management (create, update, cancel)
- [ ] Payment method storage (PCI compliant)

**Success Criteria:**
- 99.9% payment processing uptime
- <2 seconds average payment processing time
- Zero security vulnerabilities
- Full PCI DSS compliance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 **NEXT STEPS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Immediate Actions:**
1. Analyze Stripe API documentation - Assigned to: Analysis Lead
2. Design payment architecture - Assigned to: Blueprint Architect
3. Set up development environment - Assigned to: Implementation Engineer

**Team:**
Пожалуйста, ознакомьтесь с requirements и подтвердите готовность к работе.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 STATUS UPDATE TEMPLATE

### Регулярный отчет о прогрессе

```markdown
📊 **СТАТУС ПРОЕКТА: [Project Name]**

**Дата:** [YYYY-MM-DD]
**Период:** [Week/Sprint number]
**Project ID:** [UUID]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ **ЗАВЕРШЕНО**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Completed item 1] - [Agent Name]
  Результат: [Brief description of result]

- [Completed item 2] - [Agent Name]
  Результат: [Brief description of result]

**Metrics:**
- Tasks completed: [X] / [Total]
- Code coverage: [X]%
- Tests passing: [X] / [Total]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 **В РАБОТЕ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Current task 1] - [Agent Name]
  Status: [X]% complete | ETA: [Date]

- [Current task 2] - [Agent Name]
  Status: [X]% complete | ETA: [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **БЛОКЕРЫ & РИСКИ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 **КРИТИЧЕСКИЕ БЛОКЕРЫ:**
- [Blocker 1 description]
  Impact: [High/Medium/Low]
  Action: [Mitigation strategy]
  Owner: [Agent Name]

⚠️ **РИСКИ:**
- [Risk 1 description]
  Probability: [High/Medium/Low]
  Mitigation: [Strategy]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 **СЛЕДУЮЩИЕ ЭТАПЫ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**This Week:**
- [ ] [Upcoming task 1] - [Agent Name] - Due: [Date]
- [ ] [Upcoming task 2] - [Agent Name] - Due: [Date]

**Next Milestone:**
[Milestone name] - Target: [Date]
Progress: [X]% complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 **OVERALL PROGRESS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Completion:** [X]%
**On Track:** [Yes/No - with explanation if No]
**Target Date:** [Still on target / Revised to: YYYY-MM-DD]
```

---

## 🔄 PRIORITY NOTIFICATION TEMPLATE

### Уведомление команды о переприоритизации

```markdown
🔄 **ПРИОРИТЕТЫ ЗАДАЧ ОБНОВЛЕНЫ**

**Дата:** [YYYY-MM-DD]
**Проект:** [Project Name]
**Триггер:** [Причина переприоритизации]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 **ПОВЫШЕН ПРИОРИТЕТ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Task #[ID]:** "[Task Title]"
  Priority: [50] → [95]
  Причина: Блокирует 3 другие задачи
  Assigned to: [Agent Name]

- **Task #[ID]:** "[Task Title]"
  Priority: [60] → [90]
  Причина: На критическом пути проекта
  Assigned to: [Agent Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📉 **ПОНИЖЕН ПРИОРИТЕТ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Task #[ID]:** "[Task Title]"
  Priority: [80] → [30]
  Причина: Не на критическом пути
  Assigned to: [Agent Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **КОНФЛИКТЫ ОБНАРУЖЕНЫ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Task #[ID] и #[ID] требуют одновременных изменений API
  Рекомендация: [Разрешение конфликта]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **РЕКОМЕНДАЦИИ**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Сначала выполните Task #[ID] ([Task Title])
2. Затем параллельно #[ID] и #[ID]
3. Task #[ID] отложить до завершения [Dependency]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Questions?** Reply to this message or contact Project Manager
```

---

## 📝 TASK CREATION EXAMPLES

### Пример хорошо описанной задачи

```python
await mcp__archon__manage_task(
    action="create",
    project_id="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
    title="Implement JWT Token Authentication",
    description="""
## Goal
Implement secure JWT-based authentication for the API.

## Acceptance Criteria
- [ ] User can login with email/password
- [ ] JWT token generated with 24h expiry
- [ ] Refresh token mechanism implemented
- [ ] Token validation middleware created
- [ ] Unit tests with 90%+ coverage
- [ ] Integration tests for auth flow

## Technical Details
- Use pyjwt library for token generation
- Store refresh tokens in Redis with 30-day expiry
- Implement rate limiting (5 failed attempts = 15 min lockout)
- Hash passwords with bcrypt (cost factor 12)

## Dependencies
- Database schema migration (Task #123) must be completed first

## Estimated Effort
3-4 hours

## Resources
- [JWT Best Practices](https://example.com/jwt-guide)
- [FastAPI Auth Tutorial](https://example.com/fastapi-auth)
    """,
    assignee="Implementation Engineer",
    status="todo",
    task_order=85,  # High priority - blocks other features
    feature="authentication"
)
```

### Пример плохо описанной задачи (НЕ ДЕЛАЙ ТАК!)

```python
# ❌ ПЛОХОЙ ПРИМЕР
await mcp__archon__manage_task(
    action="create",
    project_id="...",
    title="Fix auth",  # Слишком расплывчато
    description="Сделать авторизацию",  # Нет деталей
    assignee="Someone",  # Неясный assignee
    status="todo"
    # Нет task_order - не ясен приоритет
    # Нет feature - сложно группировать
)
```

---

## 📈 PROJECT HEALTH REPORT

### Еженедельный health check

```markdown
📈 **PROJECT HEALTH REPORT**

**Project:** [Project Name]
**Week:** [Week of YYYY-MM-DD]
**Report Date:** [YYYY-MM-DD]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **OVERALL HEALTH: [🟢 HEALTHY / 🟡 AT RISK / 🔴 CRITICAL]**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Key Metrics:**
- Velocity: [X] story points/week (Target: [Y])
- Completion Rate: [X]% (Target: 80%+)
- Blocker Count: [X] (Target: 0-2)
- Code Quality: [X]% coverage (Target: 90%+)
- Timeline: [On Track / [X] days behind]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **PROGRESS BY AREA**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Backend:**
Status: [🟢/🟡/🔴] [X]% complete
Key Tasks: [List of main backend tasks]

**Frontend:**
Status: [🟢/🟡/🔴] [X]% complete
Key Tasks: [List of main frontend tasks]

**Infrastructure:**
Status: [🟢/🟡/🔴] [X]% complete
Key Tasks: [List of infrastructure tasks]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **RISKS & ISSUES**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Active Risks:**
1. [Risk description]
   Impact: [High/Medium/Low]
   Mitigation: [Strategy]

**Blockers:**
- [Blocker 1]: [Impact and resolution plan]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 **ACTIONS NEEDED**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Action item 1] - Owner: [Name] - Due: [Date]
2. [Action item 2] - Owner: [Name] - Due: [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 **UPCOMING MILESTONES**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Milestone 1]: [Date] - [X]% complete
- [Milestone 2]: [Date] - [X]% complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚀 RELEASE NOTES TEMPLATE

### Шаблон release notes

```markdown
# Release v[X.Y.Z] - [Release Name]

**Release Date:** [YYYY-MM-DD]
**Type:** [Major / Minor / Patch]

---

## 🎯 Highlights

[2-3 sentences summarizing the most important changes in this release]

---

## ✨ New Features

- **[Feature Name]**: [Brief description]
  - [Detail 1]
  - [Detail 2]

- **[Feature Name]**: [Brief description]
  - [Detail 1]

---

## 🔧 Improvements

- **[Area]**: [Improvement description]
- **[Area]**: [Improvement description]

---

## 🐛 Bug Fixes

- Fixed: [Bug description] (#[Issue number])
- Fixed: [Bug description] (#[Issue number])

---

## 🔄 Breaking Changes

> ⚠️ **IMPORTANT:** This release contains breaking changes

- **[Change 1]**: [Description and migration path]
- **[Change 2]**: [Description and migration path]

---

## 📦 Dependencies

**Updated:**
- [Package name]: [old version] → [new version]

**Added:**
- [New package]: [version]

---

## 🔐 Security

- [Security fix description] (CVE-[number] if applicable)

---

## 📖 Documentation

- Updated: [Documentation section]
- Added: [New documentation]

---

## 🙏 Contributors

Thanks to all contributors who made this release possible:
- [Contributor 1]
- [Contributor 2]

---

## 📥 Installation

\`\`\`bash
pip install package-name==[X.Y.Z]
\`\`\`

---

## 🔗 Links

- [Full Changelog](link-to-changelog)
- [Documentation](link-to-docs)
- [Migration Guide](link-to-migration-guide)
```

---

**Навигация:**
- [← Предыдущий модуль: Agile Methodologies](05_agile_methodologies.md)
- [↑ Назад к Project Manager Knowledge Base](../archon_project_manager_knowledge.md)
- [→ Следующий модуль: Refactoring Workflow](07_refactoring_workflow.md)
