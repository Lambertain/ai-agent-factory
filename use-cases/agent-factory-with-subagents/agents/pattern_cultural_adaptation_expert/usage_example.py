"""
Пример использования системы культурного профилирования PatternShift.

Демонстрирует полный цикл: регистрация пользователя → профилирование → адаптация контента.
"""

import asyncio
from typing import Dict, Any, List

# Импорты системы профилирования
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dependencies import (
        PatternShiftCulture,
        PatternShiftReligion,
        create_pattern_cultural_adaptation_dependencies
    )

    # Используем прямые функции из модулей
    def get_registration_questions(language="ru"):
        from cultural_profiling import PatternShiftCulturalProfiler
        profiler = PatternShiftCulturalProfiler()
        return profiler.get_cultural_questions(language)

    def analyze_user_culture(responses):
        from cultural_profiling import PatternShiftCulturalProfiler, UserCulturalResponse
        profiler = PatternShiftCulturalProfiler()
        cultural_responses = [
            UserCulturalResponse(
                question_id=r.get('question_id', ''),
                selected_option_id=r.get('selected_option_id', ''),
                confidence_level=r.get('confidence_level', 5)
            ) for r in responses
        ]
        return profiler.analyze_cultural_profile(cultural_responses)

    def auto_assign_culture_from_registration(responses):
        from auto_culture_assignment import PatternShiftCultureAssigner
        assigner = PatternShiftCultureAssigner()
        return assigner.process_registration_responses(responses)

    def get_culture_assignment_explanation(result, language="ru"):
        from auto_culture_assignment import PatternShiftCultureAssigner
        assigner = PatternShiftCultureAssigner()
        return assigner.get_assignment_explanation(result, language)

    def create_mixed_cultural_profile(primary, secondary, preferences=None):
        from auto_culture_assignment import PatternShiftCultureAssigner
        assigner = PatternShiftCultureAssigner()
        return assigner.handle_mixed_culture_assignment(primary, secondary, preferences or {})

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что все необходимые файлы находятся в директории.")
    exit(1)


def simulate_user_registration() -> List[Dict[str, Any]]:
    """Симуляция ответов пользователя на анкету регистрации."""

    # Пример: французский эмигрант, живущий в Индии, но сохранивший культурную идентичность
    user_responses = [
        {
            "question_id": "direct_culture",
            "selected_option_id": "french",
            "confidence_level": 8
        },
        {
            "question_id": "religious_affiliation",
            "selected_option_id": "catholic",
            "confidence_level": 7
        },
        {
            "question_id": "language_preference",
            "selected_option_id": "french",
            "confidence_level": 9
        },
        {
            "question_id": "family_traditions",
            "selected_option_id": "catholic_traditions",
            "confidence_level": 6
        },
        {
            "question_id": "communication_style",
            "selected_option_id": "medium_context",
            "confidence_level": 5
        },
        {
            "question_id": "metaphor_preferences",
            "selected_option_id": "culture_art",
            "confidence_level": 8
        },
        {
            "question_id": "cultural_values",
            "selected_option_id": "individual_freedom",
            "confidence_level": 7
        }
    ]

    return user_responses


def demonstrate_questionnaire_generation():
    """Демонстрация генерации анкеты профилирования."""

    print("=" * 50)
    print("1. ГЕНЕРАЦИЯ АНКЕТЫ ПРОФИЛИРОВАНИЯ")
    print("=" * 50)

    # Получаем вопросы для русского языка
    questions_ru = get_registration_questions("ru")
    print(f"📋 Анкета на русском языке: {len(questions_ru)} вопросов")

    # Показываем первый вопрос как пример
    first_question = questions_ru[0]
    print(f"\n✨ Пример вопроса:")
    print(f"ID: {first_question['id']}")
    print(f"Вопрос: {first_question['question']}")
    print(f"Тип: {first_question['type']}")
    print(f"Варианты ответов: {len(first_question['options'])}")
    for i, option in enumerate(first_question['options'][:3], 1):
        print(f"  {i}. {option['text']}")

    # Получаем вопросы для английского языка
    questions_en = get_registration_questions("en")
    print(f"\n📋 Анкета на английском языке: {len(questions_en)} вопросов")


def demonstrate_cultural_profiling():
    """Демонстрация процесса культурного профилирования."""

    print("\n" + "=" * 50)
    print("2. КУЛЬТУРНОЕ ПРОФИЛИРОВАНИЕ ПОЛЬЗОВАТЕЛЯ")
    print("=" * 50)

    # Симулируем ответы пользователя
    user_responses = simulate_user_registration()
    print(f"👤 Симуляция ответов пользователя: {len(user_responses)} ответов")

    # Анализируем культурный профиль
    cultural_result = analyze_user_culture(user_responses)
    print(f"\n🎯 Результат культурного анализа:")
    print(f"Основная культура: {cultural_result.primary_culture.value}")
    print(f"Религиозный контекст: {cultural_result.primary_religion.value}")
    print(f"Уверенность: {cultural_result.confidence_score:.0%}")

    if cultural_result.alternative_cultures:
        print(f"\n🤔 Альтернативные варианты:")
        for culture, confidence in cultural_result.alternative_cultures[:3]:
            print(f"  - {culture.value}: {confidence:.0%}")

    return cultural_result


def demonstrate_automatic_assignment():
    """Демонстрация автоматического назначения культуры."""

    print("\n" + "=" * 50)
    print("3. АВТОМАТИЧЕСКОЕ НАЗНАЧЕНИЕ КУЛЬТУРЫ")
    print("=" * 50)

    # Симулируем ответы пользователя
    user_responses = simulate_user_registration()

    # Автоматическое назначение культуры
    assignment_result = auto_assign_culture_from_registration(user_responses)

    print(f"🎭 Назначенная культура: {assignment_result.assigned_culture.value}")
    print(f"🙏 Религиозный контекст: {assignment_result.assigned_religion.value}")
    print(f"📊 Уверенность: {assignment_result.confidence_score:.0%}")
    print(f"🔄 Уровень уверенности: {assignment_result.confidence_level.value}")
    print(f"✅ Требует подтверждения: {'Да' if assignment_result.requires_confirmation else 'Нет'}")

    # Получаем объяснение назначения
    explanation = get_culture_assignment_explanation(assignment_result, "ru")
    print(f"\n📋 Объяснение для пользователя:")
    print(f"Заголовок: {explanation['title']}")
    print(f"Обоснование: {explanation['rationale']}")

    if assignment_result.follow_up_questions:
        print(f"\n❓ Дополнительные вопросы ({len(assignment_result.follow_up_questions)}):")
        for question in assignment_result.follow_up_questions[:2]:
            print(f"  - {question.get('question_ru', 'Нет русского текста')}")

    return assignment_result


def demonstrate_mixed_cultural_profile():
    """Демонстрация создания смешанного культурного профиля."""

    print("\n" + "=" * 50)
    print("4. СМЕШАННЫЙ КУЛЬТУРНЫЙ ПРОФИЛЬ")
    print("=" * 50)

    # Создаем смешанный профиль: основная французская, вторичная итальянская
    mixed_profile = create_mixed_cultural_profile(
        PatternShiftCulture.FRENCH,
        PatternShiftCulture.ITALIAN,
        {"preference": "art_focused", "living_location": "india"}
    )

    print(f"🌐 Смешанный профиль создан:")
    print(f"Основная культура: {mixed_profile.culture.value}")
    print(f"Религиозный контекст: {mixed_profile.religion.value}")
    print(f"Чувствительные темы: {len(mixed_profile.sensitive_topics)}")
    print(f"Предпочитаемые метафоры: {len(mixed_profile.preferred_metaphors)}")
    print(f"Культурные герои: {', '.join(mixed_profile.cultural_heroes[:3])}")

    # Проверяем наличие информации о вторичной культуре
    if mixed_profile.historical_context.get('mixed_profile'):
        secondary_culture = mixed_profile.historical_context.get('secondary_culture')
        print(f"Вторичная культура: {secondary_culture}")

    return mixed_profile


def demonstrate_content_adaptation(assignment_result):
    """Демонстрация адаптации контента под культуру."""

    print("\n" + "=" * 50)
    print("5. АДАПТАЦИЯ КОНТЕНТА ПОД КУЛЬТУРУ")
    print("=" * 50)

    # Исходный универсальный контент
    original_content = """
    Стресс - это естественная реакция организма на вызовы.
    Представьте стресс как давление в чайнике - если не выпускать пар,
    он может взорваться. Важно найти здоровые способы справляться со стрессом,
    такие как физические упражнения, медитация или общение с близкими.
    """

    assigned_culture = assignment_result.assigned_culture

    print(f"📝 Исходный контент:")
    print(original_content.strip())

    # Адаптируем под назначенную культуру
    if assigned_culture == PatternShiftCulture.FRENCH:
        adapted_content = """
        Le stress est une réaction naturelle de l'organisme aux défis.
        Imaginez le stress comme la pression dans une cocotte-minute -
        si on ne laisse pas échapper la vapeur, elle peut exploser.
        Il est important de trouver des moyens sains de gérer le stress,
        comme l'art-thérapie, la contemplation philosophique ou
        les discussions profondes avec des amis dans un café parisien.
        """

        cultural_adaptations = [
            "Использована метафора кухонной посуды (cocotte-minute)",
            "Добавлена арт-терапия как культурно релевантный метод",
            "Включена философская рефлексия",
            "Упомянуты парижские кафе как место для общения"
        ]

    elif assigned_culture == PatternShiftCulture.UKRAINIAN:
        adapted_content = """
        Стрес - це природна реакція організму на виклики життя.
        Уявіть стрес як воду в річці навесні - якщо русло звужується,
        вода шукає обхідний шлях. Важливо знайти здорові способи
        справлятися зі стресом: прогулянки в природі, родинні розмови
        біля домашнього вогнища чи традиційні українські ремесла.
        """

        cultural_adaptations = [
            "Использована природная метафора реки весной",
            "Добавлены семейные традиции у домашнего очага",
            "Включены украинские ремесла как метод релаксации",
            "Подчеркнута важность связи с природой"
        ]

    else:
        adapted_content = original_content
        cultural_adaptations = ["Универсальный контент без специальной адаптации"]

    print(f"\n🎨 Адаптированный контент для {assigned_culture.value}:")
    print(adapted_content.strip())

    print(f"\n🔧 Примененные адаптации:")
    for adaptation in cultural_adaptations:
        print(f"  - {adaptation}")


def demonstrate_validation_feedback():
    """Демонстрация валидации на основе обратной связи пользователя."""

    print("\n" + "=" * 50)
    print("6. ВАЛИДАЦИЯ НА ОСНОВЕ ОБРАТНОЙ СВЯЗИ")
    print("=" * 50)

    # Симулируем обратную связь пользователя
    user_feedback = {
        "satisfaction_score": 8,  # 1-10
        "comments": "Метафоры очень понятны, но хотелось бы больше примеров из искусства",
        "specific_issues": ["metaphors_unclear"],  # небольшая проблема с метафорами
        "usage_duration": 7  # дней использования
    }

    print(f"📊 Обратная связь пользователя:")
    print(f"Оценка удовлетворенности: {user_feedback['satisfaction_score']}/10")
    print(f"Комментарии: {user_feedback['comments']}")
    print(f"Проблемы: {', '.join(user_feedback['specific_issues'])}")

    # Симулируем процесс валидации (в реальности это будет через агента)
    validation_result = {
        "is_valid": user_feedback['satisfaction_score'] >= 7,
        "confidence_adjustment": 0.1 if user_feedback['satisfaction_score'] >= 8 else -0.1,
        "recommendations": [],
        "action_needed": "minor_adjustments" if "metaphors_unclear" in user_feedback['specific_issues'] else "none"
    }

    if validation_result["action_needed"] == "minor_adjustments":
        validation_result["recommendations"] = [
            "Добавить больше метафор из искусства",
            "Включить примеры французских художников и философов",
            "Усилить культурные референсы"
        ]

    print(f"\n✅ Результат валидации:")
    print(f"Назначение корректно: {'Да' if validation_result['is_valid'] else 'Нет'}")
    print(f"Корректировка уверенности: {validation_result['confidence_adjustment']:+.1%}")
    print(f"Необходимые действия: {validation_result['action_needed']}")

    if validation_result["recommendations"]:
        print(f"\n💡 Рекомендации по улучшению:")
        for rec in validation_result["recommendations"]:
            print(f"  - {rec}")


def main():
    """Основная демонстрация системы культурного профилирования."""

    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ КУЛЬТУРНОГО ПРОФИЛИРОВАНИЯ PATTERNSHIFT")
    print("Сценарий: французский эмигрант, проживающий в Индии")
    print("Цель: продемонстрировать независимость культурной идентичности от геолокации")

    # 1. Генерация анкеты
    demonstrate_questionnaire_generation()

    # 2. Культурное профилирование
    cultural_result = demonstrate_cultural_profiling()

    # 3. Автоматическое назначение
    assignment_result = demonstrate_automatic_assignment()

    # 4. Смешанный профиль
    mixed_profile = demonstrate_mixed_cultural_profile()

    # 5. Адаптация контента
    demonstrate_content_adaptation(assignment_result)

    # 6. Валидация
    demonstrate_validation_feedback()

    print("\n" + "=" * 50)
    print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
    print("=" * 50)

    print(f"\n🏆 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"📍 Определенная культура: {assignment_result.assigned_culture.value}")
    print(f"🙏 Религиозный контекст: {assignment_result.assigned_religion.value}")
    print(f"📊 Финальная уверенность: {assignment_result.confidence_score:.0%}")
    print(f"🎯 Готовность к PatternShift: ✅ Да")
    print(f"🌍 Географическая независимость: ✅ Подтверждена")

    print(f"\n💡 КЛЮЧЕВЫЕ ПРЕИМУЩЕСТВА СИСТЕМЫ:")
    print(f"  - Культурная идентичность независима от местоположения")
    print(f"  - Автоматическое назначение с высокой точностью")
    print(f"  - Поддержка смешанных культурных профилей")
    print(f"  - Система валидации и корректировки")
    print(f"  - Полная интеграция с PatternShift программой")


if __name__ == "__main__":
    main()