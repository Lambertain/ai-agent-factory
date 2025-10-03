# -*- coding: utf-8 -*-
"""
Специализированные инструменты Pattern Gender Adaptation Agent.

Инструменты для адаптации психологического контента под гендерные паттерны.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import PatternGenderAdaptationDependencies


class GenderAnalysisResult(BaseModel):
    """Результат анализа гендерных паттернов."""
    masculine_elements: List[str] = Field(description="Маскулинные элементы")
    feminine_elements: List[str] = Field(description="Фемининные элементы")
    neutral_elements: List[str] = Field(description="Нейтральные элементы")
    stereotypes_found: List[str] = Field(description="Найденные стереотипы")


class AdaptedModule(BaseModel):
    """Адаптированный модуль."""
    version: str = Field(description="masculine/feminine/neutral")
    module_id: str = Field(description="ID модуля")
    content: Dict[str, Any] = Field(description="Контент модуля")
    adaptations: List[str] = Field(description="Список адаптаций")
    validated: bool = Field(default=False, description="Проверен на стереотипы")


async def analyze_gender_patterns(
    ctx: RunContext[PatternGenderAdaptationDependencies],
    module_content: Dict[str, Any]
) -> str:
    """
    Анализирует гендерные паттерны в модуле контента.

    Args:
        ctx: Контекст выполнения
        module_content: Контент модуля для анализа

    Returns:
        Результаты анализа в JSON формате
    """
    # Маскулинные маркеры
    masculine_markers = [
        "достиж", "побед", "сил", "контрол", "власт", "конкурен",
        "преодоле", "борь", "стратег", "эффективност", "результат"
    ]

    # Фемининные маркеры
    feminine_markers = [
        "чувств", "эмоци", "связ", "отношени", "гармони", "забот",
        "поддержк", "сотрудничеств", "интуици", "эмпати", "рост"
    ]

    # Стереотипы
    stereotypes = [
        "все мужчины", "все женщины", "типично мужской",
        "типично женский", "настоящий мужчина", "настоящая женщина"
    ]

    text = str(module_content).lower()

    result = GenderAnalysisResult(
        masculine_elements=[m for m in masculine_markers if m in text],
        feminine_elements=[f for f in feminine_markers if f in text],
        neutral_elements=[] if any(m in text for m in masculine_markers + feminine_markers) else ["Нейтральный контент"],
        stereotypes_found=[s for s in stereotypes if s in text]
    )

    return result.model_dump_json(indent=2)


async def adapt_for_masculine(
    ctx: RunContext[PatternGenderAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для маскулинной аудитории.

    Применяет:
    - Прямую, деловую коммуникацию
    - Акцент на логику, стратегию, эффективность
    - Примеры из спорта, бизнеса, технологий
    - Метафоры достижения и преодоления

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    # Замены для маскулинной аудитории
    replacements = {
        "почувствуй": "осознай",
        "соединись с собой": "достигни понимания",
        "раскрой потенциал": "реализуй возможности",
        "гармония": "баланс",
        "забота о себе": "самоконтроль"
    }

    # Применяем замены
    for key, value in adapted.items():
        if isinstance(value, str):
            for old, new in replacements.items():
                if old in value.lower():
                    adapted[key] = value.replace(old, new)
                    adaptations.append(f"Заменено '{old}' на '{new}'")

    result = AdaptedModule(
        version="masculine",
        module_id=module_id,
        content=adapted,
        adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def adapt_for_feminine(
    ctx: RunContext[PatternGenderAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Адаптирует модуль для фемининной аудитории.

    Применяет:
    - Эмпатичную, поддерживающую коммуникацию
    - Акцент на эмоции, интуицию, связь
    - Примеры из отношений, природы, творчества
    - Метафоры роста и гармонии

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Адаптированный модуль в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    # Замены для фемининной аудитории
    replacements = {
        "достигни": "позволь себе достичь",
        "контролируй": "осознавай и направляй",
        "преодолей": "трансформируй",
        "эффективность": "гармоничность",
        "результат": "процесс роста"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            for old, new in replacements.items():
                if old in value.lower():
                    adapted[key] = value.replace(old, new)
                    adaptations.append(f"Заменено '{old}' на '{new}'")

    result = AdaptedModule(
        version="feminine",
        module_id=module_id,
        content=adapted,
        adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def create_neutral_version(
    ctx: RunContext[PatternGenderAdaptationDependencies],
    module_content: Dict[str, Any],
    module_id: str
) -> str:
    """
    Создает гендерно-нейтральную версию модуля.

    Применяет:
    - Инклюзивный, открытый язык
    - Баланс логики и эмоций
    - Универсальные метафоры

    Args:
        ctx: Контекст выполнения
        module_content: Исходный контент модуля
        module_id: ID модуля

    Returns:
        Нейтральная версия модуля в JSON
    """
    adaptations = []
    adapted = module_content.copy()

    # Нейтрализация языка
    replacements = {
        "он": "человек",
        "она": "человек",
        "мужчина": "человек",
        "женщина": "человек",
        "победа": "успех",
        "борьба": "процесс"
    }

    for key, value in adapted.items():
        if isinstance(value, str):
            for old, new in replacements.items():
                if old in value.lower():
                    adapted[key] = value.replace(old, new)
                    adaptations.append(f"Нейтрализовано: '{old}' → '{new}'")

    result = AdaptedModule(
        version="neutral",
        module_id=module_id,
        content=adapted,
        adaptations=adaptations,
        validated=False
    )

    return result.model_dump_json(indent=2)


async def validate_stereotypes(
    ctx: RunContext[PatternGenderAdaptationDependencies],
    adapted_module_json: str
) -> str:
    """
    Валидирует адаптированный модуль на отсутствие токсичных стереотипов.

    Args:
        ctx: Контекст выполнения
        adapted_module_json: JSON адаптированного модуля

    Returns:
        Результаты валидации
    """
    import json

    module = json.loads(adapted_module_json)
    text = str(module.get("content", "")).lower()

    # Токсичные паттерны
    toxic_patterns = [
        "все мужчины", "все женщины", "типично мужской",
        "типично женский", "настоящий мужчина", "настоящая женщина",
        "мужчины должны", "женщины должны", "мужчины не", "женщины не"
    ]

    issues = [pattern for pattern in toxic_patterns if pattern in text]

    result = {
        "is_valid": len(issues) == 0,
        "issues_found": issues,
        "recommendations": [
            f"Заменить '{issue}' на инклюзивную формулировку" for issue in issues
        ],
        "module_id": module.get("module_id"),
        "version": module.get("version")
    }

    return json.dumps(result, indent=2, ensure_ascii=False)
