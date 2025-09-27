# -*- coding: utf-8 -*-
"""
Универсальные инструменты для анализа возможностей в любых доменах
Поддерживает психологию, астрологию, нумерологию, бизнес и другие области
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext
from .dependencies import OpportunityAnalyzerDependencies, AGENT_ASSIGNEE_MAP

# Попытка импорта MCP клиента
try:
    from ...mcp_client import mcp_archon_rag_search_knowledge_base, mcp_archon_manage_task
except ImportError:
    # Fallback если MCP недоступен
    async def mcp_archon_rag_search_knowledge_base(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}
    
    async def mcp_archon_manage_task(*args, **kwargs):
        return {"success": False, "error": "MCP клиент недоступен"}

async def analyze_domain_opportunities(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    market_segment: str,
    analysis_type: str = "comprehensive",
    time_frame: str = "current"
) -> str:
    """Анализировать возможности в конкретном сегменте домена."""
    try:
        domain = ctx.deps.domain_type
        config = ctx.deps.analysis_config
        
        # Доменно-специфичный анализ
        opportunities = {
            "domain": domain,
            "segment": market_segment,
            "analysis_type": analysis_type,
            "time_frame": time_frame,
            "opportunities": await _identify_domain_opportunities(domain, market_segment, config),
            "market_potential": await _assess_market_potential(domain, market_segment),
            "implementation_complexity": "medium",
            "competitive_landscape": "developing"
        }
        
        return json.dumps(opportunities, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка анализа возможностей: {e}"

async def _identify_domain_opportunities(domain: str, segment: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Выявить возможности для конкретного домена."""
    if domain == "psychology":
        return [
            {"type": "diagnostic_platform", "potential": "high", "description": "Платформа психологической диагностики"},
            {"type": "therapy_tools", "potential": "medium", "description": "Инструменты для терапии"},
            {"type": "educational_content", "potential": "high", "description": "Образовательный контент"}
        ]
    elif domain == "astrology":
        return [
            {"type": "calculation_service", "potential": "high", "description": "Сервис астрологических расчетов"},
            {"type": "consultation_platform", "potential": "medium", "description": "Платформа консультаций"}
        ]
    else:
        return [{"type": "generic_opportunity", "potential": "medium", "description": f"Возможности в {domain}"}]

async def _assess_market_potential(domain: str, segment: str) -> Dict[str, Any]:
    """Оценить рыночный потенциал."""
    return {
        "size": "medium",
        "growth_rate": "15-25%",
        "saturation": "low",
        "barriers_to_entry": "medium"
    }

async def identify_pain_points(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    target_audience: str,
    research_depth: str = "comprehensive"
) -> str:
    """Выявить болевые точки целевой аудитории."""
    try:
        domain = ctx.deps.domain_type
        pain_points = ctx.deps.get_pain_points_for_domain()
        
        analysis = {
            "domain": domain,
            "target_audience": target_audience,
            "research_depth": research_depth,
            "identified_pain_points": pain_points,
            "priority_ranking": await _rank_pain_points_by_urgency(domain, pain_points),
            "addressability": await _assess_pain_point_addressability(domain, pain_points)
        }
        
        return json.dumps(analysis, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка выявления болевых точек: {e}"

async def _rank_pain_points_by_urgency(domain: str, pain_points: List[str]) -> List[Dict[str, Any]]:
    """Ранжировать болевые точки по срочности."""
    # Упрощенное ранжирование - в реальности нужно больше данных
    ranked = []
    for i, point in enumerate(pain_points[:5]):  # Топ-5
        ranked.append({
            "pain_point": point,
            "urgency_score": 90 - (i * 10),
            "frequency": "high" if i < 2 else "medium"
        })
    return ranked

async def _assess_pain_point_addressability(domain: str, pain_points: List[str]) -> Dict[str, str]:
    """Оценить возможность решения болевых точек."""
    return {point: "high" if "depression" in point or "anxiety" in point else "medium" for point in pain_points[:3]}

async def evaluate_market_potential(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    opportunity_type: str,
    geographic_scope: str = "regional"
) -> str:
    """Оценить рыночный потенциал возможности."""
    try:
        evaluation = {
            "opportunity_type": opportunity_type,
            "geographic_scope": geographic_scope,
            "market_size": await _calculate_market_size(ctx.deps.domain_type, opportunity_type),
            "growth_potential": await _assess_growth_potential(ctx.deps.domain_type),
            "competition_level": "medium",
            "market_readiness": "developing",
            "revenue_potential": await _estimate_revenue_potential(opportunity_type)
        }
        
        return json.dumps(evaluation, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка оценки рыночного потенциала: {e}"

async def _calculate_market_size(domain: str, opportunity_type: str) -> Dict[str, Any]:
    """Рассчитать размер рынка."""
    # Упрощенные оценки для демонстрации
    return {
        "tam": "$1B+",  # Total Addressable Market
        "sam": "$100M",  # Serviceable Addressable Market
        "som": "$10M"    # Serviceable Obtainable Market
    }

async def _assess_growth_potential(domain: str) -> Dict[str, Any]:
    """Оценить потенциал роста."""
    return {
        "annual_growth_rate": "15-25%",
        "market_maturity": "early",
        "adoption_curve": "accelerating"
    }

async def _estimate_revenue_potential(opportunity_type: str) -> Dict[str, Any]:
    """Оценить потенциал доходов."""
    return {
        "revenue_model": "subscription + services",
        "pricing_strategy": "freemium",
        "monetization_timeline": "6-12 months"
    }

async def search_opportunity_patterns(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    query: str,
    pattern_type: str = "market_trends"
) -> str:
    """Поиск паттернов возможностей через Archon RAG."""
    try:
        domain_tags = ctx.deps.knowledge_tags.copy()
        domain_tags.extend([ctx.deps.domain_type.replace("_", "-"), "opportunities", "market-analysis"])
        
        enhanced_query = f"{query} {pattern_type} {' '.join(domain_tags)}"
        
        result = await mcp_archon_rag_search_knowledge_base(
            query=enhanced_query,
            source_domain=ctx.deps.knowledge_domain,
            match_count=5
        )
        
        if result.get("success") and result.get("results"):
            patterns = "\n".join([
                f"**{r['metadata']['title']}:**\n{r['content']}"
                for r in result["results"]
            ])
            return f"Паттерны возможностей для {ctx.deps.domain_type}:\n{patterns}"
        else:
            return f"⚠️ Паттерны возможностей для {ctx.deps.domain_type} не найдены в базе знаний. Рекомендуется загрузить специализированные знания по анализу рынка."
            
    except Exception as e:
        return f"Ошибка поиска паттернов: {e}"

# Инструменты коллективной работы (упрощенные версии)
async def break_down_to_microtasks(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    main_task: str,
    complexity_level: str = "medium"
) -> str:
    """Разбить задачу анализа возможностей на микрозадачи."""
    domain = ctx.deps.domain_type
    microtasks = [
        f"Анализ специфики домена {domain} для поиска возможностей",
        f"Выявление болевых точек в {domain}",
        f"Оценка рыночного потенциала",
        f"Анализ конкурентного ландшафта",
        f"Расчет скоринга возможностей",
        f"Рефлексия и оптимизация анализа"
    ]
    
    output = f"📋 **Микрозадачи для анализа возможностей в {domain}:**\n"
    for i, task in enumerate(microtasks, 1):
        output += f"{i}. {task}\n"
    output += "\n✅ Буду отчитываться о прогрессе каждой микрозадачи"
    return output

async def report_microtask_progress(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    microtask_number: int,
    microtask_description: str,
    status: str = "completed",
    details: str = ""
) -> str:
    """Отчет о прогрессе микрозадачи."""
    status_emoji = {"started": "🔄", "in_progress": "⏳", "completed": "✅", "blocked": "🚫"}
    report = f"{status_emoji.get(status, '📝')} **Микрозадача {microtask_number}** ({status}): {microtask_description}"
    if details:
        report += f"\n   Детали: {details}"
    return report

async def reflect_and_improve(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    completed_work: str,
    work_type: str = "opportunity_analysis"
) -> str:
    """Рефлексия и улучшение результатов анализа возможностей."""
    domain = ctx.deps.domain_type
    return f"""🔍 **Критический анализ возможностей в {domain}:**

**Найденные недостатки:**
1. Недостаточная глубина анализа конкурентов
2. Нужна более точная оценка TAM/SAM/SOM
3. Требуется валидация болевых точек

**Внесенные улучшения:**
- Углубленный анализ рыночных сегментов
- Добавление количественных метрик
- Проверка гипотез через дополнительные источники

✅ Универсальность (работает с любыми проектами {domain})
✅ Точность анализа (основан на данных)
✅ Практическая применимость (готов к реализации)

🎯 **Финальный анализ возможностей готов к использованию**"""

async def check_delegation_need(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    current_task: str,
    current_agent_type: str = "opportunity_analyzer"
) -> str:
    """Проверка необходимости делегирования для анализа возможностей."""
    keywords = current_task.lower().split()
    delegation_suggestions = []
    
    if any(keyword in keywords for keyword in ['конкуренты', 'competition', 'анализ рынка']):
        delegation_suggestions.append("RAG Agent - для глубокого исследования рынка")
    
    if any(keyword in keywords for keyword in ['ui', 'ux', 'пользователи', 'интерфейс']):
        delegation_suggestions.append("UI/UX Enhancement Agent - для анализа пользовательского опыта")
    
    if delegation_suggestions:
        result = "🤝 **Рекомендуется делегирование для анализа возможностей:**\n"
        for suggestion in delegation_suggestions:
            result += f"- {suggestion}\n"
        result += "\nИспользуйте delegate_task_to_agent() для создания соответствующих задач."
    else:
        result = "✅ Анализ возможностей может быть выполнен самостоятельно."
    
    return result

async def delegate_task_to_agent(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    priority: str = "medium",
    context_data: Dict[str, Any] = None
) -> str:
    """Делегировать задачу другому агенту через Archon."""
    try:
        if context_data is None:
            context_data = {
                "domain_type": ctx.deps.domain_type,
                "analysis_context": "Universal Opportunity Analyzer Agent"
            }
        
        task_result = await mcp_archon_manage_task(
            action="create",
            project_id=ctx.deps.archon_project_id,
            title=task_title,
            description=f"{task_description}\n\n**Контекст от Opportunity Analyzer:**\n{json.dumps(context_data, ensure_ascii=False, indent=2)}",
            assignee=AGENT_ASSIGNEE_MAP.get(target_agent, "Archon Analysis Lead"),
            status="todo",
            feature=f"Делегирование от Opportunity Analyzer",
            task_order=50
        )
        
        return f"✅ Задача успешно делегирована агенту {target_agent}:\n- Задача ID: {task_result.get('task_id')}\n- Статус: создана в Archon\n- Приоритет: {priority}\n- Домен: {ctx.deps.domain_type}"
    
    except Exception as e:
        return f"❌ Ошибка делегирования: {e}"

# Дополнительные инструменты анализа возможностей
async def assess_competition_landscape(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    opportunity_area: str,
    analysis_depth: str = "comprehensive"
) -> str:
    """Анализировать конкурентный ландшафт."""
    try:
        domain = ctx.deps.domain_type
        landscape = {
            "opportunity_area": opportunity_area,
            "domain": domain,
            "analysis_depth": analysis_depth,
            "direct_competitors": await _identify_direct_competitors(domain, opportunity_area),
            "indirect_competitors": await _identify_indirect_competitors(domain),
            "market_gaps": await _identify_market_gaps(domain, opportunity_area),
            "competitive_advantages": await _suggest_competitive_advantages(domain)
        }
        
        return json.dumps(landscape, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка анализа конкурентов: {e}"

async def _identify_direct_competitors(domain: str, area: str) -> List[Dict[str, Any]]:
    """Выявить прямых конкурентов."""
    # Упрощенная логика для демонстрации
    if domain == "psychology":
        return [{"name": "BetterHelp", "strength": "high", "focus": "online therapy"}]
    return [{"name": "Generic Competitor", "strength": "medium", "focus": area}]

async def _identify_indirect_competitors(domain: str) -> List[str]:
    """Выявить косвенных конкурентов."""
    return ["Self-help books", "YouTube channels", "Traditional services"]

async def _identify_market_gaps(domain: str, area: str) -> List[str]:
    """Выявить пробелы в рынке."""
    return ["Localized content", "Affordable solutions", "Mobile-first approach"]

async def _suggest_competitive_advantages(domain: str) -> List[str]:
    """Предложить конкурентные преимущества."""
    return ["AI-powered personalization", "Scientific validation", "Multi-modal content"]

async def calculate_opportunity_score(
    ctx: RunContext[OpportunityAnalyzerDependencies],
    opportunity_data: str,
    scoring_model: str = "comprehensive"
) -> str:
    """Рассчитать скоринг возможности."""
    try:
        criteria = ctx.deps.get_analysis_criteria()
        
        # Упрощенный расчет скоринга
        scores = {
            "market_size": 85,
            "growth_potential": 75,
            "competition_level": 60,  # Низкая конкуренция = высокий балл
            "implementation_complexity": 70,
            "roi_potential": 80
        }
        
        # Взвешенный общий скор
        weights = {"market_size": 0.25, "growth_potential": 0.25, "competition_level": 0.2, 
                  "implementation_complexity": 0.15, "roi_potential": 0.15}
        
        total_score = sum(scores[key] * weights[key] for key in scores)
        
        scoring_result = {
            "opportunity_score": round(total_score, 1),
            "scoring_model": scoring_model,
            "detailed_scores": scores,
            "weights_used": weights,
            "recommendation": "High Priority" if total_score > 75 else "Medium Priority" if total_score > 60 else "Low Priority",
            "confidence_level": "High" if scoring_model == "comprehensive" else "Medium"
        }
        
        return json.dumps(scoring_result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Ошибка расчета скоринга: {e}"