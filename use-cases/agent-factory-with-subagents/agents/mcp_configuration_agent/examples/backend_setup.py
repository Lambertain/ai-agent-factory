"""
Backend MCP Configuration Setup Example

Конфигурация MCP серверов для бэкенд разработки
Включает серверы для API разработки, баз данных, мониторинга
"""

from typing import Dict, List, Any
from pydantic import BaseModel

class BackendMCPConfig(BaseModel):
    """Конфигурация MCP серверов для бэкенд проектов"""

    project_type: str = "backend"
    language: str = "python"  # python, node, go, rust, java
    framework: str = "fastapi"  # fastapi, django, express, gin, axum
    database: str = "postgresql"  # postgresql, mysql, mongodb, redis
    orm: str = "sqlalchemy"  # sqlalchemy, django-orm, prisma, gorm

    def get_mcp_servers(self) -> Dict[str, Any]:
        """Получить конфигурацию MCP серверов для бэкенда"""

        servers = {
            # Основные серверы для разработки
            "github": {
                "command": "uvx",
                "args": ["mcp-server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
                }
            },

            # Filesystem для работы с файлами проекта
            "filesystem": {
                "command": "node",
                "args": ["/path/to/mcp-server-filesystem/dist/index.js", "./src", "./api", "./models", "./migrations"],
                "env": {}
            },

            # Fetch для тестирования API и внешних интеграций
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
            }
        }

        # Добавляем специфичные для языка/фреймворка серверы
        if self.language == "python":
            if self.framework == "fastapi":
                servers["fastapi_tools"] = {
                    "command": "uvx",
                    "args": ["fastapi-mcp-server"],
                    "env": {}
                }
            elif self.framework == "django":
                servers["django_tools"] = {
                    "command": "uvx",
                    "args": ["django-mcp-server"],
                    "env": {}
                }

        elif self.language == "node":
            servers["node_tools"] = {
                "command": "npx",
                "args": ["node-mcp-server"],
                "env": {}
            }

        # Добавляем серверы для работы с базами данных
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

        # ORM специфичные серверы
        if self.orm == "prisma":
            servers["prisma"] = {
                "command": "npx",
                "args": ["prisma-mcp-server"],
                "env": {}
            }

        # Security сканер для бэкенда
        servers["security"] = {
            "command": "uvx",
            "args": ["mcp-security-agent"],
            "env": {}
        }

        return servers

def generate_backend_config(
    language: str = "python",
    framework: str = "fastapi",
    database: str = "postgresql",
    orm: str = "sqlalchemy"
) -> Dict[str, Any]:
    """Сгенерировать конфигурацию для бэкенд проекта"""

    config = BackendMCPConfig(
        language=language,
        framework=framework,
        database=database,
        orm=orm
    )

    return {
        "mcpServers": config.get_mcp_servers(),
        "project_info": {
            "type": "backend",
            "language": language,
            "framework": framework,
            "database": database,
            "orm": orm
        }
    }

# Примеры использования
if __name__ == "__main__":
    # Python + FastAPI + PostgreSQL + SQLAlchemy
    fastapi_config = generate_backend_config("python", "fastapi", "postgresql", "sqlalchemy")
    print("FastAPI конфигурация:", fastapi_config)

    # Node.js + Express + MongoDB + Prisma
    express_config = generate_backend_config("node", "express", "mongodb", "prisma")
    print("Express конфигурация:", express_config)

    # Python + Django + MySQL + Django ORM
    django_config = generate_backend_config("python", "django", "mysql", "django-orm")
    print("Django конфигурация:", django_config)