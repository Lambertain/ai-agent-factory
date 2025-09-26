"""
Конфигурация Psychology Test Generator для wellness и фитнес приложений

Этот пример показывает как настроить агент для использования в:
- Wellness платформах
- Фитнес приложениях
- Приложениях ментального здоровья
- Корпоративных wellness программах
"""

from psychology_test_generator import TestGeneratorDependencies, get_test_generator_config


def get_wellness_config():
    """
    Конфигурация для wellness приложений.

    Особенности:
    - Дружелюбный и мотивирующий тон
    - Фокус на позитивном развитии
    - Краткие и частые оценки
    - Геймификация и прогресс
    """
    return get_test_generator_config(
        domain="wellness_psychology",
        population="adults",
        test_type="progress",
        purpose="wellbeing_monitoring",

        # Wellness стандарты
        test_specification={
            "construct": "wellbeing_and_lifestyle",
            "subscales": ["mental_wellness", "physical_activity", "stress_management", "life_satisfaction"],
            "question_count": 15,
            "response_format": "frequency",
            "time_limit_minutes": 5,
            "difficulty_level": "easy",
            "cultural_adaptation": True
        },

        # Облегченные психометрические стандарты
        psychometric_standards={
            "reliability_threshold": 0.75,  # Wellness стандарт
            "validity_requirements": ["content", "construct"],
            "normative_sample_size": 200,
            "validation_type": "basic",
            "statistical_power": 0.80,
            "effect_size_detection": 0.3
        },

        # Пользовательские адаптации
        population_adaptations={
            "language_level": "grade_8",
            "cultural_considerations": True,
            "accessibility_features": ["simplified_language"],
            "administration_format": "digital",
            "support_required": "none"
        }
    )


def get_stress_tracking_config():
    """Конфигурация для отслеживания уровня стресса."""
    return TestGeneratorDependencies(
        psychological_domain="stress",
        target_population="adults",
        test_type="progress",
        measurement_purpose="daily_monitoring",

        test_specification={
            "construct": "daily_stress_levels",
            "subscales": ["work_stress", "personal_stress", "physical_symptoms", "coping_effectiveness"],
            "question_count": 8,
            "response_format": "intensity",
            "time_limit_minutes": 3,
            "difficulty_level": "easy"
        },

        psychometric_standards={
            "reliability_threshold": 0.75,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        },

        # Мобильные адаптации
        population_adaptations={
            "language_level": "grade_8",
            "administration_format": "digital",
            "support_required": "none"
        }
    )


def get_mood_tracking_config():
    """Конфигурация для мониторинга настроения."""
    return TestGeneratorDependencies(
        psychological_domain="emotional",
        target_population="adults",
        test_type="progress",
        measurement_purpose="mood_tracking",

        test_specification={
            "construct": "emotional_wellbeing",
            "subscales": ["positive_emotions", "negative_emotions", "emotional_stability", "life_satisfaction"],
            "question_count": 10,
            "response_format": "intensity",
            "time_limit_minutes": 4
        },

        psychometric_standards={
            "reliability_threshold": 0.78,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        }
    )


def get_fitness_motivation_config():
    """Конфигурация для оценки мотивации к фитнесу."""
    return TestGeneratorDependencies(
        psychological_domain="behavioral",
        target_population="adults",
        test_type="assessment",
        measurement_purpose="behavior_change",

        test_specification={
            "construct": "exercise_motivation",
            "subscales": ["intrinsic_motivation", "extrinsic_motivation", "self_efficacy", "barriers"],
            "question_count": 16,
            "response_format": "likert_5",
            "time_limit_minutes": 8
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        }
    )


def get_sleep_quality_config():
    """Конфигурация для оценки качества сна."""
    return TestGeneratorDependencies(
        psychological_domain="behavioral",
        target_population="adults",
        test_type="progress",
        measurement_purpose="sleep_monitoring",

        test_specification={
            "construct": "sleep_quality_assessment",
            "subscales": ["sleep_duration", "sleep_efficiency", "sleep_disturbances", "daytime_dysfunction"],
            "question_count": 12,
            "response_format": "frequency",
            "time_limit_minutes": 5
        },

        psychometric_standards={
            "reliability_threshold": 0.80,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        }
    )


def get_mindfulness_progress_config():
    """Конфигурация для отслеживания прогресса в майндфулнесс."""
    return TestGeneratorDependencies(
        psychological_domain="mindfulness",
        target_population="adults",
        test_type="progress",
        measurement_purpose="practice_monitoring",

        test_specification={
            "construct": "mindfulness_development",
            "subscales": ["present_moment_awareness", "non_judgmental_attitude", "emotional_regulation", "stress_reduction"],
            "question_count": 14,
            "response_format": "frequency",
            "time_limit_minutes": 6
        },

        psychometric_standards={
            "reliability_threshold": 0.82,
            "validity_requirements": ["content", "construct"],
            "validation_type": "basic"
        }
    )


def get_workplace_wellness_config():
    """Конфигурация для корпоративных wellness программ."""
    return TestGeneratorDependencies(
        psychological_domain="workplace",
        target_population="adults",
        test_type="assessment",
        measurement_purpose="workplace_wellness",

        test_specification={
            "construct": "workplace_wellbeing",
            "subscales": ["job_satisfaction", "work_life_balance", "stress_management", "team_relationships"],
            "question_count": 20,
            "response_format": "likert_5",
            "time_limit_minutes": 10
        },

        psychometric_standards={
            "reliability_threshold": 0.85,
            "validity_requirements": ["content", "construct"],
            "validation_type": "comprehensive"
        }
    )


# Пример использования в wellness приложении
WELLNESS_USAGE_EXAMPLE = """
# Интеграция в wellness платформу

from psychology_test_generator import psychology_test_generator_agent
from examples.wellness_config import get_stress_tracking_config

async def daily_stress_checkin(user_id: str, day_of_week: str):
    # Загрузка wellness конфигурации
    deps = get_stress_tracking_config()

    # Адаптация под день недели
    weekly_context = {
        "monday": "начало рабочей недели",
        "friday": "конец рабочей недели",
        "weekend": "выходные дни"
    }

    context = weekly_context.get(day_of_week, "обычный день")

    # Создание ежедневной проверки
    result = await psychology_test_generator_agent.run(
        user_prompt=f\"\"\"
        Создай ежедневную проверку уровня стресса:
        - Пользователь ID: {user_id}
        - Контекст: {context}
        - Тон: дружелюбный и поддерживающий
        - Время: максимум 3 минуты
        - Формат: мобильное приложение
        \"\"\",
        deps=deps
    )

    return {
        "daily_checkin": result.data,
        "wellness_metadata": {
            "user_id": user_id,
            "assessment_type": "daily_stress",
            "context": context,
            "completion_time": "3 minutes",
            "follow_up": "personalized_recommendations"
        }
    }

# Создание comprehensive wellness батареи
async def create_wellness_battery():
    configs = [
        ("Stress Tracking", get_stress_tracking_config()),
        ("Mood Monitoring", get_mood_tracking_config()),
        ("Fitness Motivation", get_fitness_motivation_config()),
        ("Sleep Quality", get_sleep_quality_config()),
        ("Mindfulness Progress", get_mindfulness_progress_config())
    ]

    wellness_suite = {}
    for name, config in configs:
        assessment = await psychology_test_generator_agent.run(
            user_prompt=f"Создай {name.lower()} инструмент для wellness приложения",
            deps=config
        )
        wellness_suite[name.lower().replace(" ", "_")] = assessment.data

    return {
        "wellness_suite": wellness_suite,
        "usage_patterns": {
            "daily": ["stress_tracking", "mood_monitoring"],
            "weekly": ["fitness_motivation", "sleep_quality"],
            "monthly": ["mindfulness_progress", "overall_wellness"]
        },
        "personalization": "AI-driven recommendations based on patterns"
    }
"""


# Wellness интеграции и особенности
WELLNESS_FEATURES = {
    "gamification": {
        "progress_tracking": "Visual progress bars and achievements",
        "streak_counters": "Daily, weekly, monthly streaks",
        "challenges": "Personal and social challenges",
        "rewards": "Points, badges, unlockables"
    },

    "personalization": {
        "adaptive_questioning": "Fewer questions when patterns are stable",
        "contextual_prompts": "Time, location, activity-based",
        "ai_insights": "Pattern recognition and recommendations",
        "goal_setting": "Personalized wellness goals"
    },

    "social_features": {
        "peer_support": "Anonymous community support",
        "sharing": "Optional progress sharing",
        "challenges": "Friend and group challenges",
        "accountability": "Buddy system for goals"
    },

    "integration_points": {
        "wearables": ["Apple Health", "Google Fit", "Fitbit", "Garmin"],
        "calendars": ["Google Calendar", "Outlook", "Apple Calendar"],
        "productivity": ["Slack", "Microsoft Teams", "Notion"],
        "meditation": ["Headspace", "Calm", "Insight Timer"]
    }
}


# Wellness metrics и KPIs
WELLNESS_METRICS = {
    "engagement": {
        "daily_active_users": "Users completing daily check-ins",
        "retention_rates": "7-day, 30-day, 90-day retention",
        "completion_rates": "Assessment completion percentage",
        "session_duration": "Time spent in app per session"
    },

    "wellness_outcomes": {
        "stress_reduction": "Measured stress level changes",
        "mood_improvement": "Positive mood trend tracking",
        "habit_formation": "Consistent behavior patterns",
        "goal_achievement": "Personal wellness goal completion"
    },

    "behavioral_insights": {
        "usage_patterns": "Peak usage times and frequencies",
        "drop_off_points": "Where users disengage",
        "feature_adoption": "Which features drive engagement",
        "intervention_effectiveness": "Impact of recommendations"
    }
}


# Wellness content personalization
WELLNESS_PERSONALIZATION = {
    "user_segments": {
        "beginners": {
            "characteristics": "New to wellness practices",
            "approach": "Simple, encouraging, educational",
            "frequency": "Daily brief check-ins"
        },
        "committed": {
            "characteristics": "Regular wellness practitioners",
            "approach": "Detailed tracking, advanced insights",
            "frequency": "Multiple daily touchpoints"
        },
        "inconsistent": {
            "characteristics": "Sporadic engagement",
            "approach": "Gentle reminders, easy wins",
            "frequency": "Flexible, user-driven"
        }
    },

    "contextual_factors": {
        "time_of_day": "Morning energy vs evening reflection",
        "day_of_week": "Workday stress vs weekend relaxation",
        "season": "Seasonal affective considerations",
        "life_events": "Major changes requiring support"
    }
}


if __name__ == "__main__":
    # Демонстрация wellness конфигураций
    print("=== Wellness Psychology Test Generator Configurations ===")

    configs = [
        ("Stress Tracking", get_stress_tracking_config()),
        ("Mood Monitoring", get_mood_tracking_config()),
        ("Fitness Motivation", get_fitness_motivation_config()),
        ("Sleep Quality", get_sleep_quality_config()),
        ("Mindfulness Progress", get_mindfulness_progress_config()),
        ("Workplace Wellness", get_workplace_wellness_config())
    ]

    for name, config in configs:
        print(f"\n{name}:")
        print(f"  Domain: {config.psychological_domain}")
        print(f"  Questions: {config.test_specification['question_count']}")
        print(f"  Time: {config.test_specification['time_limit_minutes']} min")
        print(f"  Purpose: {config.measurement_purpose}")

    print(f"\n=== Wellness Integration Features ===")
    for category, features in WELLNESS_FEATURES.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for feature, description in features.items():
            print(f"  • {feature.replace('_', ' ').title()}: {description}")