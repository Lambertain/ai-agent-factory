# -*- coding: utf-8 -*-
"""
Тесты для CompetencyChecker утилиты.

Проверяет правильность определения компетенций агентов
при обработке ошибок согідно с протоколом 09_problem_analysis_protocol.md
"""

import pytest
from competency_checker import (
    CompetencyChecker,
    CompetencyResult,
    is_in_competency
)
from competency_matrices import AgentType, ERROR_TYPE_MATRIX


class TestErrorTypeCompetency:
    """Тесты для проверки компетенций по типу ошибки."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.checker = CompetencyChecker()

    def test_implementation_engineer_typescript_compile_error(self):
        """Implementation Engineer должен обрабатывать TypeScript compile ошибки."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Archon Implementation Engineer",
            error_type="typescript_compile"
        )

        assert is_competent is True, "Implementation Engineer должен обрабатывать typescript_compile"
        assert recommended_agent is None, "Не должно быть рекомендации при компетентности"

    def test_implementation_engineer_database_error_escalation(self):
        """Implementation Engineer должен эскалировать Database ошибки."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Archon Implementation Engineer",
            error_type="n_plus_one_query"
        )

        assert is_competent is False, "Implementation Engineer НЕ должен обрабатывать n_plus_one_query"
        assert recommended_agent == "Prisma Database Agent", "Должна быть рекомендация Prisma Database Agent"

    def test_security_audit_xss_vulnerability(self):
        """Security Audit Agent должен обрабатывать XSS уязвимости."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Security Audit Agent",
            error_type="xss_vulnerability"
        )

        assert is_competent is True, "Security Audit Agent должен обрабатывать xss_vulnerability"
        assert recommended_agent is None

    def test_security_audit_typescript_error_escalation(self):
        """Security Audit Agent должен эскалировать TypeScript ошибки."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Security Audit Agent",
            error_type="typescript_compile"
        )

        assert is_competent is False
        assert recommended_agent == "Archon Implementation Engineer"

    def test_prisma_database_sql_optimization(self):
        """Prisma Database Agent должен обрабатывать SQL оптимизацию."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Prisma Database Agent",
            error_type="slow_query"
        )

        assert is_competent is True
        assert recommended_agent is None

    def test_quality_guardian_missing_tests(self):
        """Quality Guardian должен обрабатывать отсутствующие тесты."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Archon Quality Guardian",
            error_type="missing_tests"
        )

        assert is_competent is True
        assert recommended_agent is None

    def test_deployment_engineer_ci_cd_failure(self):
        """Deployment Engineer должен обрабатывать CI/CD ошибки."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Archon Deployment Engineer",
            error_type="ci_cd_failure"
        )

        assert is_competent is True
        assert recommended_agent is None

    def test_unknown_error_type_escalates_to_analysis_lead(self):
        """Неизвестный тип ошибки должен эскалироваться к Analysis Lead."""
        is_competent, recommended_agent = self.checker.is_in_competency(
            agent_role="Archon Implementation Engineer",
            error_type="unknown_error_type_12345"
        )

        assert is_competent is False
        assert recommended_agent == "Archon Analysis Lead", "Неизвестная ошибка → Analysis Lead"


class TestKeywordCompetency:
    """Тесты для проверки компетенций через keyword matching (старый метод)."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.checker = CompetencyChecker()

    def test_api_development_task_match(self):
        """API Development Agent должен распознавать API задачи."""
        result = self.checker.check_competency(
            task_description="Создать REST API endpoint для получения пользователей",
            agent_type=AgentType.API_DEVELOPMENT
        )

        assert result.can_handle is True, "API agent должен обрабатывать API задачи"
        assert result.confidence > 0.7, "Уверенность должна быть высокой"

    def test_security_audit_task_match(self):
        """Security Audit Agent должен распознавать security задачи."""
        result = self.checker.check_competency(
            task_description="Проверить API на XSS уязвимости и SQL injection",
            agent_type=AgentType.SECURITY_AUDIT
        )

        assert result.can_handle is True
        assert result.confidence > 0.7

    def test_exclusion_detection(self):
        """Агент должен отклонять задачи из exclusions."""
        result = self.checker.check_competency(
            task_description="Разработать UI дизайн для формы регистрации",
            agent_type=AgentType.API_DEVELOPMENT  # API agent не занимается UI
        )

        assert result.can_handle is False, "API agent должен отклонять UI задачи"
        assert result.suggested_agent is not None

    def test_low_confidence_suggests_agent(self):
        """При низкой уверенности должен быть рекомендован другой агент."""
        result = self.checker.check_competency(
            task_description="Неясная задача без ключевых слов",
            agent_type=AgentType.API_DEVELOPMENT
        )

        if not result.can_handle:
            assert result.suggested_agent is not None


class TestConvenienceFunctions:
    """Тесты для удобных функций-оберток."""

    def test_is_in_competency_function(self):
        """Тест функции is_in_competency (обертка)."""
        is_competent, recommended_agent = is_in_competency(
            agent_role="Archon Implementation Engineer",
            error_type="python_syntax"
        )

        assert is_competent is True
        assert recommended_agent is None

    def test_is_in_competency_with_escalation(self):
        """Тест функции is_in_competency с эскалацией."""
        is_competent, recommended_agent = is_in_competency(
            agent_role="Archon Implementation Engineer",
            error_type="xss_vulnerability"
        )

        assert is_competent is False
        assert recommended_agent == "Security Audit Agent"


class TestErrorTypeMatrix:
    """Тесты для проверки полноты ERROR_TYPE_MATRIX."""

    def test_all_core_agents_have_error_types(self):
        """Все Core Team агенты должны иметь типы ошибок."""
        core_agents = [
            "Archon Analysis Lead",
            "Archon Blueprint Architect",
            "Archon Implementation Engineer",
            "Archon Quality Guardian",
            "Archon Deployment Engineer"
        ]

        for agent in core_agents:
            error_types_for_agent = [
                error_type for error_type, assigned_agent in ERROR_TYPE_MATRIX.items()
                if assigned_agent == agent
            ]
            assert len(error_types_for_agent) > 0, f"{agent} должен иметь хотя бы один тип ошибки"

    def test_all_specialized_agents_have_error_types(self):
        """Все Specialized агенты должны иметь типы ошибок."""
        specialized_agents = [
            "Security Audit Agent",
            "Prisma Database Agent",
            "UI/UX Enhancement Agent",
            "Performance Optimization Agent",
            "TypeScript Architecture Agent"
        ]

        for agent in specialized_agents:
            error_types_for_agent = [
                error_type for error_type, assigned_agent in ERROR_TYPE_MATRIX.items()
                if assigned_agent == agent
            ]
            assert len(error_types_for_agent) > 0, f"{agent} должен иметь хотя бы один тип ошибки"

    def test_no_duplicate_error_types(self):
        """Каждый тип ошибки должен быть назначен только одному агенту."""
        error_types = list(ERROR_TYPE_MATRIX.keys())
        assert len(error_types) == len(set(error_types)), "Не должно быть дублирующихся типов ошибок"


class TestDelegationMatrix:
    """Тесты для проверки матрицы делегирования."""

    def setup_method(self):
        """Подготовка перед каждым тестом."""
        self.checker = CompetencyChecker()

    def test_get_delegation_suggestions(self):
        """Получение рекомендаций по делегированию."""
        suggestions = self.checker.get_delegation_suggestions(AgentType.SECURITY_AUDIT)

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0, "Security Audit должен иметь варианты делегирования"

    def test_api_agent_can_delegate_to_security(self):
        """API agent должен мочь делегировать security задачи."""
        suggestions = self.checker.get_delegation_suggestions(AgentType.API_DEVELOPMENT)

        assert "security_audit_agent" in suggestions


# [OK] Тесты написаны согласно pytest стандартам
# [OK] Покрывают основные сценарии использования
# [OK] Проверяют как метод is_in_competency (главный), так и check_competency (старый)
# [OK] Проверяют корректность ERROR_TYPE_MATRIX и DELEGATION_MATRIX
