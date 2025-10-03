"""
Примеры конфигураций для Pattern VAK Adaptation Specialist Agent.

Содержит готовые конфигурации для различных типов модулей PatternShift
и примеры адаптации под разные VAK модальности.
"""

from .nlp_techniques_config import (
    create_nlp_techniques_config,
    get_nlp_adaptation_example,
    create_custom_nlp_config,
    NLP_TECHNIQUES_EXAMPLES,
    NLP_THERAPY_CONFIG,
    NLP_COACHING_CONFIG,
    NLP_EDUCATION_CONFIG
)

from .meditation_config import (
    create_meditation_config,
    get_meditation_adaptation_example,
    create_meditation_program_config,
    MEDITATION_EXAMPLES,
    MEDITATION_THERAPY_CONFIG,
    MEDITATION_WELLNESS_CONFIG,
    MEDITATION_CORPORATE_CONFIG
)

from .visualization_movement_config import (
    create_visualization_config,
    create_movement_config,
    get_visualization_example,
    get_movement_example,
    VISUALIZATION_EXAMPLES,
    MOVEMENT_EXAMPLES,
    VISUALIZATION_THERAPY_CONFIG,
    MOVEMENT_TRAUMA_CONFIG
)

from typing import Dict, Any, List
from ..dependencies import VAKModalityType, PatternShiftModuleType


def get_example_for_module_type(
    module_type: PatternShiftModuleType,
    modality: VAKModalityType,
    specific_technique: str = None
) -> Dict[str, Any]:
    """
    Получить пример адаптации для конкретного типа модуля PatternShift.

    Args:
        module_type: Тип модуля PatternShift
        modality: Целевая VAK модальность
        specific_technique: Конкретная техника (опционально)

    Returns:
        Словарь с примером адаптации
    """
    try:
        if module_type == PatternShiftModuleType.TECHNIQUE:
            technique = specific_technique or "anchoring"
            return get_nlp_adaptation_example(technique, modality)

        elif module_type == PatternShiftModuleType.MEDITATION:
            practice = specific_technique or "breath_awareness"
            return get_meditation_adaptation_example(practice, modality)

        elif module_type == PatternShiftModuleType.VISUALIZATION:
            technique = specific_technique or "safe_place"
            return get_visualization_example(technique, modality)

        elif module_type == PatternShiftModuleType.MOVEMENT:
            practice = specific_technique or "grounding"
            return get_movement_example(practice, modality)

        elif module_type == PatternShiftModuleType.AUDIO_SESSION:
            # Аудио сессии лучше всего адаптируются через медитативные практики
            practice = specific_technique or "breath_awareness"
            return get_meditation_adaptation_example(practice, modality)

        elif module_type == PatternShiftModuleType.EXERCISE:
            # Упражнения близки к НЛП техникам
            technique = specific_technique or "reframing"
            return get_nlp_adaptation_example(technique, modality)

        elif module_type == PatternShiftModuleType.ASSESSMENT:
            # Для оценочных инструментов используем базовые принципы адаптации
            return {
                "title": f"Адаптация оценочного инструмента для {modality.value}",
                "content": _get_assessment_adaptation_content(modality),
                "key_elements": _get_assessment_key_elements(modality),
                "special_notes": "Сохраняйте валидность инструмента при адаптации"
            }

        elif module_type == PatternShiftModuleType.REFLECTION:
            # Рефлексивные практики адаптируются как НЛП техники
            technique = specific_technique or "six_step_reframe"
            return get_nlp_adaptation_example(technique, modality)

        else:
            return {"error": f"Неподдерживаемый тип модуля: {module_type}"}

    except Exception as e:
        return {"error": f"Ошибка при получении примера: {str(e)}"}


def _get_assessment_adaptation_content(modality: VAKModalityType) -> str:
    """Получить содержимое адаптации для оценочных инструментов."""

    if modality == VAKModalityType.VISUAL:
        return """
        Адаптация оценочного инструмента для визуальной модальности:

        - Используйте схемы, диаграммы и визуальные шкалы
        - Представляйте вопросы в виде картинок или метафор
        - Применяйте цветовое кодирование для категорий ответов
        - Предлагайте визуализировать ответы на шкале или графике
        - Используйте пространственные метафоры (выше-ниже, ближе-дальше)
        """

    elif modality == VAKModalityType.AUDITORY:
        return """
        Адаптация оценочного инструмента для аудиальной модальности:

        - Читайте вопросы вслух с соответствующей интонацией
        - Используйте ритмичную подачу вопросов
        - Предлагайте проговаривать ответы вслух
        - Включайте элементы внутреннего диалога
        - Используйте звуковые метафоры и аналогии
        """

    else:  # KINESTHETIC
        return """
        Адаптация оценочного инструмента для кинестетической модальности:

        - Предлагайте "почувствовать" правильность ответа
        - Используйте физические движения для выражения ответов
        - Включайте телесные ощущения в формулировки вопросов
        - Предоставляйте время для "внутреннего ощущения" ответа
        - Используйте тактильные и соматические метафоры
        """


def _get_assessment_key_elements(modality: VAKModalityType) -> List[str]:
    """Получить ключевые элементы для адаптации оценочных инструментов."""

    elements_map = {
        VAKModalityType.VISUAL: [
            "визуальные шкалы",
            "схематичное представление",
            "цветовое кодирование",
            "пространственная организация"
        ],
        VAKModalityType.AUDITORY: [
            "вербальная подача",
            "ритмичная структура",
            "проговаривание ответов",
            "звуковые аналогии"
        ],
        VAKModalityType.KINESTHETIC: [
            "телесные ощущения",
            "физические движения",
            "соматические метафоры",
            "интуитивные реакции"
        ]
    }

    return elements_map.get(modality, [])


def get_all_available_examples() -> Dict[str, List[str]]:
    """
    Получить список всех доступных примеров по категориям.

    Returns:
        Словарь с категориями и списками доступных техник
    """
    return {
        "nlp_techniques": list(NLP_TECHNIQUES_EXAMPLES.keys()),
        "meditation_practices": list(MEDITATION_EXAMPLES.keys()),
        "visualization_techniques": list(VISUALIZATION_EXAMPLES.keys()),
        "movement_practices": list(MOVEMENT_EXAMPLES.keys())
    }


def get_recommended_config_for_context(
    context: str,
    api_key: str
) -> Dict[str, Any]:
    """
    Получить рекомендуемую конфигурацию для конкретного контекста использования.

    Args:
        context: Контекст использования (therapy, coaching, education, corporate, wellness)
        api_key: API ключ для создания зависимостей

    Returns:
        Рекомендуемая конфигурация
    """
    context_configs = {
        "therapy": {
            "nlp": NLP_THERAPY_CONFIG,
            "meditation": MEDITATION_THERAPY_CONFIG,
            "visualization": VISUALIZATION_THERAPY_CONFIG,
            "movement": MOVEMENT_TRAUMA_CONFIG,
            "dependencies": create_nlp_techniques_config(api_key)
        },
        "coaching": {
            "nlp": NLP_COACHING_CONFIG,
            "meditation": MEDITATION_WELLNESS_CONFIG,
            "recommended_focus": "goal_achievement",
            "dependencies": create_nlp_techniques_config(api_key)
        },
        "education": {
            "nlp": NLP_EDUCATION_CONFIG,
            "meditation": MEDITATION_WELLNESS_CONFIG,
            "recommended_focus": "learning_enhancement",
            "dependencies": create_meditation_config(api_key)
        },
        "corporate": {
            "meditation": MEDITATION_CORPORATE_CONFIG,
            "recommended_focus": "stress_reduction",
            "time_constraints": "short_sessions",
            "dependencies": create_meditation_config(api_key)
        },
        "wellness": {
            "meditation": MEDITATION_WELLNESS_CONFIG,
            "visualization": {"accessibility_focus": True},
            "recommended_focus": "general_wellbeing",
            "dependencies": create_meditation_config(api_key)
        }
    }

    return context_configs.get(context, {
        "error": f"Неизвестный контекст: {context}",
        "available_contexts": list(context_configs.keys())
    })


def create_multi_modal_example_set(
    technique_name: str,
    module_type: PatternShiftModuleType
) -> Dict[str, Any]:
    """
    Создать набор примеров для всех модальностей для одной техники.

    Args:
        technique_name: Название техники
        module_type: Тип модуля PatternShift

    Returns:
        Словарь с примерами для всех модальностей
    """
    result = {
        "technique_name": technique_name,
        "module_type": module_type.value,
        "modalities": {}
    }

    for modality in [VAKModalityType.VISUAL, VAKModalityType.AUDITORY, VAKModalityType.KINESTHETIC]:
        example = get_example_for_module_type(module_type, modality, technique_name)
        result["modalities"][modality.value] = example

    return result


# Экспорт основных функций и конфигураций
__all__ = [
    # Функции создания конфигураций
    "create_nlp_techniques_config",
    "create_meditation_config",
    "create_visualization_config",
    "create_movement_config",

    # Функции получения примеров
    "get_nlp_adaptation_example",
    "get_meditation_adaptation_example",
    "get_visualization_example",
    "get_movement_example",
    "get_example_for_module_type",

    # Утилитарные функции
    "get_all_available_examples",
    "get_recommended_config_for_context",
    "create_multi_modal_example_set",

    # Константы с примерами
    "NLP_TECHNIQUES_EXAMPLES",
    "MEDITATION_EXAMPLES",
    "VISUALIZATION_EXAMPLES",
    "MOVEMENT_EXAMPLES",

    # Предустановленные конфигурации
    "NLP_THERAPY_CONFIG",
    "NLP_COACHING_CONFIG",
    "NLP_EDUCATION_CONFIG",
    "MEDITATION_THERAPY_CONFIG",
    "MEDITATION_WELLNESS_CONFIG",
    "MEDITATION_CORPORATE_CONFIG",
    "VISUALIZATION_THERAPY_CONFIG",
    "MOVEMENT_TRAUMA_CONFIG"
]