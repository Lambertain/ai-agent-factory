# Довідник MCP серверів

## 📡 Доступні MCP сервери

Повний список MCP серверів, доступних для використання агентами.

---

### 🎯 Archon MCP Server (mcp__archon__)
**Назначение:** Управление проектами, задачами, документами

**Основные инструменты:**
- `find_projects()` / `manage_project()` - управление проектами
- `find_tasks()` / `manage_task()` - управление задачами
- `find_documents()` / `manage_document()` - управление документами
- `rag_search_knowledge_base()` - поиск в базе знаний
- `rag_search_code_examples()` - поиск примеров кода

**Когда использовать:** ВСЕГДА для создания задач, поиска информации, управления контекстом

---

### 🐙 GitHub MCP Server (mcp__github__)
**Назначение:** Работа с GitHub репозиториями

**Основные инструменты:**
- `get_file_contents()` / `create_or_update_file()` - файловые операции
- `create_pull_request()` / `list_pull_requests()` - работа с PR
- `create_issue()` / `list_issues()` - работа с issues
- `search_repositories()` / `search_code()` - поиск

**Когда использовать:** Для работы с удалёнными репозиториями, code review, создания PR

---

### 📂 Filesystem MCP Server (mcp__filesystem__)
**Назначение:** Расширенные файловые операции

**Основные инструменты:**
- `read_file()` / `read_multiple_files()` / `write_file()` / `edit_file()`
- `list_directory()` / `directory_tree()` / `search_files()`
- `create_directory()` / `move_file()`

**Когда использовать:** Для пакетных операций с файлами, сложной навигации

---

### 🗄️ PostgreSQL MCP Server (mcp__postgres__)
**Назначение:** Работа с PostgreSQL базами данных

**Основные инструменты:**
- `query()` / `executeSafeQuery()` - выполнение SQL
- `list_tables()` / `describe_table()` / `get_constraints()`
- `list_schemas()` / `list_indexes()` / `get_table_stats()`

**Когда использовать:** Для работы с PostgreSQL БД, анализа схемы, оптимизации запросов

---

### 🌐 Puppeteer/Test-Gen MCP Servers (mcp__puppeteer__, mcp__test-gen__)
**Назначение:** Автоматизация браузера, тестирование UI

**Основные инструменты:**
- `navigate()` / `screenshot()` / `click()` / `fill()` / `evaluate()`
- `start_codegen_session()` / `end_codegen_session()` - генерация тестов
- `playwright_*()` - Playwright операции

**Когда использовать:** Для UI тестирования, скриншотов, автоматизации браузера

---

### 🎨 Shadcn MCP Server (mcp__shadcn__)
**Назначение:** Работа с Shadcn UI компонентами

**Основные инструменты:**
- `get_component()` / `list_components()` / `get_component_metadata()`
- `get_component_demo()` / `get_block()` / `list_blocks()`

**Когда использовать:** При работе с Shadcn UI, создании компонентов

---

### 🔍 Context7 MCP Server (mcp__context7__)
**Назначение:** Получение актуальной документации библиотек

**Основные инструменты:**
- `resolve-library-id()` - поиск библиотеки
- `get-library-docs()` - получение документации

**Когда использовать:** Для получения up-to-date документации внешних библиотек

---

### 🚂 Railway MCP Server (mcp__railway__)
**Назначение:** Деплой и управление на Railway

**Основные инструменты:**
- `project_*()` / `service_*()` / `deployment_*()` - управление проектами
- `domain_*()` / `tcp_proxy_*()` - настройка доменов и прокси
- `variable_*()` - управление переменными окружения

**Когда использовать:** Для деплоя на Railway, настройки инфраструктуры

---

### 🔒 Security Scan MCP Server (mcp__security-scan__)
**Назначение:** Сканирование безопасности (RAD Security)

**Основные инструменты:**
- `list_containers()` / `list_images()` / `list_cve_*()` - анализ контейнеров
- `list_k8s_resources()` / `list_clusters()` - работа с Kubernetes
- `list_security_findings()` / `get_cve()` - анализ уязвимостей

**Когда использовать:** Для security аудита, анализа уязвимостей, CVE

---

### 🗂️ SQLite MCP Server (mcp__sqlite__)
**Назначение:** Работа с SQLite базами данных

**Основные инструменты:**
- `executeQuery()` / `executeSafeQuery()` - выполнение SQL

**Когда использовать:** Для работы с SQLite БД

---

### 🌐 Web Fetch/Image Fetch MCP Servers (mcp__fetch__)
**Назначение:** Загрузка веб-контента и изображений

**Основные инструменты:**
- `imageFetch()` - загрузка страниц с извлечением изображений

**Когда использовать:** Для загрузки контента с веб-страниц, работы с изображениями

---

### 🧪 API Test MCP Server (mcp__api-test__)
**Назначение:** Тестирование API (Hacker News API)

**Основные инструменты:**
- `hn_*()` - работа с Hacker News API

**Когда использовать:** Для тестирования API, примеров работы с внешними API

---

### 🌐 Chrome DevTools MCP Server (mcp__chrome-devtools__)
**Назначение:** Автоматизация через Chrome DevTools Protocol

**Основные инструменты:**
- `navigate_page()` / `click()` / `fill()` / `take_screenshot()`
- `list_console_messages()` / `list_network_requests()`
- `performance_*()` / `emulate_*()` - тестирование производительности

**Когда использовать:** Для детального анализа веб-страниц, профилирования

---

### 🧠 Sequential Thinking MCP Server (mcp__sequential-thinking__)
**Назначение:** Структурированный анализ сложных проблем

**Основные инструменты:**
- `sequentialthinking()` - пошаговый анализ с возможностью ревизии

**Когда использовать:** Для сложных проблем, требующих глубокого анализа

---

### 😤 Code Review MCP Server (mcp__code-review__)
**Назначение:** Строгий code review

**Основные инструменты:**
- `review-code()` - критический анализ кода

**Когда использовать:** Для получения критической оценки кода

---

**Версия:** 1.0
**Дата:** 2025-10-14
**Автор:** Archon Blueprint Architect
