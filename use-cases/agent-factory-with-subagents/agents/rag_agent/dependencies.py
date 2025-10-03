"""Dependencies for Semantic Search Agent."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import asyncpg
import openai
import httpx
from settings import load_settings


@dataclass
class RAGAgentDependencies:
    """Universal dependencies for RAG Agent supporting various knowledge systems."""

    # Core dependencies
    agent_name: str = "rag_agent"  # For RAG protection
    db_pool: Optional[asyncpg.Pool] = None
    openai_client: Optional[openai.AsyncOpenAI] = None
    settings: Optional[Any] = None

    # Universal RAG configuration
    rag_type: str = "semantic-search"  # semantic-search, qa-system, document-analysis, knowledge-base, chat-assistant
    project_path: str = ""
    project_name: str = ""

    # Domain-specific RAG focus
    domain_type: str = "general"  # general, technical, medical, legal, financial, scientific
    use_case: str = "search"  # search, qa, analysis, chat, recommendation, summarization

    # Embedding configuration
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval configuration
    retrieval_strategy: str = "similarity"  # similarity, mmr, rerank, hybrid
    similarity_threshold: float = 0.7
    max_results: int = 10
    rerank_enabled: bool = False

    # Session context
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    query_history: list = field(default_factory=list)

    # RAG Configuration
    knowledge_tags: List[str] = field(default_factory=lambda: ["rag-agent", "agent-knowledge", "pydantic-ai"])
    knowledge_domain: str | None = None
    archon_project_id: str | None = None
    archon_url: str = "http://localhost:3737"

    def __post_init__(self):
        """Initialize configuration after object creation."""
        # Setup RAG-specific defaults
        self._setup_rag_defaults()

        # Configure embedding parameters based on RAG type
        self._setup_embedding_config()

        # Update knowledge tags based on domain and use case
        self._update_knowledge_tags()

    def _setup_rag_defaults(self):
        """Set up default RAG configuration based on type and domain."""
        rag_defaults = {
            "semantic-search": {
                "chunk_size": 1000,
                "chunk_overlap": 200,
                "retrieval_strategy": "similarity",
                "max_results": 10,
                "similarity_threshold": 0.7,
                "use_case": "search"
            },
            "qa-system": {
                "chunk_size": 800,
                "chunk_overlap": 100,
                "retrieval_strategy": "mmr",
                "max_results": 5,
                "similarity_threshold": 0.8,
                "use_case": "qa"
            },
            "document-analysis": {
                "chunk_size": 1500,
                "chunk_overlap": 300,
                "retrieval_strategy": "hybrid",
                "max_results": 15,
                "similarity_threshold": 0.6,
                "use_case": "analysis"
            },
            "knowledge-base": {
                "chunk_size": 1200,
                "chunk_overlap": 200,
                "retrieval_strategy": "rerank",
                "max_results": 8,
                "similarity_threshold": 0.75,
                "use_case": "search",
                "rerank_enabled": True
            },
            "chat-assistant": {
                "chunk_size": 800,
                "chunk_overlap": 150,
                "retrieval_strategy": "mmr",
                "max_results": 3,
                "similarity_threshold": 0.8,
                "use_case": "chat"
            }
        }

        if self.rag_type in rag_defaults:
            defaults = rag_defaults[self.rag_type]
            # Only update if not explicitly set
            if self.chunk_size == 1000:  # default value
                self.chunk_size = defaults["chunk_size"]
                self.chunk_overlap = defaults["chunk_overlap"]
                self.retrieval_strategy = defaults["retrieval_strategy"]
                self.max_results = defaults["max_results"]
                self.similarity_threshold = defaults["similarity_threshold"]
                if "rerank_enabled" in defaults:
                    self.rerank_enabled = defaults["rerank_enabled"]
                if "use_case" in defaults and self.use_case == "search":
                    self.use_case = defaults["use_case"]

        # Domain-specific adjustments
        domain_adjustments = {
            "technical": {
                "similarity_threshold": 0.8,  # Higher precision for technical content
                "chunk_size": 1200,
                "embedding_model": "text-embedding-3-large"
            },
            "medical": {
                "similarity_threshold": 0.85,  # Very high precision for medical
                "chunk_size": 1000,
                "rerank_enabled": True
            },
            "legal": {
                "similarity_threshold": 0.9,  # Highest precision for legal
                "chunk_size": 1500,  # Larger chunks for legal documents
                "rerank_enabled": True
            },
            "financial": {
                "similarity_threshold": 0.8,
                "chunk_size": 1000,
                "rerank_enabled": True
            },
            "scientific": {
                "similarity_threshold": 0.75,
                "chunk_size": 1300,
                "embedding_model": "text-embedding-3-large"
            }
        }

        if self.domain_type in domain_adjustments:
            adjustments = domain_adjustments[self.domain_type]
            for key, value in adjustments.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def _setup_embedding_config(self):
        """Configure embedding settings based on RAG type and domain."""
        # Model selection based on requirements
        model_recommendations = {
            "technical": "text-embedding-3-large",
            "medical": "text-embedding-3-large",
            "legal": "text-embedding-3-large",
            "scientific": "text-embedding-3-large",
            "general": "text-embedding-3-small"
        }

        if self.domain_type in model_recommendations:
            recommended_model = model_recommendations[self.domain_type]
            if self.embedding_model == "text-embedding-3-small":  # default
                self.embedding_model = recommended_model
                # Update dimensions for large model
                if "large" in recommended_model:
                    self.embedding_dimension = 3072

    def _update_knowledge_tags(self):
        """Update knowledge tags based on RAG configuration."""
        # Add RAG type specific tags
        type_tags = {
            "semantic-search": ["semantic-search", "vector-search", "similarity"],
            "qa-system": ["question-answering", "qa", "conversational"],
            "document-analysis": ["document-analysis", "text-mining", "information-extraction"],
            "knowledge-base": ["knowledge-management", "knowledge-base", "enterprise-search"],
            "chat-assistant": ["chat", "conversational-ai", "assistant"]
        }

        # Add domain specific tags
        domain_tags = {
            "technical": ["technical-docs", "api-docs", "code-search"],
            "medical": ["medical", "healthcare", "clinical"],
            "legal": ["legal", "contracts", "compliance"],
            "financial": ["financial", "banking", "fintech"],
            "scientific": ["scientific", "research", "academic"],
            "general": ["general-knowledge", "multi-domain"]
        }

        # Add use case tags
        use_case_tags = {
            "search": ["search", "retrieval", "lookup"],
            "qa": ["qa", "question-answering", "faq"],
            "analysis": ["analysis", "insights", "summarization"],
            "chat": ["chat", "conversation", "dialogue"],
            "recommendation": ["recommendation", "suggestion", "personalization"],
            "summarization": ["summarization", "synthesis", "summary"]
        }

        if self.rag_type in type_tags:
            self.knowledge_tags.extend(type_tags[self.rag_type])

        if self.domain_type in domain_tags:
            self.knowledge_tags.extend(domain_tags[self.domain_type])

        if self.use_case in use_case_tags:
            self.knowledge_tags.extend(use_case_tags[self.use_case])

        # Remove duplicates
        self.knowledge_tags = list(set(self.knowledge_tags))

    def get_rag_context(self) -> str:
        """Get RAG context description for prompts."""
        rag_descriptions = {
            "semantic-search": "Semantic search system for finding relevant information",
            "qa-system": "Question-answering system for providing accurate responses",
            "document-analysis": "Document analysis system for extracting insights",
            "knowledge-base": "Knowledge base system for enterprise information retrieval",
            "chat-assistant": "Conversational assistant with knowledge retrieval"
        }

        domain_contexts = {
            "technical": "technical documentation and API references",
            "medical": "medical literature and clinical information",
            "legal": "legal documents and regulatory compliance",
            "financial": "financial reports and market analysis",
            "scientific": "scientific papers and research data",
            "general": "general knowledge and information"
        }

        rag_desc = rag_descriptions.get(self.rag_type, "RAG system")
        domain_desc = domain_contexts.get(self.domain_type, "general information")

        return f"{rag_desc} focused on {domain_desc}"

    def get_chunking_strategy(self) -> Dict[str, Any]:
        """Get optimal chunking strategy for current configuration."""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "strategy": "recursive" if self.domain_type in ["technical", "legal"] else "sentence",
            "separators": ["\n\n", "\n", " ", ""] if self.domain_type == "general" else ["\\n\\n", "\\n", ". ", " "],
            "preserve_structure": self.domain_type in ["legal", "medical"]
        }

    def get_retrieval_config(self) -> Dict[str, Any]:
        """Get retrieval configuration."""
        return {
            "strategy": self.retrieval_strategy,
            "similarity_threshold": self.similarity_threshold,
            "max_results": self.max_results,
            "rerank_enabled": self.rerank_enabled,
            "mmr_diversity": 0.3 if self.retrieval_strategy == "mmr" else None,
            "hybrid_weights": {"semantic": 0.7, "keyword": 0.3} if self.retrieval_strategy == "hybrid" else None
        }

    def validate_configuration(self) -> List[str]:
        """Validate RAG configuration."""
        errors = []

        # Validate RAG type
        valid_rag_types = ["semantic-search", "qa-system", "document-analysis", "knowledge-base", "chat-assistant"]
        if self.rag_type not in valid_rag_types:
            errors.append(f"Invalid rag_type: {self.rag_type}. Must be one of {valid_rag_types}")

        # Validate domain type
        valid_domains = ["general", "technical", "medical", "legal", "financial", "scientific"]
        if self.domain_type not in valid_domains:
            errors.append(f"Invalid domain_type: {self.domain_type}. Must be one of {valid_domains}")

        # Validate similarity threshold
        if not 0.0 <= self.similarity_threshold <= 1.0:
            errors.append("similarity_threshold must be between 0.0 and 1.0")

        # Validate chunk size
        if self.chunk_size <= 0:
            errors.append("chunk_size must be positive")

        return errors

    def get_recommended_settings(self) -> Dict[str, Any]:
        """Get recommended settings for current RAG type and domain."""
        recommendations = {
            "embedding_model": self.embedding_model,
            "chunking": self.get_chunking_strategy(),
            "retrieval": self.get_retrieval_config(),
            "context": self.get_rag_context(),
            "performance_tips": self._get_performance_tips()
        }

        return recommendations

    def _get_performance_tips(self) -> List[str]:
        """Get performance optimization tips."""
        tips = [
            "Use batch processing for large document sets",
            "Implement caching for frequently accessed embeddings",
            "Consider index optimization for production use"
        ]

        if self.domain_type in ["medical", "legal"]:
            tips.append("Enable reranking for higher precision in specialized domains")

        if self.rag_type == "chat-assistant":
            tips.append("Implement conversation memory for better context")

        if self.retrieval_strategy == "hybrid":
            tips.append("Fine-tune semantic/keyword balance based on query types")

        return tips

    async def initialize(self):
        """Initialize external connections."""
        if not self.settings:
            self.settings = load_settings()
        
        # Initialize database pool
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                self.settings.database_url,
                min_size=self.settings.db_pool_min_size,
                max_size=self.settings.db_pool_max_size
            )
        
        # Initialize OpenAI client (or compatible provider)
        if not self.openai_client:
            self.openai_client = openai.AsyncOpenAI(
                api_key=self.settings.llm_api_key,
                base_url=self.settings.llm_base_url
            )
    
    async def cleanup(self):
        """Clean up external connections."""
        if self.db_pool:
            await self.db_pool.close()
            self.db_pool = None
    
    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using OpenAI."""
        if not self.openai_client:
            await self.initialize()
        
        response = await self.openai_client.embeddings.create(
            model=self.settings.embedding_model,
            input=text
        )
        # Return as list of floats - asyncpg will handle conversion
        return response.data[0].embedding
    
    def set_user_preference(self, key: str, value: Any):
        """Set a user preference for the session."""
        self.user_preferences[key] = value
    
    def add_to_history(self, query: str):
        """Add a query to the search history."""
        self.query_history.append(query)
        # Keep only last 10 queries
        if len(self.query_history) > 10:
            self.query_history.pop(0)