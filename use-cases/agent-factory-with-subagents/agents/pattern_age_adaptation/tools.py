# -*- coding: utf-8 -*-
"""
Специализированные инструменты Pattern Age Adaptation Agent.

Инструменты для адаптации психологического контента под возрастные особенности.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import PatternAgeAdaptationDependencies


class AgeAnalysisResult(BaseModel):
    """Результат анализа возрастных аспектов."""
    age_appropriate_elements: List[str] = Field(description="Подходящие возрастные элементы")
    complexity_level: str = Field(description="Уровень сложности контента")
    recommended_ages: List[str] = Field(description="Рекомендуемые возрастные группы")
    developmental_tasks_addressed: List[str] = Field(description="Затронутые задачи развития")


class AgeAdaptedModule(BaseModel):
    """Возрастно-адаптированный модуль."""
    version: str = Field(description="Возрастная версия")
    age_range: str = Field(description="Возрастной диапазон")
    developmental_task: str = Field(description="Задача развития")
    module_id: str = Field(description="ID модуля")
    content: Dict[str, Any] = Field(description="Контент модуля")
    age_adaptations: List[str] = Field(description="Список адаптаций")
    validated: bool = Field(default=False, description="Проверен на соответствие развитию")


async def analyze_age_patterns(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any]
) -> str:
    """
    Анализирует возрастные аспекты модуля контента.

    Args:
        ctx: Контекст выполнения
        module_content: Контент модуля для анализа

    Returns:
        Результаты анализа в JSON формате
    """
    text = str(module_content).lower()

    # Маркеры для разных возрастов
    teens_markers = ["школ", "друз", "сверстник", "родител", "иденти", "самооценк"]
    young_markers = ["карьер", "отношени", "независим", "самостоятел", "цел", "успех"]
    middle_markers = ["семь", "работ", "баланс", "ответственност", "смысл", "опыт"]
    senior_markers = ["мудрост", "наследи", "приняти", "интеграци", "жизненный путь"]

    # Определяем уровень сложности
    complexity_indicators = {
        "simple": ["просто", "легко", "быстро", "шаг за шагом"],
        "medium": ["рассмотр", "подум", "проанализ", "поним"],
        "complex": ["глубин", "фундамент", "философ", "экзистенци", "сложн"]
    }

    complexity = "medium"
    for level, indicators in complexity_indicators.items():
        if any(ind in text for ind in indicators):
            complexity = level
            break

    result = AgeAnalysisResult(
        age_appropriate_elements=[],
        complexity_level=complexity,
        recommended_ages=[],
        developmental_tasks_addressed=[]
    )

    # Определяем подходящие возрастные группы
    if any(m in text for m in teens_markers):
        result.recommended_ages.append("teens")
        result.developmental_tasks_addressed.append("identity_formation")

    if any(m in text for m in young_markers):
        result.recommended_ages.append("young_adults")
        result.developmental_tasks_addressed.append("intimacy_vs_isolation")

    if any(m in text for m in middle_markers):
        result.recommended_ages.extend(["early_middle_age", "middle_age"])
        result.developmental_tasks_addressed.extend(["generativity_beginning", "generativity_peak"])

    if any(m in text for m in senior_markers):
        result.recommended_ages.append("seniors")
        result.developmental_tasks_addressed.append("integrity_vs_despair")

    return result.model_dump_json(indent=2)


async def adapt_for_teens(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для подростков (14-18 лет).

    Применяет:
    - Энергичный язык, близкий к молодежному
    - Примеры из школьной жизни, социальных сетей
    - Метафоры открытия себя, квеста
    - Короткие предложения и сессии

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    # Замены для подростков
    replacements = {
        "достигните": "открой в себе",
        "проанализируйте": "посмотри на это так",
        "осознайте": "пойми",
        "эффективность": "крутой результат",
        "стратегия": "план действий",
        "ресурсное состояние": "когда ты на подъеме",
        "глубинные процессы": "что реально происходит внутри"
    }

    # Применяем замены
    for key, value in adapted.items():
        if isinstance(value, str):
            original = value
            for old, new in replacements.items():
                if old in value.lower():
                    value = value.replace(old, new)
            if value != original:
                adapted[key] = value
                adaptations.append(f"Адаптировано поле '{key}' для подростков")

    result = AgeAdaptedModule(
        version="teens",
        age_range=ctx.deps.get_age_range("teens"),
        developmental_task=ctx.deps.get_developmental_task("teens"),
        module_id=f"{module_id}_teens",
        content=adapted,
        age_adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def adapt_for_young_adults(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для молодых взрослых (19-25 лет).

    Применяет:
    - Современный, динамичный язык
    - Примеры из карьеры, отношений, саморазвития
    - Метафоры строительства и восхождения
    - Практичность и быстрые результаты

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    replacements = {
        "детский опыт": "предыдущий опыт",
        "мудрость лет": "накопленный опыт",
        "в вашем возрасте": "на этом этапе жизни",
        "долгосрочные цели": "цели на ближайшие годы",
        "жизненный путь": "карьерный трек и личный рост"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            original = value
            for old, new in replacements.items():
                if old in value.lower():
                    value = value.replace(old, new)
            if value != original:
                adapted[key] = value
                adaptations.append(f"Адаптировано поле '{key}' для молодых взрослых")

    result = AgeAdaptedModule(
        version="young_adults",
        age_range=ctx.deps.get_age_range("young_adults"),
        developmental_task=ctx.deps.get_developmental_task("young_adults"),
        module_id=f"{module_id}_young_adults",
        content=adapted,
        age_adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def adapt_for_early_middle_age(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для раннего среднего возраста (26-35 лет).

    Применяет:
    - Деловой, четкий язык
    - Примеры из work-life balance, семьи, карьеры
    - Метафоры баланса и мастерства
    - Системный подход

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    replacements = {
        "поиск себя": "оптимизация ролей",
        "кто я": "баланс профессионального и личного",
        "экспериментируй": "стратегически выбирай",
        "попробуй": "внедри системно"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            original = value
            for old, new in replacements.items():
                if old in value.lower():
                    value = value.replace(old, new)
            if value != original:
                adapted[key] = value
                adaptations.append(f"Адаптировано поле '{key}' для раннего среднего возраста")

    result = AgeAdaptedModule(
        version="early_middle_age",
        age_range=ctx.deps.get_age_range("early_middle_age"),
        developmental_task=ctx.deps.get_developmental_task("early_middle_age"),
        module_id=f"{module_id}_early_middle_age",
        content=adapted,
        age_adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def adapt_for_middle_age(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для среднего возраста (36-50 лет).

    Применяет:
    - Зрелый, глубокий язык
    - Примеры из наставничества, смысла жизни
    - Метафоры мудрости и передачи опыта
    - Глубинная работа и рефлексия

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    replacements = {
        "достижение целей": "вклад в развитие других",
        "личный успех": "создание наследия",
        "карьерный рост": "передача опыта",
        "самореализация": "генеративность и смысл"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            original = value
            for old, new in replacements.items():
                if old in value.lower():
                    value = value.replace(old, new)
            if value != original:
                adapted[key] = value
                adaptations.append(f"Адаптировано поле '{key}' для среднего возраста")

    result = AgeAdaptedModule(
        version="middle_age",
        age_range=ctx.deps.get_age_range("middle_age"),
        developmental_task=ctx.deps.get_developmental_task("middle_age"),
        module_id=f"{module_id}_middle_age",
        content=adapted,
        age_adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def adapt_for_seniors(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для старшего возраста (50+ лет).

    Применяет:
    - Уважительный, мудрый язык
    - Примеры из жизненного опыта, наследия
    - Метафоры интеграции и мудрости
    - Созерцательный подход

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    replacements = {
        "начни путь": "интегрируй опыт",
        "открой новое": "переосмысли прожитое",
        "достигни цели": "найди мудрость в пройденном",
        "быстрый результат": "глубокое понимание",
        "экспериментируй": "используй богатый опыт"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            original = value
            for old, new in replacements.items():
                if old in value.lower():
                    value = value.replace(old, new)
            if value != original:
                adapted[key] = value
                adaptations.append(f"Адаптировано поле '{key}' для старшего возраста")

    result = AgeAdaptedModule(
        version="seniors",
        age_range=ctx.deps.get_age_range("seniors"),
        developmental_task=ctx.deps.get_developmental_task("seniors"),
        module_id=f"{module_id}_seniors",
        content=adapted,
        age_adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def validate_developmental_tasks(
    ctx: RunContext[PatternAgeAdaptationDependencies],
    adapted_module_json: str
) -> str:
    """
    Валидирует адаптированный модуль на соответствие задачам развития.

    Args:
        ctx: Контекст выполнения
        adapted_module_json: JSON адаптированного модуля

    Returns:
        Результаты валидации
    """
    import json

    module = json.loads(adapted_module_json)
    age_version = module.get("version")
    content = str(module.get("content", "")).lower()
    developmental_task = ctx.deps.get_developmental_task(age_version)

    # Критерии для каждой задачи развития
    developmental_criteria = {
        "identity_formation": [
            "поиск себя", "идентичност", "кто я", "самоопределени", "выбор"
        ],
        "intimacy_vs_isolation": [
            "отношени", "близость", "связ", "партнер", "самостоятел"
        ],
        "generativity_beginning": [
            "вклад", "создани", "баланс", "развити", "продуктивност"
        ],
        "generativity_peak": [
            "наставничеств", "передач", "наследи", "смысл", "генеративност"
        ],
        "integrity_vs_despair": [
            "приняти", "интеграци", "мудрост", "жизненный путь", "завершенност"
        ]
    }

    criteria = developmental_criteria.get(developmental_task, [])
    matches = [c for c in criteria if c in content]

    result = {
        "is_valid": len(matches) > 0,
        "developmental_task": developmental_task,
        "age_version": age_version,
        "age_range": ctx.deps.get_age_range(age_version),
        "criteria_matched": matches,
        "criteria_missing": [c for c in criteria if c not in matches],
        "recommendations": []
    }

    if not result["is_valid"]:
        result["recommendations"].append(
            f"Добавить элементы, соответствующие задаче развития: {developmental_task}"
        )

    return json.dumps(result, indent=2, ensure_ascii=False)
