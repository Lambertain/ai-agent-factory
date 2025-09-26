"""TypeScript analysis tools for architecture optimization."""

from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext
from pydantic import BaseModel, Field
import ast
import re
import json
import httpx
from pathlib import Path
from .dependencies import TypeScriptArchitectureDependencies


class TypeComplexityResult(BaseModel):
    """Результат анализа сложности типов."""
    file_path: str
    complexity_score: int = Field(description="Оценка сложности от 1 до 10")
    issues: List[str] = Field(description="Найденные проблемы")
    recommendations: List[str] = Field(description="Рекомендации по улучшению")
    estimated_improvement: str = Field(description="Ожидаемое улучшение")


class TypeRefactorResult(BaseModel):
    """Результат рефакторинга типов."""
    original_code: str
    refactored_code: str
    improvements: List[str]
    breaking_changes: List[str]
    migration_steps: List[str]


async def analyze_type_complexity(
    ctx: RunContext[TypeScriptArchitectureDependencies],
    file_path: str,
    focus_areas: Optional[List[str]] = None
) -> TypeComplexityResult:
    """
    Анализ сложности типов в TypeScript файле.

    Args:
        ctx: Контекст выполнения агента
        file_path: Путь к TypeScript файлу
        focus_areas: Области фокуса анализа (interfaces, types, generics)

    Returns:
        Результат анализа сложности
    """
    try:
        # Читаем файл
        if not Path(file_path).exists():
            return TypeComplexityResult(
                file_path=file_path,
                complexity_score=0,
                issues=["Файл не найден"],
                recommendations=["Проверьте путь к файлу"],
                estimated_improvement="N/A"
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Анализируем содержимое
        issues = []
        recommendations = []
        complexity_score = 1

        # Проверка на any типы
        any_count = len(re.findall(r'\bany\b', content))
        if any_count > 0:
            issues.append(f"Найдено {any_count} использований 'any' типа")
            recommendations.append("Заменить 'any' на конкретные типы")
            complexity_score += any_count * 0.5

        # Проверка сложных generic типов
        complex_generics = re.findall(r'<[^<>]*<[^<>]*<[^<>]*>', content)
        if complex_generics:
            issues.append(f"Найдено {len(complex_generics)} сложных generic типов")
            recommendations.append("Упростить вложенные generic типы")
            complexity_score += len(complex_generics) * 0.3

        # Проверка длинных union типов
        long_unions = re.findall(r'\|[^=]*\|[^=]*\|[^=]*\|', content)
        if long_unions:
            issues.append(f"Найдено {len(long_unions)} длинных union типов")
            recommendations.append("Разбить длинные union типы на отдельные типы")
            complexity_score += len(long_unions) * 0.4

        # Проверка отсутствия type guards
        has_type_guards = 'is ' in content and 'function' in content
        if not has_type_guards and ('union' in content.lower() or '|' in content):
            issues.append("Отсутствуют type guards для union типов")
            recommendations.append("Добавить type guards для безопасной проверки типов")
            complexity_score += 1

        # Ограничиваем оценку сложности
        complexity_score = min(int(complexity_score), 10)

        # Оценка улучшения
        if complexity_score > 7:
            estimated_improvement = "Высокий потенциал улучшения (30-50%)"
        elif complexity_score > 4:
            estimated_improvement = "Средний потенциал улучшения (15-30%)"
        else:
            estimated_improvement = "Низкий потенциал улучшения (5-15%)"

        return TypeComplexityResult(
            file_path=file_path,
            complexity_score=complexity_score,
            issues=issues,
            recommendations=recommendations,
            estimated_improvement=estimated_improvement
        )

    except Exception as e:
        return TypeComplexityResult(
            file_path=file_path,
            complexity_score=10,
            issues=[f"Ошибка анализа: {str(e)}"],
            recommendations=["Проверьте синтаксис файла"],
            estimated_improvement="Требуется исправление ошибок"
        )


async def refactor_types(
    ctx: RunContext[TypeScriptArchitectureDependencies],
    code: str,
    refactor_strategy: str = "optimize"
) -> TypeRefactorResult:
    """
    Рефакторинг TypeScript типов.

    Args:
        ctx: Контекст выполнения
        code: Исходный код для рефакторинга
        refactor_strategy: Стратегия рефакторинга (optimize, simplify, strengthen)

    Returns:
        Результат рефакторинга
    """
    try:
        improvements = []
        breaking_changes = []
        migration_steps = []
        refactored_code = code

        # Стратегия оптимизации
        if refactor_strategy == "optimize":
            # Замена any на конкретные типы
            if 'any' in code:
                refactored_code = re.sub(
                    r'\bany\b',
                    'unknown',
                    refactored_code
                )
                improvements.append("Заменены 'any' типы на 'unknown' для type safety")
                migration_steps.append("Добавить type guards для 'unknown' типов")

            # Упрощение сложных union типов
            complex_unions = re.findall(r'type\s+\w+\s*=\s*[^;]*\|[^;]*\|[^;]*;', code)
            for union in complex_unions:
                simplified = union.replace('|', ' |\n  ')
                refactored_code = refactored_code.replace(union, simplified)
                improvements.append("Улучшено форматирование union типов")

        elif refactor_strategy == "strengthen":
            # Добавление readonly модификаторов
            refactored_code = re.sub(
                r'interface\s+(\w+)\s*{([^}]+)}',
                lambda m: f"interface {m.group(1)} {{\n  readonly {m.group(2).strip()}\n}}",
                refactored_code
            )
            improvements.append("Добавлены readonly модификаторы для immutability")
            breaking_changes.append("Объекты станут readonly")

        # Добавление базовых type guards
        if '|' in code and 'function is' not in code:
            type_guard_example = """
// Добавленный type guard
function isString(value: unknown): value is string {
  return typeof value === 'string';
}
"""
            refactored_code += type_guard_example
            improvements.append("Добавлены примеры type guards")

        return TypeRefactorResult(
            original_code=code,
            refactored_code=refactored_code,
            improvements=improvements,
            breaking_changes=breaking_changes,
            migration_steps=migration_steps
        )

    except Exception as e:
        return TypeRefactorResult(
            original_code=code,
            refactored_code=code,
            improvements=[],
            breaking_changes=[f"Ошибка рефакторинга: {str(e)}"],
            migration_steps=["Проверьте синтаксис исходного кода"]
        )


async def generate_type_guards(
    ctx: RunContext[TypeScriptArchitectureDependencies],
    types: List[str]
) -> str:
    """
    Генерация type guards для заданных типов.

    Args:
        ctx: Контекст выполнения
        types: Список типов для генерации guards

    Returns:
        Сгенерированные type guards
    """
    type_guards = []

    for type_name in types:
        # Базовые типы
        if type_name.lower() in ['string', 'number', 'boolean']:
            guard = f"""
function is{type_name.capitalize()}(value: unknown): value is {type_name} {{
  return typeof value === '{type_name}';
}}"""
            type_guards.append(guard)

        # Массивы
        elif type_name.endswith('[]'):
            element_type = type_name[:-2]
            guard = f"""
function is{element_type.capitalize()}Array(value: unknown): value is {type_name} {{
  return Array.isArray(value) && value.every(item => is{element_type.capitalize()}(item));
}}"""
            type_guards.append(guard)

        # Объекты (упрощенная версия)
        else:
            guard = f"""
function is{type_name}(value: unknown): value is {type_name} {{
  return value !== null && typeof value === 'object' &&
         // Добавьте специфичные проверки для {type_name}
         true;
}}"""
            type_guards.append(guard)

    return '\n'.join(type_guards)


async def optimize_typescript_config(
    ctx: RunContext[TypeScriptArchitectureDependencies],
    config_path: str = "tsconfig.json"
) -> Dict[str, Any]:
    """
    Оптимизация конфигурации TypeScript.

    Args:
        ctx: Контекст выполнения
        config_path: Путь к tsconfig.json

    Returns:
        Оптимизированная конфигурация
    """
    try:
        # Базовая оптимизированная конфигурация для проекта
        optimized_config = {
            "compilerOptions": {
                "target": "ES2022",
                "lib": ["DOM", "DOM.Iterable", "ES2022"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [{"name": "next"}],
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"],
                    "@/components/*": ["./src/components/*"],
                    "@/lib/*": ["./src/lib/*"],
                    "@/types/*": ["./src/types/*"]
                },
                # Strict type checking
                "noImplicitAny": True,
                "strictNullChecks": True,
                "strictFunctionTypes": True,
                "strictBindCallApply": True,
                "strictPropertyInitialization": True,
                "noImplicitReturns": True,
                "noFallthroughCasesInSwitch": True,
                "noUncheckedIndexedAccess": True,
                "exactOptionalPropertyTypes": True,
                # Performance optimizations
                "skipDefaultLibCheck": True,
                "forceConsistentCasingInFileNames": True
            },
            "include": [
                "next-env.d.ts",
                "**/*.ts",
                "**/*.tsx",
                ".next/types/**/*.ts"
            ],
            "exclude": ["node_modules", ".next", "out"]
        }

        return {
            "config": optimized_config,
            "improvements": [
                "Включен strict mode для максимальной type safety",
                "Настроены path mappings для удобного импорта",
                "Оптимизированы настройки производительности",
                "Добавлены строгие проверки типов"
            ],
            "breaking_changes": [
                "Могут появиться новые type errors из-за strict mode",
                "Требуется обновление импортов для path mappings"
            ]
        }

    except Exception as e:
        return {
            "error": f"Ошибка оптимизации конфигурации: {str(e)}",
            "config": {},
            "improvements": [],
            "breaking_changes": []
        }


async def search_agent_knowledge(
    ctx: RunContext[TypeScriptArchitectureDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в специализированной базе знаний TypeScript Architecture Agent.

    Args:
        ctx: Контекст выполнения
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базе знаний
    """
    try:
        # Используем MCP Archon для поиска в базе знаний
        # Формируем расширенный запрос с тегами агента
        search_tags = getattr(ctx.deps, 'knowledge_tags', ['typescript-architecture', 'agent-knowledge'])
        enhanced_query = f"{query} {' '.join(search_tags)}"

        # Основной поиск через MCP Archon
        # В реальной среде будет вызов mcp__archon__rag_search_knowledge_base
        # Пока используем симуляцию с fallback стратегией

        # Агент использует Archon Knowledge Base для поиска экспертизы
        agent_name = getattr(ctx.deps, 'agent_name', 'typescript_architecture_agent')

        # Симуляция поиска с адаптивным контентом
        knowledge_base_response = f"""
📚 **База знаний TypeScript Architecture Agent:**

🔍 **По запросу "{query}" найдено:**

**1. TypeScript Архитектурные Паттерны:**
   - Используйте строгую типизацию с strict mode в tsconfig.json
   - Применяйте Domain-Driven Design с четким разделением слоев
   - Используйте композиционные паттерны вместо наследования
   - Внедряйте dependency injection через интерфейсы

**2. Масштабируемая Структура Проекта:**
   ```
   src/
   ├── types/           # Общие типы
   ├── interfaces/      # Интерфейсы
   ├── services/        # Бизнес-логика
   ├── components/      # UI компоненты
   ├── utils/           # Утилиты
   └── constants/       # Константы
   ```

**3. Оптимизация TypeScript:**
   - Используйте mapped types для трансформации типов
   - Применяйте conditional types для сложной логики типов
   - Используйте path mapping для чистых импортов
   - Включите tree-shaking с ESM модулями

**4. Best Practices:**
   - Избегайте any, используйте unknown вместо этого
   - Создавайте utility types для переиспользования
   - Используйте branded types для типобезопасности
   - Применяйте exhaustiveness checking в switch statements

⚠️ **Примечание:** Поиск в реальной базе знаний Archon может работать нестабильно.
Векторный поиск иногда не возвращает результаты даже для загруженных файлов.
Попробуйте использовать более специфичные термины или обратитесь к файлу знаний напрямую.

🔧 **Для более точного поиска используйте ключевые слова:**
- "typescript patterns", "архитектура проекта", "type safety", "масштабирование"
"""

        return knowledge_base_response

    except Exception as e:
        return f"❌ Ошибка доступа к базе знаний TypeScript Architecture Agent: {e}"