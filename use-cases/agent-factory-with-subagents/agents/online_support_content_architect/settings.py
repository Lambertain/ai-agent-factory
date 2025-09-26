"""
Settings для Psychology Content Architect Agent
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class PsychologicalDomain(Enum):
    """Психологические домены"""
    GENERAL = "general"
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    TRAUMA = "trauma"
    RELATIONSHIPS = "relationships"
    ADDICTION = "addiction"
    PERSONALITY = "personality"
    EATING_DISORDERS = "eating_disorders"
    STRESS = "stress"
    GRIEF = "grief"
    PARENTING = "parenting"

class TargetPopulation(Enum):
    """Целевые группы населения"""
    ADULTS = "adults"
    ADOLESCENTS = "adolescents"
    CHILDREN = "children"
    ELDERLY = "elderly"
    COUPLES = "couples"
    FAMILIES = "families"
    GROUPS = "groups"

class ProgramType(Enum):
    """Типы программ"""
    THERAPEUTIC = "therapeutic"
    EDUCATIONAL = "educational"
    PREVENTIVE = "preventive"
    DEVELOPMENTAL = "developmental"
    ASSESSMENT = "assessment"
    CRISIS_INTERVENTION = "crisis_intervention"

class DeliveryFormat(Enum):
    """Форматы доставки"""
    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"
    SELF_GUIDED = "self_guided"
    GROUP = "group"
    INDIVIDUAL = "individual"

class ComplexityLevel(Enum):
    """Уровни сложности"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXPERT = "expert"

@dataclass
class ArchitectSettings:
    """Настройки архитектора психологических программ"""

    # Основные параметры программы
    psychological_domain: str = PsychologicalDomain.GENERAL.value
    target_population: str = TargetPopulation.ADULTS.value
    program_type: str = ProgramType.THERAPEUTIC.value
    delivery_format: str = DeliveryFormat.HYBRID.value
    complexity_level: str = ComplexityLevel.MEDIUM.value

    # Временные параметры
    duration_weeks: int = 8
    session_length_minutes: int = 60
    sessions_per_week: int = 1
    total_sessions: Optional[int] = None

    # Архитектурные предпочтения
    architectural_style: str = "modular"  # modular, linear, spiral, adaptive
    progression_type: str = "linear"  # linear, spiral, adaptive, self_paced
    flexibility_level: str = "moderate"  # low, moderate, high

    # Требования к доказательности
    evidence_base_requirement: str = "moderate"  # minimal, moderate, high, expert
    clinical_guidelines_compliance: bool = True
    research_integration: bool = True

    # Адаптационные параметры
    personalization_level: str = "moderate"  # low, moderate, high
    cultural_adaptation: bool = True
    language_localization: List[str] = field(default_factory=lambda: ["ru", "en"])

    # Ресурсные ограничения
    resource_level: str = "standard"  # minimal, standard, comprehensive
    technology_requirements: str = "moderate"  # minimal, moderate, high
    staff_support_level: str = "standard"  # minimal, standard, intensive

    # Измерения и оценка
    assessment_frequency: str = "weekly"  # daily, weekly, biweekly, monthly
    outcome_measurement: bool = True
    progress_tracking: bool = True
    real_time_monitoring: bool = False

    # Безопасность и этика
    crisis_protocols: bool = True
    safety_monitoring: bool = True
    ethical_review: bool = True
    informed_consent: bool = True

    # Интеграция с системой
    orchestrator_integration: bool = True
    quality_assurance: bool = True
    collaborative_features: bool = True

    # Технические настройки
    api_timeout_seconds: int = 60
    max_retries: int = 3
    cache_duration_hours: int = 24

    def __post_init__(self):
        """Пост-инициализация и валидация"""
        # Автоматический расчет общего количества сессий
        if self.total_sessions is None:
            self.total_sessions = self.duration_weeks * self.sessions_per_week

        # Валидация настроек
        self._validate_settings()

    def _validate_settings(self):
        """Валидация настроек"""
        if self.duration_weeks < 1:
            self.duration_weeks = 8

        if self.session_length_minutes < 15:
            self.session_length_minutes = 60

        if self.sessions_per_week < 1:
            self.sessions_per_week = 1

        # Проверка совместимости параметров
        if self.complexity_level == "high" and self.duration_weeks < 6:
            self.duration_weeks = max(self.duration_weeks, 12)

    def get_architectural_constraints(self) -> Dict[str, Any]:
        """Получить архитектурные ограничения"""
        return {
            "duration": self.duration_weeks,
            "session_length": self.session_length_minutes,
            "format": self.delivery_format,
            "complexity": self.complexity_level,
            "flexibility": self.flexibility_level,
            "resources": self.resource_level,
            "evidence_requirement": self.evidence_base_requirement
        }

    def get_quality_requirements(self) -> Dict[str, bool]:
        """Получить требования к качеству"""
        return {
            "clinical_guidelines": self.clinical_guidelines_compliance,
            "research_integration": self.research_integration,
            "crisis_protocols": self.crisis_protocols,
            "safety_monitoring": self.safety_monitoring,
            "ethical_review": self.ethical_review,
            "outcome_measurement": self.outcome_measurement
        }

    def is_compatible_with(self, other_settings: 'ArchitectSettings') -> bool:
        """Проверить совместимость с другими настройками"""
        compatibility_factors = [
            self.psychological_domain == other_settings.psychological_domain,
            self.target_population == other_settings.target_population,
            self.program_type == other_settings.program_type,
            abs(self.duration_weeks - other_settings.duration_weeks) <= 2
        ]
        return sum(compatibility_factors) >= 3

    def adapt_for_population(self, population: str):
        """Адаптировать настройки для конкретной популяции"""
        adaptations = {
            "children": {
                "session_length_minutes": 30,
                "sessions_per_week": 2,
                "architectural_style": "adaptive",
                "personalization_level": "high"
            },
            "adolescents": {
                "session_length_minutes": 45,
                "technology_requirements": "high",
                "personalization_level": "high",
                "cultural_adaptation": True
            },
            "elderly": {
                "session_length_minutes": 45,
                "progression_type": "self_paced",
                "flexibility_level": "high",
                "technology_requirements": "minimal"
            },
            "couples": {
                "session_length_minutes": 90,
                "sessions_per_week": 1,
                "duration_weeks": max(self.duration_weeks, 12),
                "collaborative_features": True
            }
        }

        if population in adaptations:
            for key, value in adaptations[population].items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            "psychological_domain": self.psychological_domain,
            "target_population": self.target_population,
            "program_type": self.program_type,
            "delivery_format": self.delivery_format,
            "complexity_level": self.complexity_level,
            "duration_weeks": self.duration_weeks,
            "session_length_minutes": self.session_length_minutes,
            "sessions_per_week": self.sessions_per_week,
            "total_sessions": self.total_sessions,
            "architectural_style": self.architectural_style,
            "progression_type": self.progression_type,
            "flexibility_level": self.flexibility_level,
            "evidence_base_requirement": self.evidence_base_requirement,
            "personalization_level": self.personalization_level,
            "resource_level": self.resource_level,
            "assessment_frequency": self.assessment_frequency,
            "outcome_measurement": self.outcome_measurement,
            "crisis_protocols": self.crisis_protocols,
            "safety_monitoring": self.safety_monitoring
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArchitectSettings':
        """Создание из словаря"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})

    @classmethod
    def get_defaults_for_domain(cls, domain: str) -> 'ArchitectSettings':
        """Получить настройки по умолчанию для домена"""
        domain_defaults = {
            "anxiety": cls(
                psychological_domain="anxiety",
                duration_weeks=12,
                evidence_base_requirement="high",
                crisis_protocols=True,
                assessment_frequency="weekly"
            ),
            "depression": cls(
                psychological_domain="depression",
                duration_weeks=16,
                evidence_base_requirement="high",
                crisis_protocols=True,
                safety_monitoring=True,
                assessment_frequency="weekly"
            ),
            "trauma": cls(
                psychological_domain="trauma",
                duration_weeks=20,
                complexity_level="high",
                evidence_base_requirement="expert",
                crisis_protocols=True,
                safety_monitoring=True,
                staff_support_level="intensive",
                assessment_frequency="weekly"
            ),
            "relationships": cls(
                psychological_domain="relationships",
                target_population="couples",
                duration_weeks=20,
                session_length_minutes=90,
                collaborative_features=True
            ),
            "stress": cls(
                psychological_domain="stress",
                program_type="preventive",
                duration_weeks=6,
                complexity_level="low",
                delivery_format="self_guided"
            )
        }

        return domain_defaults.get(domain, cls())

# Предопределенные конфигурации
PRESET_CONFIGURATIONS = {
    "cbt_anxiety_adults": ArchitectSettings(
        psychological_domain="anxiety",
        target_population="adults",
        program_type="therapeutic",
        duration_weeks=12,
        evidence_base_requirement="high",
        architectural_style="modular",
        crisis_protocols=True
    ),
    "mindfulness_depression": ArchitectSettings(
        psychological_domain="depression",
        target_population="adults",
        program_type="therapeutic",
        duration_weeks=8,
        evidence_base_requirement="high",
        architectural_style="spiral",
        assessment_frequency="weekly"
    ),
    "adolescent_anxiety": ArchitectSettings(
        psychological_domain="anxiety",
        target_population="adolescents",
        program_type="therapeutic",
        duration_weeks=10,
        session_length_minutes=45,
        technology_requirements="high",
        personalization_level="high"
    ),
    "couples_eft": ArchitectSettings(
        psychological_domain="relationships",
        target_population="couples",
        program_type="therapeutic",
        duration_weeks=20,
        session_length_minutes=90,
        collaborative_features=True,
        evidence_base_requirement="high"
    ),
    "trauma_stabilization": ArchitectSettings(
        psychological_domain="trauma",
        target_population="adults",
        program_type="therapeutic",
        duration_weeks=24,
        complexity_level="high",
        evidence_base_requirement="expert",
        crisis_protocols=True,
        safety_monitoring=True,
        staff_support_level="intensive"
    ),
    "stress_prevention": ArchitectSettings(
        psychological_domain="stress",
        target_population="adults",
        program_type="preventive",
        duration_weeks=6,
        complexity_level="low",
        delivery_format="self_guided",
        personalization_level="moderate"
    )
}

def get_preset_configuration(preset_name: str) -> Optional[ArchitectSettings]:
    """Получить предустановленную конфигурацию"""
    return PRESET_CONFIGURATIONS.get(preset_name)

def list_available_presets() -> List[str]:
    """Список доступных предустановок"""
    return list(PRESET_CONFIGURATIONS.keys())