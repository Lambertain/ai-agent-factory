"""
Dependencies для NLP Psychology Test Adapter Agent

Обеспечивает универсальную конфигурацию и RAG интеграцию для адаптации тестов.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
import asyncio
import json
from datetime import datetime
import httpx


class TestConfiguration(BaseModel):
    """Конфигурация для адаптации теста."""
    source_test_name: str = Field(description="Название исходного теста")
    target_language: str = Field(default="uk", description="Целевой язык")
    cultural_context: str = Field(default="ukrainian", description="Культурный контекст")

    # Настройки методологии PatternShift
    methodology_config: Dict[str, Any] = Field(default_factory=lambda: {
        "min_questions": 15,
        "life_situations": True,
        "adaptive_scoring": True,
        "result_levels": 4,
        "redirection_logic": True
    })

    # Поддерживаемые языки
    supported_languages: List[str] = Field(default_factory=lambda: ["uk", "en", "ru"])

    # Настройки качества
    quality_thresholds: Dict[str, float] = Field(default_factory=lambda: {
        "methodology_compliance": 0.85,
        "psychological_validity": 0.90,
        "structural_integrity": 0.80
    })

    # Настройки RAG
    rag_config: Dict[str, Any] = Field(default_factory=lambda: {
        "server_url": "http://localhost:3737",
        "knowledge_tags": ["psychology-test-adaptation", "patternshift-methodology", "psychological-assessment"],
        "match_count": 5
    })


class AdaptationResult(BaseModel):
    """Результат адаптации теста."""
    adapted_test: Optional[Dict[str, Any]] = None
    validation_results: 'TestValidationResult'
    adaptation_metadata: Dict[str, Any] = Field(default_factory=dict)


class TestValidationResult(BaseModel):
    """Результат валидации адаптированного теста."""
    is_valid: bool = False
    validation_errors: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)
    methodology_compliance: Dict[str, Any] = Field(default_factory=dict)
    psychological_validation: Dict[str, Any] = Field(default_factory=dict)
    structural_score: float = 0.0
    overall_quality_score: float = 0.0


class PatternShiftTestAdapterDeps:
    """Зависимости для агента адаптации тестов."""

    def __init__(self, config: TestConfiguration):
        self.config = config
        self.rag_client = None
        self._knowledge_cache = {}

    @classmethod
    async def create(cls, config: TestConfiguration) -> 'PatternShiftTestAdapterDeps':
        """Создает экземпляр с инициализацией RAG клиента."""
        instance = cls(config)
        await instance._initialize_rag_client()
        return instance

    async def _initialize_rag_client(self):
        """Инициализирует RAG клиент."""
        try:
            self.rag_client = httpx.AsyncClient(
                base_url=self.config.rag_config["server_url"],
                timeout=30.0
            )
            # Проверка доступности RAG сервера
            response = await self.rag_client.get("/health")
            if response.status_code != 200:
                print(f"Warning: RAG server не доступен: {response.status_code}")
        except Exception as e:
            print(f"Warning: Не удалось подключиться к RAG серверу: {e}")
            self.rag_client = None

    async def search_agent_knowledge(
        self,
        query: str,
        match_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Поиск релевантных знаний в RAG базе.

        Args:
            query: Поисковый запрос
            match_count: Количество результатов
        """
        if not self.rag_client:
            return {"results": [], "error": "RAG client not available"}

        # Проверка кэша
        cache_key = f"{query}:{match_count}"
        if cache_key in self._knowledge_cache:
            return self._knowledge_cache[cache_key]

        try:
            match_count = match_count or self.config.rag_config["match_count"]

            response = await self.rag_client.post("/search", json={
                "query": query,
                "match_count": match_count,
                "tags": self.config.rag_config["knowledge_tags"]
            })

            if response.status_code == 200:
                result = response.json()
                self._knowledge_cache[cache_key] = result
                return result
            else:
                return {"results": [], "error": f"RAG search failed: {response.status_code}"}

        except Exception as e:
            return {"results": [], "error": f"RAG search error: {str(e)}"}

    async def analyze_source_test(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализирует исходный тест для понимания его структуры и конструктов."""
        questions = test_data.get('questions', [])

        analysis = {
            'question_count': len(questions),
            'scoring_system': test_data.get('scoring', {}),
            'constructs': [],
            'difficulty_levels': [],
            'language_complexity': 'medium',
            'clinical_terminology_usage': 0,
            'recommendations': []
        }

        # Анализ использования клинической терминологии
        clinical_terms = ['депрессия', 'тревога', 'симптом', 'диагноз', 'расстройство']
        for question in questions:
            question_text = question.get('text', '').lower()
            for term in clinical_terms:
                if term in question_text:
                    analysis['clinical_terminology_usage'] += 1

        # Рекомендации на основе анализа
        if analysis['question_count'] < 15:
            analysis['recommendations'].append('expand_questions')

        if analysis['clinical_terminology_usage'] > len(questions) * 0.3:
            analysis['recommendations'].append('replace_clinical_terms')

        return analysis

    def generate_patternshift_title(self, original_title: str) -> str:
        """Генерирует заголовок в стиле PatternShift."""
        # Преобразование клинических названий в жизненные вопросы
        title_mappings = {
            'depression': 'Чому мені все байдуже?',
            'anxiety': 'Чому я постійно хвилююся?',
            'stress': 'Чому я не можу розслабитися?',
            'self-esteem': 'Чому я себе не ціную?',
            'relationships': 'Чому мені важко з людьми?'
        }

        # Пытаемся определить тип теста и применить маппинг
        for test_type, patternshift_title in title_mappings.items():
            if test_type.lower() in original_title.lower():
                return patternshift_title

        # Если маппинг не найден, создаем универсальный заголовок
        return f"Що відбувається з моїм {original_title.lower().replace('test', '').replace('questionnaire', '').strip()}?"

    async def validate_methodology_compliance(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Валидирует соответствие методологии PatternShift."""
        compliance_score = 0.0
        errors = []

        # Проверка минимального количества вопросов
        questions = test_data.get('questions', [])
        if len(questions) >= self.config.methodology_config['min_questions']:
            compliance_score += 0.25
        else:
            errors.append(f"Недостаточно вопросов: {len(questions)} < {self.config.methodology_config['min_questions']}")

        # Проверка использования жизненных ситуаций
        life_situation_count = 0
        for question in questions:
            question_text = question.get('text', '')
            if any(indicator in question_text.lower() for indicator in
                   ['коли ви', 'якщо', 'уявіть', 'ситуація', 'в житті']):
                life_situation_count += 1

        if life_situation_count >= len(questions) * 0.7:
            compliance_score += 0.25
        else:
            errors.append(f"Недостаточно вопросов в формате жизненных ситуаций: {life_situation_count}/{len(questions)}")

        # Проверка адаптивной системы оценки
        scoring = test_data.get('scoring', {})
        if 'adaptive_thresholds' in scoring or 'flexible_levels' in scoring:
            compliance_score += 0.25
        else:
            errors.append("Отсутствует адаптивная система оценки")

        # Проверка логики перенаправления
        if 'redirection_logic' in test_data:
            compliance_score += 0.25
        else:
            errors.append("Отсутствует логика перенаправления")

        return {
            'is_compliant': len(errors) == 0,
            'compliance_score': compliance_score,
            'errors': errors
        }

    async def analyze_test_constructs(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализирует психологические конструкты в вопросах."""
        # Поиск знаний о психологических конструктах
        knowledge = await self.search_agent_knowledge(
            "psychological constructs test design measurement",
            match_count=3
        )

        constructs = []
        difficulty_distribution = {'easy': 0, 'medium': 0, 'hard': 0}

        # Базовый анализ конструктов (можно расширить с помощью RAG)
        for question in questions:
            text = question.get('text', '').lower()

            # Определение конструктов по ключевым словам
            if any(word in text for word in ['настрій', 'радість', 'сумно', 'пригнічен']):
                constructs.append('mood')
            elif any(word in text for word in ['хвилюю', 'тривога', 'страх', 'нервую']):
                constructs.append('anxiety')
            elif any(word in text for word in ['енергія', 'втома', 'активність']):
                constructs.append('energy')
            elif any(word in text for word in ['сон', 'спати', 'безсоння']):
                constructs.append('sleep')

            # Оценка сложности вопроса
            if len(text.split()) < 10:
                difficulty_distribution['easy'] += 1
            elif len(text.split()) < 20:
                difficulty_distribution['medium'] += 1
            else:
                difficulty_distribution['hard'] += 1

        return {
            'constructs': list(set(constructs)),
            'difficulty_distribution': difficulty_distribution,
            'total_questions': len(questions)
        }

    async def balance_question_difficulty(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Балансирует сложность вопросов в тесте."""
        # Сортировка по сложности и перемешивание для баланса
        easy_questions = []
        medium_questions = []
        hard_questions = []

        for question in questions:
            text_length = len(question.get('text', '').split())
            if text_length < 10:
                easy_questions.append(question)
            elif text_length < 20:
                medium_questions.append(question)
            else:
                hard_questions.append(question)

        # Создание сбалансированного порядка
        balanced = []
        total = len(questions)

        # Интерливинг: легкий -> средний -> сложный
        max_len = max(len(easy_questions), len(medium_questions), len(hard_questions))
        for i in range(max_len):
            if i < len(easy_questions):
                balanced.append(easy_questions[i])
            if i < len(medium_questions):
                balanced.append(medium_questions[i])
            if i < len(hard_questions):
                balanced.append(hard_questions[i])

        return balanced[:total]

    def calculate_quality_score(
        self,
        methodology_compliance: float,
        psychological_validity: float,
        structural_integrity: float
    ) -> float:
        """Рассчитывает общий балл качества адаптации."""
        weights = {
            'methodology': 0.4,
            'psychology': 0.4,
            'structure': 0.2
        }

        return (
            methodology_compliance * weights['methodology'] +
            psychological_validity * weights['psychology'] +
            structural_integrity * weights['structure']
        )

    def get_adaptation_priorities(self) -> str:
        """Возвращает приоритеты адаптации в текстовом виде."""
        priorities = []

        if self.config.methodology_config.get('life_situations', True):
            priorities.append("Трансформация в жизненные ситуации")

        if self.config.methodology_config.get('adaptive_scoring', True):
            priorities.append("Адаптивная система оценки")

        if len(self.config.supported_languages) > 1:
            priorities.append("Мультиязычная поддержка")

        return "\n".join([f"- {priority}" for priority in priorities])

    def get_timestamp(self) -> str:
        """Возвращает текущий timestamp."""
        return datetime.now().isoformat()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.rag_client:
            await self.rag_client.aclose()