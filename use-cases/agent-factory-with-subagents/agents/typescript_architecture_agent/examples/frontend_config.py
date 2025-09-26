"""
Пример конфигурации TypeScript Architecture Agent для Frontend проекта.

Демонстрирует настройку агента для React/Vue/Angular приложений
с фокусом на type-safe компоненты и производительность.
"""

from ..dependencies import TypeScriptArchitectureDependencies


def setup_react_frontend_agent():
    """Настройка агента для React frontend проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="ReactApp",
        project_type="frontend",
        framework="react",
        architecture_focus="type-safety",
        analysis_mode="full",

        # Frontend специфичные настройки
        target_type_coverage=0.95,  # Высокое покрытие типами для UI
        performance_budget_ms=3000,  # Быстрая компиляция для dev опыта
        max_complexity_score=8,  # Умеренная сложность для компонентов

        # Domain-specific типы для React
        domain_types={
            "react_types": [
                "ComponentProps", "JSX.Element", "ReactNode", "FC",
                "Component", "RefObject", "MutableRefObject"
            ],
            "event_types": [
                "MouseEvent", "ChangeEvent", "FormEvent", "KeyboardEvent"
            ],
            "hook_types": [
                "useState", "useEffect", "useContext", "useReducer",
                "useCallback", "useMemo", "useRef"
            ]
        },

        # Архитектурные паттерны для React
        architectural_patterns=[
            "Component Composition",
            "Custom Hooks",
            "Context API",
            "Error Boundaries",
            "Higher-Order Components",
            "Render Props"
        ],

        # RAG теги для React знаний
        knowledge_tags=[
            "typescript-architecture",
            "react",
            "frontend-architecture",
            "component-design",
            "jsx",
            "hooks",
            "context",
            "state-management",
            "agent-knowledge"
        ]
    )


def setup_vue_frontend_agent():
    """Настройка агента для Vue frontend проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="VueApp",
        project_type="frontend",
        framework="vue",
        architecture_focus="type-safety",
        analysis_mode="full",

        # Vue специфичные настройки
        target_type_coverage=0.94,
        performance_budget_ms=3200,
        max_complexity_score=8,

        # Domain-specific типы для Vue
        domain_types={
            "vue_types": [
                "Component", "PropType", "ComputedRef", "Ref",
                "VNode", "ComponentInstance"
            ],
            "composition_api": [
                "ref", "computed", "watch", "reactive",
                "readonly", "unref", "toRef", "toRefs"
            ],
            "directives": [
                "v-model", "v-if", "v-for", "v-show", "v-bind"
            ]
        },

        # Архитектурные паттерны для Vue
        architectural_patterns=[
            "Composition API",
            "Provide/Inject",
            "Single File Components",
            "Custom Directives",
            "Plugins",
            "Reactive State"
        ],

        # RAG теги для Vue знаний
        knowledge_tags=[
            "typescript-architecture",
            "vue",
            "frontend-architecture",
            "composition-api",
            "reactivity",
            "directives",
            "sfc",
            "agent-knowledge"
        ]
    )


def example_frontend_analysis():
    """Пример анализа frontend TypeScript проекта."""
    react_deps = setup_react_frontend_agent()

    return {
        "dependencies": react_deps,
        "analysis_focus": [
            "Component props type safety",
            "Hook dependencies type inference",
            "Event handler type annotations",
            "Context API type definitions",
            "State management type patterns"
        ],
        "expected_optimizations": [
            "Generic component props for reusability",
            "Strict event handler typing",
            "Custom hook return type definitions",
            "Context value type safety",
            "Form validation type schemas",
            "API response type mapping",
            "Error boundary type handling"
        ],
        "performance_targets": {
            "type_check_time": "< 3s",
            "intellisense_response": "< 100ms",
            "component_inference": "< 500ms",
            "build_time_impact": "< 10%"
        },
        "frontend_patterns": [
            "Compound components with typed props",
            "Render prop pattern with generics",
            "Higher-order component typing",
            "Custom hook type inference",
            "Context API with typed providers",
            "Form handling with typed validation"
        ]
    }


if __name__ == "__main__":
    print("⚛️ FRONTEND TYPESCRIPT ARCHITECTURE")
    print("=" * 50)

    config = example_frontend_analysis()
    deps = config["dependencies"]

    print(f"Project type: {deps.project_type}")
    print(f"Framework: {deps.framework}")
    print(f"Architecture focus: {deps.architecture_focus}")
    print(f"Type coverage target: {deps.target_type_coverage * 100}%")
    print(f"Performance budget: {deps.performance_budget_ms}ms")
    print("\nReady for frontend TypeScript architecture analysis!")