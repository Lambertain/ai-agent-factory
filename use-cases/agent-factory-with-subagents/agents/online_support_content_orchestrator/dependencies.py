"""
Dependencies для Psychology Content Orchestrator Agent
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
from dataclasses import dataclass

@dataclass
class RAGConfig:
    """Конфигурация для RAG поиска психологических знаний"""
    search_tags: List[str]
    content_type: str
    target_domain: str
    expertise_level: str
    match_count: int = 5
    archon_url: str = "http://localhost:3737"

class PsychologyKnowledge(BaseModel):
    """Модель психологических знаний"""
    content: str
    domain: str
    evidence_level: str
    therapeutic_approach: str
    metadata: Dict[str, Any]

class ContentCreationRequest(BaseModel):
    """Запрос на создание контента"""
    content_type: str
    target_audience: str
    psychological_domain: str
    objectives: List[str]
    constraints: Optional[List[str]] = None
    cultural_context: Optional[str] = None

def get_rag_client() -> httpx.AsyncClient:
    """Получить клиент для RAG поиска"""
    return httpx.AsyncClient(timeout=30.0)

async def search_psychology_knowledge(
    query: str,
    domain: str = None,
    tags: List[str] = None,
    match_count: int = 5
) -> List[PsychologyKnowledge]:
    """
    Поиск психологических знаний через Archon RAG

    Args:
        query: Поисковый запрос
        domain: Психологический домен
        tags: Теги для фильтрации
        match_count: Количество результатов

    Returns:
        Список найденных знаний
    """
    async with get_rag_client() as client:
        try:
            search_tags = tags or ["psychology", "therapy"]
            if domain:
                search_tags.append(domain)

            response = await client.post(
                "http://localhost:3737/rag/search-knowledge-base",
                json={
                    "query": query,
                    "source_domain": None,  # Поиск по всем источникам
                    "match_count": match_count
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    results = []
                    for result in data.get("results", []):
                        knowledge = PsychologyKnowledge(
                            content=result.get("content", ""),
                            domain=domain or "general",
                            evidence_level="research-based",
                            therapeutic_approach="integrative",
                            metadata=result.get("metadata", {})
                        )
                        results.append(knowledge)
                    return results

            return []

        except Exception as e:
            print(f"Ошибка поиска психологических знаний: {e}")
            return []