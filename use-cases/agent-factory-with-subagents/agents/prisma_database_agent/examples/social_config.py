"""
Social Media Platform конфигурация для Prisma Database Agent.

Этот файл демонстрирует настройку агента для социальных платформ.
Включает схемы для постов, подписок, лайков, сообщений и активности.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from ..dependencies import PrismaDatabaseDependencies


@dataclass
class SocialPrismaDependencies(PrismaDatabaseDependencies):
    """Конфигурация для Social Media проектов."""

    # Основные настройки
    domain_type: str = "social"
    project_type: str = "social-media"

    # Social-специфичные настройки
    enable_direct_messages: bool = True
    enable_stories: bool = True
    enable_live_streaming: bool = False
    enable_groups: bool = True
    enable_hashtags: bool = True

    # Настройки приватности
    default_profile_visibility: str = "public"  # public, private, friends
    enable_content_moderation: bool = True
    enable_reporting: bool = True

    # Настройки уведомлений
    enable_push_notifications: bool = True
    enable_email_notifications: bool = True
    enable_real_time_updates: bool = True

    # Limits для предотвращения спама
    max_posts_per_hour: int = 50
    max_follows_per_day: int = 100
    max_dm_recipients: int = 10

    def get_schema_config(self) -> Dict[str, Any]:
        """Конфигурация схемы для Social Media."""
        return {
            "models": [
                {
                    "name": "User",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "email: String @unique",
                        "username: String @unique",
                        "displayName: String",
                        "bio: String? @db.Text",
                        "avatar: String?",
                        "coverImage: String?",
                        "location: String?",
                        "website: String?",
                        "birthDate: DateTime?",
                        "",
                        "// Privacy & Security",
                        "isPrivate: Boolean @default(false)",
                        "isVerified: Boolean @default(false)",
                        "isSuspended: Boolean @default(false)",
                        "lastActiveAt: DateTime @default(now())",
                        "",
                        "// Statistics",
                        "followerCount: Int @default(0)",
                        "followingCount: Int @default(0)",
                        "postCount: Int @default(0)",
                        "",
                        "// Relations",
                        "posts: Post[]",
                        "comments: Comment[]",
                        "likes: Like[]",
                        "followers: Follow[] @relation(\"UserFollowers\")",
                        "following: Follow[] @relation(\"UserFollowing\")",
                        "sentMessages: DirectMessage[] @relation(\"MessageSender\")",
                        "receivedMessages: DirectMessage[] @relation(\"MessageReceiver\")",
                        "stories: Story[]",
                        "notifications: Notification[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([username])",
                        "@@index([email])",
                        "@@index([isPrivate, isSuspended])",
                        "@@index([lastActiveAt])",
                        "@@map(\"users\")"
                    ]
                },
                {
                    "name": "Post",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "content: String @db.Text",
                        "mediaUrls: String[] // Array of image/video URLs",
                        "type: PostType @default(TEXT)",
                        "visibility: PostVisibility @default(PUBLIC)",
                        "",
                        "// Engagement",
                        "likeCount: Int @default(0)",
                        "commentCount: Int @default(0)",
                        "shareCount: Int @default(0)",
                        "viewCount: Int @default(0)",
                        "",
                        "// Location & Context",
                        "location: String?",
                        "taggedUsers: String[] // User IDs",
                        "",
                        "// Relations",
                        "authorId: String",
                        "author: User @relation(fields: [authorId], references: [id], onDelete: Cascade)",
                        "comments: Comment[]",
                        "likes: Like[]",
                        "hashtags: HashtagOnPost[]",
                        "",
                        "// Repost functionality",
                        "originalPostId: String?",
                        "originalPost: Post? @relation(\"PostRepost\", fields: [originalPostId], references: [id])",
                        "reposts: Post[] @relation(\"PostRepost\")",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([authorId, createdAt])",
                        "@@index([visibility, createdAt])",
                        "@@index([type, createdAt])",
                        "@@index([originalPostId])",
                        "@@map(\"posts\")"
                    ]
                },
                {
                    "name": "Comment",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "content: String @db.Text",
                        "likeCount: Int @default(0)",
                        "",
                        "// Threading support",
                        "parentId: String?",
                        "parent: Comment? @relation(\"CommentThread\", fields: [parentId], references: [id])",
                        "replies: Comment[] @relation(\"CommentThread\")",
                        "",
                        "// Relations",
                        "postId: String",
                        "post: Post @relation(fields: [postId], references: [id], onDelete: Cascade)",
                        "authorId: String",
                        "author: User @relation(fields: [authorId], references: [id], onDelete: Cascade)",
                        "likes: Like[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([postId, createdAt])",
                        "@@index([authorId])",
                        "@@index([parentId])",
                        "@@map(\"comments\")"
                    ]
                },
                {
                    "name": "Like",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "type: LikeType @default(LIKE)",
                        "",
                        "// Relations",
                        "userId: String",
                        "user: User @relation(fields: [userId], references: [id], onDelete: Cascade)",
                        "",
                        "// Polymorphic target (post or comment)",
                        "postId: String?",
                        "post: Post? @relation(fields: [postId], references: [id], onDelete: Cascade)",
                        "commentId: String?",
                        "comment: Comment? @relation(fields: [commentId], references: [id], onDelete: Cascade)",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "",
                        "@@unique([userId, postId])",
                        "@@unique([userId, commentId])",
                        "@@index([postId, type])",
                        "@@index([commentId, type])",
                        "@@map(\"likes\")"
                    ]
                },
                {
                    "name": "Follow",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "",
                        "// Relations",
                        "followerId: String",
                        "follower: User @relation(\"UserFollowing\", fields: [followerId], references: [id], onDelete: Cascade)",
                        "followingId: String",
                        "following: User @relation(\"UserFollowers\", fields: [followingId], references: [id], onDelete: Cascade)",
                        "",
                        "// Status",
                        "status: FollowStatus @default(PENDING)",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "",
                        "@@unique([followerId, followingId])",
                        "@@index([followerId, status])",
                        "@@index([followingId, status])",
                        "@@map(\"follows\")"
                    ]
                },
                {
                    "name": "DirectMessage",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "content: String @db.Text",
                        "mediaUrls: String[]",
                        "isRead: Boolean @default(false)",
                        "",
                        "// Relations",
                        "senderId: String",
                        "sender: User @relation(\"MessageSender\", fields: [senderId], references: [id], onDelete: Cascade)",
                        "receiverId: String",
                        "receiver: User @relation(\"MessageReceiver\", fields: [receiverId], references: [id], onDelete: Cascade)",
                        "",
                        "// Group messaging",
                        "conversationId: String",
                        "conversation: Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([conversationId, createdAt])",
                        "@@index([senderId])",
                        "@@index([receiverId, isRead])",
                        "@@map(\"direct_messages\")"
                    ]
                },
                {
                    "name": "Conversation",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "isGroup: Boolean @default(false)",
                        "name: String?",
                        "description: String?",
                        "avatar: String?",
                        "",
                        "// Relations",
                        "participants: String[] // User IDs",
                        "messages: DirectMessage[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([isGroup])",
                        "@@map(\"conversations\")"
                    ]
                },
                {
                    "name": "Story",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "mediaUrl: String",
                        "type: StoryType @default(IMAGE)",
                        "viewCount: Int @default(0)",
                        "expiresAt: DateTime",
                        "",
                        "// Relations",
                        "authorId: String",
                        "author: User @relation(fields: [authorId], references: [id], onDelete: Cascade)",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "",
                        "@@index([authorId, expiresAt])",
                        "@@index([expiresAt])",
                        "@@map(\"stories\")"
                    ]
                },
                {
                    "name": "Hashtag",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "name: String @unique",
                        "description: String?",
                        "postCount: Int @default(0)",
                        "trending: Boolean @default(false)",
                        "",
                        "// Relations",
                        "posts: HashtagOnPost[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([name])",
                        "@@index([trending, postCount])",
                        "@@map(\"hashtags\")"
                    ]
                },
                {
                    "name": "HashtagOnPost",
                    "fields": [
                        "postId: String",
                        "hashtagId: String",
                        "",
                        "post: Post @relation(fields: [postId], references: [id], onDelete: Cascade)",
                        "hashtag: Hashtag @relation(fields: [hashtagId], references: [id], onDelete: Cascade)",
                        "",
                        "createdAt: DateTime @default(now())",
                        "",
                        "@@id([postId, hashtagId])",
                        "@@map(\"post_hashtags\")"
                    ]
                },
                {
                    "name": "Notification",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "type: NotificationType",
                        "title: String",
                        "content: String",
                        "isRead: Boolean @default(false)",
                        "data: Json? // Additional data for different notification types",
                        "",
                        "// Relations",
                        "userId: String",
                        "user: User @relation(fields: [userId], references: [id], onDelete: Cascade)",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "",
                        "@@index([userId, isRead])",
                        "@@index([type, createdAt])",
                        "@@map(\"notifications\")"
                    ]
                }
            ],
            "enums": [
                {
                    "name": "PostType",
                    "values": ["TEXT", "IMAGE", "VIDEO", "LINK", "POLL"]
                },
                {
                    "name": "PostVisibility",
                    "values": ["PUBLIC", "PRIVATE", "FRIENDS", "FOLLOWERS"]
                },
                {
                    "name": "LikeType",
                    "values": ["LIKE", "LOVE", "LAUGH", "ANGRY", "SAD"]
                },
                {
                    "name": "FollowStatus",
                    "values": ["PENDING", "ACCEPTED", "BLOCKED"]
                },
                {
                    "name": "StoryType",
                    "values": ["IMAGE", "VIDEO"]
                },
                {
                    "name": "NotificationType",
                    "values": ["LIKE", "COMMENT", "FOLLOW", "MESSAGE", "MENTION", "SHARE", "STORY_VIEW"]
                }
            ]
        }

    def get_optimization_config(self) -> Dict[str, Any]:
        """Оптимизации для Social Media платформ."""
        return {
            "indexes": [
                # Real-time feed indexes
                "CREATE INDEX CONCURRENTLY idx_posts_feed ON posts (author_id, visibility, created_at DESC) WHERE visibility IN ('PUBLIC', 'FOLLOWERS');",
                "CREATE INDEX CONCURRENTLY idx_posts_trending ON posts (like_count DESC, comment_count DESC, created_at DESC) WHERE created_at > NOW() - INTERVAL '24 hours';",

                # Social graph indexes
                "CREATE INDEX CONCURRENTLY idx_follows_active ON follows (follower_id, status, created_at) WHERE status = 'ACCEPTED';",
                "CREATE INDEX CONCURRENTLY idx_follows_suggestions ON follows (following_id, status) WHERE status = 'ACCEPTED';",

                # Messaging indexes
                "CREATE INDEX CONCURRENTLY idx_messages_conversation ON direct_messages (conversation_id, created_at DESC);",
                "CREATE INDEX CONCURRENTLY idx_messages_unread ON direct_messages (receiver_id, is_read) WHERE is_read = false;",

                # Activity indexes
                "CREATE INDEX CONCURRENTLY idx_likes_activity ON likes (user_id, created_at DESC);",
                "CREATE INDEX CONCURRENTLY idx_notifications_unread ON notifications (user_id, is_read, created_at DESC) WHERE is_read = false;",

                # Search indexes
                "CREATE INDEX CONCURRENTLY idx_users_search ON users USING gin(to_tsvector('english', username || ' ' || display_name || ' ' || bio));",
                "CREATE INDEX CONCURRENTLY idx_posts_search ON posts USING gin(to_tsvector('english', content));",
                "CREATE INDEX CONCURRENTLY idx_hashtags_search ON hashtags (name text_pattern_ops);"
            ],
            "partitioning": [
                # Партиционирование для больших таблиц
                """
                -- Партиционирование уведомлений по месяцам
                CREATE TABLE notifications_y2024m01 PARTITION OF notifications
                FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

                -- Партиционирование сообщений по кварталам
                CREATE TABLE direct_messages_y2024q1 PARTITION OF direct_messages
                FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
                """
            ],
            "triggers": [
                # Auto-update follower counts
                """
                CREATE OR REPLACE FUNCTION update_follower_counts()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' AND NEW.status = 'ACCEPTED' THEN
                        UPDATE users SET follower_count = follower_count + 1 WHERE id = NEW.following_id;
                        UPDATE users SET following_count = following_count + 1 WHERE id = NEW.follower_id;
                        RETURN NEW;
                    ELSIF TG_OP = 'UPDATE' AND OLD.status != 'ACCEPTED' AND NEW.status = 'ACCEPTED' THEN
                        UPDATE users SET follower_count = follower_count + 1 WHERE id = NEW.following_id;
                        UPDATE users SET following_count = following_count + 1 WHERE id = NEW.follower_id;
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' AND OLD.status = 'ACCEPTED' THEN
                        UPDATE users SET follower_count = follower_count - 1 WHERE id = OLD.following_id;
                        UPDATE users SET following_count = following_count - 1 WHERE id = OLD.follower_id;
                        RETURN OLD;
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_follower_counts
                AFTER INSERT OR UPDATE OR DELETE ON follows
                FOR EACH ROW EXECUTE FUNCTION update_follower_counts();
                """,

                # Auto-update post engagement counts
                """
                CREATE OR REPLACE FUNCTION update_post_engagement()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        IF NEW.post_id IS NOT NULL THEN
                            UPDATE posts SET like_count = like_count + 1 WHERE id = NEW.post_id;
                        END IF;
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' THEN
                        IF OLD.post_id IS NOT NULL THEN
                            UPDATE posts SET like_count = like_count - 1 WHERE id = OLD.post_id;
                        END IF;
                        RETURN OLD;
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_post_engagement
                AFTER INSERT OR DELETE ON likes
                FOR EACH ROW EXECUTE FUNCTION update_post_engagement();
                """
            ]
        }


# Пример использования
def get_social_dependencies() -> SocialPrismaDependencies:
    """Создать конфигурацию для Social Media проекта."""
    return SocialPrismaDependencies(
        database_url="postgresql://user:password@localhost:5432/social_db",
        domain_type="social",
        project_type="social-media",
        enable_direct_messages=True,
        enable_stories=True,
        enable_groups=True,
        enable_hashtags=True,
        enable_content_moderation=True,
        max_posts_per_hour=50,
        max_follows_per_day=100
    )