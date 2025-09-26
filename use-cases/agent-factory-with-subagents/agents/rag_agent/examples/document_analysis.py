"""
Example configuration for Document Analysis RAG Agent.

This configuration sets up the RAG Agent for comprehensive document
analysis, information extraction, and insight generation.
"""

import asyncio
from ..agent import search_agent
from ..dependencies import RAGAgentDependencies


async def financial_document_analysis():
    """Analyze financial reports and documents for insights."""

    # Configure dependencies for financial analysis
    deps = RAGAgentDependencies(
        # Universal RAG configuration
        rag_type="document-analysis",
        project_path="/path/to/financial/reports",
        project_name="Financial Document Analysis",

        # Domain-specific RAG focus
        domain_type="financial",
        use_case="analysis",

        # Document analysis optimized configuration
        embedding_model="text-embedding-3-large",  # Better for financial terminology
        embedding_dimension=3072,
        chunk_size=1500,  # Larger chunks for financial context
        chunk_overlap=300,

        # Hybrid retrieval for comprehensive analysis
        retrieval_strategy="hybrid",
        similarity_threshold=0.6,  # Lower for broader analysis
        max_results=15,  # More results for comprehensive analysis
        rerank_enabled=True,

        # Session context
        session_id="financial-analysis-001",
        user_preferences={
            "analysis_depth": "comprehensive",
            "include_trends": True,
            "focus_areas": ["revenue", "expenses", "growth", "risks"]
        },

        # RAG Configuration
        knowledge_tags=["financial", "analysis", "reports", "business-intelligence"],
        knowledge_domain="finance.reports.com",
        archon_project_id="financial-analysis-project"
    )

    # Example financial analysis tasks
    analysis_tasks = [
        "Analyze quarterly revenue trends and identify growth patterns",
        "Extract key risk factors mentioned in the financial reports",
        "Compare operating expenses across different business segments",
        "Identify mentions of market opportunities and competitive advantages",
        "Summarize cash flow patterns and liquidity position"
    ]

    print("💰 Starting Financial Document Analysis...")

    for i, task in enumerate(analysis_tasks, 1):
        print(f"\n📊 Analysis Task {i}: {task}")

        try:
            result = await search_agent.run(
                user_prompt=f"Perform financial analysis: {task}",
                deps=deps
            )

            print(f"📈 Analysis Result: {result.data[:300]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def legal_contract_analysis():
    """Analyze legal contracts and agreements for key terms."""

    # Configure for legal document analysis
    deps = RAGAgentDependencies(
        rag_type="document-analysis",
        project_path="/path/to/legal/contracts",
        project_name="Legal Contract Analysis",

        domain_type="legal",
        use_case="analysis",

        # Legal analysis requires high precision
        embedding_model="text-embedding-3-large",
        chunk_size=1500,  # Large chunks for legal context
        chunk_overlap=300,
        retrieval_strategy="rerank",  # Best precision for legal
        similarity_threshold=0.8,
        max_results=10,
        rerank_enabled=True,

        session_id="legal-analysis-001",
        user_preferences={
            "extract_clauses": True,
            "identify_obligations": True,
            "flag_risks": True,
            "analysis_depth": "detailed"
        },

        knowledge_tags=["legal", "contracts", "compliance", "risk-analysis"],
        knowledge_domain="legal.contracts.com"
    )

    legal_analysis_tasks = [
        "Extract all payment terms and conditions from contracts",
        "Identify liability and indemnification clauses",
        "Analyze termination conditions and notice requirements",
        "Find intellectual property and confidentiality provisions",
        "Summarize compliance and regulatory requirements"
    ]

    print("⚖️ Starting Legal Contract Analysis...")

    for task in legal_analysis_tasks:
        print(f"\n📋 Legal Analysis: {task}")

        try:
            result = await search_agent.run(
                user_prompt=f"Analyze legal contracts for: {task}",
                deps=deps
            )

            print(f"📜 Legal Insights: {result.data[:250]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def research_paper_analysis():
    """Analyze research papers for methodology and findings."""

    # Configure for research analysis
    deps = RAGAgentDependencies(
        rag_type="document-analysis",
        project_path="/path/to/research/papers",
        project_name="Research Paper Analysis",

        domain_type="scientific",
        use_case="analysis",

        # Scientific analysis configuration
        embedding_model="text-embedding-3-large",
        chunk_size=1300,  # Good for scientific content
        chunk_overlap=250,
        retrieval_strategy="hybrid",
        similarity_threshold=0.7,
        max_results=12,
        rerank_enabled=False,

        session_id="research-analysis-001",
        user_preferences={
            "extract_methodology": True,
            "identify_findings": True,
            "compare_approaches": True,
            "track_citations": True
        },

        knowledge_tags=["scientific", "research", "methodology", "findings"],
        knowledge_domain="research.papers.com"
    )

    research_analysis_tasks = [
        "Extract and compare research methodologies across papers",
        "Identify key findings and their statistical significance",
        "Analyze experimental design and control variables",
        "Summarize limitations and future research directions",
        "Compare results with previous studies in the field"
    ]

    print("🔬 Starting Research Paper Analysis...")

    for task in research_analysis_tasks:
        print(f"\n📄 Research Analysis: {task}")

        try:
            result = await search_agent.run(
                user_prompt=f"Analyze research papers to: {task}",
                deps=deps
            )

            print(f"🔍 Research Insights: {result.data[:300]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


async def medical_record_analysis():
    """Analyze medical records and clinical documentation."""

    # Configure for medical analysis
    deps = RAGAgentDependencies(
        rag_type="document-analysis",
        project_path="/path/to/medical/records",
        project_name="Medical Record Analysis",

        domain_type="medical",
        use_case="analysis",

        # Medical analysis requires highest precision
        embedding_model="text-embedding-3-large",
        chunk_size=1000,  # Moderate chunks for medical context
        chunk_overlap=200,
        retrieval_strategy="rerank",
        similarity_threshold=0.85,  # Very high precision for medical
        max_results=8,
        rerank_enabled=True,

        session_id="medical-analysis-001",
        user_preferences={
            "extract_symptoms": True,
            "identify_diagnoses": True,
            "track_treatments": True,
            "flag_allergies": True,
            "privacy_compliant": True
        },

        knowledge_tags=["medical", "clinical", "healthcare", "patient-data"],
        knowledge_domain="medical.records.com"
    )

    medical_analysis_tasks = [
        "Extract patient symptoms and presenting complaints",
        "Identify diagnoses and differential diagnoses",
        "Analyze treatment plans and medication regimens",
        "Track patient progress and response to treatment",
        "Identify potential drug interactions or contraindications"
    ]

    print("🏥 Starting Medical Record Analysis...")

    for task in medical_analysis_tasks:
        print(f"\n🩺 Medical Analysis: {task}")

        try:
            result = await search_agent.run(
                user_prompt=f"Analyze medical records to: {task}",
                deps=deps
            )

            print(f"📋 Medical Insights: {result.data[:250]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    return deps


# Example usage patterns
async def main():
    """Example usage of document analysis RAG agent."""

    print("📄 Starting Document Analysis RAG Agent Examples...")

    # Financial document analysis
    print("\n💰 Financial Document Analysis")
    financial_deps = await financial_document_analysis()

    # Legal contract analysis
    print("\n⚖️ Legal Contract Analysis")
    legal_deps = await legal_contract_analysis()

    # Research paper analysis
    print("\n🔬 Research Paper Analysis")
    research_deps = await research_paper_analysis()

    # Medical record analysis
    print("\n🏥 Medical Record Analysis")
    medical_deps = await medical_record_analysis()

    # Analysis capabilities summary
    print("\n📊 Document Analysis Capabilities:")

    analysis_types = [
        ("Financial", financial_deps, "revenue trends, risk factors, cash flow"),
        ("Legal", legal_deps, "contract terms, compliance, liability"),
        ("Research", research_deps, "methodology, findings, citations"),
        ("Medical", medical_deps, "symptoms, diagnoses, treatments")
    ]

    for name, deps, capabilities in analysis_types:
        print(f"\n{name} Analysis:")
        print(f"  Domain: {deps.domain_type}")
        print(f"  Chunk Size: {deps.chunk_size}")
        print(f"  Strategy: {deps.retrieval_strategy}")
        print(f"  Precision: {deps.similarity_threshold}")
        print(f"  Capabilities: {capabilities}")

    # Performance comparison
    print("\n⚡ Analysis Performance Configuration:")
    configs = [financial_deps, legal_deps, research_deps, medical_deps]
    avg_chunk_size = sum(d.chunk_size for d in configs) / len(configs)
    avg_threshold = sum(d.similarity_threshold for d in configs) / len(configs)

    print(f"  Average chunk size: {avg_chunk_size:.0f}")
    print(f"  Average similarity threshold: {avg_threshold:.2f}")
    print(f"  Reranking enabled: {sum(d.rerank_enabled for d in configs)}/{len(configs)} configurations")


if __name__ == "__main__":
    asyncio.run(main())