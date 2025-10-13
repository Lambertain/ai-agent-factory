# 07.1. Детальна матриця компетенцій агентів

**Призначення:** Розширена матриця з типами помилок для кожного агента та правилами ескалації.

**Використання:** Агенти використовують цю матрицю для визначення чи помилка в їхній компетенції.

---

## 🎯 Core Team Agents - Детальні Компетенції

### Analysis Lead

**✅ В КОМПЕТЕНЦІЇ:**
- Аналіз вимог та декомпозиція
- Створення user stories та acceptance criteria
- Дослідження та discovery
- Пріоритизація задач
- Бізнес-логіка та процеси
- User flow та journey mapping
- Requirement документація

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Технічна реалізація коду → `Implementation Engineer`
- Архітектурні рішення → `Blueprint Architect`
- Налаштування інфраструктури → `Deployment Engineer`
- Написання тестів → `Quality Guardian`
- Database дизайн → `Prisma Database Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Неточні вимоги | "Функція створення користувача не враховує edge cases" | Виправити документацію вимог |
| Некоректні user stories | "User story не має acceptance criteria" | Доповнити story |
| Відсутня бізнес-логіка | "Процес оплати не документований" | Створити документацію |
| Conflict у requirements | "Requirement A суперечить requirement B" | Вирішити конфлікт |

---

### Blueprint Architect

**✅ В КОМПЕТЕНЦІЇ:**
- Проектування систем та архітектури
- Технічна архітектура та інтеграції
- Планування технологічного стеку
- Архітектурні рішення
- Design patterns та best practices
- Масштабованість та performance архітектура
- Вибір технологій та інструментів
- System design документація

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Конкретна реалізація коду → `Implementation Engineer`
- Написання тестів → `Quality Guardian`
- Налаштування CI/CD → `Deployment Engineer`
- TypeScript специфічні деталі → `TypeScript Architecture Agent`
- Database схеми та оптимізація → `Prisma Database Agent`
- Security аудит → `Security Audit Agent`
- UI/UX дизайн → `UI/UX Enhancement Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Архітектурний антипаттерн | "God Object - клас робить занадто багато" | Розділити на модулі |
| Проблема інтеграції | "Микросервіси не мають proper API contract" | Створити API specification |
| Порушення SOLID | "Tight coupling між модулями" | Рефакторити з DI |
| Масштабованість | "Single point of failure в архітектурі" | Додати redundancy |
| Performance design | "N+1 query pattern в архітектурі" | Переглянути data flow |

---

### Implementation Engineer

**✅ В КОМПЕТЕНЦІЇ:**
- Розробка та написання коду (Python, JavaScript/TypeScript, Go, Java)
- Реалізація функціональності згідно з вимогами
- Виправлення багів в коді
- Code reviews та рефакторинг
- TypeScript/JavaScript помилки типізації (базові)
- Python помилки синтаксису та логіки
- API endpoint реалізація
- Frontend компоненти (React, Vue, Next.js, Angular)
- Backend сервіси (FastAPI, Express, NestJS)
- Git операції та merge conflicts

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Архітектурні рішення → `Blueprint Architect`
- Database оптимізація (SQL tuning) → `Prisma Database Agent`
- Security вразливості (XSS, SQL injection) → `Security Audit Agent`
- UI/UX дизайн та accessibility → `UI/UX Enhancement Agent`
- Performance profiling та optimization → `Performance Optimization Agent`
- Infrastructure та DevOps → `Deployment Engineer`
- Complex TypeScript types → `TypeScript Architecture Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| TypeScript compile error | `Property 'email' does not exist on type 'User'` | Додати поле до інтерфейсу |
| JavaScript runtime error | `Cannot read property 'x' of undefined` | Додати null check |
| Python syntax error | `IndentationError: unexpected indent` | Виправити відступи |
| Missing import | `NameError: name 'os' is not defined` | Додати import |
| Null pointer | `TypeError: Cannot read properties of null` | Додати валідацію |
| Function signature | `Expected 2 arguments, but got 3` | Виправити виклик функції |
| HTTP status codes | `Returning 200 OK for error case` | Повернути правильний статус |
| Async/await errors | `Unhandled promise rejection` | Додати try/catch |

---

### Quality Guardian

**✅ В КОМПЕТЕНЦІЇ:**
- Стратегії тестування (unit, integration, e2e)
- Quality assurance
- Валідація deployment
- Перевірка якості коду
- Написання тестів (pytest, jest, vitest, playwright)
- Test coverage аналіз
- QA автоматизація
- CI/CD test integration
- Test data management
- Flaky test debugging

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Виправлення багів в production коді → `Implementation Engineer`
- Архітектурні зміни → `Blueprint Architect`
- Performance оптимізація → `Performance Optimization Agent`
- Security penetration testing → `Security Audit Agent`
- Infrastructure testing → `Deployment Engineer`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Missing tests | `Function createUser() has no unit tests` | Написати unit tests |
| Low test coverage | `Coverage: 45% (required: 80%)` | Додати тести |
| Failing tests | `Test 'should create user' failed` | Проаналізувати та виправити тест |
| Wrong assertions | `expect(user.id).toBe(undefined)` | Виправити assertion |
| Flaky tests | `Test passes 80% of time` | Виявити race condition |
| Test environment | `Tests fail only in CI` | Налаштувати test environment |

---

### Deployment Engineer

**✅ В КОМПЕТЕНЦІЇ:**
- Налаштування CI/CD (GitHub Actions, GitLab CI, Jenkins)
- Управління інфраструктурою (Docker, Kubernetes, AWS, GCP, Azure)
- Release management
- Налаштування моніторингу (Prometheus, Grafana, Datadog)
- Environment configuration (.env, secrets management)
- Deployment pipelines
- Load balancing та scaling
- Backup та disaster recovery

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Виправлення багів в application коді → `Implementation Engineer`
- Database схеми та migrations → `Prisma Database Agent`
- Application performance tuning → `Performance Optimization Agent`
- Security vulnerabilities в коді → `Security Audit Agent`
- Test writing → `Quality Guardian`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| CI/CD failure | `GitHub Action failed: npm build error` | Налаштувати правильну node version |
| Docker build error | `COPY failed: stat package.json: not found` | Виправити Dockerfile context |
| Kubernetes error | `CrashLoopBackOff: container failed to start` | Перевірити лог і ресурси |
| Missing env var | `Error: DATABASE_URL is not defined` | Додати змінну в secrets |
| Infrastructure config | `Terraform apply failed: invalid region` | Виправити конфігурацію |
| Deployment timeout | `Deployment exceeded 10 minutes` | Збільшити timeout або оптимізувати |

---

## 🔧 Specialized Agents - Детальні Компетенції

### Security Audit Agent

**✅ В КОМПЕТЕНЦІЇ:**
- Виявлення security вразливостей (XSS, CSRF, SQL injection)
- Code security review
- Dependency vulnerability scanning
- Authentication/Authorization review
- Compliance audit (GDPR, SOC2)
- Secrets management review
- Security best practices

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- UI/UX accessibility → `UI/UX Enhancement Agent`
- Performance optimization → `Performance Optimization Agent`
- Database optimization → `Prisma Database Agent`
- Implementation fixes → `Implementation Engineer`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| XSS vulnerability | `innerHTML = userInput` (не санітизовано) | Ескалація до `Implementation Engineer` з рекомендацією |
| SQL injection | `query = "SELECT * FROM users WHERE id=" + userId` | Ескалація до `Implementation Engineer` |
| Weak authentication | `Passwords stored in plain text` | Ескалація до `Implementation Engineer` |
| Secrets in code | `.env файл закомічений в git` | Ескалація до `Deployment Engineer` |

---

### Prisma Database Agent

**✅ В КОМПЕТЕНЦІЇ:**
- Database schema design
- Prisma schema creation
- Database migrations
- SQL query optimization
- N+1 query detection
- Index optimization
- Database performance tuning
- Data modeling

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Application code bugs → `Implementation Engineer`
- Security vulnerabilities → `Security Audit Agent`
- Infrastructure setup → `Deployment Engineer`
- TypeScript types → `TypeScript Architecture Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| N+1 query problem | `SELECT executed 1000+ times in loop` | Додати `include` в Prisma query |
| Missing index | `Full table scan on 1M rows` | Додати index в schema |
| Schema issue | `Relation missing @relation attribute` | Виправити schema.prisma |
| Migration error | `Migration failed: column already exists` | Виправити migration file |
| Slow query | `Query takes 5+ seconds` | Оптимізувати query з JOIN |

---

### UI/UX Enhancement Agent

**✅ В КОМПЕТЕНЦІЇ:**
- UI/UX design improvements
- Accessibility (WCAG compliance)
- User interface component design
- Responsive design
- Mobile optimization
- User experience research
- Design systems

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Implementation code → `Implementation Engineer`
- Performance optimization → `Performance Optimization Agent`
- Security audit → `Security Audit Agent`
- Backend logic → `Implementation Engineer`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Accessibility issue | `Button missing aria-label` | Ескалація до `Implementation Engineer` |
| Responsive bug | `Layout breaks on mobile` | Ескалація до `Implementation Engineer` |
| UX problem | `Confusing navigation flow` | Створити дизайн рекомендацію |
| Missing feedback | `No loading state on button` | Ескалація до `Implementation Engineer` |

---

### Performance Optimization Agent

**✅ В КОМПЕТЕНЦІЇ:**
- Performance profiling
- Code optimization
- Bundle size optimization
- Memory leak detection
- CPU usage optimization
- Caching strategies
- Load time optimization

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Database query tuning → `Prisma Database Agent`
- Security fixes → `Security Audit Agent`
- Infrastructure scaling → `Deployment Engineer`
- UI rendering (без performance контексту) → `UI/UX Enhancement Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Memory leak | `Memory usage grows over time` | Виявити leak source → ескалація до `Implementation Engineer` |
| Slow rendering | `Component re-renders 100+ times/sec` | Ескалація до `Implementation Engineer` з рекомендацією useMemo |
| Large bundle | `main.js is 5MB uncompressed` | Ескалація до `Implementation Engineer` для code splitting |
| Unnecessary API calls | `Same endpoint called 50 times` | Ескалація до `Implementation Engineer` для кешування |

---

### TypeScript Architecture Agent

**✅ В КОМПЕТЕНЦІЇ:**
- Complex TypeScript types design
- Type safety improvements
- Generic types и utility types
- TypeScript configuration (tsconfig.json)
- Type inference optimization
- Advanced type patterns

**❌ ПОЗА КОМПЕТЕНЦІЄЮ:**
- Runtime bugs → `Implementation Engineer`
- Business logic → `Implementation Engineer`
- Architecture decisions → `Blueprint Architect`
- Performance → `Performance Optimization Agent`

**🐛 ТИПИ ПОМИЛОК В КОМПЕТЕНЦІЇ:**
| Тип помилки | Приклад | Дія |
|-------------|---------|-----|
| Complex type error | `Type instantiation is excessively deep` | Спростити type structure |
| Type inference issue | `Parameter implicitly has 'any' type` | Додати explicit type annotation |
| Generic constraint | `Type 'T' does not satisfy constraint` | Виправити generic bounds |
| Utility type misuse | `Incorrect use of Omit<>` | Ескалація до `Implementation Engineer` |

---

## 🔄 ШВИДКИЙ ДОВІДНИК ЕСКАЛАЦІЇ

**Типи помилок → Відповідальний агент:**

| Тип помилки | Агент |
|-------------|-------|
| TypeScript syntax, basic types | Implementation Engineer |
| Complex TypeScript types | TypeScript Architecture Agent |
| Python/JavaScript syntax | Implementation Engineer |
| SQL query optimization | Prisma Database Agent |
| N+1 query problem | Prisma Database Agent |
| XSS, CSRF, SQL injection | Security Audit Agent |
| Missing tests | Quality Guardian |
| CI/CD pipeline | Deployment Engineer |
| Docker/Kubernetes | Deployment Engineer |
| Slow rendering, memory leaks | Performance Optimization Agent |
| Accessibility (WCAG) | UI/UX Enhancement Agent |
| Architecture antipattern | Blueprint Architect |
| Unclear requirements | Analysis Lead |

---

**Версія:** 1.0
**Дата створення:** 2025-10-13
**Автор:** Archon Blueprint Architect
**Призначення:** Детальний довідник для CompetencyChecker утиліти
