"""
UI/UX Design & Enhancement Agent - универсальный агент для дизайна и улучшения интерфейсов.

Агент специализируется на полном спектре UI/UX работы: дизайн с нуля, прототипирование,
улучшение существующих интерфейсов, создание дизайн систем, wireframes,
Tailwind CSS оптимизации, работе с различными компонентными библиотеками
и обеспечении accessibility. Адаптируется под любой проект и домен.
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from .dependencies import UIUXEnhancementDependencies
from ..common import check_pm_switch
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .providers import get_llm_model
from .prompts import get_system_prompt
from .tools import (
    analyze_ui_accessibility,
    optimize_tailwind_classes,
    enhance_shadcn_component,
    analyze_ux_patterns,
    generate_component_variants,
    validate_design_system,
    design_interface_from_scratch,
    create_design_system,
    create_wireframes,
    prototype_user_flow,
    # MCP Integration Tools
    use_shadcn_mcp_component,
    use_puppeteer_mcp_screenshot,
    use_context7_mcp_memory,
    mcp_ui_performance_analysis,
    mcp_accessibility_audit
)


# Create universal UI/UX enhancement agent with decorators
uiux_agent = create_universal_pydantic_agent(
    model=get_llm_model("uiux"),
    deps_type=UIUXEnhancementDependencies,
    system_prompt=lambda ctx: get_system_prompt(ctx.deps),
    agent_type="uiux_enhancement",
    knowledge_tags=["uiux", "design", "accessibility", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="ui.shadcn.com",
    with_collective_tools=True,
    with_knowledge_tool=True,
    retries=2
)

# Register agent in global registry
register_agent("uiux_enhancement", uiux_agent, agent_type="uiux_enhancement")

# Register UI/UX-specific tools
uiux_agent.tool(analyze_ui_accessibility)
uiux_agent.tool(optimize_tailwind_classes)
uiux_agent.tool(enhance_shadcn_component)
uiux_agent.tool(analyze_ux_patterns)
uiux_agent.tool(generate_component_variants)
uiux_agent.tool(validate_design_system)
uiux_agent.tool(design_interface_from_scratch)
uiux_agent.tool(create_design_system)
uiux_agent.tool(create_wireframes)
uiux_agent.tool(prototype_user_flow)

# Register MCP integration tools
uiux_agent.tool(use_shadcn_mcp_component)
uiux_agent.tool(use_puppeteer_mcp_screenshot)
uiux_agent.tool(use_context7_mcp_memory)
uiux_agent.tool(mcp_ui_performance_analysis)
uiux_agent.tool(mcp_accessibility_audit)

# Collective work tools and knowledge search now added automatically via decorators


# Factory function for MCP toolsets support
def create_uiux_agent(deps: UIUXEnhancementDependencies) -> Agent[UIUXEnhancementDependencies, str]:
    """Create UI/UX agent with MCP toolsets."""
    mcp_toolsets = deps.get_mcp_toolsets()

    if mcp_toolsets:
        # Use override to add MCP toolsets
        return uiux_agent.override(toolsets=mcp_toolsets)

    return uiux_agent


async def run_uiux_enhancement(
    task: str,
    component_code: Optional[str] = None,
    requirements: Optional[Dict[str, Any]] = None,
    project_path: str = "",
    session_id: Optional[str] = None,
    domain_type: str = "web_application",
    project_type: str = "spa",
    design_system: str = "shadcn/ui",
    css_framework: str = "tailwind"
) -> str:
    """
    Выполнить улучшение UI/UX с адаптацией под тип проекта.

    Args:
        task: Описание задачи улучшения
        component_code: Код компонента для анализа (опционально)
        requirements: Дополнительные требования
        project_path: Путь к проекту
        session_id: ID сессии для отслеживания
        domain_type: Тип домена (ecommerce, saas, blog, social, etc.)
        project_type: Тип проекта (spa, mpa, landing, dashboard, etc.)
        design_system: Используемая дизайн система
        css_framework: CSS фреймворк

    Returns:
        Результат анализа и рекомендации по улучшению
    """
    deps = UIUXEnhancementDependencies(
        api_key="dummy_key",  # Требуется для базового класса
        project_path=project_path,
        session_id=session_id,
        domain_type=domain_type,
        project_type=project_type,
        design_system_type=design_system,
        css_framework=css_framework,
        knowledge_tags=["uiux-enhancement", domain_type, design_system, css_framework],
        knowledge_domain="ui.shadcn.com"
    )

    # Создаем агента с MCP поддержкой (инструменты уже зарегистрированы)
    agent_with_mcp = create_uiux_agent(deps)

    # Формируем контекст для агента
    context = f"""
    Задача: {task}

    Компонент для анализа: {component_code or 'Не предоставлен'}

    Требования: {requirements or 'Стандартные требования UI/UX'}

    Путь к проекту: {project_path}

    🔧 MCP Серверы: {', '.join([server for server in deps.custom_mcp_servers]) if deps.custom_mcp_servers else 'Отключены'}
    """

    try:
        result = await agent_with_mcp.run(context, deps=deps)
        return result.data

    except Exception as e:
        error_msg = f"Ошибка выполнения UI/UX улучшения: {e}"
        print(f"🚨 {error_msg}")
        # Fallback к базовому агенту без MCP
        print("🔄 Пытаемся использовать базовый агент без MCP...")
        try:
            context_fallback = f"""
            Задача: {task}

            Компонент для анализа: {component_code or 'Не предоставлен'}

            Требования: {requirements or 'Стандартные требования UI/UX'}

            Путь к проекту: {project_path}

            ⚠️  MCP серверы недоступны, используется базовая функциональность
            """

            result = await uiux_agent.run(context_fallback, deps=deps)
            return result.data
        except Exception as fallback_error:
            return f"Критическая ошибка: {error_msg}\nFallback error: {fallback_error}"


def run_uiux_enhancement_sync(
    task: str,
    component_code: Optional[str] = None,
    requirements: Optional[Dict[str, Any]] = None,
    project_path: str = "",
    session_id: Optional[str] = None,
    domain_type: str = "web_application",
    project_type: str = "spa",
    design_system: str = "shadcn/ui",
    css_framework: str = "tailwind"
) -> str:
    """Синхронная версия для простого использования."""
    return asyncio.run(run_uiux_enhancement(
        task=task,
        component_code=component_code,
        requirements=requirements,
        project_path=project_path,
        session_id=session_id,
        domain_type=domain_type,
        project_type=project_type,
        design_system=design_system,
        css_framework=css_framework
    ))


def check_mcp_recommendations() -> str:
    """
    Проверить и предложить установку рекомендуемых MCP серверов для UI/UX работы.

    Returns:
        Рекомендации по установке MCP серверов
    """
    return """
    💡 **РЕКОМЕНДАЦИЯ: MCP СЕРВЕРЫ ДЛЯ UI/UX РАЗРАБОТКИ**

    Для максимальной эффективности UI/UX Enhancement Agent рекомендуется установить специализированные MCP серверы:

    🎨 **SHADCN MCP SERVER** (высокий приоритет)
    Преимущества:
    - Автоматическая интеграция с shadcn/ui компонентами
    - Валидация компонентов по shadcn стандартам
    - Генерация кода компонентов из описания
    - Обновление компонентов до последних версий

    Установка:
    ```bash
    npm install @modelcontextprotocol/server-shadcn
    ```

    ⚡ **TAILWIND CSS MCP SERVER** (рекомендуется)
    Преимущества:
    - Оптимизация Tailwind классов
    - Анализ bundle size влияния
    - Предложения по рефакторингу CSS
    - Проверка consistency утилит

    Установка:
    ```bash
    npm install @modelcontextprotocol/server-tailwind
    ```

    🎯 **FIGMA MCP SERVER** (опционально)
    Преимущества:
    - Синхронизация дизайна с кодом
    - Автоматическое извлечение дизайн токенов
    - Проверка соответствия макетам
    - Export компонентов из Figma

    Установка:
    ```bash
    npm install @modelcontextprotocol/server-figma
    ```

    📊 **LIGHTHOUSE MCP SERVER** (для аудита)
    Преимущества:
    - Автоматический performance аудит
    - Accessibility проверки
    - SEO анализ компонентов
    - Best practices валидация

    Установка:
    ```bash
    npm install @modelcontextprotocol/server-lighthouse
    ```

    🔧 **НАСТРОЙКА В CLAUDE CODE:**

    Добавь серверы в конфигурацию Claude Code:
    `C:\\Users\\Admin\\AppData\\Roaming\\Claude\\claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "shadcn": {
          "command": "npx",
          "args": ["@modelcontextprotocol/server-shadcn"]
        },
        "tailwind": {
          "command": "npx",
          "args": ["@modelcontextprotocol/server-tailwind"]
        },
        "figma": {
          "command": "npx",
          "args": ["@modelcontextprotocol/server-figma"],
          "env": {
            "FIGMA_ACCESS_TOKEN": "your_figma_token"
          }
        }
      }
    }
    ```

    После установки перезапусти Claude Code для активации серверов.

    📖 **ДОКУМЕНТАЦИЯ:**
    https://docs.claude.com/en/docs/claude-code/mcp

    ⚡ Эти MCP серверы значительно расширят возможности UI/UX анализа и сделают работу более эффективной!
    """


if __name__ == "__main__":
    # Показываем рекомендации по MCP серверам
    print(check_mcp_recommendations())
    print("\n" + "="*80 + "\n")

    # Пример использования агента (универсальный)
    sample_task = """
    Проанализируй и улучши этот компонент карточки.
    Нужно добавить лучшую accessibility, оптимизировать CSS классы
    и убедиться, что компонент соответствует современным стандартам дизайна.
    """

    sample_component = '''
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
      <img src={item.image} alt={item.title} className="w-full h-48 object-cover rounded-md mb-4" />
      <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
      <p className="text-gray-600 mb-4">{item.description}</p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-500">{item.date}</span>
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          View Details
        </button>
      </div>
    </div>
    '''

    print("🎨 Запуск UI/UX Enhancement Agent...")
    print("📋 Задача:", sample_task)
    print("🔧 Компонент предоставлен для анализа")

    result = run_uiux_enhancement_sync(
        task=sample_task,
        component_code=sample_component,
        requirements={
            "accessibility_level": "WCAG 2.1 AA",
            "design_system": "custom",  # Автоматически определяется из кода
            "theme_support": ["light", "dark"],
            "mobile_first": True
        }
    )

    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТ АНАЛИЗА UI/UX:")
    print("="*60)
    print(result)