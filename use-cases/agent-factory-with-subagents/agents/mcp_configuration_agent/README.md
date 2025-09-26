# MCP Configuration Agent

Универсальный агент для установки, настройки и управления MCP (Model Context Protocol) серверами для различных проектов и технологических стеков.

## Что это?

MCP Configuration Agent - это универсальный инструмент для:
- Установки официальных MCP серверов через npm
- Автоматической настройки Claude Desktop конфигурации
- Валидации и тестирования MCP серверов
- Создания новых серверов из шаблонов
- Управления конфигурациями для разных доменов

## Ключевые возможности

### 🔧 Установка MCP серверов
- Автоматическая установка через npm/pip/uv
- Поддержка официальных серверов от Anthropic
- Валидация конфигураций перед установкой

### ⚙️ Настройка Claude Desktop
- Автоматическое обновление `claude_desktop_config.json`
- Поддержка STDIO и HTTP транспортов
- Управление переменными окружения

### 🌐 Универсальные конфигурации
- Настройки для разных доменов (frontend, backend, AI, security)
- Адаптация под различные проекты
- Поддержка кастомных конфигураций

### 🛠️ Создание серверов
- Генерация новых MCP серверов из шаблонов
- Поддержка Python и TypeScript шаблонов
- Интеграция с официальным create-server

## Официальные MCP серверы

Агент поддерживает следующие официальные серверы:

### 📁 Файловая система
- **filesystem** - Доступ к файловой системе

### 🔍 Поиск и интеграции
- **brave-search** - Поиск в интернете
- **github** - Интеграция с GitHub API
- **slack** - Интеграция со Slack
- **linear** - Управление задачами в Linear
- **figma** - Работа с Figma API

### 💾 Базы данных
- **postgres** - Подключение к PostgreSQL
- **redis** - Работа с Redis

### 🐳 DevOps
- **docker** - Управление Docker
- **kubernetes** - Управление K8s кластерами

### 🧪 Научные вычисления
- **jupyter** - Интеграция с Jupyter Notebook
- **vector-db** - Векторные базы данных

## Использование

### Основные функции

```python
from agents.mcp_configuration_agent.agent import MCPConfigurationAgent

# Создание агента для fullstack разработки
agent = MCPConfigurationAgent(config_domain="fullstack", project_type="web")

# Получение рекомендаций для домена
recommendations = agent.get_recommended_servers_for_domain("frontend")
print(recommendations['recommended'])  # ['brave-search', 'github', 'filesystem']

# Установка сервера
install_result = await agent.install_mcp_server("brave-search")

# Настройка Claude Desktop
from dataclasses import dataclass
from typing import Dict

servers_config = {
    "brave-search": MCPServerConfig(
        name="brave-search",
        command="npx",
        args=["@modelcontextprotocol/server-brave-search"],
        description="Поиск в интернете"
    )
}

config_result = await agent.configure_claude_desktop(servers_config)

# Валидация конфигурации
test_config = MCPServerConfig(
    name="test-server",
    command="npx",
    args=["@modelcontextprotocol/server-filesystem", "C:\\"],
    description="Тестовый сервер"
)
validation = await agent.validate_server_config(test_config)

# Создание нового сервера
create_result = await agent.create_server_from_template("my-server", "python")
```

### Пример: Настройка для Frontend разработки

```python
# Получаем рекомендации для frontend
agent = MCPConfigurationAgent(config_domain="frontend")
recommendations = agent.get_recommended_servers_for_domain("frontend")

# Устанавливаем рекомендованные серверы
for server_name in recommendations['recommended']:
    result = await agent.install_mcp_server(server_name)
    print(f"Установка {server_name}: {result['success']}")

# Настраиваем Claude Desktop
servers = {}
for server_name in recommendations['recommended']:
    servers[server_name] = MCPServerConfig(
        name=server_name,
        command="npx",
        args=[f"@modelcontextprotocol/server-{server_name}"],
        description=f"Сервер {server_name}"
    )

await agent.configure_claude_desktop(servers)
```

## Конфигурация доменов

Агент включает предустановленные конфигурации для различных доменов:

### Frontend
- **Рекомендованные**: brave-search, github, filesystem
- **Опциональные**: figma, linear, slack

### Backend
- **Рекомендованные**: postgres, github, filesystem
- **Опциональные**: docker, kubernetes, redis

### Fullstack
- **Рекомендованные**: postgres, github, filesystem, brave-search
- **Опциональные**: docker, slack, linear

### AI/ML
- **Рекомендованные**: brave-search, github, filesystem
- **Опциональные**: postgres, vector-db, jupyter

### Security
- **Рекомендованные**: github, filesystem
- **Опциональные**: kubernetes, docker, slack

## Структура файлов

```
mcp_configuration_agent/
├── agent.py                    # Основной агент
├── mcp_servers.json           # Конфигурации серверов
├── README.md                  # Документация
└── examples/                  # Примеры использования
    ├── frontend_setup.py      # Настройка для frontend
    ├── backend_setup.py       # Настройка для backend
    └── custom_server.py       # Создание кастомного сервера
```

## Переменные окружения

Для работы с различными серверами требуются соответствующие API ключи:

```bash
# Brave Search
BRAVE_API_KEY=your_brave_api_key

# GitHub
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

# PostgreSQL
POSTGRES_CONNECTION_STRING=postgresql://user:pass@host:port/db

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-token

# Linear
LINEAR_API_KEY=your_linear_api_key

# Figma
FIGMA_ACCESS_TOKEN=your_figma_token

# Redis
REDIS_URL=redis://localhost:6379

# Kubernetes
KUBECONFIG=/path/to/kubeconfig

# Vector DB
VECTOR_DB_URL=your_vector_db_url
```

## Примеры Claude Desktop конфигурации

После настройки агентом ваш `claude_desktop_config.json` будет выглядеть так:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "C:\\"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_api_key"
      }
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```

## Демонстрация

Запуск демо:

```bash
python agent.py
```

Это покажет:
1. Получение рекомендаций для fullstack разработки
2. Установку рекомендованного сервера
3. Валидацию конфигурации сервера

## Расширение

Для добавления новых серверов:

1. Добавьте конфигурацию в `mcp_servers.json`
2. Обновите `domain_configurations` в агенте
3. Создайте пример использования

---

**MCP Configuration Agent** обеспечивает универсальное и надежное управление MCP серверами для любых проектов и технологических стеков.