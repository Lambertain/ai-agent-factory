"""
Professional community configuration example.

Example setup for managing a professional networking community.
"""

from ..dependencies import (
    CommunityManagementDependencies,
    CommunityType,
    CommunityPlatform,
    ModerationLevel
)


def create_professional_community_config() -> CommunityManagementDependencies:
    """
    Create configuration for professional community.

    Returns:
        Professional community dependencies
    """
    return CommunityManagementDependencies(
        # Core settings
        api_key="your-api-key-here",
        community_name="Tech Leaders Network",
        community_type=CommunityType.PROFESSIONAL,
        platforms=[CommunityPlatform.LINKEDIN, CommunityPlatform.SLACK],

        # Scale configuration
        expected_members=75000,
        current_members=18000,
        growth_target_monthly=0.12,  # Steady 12% growth

        # Strict professional moderation
        moderation_level=ModerationLevel.STRICT,
        toxicity_threshold=0.3,  # Very low tolerance
        spam_detection_enabled=True,
        auto_ban_enabled=False,  # Manual review for professionals
        profanity_filter_enabled=True,

        # Professional language settings
        primary_language="en",
        supported_languages=["en", "zh", "de", "ja", "fr"],
        timezone="UTC",
        cultural_adaptation_enabled=True,

        # Professional engagement
        auto_welcome_enabled=True,
        engagement_tracking_enabled=True,
        influencer_program_enabled=True,  # Industry leaders
        gamification_enabled=False,  # Not appropriate for professional

        # Professional growth mechanics
        referral_program_enabled=True,  # Professional referrals
        viral_mechanics_enabled=False,  # More conservative approach
        social_proof_amplification=True,  # Professional achievements
        ugc_curation_enabled=True,  # Professional content

        # Professional AI features
        sentiment_analysis_enabled=True,
        trend_detection_enabled=True,  # Industry trends
        predictive_analytics_enabled=True,
        content_recommendation_enabled=True,

        # Platform tokens
        slack_bot_token="your-slack-bot-token",

        # Performance settings
        max_concurrent_operations=15,
        cache_ttl_seconds=450,
        batch_processing_size=150,
        rate_limit_per_minute=80,

        # Professional notifications
        alert_channel="#moderators",
        critical_alert_emails=["admin@techleaders.com"],
        daily_report_enabled=True,
        weekly_analytics_enabled=True,

        # Professional rules
        custom_moderation_rules={
            "self_promotion_limit": True,
            "job_posting_format": True,
            "professional_language_only": True,
            "credential_verification": True,
            "no_political_discussions": True
        },
        custom_engagement_triggers={
            "industry_news_sharing": True,
            "professional_milestone_celebration": True,
            "expertise_knowledge_sharing": True,
            "networking_event_announcements": True,
            "thought_leadership_promotion": True
        },
        custom_viral_mechanics={
            "professional_referral_program": True,
            "industry_expertise_showcasing": True,
            "career_success_stories": True,
            "knowledge_sharing_rewards": True
        }
    )


# Example usage
if __name__ == "__main__":
    config = create_professional_community_config()
    print(f"Professional community config created for: {config.community_name}")
    print(f"Expected members: {config.expected_members:,}")
    print(f"Moderation level: {config.moderation_level.value}")
    print(f"Gamification: {config.gamification_enabled}")