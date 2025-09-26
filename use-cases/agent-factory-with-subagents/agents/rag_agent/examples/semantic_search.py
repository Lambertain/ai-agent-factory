"""
Example configuration for Semantic Search RAG Agent.

This configuration sets up the RAG Agent for semantic document search
and retrieval across various knowledge domains.
"""

import asyncio
from ..agent import search_agent
from ..dependencies import RAGAgentDependencies


async def search_technical_documentation():
    """Search technical documentation with semantic retrieval."""

    # Configure dependencies for technical documentation search
    deps = RAGAgentDependencies(
        # Universal RAG configuration
        rag_type="semantic-search",
        project_path="/path/to/tech/docs",
        project_name="Technical Documentation Search",

        # Domain-specific RAG focus
        domain_type="technical",  # Higher precision for technical content
        use_case="search",

        # Embedding configuration (optimized for technical content)
        embedding_model="text-embedding-3-large",  # Better for technical terms
        embedding_dimension=3072,
        chunk_size=1200,  # Larger chunks for technical documentation
        chunk_overlap=200,

        # Retrieval configuration
        retrieval_strategy="similarity",
        similarity_threshold=0.8,  # Higher precision for technical content
        max_results=10,
        rerank_enabled=False,

        # Session context
        session_id="tech-search-001",
        user_preferences={
            "preferred_languages": ["python", "javascript", "typescript"],
            "focus_areas": ["api-docs", "code-examples", "best-practices"]
        },

        # RAG Configuration
        knowledge_tags=["technical-docs", "api-docs", "code-search"],
        knowledge_domain="docs.technical.com",
        archon_project_id="tech-search-project"
    )

    # Example search queries
    search_queries = [
        "How to implement authentication in REST API?",
        "Best practices for database connection pooling",
        "Error handling patterns in async Python code",
        "JWT token validation implementation",
        "Database migration strategies"
    ]

    print("🔍 Starting Technical Documentation Search...")

    for i, query in enumerate(search_queries, 1):
        print(f"\n📝 Query {i}: {query}")

        try:
            result = await search_agent.run(
                user_prompt=query,
                deps=deps
            )

            print(f"✅ Result: {result.data[:200]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def search_research_papers():
    """Search scientific research papers and academic content."""

    # Configure for scientific research
    deps = RAGAgentDependencies(
        rag_type="semantic-search",
        project_path="/path/to/research/papers",
        project_name="Scientific Research Search",

        domain_type="scientific",
        use_case="search",

        # Scientific content optimization
        embedding_model="text-embedding-3-large",
        chunk_size=1300,  # Larger for academic papers
        chunk_overlap=300,
        similarity_threshold=0.75,  # Slightly lower for broader research
        max_results=8,

        session_id="research-search-001",
        user_preferences={
            "research_fields": ["machine-learning", "nlp", "computer-vision"],
            "publication_years": ["2020", "2021", "2022", "2023", "2024"]
        },

        knowledge_tags=["scientific", "research", "academic", "papers"],
        knowledge_domain="arxiv.org"
    )

    research_queries = [
        "Transformer architecture improvements for NLP",
        "Computer vision applications in medical imaging",
        "Recent advances in reinforcement learning",
        "Attention mechanisms in deep learning models"
    ]

    print("🔬 Starting Research Papers Search...")

    for query in research_queries:
        print(f"\n🔍 Searching: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Find research papers about: {query}",
                deps=deps
            )

            print(f"📄 Found: {result.data[:150]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def search_legal_documents():
    """Search legal documents with high precision requirements."""

    # Configure for legal document search
    deps = RAGAgentDependencies(
        rag_type="semantic-search",
        project_path="/path/to/legal/docs",
        project_name="Legal Document Search",

        domain_type="legal",
        use_case="search",

        # Legal requires highest precision
        embedding_model="text-embedding-3-large",
        chunk_size=1500,  # Larger for legal context
        chunk_overlap=300,
        similarity_threshold=0.9,  # Highest precision
        max_results=5,  # Fewer but more relevant results
        rerank_enabled=True,  # Enable reranking for legal

        session_id="legal-search-001",
        user_preferences={
            "jurisdictions": ["federal", "state", "international"],
            "document_types": ["contracts", "regulations", "case-law"]
        },

        knowledge_tags=["legal", "contracts", "compliance", "regulations"],
        knowledge_domain="legal.docs.com"
    )

    legal_queries = [
        "Data privacy regulations for international transfers",
        "Contract termination clauses and enforcement",
        "Intellectual property licensing agreements",
        "Employment law compliance requirements"
    ]

    print("⚖️ Starting Legal Document Search...")

    for query in legal_queries:
        print(f"\n📋 Legal Query: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Search legal documents for: {query}",
                deps=deps
            )

            print(f"📜 Legal Result: {result.data[:200]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


# Example usage patterns
async def main():
    """Example usage of semantic search RAG agent."""

    print("🎯 Starting Semantic Search RAG Agent Examples...")

    # Technical documentation search
    print("\n💻 Technical Documentation Search")
    tech_deps = await search_technical_documentation()

    # Research papers search
    print("\n🔬 Scientific Research Search")
    research_deps = await search_research_papers()

    # Legal documents search
    print("\n⚖️ Legal Document Search")
    legal_deps = await search_legal_documents()

    # Compare configuration differences
    print("\n📊 Configuration Comparison:")
    configs = [
        ("Technical", tech_deps),
        ("Research", research_deps),
        ("Legal", legal_deps)
    ]

    for name, deps in configs:
        print(f"\n{name} Configuration:")
        print(f"  Domain: {deps.domain_type}")
        print(f"  Chunk Size: {deps.chunk_size}")
        print(f"  Similarity Threshold: {deps.similarity_threshold}")
        print(f"  Max Results: {deps.max_results}")
        print(f"  Rerank Enabled: {deps.rerank_enabled}")
        print(f"  Embedding Model: {deps.embedding_model}")


if __name__ == "__main__":
    asyncio.run(main())