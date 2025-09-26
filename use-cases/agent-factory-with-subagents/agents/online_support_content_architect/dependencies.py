"""
Dependencies для Psychology Content Architect Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ArchitectDependencies:
    """Зависимости для архитектора психологических программ"""

    # Основные настройки
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    project_path: str = ""

    # Специализация архитектора
    psychological_domain: str = "general"  # anxiety, depression, relationships, trauma, etc.
    target_population: str = "adults"  # adults, adolescents, children, couples, families
    program_type: str = "therapeutic"  # therapeutic, educational, preventive, developmental
    complexity_level: str = "medium"  # low, medium, high

    # Ограничения и требования
    delivery_constraints: Dict[str, Any] = field(default_factory=lambda: {
        "format": "hybrid",  # online, offline, hybrid, self-guided
        "duration": 8,  # недели
        "session_length": 60,  # минуты
        "resources": "standard"  # minimal, standard, comprehensive
    })

    # Архитектурные предпочтения
    architectural_style: str = "modular"  # modular, linear, spiral, adaptive
    evidence_base: str = "high"  # Уровень требований к доказательной базе
    flexibility_requirement: str = "moderate"  # low, moderate, high

    # RAG конфигурация
    agent_name: str = "psychology_content_architect"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "psychology-architecture",
        "program-design",
        "therapeutic-structure",
        "evidence-based"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Интеграция с другими агентами
    enable_orchestrator_integration: bool = True
    enable_research_collaboration: bool = True
    enable_quality_review: bool = True

    def __post_init__(self):
        """Инициализация и валидация конфигурации"""
        # Автоматическое определение тегов на основе домена
        if self.psychological_domain and self.psychological_domain != "general":
            if self.psychological_domain not in self.knowledge_tags:
                self.knowledge_tags.append(self.psychological_domain)

        # Добавление тегов для целевой аудитории
        if self.target_population not in self.knowledge_tags:
            self.knowledge_tags.append(f"population-{self.target_population}")

        # Валидация ограничений
        self._validate_constraints()

    def _validate_constraints(self):
        """Валидация архитектурных ограничений"""
        valid_formats = ["online", "offline", "hybrid", "self-guided"]
        if self.delivery_constraints.get("format") not in valid_formats:
            self.delivery_constraints["format"] = "hybrid"

        if self.delivery_constraints.get("duration", 0) < 1:
            self.delivery_constraints["duration"] = 8

        if self.delivery_constraints.get("session_length", 0) < 15:
            self.delivery_constraints["session_length"] = 60

    def get_design_parameters(self) -> Dict[str, Any]:
        """Получить параметры для проектирования архитектуры"""
        return {
            "domain": self.psychological_domain,
            "population": self.target_population,
            "type": self.program_type,
            "complexity": self.complexity_level,
            "style": self.architectural_style,
            "constraints": self.delivery_constraints,
            "flexibility": self.flexibility_requirement,
            "evidence_requirement": self.evidence_base
        }

    def should_collaborate_with(self, agent_type: str) -> bool:
        """Определить необходимость сотрудничества с другим агентом"""
        collaboration_rules = {
            "orchestrator": self.enable_orchestrator_integration,
            "research": self.enable_research_collaboration and self.evidence_base == "high",
            "quality": self.enable_quality_review,
            "test_generator": self.program_type in ["therapeutic", "assessment"],
            "nlp_generator": self.program_type in ["self-help", "educational"]
        }
        return collaboration_rules.get(agent_type, False)

def get_architect_config(
    domain: str = "general",
    population: str = "adults",
    program_type: str = "therapeutic",
    **kwargs
) -> ArchitectDependencies:
    """Фабрика для создания конфигурации архитектора"""

    # Определение сложности на основе домена
    complexity_map = {
        "trauma": "high",
        "personality": "high",
        "psychosis": "high",
        "anxiety": "medium",
        "depression": "medium",
        "relationships": "medium",
        "stress": "low",
        "wellness": "low",
        "prevention": "low"
    }

    complexity = complexity_map.get(domain, "medium")

    # Определение архитектурного стиля
    style_map = {
        "therapeutic": "modular",
        "educational": "linear",
        "developmental": "spiral",
        "preventive": "adaptive"
    }

    style = style_map.get(program_type, "modular")

    return ArchitectDependencies(
        psychological_domain=domain,
        target_population=population,
        program_type=program_type,
        complexity_level=complexity,
        architectural_style=style,
        **kwargs
    )

@dataclass
class ArchitecturalTemplate:
    """Шаблон архитектуры для быстрого старта"""

    name: str
    description: str
    base_structure: Dict[str, List[str]]
    recommended_duration: int
    target_outcomes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь для использования"""
        return {
            "name": self.name,
            "description": self.description,
            "structure": self.base_structure,
            "duration_weeks": self.recommended_duration,
            "outcomes": self.target_outcomes
        }

# Предопределенные шаблоны архитектур
ARCHITECTURAL_TEMPLATES = {
    "cbt_anxiety": ArchitecturalTemplate(
        name="CBT for Anxiety",
        description="Cognitive-Behavioral Therapy program for anxiety disorders",
        base_structure={
            "foundation": ["Psychoeducation", "Self-monitoring", "Relaxation"],
            "development": ["Cognitive restructuring", "Exposure therapy", "Response prevention"],
            "integration": ["Relapse prevention", "Maintenance planning", "Generalization"]
        },
        recommended_duration=12,
        target_outcomes=["Reduced anxiety", "Improved functioning", "Coping skills"]
    ),
    "mindfulness_depression": ArchitecturalTemplate(
        name="MBCT for Depression",
        description="Mindfulness-Based Cognitive Therapy for depression",
        base_structure={
            "foundation": ["Mindfulness basics", "Awareness training", "Acceptance"],
            "development": ["Thoughts observation", "Emotions regulation", "Behavioral activation"],
            "integration": ["Relapse prevention", "Lifestyle integration", "Support building"]
        },
        recommended_duration=8,
        target_outcomes=["Reduced depressive symptoms", "Increased mindfulness", "Relapse prevention"]
    ),
    "eft_couples": ArchitecturalTemplate(
        name="EFT for Couples",
        description="Emotionally Focused Therapy for couples",
        base_structure={
            "foundation": ["Assessment", "Cycle identification", "De-escalation"],
            "development": ["Accessing emotions", "Reframing", "New interactions"],
            "integration": ["Consolidation", "New patterns", "Future planning"]
        },
        recommended_duration=20,
        target_outcomes=["Improved attachment", "Better communication", "Relationship satisfaction"]
    )
}

def get_template(template_name: str) -> Optional[ArchitecturalTemplate]:
    """Получить архитектурный шаблон по имени"""
    return ARCHITECTURAL_TEMPLATES.get(template_name)