"""
Gaming community configuration example.

Example setup for managing a gaming community with competitive elements.
"""

from ..dependencies import (
    CommunityManagementDependencies,
    CommunityType,
    CommunityPlatform,
    ModerationLevel
)


def create_gaming_community_config() -> CommunityManagementDependencies:
    """
    Create configuration for gaming community.

    Returns:
        Gaming community dependencies
    """
    return CommunityManagementDependencies(
        # Core settings
        api_key="your-api-key-here",
        community_name="Elite Gamers Hub",
        community_type=CommunityType.GAMING,
        platforms=[CommunityPlatform.DISCORD, CommunityPlatform.REDDIT],

        # Scale configuration
        expected_members=50000,
        current_members=12000,
        growth_target_monthly=0.15,  # 15% monthly growth

        # Gaming-optimized moderation
        moderation_level=ModerationLevel.STANDARD,
        toxicity_threshold=0.6,  # More lenient for gaming banter
        spam_detection_enabled=True,
        auto_ban_enabled=False,
        profanity_filter_enabled=True,

        # Language settings
        primary_language="en",
        supported_languages=["en", "es", "de", "fr"],
        timezone="UTC",
        cultural_adaptation_enabled=True,

        # Gaming engagement features
        auto_welcome_enabled=True,
        engagement_tracking_enabled=True,
        influencer_program_enabled=True,  # For streamers/pro players
        gamification_enabled=True,  # Perfect for gaming

        # Viral growth for gaming
        referral_program_enabled=True,  # Friend referrals
        viral_mechanics_enabled=True,
        social_proof_amplification=True,  # Showcase achievements
        ugc_curation_enabled=True,  # Share gameplay clips

        # Gaming-specific AI features
        sentiment_analysis_enabled=True,  # Monitor toxicity
        trend_detection_enabled=True,  # Track popular games
        predictive_analytics_enabled=True,  # Predict tournament interest
        content_recommendation_enabled=True,

        # Platform-specific tokens
        discord_token="your-discord-bot-token",
        reddit_client_id="your-reddit-client-id",
        reddit_client_secret="your-reddit-client-secret",

        # Performance optimization for active community
        max_concurrent_operations=25,
        cache_ttl_seconds=180,  # Faster cache for real-time gaming
        batch_processing_size=200,
        rate_limit_per_minute=100,

        # Gaming community notifications
        alert_channel="#admin-alerts",
        daily_report_enabled=True,
        weekly_analytics_enabled=True,

        # Custom gaming rules
        custom_moderation_rules={
            "gaming_toxicity_threshold": 0.8,  # Higher threshold for competitive trash talk
            "elo_shaming_prevention": True,
            "clan_drama_auto_lock": True,
            "tournament_spoiler_filter": True
        },
        custom_engagement_triggers={
            "achievement_celebration": True,
            "tournament_announcements": True,
            "new_game_hype": True,
            "patch_discussions": True
        },
        custom_viral_mechanics={
            "clan_recruitment_boost": True,
            "tournament_sharing": True,
            "highlight_reel_contests": True,
            "speedrun_challenges": True
        }
    )


# Example usage
if __name__ == "__main__":
    config = create_gaming_community_config()
    print(f"Gaming community config created for: {config.community_name}")
    print(f"Expected members: {config.expected_members:,}")
    print(f"Platforms: {[p.value for p in config.platforms]}")
    print(f"Gamification enabled: {config.gamification_enabled}")