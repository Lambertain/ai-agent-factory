"""
Community Management Agent - Universal agent for managing large-scale communities.

This agent provides automated community moderation, engagement optimization,
and viral growth mechanics for communities of any size and type.
"""

from .agent import agent
from .dependencies import CommunityManagementDependencies
from .tools import (
    moderate_content,
    identify_influencers,
    analyze_sentiment,
    detect_trending_topics,
    optimize_engagement
)

__all__ = [
    "agent",
    "CommunityManagementDependencies",
    "moderate_content",
    "identify_influencers",
    "analyze_sentiment",
    "detect_trending_topics",
    "optimize_engagement"
]