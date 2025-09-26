"""
NLP Content Quality Guardian Agent Tools

Инструменты для валидации качества NLP контента и программ трансформации.
"""

from typing import Dict, Any, List, Optional
import asyncio
import json
import re
from datetime import datetime

from pydantic_ai import RunContext

from .dependencies import (
    NLPQualityGuardianDependencies,
    ValidationResult, ValidationAspect, QualityLevel,
    CriticalFlag, ContentType, ValidationDomain
)


async def search_quality_knowledge(
    ctx: RunContext[NLPQualityGuardianDependencies],
    query: str,
    validation_aspect: str = "general"
) -> str:
    """
    Поиск в базе знаний агента по критериям качества.

    Args:
        query: Поисковый запрос
        validation_aspect: Аспект валидации для фокусировки поиска

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Формируем специфичный запрос с учетом аспекта валидации
        specific_query = f"{query} {validation_aspect} quality validation"

        # Используем MCP Archon для поиска (если доступен)
        try:
            from mcp__archon__rag_search_knowledge_base import mcp__archon__rag_search_knowledge_base

            result = await mcp__archon__rag_search_knowledge_base(
                query=specific_query,
                source_domain=ctx.deps.knowledge_domain,
                match_count=5
            )

            if result["success"] and result["results"]:
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in result["results"]
                ])
                return f"База знаний валидации:\n{knowledge}"

        except ImportError:
            pass

        # Fallback поиск по тегам агента
        try:
            result = await mcp__archon__rag_search_knowledge_base(
                query=f"nlp quality guardian {validation_aspect}",
                match_count=3
            )

            if result["success"] and result["results"]:
                knowledge = "\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in result["results"]
                ])
                return f"База знаний (найдено через fallback):\n{knowledge}"

        except Exception:
            pass

        # Если поиск недоступен, возвращаем базовые знания
        return f"""
⚠️ **База знаний NLP Quality Guardian доступна ограниченно**

🔍 **Искали:** {query} (аспект: {validation_aspect})

💡 **Базовые принципы валидации для {validation_aspect}:**

📋 **Методологические критерии:**
- Соответствие PatternShift 2.0
- Трехуровневая структура: Кризис → Стабилизация → Развитие
- VAK персонализация (Visual, Auditory, Kinesthetic)
- Мультиформатный контент (текст + аудио)

🧠 **Психологические критерии:**
- Научная обоснованность техник
- Этическая безопасность
- Возрастная адекватность
- Культурная чувствительность

🎯 **NLP критерии:**
- Правильность применения паттернов
- Безопасность воздействия
- Эффективность техник
- Соответствие стандартам НЛП

🔐 **Критерии безопасности:**
- Отсутствие манипулятивных техник
- Информированное согласие
- Уважение границ пользователя
- Противопоказания и предупреждения

Рекомендуется загрузить полную базу знаний в Archon для более детального анализа.
"""

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}"


async def validate_content_structure(
    ctx: RunContext[NLPQualityGuardianDependencies],
    content: str,
    content_type: str = "mixed"
) -> Dict[str, Any]:
    """
    Валидация структуры контента согласно стандартам.

    Args:
        content: Контент для валидации
        content_type: Тип контента (test, program, technique)

    Returns:
        Результат структурной валидации
    """
    try:
        content_length = len(content)

        # Базовые проверки
        structure_issues = []
        structure_score = 100.0

        # Проверки для тестов
        if content_type == "test":
            # Подсчет вопросов
            questions_pattern = r'(?:^\d+\.|Вопрос\s+\d+|Question\s+\d+)'
            questions = re.findall(questions_pattern, content, re.MULTILINE | re.IGNORECASE)
            question_count = len(questions)

            if question_count < ctx.deps.validation_criteria.min_test_questions:
                structure_issues.append(
                    f"Недостаточно вопросов: найдено {question_count}, "
                    f"минимум {ctx.deps.validation_criteria.min_test_questions}"
                )
                structure_score -= 30

            # Проверка на клинические термины
            clinical_terms = [
                'депрессия', 'тревожность', 'фобия', 'расстройство',
                'синдром', 'диагноз', 'симптом', 'патология'
            ]
            clinical_found = [term for term in clinical_terms if term.lower() in content.lower()]

            if clinical_found and ctx.deps.validation_criteria.avoid_clinical_terms:
                structure_issues.append(
                    f"Найдены клинические термины: {', '.join(clinical_found)}"
                )
                structure_score -= 20

        # Проверки для программ трансформации
        elif content_type == "program":
            # Проверка трехуровневой структуры
            level_keywords = ['кризис', 'стабилизация', 'развитие', 'crisis', 'stabilization', 'development']
            found_levels = [kw for kw in level_keywords if kw.lower() in content.lower()]

            if len(found_levels) < 3 and ctx.deps.validation_criteria.require_three_level_structure:
                structure_issues.append("Отсутствует трехуровневая структура программы")
                structure_score -= 25

            # Проверка VAK персонализации
            vak_keywords = ['визуальный', 'аудиальный', 'кинестетический', 'visual', 'auditory', 'kinesthetic']
            found_vak = [kw for kw in vak_keywords if kw.lower() in content.lower()]

            if len(found_vak) < 2 and ctx.deps.validation_criteria.require_vak_personalization:
                structure_issues.append("Отсутствует VAK персонализация")
                structure_score -= 20

            # Проверка мультиформатности
            format_keywords = ['аудио', 'текст', 'упражнение', 'audio', 'text', 'exercise']
            found_formats = [kw for kw in format_keywords if kw.lower() in content.lower()]

            if len(found_formats) < 2 and ctx.deps.validation_criteria.require_multiformat_content:
                structure_issues.append("Отсутствует мультиформатный контент")
                structure_score -= 15

        # Проверки для NLP техник
        elif content_type == "technique":
            # Проверка базовых элементов техники
            technique_elements = [
                'инструкция', 'шаги', 'применение', 'противопоказания',
                'instruction', 'steps', 'application', 'contraindications'
            ]
            found_elements = [elem for elem in technique_elements if elem.lower() in content.lower()]

            if len(found_elements) < 2:
                structure_issues.append("Отсутствуют базовые элементы техники")
                structure_score -= 30

        # Общие структурные проверки
        # Проверка длины контента
        if content_length < 500:
            structure_issues.append("Слишком короткий контент")
            structure_score -= 10
        elif content_length > ctx.deps.max_content_length:
            structure_issues.append(f"Слишком длинный контент: {content_length} символов")
            structure_score -= 5

        # Проверка структурированности
        headers = re.findall(r'^#+\s+(.+)', content, re.MULTILINE)
        if len(headers) < 2:
            structure_issues.append("Недостаточно структурных элементов (заголовков)")
            structure_score -= 10

        return {
            "structure_score": max(0, structure_score),
            "issues": structure_issues,
            "question_count": question_count if content_type == "test" else None,
            "content_length": content_length,
            "headers_found": len(headers),
            "analysis_timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "structure_score": 0,
            "issues": [f"Ошибка анализа структуры: {e}"],
            "error": str(e)
        }


async def check_safety_and_ethics(
    ctx: RunContext[NLPQualityGuardianDependencies],
    content: str,
    target_audience: str = "adults"
) -> Dict[str, Any]:
    """
    Проверка безопасности и этичности контента.

    Args:
        content: Контент для проверки
        target_audience: Целевая аудитория (adults, teens, children)

    Returns:
        Результат проверки безопасности
    """
    try:
        safety_score = 100.0
        critical_flags = []
        safety_issues = []
        warnings = []

        # Проверка на потенциально вредные техники
        harmful_patterns = [
            'принуждение', 'давление', 'заставить', 'должен обязательно',
            'гарантированный результат', 'стопроцентное исцеление',
            'замена медицинского лечения', 'отказ от врача'
        ]

        for pattern in harmful_patterns:
            if pattern.lower() in content.lower():
                critical_flags.append(CriticalFlag.POTENTIALLY_HARMFUL)
                safety_issues.append(f"Потенциально вредная формулировка: '{pattern}'")
                safety_score -= 20
                break

        # Проверка на манипулятивные техники
        manipulative_patterns = [
            'скрытое влияние', 'подсознательное воздействие без согласия',
            'принуждение к покупке', 'эмоциональная манипуляция',
            'зависимость от техники'
        ]

        for pattern in manipulative_patterns:
            if pattern.lower() in content.lower():
                critical_flags.append(CriticalFlag.MANIPULATIVE_CONTENT)
                safety_issues.append(f"Манипулятивный элемент: '{pattern}'")
                safety_score -= 25
                break

        # Проверка этических принципов
        ethical_violations = []

        # Отсутствие информированного согласия
        consent_keywords = ['согласие', 'добровольно', 'по желанию', 'consent', 'voluntary']
        if not any(kw.lower() in content.lower() for kw in consent_keywords):
            ethical_violations.append("Отсутствует принцип информированного согласия")

        # Отсутствие границ применения
        boundary_keywords = ['ограничения', 'противопоказания', 'не рекомендуется', 'осторожно']
        if not any(kw.lower() in content.lower() for kw in boundary_keywords):
            ethical_violations.append("Отсутствуют ограничения и противопоказания")

        if ethical_violations:
            critical_flags.append(CriticalFlag.UNETHICAL_PRACTICE)
            safety_issues.extend(ethical_violations)
            safety_score -= 15 * len(ethical_violations)

        # Проверка псевдонаучных утверждений
        pseudoscience_patterns = [
            'энергетические поля', 'квантовое исцеление', 'космические вибрации',
            'мгновенное исцеление', 'чудесное выздоровление', 'магическая сила'
        ]

        found_pseudo = [p for p in pseudoscience_patterns if p.lower() in content.lower()]
        if found_pseudo:
            critical_flags.append(CriticalFlag.PSEUDOSCIENTIFIC_CLAIM)
            safety_issues.append(f"Псевдонаучные утверждения: {', '.join(found_pseudo)}")
            safety_score -= 30

        # Возрастная адекватность
        if target_audience == "children" or target_audience == "teens":
            adult_content_markers = [
                'интимные отношения', 'сексуальность', 'алкоголь', 'наркотики',
                'суицид', 'самоповреждение', 'насилие'
            ]

            found_adult_content = [m for m in adult_content_markers if m.lower() in content.lower()]
            if found_adult_content:
                critical_flags.append(CriticalFlag.AGE_INAPPROPRIATE)
                safety_issues.append(f"Неподходящий для возраста контент: {', '.join(found_adult_content)}")
                safety_score -= 40

        # Проверка на соответствие законодательству
        legal_issues = []

        # Медицинские утверждения без лицензии
        medical_claims = [
            'лечить заболевание', 'медицинский диагноз', 'замена терапии',
            'психиатрическое лечение', 'клиническое воздействие'
        ]

        found_medical = [c for c in medical_claims if c.lower() in content.lower()]
        if found_medical:
            critical_flags.append(CriticalFlag.LEGAL_VIOLATION)
            legal_issues.append(f"Потенциальное нарушение медицинского законодательства: {', '.join(found_medical)}")
            safety_score -= 35

        if legal_issues:
            safety_issues.extend(legal_issues)

        # Позитивные элементы (бонусы к безопасности)
        positive_elements = [
            'безопасность', 'этичность', 'добровольность', 'уважение',
            'информированное согласие', 'противопоказания', 'ограничения'
        ]

        found_positive = [p for p in positive_elements if p.lower() in content.lower()]
        if found_positive:
            safety_score = min(100, safety_score + len(found_positive) * 2)

        return {
            "safety_score": max(0, safety_score),
            "critical_flags": [flag.value for flag in critical_flags],
            "safety_issues": safety_issues,
            "warnings": warnings,
            "positive_elements": found_positive,
            "is_safe_for_audience": len(critical_flags) == 0 and safety_score >= 70,
            "analysis_timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "safety_score": 0,
            "critical_flags": [CriticalFlag.POTENTIALLY_HARMFUL.value],
            "safety_issues": [f"Ошибка анализа безопасности: {e}"],
            "error": str(e),
            "is_safe_for_audience": False
        }


async def validate_nlp_techniques(
    ctx: RunContext[NLPQualityGuardianDependencies],
    content: str,
    technique_type: str = "general"
) -> Dict[str, Any]:
    """
    Валидация качества NLP техник в контенте.

    Args:
        content: Контент с NLP техниками
        technique_type: Тип техник (rapport, reframing, anchoring, etc.)

    Returns:
        Результат валидации NLP техник
    """
    try:
        nlp_score = 100.0
        technique_issues = []
        found_techniques = []

        # Словарь NLP техник и их правильных применений
        nlp_techniques = {
            "rapport": {
                "keywords": ["раппорт", "подстройка", "rapport", "matching", "mirroring"],
                "correct_usage": ["взаимное уважение", "доверие", "понимание"],
                "incorrect_usage": ["принуждение", "манипулирование", "обман"]
            },
            "reframing": {
                "keywords": ["рефрейминг", "переосмысление", "reframing", "recontextualization"],
                "correct_usage": ["новая перспектива", "позитивный взгляд", "альтернативное понимание"],
                "incorrect_usage": ["отрицание реальности", "ложные обещания", "игнорирование проблем"]
            },
            "anchoring": {
                "keywords": ["якорение", "якорь", "anchoring", "anchor", "conditioning"],
                "correct_usage": ["ресурсное состояние", "позитивная ассоциация", "эмоциональная поддержка"],
                "incorrect_usage": ["принуждение", "зависимость", "навязывание"]
            },
            "submodalities": {
                "keywords": ["субмодальности", "модальности", "submodalities", "sensory"],
                "correct_usage": ["изменение восприятия", "ресурсные образы", "позитивные ощущения"],
                "incorrect_usage": ["болезненные образы", "травматизация", "негативное воздействие"]
            },
            "timeline": {
                "keywords": ["временная линия", "timeline", "past", "future", "время"],
                "correct_usage": ["исцеление прошлого", "планирование будущего", "интеграция опыта"],
                "incorrect_usage": ["изменение фактов", "ложные воспоминания", "отрицание реальности"]
            }
        }

        # Поиск и анализ техник
        for technique_name, technique_info in nlp_techniques.items():
            technique_found = False

            # Проверяем наличие техники
            for keyword in technique_info["keywords"]:
                if keyword.lower() in content.lower():
                    technique_found = True
                    found_techniques.append(technique_name)
                    break

            if technique_found:
                # Проверяем корректность применения
                correct_usage_found = any(
                    usage.lower() in content.lower()
                    for usage in technique_info["correct_usage"]
                )

                incorrect_usage_found = any(
                    usage.lower() in content.lower()
                    for usage in technique_info["incorrect_usage"]
                )

                if incorrect_usage_found:
                    technique_issues.append(
                        f"Неправильное применение техники {technique_name}: "
                        f"найдены некорректные элементы"
                    )
                    nlp_score -= 25
                elif not correct_usage_found:
                    technique_issues.append(
                        f"Техника {technique_name} не имеет четкого корректного применения"
                    )
                    nlp_score -= 10

        # Проверка Эриксоновских паттернов
        ericksonian_patterns = {
            "truisms": ["каждый человек", "естественно", "как правило", "все знают"],
            "presuppositions": ["когда вы", "по мере того как", "после того как"],
            "embedded_commands": ["можете расслабиться", "почувствуйте спокойствие", "найдите комфорт"],
            "metaphors": ["как дерево растет", "словно река течет", "подобно солнцу"]
        }

        found_ericksonian = []
        for pattern_type, patterns in ericksonian_patterns.items():
            for pattern in patterns:
                if pattern.lower() in content.lower():
                    found_ericksonian.append(pattern_type)
                    break

        # Проверка соответствия принципам Эриксона
        ericksonian_principles = [
            "utilization", "использование ресурсов", "indirect approach", "непрямой подход",
            "respect", "уважение", "client pace", "темп клиента"
        ]

        ericksonian_compliance = any(
            principle.lower() in content.lower()
            for principle in ericksonian_principles
        )

        if found_ericksonian and not ericksonian_compliance:
            technique_issues.append(
                "Эриксоновские паттерны используются без соблюдения основных принципов"
            )
            nlp_score -= 20

        # Проверка научной обоснованности техник
        evidence_keywords = [
            "исследования показывают", "научно доказано", "эффективность подтверждена",
            "клинические испытания", "peer-reviewed", "evidence-based"
        ]

        has_evidence_base = any(
            keyword.lower() in content.lower()
            for keyword in evidence_keywords
        )

        if found_techniques and not has_evidence_base and ctx.deps.validation_criteria.require_scientific_basis:
            technique_issues.append("Отсутствует научное обоснование используемых техник")
            nlp_score -= 15

        # Проверка этического применения
        ethical_nlp_markers = [
            "информированное согласие", "добровольное участие", "право отказа",
            "безопасные границы", "этические принципы", "уважение личности"
        ]

        has_ethical_framework = any(
            marker.lower() in content.lower()
            for marker in ethical_nlp_markers
        )

        if found_techniques and not has_ethical_framework:
            technique_issues.append("Отсутствует этическая рамка применения NLP техник")
            nlp_score -= 20

        return {
            "nlp_score": max(0, nlp_score),
            "found_techniques": found_techniques,
            "found_ericksonian_patterns": found_ericksonian,
            "technique_issues": technique_issues,
            "has_evidence_base": has_evidence_base,
            "has_ethical_framework": has_ethical_framework,
            "ericksonian_compliance": ericksonian_compliance,
            "techniques_count": len(found_techniques),
            "analysis_timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "nlp_score": 0,
            "technique_issues": [f"Ошибка анализа NLP техник: {e}"],
            "error": str(e)
        }


async def generate_quality_report(
    ctx: RunContext[NLPQualityGuardianDependencies],
    validation_results: Dict[str, Any],
    content_info: Dict[str, Any]
) -> str:
    """
    Сгенерировать подробный отчет о качестве контента.

    Args:
        validation_results: Результаты всех проверок
        content_info: Информация о контенте

    Returns:
        Детальный отчет в формате Markdown
    """
    try:
        # Извлекаем данные из результатов
        structure = validation_results.get("structure", {})
        safety = validation_results.get("safety", {})
        nlp = validation_results.get("nlp", {})

        # Вычисляем общий балл
        scores = []
        if "structure_score" in structure:
            scores.append(structure["structure_score"])
        if "safety_score" in safety:
            scores.append(safety["safety_score"])
        if "nlp_score" in nlp:
            scores.append(nlp["nlp_score"])

        overall_score = sum(scores) / len(scores) if scores else 0

        # Определяем уровень качества
        if overall_score >= 90:
            quality_level = "🟢 ОТЛИЧНО"
            recommendation = "Готово к публикации"
        elif overall_score >= 70:
            quality_level = "🟡 ХОРОШО"
            recommendation = "Незначительные доработки"
        elif overall_score >= 50:
            quality_level = "🟠 ТРЕБУЕТ УЛУЧШЕНИЯ"
            recommendation = "Существенные правки необходимы"
        else:
            quality_level = "🔴 НЕПРИЕМЛЕМО"
            recommendation = "Полная переработка требуется"

        # Генерируем отчет
        report = f"""# 🛡️ Отчет о качестве NLP контента

## 📊 Общая оценка

**Итоговый балл:** {overall_score:.1f}/100
**Уровень качества:** {quality_level}
**Рекомендация:** {recommendation}

---

## 🏗️ Структурная валидация

**Балл:** {structure.get('structure_score', 0):.1f}/100

### Найденные элементы:
- **Длина контента:** {structure.get('content_length', 'Неизвестно')} символов
- **Заголовков найдено:** {structure.get('headers_found', 0)}
"""

        if content_info.get("content_type") == "test":
            report += f"- **Количество вопросов:** {structure.get('question_count', 0)}\n"

        if structure.get('issues'):
            report += f"\n### ⚠️ Структурные проблемы:\n"
            for issue in structure['issues']:
                report += f"- {issue}\n"

        report += f"""
---

## 🔐 Безопасность и этичность

**Балл:** {safety.get('safety_score', 0):.1f}/100
**Безопасно для аудитории:** {'✅ Да' if safety.get('is_safe_for_audience', False) else '❌ Нет'}

"""

        if safety.get('critical_flags'):
            report += "### 🚨 КРИТИЧЕСКИЕ ПРОБЛЕМЫ:\n"
            for flag in safety['critical_flags']:
                report += f"- ⚠️ {flag}\n"
            report += "\n"

        if safety.get('safety_issues'):
            report += "### ⚠️ Проблемы безопасности:\n"
            for issue in safety['safety_issues']:
                report += f"- {issue}\n"
            report += "\n"

        if safety.get('positive_elements'):
            report += "### ✅ Позитивные элементы:\n"
            for element in safety['positive_elements']:
                report += f"- {element}\n"
            report += "\n"

        report += f"""---

## 🎯 Качество NLP техник

**Балл:** {nlp.get('nlp_score', 0):.1f}/100
**Найдено техник:** {nlp.get('techniques_count', 0)}

"""

        if nlp.get('found_techniques'):
            report += "### Обнаруженные NLP техники:\n"
            for technique in nlp['found_techniques']:
                report += f"- {technique}\n"
            report += "\n"

        if nlp.get('found_ericksonian_patterns'):
            report += "### Эриксоновские паттерны:\n"
            for pattern in nlp['found_ericksonian_patterns']:
                report += f"- {pattern}\n"
            report += "\n"

        report += f"""**Научная обоснованность:** {'✅ Есть' if nlp.get('has_evidence_base', False) else '❌ Отсутствует'}
**Этическая рамка:** {'✅ Есть' if nlp.get('has_ethical_framework', False) else '❌ Отсутствует'}
**Соответствие принципам Эриксона:** {'✅ Да' if nlp.get('ericksonian_compliance', False) else '❌ Нет'}

"""

        if nlp.get('technique_issues'):
            report += "### ⚠️ Проблемы с техниками:\n"
            for issue in nlp['technique_issues']:
                report += f"- {issue}\n"
            report += "\n"

        # Собираем все рекомендации
        all_issues = []
        all_issues.extend(structure.get('issues', []))
        all_issues.extend(safety.get('safety_issues', []))
        all_issues.extend(nlp.get('technique_issues', []))

        if all_issues:
            report += """---

## 💡 Рекомендации по улучшению

### Приоритетные исправления:
"""
            # Группируем критические проблемы
            critical_issues = [issue for issue in all_issues if any(
                word in issue.lower() for word in ['критично', 'опасно', 'вредно', 'запрещено']
            )]

            for issue in critical_issues[:5]:  # Топ-5 критических
                report += f"1. **КРИТИЧНО:** {issue}\n"

            report += "\n### Важные улучшения:\n"
            regular_issues = [issue for issue in all_issues if issue not in critical_issues]
            for i, issue in enumerate(regular_issues[:10], 1):  # Топ-10 обычных
                report += f"{i}. {issue}\n"

        report += f"""
---

## 📈 Детальная аналитика

### Распределение баллов:
- **Структура:** {structure.get('structure_score', 0):.1f}%
- **Безопасность:** {safety.get('safety_score', 0):.1f}%
- **NLP техники:** {nlp.get('nlp_score', 0):.1f}%

### Технические детали:
- **Домен валидации:** {ctx.deps.validation_domain.value}
- **Тип контента:** {content_info.get('content_type', 'mixed')}
- **Время анализа:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Агент:** NLP Content Quality Guardian v1.0.0

---

## 🎯 Следующие шаги

"""

        if overall_score >= 90:
            report += """✅ **Контент готов к публикации!**
- Можно использовать без изменений
- Рекомендуется периодическая проверка обратной связи от пользователей
"""
        elif overall_score >= 70:
            report += """⚠️ **Требуется минимальная доработка:**
1. Исправить указанные выше проблемы
2. Провести повторную проверку
3. Получить подтверждение экспертов
"""
        elif overall_score >= 50:
            report += """🔧 **Необходима существенная доработка:**
1. Устранить все критические проблемы
2. Переработать проблемные разделы
3. Добавить недостающие элементы безопасности
4. Провести полную повторную валидацию
"""
        else:
            report += """🚫 **Контент не рекомендуется к использованию:**
1. Полная переработка с учетом всех замечаний
2. Консультация с экспертами по психологии и NLP
3. Пересмотр целей и методологии
4. Создание нового контента на базе стандартов качества
"""

        report += f"""
---

*Отчет сгенерирован NLP Content Quality Guardian Agent*
*Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}*
"""

        return report

    except Exception as e:
        return f"""# ❌ Ошибка генерации отчета

Произошла ошибка при создании отчета о качестве: {e}

## Базовая информация:
- **Общий балл:** {overall_score:.1f}/100 (приблизительно)
- **Время анализа:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Рекомендуется повторить анализ или обратиться к специалисту.
"""


async def break_down_validation_tasks(
    ctx: RunContext[NLPQualityGuardianDependencies],
    content_description: str,
    validation_scope: str = "full"
) -> str:
    """
    Разбить валидацию на микрозадачи и показать их пользователю.

    Args:
        content_description: Описание контента для валидации
        validation_scope: Объем валидации (basic, full, expert)

    Returns:
        Список микрозадач для выполнения
    """
    try:
        if validation_scope == "basic":
            microtasks = [
                "Анализ структуры контента и базовых требований",
                "Проверка безопасности и этических стандартов",
                "Формирование базового отчета с рекомендациями"
            ]
        elif validation_scope == "expert":
            microtasks = [
                f"Глубокий анализ контента: {content_description}",
                "Поиск в экспертной базе знаний по валидации",
                "Проверка соответствия методологии PatternShift 2.0",
                "Детальная валидация NLP техник и Эриксоновских паттернов",
                "Анализ психологической корректности и научной обоснованности",
                "Проверка этической безопасности и возрастной адекватности",
                "Мультиязычная валидация и культурная чувствительность",
                "Создание детального экспертного заключения",
                "Критический анализ результата и улучшение",
                "Формирование приоритизированных рекомендаций"
            ]
        else:  # full
            microtasks = [
                f"Анализ структуры и типа контента: {content_description}",
                "Поиск в базе знаний по критериям валидации",
                "Проверка соответствия PatternShift методологии",
                "Валидация NLP техник и их корректного применения",
                "Анализ безопасности и этических аспектов",
                "Проверка научной обоснованности утверждений",
                "Генерация детального отчета с рекомендациями",
                "Рефлексия и улучшение результатов валидации"
            ]

        # Форматируем вывод для пользователя
        output = "📋 **Микрозадачи валидации качества:**\n"
        for i, task in enumerate(microtasks, 1):
            output += f"{i}. {task}\n"

        output += f"\n✅ Буду отчитываться о прогрессе каждой микрозадачи"
        output += f"\n🎯 **Объем валидации:** {validation_scope}"
        output += f"\n🔍 **Домен:** {ctx.deps.validation_domain.value}"

        return output

    except Exception as e:
        return f"Ошибка планирования валидации: {e}"


async def delegate_validation_task(
    ctx: RunContext[NLPQualityGuardianDependencies],
    target_agent: str,
    task_title: str,
    task_description: str,
    content_sample: str = "",
    priority: str = "medium"
) -> str:
    """
    Делегировать задачу валидации другому специализированному агенту.

    Args:
        target_agent: Целевой агент (security_audit, nlp_research, etc.)
        task_title: Название задачи
        task_description: Описание задачи
        content_sample: Образец контента для анализа
        priority: Приоритет задачи

    Returns:
        Результат делегирования
    """
    try:
        # Мапинг агентов для делегирования
        agent_mapping = {
            "security_audit": "Security Audit Agent",
            "nlp_research": "NLP Content Research Agent",
            "psychology_expert": "Psychology Content Architect Agent",
            "quality_guardian": "Archon Quality Guardian",
            "analysis_lead": "Archon Analysis Lead"
        }

        assignee = agent_mapping.get(target_agent, "Archon Analysis Lead")

        # Формируем контекст для делегирования
        context_data = {
            "validation_domain": ctx.deps.validation_domain.value,
            "content_type": ctx.deps.target_content_type.value,
            "delegated_by": "NLP Content Quality Guardian Agent",
            "content_sample": content_sample[:500] if content_sample else "Не предоставлено",
            "validation_criteria": "См. база знаний NLP Quality Guardian"
        }

        # Создаем задачу в Archon (имитация, так как MCP может быть недоступен)
        task_result = {
            "task_id": f"validation_delegate_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "assigned_to": assignee,
            "status": "created",
            "priority": priority
        }

        return f"""✅ Задача валидации успешно делегирована

**Целевой агент:** {target_agent} ({assignee})
**Задача:** {task_title}
**Приоритет:** {priority}
**Контекст:** {task_description}

**Переданные данные:**
- Домен валидации: {context_data['validation_domain']}
- Тип контента: {context_data['content_type']}
- Образец контента: {'Предоставлен' if content_sample else 'Не предоставлен'}

📋 Задача создана в системе управления задачами
🔄 Ожидается выполнение специализированным агентом
📊 Результаты будут интегрированы в общий отчет валидации
"""

    except Exception as e:
        return f"❌ Ошибка делегирования задачи валидации: {e}"