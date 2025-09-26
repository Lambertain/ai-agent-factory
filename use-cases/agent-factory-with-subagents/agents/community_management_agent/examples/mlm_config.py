"""
MLM community configuration example.

Example setup for managing a multi-level marketing community.
"""

from ..dependencies import (
    CommunityManagementDependencies,
    CommunityType,
    CommunityPlatform,
    ModerationLevel
)


def create_mlm_community_config() -> CommunityManagementDependencies:
    """
    Create configuration for MLM community.

    Returns:
        MLM community dependencies
    """
    return CommunityManagementDependencies(
        # Core settings
        api_key="your-api-key-here",
        community_name="Success Network Community",
        community_type=CommunityType.MLM,
        platforms=[CommunityPlatform.TELEGRAM, CommunityPlatform.FACEBOOK],

        # Scale configuration for viral MLM growth
        expected_members=1000000,  # Million-member target
        current_members=25000,
        growth_target_monthly=0.50,  # Aggressive 50% monthly growth

        # Strict moderation for professional image
        moderation_level=ModerationLevel.STRICT,
        toxicity_threshold=0.4,  # Low tolerance for negativity
        spam_detection_enabled=True,
        auto_ban_enabled=True,  # Auto-ban for scam accusations
        profanity_filter_enabled=True,

        # Multi-language for global reach
        primary_language="en",
        supported_languages=["en", "es", "zh", "hi", "ar", "pt"],
        timezone="UTC",
        cultural_adaptation_enabled=True,

        # MLM engagement features
        auto_welcome_enabled=True,
        engagement_tracking_enabled=True,
        influencer_program_enabled=True,  # Top performers
        gamification_enabled=True,  # Rank advancement system

        # Essential for MLM viral growth
        referral_program_enabled=True,  # Core MLM mechanic
        viral_mechanics_enabled=True,
        social_proof_amplification=True,  # Success stories
        ugc_curation_enabled=True,  # Member testimonials

        # MLM-specific features
        mlm_features_enabled=True,
        mlm_tier_tracking=True,
        mlm_commission_tracking=True,
        mlm_training_distribution=True,

        # AI features for scale
        sentiment_analysis_enabled=True,
        trend_detection_enabled=True,
        predictive_analytics_enabled=True,  # Churn prediction
        content_recommendation_enabled=True,

        # Platform tokens
        telegram_bot_token="your-telegram-bot-token",
        facebook_access_token="your-facebook-access-token",

        # High-performance settings for scale
        max_concurrent_operations=100,
        cache_ttl_seconds=600,
        batch_processing_size=1000,
        rate_limit_per_minute=200,

        # MLM community notifications
        alert_channel="@admin_channel",
        critical_alert_emails=["admin@mlm-company.com"],
        daily_report_enabled=True,
        weekly_analytics_enabled=True,

        # MLM-specific rules
        custom_moderation_rules={
            "income_claim_filter": True,
            "pyramid_scheme_mentions": True,
            "competitor_promotion_ban": True,
            "negative_sponsor_comments": True,
            "unrealistic_promise_filter": True
        },
        custom_engagement_triggers={
            "rank_advancement_celebration": True,
            "monthly_bonus_announcements": True,
            "top_performer_recognition": True,
            "new_product_launches": True,
            "training_event_reminders": True
        },
        custom_viral_mechanics={
            "sponsor_recruitment_contests": True,
            "success_story_amplification": True,
            "team_building_challenges": True,
            "milestone_achievement_sharing": True,
            "mentor_mentee_program": True
        }
    )


# Example usage
if __name__ == "__main__":
    config = create_mlm_community_config()
    print(f"MLM community config created for: {config.community_name}")
    print(f"Expected members: {config.expected_members:,}")
    print(f"MLM features enabled: {config.mlm_features_enabled}")
    print(f"Growth target: {config.growth_target_monthly:.0%} monthly")