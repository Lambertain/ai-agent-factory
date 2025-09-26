# API Reference - Psychology Content Orchestrator

## Главные классы

### PsychologyContentOrchestrator

Основной класс для координации создания психологического контента.

#### Конструктор

```javascript
new PsychologyContentOrchestrator(config)
```

**Параметры:**
- `config` (Object) - Объект конфигурации
  - `domain` (string) - Психологический домен (по умолчанию: 'general-psychology')
  - `integrationStrategy` (string) - Стратегия интеграции (по умолчанию: 'standard')
  - `qualityThreshold` (number) - Порог качества (по умолчанию: 0.8)
  - `ragEnabled` (boolean) - Включить RAG (по умолчанию: true)
  - `maxRetries` (number) - Максимальное количество повторов (по умолчанию: 3)
  - `timeout` (number) - Таймаут в миллисекундах (по умолчанию: 300000)

#### Методы

##### createContent(request)

Создает психологический контент на основе запроса.

```javascript
async createContent(request)
```

**Параметры:**
- `request` (Object) - Запрос на создание контента
  - `type` (string) - Тип контента ('therapeutic-program', 'assessment-tool', etc.)
  - `description` (string) - Описание требований
  - `domain` (string) - Психологический домен (опционально)
  - `targetAudience` (string) - Целевая аудитория
  - `objectives` (Array) - Цели и задачи
  - `parameters` (Object) - Дополнительные параметры

**Возвращает:**
```javascript
{
  success: boolean,
  workflowId: string,
  content: Object,
  quality: Object,
  metrics: Object,
  metadata: Object
}
```

##### getStatus()

Получает текущий статус оркестратора.

```javascript
getStatus()
```

**Возвращает:**
```javascript
{
  activeWorkflows: number,
  totalProcessed: number,
  successRate: number,
  averageQuality: number,
  averageCompletionTime: number,
  config: Object
}
```

## Фабричные методы

### QuickStart

Предустановленные конфигурации для разных доменов.

#### QuickStart.clinical(config)

Создает оркестратор для клинической психологии.

```javascript
const orchestrator = QuickStart.clinical({
  qualityThreshold: 0.95,
  strictMode: true
});
```

#### QuickStart.educational(config)

Создает оркестратор для педагогической психологии.

```javascript
const orchestrator = QuickStart.educational({
  assessmentFocus: true
});
```

#### QuickStart.organizational(config)

Создает оркестратор для организационной психологии.

```javascript
const orchestrator = QuickStart.organizational({
  businessAlignment: true
});
```

### ContentFactory

Фабричные методы для создания конкретных типов контента.

#### ContentFactory.therapeuticProgram(orchestrator, description, options)

```javascript
const result = await ContentFactory.therapeuticProgram(
  orchestrator,
  'Программа КПТ для тревожных расстройств',
  {
    targetAudience: 'adults',
    duration: '12-16 sessions',
    evidenceLevel: 'high'
  }
);
```

#### ContentFactory.assessmentTool(orchestrator, description, options)

```javascript
const result = await ContentFactory.assessmentTool(
  orchestrator,
  'Шкала оценки депрессии для подростков',
  {
    items: 21,
    responseFormat: 'likert-4-point',
    validity: 'construct-validity'
  }
);
```

## Конфигурационные объекты

### Agent Configs

Конфигурация доступных агентов.

```javascript
const agentConfigs = {
  contentTypeMapping: {
    'therapeutic-program': ['research', 'clinical-expert', 'nlp-generator'],
    'assessment-tool': ['research', 'test-generator', 'psychometrician']
  },
  agentDefinitions: {
    'research': {
      capabilities: ['literature-review', 'evidence-synthesis'],
      processingTime: { simple: 60000, complex: 300000 }
    }
  }
}
```

### Domain Settings

Настройки для различных психологических доменов.

```javascript
const domainSettings = {
  'clinical-psychology': {
    requirements: ['clinical-evidence-base', 'safety-protocols'],
    validation: ['clinical-validity', 'safety-assessment'],
    approaches: ['cognitive-behavioral-therapy', 'psychodynamic'],
    qualityThreshold: 0.95
  }
}
```

## Интеграционные модули

### RAGConnector

Интеграция с системами поиска знаний.

#### searchRelevantKnowledge(query, domain, options)

```javascript
const ragConnector = new RAGConnector(config);

const results = await ragConnector.searchRelevantKnowledge(
  'cognitive behavioral therapy for anxiety',
  'clinical-psychology',
  {
    matchCount: 10,
    relevanceThreshold: 0.8
  }
);
```

### ExternalAPIs

Интеграция с внешними API.

#### createProject(projectData)

```javascript
const externalAPIs = new ExternalAPIs(config);

const project = await externalAPIs.createProject({
  title: 'Проект психологической программы',
  description: 'Описание проекта',
  githubRepo: 'https://github.com/user/repo'
});
```

## Утилитарные классы

### ContentMerger

Объединение результатов от множественных агентов.

#### mergeResults(executionResults, context)

```javascript
const merger = new ContentMerger(config);

const mergedContent = await merger.mergeResults(
  executionResults,
  {
    workflowId: 'wf_123',
    domain: 'clinical-psychology',
    integrationStrategy: 'clinical-protocols'
  }
);
```

### QualityValidator

Валидация качества контента.

#### validateContent(content, context)

```javascript
const validator = new QualityValidator(config);

const validation = await validator.validateContent(
  content,
  {
    domain: 'clinical-psychology',
    threshold: 0.9,
    strictMode: true
  }
);
```

## Утилитарные функции

### Utils.validateConfig(config)

Валидация конфигурации перед созданием оркестратора.

```javascript
const validation = Utils.validateConfig({
  domain: 'clinical-psychology',
  qualityThreshold: 0.9
});

if (!validation.valid) {
  console.error('Ошибки конфигурации:', validation.errors);
}
```

### Utils.findBestDomain(requirements)

Поиск наиболее подходящего домена для требований.

```javascript
const result = Utils.findBestDomain([
  'evidence-based-treatment',
  'clinical-assessment',
  'therapeutic-intervention'
]);

console.log('Рекомендуемый домен:', result.domain);
console.log('Уверенность:', result.confidence);
```

## Интеграционные хелперы

### Integrations.withRAG(config)

Создание оркестратора с включенным RAG.

```javascript
const orchestrator = Integrations.withRAG({
  domain: 'clinical-psychology',
  relevanceThreshold: 0.8,
  defaultMatchCount: 10
});
```

### Integrations.withArchon(projectId, config)

Создание оркестратора с интеграцией Archon.

```javascript
const orchestrator = Integrations.withArchon(
  'proj-123',
  {
    domain: 'organizational-psychology',
    taskManagement: true
  }
);
```

## События и мониторинг

### События WorkflowManager

```javascript
orchestrator.workflowManager.on('phaseCompleted', (phase) => {
  console.log(`Фаза завершена: ${phase.name}`);
});

orchestrator.workflowManager.on('workflowCompleted', (workflow) => {
  console.log(`Workflow завершен: ${workflow.id}`);
});
```

### События AgentDelegator

```javascript
orchestrator.agentDelegator.on('taskDelegated', (task) => {
  console.log(`Задача делегирована: ${task.id} -> ${task.agent}`);
});

orchestrator.agentDelegator.on('taskCompleted', (result) => {
  console.log(`Задача завершена: ${result.taskId}`);
});
```

## Типы ошибок

### OrchestratorError

Базовый класс ошибок оркестратора.

```javascript
try {
  await orchestrator.createContent(request);
} catch (error) {
  if (error instanceof OrchestratorError) {
    console.error('Ошибка оркестратора:', error.message);
    console.error('Фаза:', error.phase);
    console.error('Workflow ID:', error.workflowId);
  }
}
```

### ValidationError

Ошибки валидации контента.

```javascript
try {
  await validator.validateContent(content);
} catch (error) {
  if (error instanceof ValidationError) {
    console.error('Ошибка валидации:', error.message);
    console.error('Критерий:', error.criterion);
    console.error('Ожидаемый порог:', error.threshold);
  }
}
```

## Константы и перечисления

### Content Types

```javascript
const CONTENT_TYPES = {
  THERAPEUTIC_PROGRAM: 'therapeutic-program',
  ASSESSMENT_TOOL: 'assessment-tool',
  TECHNIQUE_LIBRARY: 'technique-library',
  INTERVENTION_PROTOCOL: 'intervention-protocol',
  COMPREHENSIVE_PROGRAM: 'comprehensive-program',
  RESEARCH_METHODOLOGY: 'research-methodology'
};
```

### Integration Strategies

```javascript
const INTEGRATION_STRATEGIES = {
  STANDARD: 'standard',
  CLINICAL_PROTOCOLS: 'clinical-protocols',
  EDUCATIONAL_CURRICULUM: 'educational-curriculum',
  ORGANIZATIONAL_SYSTEMS: 'organizational-systems',
  HOLISTIC_WELLBEING: 'holistic-wellbeing',
  PERFORMANCE_OPTIMIZATION: 'performance-optimization'
};
```

### Quality Thresholds

```javascript
const QUALITY_THRESHOLDS = {
  MINIMAL: 0.6,
  STANDARD: 0.8,
  HIGH: 0.9,
  CLINICAL: 0.95,
  RESEARCH: 0.9
};
```

## Примеры полных workflow

### Создание терапевтической программы

```javascript
const { QuickStart, ContentFactory } = require('psychology-content-orchestrator');

async function createTherapyProgram() {
  // Создание оркестратора
  const orchestrator = QuickStart.clinical({
    qualityThreshold: 0.95,
    ragEnabled: true
  });

  // Создание контента
  const result = await ContentFactory.therapeuticProgram(
    orchestrator,
    'Программа КПТ для лечения социальной тревожности',
    {
      targetAudience: 'young-adults',
      objectives: [
        'Снижение социальной тревожности',
        'Развитие социальных навыков',
        'Повышение самооценки'
      ],
      parameters: {
        duration: '16 sessions',
        format: 'group-therapy',
        evidenceLevel: 'high'
      }
    }
  );

  if (result.success) {
    console.log('✅ Программа создана успешно');
    return result.content;
  } else {
    console.error('❌ Ошибка создания программы:', result.error);
    return null;
  }
}
```

### Мониторинг создания контента

```javascript
async function monitoredContentCreation() {
  const orchestrator = QuickStart.general();

  // Подписка на события
  orchestrator.agentDelegator.on('taskDelegated', (task) => {
    console.log(`🤖 Задача делегирована агенту ${task.agent}`);
  });

  orchestrator.workflowManager.on('phaseCompleted', (phase) => {
    console.log(`✅ Фаза "${phase.name}" завершена`);
  });

  // Мониторинг статуса
  const statusInterval = setInterval(() => {
    const status = orchestrator.getStatus();
    console.log(`📊 Активные workflow: ${status.activeWorkflows}`);
  }, 5000);

  try {
    const result = await orchestrator.createContent({
      type: 'assessment-tool',
      description: 'Инструмент оценки стресса на рабочем месте',
      domain: 'organizational-psychology'
    });

    clearInterval(statusInterval);
    return result;

  } catch (error) {
    clearInterval(statusInterval);
    throw error;
  }
}
```