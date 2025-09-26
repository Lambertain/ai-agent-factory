"""
Example configuration for Question-Answering RAG System.

This configuration sets up the RAG Agent for conversational Q&A
with context-aware responses and memory management.
"""

import asyncio
from ..agent import search_agent
from ..dependencies import RAGAgentDependencies


async def customer_support_qa():
    """Customer support Q&A system with conversational memory."""

    # Configure dependencies for customer support
    deps = RAGAgentDependencies(
        # Universal RAG configuration
        rag_type="qa-system",
        project_path="/path/to/support/docs",
        project_name="Customer Support Q&A System",

        # Domain-specific RAG focus
        domain_type="general",  # Customer-facing content
        use_case="qa",

        # Q&A optimized configuration
        embedding_model="text-embedding-3-small",  # Cost-effective for general content
        embedding_dimension=1536,
        chunk_size=800,  # Smaller chunks for focused answers
        chunk_overlap=100,

        # MMR retrieval for diverse answers
        retrieval_strategy="mmr",
        similarity_threshold=0.8,
        max_results=5,  # Fewer results for focused answers
        rerank_enabled=False,

        # Session context for conversation
        session_id="support-qa-001",
        user_preferences={
            "communication_style": "friendly",
            "detail_level": "moderate",
            "include_examples": True
        },
        query_history=[],

        # RAG Configuration
        knowledge_tags=["customer-support", "qa", "help-docs", "faq"],
        knowledge_domain="support.company.com",
        archon_project_id="support-qa-project"
    )

    # Example Q&A conversation
    qa_conversation = [
        "How do I reset my password?",
        "What if I don't receive the reset email?",
        "Can I change my email address?",
        "How do I update my billing information?",
        "What payment methods do you accept?"
    ]

    print("💬 Starting Customer Support Q&A...")

    for i, question in enumerate(qa_conversation, 1):
        print(f"\n❓ Q{i}: {question}")

        # Add to conversation history
        deps.add_to_history(question)

        try:
            result = await search_agent.run(
                user_prompt=f"Answer this customer question: {question}",
                deps=deps
            )

            print(f"✅ A{i}: {result.data}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def technical_qa_system():
    """Technical Q&A system for developers and technical users."""

    # Configure for technical Q&A
    deps = RAGAgentDependencies(
        rag_type="qa-system",
        project_path="/path/to/technical/docs",
        project_name="Technical Q&A System",

        domain_type="technical",
        use_case="qa",

        # Technical content optimization
        embedding_model="text-embedding-3-large",  # Better for technical terms
        embedding_dimension=3072,
        chunk_size=1000,
        chunk_overlap=150,

        retrieval_strategy="mmr",
        similarity_threshold=0.85,  # Higher precision for technical accuracy
        max_results=3,  # Focused technical answers
        rerank_enabled=True,

        session_id="tech-qa-001",
        user_preferences={
            "include_code_examples": True,
            "show_api_references": True,
            "detail_level": "comprehensive"
        },

        knowledge_tags=["technical-qa", "api-docs", "code-examples", "troubleshooting"],
        knowledge_domain="docs.technical.com"
    )

    technical_questions = [
        "How do I configure database connection pooling?",
        "What's the best way to handle authentication errors?",
        "How to implement rate limiting in the API?",
        "What are the recommended caching strategies?",
        "How to debug memory leaks in the application?"
    ]

    print("🔧 Starting Technical Q&A System...")

    for question in technical_questions:
        print(f"\n🔍 Technical Q: {question}")

        try:
            result = await search_agent.run(
                user_prompt=f"Provide a technical answer with examples: {question}",
                deps=deps
            )

            print(f"💡 Technical A: {result.data[:300]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def educational_qa_system():
    """Educational Q&A system for learning and training content."""

    # Configure for educational content
    deps = RAGAgentDependencies(
        rag_type="qa-system",
        project_path="/path/to/educational/content",
        project_name="Educational Q&A System",

        domain_type="general",
        use_case="qa",

        # Educational content optimization
        embedding_model="text-embedding-3-small",
        chunk_size=900,
        chunk_overlap=120,

        retrieval_strategy="mmr",
        similarity_threshold=0.75,  # More inclusive for learning
        max_results=4,
        rerank_enabled=False,

        session_id="edu-qa-001",
        user_preferences={
            "learning_style": "step-by-step",
            "include_examples": True,
            "difficulty_level": "beginner"
        },

        knowledge_tags=["education", "learning", "training", "tutorials"],
        knowledge_domain="learn.platform.com"
    )

    educational_questions = [
        "What is machine learning and how does it work?",
        "Explain the difference between supervised and unsupervised learning",
        "How do neural networks process information?",
        "What are the main types of data preprocessing?",
        "How to evaluate model performance?"
    ]

    print("📚 Starting Educational Q&A System...")

    for question in educational_questions:
        print(f"\n🎓 Education Q: {question}")

        try:
            result = await search_agent.run(
                user_prompt=f"Explain in an educational way: {question}",
                deps=deps
            )

            print(f"📖 Education A: {result.data[:250]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


# Example usage patterns
async def main():
    """Example usage of Q&A RAG system."""

    print("❓ Starting Q&A RAG System Examples...")

    # Customer support Q&A
    print("\n💬 Customer Support Q&A")
    support_deps = await customer_support_qa()

    # Technical Q&A
    print("\n🔧 Technical Q&A System")
    tech_deps = await technical_qa_system()

    # Educational Q&A
    print("\n📚 Educational Q&A System")
    edu_deps = await educational_qa_system()

    # Analyze conversation history
    print(f"\n📊 Support conversation history: {len(support_deps.query_history)} questions")
    for i, query in enumerate(support_deps.query_history[-3:], 1):
        print(f"  {i}. {query}")

    # Compare Q&A configurations
    print("\n⚙️ Q&A Configuration Summary:")
    systems = [
        ("Support", support_deps),
        ("Technical", tech_deps),
        ("Educational", edu_deps)
    ]

    for name, deps in systems:
        print(f"\n{name} Q&A System:")
        print(f"  Domain: {deps.domain_type}")
        print(f"  Chunk Size: {deps.chunk_size}")
        print(f"  Strategy: {deps.retrieval_strategy}")
        print(f"  Max Results: {deps.max_results}")
        print(f"  Use Case: {deps.use_case}")


if __name__ == "__main__":
    asyncio.run(main())