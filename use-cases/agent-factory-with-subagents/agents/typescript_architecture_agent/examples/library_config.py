"""
Пример конфигурации TypeScript Architecture Agent для Library проекта.

Демонстрирует настройку агента для npm пакетов и библиотек
с фокусом на excellent TypeScript support и public API design.
"""

from ..dependencies import TypeScriptArchitectureDependencies


def setup_npm_library_agent():
    """Настройка агента для npm library проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="TypeScriptLibrary",
        project_type="library",
        framework="npm",
        architecture_focus="maintainability",
        analysis_mode="full",

        # Library специфичные настройки
        target_type_coverage=0.99,  # Максимальная типизация для библиотек
        performance_budget_ms=2000,  # Быстрая компиляция для разработчиков
        max_complexity_score=8,  # Простые и понятные типы для пользователей

        # Domain-specific типы для Library
        domain_types={
            "library_types": [
                "PublicAPI", "Config", "Options", "Plugin",
                "Middleware", "Handler", "Callback", "Event"
            ],
            "utility_types": [
                "Utility", "Helper", "Transformer", "Validator",
                "Parser", "Formatter", "Converter"
            ],
            "generic_types": [
                "Generic", "Conditional", "Mapped", "Template",
                "Recursive", "Branded", "Nominal"
            ],
            "export_types": [
                "DefaultExport", "NamedExport", "TypeOnlyExport",
                "ReExport", "ModuleExport"
            ]
        },

        # Архитектурные паттерны для Library
        architectural_patterns=[
            "Factory Pattern",
            "Builder Pattern",
            "Plugin Architecture",
            "Public API Design",
            "Type-only Exports",
            "Generic Utilities",
            "Configuration Objects",
            "Error Handling Strategy"
        ],

        # RAG теги для Library знаний
        knowledge_tags=[
            "typescript-architecture",
            "library-design",
            "public-api",
            "npm-packaging",
            "type-exports",
            "generic-programming",
            "utility-types",
            "agent-knowledge"
        ]
    )


def setup_utility_library_agent():
    """Настройка агента для utility library проекта."""
    return TypeScriptArchitectureDependencies(
        project_name="UtilityLibrary",
        project_type="library",
        framework="utility",
        architecture_focus="performance",
        analysis_mode="types",

        # Utility специфичные настройки
        target_type_coverage=0.99,
        performance_budget_ms=1500,  # Максимально быстрая компиляция
        max_complexity_score=6,  # Простые utility типы

        # Domain-specific типы для Utility
        domain_types={
            "utility_functions": [
                "ArrayUtility", "ObjectUtility", "StringUtility",
                "NumberUtility", "DateUtility", "PromiseUtility"
            ],
            "type_helpers": [
                "DeepPartial", "DeepRequired", "DeepReadonly",
                "Prettify", "PickByType", "OmitByType"
            ],
            "conditional_types": [
                "If", "Unless", "Switch", "Case",
                "IsNever", "IsAny", "IsUnknown"
            ]
        },

        # Архитектурные паттерны для Utility
        architectural_patterns=[
            "Type Utilities",
            "Function Overloads",
            "Conditional Type Logic",
            "Mapped Type Transformations",
            "Template Literal Types",
            "Recursive Type Definitions"
        ],

        # RAG теги для Utility знаний
        knowledge_tags=[
            "typescript-architecture",
            "utility-types",
            "advanced-types",
            "type-inference",
            "generic-programming",
            "conditional-types",
            "mapped-types",
            "agent-knowledge"
        ]
    )


def example_library_analysis():
    """Пример анализа library TypeScript проекта."""
    npm_deps = setup_npm_library_agent()

    return {
        "dependencies": npm_deps,
        "analysis_focus": [
            "Public API type definitions",
            "Generic type parameters",
            "Type export strategies",
            "Documentation generation",
            "Backward compatibility"
        ],
        "expected_optimizations": [
            "Clear and intuitive public API types",
            "Comprehensive generic type support",
            "Proper type-only exports",
            "Excellent IntelliSense experience",
            "Zero runtime overhead types",
            "Branded types for type safety",
            "Utility type composition"
        ],
        "performance_targets": {
            "compile_time": "< 2s",
            "type_resolution": "< 100ms",
            "intellisense_response": "< 50ms",
            "bundle_size_impact": "0KB (types only)"
        },
        "library_patterns": [
            "Factory functions with typed options",
            "Plugin system with typed interfaces",
            "Builder pattern with fluent API",
            "Event system with typed events",
            "Configuration with default values",
            "Error types for different scenarios"
        ],
        "distribution_requirements": [
            "Clean .d.ts file generation",
            "Proper package.json types field",
            "Compatible with module resolution",
            "Support for both CJS and ESM",
            "No internal type leakage"
        ]
    }


if __name__ == "__main__":
    print("📦 LIBRARY TYPESCRIPT ARCHITECTURE")
    print("=" * 50)

    config = example_library_analysis()
    deps = config["dependencies"]

    print(f"Project type: {deps.project_type}")
    print(f"Framework: {deps.framework}")
    print(f"Architecture focus: {deps.architecture_focus}")
    print(f"Type coverage target: {deps.target_type_coverage * 100}%")
    print(f"Performance budget: {deps.performance_budget_ms}ms")
    print("\nReady for library TypeScript architecture analysis!")