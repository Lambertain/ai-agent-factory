# UI/UX Enhancement Agent - Module Selection Logic

## 🎯 Коли читати цей файл:

**ЗАВЖДИ після прочитання системного промпту та задачі з Archon MCP.**

Цей файл містить логіку вибору модулів для контекстно-залежного читання.

## 📊 MODULE OVERVIEW

| # | Module | Priority | Lines | Domain | Load When |
|---|--------|----------|-------|--------|-----------|
| **01** | [Design Systems](modules/01_design_systems.md) | 🔴 CRITICAL | ~409 | Tailwind & shadcn/ui | Design system, themes, UI components |
| **02** | [Accessibility](modules/02_accessibility.md) | 🟡 HIGH | ~284 | WCAG & a11y | Accessibility, WCAG, focus, screen readers |
| **03** | [CSS Animations](modules/03_animations.md) | 🟢 MEDIUM | ~329 | Animations & Transitions | Animations, loading states, transitions |
| **04** | [Responsive Design](modules/04_responsive_design.md) | 🔴 CRITICAL | ~456 | Mobile-First Layout | Responsive, mobile-first, breakpoints |
| **05** | [Performance UI](modules/05_performance_ui.md) | 🟡 HIGH | ~538 | UI Optimization | Performance, lazy loading, virtual scrolling |
| **06** | [Domain Patterns](modules/06_domain_patterns.md) | 🟢 MEDIUM | ~484 | Domain-Specific UI | E-commerce, SaaS, Blog, Social UI |
| **07** | [MCP Integration](modules/07_mcp_integration.md) | 🟢 MEDIUM | ~241 | Testing & Automation | Puppeteer, Figma, Lighthouse MCPs |

**Общее количество строк в модулях:** ~2,741 строк

**Стратегия чтения:** 2-4 модуля на задачу (~800-1,800 токенов)

## 📦 Module 01: Design Systems - Tailwind CSS & shadcn/ui

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание любых UI компонентов
- Настройка дизайн-системы проекта
- Работа с Tailwind CSS конфигурацией
- Темизация (light/dark mode)
- Интеграция shadcn/ui компонентов

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* дизайн-система, tailwind, shadcn, тема, темізація, кольори, css variables, адаптивна типографія, компоненти ui, універсальна карточка, theme provider

*English:* design system, tailwind, shadcn, theme, theming, colors, css variables, adaptive typography, ui components, universal card, theme provider

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Tailwind Config (tailwind.config.js, colors, animations, breakpoints)
- shadcn/ui Components (Button, Card, Badge, Progress, Dialog)
- CSS Variables (hsl(), var(--primary), semantic colors)
- Theme System (ThemeProvider, useTheme, light/dark mode)
- Universal Components (UniversalCard, responsive variants, size variants)
- Design Tokens (spacing, borderRadius, fontFamily, screens)

**Примеры задач:**
- "Настроить дизайн-систему для проекта"
- "Создать универсальный UI компонент"
- "Добавить dark mode в приложение"
- "Интегрировать shadcn/ui компоненты"
- "Настроить Tailwind конфигурацию"

## 📦 Module 02: Accessibility (WCAG & a11y Patterns)

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Обеспечение доступности интерфейса
- Реализация WCAG 2.1 AA требований
- Focus management в модальных окнах
- Screen reader поддержка
- Keyboard navigation

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* доступність, wcag, a11y, фокус, focus management, screen reader, aria, клавіатурна навігація, skip navigation, accessibility

*English:* accessibility, wcag, a11y, focus, focus management, screen reader, aria, keyboard navigation, skip navigation, accessible

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- WCAG Compliance (2.1 AA, color contrast 4.5:1, keyboard support)
- Focus Management (useFocusManagement, trap focus, restore focus)
- ARIA Attributes (aria-label, aria-describedby, aria-live, aria-atomic)
- Screen Readers (useScreenReaderAnnouncements, live regions, polite/assertive)
- Skip Navigation (SkipNavigation component, #main-content anchors)
- Semantic HTML (<button>, <nav>, <main>, <label> tags)

**Примеры задач:**
- "Сделать интерфейс доступным для screen readers"
- "Реализовать keyboard navigation"
- "Добавить skip navigation links"
- "Проверить WCAG 2.1 AA compliance"
- "Улучшить focus management в модальных окнах"

## 📦 Module 03: CSS Animation Library

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Добавление анимаций в UI
- Loading states (skeleton, shimmer)
- Micro-interactions (button press, hover)
- Page transitions
- Status indicators

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* анімація, skeleton, shimmer, перехід, loading state, інтеракція, button press, page transition, glass morphism, gradient text

*English:* animation, skeleton, shimmer, transition, loading state, interaction, button press, page transition, glass morphism, gradient text

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Loading States (skeleton, shimmer, pulse)
- Interaction Feedback (button-press, card-hover, gentle-bounce)
- Page Transitions (page-enter, fade-in, slide-in)
- Status Indicators (pulse-success, pulse-warning, pulse-error)
- Scroll Effects (smooth-scroll, scroll-fade)
- Glass Morphism (backdrop-blur, glass effect)
- Text Effects (gradient-text, animated gradients)

**Примеры задач:**
- "Добавить skeleton loading для карточек"
- "Реализовать smooth page transitions"
- "Создать micro-interactions для кнопок"
- "Добавить shimmer эффект к изображениям"
- "Применить glass morphism к navigation bar"

## 📦 Module 04: Responsive Design System

### 🔴 CRITICAL Priority

**КОГДА ЧИТАТЬ:**
- Создание responsive layout
- Mobile-first design
- Adaptive navigation
- Grid systems
- Breakpoint management

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* responsive, адаптивний, mobile-first, breakpoints, сітка, grid, навігація, adaptive navigation, responsive container, fluid typography

*English:* responsive, adaptive, mobile-first, breakpoints, grid, navigation, adaptive navigation, responsive container, fluid typography

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Mobile-First Approach (sm: → md: → lg: progression)
- Responsive Components (ResponsiveContainer, ResponsiveGrid, AdaptiveNavigation)
- Breakpoint System (xs, sm, md, lg, xl, 2xl, 3xl)
- Touch Targets (min 44x44px, spacing 8px between targets)
- Container Queries (@container, component-level responsiveness)
- Fluid Typography (clamp(), responsive text sizes)
- Responsive Images (srcSet, sizes, picture element, art direction)

**Примеры задач:**
- "Создать responsive layout для dashboard"
- "Реализовать adaptive navigation с mobile menu"
- "Настроить breakpoints для проекта"
- "Добавить fluid typography"
- "Создать responsive grid для продуктов"

## 📦 Module 05: UI Performance Optimization

### 🟡 HIGH Priority

**КОГДА ЧИТАТЬ:**
- Оптимизация производительности UI
- Работа с большими списками
- Lazy loading контента
- Code splitting
- Core Web Vitals optimization

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* performance, оптимізація, продуктивність, віртуалізація, lazy loading, code splitting, bundle size, core web vitals, lcp, fid, cls

*English:* performance, optimization, virtualization, lazy loading, code splitting, bundle size, core web vitals, lcp, fid, cls

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Virtual Scrolling (VirtualizedList, @tanstack/react-virtual, overscan)
- Lazy Loading (LazyLoadImage, Intersection Observer, loading="lazy")
- Code Splitting (React.lazy, Suspense, dynamic imports, route splitting)
- Image Optimization (WebP, AVIF, srcSet, Next/Image, quality settings)
- Core Web Vitals (LCP, FID, CLS, FCP, TTI metrics)
- Bundle Optimization (tree shaking, webpack-bundle-analyzer)
- React Optimization (React.memo, useMemo, useCallback)
- Runtime Performance (debounce, throttle, requestAnimationFrame)

**Примеры задач:**
- "Оптимизировать список с 10,000+ элементов"
- "Добавить lazy loading для изображений"
- "Реализовать code splitting по роутам"
- "Улучшить Core Web Vitals метрики"
- "Уменьшить bundle size приложения"

## 📦 Module 06: Domain-Specific UI Patterns

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- E-commerce проекты
- SaaS dashboard
- Blog/CMS системы
- Social media приложения

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* e-commerce, продукт, магазин, saas, dashboard, аналітика, blog, cms, стаття, social media, пост, коментарі

*English:* e-commerce, product, shop, saas, dashboard, analytics, blog, cms, article, social media, post, comments

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- E-commerce UI (ProductCard, ratings, discounts, add-to-cart, quick-view)
- SaaS Dashboard (AnalyticsWidget, metrics, trends, charts, KPI cards)
- Blog/CMS (ArticleCard, author, excerpt, read-time, categories, tags)
- Social Media (PostCard, likes, comments, shares, feed, timeline)
- Domain-Specific Patterns (checkout flow, user profile, content feed)

**Примеры задач:**
- "Создать карточку продукта для интернет-магазина"
- "Реализовать SaaS dashboard с метриками"
- "Добавить blog layout для статей"
- "Создать social media feed компонент"
- "Разработать checkout flow для e-commerce"

## 📦 Module 07: MCP Integration для UI/UX

### 🟢 MEDIUM Priority

**КОГДА ЧИТАТЬ:**
- Автоматизация визуального тестирования
- Синхронизация дизайна с Figma
- Performance audits
- Cross-browser testing
- Accessibility validation

**КЛЮЧЕВЫЕ СЛОВА:**

*Русские:* mcp, puppeteer, figma, lighthouse, тестування, візуальна регресія, accessibility audit, cross-browser, browserstack

*English:* mcp, puppeteer, figma, lighthouse, testing, visual regression, accessibility audit, cross-browser, browserstack

**ТЕХНИЧЕСКИЕ ТРИГГЕРЫ:**
- Puppeteer MCP (screenshot, navigate, visual testing, E2E automation)
- Figma MCP (design tokens export, component generation, design sync)
- Lighthouse MCP (Core Web Vitals, accessibility audit, performance report)
- BrowserStack MCP (cross-browser testing, real devices, iOS/Android)
- Contrast Checker MCP (WCAG color validation, contrast ratio, accessible palettes)
- Automated Testing (pre-commit hooks, CI/CD integration, visual regression)

**Примеры задач:**
- "Настроить автоматическое тестирование UI"
- "Синхронизировать design tokens из Figma"
- "Запустить accessibility audit через Lighthouse"
- "Проверить кросс-браузерную совместимость"
- "Настроить visual regression testing"

---

## 🎯 PRIORITY CASCADE (как часто читается каждый модуль)

### 🔴 CRITICAL Priority (читаются 70-80% задач)
- **Module 01:** Design Systems - основа любого UI компонента
- **Module 04:** Responsive Design - каждый UI должен быть адаптивным

### 🟡 HIGH Priority (читаются 50-60% задач)
- **Module 02:** Accessibility - важно для качественных приложений
- **Module 05:** Performance UI - критично для больших приложений

### 🟢 MEDIUM Priority (читаются 20-40% задач)
- **Module 03:** Animations - для улучшения UX, но не всегда
- **Module 06:** Domain Patterns - специфично для определенных доменов
- **Module 07:** MCP Integration - для автоматизации и тестирования

---

## 📝 ПРИМЕРЫ КОМБИНАЦИЙ МОДУЛЕЙ ДЛЯ ТИПОВЫХ ЗАДАЧ

### Задача: "Создать универсальный UI компонент для проекта"
**Читать:**
- ✅ Module 01 (Design Systems) - CRITICAL
- ✅ Module 04 (Responsive Design) - CRITICAL

**Токены:** ~865 (409 + 456)

### Задача: "Улучшить accessibility приложения"
**Читать:**
- ✅ Module 02 (Accessibility) - HIGH
- ✅ Module 01 (Design Systems) - CRITICAL
- ✅ Module 04 (Responsive Design) - CRITICAL

**Токены:** ~1,149 (284 + 409 + 456)

### Задача: "Оптимизировать performance большого списка"
**Читать:**
- ✅ Module 05 (Performance UI) - HIGH
- ✅ Module 04 (Responsive Design) - CRITICAL

**Токены:** ~994 (538 + 456)

### Задача: "Создать E-commerce product card с анимациями"
**Читать:**
- ✅ Module 01 (Design Systems) - CRITICAL
- ✅ Module 06 (Domain Patterns) - MEDIUM
- ✅ Module 03 (Animations) - MEDIUM
- ✅ Module 04 (Responsive Design) - CRITICAL

**Токены:** ~1,678 (409 + 484 + 329 + 456)

### Задача: "Настроить автоматическое тестирование UI"
**Читать:**
- ✅ Module 07 (MCP Integration) - MEDIUM
- ✅ Module 02 (Accessibility) - HIGH

**Токены:** ~525 (241 + 284)

---

## 🔍 KEYWORD-BASED MODULE SELECTION FUNCTION

```python
def select_modules_for_task(task_description: str) -> list[str]:
    """
    Выбрать модули для чтения на основе описания задачи.

    Args:
        task_description: Описание задачи от пользователя или из Archon

    Returns:
        list[str]: Список путей к модулям для чтения
    """
    task_lower = task_description.lower()
    modules = []

    # Module 01: Design Systems (CRITICAL - читается почти всегда для UI)
    if any(keyword in task_lower for keyword in [
        "дизайн", "design", "система", "system", "tailwind", "shadcn",
        "тема", "theme", "темізація", "theming", "компонент", "component",
        "ui", "кольор", "color", "card", "button", "карточка"
    ]):
        modules.append("modules/01_design_systems.md")

    # Module 02: Accessibility (HIGH)
    if any(keyword in task_lower for keyword in [
        "доступн", "accessib", "wcag", "a11y", "фокус", "focus",
        "screen reader", "aria", "клавіатур", "keyboard", "навігація", "navigation",
        "skip", "semantic"
    ]):
        modules.append("modules/02_accessibility.md")

    # Module 03: Animations (MEDIUM)
    if any(keyword in task_lower for keyword in [
        "анімація", "animation", "skeleton", "shimmer", "перехід", "transition",
        "loading", "hover", "interaction", "інтеракція", "button press",
        "glass", "gradient"
    ]):
        modules.append("modules/03_animations.md")

    # Module 04: Responsive Design (CRITICAL - читається для всіх адаптивних UI)
    if any(keyword in task_lower for keyword in [
        "responsive", "адаптив", "mobile", "мобільн", "breakpoint",
        "grid", "сітка", "container", "fluid", "touch"
    ]):
        modules.append("modules/04_responsive_design.md")

    # Module 05: Performance UI (HIGH)
    if any(keyword in task_lower for keyword in [
        "performance", "оптиміз", "продуктивн", "виртуал", "virtual",
        "lazy", "code splitting", "bundle", "web vitals", "lcp", "fid", "cls"
    ]):
        modules.append("modules/05_performance_ui.md")

    # Module 06: Domain Patterns (MEDIUM)
    if any(keyword in task_lower for keyword in [
        "e-commerce", "продукт", "product", "магазин", "shop", "saas",
        "dashboard", "аналітика", "analytics", "blog", "cms", "стаття",
        "article", "social", "пост", "post", "коментар", "comment"
    ]):
        modules.append("modules/06_domain_patterns.md")

    # Module 07: MCP Integration (MEDIUM)
    if any(keyword in task_lower for keyword in [
        "mcp", "puppeteer", "figma", "lighthouse", "тестування", "testing",
        "visual regression", "browserstack", "cross-browser", "audit"
    ]):
        modules.append("modules/07_mcp_integration.md")

    # FALLBACK: если ключевых слов не найдено, читать CRITICAL модули
    if not modules:
        modules = [
            "modules/01_design_systems.md",     # CRITICAL
            "modules/04_responsive_design.md"   # CRITICAL
        ]

    return modules
```

---

## 📊 МЕТРИКИ ОПТИМИЗАЦИИ ТОКЕНОВ (OLD vs NEW)

### OLD Workflow (читать ВСЕ модули):
- Модулей: 7
- Строк: ~2,741
- Токенов: ~4,100-4,300

### NEW Workflow (контекстное чтение):
- Модулей за задачу: 2-4
- Строк за задачу: ~800-1,800
- Токенов за задачу: ~1,200-2,700

### Экономия токенов:
- **Минимум:** 37% (4,300 → 2,700)
- **Максимум:** 72% (4,300 → 1,200)
- **Среднее:** 58% (4,300 → 1,800)

---

**Версия:** 1.0
**Дата создания:** 2025-10-20
**Автор:** Archon Implementation Engineer
**Проект:** AI Agent Factory - UI/UX Agent Refactoring (NEW workflow)

**Изменения:**
- ✅ Создана модульная навигация с приоритетами (CRITICAL/HIGH/MEDIUM)
- ✅ Добавлены Russian + English keywords для каждого модуля
- ✅ Добавлены технические триггеры для точного выбора
- ✅ Примеры типовых задач и комбинаций модулей
- ✅ Функция select_modules_for_task() с keyword mapping
- ✅ Метрики оптимизации токенов (OLD vs NEW)
