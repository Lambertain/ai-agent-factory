"""
Frontend MCP Configuration Setup Example

Конфигурация MCP серверов для фронтенд разработки
Включает серверы для UI компонентов, дизайн систем, тестирования интерфейсов
"""

from typing import Dict, List, Any
from pydantic import BaseModel

class FrontendMCPConfig(BaseModel):
    """Конфигурация MCP серверов для фронтенд проектов"""

    project_type: str = "frontend"
    framework: str = "react"  # react, vue, angular, svelte
    ui_library: str = "shadcn"  # shadcn, chakra, material, tailwind
    testing_framework: str = "jest"  # jest, vitest, cypress

    def get_mcp_servers(self) -> Dict[str, Any]:
        """Получить конфигурацию MCP серверов для фронтенда"""

        servers = {
            # Основные серверы для разработки
            "github": {
                "command": "uvx",
                "args": ["mcp-server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
                }
            },

            # UI компоненты и дизайн система
            "shadcn": {
                "command": "npx",
                "args": ["shadcn-mcp"],
                "env": {}
            } if self.ui_library == "shadcn" else None,

            # Puppeteer для E2E тестирования
            "puppeteer": {
                "command": "uvx",
                "args": ["mcp-server-puppeteer"],
                "env": {}
            },

            # Filesystem для работы с файлами
            "filesystem": {
                "command": "node",
                "args": ["/path/to/mcp-server-filesystem/dist/index.js", "./src", "./public"],
                "env": {}
            },

            # Fetch для работы с API и данными
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"],
                "env": {}
            }
        }

        # Добавляем специфичные для фреймворка серверы
        if self.framework == "react":
            servers["react_devtools"] = {
                "command": "npx",
                "args": ["react-mcp-server"],
                "env": {}
            }
        elif self.framework == "vue":
            servers["vue_devtools"] = {
                "command": "npx",
                "args": ["vue-mcp-server"],
                "env": {}
            }

        # Фильтруем None значения
        return {k: v for k, v in servers.items() if v is not None}

def generate_frontend_config(
    framework: str = "react",
    ui_library: str = "shadcn",
    testing_framework: str = "jest"
) -> Dict[str, Any]:
    """Сгенерировать конфигурацию для фронтенд проекта"""

    config = FrontendMCPConfig(
        framework=framework,
        ui_library=ui_library,
        testing_framework=testing_framework
    )

    return {
        "mcpServers": config.get_mcp_servers(),
        "project_info": {
            "type": "frontend",
            "framework": framework,
            "ui_library": ui_library,
            "testing_framework": testing_framework
        }
    }

# Примеры использования
if __name__ == "__main__":
    # React + Shadcn/ui + Jest
    react_config = generate_frontend_config("react", "shadcn", "jest")
    print("React конфигурация:", react_config)

    # Vue + Tailwind + Vitest
    vue_config = generate_frontend_config("vue", "tailwind", "vitest")
    print("Vue конфигурация:", vue_config)

    # Angular + Material + Karma
    angular_config = generate_frontend_config("angular", "material", "karma")
    print("Angular конфигурация:", angular_config)