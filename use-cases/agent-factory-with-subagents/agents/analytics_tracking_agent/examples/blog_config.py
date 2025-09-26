# -*- coding: utf-8 -*-
"""
Пример конфигурации Analytics & Tracking Agent для блог проектов
Настроен для контентных сайтов с фокусом на читательскую аудиторию и engagement
"""

import os
from ..settings import Settings
from ..dependencies import AnalyticsTrackingDependencies

def get_blog_config() -> AnalyticsTrackingDependencies:
    """
    Конфигурация агента для блог проектов.

    Включает:
    - Content performance tracking
    - Reader engagement analytics
    - Social sharing analysis
    - Newsletter subscription tracking
    - Author performance metrics
    """

    # Настройки для блога
    settings = Settings(
        # Основные настройки LLM
        llm_api_key=os.getenv("LLM_API_KEY", "your-llm-api-key"),

        # Тип проекта
        project_type="blog_analytics",
        domain_type="analytics",
        tracking_focus="engagement",

        # Google Analytics для content tracking
        ga4_measurement_id=os.getenv("GA4_MEASUREMENT_ID", "G-XXXXXXXXXX"),
        ga4_api_secret=os.getenv("GA4_API_SECRET"),

        # Mixpanel для detailed reader behavior (опционально)
        mixpanel_project_token=os.getenv("MIXPANEL_TOKEN"),
        mixpanel_api_key=os.getenv("MIXPANEL_API_KEY"),

        # Blog специфичные настройки
        enable_content_tracking=True,
        enable_user_journey_mapping=True,

        # Privacy compliance для блогов
        gdpr_compliance=True,
        ccpa_compliance=False,  # Обычно не критично для контентных сайтов
        anonymize_ip=True,
        cookie_consent_required=True,

        # Performance настройки для контента
        enable_batch_events=True,
        batch_size=20,  # Малый batch для reading events
        flush_interval=6000  # Медленная отправка для читательских событий
    )

    return AnalyticsTrackingDependencies(
        settings=settings,
        domain_type="analytics",
        project_type="blog_analytics",
        tracking_focus="engagement",

        # Blog провайдеры
        analytics_providers=["google_analytics", "mixpanel"],
        primary_provider="google_analytics",

        # Специализированные knowledge tags
        knowledge_tags=[
            "analytics-tracking", "agent-knowledge", "pydantic-ai",
            "blog", "content-analytics", "reader-engagement",
            "google-analytics", "content-performance", "social-sharing",
            "newsletter-analytics", "seo-tracking", "author-metrics"
        ],

        # Blog оптимизации
        enable_batch_processing=True,
        batch_size=20,
        gdpr_enabled=True,
        ccpa_enabled=False
    )

# Пример событий для блога
BLOG_EVENTS = {
    "post_view": {
        "description": "Просмотр статьи",
        "parameters": ["post_id", "post_title", "post_category", "author", "word_count", "reading_time"],
        "example": {
            "post_id": "post_123",
            "post_title": "Как создать успешный блог",
            "post_category": "Blogging",
            "author": "john_doe",
            "word_count": 1500,
            "reading_time": "7 min"
        }
    },

    "reading_progress": {
        "description": "Прогресс чтения статьи",
        "parameters": ["post_id", "progress_percentage", "time_spent", "reading_speed"],
        "example": {
            "post_id": "post_123",
            "progress_percentage": 75,
            "time_spent": 300,  # секунд
            "reading_speed": "normal"  # slow, normal, fast
        }
    },

    "social_share": {
        "description": "Поделиться в социальных сетях",
        "parameters": ["post_id", "platform", "share_type", "post_category"],
        "example": {
            "post_id": "post_123",
            "platform": "twitter",
            "share_type": "native_share",  # native_share, copy_link
            "post_category": "Technology"
        }
    },

    "comment": {
        "description": "Комментарий к статье",
        "parameters": ["post_id", "comment_id", "comment_length", "is_reply", "author_response"],
        "example": {
            "post_id": "post_123",
            "comment_id": "comment_456",
            "comment_length": 150,
            "is_reply": False,
            "author_response": False
        }
    },

    "newsletter_signup": {
        "description": "Подписка на рассылку",
        "parameters": ["signup_source", "post_id", "signup_type", "lead_magnet"],
        "example": {
            "signup_source": "inline_form",
            "post_id": "post_123",
            "signup_type": "newsletter",
            "lead_magnet": "free_ebook"
        }
    },

    "category_view": {
        "description": "Просмотр категории",
        "parameters": ["category_name", "posts_count", "view_source"],
        "example": {
            "category_name": "Web Development",
            "posts_count": 25,
            "view_source": "navigation_menu"
        }
    },

    "author_follow": {
        "description": "Подписка на автора",
        "parameters": ["author_id", "author_name", "follow_source", "posts_read_before"],
        "example": {
            "author_id": "author_123",
            "author_name": "Jane Smith",
            "follow_source": "author_page",
            "posts_read_before": 3
        }
    },

    "search": {
        "description": "Поиск по блогу",
        "parameters": ["search_query", "results_count", "result_clicked", "search_source"],
        "example": {
            "search_query": "react hooks tutorial",
            "results_count": 5,
            "result_clicked": True,
            "search_source": "header_search"
        }
    }
}

# KPI для блога
BLOG_KPIS = {
    "unique_visitors": {
        "name": "Unique Visitors",
        "description": "Количество уникальных посетителей за период",
        "formula": "COUNT(DISTINCT user_id)",
        "target": "Рост месяц к месяцу ≥ 10%"
    },

    "returning_visitors": {
        "name": "Returning Visitors Rate",
        "description": "Процент возвращающихся читателей",
        "formula": "Returning Users / Total Users * 100",
        "target": "> 30%"
    },

    "average_session_duration": {
        "name": "Average Session Duration",
        "description": "Среднее время, проведенное на сайте за сессию",
        "formula": "Total Session Duration / Total Sessions",
        "target": "> 2 минуты"
    },

    "bounce_rate": {
        "name": "Bounce Rate",
        "description": "Процент пользователей, покинувших сайт после просмотра одной страницы",
        "formula": "Single Page Sessions / Total Sessions * 100",
        "target": "< 60%"
    },

    "pages_per_session": {
        "name": "Pages per Session",
        "description": "Среднее количество страниц за сессию",
        "formula": "Total Pageviews / Total Sessions",
        "target": "> 2.5"
    },

    "post_engagement_rate": {
        "name": "Post Engagement Rate",
        "description": "Процент читателей, взаимодействующих с контентом",
        "formula": "(Comments + Shares + Newsletter Signups) / Post Views * 100",
        "target": "> 5%"
    },

    "newsletter_conversion": {
        "name": "Newsletter Conversion Rate",
        "description": "Процент читателей, подписавшихся на рассылку",
        "formula": "Newsletter Signups / Unique Visitors * 100",
        "target": "> 2%"
    },

    "social_sharing_rate": {
        "name": "Social Sharing Rate",
        "description": "Процент статей, которыми поделились в соцсетях",
        "formula": "Posts with Shares / Total Posts * 100",
        "target": "> 15%"
    }
}

# Сегменты читателей для блога
READER_SEGMENTS = {
    "first_time_visitors": {
        "description": "Первичные посетители",
        "criteria": "Session count = 1",
        "marketing_focus": "Newsletter signup, content discovery"
    },

    "regular_readers": {
        "description": "Постоянные читатели",
        "criteria": "Sessions > 3 AND last visit < 30 days",
        "marketing_focus": "Premium content, author following"
    },

    "engaged_readers": {
        "description": "Активные читатели",
        "criteria": "Comments > 0 OR shares > 0 OR newsletter subscriber",
        "marketing_focus": "Community building, guest posting opportunities"
    },

    "category_focused": {
        "description": "Читатели с интересом к определенной категории",
        "criteria": "80%+ pageviews in single category",
        "marketing_focus": "Category-specific content, expert positioning"
    },

    "high_value_readers": {
        "description": "Ценные читатели",
        "criteria": "High session duration + multiple visits + social sharing",
        "marketing_focus": "Exclusive content, affiliate partnerships"
    },

    "at_risk_subscribers": {
        "description": "Подписчики в риске оттока",
        "criteria": "Newsletter subscriber + no visits in last 45 days",
        "marketing_focus": "Re-engagement emails, content highlights"
    }
}

# Контентные метрики
CONTENT_METRICS = {
    "top_performing_posts": {
        "description": "Самые популярные статьи",
        "metrics": ["pageviews", "time_on_page", "social_shares", "comments"]
    },

    "author_performance": {
        "description": "Эффективность авторов",
        "metrics": ["avg_pageviews_per_post", "engagement_rate", "follower_growth"]
    },

    "category_performance": {
        "description": "Популярность категорий",
        "metrics": ["category_pageviews", "subscriber_interest", "time_on_category"]
    },

    "seo_performance": {
        "description": "SEO эффективность",
        "metrics": ["organic_traffic", "keyword_rankings", "click_through_rate"]
    }
}

def get_blog_setup_guide():
    """Руководство по настройке блог аналитики."""

    return """
# 📝 Blog Analytics Setup Guide

## 1. ОБЯЗАТЕЛЬНАЯ НАСТРОЙКА

### Google Analytics 4 для блогов:
```javascript
// Enhanced измерения для контента
gtag('config', 'GA_MEASUREMENT_ID', {
    // Автоматическое отслеживание scroll depth
    enhanced_measurement: {
        scroll_events: true,
        outbound_clicks: true,
        site_search: true,
        video_engagement: true,
        file_downloads: true
    }
});

// Custom события для блога
gtag('event', 'post_view', {
    'custom_parameters': {
        'post_id': 'post-123',
        'post_category': 'Technology',
        'author': 'john-doe',
        'word_count': 1500,
        'reading_time': 7
    }
});
```

### Content-specific события:
```javascript
// Отслеживание прогресса чтения
function trackReadingProgress() {
    let scrollPercent = Math.round(
        (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
    );

    if ([25, 50, 75, 100].includes(scrollPercent)) {
        gtag('event', 'reading_progress', {
            'post_id': getCurrentPostId(),
            'progress_percentage': scrollPercent,
            'time_spent': getTimeOnPage()
        });
    }
}

// Поделиться в социальных сетях
function trackSocialShare(platform, postId) {
    gtag('event', 'social_share', {
        'platform': platform,
        'post_id': postId,
        'share_type': 'native_share'
    });

    // Mixpanel для детального анализа
    mixpanel.track('Content Shared', {
        'Platform': platform,
        'Post ID': postId,
        'Post Category': getCurrentPostCategory(),
        'Author': getCurrentAuthor()
    });
}
```

## 2. КЛЮЧЕВЫЕ СОБЫТИЯ ДЛЯ БЛОГОВ

### Content Engagement:
- ✅ post_view - просмотр статьи (с метаданными)
- ✅ reading_progress - прогресс чтения (25%, 50%, 75%, 100%)
- ✅ time_on_page - время на странице
- ✅ scroll_depth - глубина прокрутки

### Social Interaction:
- ✅ social_share - поделиться в соцсетях
- ✅ comment - комментарий к статье
- ✅ like_post - лайк статьи (если есть)
- ✅ bookmark - добавить в закладки

### Newsletter & Subscriptions:
- ✅ newsletter_signup - подписка на рассылку
- ✅ author_follow - подписка на автора
- ✅ category_subscribe - подписка на категорию

### Navigation:
- ✅ category_view - просмотр категории
- ✅ tag_view - просмотр по тегу
- ✅ search - поиск по сайту
- ✅ related_post_click - клик по похожим статьям

## 3. БЛОГ ДАШБОРДЫ И ОТЧЕТЫ

### Content Performance Dashboard:
- Top Posts по pageviews, time on page, engagement
- Category Performance comparison
- Author Statistics и popularity
- Social Sharing Analysis по платформам

### Audience Analytics:
- Reader Segments (new, returning, engaged)
- Geographic Distribution читательской аудитории
- Device & Browser Analytics для content optimization
- Reading Patterns (peak hours, day of week)

### Growth Metrics:
- Unique Visitors growth month-over-month
- Newsletter Subscriber Growth
- Return Visitor Rate trend
- Content Engagement Rate по типам постов

## 4. АВТОМАТИЧЕСКИЕ СЕГМЕНТЫ

### Reader Behavior:
- Deep Readers (time on page > 3min)
- Skimmers (time on page < 30sec)
- Social Sharers (shared ≥ 1 post)
- Comment Contributors (left ≥ 1 comment)

### Content Preferences:
- Technology Enthusiasts (70%+ tech content)
- Tutorial Seekers (high engagement with how-to posts)
- Industry News Readers (frequent visits to news category)

### Subscription Status:
- Newsletter Subscribers
- Author Followers
- RSS Feed Subscribers
- Social Media Followers

## 5. SEO И CONTENT OPTIMIZATION

### SEO Tracking:
```javascript
// Отслеживание organic search
gtag('event', 'organic_search_landing', {
    'search_term': getUrlParameter('q'),
    'post_id': getCurrentPostId(),
    'search_engine': getReferrerSearchEngine()
});

// Внутренний поиск
gtag('event', 'site_search', {
    'search_term': searchQuery,
    'results_count': resultsCount,
    'search_location': 'header'
});
```

### Content A/B Testing:
- Заголовки статей
- Call-to-Action размещение
- Newsletter signup forms
- Social sharing buttons placement

## 6. PERFORMANCE MONITORING

### Core Web Vitals для блога:
- Largest Contentful Paint (LCP) < 2.5s
- Cumulative Layout Shift (CLS) < 0.1
- First Input Delay (FID) < 100ms

### Content Loading Optimization:
- Image optimization tracking
- Font loading performance
- Third-party script impact
- CDN performance metrics

## 7. PRIVACY И CONSENT

### GDPR для контентных сайтов:
```javascript
// Cookie consent для analytics
if (cookieConsentGiven) {
    // Полная аналитика
    gtag('config', 'GA_MEASUREMENT_ID', {
        'anonymize_ip': false,
        'allow_ad_personalization_signals': true
    });
} else {
    // Базовая аналитика без персонализации
    gtag('config', 'GA_MEASUREMENT_ID', {
        'anonymize_ip': true,
        'allow_ad_personalization_signals': false
    });
}
```

## 8. ИНТЕГРАЦИИ ДЛЯ БЛОГОВ

### Content Management:
- WordPress/Ghost analytics plugins
- Social media scheduling tools correlation
- Email marketing platform integration (Mailchimp/ConvertKit)

### Author Tools:
- Writing performance dashboard
- Content idea tracking
- Reader feedback aggregation
- Social media mention monitoring

### Revenue Tracking (если применимо):
- Affiliate link click tracking
- Sponsored content performance
- Product placement effectiveness
- Newsletter monetization metrics
"""

if __name__ == "__main__":
    # Пример использования
    config = get_blog_config()
    print("Blog конфигурация создана:")
    print(f"- Тип проекта: {config.project_type}")
    print(f"- Analytics провайдеры: {config.analytics_providers}")
    print(f"- Ключевые метрики: {config.get_key_metrics()}")
    print(f"- Рекомендуемые события: {config.get_recommended_events()}")