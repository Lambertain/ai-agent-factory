"""
Blog/CMS UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для блогов и CMS систем.
Включает специфичные UI компоненты для контента, читательского опыта и управления публикациями.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class BlogUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для Blog/CMS проектов."""

    # Основные настройки
    domain_type: str = "blog"
    project_type: str = "content_management"

    # Blog специфичные настройки
    enable_comments: bool = True
    enable_categories: bool = True
    enable_tags: bool = True
    enable_search: bool = True
    enable_newsletter: bool = True

    # Reading experience
    enable_reading_time: bool = True
    enable_reading_progress: bool = True
    enable_dark_mode_reading: bool = True
    enable_font_size_adjustment: bool = True
    enable_table_of_contents: bool = True

    # Social features
    enable_social_sharing: bool = True
    enable_author_profiles: bool = True
    enable_related_posts: bool = True
    enable_post_reactions: bool = True

    # Layout настройки
    article_layout: str = "centered"  # centered, wide, narrow
    sidebar_position: str = "right"   # left, right, none
    enable_featured_image: bool = True

    def get_color_scheme(self) -> Dict[str, Any]:
        """Цветовая схема для Blog/CMS."""
        return {
            "primary": "hsl(225, 6%, 13%)",    # Dark text for readability
            "secondary": "hsl(210, 16%, 82%)", # Light gray
            "success": "hsl(142, 76%, 36%)",   # Success green
            "warning": "hsl(38, 92%, 50%)",    # Warning amber
            "destructive": "hsl(0, 84%, 60%)", # Error red
            "accent": "hsl(262, 83%, 58%)",    # Accent purple

            # Blog specific colors
            "text_primary": "hsl(225, 6%, 13%)",   # Main text
            "text_secondary": "hsl(215, 16%, 47%)", # Secondary text
            "text_muted": "hsl(215, 16%, 57%)",     # Muted text
            "background": "hsl(0, 0%, 100%)",       # White background
            "surface": "hsl(210, 40%, 98%)",        # Light surface

            # Reading mode colors
            "reading_bg": "hsl(45, 29%, 97%)",      # Warm reading background
            "reading_text": "hsl(225, 6%, 13%)",   # Reading text
            "link": "hsl(221, 83%, 53%)",           # Link blue
            "link_hover": "hsl(221, 83%, 45%)",     # Darker on hover

            # Category colors
            "category_tech": "hsl(221, 83%, 53%)",
            "category_lifestyle": "hsl(142, 76%, 36%)",
            "category_business": "hsl(262, 83%, 58%)",
            "category_travel": "hsl(38, 92%, 50%)",
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для Blog/CMS."""
        return {
            "article": {
                "layout": self.article_layout,
                "max_width": "768px",
                "font_family": "Georgia, serif",
                "font_size": "18px",
                "line_height": "1.6",
                "show_reading_time": self.enable_reading_time,
                "show_progress": self.enable_reading_progress,
                "show_toc": self.enable_table_of_contents
            },
            "post_card": {
                "show_excerpt": True,
                "show_author": self.enable_author_profiles,
                "show_date": True,
                "show_category": self.enable_categories,
                "show_tags": self.enable_tags,
                "show_reading_time": self.enable_reading_time,
                "image_aspect_ratio": "16:9"
            },
            "navigation": {
                "show_categories": self.enable_categories,
                "show_search": self.enable_search,
                "show_theme_toggle": self.enable_dark_mode_reading,
                "sticky": True,
                "dropdown_categories": True
            },
            "sidebar": {
                "position": self.sidebar_position,
                "width": "320px",
                "show_recent_posts": True,
                "show_categories": self.enable_categories,
                "show_tags": self.enable_tags,
                "show_newsletter": self.enable_newsletter
            },
            "comments": {
                "enabled": self.enable_comments,
                "nested": True,
                "markdown": True,
                "emoji_reactions": self.enable_post_reactions,
                "moderation": True
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для Blog/CMS."""
        return {
            "article_layout": self.article_layout,
            "sidebar_position": self.sidebar_position,
            "spacing": {
                "section_gap": "4rem",
                "component_gap": "2rem",
                "element_gap": "1rem",
                "paragraph_gap": "1.5rem"
            },
            "containers": {
                "header": "full",
                "main": "wide" if self.article_layout == "wide" else "default",
                "footer": "full"
            },
            "grid": {
                "post_grid": {"mobile": 1, "tablet": 2, "desktop": 3},
                "featured_grid": {"mobile": 1, "tablet": 1, "desktop": 2}
            }
        }

    def get_typography_config(self) -> Dict[str, Any]:
        """Конфигурация типографики для Blog/CMS."""
        return {
            "headings": {
                "font_family": "Inter, system-ui, sans-serif",
                "font_weight": "600",
                "line_height": "1.25",
                "letter_spacing": "-0.025em"
            },
            "body": {
                "font_family": "Georgia, serif",
                "font_size": "18px",
                "line_height": "1.6",
                "font_weight": "400"
            },
            "ui": {
                "font_family": "Inter, system-ui, sans-serif",
                "font_size": "14px",
                "line_height": "1.5"
            },
            "scale": {
                "xs": "0.75rem",
                "sm": "0.875rem",
                "base": "1rem",
                "lg": "1.125rem",
                "xl": "1.25rem",
                "2xl": "1.5rem",
                "3xl": "1.875rem",
                "4xl": "2.25rem"
            }
        }

    def get_animation_config(self) -> Dict[str, Any]:
        """Конфигурация анимаций для Blog/CMS."""
        return {
            "page_transitions": {
                "duration": "300ms",
                "easing": "ease-out"
            },
            "reading_progress": {
                "type": "smooth",
                "duration": "100ms"
            },
            "hover_effects": {
                "post_card": "translateY(-4px)",
                "button": "scale(1.02)",
                "link": "underline"
            },
            "loading_states": {
                "skeleton": True,
                "fade_in": True,
                "stagger": True
            },
            "scroll_animations": {
                "fade_in_up": True,
                "parallax_header": True
            }
        }

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Конфигурация accessibility для Blog/CMS."""
        return {
            "high_contrast_mode": True,
            "keyboard_navigation": True,
            "screen_reader_optimized": True,
            "focus_indicators": True,
            "reduced_motion": True,
            "reading_aids": {
                "font_size_control": self.enable_font_size_adjustment,
                "line_height_control": True,
                "reading_mode": self.enable_dark_mode_reading
            },
            "aria_labels": {
                "article": "Article: {title}",
                "read_more": "Read more about {title}",
                "comment_form": "Leave a comment",
                "share_button": "Share {title}",
                "category": "Category: {name}",
                "tag": "Tag: {name}"
            },
            "skip_links": [
                {"href": "#main", "label": "Skip to main content"},
                {"href": "#article", "label": "Skip to article"},
                {"href": "#comments", "label": "Skip to comments"}
            ]
        }

    def get_seo_config(self) -> Dict[str, Any]:
        """Конфигурация SEO для Blog/CMS."""
        return {
            "meta_tags": {
                "og_image": True,
                "twitter_card": True,
                "structured_data": True,
                "canonical_url": True
            },
            "article_schema": {
                "headline": True,
                "author": self.enable_author_profiles,
                "date_published": True,
                "date_modified": True,
                "word_count": True,
                "reading_time": self.enable_reading_time
            },
            "social_sharing": {
                "platforms": ["twitter", "facebook", "linkedin", "reddit"],
                "show_counts": False,
                "custom_text": True
            }
        }


# Пример использования
def get_blog_uiux_dependencies() -> BlogUIUXDependencies:
    """Создать конфигурацию для Blog/CMS проекта."""
    return BlogUIUXDependencies(
        api_key="your-api-key",
        domain_type="blog",
        project_type="content_management",
        enable_comments=True,
        enable_categories=True,
        enable_tags=True,
        enable_reading_progress=True,
        article_layout="centered"
    )


# Пример использования в React компоненте
BLOG_COMPONENT_EXAMPLES = {
    "article_reader": """
// Blog Article Reader Component
export function BlogArticleReader({
  article,
  config
}: {
  article: BlogArticle;
  config: BlogUIUXDependencies;
}) {
  const colorScheme = config.get_color_scheme();
  const articleConfig = config.get_component_config().article;
  const typographyConfig = config.get_typography_config();

  const [readingProgress, setReadingProgress] = useState(0);
  const [fontSize, setFontSize] = useState(18);

  useEffect(() => {
    const handleScroll = () => {
      const article = document.getElementById('article-content');
      if (!article) return;

      const scrollTop = window.scrollY;
      const scrollHeight = article.scrollHeight - window.innerHeight;
      const progress = Math.min((scrollTop / scrollHeight) * 100, 100);
      setReadingProgress(progress);
    };

    if (articleConfig.show_progress) {
      window.addEventListener('scroll', handleScroll);
      return () => window.removeEventListener('scroll', handleScroll);
    }
  }, [articleConfig.show_progress]);

  return (
    <article className="max-w-4xl mx-auto">
      {/* Reading Progress */}
      {articleConfig.show_progress && (
        <div className="fixed top-0 left-0 w-full h-1 bg-gray-200 z-50">
          <div
            className="h-full transition-all duration-100"
            style={{
              width: `${readingProgress}%`,
              backgroundColor: colorScheme.primary
            }}
          />
        </div>
      )}

      {/* Article Header */}
      <header className="mb-8">
        {article.featuredImage && config.enable_featured_image && (
          <div className="aspect-video mb-6 rounded-lg overflow-hidden">
            <img
              src={article.featuredImage}
              alt={article.title}
              className="w-full h-full object-cover"
            />
          </div>
        )}

        <div className="space-y-4">
          {config.enable_categories && article.category && (
            <Badge
              variant="secondary"
              style={{ backgroundColor: colorScheme[`category_${article.category.toLowerCase()}`] }}
            >
              {article.category}
            </Badge>
          )}

          <h1
            className="text-4xl font-bold leading-tight"
            style={{
              fontFamily: typographyConfig.headings.font_family,
              color: colorScheme.text_primary
            }}
          >
            {article.title}
          </h1>

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            {config.enable_author_profiles && (
              <div className="flex items-center gap-2">
                <Avatar className="w-8 h-8">
                  <AvatarImage src={article.author.avatar} />
                  <AvatarFallback>{article.author.name[0]}</AvatarFallback>
                </Avatar>
                <span>{article.author.name}</span>
              </div>
            )}

            <time dateTime={article.publishedAt.toISOString()}>
              {article.publishedAt.toLocaleDateString()}
            </time>

            {articleConfig.show_reading_time && (
              <span>{article.readingTime} min read</span>
            )}
          </div>
        </div>
      </header>

      {/* Reading Controls */}
      {config.enable_font_size_adjustment && (
        <div className="fixed right-4 top-1/2 transform -translate-y-1/2 bg-white rounded-lg shadow-lg p-2 space-y-2">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setFontSize(prev => Math.min(prev + 2, 24))}
          >
            A+
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setFontSize(prev => Math.max(prev - 2, 14))}
          >
            A-
          </Button>
        </div>
      )}

      {/* Table of Contents */}
      {articleConfig.show_toc && article.tableOfContents && (
        <div className="mb-8 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-3">Table of Contents</h3>
          <nav className="space-y-1">
            {article.tableOfContents.map((item, index) => (
              <a
                key={index}
                href={`#${item.slug}`}
                className="block text-sm hover:text-primary transition-colors"
                style={{ paddingLeft: `${(item.level - 1) * 1}rem` }}
              >
                {item.title}
              </a>
            ))}
          </nav>
        </div>
      )}

      {/* Article Content */}
      <div
        id="article-content"
        className="prose prose-lg max-w-none"
        style={{
          fontSize: `${fontSize}px`,
          lineHeight: typographyConfig.body.line_height,
          fontFamily: typographyConfig.body.font_family,
          color: colorScheme.text_primary
        }}
        dangerouslySetInnerHTML={{ __html: article.content }}
      />

      {/* Tags */}
      {config.enable_tags && article.tags && article.tags.length > 0 && (
        <div className="mt-8 pt-8 border-t">
          <h3 className="text-sm font-medium mb-3">Tags:</h3>
          <div className="flex flex-wrap gap-2">
            {article.tags.map(tag => (
              <Badge key={tag} variant="outline">
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Social Sharing */}
      {config.enable_social_sharing && (
        <div className="mt-8 pt-8 border-t">
          <h3 className="text-sm font-medium mb-3">Share this article:</h3>
          <div className="flex gap-2">
            <Button size="sm" variant="outline">
              <Twitter className="w-4 h-4 mr-2" />
              Twitter
            </Button>
            <Button size="sm" variant="outline">
              <Facebook className="w-4 h-4 mr-2" />
              Facebook
            </Button>
            <Button size="sm" variant="outline">
              <Linkedin className="w-4 h-4 mr-2" />
              LinkedIn
            </Button>
          </div>
        </div>
      )}
    </article>
  );
}
""",

    "post_card": """
// Blog Post Card Component
export function BlogPostCard({
  post,
  config
}: {
  post: BlogPost;
  config: BlogUIUXDependencies;
}) {
  const colorScheme = config.get_color_scheme();
  const postCardConfig = config.get_component_config().post_card;

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-all duration-300 group">
      {post.featuredImage && (
        <div className="aspect-video overflow-hidden">
          <img
            src={post.featuredImage}
            alt={post.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
      )}

      <CardContent className="p-6">
        <div className="space-y-3">
          {/* Category & Reading Time */}
          <div className="flex items-center justify-between">
            {postCardConfig.show_category && post.category && (
              <Badge
                variant="secondary"
                style={{ backgroundColor: colorScheme[`category_${post.category.toLowerCase()}`] }}
              >
                {post.category}
              </Badge>
            )}
            {postCardConfig.show_reading_time && (
              <span className="text-xs text-muted-foreground">
                {post.readingTime} min read
              </span>
            )}
          </div>

          {/* Title */}
          <h3 className="text-xl font-semibold line-clamp-2 group-hover:text-primary transition-colors">
            {post.title}
          </h3>

          {/* Excerpt */}
          {postCardConfig.show_excerpt && post.excerpt && (
            <p className="text-muted-foreground line-clamp-3">
              {post.excerpt}
            </p>
          )}

          {/* Author & Date */}
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            {postCardConfig.show_author && (
              <div className="flex items-center gap-2">
                <Avatar className="w-6 h-6">
                  <AvatarImage src={post.author.avatar} />
                  <AvatarFallback>{post.author.name[0]}</AvatarFallback>
                </Avatar>
                <span>{post.author.name}</span>
              </div>
            )}
            {postCardConfig.show_date && (
              <time dateTime={post.publishedAt.toISOString()}>
                {post.publishedAt.toLocaleDateString()}
              </time>
            )}
          </div>

          {/* Tags */}
          {postCardConfig.show_tags && post.tags && post.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {post.tags.slice(0, 3).map(tag => (
                <Badge key={tag} variant="outline" className="text-xs">
                  {tag}
                </Badge>
              ))}
              {post.tags.length > 3 && (
                <span className="text-xs text-muted-foreground">
                  +{post.tags.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="p-6 pt-0">
        <Button
          variant="ghost"
          className="w-full justify-start p-0 h-auto text-primary hover:text-primary/80"
          asChild
        >
          <a href={`/posts/${post.slug}`}>
            Read more <ArrowRight className="w-4 h-4 ml-2" />
          </a>
        </Button>
      </CardFooter>
    </Card>
  );
}
"""
}