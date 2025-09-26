#!/usr/bin/env python3
"""
Тест интеграции Context7 MCP с Performance Optimization Agent.

Проверяет работоспособность интеграции и новых инструментов.
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем путь к агенту
sys.path.append(str(Path(__file__).parent))

from dependencies import PerformanceOptimizationDependencies
from tools import (
    resolve_library_id_context7,
    get_library_docs_context7,
    analyze_project_context,
    search_performance_knowledge_context7,
    get_performance_best_practices_context7,
    analyze_technology_performance_context7
)


async def test_context7_integration():
    """Тестирование Context7 MCP интеграции."""
    print("🧪 Тестирование Context7 MCP интеграции с Performance Optimization Agent")
    print("=" * 80)

    # Создаем тестовые зависимости
    deps = PerformanceOptimizationDependencies(
        api_key="test_key",
        project_path="./test_project",
        framework="react",
        domain_type="web_application",
        enable_context7_mcp=True
    )

    # Имитируем RunContext
    class MockRunContext:
        def __init__(self, deps):
            self.deps = deps

    ctx = MockRunContext(deps)

    print("\n1. 🔍 Тестирование resolve_library_id_context7...")
    try:
        result = await resolve_library_id_context7(ctx, "react")
        print(f"✅ Результат: {result}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n2. 📚 Тестирование get_library_docs_context7...")
    try:
        # Используем простой пример ID
        result = await get_library_docs_context7(
            ctx, "/react/docs", "performance optimization", 1000
        )
        print(f"✅ Результат: {result[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n3. 🔬 Тестирование analyze_project_context...")
    try:
        # Создаем тестовую директорию
        test_dir = Path("./test_project")
        test_dir.mkdir(exist_ok=True)

        result = await analyze_project_context(ctx, str(test_dir), "react")
        print(f"✅ Результат: {result[:200]}...")

        # Удаляем тестовую директорию
        if test_dir.exists() and test_dir.is_dir():
            test_dir.rmdir()

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n4. ⚙️ Проверка конфигурации Context7...")
    print(f"Context7 MCP включен: {deps.enable_context7_mcp}")
    print(f"Кэш библиотек: {len(deps.context7_library_cache)} записей")
    print(f"Кэш документации: {len(deps.context7_docs_cache)} записей")

    print("\n5. 🔍 Тестирование search_performance_knowledge_context7...")
    try:
        result = await search_performance_knowledge_context7(
            ctx, "react optimization", "web_application"
        )
        print(f"✅ Результат: {result[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n6. 📚 Тестирование get_performance_best_practices_context7...")
    try:
        result = await get_performance_best_practices_context7(
            ctx, ["react", "fastapi"]
        )
        print(f"✅ Результат: {result[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n7. 🔬 Тестирование analyze_technology_performance_context7...")
    try:
        test_dir = Path("./test_project")
        test_dir.mkdir(exist_ok=True)

        result = await analyze_technology_performance_context7(
            ctx, str(test_dir), "react"
        )
        print(f"✅ Результат: {result[:200]}...")

        # Удаляем тестовую директорию
        if test_dir.exists() and test_dir.is_dir():
            test_dir.rmdir()

    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n" + "=" * 80)
    print("🎯 Тестирование расширенной Context7 интеграции завершено!")


def test_context7_configuration():
    """Тестирование конфигурации Context7."""
    print("\n📋 Проверка конфигурации Context7 MCP:")

    # Проверяем наличие context7-mcp
    import subprocess
    try:
        result = subprocess.run(
            ["context7-mcp", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Context7 MCP доступен")
        else:
            print("❌ Context7 MCP недоступен")
    except Exception as e:
        print(f"❌ Ошибка проверки Context7 MCP: {e}")

    # Проверяем зависимости
    print("\n📦 Проверка зависимостей:")
    deps = PerformanceOptimizationDependencies(
        api_key="test",
        enable_context7_mcp=True
    )

    print(f"✅ Context7 интеграция включена: {deps.enable_context7_mcp}")
    print(f"✅ Кэш библиотек инициализирован: {type(deps.context7_library_cache)}")
    print(f"✅ Кэш документации инициализирован: {type(deps.context7_docs_cache)}")


if __name__ == "__main__":
    print("🚀 Запуск тестов интеграции Context7 MCP")

    # Синхронные тесты
    test_context7_configuration()

    # Асинхронные тесты
    try:
        asyncio.run(test_context7_integration())
    except KeyboardInterrupt:
        print("\n⏹️ Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка тестирования: {e}")