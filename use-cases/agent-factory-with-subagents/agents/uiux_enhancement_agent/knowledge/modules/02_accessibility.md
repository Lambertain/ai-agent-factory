# Module 02: Accessibility (WCAG & a11y Patterns)

## 🎯 Universal Accessibility Patterns

Универсальные паттерны для обеспечения доступности (WCAG 2.1 AA) в любых типах приложений с поддержкой keyboard navigation, screen readers и focus management.

### Comprehensive Focus Management Hook

Хук для управления фокусом в модальных окнах, диалогах и других интерактивных компонентах с поддержкой trap focus и восстановления фокуса.

```typescript
// Comprehensive Focus Management
import { useEffect, useRef, useCallback } from 'react';

export function useFocusManagement(isActive: boolean, restoreFocus = true) {
  const containerRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<Element | null>(null);

  useEffect(() => {
    if (!isActive) return;

    // Store previously focused element
    previousActiveElement.current = document.activeElement;

    const container = containerRef.current;
    if (!container) return;

    // Focus the container or first focusable element
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"]), [contenteditable]'
    );

    const firstFocusable = focusableElements[0] as HTMLElement;
    const lastFocusable = focusableElements[focusableElements.length - 1] as HTMLElement;

    // Focus first element
    firstFocusable?.focus();

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (focusableElements.length === 1) {
        e.preventDefault();
        return;
      }

      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable?.focus();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable?.focus();
        }
      }
    };

    const handleEscapeKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        // Let parent components handle escape
        e.stopPropagation();
      }
    };

    container.addEventListener('keydown', handleTabKey);
    container.addEventListener('keydown', handleEscapeKey);

    return () => {
      container.removeEventListener('keydown', handleTabKey);
      container.removeEventListener('keydown', handleEscapeKey);

      // Restore focus to previously active element
      if (restoreFocus && previousActiveElement.current) {
        (previousActiveElement.current as HTMLElement).focus?.();
      }
    };
  }, [isActive, restoreFocus]);

  return containerRef;
}
```

**Возможности хука:**
- **Focus Trap**: Удерживает фокус внутри контейнера при нажатии Tab
- **Circular Navigation**: Tab на последнем элементе переходит на первый
- **Escape Handling**: Обрабатывает клавишу Escape для закрытия
- **Focus Restoration**: Возвращает фокус на предыдущий элемент при закрытии
- **Keyboard Support**: Полная поддержка клавиатурной навигации

---

### Screen Reader Announcements Hook

Хук для создания live region для screen reader announcements с поддержкой приоритетов (polite/assertive).

```typescript
// Screen Reader Announcements
export function useScreenReaderAnnouncements() {
  const announceRef = useRef<HTMLDivElement>(null);

  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (!announceRef.current) return;

    announceRef.current.setAttribute('aria-live', priority);
    announceRef.current.textContent = message;

    // Clear after announcement
    setTimeout(() => {
      if (announceRef.current) {
        announceRef.current.textContent = '';
      }
    }, 1000);
  }, []);

  const AnnouncementRegion = () => (
    <div
      ref={announceRef}
      className="sr-only"
      aria-live="polite"
      aria-atomic="true"
    />
  );

  return { announce, AnnouncementRegion };
}
```

**Использование:**
```typescript
function MyComponent() {
  const { announce, AnnouncementRegion } = useScreenReaderAnnouncements();

  const handleSubmit = () => {
    // ... submit logic
    announce('Form submitted successfully', 'polite');
  };

  const handleError = () => {
    // ... error handling
    announce('Error: Please fix validation errors', 'assertive');
  };

  return (
    <>
      <AnnouncementRegion />
      {/* Your component UI */}
    </>
  );
}
```

**Возможности хука:**
- **Live Region**: Автоматически объявляет изменения для screen readers
- **Priority Levels**:
  - `polite` - объявляет после завершения текущей речи
  - `assertive` - прерывает текущую речь для важных сообщений
- **Auto Cleanup**: Очищает announcement region после объявления
- **Invisible UI**: Использует `.sr-only` класс для скрытия от визуальных пользователей

---

### Responsive Skip Navigation Component

Компонент для skip navigation links, позволяющий пользователям клавиатуры быстро переходить к основному контенту.

```typescript
// Responsive Skip Navigation
export function SkipNavigation({ links }: { links: Array<{ href: string; label: string }> }) {
  return (
    <div className="sr-only focus-within:not-sr-only">
      <div className="fixed top-0 left-0 z-50 bg-background border border-border p-2 m-2 rounded-md shadow-lg">
        <p className="text-sm font-medium mb-2">Skip to:</p>
        <nav className="space-y-1">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="block text-sm underline hover:no-underline focus:ring-2 focus:ring-ring rounded px-1"
            >
              {link.label}
            </a>
          ))}
        </nav>
      </div>
    </div>
  );
}
```

**Использование:**
```typescript
function AppLayout() {
  return (
    <>
      <SkipNavigation
        links={[
          { href: '#main-content', label: 'Main Content' },
          { href: '#navigation', label: 'Navigation' },
          { href: '#footer', label: 'Footer' }
        ]}
      />

      <header id="navigation">
        {/* Navigation */}
      </header>

      <main id="main-content">
        {/* Main content */}
      </main>

      <footer id="footer">
        {/* Footer */}
      </footer>
    </>
  );
}
```

**Возможности компонента:**
- **Focus Visibility**: Появляется только при фокусе клавиатурой
- **Multiple Links**: Поддержка нескольких точек перехода
- **High Z-Index**: Отображается поверх всего контента
- **Keyboard Friendly**: Полная поддержка Tab навигации
- **WCAG Compliance**: Соответствует WCAG 2.1 AA требованиям

---

## 🎯 Best Practices для Accessibility

### 1. WCAG 2.1 AA Checklist
- ✅ **Цветовой контраст**: Минимум 4.5:1 для обычного текста, 3:1 для крупного
- ✅ **Keyboard Navigation**: Все интерактивные элементы доступны с клавиатуры
- ✅ **Screen Reader Support**: ARIA labels и roles для всех компонентов
- ✅ **Focus Indicators**: Видимые индикаторы фокуса для всех интерактивных элементов
- ✅ **Accessible Names**: Все элементы имеют понятные имена для screen readers
- ✅ **Color Independence**: Информация не передается только через цвет

### 2. Common Accessibility Patterns

**ARIA Labels:**
```typescript
<button aria-label="Close dialog">
  <X className="h-4 w-4" />
</button>
```

**ARIA Descriptions:**
```typescript
<input
  type="password"
  aria-describedby="password-requirements"
/>
<p id="password-requirements" className="text-sm text-muted-foreground">
  Password must be at least 8 characters
</p>
```

**ARIA Live Regions:**
```typescript
<div aria-live="polite" aria-atomic="true">
  {successMessage}
</div>
```

### 3. Focus Management Guidelines
- Управляй фокусом в модальных окнах и диалогах
- Восстанавливай фокус при закрытии overlays
- Используй trap focus для модальных контекстов
- Обеспечь circular navigation для списков элементов

### 4. Semantic HTML
- Используй корректные HTML теги (`<button>`, `<nav>`, `<main>`, etc.)
- Избегай `<div>` с `onClick` вместо `<button>`
- Используй `<label>` для всех форм инпутов
- Структурируй заголовки логично (h1 → h2 → h3)

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
