"""
Dependencies for Psychology Content Architect Agent
Зависимости для агента создания психологических тестов
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ContentArchitectDependencies:
    """
    Зависимости для Psychology Content Architect Agent
    Поддерживает 4-уровневую методологию PatternShift
    """
    # Основные параметры
    test_domain: str = "mental_health"  # mental_health, personality, cognitive, emotional
    test_type: str = "diagnostic"  # diagnostic, screening, assessment, monitoring
    target_language: str = "ukrainian"  # ukrainian, russian, english
    methodology_level: str = "patternshift_full"  # patternshift_full, simplified, custom
    
    # Настройки теста
    test_specification: Dict[str, Any] = field(default_factory=dict)
    
    # VAK адаптации (визуал/аудиал/кинестетик)
    vak_adaptations: Dict[str, Dict] = field(default_factory=lambda: {
        "visual": {
            "focus_words": ["побачиш", "уяви", "картина", "яскраво"],
            "metaphors": ["світло", "кольори", "образи"]
        },
        "auditory": {
            "focus_words": ["почуєш", "звучить", "мелодія", "голос"],
            "metaphors": ["ритм", "гармонія", "тиша"]
        },
        "kinesthetic": {
            "focus_words": ["відчуваєш", "доторкнутися", "тепло", "важко"],
            "metaphors": ["тепло", "легко", "сила"]
        }
    })
    
    # Адаптация по возрасту
    age_adaptations: Dict[str, Dict] = field(default_factory=lambda: {
        "youth": {  # 18-25
            "tone": "informal",
            "slang": ["йо", "челлендж", "топово", "кайф"],
            "references": ["social_media", "gaming", "trends"]
        },
        "friendly": {  # 26-35
            "tone": "conversational",
            "slang": ["круто", "давай розберемося"],
            "references": ["work_life", "relationships", "goals"]
        },
        "professional": {  # 36+
            "tone": "respectful",
            "slang": ["цікаво", "варто зауважити"],
            "references": ["experience", "wisdom", "stability"]
        }
    })
    
    # Клинические референсы
    clinical_references: Dict[str, str] = field(default_factory=lambda: {
        "depression": "PHQ-9",
        "anxiety": "GAD-7",
        "stress": "PSS-10",
        "trauma": "PCL-5",
        "personality": "Big Five"
    })
    
    # RAG конфигурация
    knowledge_tags: List[str] = field(default_factory=lambda: [
        "psychology-content",
        "patternshift",
        "test-creation"
    ])
    knowledge_domain: Optional[str] = None
    archon_project_id: str = "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a"  # AI Agent Factory
    
    # Имя агента для RAG
    agent_name: str = "psychology_content_architect"
    
    # Межагентное взаимодействие
    enable_task_delegation: bool = True
    delegation_threshold: str = "medium"
    
    def __post_init__(self):
        """Инициализация дополнительных параметров"""
        # Добавляем теги на основе домена
        if self.test_domain and self.test_domain not in self.knowledge_tags:
            self.knowledge_tags.append(self.test_domain)
        
        # Устанавливаем domain для RAG
        if not self.knowledge_domain:
            self.knowledge_domain = f"{self.test_domain}.patternshift.ai"
    
    def get_vak_adaptation(self, vak_type: str) -> Dict[str, Any]:
        """Получить адаптацию для конкретного VAK типа"""
        return self.vak_adaptations.get(vak_type, self.vak_adaptations["visual"])
    
    def get_age_adaptation(self, age: int) -> Dict[str, Any]:
        """Получить адаптацию по возрасту"""
        if age <= 25:
            return self.age_adaptations["youth"]
        elif age <= 35:
            return self.age_adaptations["friendly"]
        else:
            return self.age_adaptations["professional"]
    
    def get_clinical_reference(self, test_topic: str) -> str:
        """Получить клиническую референсную шкалу"""
        return self.clinical_references.get(test_topic.lower(), "custom_scale")
    
    def should_delegate(self, task_keywords: List[str]) -> Optional[str]:
        """
        Определить нужно ли делегировать задачу и кому
        """
        # Матрица компетенций для делегирования
        delegation_map = {
            "transformation_plan": "psychology_transformation_planner",
            "test_generation": "psychology_test_generator",
            "quality_check": "psychology_quality_guardian",
            "orchestration": "psychology_content_orchestrator"
        }
        
        for keyword_group, agent in delegation_map.items():
            if any(kw in keyword_group for kw in task_keywords):
                return agent
        
        return None

def get_content_config() -> ContentArchitectDependencies:
    """
    Получить конфигурацию зависимостей из переменных окружения
    """
    return ContentArchitectDependencies(
        test_domain=os.getenv("TEST_DOMAIN", "mental_health"),
        test_type=os.getenv("TEST_TYPE", "diagnostic"),
        target_language=os.getenv("TARGET_LANGUAGE", "ukrainian"),
        methodology_level=os.getenv("METHODOLOGY_LEVEL", "patternshift_full"),
        archon_project_id=os.getenv("ARCHON_PROJECT_ID", "c75ef8e3-6f4d-4da2-9e81-8d38d04a341a")
    )