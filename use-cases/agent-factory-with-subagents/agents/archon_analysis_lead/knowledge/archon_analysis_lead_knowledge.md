# Archon Analysis Lead Knowledge Base

## Системный промпт для Archon Analysis Lead

```
Ты главный аналитик проектов Archon - специалист по анализу требований, декомпозиции задач и планированию архитектуры. Твоя роль критически важна для успеха любого проекта.

**Твоя экспертиза:**
- Анализ и декомпозиция сложных требований на управляемые задачи
- Архитектурное планирование и проектирование систем
- Техническое исследование и оценка рисков
- Планирование ресурсов и временных рамок
- Координация между техническими и бизнес-требованиями
- Создание технических спецификаций и roadmap

**Ключевые области анализа:**

1. **Requirements Engineering:**
   - Сбор и анализ функциональных требований
   - Выявление нефункциональных требований
   - Анализ ограничений и зависимостей
   - Приоритизация требований по важности

2. **Technical Analysis:**
   - Архитектурный анализ и выбор технологий
   - Анализ производительности и масштабируемости
   - Оценка технических рисков
   - Исследование совместимости и интеграций

3. **Project Planning:**
   - Декомпозиция задач на микроуровне
   - Оценка временных затрат и сложности
   - Планирование зависимостей между задачами
   - Создание milestone и checkpoint планов

**Подход к работе:**
1. Всегда начинай с глубокого анализа требований
2. Задавай уточняющие вопросы для полного понимания
3. Разбивай сложные задачи на простые, выполнимые компоненты
4. Учитывай технические и бизнес ограничения
5. Документируй все ключевые решения и их обоснования
```

## Методологии анализа требований

### User Story Analysis
```markdown
**Шаблон анализа User Story:**

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

### Requirements Prioritization Matrix
```
| Requirement | Business Value | Technical Complexity | Risk Level | Priority |
|-------------|----------------|---------------------|------------|----------|
| Feature A   | High          | Low                 | Low        | P0       |
| Feature B   | Medium        | High                | Medium     | P1       |
| Feature C   | Low           | Medium              | High       | P2       |
```

## Архитектурный анализ

### System Architecture Analysis Framework
```python
# Шаблон архитектурного анализа
class ArchitecturalAnalysis:
    """Структура для архитектурного анализа системы."""

    def __init__(self, system_name: str):
        self.system_name = system_name
        self.components = []
        self.integrations = []
        self.non_functional_requirements = {}

    def analyze_requirements(self, requirements: List[str]) -> Dict:
        """Анализ требований для архитектурных решений."""
        analysis = {
            "functional_requirements": [],
            "non_functional_requirements": {},
            "constraints": [],
            "assumptions": []
        }

        for req in requirements:
            # Классификация требований
            if self.is_performance_requirement(req):
                analysis["non_functional_requirements"]["performance"] = req
            elif self.is_security_requirement(req):
                analysis["non_functional_requirements"]["security"] = req
            elif self.is_scalability_requirement(req):
                analysis["non_functional_requirements"]["scalability"] = req
            else:
                analysis["functional_requirements"].append(req)

        return analysis

    def design_system_architecture(self, requirements: Dict) -> Dict:
        """Проектирование архитектуры на основе требований."""
        architecture = {
            "layers": self.define_layers(requirements),
            "components": self.identify_components(requirements),
            "data_flow": self.design_data_flow(requirements),
            "integration_points": self.identify_integrations(requirements),
            "technology_stack": self.recommend_technologies(requirements)
        }
        return architecture
```

### Technology Stack Analysis
```yaml
# Критерии выбора технологий
Technology Selection Criteria:

  Backend Framework:
    - Performance: Latency < 100ms, Throughput > 1000 RPS
    - Scalability: Horizontal scaling support
    - Ecosystem: Rich library ecosystem
    - Team Expertise: Existing knowledge
    - Long-term Support: Active maintenance

  Database:
    - Data Model: Relational vs NoSQL requirements
    - ACID Requirements: Transaction consistency needs
    - Scalability: Read/Write patterns
    - Backup & Recovery: RTO/RPO requirements

  Frontend:
    - User Experience: Responsive, accessible
    - Performance: Bundle size, loading speed
    - SEO Requirements: Server-side rendering needs
    - Browser Support: Target browser matrix
```

## Декомпозиция задач

### Task Breakdown Structure (TBS)
```
Project: [Название проекта]
├── 1. Analysis & Design
│   ├── 1.1 Requirements Analysis
│   ├── 1.2 System Design
│   └── 1.3 Technical Specifications
├── 2. Foundation
│   ├── 2.1 Project Setup
│   ├── 2.2 Infrastructure Setup
│   └── 2.3 Development Environment
├── 3. Core Implementation
│   ├── 3.1 Backend Development
│   ├── 3.2 Frontend Development
│   └── 3.3 Database Implementation
├── 4. Integration & Testing
│   ├── 4.1 Component Integration
│   ├── 4.2 System Testing
│   └── 4.3 Performance Testing
└── 5. Deployment & Monitoring
    ├── 5.1 Production Deployment
    ├── 5.2 Monitoring Setup
    └── 5.3 Documentation
```

### Estimation Techniques
```python
# Planning Poker для оценки сложности
STORY_POINTS = {
    1: "Очень простая задача, 1-2 часа",
    2: "Простая задача, полдня",
    3: "Стандартная задача, день",
    5: "Средняя задача, 2-3 дня",
    8: "Сложная задача, неделя",
    13: "Очень сложная, требует декомпозиции",
    21: "Эпик, необходимо разбить на stories"
}

# Three-Point Estimation
def estimate_effort(optimistic, realistic, pessimistic):
    """PERT оценка: (O + 4R + P) / 6"""
    return (optimistic + 4 * realistic + pessimistic) / 6

# Example:
# Optimistic: 2 days, Realistic: 5 days, Pessimistic: 10 days
# PERT Estimate: (2 + 4*5 + 10) / 6 = 5.33 days
```

## Паттерны анализа для AI Agent Factory

### AI Agent Requirements Analysis
```markdown
# AI Agent Analysis Template

## Agent Purpose & Scope
**Primary Function:** [основная функция агента]
**Target Domain:** [область применения]
**User Personas:** [кто будет использовать]
**Success Metrics:** [как измерить успех]

## Functional Requirements
### Core Capabilities:
- [ ] **Input Processing:** [типы входных данных]
- [ ] **Data Processing:** [логика обработки]
- [ ] **Output Generation:** [формат результатов]
- [ ] **Error Handling:** [обработка ошибок]

### Integration Requirements:
- [ ] **APIs:** [внешние API для интеграции]
- [ ] **Data Sources:** [источники данных]
- [ ] **Authentication:** [требования безопасности]
- [ ] **Monitoring:** [метрики и логирование]

## Non-Functional Requirements
**Performance:**
- Response Time: < [время] ms
- Throughput: > [количество] requests/second
- Accuracy: > [процент]% correct responses

**Scalability:**
- Concurrent Users: [количество]
- Data Volume: [объем данных]
- Geographic Distribution: [регионы]

**Reliability:**
- Uptime: [процент]%
- Error Rate: < [процент]%
- Recovery Time: < [время]
```

### Pydantic AI Specific Analysis
```python
# Анализ архитектуры Pydantic AI агента
class PydanticAgentAnalysis:
    """Анализ требований для Pydantic AI агента."""

    @staticmethod
    def analyze_agent_requirements(description: str) -> Dict:
        """Анализ требований к агенту на основе описания."""
        return {
            "agent_type": "conversational|tool_using|data_processing",
            "model_requirements": {
                "provider": "openai|anthropic|google|local",
                "model_size": "small|medium|large",
                "context_length": "4k|8k|32k|128k",
                "cost_optimization": True
            },
            "tools_needed": [],
            "dependencies": [],
            "complexity": "low|medium|high"
        }

    @staticmethod
    def design_agent_architecture(requirements: Dict) -> Dict:
        """Проектирование архитектуры агента."""
        return {
            "components": {
                "agent.py": "Основной агент с промптами",
                "tools.py": "Инструменты и функции",
                "settings.py": "Конфигурация и настройки",
                "dependencies.py": "Dependency injection",
                "providers.py": "LLM провайдеры"
            },
            "data_models": "Pydantic модели для валидации",
            "error_handling": "Обработка ошибок и retry логика",
            "testing_strategy": "Unit и integration тесты"
        }
```

## Risk Analysis Framework

### Technical Risk Assessment
```
Risk Category | Impact | Probability | Mitigation Strategy
-------------|---------|-------------|-------------------
Technology Lock-in | High | Medium | Use standard APIs, avoid vendor-specific features
Performance Bottlenecks | High | Medium | Early prototyping, load testing
Integration Complexity | Medium | High | API documentation, sandbox testing
Skills Gap | Medium | Low | Training plan, knowledge transfer
Security Vulnerabilities | High | Low | Security review, penetration testing
```

### Decision Matrix
```python
# Матрица принятия решений
class DecisionMatrix:
    """Матрица для принятия архитектурных решений."""

    def __init__(self, criteria: List[str], weights: List[float]):
        self.criteria = criteria
        self.weights = weights

    def evaluate_options(self, options: Dict[str, List[float]]) -> Dict:
        """Оценка вариантов по критериям."""
        scores = {}
        for option, values in options.items():
            weighted_score = sum(v * w for v, w in zip(values, self.weights))
            scores[option] = weighted_score
        return scores

# Пример использования:
# criteria = ["Performance", "Cost", "Maintainability", "Scalability"]
# weights = [0.3, 0.2, 0.3, 0.2]
# options = {
#     "Option A": [8, 6, 9, 7],
#     "Option B": [9, 4, 7, 9],
#     "Option C": [7, 9, 8, 6]
# }
```

## Шаблоны документации

### Technical Specification Template
```markdown
# Technical Specification: [Project Name]

## 1. Executive Summary
**Project:** [название]
**Objective:** [цель проекта]
**Timeline:** [временные рамки]
**Budget:** [ресурсы]

## 2. Requirements Analysis
### 2.1 Functional Requirements
[детальный список функциональных требований]

### 2.2 Non-Functional Requirements
[производительность, безопасность, масштабируемость]

### 2.3 Constraints
[технические и бизнес ограничения]

## 3. System Architecture
### 3.1 High-Level Architecture
[диаграмма архитектуры]

### 3.2 Component Design
[детальное описание компонентов]

### 3.3 Data Flow
[описание потоков данных]

## 4. Implementation Plan
### 4.1 Task Breakdown
[декомпозиция на задачи]

### 4.2 Timeline
[временные рамки по этапам]

### 4.3 Resource Allocation
[распределение ресурсов]

## 5. Risk Analysis
[анализ рисков и план митигации]

## 6. Success Criteria
[критерии успеха и метрики]
```

## Best Practices для Analysis Lead

### 1. Effective Requirements Gathering
- **Ask "Why"**: Понимай бизнес-логику за каждым требованием
- **Use Examples**: Конкретные примеры использования
- **Document Assumptions**: Явно фиксируй все предположения
- **Validate Early**: Раннее подтверждение понимания с заказчиком

### 2. Quality Analysis Checklist
- [ ] Все требования SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] Нет противоречащих требований
- [ ] Учтены все stakeholders
- [ ] Определены критерии приемки
- [ ] Оценены риски и зависимости

### 3. Communication Patterns
- **Structured Updates**: Регулярные статус репорты
- **Visual Documentation**: Диаграммы и схемы для сложных концепций
- **Collaborative Reviews**: Включай команду в процесс анализа
- **Change Management**: Процедуры для управления изменениями

### 4. Tools & Techniques
- **Mind Mapping**: Для исследования требований
- **User Journey Mapping**: Понимание пользовательского опыта
- **Impact/Effort Matrix**: Приоритизация задач
- **SWOT Analysis**: Анализ сильных/слабых сторон решения