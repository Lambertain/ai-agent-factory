"""
Dependencies для Psychology Research Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ResearchDependencies:
    """Зависимости для исследователя психологических методик"""

    # Основные настройки
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    project_path: str = ""

    # Исследовательские параметры
    research_domain: str = "general"  # anxiety, depression, trauma, relationships, etc.
    target_population: str = "adults"  # adults, adolescents, children, elderly, etc.
    evidence_standard: str = "moderate"  # low, moderate, high, expert
    research_question_type: str = "effectiveness"  # effectiveness, safety, comparison, mechanism

    # Параметры поиска литературы
    search_parameters: Dict[str, Any] = field(default_factory=lambda: {
        "databases": ["pubmed", "psycinfo", "cochrane"],
        "years": "2010-2024",
        "languages": ["en", "ru"],
        "study_types": ["rct", "meta-analysis", "systematic_review"],
        "max_results": 50
    })

    # Критерии качества исследований
    quality_criteria: Dict[str, Any] = field(default_factory=lambda: {
        "minimum_sample_size": 30,
        "require_control_group": True,
        "require_randomization": True,
        "require_blinding": False,
        "maximum_dropout_rate": 0.3,
        "require_intention_to_treat": True
    })

    # Статистические параметры
    statistical_parameters: Dict[str, Any] = field(default_factory=lambda: {
        "alpha_level": 0.05,
        "power": 0.80,
        "effect_size_threshold": 0.2,
        "heterogeneity_threshold": 0.75,
        "publication_bias_tests": ["egger", "begg"]
    })

    # RAG конфигурация
    agent_name: str = "psychology_research"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "psychology-research",
        "evidence-based",
        "meta-analysis",
        "systematic-review"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Интеграция с другими агентами
    enable_orchestrator_integration: bool = True
    enable_architect_collaboration: bool = True
    enable_quality_review: bool = True

    def __post_init__(self):
        """Инициализация и валидация конфигурации"""
        # Добавление доменных тегов
        if self.research_domain != "general":
            self.knowledge_tags.append(self.research_domain)

        # Добавление популяционных тегов
        if self.target_population != "adults":
            self.knowledge_tags.append(f"population-{self.target_population}")

        # Валидация параметров
        self._validate_search_parameters()
        self._validate_quality_criteria()

    def _validate_search_parameters(self):
        """Валидация параметров поиска"""
        valid_databases = ["pubmed", "psycinfo", "cochrane", "embase", "web_of_science"]
        self.search_parameters["databases"] = [
            db for db in self.search_parameters.get("databases", [])
            if db in valid_databases
        ]

        if not self.search_parameters["databases"]:
            self.search_parameters["databases"] = ["pubmed", "psycinfo"]

        if self.search_parameters.get("max_results", 0) > 500:
            self.search_parameters["max_results"] = 500

    def _validate_quality_criteria(self):
        """Валидация критериев качества"""
        if self.quality_criteria.get("minimum_sample_size", 0) < 10:
            self.quality_criteria["minimum_sample_size"] = 30

        if self.quality_criteria.get("maximum_dropout_rate", 1) > 0.5:
            self.quality_criteria["maximum_dropout_rate"] = 0.3

    def get_search_strategy(self) -> Dict[str, Any]:
        """Получить стратегию поиска"""
        return {
            "research_question": f"{self.research_question_type} in {self.research_domain}",
            "population": self.target_population,
            "databases": self.search_parameters["databases"],
            "inclusion_criteria": self._get_inclusion_criteria(),
            "exclusion_criteria": self._get_exclusion_criteria(),
            "search_terms": self._generate_search_terms()
        }

    def _get_inclusion_criteria(self) -> List[str]:
        """Получить критерии включения"""
        criteria = [
            "Peer-reviewed studies",
            f"Published {self.search_parameters['years']}",
            f"Population: {self.target_population}"
        ]

        if self.quality_criteria["require_randomization"]:
            criteria.append("Randomized controlled trials")

        return criteria

    def _get_exclusion_criteria(self) -> List[str]:
        """Получить критерии исключения"""
        return [
            "Case reports",
            "Editorial comments",
            "Non-human studies",
            f"Sample size < {self.quality_criteria['minimum_sample_size']}"
        ]

    def _generate_search_terms(self) -> Dict[str, List[str]]:
        """Генерировать поисковые термины"""
        domain_terms = {
            "anxiety": ["anxiety", "worry", "fear", "panic", "phobia"],
            "depression": ["depression", "depressive", "mood", "melancholia"],
            "trauma": ["trauma", "PTSD", "stress disorder", "traumatic"],
            "relationships": ["couples", "marriage", "relationship", "family"]
        }

        intervention_terms = [
            "psychotherapy", "cognitive", "behavioral", "therapy",
            "intervention", "treatment", "counseling"
        ]

        population_terms = {
            "adults": ["adult", "grown-up"],
            "adolescents": ["adolescent", "teenager", "youth"],
            "children": ["child", "pediatric", "kid"],
            "elderly": ["elderly", "geriatric", "older adult"]
        }

        return {
            "domain": domain_terms.get(self.research_domain, [self.research_domain]),
            "intervention": intervention_terms,
            "population": population_terms.get(self.target_population, [self.target_population])
        }

def get_research_config(
    domain: str = "general",
    population: str = "adults",
    evidence_standard: str = "moderate",
    **kwargs
) -> ResearchDependencies:
    """Фабрика для создания конфигурации исследователя"""

    # Настройка стандартов доказательности
    quality_standards = {
        "low": {
            "minimum_sample_size": 20,
            "require_control_group": False,
            "require_randomization": False
        },
        "moderate": {
            "minimum_sample_size": 30,
            "require_control_group": True,
            "require_randomization": True
        },
        "high": {
            "minimum_sample_size": 50,
            "require_control_group": True,
            "require_randomization": True,
            "require_blinding": True,
            "require_intention_to_treat": True
        },
        "expert": {
            "minimum_sample_size": 100,
            "require_control_group": True,
            "require_randomization": True,
            "require_blinding": True,
            "require_intention_to_treat": True,
            "maximum_dropout_rate": 0.2
        }
    }

    quality_criteria = quality_standards.get(evidence_standard, quality_standards["moderate"])

    return ResearchDependencies(
        research_domain=domain,
        target_population=population,
        evidence_standard=evidence_standard,
        quality_criteria=quality_criteria,
        **kwargs
    )