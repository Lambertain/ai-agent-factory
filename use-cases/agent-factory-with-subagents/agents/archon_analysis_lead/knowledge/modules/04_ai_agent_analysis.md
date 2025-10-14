# Module 04: AI Agent Analysis & Pydantic AI Patterns

**Назад к:** [Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)

---

## AI Agent Requirements Analysis Template

### Шаблон анализа AI агента

```markdown
# AI Agent Analysis: [Название агента]

## 1. Agent Purpose & Scope
**Primary Function:** [основная функция агента]
**Target Domain:** [область применения - e.g., customer support, data analysis, content generation]
**User Personas:** [кто будет использовать - developers, end-users, business analysts]
**Success Metrics:**
- Response accuracy: > 95%
- Average response time: < 3 seconds
- User satisfaction: > 4.5/5
- Cost per request: < $0.05

## 2. Functional Requirements

### Core Capabilities:
- [ ] **Input Processing:**
  - Text input: Natural language queries
  - File uploads: PDF, CSV, JSON
  - API requests: REST/GraphQL
  - Max input length: 10,000 tokens

- [ ] **Data Processing:**
  - Query understanding: Intent classification
  - Context management: Conversation history (last 10 messages)
  - Response generation: Structured output (Pydantic models)
  - Error handling: Graceful degradation with fallbacks

- [ ] **Output Generation:**
  - Format: JSON, Markdown, Plain text
  - Streaming: Support for SSE (Server-Sent Events)
  - Citations: Include sources for factual claims
  - Confidence scoring: 0-100% confidence in response

- [ ] **Error Handling:**
  - Invalid input → Helpful error message with examples
  - Rate limiting → Queue request or reject with retry info
  - API failures → Fallback to cached responses or alternative models
  - Timeout → Partial response with continuation token

### Integration Requirements:
- [ ] **APIs:**
  - External APIs: Weather, Maps, Payment gateways
  - Authentication: OAuth2, API keys
  - Rate limiting: 100 requests/minute per user

- [ ] **Data Sources:**
  - Vector database: Pinecone/Weaviate for RAG
  - SQL database: PostgreSQL for structured data
  - Cache layer: Redis for frequently accessed data
  - File storage: S3 for document uploads

- [ ] **Authentication:**
  - User authentication: JWT tokens
  - API key management: Encrypted storage
  - Role-based access: Admin, User, Guest

- [ ] **Monitoring:**
  - Metrics: Request count, latency, error rate
  - Logging: Structured logs with correlation IDs
  - Alerting: PagerDuty for critical errors
  - Dashboards: Grafana for real-time monitoring

## 3. Non-Functional Requirements

**Performance:**
- Response Time: < 3s (P95), < 5s (P99)
- Throughput: > 100 requests/second
- Accuracy: > 95% correct responses on benchmark
- Token efficiency: < 500 tokens per response average

**Scalability:**
- Concurrent Users: 1,000 simultaneous users
- Data Volume: 100M documents in vector DB
- Geographic Distribution: Multi-region deployment (US, EU, APAC)

**Reliability:**
- Uptime: 99.9% (8.76 hours downtime/year)
- Error Rate: < 1% of requests
- Recovery Time: < 5 minutes (automated failover)

**Cost Optimization:**
- Model selection: Use smaller models for simple queries
- Caching: 70% cache hit rate for common queries
- Token optimization: Compress prompts, use system messages efficiently
- Target cost: < $1,000/month for 100K requests

## 4. Agent Behavior Design

**Personality & Tone:**
- Professional and helpful
- Concise but thorough
- Admits uncertainty ("I'm not sure, but...")
- Provides sources and citations

**Conversation Patterns:**
- Multi-turn conversations: Maintain context
- Clarifying questions: Ask when input is ambiguous
- Progressive disclosure: Start with summary, offer details
- Graceful exits: "Is there anything else I can help with?"

**Safety & Ethics:**
- Content filtering: No harmful, offensive, or illegal content
- Bias mitigation: Diverse training data, regular audits
- Privacy: No PII in logs, GDPR compliant
- Transparency: Disclose AI limitations
```

---

## Pydantic AI Specific Analysis

### Анализ требований для Pydantic AI агента

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PydanticAgentRequirements(BaseModel):
    """Модель требований для Pydantic AI агента."""

    agent_name: str = Field(..., description="Название агента")
    agent_type: str = Field(..., description="conversational | tool_using | data_processing | hybrid")

    model_requirements: ModelRequirements
    tools_needed: List[ToolRequirement]
    dependencies: List[str]
    complexity: str = Field(..., description="low | medium | high")

class ModelRequirements(BaseModel):
    """Требования к LLM модели."""

    provider: str = Field(..., description="openai | anthropic | google | local")
    model_size: str = Field(..., description="small | medium | large")
    context_length: str = Field(..., description="4k | 8k | 32k | 128k")
    cost_optimization: bool = Field(default=True)

    # Дополнительные параметры
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0, le=4096)
    streaming: bool = Field(default=False)

    def estimate_cost_per_request(self) -> float:
        """Оценка стоимости одного запроса."""
        # Примерные цены (USD per 1M tokens)
        pricing = {
            "openai": {
                "gpt-4": 0.03,
                "gpt-3.5-turbo": 0.002
            },
            "anthropic": {
                "claude-3-opus": 0.015,
                "claude-3-sonnet": 0.003,
                "claude-3-haiku": 0.00025
            },
            "google": {
                "gemini-pro": 0.0005
            }
        }

        base_cost = pricing.get(self.provider, {}).get(self.model_size, 0.01)
        avg_tokens = self.max_tokens * 0.7  # Средний расход токенов
        return (avg_tokens / 1_000_000) * base_cost

class ToolRequirement(BaseModel):
    """Требования к инструменту агента."""

    tool_name: str
    tool_type: str = Field(..., description="api | database | file_system | computation")
    description: str
    required: bool = Field(default=True)
    dependencies: List[str] = Field(default_factory=list)

    # Параметры производительности
    max_execution_time: int = Field(default=30, description="Максимальное время выполнения в секундах")
    retry_strategy: Optional[str] = Field(default=None, description="exponential_backoff | fixed_delay")

class PydanticAgentAnalyzer:
    """Анализатор требований для Pydantic AI агента."""

    @staticmethod
    def analyze_agent_requirements(description: str) -> PydanticAgentRequirements:
        """Анализ требований к агенту на основе описания.

        Args:
            description: Текстовое описание назначения агента

        Returns:
            Структурированные требования
        """
        # Определение типа агента
        agent_type = "conversational"
        if "tool" in description.lower() or "api" in description.lower():
            agent_type = "tool_using"
        elif "analyze" in description.lower() or "process" in description.lower():
            agent_type = "data_processing"

        # Оценка сложности
        complexity = "medium"
        if len(description.split()) < 50:
            complexity = "low"
        elif "integrate" in description.lower() or "complex" in description.lower():
            complexity = "high"

        # Подбор модели
        model_reqs = ModelRequirements(
            provider="anthropic",
            model_size="medium",
            context_length="32k",
            cost_optimization=True
        )

        if complexity == "low":
            model_reqs.model_size = "small"
            model_reqs.context_length = "8k"
        elif complexity == "high":
            model_reqs.model_size = "large"
            model_reqs.context_length = "128k"

        return PydanticAgentRequirements(
            agent_name="Generated Agent",
            agent_type=agent_type,
            model_requirements=model_reqs,
            tools_needed=[],
            dependencies=[],
            complexity=complexity
        )

    @staticmethod
    def design_agent_architecture(requirements: PydanticAgentRequirements) -> Dict:
        """Проектирование архитектуры агента на основе требований.

        Returns:
            Словарь с компонентами архитектуры
        """
        architecture = {
            "components": {
                "agent.py": "Основной агент с промптами и логикой",
                "tools.py": "Инструменты и функции для агента",
                "settings.py": "Конфигурация и настройки",
                "dependencies.py": "Dependency injection для сервисов",
                "providers.py": "LLM провайдеры и их конфигурация"
            },
            "data_models": {
                "input_schema": "Pydantic модель для валидации входных данных",
                "output_schema": "Pydantic модель для структурированного вывода",
                "context_schema": "Модель для сохранения контекста разговора"
            },
            "error_handling": {
                "retry_logic": "Exponential backoff для API вызовов",
                "fallback_models": "Резервные модели при недоступности основной",
                "graceful_degradation": "Partial responses при timeout"
            },
            "testing_strategy": {
                "unit_tests": "Тестирование tools и utility функций",
                "integration_tests": "Тестирование агента с mock LLM",
                "e2e_tests": "Полный flow с реальными API (staging)"
            },
            "monitoring": {
                "metrics": ["request_count", "latency", "token_usage", "error_rate"],
                "logging": "Structured JSON logs с correlation IDs",
                "alerting": "Alerts для error_rate > 5% или latency > 10s"
            }
        }

        # Добавить специфичные компоненты для tool-using агентов
        if requirements.agent_type == "tool_using":
            architecture["components"]["tool_registry.py"] = "Регистрация и управление инструментами"
            architecture["components"]["tool_executor.py"] = "Безопасное выполнение инструментов"

        # Добавить специфичные компоненты для data-processing агентов
        if requirements.agent_type == "data_processing":
            architecture["components"]["data_loader.py"] = "Загрузка и предобработка данных"
            architecture["components"]["data_validator.py"] = "Валидация входных/выходных данных"

        return architecture
```

---

## Agent Capability Matrix

### Матрица возможностей AI агентов

```python
from enum import Enum
from typing import List, Dict
from dataclasses import dataclass

class AgentCapability(Enum):
    """Основные возможности AI агентов."""
    TEXT_GENERATION = "text_generation"
    QUESTION_ANSWERING = "question_answering"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    IMAGE_UNDERSTANDING = "image_understanding"
    FUNCTION_CALLING = "function_calling"
    MULTI_TURN_CONVERSATION = "multi_turn_conversation"
    RAG = "retrieval_augmented_generation"
    STRUCTURED_OUTPUT = "structured_output"
    STREAMING = "streaming_responses"

@dataclass
class AgentCapabilitySpec:
    """Спецификация возможности агента."""
    capability: AgentCapability
    required: bool
    complexity: str  # low | medium | high
    implementation_notes: str
    estimated_tokens: int  # Средний расход токенов
    examples: List[str]

class AgentCapabilityAnalyzer:
    """Анализатор возможностей агента."""

    @staticmethod
    def analyze_required_capabilities(use_cases: List[str]) -> List[AgentCapabilitySpec]:
        """Определить необходимые возможности на основе use cases.

        Args:
            use_cases: Список сценариев использования

        Returns:
            Список спецификаций возможностей
        """
        capabilities = []

        # Анализ каждого use case
        for use_case in use_cases:
            lower_case = use_case.lower()

            # Text Generation
            if any(keyword in lower_case for keyword in ["generate", "write", "create text"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.TEXT_GENERATION,
                    required=True,
                    complexity="medium",
                    implementation_notes="Use structured prompts with few-shot examples",
                    estimated_tokens=500,
                    examples=["Generate product descriptions", "Write email templates"]
                ))

            # Question Answering
            if any(keyword in lower_case for keyword in ["answer", "explain", "what is"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.QUESTION_ANSWERING,
                    required=True,
                    complexity="low",
                    implementation_notes="Direct prompting with context",
                    estimated_tokens=300,
                    examples=["Answer customer support questions", "Explain technical concepts"]
                ))

            # Code Generation
            if any(keyword in lower_case for keyword in ["code", "function", "script"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.CODE_GENERATION,
                    required=True,
                    complexity="high",
                    implementation_notes="Use code-specific models or fine-tuned variants",
                    estimated_tokens=1000,
                    examples=["Generate Python functions", "Create SQL queries"]
                ))

            # Function Calling
            if any(keyword in lower_case for keyword in ["api", "tool", "execute", "action"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.FUNCTION_CALLING,
                    required=True,
                    complexity="high",
                    implementation_notes="Implement Pydantic AI tools with proper error handling",
                    estimated_tokens=400,
                    examples=["Call weather API", "Execute database queries"]
                ))

            # RAG
            if any(keyword in lower_case for keyword in ["search", "knowledge base", "documents"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.RAG,
                    required=True,
                    complexity="high",
                    implementation_notes="Vector DB + embedding model + reranking",
                    estimated_tokens=1500,
                    examples=["Search company docs", "Answer from knowledge base"]
                ))

            # Multi-turn Conversation
            if any(keyword in lower_case for keyword in ["conversation", "chat", "follow-up"]):
                capabilities.append(AgentCapabilitySpec(
                    capability=AgentCapability.MULTI_TURN_CONVERSATION,
                    required=True,
                    complexity="medium",
                    implementation_notes="Maintain conversation history, use context window efficiently",
                    estimated_tokens=800,
                    examples=["Customer support chat", "Interview assistant"]
                ))

        # Remove duplicates
        unique_capabilities = {cap.capability: cap for cap in capabilities}
        return list(unique_capabilities.values())

    @staticmethod
    def estimate_total_cost(capabilities: List[AgentCapabilitySpec],
                          requests_per_day: int = 1000) -> Dict[str, float]:
        """Оценка общей стоимости использования агента.

        Args:
            capabilities: Список возможностей агента
            requests_per_day: Количество запросов в день

        Returns:
            Словарь с оценками стоимости
        """
        # Средний расход токенов на запрос
        avg_tokens = sum(cap.estimated_tokens for cap in capabilities) / len(capabilities)

        # Стоимость (примерная для GPT-4)
        cost_per_1m_tokens = 0.03  # $30 за 1M tokens
        daily_tokens = avg_tokens * requests_per_day
        daily_cost = (daily_tokens / 1_000_000) * cost_per_1m_tokens

        return {
            "avg_tokens_per_request": round(avg_tokens),
            "daily_tokens": int(daily_tokens),
            "daily_cost_usd": round(daily_cost, 2),
            "monthly_cost_usd": round(daily_cost * 30, 2),
            "yearly_cost_usd": round(daily_cost * 365, 2)
        }


# Пример использования
use_cases = [
    "Answer customer support questions",
    "Search through company documentation",
    "Generate code snippets for common tasks",
    "Execute API calls to fetch data",
    "Maintain multi-turn conversations"
]

analyzer = AgentCapabilityAnalyzer()
capabilities = analyzer.analyze_required_capabilities(use_cases)

print("Необходимые возможности агента:\n")
for cap in capabilities:
    print(f"✓ {cap.capability.value}")
    print(f"  Complexity: {cap.complexity}")
    print(f"  Tokens: ~{cap.estimated_tokens}/request")
    print(f"  Implementation: {cap.implementation_notes}")
    print(f"  Examples: {', '.join(cap.examples[:2])}\n")

cost_estimate = analyzer.estimate_total_cost(capabilities, requests_per_day=1000)
print("\nОценка стоимости (1000 запросов/день):")
print(f"Средний расход токенов: {cost_estimate['avg_tokens_per_request']}/request")
print(f"Месячная стоимость: ${cost_estimate['monthly_cost_usd']}")
print(f"Годовая стоимость: ${cost_estimate['yearly_cost_usd']}")
```

---

## Agent Evaluation Framework

### Фреймворк оценки качества агента

```python
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class EvaluationMetric:
    """Метрика для оценки агента."""
    name: str
    target_value: float  # Целевое значение
    current_value: float  # Текущее значение
    unit: str  # Единица измерения
    weight: float  # Вес метрики (сумма весов = 1.0)

class AgentEvaluator:
    """Оценщик качества AI агента."""

    @staticmethod
    def evaluate_agent(metrics: List[EvaluationMetric]) -> Tuple[float, Dict]:
        """Оценить общее качество агента.

        Args:
            metrics: Список метрик для оценки

        Returns:
            Tuple[overall_score, detailed_results]
        """
        detailed_results = {}
        weighted_score = 0.0

        for metric in metrics:
            # Процент достижения целевого значения
            achievement = (metric.current_value / metric.target_value) * 100
            achievement = min(achievement, 100)  # Cap at 100%

            # Взвешенный вклад в общий score
            contribution = (achievement / 100) * metric.weight
            weighted_score += contribution

            detailed_results[metric.name] = {
                "target": metric.target_value,
                "current": metric.current_value,
                "achievement": f"{achievement:.1f}%",
                "unit": metric.unit,
                "contribution": f"{contribution:.2f}"
            }

        overall_score = weighted_score * 100  # Convert to percentage

        return round(overall_score, 2), detailed_results


# Пример использования
metrics = [
    EvaluationMetric(
        name="Response Accuracy",
        target_value=95.0,  # 95%
        current_value=92.5,  # 92.5%
        unit="%",
        weight=0.30
    ),
    EvaluationMetric(
        name="Response Time",
        target_value=3.0,  # 3 seconds target
        current_value=2.5,  # 2.5 seconds current
        unit="seconds",
        weight=0.20
    ),
    EvaluationMetric(
        name="User Satisfaction",
        target_value=4.5,  # 4.5/5 stars
        current_value=4.2,  # 4.2/5 stars
        unit="/5",
        weight=0.25
    ),
    EvaluationMetric(
        name="Cost Efficiency",
        target_value=0.05,  # $0.05 per request target
        current_value=0.04,  # $0.04 per request current
        unit="$ per request",
        weight=0.15
    ),
    EvaluationMetric(
        name="Token Efficiency",
        target_value=500,  # 500 tokens target
        current_value=450,  # 450 tokens current
        unit="tokens",
        weight=0.10
    )
]

evaluator = AgentEvaluator()
overall_score, results = evaluator.evaluate_agent(metrics)

print(f"Общая оценка агента: {overall_score}/100\n")
print("Детальные результаты:\n")

for metric_name, result in results.items():
    print(f"{metric_name}:")
    print(f"  Target: {result['target']} {result['unit']}")
    print(f"  Current: {result['current']} {result['unit']}")
    print(f"  Achievement: {result['achievement']}")
    print(f"  Contribution to score: {result['contribution']}\n")

# Определение grade
if overall_score >= 90:
    grade = "A (Excellent)"
elif overall_score >= 80:
    grade = "B (Good)"
elif overall_score >= 70:
    grade = "C (Acceptable)"
else:
    grade = "D (Needs Improvement)"

print(f"Grade: {grade}")
```

---

**Навигация:**
- [← Предыдущий модуль: Task Breakdown & Estimation](03_task_breakdown_estimation.md)
- [↑ Назад к Analysis Lead Knowledge Base](../archon_analysis_lead_knowledge.md)
- [→ Следующий модуль: Risk & Documentation](05_risk_documentation.md)
