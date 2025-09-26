"""
Blog/CMS конфигурация для Prisma Database Agent.

Этот файл демонстрирует настройку агента для блогов и CMS систем.
Включает схемы для постов, комментариев, категорий и пользователей.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from ..dependencies import PrismaDatabaseDependencies


@dataclass
class BlogPrismaDependencies(PrismaDatabaseDependencies):
    """Конфигурация для Blog/CMS проектов."""

    # Основные настройки
    domain_type: str = "blog"
    project_type: str = "cms"

    # Blog-специфичные настройки
    enable_comments: bool = True
    enable_categories: bool = True
    enable_tags: bool = True
    enable_seo_features: bool = True
    enable_multilanguage: bool = False

    # Настройки контента
    max_post_length: int = 50000
    enable_draft_mode: bool = True
    enable_scheduling: bool = True

    # Настройки модерации
    comment_moderation: bool = True
    auto_approve_comments: bool = False

    def get_schema_config(self) -> Dict[str, Any]:
        """Конфигурация схемы для Blog/CMS."""
        return {
            "models": [
                {
                    "name": "User",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "email: String @unique",
                        "username: String @unique",
                        "name: String?",
                        "bio: String? @db.Text",
                        "avatar: String?",
                        "role: UserRole @default(AUTHOR)",
                        "emailVerified: Boolean @default(false)",
                        "isActive: Boolean @default(true)",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "// Relations",
                        "posts: Post[]",
                        "comments: Comment[]",
                        "authoredCategories: Category[] @relation(\"CategoryAuthor\")",
                        "",
                        "@@index([email])",
                        "@@index([username])",
                        "@@index([role, isActive])",
                        "@@map(\"users\")"
                    ]
                },
                {
                    "name": "Post",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "title: String",
                        "slug: String @unique",
                        "excerpt: String? @db.Text",
                        "content: String @db.Text",
                        "status: PostStatus @default(DRAFT)",
                        "featured: Boolean @default(false)",
                        "viewCount: Int @default(0)",
                        "commentCount: Int @default(0)",
                        "",
                        "// SEO fields",
                        "metaTitle: String?",
                        "metaDescription: String? @db.Text",
                        "ogImage: String?",
                        "",
                        "// Publishing",
                        "publishedAt: DateTime?",
                        "scheduledAt: DateTime?",
                        "",
                        "// Relations",
                        "authorId: String",
                        "author: User @relation(fields: [authorId], references: [id])",
                        "categoryId: String?",
                        "category: Category? @relation(fields: [categoryId], references: [id])",
                        "comments: Comment[]",
                        "tags: TagOnPost[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([authorId, status])",
                        "@@index([categoryId, status])",
                        "@@index([status, publishedAt])",
                        "@@index([slug])",
                        "@@index([featured, status])",
                        "@@map(\"posts\")"
                    ]
                },
                {
                    "name": "Category",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "name: String @unique",
                        "slug: String @unique",
                        "description: String? @db.Text",
                        "color: String? // Hex color code",
                        "icon: String?",
                        "isActive: Boolean @default(true)",
                        "postCount: Int @default(0)",
                        "",
                        "// Hierarchy support",
                        "parentId: String?",
                        "parent: Category? @relation(\"CategoryHierarchy\", fields: [parentId], references: [id])",
                        "children: Category[] @relation(\"CategoryHierarchy\")",
                        "",
                        "// Relations",
                        "posts: Post[]",
                        "authorId: String",
                        "author: User @relation(\"CategoryAuthor\", fields: [authorId], references: [id])",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([parentId])",
                        "@@index([isActive, name])",
                        "@@index([slug])",
                        "@@map(\"categories\")"
                    ]
                },
                {
                    "name": "Tag",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "name: String @unique",
                        "slug: String @unique",
                        "description: String?",
                        "color: String?",
                        "postCount: Int @default(0)",
                        "",
                        "// Relations",
                        "posts: TagOnPost[]",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([name])",
                        "@@index([slug])",
                        "@@map(\"tags\")"
                    ]
                },
                {
                    "name": "TagOnPost",
                    "fields": [
                        "postId: String",
                        "tagId: String",
                        "",
                        "post: Post @relation(fields: [postId], references: [id], onDelete: Cascade)",
                        "tag: Tag @relation(fields: [tagId], references: [id], onDelete: Cascade)",
                        "",
                        "assignedAt: DateTime @default(now())",
                        "",
                        "@@id([postId, tagId])",
                        "@@map(\"post_tags\")"
                    ]
                },
                {
                    "name": "Comment",
                    "fields": [
                        "id: String @id @default(cuid())",
                        "content: String @db.Text",
                        "status: CommentStatus @default(PENDING)",
                        "ipAddress: String?",
                        "userAgent: String?",
                        "",
                        "// Thread support",
                        "parentId: String?",
                        "parent: Comment? @relation(\"CommentThread\", fields: [parentId], references: [id])",
                        "replies: Comment[] @relation(\"CommentThread\")",
                        "",
                        "// Relations",
                        "postId: String",
                        "post: Post @relation(fields: [postId], references: [id], onDelete: Cascade)",
                        "authorId: String?",
                        "author: User? @relation(fields: [authorId], references: [id])",
                        "",
                        "// Guest comment fields (if no author)",
                        "guestName: String?",
                        "guestEmail: String?",
                        "guestWebsite: String?",
                        "",
                        "// Metadata",
                        "createdAt: DateTime @default(now())",
                        "updatedAt: DateTime @updatedAt",
                        "",
                        "@@index([postId, status])",
                        "@@index([authorId])",
                        "@@index([parentId])",
                        "@@index([status, createdAt])",
                        "@@map(\"comments\")"
                    ]
                }
            ],
            "enums": [
                {
                    "name": "UserRole",
                    "values": ["ADMIN", "EDITOR", "AUTHOR", "MODERATOR", "SUBSCRIBER"]
                },
                {
                    "name": "PostStatus",
                    "values": ["DRAFT", "PENDING", "PUBLISHED", "ARCHIVED", "DELETED"]
                },
                {
                    "name": "CommentStatus",
                    "values": ["PENDING", "APPROVED", "REJECTED", "SPAM", "DELETED"]
                }
            ]
        }

    def get_optimization_config(self) -> Dict[str, Any]:
        """Оптимизации для Blog/CMS."""
        return {
            "indexes": [
                # Performance indexes для блога
                "CREATE INDEX CONCURRENTLY idx_posts_published ON posts (status, published_at DESC) WHERE status = 'PUBLISHED';",
                "CREATE INDEX CONCURRENTLY idx_posts_author_status ON posts (author_id, status, created_at DESC);",
                "CREATE INDEX CONCURRENTLY idx_posts_category_published ON posts (category_id, status, published_at DESC) WHERE status = 'PUBLISHED';",
                "CREATE INDEX CONCURRENTLY idx_posts_featured ON posts (featured, status, published_at DESC) WHERE featured = true AND status = 'PUBLISHED';",
                "CREATE INDEX CONCURRENTLY idx_comments_post_status ON comments (post_id, status, created_at DESC);",
                "CREATE INDEX CONCURRENTLY idx_posts_slug_gin ON posts USING gin(to_tsvector('english', title || ' ' || excerpt || ' ' | content));",

                # Search indexes
                "CREATE INDEX CONCURRENTLY idx_posts_search ON posts USING gin(to_tsvector('english', title || ' ' || content));",
                "CREATE INDEX CONCURRENTLY idx_categories_search ON categories USING gin(to_tsvector('english', name || ' ' || description));",
                "CREATE INDEX CONCURRENTLY idx_tags_search ON tags USING gin(to_tsvector('english', name || ' ' || description));"
            ],
            "triggers": [
                # Auto-update post counts
                """
                CREATE OR REPLACE FUNCTION update_category_post_count()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        UPDATE categories SET post_count = post_count + 1 WHERE id = NEW.category_id;
                        RETURN NEW;
                    ELSIF TG_OP = 'UPDATE' THEN
                        IF OLD.category_id != NEW.category_id THEN
                            UPDATE categories SET post_count = post_count - 1 WHERE id = OLD.category_id;
                            UPDATE categories SET post_count = post_count + 1 WHERE id = NEW.category_id;
                        END IF;
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' THEN
                        UPDATE categories SET post_count = post_count - 1 WHERE id = OLD.category_id;
                        RETURN OLD;
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_category_post_count
                AFTER INSERT OR UPDATE OR DELETE ON posts
                FOR EACH ROW EXECUTE FUNCTION update_category_post_count();
                """,

                # Auto-update comment counts
                """
                CREATE OR REPLACE FUNCTION update_post_comment_count()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' THEN
                        UPDATE posts SET comment_count = comment_count - 1 WHERE id = OLD.post_id;
                        RETURN OLD;
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_post_comment_count
                AFTER INSERT OR DELETE ON comments
                FOR EACH ROW EXECUTE FUNCTION update_post_comment_count();
                """
            ],
            "views": [
                # Популярные посты
                """
                CREATE VIEW popular_posts AS
                SELECT
                    p.*,
                    u.name as author_name,
                    u.username as author_username,
                    c.name as category_name,
                    c.slug as category_slug
                FROM posts p
                LEFT JOIN users u ON p.author_id = u.id
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'PUBLISHED'
                ORDER BY p.view_count DESC, p.comment_count DESC;
                """,

                # Последние комментарии
                """
                CREATE VIEW latest_comments AS
                SELECT
                    cm.*,
                    p.title as post_title,
                    p.slug as post_slug,
                    u.name as author_name,
                    u.username as author_username
                FROM comments cm
                LEFT JOIN posts p ON cm.post_id = p.id
                LEFT JOIN users u ON cm.author_id = u.id
                WHERE cm.status = 'APPROVED'
                ORDER BY cm.created_at DESC;
                """
            ]
        }


# Пример использования
def get_blog_dependencies() -> BlogPrismaDependencies:
    """Создать конфигурацию для Blog/CMS проекта."""
    return BlogPrismaDependencies(
        database_url="postgresql://user:password@localhost:5432/blog_db",
        domain_type="blog",
        project_type="cms",
        enable_comments=True,
        enable_categories=True,
        enable_tags=True,
        enable_seo_features=True,
        comment_moderation=True
    )