# UI/UX Design & Enhancement Agent

**Универсальный агент для дизайна и улучшения пользовательских интерфейсов**

Агент специализируется на полном спектре UI/UX работы: дизайн с нуля, прототипирование, улучшение существующих интерфейсов, создание дизайн систем, wireframes, оптимизации CSS, работе с компонентными библиотеками и обеспечении accessibility. Адаптируется под любой проект и технологический стек.

## 🎯 Основные возможности

### 🎨 Дизайн с нуля
- **Interface Design** - создание полных интерфейсов для любого домена
- **Wireframes** - ASCII и high-fidelity wireframes с аннотациями
- **Design Systems** - создание полных дизайн систем с токенами
- **User Flow Prototyping** - интерактивные прототипы с переходами
- **Brand Adaptation** - адаптация под брендинг и требования
- **Multi-device** - дизайн для desktop, tablet и mobile

### ✨ Анализ и улучшение UI
- **Accessibility аудит** - проверка соответствия WCAG 2.1 стандартам
- **Performance анализ** - оптимизация рендеринга и bundle size
- **Responsive дизайн** - mobile-first подход и адаптивность
- **Cross-browser compatibility** - поддержка различных браузеров

### 🎨 Работа с дизайн системами
- **Автоматическое определение** используемой дизайн системы
- **Поддержка дизайн систем**: Material Design, Bootstrap, Tailwind UI, shadcn/ui, Chakra UI, Mantine, Ant Design
- **UI фреймворки**: React, Vue, Angular, Svelte, Solid, Lit
- **CSS технологии**: Tailwind CSS, Emotion, Styled Components, CSS Modules, SCSS
- **Accessibility уровни**: WCAG-A, WCAG-AA, WCAG-AAA, Section 508
- **Responsive стратегии**: mobile-first, desktop-first, adaptive, progressive
- **Темизация** - light/dark mode и кастомные темы

### 🛠️ CSS оптимизация
- **Tailwind CSS** - оптимизация классов, удаление дублей, custom utilities
- **Bundle size** - анализ влияния на размер сборки
- **Performance** - оптимизация CSS для быстрой загрузки
- **Consistency** - проверка соответствия дизайн системе

### 🔍 Компонентный анализ
- **Генерация вариантов** компонентов с использованием cva
- **Refactoring** - улучшение структуры и читаемости
- **Type safety** - TypeScript интеграция для компонентов
- **Documentation** - генерация примеров использования

## ⚡ MCP Integration

**НОВИНКА**: Агент поддерживает интеграцию с Model Context Protocol (MCP) серверами!

### Поддерживаемые MCP Серверы:
- **🎨 Shadcn MCP** - автоматическая генерация shadcn/ui компонентов
- **🤖 Puppeteer MCP** - скриншоты и visual testing
- **🧠 Context7 MCP** - долговременная память дизайн решений

### Преимущества MCP:
- **Автоматизация**: Генерация компонентов одной командой
- **Качество**: Автоматические accessibility и performance проверки
- **Память**: Сохранение и переиспользование успешных дизайн решений
- **Тестирование**: Visual regression testing через браузер

📖 **Подробнее**: [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)

## 🚀 Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Проверка MCP интеграции

```bash
python simple_test.py
```

**Ожидаемый результат:**
```
MCP INTEGRATION TESTING
============================================================
TESTING MCP DEPENDENCIES
==================================================
Created: UIUXEnhancementDependencies
MCP Enabled: True
MCP Servers: ['shadcn', 'puppeteer', 'context7']
...
RESULTS: 2/2 tests passed
SUCCESS: All tests passed!
```

### Настройка переменных окружения

Скопируйте `.env.example` в `.env` и настройте:

```bash
cp .env.example .env
```

Заполните обязательные переменные:
- `LLM_API_KEY` - API ключ для Qwen/Alibaba Cloud
- `GEMINI_API_KEY` - API ключ для Google Gemini

### Базовое использование

```python
from uiux_enhancement_agent import run_uiux_enhancement_sync

# Анализ компонента
result = run_uiux_enhancement_sync(
    task="Улучши accessibility этого компонента",
    component_code="""
    <button className="bg-blue-500 text-white px-4 py-2 rounded">
      Click me
    </button>
    """,
    requirements={
        "accessibility_level": "WCAG 2.1 AA",
        "design_system": "tailwind",
        "mobile_first": True
    }
)

print(result)
```

### Настройка под проект

```python
from uiux_enhancement_agent import AgentDependencies

# Настройка для конкретного проекта
deps = AgentDependencies(
    project_name="MyApp",
    design_system="shadcn/ui",
    css_framework="tailwind",
    project_specific_colors={
        "brand-primary": "#3B82F6",
        "brand-secondary": "#10B981"
    },
    knowledge_tags=["myapp", "ecommerce", "b2b"],
    archon_project_id="your-project-id"
)
```

## 🎨 Поддерживаемые технологии

### Дизайн системы
- **Material Design** - Google Material Design principles
- **Bootstrap** - Popular CSS framework
- **Tailwind UI** - Official Tailwind CSS components
- **shadcn/ui** - Radix UI + Tailwind CSS
- **Chakra UI** - Simple, Modular, Accessible
- **Mantine** - Full-featured React library
- **Ant Design** - Enterprise-class UI design language
- **Custom** - Любые кастомные дизайн системы

### CSS технологии
- **Tailwind CSS** - Utility-first CSS framework
- **Emotion** - CSS-in-JS library
- **Styled Components** - CSS-in-JS для React/Vue
- **CSS Modules** - Локально ограниченный CSS
- **SCSS** - Enhanced CSS with variables and mixins

### UI фреймворки
- **React** - компоненты, hooks, functional/class-based
- **Vue** - Vue 2/3, Composition API, SFC
- **Angular** - TypeScript components, standalone, signals
- **Svelte** - Reactive components, SvelteKit
- **Solid** - Fine-grained reactivity
- **Lit** - Lightweight web components

## 🔧 Расширенная конфигурация

### Accessibility настройки

```python
accessibility_config = {
    "wcag_level": "AA",  # A, AA, AAA
    "tools": ["axe-core", "lighthouse", "wave"],
    "auto_focus": True,
    "keyboard_nav": True,
    "screen_reader": True,
    "high_contrast": True
}
```

### Performance бюджет

```python
performance_budget = {
    "first_contentful_paint": 1500,  # ms
    "cumulative_layout_shift": 0.1,
    "total_blocking_time": 300,
    "bundle_size_limit": 100  # KB
}
```

### Responsive breakpoints

```python
breakpoints = {
    "xs": "475px",
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
}
```

## 📊 Доступные инструменты

### `analyze_ui_accessibility`
Детальный анализ accessibility с проверкой WCAG критериев.

```python
result = await analyze_ui_accessibility(
    ctx,
    component_code="<button>Click</button>",
    component_type="button"
)
```

### `optimize_tailwind_classes`
Оптимизация Tailwind CSS классов, удаление дублей, custom utilities.

```python
result = await optimize_tailwind_classes(
    ctx,
    component_code="<div className='p-4 p-4 bg-white bg-white'>",
    optimization_level="aggressive"
)
```

### `enhance_shadcn_component`
Улучшение shadcn/ui компонентов с добавлением variants и proper patterns.

```python
result = await enhance_shadcn_component(
    ctx,
    component_code="<Button>Click</Button>",
    enhancement_type="accessibility"
)
```

### `generate_component_variants`
Генерация type-safe вариантов компонента с использованием cva.

```python
result = await generate_component_variants(
    ctx,
    base_component="<Button>Click</Button>",
    variant_types=["size", "style", "state"]
)
```

### `validate_design_system`
Проверка соответствия компонента дизайн системе проекта.

```python
result = await validate_design_system(
    ctx,
    component_code="<Button variant='primary'>",
    design_tokens={"primary": "#3B82F6"}
)
```

## 💡 Рекомендуемые MCP серверы

Для максимальной эффективности рекомендуется установить специализированные MCP серверы:

### 🎨 Shadcn MCP Server (высокий приоритет)
```bash
npm install @modelcontextprotocol/server-shadcn
```

### ⚡ Tailwind CSS MCP Server
```bash
npm install @modelcontextprotocol/server-tailwind
```

### 🎯 Figma MCP Server (опционально)
```bash
npm install @modelcontextprotocol/server-figma
```

### 📊 Lighthouse MCP Server (для аудита)
```bash
npm install @modelcontextprotocol/server-lighthouse
```

## 🔄 Мультиагентные паттерны

Агент реализует 4 ключевых паттерна работы:

### 1. **Reflection (Рефлексия)**
- Критический анализ результата после каждой задачи
- Выявление недостатков и возможностей улучшения
- Создание улучшенной версии решения

### 2. **Tool Use (Использование инструментов)**
- Автоматический выбор подходящих инструментов
- RAG поиск в базе знаний
- Интеграция с внешними API и сервисами

### 3. **Planning (Планирование)**
- Разбивка сложных задач на этапы
- Создание плана выполнения
- Адаптация плана по ходу работы

### 4. **Multi-Agent Collaboration**
- Взаимодействие с другими агентами
- Передача результатов для улучшения
- Итеративное сотрудничество

## 🌐 Конфигурации для разных доменов

### E-commerce проекты
```python
from uiux_enhancement_agent.examples import get_ecommerce_uiux_dependencies

# Настройка для интернет-магазина
config = get_ecommerce_uiux_dependencies()
config.project_name = "My Store"
config.enable_product_cards = True
config.enable_shopping_cart = True
config.enable_quick_view = True
```

### SaaS платформы
```python
from uiux_enhancement_agent.examples import get_saas_uiux_dependencies

# Настройка для B2B SaaS
config = get_saas_uiux_dependencies()
config.project_name = "Analytics Platform"
config.enable_dashboard = True
config.enable_user_management = True
```

### Enterprise корпоративные системы
```python
from uiux_enhancement_agent.examples import get_enterprise_uiux_dependencies

# Настройка для корпоративной платформы
config = get_enterprise_uiux_dependencies()
config.project_name = "Corporate Portal"
config.accessibility_level = "wcag-aaa"
config.enable_role_based_ui = True
config.enable_audit_logging = True
```

### CRM системы
```python
from uiux_enhancement_agent.examples import get_crm_uiux_dependencies

# Настройка для CRM
config = get_crm_uiux_dependencies()
config.project_name = "Sales CRM"
config.enable_contact_management = True
config.enable_opportunity_pipeline = True
config.enable_activity_timeline = True
```

### Социальные платформы
```python
from uiux_enhancement_agent.examples import get_social_uiux_dependencies

# Настройка для социальной сети
config = get_social_uiux_dependencies()
config.project_name = "Community Platform"
config.enable_feed_design = True
config.enable_real_time_chat = True
```

### Блоги и контент-платформы
```python
from uiux_enhancement_agent.examples import get_blog_uiux_dependencies

# Настройка для блога
config = get_blog_uiux_dependencies()
config.project_name = "Tech Blog"
config.enable_reading_optimization = True
config.enable_content_sharing = True
```

## 📈 Примеры использования

### Анализ accessibility

```python
accessibility_result = run_uiux_enhancement_sync(
    task="Проведи полный accessibility аудит этой формы",
    component_code="""
    <form>
      <input type="email" placeholder="Email">
      <input type="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
    """,
    requirements={
        "accessibility_level": "WCAG 2.1 AA",
        "check_keyboard_nav": True,
        "check_screen_reader": True
    }
)
```

### Оптимизация Tailwind

```python
tailwind_result = run_uiux_enhancement_sync(
    task="Оптимизируй Tailwind классы и предложи custom utilities",
    component_code="""
    <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300">
      <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
        Duplicate styles
      </div>
    </div>
    """,
    requirements={
        "optimization_level": "aggressive",
        "suggest_custom_utilities": True
    }
)
```

### Генерация вариантов компонента

```python
variants_result = run_uiux_enhancement_sync(
    task="Создай type-safe варианты для этого Button компонента",
    component_code="""
    <button className="px-4 py-2 rounded font-medium">
      Click me
    </button>
    """,
    requirements={
        "variant_types": ["size", "style", "state"],
        "use_cva": True,
        "typescript_support": True
    }
)
```

## 🛡️ Accessibility Features

- **WCAG 2.1 AA/AAA compliance** - полная проверка стандартов
- **Keyboard navigation** - проверка доступности с клавиатуры
- **Screen reader support** - совместимость с программами чтения экрана
- **Color contrast** - проверка контрастности цветов
- **Focus management** - правильное управление фокусом
- **ARIA attributes** - корректные ARIA метки и роли

## 🚀 Performance Optimization

- **Bundle size analysis** - анализ влияния на размер сборки
- **CSS optimization** - оптимизация CSS для быстрой загрузки
- **Lazy loading** - ленивая загрузка компонентов
- **Tree shaking** - удаление неиспользуемого кода
- **Critical CSS** - выделение критического CSS

## 🔧 Настройка интеграций

### Archon RAG Integration

```python
# Поиск в базе знаний
knowledge_result = await search_uiux_knowledge(
    ctx,
    query="shadcn button accessibility patterns",
    match_count=5
)
```

### Figma Integration

```python
# Настройка Figma интеграции
settings = UIUXAgentSettings(
    figma_api_key="your_figma_token",
    figma_integration_enabled=True
)
```

### Storybook Integration

```python
# Настройка Storybook
settings = UIUXAgentSettings(
    storybook_integration=True,
    storybook_base_url="http://localhost:6006"
)
```

## 📚 Дополнительные ресурсы

- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [MCP Documentation](https://docs.claude.com/en/docs/claude-code/mcp)

## 🤝 Участие в разработке

Агент постоянно развивается. Предложения по улучшению и баг-репорты приветствуются!

## 📄 Лицензия

MIT License - используйте в любых проектах.

---

**UI/UX Enhancement Agent** - делаем интерфейсы лучше, доступнее и производительнее! 🎨✨