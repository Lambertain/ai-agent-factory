# Psychology Content Orchestrator

**Универсальный агент для координации создания психологического контента через мультиагентную систему**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/psychology-ai/content-orchestrator)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org)

## 🎯 Обзор

Psychology Content Orchestrator - это универсальный агент, предназначенный для координации создания психологического контента через мультиагентную систему. Агент НЕ привязан к конкретному проекту и может быть адаптирован для любых психологических доменов и задач.

### ✨ Ключевые особенности

- **🌐 Универсальная архитектура** - подходит для любых психологических доменов
- **🤖 Мультиагентная координация** - управление специализированными агентами
- **🔧 Конфигурируемые workflow** - настраиваемые процессы работы
- **🧠 RAG интеграция** - поддержка различных баз знаний
- **📊 Контроль качества** - комплексная валидация контента
- **🎭 Роль-ориентированность** - специализированные агенты-эксперты
- **🌍 Модульность** - легкая интеграция в существующие системы

## 🏗️ Архитектура

```
psychology-content-orchestrator/
├── core/                           # Основная логика
│   ├── orchestrator.js            # Главный координатор
│   ├── workflow-manager.js        # Управление workflow
│   └── agent-delegator.js         # Делегирование задач
├── config/                        # Конфигурации
│   ├── agent-configs.js          # Настройки агентов
│   └── domain-settings.js        # Настройки доменов
├── integrations/                  # Интеграции
│   ├── rag-connector.js          # RAG подключение
│   └── external-apis.js          # Внешние API
├── utils/                         # Утилиты
│   ├── content-merger.js         # Объединение контента
│   └── quality-validator.js      # Валидация качества
└── examples/                      # Примеры использования
    └── usage-examples.js         # Демонстрационные примеры
```

## 🚀 Быстрый старт

### Установка

```bash
npm install psychology-content-orchestrator
```

### Базовое использование

```javascript
const PsychologyContentOrchestrator = require('psychology-content-orchestrator');

// Создание экземпляра оркестратора
const orchestrator = new PsychologyContentOrchestrator({
    domain: 'clinical-psychology',
    integrationStrategy: 'clinical-protocols',
    qualityThreshold: 0.9,
    ragEnabled: true
});

// Запрос на создание контента
const request = {
    type: 'therapeutic-program',
    description: 'Создать программу КПТ для лечения тревожных расстройств',
    domain: 'clinical-psychology',
    targetAudience: 'adults-with-anxiety',
    objectives: [
        'Снижение уровня тревожности',
        'Развитие навыков совладания',
        'Улучшение качества жизни'
    ]
};

// Создание контента
const result = await orchestrator.createContent(request);

if (result.success) {
    console.log('✅ Контент создан успешно!');
    console.log(`📊 Качество: ${result.quality.score}`);
    console.log(`🤖 Использовано агентов: ${result.metrics.agentsUsed}`);
}
```

## 🎭 Поддерживаемые домены

### Основные психологические домены

- **🏥 Clinical Psychology** - клиническая психология, терапия, диагностика
- **🎓 Educational Psychology** - педагогическая психология, обучение
- **🏢 Organizational Psychology** - организационная психология, HR
- **💚 Health Psychology** - психология здоровья, профилактика
- **⭐ Positive Psychology** - позитивная психология, благополучие
- **🧠 Cognitive Psychology** - когнитивная психология, мышление
- **👥 Social Psychology** - социальная психология, групповая динамика
- **🌱 Developmental Psychology** - возрастная психология, развитие

### Специализированные области

- **⚽ Sports Psychology** - спортивная психология, производительность
- **⚖️ Forensic Psychology** - судебная психология, экспертиза

## 🛠️ Типы контента

### Терапевтические программы
```javascript
const request = {
    type: 'therapeutic-program',
    description: 'Программа терапии для конкретного расстройства',
    domain: 'clinical-psychology',
    // ... дополнительные параметры
};
```

### Инструменты оценки
```javascript
const request = {
    type: 'assessment-tool',
    description: 'Психометрический инструмент для измерения конструкта',
    domain: 'educational-psychology',
    // ... дополнительные параметры
};
```

### Библиотеки техник
```javascript
const request = {
    type: 'technique-library',
    description: 'Коллекция психологических техник и упражнений',
    domain: 'positive-psychology',
    // ... дополнительные параметры
};
```

### Комплексные программы
```javascript
const request = {
    type: 'comprehensive-program',
    description: 'Многокомпонентная программа с различными модулями',
    domain: 'organizational-psychology',
    // ... дополнительные параметры
};
```

## ⚙️ Конфигурация

### Настройка доменов

```javascript
const customDomainSettings = {
    'my-custom-domain': {
        name: 'My Custom Domain',
        requirements: ['requirement1', 'requirement2'],
        validation: ['validation1', 'validation2'],
        approaches: ['approach1', 'approach2'],
        integrationStrategy: 'custom-strategy',
        qualityThreshold: 0.85
    }
};

const orchestrator = new PsychologyContentOrchestrator({
    domain: 'my-custom-domain',
    domainSettings: customDomainSettings
});
```

### Настройка агентов

```javascript
const customAgentConfigs = {
    contentTypeMapping: {
        'my-content-type': ['research', 'my-custom-agent', 'quality-guardian']
    },
    agentDefinitions: {
        'my-custom-agent': {
            name: 'My Custom Agent',
            capabilities: ['custom-capability1', 'custom-capability2'],
            // ... дополнительные настройки
        }
    }
};

const orchestrator = new PsychologyContentOrchestrator({
    agentConfigs: customAgentConfigs
});
```

## 🔌 Интеграции

### RAG (Retrieval-Augmented Generation)

```javascript
const orchestrator = new PsychologyContentOrchestrator({
    ragEnabled: true,
    ragEndpoint: 'mcp__archon__rag_search_knowledge_base',
    relevanceThreshold: 0.7,
    defaultMatchCount: 5
});
```

### Archon MCP Server

```javascript
const orchestrator = new PsychologyContentOrchestrator({
    archonEnabled: true,
    projectId: 'your-project-id'
});

// Автоматическое создание задач в Archon
const result = await orchestrator.createContent(request);
```

### GitHub интеграция

```javascript
const orchestrator = new PsychologyContentOrchestrator({
    githubToken: 'your-github-token',
    githubIntegration: true
});
```

## 📊 Контроль качества

### Настройка валидации

```javascript
const orchestrator = new PsychologyContentOrchestrator({
    qualityThreshold: 0.9,      // Порог качества
    strictMode: true,           // Строгий режим
    validationRules: {          // Кастомные правила
        'safety-assessment': {
            threshold: 0.95,
            mandatory: true
        }
    }
});
```

### Мониторинг качества

```javascript
const result = await orchestrator.createContent(request);

console.log('Результаты валидации:');
console.log(`Общий балл: ${result.quality.score}`);
console.log(`Пройдена: ${result.quality.passed}`);
console.log(`Рекомендации: ${result.quality.recommendations.length}`);
```

## 🎯 Стратегии интеграции

- **standard** - стандартная интеграция для общих задач
- **clinical-protocols** - протоколы для клинического контента
- **educational-curriculum** - структурирование учебного контента
- **organizational-systems** - системный подход для организаций
- **holistic-wellbeing** - холистический подход к благополучию
- **performance-optimization** - оптимизация производительности

## 📈 Мониторинг и метрики

```javascript
// Получение статуса оркестратора
const status = orchestrator.getStatus();
console.log('Активные workflow:', status.activeWorkflows);
console.log('Процент успеха:', status.successRate);
console.log('Среднее качество:', status.averageQuality);

// Мониторинг конкретных компонентов
const ragStatus = orchestrator.ragConnector?.getStatus();
const delegatorStatus = orchestrator.agentDelegator?.getStatus();
const mergerStatus = orchestrator.contentMerger?.getStatus();
```

## 🔧 Примеры использования

### Запуск всех примеров
```bash
npm start
```

### Запуск конкретных примеров
```bash
npm run example:therapeutic     # Терапевтическая программа
npm run example:assessment      # Инструмент оценки
npm run example:organizational  # Организационная программа
npm run example:research        # Исследовательская методология
npm run example:custom          # Кастомный домен
npm run example:multi-domain    # Мультидоменная интеграция
npm run example:monitoring      # Мониторинг статуса
```

## 🤝 Workflow агентов

### Типичный workflow

1. **Research Agent** → исследование и анализ
2. **Architect Agent** → проектирование структуры
3. **Content Generators** → создание контента (параллельно)
   - NLP Generator
   - Technique Designer
   - Test Generator
4. **Quality Guardian** → валидация качества
5. **Integrator** → объединение результатов

### Специализированные агенты

- **Clinical Expert** - клиническая экспертиза
- **Pedagogy Expert** - педагогическая экспертиза
- **Organizational Expert** - организационная экспертиза
- **Psychometrician** - психометрическая валидация
- **Statistical Analyst** - статистический анализ

## 🛡️ Безопасность и этика

### Встроенные проверки
- Этическое соответствие
- Оценка безопасности
- Культурная чувствительность
- Профессиональные стандарты

### Обязательные валидации
- Противопоказания и риски
- Требования к супервизии
- Информированное согласие
- Конфиденциальность

## 📚 Документация

- [API Reference](docs/api-reference.md)
- [Configuration Guide](docs/configuration.md)
- [Domain Customization](docs/domain-customization.md)
- [Agent Development](docs/agent-development.md)
- [Integration Guide](docs/integration-guide.md)

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🙋 Поддержка

- **Issues**: [GitHub Issues](https://github.com/psychology-ai/content-orchestrator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/psychology-ai/content-orchestrator/discussions)
- **Email**: support@psychology-ai.org

## 🌟 Благодарности

- Архитекторам мультиагентных систем
- Сообществу психологов-исследователей
- Разработчикам open-source инструментов

---

**Psychology Content Orchestrator** - универсальное решение для создания качественного психологического контента через координацию специализированных AI-агентов. 🧠✨