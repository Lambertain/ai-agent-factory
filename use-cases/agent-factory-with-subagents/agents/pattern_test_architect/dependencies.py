"""
Зависимости для Pattern Test Architect Agent
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import aiofiles


class PsychometricDatabase:
    """База данных психометрических методик"""

    def __init__(self):
        self.methodologies = {}
        self.constructs = {}
        self.validation_cache = {}

    async def get_methodology(self, name: str) -> Optional[Dict[str, Any]]:
        """Получение данных о методике"""
        return self.methodologies.get(name)

    async def validate_construct_match(self, methodology: str, construct: str) -> bool:
        """Проверка соответствия методики и конструкта"""
        method_data = await self.get_methodology(methodology)
        if not method_data:
            return False
        return construct in method_data.get("constructs", [])

    async def get_reliability_data(self, methodology: str) -> Dict[str, float]:
        """Получение данных о надежности методики"""
        method_data = await self.get_methodology(methodology)
        if not method_data:
            return {}
        return method_data.get("reliability", {})


class ViralPatternsDatabase:
    """База данных успешных вирусных паттернов"""

    def __init__(self):
        self.viral_patterns = {}
        self.emotional_hooks = {}
        self.language_styles = {}

    async def get_viral_patterns(self, category: str) -> List[str]:
        """Получение вирусных паттернов для категории"""
        return self.viral_patterns.get(category, [])

    async def get_emotional_hooks(self, audience: str) -> List[str]:
        """Получение эмоциональных крючков для аудитории"""
        return self.emotional_hooks.get(audience, [])

    async def analyze_viral_potential(self, text: str) -> float:
        """Анализ вирусного потенциала текста"""
        # Упрощенный анализ
        viral_keywords = ["почему", "что", "как", "ты", "твой", "не"]
        score = sum(1 for word in viral_keywords if word in text.lower())
        return min(score / len(viral_keywords), 1.0)


class TransformationProgramsRegistry:
    """Реестр программ трансформации"""

    def __init__(self):
        self.programs = {}
        self.construct_mappings = {}

    async def get_programs_for_construct(self, construct: str) -> List[str]:
        """Получение программ для психологического конструкта"""
        return self.construct_mappings.get(construct, [])

    async def get_program_details(self, program_id: str) -> Optional[Dict[str, Any]]:
        """Получение детальной информации о программе"""
        return self.programs.get(program_id)

    async def register_program(self, program_id: str, program_data: Dict[str, Any]):
        """Регистрация новой программы"""
        self.programs[program_id] = program_data

        # Обновляем маппинги конструктов
        constructs = program_data.get("constructs", [])
        for construct in constructs:
            if construct not in self.construct_mappings:
                self.construct_mappings[construct] = []
            if program_id not in self.construct_mappings[construct]:
                self.construct_mappings[construct].append(program_id)


class TestValidationService:
    """Сервис валидации тестов"""

    def __init__(self):
        self.validation_rules = {}
        self.ethical_guidelines = {}

    async def validate_ethical_compliance(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Проверка этического соответствия теста"""
        issues = []

        # Проверка на диагностику серьезных расстройств
        dangerous_constructs = ["суицидальность", "психоз", "шизофрения", "биполярное"]
        test_text = str(test_data).lower()

        for construct in dangerous_constructs:
            if construct in test_text:
                issues.append(f"Недопустимо диагностировать {construct} без профессионала")

        # Проверка возрастных ограничений
        if test_data.get("target_audience") == "children" and not test_data.get("parental_consent"):
            issues.append("Требуется согласие родителей для детских тестов")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues,
            "recommendations": self._get_ethical_recommendations(issues)
        }

    def _get_ethical_recommendations(self, issues: List[str]) -> List[str]:
        """Получение этических рекомендаций"""
        recommendations = []

        if any("диагностировать" in issue for issue in issues):
            recommendations.append("Добавить предупреждение о необходимости консультации специалиста")
            recommendations.append("Изменить формулировки с диагностических на описательные")

        if any("согласие" in issue for issue in issues):
            recommendations.append("Добавить форму согласия родителей")
            recommendations.append("Создать отдельную версию для взрослых")

        return recommendations


class TestMetricsAnalyzer:
    """Анализатор метрик эффективности тестов"""

    def __init__(self):
        self.historical_data = {}
        self.benchmarks = {}

    async def analyze_completion_rate(self, test_data: Dict[str, Any]) -> float:
        """Анализ прогнозируемого процента завершения"""
        question_count = len(test_data.get("questions", []))

        # Базовые факторы влияния на завершаемость
        base_rate = 0.85

        # Влияние количества вопросов
        if question_count > 30:
            base_rate -= 0.3
        elif question_count > 20:
            base_rate -= 0.15
        elif question_count < 5:
            base_rate -= 0.1

        # Влияние сложности вопросов
        avg_complexity = test_data.get("avg_complexity", 0.5)
        if avg_complexity > 0.8:
            base_rate -= 0.2
        elif avg_complexity < 0.3:
            base_rate -= 0.1

        return max(0.1, min(1.0, base_rate))

    async def predict_viral_potential(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Прогноз вирусного потенциала"""
        viral_name = test_data.get("viral_name", "")

        factors = {
            "emotional_trigger": self._analyze_emotional_trigger(viral_name),
            "curiosity_gap": self._analyze_curiosity_gap(viral_name),
            "personal_relevance": self._analyze_personal_relevance(viral_name),
            "shareability": self._analyze_shareability(viral_name)
        }

        overall_score = sum(factors.values()) / len(factors)

        return {
            "overall_viral_score": overall_score,
            **factors,
            "predicted_shares": int(overall_score * 10000),
            "predicted_reach": int(overall_score * 50000)
        }

    def _analyze_emotional_trigger(self, text: str) -> float:
        """Анализ эмоционального триггера"""
        emotional_words = ["почему", "не", "мешает", "проблема", "боль", "страх"]
        score = sum(1 for word in emotional_words if word in text.lower())
        return min(score / 3, 1.0)

    def _analyze_curiosity_gap(self, text: str) -> float:
        """Анализ любопытства"""
        curiosity_patterns = ["почему", "что", "как", "откуда", "зачем"]
        score = sum(1 for pattern in curiosity_patterns if pattern in text.lower())
        return min(score / 2, 1.0)

    def _analyze_personal_relevance(self, text: str) -> float:
        """Анализ личной релевантности"""
        personal_pronouns = ["ты", "твой", "тебя", "у тебя"]
        score = sum(1 for pronoun in personal_pronouns if pronoun in text.lower())
        return min(score / 2, 1.0)

    def _analyze_shareability(self, text: str) -> float:
        """Анализ склонности к репосту"""
        # Упрощенный анализ
        if len(text) < 10:
            return 0.3
        elif len(text) > 100:
            return 0.5
        return 0.8


class ContentQualityChecker:
    """Проверщик качества контента"""

    def __init__(self):
        self.language_models = {}
        self.readability_analyzer = None

    async def check_question_clarity(self, question: str) -> Dict[str, Any]:
        """Проверка ясности вопроса"""
        # Метрики ясности
        word_count = len(question.split())
        sentence_count = question.count('.') + question.count('?') + question.count('!')

        clarity_score = 1.0

        # Штрафы за сложность
        if word_count > 20:
            clarity_score -= 0.2
        if sentence_count > 2:
            clarity_score -= 0.1

        # Проверка понятности слов
        complex_words = ["психологический", "когнитивный", "аффективный", "интроверсия"]
        for word in complex_words:
            if word in question.lower():
                clarity_score -= 0.1

        issues = []
        recommendations = []

        if word_count > 25:
            issues.append("Вопрос слишком длинный")
            recommendations.append("Разбить на два коротких вопроса")

        if clarity_score < 0.6:
            issues.append("Низкая ясность формулировки")
            recommendations.append("Упростить язык и структуру")

        return {
            "clarity_score": max(0.0, clarity_score),
            "word_count": word_count,
            "issues": issues,
            "recommendations": recommendations
        }

    async def analyze_interpretation_quality(self, interpretation: str) -> Dict[str, Any]:
        """Анализ качества интерпретации"""
        # Проверка структуры интерпретации
        has_explanation = len(interpretation) > 100
        has_recommendations = "рекомендации" in interpretation.lower() or "советы" in interpretation.lower()
        is_encouraging = any(word in interpretation.lower() for word in ["можешь", "способен", "поможет"])

        quality_score = 0.0

        if has_explanation:
            quality_score += 0.4
        if has_recommendations:
            quality_score += 0.3
        if is_encouraging:
            quality_score += 0.3

        return {
            "quality_score": quality_score,
            "has_explanation": has_explanation,
            "has_recommendations": has_recommendations,
            "is_encouraging": is_encouraging,
            "readability": "good" if len(interpretation.split()) < 150 else "too_long"
        }


@dataclass
class PatternTestArchitectDependencies:
    """Основной класс зависимостей для Pattern Test Architect Agent"""

    api_key: str
    patternshift_project_path: str = ""

    # Базы данных и сервисы
    psychometric_db: PsychometricDatabase = field(default_factory=PsychometricDatabase)
    viral_patterns_db: ViralPatternsDatabase = field(default_factory=ViralPatternsDatabase)
    programs_registry: TransformationProgramsRegistry = field(default_factory=TransformationProgramsRegistry)
    validation_service: TestValidationService = field(default_factory=TestValidationService)
    metrics_analyzer: TestMetricsAnalyzer = field(default_factory=TestMetricsAnalyzer)
    quality_checker: ContentQualityChecker = field(default_factory=ContentQualityChecker)

    def __post_init__(self):
        """Инициализация после создания dataclass"""
        pass

    async def initialize(self):
        """Инициализация всех зависимостей"""
        await self._load_psychometric_data()
        await self._load_viral_patterns()
        await self._load_transformation_programs()

    async def _load_psychometric_data(self):
        """Загрузка данных о психометрических методиках"""
        # В реальном приложении здесь будет загрузка из базы данных
        sample_data = {
            "PHQ-9": {
                "name": "Patient Health Questionnaire-9",
                "constructs": ["depression"],
                "reliability": {
                    "internal_consistency": 0.89,
                    "test_retest": 0.84,
                    "validity": 0.88
                },
                "question_count": 9,
                "validated": True
            },
            "GAD-7": {
                "name": "Generalized Anxiety Disorder-7",
                "constructs": ["anxiety"],
                "reliability": {
                    "internal_consistency": 0.92,
                    "test_retest": 0.83,
                    "validity": 0.86
                },
                "question_count": 7,
                "validated": True
            }
        }
        self.psychometric_db.methodologies = sample_data

    async def _load_viral_patterns(self):
        """Загрузка паттернов вирусного контента"""
        sample_patterns = {
            "depression": [
                "Почему ты постоянно грустный?",
                "Что отнимает у тебя энергию?",
                "Почему жизнь кажется серой?"
            ],
            "anxiety": [
                "Почему ты постоянно переживаешь?",
                "Что тебя так беспокоит?",
                "Откуда твои страхи?"
            ],
            "relationships": [
                "Почему у тебя не складываются отношения?",
                "Почему тебя не понимают в отношениях?"
            ]
        }
        self.viral_patterns_db.viral_patterns = sample_patterns

    async def _load_transformation_programs(self):
        """Загрузка данных о программах трансформации"""
        sample_programs = {
            "depression_recovery": {
                "name": "Путь к радости",
                "constructs": ["depression"],
                "duration_days": 21,
                "modules": ["mindfulness", "activity_planning", "cognitive_restructuring"]
            },
            "anxiety_management": {
                "name": "Спокойствие и уверенность",
                "constructs": ["anxiety"],
                "duration_days": 14,
                "modules": ["breathing_techniques", "progressive_relaxation", "exposure_therapy"]
            }
        }
        self.programs_registry.programs = sample_programs
        self.programs_registry.construct_mappings = {
            "depression": ["depression_recovery"],
            "anxiety": ["anxiety_management"]
        }

    async def get_psychometric_validation(self, methodology: str, construct: str) -> Dict[str, Any]:
        """Получение психометрической валидации"""
        return await self.validation_service.validate_ethical_compliance({
            "methodology": methodology,
            "construct": construct
        })

    async def get_viral_transformation(self, academic_name: str, audience: str) -> Dict[str, Any]:
        """Получение вирусной трансформации"""
        patterns = await self.viral_patterns_db.get_viral_patterns("general")
        return {
            "viral_name": patterns[0] if patterns else "Что это говорит о тебе?",
            "emotional_hook": "Узнай правду о себе",
            "viral_score": 0.7
        }

    async def get_effectiveness_metrics(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Получение метрик эффективности"""
        completion_rate = await self.metrics_analyzer.analyze_completion_rate(test_data)
        viral_metrics = await self.metrics_analyzer.predict_viral_potential(test_data)

        return {
            "completion_rate": completion_rate,
            **viral_metrics
        }


# Создание глобального экземпляра зависимостей
dependencies = PatternTestArchitectDependencies()