"""
Social Media UI/UX конфигурация для UI/UX Enhancement Agent.

Этот файл демонстрирует настройку агента для социальных платформ.
Включает специфичные UI компоненты для постов, профилей, уведомлений и социальных взаимодействий.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from ..dependencies import UIUXEnhancementDependencies


@dataclass
class SocialUIUXDependencies(UIUXEnhancementDependencies):
    """Конфигурация для Social Media проектов."""

    # Основные настройки
    domain_type: str = "social"
    project_type: str = "social_network"

    # Social специфичные настройки
    enable_posts: bool = True
    enable_stories: bool = True
    enable_direct_messages: bool = True
    enable_live_chat: bool = True
    enable_video_calls: bool = False

    # Interaction настройки
    enable_likes: bool = True
    enable_comments: bool = True
    enable_shares: bool = True
    enable_reactions: bool = True
    enable_bookmarks: bool = True

    # Feed настройки
    feed_algorithm: str = "chronological"  # chronological, algorithmic, mixed
    enable_infinite_scroll: bool = True
    enable_pull_to_refresh: bool = True
    posts_per_page: int = 10

    # Privacy настройки
    enable_privacy_controls: bool = True
    enable_content_warnings: bool = True
    enable_blocking: bool = True
    enable_reporting: bool = True

    # Real-time настройки
    enable_live_notifications: bool = True
    enable_typing_indicators: bool = True
    enable_read_receipts: bool = True
    enable_online_status: bool = True

    def get_color_scheme(self) -> Dict[str, Any]:
        """Цветовая схема для Social Media."""
        return {
            "primary": "hsl(221, 83%, 53%)",   # Social blue
            "secondary": "hsl(210, 11%, 15%)", # Dark gray
            "success": "hsl(142, 76%, 36%)",   # Success green
            "warning": "hsl(38, 92%, 50%)",    # Warning amber
            "destructive": "hsl(0, 84%, 60%)", # Error red
            "accent": "hsl(262, 83%, 58%)",    # Accent purple

            # Social specific colors
            "like": "hsl(0, 84%, 60%)",        # Heart red
            "comment": "hsl(210, 11%, 71%)",   # Comment gray
            "share": "hsl(142, 76%, 36%)",     # Share green
            "message": "hsl(221, 83%, 53%)",   # Message blue
            "notification": "hsl(38, 92%, 50%)", # Notification amber

            # Status colors
            "online": "hsl(142, 76%, 36%)",    # Online green
            "away": "hsl(38, 92%, 50%)",       # Away yellow
            "busy": "hsl(0, 84%, 60%)",        # Busy red
            "offline": "hsl(210, 11%, 71%)",   # Offline gray

            # Content types
            "text_post": "hsl(210, 11%, 15%)",
            "image_post": "hsl(262, 83%, 58%)",
            "video_post": "hsl(0, 84%, 60%)",
            "story": "hsl(291, 64%, 42%)",

            # Reaction colors
            "reaction_love": "hsl(0, 84%, 60%)",
            "reaction_like": "hsl(221, 83%, 53%)",
            "reaction_laugh": "hsl(45, 93%, 58%)",
            "reaction_wow": "hsl(38, 92%, 50%)",
            "reaction_sad": "hsl(210, 11%, 71%)",
            "reaction_angry": "hsl(14, 100%, 57%)",
        }

    def get_component_config(self) -> Dict[str, Any]:
        """Конфигурация компонентов для Social Media."""
        return {
            "post": {
                "max_length": 280,
                "media_upload": True,
                "polls": True,
                "location_tagging": True,
                "user_tagging": True,
                "hashtags": True,
                "auto_link": True
            },
            "feed": {
                "algorithm": self.feed_algorithm,
                "infinite_scroll": self.enable_infinite_scroll,
                "pull_to_refresh": self.enable_pull_to_refresh,
                "posts_per_load": self.posts_per_page,
                "skeleton_loading": True
            },
            "interactions": {
                "like": self.enable_likes,
                "comment": self.enable_comments,
                "share": self.enable_shares,
                "reactions": self.enable_reactions,
                "bookmark": self.enable_bookmarks,
                "double_tap_like": True
            },
            "stories": {
                "enabled": self.enable_stories,
                "duration": 15,  # seconds
                "auto_advance": True,
                "close_friends": True,
                "highlights": True
            },
            "messaging": {
                "enabled": self.enable_direct_messages,
                "typing_indicators": self.enable_typing_indicators,
                "read_receipts": self.enable_read_receipts,
                "voice_messages": True,
                "file_sharing": True,
                "emoji_reactions": True
            },
            "notifications": {
                "real_time": self.enable_live_notifications,
                "push_notifications": True,
                "email_notifications": False,
                "grouping": True,
                "mark_as_read": True
            }
        }

    def get_layout_config(self) -> Dict[str, Any]:
        """Конфигурация layout для Social Media."""
        return {
            "navigation": {
                "type": "bottom_tabs",  # top_nav, bottom_tabs, sidebar
                "items": ["home", "search", "create", "activity", "profile"],
                "floating_action": True
            },
            "spacing": {
                "post_gap": "1rem",
                "section_gap": "2rem",
                "component_gap": "0.75rem",
                "element_gap": "0.5rem"
            },
            "containers": {
                "header": "full",
                "main": "narrow",  # optimized for mobile
                "sidebar": "none"
            },
            "responsive": {
                "mobile_first": True,
                "breakpoints": {
                    "mobile": "0px",
                    "tablet": "768px",
                    "desktop": "1024px"
                }
            }
        }

    def get_animation_config(self) -> Dict[str, Any]:
        """Конфигурация анимаций для Social Media."""
        return {
            "micro_interactions": {
                "like_animation": "heart_burst",
                "comment_expand": "slide_down",
                "share_feedback": "bounce",
                "pull_to_refresh": "elastic"
            },
            "page_transitions": {
                "type": "slide",
                "duration": "300ms",
                "easing": "cubic-bezier(0.4, 0, 0.2, 1)"
            },
            "story_transitions": {
                "type": "fade",
                "duration": "200ms",
                "auto_advance": True
            },
            "notification_animations": {
                "new_notification": "slide_in",
                "badge_update": "scale_bounce",
                "toast": "slide_up"
            },
            "loading_states": {
                "skeleton": True,
                "shimmer": True,
                "progressive": True
            }
        }

    def get_accessibility_config(self) -> Dict[str, Any]:
        """Конфигурация accessibility для Social Media."""
        return {
            "high_contrast_mode": True,
            "keyboard_navigation": True,
            "screen_reader_optimized": True,
            "focus_indicators": True,
            "reduced_motion": True,
            "content_warnings": self.enable_content_warnings,
            "aria_labels": {
                "post": "Post by {author}: {content}",
                "like_button": "Like post by {author}",
                "comment_button": "Comment on post by {author}",
                "share_button": "Share post by {author}",
                "story": "Story by {author}",
                "notification": "Notification: {type} from {user}"
            },
            "skip_links": [
                {"href": "#main", "label": "Skip to main content"},
                {"href": "#navigation", "label": "Skip to navigation"},
                {"href": "#create-post", "label": "Skip to create post"}
            ],
            "alternative_text": {
                "image_posts": True,
                "video_captions": True,
                "emoji_descriptions": True
            }
        }

    def get_privacy_config(self) -> Dict[str, Any]:
        """Конфигурация privacy для Social Media."""
        return {
            "privacy_controls": self.enable_privacy_controls,
            "content_warnings": self.enable_content_warnings,
            "blocking": self.enable_blocking,
            "reporting": self.enable_reporting,
            "data_control": {
                "download_data": True,
                "delete_account": True,
                "privacy_settings": True,
                "data_visibility": True
            },
            "safety_features": {
                "content_filtering": True,
                "sensitive_content_warning": True,
                "harassment_detection": True,
                "spam_detection": True
            }
        }

    def get_engagement_config(self) -> Dict[str, Any]:
        """Конфигурация engagement для Social Media."""
        return {
            "gamification": {
                "streak_counters": True,
                "achievement_badges": True,
                "level_system": False,
                "leaderboards": False
            },
            "social_proof": {
                "like_counts": True,
                "follower_counts": True,
                "verification_badges": True,
                "trending_indicators": True
            },
            "discovery": {
                "hashtag_trending": True,
                "suggested_users": True,
                "explore_page": True,
                "location_based": True
            }
        }


# Пример использования
def get_social_uiux_dependencies() -> SocialUIUXDependencies:
    """Создать конфигурацию для Social Media проекта."""
    return SocialUIUXDependencies(
        api_key="your-api-key",
        domain_type="social",
        project_type="social_network",
        enable_posts=True,
        enable_stories=True,
        enable_direct_messages=True,
        enable_reactions=True,
        feed_algorithm="chronological"
    )


# Пример использования в React компоненте
SOCIAL_COMPONENT_EXAMPLES = {
    "social_post": """
// Social Media Post Component
export function SocialPost({
  post,
  config,
  onLike,
  onComment,
  onShare
}: {
  post: SocialPost;
  config: SocialUIUXDependencies;
  onLike: (postId: string) => void;
  onComment: (postId: string) => void;
  onShare: (postId: string) => void;
}) {
  const colorScheme = config.get_color_scheme();
  const interactionConfig = config.get_component_config().interactions;
  const [isLiked, setIsLiked] = useState(post.isLiked);
  const [likeCount, setLikeCount] = useState(post.likeCount);

  const handleLike = () => {
    setIsLiked(!isLiked);
    setLikeCount(prev => isLiked ? prev - 1 : prev + 1);
    onLike(post.id);
  };

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return 'now';
    if (minutes < 60) return `${minutes}m`;
    if (minutes < 1440) return `${Math.floor(minutes / 60)}h`;
    return `${Math.floor(minutes / 1440)}d`;
  };

  return (
    <Card className="w-full max-w-lg mx-auto">
      {/* Post Header */}
      <CardHeader className="flex flex-row items-center space-y-0 space-x-4 pb-2">
        <Avatar className="h-10 w-10">
          <AvatarImage src={post.author.avatar} alt={post.author.name} />
          <AvatarFallback>{post.author.name[0]}</AvatarFallback>
        </Avatar>

        <div className="flex-1">
          <div className="flex items-center gap-2">
            <p className="font-semibold text-sm">{post.author.name}</p>
            {post.author.verified && (
              <Badge variant="secondary" className="h-4 w-4 p-0">
                <Check className="h-3 w-3" />
              </Badge>
            )}
          </div>
          <p className="text-xs text-muted-foreground">
            @{post.author.username} · {formatTimeAgo(post.createdAt)}
          </p>
        </div>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="h-8 w-8">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {config.enable_bookmarks && (
              <DropdownMenuItem>
                <Bookmark className="h-4 w-4 mr-2" />
                Save post
              </DropdownMenuItem>
            )}
            <DropdownMenuItem>
              <Link className="h-4 w-4 mr-2" />
              Copy link
            </DropdownMenuItem>
            {config.enable_reporting && (
              <DropdownMenuItem className="text-destructive">
                <Flag className="h-4 w-4 mr-2" />
                Report
              </DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Post Content */}
        <p className="text-sm mb-3 whitespace-pre-wrap">{post.content}</p>

        {/* Media */}
        {post.media && post.media.length > 0 && (
          <div className="mb-3 rounded-lg overflow-hidden">
            {post.media[0].type === 'image' && (
              <img
                src={post.media[0].url}
                alt="Post media"
                className="w-full h-auto"
              />
            )}
            {post.media[0].type === 'video' && (
              <video
                src={post.media[0].url}
                controls
                className="w-full h-auto"
              />
            )}
          </div>
        )}

        {/* Engagement Stats */}
        <div className="flex items-center justify-between py-2 border-t border-b text-xs text-muted-foreground">
          <div className="flex items-center gap-4">
            {interactionConfig.like && (
              <span>{likeCount} likes</span>
            )}
            {interactionConfig.comment && (
              <span>{post.commentCount} comments</span>
            )}
            {interactionConfig.share && (
              <span>{post.shareCount} shares</span>
            )}
          </div>
          <span>{post.viewCount} views</span>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between pt-2">
          {interactionConfig.like && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLike}
              className={cn(
                "flex-1",
                isLiked && "text-red-500"
              )}
            >
              <Heart
                className={cn(
                  "h-4 w-4 mr-2 transition-all",
                  isLiked && "fill-current scale-110"
                )}
              />
              Like
            </Button>
          )}

          {interactionConfig.comment && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onComment(post.id)}
              className="flex-1"
            >
              <MessageCircle className="h-4 w-4 mr-2" />
              Comment
            </Button>
          )}

          {interactionConfig.share && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onShare(post.id)}
              className="flex-1"
            >
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
          )}

          {interactionConfig.reactions && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm">
                  <Smile className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <div className="flex gap-1 p-2">
                  {['❤️', '👍', '😂', '😮', '😢', '😠'].map((emoji, index) => (
                    <Button
                      key={index}
                      variant="ghost"
                      size="sm"
                      className="p-1 h-8 w-8"
                    >
                      {emoji}
                    </Button>
                  ))}
                </div>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
""",

    "story_viewer": """
// Social Media Story Viewer Component
export function SocialStoryViewer({
  stories,
  config,
  onClose
}: {
  stories: Story[];
  config: SocialUIUXDependencies;
  onClose: () => void;
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const colorScheme = config.get_color_scheme();
  const storyConfig = config.get_component_config().stories;

  useEffect(() => {
    if (!storyConfig.enabled) return;

    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          // Auto advance to next story
          if (currentIndex < stories.length - 1) {
            setCurrentIndex(prev => prev + 1);
            return 0;
          } else {
            onClose();
            return 100;
          }
        }
        return prev + (100 / (storyConfig.duration * 10)); // 100ms intervals
      });
    }, 100);

    return () => clearInterval(timer);
  }, [currentIndex, stories.length, storyConfig, onClose]);

  const currentStory = stories[currentIndex];

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      setProgress(0);
    }
  };

  const handleNext = () => {
    if (currentIndex < stories.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setProgress(0);
    } else {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
      {/* Progress Bars */}
      <div className="absolute top-4 left-4 right-4 flex gap-1">
        {stories.map((_, index) => (
          <div
            key={index}
            className="flex-1 h-1 bg-white/30 rounded-full overflow-hidden"
          >
            <div
              className="h-full bg-white transition-all duration-100"
              style={{
                width: index < currentIndex ? '100%' :
                       index === currentIndex ? `${progress}%` : '0%'
              }}
            />
          </div>
        ))}
      </div>

      {/* Story Header */}
      <div className="absolute top-8 left-4 right-4 flex items-center justify-between text-white z-10">
        <div className="flex items-center gap-3">
          <Avatar className="h-8 w-8 border-2 border-white">
            <AvatarImage src={currentStory.author.avatar} />
            <AvatarFallback>{currentStory.author.name[0]}</AvatarFallback>
          </Avatar>
          <div>
            <p className="font-semibold text-sm">{currentStory.author.name}</p>
            <p className="text-xs opacity-75">
              {formatTimeAgo(currentStory.createdAt)}
            </p>
          </div>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="text-white hover:bg-white/20"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>

      {/* Story Content */}
      <div className="relative w-full h-full max-w-sm max-h-[80vh] mx-auto">
        {/* Click Areas for Navigation */}
        <div className="absolute inset-0 flex">
          <div className="flex-1" onClick={handlePrevious} />
          <div className="flex-1" onClick={handleNext} />
        </div>

        {/* Story Media */}
        {currentStory.type === 'image' && (
          <img
            src={currentStory.media}
            alt="Story"
            className="w-full h-full object-cover rounded-lg"
          />
        )}

        {currentStory.type === 'video' && (
          <video
            src={currentStory.media}
            autoPlay
            muted
            className="w-full h-full object-cover rounded-lg"
          />
        )}

        {/* Story Text Overlay */}
        {currentStory.text && (
          <div className="absolute inset-0 flex items-center justify-center p-4">
            <p
              className="text-white text-center text-lg font-semibold drop-shadow-lg"
              style={{ textShadow: '0 0 10px rgba(0,0,0,0.8)' }}
            >
              {currentStory.text}
            </p>
          </div>
        )}
      </div>

      {/* Story Actions */}
      <div className="absolute bottom-8 left-4 right-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            className="text-white hover:bg-white/20"
          >
            <Heart className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-white hover:bg-white/20"
          >
            <MessageCircle className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-white hover:bg-white/20"
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>

        <Button
          variant="ghost"
          size="icon"
          className="text-white hover:bg-white/20"
        >
          <Bookmark className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}
"""
}