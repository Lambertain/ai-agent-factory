# -*- coding: utf-8 -*-
"""
Зависимости для Universal Domain Knowledge Extractor Agent
Универсальная конфигурация для работы с любыми доменами знаний
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Матрица компетенций агентов для делегирования
AGENT_COMPETENCIES = {
    "security_audit": [
        "безопасность", "уязвимости", "compliance", "аудит безопасности",
        "secrets detection", "penetration testing", "OWASP", "CVE"
    ],
    "rag_agent": [
        "поиск информации", "семантический анализ", "knowledge base",
        "document retrieval", "информационный поиск", "текстовый анализ"
    ],
    "uiux_enhancement": [
        "дизайн", "пользовательский интерфейс", "accessibility", "UX/UI",
        "компонентные библиотеки", "дизайн системы", "пользовательский опыт"
    ],
    "performance_optimization": [
        "производительность", "оптимизация", "скорость", "memory usage",
        "cpu optimization", "caching", "load testing", "профилирование"
    ]
}

AGENT_ASSIGNEE_MAP = {
    "security_audit": "Security Audit Agent",
    "rag_agent": "Archon Analysis Lead",
    "uiux_enhancement": "Archon UI/UX Designer",
    "performance_optimization": "Performance Optimization Agent"
}

@dataclass
class DomainKnowledgeExtractorDependencies:
    """
    Универсальные зависимости для извлечения знаний из любых доменов.

    Поддерживает психологию, астрологию, нумерологию, бизнес и другие области.
    """

    # Основные настройки
    api_key: str
    project_path: str = ""

    # Универсальная конфигурация домена
    domain_type: str = "psychology"  # psychology, astrology, numerology, business, etc.
    project_type: str = "transformation_platform"  # educational_system, consultancy, etc.
    framework: str = "pydantic_ai"  # fastapi, django, etc.

    # RAG конфигурация
    agent_name: str = "universal_domain_knowledge_extractor"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "domain-knowledge", "knowledge-extraction", "agent-knowledge", "pydantic-ai"
    ])
    knowledge_domain: str | None = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"

    # Доменно-специфичные настройки
    domain_config: Dict[str, Any] = field(default_factory=dict)

    # Конфигурация извлечения знаний
    knowledge_sources: List[str] = field(default_factory=list)
    output_format: str = "modular"  # modular, structured, narrative
    validation_level: str = "scientific"  # basic, scientific, expert

    # Локализация
    primary_language: str = "ukrainian"  # ukrainian, polish, english
    secondary_languages: List[str] = field(default_factory=lambda: ["polish", "english"])

    def __post_init__(self):
        """Инициализация конфигурации после создания объекта."""
        # Настройка доменно-специфичных конфигураций
        if not self.domain_config:
            self.domain_config = self._get_domain_config()

        # Обновление тегов знаний с учетом домена
        domain_tag = self.domain_type.replace("_", "-")
        if domain_tag not in self.knowledge_tags:
            self.knowledge_tags.append(domain_tag)

        # Настройка источников знаний по умолчанию
        if not self.knowledge_sources:
            self.knowledge_sources = self._get_default_knowledge_sources()

    def _get_domain_config(self) -> Dict[str, Any]:
        """Получить конфигурацию для конкретного домена."""
        domain_configs = {
            "psychology": {
                "scientific_validation": True,
                "clinical_standards": True,
                "therapy_approaches": ["CBT", "TA", "Ericksonian", "NLP"],
                "test_types": ["personality", "clinical", "behavioral"],
                "cultural_adaptation": True
            },
            "astrology": {
                "house_systems": ["Placidus", "Koch", "Equal"],
                "planet_aspects": True,
                "traditional_modern": "both",
                "cultural_systems": ["Western", "Vedic", "Chinese"],
                "calculation_precision": "high"
            },
            "numerology": {
                "calculation_methods": ["Pythagorean", "Chaldean", "Kabbalah"],
                "name_analysis": True,
                "birth_date_analysis": True,
                "compatibility_analysis": True,
                "cultural_variants": True
            },
            "business": {
                "frameworks": ["SWOT", "Porter", "Lean", "Agile"],
                "metrics_focus": True,
                "industry_adaptation": True,
                "scalability_analysis": True,
                "market_research": True
            }
        }
        return domain_configs.get(self.domain_type, {})

    def _get_default_knowledge_sources(self) -> List[str]:
        """Получить источники знаний по умолчанию для домена."""
        source_mapping = {
            "psychology": [
                "scientific_publications",
                "clinical_studies",
                "therapy_manuals",
                "test_methodologies"
            ],
            "astrology": [
                "classical_texts",
                "modern_techniques",
                "cultural_traditions",
                "calculation_methods"
            ],
            "numerology": [
                "traditional_systems",
                "calculation_methods",
                "cultural_variants",
                "compatibility_matrices"
            ],
            "business": [
                "business_frameworks",
                "case_studies",
                "market_research",
                "best_practices"
            ]
        }
        return source_mapping.get(self.domain_type, ["general_knowledge"])

    def should_delegate(self, task_keywords: List[str], current_agent_type: str = "domain_knowledge") -> Optional[str]:
        """Определить нужно ли делегировать задачу и кому."""
        for agent_type, competencies in AGENT_COMPETENCIES.items():
            if agent_type != current_agent_type:
                overlap = set(task_keywords) & set(competencies)
                if len(overlap) >= 2:  # Значительное пересечение компетенций
                    return agent_type
        return None

    def get_domain_specific_prompt_variables(self) -> Dict[str, str]:
        """Получить переменные для адаптации промптов под домен."""
        return {
            "domain_type": self.domain_type,
            "project_type": self.project_type,
            "framework": self.framework,
            "primary_language": self.primary_language,
            "validation_level": self.validation_level,
            "output_format": self.output_format
        }

def load_dependencies(
    domain_type: str = "psychology",
    project_type: str = "transformation_platform",
    framework: str = "pydantic_ai"
) -> DomainKnowledgeExtractorDependencies:
    """
    Загрузить зависимости для Universal Domain Knowledge Extractor Agent.

    Args:
        domain_type: Тип домена для извлечения знаний
        project_type: Тип проекта
        framework: Технологический фреймворк

    Returns:
        Настроенные зависимости агента
    """
    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("LLM_API_KEY не найден в переменных окружения")

    return DomainKnowledgeExtractorDependencies(
        api_key=api_key,
        project_path=os.getenv("PROJECT_PATH", ""),
        domain_type=domain_type,
        project_type=project_type,
        framework=framework,
        knowledge_domain=os.getenv("KNOWLEDGE_DOMAIN"),
        primary_language=os.getenv("PRIMARY_LANGUAGE", "ukrainian")
    )