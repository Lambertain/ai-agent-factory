"""
NLP Content Research Agent

Универсальный агент для профессиональных исследований с NLP специализацией.
Поддерживает любые домены: психология, астрология, таро, нумерология и др.

Использует методологию PatternShift v2.0 для создания высоковирусного контента.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
from datetime import datetime

from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field

from .dependencies import (
from ..common import check_pm_switch
    NLPContentResearchDependencies,
    create_research_dependencies,
    create_psychology_research_dependencies,
    create_astrology_research_dependencies,
    create_universal_research_dependencies,
    ResearchDomain,
    NLPTechnique,
    AudienceType
)
from .settings import load_settings
from .prompts import get_system_prompt, get_task_specific_prompt
from .tools import (
    search_agent_knowledge,
    conduct_web_research,
    analyze_viral_potential,
    conduct_competitor_analysis,
    generate_content_brief,
    break_down_to_microtasks,
    delegate_research_task,
    ResearchQuery,
    ViralAnalysisRequest,
    CompetitorAnalysisRequest
)


# === МОДЕЛИ ЗАПРОСОВ ===

class ResearchRequest(BaseModel):
    """Основной запрос на исследование."""
    topic: str = Field(description="Тема исследования")
    domain: str = Field(default="psychology", description="Домен исследования")
    research_type: str = Field(default="comprehensive", description="Тип исследования")
    target_audience: str = Field(default="general_public", description="Целевая аудитория")
    focus_areas: List[str] = Field(default=[], description="Области фокуса")
    nlp_techniques: List[str] = Field(default=[], description="Конкретные NLP техники")
    enable_viral_analysis: bool = Field(default=True, description="Включить анализ вирусности")
    enable_competitor_analysis: bool = Field(default=True, description="Включить конкурентный анализ")
    output_format: str = Field(default="research_brief", description="Формат вывода")


class QuickInsightRequest(BaseModel):
    """Быстрый запрос на инсайты."""
    topic: str = Field(description="Тема для анализа")
    insight_type: str = Field(default="pain_points", description="Тип инсайтов")


class ContentOptimizationRequest(BaseModel):
    """Запрос на NLP оптимизацию контента."""
    content: str = Field(description="Исходный контент")
    target_audience: str = Field(default="general", description="Целевая аудитория")
    optimization_goals: List[str] = Field(default=["engagement"], description="Цели оптимизации")
    nlp_techniques: List[str] = Field(default=[], description="Применяемые техники")


# === ОСНОВНОЙ АГЕНТ ===

def create_nlp_content_research_agent(
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> Agent[NLPContentResearchDependencies, str]:
    """
    Создать универсальный NLP Content Research Agent.

    Args:
        dependencies: Зависимости агента

    Returns:
        Экземпляр агента
    """
    # Загружаем зависимости по умолчанию если не предоставлены
    if dependencies is None:
        settings = load_settings()
        dependencies = NLPContentResearchDependencies(
            api_key=settings.llm_api_key,
            research_domain=ResearchDomain(settings.research_domain),
            target_audience=AudienceType(settings.target_audience),
            primary_nlp_techniques=[NLPTechnique(t) for t in settings.primary_nlp_techniques],
            enable_web_search=settings.enable_web_search,
            enable_competitive_analysis=settings.enable_competitive_analysis,
            enable_viral_content_analysis=settings.enable_viral_content_analysis
        )

    # Получаем модель для агента
    model = _get_llm_model(dependencies)

    # Создаем системный промпт
    system_prompt = get_system_prompt(dependencies)

    # Создаем агента
    agent = Agent(
        model=model,
        deps_type=NLPContentResearchDependencies,
        system_prompt=system_prompt
    )

    # Регистрируем все инструменты
    _register_agent_tools(agent)

    return agent


def _get_llm_model(deps: NLPContentResearchDependencies):
    """Получить оптимальную модель для исследований."""
    try:
        settings = load_settings()

        # Для исследовательских задач используем cost-optimized модели
        model_name = settings.get_model_for_task("research")

        if "gemini" in model_name.lower():
            # Используем Gemini для дешевых исследовательских задач
            if hasattr(settings, 'gemini_api_key') and settings.gemini_api_key:
                provider = GeminiProvider(api_key=settings.gemini_api_key)
                return GeminiModel(model_name, provider=provider)

        # Fallback на основную модель
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)

    except Exception as e:
        # Emergency fallback
        provider = OpenAIProvider(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=deps.api_key
        )
        return OpenAIModel("qwen2.5-coder-32b-instruct", provider=provider)


def _register_agent_tools(agent: Agent):
    """Регистрация всех инструментов агента."""
    # Основные исследовательские инструменты
    agent.tool(search_agent_knowledge)
    agent.tool(conduct_web_research)
    agent.tool(analyze_viral_potential)
    agent.tool(conduct_competitor_analysis)
    agent.tool(generate_content_brief)

    # Коллективные инструменты
    agent.tool(break_down_to_microtasks)
    agent.tool(delegate_research_task)


# === ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР ===

# Функция создания агента - создается по запросу
def get_nlp_content_research_agent():
    """Получить экземпляр NLP Content Research Agent."""
    return create_nlp_content_research_agent()


# === ОСНОВНЫЕ ФУНКЦИИ ===

async def conduct_comprehensive_research(
    request: ResearchRequest,
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> str:
    """
    Провести комплексное исследование с NLP анализом.

    Args:
        request: Параметры исследования
        dependencies: Зависимости агента

    Returns:
        Результаты исследования
    """
    # Настраиваем зависимости под запрос
    if dependencies is None:
        dependencies = _create_dependencies_from_request(request)

    agent = create_nlp_content_research_agent(dependencies)

    # Формируем промпт для исследования
    research_prompt = f"""
Проведите комплексное исследование по теме: "{request.topic}"

**ПАРАМЕТРЫ ИССЛЕДОВАНИЯ:**
- Домен: {request.domain}
- Тип исследования: {request.research_type}
- Целевая аудитория: {request.target_audience}
- Области фокуса: {', '.join(request.focus_areas) if request.focus_areas else 'Не указаны'}
- NLP техники: {', '.join(request.nlp_techniques) if request.nlp_techniques else 'По умолчанию'}

**ТРЕБУЕМЫЕ АНАЛИЗЫ:**
- Анализ вирусного потенциала: {"Да" if request.enable_viral_analysis else "Нет"}
- Конкурентный анализ: {"Да" if request.enable_competitor_analysis else "Нет"}

**ФОРМАТ РЕЗУЛЬТАТА:** {request.output_format}

Используйте методологию PatternShift v2.0 и все доступные NLP техники для создания максимально эффективного исследования.
"""

    result = await agent.run(research_prompt, deps=dependencies)
    return result.data


async def get_quick_insights(
    request: QuickInsightRequest,
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> str:
    """
    Получить быстрые инсайты по теме.

    Args:
        request: Параметры запроса
        dependencies: Зависимости агента

    Returns:
        Быстрые инсайты
    """
    if dependencies is None:
        settings = load_settings()
        dependencies = create_universal_research_dependencies(settings.llm_api_key)

    agent = create_nlp_content_research_agent(dependencies)

    insight_prompt = f"""
Предоставьте быстрые профессиональные инсайты по теме: "{request.topic}"

Фокус анализа: {request.insight_type}

Требования:
- Используйте NLP подход к анализу
- Выявите ключевые болевые точки аудитории
- Оцените вирусный потенциал
- Дайте практические рекомендации

Формат: краткий, структурированный анализ с конкретными выводами.
"""

    result = await agent.run(insight_prompt, deps=dependencies)
    return result.data


async def optimize_content_with_nlp(
    request: ContentOptimizationRequest,
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> str:
    """
    Оптимизировать контент с помощью NLP техник.

    Args:
        request: Параметры оптимизации
        dependencies: Зависимости агента

    Returns:
        Оптимизированный контент
    """
    if dependencies is None:
        settings = load_settings()
        dependencies = create_universal_research_dependencies(settings.llm_api_key)

    # Настраиваем NLP техники для оптимизации
    if request.nlp_techniques:
        dependencies.primary_nlp_techniques = [NLPTechnique(t) for t in request.nlp_techniques]

    agent = create_nlp_content_research_agent(dependencies)

    optimization_prompt = f"""
Оптимизируйте следующий контент с помощью продвинутых NLP техник:

**ИСХОДНЫЙ КОНТЕНТ:**
{request.content}

**ЦЕЛЕВАЯ АУДИТОРИЯ:** {request.target_audience}
**ЦЕЛИ ОПТИМИЗАЦИИ:** {', '.join(request.optimization_goals)}
**ПРИМЕНЯЕМЫЕ NLP ТЕХНИКИ:** {', '.join(request.nlp_techniques) if request.nlp_techniques else 'Все доступные'}

**ТРЕБОВАНИЯ:**
1. Применить VAK адаптацию (визуальные, аудиальные, кинестетические предикаты)
2. Использовать техники раппорта и присоединения
3. Встроить пресуппозиции и вставленные команды
4. Оптимизировать эмоциональное воздействие
5. Повысить вирусный потенциал

**РЕЗУЛЬТАТ:** Предоставить оптимизированную версию + объяснение примененных техник.
"""

    result = await agent.run(optimization_prompt, deps=dependencies)
    return result.data


async def analyze_audience_pain_points(
    topic: str,
    domain: str = "psychology",
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> str:
    """
    Анализ болевых точек аудитории по теме.

    Args:
        topic: Тема для анализа
        domain: Домен исследования
        dependencies: Зависимости агента

    Returns:
        Анализ болевых точек
    """
    if dependencies is None:
        settings = load_settings()
        dependencies = create_universal_research_dependencies(
            settings.llm_api_key,
            domain=domain
        )

    agent = create_nlp_content_research_agent(dependencies)

    # Используем специализированный промпт
    task_prompt = get_task_specific_prompt("audience_research", ResearchDomain(domain))

    pain_points_prompt = f"""
{task_prompt}

**ТЕМА АНАЛИЗА:** {topic}

Проведите глубинный анализ болевых точек аудитории:

1. **Эмоциональные болевые точки** - страхи, тревоги, фрустрации
2. **Практические проблемы** - конкретные вызовы и препятствия
3. **Социальные факторы** - давление окружения, стереотипы
4. **Языковые паттерны** - как аудитория описывает свои проблемы

**Результат:** Структурированный список болевых точек с NLP-анализом и рекомендациями по их использованию в контенте.
"""

    result = await agent.run(pain_points_prompt, deps=dependencies)
    return result.data


# === СПЕЦИАЛИЗИРОВАННЫЕ АГЕНТЫ ===

def create_psychology_research_agent(api_key: str) -> Agent[NLPContentResearchDependencies, str]:
    """Создать агента для психологических исследований."""
    deps = create_psychology_research_dependencies(api_key)
    return create_nlp_content_research_agent(deps)


def create_astrology_research_agent(api_key: str) -> Agent[NLPContentResearchDependencies, str]:
    """Создать агента для астрологических исследований."""
    deps = create_astrology_research_dependencies(api_key)
    return create_nlp_content_research_agent(deps)


def create_universal_research_agent(api_key: str, domain: str = "general") -> Agent[NLPContentResearchDependencies, str]:
    """Создать универсальный исследовательский агент."""
    deps = create_universal_research_dependencies(api_key, domain)
    return create_nlp_content_research_agent(deps)


# === ПАКЕТНАЯ ОБРАБОТКА ===

async def batch_analyze_topics(
    topics: List[str],
    domain: str = "psychology",
    analysis_type: str = "pain_points",
    dependencies: Optional[NLPContentResearchDependencies] = None
) -> List[Dict[str, Any]]:
    """
    Пакетный анализ нескольких тем.

    Args:
        topics: Список тем для анализа
        domain: Домен исследования
        analysis_type: Тип анализа
        dependencies: Зависимости агента

    Returns:
        Результаты анализа для каждой темы
    """
    if dependencies is None:
        settings = load_settings()
        dependencies = create_universal_research_dependencies(
            settings.llm_api_key,
            domain=domain
        )

    results = []

    # Обрабатываем темы параллельно (ограничено по производительности)
    semaphore = asyncio.Semaphore(3)  # Максимум 3 параллельных запроса

    async def analyze_topic(topic: str) -> Dict[str, Any]:
        async with semaphore:
            try:
                if analysis_type == "pain_points":
                    result = await analyze_audience_pain_points(topic, domain, dependencies)
                else:
                    request = QuickInsightRequest(topic=topic, insight_type=analysis_type)
                    result = await get_quick_insights(request, dependencies)

                return {
                    "topic": topic,
                    "analysis_type": analysis_type,
                    "result": result,
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {
                    "topic": topic,
                    "analysis_type": analysis_type,
                    "result": None,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

    # Запускаем все анализы параллельно
    tasks = [analyze_topic(topic) for topic in topics]
    results = await asyncio.gather(*tasks)

    return results


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def _create_dependencies_from_request(request: ResearchRequest) -> NLPContentResearchDependencies:
    """Создать зависимости из запроса."""
    settings = load_settings()

    return create_research_dependencies(
        api_key=settings.llm_api_key,
        research_domain=request.domain,
        target_audience=request.target_audience,
        nlp_techniques=request.nlp_techniques or settings.primary_nlp_techniques,
        enable_web_search=settings.enable_web_search,
        enable_competitive_analysis=request.enable_competitor_analysis,
        enable_viral_content_analysis=request.enable_viral_analysis
    )


def get_agent_capabilities() -> Dict[str, Any]:
    """Получить информацию о возможностях агента."""
    return {
        "name": "NLP Content Research Agent",
        "version": "2.0.0",
        "specialization": "Universal research with NLP optimization",
        "supported_domains": [domain.value for domain in ResearchDomain],
        "nlp_techniques": [technique.value for technique in NLPTechnique],
        "audience_types": [audience.value for audience in AudienceType],
        "methodologies": ["PatternShift v2.0", "VAK Adaptation", "Ericksonian Hypnosis"],
        "capabilities": [
            "Comprehensive research",
            "Viral potential analysis",
            "Competitor analysis",
            "Pain point identification",
            "NLP content optimization",
            "VAK adaptations",
            "Multi-domain support",
            "Cost-optimized models",
            "Batch processing"
        ],
        "output_formats": [
            "research_brief",
            "content_outline",
            "vak_adaptations",
            "viral_analysis",
            "competitor_report"
        ]
    }


# === ЭКСПОРТ ===

__all__ = [
    # Основной агент
    "nlp_content_research_agent",
    "create_nlp_content_research_agent",

    # Основные функции
    "conduct_comprehensive_research",
    "get_quick_insights",
    "optimize_content_with_nlp",
    "analyze_audience_pain_points",

    # Специализированные агенты
    "create_psychology_research_agent",
    "create_astrology_research_agent",
    "create_universal_research_agent",

    # Пакетная обработка
    "batch_analyze_topics",

    # Модели запросов
    "ResearchRequest",
    "QuickInsightRequest",
    "ContentOptimizationRequest",

    # Утилиты
    "get_agent_capabilities"
]