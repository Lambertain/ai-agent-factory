"""
Dependencies для Psychology Test Generator Agent
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TestGeneratorDependencies:
    """Зависимости для генератора психологических тестов"""

    # Основные настройки
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    project_path: str = ""

    # Параметры генерации тестов
    psychological_domain: str = "general"  # anxiety, depression, trauma, personality, etc.
    target_population: str = "adults"  # adults, adolescents, children, elderly, etc.
    test_type: str = "assessment"  # assessment, diagnostic, progress, personality, screening
    measurement_purpose: str = "screening"  # screening, diagnosis, monitoring, research

    # Спецификация теста
    test_specification: Dict[str, Any] = field(default_factory=lambda: {
        "construct": "general_psychological",
        "subscales": ["main_factor"],
        "question_count": 20,
        "response_format": "likert_5",  # likert_5, likert_7, frequency, intensity, binary
        "time_limit_minutes": 15,
        "difficulty_level": "moderate",  # easy, moderate, difficult
        "cultural_adaptation": True
    })

    # Психометрические стандарты
    psychometric_standards: Dict[str, Any] = field(default_factory=lambda: {
        "reliability_threshold": 0.80,  # Минимальная надежность (α Кронбаха)
        "validity_requirements": ["content", "construct"],
        "normative_sample_size": 200,
        "validation_type": "basic",  # basic, comprehensive, clinical
        "statistical_power": 0.80,
        "effect_size_detection": 0.3
    })

    # Адаптации под популяцию
    population_adaptations: Dict[str, Any] = field(default_factory=lambda: {
        "language_level": "grade_8",  # grade_6, grade_8, grade_10, professional
        "cultural_considerations": True,
        "accessibility_features": [],  # large_print, audio, simplified_language
        "administration_format": "digital",  # digital, paper, mixed
        "support_required": "none"  # none, minimal, moderate, intensive
    })

    # Интеграция с системой
    enable_validation_tools: bool = True
    enable_psychometric_analysis: bool = True
    enable_population_adaptation: bool = True
    enable_test_battery_creation: bool = True

    # RAG конфигурация
    agent_name: str = "psychology_test_generator"
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "psychology-test-generation",
        "psychometrics",
        "test-validation",
        "psychological-assessment"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Интеграция с другими агентами
    enable_research_integration: bool = True  # Интеграция с Psychology Research Agent
    enable_architect_collaboration: bool = True  # Работа с Psychology Content Architect
    enable_quality_assurance: bool = True  # Проверка через Psychology Quality Guardian

    def __post_init__(self):
        """Инициализация и валидация конфигурации"""
        # Добавление доменных тегов
        if self.psychological_domain != "general":
            self.knowledge_tags.append(self.psychological_domain)

        # Добавление популяционных тегов
        if self.target_population != "adults":
            self.knowledge_tags.append(f"population-{self.target_population}")

        # Добавление тегов типа теста
        if self.test_type != "assessment":
            self.knowledge_tags.append(f"test-type-{self.test_type}")

        # Валидация настроек
        self._validate_test_specification()
        self._validate_psychometric_standards()
        self._validate_population_adaptations()

    def _validate_test_specification(self):
        """Валидация спецификации теста"""
        # Проверка количества вопросов
        question_count = self.test_specification.get("question_count", 20)
        if question_count < 5:
            self.test_specification["question_count"] = 10
        elif question_count > 100:
            self.test_specification["question_count"] = 50

        # Проверка временных ограничений
        time_limit = self.test_specification.get("time_limit_minutes", 15)
        if time_limit < 5:
            self.test_specification["time_limit_minutes"] = 10
        elif time_limit > 120:
            self.test_specification["time_limit_minutes"] = 60

        # Валидация формата ответов
        valid_formats = ["likert_5", "likert_7", "frequency", "intensity", "binary", "multiple_choice"]
        if self.test_specification.get("response_format") not in valid_formats:
            self.test_specification["response_format"] = "likert_5"

    def _validate_psychometric_standards(self):
        """Валидация психометрических стандартов"""
        # Проверка порога надежности
        reliability = self.psychometric_standards.get("reliability_threshold", 0.80)
        if not 0.60 <= reliability <= 0.95:
            self.psychometric_standards["reliability_threshold"] = 0.80

        # Проверка размера выборки
        sample_size = self.psychometric_standards.get("normative_sample_size", 200)
        if sample_size < 50:
            self.psychometric_standards["normative_sample_size"] = 100
        elif sample_size > 5000:
            self.psychometric_standards["normative_sample_size"] = 1000

        # Валидация требований к валидности
        valid_types = ["content", "construct", "criterion", "convergent", "discriminant"]
        validity_reqs = self.psychometric_standards.get("validity_requirements", [])
        self.psychometric_standards["validity_requirements"] = [
            vtype for vtype in validity_reqs if vtype in valid_types
        ]
        if not self.psychometric_standards["validity_requirements"]:
            self.psychometric_standards["validity_requirements"] = ["content", "construct"]

    def _validate_population_adaptations(self):
        """Валидация адаптаций под популяцию"""
        # Проверка уровня языка
        valid_levels = ["grade_6", "grade_8", "grade_10", "professional"]
        if self.population_adaptations.get("language_level") not in valid_levels:
            self.population_adaptations["language_level"] = "grade_8"

        # Валидация формата администрирования
        valid_formats = ["digital", "paper", "mixed", "adaptive"]
        if self.population_adaptations.get("administration_format") not in valid_formats:
            self.population_adaptations["administration_format"] = "digital"

        # Проверка возможностей доступности
        valid_accessibility = ["large_print", "audio", "simplified_language", "braille", "sign_language"]
        accessibility = self.population_adaptations.get("accessibility_features", [])
        self.population_adaptations["accessibility_features"] = [
            feature for feature in accessibility if feature in valid_accessibility
        ]

    def get_test_configuration(self) -> Dict[str, Any]:
        """Получить полную конфигурацию теста"""
        return {
            "psychological_domain": self.psychological_domain,
            "target_population": self.target_population,
            "test_type": self.test_type,
            "measurement_purpose": self.measurement_purpose,
            "test_specification": self.test_specification,
            "psychometric_standards": self.psychometric_standards,
            "population_adaptations": self.population_adaptations
        }

    def get_generation_parameters(self) -> Dict[str, Any]:
        """Получить параметры для генерации тестов"""
        return {
            "construct": self.test_specification.get("construct"),
            "subscales": self.test_specification.get("subscales", []),
            "question_count": self.test_specification.get("question_count"),
            "response_format": self.test_specification.get("response_format"),
            "difficulty_level": self.test_specification.get("difficulty_level"),
            "target_population": self.target_population,
            "language_level": self.population_adaptations.get("language_level"),
            "cultural_adaptation": self.test_specification.get("cultural_adaptation", True)
        }

    def get_validation_requirements(self) -> Dict[str, Any]:
        """Получить требования к валидации"""
        return {
            "reliability_threshold": self.psychometric_standards.get("reliability_threshold"),
            "validity_requirements": self.psychometric_standards.get("validity_requirements"),
            "sample_size": self.psychometric_standards.get("normative_sample_size"),
            "validation_type": self.psychometric_standards.get("validation_type"),
            "statistical_power": self.psychometric_standards.get("statistical_power"),
            "effect_size_detection": self.psychometric_standards.get("effect_size_detection")
        }

    def get_adaptation_guidelines(self) -> Dict[str, Any]:
        """Получить руководство по адаптации"""
        adaptation_map = {
            "children": {
                "language_simplification": True,
                "visual_elements": True,
                "shorter_sessions": True,
                "parental_involvement": True
            },
            "adolescents": {
                "peer_relevant_examples": True,
                "digital_native_format": True,
                "privacy_emphasis": True,
                "contemporary_language": True
            },
            "elderly": {
                "large_font": True,
                "simplified_technology": True,
                "medical_considerations": True,
                "slower_pace": True
            },
            "special_needs": {
                "accessibility_features": True,
                "flexible_administration": True,
                "support_person_allowed": True,
                "alternative_formats": True
            }
        }

        base_guidelines = {
            "cultural_sensitivity": self.population_adaptations.get("cultural_considerations"),
            "language_level": self.population_adaptations.get("language_level"),
            "accessibility_features": self.population_adaptations.get("accessibility_features"),
            "administration_format": self.population_adaptations.get("administration_format")
        }

        # Добавляем специфические рекомендации для популяции
        specific_guidelines = adaptation_map.get(self.target_population, {})
        base_guidelines.update(specific_guidelines)

        return base_guidelines

    def is_suitable_for_population(self, population: str) -> bool:
        """Проверить подходит ли конфигурация для популяции"""
        if population == self.target_population:
            return True

        # Проверка совместимости популяций
        compatible_groups = {
            "adults": ["young_adults", "middle_aged", "professionals"],
            "adolescents": ["teens", "high_school", "young_adults"],
            "children": ["school_age", "elementary", "middle_school"],
            "elderly": ["seniors", "older_adults", "retired"]
        }

        target_compatible = compatible_groups.get(self.target_population, [])
        return population in target_compatible

    def adapt_for_domain(self, domain: str):
        """Адаптировать настройки под конкретный домен"""
        domain_adaptations = {
            "anxiety": {
                "construct": "anxiety_assessment",
                "subscales": ["general_anxiety", "social_anxiety", "panic", "worry"],
                "question_count": 21,  # Стандарт для GAD-7 расширенный
                "response_format": "frequency"
            },
            "depression": {
                "construct": "depression_assessment",
                "subscales": ["mood", "anhedonia", "cognitive", "somatic"],
                "question_count": 18,  # На основе PHQ-9 расширенный
                "response_format": "frequency"
            },
            "trauma": {
                "construct": "trauma_impact_assessment",
                "subscales": ["trauma_exposure", "ptsd_symptoms", "dissociation", "functional_impact"],
                "question_count": 25,
                "response_format": "intensity"
            },
            "personality": {
                "construct": "personality_traits",
                "subscales": ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"],
                "question_count": 50,  # 10 items per Big Five factor
                "response_format": "likert_7"
            },
            "stress": {
                "construct": "stress_assessment",
                "subscales": ["stress_sources", "stress_response", "coping_ability", "stress_impact"],
                "question_count": 20,
                "response_format": "frequency"
            },
            "relationships": {
                "construct": "relationship_quality",
                "subscales": ["communication", "intimacy", "conflict_resolution", "satisfaction"],
                "question_count": 24,
                "response_format": "likert_5"
            }
        }

        if domain in domain_adaptations:
            adaptations = domain_adaptations[domain]
            for key, value in adaptations.items():
                if key in self.test_specification:
                    self.test_specification[key] = value

            # Обновление доменных тегов
            self.psychological_domain = domain
            if domain not in self.knowledge_tags:
                self.knowledge_tags.append(domain)

    def get_ethical_guidelines(self) -> Dict[str, Any]:
        """Получить этические рекомендации для тестирования"""
        return {
            "informed_consent": {
                "required": True,
                "age_appropriate": self.target_population in ["children", "adolescents"],
                "parental_consent": self.target_population == "children"
            },
            "confidentiality": {
                "data_protection": True,
                "results_sharing": "authorized_only",
                "anonymization": "when_possible"
            },
            "cultural_sensitivity": {
                "avoid_bias": True,
                "cultural_adaptation": self.test_specification.get("cultural_adaptation", True),
                "language_appropriate": True
            },
            "harm_prevention": {
                "distressing_content_warning": True,
                "support_resources": True,
                "crisis_protocols": self.psychological_domain in ["depression", "trauma", "anxiety"]
            },
            "fair_testing": {
                "accessibility_accommodations": True,
                "equal_opportunity": True,
                "bias_monitoring": True
            }
        }

def get_test_generator_config(
    domain: str = "general",
    population: str = "adults",
    test_type: str = "assessment",
    purpose: str = "screening",
    **kwargs
) -> TestGeneratorDependencies:
    """Фабрика для создания конфигурации генератора тестов"""

    # Настройка стандартных конфигураций для доменов
    domain_configs = {
        "anxiety": {
            "test_specification": {
                "construct": "anxiety_assessment",
                "subscales": ["generalized", "social", "panic", "specific_phobias"],
                "question_count": 21,
                "response_format": "frequency",
                "time_limit_minutes": 10
            },
            "psychometric_standards": {
                "reliability_threshold": 0.85,
                "validity_requirements": ["content", "construct", "criterion"],
                "validation_type": "clinical"
            }
        },
        "depression": {
            "test_specification": {
                "construct": "depression_severity",
                "subscales": ["mood", "anhedonia", "cognitive", "somatic"],
                "question_count": 18,
                "response_format": "frequency",
                "time_limit_minutes": 8
            },
            "psychometric_standards": {
                "reliability_threshold": 0.88,
                "validity_requirements": ["content", "construct", "criterion"],
                "validation_type": "clinical"
            }
        },
        "personality": {
            "test_specification": {
                "construct": "personality_traits",
                "subscales": ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"],
                "question_count": 50,
                "response_format": "likert_7",
                "time_limit_minutes": 20
            },
            "psychometric_standards": {
                "reliability_threshold": 0.80,
                "validity_requirements": ["content", "construct", "convergent"],
                "validation_type": "comprehensive"
            }
        }
    }

    # Базовая конфигурация
    config = TestGeneratorDependencies(
        psychological_domain=domain,
        target_population=population,
        test_type=test_type,
        measurement_purpose=purpose,
        **kwargs
    )

    # Применение доменной конфигурации
    if domain in domain_configs:
        domain_config = domain_configs[domain]
        config.test_specification.update(domain_config.get("test_specification", {}))
        config.psychometric_standards.update(domain_config.get("psychometric_standards", {}))

    # Адаптация под популяцию
    population_adaptations = {
        "children": {
            "language_level": "grade_6",
            "administration_format": "mixed",
            "support_required": "moderate"
        },
        "adolescents": {
            "language_level": "grade_8",
            "administration_format": "digital",
            "support_required": "minimal"
        },
        "elderly": {
            "language_level": "grade_8",
            "administration_format": "paper",
            "support_required": "moderate",
            "accessibility_features": ["large_print"]
        }
    }

    if population in population_adaptations:
        config.population_adaptations.update(population_adaptations[population])

    return config