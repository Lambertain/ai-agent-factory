"""
Tools for Community Management Agent.

Provides automated moderation, engagement optimization, and community analytics tools.
"""

from pydantic_ai import RunContext
from typing import Dict, List, Any, Optional, Tuple
import random
from datetime import datetime, timedelta
from .dependencies import CommunityManagementDependencies, ModerationLevel


async def moderate_content(
    ctx: RunContext[CommunityManagementDependencies],
    content: str,
    author_id: str,
    platform: str,
    content_type: str = "text"
) -> Dict[str, Any]:
    """
    Moderate user-generated content for toxicity, spam, and policy violations.

    Args:
        content: The content to moderate
        author_id: ID of the content author
        platform: Platform where content was posted
        content_type: Type of content (text, image, video)

    Returns:
        Moderation result with action recommendations
    """
    moderation_config = ctx.deps.get_moderation_config()

    # Simulate toxicity analysis (in production, use ML model)
    toxicity_score = random.random() * 0.8  # Simulated score

    # Check against thresholds
    is_toxic = toxicity_score > moderation_config["toxicity_threshold"]

    # Check for spam patterns
    spam_indicators = [
        content.count("http") > 3,
        content.count("@") > 5,
        len(content) > 5000,
        content.isupper() and len(content) > 50,
        "buy now" in content.lower(),
        "click here" in content.lower()
    ]
    spam_score = sum(spam_indicators) / len(spam_indicators)
    is_spam = spam_score > moderation_config.get("spam_threshold", 0.5)

    # Determine action
    action = "approve"
    if is_toxic or is_spam:
        action = "delete" if moderation_config["auto_delete"] else "flag"

    return {
        "content_id": f"{platform}_{author_id}_{datetime.now().timestamp()}",
        "action": action,
        "toxicity_score": toxicity_score,
        "spam_score": spam_score,
        "is_toxic": is_toxic,
        "is_spam": is_spam,
        "reasons": [],
        "platform": platform,
        "moderation_level": ctx.deps.moderation_level.value,
        "timestamp": datetime.now().isoformat()
    }


async def identify_influencers(
    ctx: RunContext[CommunityManagementDependencies],
    member_stats: List[Dict[str, Any]],
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Identify top influencers in the community based on engagement metrics.

    Args:
        member_stats: List of member statistics
        top_n: Number of top influencers to return

    Returns:
        List of identified influencers with scores and tiers
    """
    influencer_tiers = ctx.deps.get_influencer_tiers()
    influencers = []

    for member in member_stats:
        # Calculate influence score
        follower_weight = 0.3
        engagement_weight = 0.4
        content_weight = 0.3

        follower_score = min(member.get("followers", 0) / 10000, 1.0)
        engagement_score = member.get("engagement_rate", 0)
        content_score = min(member.get("content_count", 0) / 100, 1.0)

        influence_score = (
            follower_score * follower_weight +
            engagement_score * engagement_weight +
            content_score * content_weight
        )

        # Determine tier
        tier = "none"
        followers = member.get("followers", 0)
        engagement = member.get("engagement_rate", 0)

        for tier_name, tier_config in influencer_tiers.items():
            min_followers = tier_config["min_followers"]
            max_followers = tier_config["max_followers"] or float('inf')
            min_engagement = tier_config["min_engagement"]

            if min_followers <= followers <= max_followers and engagement >= min_engagement:
                tier = tier_name
                break

        if influence_score > 0.1:  # Threshold for influencer status
            influencers.append({
                "member_id": member["id"],
                "username": member.get("username", "unknown"),
                "influence_score": round(influence_score, 3),
                "tier": tier,
                "followers": followers,
                "engagement_rate": engagement,
                "content_count": member.get("content_count", 0),
                "benefits": influencer_tiers.get(tier, {}).get("benefits", []),
                "potential_reach": followers * (1 + engagement)
            })

    # Sort by influence score and return top N
    influencers.sort(key=lambda x: x["influence_score"], reverse=True)
    return influencers[:top_n]


async def analyze_sentiment(
    ctx: RunContext[CommunityManagementDependencies],
    messages: List[str],
    time_window: str = "24h"
) -> Dict[str, Any]:
    """
    Analyze community sentiment from recent messages.

    Args:
        messages: List of recent messages
        time_window: Time window for analysis

    Returns:
        Sentiment analysis results with trends
    """
    if not messages:
        return {
            "overall_sentiment": "neutral",
            "sentiment_score": 0.0,
            "positive_ratio": 0.0,
            "negative_ratio": 0.0,
            "neutral_ratio": 1.0,
            "trend": "stable",
            "sample_size": 0
        }

    # Simulate sentiment analysis (in production, use NLP model)
    positive_keywords = ["love", "awesome", "great", "amazing", "thank", "happy", "excellent", "wonderful"]
    negative_keywords = ["hate", "terrible", "awful", "bad", "angry", "disappointed", "frustrating", "worst"]

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for message in messages:
        message_lower = message.lower()
        pos_score = sum(1 for keyword in positive_keywords if keyword in message_lower)
        neg_score = sum(1 for keyword in negative_keywords if keyword in message_lower)

        if pos_score > neg_score:
            positive_count += 1
        elif neg_score > pos_score:
            negative_count += 1
        else:
            neutral_count += 1

    total = len(messages)
    positive_ratio = positive_count / total
    negative_ratio = negative_count / total
    neutral_ratio = neutral_count / total

    # Calculate overall sentiment
    sentiment_score = positive_ratio - negative_ratio
    if sentiment_score > 0.3:
        overall_sentiment = "positive"
    elif sentiment_score < -0.3:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"

    # Determine trend (simulated)
    trend = "stable"
    if positive_ratio > 0.6:
        trend = "improving"
    elif negative_ratio > 0.4:
        trend = "declining"

    return {
        "overall_sentiment": overall_sentiment,
        "sentiment_score": round(sentiment_score, 3),
        "positive_ratio": round(positive_ratio, 3),
        "negative_ratio": round(negative_ratio, 3),
        "neutral_ratio": round(neutral_ratio, 3),
        "trend": trend,
        "sample_size": total,
        "time_window": time_window,
        "analysis_timestamp": datetime.now().isoformat(),
        "alerts": []
    }


async def detect_trending_topics(
    ctx: RunContext[CommunityManagementDependencies],
    messages: List[str],
    hashtags: List[str] = None,
    time_window: str = "6h"
) -> List[Dict[str, Any]]:
    """
    Detect trending topics and hashtags in the community.

    Args:
        messages: Recent messages to analyze
        hashtags: Optional list of hashtags to track
        time_window: Time window for trend detection

    Returns:
        List of trending topics with metrics
    """
    # Extract topics (simplified - in production use NLP)
    topic_counts = {}

    # Count hashtags
    if hashtags:
        for tag in hashtags:
            topic_counts[tag] = topic_counts.get(tag, 0) + 1

    # Extract common words as topics (simplified)
    common_topics = [
        "announcement", "event", "update", "question", "help",
        "feature", "bug", "suggestion", "community", "welcome"
    ]

    for message in messages:
        message_lower = message.lower()
        for topic in common_topics:
            if topic in message_lower:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

    # Calculate trending score
    trending_topics = []
    for topic, count in topic_counts.items():
        # Simulate velocity (growth rate)
        velocity = random.uniform(0.5, 2.0)

        trending_score = count * velocity

        trending_topics.append({
            "topic": topic,
            "mention_count": count,
            "velocity": round(velocity, 2),
            "trending_score": round(trending_score, 2),
            "sentiment": "positive" if random.random() > 0.3 else "neutral",
            "estimated_reach": count * random.randint(10, 100),
            "time_window": time_window
        })

    # Sort by trending score
    trending_topics.sort(key=lambda x: x["trending_score"], reverse=True)
    return trending_topics[:10]  # Return top 10


async def optimize_engagement(
    ctx: RunContext[CommunityManagementDependencies],
    content: str,
    target_audience: str = "general",
    platform: str = "discord"
) -> Dict[str, Any]:
    """
    Optimize content for maximum engagement.

    Args:
        content: Content to optimize
        target_audience: Target audience segment
        platform: Platform for posting

    Returns:
        Optimized content with recommendations
    """
    # Get engagement thresholds
    thresholds = ctx.deps.get_engagement_thresholds()

    # Platform-specific optimizations
    platform_config = ctx.deps.get_platform_config(platform)
    max_length = platform_config.get("max_message_length", 2000)

    # Optimize content
    optimized_content = content
    recommendations = []

    # Length optimization
    if len(content) > max_length:
        optimized_content = content[:max_length-3] + "..."
        recommendations.append(f"Content truncated to {max_length} characters for {platform}")

    # Add engagement hooks
    hooks = {
        "question": "What do you think? 🤔",
        "poll": "Vote with reactions: 👍 for yes, 👎 for no",
        "call_to_action": "Share your experience below! 💬",
        "urgency": "⏰ Limited time - act fast!",
        "social_proof": "Join 1000+ community members who already..."
    }

    # Determine best posting time
    best_times = {
        "morning": "09:00",
        "lunch": "12:30",
        "evening": "19:00",
        "night": "21:00"
    }

    # Calculate predicted engagement
    base_engagement = random.uniform(0.05, 0.25)

    # Apply multipliers
    if "?" in content:
        base_engagement *= 1.3  # Questions increase engagement
    if len(content) < 280:
        base_engagement *= 1.2  # Shorter content performs better
    if any(emoji in content for emoji in ["🎉", "🚀", "💡", "❤️"]):
        base_engagement *= 1.1  # Emojis boost engagement

    predicted_engagement = min(base_engagement, 1.0)

    return {
        "original_content": content,
        "optimized_content": optimized_content,
        "recommendations": recommendations,
        "suggested_hooks": list(hooks.values())[:3],
        "best_posting_time": best_times.get("evening"),
        "predicted_engagement_rate": round(predicted_engagement, 3),
        "engagement_category": "high" if predicted_engagement > thresholds["high_engagement"] else "normal",
        "platform_specific": {
            "max_length": max_length,
            "optimal_media": "image" if platform in ["instagram", "facebook"] else "text",
            "hashtag_limit": 30 if platform == "instagram" else 5
        }
    }


async def track_community_health(
    ctx: RunContext[CommunityManagementDependencies],
    metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Track and analyze overall community health.

    Args:
        metrics: Current community metrics

    Returns:
        Community health score and recommendations
    """
    # Calculate health score components
    activity_score = min(metrics.get("daily_active_users", 0) / max(ctx.deps.current_members, 1), 1.0)
    retention_score = metrics.get("retention_30d", 0.5)
    sentiment_score = metrics.get("positive_sentiment_ratio", 0.5)
    growth_score = min(metrics.get("growth_rate", 0) / ctx.deps.growth_target_monthly, 1.0)

    # Calculate overall health score
    health_score = (
        activity_score * 0.3 +
        retention_score * 0.3 +
        sentiment_score * 0.2 +
        growth_score * 0.2
    )

    # Determine health status
    if health_score > 0.8:
        status = "excellent"
    elif health_score > 0.6:
        status = "good"
    elif health_score > 0.4:
        status = "fair"
    else:
        status = "needs_attention"

    # Generate recommendations
    recommendations = []
    if activity_score < 0.5:
        recommendations.append("Increase engagement activities and events")
    if retention_score < 0.6:
        recommendations.append("Improve onboarding and member value proposition")
    if sentiment_score < 0.6:
        recommendations.append("Address community concerns and increase positive interactions")
    if growth_score < 0.5:
        recommendations.append("Implement viral growth strategies and referral programs")

    return {
        "health_score": round(health_score, 3),
        "status": status,
        "components": {
            "activity": round(activity_score, 3),
            "retention": round(retention_score, 3),
            "sentiment": round(sentiment_score, 3),
            "growth": round(growth_score, 3)
        },
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat(),
        "member_count": ctx.deps.current_members,
        "expected_members": ctx.deps.expected_members
    }


async def automate_welcome(
    ctx: RunContext[CommunityManagementDependencies],
    new_member: Dict[str, Any],
    platform: str
) -> str:
    """
    Generate personalized welcome message for new members.

    Args:
        new_member: Information about the new member
        platform: Platform where member joined

    Returns:
        Personalized welcome message
    """
    username = new_member.get("username", "friend")
    member_number = ctx.deps.current_members + 1

    # Platform-specific formatting
    if platform == "discord":
        mention = f"<@{new_member.get('id', '')}>"
    elif platform == "telegram":
        mention = f"@{username}"
    else:
        mention = f"@{username}"

    # Generate welcome message
    templates = [
        f"🎉 Welcome to {ctx.deps.community_name}, {mention}! You're member #{member_number}. We're excited to have you here!",
        f"👋 Hey {mention}! Welcome aboard! You're now part of our amazing {ctx.deps.community_name} community!",
        f"🚀 Welcome {mention}! Great to see you join {ctx.deps.community_name}! Check out our pinned messages to get started."
    ]

    welcome_message = random.choice(templates)

    # Add onboarding instructions
    if ctx.deps.community_type == "MLM":
        welcome_message += "\n\n💼 Check out our training resources and connect with your mentor!"
    elif ctx.deps.community_type == "EDUCATIONAL":
        welcome_message += "\n\n📚 Browse our learning paths and join study groups!"
    elif ctx.deps.community_type == "GAMING":
        welcome_message += "\n\n🎮 Find your squad and join the action!"

    return welcome_message


async def manage_viral_campaign(
    ctx: RunContext[CommunityManagementDependencies],
    campaign_type: str,
    campaign_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Manage viral growth campaigns.

    Args:
        campaign_type: Type of viral campaign
        campaign_data: Campaign configuration

    Returns:
        Campaign execution result
    """
    campaign_results = {
        "campaign_id": f"campaign_{datetime.now().timestamp()}",
        "type": campaign_type,
        "status": "active",
        "start_time": datetime.now().isoformat()
    }

    if campaign_type == "referral":
        # Referral campaign logic
        campaign_results.update({
            "referral_code": f"{ctx.deps.community_name[:3].upper()}{random.randint(1000, 9999)}",
            "reward_structure": {
                "referrer": "10 points per successful referral",
                "referee": "5 points welcome bonus"
            },
            "tracking_enabled": True,
            "projected_growth": f"{ctx.deps.growth_target_monthly * 100:.0f}%"
        })

    elif campaign_type == "contest":
        # Contest campaign logic
        campaign_results.update({
            "contest_name": campaign_data.get("name", "Community Challenge"),
            "prizes": campaign_data.get("prizes", ["1st: Premium membership", "2nd: Merch pack"]),
            "participation_method": "Share and tag friends",
            "viral_coefficient": random.uniform(1.2, 2.5)
        })

    elif campaign_type == "ugc":
        # User-generated content campaign
        campaign_results.update({
            "hashtag": f"#{ctx.deps.community_name}Challenge",
            "content_type": "photos/videos",
            "amplification_strategy": "Feature best content",
            "expected_submissions": ctx.deps.current_members * 0.1
        })

    return campaign_results