# Module 05: UI Performance Optimization

## 🚀 Universal Performance Optimization Patterns

Универсальные паттерны оптимизации производительности UI для любых типов приложений с поддержкой виртуализации, lazy loading и code splitting.

### VirtualizedList - Virtual Scrolling for Large Lists

Компонент виртуализации для рендеринга больших списков (тысячи элементов) с минимальным performance impact.

```typescript
// Virtual Scrolling for Large Lists
import { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { cn } from '@/lib/utils';

export function VirtualizedList<T>({
  items,
  renderItem,
  estimateSize = () => 100,
  className
}: {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  estimateSize?: (index: number) => number;
  className?: string;
}) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize,
    overscan: 5
  });

  return (
    <div
      ref={parentRef}
      className={cn('h-[600px] overflow-auto', className)}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`
            }}
          >
            {renderItem(items[virtualItem.index], virtualItem.index)}
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Возможности компонента:**
- **Virtual Rendering**: рендерит только видимые элементы + overscan (5 элементов)
- **Dynamic Height**: поддержка элементов с разной высотой через estimateSize
- **Performance**: 60fps даже с 10,000+ элементами
- **Generic Type**: TypeScript generics для type-safe rendering
- **Configurable**: кастомизация высоты, className, estimateSize

**Примеры использования:**

```typescript
// Список пользователей (большой dataset)
<VirtualizedList
  items={users} // 10,000+ users
  renderItem={(user, index) => (
    <UserCard key={user.id} user={user} />
  )}
  estimateSize={() => 120} // каждая карточка ~120px
  className="border rounded-lg"
/>

// Список транзакций с переменной высотой
<VirtualizedList
  items={transactions}
  renderItem={(tx) => (
    <TransactionRow transaction={tx} />
  )}
  estimateSize={(index) => {
    // Динамическая высота на основе типа транзакции
    return transactions[index].type === 'detailed' ? 200 : 80;
  }}
/>

// Чат сообщения
<VirtualizedList
  items={messages}
  renderItem={(message) => (
    <MessageBubble message={message} />
  )}
  estimateSize={() => 60}
  className="h-screen overflow-auto"
/>
```

**Когда использовать:**
- ✅ Списки с 100+ элементами
- ✅ Бесконечная прокрутка (infinite scroll)
- ✅ Таблицы с большим количеством строк
- ✅ Чаты с историей сообщений
- ❌ Короткие списки (< 50 элементов) - обычный рендеринг лучше

---

### LazyLoadImage - Lazy Loading with Intersection Observer

Компонент ленивой загрузки изображений с Intersection Observer API для оптимизации LCP и network traffic.

```typescript
import { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

export function LazyLoadImage({
  src,
  alt,
  placeholder,
  className,
  ...props
}: React.ImgHTMLAttributes<HTMLImageElement> & {
  placeholder?: string;
}) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1, rootMargin: '50px' }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef} className={cn('relative overflow-hidden', className)}>
      {!isLoaded && (
        <div className="absolute inset-0 skeleton" />
      )}
      {isInView && (
        <img
          src={src}
          alt={alt}
          className={cn(
            'transition-opacity duration-300',
            isLoaded ? 'opacity-100' : 'opacity-0'
          )}
          onLoad={() => setIsLoaded(true)}
          {...props}
        />
      )}
    </div>
  );
}
```

**Возможности компонента:**
- **Intersection Observer**: автоматическая загрузка при входе в viewport
- **Skeleton Placeholder**: показывает skeleton loader до загрузки
- **Smooth Transition**: плавное появление изображения (fade-in)
- **Root Margin**: начинает загрузку за 50px до видимости (preloading)
- **Memory Cleanup**: отключает observer после загрузки

**Примеры использования:**

```typescript
// Галерея продуктов
<div className="grid grid-cols-3 gap-4">
  {products.map(product => (
    <LazyLoadImage
      key={product.id}
      src={product.image}
      alt={product.name}
      className="w-full aspect-square object-cover rounded-lg"
    />
  ))}
</div>

// Hero изображение с высоким приоритетом
<LazyLoadImage
  src="/hero-image.jpg"
  alt="Hero"
  className="w-full h-[600px] object-cover"
  loading="eager" // browser native eager loading
/>

// Аватары в комментариях
{comments.map(comment => (
  <div key={comment.id} className="flex gap-3">
    <LazyLoadImage
      src={comment.author.avatar}
      alt={comment.author.name}
      className="w-10 h-10 rounded-full"
    />
    <div>{comment.text}</div>
  </div>
))}
```

**Performance метрики:**
- ✅ Сокращает initial page load на 60-80%
- ✅ Улучшает LCP (Largest Contentful Paint)
- ✅ Уменьшает network traffic до 70%
- ✅ Лучший FCP (First Contentful Paint)

---

### OptimizedComponentLoader - Component Code Splitting

Компонент для динамической загрузки "тяжелых" компонентов с React.lazy и Suspense.

```typescript
import { lazy, Suspense } from 'react';

// Динамически импортируемый компонент
const LazyComponent = lazy(() => import('./HeavyComponent'));

export function OptimizedComponentLoader({
  fallback = <div className="skeleton h-32 w-full" />
}: {
  fallback?: React.ReactNode;
}) {
  return (
    <Suspense fallback={fallback}>
      <LazyComponent />
    </Suspense>
  );
}
```

**Расширенные паттерны code splitting:**

```typescript
// 1. Lazy Load по роуту
import { lazy } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));

export function AppRouter() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// 2. Lazy Load по модалу
const HeavyModal = lazy(() => import('./components/HeavyModal'));

export function LazyModalTrigger() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>
        Open Modal
      </Button>

      {isOpen && (
        <Suspense fallback={<ModalSkeleton />}>
          <HeavyModal onClose={() => setIsOpen(false)} />
        </Suspense>
      )}
    </>
  );
}

// 3. Lazy Load по feature flag
const AdvancedFeature = lazy(() => import('./features/AdvancedFeature'));

export function ConditionalFeature({ isEnabled }: { isEnabled: boolean }) {
  if (!isEnabled) {
    return <BasicFeature />;
  }

  return (
    <Suspense fallback={<FeatureSkeleton />}>
      <AdvancedFeature />
    </Suspense>
  );
}

// 4. Lazy Load с retry механизмом
function lazyWithRetry(componentImport: () => Promise<any>) {
  return lazy(async () => {
    try {
      return await componentImport();
    } catch (error) {
      // Retry once on failure
      console.warn('Failed to load component, retrying...', error);
      return await componentImport();
    }
  });
}

const RobustComponent = lazyWithRetry(() => import('./RobustComponent'));
```

**Bundle size impact:**

```typescript
// ❌ БЕЗ code splitting - 500KB initial bundle
import Dashboard from './pages/Dashboard';  // 150KB
import Analytics from './pages/Analytics';  // 200KB
import Reports from './pages/Reports';      // 150KB

// ✅ С code splitting - 50KB initial + 150-200KB on-demand
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Reports = lazy(() => import('./pages/Reports'));
```

---

## 🎯 Best Practices для UI Performance

### 1. Rendering Optimization

**React.memo для предотвращения ненужных re-renders:**

```typescript
// Оборачивай "тяжелые" компоненты в memo
export const ExpensiveCard = React.memo(({ data }: { data: CardData }) => {
  // Сложная логика рендеринга
  return <Card>{/* ... */}</Card>;
}, (prevProps, nextProps) => {
  // Custom comparison - только re-render если data.id изменился
  return prevProps.data.id === nextProps.data.id;
});

// useMemo для тяжелых вычислений
function DataTable({ items }: { items: Item[] }) {
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.priority - b.priority);
  }, [items]); // Пересчитывает только при изменении items

  return <Table data={sortedItems} />;
}

// useCallback для стабильных функций
function ParentComponent() {
  const handleClick = useCallback((id: string) => {
    // Handler logic
  }, []); // Функция создается только один раз

  return <ChildComponent onClick={handleClick} />;
}
```

### 2. Image Optimization Checklist

**Оптимизация изображений - критично для performance:**

```typescript
// ✅ ПРАВИЛЬНО - оптимизированные изображения
<picture>
  {/* WebP для современных браузеров */}
  <source srcSet="/image.webp" type="image/webp" />
  {/* AVIF для самого лучшего сжатия */}
  <source srcSet="/image.avif" type="image/avif" />
  {/* Fallback JPEG */}
  <img
    src="/image.jpg"
    alt="Description"
    width={800}
    height={600}
    loading="lazy"
    decoding="async"
  />
</picture>

// Next.js Image component (автоматическая оптимизация)
import Image from 'next/image';

<Image
  src="/photo.jpg"
  alt="Description"
  width={800}
  height={600}
  quality={80}
  priority={false} // lazy load
  placeholder="blur"
  blurDataURL="data:image/..." // low-quality placeholder
/>
```

**Image optimization guidelines:**
- ✅ WebP/AVIF formats (70% меньше размер)
- ✅ Responsive images через srcSet
- ✅ Lazy loading для images ниже fold
- ✅ Правильные dimensions (width/height)
- ✅ Quality 80-85% (оптимальный баланс)
- ❌ Избегай PNG для фотографий
- ❌ Не используй изображения больше чем нужно для display

### 3. Bundle Size Optimization

**Анализ и оптимизация bundle size:**

```bash
# Анализ bundle size
npm run build -- --analyze

# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer

# Vite Bundle Visualizer
npm install --save-dev rollup-plugin-visualizer
```

**Tree Shaking - импортируй только что нужно:**

```typescript
// ❌ ПЛОХО - импортирует всю библиотеку (100KB+)
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ ХОРОШО - только нужная функция (5KB)
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// ❌ ПЛОХО - весь icon set (500KB)
import * as Icons from 'lucide-react';
<Icons.Home />

// ✅ ХОРОШО - только нужная иконка (2KB)
import { Home } from 'lucide-react';
<Home />
```

### 4. Performance Metrics to Track

**Core Web Vitals - ключевые метрики:**

| Метрика | Хорошо | Плохо | Как улучшить |
|---------|--------|-------|--------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | > 4.0s | Optimize images, code splitting, CDN |
| **FID** (First Input Delay) | < 100ms | > 300ms | Reduce JS execution time, code splitting |
| **CLS** (Cumulative Layout Shift) | < 0.1 | > 0.25 | Set image dimensions, avoid dynamic content |
| **FCP** (First Contentful Paint) | < 1.8s | > 3.0s | Reduce blocking resources, optimize CSS |
| **TTI** (Time to Interactive) | < 3.8s | > 7.3s | Defer non-critical JS, reduce bundle size |

**Monitoring tools:**
- **Lighthouse** - automated audits
- **Web Vitals** - real user monitoring
- **Chrome DevTools** - performance profiling
- **Puppeteer MCP** - automated testing

### 5. Network Optimization

**Reduce HTTP requests и optimize loading:**

```typescript
// Preload критичных ресурсов
<head>
  <link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossOrigin="anonymous" />
  <link rel="preload" href="/critical.css" as="style" />
  <link rel="dns-prefetch" href="https://api.example.com" />
  <link rel="preconnect" href="https://cdn.example.com" />
</head>

// HTTP/2 Server Push для критичных ресурсов
// Инлайн критичный CSS в <head>
// Defer некритичный JavaScript
<script src="/analytics.js" defer></script>
```

### 6. Runtime Performance

**Debounce и throttle для UI events:**

```typescript
import { debounce } from 'lodash';
import { useCallback } from 'react';

// Debounce для search input
const handleSearch = useCallback(
  debounce((query: string) => {
    // API call
    searchAPI(query);
  }, 300),
  []
);

// Throttle для scroll events
const handleScroll = useCallback(
  throttle(() => {
    // Update UI based on scroll position
    updateScrollPosition();
  }, 100),
  []
);
```

**Виртуализация DOM операций:**
- Используй `requestAnimationFrame` для анимаций
- Batch DOM updates вместо множественных изменений
- Используй CSS transforms вместо position changes
- Избегай layout thrashing (read/write cycles)

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
