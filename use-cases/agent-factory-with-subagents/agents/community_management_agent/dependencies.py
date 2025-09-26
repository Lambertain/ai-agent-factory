"""
Dependencies for Community Management Agent.

Configurable settings for different community types and scales.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class CommunityType(str, Enum):
    """Types of communities the agent can manage."""
    SOCIAL = "social"
    PROFESSIONAL = "professional"
    GAMING = "gaming"
    EDUCATIONAL = "educational"
    MLM = "mlm"
    SUPPORT = "support"
    BRAND = "brand"
    CREATOR = "creator"
    OPENSOURCE = "opensource"


class CommunityPlatform(str, Enum):
    """Supported community platforms."""
    DISCORD = "discord"
    TELEGRAM = "telegram"
    FACEBOOK = "facebook"
    REDDIT = "reddit"
    SLACK = "slack"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    CUSTOM = "custom"


class ModerationLevel(str, Enum):
    """Content moderation strictness levels."""
    RELAXED = "relaxed"      # Minimal moderation
    STANDARD = "standard"    # Balanced approach
    STRICT = "strict"        # High moderation
    CUSTOM = "custom"        # Custom rules


@dataclass
class CommunityManagementDependencies:
    """Dependencies for Community Management Agent."""

    # Core configuration
    api_key: str
    community_name: str = "My Community"
    community_type: CommunityType = CommunityType.SOCIAL
    platforms: List[CommunityPlatform] = field(default_factory=lambda: [CommunityPlatform.DISCORD])

    # Scale configuration
    expected_members: int = 1000
    current_members: int = 0
    growth_target_monthly: float = 0.20  # 20% monthly growth

    # Moderation settings
    moderation_level: ModerationLevel = ModerationLevel.STANDARD
    toxicity_threshold: float = 0.7
    spam_detection_enabled: bool = True
    auto_ban_enabled: bool = False
    profanity_filter_enabled: bool = True

    # Language and localization
    primary_language: str = "en"
    supported_languages: List[str] = field(default_factory=lambda: ["en"])
    timezone: str = "UTC"
    cultural_adaptation_enabled: bool = True

    # Engagement settings
    auto_welcome_enabled: bool = True
    engagement_tracking_enabled: bool = True
    influencer_program_enabled: bool = False
    gamification_enabled: bool = True

    # Viral growth settings
    referral_program_enabled: bool = False
    viral_mechanics_enabled: bool = True
    social_proof_amplification: bool = True
    ugc_curation_enabled: bool = True

    # MLM specific settings (if applicable)
    mlm_features_enabled: bool = False
    mlm_tier_tracking: bool = False
    mlm_commission_tracking: bool = False
    mlm_training_distribution: bool = False

    # AI features
    sentiment_analysis_enabled: bool = True
    trend_detection_enabled: bool = True
    predictive_analytics_enabled: bool = False
    content_recommendation_enabled: bool = True

    # Platform-specific credentials
    discord_token: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    facebook_access_token: Optional[str] = None
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    slack_bot_token: Optional[str] = None
    twitter_api_key: Optional[str] = None

    # Performance settings
    max_concurrent_operations: int = 10
    cache_ttl_seconds: int = 300
    batch_processing_size: int = 100
    rate_limit_per_minute: int = 60

    # Notification settings
    alert_channel: Optional[str] = None
    critical_alert_emails: List[str] = field(default_factory=list)
    daily_report_enabled: bool = True
    weekly_analytics_enabled: bool = True

    # Custom rules and patterns
    custom_moderation_rules: Dict[str, Any] = field(default_factory=dict)
    custom_engagement_triggers: Dict[str, Any] = field(default_factory=dict)
    custom_viral_mechanics: Dict[str, Any] = field(default_factory=dict)

    # Archon integration
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"
    enable_task_communication: bool = True
    agent_name: str = "community_management_agent"

    def __post_init__(self):
        """Validate and adjust settings based on scale."""
        # Auto-adjust settings based on expected scale
        if self.expected_members > 100000:
            # Large scale optimizations
            self.max_concurrent_operations = min(50, self.max_concurrent_operations * 5)
            self.batch_processing_size = min(500, self.batch_processing_size * 5)
            self.predictive_analytics_enabled = True

        if self.expected_members > 1000000:
            # Massive scale optimizations
            self.max_concurrent_operations = 100
            self.batch_processing_size = 1000
            self.cache_ttl_seconds = 600

        # Enable MLM features for MLM communities
        if self.community_type == CommunityType.MLM:
            self.mlm_features_enabled = True
            self.mlm_tier_tracking = True
            self.referral_program_enabled = True

        # Adjust moderation based on community type
        if self.community_type == CommunityType.PROFESSIONAL:
            self.moderation_level = ModerationLevel.STRICT
            self.profanity_filter_enabled = True

        elif self.community_type == CommunityType.GAMING:
            self.moderation_level = ModerationLevel.STANDARD
            self.gamification_enabled = True

    def get_platform_config(self, platform: CommunityPlatform) -> Dict[str, Any]:
        """Get platform-specific configuration."""
        configs = {
            CommunityPlatform.DISCORD: {
                "token": self.discord_token,
                "intents": ["guilds", "members", "messages", "reactions"],
                "command_prefix": "!",
                "max_message_length": 2000
            },
            CommunityPlatform.TELEGRAM: {
                "token": self.telegram_bot_token,
                "max_group_size": 200000,
                "max_message_length": 4096,
                "parse_mode": "MarkdownV2"
            },
            CommunityPlatform.FACEBOOK: {
                "access_token": self.facebook_access_token,
                "api_version": "v17.0",
                "max_post_length": 63206
            },
            CommunityPlatform.REDDIT: {
                "client_id": self.reddit_client_id,
                "client_secret": self.reddit_client_secret,
                "user_agent": f"{self.community_name} Bot",
                "max_title_length": 300,
                "max_text_length": 40000
            },
            CommunityPlatform.SLACK: {
                "bot_token": self.slack_bot_token,
                "max_message_length": 40000,
                "max_blocks": 50
            },
            CommunityPlatform.TWITTER: {
                "api_key": self.twitter_api_key,
                "max_tweet_length": 280,
                "max_thread_length": 25
            }
        }
        return configs.get(platform, {})

    def get_moderation_config(self) -> Dict[str, Any]:
        """Get moderation configuration based on level."""
        configs = {
            ModerationLevel.RELAXED: {
                "toxicity_threshold": 0.9,
                "spam_threshold": 0.95,
                "auto_delete": False,
                "warning_before_action": True
            },
            ModerationLevel.STANDARD: {
                "toxicity_threshold": 0.7,
                "spam_threshold": 0.85,
                "auto_delete": True,
                "warning_before_action": True
            },
            ModerationLevel.STRICT: {
                "toxicity_threshold": 0.5,
                "spam_threshold": 0.7,
                "auto_delete": True,
                "warning_before_action": False
            }
        }

        base_config = configs.get(self.moderation_level, configs[ModerationLevel.STANDARD])
        # Override with custom settings
        base_config.update(self.custom_moderation_rules)
        return base_config

    def get_engagement_thresholds(self) -> Dict[str, float]:
        """Get engagement thresholds based on community size."""
        if self.current_members < 1000:
            return {
                "low_engagement": 0.05,
                "normal_engagement": 0.15,
                "high_engagement": 0.30,
                "viral_threshold": 0.50
            }
        elif self.current_members < 10000:
            return {
                "low_engagement": 0.03,
                "normal_engagement": 0.10,
                "high_engagement": 0.20,
                "viral_threshold": 0.35
            }
        elif self.current_members < 100000:
            return {
                "low_engagement": 0.02,
                "normal_engagement": 0.07,
                "high_engagement": 0.15,
                "viral_threshold": 0.25
            }
        else:  # 100K+
            return {
                "low_engagement": 0.01,
                "normal_engagement": 0.05,
                "high_engagement": 0.10,
                "viral_threshold": 0.20
            }

    def get_influencer_tiers(self) -> Dict[str, Dict[str, Any]]:
        """Get influencer tier definitions based on community size."""
        base_size = max(1000, self.current_members)

        return {
            "nano": {
                "min_followers": int(base_size * 0.001),
                "max_followers": int(base_size * 0.01),
                "min_engagement": 0.08,
                "benefits": ["early_access", "recognition_badge"]
            },
            "micro": {
                "min_followers": int(base_size * 0.01),
                "max_followers": int(base_size * 0.1),
                "min_engagement": 0.05,
                "benefits": ["early_access", "special_badge", "exclusive_content"]
            },
            "macro": {
                "min_followers": int(base_size * 0.1),
                "max_followers": int(base_size * 0.5),
                "min_engagement": 0.03,
                "benefits": ["all_benefits", "direct_support", "collaboration_opportunities"]
            },
            "mega": {
                "min_followers": int(base_size * 0.5),
                "max_followers": None,
                "min_engagement": 0.015,
                "benefits": ["all_benefits", "revenue_sharing", "strategic_partnership"]
            }
        }