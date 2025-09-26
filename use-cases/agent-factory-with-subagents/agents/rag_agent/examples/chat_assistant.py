"""
Example configuration for Conversational Chat Assistant RAG Agent.

This configuration sets up the RAG Agent for interactive chat experiences
with context-aware responses and conversation memory.
"""

import asyncio
from ..agent import search_agent
from ..dependencies import RAGAgentDependencies


async def personal_assistant_chat():
    """Personal AI assistant with conversational RAG capabilities."""

    # Configure dependencies for personal assistant
    deps = RAGAgentDependencies(
        # Universal RAG configuration
        rag_type="chat-assistant",
        project_path="/path/to/personal/knowledge",
        project_name="Personal AI Assistant",

        # Domain-specific RAG focus
        domain_type="general",
        use_case="chat",

        # Chat-optimized configuration
        embedding_model="text-embedding-3-small",  # Cost-effective for conversations
        embedding_dimension=1536,
        chunk_size=800,  # Smaller chunks for conversational context
        chunk_overlap=150,

        # MMR retrieval for diverse conversation topics
        retrieval_strategy="mmr",
        similarity_threshold=0.8,
        max_results=3,  # Few but relevant results for chat
        rerank_enabled=False,

        # Session context for conversation memory
        session_id="personal-chat-001",
        user_preferences={
            "communication_style": "friendly",
            "response_length": "concise",
            "interests": ["technology", "productivity", "learning"],
            "conversation_context": "personal_assistant"
        },
        query_history=[],

        # RAG Configuration
        knowledge_tags=["personal-assistant", "chat", "conversational-ai", "general-knowledge"],
        knowledge_domain="personal.assistant.com",
        archon_project_id="personal-assistant-project"
    )

    # Example conversational interaction
    conversation_flow = [
        "Hi! Can you help me plan my day?",
        "What are some productivity techniques I should know about?",
        "Tell me about the Pomodoro Technique",
        "How can I implement this in my work routine?",
        "What other time management methods work well with Pomodoro?",
        "Can you remind me about my previous question about productivity?",
        "Thanks! What about stress management techniques?",
        "How do I know which technique will work best for me?"
    ]

    print("🤖 Starting Personal Assistant Chat...")

    for i, message in enumerate(conversation_flow, 1):
        print(f"\n👤 User {i}: {message}")

        # Add to conversation history
        deps.add_to_history(message)

        try:
            result = await search_agent.run(
                user_prompt=message,
                deps=deps
            )

            print(f"🤖 Assistant {i}: {result.data}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def customer_service_chat():
    """Customer service chat assistant with support knowledge."""

    # Configure for customer service chat
    deps = RAGAgentDependencies(
        rag_type="chat-assistant",
        project_path="/path/to/support/knowledge",
        project_name="Customer Service Chat Assistant",

        domain_type="general",
        use_case="chat",

        # Customer service optimization
        embedding_model="text-embedding-3-small",
        chunk_size=700,  # Shorter for quick support responses
        chunk_overlap=100,
        retrieval_strategy="mmr",
        similarity_threshold=0.85,  # Higher precision for support
        max_results=3,
        rerank_enabled=False,

        session_id="customer-chat-001",
        user_preferences={
            "communication_style": "professional",
            "response_length": "detailed",
            "urgency_level": "medium",
            "customer_tier": "premium"
        },

        knowledge_tags=["customer-service", "support-chat", "troubleshooting", "help"],
        knowledge_domain="support.customer.com"
    )

    # Customer service conversation
    support_conversation = [
        "Hello, I'm having trouble logging into my account",
        "I've tried resetting my password but I'm not receiving the email",
        "My email is correct, but still no reset email in inbox or spam",
        "Could you check if there's an issue with my account?",
        "Great! Now I can log in. Can you help me update my billing information?",
        "I need to change my credit card and billing address",
        "Thank you! One more question - how do I download my data?",
        "Perfect, that's exactly what I needed. Thanks for your help!"
    ]

    print("🎧 Starting Customer Service Chat...")

    for i, message in enumerate(support_conversation, 1):
        print(f"\n👤 Customer {i}: {message}")

        deps.add_to_history(message)

        try:
            result = await search_agent.run(
                user_prompt=f"Customer support request: {message}",
                deps=deps
            )

            print(f"🎧 Support {i}: {result.data}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def educational_tutor_chat():
    """Educational tutor chat assistant for learning support."""

    # Configure for educational tutor
    deps = RAGAgentDependencies(
        rag_type="chat-assistant",
        project_path="/path/to/educational/content",
        project_name="Educational Tutor Chat",

        domain_type="general",
        use_case="chat",

        # Educational optimization
        embedding_model="text-embedding-3-small",
        chunk_size=900,  # Good for educational explanations
        chunk_overlap=150,
        retrieval_strategy="mmr",
        similarity_threshold=0.75,  # Balanced for learning
        max_results=4,  # More context for education
        rerank_enabled=False,

        session_id="tutor-chat-001",
        user_preferences={
            "learning_style": "visual",
            "difficulty_level": "intermediate",
            "subject_areas": ["programming", "data-science", "web-development"],
            "explanation_style": "step-by-step"
        },

        knowledge_tags=["educational-tutor", "learning", "programming", "tutorials"],
        knowledge_domain="education.tutor.com"
    )

    # Educational conversation
    learning_conversation = [
        "Can you explain what machine learning is?",
        "What's the difference between supervised and unsupervised learning?",
        "Can you give me a simple example of supervised learning?",
        "How would I implement this in Python?",
        "What libraries should I use for machine learning in Python?",
        "Can you show me a basic example with scikit-learn?",
        "What should I learn next after understanding basic ML concepts?",
        "How long does it typically take to become proficient in ML?"
    ]

    print("📚 Starting Educational Tutor Chat...")

    for i, message in enumerate(learning_conversation, 1):
        print(f"\n🎓 Student {i}: {message}")

        deps.add_to_history(message)

        try:
            result = await search_agent.run(
                user_prompt=f"Educational question: {message}",
                deps=deps
            )

            print(f"📚 Tutor {i}: {result.data[:300]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def technical_advisor_chat():
    """Technical advisor chat assistant for development teams."""

    # Configure for technical advisor
    deps = RAGAgentDependencies(
        rag_type="chat-assistant",
        project_path="/path/to/technical/docs",
        project_name="Technical Advisor Chat",

        domain_type="technical",
        use_case="chat",

        # Technical advisor optimization
        embedding_model="text-embedding-3-large",  # Better for technical terms
        embedding_dimension=3072,
        chunk_size=1000,  # More technical context
        chunk_overlap=200,
        retrieval_strategy="mmr",
        similarity_threshold=0.8,
        max_results=3,
        rerank_enabled=False,

        session_id="tech-advisor-001",
        user_preferences={
            "expertise_level": "senior",
            "technologies": ["python", "javascript", "docker", "kubernetes"],
            "response_style": "technical",
            "include_examples": True
        },

        knowledge_tags=["technical-advisor", "development", "architecture", "best-practices"],
        knowledge_domain="tech.advisor.com"
    )

    # Technical conversation
    tech_conversation = [
        "What's the best approach for microservices architecture?",
        "How should I handle inter-service communication?",
        "What about data consistency across microservices?",
        "Can you explain the Saga pattern for distributed transactions?",
        "How do I implement monitoring and observability?",
        "What are the key metrics I should track?",
        "How do I handle service discovery in Kubernetes?",
        "What's your recommendation for CI/CD with microservices?"
    ]

    print("💻 Starting Technical Advisor Chat...")

    for i, message in enumerate(tech_conversation, 1):
        print(f"\n👨‍💻 Developer {i}: {message}")

        deps.add_to_history(message)

        try:
            result = await search_agent.run(
                user_prompt=f"Technical question: {message}",
                deps=deps
            )

            print(f"💻 Advisor {i}: {result.data[:350]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


# Example usage patterns
async def main():
    """Example usage of chat assistant RAG agent."""

    print("💬 Starting Chat Assistant RAG Agent Examples...")

    # Personal assistant chat
    print("\n🤖 Personal Assistant Chat")
    personal_deps = await personal_assistant_chat()

    # Customer service chat
    print("\n🎧 Customer Service Chat")
    service_deps = await customer_service_chat()

    # Educational tutor chat
    print("\n📚 Educational Tutor Chat")
    tutor_deps = await educational_tutor_chat()

    # Technical advisor chat
    print("\n💻 Technical Advisor Chat")
    tech_deps = await technical_advisor_chat()

    # Conversation analysis
    print("\n📊 Conversation Analysis:")

    chat_systems = [
        ("Personal", personal_deps),
        ("Customer Service", service_deps),
        ("Educational", tutor_deps),
        ("Technical", tech_deps)
    ]

    for name, deps in chat_systems:
        history_length = len(deps.query_history)
        print(f"\n{name} Assistant:")
        print(f"  Conversation length: {history_length} exchanges")
        print(f"  Domain: {deps.domain_type}")
        print(f"  Chunk size: {deps.chunk_size}")
        print(f"  Communication style: {deps.user_preferences.get('communication_style', 'default')}")

        # Show last 2 queries from conversation
        if deps.query_history:
            print(f"  Recent topics:")
            for query in deps.query_history[-2:]:
                print(f"    - {query[:50]}...")

    # Chat optimization insights
    print("\n💡 Chat Optimization Insights:")

    # Chunk size analysis for chat
    chunk_sizes = [deps.chunk_size for _, deps in chat_systems]
    avg_chunk_size = sum(chunk_sizes) / len(chunk_sizes)
    print(f"  Average chunk size for chat: {avg_chunk_size:.0f}")

    # Response configuration
    max_results = [deps.max_results for _, deps in chat_systems]
    avg_max_results = sum(max_results) / len(max_results)
    print(f"  Average max results for chat: {avg_max_results:.1f}")

    # Communication styles
    styles = [deps.user_preferences.get('communication_style', 'default') for _, deps in chat_systems]
    print(f"  Communication styles: {', '.join(set(styles))}")


if __name__ == "__main__":
    asyncio.run(main())