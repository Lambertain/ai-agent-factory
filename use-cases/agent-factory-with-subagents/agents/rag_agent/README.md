# RAG Agent

**Universal Retrieval Augmented Generation Agent for intelligent information search and analysis across any domain**

The RAG Agent specializes in semantic search, question-answering, document analysis, knowledge management, and conversational AI with configurable retrieval strategies and domain-specific optimizations.

## 🎯 Purpose

The agent provides intelligent information retrieval with focus on:
- **Semantic Search**: Vector-based similarity search across documents
- **Question Answering**: Conversational Q&A with context awareness
- **Document Analysis**: Information extraction and insight generation
- **Knowledge Management**: Enterprise knowledge base and search
- **Chat Assistant**: Conversational AI with retrieval capabilities

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
cp .env.example .env
# Configure LLM API keys and embedding settings in .env
```

### CLI Usage
```bash
# Semantic search across technical documentation
python -m rag_agent.cli search /path/to/docs --rag-type semantic-search --domain technical

# Q&A system for customer support
python -m rag_agent.cli qa /path/to/support/docs --rag-type qa-system --use-case qa

# Document analysis for financial reports
python -m rag_agent.cli analyze /path/to/reports --rag-type document-analysis --domain financial

# Knowledge base search for enterprise content
python -m rag_agent.cli knowledge /path/to/kb --rag-type knowledge-base --domain general

# Chat assistant with conversational memory
python -m rag_agent.cli chat /path/to/knowledge --rag-type chat-assistant --use-case chat
```

### Python API Usage
```python
import asyncio
from rag_agent import search_agent
from rag_agent.dependencies import RAGAgentDependencies

async def main():
    # Configure for your use case
    deps = RAGAgentDependencies(
        rag_type="semantic-search",  # or qa-system, document-analysis, knowledge-base, chat-assistant
        project_path="/path/to/documents",
        domain_type="technical",  # or general, medical, legal, financial, scientific
        use_case="search",  # or qa, analysis, chat, recommendation, summarization

        # Embedding configuration
        embedding_model="text-embedding-3-small",
        chunk_size=1000,
        retrieval_strategy="similarity"
    )

    result = await search_agent.run(
        user_prompt="How to implement authentication in REST API?",
        deps=deps
    )
    print(f"Search result: {result.data}")

asyncio.run(main())
```

## 🛠️ RAG Types & Configurations

### 1. Semantic Search (`semantic-search`)
- **Focus Areas**: Document retrieval, similarity search, information discovery
- **Use Cases**: Technical documentation search, research paper discovery
- **Optimization**: Large chunk sizes, similarity-based retrieval
- **Example**: [semantic_search.py](examples/semantic_search.py)

### 2. Question Answering (`qa-system`)
- **Focus Areas**: Conversational Q&A, context-aware responses
- **Use Cases**: Customer support, educational tutoring, technical Q&A
- **Optimization**: MMR retrieval, conversation memory, smaller chunks
- **Example**: [qa_system.py](examples/qa_system.py)

### 3. Document Analysis (`document-analysis`)
- **Focus Areas**: Information extraction, insight generation, comprehensive analysis
- **Use Cases**: Financial analysis, legal document review, research synthesis
- **Optimization**: Hybrid retrieval, larger chunks, reranking enabled
- **Example**: [document_analysis.py](examples/document_analysis.py)

### 4. Knowledge Base (`knowledge-base`)
- **Focus Areas**: Enterprise search, organizational memory, information management
- **Use Cases**: Company knowledge base, technical documentation, compliance docs
- **Optimization**: Reranking strategy, balanced precision, structured search
- **Example**: [knowledge_base.py](examples/knowledge_base.py)

### 5. Chat Assistant (`chat-assistant`)
- **Focus Areas**: Conversational AI, interactive assistance, context retention
- **Use Cases**: Personal assistant, customer service chat, educational tutor
- **Optimization**: MMR diversity, conversation history, quick responses
- **Example**: [chat_assistant.py](examples/chat_assistant.py)

## 📋 Domain Types & Configurations

### 1. General Domain (`general`)
- **Content**: Mixed content, customer-facing information
- **Optimization**: Balanced settings, cost-effective models
- **Chunk Size**: 800-1000
- **Similarity Threshold**: 0.7-0.8

### 2. Technical Domain (`technical`)
- **Content**: API docs, code examples, technical specifications
- **Optimization**: Large embedding model, higher precision
- **Chunk Size**: 1000-1200
- **Similarity Threshold**: 0.8+

### 3. Medical Domain (`medical`)
- **Content**: Medical literature, clinical documentation
- **Optimization**: Highest precision, reranking enabled
- **Chunk Size**: 1000
- **Similarity Threshold**: 0.85+

### 4. Legal Domain (`legal`)
- **Content**: Contracts, regulations, legal documents
- **Optimization**: Maximum precision, large chunks, reranking
- **Chunk Size**: 1500
- **Similarity Threshold**: 0.9+

### 5. Financial Domain (`financial`)
- **Content**: Financial reports, market analysis
- **Optimization**: High precision, reranking, structured analysis
- **Chunk Size**: 1000-1200
- **Similarity Threshold**: 0.8+

### 6. Scientific Domain (`scientific`)
- **Content**: Research papers, academic content
- **Optimization**: Large model, scientific terminology handling
- **Chunk Size**: 1300
- **Similarity Threshold**: 0.75

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# LLM Configuration
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=https://api.provider.com/v1
LLM_MODEL=qwen2.5-coder-32b-instruct

# Embedding Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# Vector Database
VECTOR_DB_URL=postgresql://user:pass@localhost/vectordb
VECTOR_DB_COLLECTION=rag_embeddings

# Archon Integration
ARCHON_URL=http://localhost:3737
ARCHON_PROJECT_ID=your_project_id

# Performance
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_RESULTS=10
SIMILARITY_THRESHOLD=0.7
```

### Custom RAG Configuration
```python
# Custom configuration example
deps = RAGAgentDependencies(
    # Universal configuration
    rag_type="semantic-search",
    domain_type="technical",
    use_case="search",

    # Embedding settings
    embedding_model="text-embedding-3-large",
    embedding_dimension=3072,

    # Chunking strategy
    chunk_size=1200,
    chunk_overlap=200,

    # Retrieval configuration
    retrieval_strategy="hybrid",
    similarity_threshold=0.8,
    max_results=8,
    rerank_enabled=True,

    # Knowledge integration
    knowledge_tags=["technical-docs", "api-reference"],
    knowledge_domain="docs.technical.com",
    archon_project_id="tech-project-id"
)
```

## 🏗️ Architecture

```
rag_agent/
├── agent.py                    # Main RAG agent implementation
├── dependencies.py             # Universal RAG dependencies
├── tools.py                    # Search and retrieval tools
├── prompts.py                  # Domain-adaptive prompts
├── settings.py                 # Configuration management
├── providers.py                # LLM providers for analysis
├── examples/                   # Configuration examples
│   ├── semantic_search.py      # Semantic search configurations
│   ├── qa_system.py            # Q&A system configurations
│   ├── document_analysis.py    # Document analysis configurations
│   ├── knowledge_base.py       # Knowledge base configurations
│   └── chat_assistant.py       # Chat assistant configurations
├── knowledge/                  # RAG knowledge base
│   └── rag_agent_knowledge.md  # Agent expertise knowledge
├── tests/                      # Testing framework
└── README.md                   # This documentation
```

## 🔄 RAG Workflow

### 1. **Document Ingestion**
- Document chunking with overlap
- Embedding generation
- Vector database storage
- Metadata extraction

### 2. **Query Processing**
- Query understanding and expansion
- Embedding generation for search
- Intent classification

### 3. **Retrieval Strategy**
- **Similarity**: Basic vector similarity search
- **MMR**: Maximum marginal relevance for diversity
- **Hybrid**: Combination of semantic and keyword search
- **Rerank**: Re-scoring results for better precision

### 4. **Context Generation**
- Retrieved content synthesis
- Context window optimization
- Relevance scoring and filtering

### 5. **Response Generation**
- LLM-based response synthesis
- Context-aware answer generation
- Citation and source attribution

## 📊 Performance Optimization

### Embedding Models
- **text-embedding-3-small**: Cost-effective for general content
- **text-embedding-3-large**: Better performance for specialized domains
- **Domain-specific**: Automatic model selection based on domain type

### Chunk Size Optimization
```python
# Recommended chunk sizes by RAG type
chunk_sizes = {
    "semantic-search": 1000,    # Balanced for search
    "qa-system": 800,           # Smaller for focused answers
    "document-analysis": 1500,  # Larger for comprehensive analysis
    "knowledge-base": 1200,     # Good for enterprise content
    "chat-assistant": 800       # Quick conversational responses
}
```

### Retrieval Strategy Selection
```python
# Strategy recommendations by use case
strategies = {
    "search": "similarity",     # Fast and effective
    "qa": "mmr",               # Diverse answers
    "analysis": "hybrid",      # Comprehensive coverage
    "chat": "mmr",             # Conversational diversity
}
```

## 🧪 Testing

```bash
# Run RAG tests
pytest tests/ -v

# Test specific RAG configurations
pytest tests/test_semantic_search.py
pytest tests/test_qa_system.py

# Integration testing with vector database
pytest tests/test_vector_integration.py

# Performance benchmarking
pytest tests/test_performance.py --benchmark
```

## 📚 Knowledge Base Integration

The agent leverages Archon Knowledge Base for:
- **RAG Patterns**: Retrieval and generation strategies
- **Domain Knowledge**: Specialized terminology and concepts
- **Configuration Examples**: Proven RAG configurations
- **Performance Tuning**: Optimization techniques and best practices

### Knowledge Base Tags
- `rag-agent`, `retrieval-augmented-generation`, `semantic-search`
- `qa-system`, `document-analysis`, `knowledge-base`, `chat-assistant`
- `embedding-models`, `vector-search`, `chunking-strategies`

## 🔗 Universal Integration

The RAG Agent adapts to any information retrieval context:
- **Document Types**: PDF, Text, HTML, Markdown, JSON
- **Vector Databases**: PostgreSQL+pgvector, Pinecone, Weaviate, Chroma
- **Embedding Providers**: OpenAI, Cohere, HuggingFace, Local models
- **LLM Providers**: OpenAI, Anthropic, Cohere, Local models
- **Search Backends**: Elasticsearch, Solr, vector databases

## 📈 Advanced Features

### Conversation Memory
- Query history tracking
- Context-aware responses
- Session state management
- User preference learning

### Intelligent Routing
- Query intent classification
- Optimal strategy selection
- Domain-specific processing
- Performance optimization

### Real-time Learning
- Feedback incorporation
- Result quality improvement
- User interaction analysis
- Adaptive configuration

## 🤝 Integration with Other Agents

RAG Agent collaborates with:
- **Knowledge Management Agent**: Content organization and curation
- **Data Processing Agent**: Document preparation and preprocessing
- **Analytics Agent**: Search performance analysis and optimization
- **Security Agent**: Access control and data privacy compliance

---

**Version**: 2.0.0
**License**: MIT
**Support**: Create issues in the repository for RAG-related questions