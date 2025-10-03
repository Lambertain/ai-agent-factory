"""Dependencies and context management for TypeScript Architecture Agent."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class TypeScriptArchitectureDependencies:
    """Зависимости для TypeScript Architecture Agent с поддержкой RAG."""

    # Основные настройки
    agent_name: str = "typescript_architecture"  # For RAG protection
    context: str = ""
    project_path: str = ""
    project_name: str = ""

    # Универсальная конфигурация проекта
    project_type: str = "frontend"  # frontend, backend, full-stack, library, mobile
    framework: str = "react"  # react, vue, angular, nextjs, nestjs, express, etc.
    architecture_focus: str = "type-safety"  # type-safety, performance, maintainability, scalability

    # Режимы анализа
    analysis_mode: str = "full"  # full, types, performance, refactor, migration

    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "typescript-architecture",
        "agent-knowledge",
        "pydantic-ai",
        "type-safety"
    ])
    knowledge_domain: str = "typescript-docs"
    archon_url: str = "http://localhost:3737"
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"

    # Domain-specific конфигурация
    domain_types: Dict[str, List[str]] = field(default_factory=dict)
    architectural_patterns: List[str] = field(default_factory=list)

    # Настройки анализа
    max_complexity_score: int = 10
    target_type_coverage: float = 0.95  # 95% покрытие типами
    performance_budget_ms: int = 5000  # Максимальное время компиляции

    # Кэш для оптимизации
    analysis_cache: Dict[str, Any] = field(default_factory=dict)

    # Отслеживание улучшений
    improvements_made: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация конфигурации после создания."""
        # Настройка тегов на основе анализа
        self._setup_analysis_tags()

        # Настройка domain-specific конфигурации
        self._setup_domain_defaults()

        # Настройка архитектурных паттернов
        self._setup_architectural_patterns()

        # Обновление knowledge tags
        self._update_knowledge_tags()

        # Проверка обязательных настроек
        if not self.context:
            self.context = f"TypeScript architecture analysis for {self.project_type} {self.framework} project"

    def add_improvement(self, improvement: str, is_breaking: bool = False):
        """Добавление записи об улучшении."""
        self.improvements_made.append(improvement)
        if is_breaking:
            self.breaking_changes.append(improvement)

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Получение сводки анализа."""
        return {
            "project_type": self.project_type,
            "framework": self.framework,
            "architecture_focus": self.architecture_focus,
            "mode": self.analysis_mode,
            "improvements_count": len(self.improvements_made),
            "breaking_changes_count": len(self.breaking_changes),
            "target_coverage": self.target_type_coverage,
            "performance_budget": self.performance_budget_ms,
            "architectural_patterns": self.architectural_patterns
        }

    def _setup_analysis_tags(self):
        """Настройка тегов на основе режима анализа."""
        mode_tags = {
            "performance": ["typescript-performance", "compilation-speed"],
            "refactor": ["typescript-refactoring", "code-quality"],
            "migration": ["typescript-migration", "version-upgrade"],
            "types": ["advanced-types", "type-inference"],
            "full": ["comprehensive-analysis", "best-practices"]
        }

        if self.analysis_mode in mode_tags:
            self.knowledge_tags.extend(mode_tags[self.analysis_mode])

    def _setup_domain_defaults(self):
        """Настройка domain-specific типов по умолчанию."""
        if not self.domain_types:
            domain_defaults = {
                "frontend": {
                    "react": ["ComponentProps", "JSX.Element", "ReactNode", "FC", "Component"],
                    "vue": ["Component", "PropType", "ComputedRef", "Ref", "VNode"],
                    "angular": ["Component", "Injectable", "OnInit", "EventEmitter", "TemplateRef"]
                },
                "backend": {
                    "express": ["Request", "Response", "NextFunction", "Router", "Application"],
                    "nestjs": ["Controller", "Injectable", "Module", "Guard", "Interceptor"],
                    "fastify": ["FastifyRequest", "FastifyReply", "FastifyInstance", "RouteOptions"]
                },
                "full-stack": {
                    "nextjs": ["NextPage", "GetServerSideProps", "GetStaticProps", "NextApiRequest"],
                    "t3-stack": ["NextPage", "AppRouter", "TRPCRouter", "PrismaClient"],
                    "remix": ["LoaderFunction", "ActionFunction", "MetaFunction", "LinksFunction"]
                },
                "library": {
                    "npm": ["PublicAPI", "Config", "Options", "Plugin", "Middleware"],
                    "utility": ["Utility", "Helper", "Transformer", "Validator", "Parser"]
                },
                "mobile": {
                    "react-native": ["ComponentProps", "NativeStackScreenProps", "StyleProp", "ViewStyle"]
                }
            }

            if self.project_type in domain_defaults and self.framework in domain_defaults[self.project_type]:
                self.domain_types = {
                    "common_types": domain_defaults[self.project_type][self.framework]
                }

    def _setup_architectural_patterns(self):
        """Настройка архитектурных паттернов."""
        if not self.architectural_patterns:
            pattern_defaults = {
                "frontend": ["Component Composition", "Custom Hooks", "Context API", "State Management"],
                "backend": ["Repository Pattern", "Service Layer", "Dependency Injection", "Middleware Pattern"],
                "full-stack": ["API Routes", "Server Components", "Data Fetching", "Authentication"],
                "library": ["Factory Pattern", "Builder Pattern", "Plugin Architecture", "Public API Design"],
                "mobile": ["Navigation Types", "Platform Detection", "Native Modules", "Performance Optimization"]
            }

            if self.project_type in pattern_defaults:
                self.architectural_patterns = pattern_defaults[self.project_type]

    def _update_knowledge_tags(self):
        """Обновление knowledge tags на основе конфигурации."""
        # Добавляем теги на основе типа проекта
        type_tags = {
            "frontend": ["frontend-architecture", "component-design", "state-management"],
            "backend": ["backend-architecture", "api-design", "database-types"],
            "full-stack": ["full-stack-architecture", "ssr", "api-routes"],
            "library": ["library-design", "public-api", "npm-packaging"],
            "mobile": ["mobile-development", "react-native", "platform-specific"]
        }

        # Добавляем теги на основе фреймворка
        framework_tags = {
            "react": ["react", "jsx", "hooks", "context"],
            "vue": ["vue", "composition-api", "reactivity", "directives"],
            "angular": ["angular", "decorators", "dependency-injection", "rxjs"],
            "nextjs": ["nextjs", "ssr", "app-router", "server-components"],
            "nestjs": ["nestjs", "decorators", "modules", "guards"],
            "express": ["express", "middleware", "routing", "req-res"]
        }

        # Добавляем теги на основе фокуса архитектуры
        focus_tags = {
            "type-safety": ["strict-types", "type-guards", "runtime-validation"],
            "performance": ["performance", "compilation-speed", "tree-shaking"],
            "maintainability": ["code-organization", "modularity", "documentation"],
            "scalability": ["large-scale", "team-development", "architecture-patterns"]
        }

        if self.project_type in type_tags:
            self.knowledge_tags.extend(type_tags[self.project_type])

        if self.framework in framework_tags:
            self.knowledge_tags.extend(framework_tags[self.framework])

        if self.architecture_focus in focus_tags:
            self.knowledge_tags.extend(focus_tags[self.architecture_focus])

        # Убираем дубликаты
        self.knowledge_tags = list(set(self.knowledge_tags))

    def add_improvement_with_timestamp(self, improvement: str, is_breaking: bool = False):
        """Добавление записи об улучшении с временной меткой."""
        timestamp = datetime.now().isoformat()
        improvement_record = f"[{timestamp}] {improvement}"

        self.improvements_made.append(improvement_record)
        if is_breaking:
            self.breaking_changes.append(improvement_record)

    def should_use_rag(self) -> bool:
        """Определить, нужно ли использовать RAG для текущей задачи."""
        # RAG полезен для сложных задач анализа и рефакторинга
        complex_modes = ["full", "refactor", "migration"]
        return self.analysis_mode in complex_modes

    def get_rag_query_context(self, base_query: str) -> str:
        """Создать контекст для RAG запроса."""
        context_parts = [
            base_query,
            f"Project type: {self.project_type}",
            f"Framework: {self.framework}",
            f"Architecture focus: {self.architecture_focus}",
            f"Analysis mode: {self.analysis_mode}"
        ]

        if self.improvements_made:
            context_parts.append(f"Previous improvements: {len(self.improvements_made)}")

        return " | ".join(context_parts)

    def get_project_context(self) -> str:
        """Получить контекст проекта для принятия архитектурных решений."""
        project_descriptions = {
            "frontend": f"Frontend application using {self.framework} framework",
            "backend": f"Backend service using {self.framework} framework",
            "full-stack": f"Full-stack application using {self.framework} stack",
            "library": f"TypeScript library for {self.framework} ecosystem",
            "mobile": f"Mobile application using {self.framework}"
        }

        return project_descriptions.get(self.project_type, "TypeScript project")

    def validate_configuration(self) -> List[str]:
        """Валидация конфигурации агента."""
        errors = []

        # Валидация project_type
        valid_types = ["frontend", "backend", "full-stack", "library", "mobile"]
        if self.project_type not in valid_types:
            errors.append(f"Invalid project_type: {self.project_type}. Must be one of {valid_types}")

        # Валидация architecture_focus
        valid_focuses = ["type-safety", "performance", "maintainability", "scalability"]
        if self.architecture_focus not in valid_focuses:
            errors.append(f"Invalid architecture_focus: {self.architecture_focus}. Must be one of {valid_focuses}")

        # Валидация analysis_mode
        valid_modes = ["full", "types", "performance", "refactor", "migration"]
        if self.analysis_mode not in valid_modes:
            errors.append(f"Invalid analysis_mode: {self.analysis_mode}. Must be one of {valid_modes}")

        # Валидация performance настроек
        if self.target_type_coverage < 0 or self.target_type_coverage > 1:
            errors.append("target_type_coverage must be between 0 and 1")

        if self.performance_budget_ms <= 0:
            errors.append("performance_budget_ms must be positive")

        return errors

    def get_recommended_settings(self) -> Dict[str, Any]:
        """Получить рекомендуемые настройки для текущего типа проекта."""
        recommendations = {
            "frontend": {
                "target_type_coverage": 0.95,
                "performance_budget_ms": 3000,
                "recommended_patterns": ["Component Composition", "Custom Hooks", "Error Boundaries"],
                "critical_types": ["Props", "State", "Events", "Refs"]
            },
            "backend": {
                "target_type_coverage": 0.98,  # Более строгая типизация для backend
                "performance_budget_ms": 5000,
                "recommended_patterns": ["Repository Pattern", "Service Layer", "DTO Pattern"],
                "critical_types": ["Request", "Response", "Entities", "DTOs"]
            },
            "full-stack": {
                "target_type_coverage": 0.96,
                "performance_budget_ms": 4000,
                "recommended_patterns": ["API Routes", "Server Components", "Shared Types"],
                "critical_types": ["API Schema", "Page Props", "Database Models"]
            },
            "library": {
                "target_type_coverage": 0.99,  # Максимальная типизация для библиотек
                "performance_budget_ms": 2000,
                "recommended_patterns": ["Factory Pattern", "Builder Pattern", "Public API"],
                "critical_types": ["Public API", "Options", "Config", "Plugin"]
            },
            "mobile": {
                "target_type_coverage": 0.94,
                "performance_budget_ms": 3500,
                "recommended_patterns": ["Navigation Types", "Platform Detection", "Native Modules"],
                "critical_types": ["Screen Props", "Navigation", "Platform Types"]
            }
        }

        return recommendations.get(self.project_type, {
            "target_type_coverage": 0.95,
            "performance_budget_ms": 4000,
            "recommended_patterns": ["General TypeScript Patterns"],
            "critical_types": ["Core Types"]
        })