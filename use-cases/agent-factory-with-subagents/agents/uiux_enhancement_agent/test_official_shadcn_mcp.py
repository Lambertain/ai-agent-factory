# -*- coding: utf-8 -*-
"""
Тест официального Shadcn MCP в UI/UX Enhancement Agent
Implementation Engineer: проверка интеграции с официальным MCP
"""

import sys
from pathlib import Path

# Настройка путей
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from dependencies import UIUXEnhancementDependencies

class OfficialShadcnMCPTest:
    """Тест официального Shadcn MCP интеграции"""

    def __init__(self):
        print("=== OFFICIAL SHADCN MCP TEST ===")
        print()

        # Создаю зависимости агента
        try:
            self.deps = UIUXEnhancementDependencies(
                api_key="test_key",
                domain_type="ui",
                design_system_type="shadcn/ui",
                css_framework="tailwind"
            )
            print("✅ AGENT INIT: SUCCESS")
            print(f"Agent Type: {self.deps.agent_type}")
            print(f"MCP Enabled: {self.deps.enable_mcp_integration}")
            print(f"Custom Servers: {self.deps.custom_mcp_servers}")

        except Exception as e:
            print(f"❌ AGENT INIT: FAILED - {e}")
            return

    def test_official_mcp_detection(self):
        """Тест определения официального Shadcn MCP"""
        print()
        print("=== OFFICIAL MCP DETECTION TEST ===")

        instructions = """
🎯 ЗАДАЧА: Проверить доступность официального Shadcn MCP

Claude Code должен иметь доступ к следующим инструментам:
- shadcn component generation tools
- registry browsing tools
- template creation tools

ЕСЛИ ты видишь shadcn MCP инструменты в Claude Code:
✅ Покажи список доступных shadcn инструментов
✅ Попробуй сгенерировать простой Button компонент
✅ Покажи код компонента

ЕСЛИ shadcn MCP НЕ активен:
❌ Сообщи что MCP недоступен
❌ Предложи решения для активации

⚡ ВАЖНО: Используй ТОЛЬКО официальный shadcn MCP, установленный через:
'npx shadcn@latest mcp init --client claude'
        """

        print(instructions)
        return instructions

    def test_component_generation_request(self):
        """Тест запроса на генерацию компонента"""
        print()
        print("=== COMPONENT GENERATION REQUEST ===")

        request = """
🎨 ГЕНЕРАЦИЯ SHADCN КОМПОНЕНТА

Используй официальный Shadcn MCP для создания:

**Компонент:** Button
**Требования:**
- React + TypeScript
- Tailwind CSS styling
- CVA variants для размеров (sm, md, lg)
- CVA variants для стилей (default, destructive, outline)
- ForwardRef pattern
- Proper accessibility attributes
- cn() utility integration

**Ожидаемый результат:**
Полный TypeScript код готового к использованию Button компонента
        """

        print(request)
        return request

def main():
    """Основная функция теста"""
    print("=" * 60)
    print("UI/UX AGENT - OFFICIAL SHADCN MCP INTEGRATION TEST")
    print("Implementation Engineer: Testing official MCP connection")
    print("=" * 60)

    # Создаю тест
    test = OfficialShadcnMCPTest()

    if not hasattr(test, 'deps'):
        print("FATAL: Could not initialize test")
        return False

    # Проверяю определение MCP
    detection_result = test.test_official_mcp_detection()

    # Тестирую запрос на генерацию
    generation_result = test.test_component_generation_request()

    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("1. Перезапусти Claude Code если shadcn MCP не виден")
    print("2. Включи галочку Shadcn в MCP Integrations")
    print("3. Используй этот тест для проверки доступности инструментов")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)