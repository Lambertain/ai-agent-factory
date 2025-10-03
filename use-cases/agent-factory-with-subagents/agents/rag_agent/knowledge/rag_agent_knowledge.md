# ⚠️ КРИТИЧЕСКИ ВАЖНО: ОБЯЗАТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ В РОЛЬ

**🚨 ПЕРЕД НАЧАЛОМ ЛЮБОЙ РАБОТЫ ТЫ ДОЛЖЕН:**

## 📢 ШАГ 1: ОБЪЯВИТЬ ПЕРЕКЛЮЧЕНИЕ ПОЛЬЗОВАТЕЛЮ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎭 ПЕРЕКЛЮЧАЮСЬ В РОЛЬ СПЕЦИАЛИЗИРОВАННЫЙ АГЕНТ ПО ПОСТРОЕНИЮ И ОПТИМИЗАЦИИ RAG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Моя экспертиза:
• Векторные базы данных и vector search оптимизация
• Embedding models и семантический поиск
• Chunking strategies и preprocessing pipeline
• Hybrid search (semantic + keyword) реализация

🎯 Специализация:
• . **Vector Database Management:**

✅ Готов выполнить задачу в роли эксперта специализированный агент по построению и оптимизации RAG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ЭТО СООБЩЕНИЕ ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ПОКАЗАНО ПОЛЬЗОВАТЕЛЮ!**

## 🚫 ШАГ 2: СОЗДАТЬ МИКРОЗАДАЧИ ЧЕРЕЗ TodoWrite

**СРАЗУ ПОСЛЕ объявления переключения создать 3-7 микрозадач**

## ✅ ШАГ 3: ТОЛЬКО ПОТОМ НАЧИНАТЬ РАБОТУ

---

# 🚨 КРИТИЧЕСКИ ВАЖНО: ЗАПРЕТ ТОКЕН-ЭКОНОМИИ И МАССОВЫХ ОПЕРАЦИЙ

**НИКОГДА НЕ ДЕЛАЙ:**
- ❌ Сокращать файлы "для экономии токенов"
- ❌ Писать "... (остальной код без изменений)"
- ❌ Пропускать комментарии и документацию
- ❌ Обрабатывать файлы "массово" без тщательной проверки
- ❌ Делать задачи "быстро" за счет качества

**ОБЯЗАТЕЛЬНО ДЕЛАЙ:**
- ✅ Пиши ПОЛНЫЙ код с ВСЕМИ комментариями
- ✅ Если файл большой - пиши его ЧАСТЯМИ, но полностью
- ✅ Обрабатывай КАЖДЫЙ файл тщательно и индивидуально
- ✅ Проверяй КАЖДОЕ изменение перед следующим
- ✅ Документируй КАЖДУЮ функцию и класс

**ПРАВИЛО БОЛЬШИХ ФАЙЛОВ:**
Если файл превышает лимит токенов:
1. Разбей на логические секции
2. Пиши каждую секцию полностью
3. Не используй "..." или сокращения
4. Сохраняй ВСЕ комментарии

**КАЧЕСТВО > СКОРОСТЬ**

---

# RAG Agent Knowledge Base

## Системный промпт для RAG Agent

```
Ты специализированный агент по построению и оптимизации RAG (Retrieval-Augmented Generation) систем с фокусом на современные векторные базы данных и embedding модели.

**Твоя экспертиза:**
- Векторные базы данных и vector search оптимизация
- Embedding models и семантический поиск
- Chunking strategies и preprocessing pipeline
- Hybrid search (semantic + keyword) реализация
- RAG evaluation и performance метрики
- Integration с различными LLM провайдерами
- Production-ready RAG архитектуры

**Ключевые области:**

1. **Vector Database Management:**
   - Pinecone, Weaviate, Chroma, Qdrant настройка
   - Index optimization и scaling стратегии
   - Vector storage и retrieval performance
   - Metadata filtering и hybrid queries

2. **Embedding & Retrieval:**
   - Embedding model selection (OpenAI, Sentence-BERT, E5)
   - Contextual retrieval и reranking
   - Multi-modal embeddings (text, image, code)
   - Retrieval quality optimization

3. **Processing Pipeline:**
   - Document chunking strategies
   - Text preprocessing и cleaning
   - Hierarchical chunking и parent-child relationships
   - Real-time document updates

4. **Performance & Evaluation:**
   - Retrieval accuracy metrics (NDCG, MRR, Recall@K)
   - Latency optimization
   - Cost optimization strategies
   - A/B testing frameworks

**Подход к работе:**
1. Анализ требований к RAG системе
2. Выбор оптимальной архитектуры
3. Настройка vector database и embedding pipeline
4. Реализация evaluation framework
5. Production deployment и мониторинг
```

## Vector Database Architectures

### Pinecone Implementation
```python
import pinecone
from pinecone import Pinecone, ServerlessSpec

class PineconeRAG:
    """Production-ready Pinecone RAG implementation."""

    def __init__(self, api_key: str, environment: str):
        self.pc = Pinecone(api_key=api_key)
        self.index_name = "rag-knowledge-base"

    def setup_index(self, dimension: int = 1536):
        """Create optimized Pinecone index."""
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = self.pc.Index(self.index_name)

    def upsert_documents(self, documents: List[Dict]):
        """Batch upsert with metadata."""
        vectors = []
        for doc in documents:
            vectors.append({
                "id": doc["id"],
                "values": doc["embedding"],
                "metadata": {
                    "text": doc["text"],
                    "source": doc["source"],
                    "chunk_id": doc["chunk_id"],
                    "token_count": len(doc["text"].split())
                }
            })

        # Batch upsert for performance
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)

    def semantic_search(self, query_embedding: List[float],
                       top_k: int = 10,
                       metadata_filter: Dict = None) -> List[Dict]:
        """Optimized semantic search with filtering."""
        search_kwargs = {
            "vector": query_embedding,
            "top_k": top_k,
            "include_metadata": True,
            "include_values": False
        }

        if metadata_filter:
            search_kwargs["filter"] = metadata_filter

        results = self.index.query(**search_kwargs)

        return [{
            "id": match["id"],
            "score": match["score"],
            "text": match["metadata"]["text"],
            "source": match["metadata"]["source"]
        } for match in results["matches"]]
```

### Weaviate Implementation
```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

class WeaviateRAG:
    """Advanced Weaviate RAG with hybrid search."""

    def __init__(self, url: str, api_key: str = None):
        auth_config = None
        if api_key:
            auth_config = weaviate.AuthApiKey(api_key=api_key)

        self.client = weaviate.Client(
            url=url,
            auth_client_secret=auth_config,
            additional_headers={
                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
            }
        )

    def create_schema(self):
        """Create optimized schema for RAG."""
        class_obj = {
            "class": "Document",
            "description": "RAG knowledge base documents",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada-002",
                    "modelVersion": "002",
                    "type": "text"
                },
                "generative-openai": {
                    "model": "gpt-4"
                }
            },
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "Document content",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    }
                },
                {
                    "name": "source",
                    "dataType": ["string"],
                    "description": "Document source"
                },
                {
                    "name": "chunk_id",
                    "dataType": ["int"],
                    "description": "Chunk identifier"
                },
                {
                    "name": "metadata",
                    "dataType": ["object"],
                    "description": "Additional metadata"
                }
            ]
        }

        if not self.client.schema.exists("Document"):
            self.client.schema.create_class(class_obj)

    def hybrid_search(self, query: str, top_k: int = 10, alpha: float = 0.5):
        """Hybrid search combining semantic and keyword search."""
        result = (
            self.client.query
            .get("Document", ["content", "source", "chunk_id", "metadata"])
            .with_hybrid(
                query=query,
                alpha=alpha,  # 0 = pure keyword, 1 = pure semantic
                properties=["content"]
            )
            .with_limit(top_k)
            .with_additional(["score", "explainScore"])
            .do()
        )

        return result["data"]["Get"]["Document"]
```

### Chroma Local Implementation
```python
import chromadb
from chromadb.config import Settings

class ChromaRAG:
    """Local Chroma implementation for development."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

    def setup_collection(self, collection_name: str = "rag_knowledge"):
        """Setup collection with embedding function."""
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_name="text-embedding-3-small"
                )
            )
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_name="text-embedding-3-small"
                )
            )

    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents with automatic embedding."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query_documents(self, query: str, n_results: int = 10, where: Dict = None):
        """Query with optional metadata filtering."""
        return self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
```

## Advanced Chunking Strategies

### Intelligent Text Chunking
```python
import tiktoken
from typing import List, Dict
import re

class AdvancedChunker:
    """Advanced text chunking with context preservation."""

    def __init__(self, model_name: str = "gpt-4", chunk_size: int = 1000, overlap: int = 200):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.chunk_size = chunk_size
        self.overlap = overlap

    def semantic_chunking(self, text: str) -> List[Dict]:
        """Semantic-aware chunking preserving sentence boundaries."""
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        current_tokens = 0

        for para in paragraphs:
            para_tokens = len(self.encoding.encode(para))

            # If paragraph fits in current chunk
            if current_tokens + para_tokens <= self.chunk_size:
                current_chunk += para + "\n\n"
                current_tokens += para_tokens
            else:
                # Save current chunk if not empty
                if current_chunk.strip():
                    chunks.append(self._create_chunk_dict(current_chunk.strip(), len(chunks)))

                # Handle oversized paragraphs
                if para_tokens > self.chunk_size:
                    sub_chunks = self._split_large_paragraph(para)
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                    current_tokens = 0
                else:
                    current_chunk = para + "\n\n"
                    current_tokens = para_tokens

        # Add final chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk_dict(current_chunk.strip(), len(chunks)))

        return self._add_overlap(chunks)

    def hierarchical_chunking(self, text: str) -> Dict[str, List[Dict]]:
        """Create hierarchical chunks (document -> sections -> paragraphs)."""
        # Extract sections (assuming markdown headers)
        sections = re.split(r'\n#{1,3}\s+', text)

        hierarchy = {
            "document": [self._create_chunk_dict(text[:500] + "...", 0)],  # Document summary
            "sections": [],
            "chunks": []
        }

        for i, section in enumerate(sections[1:], 1):  # Skip first empty split
            # Section-level chunk
            section_summary = section[:200] + "..." if len(section) > 200 else section
            hierarchy["sections"].append(self._create_chunk_dict(section_summary, i))

            # Detailed chunks from section
            section_chunks = self.semantic_chunking(section)
            for chunk in section_chunks:
                chunk["parent_section"] = i
            hierarchy["chunks"].extend(section_chunks)

        return hierarchy

    def code_aware_chunking(self, code_text: str, language: str = "python") -> List[Dict]:
        """Chunk code while preserving function/class boundaries."""
        if language == "python":
            # Split by function/class definitions
            pattern = r'\n(def |class |async def )'
        elif language == "javascript":
            pattern = r'\n(function |class |const \w+ = |let \w+ = |var \w+ = )'
        else:
            # Fallback to semantic chunking
            return self.semantic_chunking(code_text)

        code_blocks = re.split(pattern, code_text)
        chunks = []

        current_chunk = code_blocks[0] if code_blocks else ""
        current_tokens = len(self.encoding.encode(current_chunk))

        i = 1
        while i < len(code_blocks):
            if i + 1 < len(code_blocks):
                block = code_blocks[i] + code_blocks[i + 1]
                i += 2
            else:
                block = code_blocks[i]
                i += 1

            block_tokens = len(self.encoding.encode(block))

            if current_tokens + block_tokens <= self.chunk_size:
                current_chunk += block
                current_tokens += block_tokens
            else:
                if current_chunk.strip():
                    chunks.append(self._create_chunk_dict(current_chunk, len(chunks), {"type": "code", "language": language}))

                current_chunk = block
                current_tokens = block_tokens

        if current_chunk.strip():
            chunks.append(self._create_chunk_dict(current_chunk, len(chunks), {"type": "code", "language": language}))

        return chunks

    def _create_chunk_dict(self, text: str, chunk_id: int, metadata: Dict = None) -> Dict:
        """Create standardized chunk dictionary."""
        return {
            "chunk_id": chunk_id,
            "text": text,
            "token_count": len(self.encoding.encode(text)),
            "char_count": len(text),
            "metadata": metadata or {}
        }

    def _split_large_paragraph(self, paragraph: str) -> List[Dict]:
        """Split large paragraphs by sentences."""
        sentences = re.split(r'[.!?]+\s+', paragraph)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence_tokens = len(self.encoding.encode(sentence))
            current_tokens = len(self.encoding.encode(current_chunk))

            if current_tokens + sentence_tokens <= self.chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk.strip():
                    chunks.append(self._create_chunk_dict(current_chunk.strip(), len(chunks)))
                current_chunk = sentence + ". "

        if current_chunk.strip():
            chunks.append(self._create_chunk_dict(current_chunk.strip(), len(chunks)))

        return chunks

    def _add_overlap(self, chunks: List[Dict]) -> List[Dict]:
        """Add overlap between consecutive chunks."""
        if len(chunks) <= 1:
            return chunks

        overlapped_chunks = [chunks[0]]

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i-1]
            current_chunk = chunks[i]

            # Get last few sentences from previous chunk
            prev_text = prev_chunk["text"]
            sentences = re.split(r'[.!?]+\s+', prev_text)
            overlap_text = ". ".join(sentences[-2:]) + ". " if len(sentences) >= 2 else ""

            # Prepend overlap to current chunk
            overlapped_text = overlap_text + current_chunk["text"]

            overlapped_chunk = current_chunk.copy()
            overlapped_chunk["text"] = overlapped_text
            overlapped_chunk["token_count"] = len(self.encoding.encode(overlapped_text))
            overlapped_chunk["char_count"] = len(overlapped_text)

            overlapped_chunks.append(overlapped_chunk)

        return overlapped_chunks
```

## Embedding Models & Strategies

### Multi-Model Embedding Pipeline
```python
from sentence_transformers import SentenceTransformer
import openai
from typing import List, Dict, Union

class EmbeddingPipeline:
    """Multi-model embedding pipeline with fallbacks."""

    def __init__(self):
        self.models = {
            "openai": {
                "model": "text-embedding-3-large",
                "dimension": 3072,
                "cost_per_token": 0.00013
            },
            "sentence_bert": {
                "model": SentenceTransformer('all-MiniLM-L6-v2'),
                "dimension": 384,
                "cost_per_token": 0.0  # Free
            },
            "e5_large": {
                "model": SentenceTransformer('intfloat/e5-large-v2'),
                "dimension": 1024,
                "cost_per_token": 0.0  # Free
            }
        }

    def get_embeddings(self, texts: List[str], model_name: str = "openai") -> List[List[float]]:
        """Get embeddings with specified model."""
        if model_name == "openai":
            return self._openai_embeddings(texts)
        elif model_name in ["sentence_bert", "e5_large"]:
            return self._local_embeddings(texts, model_name)
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def _openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get OpenAI embeddings with batching."""
        batch_size = 100  # OpenAI limit
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = openai.embeddings.create(
                model=self.models["openai"]["model"],
                input=batch
            )

            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def _local_embeddings(self, texts: List[str], model_name: str) -> List[List[float]]:
        """Get embeddings from local models."""
        model = self.models[model_name]["model"]

        # E5 models need special prefixes
        if model_name == "e5_large":
            texts = [f"passage: {text}" for text in texts]

        embeddings = model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

    def hybrid_embeddings(self, texts: List[str]) -> Dict[str, List[List[float]]]:
        """Generate embeddings with multiple models for ensemble."""
        return {
            "openai": self.get_embeddings(texts, "openai"),
            "sentence_bert": self.get_embeddings(texts, "sentence_bert"),
            "e5_large": self.get_embeddings(texts, "e5_large")
        }

    def cost_analysis(self, text_count: int, avg_tokens: int = 100) -> Dict[str, float]:
        """Calculate embedding costs for different models."""
        total_tokens = text_count * avg_tokens

        costs = {}
        for model_name, config in self.models.items():
            cost = total_tokens * config["cost_per_token"]
            costs[model_name] = {
                "total_cost": cost,
                "cost_per_1k_texts": (cost / text_count) * 1000 if text_count > 0 else 0,
                "dimension": config["dimension"]
            }

        return costs
```

## RAG Evaluation Framework

### Comprehensive RAG Metrics
```python
import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import ragas
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

class RAGEvaluator:
    """Comprehensive RAG system evaluation."""

    def __init__(self):
        self.metrics_history = []

    def evaluate_retrieval(self, queries: List[str],
                          retrieved_docs: List[List[str]],
                          ground_truth: List[List[str]]) -> Dict[str, float]:
        """Evaluate retrieval quality."""
        metrics = {
            "recall_at_k": [],
            "precision_at_k": [],
            "mrr": [],  # Mean Reciprocal Rank
            "ndcg": []  # Normalized Discounted Cumulative Gain
        }

        for query, retrieved, truth in zip(queries, retrieved_docs, ground_truth):
            # Recall@K
            relevant_retrieved = len(set(retrieved) & set(truth))
            recall = relevant_retrieved / len(truth) if truth else 0
            metrics["recall_at_k"].append(recall)

            # Precision@K
            precision = relevant_retrieved / len(retrieved) if retrieved else 0
            metrics["precision_at_k"].append(precision)

            # MRR
            rr = 0
            for i, doc in enumerate(retrieved):
                if doc in truth:
                    rr = 1 / (i + 1)
                    break
            metrics["mrr"].append(rr)

            # NDCG (simplified)
            dcg = sum(1 / np.log2(i + 2) for i, doc in enumerate(retrieved) if doc in truth)
            idcg = sum(1 / np.log2(i + 2) for i in range(min(len(truth), len(retrieved))))
            ndcg = dcg / idcg if idcg > 0 else 0
            metrics["ndcg"].append(ndcg)

        return {k: np.mean(v) for k, v in metrics.items()}

    def evaluate_generation(self, questions: List[str],
                           contexts: List[List[str]],
                           answers: List[str],
                           ground_truth: List[str]) -> Dict[str, float]:
        """Evaluate generation quality using RAGAS."""
        from datasets import Dataset

        # Prepare dataset for RAGAS
        data = {
            "question": questions,
            "contexts": contexts,
            "answer": answers,
            "ground_truths": [[gt] for gt in ground_truth]
        }
        dataset = Dataset.from_dict(data)

        # Evaluate with RAGAS metrics
        result = ragas.evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
        )

        return dict(result)

    def latency_analysis(self, retrieval_times: List[float],
                        generation_times: List[float]) -> Dict[str, float]:
        """Analyze system latency."""
        total_times = [r + g for r, g in zip(retrieval_times, generation_times)]

        return {
            "avg_retrieval_time": np.mean(retrieval_times),
            "p95_retrieval_time": np.percentile(retrieval_times, 95),
            "avg_generation_time": np.mean(generation_times),
            "p95_generation_time": np.percentile(generation_times, 95),
            "avg_total_time": np.mean(total_times),
            "p95_total_time": np.percentile(total_times, 95)
        }

    def cost_analysis(self, embedding_calls: int,
                     llm_input_tokens: int,
                     llm_output_tokens: int) -> Dict[str, float]:
        """Calculate operational costs."""
        costs = {
            "embedding_cost": embedding_calls * 0.00013,  # OpenAI text-embedding-3-large
            "llm_input_cost": llm_input_tokens * 0.03 / 1000,  # GPT-4 input
            "llm_output_cost": llm_output_tokens * 0.06 / 1000,  # GPT-4 output
        }

        costs["total_cost"] = sum(costs.values())
        costs["cost_per_query"] = costs["total_cost"] / max(1, embedding_calls)

        return costs
```

## Production RAG Architecture

### Scalable RAG System
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import List, Optional
import redis
import hashlib

class RAGRequest(BaseModel):
    query: str
    top_k: int = 10
    use_reranking: bool = True
    filters: Optional[Dict] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict]
    retrieval_score: float
    generation_time: float

class ProductionRAG:
    """Production-ready RAG system with caching and monitoring."""

    def __init__(self):
        self.vector_db = None  # Initialize your vector DB
        self.embedder = EmbeddingPipeline()
        self.llm = None  # Initialize your LLM
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.reranker = None  # Initialize reranker if needed

    async def query(self, request: RAGRequest) -> RAGResponse:
        """Main RAG query endpoint."""
        start_time = time.time()

        # Check cache first
        cache_key = self._get_cache_key(request.query, request.top_k)
        cached_result = self.cache.get(cache_key)

        if cached_result:
            return RAGResponse.parse_raw(cached_result)

        # Get embeddings
        query_embedding = self.embedder.get_embeddings([request.query])[0]

        # Retrieve documents
        retrieved_docs = await self._retrieve_documents(
            query_embedding,
            request.top_k,
            request.filters
        )

        # Rerank if requested
        if request.use_reranking and self.reranker:
            retrieved_docs = await self._rerank_documents(
                request.query,
                retrieved_docs
            )

        # Generate answer
        answer = await self._generate_answer(request.query, retrieved_docs)

        # Calculate metrics
        generation_time = time.time() - start_time
        retrieval_score = np.mean([doc["score"] for doc in retrieved_docs])

        response = RAGResponse(
            answer=answer,
            sources=retrieved_docs,
            retrieval_score=retrieval_score,
            generation_time=generation_time
        )

        # Cache result
        self.cache.setex(
            cache_key,
            3600,  # 1 hour TTL
            response.json()
        )

        return response

    async def _retrieve_documents(self, embedding: List[float],
                                 top_k: int,
                                 filters: Optional[Dict]) -> List[Dict]:
        """Retrieve relevant documents."""
        # Implement vector search logic
        pass

    async def _rerank_documents(self, query: str,
                               documents: List[Dict]) -> List[Dict]:
        """Rerank documents using cross-encoder."""
        # Implement reranking logic
        pass

    async def _generate_answer(self, query: str,
                              context_docs: List[Dict]) -> str:
        """Generate answer using LLM."""
        context = "\n\n".join([doc["text"] for doc in context_docs])

        prompt = f"""
        Context: {context}

        Question: {query}

        Please provide a comprehensive answer based on the context provided.
        """

        # Implement LLM generation logic
        pass

    def _get_cache_key(self, query: str, top_k: int) -> str:
        """Generate cache key for query."""
        key_string = f"{query}:{top_k}"
        return hashlib.md5(key_string.encode()).hexdigest()

# FastAPI app
app = FastAPI(title="Production RAG API")
rag_system = ProductionRAG()

@app.post("/query", response_model=RAGResponse)
async def query_rag(request: RAGRequest):
    """Query the RAG system."""
    try:
        return await rag_system.query(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

## Integration Patterns

### Pydantic AI RAG Integration
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

class RAGDependencies:
    """Dependencies for RAG-enabled agent."""

    def __init__(self, vector_db, embedding_model):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.cache = {}

# Create RAG-enabled agent
rag_agent = Agent(
    "gpt-4",
    deps_type=RAGDependencies,
    system_prompt="You are a helpful assistant with access to a knowledge base."
)

@rag_agent.tool
async def search_knowledge_base(ctx: RunContext[RAGDependencies],
                               query: str,
                               top_k: int = 5) -> str:
    """Search the vector database for relevant information."""
    # Get query embedding
    query_embedding = ctx.deps.embedding_model.encode([query])[0]

    # Search vector database
    results = ctx.deps.vector_db.search(
        vector=query_embedding,
        top_k=top_k
    )

    # Format results
    context = "\n\n".join([
        f"Source: {result['metadata']['source']}\n{result['text']}"
        for result in results
    ])

    return f"Knowledge base search results:\n\n{context}"

@rag_agent.tool
async def get_document_summary(ctx: RunContext[RAGDependencies],
                              document_id: str) -> str:
    """Get summary of a specific document."""
    doc = ctx.deps.vector_db.get_document(document_id)

    if not doc:
        return "Document not found."

    return f"Document: {doc['title']}\nSummary: {doc['summary']}"

# Usage example
async def main():
    deps = RAGDependencies(
        vector_db=your_vector_db,
        embedding_model=your_embedding_model
    )

    result = await rag_agent.run(
        "What are the best practices for RAG implementation?",
        deps=deps
    )

    print(result.data)
```

## Performance Optimization Checklist

### Vector Database Optimization
- [ ] Index optimization (HNSW parameters, quantization)
- [ ] Batch operations for bulk updates
- [ ] Metadata filtering strategies
- [ ] Connection pooling и query optimization
- [ ] Monitoring query latency и throughput

### Embedding Optimization
- [ ] Model selection based on use case
- [ ] Batch processing для multiple texts
- [ ] Caching frequently used embeddings
- [ ] Dimensionality reduction если нужно
- [ ] Cost optimization (local vs API models)

### Production Readiness
- [ ] Horizontal scaling architecture
- [ ] Caching layer (Redis/Memcached)
- [ ] Monitoring и alerting
- [ ] Error handling и graceful degradation
- [ ] Security (authentication, rate limiting)

### RAG Quality
- [ ] Comprehensive evaluation framework
- [ ] A/B testing для different configurations
- [ ] Feedback loop для continuous improvement
- [ ] Version control для embeddings и indexes
- [ ] Data quality monitoring