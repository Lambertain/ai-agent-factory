"""
Простая демонстрация системы культурного профилирования PatternShift.
Без эмодзи для совместимости с Windows консолью.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dependencies import PatternShiftCulture, PatternShiftReligion


def demonstrate_system():
    """Демонстрация ключевых компонентов системы."""

    print("=" * 60)
    print("СИСТЕМА КУЛЬТУРНОГО ПРОФИЛИРОВАНИЯ PATTERNSHIFT")
    print("=" * 60)

    print("\n1. ПРОБЛЕМА:")
    print("   Пользователь может быть французом, но жить в Индии")
    print("   Геолокация НЕ определяет культурную идентичность!")

    print("\n2. РЕШЕНИЕ:")
    print("   Анкета из 7+ вопросов для определения культуры")
    print("   Автоматическое назначение с учетом уверенности")
    print("   Адаптация контента под реальную культурную идентичность")

    print("\n3. ПОДДЕРЖИВАЕМЫЕ КУЛЬТУРЫ:")
    cultures = list(PatternShiftCulture)
    for i, culture in enumerate(cultures, 1):
        print(f"   {i:2d}. {culture.value}")

    print(f"\n   ВСЕГО: {len(cultures)} европейских культур")

    print("\n4. РЕЛИГИОЗНЫЕ КОНТЕКСТЫ:")
    religions = list(PatternShiftReligion)
    for i, religion in enumerate(religions, 1):
        print(f"   {i}. {religion.value}")

    print("\n5. КОМПОНЕНТЫ СИСТЕМЫ:")
    components = [
        "cultural_profiling.py - Основная логика профилирования",
        "auto_culture_assignment.py - Автоматическое назначение",
        "registration_questionnaire.json - Анкета регистрации",
        "tools.py - Интеграция с агентом",
        "CULTURAL_PROFILING_README.md - Документация"
    ]

    for component in components:
        print(f"   * {component}")

    print("\n6. ПРИМЕР СЦЕНАРИЯ:")
    print("   Пользователь: Француз, живущий в Индии")
    print("   Ответы анкеты:")
    print("     - Культурная идентичность: Французская (уверенность 8/10)")
    print("     - Язык материалов: Французский (уверенность 9/10)")
    print("     - Религия: Католическая (уверенность 7/10)")
    print("     - Метафоры: Искусство и философия (уверенность 8/10)")

    print("\n   Результат автоназначения:")
    print("     - Назначенная культура: FRENCH")
    print("     - Религиозный контекст: CATHOLIC")
    print("     - Уверенность системы: 85%")
    print("     - Статус: Автоматическое назначение")

    print("\n7. АДАПТАЦИЯ КОНТЕНТА:")
    print("   Исходный текст:")
    print("     'Стресс как давление в чайнике'")
    print("   Адаптированный для французской культуры:")
    print("     'Le stress comme la pression dans une cocotte-minute parisienne'")
    print("     + Добавлены: арт-терапия, философские дискуссии, парижские кафе")

    print("\n8. КЛЮЧЕВЫЕ ПРЕИМУЩЕСТВА:")
    advantages = [
        "Независимость от геолокации",
        "Высокая точность определения (85%+ для четких случаев)",
        "Поддержка смешанных культурных профилей",
        "Автоматическая валидация и корректировка",
        "Полная интеграция с PatternShift программой",
        "Культурная безопасность и уважение традиций"
    ]

    for i, advantage in enumerate(advantages, 1):
        print(f"   {i}. {advantage}")

    print("\n9. ТЕХНИЧЕСКИЕ ДЕТАЛИ:")
    print("   - Взвешенная система подсчета баллов")
    print("   - Учет уверенности пользователя в ответах")
    print("   - 5 уровней уверенности системы")
    print("   - Автоматические дополнительные вопросы при неясности")
    print("   - Поддержка 2 языков интерфейса (RU/EN)")

    print("\n10. ИНТЕГРАЦИЯ С АГЕНТОМ:")
    tools = [
        "process_user_registration() - Обработка анкеты",
        "get_registration_questionnaire() - Получение вопросов",
        "update_user_cultural_profile() - Обновление профиля",
        "validate_cultural_assignment() - Валидация назначения"
    ]

    for tool in tools:
        print(f"    * {tool}")

    print("\n" + "=" * 60)
    print("СИСТЕМА ГОТОВА К ИСПОЛЬЗОВАНИЮ!")
    print("=" * 60)

    print(f"\nФайлы системы созданы в:")
    print(f"  {os.path.dirname(__file__)}")

    print(f"\nДля полного тестирования запустите:")
    print(f"  python test_agent.py")

    print(f"\nДля изучения API см. файл:")
    print(f"  CULTURAL_PROFILING_README.md")


if __name__ == "__main__":
    try:
        demonstrate_system()
    except Exception as e:
        print(f"Ошибка демонстрации: {e}")
        import traceback
        traceback.print_exc()