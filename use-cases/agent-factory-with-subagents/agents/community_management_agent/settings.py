"""
Settings configuration for Community Management Agent.

Load and validate environment variables and settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional


class Settings(BaseSettings):
    """Settings for Community Management Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for LLM provider")
    llm_model: str = Field(default="gpt-4", description="Model name")
    llm_base_url: Optional[str] = Field(
        default=None,
        description="Custom base URL for API"
    )

    # Community Platform Keys
    discord_token: Optional[str] = Field(
        default=None,
        env="DISCORD_BOT_TOKEN",
        description="Discord bot token"
    )
    telegram_bot_token: Optional[str] = Field(
        default=None,
        env="TELEGRAM_BOT_TOKEN",
        description="Telegram bot token"
    )
    facebook_access_token: Optional[str] = Field(
        default=None,
        env="FACEBOOK_ACCESS_TOKEN",
        description="Facebook Graph API token"
    )
    reddit_client_id: Optional[str] = Field(
        default=None,
        env="REDDIT_CLIENT_ID",
        description="Reddit app client ID"
    )
    reddit_client_secret: Optional[str] = Field(
        default=None,
        env="REDDIT_CLIENT_SECRET",
        description="Reddit app client secret"
    )
    slack_bot_token: Optional[str] = Field(
        default=None,
        env="SLACK_BOT_TOKEN",
        description="Slack bot token"
    )
    twitter_api_key: Optional[str] = Field(
        default=None,
        env="TWITTER_API_KEY",
        description="Twitter API key"
    )

    # Community Settings
    community_name: str = Field(
        default="My Community",
        env="COMMUNITY_NAME",
        description="Name of the community"
    )
    community_type: str = Field(
        default="social",
        env="COMMUNITY_TYPE",
        description="Type of community"
    )
    expected_members: int = Field(
        default=10000,
        env="EXPECTED_MEMBERS",
        description="Expected community size"
    )
    growth_target: float = Field(
        default=0.20,
        env="GROWTH_TARGET_MONTHLY",
        description="Monthly growth target (decimal)"
    )

    # Feature Flags
    enable_auto_moderation: bool = Field(
        default=True,
        env="ENABLE_AUTO_MODERATION",
        description="Enable automatic content moderation"
    )
    enable_influencer_program: bool = Field(
        default=False,
        env="ENABLE_INFLUENCER_PROGRAM",
        description="Enable influencer identification and management"
    )
    enable_viral_mechanics: bool = Field(
        default=True,
        env="ENABLE_VIRAL_MECHANICS",
        description="Enable viral growth features"
    )
    enable_mlm_features: bool = Field(
        default=False,
        env="ENABLE_MLM_FEATURES",
        description="Enable MLM-specific features"
    )
    enable_sentiment_analysis: bool = Field(
        default=True,
        env="ENABLE_SENTIMENT_ANALYSIS",
        description="Enable sentiment analysis"
    )

    # Performance Settings
    max_concurrent_operations: int = Field(
        default=10,
        env="MAX_CONCURRENT_OPS",
        description="Maximum concurrent operations"
    )
    cache_ttl: int = Field(
        default=300,
        env="CACHE_TTL_SECONDS",
        description="Cache time-to-live in seconds"
    )
    batch_size: int = Field(
        default=100,
        env="BATCH_PROCESSING_SIZE",
        description="Batch processing size"
    )


def load_settings() -> Settings:
    """
    Load and validate settings from environment.

    Returns:
        Validated settings instance
    """
    load_dotenv()

    try:
        settings = Settings()
        return settings
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nPlease set LLM_API_KEY in .env file"
        raise ValueError(error_msg) from e