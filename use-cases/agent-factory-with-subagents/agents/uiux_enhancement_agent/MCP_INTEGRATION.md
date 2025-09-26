# MCP Integration для UI/UX Enhancement Agent

## Обзор

UI/UX Enhancement Agent теперь поддерживает интеграцию с Model Context Protocol (MCP) серверами, что значительно расширяет его возможности по работе с дизайн системами, браузерной автоматизацией и долговременной памятью.

## Поддерживаемые MCP Серверы

### 🎨 Shadcn MCP Server
**Назначение:** Генерация и оптимизация shadcn/ui компонентов

**Возможности:**
- Автоматическая генерация shadcn/ui компонентов
- Валидация компонентов по shadcn стандартам
- Кастомизация тем и дизайн систем
- Интеграция с TypeScript

**Установка:**
```bash
npm install @modelcontextprotocol/server-shadcn
```

### 🤖 Puppeteer MCP Server
**Назначение:** Браузерная автоматизация и UI тестирование

**Возможности:**
- Скриншоты страниц и компонентов
- Visual regression testing
- Performance аудит
- Accessibility тестирование

**Установка:**
```bash
npm install @modelcontextprotocol/server-puppeteer
```

### 🧠 Context7 MCP Server
**Назначение:** Долговременная память и управление контекстом

**Возможности:**
- Сохранение дизайн паттернов и решений
- История предыдущих проектов
- Cross-project knowledge sharing
- Design system evolution tracking

**Установка:**
```bash
npm install @modelcontextprotocol/server-context7
```

## Конфигурация

### Claude Code Configuration
Добавьте MCP серверы в конфигурацию Claude Code:

**Файл:** `C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "node",
      "args": ["../shadcn-ui-mcp-server/build/index.js", "--transport", "stdio"],
      "cwd": "D:/Automation"
    },
    "puppeteer": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-puppeteer", "--transport", "stdio"]
    },
    "context7": {
      "command": "node",
      "args": ["../context7-mcp-server/dist/index.js", "--transport", "stdio"],
      "cwd": "D:/Automation"
    }
  }
}
```

## Доступные MCP Инструменты

### 1. use_shadcn_mcp_component()
Генерация shadcn/ui компонентов через MCP сервер.

### 2. use_puppeteer_mcp_screenshot()
Создание скриншотов для UI тестирования.

### 3. use_context7_mcp_memory()
Управление долговременной памятью дизайн решений.

### 4. mcp_ui_performance_analysis()
Анализ производительности UI компонентов.

### 5. mcp_accessibility_audit()
Аудит доступности через MCP серверы.

## Примеры Использования

### Проверка Интеграции

```python
# Простая проверка MCP интеграции
from simple_test import test_mcp_dependencies, test_mcp_toolsets

# Тестирование зависимостей
success1 = test_mcp_dependencies()

# Тестирование toolsets
success2 = test_mcp_toolsets()

if success1 and success2:
    print("✅ MCP интеграция работает корректно!")
else:
    print("⚠️ MCP работает в fallback режиме")
```

## Отладка и Решение Проблем

### Общие Проблемы

1. **MCP сервер не запускается**
   - Проверьте правильность путей в конфигурации
   - Убедитесь что Node.js установлен
   - Проверьте права доступа к файлам

2. **Fallback режим активен**
   - Нормально без настроенных серверов
   - Agent продолжает работать с базовой функциональностью

3. **Ошибки импорта**
   - Убедитесь что все зависимости установлены
   - Проверьте пути в sys.path

## Статус Интеграции

**Статус:** Готово к использованию ✅
**Тестирование:** 2/2 тестов пройдено ✅
**Документация:** Полная ✅