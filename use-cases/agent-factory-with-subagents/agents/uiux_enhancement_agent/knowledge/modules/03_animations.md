# Module 03: CSS Animation Library

## 🎨 Domain-Specific Animation Patterns

Универсальная библиотека CSS анимаций для любых типов проектов с поддержкой loading states, interaction feedback, transitions и micro-interactions.

### Universal Animation Library (globals.css)

Добавь эти utility классы в `globals.css` для использования в любых компонентах приложения.

```css
/* globals.css - Universal Animation Library */
@layer utilities {
  /* Loading States */
  .skeleton {
    @apply animate-pulse bg-gradient-to-r from-muted via-muted/50 to-muted;
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s ease-in-out infinite;
  }

  @keyframes skeleton-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }

  .shimmer {
    @apply relative overflow-hidden;
  }

  .shimmer::after {
    @apply absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent;
    content: '';
    animation: shimmer 2s infinite;
  }

  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

  /* Interaction Feedback */
  .button-press {
    @apply transition-transform duration-75 active:scale-95;
  }

  .card-hover {
    @apply transition-all duration-300 hover:scale-[1.02] hover:shadow-xl;
  }

  .gentle-bounce {
    animation: gentle-bounce 0.6s ease-out;
  }

  @keyframes gentle-bounce {
    0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
    40%, 43% { transform: translate3d(0,-8px,0); }
    70% { transform: translate3d(0,-4px,0); }
    90% { transform: translate3d(0,-2px,0); }
  }

  /* Page Transitions */
  .page-enter {
    animation: page-enter 0.3s ease-out;
  }

  @keyframes page-enter {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Status Indicators */
  .pulse-success {
    @apply animate-pulse bg-success/20 text-success-foreground;
  }

  .pulse-warning {
    @apply animate-pulse bg-warning/20 text-warning-foreground;
  }

  .pulse-error {
    @apply animate-pulse bg-destructive/20 text-destructive-foreground;
  }

  /* Scroll Enhancements */
  .smooth-scroll {
    scroll-behavior: smooth;
    scroll-padding-top: 5rem;
  }

  .scroll-fade {
    @apply relative;
  }

  .scroll-fade::before,
  .scroll-fade::after {
    @apply absolute left-0 right-0 h-4 pointer-events-none z-10;
    content: '';
  }

  .scroll-fade::before {
    @apply top-0 bg-gradient-to-b from-background to-transparent;
  }

  .scroll-fade::after {
    @apply bottom-0 bg-gradient-to-t from-background to-transparent;
  }

  /* Glass Morphism */
  .glass {
    @apply backdrop-blur-lg bg-background/80 border border-border/50;
  }

  .glass-strong {
    @apply backdrop-blur-xl bg-background/90 border border-border;
  }

  /* Text Effects */
  .gradient-text {
    @apply bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent;
    background-size: 200% auto;
    animation: gradient-text 3s ease-in-out infinite;
  }

  @keyframes gradient-text {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 200% center; }
  }
}
```

---

## 🎯 Примеры использования анимаций

### Loading States

**Skeleton Loader:**
```tsx
// Используй для placeholder контента во время загрузки
<div className="skeleton h-32 w-full rounded-md" />

// Skeleton для списка карточек
<div className="space-y-4">
  {[1, 2, 3].map(i => (
    <div key={i} className="skeleton h-24 w-full rounded-lg" />
  ))}
</div>
```

**Shimmer Effect:**
```tsx
// Добавь shimmer эффект к любому элементу
<div className="shimmer rounded-lg">
  <img src="/placeholder.jpg" alt="Loading..." />
</div>
```

### Interaction Feedback

**Button Press:**
```tsx
// Визуальный фидбэк при клике на кнопку
<Button className="button-press">
  Click Me
</Button>
```

**Card Hover:**
```tsx
// Hover эффект для интерактивных карточек
<Card className="card-hover cursor-pointer">
  <CardContent>
    {/* Card content */}
  </CardContent>
</Card>
```

**Gentle Bounce:**
```tsx
// Анимация подтверждения действия
<div className="gentle-bounce">
  <CheckCircle className="text-success" />
  <p>Action completed!</p>
</div>
```

### Page Transitions

**Page Enter Animation:**
```tsx
// Анимация появления страницы/секции
<main className="page-enter">
  <h1>Welcome to Dashboard</h1>
  {/* Page content */}
</main>
```

### Status Indicators

**Success State:**
```tsx
<div className="pulse-success p-4 rounded-md">
  ✅ Data saved successfully
</div>
```

**Warning State:**
```tsx
<div className="pulse-warning p-4 rounded-md">
  ⚠️ Please review your information
</div>
```

**Error State:**
```tsx
<div className="pulse-error p-4 rounded-md">
  ❌ An error occurred
</div>
```

### Scroll Enhancements

**Smooth Scrolling:**
```tsx
// Применить к html или body для плавной прокрутки
<html className="smooth-scroll">
  {/* ... */}
</html>

// Или к конкретному контейнеру
<div className="smooth-scroll h-96 overflow-auto">
  {/* Scrollable content */}
</div>
```

**Scroll Fade Effect:**
```tsx
// Fade градиент сверху и снизу для длинных списков
<div className="scroll-fade h-96 overflow-auto">
  {items.map(item => (
    <div key={item.id}>{item.content}</div>
  ))}
</div>
```

### Glass Morphism

**Glass Background:**
```tsx
// Полупрозрачный backdrop с blur
<div className="glass p-6 rounded-xl">
  <h2>Glassmorphism Card</h2>
  <p>Content over image background</p>
</div>
```

**Strong Glass:**
```tsx
// Более выраженный glass эффект
<nav className="glass-strong sticky top-0">
  <NavItems />
</nav>
```

### Text Effects

**Gradient Animated Text:**
```tsx
<h1 className="gradient-text text-4xl font-bold">
  Premium Feature
</h1>
```

---

## 🎨 Best Practices для анимаций

### 1. Performance Guidelines
- **Используй CSS animations** вместо JavaScript где возможно
- **Анимируй transform и opacity** - они наиболее производительны
- **Избегай анимации layout properties** (width, height, margin) - вызывают reflow
- **Используй will-change** для сложных анимаций, но осторожно

### 2. Accessibility для анимаций
- **Уважай prefers-reduced-motion**:
```css
@media (prefers-reduced-motion: reduce) {
  .skeleton,
  .shimmer,
  .gentle-bounce,
  .gradient-text {
    animation: none;
  }
}
```

### 3. Timing и Easing
- **Loading states**: 1-2s durations для skeleton/shimmer
- **Micro-interactions**: 75-200ms для button-press
- **Page transitions**: 300-400ms для smooth UX
- **Easing functions**: ease-out для входа, ease-in для выхода

### 4. Комбинирование анимаций
```tsx
// Пример: Card с hover и loading state
<Card className={cn(
  'card-hover',
  isLoading && 'shimmer'
)}>
  {isLoading ? (
    <div className="skeleton h-32 w-full" />
  ) : (
    <CardContent>{content}</CardContent>
  )}
</Card>
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
