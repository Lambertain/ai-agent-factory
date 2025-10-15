# Module 06: Domain-Specific UI Patterns

## 🎯 Universal UI Components для різних доменів

Універсальні UI паттерни з реальними прикладами коду для E-commerce, SaaS, Blog/CMS та Social Media додатків. Всі компоненти побудовані на базі shadcn/ui та Tailwind CSS.

### E-commerce UI Components

Компоненти для інтернет-магазинів з підтримкою товарних карточок, рейтингів, знижок та швидкого перегляду.

```typescript
// Product Card for E-commerce
import { UniversalCard } from './UniversalCard';

export function ProductCard({
  product,
  onAddToCart,
  onQuickView
}: {
  product: {
    id: string;
    name: string;
    price: number;
    originalPrice?: number;
    image: string;
    rating: number;
    reviewCount: number;
    badges?: string[];
  };
  onAddToCart: (productId: string) => void;
  onQuickView: (productId: string) => void;
}) {
  const discount = product.originalPrice
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0;

  return (
    <UniversalCard
      item={{
        title: product.name,
        image: product.image,
        tags: product.badges,
        metadata: {
          rating: `${product.rating} ⭐ (${product.reviewCount} reviews)`,
          price: `$${product.price}${product.originalPrice ? ` (${discount}% off)` : ''}`
        },
        actions: [
          { label: 'Quick View', variant: 'outline', onClick: () => onQuickView(product.id) },
          { label: 'Add to Cart', variant: 'default', onClick: () => onAddToCart(product.id) }
        ]
      }}
      variant="interactive"
    />
  );
}
```

**Можливості компонента:**
- **Розрахунок знижки**: автоматичне обчислення відсотка знижки при наявності originalPrice
- **Рейтинг з відгуками**: відображення зіркового рейтингу та кількості відгуків
- **Бейджі**: відображення міток (New, Sale, Limited)
- **Швидкі дії**: Quick View та Add to Cart в одній карточці
- **Інтерактивність**: hover ефект через variant="interactive"

**Приклади використання:**

```typescript
// Сітка продуктів
<ResponsiveGrid
  columns={{ sm: 1, md: 2, lg: 3, xl: 4 }}
  gap="md"
>
  {products.map(product => (
    <ProductCard
      key={product.id}
      product={product}
      onAddToCart={(id) => addToCart(id)}
      onQuickView={(id) => openQuickView(id)}
    />
  ))}
</ResponsiveGrid>

// Акційні товари
{saleProducts.map(product => (
  <ProductCard
    key={product.id}
    product={{
      ...product,
      badges: ['Sale', 'Limited Offer']
    }}
    onAddToCart={handleAddToCart}
    onQuickView={handleQuickView}
  />
))}
```

**E-commerce Best Practices:**
- ✅ Чіткі ціни з виділенням знижок
- ✅ Візуальне виділення rating через іконки
- ✅ Швидкий доступ до додавання в кошик
- ✅ Quick View для перегляду без переходу
- ✅ Responsive layout для всіх пристроїв

---

### SaaS Dashboard UI

Компоненти для SaaS панелей управління з аналітикою, метриками та візуалізацією даних.

```typescript
// Analytics Widget for SaaS
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';

export function AnalyticsWidget({
  title,
  value,
  change,
  period = '30 days',
  format = 'number'
}: {
  title: string;
  value: number;
  change: number;
  period?: string;
  format?: 'number' | 'currency' | 'percentage';
}) {
  const formatValue = (val: number) => {
    switch (format) {
      case 'currency': return `$${val.toLocaleString()}`;
      case 'percentage': return `${val}%`;
      default: return val.toLocaleString();
    }
  };

  const isPositive = change >= 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <TrendingUp className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatValue(value)}</div>
        <p className="text-xs text-muted-foreground">
          <span className={cn(
            'inline-flex items-center',
            isPositive ? 'text-success' : 'text-destructive'
          )}>
            {isPositive ? '↗' : '↘'} {Math.abs(change)}%
          </span>
          {' '}from last {period}
        </p>
      </CardContent>
    </Card>
  );
}
```

**Можливості компонента:**
- **Гнучке форматування**: currency, percentage, number
- **Автоматичне визначення тренду**: позитивний (зелений) або негативний (червоний)
- **Кастомізований період**: "30 days", "last week", "this month"
- **Іконки індикаторів**: стрілки вгору/вниз для візуалізації тренду
- **Локалізація чисел**: toLocaleString() для правильного відображення

**Приклади використання:**

```typescript
// SaaS Dashboard метрики
<ResponsiveGrid columns={{ sm: 1, md: 2, lg: 4 }} gap="md">
  <AnalyticsWidget
    title="Total Revenue"
    value={45231}
    change={12.5}
    format="currency"
    period="30 days"
  />

  <AnalyticsWidget
    title="Active Users"
    value={2350}
    change={-2.1}
    format="number"
    period="this week"
  />

  <AnalyticsWidget
    title="Conversion Rate"
    value={3.8}
    change={0.5}
    format="percentage"
    period="last month"
  />

  <AnalyticsWidget
    title="Churn Rate"
    value={1.2}
    change={-0.3}
    format="percentage"
    period="this quarter"
  />
</ResponsiveGrid>
```

**SaaS Best Practices:**
- ✅ Чіткі метрики з великими числами
- ✅ Контекст через порівняння з попереднім періодом
- ✅ Колірне кодування трендів (success/destructive)
- ✅ Компактний layout для multiple widgets
- ✅ Іконки для швидкого розпізнавання типу метрики

---

### Blog/CMS UI Components

Компоненти для блогів та CMS систем з підтримкою статей, авторів та категорій.

```typescript
// Article Card for Blogs
import { UniversalCard } from './UniversalCard';

export function ArticleCard({
  article,
  onRead
}: {
  article: {
    id: string;
    title: string;
    excerpt: string;
    author: string;
    publishedAt: Date;
    readTime: number;
    category: string;
    tags: string[];
    image?: string;
  };
  onRead: (articleId: string) => void;
}) {
  return (
    <UniversalCard
      item={{
        title: article.title,
        description: article.excerpt,
        image: article.image,
        tags: [article.category, ...article.tags.slice(0, 2)],
        metadata: {
          author: article.author,
          published: article.publishedAt.toLocaleDateString(),
          'read time': `${article.readTime} min`
        },
        actions: [
          { label: 'Read Article', variant: 'default', onClick: () => onRead(article.id) }
        ]
      }}
      variant="interactive"
    />
  );
}
```

**Можливості компонента:**
- **Excerpt preview**: короткий опис статті (line-clamp-3)
- **Мета-інформація**: автор, дата публікації, час читання
- **Категорії та теги**: візуальне групування контенту
- **Адаптивне зображення**: опціональне featured image
- **CTA кнопка**: чітка дія "Read Article"

**Приклади використання:**

```typescript
// Список статей блогу
<ResponsiveGrid columns={{ sm: 1, md: 2 }} gap="lg">
  {articles.map(article => (
    <ArticleCard
      key={article.id}
      article={article}
      onRead={(id) => router.push(`/blog/${id}`)}
    />
  ))}
</ResponsiveGrid>

// Featured articles
<div className="space-y-6">
  {featuredArticles.map(article => (
    <ArticleCard
      key={article.id}
      article={{
        ...article,
        tags: ['Featured', ...article.tags]
      }}
      onRead={handleReadArticle}
    />
  ))}
</div>
```

**Blog/CMS Best Practices:**
- ✅ Чіткий excerpt (2-3 рядки максимум)
- ✅ Відображення автора для довіри
- ✅ Read time для UX planning
- ✅ Категорії для швидкої навігації
- ✅ Featured image для візуального залучення

---

### Social Media UI Components

Компоненти для соціальних медіа з підтримкою постів, лайків, коментарів та шерінгу.

```typescript
// Post Card for Social Platforms
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Heart, MessageCircle, Share2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export function PostCard({
  post,
  onLike,
  onComment,
  onShare
}: {
  post: {
    id: string;
    author: { name: string; avatar: string; username: string };
    content: string;
    image?: string;
    likes: number;
    comments: number;
    shares: number;
    timestamp: Date;
    isLiked: boolean;
  };
  onLike: (postId: string) => void;
  onComment: (postId: string) => void;
  onShare: (postId: string) => void;
}) {
  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center space-y-0 space-x-4 pb-2">
        <img
          src={post.author.avatar}
          alt={post.author.name}
          className="w-10 h-10 rounded-full"
        />
        <div className="flex-1">
          <p className="font-semibold text-sm">{post.author.name}</p>
          <p className="text-xs text-muted-foreground">@{post.author.username}</p>
        </div>
        <span className="text-xs text-muted-foreground">
          {post.timestamp.toLocaleDateString()}
        </span>
      </CardHeader>

      <CardContent className="pt-0">
        <p className="text-sm mb-3">{post.content}</p>
        {post.image && (
          <img
            src={post.image}
            alt="Post content"
            className="w-full rounded-md mb-3"
          />
        )}

        <div className="flex items-center justify-between pt-2 border-t">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onLike(post.id)}
            className={cn(post.isLiked && 'text-red-500')}
          >
            <Heart className="w-4 h-4 mr-1" />
            {post.likes}
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => onComment(post.id)}
          >
            <MessageCircle className="w-4 h-4 mr-1" />
            {post.comments}
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => onShare(post.id)}
          >
            <Share2 className="w-4 h-4 mr-1" />
            {post.shares}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

**Можливості компонента:**
- **Інформація про автора**: аватар, ім'я, username в одному рядку
- **Мультимедійний контент**: текст + опціональне зображення
- **Інтерактивні метрики**: likes, comments, shares з іконками
- **Візуальний стан**: isLiked для червоного кольору сердечка
- **Timestamp**: дата публікації для контексту

**Приклади використання:**

```typescript
// Feed постів
<div className="space-y-4 max-w-2xl mx-auto">
  {posts.map(post => (
    <PostCard
      key={post.id}
      post={post}
      onLike={(id) => handleLike(id)}
      onComment={(id) => openComments(id)}
      onShare={(id) => openShareModal(id)}
    />
  ))}
</div>

// Профіль користувача
<div className="grid grid-cols-1 gap-4">
  {userPosts.map(post => (
    <PostCard
      key={post.id}
      post={post}
      onLike={toggleLike}
      onComment={navigateToComments}
      onShare={sharePost}
    />
  ))}
</div>
```

**Social Media Best Practices:**
- ✅ Автор завжди на видному місці
- ✅ Метрики з іконками для quick scan
- ✅ Візуальний фідбек для liked стану
- ✅ Компактний layout для feed scrolling
- ✅ Чіткі CTA для кожної дії

---

## 🎯 Best Practices для кожного домену

### E-commerce Checklist:
- ✅ Чіткі ціни та знижки
- ✅ Рейтинг продуктів видимий
- ✅ Quick actions (Add to Cart, Wishlist)
- ✅ High-quality product images
- ✅ Stock indicators для inventory management

### SaaS Dashboard Checklist:
- ✅ Ключові метрики на першому екрані
- ✅ Тренди з історичним контекстом
- ✅ Колірне кодування (success/warning/destructive)
- ✅ Експорт даних для advanced users
- ✅ Real-time updates через WebSockets

### Blog/CMS Checklist:
- ✅ SEO-friendly URLs та metadata
- ✅ Author bio для credibility
- ✅ Related articles recommendations
- ✅ Social sharing buttons
- ✅ Comments system integration

### Social Media Checklist:
- ✅ Infinite scroll для feed
- ✅ Оптимістичний UI для like/comment
- ✅ Image optimization для швидкого завантаження
- ✅ Accessibility для screen readers
- ✅ Responsive design для mobile-first

---

**Версія:** 1.0
**Дата створення:** 2025-10-15
**Автор:** Archon Blueprint Architect
