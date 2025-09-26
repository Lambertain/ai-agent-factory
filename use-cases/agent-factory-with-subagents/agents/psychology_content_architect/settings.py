"""
Settings for Psychology Content Architect Agent
Настройки для агента создания психологических тестов
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class ContentArchitectSettings(BaseSettings):
    """
    Настройки приложения для Psychology Content Architect
    """
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Основные параметры LLM
    llm_provider: str = Field(default="openai", description="Провайдер LLM")
    llm_api_key: str = Field(..., description="API-ключ провайдера")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="Название модели")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Базовый URL API"
    )
    
    # Параметры тестов
    test_domain: str = Field(default="mental_health", description="Домен теста")
    test_type: str = Field(default="diagnostic", description="Тип теста")
    target_language: str = Field(default="ukrainian", description="Целевой язык")
    question_count: int = Field(default=16, description="Количество вопросов")
    scoring_system: str = Field(default="3_point_scale", description="Система оценки")
    result_levels: int = Field(default=4, description="Количество уровней результата")
    
    # Методология PatternShift
    methodology_level: str = Field(default="patternshift_full", description="Уровень методологии")
    enable_vak_adaptation: bool = Field(default=True, description="Включить VAK адаптацию")
    enable_age_adaptation: bool = Field(default=True, description="Включить возрастную адаптацию")
    enable_language_adaptation: bool = Field(default=True, description="Включить языковую адаптацию")
    
    # Клинические параметры
    clinical_accuracy_required: bool = Field(default=True, description="Требуется клиническая точность")
    enable_urgent_marking: bool = Field(default=True, description="Маркировать критические состояния")
    
    # Archon интеграция
    archon_project_id: str = Field(
        default="c75ef8e3-6f4d-4da2-9e81-8d38d04a341a",
        description="ID проекта Archon"
    )
    enable_rag_search: bool = Field(default=True, description="Использовать RAG поиск")
    rag_match_count: int = Field(default=5, description="Количество результатов RAG")
    
    def get_language_tone(self) -> str:
        """Получить языковой тон на основе целевого языка"""
        tone_map = {
            "ukrainian": "conversational_empathetic",
            "russian": "literary_supportive",
            "english": "clear_professional"
        }
        return tone_map.get(self.target_language, "neutral")
    
    def get_clinical_references(self, topic: str) -> str:
        """Получить клинические референсы для темы"""
        clinical_map = {
            "depression": "PHQ-9, Beck Depression Inventory",
            "anxiety": "GAD-7, Hamilton Anxiety Scale",
            "stress": "PSS-10, DASS-21",
            "trauma": "PCL-5, IES-R",
            "personality": "Big Five, MMPI-2",
            "cognitive": "MMSE, MoCA",
            "emotional": "EQ-i 2.0, Bar-On EQ"
        }
        return clinical_map.get(topic.lower(), "Custom Clinical Assessment")
    
    def get_vak_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Получить шаблоны VAK адаптации"""
        if not self.enable_vak_adaptation:
            return {}
        
        if self.target_language == "ukrainian":
            return {
                "visual": {
                    "keywords": ["побачиш", "яскраво", "образ", "картина"],
                    "metaphors": ["світло", "кольори", "тіні"]
                },
                "auditory": {
                    "keywords": ["почуєш", "голос", "мелодія", "ритм"],
                    "metaphors": ["музика", "тиша", "ехо"]
                },
                "kinesthetic": {
                    "keywords": ["відчуваєш", "тепло", "легко", "важко"],
                    "metaphors": ["дотик", "рух", "температура"]
                }
            }
        else:
            # Английские аналоги
            return {
                "visual": {
                    "keywords": ["see", "bright", "picture", "image"],
                    "metaphors": ["light", "colors", "shadows"]
                },
                "auditory": {
                    "keywords": ["hear", "voice", "melody", "rhythm"],
                    "metaphors": ["music", "silence", "echo"]
                },
                "kinesthetic": {
                    "keywords": ["feel", "warm", "light", "heavy"],
                    "metaphors": ["touch", "movement", "temperature"]
                }
            }
    
    def get_age_adaptations(self) -> Dict[str, Dict[str, Any]]:
        """Получить возрастные адаптации"""
        if not self.enable_age_adaptation:
            return {}
        
        if self.target_language == "ukrainian":
            return {
                "youth": {  # 18-25
                    "tone": "informal",
                    "slang": ["челлендж", "топово", "кайф"],
                    "references": ["social_media", "trends", "gaming"]
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
            }
        else:
            return {
                "youth": {
                    "tone": "informal",
                    "slang": ["cool", "awesome", "vibe"],
                    "references": ["social_media", "trends", "gaming"]
                },
                "friendly": {
                    "tone": "conversational",
                    "slang": ["great", "let's figure it out"],
                    "references": ["work_life", "relationships", "goals"]
                },
                "professional": {
                    "tone": "respectful",
                    "slang": ["interesting", "worth noting"],
                    "references": ["experience", "wisdom", "stability"]
                }
            }
    
    def get_scoring_templates(self) -> Dict[str, Any]:
        """Получить шаблоны систем оценки"""
        scoring_templates = {
            "3_point_scale": {
                "values": [1, 2, 3],
                "labels": ["николи", "иноди", "часто"] if self.target_language == "ukrainian" else ["never", "sometimes", "often"],
                "max_score": self.question_count * 3
            },
            "likert_5": {
                "values": [1, 2, 3, 4, 5],
                "labels": ["повністю не згоден", "не згоден", "нейтрально", "згоден", "повністю згоден"] if self.target_language == "ukrainian" else ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"],
                "max_score": self.question_count * 5
            },
            "binary": {
                "values": [0, 1],
                "labels": ["ні", "так"] if self.target_language == "ukrainian" else ["no", "yes"],
                "max_score": self.question_count
            }
        }
        return scoring_templates.get(self.scoring_system, scoring_templates["3_point_scale"])
    
    def get_result_level_templates(self) -> List[Dict[str, Any]]:
        """Получить шаблоны уровней результатов"""
        max_score = self.get_scoring_templates()["max_score"]
        
        if self.result_levels == 2:
            return [
                {
                    "level": "low",
                    "range": [0, max_score // 2],
                    "color": "#10B981",
                    "emoji": "😊"
                },
                {
                    "level": "high",
                    "range": [max_score // 2 + 1, max_score],
                    "color": "#EF4444",
                    "emoji": "😔"
                }
            ]
        elif self.result_levels == 3:
            third = max_score // 3
            return [
                {
                    "level": "low",
                    "range": [0, third],
                    "color": "#10B981",
                    "emoji": "😊"
                },
                {
                    "level": "moderate",
                    "range": [third + 1, third * 2],
                    "color": "#F59E0B",
                    "emoji": "😐"
                },
                {
                    "level": "high",
                    "range": [third * 2 + 1, max_score],
                    "color": "#EF4444",
                    "emoji": "😔"
                }
            ]
        else:  # 4 уровня (по умолчанию)
            quarter = max_score // 4
            return [
                {
                    "level": "minimal",
                    "range": [0, quarter],
                    "color": "#10B981",
                    "emoji": "😊"
                },
                {
                    "level": "mild",
                    "range": [quarter + 1, quarter * 2],
                    "color": "#F59E0B",
                    "emoji": "😐"
                },
                {
                    "level": "moderate",
                    "range": [quarter * 2 + 1, quarter * 3],
                    "color": "#EF4444",
                    "emoji": "😔"
                },
                {
                    "level": "severe",
                    "range": [quarter * 3 + 1, max_score],
                    "color": "#DC2626",
                    "emoji": "😢",
                    "urgent": True
                }
            ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать настройки в словарь"""
        return {
            "test_domain": self.test_domain,
            "test_type": self.test_type,
            "target_language": self.target_language,
            "question_count": self.question_count,
            "scoring_system": self.scoring_system,
            "result_levels": self.result_levels,
            "methodology_level": self.methodology_level,
            "vak_enabled": self.enable_vak_adaptation,
            "age_enabled": self.enable_age_adaptation,
            "language_enabled": self.enable_language_adaptation
        }

def load_content_settings() -> ContentArchitectSettings:
    """
    Загрузить настройки и проверить наличие переменных
    """
    try:
        return ContentArchitectSettings()
    except Exception as e:
        error_msg = f"Не удалось загрузить настройки: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nУбедитесь, что LLM_API_KEY указан в файле .env"
        raise ValueError(error_msg) from e