# TypeScript Architecture Agent

**Универсальный агент для анализа и оптимизации архитектуры TypeScript приложений любого типа**

Агент специализируется на комплексном анализе TypeScript кодовых баз, адаптируясь под различные типы проектов и фреймворков, обеспечивая type safety и архитектурную excellence.

## 🎯 Назначение

Агент выполняет комплексный анализ TypeScript кодовой базы с фокусом на:
- **Type Safety**: устранение 'any' типов, улучшение типизации
- **Архитектурные паттерны**: рефакторинг компонентов, модулей
- **Производительность**: оптимизация сборки и runtime
- **Maintainability**: улучшение читаемости и тестируемости кода

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка окружения
```bash
cp .env.example .env
# Заполните необходимые API ключи в .env
```

### Использование через CLI
```bash
# Анализ одного файла
python -m typescript_architecture_agent.cli analyze src/components/EventCard.tsx

# Полный аудит проекта
python -m typescript_architecture_agent.cli audit /path/to/project --report=report.md

# Рефакторинг кода
python -m typescript_architecture_agent.cli refactor "interface User { id: any; }" --strategy=optimize

# Оптимизация tsconfig.json
python -m typescript_architecture_agent.cli optimize-config --project-path=/path/to/project
```

### Использование как модуль
```python
import asyncio
from typescript_architecture_agent import run_typescript_analysis

async def main():
    result = await run_typescript_analysis(
        context="Анализ файла src/types/Event.ts",
        project_path="/path/to/your-project",
        analysis_type="types"
    )
    print(result)

asyncio.run(main())
```

## 🛠️ Инструменты агента

### 1. `analyze_type_complexity`
Анализирует сложность типов и выявляет проблемы:
- Обнаружение избыточных union типов
- Поиск циклических зависимостей
- Расчет метрик сложности

### 2. `refactor_types`
Предлагает улучшения структуры типов:
- Разделение сложных интерфейсов
- Создание utility типов
- Оптимизация generic параметров

### 3. `generate_type_guards`
Создает type guards для runtime проверок:
- Валидация входных данных
- Безопасные type assertions
- Защита от типовых ошибок

### 4. `optimize_typescript_config`
Настраивает tsconfig.json для лучшей производительности:
- Оптимизация strict режима
- Настройка path mapping
- Конфигурация incremental compilation

### 5. `search_agent_knowledge`
Поиск в базе знаний агента через Archon RAG:
- TypeScript best practices
- Архитектурные паттерны
- Примеры решений

## 📋 Типы анализа

| Тип | Описание | Когда использовать |
|-----|----------|-------------------|
| `full` | Комплексный анализ архитектуры | Общий аудит проекта |
| `types` | Фокус на type safety | Проблемы с типизацией |
| `performance` | Оптимизация производительности | Медленная сборка |
| `refactor` | Рекомендации по рефакторингу | Техдолг, legacy код |

## 🏗️ Архитектура агента

```
typescript_architecture_agent/
├── agent.py              # Основной агент с мультиагентными паттернами
├── tools.py              # 5 специализированных инструментов
├── prompts.py            # Системные промпты с reflection
├── dependencies.py       # RAG-интеграция и зависимости
├── providers.py          # Cost-optimized модели (Qwen + Gemini)
├── settings.py           # Конфигурация через Pydantic Settings
├── cli.py                # Командная строка
├── knowledge/            # База знаний для Archon RAG
│   └── typescript_architecture_knowledge.md
├── tests/                # Полный набор тестов
│   └── test_agent.py
└── README.md             # Эта документация
```

## 🔄 Мультиагентные паттерны

Агент следует паттернам из видео Andrew Ng:

### 1. **🔄 Reflection Pattern**
После каждой задачи выполняется цикл рефлексии:
```
## 🔄 РЕФЛЕКСИЯ-УЛУЧШЕНИЕ
1. Критический анализ результата
2. Выявление 2-3 недостатков
3. Создание улучшенной версии
```

### 2. **🛠️ Tool Use Pattern**
Динамическое использование инструментов на основе анализа:
- Выбор подходящего инструмента для задачи
- Комбинирование результатов нескольких инструментов
- RAG-поиск для принятия решений

### 3. **📋 Planning Pattern**
Разбивка сложных задач:
```
## 📋 ПЛАНИРОВАНИЕ
1. Анализ входных данных
2. Выбор стратегии анализа
3. Последовательность действий
```

### 4. **👥 Multi-Agent Collaboration**
Интеграция с другими агентами через Archon.

## ⚙️ Конфигурация

### Переменные окружения (.env)
```bash
# LLM Configuration
LLM_API_KEY=your_qwen_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
GEMINI_API_KEY=your_gemini_api_key_here

# Cost-Optimized Models
LLM_ARCHITECTURE_MODEL=qwen2.5-72b-instruct      # Сложный анализ
LLM_CODING_MODEL=qwen2.5-coder-32b-instruct      # Генерация кода
LLM_PLANNING_MODEL=gemini-2.5-flash-lite         # Планирование

# TypeScript Settings
TYPESCRIPT_STRICT_MODE=true
TARGET_TYPE_COVERAGE=0.95
MAX_COMPLEXITY_SCORE=7

# Archon Integration
ARCHON_URL=http://localhost:3737
ARCHON_PROJECT_ID=c75ef8e3-6f4d-4da2-9e81-8d38d04a341a
```

### Настройка моделей по стоимости
- **Архитектурный анализ**: Qwen 2.5 72B ($2-3/1M токенов)
- **Генерация кода**: Qwen 2.5 Coder 32B ($1-2/1M токенов)
- **Планирование**: Gemini 2.5 Flash-Lite ($0.10-0.40/1M токенов)

Экономия до 80% на операционных расходах по сравнению с GPT-4.

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest tests/ -v

# Тестирование с покрытием
pytest tests/ --cov=typescript_architecture_agent

# Тестирование CLI
pytest tests/test_agent.py::TestTypeScriptAgent::test_cli_integration
```

## 📚 База знаний

Агент интегрирован с Archon Knowledge Base:
- **Файл знаний**: `knowledge/typescript_architecture_knowledge.md`
- **Теги**: `typescript-architecture`, `agent-knowledge`, `pydantic-ai`
- **Домен**: Архитектурные паттерны TypeScript, оптимизация

### Загрузка в Archon:
1. Откройте http://localhost:3737/
2. Knowledge Base → Upload → выберите файл знаний
3. Добавьте теги: `typescript-architecture`, `agent-knowledge`
4. Привяжите к проекту "AI Agent Factory"

## 🔗 Универсальная интеграция

Агент адаптируется к любым современным стекам:
- **Frontend**: React, Vue, Angular, Svelte
- **Backend**: Node.js, NestJS, Express, Fastify
- **Full-stack**: Next.js, Remix, T3 Stack, SvelteKit
- **Mobile**: React Native, Ionic, Tauri
- **Libraries**: Любые TypeScript библиотеки и пакеты

## 📊 Метрики качества

Агент отслеживает:
- **Type Coverage**: целевое значение 95%
- **Complexity Score**: максимум 7 баллов
- **Build Performance**: время сборки
- **Bundle Size**: размер финальных файлов

## 🚀 Дальнейшее развитие

- [ ] Интеграция с ESLint/TSLint правилами
- [ ] Автоматическое применение рефакторинга
- [ ] Visual Studio Code расширение
- [ ] CI/CD интеграция для автоматического аудита

## 🤝 Интеграция с другими агентами

TypeScript Architecture Agent работает в экосистеме AI Agent Factory и интегрируется с другими универсальными агентами:

- **Next.js Optimization Agent**: совместная оптимизация TypeScript + Next.js архитектуры
- **Prisma Database Agent**: синхронизация схем базы данных с TypeScript типами
- **UI/UX Enhancement Agent**: type-safe интерфейсы и компонентная архитектура
- **PWA Mobile Agent**: кроссплатформенная TypeScript разработка

Агенты автоматически обмениваются знаниями через Archon RAG и координируют работу через единую систему задач.

---

**Версия**: 1.0.0
**Лицензия**: MIT
**Поддержка**: Создавайте issues в репозитории