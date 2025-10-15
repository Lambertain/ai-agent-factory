# Module 07: MCP Integration для UI/UX

## 🔌 MCP серверы в дизайн-процессе

Интеграция Model Context Protocol (MCP) серверов в UI/UX workflow позволяет автоматизировать визуальное тестирование, синхронизацию дизайна, аудит доступности и кросс-браузерную совместимость. Этот модуль описывает ключевые MCP инструменты для современной UI/UX разработки.

---

## 🛠️ Рекомендуемые MCP серверы

### 1. Puppeteer MCP - Visual Testing & Automation

**Использование:**
- Автоматизация визуального тестирования компонентов
- Создание скриншотов для документации
- E2E тестирование пользовательских сценариев
- Performance profiling рендеринга

**Примеры интеграции:**
```typescript
// Автоматическое тестирование компонента с разными пропсами
await puppeteer.navigate("http://localhost:3000/components/button");
await puppeteer.screenshot("button-default.png");

await puppeteer.click("[data-testid='variant-primary']");
await puppeteer.screenshot("button-primary.png");

await puppeteer.click("[data-testid='variant-destructive']");
await puppeteer.screenshot("button-destructive.png");
```

### 2. Figma MCP - Design-to-Code Sync

**Использование:**
- Экспорт компонентов и стилей из Figma в код
- Синхронизация design tokens (цвета, шрифты, spacing)
- Валидация соответствия дизайну
- Генерация React компонентов из Figma frames

**Примеры интеграции:**
```typescript
// Экспорт design tokens из Figma
const designTokens = await figma.exportTokens("file-id");
// → { colors: { primary: "#3B82F6", ... }, spacing: { sm: "8px", ... } }

// Генерация компонента из Figma frame
const component = await figma.generateComponent("frame-id");
// → React component code ready to use
```

### 3. Lighthouse MCP - Performance & Accessibility Audits

**Использование:**
- Автоматический аудит Core Web Vitals
- WCAG accessibility compliance проверка
- Best practices validation
- SEO optimization recommendations

**Примеры интеграции:**
```typescript
// Запуск Lighthouse audit для страницы
const report = await lighthouse.audit("https://myapp.com/dashboard");

// Проверка Core Web Vitals
console.log(report.metrics.LCP); // Largest Contentful Paint
console.log(report.metrics.CLS); // Cumulative Layout Shift
console.log(report.metrics.FID); // First Input Delay

// Accessibility score
console.log(report.accessibility.score); // 0-100
console.log(report.accessibility.violations); // Array of issues
```

### 4. BrowserStack MCP - Cross-Browser Testing

**Использование:**
- Тестирование на реальных устройствах и браузерах
- Валидация responsive design на iOS/Android
- Проверка совместимости с legacy browsers
- Automated testing на multiple configurations

**Примеры интеграции:**
```typescript
// Запуск теста на разных браузерах
await browserstack.runTest({
  browsers: ["chrome:latest", "safari:15", "firefox:90"],
  devices: ["iPhone 13", "Samsung Galaxy S21", "iPad Pro"],
  url: "https://myapp.com"
});

// Получение скриншотов со всех устройств
const screenshots = await browserstack.getScreenshots();
```

### 5. Contrast Checker MCP - Color Accessibility

**Использование:**
- Валидация цветового контраста WCAG AA/AAA
- Проверка доступности для color blindness
- Генерация accessible color palettes
- Real-time contrast warnings

**Примеры интеграции:**
```typescript
// Проверка контраста текста и фона
const contrast = await contrastChecker.check({
  foreground: "#3B82F6",
  background: "#FFFFFF"
});
// → { ratio: 4.5, wcagAA: true, wcagAAA: false }

// Получение рекомендаций для improvement
const suggestions = await contrastChecker.getSuggestions("#3B82F6", "#FFFFFF");
// → [{ color: "#2563EB", ratio: 5.2, wcagAAA: true }]
```

---

## 🔄 Паттерны интеграции с дизайн-процессом

### Continuous Accessibility Testing

```typescript
// Pre-commit hook для accessibility audit
async function preCommitAccessibilityCheck() {
  const pages = ["/", "/dashboard", "/profile", "/settings"];

  for (const page of pages) {
    const report = await lighthouse.audit(`http://localhost:3000${page}`, {
      onlyCategories: ["accessibility"]
    });

    if (report.accessibility.score < 90) {
      throw new Error(`Accessibility score too low for ${page}: ${report.accessibility.score}`);
    }
  }
}
```

### Visual Regression Testing

```typescript
// Автоматическое сравнение скриншотов после изменений
async function visualRegressionTest(componentPath: string) {
  await puppeteer.navigate(`http://localhost:3000${componentPath}`);

  const currentScreenshot = await puppeteer.screenshot("current.png");
  const baselineScreenshot = loadBaselineScreenshot(componentPath);

  const diff = compareImages(currentScreenshot, baselineScreenshot);

  if (diff.percentage > 0.1) {
    console.warn(`Visual changes detected: ${diff.percentage}% difference`);
    // Show diff for manual review
  }
}
```

### Automated Responsive Testing

```typescript
// Тестирование на всех breakpoints
async function responsiveTest(url: string) {
  const breakpoints = [
    { name: "mobile", width: 375, height: 667 },
    { name: "tablet", width: 768, height: 1024 },
    { name: "desktop", width: 1920, height: 1080 }
  ];

  for (const bp of breakpoints) {
    await puppeteer.resizePage(bp.width, bp.height);
    await puppeteer.screenshot(`${bp.name}-${url}.png`);

    // Validate layout не сломан
    const layoutIssues = await puppeteer.evaluate(() => {
      // Check for horizontal overflow, broken layouts
      return document.documentElement.scrollWidth > window.innerWidth;
    });

    if (layoutIssues) {
      console.error(`Layout broken on ${bp.name} for ${url}`);
    }
  }
}
```

### Real-time Performance Monitoring

```typescript
// CI/CD integration для мониторинга performance
async function performanceMonitor() {
  const criticalPages = ["/", "/dashboard", "/products"];

  for (const page of criticalPages) {
    const metrics = await lighthouse.audit(`https://production.app${page}`, {
      onlyCategories: ["performance"]
    });

    // Alert если performance деградировал
    if (metrics.performance.score < 85) {
      await sendAlert({
        type: "performance_degradation",
        page,
        score: metrics.performance.score,
        metrics: metrics.metrics
      });
    }
  }
}
```

---

## 🎯 Best Practices для MCP Integration

### 1. Automated Testing Pipeline
- ✅ Интегрируй Lighthouse в CI/CD для каждого PR
- ✅ Запускай visual regression tests перед merge
- ✅ Используй BrowserStack для кросс-браузерного тестирования critical flows

### 2. Design Sync Workflow
- ✅ Синхронизируй design tokens из Figma еженедельно
- ✅ Валидируй соответствие компонентов дизайну автоматически
- ✅ Генерируй компоненты из Figma для быстрого прототипирования

### 3. Accessibility First
- ✅ Проверяй контраст всех новых цветов через Contrast Checker
- ✅ Запускай accessibility audit для каждого нового компонента
- ✅ Автоматизируй проверку keyboard navigation

### 4. Performance Monitoring
- ✅ Отслеживай Core Web Vitals в production
- ✅ Установи performance budgets и automated alerts
- ✅ Регулярно профилируй rendering performance

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
