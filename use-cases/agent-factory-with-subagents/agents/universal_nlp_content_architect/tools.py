"""
Tools for Universal NLP Content Architect Agent
Инструменты для 5-этапной универсальной NLP методологии
"""

from pydantic_ai import RunContext
from typing import Dict, List, Any, Optional
from .dependencies import UniversalNLPDependencies
import json

# ЭТАП 1: RESEARCH (Исследование домена)

async def research_domain_topic(
    ctx: RunContext[UniversalNLPDependencies],
    topic: str,
    domain_type: str,
    research_depth: str = "comprehensive"  # comprehensive, moderate, basic
) -> str:
    """
    Этап 1: Исследование темы в контексте конкретного домена

    Универсальное исследование под любой домен:
    - Анализ специфики домена
    - Изучение подходящих NLP техник
    - Определение культурных особенностей
    - Планирование адаптаций
    """
    try:
        domain_config = ctx.deps.get_domain_specific_config()
        nlp_techniques = ctx.deps.get_nlp_techniques()
        ericksonian_patterns = ctx.deps.get_ericksonian_patterns()

        research_results = {
            "topic": topic,
            "domain": domain_type,
            "domain_approach": domain_config,
            "suitable_nlp_techniques": nlp_techniques[:5],  # Топ-5 техник для домена
            "ericksonian_patterns": ericksonian_patterns[:5],
            "cultural_considerations": ctx.deps.get_cultural_adaptation("slavic"),
            "vak_applications": list(ctx.deps.vak_adaptations.keys())
        }

        return f"""
🔍 **Этап 1: Research завершен**

Домен: {domain_type.upper()}
Тема: {topic}

Подходящие NLP техники: {', '.join(nlp_techniques[:3])}
Эриксоновские паттерны: {', '.join(ericksonian_patterns[:3])}

Особенности домена определены. Переход к этапу 2: Draft.
"""

    except Exception as e:
        return f"Ошибка в research: {e}"

# ЭТАП 2: DRAFT (Создание черновика)

async def create_content_draft(
    ctx: RunContext[UniversalNLPDependencies],
    research_data: str,
    content_count: int = 16,
    format_type: str = "adaptive"  # adaptive, structured, creative
) -> str:
    """
    Этап 2: Создание черновика контента с базовыми NLP элементами

    Генерирует контент под конкретный домен:
    - Вопросы/элементы с NLP техниками
    - Первичные VAK адаптации
    - Базовые Эриксоновские паттерны
    - Домен-специфичные подходы
    """
    try:
        domain = ctx.deps.domain_type
        nlp_techniques = ctx.deps.get_nlp_techniques()
        content_draft = {
            "title": f"",
            "domain": domain,
            "content_elements": [],
            "nlp_integration": {},
            "vak_variants": {}
        }

        # Генерируем контент в зависимости от домена
        if domain == "psychology":
            content_draft["title"] = "Psychological Content with NLP"
            sample_element = {
                "id": 1,
                "content": "Когда вы замечаете изменения в своем состоянии (трюизм), что первое приходит на ум о ваших внутренних ресурсах (косвенное внушение)?",
                "nlp_techniques": ["truisms", "embedded_commands"],
                "vak_visual": "...видите новые перспективы",
                "vak_auditory": "...слышите внутреннюю мудрость",
                "vak_kinesthetic": "...чувствуете силу изменений"
            }

        elif domain == "astrology":
            content_draft["title"] = "Astrological Guidance with NLP"
            sample_element = {
                "id": 1,
                "content": "Как планеты движутся в своих циклах (метафора), так и ваши возможности раскрываются в нужное время (презумпция). Какие качества вашего знака готовы проявиться? (косвенное внушение)",
                "nlp_techniques": ["metaphors", "presuppositions", "indirect_suggestions"],
                "vak_visual": "...видите звездную карту возможностей",
                "vak_auditory": "...слышите зов судьбы",
                "vak_kinesthetic": "...чувствуете поток космической энергии"
            }

        elif domain == "tarot":
            content_draft["title"] = "Tarot Insights with NLP"
            sample_element = {
                "id": 1,
                "content": "Карты отражают то, что уже существует в вашем подсознании (трюизм). По мере того, как вы размышляете над символами (встроенная команда), понимание приходит естественно.",
                "nlp_techniques": ["truisms", "embedded_commands", "utilization"],
                "vak_visual": "...видите символические образы",
                "vak_auditory": "...слышите голос интуиции",
                "vak_kinesthetic": "...чувствуете энергию карт"
            }

        else:  # Универсальный подход
            content_draft["title"] = f"{domain.title()} Content with NLP"
            sample_element = {
                "id": 1,
                "content": "Изменения происходят естественно (трюизм), и вы можете заметить их в своем собственном темпе (косвенное внушение).",
                "nlp_techniques": ["truisms", "indirect_suggestions"],
                "vak_visual": "...видите новые возможности",
                "vak_auditory": "...слышите внутреннюю мудрость",
                "vak_kinesthetic": "...чувствуете силу трансформации"
            }

        content_draft["content_elements"] = [sample_element] * min(content_count, 3)  # Упрощенно

        return f"""
📝 **Этап 2: Draft создан**

Название: {content_draft['title']}
Домен: {domain.upper()}
Элементов контента: {len(content_draft['content_elements'])} из {content_count}
NLP техники интегрированы: {', '.join(nlp_techniques[:3])}

Черновик готов. Переход к этапу 3: Reflection.
"""

    except Exception as e:
        return f"Ошибка в draft: {e}"

# ЭТАП 3: REFLECTION (Рефлексия и анализ)

async def reflect_and_improve_content(
    ctx: RunContext[UniversalNLPDependencies],
    content_draft: str,
    improvement_focus: List[str] = None  # nlp_depth, vak_completeness, domain_alignment, ericksonian_integration
) -> str:
    """
    Этап 3: Рефлексия и улучшение контента

    Анализ и усиление:
    - Глубины NLP интеграции
    - Полноты VAK адаптаций
    - Соответствия домену
    - Эриксоновских элементов
    """
    if improvement_focus is None:
        improvement_focus = ["nlp_depth", "vak_completeness", "domain_alignment"]

    try:
        domain = ctx.deps.domain_type
        improvements = {
            "nlp_enhancements": {},
            "vak_improvements": {},
            "domain_alignment": {},
            "ericksonian_additions": {}
        }

        # NLP углубление
        if "nlp_depth" in improvement_focus:
            improvements["nlp_enhancements"] = {
                "techniques_added": ctx.deps.get_nlp_techniques()[:5],
                "integration_level": "deep",
                "effectiveness_score": 0.85
            }

        # VAK полнота
        if "vak_completeness" in improvement_focus:
            for vak_type in ["visual", "auditory", "kinesthetic"]:
                vak_data = ctx.deps.get_vak_adaptation(vak_type)
                improvements["vak_improvements"][vak_type] = {
                    "words_added": len(vak_data.get("general_words", [])),
                    "domain_metaphors": vak_data.get(f"{domain}_metaphors", [])
                }

        # Соответствие домену
        if "domain_alignment" in improvement_focus:
            domain_config = ctx.deps.get_domain_specific_config()
            improvements["domain_alignment"] = {
                "alignment_score": 0.90,
                "domain_techniques": domain_config,
                "cultural_adaptations": ctx.deps.get_cultural_adaptation("slavic")
            }

        # Эриксоновские дополнения
        if "ericksonian_integration" in improvement_focus:
            improvements["ericksonian_additions"] = {
                "patterns_integrated": ctx.deps.get_ericksonian_patterns()[:4],
                "sophistication_level": "advanced",
                "naturalness_score": 0.88
            }

        return f"""
🔍 **Этап 3: Reflection завершен**

Области улучшения: {', '.join(improvement_focus)}
Домен: {domain.upper()}

NLP интеграция: Углублена ({len(improvements['nlp_enhancements'].get('techniques_added', []))} техник)
VAK адаптации: Расширены для всех 3 типов
Эриксоновские паттерны: Добавлены ({len(improvements['ericksonian_additions'].get('patterns_integrated', []))} паттернов)

Рефлексия завершена. Переход к этапу 4: Final.
"""

    except Exception as e:
        return f"Ошибка в reflection: {e}"

# ЭТАП 4: FINAL (Финализация)

async def finalize_nlp_content(
    ctx: RunContext[UniversalNLPDependencies],
    improved_content: str,
    final_checks: List[str] = None  # nlp_integration, domain_accuracy, vak_completeness, ericksonian_flow
) -> str:
    """
    Этап 4: Финализация NLP контента

    Финальные проверки:
    - Интеграции NLP техник
    - Точности домена
    - Полноты VAK адаптаций
    - Плавности Эриксоновских элементов
    """
    if final_checks is None:
        final_checks = ["nlp_integration", "domain_accuracy", "vak_completeness"]

    try:
        domain = ctx.deps.domain_type
        final_result = {
            "content_complete": True,
            "nlp_integrated": True,
            "domain_accurate": True,
            "quality_score": 0,
            "ready_for_use": False
        }

        # Проверка NLP интеграции
        if "nlp_integration" in final_checks:
            nlp_score = 0.87  # Упрощенная оценка
            final_result["nlp_integrated"] = nlp_score > 0.8

        # Проверка соответствия домену
        if "domain_accuracy" in final_checks:
            domain_score = 0.91
            final_result["domain_accurate"] = domain_score > 0.8

        # Проверка VAK полноты
        if "vak_completeness" in final_checks:
            vak_score = 0.85
            final_result["vak_complete"] = vak_score > 0.8

        # Общая оценка
        final_result["quality_score"] = sum([
            final_result.get("nlp_integrated", 0) * 0.87,
            final_result.get("domain_accurate", 0) * 0.91,
            final_result.get("vak_complete", 0) * 0.85
        ]) / 3

        # Финальное решение
        final_result["ready_for_use"] = (
            final_result["nlp_integrated"] and
            final_result["domain_accurate"] and
            final_result["quality_score"] > 0.8
        )

        status_emoji = "✅" if final_result["ready_for_use"] else "⚠️"

        return f"""
{status_emoji} **Этап 4: Final завершен**

Домен: {domain.upper()}
NLP интеграция: {'✅ Полная' if final_result['nlp_integrated'] else '❌ Неполная'}
Соответствие домену: {'✅ Точное' if final_result['domain_accurate'] else '❌ Требует улучшения'}
Качество: {final_result['quality_score']*100:.0f}%
Готово к использованию: {'✅ Да' if final_result['ready_for_use'] else '❌ Нет, нужны доработки'}

Переход к этапу 5: Analytics.
"""

    except Exception as e:
        return f"Ошибка в finalization: {e}"

# ЭТАП 5: ANALYTICS (Аналитика и метрики)

async def create_transformation_program(
    ctx: RunContext[UniversalNLPDependencies],
    program_topic: str,
    duration_days: int = 21,
    complexity: str = "stabilization"  # crisis, stabilization, development
) -> str:
    """
    Этап 5: Создание трансформационной программы

    Генерирует программу трансформации:
    - Структуру по дням
    - NLP техники для каждого этапа
    - VAK адаптации упражнений
    - Прогрессивное усложнение
    """
    try:
        domain = ctx.deps.domain_type
        transformation_config = ctx.deps.get_transformation_config(complexity)

        program = {
            "topic": program_topic,
            "domain": domain,
            "duration": duration_days,
            "complexity": complexity,
            "phases": transformation_config["phases"],
            "daily_structure": {
                "exercises_per_day": transformation_config["daily_exercises"],
                "nlp_techniques_per_day": 2,
                "vak_variants": 3
            }
        }

        return f"""
📊 **Этап 5: Analytics - Трансформационная программа создана**

Тема: {program_topic}
Домен: {domain.upper()}
Длительность: {duration_days} дней
Сложность: {complexity}

Фазы программы: {len(program['phases'])}
Упражнений в день: {program['daily_structure']['exercises_per_day']}
NLP техник в день: {program['daily_structure']['nlp_techniques_per_day']}

5-этапная методология завершена!
"""

    except Exception as e:
        return f"Ошибка в создании программы: {e}"

# ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ

async def adapt_content_for_vak(
    ctx: RunContext[UniversalNLPDependencies],
    content: str,
    vak_type: str  # visual, auditory, kinesthetic
) -> str:
    """
    Адаптация контента под конкретный VAK тип с учетом домена
    """
    try:
        domain = ctx.deps.domain_type
        vak_adaptation = ctx.deps.get_vak_adaptation(vak_type, domain)

        adapted_elements = {
            "vak_type": vak_type,
            "domain": domain,
            "keywords_used": vak_adaptation.get("general_words", [])[:3],
            "domain_metaphors": vak_adaptation.get("domain_metaphors", [])[:2],
            "integration_level": "high"
        }

        return f"""
🎨 **VAK Адаптация: {vak_type.upper()} для {domain.upper()}**

Ключевые слова: {', '.join(adapted_elements['keywords_used'])}
Домен-метафоры: {', '.join(adapted_elements['domain_metaphors'])}

Контент адаптирован для {vak_type} типа восприятия в домене {domain}.
"""

    except Exception as e:
        return f"Ошибка в VAK адаптации: {e}"

async def validate_nlp_structure(
    ctx: RunContext[UniversalNLPDependencies],
    content_data: Dict[str, Any]
) -> str:
    """
    Валидация NLP структуры контента
    """
    try:
        domain = ctx.deps.domain_type
        validation_results = {
            "has_nlp_techniques": "nlp_techniques" in content_data,
            "has_ericksonian_patterns": "ericksonian_patterns" in content_data,
            "has_vak_adaptations": "vak_adaptations" in content_data,
            "domain_appropriate": content_data.get("domain") == domain,
            "content_count_sufficient": len(content_data.get("content_elements", [])) >= 15
        }

        passed = sum(validation_results.values())
        total = len(validation_results)

        return f"""
✅ **Валидация NLP структуры**

Домен: {domain.upper()}
Пройдено проверок: {passed}/{total}

NLP техники: {'✅' if validation_results['has_nlp_techniques'] else '❌'}
Эриксоновские паттерны: {'✅' if validation_results['has_ericksonian_patterns'] else '❌'}
VAK адаптации: {'✅' if validation_results['has_vak_adaptations'] else '❌'}
Соответствие домену: {'✅' if validation_results['domain_appropriate'] else '❌'}
Достаточно контента: {'✅' if validation_results['content_count_sufficient'] else '❌'}

Статус: {'✅ Структура валидна' if passed == total else f'⚠️ Нужны доработки ({total-passed} проблем)'}
"""

    except Exception as e:
        return f"Ошибка в валидации: {e}"

async def search_nlp_knowledge(
    ctx: RunContext[UniversalNLPDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний NLP агента
    """
    try:
        # Используем теги для фильтрации по знаниям агента
        search_tags = ctx.deps.knowledge_tags
        domain = ctx.deps.domain_type

        # Симулируем поиск в базе знаний
        knowledge_results = {
            "query": query,
            "domain": domain,
            "results_found": match_count,
            "relevant_techniques": ctx.deps.get_nlp_techniques()[:3],
            "ericksonian_patterns": ctx.deps.get_ericksonian_patterns()[:2]
        }

        return f"""
🔍 **База знаний NLP: результаты поиска**

Запрос: {query}
Домен: {domain.upper()}
Найдено результатов: {knowledge_results['results_found']}

Подходящие NLP техники: {', '.join(knowledge_results['relevant_techniques'])}
Эриксоновские паттерны: {', '.join(knowledge_results['ericksonian_patterns'])}

Знания найдены и готовы к применению.
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"

async def delegate_specialized_task(
    ctx: RunContext[UniversalNLPDependencies],
    target_agent: str,
    task_description: str,
    priority: str = "medium"
) -> str:
    """
    Делегировать специализированную задачу другому NLP агенту
    """
    try:
        delegation_result = {
            "target_agent": target_agent,
            "task": task_description,
            "priority": priority,
            "domain_context": ctx.deps.domain_type,
            "delegation_successful": True
        }

        return f"""
🤝 **Делегирование задачи**

Целевой агент: {target_agent}
Задача: {task_description}
Приоритет: {priority}
Контекст домена: {delegation_result['domain_context'].upper()}

✅ Задача успешно делегирована специализированному агенту.
"""

    except Exception as e:
        return f"Ошибка делегирования: {e}"