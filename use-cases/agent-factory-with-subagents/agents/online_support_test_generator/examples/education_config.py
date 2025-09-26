"""
Конфигурация Psychology Test Generator для образовательных систем

Этот пример показывает как настроить агент для использования в:
- Образовательных платформах
- Системах обучения
- Академических исследованиях
- Студенческих сервисах
"""

from psychology_test_generator import TestGeneratorDependencies, get_test_generator_config


def get_education_config():
    """
    Конфигурация для образовательных приложений.

    Особенности:
    - Адаптация под разные возрастные группы
    - Образовательные стандарты
    - Мониторинг прогресса обучения
    - Поддержка многоязычности
    """
    return get_test_generator_config(
        domain="educational_psychology",
        population="students",
        test_type="progress_monitoring",
        purpose="educational_assessment",

        # Образовательные стандарты
        test_specification={
            "construct": "learning_and_development",
            "subscales": ["academic_motivation", "learning_strategies", "stress_management", "social_skills"],
            "question_count": 20,
            "response_format": "likert_5",
            "time_limit_minutes": 12,
            "difficulty_level": "easy",
            "cultural_adaptation": True
        },

        # Образовательные психометрические стандарты
        psychometric_standards={
            "reliability_threshold": 0.75,  # Образовательный стандарт
            "validity_requirements": ["content", "construct"],
            "normative_sample_size": 300,
            "validation_type": "basic",
            "statistical_power": 0.80,
            "effect_size_detection": 0.3
        },

        # Студенческие адаптации
        population_adaptations={
            "language_level": "grade_8",
            "cultural_considerations": True,
            "accessibility_features": ["simplified_language"],
            "administration_format": "digital",
            "support_required": "minimal"
        }
    )


def get_student_wellbeing_config():
    """Конфигурация для мониторинга благополучия студентов."""
    return TestGeneratorDependencies(
        psychological_domain="stress",
        target_population="adolescents",
        test_type="progress",
        measurement_purpose="monitoring",

        test_specification={
            "construct": "student_wellbeing",
            "subscales": ["academic_stress", "social_pressure", "time_management", "emotional_regulation"],
            "question_count": 16,
            "response_format": "frequency",
            "time_limit_minutes": 8,
            "difficulty_level": "easy"
        },

        psychometric_standards={
            "reliability_threshold": 0.78,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        },

        # Подростковые адаптации
        population_adaptations={
            "language_level": "grade_8",
            "cultural_considerations": True,
            "administration_format": "digital",
            "support_required": "minimal"
        }
    )


def get_learning_motivation_config():
    """Конфигурация для оценки учебной мотивации."""
    return TestGeneratorDependencies(
        psychological_domain="personality",
        target_population="adolescents",
        test_type="assessment",
        measurement_purpose="educational_planning",

        test_specification={
            "construct": "learning_motivation",
            "subscales": ["intrinsic_motivation", "extrinsic_motivation", "goal_orientation", "self_efficacy"],
            "question_count": 24,
            "response_format": "likert_7",
            "time_limit_minutes": 15
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct"],
            "validation_type": "comprehensive"
        }
    )


def get_children_social_skills_config():
    """Конфигурация для оценки социальных навыков детей."""
    return TestGeneratorDependencies(
        psychological_domain="behavioral",
        target_population="children",
        test_type="assessment",
        measurement_purpose="educational_support",

        test_specification={
            "construct": "social_skills_development",
            "subscales": ["peer_interaction", "communication", "empathy", "conflict_resolution"],
            "question_count": 12,
            "response_format": "frequency",
            "time_limit_minutes": 10
        },

        psychometric_standards={
            "reliability_threshold": 0.75,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        },

        # Детские адаптации
        population_adaptations={
            "language_level": "grade_6",
            "cultural_considerations": True,
            "accessibility_features": ["simplified_language", "visual_aids"],
            "administration_format": "mixed",
            "support_required": "moderate"
        }
    )


def get_teacher_burnout_config():
    """Конфигурация для оценки эмоционального выгорания учителей."""
    return TestGeneratorDependencies(
        psychological_domain="stress",
        target_population="adults",
        test_type="diagnostic",
        measurement_purpose="workplace_assessment",

        test_specification={
            "construct": "teacher_burnout",
            "subscales": ["emotional_exhaustion", "depersonalization", "personal_accomplishment", "work_engagement"],
            "question_count": 22,
            "response_format": "frequency",
            "time_limit_minutes": 12
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct", "criterion"],
            "validation_type": "comprehensive"
        }
    )


# Пример использования в образовательной системе
EDUCATION_USAGE_EXAMPLE = """
# Интеграция в образовательную платформу

from psychology_test_generator import psychology_test_generator_agent
from examples.education_config import get_student_wellbeing_config

async def monitor_student_wellbeing(student_id: str, grade_level: str):
    # Загрузка образовательной конфигурации
    deps = get_student_wellbeing_config()

    # Адаптация под уровень класса
    if grade_level in ["6", "7", "8"]:
        deps.population_adaptations["language_level"] = "grade_6"
    elif grade_level in ["9", "10", "11"]:
        deps.population_adaptations["language_level"] = "grade_8"

    # Создание теста мониторинга
    result = await psychology_test_generator_agent.run(
        user_prompt=f\"\"\"
        Создай тест для мониторинга благополучия студента:
        - Студент ID: {student_id}
        - Класс: {grade_level}
        - Цель: регулярный мониторинг состояния
        - Формат: дружелюбный и неинтрузивный
        \"\"\",
        deps=deps
    )

    return {
        "test_content": result.data,
        "student_metadata": {
            "student_id": student_id,
            "grade_level": grade_level,
            "test_type": "wellbeing_monitoring",
            "frequency": "weekly",
            "privacy_level": "high"
        }
    }

# Создание образовательной батареи тестов
async def create_school_assessment_battery():
    configs = [
        ("Student Wellbeing", get_student_wellbeing_config()),
        ("Learning Motivation", get_learning_motivation_config()),
        ("Social Skills", get_children_social_skills_config()),
        ("Teacher Burnout", get_teacher_burnout_config())
    ]

    battery = {}
    for name, config in configs:
        test = await psychology_test_generator_agent.run(
            user_prompt=f"Создай {name.lower()} тест согласно образовательным стандартам",
            deps=config
        )
        battery[name.lower().replace(" ", "_")] = test.data

    return {
        "assessment_battery": battery,
        "target_groups": ["students", "teachers", "parents"],
        "implementation": "gradual_rollout",
        "support_required": "training_sessions"
    }
"""


# Образовательные стандарты и интеграция
EDUCATION_INTEGRATION = {
    "learning_management_systems": {
        "supported_lms": ["Moodle", "Canvas", "Blackboard", "Google Classroom"],
        "integration_types": ["LTI", "API", "Single Sign-On"],
        "data_sync": ["grades", "progress", "analytics"]
    },

    "age_adaptations": {
        "elementary": {
            "age_range": "6-11",
            "language_level": "grade_6",
            "max_questions": 10,
            "visual_aids": True,
            "time_limit": 8
        },
        "middle_school": {
            "age_range": "12-14",
            "language_level": "grade_8",
            "max_questions": 15,
            "digital_native": True,
            "time_limit": 12
        },
        "high_school": {
            "age_range": "15-18",
            "language_level": "grade_10",
            "max_questions": 25,
            "career_focus": True,
            "time_limit": 20
        }
    },

    "privacy_compliance": {
        "ferpa_compliance": "Required for US schools",
        "gdpr_compliance": "Required for EU schools",
        "parental_consent": "Required for under 13",
        "data_retention": "Limited to academic purpose"
    },

    "progress_tracking": {
        "frequency": ["daily", "weekly", "monthly", "quarterly"],
        "metrics": ["wellbeing", "motivation", "stress", "engagement"],
        "alerts": ["risk_detection", "improvement_opportunities"],
        "reporting": ["individual", "class", "school", "district"]
    }
}


# Многоязычная поддержка для образования
EDUCATION_LANGUAGES = {
    "primary_languages": ["en", "es", "fr", "de", "zh", "ja", "ru"],
    "regional_adaptations": {
        "latin_america": ["es", "pt"],
        "europe": ["en", "fr", "de", "it", "nl"],
        "asia_pacific": ["zh", "ja", "ko", "th", "vi"],
        "africa": ["en", "fr", "ar", "sw"],
        "middle_east": ["ar", "fa", "he", "tr"]
    },
    "cultural_considerations": {
        "collectivist_cultures": "Emphasis on group harmony",
        "individualist_cultures": "Focus on personal achievement",
        "high_context": "Indirect communication style",
        "low_context": "Direct communication style"
    }
}


if __name__ == "__main__":
    # Демонстрация образовательных конфигураций
    print("=== Education Psychology Test Generator Configurations ===")

    configs = [
        ("Student Wellbeing", get_student_wellbeing_config()),
        ("Learning Motivation", get_learning_motivation_config()),
        ("Children Social Skills", get_children_social_skills_config()),
        ("Teacher Burnout", get_teacher_burnout_config())
    ]

    for name, config in configs:
        print(f"\n{name}:")
        print(f"  Domain: {config.psychological_domain}")
        print(f"  Population: {config.target_population}")
        print(f"  Questions: {config.test_specification['question_count']}")
        print(f"  Time: {config.test_specification['time_limit_minutes']} min")
        print(f"  Language Level: {config.population_adaptations['language_level']}")

    print(f"\n=== Age Group Adaptations ===")
    for group, details in EDUCATION_INTEGRATION["age_adaptations"].items():
        print(f"{group.title()}: Ages {details['age_range']}, {details['max_questions']} questions max")