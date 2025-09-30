"""
Инструменты для Pattern Ericksonian Hypnosis Scriptwriter Agent
"""

from typing import Dict, List, Any, Optional
from pydantic_ai import RunContext
from .dependencies import PatternEricksonianHypnosisScriptwriterDependencies
from .models import TranceDepth, TherapeuticGoal, HypnoticTechnique


async def search_agent_knowledge(
    ctx: RunContext[PatternEricksonianHypnosisScriptwriterDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний агента.

    Args:
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    search_tags = getattr(ctx.deps, 'knowledge_tags', [])

    try:
        # Здесь будет вызов к mcp_archon_rag_search_knowledge_base
        # Сейчас заглушка
        return f"Поиск в базе знаний: {query} (теги: {', '.join(search_tags)})"

    except Exception as e:
        return f"Ошибка доступа к базе знаний: {e}"


async def create_hypnotic_script(
    title: str,
    goal: str,
    problem: str,
    depth: TranceDepth,
    duration: int
) -> Dict[str, Any]:
    """
    Создание структурированного гипнотического скрипта.

    Returns:
        Словарь с компонентами скрипта
    """
    # Базовая структура скрипта
    script = {
        "induction": generate_induction(depth, duration // 5),
        "deepening": generate_deepening(depth, duration // 5),
        "therapeutic_work": generate_therapeutic_work(goal, problem, duration // 2),
        "posthypnotic_suggestions": generate_posthypnotic(goal, duration // 10),
        "emergence": generate_emergence(depth, duration // 10)
    }

    return script


def generate_induction(depth: TranceDepth, duration: int) -> Dict[str, str]:
    """Генерация индукции транса"""
    if depth == TranceDepth.LIGHT:
        return {
            "content": """Устройся поудобнее и позволь себе сосредоточиться на дыхании...

Вдох... выдох... естественно и легко...

С каждым выдохом плечи опускаются... лицо расслабляется...

И ты можешь ЗАМЕТИТЬ, как тело само собой становится более расслабленным...""",
            "techniques": ["breathing_focus", "progressive_relaxation"]
        }
    elif depth == TranceDepth.MEDIUM:
        return {
            "content": """Устройся поудобнее, закрой глаза или найди точку для фиксации взгляда...

И пока ты читаешь эти слова, дыхание само собой становится более глубоким и спокойным...

Вдох... и выдох... и с каждым выдохом мышцы лица... шеи... плеч... РАССЛАБЛЯЮТСЯ...

Ты можешь ЗАМЕТИТЬ, как приятная тяжесть появляется в руках и ногах...

И это совершенно естественно... позволяя себе ПОГРУЖАТЬСЯ ГЛУБЖЕ с каждым дыханием...""",
            "techniques": ["eye_fixation", "progressive_relaxation", "embedded_commands"]
        }
    else:  # DEEP
        return {
            "content": """Найди удобное положение и позволь глазам закрыться...

Сосредоточься на дыхании... вдох... выдох... естественно и легко...

И с каждым выдохом ты можешь ОТПУСКАТЬ все напряжение...

Представь поток теплого золотого света, который начинает течь от макушки головы...

Он медленно стекает по лбу, РАССЛАБЛЯЯ каждую морщинку...
Течет по векам, снимая напряжение с глаз...
Спускается по щекам, РАССЛАБЛЯЯ челюсть...

И продолжает свой путь по шее... плечам... рукам...
С каждым вдохом свет наполняет тело... с каждым выдохом ОТПУСКАЕТСЯ всё ненужное...

ПОГРУЖАЙСЯ ГЛУБЖЕ... глубже... в это приятное состояние покоя...""",
            "techniques": ["visualization", "progressive_relaxation", "embedded_commands", "fractionation"]
        }


def generate_deepening(depth: TranceDepth, duration: int) -> Dict[str, str]:
    """Генерация углубления транса"""
    return {
        "content": """Представь, что спускаешься по мягким ступенькам...

10... с каждым шагом глубже... приятнее...
9... ОТПУСКАЯ всё ненужное...
8... позволяя себе РАССЛАБЛЯТЬСЯ полностью...
7... погружаясь в это спокойствие...
6... всё глубже... и глубже...
5... ощущая приятную тяжесть тела...
4... дыхание становится ещё более глубоким...
3... полностью в этом состоянии...
2... комфортно и безопасно...
1... достигая идеальной глубины для трансформации...""",
        "techniques": ["countdown", "embedded_commands", "metaphor"]
    }


def generate_therapeutic_work(goal: str, problem: str, duration: int) -> Dict[str, str]:
    """Генерация терапевтической работы"""
    return {
        "content": f"""И теперь, находясь в этом спокойном состоянии,
подсознание готово работать над изменениями...

Та часть тебя, которая раньше {problem},
может сейчас УЧИТЬСЯ новому способу реагирования...

Представь себя в будущем, где ты УЖЕ ДОСТИГ {goal}...
Посмотри, как ты выглядишь... как двигаешься... что чувствуешь...

Это новое состояние СТАНОВИТСЯ частью тебя... здесь и сейчас...

И с каждым дыханием оно УКРЕПЛЯЕТСЯ... ИНТЕГРИРУЕТСЯ...
СТАНОВИТСЯ твоей естественной реакцией...""",
        "techniques": ["future_pacing", "embedded_commands", "integration"]
    }


def generate_posthypnotic(goal: str, duration: int) -> Dict[str, str]:
    """Генерация постгипнотических внушений"""
    return {
        "content": f"""И когда ты вернёшься в обычное состояние,
часть тебя БУДЕТ ПОМНИТЬ это чувство {goal}...

В нужный момент оно ПОЯВИТСЯ САМО,
естественно и легко, без усилий...

Это станет твоей автоматической реакцией...
Работающей на благо всей системы...""",
        "techniques": ["posthypnotic_suggestion", "embedded_commands", "anchoring"]
    }


def generate_emergence(depth: TranceDepth, duration: int) -> Dict[str, str]:
    """Генерация выхода из транса"""
    return {
        "content": """И сейчас, когда будешь готов,
можешь начать возвращать внимание сюда...

Чувствуя тело на стуле... или кровати...
Слыша звуки вокруг...
Ощущая воздух на коже...

Постепенно активируя тело...
Двигая пальцами рук... ног...

И когда будешь полностью готов,
можешь открыть глаза, чувствуя себя отдохнувшим, обновлённым,
с ясным умом и энергией для действий...""",
        "techniques": ["gradual_return", "orientation", "energization"]
    }


async def generate_embedded_commands(
    therapeutic_goal: str,
    target_context: str
) -> List[str]:
    """Генерация встроенных команд для цели"""
    commands = [
        f"РАССЛАБЬСЯ И ОТПУСТИ",
        f"ПОЧУВСТВУЙ ИЗМЕНЕНИЯ",
        f"ПРИМИ ЭТО СЕЙЧАС",
        f"ИНТЕГРИРУЙ НОВЫЙ ПАТТЕРН",
        f"ПОЗВОЛЬ ПРОИЗОЙТИ"
    ]
    return commands


async def create_therapeutic_metaphor(
    problem: str,
    desired_outcome: str
) -> Dict[str, str]:
    """Создание терапевтической метафоры"""
    metaphor = {
        "title": "Метафора трансформации",
        "text": f"""Представь маленькое семя, которое лежит в темноте земли.
Оно не знает, что произойдёт, когда начнёт расти.
Но что-то внутри знает... и начинает прорастать...
пробиваясь через тьму к свету...
и однажды становится сильным деревом, достигающим неба...""",
        "therapeutic_message": f"Трансформация из {problem} в {desired_outcome} происходит естественно"
    }
    return metaphor


async def assess_script_safety(
    target_problem: str,
    therapeutic_goal: str
) -> Dict[str, Any]:
    """Оценка безопасности темы скрипта"""

    # Список противопоказаний
    high_risk_keywords = [
        "суицид", "психоз", "шизофрения", "биполярное расстройство",
        "эпилепсия", "серьёзная депрессия", "травма", "насилие"
    ]

    is_high_risk = any(keyword in target_problem.lower() for keyword in high_risk_keywords)

    if is_high_risk:
        return {
            "is_safe": False,
            "risk_level": "high",
            "warning": "Данная тема требует работы с квалифицированным специалистом",
            "recommendations": [
                "Обратиться к психотерапевту или психиатру",
                "Не использовать самостоятельную работу с гипнозом",
                "Получить профессиональную диагностику"
            ]
        }

    return {
        "is_safe": True,
        "risk_level": "low",
        "recommendations": [
            "Работать в комфортном темпе",
            "Прерывать при дискомфорте",
            "Обращаться к специалисту при необходимости"
        ]
    }


async def adapt_trance_depth(
    script: Dict[str, Any],
    target_depth: TranceDepth,
    client_context: str
) -> Dict[str, Any]:
    """Адаптация глубины транса под контекст"""
    # Логика адаптации скрипта
    return script