"""
Простой тест для Pattern Cultural Adaptation Expert Agent.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dependencies import (
        PatternCulturalAdaptationExpertDependencies,
        PatternShiftCulture,
        create_pattern_cultural_adaptation_dependencies
    )
    from prompts import get_system_prompt
    print("OK: Все импорты работают корректно")

    # Тестируем создание зависимостей
    deps = create_pattern_cultural_adaptation_dependencies(
        api_key="test_key",
        target_culture=PatternShiftCulture.UKRAINIAN
    )
    print(f"OK: Зависимости созданы для культуры: {deps.target_culture.value}")

    # Тестируем системный промпт
    system_prompt = get_system_prompt()
    print(f"OK: Системный промпт загружен (длина: {len(system_prompt)} символов)")

    # Тестируем культурный контекст
    context = deps.get_patternshift_cultural_context()
    print(f"OK: Культурный контекст: {context['culture']}")
    print(f"   Религия: {context['religion']}")
    print(f"   Фаза: {context['phase']}")

    # Тестируем реестр агентов
    print(f"OK: Доступные Pattern агенты:")
    for agent_type, agent_name in deps.pattern_agents_registry.items():
        print(f"   - {agent_type}: {agent_name}")

    print("\nSUCCESS: Все тесты прошли успешно!")
    print("READY: Pattern Cultural Adaptation Expert Agent готов к работе")

except Exception as e:
    print(f"ERROR: Ошибка тестирования: {e}")
    import traceback
    traceback.print_exc()