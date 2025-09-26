"""
Settings for Psychology Content Orchestrator Agent
Настройки для агента-оркестратора психологического контента
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class OrchestratorSettings(BaseSettings):
    """
    Настройки приложения для Psychology Content Orchestrator
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Основные параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Название модели")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )

    # Параметры оркестрации
    project_name: str = Field(default="New Psychology Project", description="Название проекта")
    project_description: str = Field(default="Psychology testing project", description="Описание проекта")
    test_topics: List[str] = Field(default_factory=lambda: ["general"], description="Темы тестов")
    target_audience: str = Field(default="general", description="Целевая аудитория")
    complexity_level: str = Field(default="standard", description="Уровень сложности")
    target_language: str = Field(default="ukrainian", description="Целевой язык")

    # Управление workflow
    orchestration_level: str = Field(default="full_pipeline", description="Уровень оркестрации")
    workflow_complexity: str = Field(default="standard", description="Сложность workflow")
    enable_parallel_execution: bool = Field(default=True, description="Параллельное выполнение")
    max_parallel_agents: int = Field(default=3, description="Максимум параллельных агентов")
    coordination_timeout: int = Field(default=300, description="Таймаут координации (сек)")

    # Качественные гейты
    patternshift_threshold: float = Field(default=0.85, description="Порог PatternShift методологии")
    clinical_accuracy_threshold: float = Field(default=0.90, description="Порог клинической точности")
    vak_adaptations_threshold: float = Field(default=0.80, description="Порог VAK адаптаций")
    language_quality_threshold: float = Field(default=0.85, description="Порог качества языка")

    # Мониторинг и отчетность
    enable_progress_tracking: bool = Field(default=True, description="Отслеживание прогресса")
    enable_detailed_logging: bool = Field(default=True, description="Детальное логирование")
    report_frequency: str = Field(default="per_stage", description="Частота отчетов")

    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта Archon"
    )
    enable_rag_search: bool = Field(default=True, description="Использовать RAG поиск")
    rag_match_count: int = Field(default=5, description="Количество результатов RAG")

    def get_agent_workflow(self) -> Dict[str, Dict]:
        """Получить конфигурацию workflow агентов"""
        if self.complexity_level == "simple":
            return {
                "content_architect": {
                    "role": "test_creation",
                    "priority": 1,
                    "dependencies": [],
                    "outputs": ["basic_tests"]
                },
                "quality_guardian": {
                    "role": "basic_validation",
                    "priority": 2,
                    "dependencies": ["content_architect"],
                    "outputs": ["validation_report"]
                }
            }
        elif self.complexity_level == "standard":
            return {
                "content_architect": {
                    "role": "test_creation",
                    "priority": 1,
                    "dependencies": [],
                    "outputs": ["psychological_tests"]
                },
                "test_generator": {
                    "role": "test_instantiation",
                    "priority": 2,
                    "dependencies": ["content_architect"],
                    "outputs": ["test_instances"]
                },
                "quality_guardian": {
                    "role": "quality_assurance",
                    "priority": 3,
                    "dependencies": ["content_architect", "test_generator"],
                    "outputs": ["quality_reports"]
                },
                "transformation_planner": {
                    "role": "program_creation",
                    "priority": 4,
                    "dependencies": ["content_architect", "quality_guardian"],
                    "outputs": ["transformation_programs"]
                }
            }
        elif self.complexity_level in ["advanced", "expert"]:
            return {
                "research_agent": {
                    "role": "research",
                    "priority": 1,
                    "dependencies": [],
                    "outputs": ["research_data"]
                },
                "content_architect": {
                    "role": "test_creation",
                    "priority": 2,
                    "dependencies": ["research_agent"],
                    "outputs": ["psychological_tests"]
                },
                "test_generator": {
                    "role": "test_instantiation",
                    "priority": 3,
                    "dependencies": ["content_architect"],
                    "outputs": ["test_instances"]
                },
                "quality_guardian": {
                    "role": "comprehensive_qa",
                    "priority": 4,
                    "dependencies": ["content_architect", "test_generator"],
                    "outputs": ["detailed_quality_reports"]
                },
                "transformation_planner": {
                    "role": "program_creation",
                    "priority": 5,
                    "dependencies": ["content_architect", "quality_guardian"],
                    "outputs": ["transformation_programs"]
                }
            }
        else:
            # Default workflow
            return self.get_agent_workflow()

    def get_quality_gates(self) -> Dict[str, Dict]:
        """Получить конфигурацию качественных гейтов"""
        base_gates = {
            "patternshift_compliance": {
                "threshold": self.patternshift_threshold,
                "required": True,
                "validator": "quality_guardian"
            },
            "language_quality": {
                "threshold": self.language_quality_threshold,
                "required": True,
                "validator": "quality_guardian"
            }
        }

        if self.complexity_level in ["standard", "advanced", "expert"]:
            base_gates.update({
                "clinical_accuracy": {
                    "threshold": self.clinical_accuracy_threshold,
                    "required": True,
                    "validator": "quality_guardian"
                },
                "vak_adaptations": {
                    "threshold": self.vak_adaptations_threshold,
                    "required": True,
                    "validator": "content_architect"
                }
            })

        if self.complexity_level == "expert":
            base_gates.update({
                "research_quality": {
                    "threshold": 0.85,
                    "required": True,
                    "validator": "research_agent"
                },
                "transformation_viability": {
                    "threshold": 0.80,
                    "required": True,
                    "validator": "transformation_planner"
                }
            })

        return base_gates

    def get_deliverables(self) -> Dict[str, Any]:
        """Получить ожидаемые deliverables проекта"""
        base_deliverables = {
            "psychological_tests": {
                "count": len(self.test_topics),
                "format": "patternshift_compliant",
                "validation_required": True
            },
            "quality_reports": {
                "count": 1,
                "format": "comprehensive",
                "validation_required": False
            }
        }

        if self.complexity_level in ["standard", "advanced", "expert"]:
            base_deliverables.update({
                "test_instances": {
                    "count": len(self.test_topics) * 2,
                    "format": "multiple_variants",
                    "validation_required": True
                },
                "transformation_programs": {
                    "count": len(self.test_topics),
                    "format": "behavioral_change_focused",
                    "validation_required": True
                }
            })

        if self.complexity_level in ["advanced", "expert"]:
            base_deliverables.update({
                "research_reports": {
                    "count": len(self.test_topics),
                    "format": "comprehensive_analysis",
                    "validation_required": True
                },
                "documentation": {
                    "count": 1,
                    "format": "complete_project_docs",
                    "validation_required": False
                }
            })

        return base_deliverables

    def get_agent_priority_matrix(self) -> Dict[str, int]:
        """Получить матрицу приоритетов агентов"""
        if self.complexity_level == "simple":
            return {
                "psychology_content_architect": 1,
                "psychology_quality_guardian": 2
            }
        elif self.complexity_level == "standard":
            return {
                "psychology_content_architect": 1,
                "psychology_test_generator": 2,
                "psychology_quality_guardian": 3,
                "psychology_transformation_planner": 4
            }
        else:  # advanced, expert
            return {
                "psychology_research_agent": 1,
                "psychology_content_architect": 2,
                "psychology_test_generator": 3,
                "psychology_quality_guardian": 4,
                "psychology_transformation_planner": 5
            }

    def get_parallel_execution_groups(self) -> List[List[str]]:
        """Получить группы агентов для параллельного выполнения"""
        if not self.enable_parallel_execution:
            # Последовательное выполнение
            agents = list(self.get_agent_priority_matrix().keys())
            return [[agent] for agent in agents]

        if self.complexity_level == "simple":
            return [
                ["psychology_content_architect"],
                ["psychology_quality_guardian"]
            ]
        elif self.complexity_level == "standard":
            return [
                ["psychology_content_architect"],
                ["psychology_test_generator"],
                ["psychology_quality_guardian", "psychology_transformation_planner"]
            ]
        else:  # advanced, expert
            return [
                ["psychology_research_agent"],
                ["psychology_content_architect"],
                ["psychology_test_generator"],
                ["psychology_quality_guardian", "psychology_transformation_planner"]
            ]

    def get_coordination_strategy(self) -> Dict[str, Any]:
        """Получить стратегию координации"""
        return {
            "execution_mode": "parallel" if self.enable_parallel_execution else "sequential",
            "max_parallel_agents": self.max_parallel_agents,
            "timeout": self.coordination_timeout,
            "retry_policy": {
                "max_retries": 2,
                "retry_delay": 30,
                "retry_on_failure": True
            },
            "quality_gates": self.get_quality_gates(),
            "monitoring": {
                "progress_tracking": self.enable_progress_tracking,
                "detailed_logging": self.enable_detailed_logging,
                "report_frequency": self.report_frequency
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать настройки в словарь"""
        return {
            "project_info": {
                "name": self.project_name,
                "description": self.project_description,
                "topics": self.test_topics,
                "audience": self.target_audience,
                "complexity": self.complexity_level,
                "language": self.target_language
            },
            "orchestration": {
                "level": self.orchestration_level,
                "workflow_complexity": self.workflow_complexity,
                "parallel_execution": self.enable_parallel_execution,
                "max_parallel_agents": self.max_parallel_agents
            },
            "quality": {
                "patternshift_threshold": self.patternshift_threshold,
                "clinical_accuracy_threshold": self.clinical_accuracy_threshold,
                "vak_adaptations_threshold": self.vak_adaptations_threshold,
                "language_quality_threshold": self.language_quality_threshold
            },
            "monitoring": {
                "progress_tracking": self.enable_progress_tracking,
                "detailed_logging": self.enable_detailed_logging,
                "report_frequency": self.report_frequency
            }
        }

def load_orchestrator_settings() -> OrchestratorSettings:
    """
    Загрузить настройки и проверить наличие переменных
    """
    try:
        return OrchestratorSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки оркестратора: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e

# Предустановленные конфигурации

SIMPLE_ORCHESTRATION_CONFIG = {
    "orchestration_level": "targeted",
    "workflow_complexity": "simple",
    "complexity_level": "simple",
    "enable_parallel_execution": False,
    "patternshift_threshold": 0.70,
    "clinical_accuracy_threshold": 0.75,
}

STANDARD_ORCHESTRATION_CONFIG = {
    "orchestration_level": "full_pipeline",
    "workflow_complexity": "standard",
    "complexity_level": "standard",
    "enable_parallel_execution": True,
    "max_parallel_agents": 2,
    "patternshift_threshold": 0.85,
    "clinical_accuracy_threshold": 0.90,
}

ADVANCED_ORCHESTRATION_CONFIG = {
    "orchestration_level": "full_pipeline",
    "workflow_complexity": "advanced",
    "complexity_level": "advanced",
    "enable_parallel_execution": True,
    "max_parallel_agents": 3,
    "patternshift_threshold": 0.90,
    "clinical_accuracy_threshold": 0.95,
    "enable_detailed_logging": True,
}

EXPERT_ORCHESTRATION_CONFIG = {
    "orchestration_level": "full_pipeline",
    "workflow_complexity": "expert",
    "complexity_level": "expert",
    "enable_parallel_execution": True,
    "max_parallel_agents": 3,
    "coordination_timeout": 600,
    "patternshift_threshold": 0.95,
    "clinical_accuracy_threshold": 0.98,
    "vak_adaptations_threshold": 0.90,
    "language_quality_threshold": 0.95,
    "enable_detailed_logging": True,
    "report_frequency": "per_task"
}