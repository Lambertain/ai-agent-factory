# Module 01: Design Systems - Tailwind CSS & shadcn/ui

## 🎨 Adaptive Tailwind Configuration

Универсальная конфигурация Tailwind CSS для любых типов проектов с поддержкой адаптивных дизайн-токенов, темизации и гибкой типографики.

### Tailwind Config - Universal Design System

```javascript
// tailwind.config.js - Universal Design System
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      // CSS Variables для адаптивных цветов
      colors: {
        // Base semantic colors (customizable via CSS variables)
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",

        // Brand colors (configurable)
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
          50: "hsl(var(--primary-50, 240 100% 98%))",
          100: "hsl(var(--primary-100, 240 100% 96%))",
          500: "hsl(var(--primary-500, 240 100% 50%))",
          900: "hsl(var(--primary-900, 240 100% 10%))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },

        // Success/Warning/Info states
        success: {
          DEFAULT: "hsl(var(--success, 142 76% 36%))",
          foreground: "hsl(var(--success-foreground, 0 0% 100%))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning, 38 92% 50%))",
          foreground: "hsl(var(--warning-foreground, 0 0% 0%))",
        },
        info: {
          DEFAULT: "hsl(var(--info, 217 91% 60%))",
          foreground: "hsl(var(--info-foreground, 0 0% 100%))",
        }
      },

      // Universal animations
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "slide-in": "slide-in 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
        "slide-out": "slide-out 0.2s cubic-bezier(0.16, 1, 0.3, 1)",
        "fade-in": "fade-in 0.5s ease-out",
        "fade-out": "fade-out 0.3s ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "bounce-subtle": "bounce-subtle 0.6s ease-out",
        "scale-in": "scale-in 0.2s ease-out",
        "scale-out": "scale-out 0.2s ease-out",
      },

      // Adaptive typography
      fontFamily: {
        sans: ['var(--font-sans, Inter)', 'system-ui', 'sans-serif'],
        display: ['var(--font-display, Cal Sans)', 'var(--font-sans, Inter)', 'sans-serif'],
        mono: ['var(--font-mono, Fira Code)', 'Menlo', 'Monaco', 'monospace'],
      },

      // Flexible spacing system
      spacing: {
        '15': '3.75rem',
        '18': '4.5rem',
        '88': '22rem',
        '120': '30rem',
        '144': '36rem',
      },

      // Adaptive breakpoints
      screens: {
        'xs': '475px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1400px',
        '3xl': '1920px',
      },

      // Configurable border radius
      borderRadius: {
        'xs': 'var(--radius-xs, 0.125rem)',
        'sm': 'var(--radius-sm, 0.25rem)',
        DEFAULT: 'var(--radius, 0.5rem)',
        'md': 'var(--radius-md, 0.75rem)',
        'lg': 'var(--radius-lg, 1rem)',
        'xl': 'var(--radius-xl, 1.5rem)',
      }
    }
  },
  plugins: [
    require("tailwindcss-animate"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/container-queries"),
  ]
}
```

**Ключевые особенности конфигурации:**
- **CSS Variables**: Все цвета через CSS переменные для динамической темизации
- **Semantic Naming**: Понятные имена для контекста использования (primary, destructive, muted)
- **Flexible Scales**: Расширенная шкала брейкпоинтов (xs до 3xl) для любых устройств
- **Universal Animations**: Набор готовых анимаций для типичных интеракций
- **Typography System**: Адаптивная типографика с переменными для кастомизации

---

## 🧩 Universal shadcn/ui Component Patterns

Универсальные паттерны компонентов на базе shadcn/ui, адаптируемые под любой тип контента и домен.

### Universal Card Component

Универсальный компонент карточки для отображения любого типа контента с поддержкой вариантов, размеров и интерактивности.

```typescript
// Universal Card Component for any content type
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface UniversalCardProps {
  item: {
    title: string;
    description?: string;
    image?: string;
    status?: string;
    progress?: number;
    tags?: string[];
    metadata?: Record<string, any>;
    actions?: Array<{
      label: string;
      variant?: 'default' | 'secondary' | 'outline' | 'destructive';
      onClick: () => void;
    }>;
  };
  variant?: 'default' | 'interactive' | 'elevated';
  size?: 'sm' | 'md' | 'lg';
}

export function UniversalCard({ item, variant = 'default', size = 'md' }: UniversalCardProps) {
  const cardVariants = {
    default: "border shadow-sm",
    interactive: "border shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer hover:scale-[1.02]",
    elevated: "border-0 shadow-lg hover:shadow-xl transition-shadow duration-300"
  };

  const sizeVariants = {
    sm: "p-4",
    md: "p-6",
    lg: "p-8"
  };

  return (
    <Card className={cn(cardVariants[variant], "overflow-hidden")}>
      {item.image && (
        <div className="aspect-video relative overflow-hidden">
          <img
            src={item.image}
            alt={item.title}
            className="object-cover w-full h-full hover:scale-105 transition-transform duration-300"
          />
          {item.status && (
            <Badge
              className="absolute top-2 right-2"
              variant={item.status === 'urgent' ? 'destructive' : 'secondary'}
            >
              {item.status}
            </Badge>
          )}
        </div>
      )}

      <CardHeader className={cn("space-y-2", sizeVariants[size])}>
        <h3 className="font-semibold text-lg line-clamp-2">{item.title}</h3>
        {item.description && (
          <p className="text-sm text-muted-foreground line-clamp-3">
            {item.description}
          </p>
        )}
        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {item.tags.map(tag => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        )}
      </CardHeader>

      <CardContent className={cn("space-y-2", sizeVariants[size])}>
        {item.metadata && Object.entries(item.metadata).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground capitalize">{key}:</span>
            <span className="font-medium">{String(value)}</span>
          </div>
        ))}

        {typeof item.progress === 'number' && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Progress</span>
              <span>{item.progress}%</span>
            </div>
            <Progress value={item.progress} className="h-2" />
          </div>
        )}
      </CardContent>

      {item.actions && item.actions.length > 0 && (
        <CardFooter className={cn("flex gap-2", sizeVariants[size])}>
          {item.actions.map((action, index) => (
            <Button
              key={index}
              variant={action.variant || 'default'}
              onClick={action.onClick}
              className="flex-1"
            >
              {action.label}
            </Button>
          ))}
        </CardFooter>
      )}
    </Card>
  );
}
```

**Возможности компонента:**
- **Универсальность**: Подходит для продуктов, статей, профилей, задач, любого контента
- **Варианты**: default (обычная), interactive (с hover эффектами), elevated (приподнятая)
- **Размеры**: sm, md, lg для адаптации под разные контексты
- **Гибкость**: Опциональные image, tags, metadata, progress, actions
- **Accessibility**: Корректные семантические теги и ARIA attributes

---

### Adaptive Theme Provider

Провайдер темизации с поддержкой light/dark/system режимов и localStorage для сохранения предпочтений пользователя.

```typescript
// Adaptive Theme Provider
import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';
type ThemeProviderProps = {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
};

const ThemeProviderContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({
  theme: 'system',
  setTheme: () => null,
});

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'ui-theme',
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  );

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
      return;
    }

    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme);
      setTheme(theme);
    },
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext);
  if (context === undefined)
    throw new Error('useTheme must be used within a ThemeProvider');
  return context;
};
```

**Возможности провайдера:**
- **System Theme Detection**: Автоматическое определение системных предпочтений
- **Persistence**: Сохранение выбора пользователя в localStorage
- **Customizable Storage Key**: Возможность использовать разные ключи для разных приложений
- **React Context**: Глобальный доступ к теме из любого компонента через useTheme hook
- **Dynamic Class Application**: Автоматическое применение классов light/dark к documentElement

---

## 🎯 Best Practices для Design Systems

### 1. Semantic Color Naming
Используй семантические имена (primary, destructive, muted) вместо конкретных цветов (blue, red, gray). Это позволяет легко менять цветовую схему без рефакторинга компонентов.

### 2. CSS Variables для Темизации
Все дизайн-токены через CSS переменные:
```css
:root {
  --primary: 240 100% 50%;
  --background: 0 0% 100%;
}

.dark {
  --primary: 240 100% 60%;
  --background: 0 0% 10%;
}
```

### 3. Component Variants через cn() Utility
Используй tailwind-merge для композиции классов:
```typescript
const variants = {
  default: "bg-primary text-primary-foreground",
  outline: "border border-input bg-background"
};
className={cn(variants[variant], className)}
```

### 4. Responsive Defaults
Всегда проектируй mobile-first:
```typescript
className="text-sm md:text-base lg:text-lg"
```

### 5. Accessibility First
Каждый компонент должен иметь:
- Правильные ARIA attributes
- Keyboard navigation support
- Focus indicators
- Screen reader compatibility

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
