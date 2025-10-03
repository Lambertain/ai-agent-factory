"""
Pattern NLP Technique Master Agent Tools

Инструменты для создания модульных НЛП-техник трансформации.
"""

from typing import Dict, Any, List, Optional, Union
import asyncio
import json
from datetime import datetime
from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import (
    PatternNLPTechniqueMasterDependencies,
    NLPTechniqueType,
    TherapyModality,
    ProblemArea,
    RepresentationalSystem,
    DifficultyLevel,
    TechniqueFormat
)


# === МОДЕЛИ ДАННЫХ ===

class TechniqueRequest(BaseModel):
    """Запрос на создание НЛП техники."""
    technique_type: str = Field(description="Тип НЛП техники")
    therapy_modality: str = Field(description="Модальность терапии")
    problem_area: str = Field(description="Область проблемы")
    rep_system: str = Field(default="multimodal", description="Репрезентативная система")
    difficulty: str = Field(default="beginner", description="Уровень сложности")
    duration_minutes: int = Field(default=15, description="Длительность в минутах")
    include_audio_script: bool = Field(default=True, description="Включить аудио скрипт")
    cultural_adaptation: Optional[str] = Field(default=None, description="Культурная адаптация")


class TechniqueModule(BaseModel):
    """Модуль НЛП техники."""
    name: str = Field(description="Название техники")
    type: str = Field(description="Тип техники")
    modality: str = Field(description="Модальность терапии")
    problem_area: str = Field(description="Область применения")
    duration_minutes: int = Field(description="Длительность")
    difficulty: str = Field(description="Уровень сложности")
    rep_system: str = Field(description="Репрезентативная система")

    introduction: str = Field(description="Введение и цель")
    preparation: str = Field(description="Подготовка")
    instructions: List[str] = Field(description="Пошаговые инструкции")
    integration: str = Field(description="Интеграция результатов")
    safety_check: str = Field(description="Проверка экологичности")
    homework: str = Field(description="Домашнее задание")

    contraindications: List[str] = Field(description="Противопоказания")
    safety_protocols: List[str] = Field(description="Протоколы безопасности")
    evidence_base: str = Field(description="Научная обоснованность")

    audio_script: Optional[str] = Field(default=None, description="Аудио скрипт")
    cultural_notes: Optional[str] = Field(default=None, description="Культурные особенности")


class VAKAdaptation(BaseModel):
    """Адаптация техники под репрезентативные системы."""
    visual_elements: List[str] = Field(description="Визуальные элементы")
    auditory_elements: List[str] = Field(description="Аудиальные элементы")
    kinesthetic_elements: List[str] = Field(description="Кинестетические элементы")
    multimodal_integration: str = Field(description="Мультимодальная интеграция")


class SafetyAssessment(BaseModel):
    """Оценка безопасности техники."""
    risk_level: str = Field(description="Уровень риска")
    contraindications: List[str] = Field(description="Противопоказания")
    safety_measures: List[str] = Field(description="Меры безопасности")
    crisis_protocols: List[str] = Field(description="Протоколы кризиса")
    professional_referral_criteria: List[str] = Field(description="Критерии направления к специалисту")


# === ОСНОВНЫЕ ИНСТРУМЕНТЫ ===

async def search_agent_knowledge(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний Pattern NLP Technique Master Agent.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация
    """
    try:
        # Используем MCP Archon для поиска в базе знаний
        from ...common.archon_integration import search_knowledge_base

        result = await search_knowledge_base(
            query=f"{query} pattern nlp technique master",
            source_tags=ctx.deps.knowledge_tags,
            match_count=match_count
        )

        if result and "results" in result:
            knowledge = "\n".join([
                f"**{r.get('metadata', {}).get('title', 'Знания')}:**\n{r.get('content', '')}"
                for r in result["results"]
            ])
            return f"База знаний Pattern NLP Technique Master:\n{knowledge}"
        else:
            return "Поиск в базе знаний не дал результатов. Используется встроенная экспертиза."

    except Exception as e:
        return f"Ошибка поиска в базе знаний: {e}. Используется встроенная экспертиза."


async def create_nlp_technique(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique_request: TechniqueRequest
) -> TechniqueModule:
    """
    Создать модульную НЛП технику.

    Args:
        technique_request: Параметры техники

    Returns:
        Созданная техника
    """
    # Поиск в базе знаний по типу техники
    knowledge = await search_agent_knowledge(
        ctx,
        f"{technique_request.technique_type} {technique_request.therapy_modality} {technique_request.problem_area}",
        3
    )

    # Генерация техники на основе параметров
    technique_name = f"{technique_request.technique_type.title()} для {technique_request.problem_area.replace('_', ' ')}"

    # Базовая структура техники
    technique = TechniqueModule(
        name=technique_name,
        type=technique_request.technique_type,
        modality=technique_request.therapy_modality,
        problem_area=technique_request.problem_area,
        duration_minutes=technique_request.duration_minutes,
        difficulty=technique_request.difficulty,
        rep_system=technique_request.rep_system,

        introduction=_generate_introduction(technique_request),
        preparation=_generate_preparation(technique_request),
        instructions=_generate_instructions(technique_request),
        integration=_generate_integration(technique_request),
        safety_check=_generate_safety_check(technique_request),
        homework=_generate_homework(technique_request),

        contraindications=_get_contraindications(technique_request),
        safety_protocols=_get_safety_protocols(technique_request),
        evidence_base=_get_evidence_base(technique_request)
    )

    # Добавляем аудио скрипт если нужен
    if technique_request.include_audio_script:
        technique.audio_script = _generate_audio_script(technique_request, technique)

    # Добавляем культурные заметки если нужны
    if technique_request.cultural_adaptation:
        technique.cultural_notes = _generate_cultural_notes(technique_request)

    return technique


async def adapt_technique_vak(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique: TechniqueModule,
    target_rep_system: str
) -> TechniqueModule:
    """
    Адаптировать технику под конкретную репрезентативную систему.

    Args:
        technique: Базовая техника
        target_rep_system: Целевая репрезентативная система

    Returns:
        Адаптированная техника
    """
    # Создаем копию техники
    adapted_technique = TechniqueModule(**technique.model_dump())
    adapted_technique.rep_system = target_rep_system

    # Адаптируем инструкции
    if target_rep_system == "visual":
        adapted_technique.instructions = _adapt_to_visual(technique.instructions)
    elif target_rep_system == "auditory":
        adapted_technique.instructions = _adapt_to_auditory(technique.instructions)
    elif target_rep_system == "kinesthetic":
        adapted_technique.instructions = _adapt_to_kinesthetic(technique.instructions)

    return adapted_technique


async def assess_technique_safety(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    technique: TechniqueModule
) -> SafetyAssessment:
    """
    Оценить безопасность НЛП техники.

    Args:
        technique: Техника для оценки

    Returns:
        Оценка безопасности
    """
    risk_factors = []

    # Оценка рисков по типу техники
    high_risk_techniques = ["timeline_therapy", "change_personal_history", "phobia_cure"]
    medium_risk_techniques = ["anchoring", "six_step_reframing"]

    if technique.type in high_risk_techniques:
        risk_level = "high"
        risk_factors.extend([
            "Работа с травматическими воспоминаниями",
            "Возможность эмоциональной активации",
            "Риск диссоциации"
        ])
    elif technique.type in medium_risk_techniques:
        risk_level = "medium"
        risk_factors.extend([
            "Эмоциональное воздействие",
            "Возможность сопротивления"
        ])
    else:
        risk_level = "low"
        risk_factors.append("Минимальные риски")

    # Общие противопоказания
    contraindications = [
        "Активный психоз",
        "Тяжелые суицидальные мысли",
        "Недавняя психиатрическая госпитализация",
        "Злоупотребление психоактивными веществами",
        "Тяжелое диссоциативное расстройство"
    ]

    # Меры безопасности
    safety_measures = [
        "Информированное согласие",
        "Проверка противопоказаний",
        "Мониторинг состояния",
        "Возможность прекращения в любой момент",
        "Проверка экологичности изменений"
    ]

    # Протоколы кризиса
    crisis_protocols = [
        "Немедленное прекращение техники",
        "Техники заземления и стабилизации",
        "Обращение к специалисту при необходимости",
        "Контакты экстренной помощи"
    ]

    # Критерии направления к специалисту
    referral_criteria = [
        "Усиление симптомов после техники",
        "Появление диссоциативных симптомов",
        "Суицидальные мысли",
        "Неконтролируемые эмоциональные реакции",
        "Галлюцинации или бредовые идеи"
    ]

    return SafetyAssessment(
        risk_level=risk_level,
        contraindications=contraindications,
        safety_measures=safety_measures,
        crisis_protocols=crisis_protocols,
        professional_referral_criteria=referral_criteria
    )


async def generate_technique_variants(
    ctx: RunContext[PatternNLPTechniqueMasterDependencies],
    base_technique: TechniqueModule,
    variant_types: List[str]
) -> Dict[str, TechniqueModule]:
    """
    Создать варианты техники.

    Args:
        base_technique: Базовая техника
        variant_types: Типы вариантов (age, gender, culture, language)

    Returns:
        Словарь вариантов техники
    """
    variants = {}

    for variant_type in variant_types:
        if variant_type == "age":
            variants.update({
                "teens": _adapt_for_teens(base_technique),
                "adults": base_technique,
                "seniors": _adapt_for_seniors(base_technique)
            })
        elif variant_type == "gender":
            variants.update({
                "male": _adapt_for_males(base_technique),
                "female": _adapt_for_females(base_technique),
                "non_binary": _adapt_for_non_binary(base_technique)
            })
        elif variant_type == "culture":
            variants.update({
                "western": base_technique,
                "eastern": _adapt_for_eastern_culture(base_technique),
                "traditional": _adapt_for_traditional_culture(base_technique)
            })

    return variants


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def _generate_introduction(request: TechniqueRequest) -> str:
    """Генерация введения техники."""
    return f"""
Добро пожаловать в технику {request.technique_type.replace('_', ' ').title()}!

Эта техника предназначена для работы с {request.problem_area.replace('_', ' ')} и основана на принципах {request.therapy_modality.upper()}.

Цель: Помочь вам развить навыки управления своим состоянием и создать позитивные изменения в жизни.

Продолжительность: {request.duration_minutes} минут
Уровень сложности: {request.difficulty}

Перед началом убедитесь, что у вас есть безопасное и спокойное место для выполнения техники.
"""


def _generate_preparation(request: TechniqueRequest) -> str:
    """Генерация этапа подготовки."""
    return """
1. Найдите тихое место, где вас никто не побеспокоит
2. Примите удобное положение (сидя или лежа)
3. Отключите все отвлекающие устройства
4. Сделайте несколько глубоких вдохов
5. Настройтесь на работу с собой
6. Убедитесь, что чувствуете себя в безопасности
"""


def _generate_instructions(request: TechniqueRequest) -> List[str]:
    """Генерация пошаговых инструкций."""
    if request.technique_type == "reframing":
        return [
            "Определите проблемную ситуацию или убеждение",
            "Найдите 3 негативных аспекта этой ситуации",
            "Для каждого негативного аспекта найдите позитивную альтернативу",
            "Создайте новый взгляд на ситуацию",
            "Визуализируйте себя с новым пониманием",
            "Закрепите новое понимание через повторение"
        ]
    elif request.technique_type == "anchoring":
        return [
            "Вспомните сильное позитивное переживание",
            "Погрузитесь в это воспоминание полностью",
            "Усильте позитивные ощущения",
            "В пик переживания создайте физический якорь",
            "Отпустите воспоминание и якорь",
            "Проверьте якорь через несколько минут"
        ]
    else:
        return [
            "Сосредоточьтесь на проблемной области",
            "Примените техники осознанности",
            "Используйте дыхательные упражнения",
            "Работайте с внутренними образами",
            "Интегрируйте изменения",
            "Закрепите результат"
        ]


def _generate_integration(request: TechniqueRequest) -> str:
    """Генерация этапа интеграции."""
    return """
Теперь важно интегрировать полученный опыт:

1. Оцените произошедшие изменения по шкале от 1 до 10
2. Заметьте новые ощущения в теле и эмоции
3. Подумайте, как эти изменения повлияют на вашу жизнь
4. Создайте план применения новых навыков
5. Запишите свои наблюдения и инсайты
6. Поблагодарите себя за проделанную работу
"""


def _generate_safety_check(request: TechniqueRequest) -> str:
    """Генерация проверки экологичности."""
    return """
Проверка экологичности изменений:

1. Соответствуют ли изменения вашим ценностям?
2. Не нарушают ли они ваши отношения с близкими?
3. Чувствуете ли вы себя в безопасности с этими изменениями?
4. Готовы ли вы к последствиям этих изменений?
5. Есть ли какая-то часть вас, которая возражает против изменений?

Если на любой вопрос ответ отрицательный, обратитесь к специалисту.
"""


def _generate_homework(request: TechniqueRequest) -> str:
    """Генерация домашнего задания."""
    return f"""
Домашнее задание на ближайшие дни:

1. Практикуйте технику ежедневно в течение {min(request.duration_minutes, 10)} минут
2. Ведите дневник изменений и наблюдений
3. Применяйте полученные навыки в повседневных ситуациях
4. Отмечайте прогресс и трудности
5. При необходимости адаптируйте технику под свои потребности

Помните: изменения требуют времени и постоянной практики.
"""


def _get_contraindications(request: TechniqueRequest) -> List[str]:
    """Получить противопоказания для техники."""
    base_contraindications = [
        "Активный психоз или психотические эпизоды",
        "Тяжелые суицидальные мысли",
        "Недавняя госпитализация по психиатрическим причинам",
        "Злоупотребление психоактивными веществами",
        "Возраст до 16 лет (требует адаптации)"
    ]

    if request.technique_type in ["timeline_therapy", "change_personal_history"]:
        base_contraindications.extend([
            "Тяжелое диссоциативное расстройство",
            "Острое травматическое стрессовое расстройство"
        ])

    return base_contraindications


def _get_safety_protocols(request: TechniqueRequest) -> List[str]:
    """Получить протоколы безопасности."""
    return [
        "Информированное согласие перед началом",
        "Проверка противопоказаний",
        "Мониторинг эмоционального состояния",
        "Возможность прекращения в любой момент",
        "Техники заземления при необходимости",
        "Контакты экстренной психологической помощи"
    ]


def _get_evidence_base(request: TechniqueRequest) -> str:
    """Получить научную базу для техники."""
    evidence_bases = {
        "reframing": "Когнитивно-поведенческая терапия имеет обширную доказательную базу с effect size 0.7-0.8 для тревожных и депрессивных расстройств.",
        "anchoring": "НЛП техники показывают эффективность в краткосрочных интервенциях, особенно для работы с фобиями и тревогой.",
        "swish_pattern": "Визуальные техники НЛП демонстрируют быстрые изменения в субъективном восприятии проблемных ситуаций."
    }

    return evidence_bases.get(request.technique_type, "Техника основана на принципах доказательной психотерапии.")


def _generate_audio_script(request: TechniqueRequest, technique: TechniqueModule) -> str:
    """Генерация аудио скрипта."""
    return f"""
[АУДИО СКРИПТ - {technique.name}]

[Спокойный, уверенный голос]

Добро пожаловать... Сейчас мы проведем технику {technique.name}...
Найдите удобное положение... закройте глаза...
и позвольте себе полностью расслабиться...

[Пауза 3 секунды]

Сделайте глубокий вдох... и медленный выдох...
Почувствуйте, как ваше тело расслабляется...

[Далее следуют инструкции техники с паузами и успокаивающими интонациями]

[Завершение]
Отлично... вы проделали хорошую работу...
Когда будете готовы... медленно откройте глаза...
и вернитесь в настоящий момент...
"""


def _generate_cultural_notes(request: TechniqueRequest) -> str:
    """Генерация культурных заметок."""
    return f"""
Культурная адаптация для {request.cultural_adaptation}:

- Учитывайте культурные особенности восприятия эмоций
- Адаптируйте метафоры под культурный контекст
- Соблюдайте принятые нормы взаимодействия
- Учитывайте роль семьи и сообщества
- Респектуйте религиозные и духовные убеждения
"""


# Функции адаптации VAK
def _adapt_to_visual(instructions: List[str]) -> List[str]:
    """Адаптация инструкций для визуальной модальности."""
    visual_adaptations = {
        "представьте": "увидьте яркую картину",
        "почувствуйте": "визуализируйте",
        "услышьте": "увидьте образ"
    }

    adapted = []
    for instruction in instructions:
        adapted_instruction = instruction
        for old, new in visual_adaptations.items():
            adapted_instruction = adapted_instruction.replace(old, new)
        adapted.append(adapted_instruction + " Используйте яркие образы и цвета.")

    return adapted


def _adapt_to_auditory(instructions: List[str]) -> List[str]:
    """Адаптация инструкций для аудиальной модальности."""
    auditory_adaptations = {
        "увидьте": "услышьте",
        "визуализируйте": "проговорите про себя",
        "представьте": "скажите себе"
    }

    adapted = []
    for instruction in instructions:
        adapted_instruction = instruction
        for old, new in auditory_adaptations.items():
            adapted_instruction = adapted_instruction.replace(old, new)
        adapted.append(adapted_instruction + " Обращайте внимание на внутренний голос.")

    return adapted


def _adapt_to_kinesthetic(instructions: List[str]) -> List[str]:
    """Адаптация инструкций для кинестетической модальности."""
    kinesthetic_adaptations = {
        "увидьте": "почувствуйте",
        "услышьте": "ощутите",
        "представьте": "прочувствуйте"
    }

    adapted = []
    for instruction in instructions:
        adapted_instruction = instruction
        for old, new in kinesthetic_adaptations.items():
            adapted_instruction = adapted_instruction.replace(old, new)
        adapted.append(adapted_instruction + " Сосредоточьтесь на телесных ощущениях.")

    return adapted


# Функции адаптации по возрасту и полу
def _adapt_for_teens(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для подростков."""
    teen_technique = TechniqueModule(**technique.model_dump())
    teen_technique.name += " (для подростков)"
    teen_technique.introduction = teen_technique.introduction.replace(
        "взрослый", "подросток"
    ).replace("зрелый", "молодой")
    return teen_technique


def _adapt_for_seniors(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для пожилых людей."""
    senior_technique = TechniqueModule(**technique.model_dump())
    senior_technique.name += " (для пожилых)"
    senior_technique.duration_minutes = min(technique.duration_minutes, 10)
    return senior_technique


def _adapt_for_males(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для мужчин."""
    male_technique = TechniqueModule(**technique.model_dump())
    male_technique.name += " (мужская версия)"
    return male_technique


def _adapt_for_females(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для женщин."""
    female_technique = TechniqueModule(**technique.model_dump())
    female_technique.name += " (женская версия)"
    return female_technique


def _adapt_for_non_binary(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для небинарных людей."""
    nb_technique = TechniqueModule(**technique.model_dump())
    nb_technique.name += " (небинарная версия)"
    return nb_technique


def _adapt_for_eastern_culture(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для восточной культуры."""
    eastern_technique = TechniqueModule(**technique.model_dump())
    eastern_technique.name += " (восточная версия)"
    eastern_technique.cultural_notes = "Интегрированы принципы восточной философии и практик осознанности"
    return eastern_technique


def _adapt_for_traditional_culture(technique: TechniqueModule) -> TechniqueModule:
    """Адаптация для традиционной культуры."""
    traditional_technique = TechniqueModule(**technique.model_dump())
    traditional_technique.name += " (традиционная версия)"
    traditional_technique.cultural_notes = "Адаптировано с учетом традиционных ценностей и норм"
    return traditional_technique