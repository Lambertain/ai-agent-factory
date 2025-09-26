"""
Example configuration for Knowledge Base RAG Agent.

This configuration sets up the RAG Agent for enterprise knowledge management,
information retrieval, and organizational memory systems.
"""

import asyncio
from ..agent import search_agent
from ..dependencies import RAGAgentDependencies


async def enterprise_knowledge_base():
    """Enterprise knowledge management and search system."""

    # Configure dependencies for enterprise knowledge base
    deps = RAGAgentDependencies(
        # Universal RAG configuration
        rag_type="knowledge-base",
        project_path="/path/to/enterprise/knowledge",
        project_name="Enterprise Knowledge Base",

        # Domain-specific RAG focus
        domain_type="general",  # Mixed enterprise content
        use_case="search",

        # Knowledge base optimized configuration
        embedding_model="text-embedding-3-small",  # Cost-effective for large KB
        embedding_dimension=1536,
        chunk_size=1200,  # Good balance for enterprise content
        chunk_overlap=200,

        # Rerank strategy for enterprise accuracy
        retrieval_strategy="rerank",
        similarity_threshold=0.75,
        max_results=8,
        rerank_enabled=True,

        # Session context
        session_id="enterprise-kb-001",
        user_preferences={
            "content_types": ["policies", "procedures", "best-practices", "faqs"],
            "departments": ["hr", "finance", "engineering", "sales"],
            "access_level": "employee"
        },

        # RAG Configuration
        knowledge_tags=["enterprise-kb", "knowledge-management", "organizational-memory"],
        knowledge_domain="knowledge.company.com",
        archon_project_id="enterprise-kb-project"
    )

    # Example enterprise knowledge queries
    enterprise_queries = [
        "What is the company's remote work policy?",
        "How do I submit an expense report?",
        "What are the security guidelines for handling customer data?",
        "How to escalate a customer support issue?",
        "What is the process for requesting vacation time?",
        "Company guidelines for software licensing and procurement",
        "Emergency procedures and contact information",
        "New employee onboarding checklist and timeline"
    ]

    print("🏢 Starting Enterprise Knowledge Base Search...")

    for i, query in enumerate(enterprise_queries, 1):
        print(f"\n📋 Enterprise Query {i}: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Search company knowledge base: {query}",
                deps=deps
            )

            print(f"📚 KB Result: {result.data[:200]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def technical_documentation_kb():
    """Technical documentation knowledge base for development teams."""

    # Configure for technical knowledge base
    deps = RAGAgentDependencies(
        rag_type="knowledge-base",
        project_path="/path/to/technical/docs",
        project_name="Technical Documentation KB",

        domain_type="technical",
        use_case="search",

        # Technical KB optimization
        embedding_model="text-embedding-3-large",  # Better for technical terms
        embedding_dimension=3072,
        chunk_size=1200,
        chunk_overlap=200,
        retrieval_strategy="rerank",
        similarity_threshold=0.75,
        max_results=8,
        rerank_enabled=True,

        session_id="tech-kb-001",
        user_preferences={
            "doc_types": ["api-docs", "architecture", "deployment", "troubleshooting"],
            "technologies": ["python", "javascript", "docker", "kubernetes"],
            "audience": "developers"
        },

        knowledge_tags=["technical-kb", "development", "documentation", "engineering"],
        knowledge_domain="docs.engineering.com"
    )

    technical_queries = [
        "How to set up the development environment?",
        "API authentication and authorization patterns",
        "Database migration best practices",
        "Docker containerization guidelines",
        "Kubernetes deployment configurations",
        "Code review process and standards",
        "Testing strategies and frameworks",
        "Production monitoring and alerting setup"
    ]

    print("💻 Starting Technical Documentation KB...")

    for query in technical_queries:
        print(f"\n🔧 Tech Query: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Find technical documentation: {query}",
                deps=deps
            )

            print(f"📖 Tech KB: {result.data[:250]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def customer_support_kb():
    """Customer support knowledge base for service teams."""

    # Configure for customer support KB
    deps = RAGAgentDependencies(
        rag_type="knowledge-base",
        project_path="/path/to/support/kb",
        project_name="Customer Support Knowledge Base",

        domain_type="general",
        use_case="search",

        # Support KB configuration
        embedding_model="text-embedding-3-small",
        chunk_size=800,  # Smaller for quick support answers
        chunk_overlap=150,
        retrieval_strategy="rerank",
        similarity_threshold=0.75,
        max_results=5,  # Quick, focused answers
        rerank_enabled=True,

        session_id="support-kb-001",
        user_preferences={
            "content_types": ["faqs", "troubleshooting", "how-to-guides"],
            "urgency_levels": ["low", "medium", "high", "critical"],
            "product_areas": ["billing", "technical", "account-management"]
        },

        knowledge_tags=["support-kb", "customer-service", "troubleshooting", "faqs"],
        knowledge_domain="support.help.com"
    )

    support_queries = [
        "How to troubleshoot login issues?",
        "Billing and payment problems resolution",
        "Account suspension and reactivation process",
        "Feature requests and feedback submission",
        "Data export and backup procedures",
        "Integration setup and configuration help",
        "Performance issues and optimization tips",
        "Security incident reporting and response"
    ]

    print("🎧 Starting Customer Support KB...")

    for query in support_queries:
        print(f"\n❓ Support Query: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Search support knowledge base: {query}",
                deps=deps
            )

            print(f"💡 Support KB: {result.data[:200]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def regulatory_compliance_kb():
    """Regulatory compliance knowledge base for legal and compliance teams."""

    # Configure for compliance KB
    deps = RAGAgentDependencies(
        rag_type="knowledge-base",
        project_path="/path/to/compliance/docs",
        project_name="Regulatory Compliance KB",

        domain_type="legal",
        use_case="search",

        # Compliance requires high precision
        embedding_model="text-embedding-3-large",
        chunk_size=1500,  # Larger for regulatory context
        chunk_overlap=300,
        retrieval_strategy="rerank",
        similarity_threshold=0.8,  # Higher precision for compliance
        max_results=6,
        rerank_enabled=True,

        session_id="compliance-kb-001",
        user_preferences={
            "regulations": ["gdpr", "hipaa", "pci-dss", "sox"],
            "jurisdictions": ["eu", "us", "global"],
            "compliance_areas": ["data-privacy", "financial", "healthcare"]
        },

        knowledge_tags=["compliance-kb", "regulatory", "legal", "governance"],
        knowledge_domain="compliance.legal.com"
    )

    compliance_queries = [
        "GDPR data processing requirements and obligations",
        "HIPAA patient data security and access controls",
        "PCI-DSS payment card data protection standards",
        "SOX financial reporting and internal controls",
        "Data breach notification requirements by jurisdiction",
        "Cross-border data transfer compliance mechanisms",
        "Audit preparation and documentation requirements",
        "Incident response and regulatory reporting procedures"
    ]

    print("⚖️ Starting Regulatory Compliance KB...")

    for query in compliance_queries:
        print(f"\n📋 Compliance Query: {query}")

        try:
            result = await search_agent.run(
                user_prompt=f"Search compliance knowledge base: {query}",
                deps=deps
            )

            print(f"📜 Compliance KB: {result.data[:250]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


# Example usage patterns
async def main():
    """Example usage of knowledge base RAG agent."""

    print("📚 Starting Knowledge Base RAG Agent Examples...")

    # Enterprise knowledge base
    print("\n🏢 Enterprise Knowledge Base")
    enterprise_deps = await enterprise_knowledge_base()

    # Technical documentation KB
    print("\n💻 Technical Documentation KB")
    tech_deps = await technical_documentation_kb()

    # Customer support KB
    print("\n🎧 Customer Support KB")
    support_deps = await customer_support_kb()

    # Regulatory compliance KB
    print("\n⚖️ Regulatory Compliance KB")
    compliance_deps = await regulatory_compliance_kb()

    # Knowledge base performance metrics
    print("\n📊 Knowledge Base Performance Summary:")

    kb_systems = [
        ("Enterprise", enterprise_deps),
        ("Technical", tech_deps),
        ("Support", support_deps),
        ("Compliance", compliance_deps)
    ]

    for name, deps in kb_systems:
        print(f"\n{name} KB Configuration:")
        print(f"  Domain: {deps.domain_type}")
        print(f"  Chunk Size: {deps.chunk_size}")
        print(f"  Max Results: {deps.max_results}")
        print(f"  Similarity Threshold: {deps.similarity_threshold}")
        print(f"  Reranking: {'✅' if deps.rerank_enabled else '❌'}")

    # Knowledge base optimization insights
    print("\n💡 KB Optimization Insights:")

    # Analyze chunk sizes by domain
    chunk_sizes = {name: deps.chunk_size for name, deps in kb_systems}
    print(f"  Chunk size range: {min(chunk_sizes.values())} - {max(chunk_sizes.values())}")

    # Analyze precision requirements
    thresholds = {name: deps.similarity_threshold for name, deps in kb_systems}
    print(f"  Precision range: {min(thresholds.values())} - {max(thresholds.values())}")

    # Reranking usage
    rerank_count = sum(1 for _, deps in kb_systems if deps.rerank_enabled)
    print(f"  Reranking usage: {rerank_count}/{len(kb_systems)} systems")

    # Session management
    print(f"\n📈 Session Management:")
    for name, deps in kb_systems:
        session_features = len(deps.user_preferences)
        print(f"  {name}: {session_features} preference categories")


if __name__ == "__main__":
    asyncio.run(main())