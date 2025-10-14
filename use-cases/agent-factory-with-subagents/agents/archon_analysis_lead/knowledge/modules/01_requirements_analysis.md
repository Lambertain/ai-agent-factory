# Module 01: Requirements Analysis & User Story Engineering

**Назад к:** [Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)

---

## User Story Analysis

### Шаблон анализа User Story

```markdown
## User Story: [Название]
**As a** [тип пользователя]
**I want** [функция/возможность]
**So that** [бизнес-ценность]

### Acceptance Criteria:
- [ ] Критерий 1: [детальное описание]
- [ ] Критерий 2: [детальное описание]
- [ ] Критерий 3: [детальное описание]

### Technical Analysis:
**Dependencies:** [список зависимостей]
**Complexity:** [Low/Medium/High]
**Effort:** [Story Points или часы]
**Risks:** [технические риски]

### Task Breakdown:
1. **Design Phase:** [задачи дизайна]
2. **Implementation:** [задачи разработки]
3. **Testing:** [задачи тестирования]
4. **Integration:** [задачи интеграции]
```

### Когда использовать:
- При получении новых требований от stakeholders
- Для структурирования функциональных требований
- При планировании спринтов и релизов
- Для коммуникации с командой разработки

---

## Requirements Prioritization Matrix

### Матрица приоритизации

| Requirement | Business Value | Technical Complexity | Risk Level | Priority |
|-------------|----------------|---------------------|------------|----------|
| Feature A   | High          | Low                 | Low        | P0       |
| Feature B   | Medium        | High                | Medium     | P1       |
| Feature C   | Low           | Medium              | High       | P2       |

### Критерии оценки

**Business Value:**
- **High**: Критично для бизнеса, прямое влияние на revenue
- **Medium**: Важно для пользователей, улучшает UX
- **Low**: Nice-to-have, опциональная функциональность

**Technical Complexity:**
- **High**: > 13 story points, требует исследования и сложной архитектуры
- **Medium**: 5-8 story points, стандартная разработка с известными решениями
- **Low**: 1-3 story points, простая имплементация

**Risk Level:**
- **High**: Новые технологии, интеграции, security concerns
- **Medium**: Известные технологии, но сложная логика
- **Low**: Стандартные паттерны, проверенные решения

**Priority Levels:**
- **P0**: Критично, блокирует релиз
- **P1**: Важно, нужно для релиза
- **P2**: Желательно, можно в следующем релизе
- **P3**: Backlog, low priority

---

## SMART Requirements Framework

### Критерии качественных требований

**S - Specific (Конкретные)**
```
❌ Плохо: "Система должна быть быстрой"
✅ Хорошо: "API должен возвращать ответ за < 200ms для 95% запросов"
```

**M - Measurable (Измеримые)**
```
❌ Плохо: "Высокая доступность системы"
✅ Хорошо: "Uptime 99.9% (не более 8.76 часов downtime в год)"
```

**A - Achievable (Достижимые)**
```
❌ Плохо: "Обработка 1 млн транзакций/сек на одном сервере"
✅ Хорошо: "Обработка 10к транзакций/сек с горизонтальным масштабированием"
```

**R - Relevant (Релевантные)**
```
❌ Плохо: "Добавить blockchain в простое CRUD приложение"
✅ Хорошо: "Использовать PostgreSQL для транзакционных данных"
```

**T - Time-bound (Ограниченные во времени)**
```
❌ Плохо: "Реализовать аутентификацию когда-нибудь"
✅ Хорошо: "Реализовать OAuth2 аутентификацию в Sprint 3 (14 дней)"
```

---

## Requirements Elicitation Techniques

### 1. Stakeholder Interviews

**Цель**: Глубокое понимание бизнес-требований

**Ключевые вопросы:**
- "Какую проблему мы решаем?"
- "Кто основные пользователи системы?"
- "Каковы критерии успеха проекта?"
- "Какие ограничения (бюджет, время, технологии)?"

**Best Practices:**
- Записывать все обсуждения
- Использовать примеры из реальной жизни
- Фокусироваться на "why", не только "what"
- Подтверждать понимание повторением

### 2. User Journey Mapping

**Цель**: Визуализация пользовательского опыта

```
User Journey: Online Shopping

1. Discovery → 2. Selection → 3. Checkout → 4. Payment → 5. Confirmation

Touchpoints:
- Landing page
- Product catalog
- Shopping cart
- Payment gateway
- Order confirmation email

Pain Points:
- Сложная навигация по каталогу
- Долгая загрузка страниц
- Непонятный процесс checkout
```

### 3. Use Case Analysis

**Структура Use Case:**

```markdown
**Use Case:** Оформление заказа

**Actors:**
- Покупатель (Primary)
- Платежная система (Secondary)

**Preconditions:**
- Пользователь залогинен
- Корзина содержит минимум 1 товар

**Main Flow:**
1. Пользователь переходит на страницу checkout
2. Система отображает сводку заказа
3. Пользователь выбирает способ доставки
4. Пользователь вводит адрес доставки
5. Пользователь выбирает способ оплаты
6. Система инициирует платеж через Payment Gateway
7. Payment Gateway подтверждает успешную оплату
8. Система создает заказ и отправляет confirmation email

**Alternative Flows:**
- 7a. Платеж отклонен → показать ошибку и предложить другой способ
- 8a. Email не доставлен → сохранить для повторной отправки

**Postconditions:**
- Заказ создан в системе
- Платеж обработан
- Покупатель получил confirmation
```

---

## Acceptance Criteria Best Practices

### Given-When-Then Format (BDD Style)

```gherkin
Feature: User Authentication

Scenario: Successful login with valid credentials
  Given I am on the login page
  And I have a registered account
  When I enter valid email "user@example.com"
  And I enter valid password "SecurePass123"
  And I click the "Login" button
  Then I should be redirected to the dashboard
  And I should see welcome message "Welcome, John Doe"
  And session token should be stored in cookies

Scenario: Failed login with invalid password
  Given I am on the login page
  When I enter valid email "user@example.com"
  And I enter invalid password "WrongPass"
  And I click the "Login" button
  Then I should see error message "Invalid credentials"
  And I should remain on the login page
  And no session token should be created
```

### Checklist Format

```markdown
## Acceptance Criteria: Payment Processing

### Функциональные требования:
- [ ] Поддержка Visa, Mastercard, AmEx
- [ ] 3D Secure валидация для карт
- [ ] Автоматический retry при временных ошибках (до 3 попыток)
- [ ] Webhook для асинхронных обновлений статуса платежа

### Безопасность:
- [ ] PCI DSS compliance - не хранить CVV
- [ ] Шифрование данных карты в transit (TLS 1.3)
- [ ] Токенизация чувствительных данных
- [ ] Rate limiting: максимум 5 попыток оплаты в 10 минут

### Производительность:
- [ ] Обработка платежа < 3 секунд (P95)
- [ ] Поддержка 100 concurrent платежей
- [ ] Graceful degradation при недоступности Payment Gateway

### UX/UI:
- [ ] Валидация номера карты в реальном времени
- [ ] Понятные сообщения об ошибках
- [ ] Loading состояние во время обработки
- [ ] Автосохранение данных при ошибке сети
```

---

**Навигация:**
- [↑ Назад к Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)
- [→ Следующий модуль: Architecture & Technology Analysis](02_architecture_technology.md)
