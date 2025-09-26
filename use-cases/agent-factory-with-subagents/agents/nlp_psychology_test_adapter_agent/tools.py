"""
Tools для NLP Psychology Test Adapter Agent

Инструменты для адаптации психологических тестов под методологию PatternShift
с сохранением научной валидности и универсальным подходом.
"""

from pydantic_ai import RunContext
from typing import Dict, List, Any, Optional, Union
import asyncio
import random
import re
from datetime import datetime

from .dependencies import (
    PatternShiftTestAdapterDeps,
    TestValidationResult,
    AdaptationResult
)


async def adapt_test_questions(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    source_questions: List[Dict[str, Any]],
    target_methodology: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Адаптирует вопросы теста под методологию PatternShift.

    Args:
        source_questions: Исходные вопросы теста
        target_methodology: Настройки целевой методологии
    """
    deps = ctx.deps
    adapted_questions = []

    # Получение знаний о трансформации вопросов
    knowledge = await deps.search_agent_knowledge(
        "psychological test questions adaptation life situations PatternShift",
        match_count=3
    )

    for i, question in enumerate(source_questions):
        original_text = question.get('text', '')

        # Трансформация клинических формулировок в жизненные ситуации
        adapted_text = await _transform_to_life_situation(
            original_text,
            question.get('construct', 'general'),
            target_methodology.get('cultural_context', 'ukrainian')
        )

        # Сохранение структуры вопроса с адаптацией
        adapted_question = {
            **question,
            'id': f"ps_{question.get('id', i+1)}",
            'text': adapted_text,
            'original_text': original_text,
            'adaptation_metadata': {
                'transformation_type': 'life_situation',
                'cultural_adaptation': target_methodology.get('cultural_context', 'ukrainian'),
                'difficulty_level': _assess_question_difficulty(adapted_text),
                'construct_preserved': True
            }
        }

        # Адаптация вариантов ответов для жизненных ситуаций
        if 'options' in question:
            adapted_question['options'] = _adapt_answer_options(
                question['options'],
                target_methodology.get('cultural_context', 'ukrainian')
            )

        adapted_questions.append(adapted_question)

    return adapted_questions


async def _transform_to_life_situation(
    original_text: str,
    construct: str,
    cultural_context: str = 'ukrainian'
) -> str:
    """Трансформирует клинический вопрос в жизненную ситуацию."""

    # Паттерны трансформации для разных конструктов
    transformation_patterns = {
        'depression': {
            'ukrainian': [
                'Коли ви прокидаєтеся вранці, {situation}',
                'Уявіть ситуацію: ваші друзі запрошують вас на зустріч, але {feeling}',
                'В кінці робочого дня, коли всі справи зроблені, {state}'
            ]
        },
        'anxiety': {
            'ukrainian': [
                'Перед важливою зустріччю ви відчуваєте, що {feeling}',
                'Коли вам потрібно прийняти рішення, {behavior}',
                'В незнайомому місці з незнайомими людьми {reaction}'
            ]
        },
        'general': {
            'ukrainian': [
                'В повсякденному житті, коли {situation}',
                'Зазвичай, у схожих ситуаціях ви {behavior}',
                'Коли виникає така ситуація, {feeling}'
            ]
        }
    }

    # Ключевые слова для замены клинических терминов
    clinical_replacements = {
        'symptom': 'відчуваєте',
        'depression': 'пригніченість',
        'anxiety': 'хвилювання',
        'mood': 'настрій',
        'feeling': 'почуття',
        'behavior': 'поведінка',
        'little interest': 'мало цікавлять справи',
        'pleasure': 'задоволення',
        'energy': 'енергія',
        'concentration': 'концентрація уваги'
    }

    # Определение подходящих паттернов
    patterns = transformation_patterns.get(construct, transformation_patterns['general'])
    context_patterns = patterns.get(cultural_context, patterns.get('ukrainian', patterns['general']))

    # Замена клинических терминов
    adapted_text = original_text.lower()
    for clinical, natural in clinical_replacements.items():
        adapted_text = adapted_text.replace(clinical, natural)

    # Применение паттерна жизненной ситуации
    if context_patterns:
        pattern = random.choice(context_patterns)
        # Простая адаптация - вставка адаптированного текста в паттерн
        if '{situation}' in pattern:
            adapted_text = pattern.format(situation=adapted_text)
        elif '{feeling}' in pattern:
            adapted_text = pattern.format(feeling=adapted_text)
        elif '{behavior}' in pattern:
            adapted_text = pattern.format(behavior=adapted_text)
        else:
            adapted_text = pattern.format(state=adapted_text)

    # Капитализация первой буквы
    adapted_text = adapted_text[0].upper() + adapted_text[1:] if adapted_text else original_text

    return adapted_text


def _adapt_answer_options(options: List[str], cultural_context: str = 'ukrainian') -> List[str]:
    """Адаптирует варианты ответов под культурный контекст."""

    # Маппинги для разных культурных контекстов
    option_mappings = {
        'ukrainian': {
            'not at all': 'зовсім ні',
            'several days': 'кілька днів',
            'more than half the days': 'більше половини днів',
            'nearly every day': 'майже щодня',
            'never': 'ніколи',
            'sometimes': 'іноді',
            'often': 'часто',
            'always': 'завжди',
            'strongly disagree': 'категорично не згоден',
            'disagree': 'не згоден',
            'agree': 'згоден',
            'strongly agree': 'повністю згоден'
        }
    }

    mappings = option_mappings.get(cultural_context, option_mappings['ukrainian'])
    adapted_options = []

    for option in options:
        # Попытка найти прямое соответствие
        adapted = mappings.get(option.lower(), option)
        adapted_options.append(adapted)

    return adapted_options


def _assess_question_difficulty(question_text: str) -> str:
    """Оценивает сложность вопроса."""
    word_count = len(question_text.split())
    complexity_indicators = len(re.findall(r'[,;:]', question_text))

    if word_count < 10 and complexity_indicators <= 1:
        return 'easy'
    elif word_count < 20 and complexity_indicators <= 3:
        return 'medium'
    else:
        return 'hard'


async def validate_test_structure(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    adapted_test: Dict[str, Any]
) -> TestValidationResult:
    """
    Валидирует структуру адаптированного теста.

    Args:
        adapted_test: Адаптированный тест для проверки
    """
    deps = ctx.deps

    validation_errors = []
    validation_warnings = []
    structural_score = 0.0

    # Проверка наличия обязательных компонентов
    required_components = ['questions', 'scoring', 'redirection_logic']
    for component in required_components:
        if component not in adapted_test:
            validation_errors.append(f"Отсутствует обязательный компонент: {component}")
        else:
            structural_score += 0.25

    # Проверка вопросов
    questions = adapted_test.get('questions', [])
    if len(questions) < deps.config.methodology_config.get('min_questions', 15):
        validation_errors.append(f"Недостаточно вопросов: {len(questions)}")
    else:
        structural_score += 0.25

    # Проверка качества адаптации вопросов
    life_situation_count = 0
    for question in questions:
        text = question.get('text', '').lower()
        if any(indicator in text for indicator in ['коли', 'уявіть', 'ситуація', 'в житті']):
            life_situation_count += 1

    life_situation_ratio = life_situation_count / len(questions) if questions else 0
    if life_situation_ratio < 0.7:
        validation_warnings.append(f"Низкий процент вопросов-ситуаций: {life_situation_ratio:.2%}")

    # Проверка системы оценки
    scoring = adapted_test.get('scoring', {})
    if 'adaptive_thresholds' not in scoring and 'levels' not in scoring:
        validation_errors.append("Отсутствует система оценки результатов")

    # Проверка мультиязычности (если требуется)
    multilingual_variants = adapted_test.get('multilingual_variants', {})
    if len(deps.config.supported_languages) > 1 and len(multilingual_variants) < len(deps.config.supported_languages):
        validation_warnings.append("Неполная мультиязычная поддержка")

    return TestValidationResult(
        is_valid=len(validation_errors) == 0,
        validation_errors=validation_errors,
        validation_warnings=validation_warnings,
        structural_score=structural_score,
        overall_quality_score=structural_score * 0.8  # Снижаем из-за предупреждений
    )


async def generate_life_situations(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    constructs: List[str],
    existing_questions: List[Dict[str, Any]],
    questions_needed: int,
    difficulty_distribution: Dict[str, int]
) -> List[Dict[str, Any]]:
    """
    Генерирует дополнительные вопросы в формате жизненных ситуаций.

    Args:
        constructs: Психологические конструкты для покрытия
        existing_questions: Существующие вопросы
        questions_needed: Количество дополнительных вопросов
        difficulty_distribution: Распределение сложности
    """
    deps = ctx.deps

    # Поиск примеров вопросов в базе знаний
    knowledge = await deps.search_agent_knowledge(
        f"life situation questions {' '.join(constructs)} psychological assessment",
        match_count=5
    )

    generated_questions = []

    # Шаблоны ситуаций для разных конструктов
    situation_templates = {
        'mood': [
            "На роботі ваш колега критикує вашу роботу перед усіма. Як ви зазвичай реагуєте?",
            "Ви плануєте зустріч з друзями, але в останню хвилину всі відміняють. Що ви відчуваєте?",
            "Вечором, коли всі справи зроблені, ви сидите вдома. Який ваш звичайний стан?"
        ],
        'anxiety': [
            "Вам потрібно виступити з презентацією перед незнайомою аудиторією. Що ви відчуваєте?",
            "Ви їдете на співбесіду на роботу мрії. Як ви себе почуваєте за день до неї?",
            "Телефон дзвонить о пізній годині від невідомого номера. Ваша реакція?"
        ],
        'energy': [
            "Ранок суботи, у вас вільний день без планів. Що ви хочете робити?",
            "Після восьмигодинного робочого дня ви приходите додому. Який ваш рівень енергії?",
            "Друзі пропонують піти на активний відпочинок у вихідні. Ваша реакція?"
        ],
        'sleep': [
            "Лягаючи спати, ви зазвичай...",
            "Прокидаючись вранці, ви відчуваєте...",
            "Коли не можете заснути, ви..."
        ]
    }

    # Генерация вопросов для каждого конструкта
    questions_per_construct = questions_needed // len(constructs) if constructs else questions_needed

    for i, construct in enumerate(constructs):
        if len(generated_questions) >= questions_needed:
            break

        templates = situation_templates.get(construct, situation_templates['mood'])

        for j, template in enumerate(templates):
            if len(generated_questions) >= questions_needed:
                break

            question = {
                'id': f"generated_{construct}_{j+1}",
                'text': template,
                'construct': construct,
                'options': _generate_situation_options(construct),
                'values': [0, 1, 2, 3, 4],
                'adaptation_metadata': {
                    'generated': True,
                    'template_based': True,
                    'construct': construct,
                    'difficulty_level': 'medium'
                }
            }

            generated_questions.append(question)

    # Если нужно больше вопросов, дублируем с вариациями
    while len(generated_questions) < questions_needed:
        base_question = random.choice(generated_questions)
        variation = {
            **base_question,
            'id': f"variation_{len(generated_questions)+1}",
            'text': _create_question_variation(base_question['text']),
            'adaptation_metadata': {
                **base_question['adaptation_metadata'],
                'variation': True
            }
        }
        generated_questions.append(variation)

    return generated_questions[:questions_needed]


def _generate_situation_options(construct: str) -> List[str]:
    """Генерирует варианты ответов для ситуационных вопросов."""

    option_sets = {
        'mood': [
            "Мене це зовсім не зачіпає",
            "Трохи засмучуюся, але швидко відновлююся",
            "Досить сильно переживаю",
            "Дуже болісно реагую",
            "Це може зіпсувати мій день"
        ],
        'anxiety': [
            "Спокійно і впевнено",
            "Трохи нервую, але справляюся",
            "Відчуваю помітне хвилювання",
            "Дуже нервую",
            "Панікую і намагаюся уникнути"
        ],
        'energy': [
            "Багато енергії та ентузіазму",
            "Нормальна активність",
            "Трохи втомлений, але можу діяти",
            "Низька енергія",
            "Повна втома, нічого не хочеться"
        ]
    }

    return option_sets.get(construct, option_sets['mood'])


def _create_question_variation(original_text: str) -> str:
    """Создает вариацию вопроса."""
    variations = [
        lambda x: x.replace("ви", "людина"),
        lambda x: x.replace("зазвичай", "частіше за все"),
        lambda x: x.replace("Як", "Яким чином"),
        lambda x: x.replace("Що", "Які почуття")
    ]

    variation = random.choice(variations)
    return variation(original_text)


async def create_multilingual_variants(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    base_questions: List[Dict[str, Any]],
    target_languages: List[str]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Создает мультиязычные варианты тестовых вопросов.

    Args:
        base_questions: Базовые вопросы (обычно на украинском)
        target_languages: Список целевых языков
    """
    deps = ctx.deps

    multilingual_variants = {}

    # Поиск знаний о мультиязычной адаптации
    knowledge = await deps.search_agent_knowledge(
        "multilingual test adaptation cultural psychology",
        match_count=3
    )

    for language in target_languages:
        if language == 'uk':  # Украинский - базовый язык
            multilingual_variants[language] = base_questions
            continue

        translated_questions = []

        for question in base_questions:
            translated_question = await _translate_question(question, language)
            translated_questions.append(translated_question)

        multilingual_variants[language] = translated_questions

    return multilingual_variants


async def _translate_question(question: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    """Переводит вопрос на целевой язык с культурной адаптацией."""

    # Базовые переводы (в реальном проекте лучше использовать профессиональный API)
    translation_mappings = {
        'en': {
            'Коли ви прокидаєтеся вранці': 'When you wake up in the morning',
            'Уявіть ситуацію': 'Imagine a situation',
            'зовсім ні': 'not at all',
            'іноді': 'sometimes',
            'часто': 'often',
            'завжди': 'always'
        },
        'ru': {
            'Коли ви прокидаєтеся вранці': 'Когда вы просыпаетесь утром',
            'Уявіть ситуацію': 'Представьте ситуацию',
            'зовсім ні': 'совсем нет',
            'іноді': 'иногда',
            'часто': 'часто',
            'завжди': 'всегда'
        }
    }

    mappings = translation_mappings.get(target_language, {})

    translated_question = {**question}
    original_text = question.get('text', '')

    # Простой перевод по маппингам
    translated_text = original_text
    for uk_phrase, translated_phrase in mappings.items():
        translated_text = translated_text.replace(uk_phrase, translated_phrase)

    translated_question['text'] = translated_text
    translated_question['language'] = target_language

    # Перевод вариантов ответов
    if 'options' in question:
        translated_options = []
        for option in question['options']:
            translated_option = option
            for uk_phrase, translated_phrase in mappings.items():
                translated_option = translated_option.replace(uk_phrase, translated_phrase)
            translated_options.append(translated_option)
        translated_question['options'] = translated_options

    return translated_question


async def calculate_adaptive_thresholds(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    source_scoring: Dict[str, Any],
    target_levels: int
) -> Dict[str, Any]:
    """
    Рассчитывает адаптивные пороги для системы оценки PatternShift.

    Args:
        source_scoring: Исходная система оценки
        target_levels: Количество уровней результата
    """
    deps = ctx.deps

    # Поиск знаний о системах оценки
    knowledge = await deps.search_agent_knowledge(
        "adaptive scoring thresholds psychological assessment PatternShift",
        match_count=3
    )

    # Создание адаптивной системы оценки
    adaptive_scoring = {
        'system_type': 'adaptive_patternshift',
        'levels': target_levels,
        'adaptive_thresholds': {},
        'redirection_rules': {},
        'interpretation_guide': {}
    }

    # Расчет базовых порогов
    if 'max_score' in source_scoring:
        max_score = source_scoring['max_score']
    else:
        # Предполагаем стандартную шкалу
        max_score = 60  # Например, для 15 вопросов по 4 балла

    # Создание адаптивных порогов (не жесткие границы)
    thresholds = []
    for i in range(target_levels):
        threshold = {
            'level': i + 1,
            'min_score': int(max_score * i / target_levels),
            'max_score': int(max_score * (i + 1) / target_levels),
            'adaptive_range': int(max_score * 0.1),  # 10% гибкости
            'context_modifiers': {
                'age_adjustment': 0.05,
                'cultural_adjustment': 0.03,
                'situational_adjustment': 0.07
            }
        }
        thresholds.append(threshold)

    adaptive_scoring['adaptive_thresholds'] = thresholds

    # Создание правил перенаправления
    redirection_rules = {
        'healthy_range': {
            'levels': [1, 2],
            'action': 'continue_testing',
            'next_test': 'complementary_assessment'
        },
        'concern_range': {
            'levels': [3],
            'action': 'provide_resources',
            'resources': ['self_help_materials', 'lifestyle_recommendations']
        },
        'high_concern_range': {
            'levels': [4, 5] if target_levels >= 5 else [4],
            'action': 'recommend_program',
            'program_type': 'transformation_program'
        }
    }

    adaptive_scoring['redirection_rules'] = redirection_rules

    return adaptive_scoring


async def integrate_redirection_logic(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    test_type: Optional[str],
    scoring_system: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Интегрирует логику перенаправления в адаптированный тест.

    Args:
        test_type: Тип теста (depression, anxiety, etc.)
        scoring_system: Система оценки теста
    """
    deps = ctx.deps

    redirection_logic = {
        'decision_tree': {},
        'program_mappings': {},
        'resource_recommendations': {},
        'follow_up_assessments': {}
    }

    # Базовая логика перенаправления по типам тестов
    type_specific_logic = {
        'depression': {
            'low_score': {
                'action': 'positive_reinforcement',
                'next_steps': ['resilience_building', 'preventive_care']
            },
            'moderate_score': {
                'action': 'lifestyle_intervention',
                'program': 'mood_enhancement_program',
                'duration': '4-6_weeks'
            },
            'high_score': {
                'action': 'intensive_support',
                'program': 'comprehensive_transformation_program',
                'urgent': True
            }
        },
        'anxiety': {
            'low_score': {
                'action': 'stress_management_tips',
                'resources': ['relaxation_techniques', 'mindfulness_basics']
            },
            'moderate_score': {
                'action': 'anxiety_management_program',
                'program': 'calm_mind_transformation',
                'techniques': ['breathing_exercises', 'cognitive_restructuring']
            },
            'high_score': {
                'action': 'comprehensive_anxiety_support',
                'program': 'anxiety_liberation_program',
                'immediate_support': True
            }
        }
    }

    # Определение логики для конкретного типа теста
    if test_type and test_type in type_specific_logic:
        redirection_logic['decision_tree'] = type_specific_logic[test_type]
    else:
        # Универсальная логика для неизвестных типов тестов
        redirection_logic['decision_tree'] = {
            'low_score': {
                'action': 'maintain_wellness',
                'resources': ['general_wellness_tips']
            },
            'moderate_score': {
                'action': 'targeted_improvement',
                'program': 'personal_growth_program'
            },
            'high_score': {
                'action': 'comprehensive_support',
                'program': 'transformation_program',
                'priority': 'high'
            }
        }

    # Интеграция с системой оценки
    if 'adaptive_thresholds' in scoring_system:
        thresholds = scoring_system['adaptive_thresholds']
        for threshold in thresholds:
            level = threshold['level']
            if level <= 2:
                category = 'low_score'
            elif level <= 3:
                category = 'moderate_score'
            else:
                category = 'high_score'

            threshold['redirection'] = redirection_logic['decision_tree'].get(category, {})

    return redirection_logic


async def validate_psychological_correctness(
    ctx: RunContext[PatternShiftTestAdapterDeps],
    adapted_test: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Валидирует психологическую корректность адаптированного теста.

    Args:
        adapted_test: Адаптированный тест для валидации
    """
    deps = ctx.deps

    # Поиск знаний о валидации психологических тестов
    knowledge = await deps.search_agent_knowledge(
        "psychological test validation psychometric properties reliability validity",
        match_count=5
    )

    validation_result = {
        'is_valid': True,
        'validity_score': 0.0,
        'errors': [],
        'warnings': [],
        'psychometric_properties': {}
    }

    questions = adapted_test.get('questions', [])

    # Проверка содержательной валидности
    content_validity_score = 0.0

    # 1. Проверка покрытия конструктов
    constructs_covered = set()
    for question in questions:
        construct = question.get('construct', question.get('adaptation_metadata', {}).get('construct', 'unknown'))
        constructs_covered.add(construct)

    if len(constructs_covered) >= 3:  # Минимум 3 конструкта
        content_validity_score += 0.3
    else:
        validation_result['warnings'].append(f"Недостаточно конструктов покрыто: {len(constructs_covered)}")

    # 2. Проверка баланса сложности
    difficulty_levels = [q.get('adaptation_metadata', {}).get('difficulty_level', 'medium') for q in questions]
    easy_count = difficulty_levels.count('easy')
    medium_count = difficulty_levels.count('medium')
    hard_count = difficulty_levels.count('hard')

    total_questions = len(questions)
    if total_questions > 0:
        easy_ratio = easy_count / total_questions
        medium_ratio = medium_count / total_questions
        hard_ratio = hard_count / total_questions

        # Идеальное распределение: 30% легких, 50% средних, 20% сложных
        if 0.2 <= easy_ratio <= 0.4 and 0.4 <= medium_ratio <= 0.6 and 0.1 <= hard_ratio <= 0.3:
            content_validity_score += 0.2
        else:
            validation_result['warnings'].append(f"Неоптимальное распределение сложности: легкие={easy_ratio:.1%}, средние={medium_ratio:.1%}, сложные={hard_ratio:.1%}")

    # 3. Проверка качества трансформации в жизненные ситуации
    life_situation_quality = 0.0
    for question in questions:
        text = question.get('text', '').lower()

        # Позитивные индикаторы жизненных ситуаций
        positive_indicators = ['коли ви', 'уявіть', 'ситуація', 'в житті', 'зазвичай', 'як ви']
        negative_indicators = ['симптом', 'діагноз', 'розлад', 'патологія']

        positive_count = sum(1 for indicator in positive_indicators if indicator in text)
        negative_count = sum(1 for indicator in negative_indicators if indicator in text)

        if positive_count > 0 and negative_count == 0:
            life_situation_quality += 1
        elif negative_count > 0:
            life_situation_quality -= 0.5

    if total_questions > 0:
        life_situation_ratio = max(0, life_situation_quality / total_questions)
        if life_situation_ratio >= 0.8:
            content_validity_score += 0.3
        elif life_situation_ratio >= 0.6:
            content_validity_score += 0.2
        else:
            validation_result['warnings'].append(f"Низкое качество трансформации в жизненные ситуации: {life_situation_ratio:.1%}")

    # 4. Проверка системы оценки
    scoring = adapted_test.get('scoring', {})
    if 'adaptive_thresholds' in scoring and 'redirection_rules' in scoring:
        content_validity_score += 0.2
    else:
        validation_result['errors'].append("Отсутствует адаптивная система оценки")

    validation_result['validity_score'] = min(1.0, content_validity_score)
    validation_result['is_valid'] = validation_result['validity_score'] >= 0.7 and len(validation_result['errors']) == 0

    # Добавление психометрических свойств
    validation_result['psychometric_properties'] = {
        'content_validity': content_validity_score,
        'construct_coverage': len(constructs_covered),
        'difficulty_balance': {
            'easy': easy_ratio if total_questions > 0 else 0,
            'medium': medium_ratio if total_questions > 0 else 0,
            'hard': hard_ratio if total_questions > 0 else 0
        },
        'life_situation_quality': life_situation_ratio if total_questions > 0 else 0
    }

    return validation_result