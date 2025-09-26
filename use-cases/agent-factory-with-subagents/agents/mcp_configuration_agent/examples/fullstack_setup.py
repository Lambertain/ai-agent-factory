"""
Fullstack MCP Configuration Setup Example

Конфигурация MCP серверов для полнофункциональных приложений
Включает серверы для фронтенда, бэкенда, баз данных, развертывания
"""

from typing import Dict, List, Any
from pydantic import BaseModel

class FullstackMCPConfig(BaseModel):
    """Конфигурация MCP серверов для fullstack проектов"""

    project_type: str = "fullstack"
    frontend_framework: str = "react"  # react, vue, angular, svelte
    backend_language: str = "python"   # python, node, go, rust
    backend_framework: str = "fastapi" # fastapi, django, express, gin
    database: str = "postgresql"       # postgresql, mysql, mongodb
    deployment: str = "docker"         # docker, vercel, netlify, aws

    def get_mcp_servers(self) -> Dict[str, Any]:
        """Получить полную конфигурацию MCP серверов для fullstack"""

        servers = {
            # Основные универсальные серверы
            "github": {
                "command": "uvx",
                "args": ["mcp-server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
                }
            },

            # Filesystem с расширенным доступом
            "filesystem": {
                "command": "node",
                "args": ["/path/to/mcp-server-filesystem/dist/index.js",
                        "./frontend", "./backend", "./shared", "./docs", "./deploy"],
                "env": {}
            },

            # Fetch для API тестирования и интеграций
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"],
                "env": {}
            },

            # Memory для кэширования и сессий
            "memory": {
                "command": "uvx",
                "args": ["mcp-server-memory"],
                "env": {}
            },

            # Puppeteer для E2E тестирования всего стека
            "puppeteer": {
                "command": "uvx",
                "args": ["mcp-server-puppeteer"],
                "env": {}
            },

            # Security сканер для всего проекта
            "security": {
                "command": "uvx",
                "args": ["mcp-security-agent"],
                "env": {}
            }
        }

        # Frontend специфичные серверы
        if self.frontend_framework == "react":
            servers["shadcn"] = {
                "command": "npx",
                "args": ["shadcn-mcp"],
                "env": {}
            }
        elif self.frontend_framework == "vue":
            servers["vue_tools"] = {
                "command": "npx",
                "args": ["vue-mcp-server"],
                "env": {}
            }

        # Backend специфичные серверы
        if self.backend_language == "python":
            if self.backend_framework == "fastapi":
                servers["fastapi_tools"] = {
                    "command": "uvx",
                    "args": ["fastapi-mcp-server"],
                    "env": {}
                }
            elif self.backend_framework == "django":
                servers["django_tools"] = {
                    "command": "uvx",
                    "args": ["django-mcp-server"],
                    "env": {}
                }

        # Database серверы
        if self.database == "postgresql":
            servers["postgresql"] = {
                "command": "uvx",
                "args": ["postgres-mcp-server"],
                "env": {
                    "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
                }
            }
        elif self.database == "mongodb":
            servers["mongodb"] = {
                "command": "uvx",
                "args": ["mongo-mcp-server"],
                "env": {
                    "MONGO_CONNECTION_STRING": "${MONGODB_URL}"
                }
            }

        # Deployment и DevOps серверы
        if self.deployment == "docker":
            servers["docker_tools"] = {
                "command": "uvx",
                "args": ["docker-mcp-server"],
                "env": {}
            }
        elif self.deployment == "aws":
            servers["aws_tools"] = {
                "command": "uvx",
                "args": ["aws-mcp-server"],
                "env": {
                    "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
                    "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
                    "AWS_REGION": "${AWS_REGION}"
                }
            }

        # Context управление для больших проектов
        servers["context7"] = {
            "command": "npx",
            "args": ["context7-mcp"],
            "env": {}
        }

        return servers

def generate_fullstack_config(
    frontend_framework: str = "react",
    backend_language: str = "python",
    backend_framework: str = "fastapi",
    database: str = "postgresql",
    deployment: str = "docker"
) -> Dict[str, Any]:
    """Сгенерировать конфигурацию для fullstack проекта"""

    config = FullstackMCPConfig(
        frontend_framework=frontend_framework,
        backend_language=backend_language,
        backend_framework=backend_framework,
        database=database,
        deployment=deployment
    )

    return {
        "mcpServers": config.get_mcp_servers(),
        "project_info": {
            "type": "fullstack",
            "frontend_framework": frontend_framework,
            "backend_language": backend_language,
            "backend_framework": backend_framework,
            "database": database,
            "deployment": deployment
        },
        "recommended_workflow": {
            "development": [
                "1. Запустить backend сервер",
                "2. Запустить frontend dev server",
                "3. Настроить hot reload для обеих частей",
                "4. Использовать Puppeteer для E2E тестирования"
            ],
            "deployment": [
                "1. Собрать frontend production build",
                "2. Создать Docker контейнеры",
                "3. Запустить миграции базы данных",
                "4. Развернуть с помощью выбранной платформы"
            ]
        }
    }

# Примеры использования
if __name__ == "__main__":
    # MERN Stack (React + Node + MongoDB)
    mern_config = generate_fullstack_config(
        frontend_framework="react",
        backend_language="node",
        backend_framework="express",
        database="mongodb",
        deployment="docker"
    )
    print("MERN Stack конфигурация:", mern_config)

    # Python Fullstack (React + FastAPI + PostgreSQL)
    python_fullstack = generate_fullstack_config(
        frontend_framework="react",
        backend_language="python",
        backend_framework="fastapi",
        database="postgresql",
        deployment="aws"
    )
    print("Python Fullstack конфигурация:", python_fullstack)

    # Vue + Django Stack
    vue_django = generate_fullstack_config(
        frontend_framework="vue",
        backend_language="python",
        backend_framework="django",
        database="postgresql",
        deployment="docker"
    )
    print("Vue + Django конфигурация:", vue_django)