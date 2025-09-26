"""
Конфигурация Psychology Test Generator для медицинских/клинических приложений

Этот пример показывает как настроить агент для использования в:
- Клинических системах
- Медицинских приложениях
- Системах телемедицины
- Психиатрических платформах
"""

from psychology_test_generator import TestGeneratorDependencies, get_test_generator_config


def get_healthcare_config():
    """
    Конфигурация для медицинских приложений.

    Особенности:
    - Высокие стандарты надежности
    - Клиническая валидация
    - HIPAA соответствие
    - Интеграция с EMR системами
    """
    return get_test_generator_config(
        domain="clinical_assessment",
        population="adults",
        test_type="diagnostic",
        purpose="clinical_diagnosis",

        # Медицинские стандарты
        test_specification={
            "construct": "clinical_symptom_assessment",
            "subscales": ["primary_symptoms", "severity", "functional_impact", "duration"],
            "question_count": 25,
            "response_format": "intensity",
            "time_limit_minutes": 15,
            "difficulty_level": "moderate",
            "cultural_adaptation": True
        },

        # Высокие психометрические стандарты
        psychometric_standards={
            "reliability_threshold": 0.88,  # Клинический стандарт
            "validity_requirements": ["content", "construct", "criterion", "predictive"],
            "normative_sample_size": 1000,
            "validation_type": "clinical",
            "statistical_power": 0.90,
            "effect_size_detection": 0.2
        },

        # Медицинские адаптации
        population_adaptations={
            "language_level": "professional",
            "cultural_considerations": True,
            "accessibility_features": ["large_print", "audio"],
            "administration_format": "digital",
            "support_required": "minimal"
        }
    )


def get_depression_screening_config():
    """Конфигурация для скрининга депрессии в медицинских учреждениях."""
    return TestGeneratorDependencies(
        psychological_domain="depression",
        target_population="adults",
        test_type="diagnostic",
        measurement_purpose="clinical_screening",

        test_specification={
            "construct": "depression_severity",
            "subscales": ["mood", "anhedonia", "cognitive", "somatic", "suicidal_ideation"],
            "question_count": 21,  # Расширенная версия PHQ-9
            "response_format": "frequency",
            "time_limit_minutes": 8,
            "difficulty_level": "moderate"
        },

        psychometric_standards={
            "reliability_threshold": 0.90,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "clinical"
        },

        # Медицинская интеграция
        enable_validation_tools=True,
        enable_psychometric_analysis=True,
        enable_quality_assurance=True
    )


def get_anxiety_assessment_config():
    """Конфигурация для клинической оценки тревожности."""
    return TestGeneratorDependencies(
        psychological_domain="anxiety",
        target_population="adults",
        test_type="diagnostic",
        measurement_purpose="clinical_assessment",

        test_specification={
            "construct": "anxiety_disorders_assessment",
            "subscales": ["generalized_anxiety", "panic_disorder", "social_anxiety", "specific_phobias"],
            "question_count": 28,
            "response_format": "intensity",
            "time_limit_minutes": 12
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "clinical"
        }
    )


def get_trauma_screening_config():
    """Конфигурация для скрининга травматических расстройств."""
    return TestGeneratorDependencies(
        psychological_domain="trauma",
        target_population="adults",
        test_type="diagnostic",
        measurement_purpose="trauma_screening",

        test_specification={
            "construct": "trauma_impact_assessment",
            "subscales": ["trauma_exposure", "ptsd_symptoms", "dissociation", "functional_impact"],
            "question_count": 30,
            "response_format": "intensity",
            "time_limit_minutes": 15
        },

        psychometric_standards={
            "reliability_threshold": 0.87,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "clinical"
        },

        # Особые требования для травмы
        population_adaptations={
            "cultural_considerations": True,
            "support_required": "moderate",  # Возможность консультации
            "administration_format": "digital"
        }
    )


# Пример использования в медицинском приложении
HEALTHCARE_USAGE_EXAMPLE = """
# Интеграция в медицинскую систему

from psychology_test_generator import psychology_test_generator_agent
from examples.healthcare_config import get_depression_screening_config

async def clinical_depression_screening(patient_id: str, clinician_id: str):
    # Загрузка медицинской конфигурации
    deps = get_depression_screening_config()

    # Создание скринингового теста
    result = await psychology_test_generator_agent.run(
        user_prompt=f\"\"\"
        Создай клинический скрининговый тест для депрессии:
        - Пациент ID: {patient_id}
        - Клиницист: {clinician_id}
        - Требования: HIPAA соответствие, клиническая валидация
        - Формат: цифровая форма с интеграцией в EMR
        \"\"\",
        deps=deps
    )

    return {
        "test_content": result.data,
        "clinical_metadata": {
            "patient_id": patient_id,
            "clinician_id": clinician_id,
            "test_type": "depression_screening",
            "reliability": deps.psychometric_standards["reliability_threshold"],
            "hipaa_compliant": True
        }
    }

# Пакетная генерация для клиники
async def generate_clinic_test_battery():
    configs = [
        get_depression_screening_config(),
        get_anxiety_assessment_config(),
        get_trauma_screening_config()
    ]

    tests = []
    for config in configs:
        test = await psychology_test_generator_agent.run(
            user_prompt="Создай клинический тест согласно конфигурации",
            deps=config
        )
        tests.append(test.data)

    return {
        "test_battery": tests,
        "clinical_standards": "Все тесты соответствуют клиническим стандартам",
        "total_time": "35-40 минут",
        "reliability_range": "0.85-0.90"
    }
"""


# Медицинские стандарты и соответствие
HEALTHCARE_COMPLIANCE = {
    "hipaa_requirements": {
        "data_encryption": "AES-256",
        "access_control": "Role-based",
        "audit_logging": "Required",
        "patient_consent": "Informed consent mandatory"
    },

    "clinical_standards": {
        "reliability_minimum": 0.85,
        "validation_required": ["content", "construct", "criterion"],
        "sample_size_minimum": 500,
        "cultural_adaptation": "Required for diverse populations"
    },

    "integration_points": {
        "emr_systems": ["Epic", "Cerner", "AllScripts"],
        "data_formats": ["HL7 FHIR", "JSON", "XML"],
        "apis": ["RESTful", "GraphQL"],
        "security": ["OAuth 2.0", "SAML", "JWT"]
    }
}


if __name__ == "__main__":
    # Демонстрация конфигураций
    print("=== Healthcare Psychology Test Generator Configurations ===")

    configs = [
        ("Depression Screening", get_depression_screening_config()),
        ("Anxiety Assessment", get_anxiety_assessment_config()),
        ("Trauma Screening", get_trauma_screening_config())
    ]

    for name, config in configs:
        print(f"\n{name}:")
        print(f"  Domain: {config.psychological_domain}")
        print(f"  Questions: {config.test_specification['question_count']}")
        print(f"  Reliability: {config.psychometric_standards['reliability_threshold']}")
        print(f"  Format: {config.test_specification['response_format']}")