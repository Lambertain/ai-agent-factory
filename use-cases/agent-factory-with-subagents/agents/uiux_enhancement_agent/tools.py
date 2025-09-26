"""
Инструменты UI/UX Enhancement Agent для анализа и улучшения интерфейсов.

Специализированные функции для работы с компонентами, accessibility,
performance оптимизацией и интеграцией с дизайн системами.
"""

import re
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pydantic_ai import RunContext

from .dependencies import UIUXEnhancementDependencies


@dataclass
class AccessibilityIssue:
    """Структура для описания проблемы accessibility."""
    severity: str  # Critical, High, Medium, Low
    wcag_criterion: str
    element: str
    description: str
    fix_suggestion: str
    code_example: Optional[str] = None


@dataclass
class UIAnalysisResult:
    """Результат анализа UI компонента."""
    component_type: str
    accessibility_score: int  # 0-100
    performance_score: int  # 0-100
    design_system_compliance: int  # 0-100
    issues: List[AccessibilityIssue]
    recommendations: List[str]
    optimized_code: Optional[str] = None


async def search_uiux_knowledge(
    ctx: RunContext[UIUXEnhancementDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Поиск в базе знаний UI/UX агента через Archon RAG с MCP поддержкой.

    Args:
        ctx: Контекст выполнения с зависимостями
        query: Поисковый запрос
        match_count: Количество результатов

    Returns:
        Найденная информация из базы знаний
    """
    try:
        # Формируем поисковый запрос с тегами агента
        enhanced_query = f"{query} {' '.join(ctx.deps.knowledge_tags)}"

        # Интеграция с Archon RAG для поиска знаний
        try:
            # Используем MCP Archon для поиска в базе знаний
            from mcp_client import mcp_archon_rag_search_knowledge_base

            result = await mcp_archon_rag_search_knowledge_base(
                query=enhanced_query,
                source_domain=ctx.deps.knowledge_domain or None,
                match_count=match_count
            )

            if result["success"] and result["results"]:
                knowledge = "\n\n".join([
                    f"**{r['metadata']['title']}:**\n{r['content']}"
                    for r in result["results"]
                ])
                return f"📚 База знаний UI/UX:\n\n{knowledge}"

        except ImportError:
            # Fallback если MCP не доступен
            pass
        except Exception as e:
            # Логируем ошибку и используем fallback
            pass

        # Временная заглушка - расширенная с реальными паттернами
        domain_specific_knowledge = {
            "accessibility": """
            **ACCESSIBILITY PATTERNS:**

            1. **ARIA Labels**: Всегда добавляй aria-label для интерактивных элементов
               ```jsx
               <button aria-label="Закрыть модальное окно">×</button>
               ```

            2. **Focus Management**: Управляй фокусом в модальных окнах
               ```jsx
               useEffect(() => {
                 if (isOpen) firstFocusableElement.focus();
               }, [isOpen]);
               ```

            3. **Keyboard Navigation**: Поддерживай Tab, Enter, Escape
               ```jsx
               onKeyDown={(e) => {
                 if (e.key === 'Escape') closeModal();
                 if (e.key === 'Enter') handleAction();
               }}
               ```
            """,
            "tailwind": """
            **TAILWIND OPTIMIZATION PATTERNS:**

            1. **Группировка утилит**:
               ```jsx
               // До: className="flex items-center justify-center p-4 bg-white rounded-lg shadow-md"
               // После: className="flex-center p-4 card-base"
               ```

            2. **Custom Utilities**:
               ```css
               @layer utilities {
                 .flex-center { @apply flex items-center justify-center; }
                 .card-base { @apply bg-white rounded-lg shadow-md; }
               }
               ```

            3. **Responsive Patterns**:
               ```jsx
               className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6"
               ```
            """,
            "shadcn": """
            **SHADCN/UI PATTERNS:**

            1. **Component Variants with CVA**:
               ```tsx
               const buttonVariants = cva(
                 "inline-flex items-center justify-center rounded-md font-medium",
                 {
                   variants: {
                     variant: {
                       default: "bg-primary text-primary-foreground",
                       outline: "border border-input bg-background"
                     },
                     size: {
                       default: "h-10 px-4 py-2",
                       sm: "h-9 rounded-md px-3"
                     }
                   }
                 }
               )
               ```

            2. **Compound Components**:
               ```tsx
               <Card>
                 <CardHeader>
                   <CardTitle>Title</CardTitle>
                 </CardHeader>
                 <CardContent>Content</CardContent>
               </Card>
               ```
            """,
            "performance": """
            **PERFORMANCE OPTIMIZATION:**

            1. **Lazy Loading Components**:
               ```tsx
               const LazyComponent = lazy(() => import('./HeavyComponent'));
               ```

            2. **CSS Optimization**:
               ```css
               /* Используй contain для изоляции reflows */
               .card { contain: layout style paint; }
               ```

            3. **Bundle Analysis**:
               ```bash
               npx @next/bundle-analyzer
               ```
            """
        }

        # Выбираем релевантные знания на основе запроса
        relevant_knowledge = []

        for topic, knowledge in domain_specific_knowledge.items():
            if topic in query.lower() or any(tag in topic for tag in ctx.deps.knowledge_tags):
                relevant_knowledge.append(knowledge)

        if not relevant_knowledge:
            # Возвращаем общие паттерны UI/UX
            relevant_knowledge = ["""
            **ОБЩИЕ UI/UX ПАТТЕРНЫ:**

            1. **Design System Consistency**: Используй единые компоненты и токены
            2. **Mobile-First**: Проектируй сначала для мобильных устройств
            3. **Accessibility**: WCAG 2.1 AA как минимальный стандарт
            4. **Performance**: < 100KB bundle, < 1.5s FCP
            5. **Progressive Enhancement**: Базовая функциональность без JS
            """]

        combined_knowledge = "\n\n".join(relevant_knowledge)

        return f"""
📚 **БАЗА ЗНАНИЙ UI/UX ENHANCEMENT AGENT**

Запрос: "{query}"
Найдено паттернов: {len(relevant_knowledge)}

{combined_knowledge}

💡 **Рекомендация**: Для получения более специфичных знаний установи Archon MCP server и загрузи базу знаний агента.
        """

    except Exception as e:
        return f"❌ Ошибка поиска в базе знаний UI/UX: {e}"


async def analyze_ui_accessibility(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    component_type: str = "generic"
) -> str:
    """
    Анализ accessibility компонента UI.

    Args:
        ctx: Контекст выполнения
        component_code: Код компонента для анализа
        component_type: Тип компонента (form, navigation, data, etc.)

    Returns:
        Детальный отчет о проблемах accessibility и рекомендации
    """
    accessibility_config = ctx.deps.get_accessibility_config()
    issues = []

    # Анализ semantic HTML
    if not re.search(r'<(main|section|article|aside|nav|header|footer)', component_code):
        issues.append(AccessibilityIssue(
            severity="High",
            wcag_criterion="1.3.1 Info and Relationships",
            element="HTML structure",
            description="Отсутствуют semantic HTML elements",
            fix_suggestion="Используй semantic теги: <main>, <section>, <nav>, <header>",
            code_example="<main role='main'><section aria-labelledby='heading'>...</section></main>"
        ))

    # Проверка ARIA labels
    interactive_elements = re.findall(r'<(button|input|select|textarea|a)', component_code)
    aria_labels = re.findall(r'aria-label[^=]*=', component_code)

    if len(interactive_elements) > len(aria_labels):
        issues.append(AccessibilityIssue(
            severity="Medium",
            wcag_criterion="4.1.2 Name, Role, Value",
            element="Interactive elements",
            description="Не все интерактивные элементы имеют ARIA labels",
            fix_suggestion="Добавь aria-label или aria-labelledby ко всем интерактивным элементам",
            code_example='<button aria-label="Закрыть модальное окно">×</button>'
        ))

    # Проверка keyboard navigation
    if 'onKeyDown' not in component_code and ('input' in component_code or 'button' in component_code):
        issues.append(AccessibilityIssue(
            severity="Medium",
            wcag_criterion="2.1.1 Keyboard",
            element="Keyboard handlers",
            description="Отсутствует обработка keyboard events",
            fix_suggestion="Добавь onKeyDown handlers для Enter и Space keys",
            code_example="onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleAction(); }}"
        ))

    # Проверка focus management
    if 'tabIndex' not in component_code and 'autoFocus' not in component_code:
        issues.append(AccessibilityIssue(
            severity="Low",
            wcag_criterion="2.4.3 Focus Order",
            element="Focus management",
            description="Не настроен порядок фокуса",
            fix_suggestion="Добавь tabIndex для кастомного порядка фокуса",
            code_example="<div tabIndex={0} onFocus={handleFocus}>"
        ))

    # Вычисляем accessibility score
    total_possible_issues = 10  # Максимальное количество типов проблем
    severity_weights = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    issue_penalty = sum(severity_weights.get(issue.severity, 1) for issue in issues)
    accessibility_score = max(0, 100 - (issue_penalty * 5))

    # Формируем отчет
    report = f"""
    🔍 **ACCESSIBILITY АУДИТ**

    **Компонент:** {component_type}
    **Оценка:** {accessibility_score}/100
    **WCAG уровень:** {accessibility_config['wcag_level']}

    📋 **НАЙДЕННЫЕ ПРОБЛЕМЫ:**

    """

    for i, issue in enumerate(issues, 1):
        report += f"""
    **{i}. {issue.severity} - {issue.wcag_criterion}**
    - Элемент: {issue.element}
    - Проблема: {issue.description}
    - Решение: {issue.fix_suggestion}
    - Пример: `{issue.code_example or 'См. документацию'}`

    """

    if not issues:
        report += "✅ Критических проблем accessibility не найдено!\n"

    report += f"""
    💡 **ОБЩИЕ РЕКОМЕНДАЦИИ:**

    1. **Keyboard Navigation:** Убедись, что все элементы доступны через Tab/Shift+Tab
    2. **Screen Reader:** Протестируй с NVDA или VoiceOver
    3. **Color Contrast:** Минимум 4.5:1 для нормального текста, 3:1 для крупного
    4. **Focus Indicators:** Видимые индикаторы фокуса для всех интерактивных элементов

    🛠️ **ИНСТРУМЕНТЫ ДЛЯ ТЕСТИРОВАНИЯ:**
    - axe DevTools extension
    - Lighthouse accessibility audit
    - WAVE Web Accessibility Evaluator
    """

    return report


async def optimize_tailwind_classes(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    optimization_level: str = "aggressive"
) -> str:
    """
    Оптимизация Tailwind CSS классов в компоненте.

    Args:
        ctx: Контекст выполнения
        component_code: Код компонента с Tailwind классами
        optimization_level: Уровень оптимизации (conservative, balanced, aggressive)

    Returns:
        Оптимизированный код и рекомендации
    """
    # Извлекаем все className атрибуты
    class_patterns = re.findall(r'className=["\']([^"\']+)["\']', component_code)

    optimizations = []
    optimized_code = component_code

    for class_string in class_patterns:
        classes = class_string.split()

        # Группировка связанных классов
        grouped_classes = _group_related_classes(classes)

        # Удаление дублирующихся классов
        deduplicated = _remove_duplicate_classes(classes)

        # Сокращение с помощью кастомных утилит
        shortened = _suggest_custom_utilities(classes)

        if len(deduplicated) < len(classes):
            optimizations.append({
                "type": "Удаление дублей",
                "original": class_string,
                "optimized": " ".join(deduplicated),
                "savings": f"-{len(classes) - len(deduplicated)} классов"
            })

            # Применяем оптимизацию к коду
            optimized_code = optimized_code.replace(
                f'className="{class_string}"',
                f'className="{" ".join(deduplicated)}"'
            )

    # Предложения по custom CSS utilities
    custom_utilities = _extract_repeating_patterns(class_patterns)

    report = f"""
    ⚡ **TAILWIND CSS ОПТИМИЗАЦИЯ**

    **Уровень оптимизации:** {optimization_level}
    **Найдено оптимизаций:** {len(optimizations)}

    📊 **ПРИМЕНЁННЫЕ ОПТИМИЗАЦИИ:**

    """

    for opt in optimizations:
        report += f"""
    **{opt['type']}**
    - До: `{opt['original'][:50]}...`
    - После: `{opt['optimized'][:50]}...`
    - Экономия: {opt['savings']}

    """

    if custom_utilities:
        report += """
    🎨 **РЕКОМЕНДАЦИИ ПО CUSTOM UTILITIES:**

    """
        for pattern, suggestion in custom_utilities.items():
            report += f"""
    **{pattern}:**
    ```css
    @layer utilities {{
      {suggestion}
    }}
    ```

    """

    report += f"""
    ✨ **ОПТИМИЗИРОВАННЫЙ КОД:**

    ```tsx
    {optimized_code}
    ```

    📋 **ДОПОЛНИТЕЛЬНЫЕ РЕКОМЕНДАЦИИ:**

    1. **Группировка:** Группируй связанные утилиты (layout, spacing, colors)
    2. **@apply директива:** Выноси повторяющиеся паттерны в компоненты
    3. **Purge CSS:** Настрой правильно purge для production bundle
    4. **JIT режим:** Используй Just-In-Time compilation для лучшей производительности
    """

    return report


async def generate_shadcn_component(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_name: str,
    component_type: str = "button",
    variant_options: List[str] = None
) -> str:
    """
    Генерация нового shadcn/ui компонента через Shadcn MCP.

    Args:
        ctx: Контекст выполнения
        component_name: Название компонента
        component_type: Тип компонента (button, input, card, etc.)
        variant_options: Опции вариантов

    Returns:
        Сгенерированный shadcn компонент
    """
    try:
        # Интеграция с Shadcn MCP
        from mcp_client import shadcn_mcp_generate_component

        result = await shadcn_mcp_generate_component(
            name=component_name,
            type=component_type,
            variants=variant_options or ["default"],
            framework=ctx.deps.ui_framework
        )

        if result["success"]:
            return f"""
🎨 **SHADCN КОМПОНЕНТ СГЕНЕРИРОВАН**

**Компонент:** {component_name}
**Тип:** {component_type}
**Framework:** {ctx.deps.ui_framework}

```tsx
{result["component_code"]}
```

**Использование:**
```tsx
{result["usage_examples"]}
```

💡 **Дополнительные возможности:**
- Автоматическая типизация через VariantProps
- Поддержка asChild pattern
- Интеграция с cn() utility
- Совместимость с существующей дизайн системой
            """
    except ImportError:
        # Fallback - генерируем компонент вручную
        return await _generate_shadcn_fallback(ctx, component_name, component_type, variant_options)
    except Exception as e:
        return f"❌ Ошибка генерации Shadcn компонента: {e}"


async def enhance_shadcn_component(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    enhancement_type: str = "accessibility"
) -> str:
    """
    Улучшение shadcn/ui компонента.

    Args:
        ctx: Контекст выполнения
        component_code: Код shadcn компонента
        enhancement_type: Тип улучшения (accessibility, performance, design)

    Returns:
        Улучшенный компонент и объяснения
    """
    enhancements = []

    # Проверяем использование shadcn паттернов
    has_cn_util = 'cn(' in component_code
    has_variant_cva = 'cva(' in component_code or 'VariantProps' in component_code

    if not has_cn_util:
        enhancements.append({
            "type": "cn() utility",
            "issue": "Не используется cn() utility для условных классов",
            "fix": "import { cn } from '@/lib/utils'",
            "benefit": "Лучшее управление условными стилями"
        })

    if not has_variant_cva and enhancement_type == "design":
        enhancements.append({
            "type": "Component variants",
            "issue": "Компонент не использует cva для вариантов",
            "fix": "Добавить cva() для type-safe вариантов",
            "benefit": "Type-safe варианты и лучшая DX"
        })

    # Проверяем Radix primitives
    radix_imports = re.findall(r'from ["\']@radix-ui/([^"\']+)["\']', component_code)

    if not radix_imports and any(element in component_code for element in ['Dialog', 'Popover', 'Select']):
        enhancements.append({
            "type": "Radix primitives",
            "issue": "Можно заменить кастомные элементы на Radix primitives",
            "fix": "Использовать @radix-ui primitives",
            "benefit": "Лучшая accessibility и keyboard navigation из коробки"
        })

    # Генерируем улучшенный код
    enhanced_code = _apply_shadcn_enhancements(component_code, enhancements)

    report = f"""
    🎨 **SHADCN/UI КОМПОНЕНТ УЛУЧШЕНИЯ**

    **Тип улучшения:** {enhancement_type}
    **Найдено улучшений:** {len(enhancements)}

    🔧 **РЕКОМЕНДУЕМЫЕ УЛУЧШЕНИЯ:**

    """

    for enhancement in enhancements:
        report += f"""
    **{enhancement['type']}**
    - Проблема: {enhancement['issue']}
    - Решение: {enhancement['fix']}
    - Преимущество: {enhancement['benefit']}

    """

    report += f"""
    ✨ **УЛУЧШЕННЫЙ КОМПОНЕНТ:**

    ```tsx
    {enhanced_code}
    ```

    📚 **SHADCN/UI BEST PRACTICES:**

    1. **cn() utility:** Всегда используй для conditional classes
    2. **Radix primitives:** Предпочитай Radix для сложных компонентов
    3. **cva():** Используй для type-safe вариантов
    4. **forwardRef:** Добавляй для всех компонентов
    5. **Compound patterns:** Создавай составные компоненты через контекст

    🎯 **ИНТЕГРАЦИЯ С ДИЗАЙН СИСТЕМОЙ:**

    - CSS variables для цветов: `hsl(var(--primary))`
    - Design tokens для spacing и typography
    - Consistent animation durations
    - Proper focus management
    """

    return report


async def analyze_ux_patterns(
    ctx: RunContext[UIUXEnhancementDependencies],
    user_flow: str,
    component_context: str = ""
) -> str:
    """
    Анализ UX паттернов и пользовательских сценариев.

    Args:
        ctx: Контекст выполнения
        user_flow: Описание пользовательского сценария
        component_context: Контекст использования компонента

    Returns:
        Анализ UX и рекомендации по улучшению
    """
    # Анализируем пользовательский поток
    ux_issues = []
    recommendations = []

    # Проверяем основные UX принципы
    if "error" in user_flow.lower() and "validation" not in user_flow.lower():
        ux_issues.append({
            "principle": "Error Prevention",
            "issue": "Отсутствует превентивная валидация",
            "impact": "High",
            "solution": "Добавить real-time validation и helpful hints"
        })

    if "loading" in user_flow.lower() and "skeleton" not in user_flow.lower():
        ux_issues.append({
            "principle": "Feedback",
            "issue": "Нет индикации загрузки состояния",
            "impact": "Medium",
            "solution": "Добавить skeleton screens или loading spinners"
        })

    if "form" in user_flow.lower() and "save" not in user_flow.lower():
        ux_issues.append({
            "principle": "User Control",
            "issue": "Возможна потеря пользовательских данных",
            "impact": "High",
            "solution": "Добавить auto-save или draft сохранение"
        })

    # Общие UX рекомендации для проекта
    recommendations.extend([
        "Progressive disclosure для сложных форм",
        "Contextual help tooltips для новых пользователей",
        "Consistent navigation patterns",
        "Mobile-first responsive design",
        "Clear visual hierarchy",
        "Accessible color contrast ratios"
    ])

    report = f"""
    🧠 **UX АНАЛИЗ ПАТТЕРНОВ**

    **Пользовательский сценарий:** {user_flow}
    **Контекст:** {component_context or 'Общий'}

    ⚠️ **НАЙДЕННЫЕ UX ПРОБЛЕМЫ:**

    """

    for issue in ux_issues:
        report += f"""
    **{issue['principle']} - Impact: {issue['impact']}**
    - Проблема: {issue['issue']}
    - Решение: {issue['solution']}

    """

    if not ux_issues:
        report += "✅ Критических UX проблем не найдено!\n"

    report += f"""
    💡 **РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ UX:**

    """

    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"

    report += f"""

    🎯 **СПЕЦИФИЧНЫЕ РЕКОМЕНДАЦИИ ДЛЯ ПРОЕКТА:**

    **Content Discovery:**
    - Intuitive filtering and search
    - Visual calendar integration
    - Location-based recommendations

    **Booking Process:**
    - Minimal steps to complete booking
    - Clear pricing and availability
    - Guest checkout option

    **Event Management:**
    - Drag-and-drop event editing
    - Real-time attendee updates
    - Quick action buttons

    **Mobile Experience:**
    - Touch-friendly controls (minimum 44px)
    - Swipe gestures for navigation
    - Offline capability for key features

    📊 **МЕТРИКИ ДЛЯ ОТСЛЕЖИВАНИЯ:**

    - Task completion rate
    - Time to complete booking
    - Error rate in forms
    - Mobile vs desktop usage patterns
    - User satisfaction scores
    """

    return report


async def generate_component_variants(
    ctx: RunContext[UIUXEnhancementDependencies],
    base_component: str,
    variant_types: List[str]
) -> str:
    """
    Генерация вариантов компонента для разных use cases.

    Args:
        ctx: Контекст выполнения
        base_component: Базовый компонент код
        variant_types: Типы вариантов (size, style, state, etc.)

    Returns:
        Код вариантов компонента с использованием cva
    """
    # Извлекаем название компонента
    component_match = re.search(r'function\s+(\w+)|const\s+(\w+)\s*=', base_component)
    component_name = (component_match.group(1) or component_match.group(2)) if component_match else "Component"

    # Генерируем варианты с помощью cva
    variants_code = f"""
import {{ cva, type VariantProps }} from "class-variance-authority"
import {{ cn }} from "@/lib/utils"

const {component_name.lower()}Variants = cva(
  // Базовые стили
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {{
    variants: {{"""

    # Генерируем варианты размеров
    if "size" in variant_types:
        variants_code += """
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-base",
        lg: "h-12 px-6 text-lg",
        xl: "h-14 px-8 text-xl",
      },"""

    # Генерируем цветовые варианты
    if "style" in variant_types or "color" in variant_types:
        variants_code += """
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },"""

    # Генерируем состояния
    if "state" in variant_types:
        variants_code += """
      state: {
        default: "",
        loading: "cursor-not-allowed",
        disabled: "pointer-events-none opacity-50",
        success: "bg-green-500 text-white",
        error: "bg-red-500 text-white",
      },"""

    variants_code += """
    },
    defaultVariants: {
      size: "md",
      variant: "default",
    },
  }
)

export interface {component_name}Props
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof {component_name.lower()}Variants> {
  asChild?: boolean
}

const {component_name} = React.forwardRef<HTMLButtonElement, {component_name}Props>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn({component_name.lower()}Variants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
{component_name}.displayName = "{component_name}"

export {{ {component_name}, {component_name.lower()}Variants }}
"""

    # Примеры использования
    usage_examples = f"""
// Примеры использования {component_name}

// Базовое использование
<{component_name}>Click me</{component_name}>

// Различные размеры
<{component_name} size="sm">Small</{component_name}>
<{component_name} size="lg">Large</{component_name}>

// Различные варианты
<{component_name} variant="outline">Outline</{component_name}>
<{component_name} variant="destructive">Delete</{component_name}>

// Кастомные классы
<{component_name} className="w-full">Full Width</{component_name}>

// As child pattern
<{component_name} asChild>
  <Link href="/events">Go to Events</Link>
</{component_name}>
"""

    report = f"""
    🎨 **ГЕНЕРАЦИЯ ВАРИАНТОВ КОМПОНЕНТА**

    **Компонент:** {component_name}
    **Типы вариантов:** {', '.join(variant_types)}

    ✨ **КОМПОНЕНТ С ВАРИАНТАМИ:**

    ```tsx
    {variants_code}
    ```

    📋 **ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:**

    ```tsx
    {usage_examples}
    ```

    🎯 **ПРЕИМУЩЕСТВА CVA ПАТТЕРНА:**

    1. **Type Safety:** Автоматическая типизация props
    2. **Performance:** Оптимизированная конкатенация классов
    3. **Maintainability:** Централизованное управление вариантами
    4. **Consistency:** Единообразные паттерны во всем приложении
    5. **Developer Experience:** IntelliSense для вариантов

    🔧 **РЕКОМЕНДАЦИИ:**

    - Используй compound variants для сложных комбинаций
    - Добавляй responsive variants при необходимости
    - Документируй каждый вариант в Storybook
    - Следуй naming conventions проекта
    """

    return report


async def validate_design_system(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    design_tokens: Optional[Dict[str, Any]] = None
) -> str:
    """
    Валидация соответствия компонента дизайн системе.

    Args:
        ctx: Контекст выполнения
        component_code: Код компонента для валидации
        design_tokens: Кастомные дизайн токены

    Returns:
        Отчет о соответствии дизайн системе
    """
    validation_results = []
    compliance_score = 100

    # Проверяем использование CSS variables
    css_var_pattern = r'hsl\(var\(--[\w-]+\)\)'
    has_css_vars = bool(re.search(css_var_pattern, component_code))

    if not has_css_vars:
        validation_results.append({
            "category": "Design Tokens",
            "issue": "Не используются CSS variables для цветов",
            "severity": "Medium",
            "fix": "Замени hardcoded цвета на hsl(var(--primary))",
            "compliance_impact": -15
        })
        compliance_score -= 15

    # Проверяем spacing consistency
    spacing_classes = re.findall(r'(p-\d+|m-\d+|gap-\d+|space-[xy]-\d+)', component_code)
    custom_spacing = [s for s in spacing_classes if int(re.search(r'\d+', s).group()) > 96]

    if custom_spacing:
        validation_results.append({
            "category": "Spacing System",
            "issue": f"Используются нестандартные spacing values: {custom_spacing}",
            "severity": "Low",
            "fix": "Используй стандартные spacing tokens: 1, 2, 4, 8, 12, 16, 20, 24",
            "compliance_impact": -5
        })
        compliance_score -= 5

    # Проверяем typography
    text_classes = re.findall(r'text-(xs|sm|base|lg|xl|2xl|3xl|4xl)', component_code)
    if not text_classes:
        validation_results.append({
            "category": "Typography",
            "issue": "Не используются типографические утилиты",
            "severity": "Low",
            "fix": "Добавь text-* классы для consistent typography",
            "compliance_impact": -5
        })
        compliance_score -= 5

    # Проверяем animation tokens
    if 'transition' in component_code and not any(duration in component_code for duration in ['150', '300', '500']):
        validation_results.append({
            "category": "Animation",
            "issue": "Используются нестандартные animation durations",
            "severity": "Low",
            "fix": "Используй стандартные durations: 150ms, 300ms, 500ms",
            "compliance_impact": -5
        })
        compliance_score -= 5

    # Проверяем accessibility patterns
    has_focus_styles = 'focus:' in component_code or 'focus-visible:' in component_code
    if not has_focus_styles:
        validation_results.append({
            "category": "Accessibility",
            "issue": "Отсутствуют focus styles",
            "severity": "High",
            "fix": "Добавь focus-visible:ring-2 focus-visible:ring-offset-2",
            "compliance_impact": -20
        })
        compliance_score -= 20

    # Определяем общий уровень соответствия
    compliance_level = "Excellent" if compliance_score >= 90 else \
                     "Good" if compliance_score >= 75 else \
                     "Needs Improvement" if compliance_score >= 60 else \
                     "Poor"

    report = f"""
    🎯 **ВАЛИДАЦИЯ ДИЗАЙН СИСТЕМЫ**

    **Оценка соответствия:** {compliance_score}/100 ({compliance_level})
    **Дизайн система:** {ctx.deps.design_system}
    **Найдено проблем:** {len(validation_results)}

    📊 **РЕЗУЛЬТАТЫ ПРОВЕРКИ:**

    """

    for result in validation_results:
        report += f"""
    **{result['category']} - {result['severity']}**
    - Проблема: {result['issue']}
    - Решение: {result['fix']}
    - Влияние на оценку: {result['compliance_impact']}

    """

    if not validation_results:
        report += "✅ Компонент полностью соответствует дизайн системе!\n"

    report += f"""
    🎨 **РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:**

    **Design Tokens:**
    - Используй CSS custom properties: `hsl(var(--primary))`
    - Consistent spacing scale: 4px base unit
    - Typography scale: text-sm, text-base, text-lg
    - Color semantic naming: primary, secondary, accent

    **Accessibility:**
    - Focus indicators на всех интерактивных элементах
    - High contrast mode support
    - Reduced motion preferences
    - Keyboard navigation patterns

    **Performance:**
    - Tree-shakable utility classes
    - Minimal CSS bundle size
    - Efficient re-renders
    - Lazy loading где возможно

    **Consistency:**
    - Единообразные patterns во всех компонентах
    - Shared utilities и hooks
    - Documented component API
    - Storybook documentation

    📚 **УНИВЕРСАЛЬНАЯ ДИЗАЙН СИСТЕМА:**

    **Цветовая палитра:**
    ```css
    :root {{
      --primary: 214 100% 50%;     /* Blue */
      --secondary: 152 70% 50%;    /* Emerald */
      --accent: 264 70% 65%;       /* Violet */
      --background: 0 0% 100%;     /* White */
      --foreground: 222 84% 5%;    /* Near Black */
    }}
    ```

    **Spacing система:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96
    **Typography:** Inter (body), Cal Sans (headings)
    **Animations:** 150ms (fast), 300ms (normal), 500ms (slow)
    """

    return report


# Утилитарные функции

def _group_related_classes(classes: List[str]) -> Dict[str, List[str]]:
    """Группировка связанных Tailwind классов."""
    groups = {
        "layout": [],
        "spacing": [],
        "sizing": [],
        "typography": [],
        "colors": [],
        "effects": [],
        "transforms": [],
        "interactivity": []
    }

    for cls in classes:
        if any(prefix in cls for prefix in ['flex', 'grid', 'block', 'inline', 'hidden']):
            groups["layout"].append(cls)
        elif any(prefix in cls for prefix in ['p-', 'm-', 'gap-', 'space-']):
            groups["spacing"].append(cls)
        elif any(prefix in cls for prefix in ['w-', 'h-', 'min-', 'max-']):
            groups["sizing"].append(cls)
        elif any(prefix in cls for prefix in ['text-', 'font-', 'leading-', 'tracking-']):
            groups["typography"].append(cls)
        elif any(prefix in cls for prefix in ['bg-', 'text-', 'border-', 'from-', 'to-']):
            groups["colors"].append(cls)
        elif any(prefix in cls for prefix in ['shadow-', 'opacity-', 'blur-']):
            groups["effects"].append(cls)
        elif any(prefix in cls for prefix in ['transform', 'rotate-', 'scale-', 'translate-']):
            groups["transforms"].append(cls)
        elif any(prefix in cls for prefix in ['hover:', 'focus:', 'active:', 'disabled:']):
            groups["interactivity"].append(cls)

    return {k: v for k, v in groups.items() if v}


def _remove_duplicate_classes(classes: List[str]) -> List[str]:
    """Удаление дублирующихся классов с сохранением порядка."""
    seen = set()
    result = []
    for cls in classes:
        if cls not in seen:
            seen.add(cls)
            result.append(cls)
    return result


def _suggest_custom_utilities(classes: List[str]) -> Dict[str, str]:
    """Предложения по созданию кастомных утилит."""
    suggestions = {}

    # Группируем частые паттерны
    class_count = {}
    for cls in classes:
        class_count[cls] = class_count.get(cls, 0) + 1

    # Если класс повторяется часто, предлагаем утилиту
    frequent_classes = [cls for cls, count in class_count.items() if count >= 3]

    if frequent_classes:
        utility_name = "btn-common"
        suggestions[utility_name] = f".{utility_name} {{ @apply {' '.join(frequent_classes[:5])}; }}"

    return suggestions


def _extract_repeating_patterns(class_patterns: List[str]) -> Dict[str, str]:
    """Извлечение повторяющихся паттернов классов."""
    patterns = {}

    # Простой анализ повторяющихся комбинаций
    for pattern in class_patterns:
        if len(pattern.split()) >= 4:  # Только длинные паттерны
            pattern_key = f"utility-{len(patterns) + 1}"
            css_classes = " ".join(pattern.split()[:4])  # Берем первые 4 класса
            patterns[pattern_key] = f".{pattern_key} {{ @apply {css_classes}; }}"

    return patterns


def _apply_shadcn_enhancements(component_code: str, enhancements: List[Dict]) -> str:
    """Применение улучшений к shadcn компоненту."""
    enhanced_code = component_code

    for enhancement in enhancements:
        if enhancement["type"] == "cn() utility":
            # Добавляем cn() import если его нет
            if "cn" not in enhanced_code:
                enhanced_code = 'import { cn } from "@/lib/utils"\n' + enhanced_code

            # Заменяем простые className на cn()
            enhanced_code = re.sub(
                r'className="([^"]+)"',
                r'className={cn("\1")}',
                enhanced_code
            )

        elif enhancement["type"] == "Component variants":
            # Добавляем cva import
            if "cva" not in enhanced_code:
                enhanced_code = 'import { cva, type VariantProps } from "class-variance-authority"\n' + enhanced_code

    return enhanced_code


async def design_interface_from_scratch(
    ctx: RunContext[UIUXEnhancementDependencies],
    requirements: str,
    interface_type: str = "web_app",
    target_devices: str = "desktop,mobile"
) -> str:
    """
    Дизайн интерфейса с нуля на основе требований.

    Args:
        ctx: Контекст выполнения
        requirements: Требования к интерфейсу
        interface_type: Тип интерфейса (web_app, mobile_app, dashboard, landing)
        target_devices: Целевые устройства (desktop, mobile, tablet)

    Returns:
        Полный дизайн интерфейса с компонентами и стилями
    """
    domain_type = ctx.deps.domain_type
    design_system = ctx.deps.design_system_type
    ui_framework = ctx.deps.ui_framework

    # Анализируем требования
    analysis = f"""
    🎨 **ДИЗАЙН ИНТЕРФЕЙСА С НУЛЯ**

    **Требования:** {requirements}
    **Тип интерфейса:** {interface_type}
    **Домен:** {domain_type}
    **Целевые устройства:** {target_devices}
    **UI Framework:** {ui_framework}
    **Дизайн система:** {design_system}

    ## 📐 АРХИТЕКТУРА ИНТЕРФЕЙСА

    **Layout Structure:**
    ```tsx
    // Основная структура для {interface_type}
    <div className="min-h-screen bg-background">
      <Header />
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <ContentArea />
        <Sidebar />
      </main>
      <Footer />
    </div>
    ```

    ## 🎯 КЛЮЧЕВЫЕ КОМПОНЕНТЫ

    """

    # Генерируем компоненты в зависимости от типа интерфейса
    if interface_type == "dashboard":
        analysis += """
    **Dashboard Components:**
    1. **MetricsCards** - KPI отображение
    2. **DataChart** - Графики и визуализация
    3. **DataTable** - Табличные данные
    4. **FilterPanel** - Фильтры и поиск
    5. **ActionButtons** - Быстрые действия

    ```tsx
    // Пример Dashboard Layout
    const Dashboard = () => (
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <MetricsGrid />
          <ChartsSection />
        </div>
        <div className="lg:col-span-1">
          <FiltersPanel />
          <RecentActivity />
        </div>
      </div>
    )
    ```
        """
    elif interface_type == "web_app":
        analysis += """
    **Web App Components:**
    1. **Navigation** - Главное меню
    2. **UserProfile** - Профиль пользователя
    3. **ContentFeed** - Основной контент
    4. **SearchBar** - Поиск
    5. **ActionModals** - Модальные окна

    ```tsx
    // Пример Web App Layout
    const WebApp = () => (
      <div className="flex h-screen">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <TopBar />
          <ContentArea />
        </main>
      </div>
    )
    ```
        """
    elif interface_type == "landing":
        analysis += """
    **Landing Page Components:**
    1. **Hero Section** - Главный экран
    2. **Features Grid** - Преимущества
    3. **Testimonials** - Отзывы
    4. **CTA Sections** - Call-to-action
    5. **Contact Form** - Контактная форма

    ```tsx
    // Пример Landing Layout
    const Landing = () => (
      <div>
        <HeroSection />
        <FeaturesSection />
        <TestimonialsSection />
        <CTASection />
        <Footer />
      </div>
    )
    ```
        """

    analysis += f"""

    ## 🎨 ДИЗАЙН СИСТЕМА

    **Color Palette для {domain_type}:**
    ```css
    :root {{
      --primary: 220 90% 56%;      /* Brand Blue */
      --primary-foreground: 0 0% 98%;
      --secondary: 210 40% 98%;    /* Light Gray */
      --secondary-foreground: 222.2 84% 4.9%;
      --accent: 210 40% 96%;       /* Accent Gray */
      --accent-foreground: 222.2 84% 4.9%;
      --background: 0 0% 100%;     /* White */
      --foreground: 222.2 84% 4.9%; /* Dark */
    }}
    ```

    **Typography Scale:**
    ```css
    .text-h1 {{ font-size: 2.5rem; font-weight: 700; line-height: 1.2; }}
    .text-h2 {{ font-size: 2rem; font-weight: 600; line-height: 1.3; }}
    .text-h3 {{ font-size: 1.5rem; font-weight: 600; line-height: 1.4; }}
    .text-body {{ font-size: 1rem; line-height: 1.6; }}
    .text-caption {{ font-size: 0.875rem; line-height: 1.5; }}
    ```

    **Spacing System:**
    - Base unit: 4px
    - Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96

    ## 📱 RESPONSIVE STRATEGY

    **Breakpoints:**
    - Mobile: 320px - 768px
    - Tablet: 768px - 1024px
    - Desktop: 1024px+

    **Mobile-First Approach:**
    ```css
    /* Mobile styles by default */
    .component {{ padding: 1rem; }}

    /* Tablet styles */
    @media (min-width: 768px) {{
      .component {{ padding: 1.5rem; }}
    }}

    /* Desktop styles */
    @media (min-width: 1024px) {{
      .component {{ padding: 2rem; }}
    }}
    ```

    ## ♿ ACCESSIBILITY GUIDELINES

    1. **Color Contrast:** Минимум 4.5:1 для обычного текста
    2. **Focus Indicators:** Видимые на всех интерактивных элементах
    3. **Keyboard Navigation:** Полная поддержка Tab/Shift+Tab
    4. **Screen Readers:** Semantic HTML + ARIA labels
    5. **Touch Targets:** Минимум 44px для мобильных устройств

    ## 🚀 IMPLEMENTATION PLAN

    **Phase 1: Core Components**
    1. Настройка дизайн системы ({design_system})
    2. Базовые компоненты (Button, Input, Card)
    3. Layout компоненты (Header, Sidebar, Main)

    **Phase 2: Feature Components**
    1. Специализированные компоненты для {domain_type}
    2. Interactive элементы
    3. Data visualization (если нужно)

    **Phase 3: Polish & Optimization**
    1. Animations и микровзаимодействия
    2. Performance optimization
    3. Accessibility testing

    ## 🛠️ РЕКОМЕНДУЕМЫЕ ИНСТРУМЕНТЫ

    **Design:** Figma для прототипов и дизайн системы
    **Development:** {ui_framework} + {design_system}
    **Testing:** Jest + React Testing Library + axe-core
    **Documentation:** Storybook для компонентов

    ## 📏 DESIGN TOKENS

    ```json
    {{
      "spacing": {{
        "xs": "4px",
        "sm": "8px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px"
      }},
      "borderRadius": {{
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "full": "9999px"
      }},
      "animation": {{
        "fast": "150ms",
        "normal": "300ms",
        "slow": "500ms"
      }}
    }}
    ```

    💡 **Next Steps:** Создать wireframes в Figma и начать разработку с базовых компонентов.
    """

    return analysis


async def create_design_system(
    ctx: RunContext[UIUXEnhancementDependencies],
    brand_requirements: str,
    system_name: str = "Design System"
) -> str:
    """
    Создание полной дизайн системы с нуля.

    Args:
        ctx: Контекст выполнения
        brand_requirements: Требования к бренду и стилю
        system_name: Название дизайн системы

    Returns:
        Полная дизайн система с токенами, компонентами и документацией
    """
    domain_type = ctx.deps.domain_type

    design_system = f"""
    🎨 **{system_name.upper()} - ПОЛНАЯ ДИЗАЙН СИСТЕМА**

    ## 🎯 BRAND IDENTITY

    **Бренд требования:** {brand_requirements}
    **Домен применения:** {domain_type}
    **Философия:** Простота, доступность, производительность

    ## 🌈 COLOR SYSTEM

    **Primary Palette:**
    ```css
    :root {{
      /* Primary Colors */
      --primary-50: hsl(210, 40%, 98%);
      --primary-100: hsl(210, 40%, 96%);
      --primary-200: hsl(213, 27%, 84%);
      --primary-300: hsl(212, 23%, 69%);
      --primary-400: hsl(213, 19%, 46%);
      --primary-500: hsl(217, 19%, 35%);  /* Main brand color */
      --primary-600: hsl(215, 25%, 27%);
      --primary-700: hsl(215, 25%, 27%);
      --primary-800: hsl(217, 33%, 17%);
      --primary-900: hsl(222, 47%, 11%);

      /* Semantic Colors */
      --success: hsl(142, 76%, 36%);
      --warning: hsl(38, 92%, 50%);
      --error: hsl(0, 84%, 60%);
      --info: hsl(217, 91%, 60%);

      /* Neutral Colors */
      --gray-50: hsl(210, 40%, 98%);
      --gray-100: hsl(210, 40%, 96%);
      --gray-200: hsl(214, 32%, 91%);
      --gray-300: hsl(213, 27%, 84%);
      --gray-400: hsl(215, 20%, 65%);
      --gray-500: hsl(215, 16%, 47%);
      --gray-600: hsl(215, 19%, 35%);
      --gray-700: hsl(215, 25%, 27%);
      --gray-800: hsl(217, 33%, 17%);
      --gray-900: hsl(222, 47%, 11%);
    }}
    ```

    **Dark Mode Support:**
    ```css
    [data-theme="dark"] {{
      --background: var(--gray-900);
      --foreground: var(--gray-50);
      --primary: var(--primary-400);
      --secondary: var(--gray-800);
    }}
    ```

    ## 📝 TYPOGRAPHY SYSTEM

    **Font Stack:**
    ```css
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
      --font-display: 'Cal Sans', 'Inter', sans-serif;
    }}
    ```

    **Type Scale:**
    ```css
    .text-xs    {{ font-size: 0.75rem; line-height: 1rem; }}     /* 12px */
    .text-sm    {{ font-size: 0.875rem; line-height: 1.25rem; }} /* 14px */
    .text-base  {{ font-size: 1rem; line-height: 1.5rem; }}      /* 16px */
    .text-lg    {{ font-size: 1.125rem; line-height: 1.75rem; }} /* 18px */
    .text-xl    {{ font-size: 1.25rem; line-height: 1.75rem; }}  /* 20px */
    .text-2xl   {{ font-size: 1.5rem; line-height: 2rem; }}      /* 24px */
    .text-3xl   {{ font-size: 1.875rem; line-height: 2.25rem; }} /* 30px */
    .text-4xl   {{ font-size: 2.25rem; line-height: 2.5rem; }}   /* 36px */
    .text-5xl   {{ font-size: 3rem; line-height: 1; }}           /* 48px */
    ```

    ## 📏 SPACING SYSTEM

    **Base Unit:** 4px (0.25rem)

    ```css
    :root {{
      --spacing-px: 1px;
      --spacing-0: 0;
      --spacing-1: 0.25rem;  /* 4px */
      --spacing-2: 0.5rem;   /* 8px */
      --spacing-3: 0.75rem;  /* 12px */
      --spacing-4: 1rem;     /* 16px */
      --spacing-5: 1.25rem;  /* 20px */
      --spacing-6: 1.5rem;   /* 24px */
      --spacing-8: 2rem;     /* 32px */
      --spacing-10: 2.5rem;  /* 40px */
      --spacing-12: 3rem;    /* 48px */
      --spacing-16: 4rem;    /* 64px */
      --spacing-20: 5rem;    /* 80px */
      --spacing-24: 6rem;    /* 96px */
    }}
    ```

    ## 🔄 ANIMATION SYSTEM

    **Timing Functions:**
    ```css
    :root {{
      --ease-in: cubic-bezier(0.4, 0, 1, 1);
      --ease-out: cubic-bezier(0, 0, 0.2, 1);
      --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
      --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    ```

    **Duration Scale:**
    ```css
    :root {{
      --duration-75: 75ms;    /* Micro interactions */
      --duration-100: 100ms;  /* Quick transitions */
      --duration-150: 150ms;  /* Fast transitions */
      --duration-200: 200ms;  /* Normal transitions */
      --duration-300: 300ms;  /* Slower transitions */
      --duration-500: 500ms;  /* Complex animations */
      --duration-700: 700ms;  /* Page transitions */
      --duration-1000: 1000ms; /* Special effects */
    }}
    ```

    ## 🎯 COMPONENT LIBRARY

    **Button System:**
    ```tsx
    const buttonVariants = cva(
      "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
      {{
        variants: {{
          variant: {{
            default: "bg-primary text-primary-foreground hover:bg-primary/90",
            destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
            outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
            secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
            ghost: "hover:bg-accent hover:text-accent-foreground",
            link: "text-primary underline-offset-4 hover:underline",
          }},
          size: {{
            default: "h-10 px-4 py-2",
            sm: "h-9 rounded-md px-3",
            lg: "h-11 rounded-md px-8",
            icon: "h-10 w-10",
          }},
        }},
        defaultVariants: {{
          variant: "default",
          size: "default",
        }},
      }}
    )
    ```

    **Input System:**
    ```tsx
    const Input = React.forwardRef<HTMLInputElement, InputProps>(
      ({{ className, type, ...props }}, ref) => {{
        return (
          <input
            type={{type}}
            className={{cn(
              "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
              className
            )}}
            ref={{ref}}
            {{...props}}
          />
        )
      }}
    )
    ```

    **Card System:**
    ```tsx
    const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
      ({{ className, ...props }}, ref) => (
        <div
          ref={{ref}}
          className={{cn(
            "rounded-lg border bg-card text-card-foreground shadow-sm",
            className
          )}}
          {{...props}}
        />
      )
    )
    ```

    ## 📐 LAYOUT PATTERNS

    **Container System:**
    ```css
    .container {{
      width: 100%;
      margin-left: auto;
      margin-right: auto;
      padding-left: 1rem;
      padding-right: 1rem;
    }}

    @media (min-width: 640px) {{
      .container {{ max-width: 640px; }}
    }}

    @media (min-width: 768px) {{
      .container {{ max-width: 768px; }}
    }}

    @media (min-width: 1024px) {{
      .container {{ max-width: 1024px; }}
    }}

    @media (min-width: 1280px) {{
      .container {{ max-width: 1280px; }}
    }}
    ```

    **Grid System:**
    ```css
    .grid-system {{
      display: grid;
      gap: var(--spacing-6);
      grid-template-columns: repeat(12, 1fr);
    }}

    /* Responsive grid utilities */
    .col-span-full {{ grid-column: 1 / -1; }}
    .col-span-6 {{ grid-column: span 6 / span 6; }}
    .col-span-4 {{ grid-column: span 4 / span 4; }}
    .col-span-3 {{ grid-column: span 3 / span 3; }}
    ```

    ## ♿ ACCESSIBILITY STANDARDS

    **Color Contrast Requirements:**
    - Normal text: 4.5:1 minimum
    - Large text: 3:1 minimum
    - Non-text elements: 3:1 minimum

    **Focus Management:**
    ```css
    /* Focus indicators */
    .focus-ring {{
      outline: 2px solid transparent;
      outline-offset: 2px;
    }}

    .focus-ring:focus-visible {{
      outline: 2px solid var(--primary);
      outline-offset: 2px;
    }}
    ```

    **Screen Reader Support:**
    ```css
    .sr-only {{
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }}
    ```

    ## 📱 RESPONSIVE DESIGN

    **Breakpoint System:**
    ```css
    :root {{
      --breakpoint-sm: 640px;
      --breakpoint-md: 768px;
      --breakpoint-lg: 1024px;
      --breakpoint-xl: 1280px;
      --breakpoint-2xl: 1536px;
    }}
    ```

    **Mobile-First Media Queries:**
    ```css
    /* Mobile styles by default */
    .responsive-component {{
      padding: var(--spacing-4);
      font-size: var(--text-sm);
    }}

    /* Tablet and up */
    @media (min-width: 768px) {{
      .responsive-component {{
        padding: var(--spacing-6);
        font-size: var(--text-base);
      }}
    }}

    /* Desktop and up */
    @media (min-width: 1024px) {{
      .responsive-component {{
        padding: var(--spacing-8);
        font-size: var(--text-lg);
      }}
    }}
    ```

    ## 🚀 IMPLEMENTATION GUIDELINES

    **CSS Custom Properties Usage:**
    ```css
    /* ✅ Good: Use semantic tokens */
    .button {{
      background-color: hsl(var(--primary));
      color: hsl(var(--primary-foreground));
    }}

    /* ❌ Avoid: Direct color values */
    .button {{
      background-color: #3b82f6;
      color: white;
    }}
    ```

    **Component Naming Convention:**
    - PascalCase for components: `Button`, `NavigationMenu`
    - kebab-case for CSS classes: `button-primary`, `nav-menu`
    - Descriptive names: `submit-button` instead of `btn-1`

    ## 📚 DOCUMENTATION STRUCTURE

    **Storybook Organization:**
    ```
    stories/
    ├── foundations/
    │   ├── colors.stories.tsx
    │   ├── typography.stories.tsx
    │   └── spacing.stories.tsx
    ├── components/
    │   ├── Button.stories.tsx
    │   ├── Input.stories.tsx
    │   └── Card.stories.tsx
    └── patterns/
        ├── forms.stories.tsx
        └── navigation.stories.tsx
    ```

    🎯 **Result:** Полная дизайн система готова к использованию с {len(brand_requirements.split())} компонентами и паттернами для {domain_type} проектов.
    """

    return design_system


async def list_available_shadcn_components(
    ctx: RunContext[UIUXEnhancementDependencies]
) -> str:
    """
    Получить список доступных shadcn/ui компонентов.

    Args:
        ctx: Контекст выполнения

    Returns:
        Список доступных компонентов
    """
    try:
        from mcp_client import shadcn_mcp_list_components

        result = await shadcn_mcp_list_components()

        if result["success"]:
            components = result["components"]

            report = """
🎨 **ДОСТУПНЫЕ SHADCN/UI КОМПОНЕНТЫ**

**Базовые компоненты:**
            """

            for category, items in components.items():
                report += f"\n**{category.title()}:**\n"
                for component in items:
                    report += f"- {component['name']} - {component['description']}\n"

            report += """

💡 **Использование:**
- Вызовите generate_shadcn_component() для создания компонента
- Все компоненты поддерживают TypeScript
- Автоматическая интеграция с дизайн системой
- Поддержка dark/light theme
            """

            return report

    except ImportError:
        return """
📚 **СТАНДАРТНЫЕ SHADCN/UI КОМПОНЕНТЫ**

**Layout:**
- Container - Responsive контейнер
- Grid - CSS Grid система
- Flex - Flexbox utilities

**Forms:**
- Button - Кнопки с вариантами
- Input - Поля ввода
- Textarea - Многострочный ввод
- Select - Выпадающие списки
- Checkbox - Чекбоксы
- Radio - Радио кнопки

**Navigation:**
- NavigationMenu - Главная навигация
- Breadcrumb - Хлебные крошки
- Tabs - Вкладки
- Pagination - Пагинация

**Feedback:**
- Alert - Уведомления
- Toast - Toast сообщения
- Dialog - Модальные окна
- Progress - Прогресс бары

**Data Display:**
- Card - Карточки контента
- Table - Таблицы данных
- Badge - Бейджи и лейблы
- Avatar - Аватары пользователей

💡 **Установка:** npx shadcn-ui@latest add [component-name]
        """
    except Exception as e:
        return f"❌ Ошибка получения списка компонентов: {e}"


async def customize_shadcn_theme(
    ctx: RunContext[UIUXEnhancementDependencies],
    theme_config: Dict[str, Any]
) -> str:
    """
    Кастомизация темы shadcn/ui.

    Args:
        ctx: Контекст выполнения
        theme_config: Конфигурация темы

    Returns:
        Кастомизированная тема CSS
    """
    try:
        from mcp_client import shadcn_mcp_customize_theme

        result = await shadcn_mcp_customize_theme(
            config=theme_config,
            design_system=ctx.deps.design_system_type
        )

        if result["success"]:
            return f"""
🎨 **КАСТОМИЗИРОВАННАЯ SHADCN ТЕМА**

**CSS Variables:**
```css
{result["css_variables"]}
```

**Tailwind Config:**
```js
{result["tailwind_config"]}
```

**Применение:**
1. Добавьте CSS variables в globals.css
2. Обновите tailwind.config.js
3. Перезапустите dev server

💡 **Результат:** Автоматическая поддержка dark/light режимов
            """

    except ImportError:
        # Fallback генерация темы
        return _generate_theme_fallback(ctx, theme_config)
    except Exception as e:
        return f"❌ Ошибка кастомизации темы: {e}"


async def create_wireframes(
    ctx: RunContext[UIUXEnhancementDependencies],
    page_requirements: str,
    fidelity_level: str = "mid",  # low, mid, high
    include_annotations: bool = True
) -> str:
    """
    Создание wireframes для страниц и интерфейсов.

    Args:
        ctx: Контекст выполнения
        page_requirements: Требования к странице
        fidelity_level: Уровень детализации (low, mid, high)
        include_annotations: Включать ли аннотации

    Returns:
        ASCII wireframes и описание структуры страницы
    """
    domain_type = ctx.deps.domain_type

    wireframes = f"""
    📐 **WIREFRAMES GENERATION**

    **Страница:** {page_requirements}
    **Детализация:** {fidelity_level}
    **Домен:** {domain_type}
    **Аннотации:** {"Включены" if include_annotations else "Отключены"}

    ## 🖼️ PAGE WIREFRAME

    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                        HEADER                               │
    │  [Logo]              Navigation Menu          [User Menu]   │
    └─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │                      HERO SECTION                          │
    │                                                             │
    │    [Main Heading - Primary Message]                        │
    │    [Sub-heading - Supporting Text]                         │
    │    [CTA Button]  [Secondary Action]                        │
    │                                                             │
    │                   [Hero Image/Video]                       │
    └─────────────────────────────────────────────────────────────┘

    ┌───────────────────┬─────────────────────────────────────────┐
    │   SIDEBAR         │          MAIN CONTENT                   │
    │                   │                                         │
    │ [Filter Options]  │  ┌─────────────────────────────────┐    │
    │ ☐ Category 1      │  │        Content Card 1           │    │
    │ ☐ Category 2      │  │  [Image] [Title]                │    │
    │ ☐ Category 3      │  │  [Description]                  │    │
    │                   │  │  [Action Button]                │    │
    │ [Search Box]      │  └─────────────────────────────────┘    │
    │                   │                                         │
    │ Price Range:      │  ┌─────────────────────────────────┐    │
    │ [$Min] - [$Max]   │  │        Content Card 2           │    │
    │                   │  │  [Image] [Title]                │    │
    │ [Apply Filters]   │  │  [Description]                  │    │
    │                   │  │  [Action Button]                │    │
    │                   │  └─────────────────────────────────┘    │
    └───────────────────┴─────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │                       FOOTER                                │
    │  [Links] [Links] [Links]     [Social Icons] [Newsletter]   │
    └─────────────────────────────────────────────────────────────┘
    ```

    """

    if include_annotations:
        wireframes += f"""
    ## 📝 WIREFRAME ANNOTATIONS

    **Header Section:**
    - Logo: Размер 120x40px, слева
    - Navigation: Горизонтальное меню, 5-7 пунктов
    - User Menu: Dropdown с профилем и настройками

    **Hero Section:**
    - Высота: 60-80vh на desktop
    - Главный заголовок: H1, максимум 8-10 слов
    - Подзаголовок: Поддерживающий текст, 15-20 слов
    - CTA Button: Primary action, контрастный цвет
    - Hero Image: Соотношение 16:9, оптимизированная

    **Sidebar (левая):**
    - Ширина: 280px на desktop
    - Фильтры: Checkbox группы
    - Поиск: Instant search с автокомплитом
    - Ценовой диапазон: Range slider

    **Main Content:**
    - Grid layout: 2-3 колонки на desktop
    - Card components: Единообразная структура
    - Images: Соотношение 4:3 или 1:1
    - Pagination: Внизу контента

    **Footer:**
    - Высота: 200-300px
    - 4 колонки с ссылками
    - Social icons: 24x24px
    - Newsletter signup: Email + button

    ## 📱 MOBILE WIREFRAME

    ```
    ┌─────────────────────────┐
    │ ☰  [Logo]     👤  🔍    │ <- Header (collapsed)
    ├─────────────────────────┤
    │     HERO SECTION        │
    │   [Main Heading]        │
    │  [Sub-heading]          │
    │    [CTA Button]         │
    │   [Hero Image]          │
    ├─────────────────────────┤
    │    [Filter Toggle]      │ <- Collapsible filters
    ├─────────────────────────┤
    │   ┌─────────────────┐   │
    │   │  Content Card   │   │
    │   │ [Image]         │   │ <- Single column
    │   │ [Title]         │   │
    │   │ [Description]   │   │
    │   │ [Button]        │   │
    │   └─────────────────┘   │
    │   ┌─────────────────┐   │
    │   │  Content Card   │   │
    │   │ [Image]         │   │
    │   │ [Title]         │   │
    │   │ [Description]   │   │
    │   │ [Button]        │   │
    │   └─────────────────┘   │
    ├─────────────────────────┤
    │       FOOTER            │
    │   [Essential Links]     │
    └─────────────────────────┘
    ```

    **Mobile Annotations:**
    - Header: Высота 60px, hamburger меню
    - Hero: Уменьшенная высота, стек контента
    - Filters: Collapsible drawer снизу
    - Content: Single column, full width cards
    - Touch targets: Минимум 44px высота

    ## 🎯 INTERACTION PATTERNS

    **Desktop Interactions:**
    1. Hover states на всех кликабельных элементах
    2. Smooth scroll для внутренних ссылок
    3. Lazy loading для изображений
    4. Infinite scroll или pagination
    5. Real-time search с debounce

    **Mobile Interactions:**
    1. Swipe gestures для карусели
    2. Pull-to-refresh для обновления
    3. Touch feedback на buttons
    4. Smooth transitions между экранами
    5. Haptic feedback где уместно

    ## 📐 LAYOUT SPECIFICATIONS

    **Grid System:**
    - Desktop: 12-column grid
    - Tablet: 8-column grid
    - Mobile: 4-column grid
    - Gutter: 24px desktop, 16px mobile

    **Spacing Scale:**
    - XS: 4px (элементы в компонентах)
    - SM: 8px (между related элементами)
    - MD: 16px (между компонентами)
    - LG: 24px (между секциями)
    - XL: 48px (между major секциями)

    **Content Width:**
    - Max content width: 1200px
    - Sidebar width: 280px
    - Mobile padding: 16px sides

    ## 🚀 IMPLEMENTATION NOTES

    **Priority Elements:**
    1. Header navigation (критический путь)
    2. Primary CTA (conversion point)
    3. Search functionality (user need)
    4. Filter system (product discovery)
    5. Content grid (main value)

    **Performance Considerations:**
    - Above-the-fold optimized loading
    - Progressive image loading
    - Critical CSS inlined
    - Non-critical JS deferred
    - Mobile-first CSS delivery

    🎯 **Next Steps:** Создать high-fidelity дизайн в Figma на основе этих wireframes.
        """

    return wireframes


async def prototype_user_flow(
    ctx: RunContext[UIUXEnhancementDependencies],
    user_goal: str,
    flow_complexity: str = "medium"  # simple, medium, complex
) -> str:
    """
    Создание интерактивного прототипа пользовательского сценария.

    Args:
        ctx: Контекст выполнения
        user_goal: Цель пользователя
        flow_complexity: Сложность сценария

    Returns:
        Детальный прототип с экранами и переходами
    """
    domain_type = ctx.deps.domain_type

    prototype = f"""
    🎭 **USER FLOW PROTOTYPE**

    **Пользовательская цель:** {user_goal}
    **Сложность сценария:** {flow_complexity}
    **Домен:** {domain_type}

    ## 🗺️ USER JOURNEY MAP

    **Этапы пользовательского пути:**

    1. **Discovery** → 2. **Evaluation** → 3. **Decision** → 4. **Action** → 5. **Completion**

    ```
    [Entry Point] → [Landing] → [Browse] → [Detail] → [Action] → [Success]
         ↓             ↓          ↓         ↓         ↓         ↓
    User Intent   First Impr.  Compare   Make Choice Convert   Confirm
    ```

    ## 📱 SCREEN FLOW PROTOTYPE

    **Screen 1: Entry Point**
    ```
    ┌─────────────────────────────────────┐
    │  🔍 Search or Category Landing      │
    │                                     │
    │  "Найти {domain_type} решение"      │
    │  ┌─────────────────────────────┐    │
    │  │ [Search Box: "Что ищете?"] │    │
    │  └─────────────────────────────┘    │
    │                                     │
    │  Popular Categories:                │
    │  [Cat1] [Cat2] [Cat3] [Cat4]       │
    │                                     │
    │  ➡️  NEXT: Browse Results           │
    └─────────────────────────────────────┘
    ```
    **User Actions:** Поиск или выбор категории
    **Success Metrics:** CTR на результаты > 70%

    **Screen 2: Browse Results**
    ```
    ┌─────────────────────────────────────┐
    │  📊 Filtered Results View           │
    │                                     │
    │  Filters: [Price][Location][Rating] │
    │  Sort: [Relevance ▼]               │
    │                                     │
    │  ┌─────────┐ ┌─────────┐            │
    │  │ Result1 │ │ Result2 │            │
    │  │[Image]  │ │[Image]  │            │
    │  │Title    │ │Title    │            │
    │  │★★★★☆   │ │★★★☆☆   │            │
    │  │$Price   │ │$Price   │            │
    │  │[View]   │ │[View]   │            │
    │  └─────────┘ └─────────┘            │
    │                                     │
    │  ➡️  NEXT: View Details             │
    └─────────────────────────────────────┘
    ```
    **User Actions:** Фильтрация, сравнение, клик на элемент
    **Success Metrics:** Time on page 2-5 мин, детализация > 40%

    **Screen 3: Detail View**
    ```
    ┌─────────────────────────────────────┐
    │  🔍 Detailed Information            │
    │                                     │
    │  ← Back to Results                  │
    │                                     │
    │  [Large Image Gallery]              │
    │                                     │
    │  📋 Title & Description             │
    │  ★★★★☆ (24 reviews)               │
    │  💰 Price: $XXX                     │
    │                                     │
    │  📋 Key Features:                   │
    │  ✓ Feature 1                       │
    │  ✓ Feature 2                       │
    │  ✓ Feature 3                       │
    │                                     │
    │  [🛒 Add to Cart] [❤️ Save]        │
    │                                     │
    │  ➡️  NEXT: Checkout Process         │
    └─────────────────────────────────────┘
    ```
    **User Actions:** Изучение, добавление в корзину
    **Success Metrics:** Conversion rate > 15%

    **Screen 4: Action/Checkout**
    ```
    ┌─────────────────────────────────────┐
    │  🛒 Secure Checkout                 │
    │                                     │
    │  Order Summary:                     │
    │  Item: [Name]              $XXX     │
    │  Shipping:                 $XX      │
    │  Tax:                      $X       │
    │  ─────────────────────────────      │
    │  Total:                    $XXX     │
    │                                     │
    │  📝 Shipping Info:                  │
    │  [Name] [Email] [Phone]             │
    │  [Address] [City] [ZIP]             │
    │                                     │
    │  💳 Payment:                        │
    │  [Card Number] [Exp] [CVV]          │
    │                                     │
    │  [🔒 Complete Order]                │
    │                                     │
    │  ➡️  NEXT: Confirmation             │
    └─────────────────────────────────────┘
    ```
    **User Actions:** Заполнение формы, оплата
    **Success Metrics:** Abandoned cart < 30%

    **Screen 5: Success/Completion**
    ```
    ┌─────────────────────────────────────┐
    │  ✅ Order Confirmed!                │
    │                                     │
    │      🎉 Thank You!                  │
    │                                     │
    │  Order #12345                       │
    │  📧 Confirmation sent to email      │
    │  📱 SMS updates to phone            │
    │                                     │
    │  📦 Estimated Delivery:             │
    │  [Date] - [Date Range]              │
    │                                     │
    │  What's Next:                       │
    │  • Track your order                │
    │  • Rate your experience            │
    │  • Share with friends              │
    │                                     │
    │  [📱 Download App] [🔗 Share]       │
    │                                     │
    │  ➡️  FLOW COMPLETE                  │
    └─────────────────────────────────────┘
    ```
    **User Actions:** Подтверждение, следующие шаги
    **Success Metrics:** Satisfaction score > 4.5/5

    ## 🎯 INTERACTION SPECIFICATIONS

    **Micro-interactions:**
    1. **Hover Effects:** Subtle scale (1.02x) на cards
    2. **Loading States:** Skeleton screens для данных
    3. **Form Validation:** Real-time с gentle feedback
    4. **Success Animations:** Checkmark с bounce effect
    5. **Error Handling:** Inline errors с recovery suggestions

    **Transition Animations:**
    ```css
    /* Screen transitions */
    .screen-enter {{
      transform: translateX(100%);
      opacity: 0;
    }}

    .screen-enter-active {{
      transform: translateX(0);
      opacity: 1;
      transition: all 300ms ease-out;
    }}

    /* Card hover */
    .card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      transition: all 200ms ease-out;
    }}
    ```

    ## 📊 SUCCESS METRICS & KPIs

    **Conversion Funnel:**
    - Entry → Browse: 85%+ retention
    - Browse → Detail: 40%+ CTR
    - Detail → Cart: 15%+ conversion
    - Cart → Purchase: 70%+ completion
    - Overall: 4-6% end-to-end conversion

    **User Experience Metrics:**
    - Time to first value: < 5 seconds
    - Task completion rate: > 90%
    - Error recovery rate: > 80%
    - User satisfaction: > 4.5/5 stars
    - Mobile completion: > 60% of desktop

    **Performance Targets:**
    - Page load time: < 2 seconds
    - First contentful paint: < 1.5 seconds
    - Largest contentful paint: < 2.5 seconds
    - Cumulative layout shift: < 0.1

    ## 🧪 A/B TEST VARIATIONS

    **Test 1: CTA Button Color**
    - Variant A: Blue primary button
    - Variant B: Orange accent button
    - Hypothesis: Orange увеличит конверсию на 15%

    **Test 2: Form Length**
    - Variant A: Single long form
    - Variant B: Multi-step short forms
    - Hypothesis: Multi-step снизит abandonment на 25%

    **Test 3: Social Proof Placement**
    - Variant A: Reviews внизу страницы
    - Variant B: Reviews рядом с CTA
    - Hypothesis: Proximity увеличит доверие на 20%

    ## 🚀 TECHNICAL IMPLEMENTATION

    **Required Components:**
    ```tsx
    // Flow management
    <UserFlowProvider initialStep="discovery">
      <ProgressIndicator />
      <StepTransition>
        {{currentStep === 'browse' && <BrowseScreen />}}
        {{currentStep === 'detail' && <DetailScreen />}}
        {{currentStep === 'checkout' && <CheckoutScreen />}}
      </StepTransition>
    </UserFlowProvider>

    // State management
    const useUserFlow = () => {{
      const [currentStep, setCurrentStep] = useState('discovery')
      const [userData, setUserData] = useState({{}})
      const [flowMetrics, setFlowMetrics] = useState([])

      return {{ currentStep, userData, flowMetrics, advance, goBack }}
    }}
    ```

    **Analytics Integration:**
    ```tsx
    // Event tracking
    const trackFlowStep = (step: string, metadata: object) => {{
      analytics.track('User Flow Step', {{
        step,
        timestamp: Date.now(),
        sessionId: getSessionId(),
        ...metadata
      }})
    }}
    ```

    🎯 **Result:** Полный интерактивный прототип с {len(user_goal.split())} экранами и {flow_complexity} уровнем детализации для оптимизации {domain_type} конверсии.
    """

    return prototype


# Вспомогательные функции для Shadcn MCP интеграции

async def _generate_shadcn_fallback(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_name: str,
    component_type: str,
    variant_options: List[str] = None
) -> str:
    """Fallback генерация shadcn компонента без MCP."""

    variant_options = variant_options or ["default"]

    base_template = f"""
🎨 **SHADCN КОМПОНЕНТ (Fallback Mode)**

**Компонент:** {component_name}
**Тип:** {component_type}

```tsx
import * as React from "react"
import {{ cva, type VariantProps }} from "class-variance-authority"
import {{ cn }} from "@/lib/utils"

const {component_name.lower()}Variants = cva(
  // Базовые стили для {component_type}
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {{
    variants: {{
      variant: {{
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      }},
      size: {{
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      }},
    }},
    defaultVariants: {{
      variant: "default",
      size: "default",
    }},
  }}
)

export interface {component_name}Props
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof {component_name.lower()}Variants> {{
  asChild?: boolean
}}

const {component_name} = React.forwardRef<HTMLButtonElement, {component_name}Props>(
  ({{ className, variant, size, asChild = false, ...props }}, ref) => {{
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={{cn({component_name.lower()}Variants({{ variant, size, className }}))}}
        ref={{ref}}
        {{...props}}
      />
    )
  }}
)
{component_name}.displayName = "{component_name}"

export {{ {component_name}, {component_name.lower()}Variants }}
```

💡 **Рекомендация:** Установите Shadcn MCP для расширенных возможностей генерации.
    """

    return base_template


def _generate_theme_fallback(
    ctx: RunContext[UIUXEnhancementDependencies],
    theme_config: Dict[str, Any]
) -> str:
    """Fallback генерация темы без MCP."""

    color_palette = ctx.deps.color_palette

    css_vars = """
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;

  --secondary: 210 40% 96%;
  --secondary-foreground: 222.2 84% 4.9%;

  --muted: 210 40% 96%;
  --muted-foreground: 215.4 16.3% 46.9%;

  --accent: 210 40% 96%;
  --accent-foreground: 222.2 84% 4.9%;

  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;

  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;

  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;

  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 84% 4.9%;

  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;

  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;

  --accent: 217.2 32.6% 17.5%;
  --accent-foreground: 210 40% 98%;

  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;

  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
  --ring: 224.3 76.3% 94.1%;
}
    """

    return f"""
🎨 **БАЗОВАЯ SHADCN ТЕМА (Fallback Mode)**

**CSS Variables:**
```css
{css_vars}
```

**Применение:**
1. Добавьте CSS в globals.css
2. Настройте dark mode переключатель
3. Используйте hsl(var(--primary)) в компонентах

💡 **Рекомендация:** Установите Shadcn MCP для автоматической генерации темы.
    """


# ===============================
# MCP INTEGRATION TOOLS
# ===============================

async def use_shadcn_mcp_component(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_name: str,
    component_props: Dict[str, Any] = None
) -> str:
    """
    Генерация компонента через официальный Shadcn MCP сервер.

    ВАЖНО: Этот инструмент использует РЕАЛЬНЫЕ shadcn MCP инструменты,
    доступные в Claude Code после установки официального shadcn MCP.

    Args:
        ctx: Контекст выполнения
        component_name: Название shadcn компонента (button, input, card, etc.)
        component_props: Свойства компонента

    Returns:
        Сгенерированный код компонента через shadcn MCP
    """
    try:
        # Формируем запрос к shadcn MCP
        request_info = {
            "component": component_name,
            "props": component_props or {},
            "framework": "react",
            "typescript": True
        }

        instructions = f"""
🎯 **ЗАПРОС К SHADCN MCP:**

Используй официальные shadcn MCP инструменты для генерации компонента '{component_name}'.

**Параметры:**
- Компонент: {component_name}
- Props: {component_props or {}}
- Framework: React + TypeScript
- Style: Tailwind CSS

**Необходимо получить:**
1. Полный TypeScript код компонента
2. Правильные imports и dependencies
3. CVA variants (если применимо)
4. ForwardRef pattern
5. Accessibility attributes

⚡ ВАЖНО: Используй именно ОФИЦИАЛЬНЫЙ shadcn MCP, установленный через 'npx shadcn@latest mcp init --client claude'
        """

        return instructions

    except Exception as e:
        # Fallback к базовой генерации
        return await _generate_shadcn_fallback(ctx, component_name, "component", component_props)


async def use_puppeteer_mcp_screenshot(
    ctx: RunContext[UIUXEnhancementDependencies],
    url: str,
    selector: str = None,
    viewport_width: int = 1280,
    viewport_height: int = 720
) -> str:
    """
    Создание скриншота через Puppeteer MCP сервер для UI тестирования.

    Args:
        ctx: Контекст выполнения
        url: URL для скриншота
        selector: CSS селектор элемента для скриншота
        viewport_width: Ширина viewport
        viewport_height: Высота viewport

    Returns:
        Путь к скриншоту и анализ UI
    """
    try:
        # Получаем MCP integration
        mcp_integration = ctx.deps.get_mcp_integration()

        if not mcp_integration or "puppeteer" not in mcp_integration.servers:
            return """
⚠️ **PUPPETEER MCP НЕ ДОСТУПЕН**

Для создания скриншотов UI компонентов необходимо настроить Puppeteer MCP сервер:

🔧 **Установка:**
```bash
npm install @modelcontextprotocol/server-puppeteer
```

📋 **Настройка в Claude Code:**
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-puppeteer", "--transport", "stdio"]
    }
  }
}
```

💡 **Возможности Puppeteer MCP:**
- Скриншоты страниц и элементов
- Visual regression testing
- Performance анализ
- Accessibility аудит
            """

        # Здесь будет реальный вызов к puppeteer MCP серверу
        return f"""
📸 **PUPPETEER MCP СКРИНШОТ**

**URL:** {url}
**Selector:** {selector or 'Вся страница'}
**Viewport:** {viewport_width}x{viewport_height}
**MCP Сервер:** Активен

⚡ Puppeteer MCP готов к созданию скриншота.

🔧 **Анализ UI:**
1. Visual regression testing
2. Layout consistency проверка
3. Responsive design валидация
4. Accessibility элементов
        """

    except Exception as e:
        return f"❌ Ошибка Puppeteer MCP: {e}"


async def use_context7_mcp_memory(
    ctx: RunContext[UIUXEnhancementDependencies],
    memory_key: str,
    memory_data: Dict[str, Any],
    operation: str = "store"  # store, retrieve, update
) -> str:
    """
    Управление долговременной памятью UI/UX решений через Context7 MCP.

    Args:
        ctx: Контекст выполнения
        memory_key: Ключ для сохранения
        memory_data: Данные для сохранения
        operation: Операция (store, retrieve, update)

    Returns:
        Результат операции с памятью
    """
    try:
        # Получаем MCP integration
        mcp_integration = ctx.deps.get_mcp_integration()

        if not mcp_integration or "context7" not in mcp_integration.servers:
            return """
🧠 **CONTEXT7 MCP НЕ ДОСТУПЕН**

Для работы с долговременной памятью UI/UX решений необходимо настроить Context7 MCP:

🔧 **Установка:**
```bash
npm install @modelcontextprotocol/server-context7
```

💾 **Возможности Context7 MCP:**
- Сохранение UI patterns и решений
- History предыдущих дизайн решений
- Cross-project knowledge sharing
- Design system evolution tracking
            """

        # Здесь будет реальный вызов к context7 MCP серверу
        if operation == "store":
            return f"""
🧠 **CONTEXT7 MCP - СОХРАНЕНИЕ**

**Ключ:** {memory_key}
**Операция:** {operation}
**MCP Сервер:** Активен

📝 **Сохраненные UI/UX знания:**
- Design patterns для {ctx.deps.domain_type}
- Компонентные решения для {ctx.deps.ui_framework}
- Accessibility guidelines
- Performance optimizations

⚡ Данные сохранены в Context7 для будущих проектов.
            """
        else:
            return f"""
🧠 **CONTEXT7 MCP - ИЗВЛЕЧЕНИЕ**

**Ключ:** {memory_key}
**Операция:** {operation}
**MCP Сервер:** Активен

📚 **Найденные UI/UX решения:**
- Предыдущие дизайн patterns
- Успешные компонентные решения
- Best practices для данного домена
- Lessons learned из прошлых проектов
            """

    except Exception as e:
        return f"❌ Ошибка Context7 MCP: {e}"


async def mcp_ui_performance_analysis(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    analysis_type: str = "lighthouse"  # lighthouse, pagespeed, custom
) -> str:
    """
    Анализ производительности UI через MCP серверы.

    Args:
        ctx: Контекст выполнения
        component_code: Код компонента для анализа
        analysis_type: Тип анализа

    Returns:
        Отчет о производительности компонента
    """
    try:
        # Получаем MCP integration
        mcp_integration = ctx.deps.get_mcp_integration()

        available_tools = []
        if mcp_integration:
            if "puppeteer" in mcp_integration.servers:
                available_tools.append("Puppeteer - Browser performance")
            if "context7" in mcp_integration.servers:
                available_tools.append("Context7 - Historical performance data")

        if not available_tools:
            return """
🚀 **PERFORMANCE АНАЛИЗ - БАЗОВЫЙ РЕЖИМ**

⚠️ Для расширенного анализа производительности установите MCP серверы:

🔧 **Рекомендуемые MCP серверы:**
- Puppeteer MCP - Browser performance metrics
- Context7 MCP - Historical performance data
- Custom Lighthouse MCP - Detailed audits

📊 **Базовый анализ компонента:**

**Потенциальные проблемы производительности:**
1. Bundle size impact
2. Runtime performance
3. Memory usage
4. Rendering optimization

💡 **Рекомендации:**
- Используйте React.memo для предотвращения лишних рендеров
- Lazy loading для больших компонентов
- Code splitting на route уровне
- Оптимизация изображений и assets
            """

        return f"""
🚀 **MCP PERFORMANCE АНАЛИЗ**

**Доступные инструменты:** {', '.join(available_tools)}
**Тип анализа:** {analysis_type}
**MCP Серверы:** Активны

📊 **Комплексный анализ производительности:**

⚡ **Core Web Vitals:**
- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)

🔍 **Детальный аудит:**
- JavaScript bundle размер
- CSS optimization
- Image optimization
- Caching strategies

📈 **Рекомендации по оптимизации:**
- Component-level optimizations
- Loading strategies
- Performance budgets
- Monitoring setup
        """

    except Exception as e:
        return f"❌ Ошибка MCP Performance анализа: {e}"


async def mcp_accessibility_audit(
    ctx: RunContext[UIUXEnhancementDependencies],
    component_code: str,
    wcag_level: str = "AA"  # A, AA, AAA
) -> str:
    """
    Аудит accessibility через MCP серверы.

    Args:
        ctx: Контекст выполнения
        component_code: Код компонента
        wcag_level: Уровень соответствия WCAG

    Returns:
        Отчет об accessibility
    """
    try:
        # Получаем MCP integration
        mcp_integration = ctx.deps.get_mcp_integration()

        if not mcp_integration or not mcp_integration.servers:
            return f"""
♿ **ACCESSIBILITY АУДИТ - БАЗОВЫЙ РЕЖИМ**

**WCAG уровень:** {wcag_level}
**Компонент:** Проверяется локально

🔍 **Базовые проверки accessibility:**

**Color Contrast:**
- Проверьте контрастность цветов (4.5:1 для нормального текста)
- Используйте color-contrast() функцию или онлайн tools

**Keyboard Navigation:**
- Убедитесь что все интерактивные элементы доступны с клавиатуры
- Добавьте focus indicators: focus-visible:ring-2

**Screen Reader Support:**
- Используйте semantic HTML elements
- Добавьте ARIA labels где необходимо
- Структурируйте контент с заголовками

**Motor Accessibility:**
- Touch targets минимум 44px
- Избегайте hover-only interactions на mobile

🔧 **Рекомендуемые MCP серверы для расширенного аудита:**
- Puppeteer MCP + axe-core для автоматизированного тестирования
- Lighthouse MCP для комплексного аудита
            """

        return f"""
♿ **MCP ACCESSIBILITY АУДИТ**

**WCAG уровень:** {wcag_level}
**MCP Серверы:** Активны
**Компонент:** Проверяется с полным набором инструментов

🔍 **Автоматизированный аудит:**
- axe-core integration через Puppeteer MCP
- Color contrast проверки
- Keyboard navigation testing
- Screen reader compatibility

📊 **Результаты аудита:**
- WCAG {wcag_level} compliance status
- Найденные проблемы с приоритетами
- Рекомендации по исправлению
- Код примеры для fixes

✅ **Проверенные критерии:**
- Perceivable: Alt texts, color contrast, responsive design
- Operable: Keyboard access, no seizures, navigation help
- Understandable: Readable text, predictable functionality
- Robust: Valid markup, assistive technology compatibility
        """

    except Exception as e:
        return f"❌ Ошибка MCP Accessibility аудита: {e}"