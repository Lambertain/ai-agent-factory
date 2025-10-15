# Module 04: Responsive Design System

## 🎯 Universal Responsive Layout Components

Универсальная система адаптивных компонентов для любых типов проектов с поддержкой mobile-first подхода, гибких breakpoints и адаптивной навигации.

### ResponsiveContainer - Universal Layout Container

Адаптивный контейнер с вариантами ширины для разных типов контента и layout требований.

```typescript
// Universal Layout Components
import { cn } from "@/lib/utils";

export function ResponsiveContainer({
  children,
  variant = 'default',
  className
}: {
  children: React.ReactNode;
  variant?: 'default' | 'narrow' | 'wide' | 'full';
  className?: string;
}) {
  const variants = {
    default: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
    narrow: 'max-w-4xl mx-auto px-4 sm:px-6 lg:px-8',
    wide: 'max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8',
    full: 'w-full px-4 sm:px-6 lg:px-8'
  };

  return (
    <div className={cn(variants[variant], className)}>
      {children}
    </div>
  );
}
```

**Возможности компонента:**
- **4 варианта ширины**: default (7xl), narrow (4xl), wide (2xl), full (100%)
- **Адаптивный padding**: 4px (mobile) → 6px (sm) → 8px (lg)
- **Центрирование**: автоматическое через mx-auto
- **Гибкость**: поддержка custom className для расширения

**Примеры использования:**

```typescript
// Основной контент (статьи, блоги)
<ResponsiveContainer variant="narrow">
  <Article />
</ResponsiveContainer>

// Dashboard (широкие таблицы, графики)
<ResponsiveContainer variant="wide">
  <Dashboard />
</ResponsiveContainer>

// Hero секции (на всю ширину)
<ResponsiveContainer variant="full">
  <HeroSection />
</ResponsiveContainer>
```

---

### ResponsiveGrid - Adaptive Grid System

Универсальная адаптивная сетка с гибкой конфигурацией колонок для каждого breakpoint.

```typescript
export function ResponsiveGrid({
  children,
  columns = { sm: 1, md: 2, lg: 3, xl: 4 },
  gap = 'md',
  className
}: {
  children: React.ReactNode;
  columns?: { sm?: number; md?: number; lg?: number; xl?: number; '2xl'?: number };
  gap?: 'sm' | 'md' | 'lg';
  className?: string;
}) {
  const gapVariants = {
    sm: 'gap-2 md:gap-3',
    md: 'gap-4 md:gap-6',
    lg: 'gap-6 md:gap-8'
  };

  const gridCols = `grid-cols-${columns.sm || 1}
    ${columns.md ? `md:grid-cols-${columns.md}` : ''}
    ${columns.lg ? `lg:grid-cols-${columns.lg}` : ''}
    ${columns.xl ? `xl:grid-cols-${columns.xl}` : ''}
    ${columns['2xl'] ? `2xl:grid-cols-${columns['2xl']}` : ''}`.replace(/\s+/g, ' ');

  return (
    <div className={cn('grid', gridCols, gapVariants[gap], className)}>
      {children}
    </div>
  );
}
```

**Возможности компонента:**
- **Гибкая конфигурация**: индивидуальные настройки для каждого breakpoint
- **Адаптивный gap**: sm (2-3), md (4-6), lg (6-8) с responsive scaling
- **Mobile-first**: по умолчанию 1 колонка на мобильных
- **5 breakpoints**: sm, md, lg, xl, 2xl для максимальной гибкости

**Примеры использования:**

```typescript
// Продуктовая сетка (E-commerce)
<ResponsiveGrid
  columns={{ sm: 1, md: 2, lg: 3, xl: 4 }}
  gap="md"
>
  {products.map(product => (
    <ProductCard key={product.id} product={product} />
  ))}
</ResponsiveGrid>

// Блог статьи (2 колонки макс)
<ResponsiveGrid
  columns={{ sm: 1, md: 2 }}
  gap="lg"
>
  {articles.map(article => (
    <ArticleCard key={article.id} article={article} />
  ))}
</ResponsiveGrid>

// Галерея изображений (до 6 колонок на wide screens)
<ResponsiveGrid
  columns={{ sm: 2, md: 3, lg: 4, xl: 5, '2xl': 6 }}
  gap="sm"
>
  {images.map(image => (
    <GalleryImage key={image.id} image={image} />
  ))}
</ResponsiveGrid>
```

---

### AdaptiveNavigation - Responsive Navigation Component

Универсальная навигация с адаптацией под мобильные устройства через выдвижное меню.

```typescript
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Menu } from 'lucide-react';

export function AdaptiveNavigation({
  items,
  logo,
  actions
}: {
  items: Array<{ label: string; href: string; icon?: React.ReactNode }>;
  logo?: React.ReactNode;
  actions?: React.ReactNode;
}) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <ResponsiveContainer>
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex-shrink-0">
            {logo}
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {items.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="text-sm font-medium transition-colors hover:text-primary"
              >
                {item.label}
              </a>
            ))}
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-2">
            {actions}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label="Toggle menu"
              aria-expanded={isMobileMenuOpen}
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t bg-background">
            <nav className="flex flex-col space-y-1 px-2 py-4">
              {items.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {item.icon}
                  {item.label}
                </a>
              ))}
            </nav>
          </div>
        )}
      </ResponsiveContainer>
    </header>
  );
}
```

**Возможности компонента:**
- **Sticky Header**: прилипает к верху при прокрутке
- **Backdrop Blur**: современный полупрозрачный эффект
- **Desktop Navigation**: горизонтальная навигация для md+ экранов
- **Mobile Menu**: выдвижное меню с анимацией для мобильных
- **Accessibility**: корректные ARIA attributes для screen readers
- **Auto Close**: мобильное меню закрывается при выборе пункта

**Примеры использования:**

```typescript
// SaaS приложение
<AdaptiveNavigation
  logo={<Logo />}
  items={[
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Analytics', href: '/analytics' },
    { label: 'Settings', href: '/settings' }
  ]}
  actions={
    <>
      <Button variant="ghost">Sign In</Button>
      <Button>Get Started</Button>
    </>
  }
/>

// E-commerce сайт с иконками
<AdaptiveNavigation
  logo={<StoreLogo />}
  items={[
    { label: 'Products', href: '/products', icon: <ShoppingBag /> },
    { label: 'Categories', href: '/categories', icon: <Grid /> },
    { label: 'Deals', href: '/deals', icon: <Tag /> }
  ]}
  actions={
    <>
      <CartButton />
      <UserMenu />
    </>
  }
/>
```

---

## 🎯 Best Practices для Responsive Design

### 1. Mobile-First Approach

**ВСЕГДА начинай с мобильной версии:**

```typescript
// ✅ ПРАВИЛЬНО - mobile-first
className="text-sm md:text-base lg:text-lg"

// ❌ НЕПРАВИЛЬНО - desktop-first
className="text-lg md:text-base sm:text-sm"
```

**Почему mobile-first:**
- Производительность: меньше CSS для мобильных устройств
- Прогрессивное улучшение: базовая функциональность работает везде
- Фокус на главном: мобильная версия заставляет приоритизировать контент

### 2. Breakpoint System Strategy

**Используй систему breakpoints логично:**

| Breakpoint | Размер | Устройства | Когда использовать |
|-----------|--------|-----------|-------------------|
| xs | 475px | Маленькие телефоны | Редко, только для edge cases |
| sm | 640px | Телефоны в портрете | Переход от mobile к tablet |
| md | 768px | Tablet портрет | Основной переход к desktop layout |
| lg | 1024px | Tablet landscape, ноутбуки | Расширение desktop функционала |
| xl | 1280px | Десктопы | Оптимизация для больших экранов |
| 2xl | 1400px | Wide desktops | Premium layouts |
| 3xl | 1920px | Ultra-wide | Максимальный контент |

### 3. Touch Target Sizes

**Минимальные размеры для touch интерфейсов:**

```typescript
// ✅ Touch-friendly кнопка
<Button className="h-11 px-4 min-w-[44px]">
  Click Me
</Button>

// ✅ Touch-friendly иконка кнопка
<Button
  size="icon"
  className="h-11 w-11" // минимум 44x44px
>
  <Icon className="h-5 w-5" />
</Button>
```

**WCAG рекомендации:**
- Минимум 44x44px для всех интерактивных элементов
- 48x48px рекомендуется для лучшего UX
- Spacing минимум 8px между touch targets

### 4. Responsive Typography Scale

**Адаптивная типографика через clamp:**

```css
/* Fluid Typography - плавное масштабирование */
.fluid-text {
  font-size: clamp(1rem, 0.5rem + 1.5vw, 2rem);
}

/* Tailwind custom utilities */
@layer utilities {
  .text-fluid-sm {
    font-size: clamp(0.875rem, 0.7rem + 0.5vw, 1rem);
  }

  .text-fluid-base {
    font-size: clamp(1rem, 0.85rem + 0.75vw, 1.25rem);
  }

  .text-fluid-lg {
    font-size: clamp(1.25rem, 1rem + 1vw, 1.875rem);
  }

  .text-fluid-xl {
    font-size: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
  }
}
```

### 5. Container Queries (Modern Approach)

**Используй container queries для компонентной адаптивности:**

```typescript
// Container-responsive компонент
export function AdaptiveCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="@container">
      <div className="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3 gap-4">
        {children}
      </div>
    </div>
  );
}
```

**Преимущества:**
- Компонент адаптируется к своему контейнеру, а не viewport
- Реюзабельность: работает в любом контексте
- Предсказуемость: поведение не зависит от положения в layout

### 6. Responsive Images Best Practices

**Оптимизация изображений для разных экранов:**

```typescript
// Responsive Image Component
export function ResponsiveImage({
  src,
  alt,
  sizes = "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
}: {
  src: string;
  alt: string;
  sizes?: string;
}) {
  return (
    <img
      src={src}
      alt={alt}
      sizes={sizes}
      className="w-full h-auto"
      loading="lazy"
      decoding="async"
    />
  );
}

// Picture element для art direction
export function ArtDirectedImage() {
  return (
    <picture>
      {/* Мобильная версия - портрет */}
      <source
        media="(max-width: 640px)"
        srcSet="/image-mobile.webp"
      />
      {/* Tablet - квадрат */}
      <source
        media="(max-width: 1024px)"
        srcSet="/image-tablet.webp"
      />
      {/* Desktop - landscape */}
      <img
        src="/image-desktop.webp"
        alt="Responsive image"
        className="w-full h-auto"
      />
    </picture>
  );
}
```

### 7. Responsive Testing Checklist

**ВСЕГДА тестируй на:**
- ✅ iPhone SE (375px) - минимальная ширина
- ✅ iPhone 12/13 (390px) - стандартный телефон
- ✅ iPad Mini (768px) - tablet портрет
- ✅ iPad Pro (1024px) - tablet landscape
- ✅ Desktop (1280px) - стандартный desktop
- ✅ Wide Desktop (1920px+) - большие экраны

**Тестируй также:**
- Ротацию экрана (portrait ↔ landscape)
- Zoom levels (100%, 125%, 150%, 200%)
- Font size adjustments (browser settings)
- Touch gestures (swipe, pinch, tap)

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
