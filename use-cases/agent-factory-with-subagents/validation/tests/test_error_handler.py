"""
Tests for the validation error handler system.
"""

import pytest
from datetime import datetime
from pydantic import BaseModel, ValidationError, Field

from ..error_handler import (
    ErrorSeverity, ErrorCategory, ValidationErrorDetail,
    ValidationReport, ValidationErrorHandler,
    handle_validation_error, create_custom_error, format_error_for_user
)


# Test models for Pydantic error testing
class TestModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=0, le=150)
    email: str


class TestValidationErrorDetail:
    """Test ValidationErrorDetail class."""

    def test_error_detail_creation(self):
        """Test error detail creation."""
        error = ValidationErrorDetail(
            field_name="test_field",
            field_path="root.test_field",
            error_type="value_error",
            error_message="Test error message",
            invalid_value="invalid",
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.VALUE_ERROR
        )

        assert error.field_name == "test_field"
        assert error.field_path == "root.test_field"
        assert error.error_type == "value_error"
        assert error.severity == ErrorSeverity.HIGH
        assert error.category == ErrorCategory.VALUE_ERROR

    def test_error_detail_to_dict(self):
        """Test error detail dictionary conversion."""
        error = ValidationErrorDetail(
            field_name="test_field",
            field_path="root.test_field",
            error_type="value_error",
            error_message="Test error message",
            invalid_value="invalid"
        )

        error_dict = error.to_dict()

        assert isinstance(error_dict, dict)
        assert error_dict["field_name"] == "test_field"
        assert error_dict["error_type"] == "value_error"
        assert error_dict["severity"] == ErrorSeverity.MEDIUM.value
        assert "timestamp" in error_dict

    def test_error_detail_with_suggestions(self):
        """Test error detail with suggestions."""
        error = ValidationErrorDetail(
            field_name="email",
            field_path="email",
            error_type="format_error",
            error_message="Invalid email format",
            invalid_value="not-an-email",
            suggestions=["Add @ symbol", "Add domain extension"]
        )

        assert len(error.suggestions) == 2
        assert "Add @ symbol" in error.suggestions

    def test_error_detail_with_context(self):
        """Test error detail with context."""
        context = {"user_id": "123", "request_id": "req_456"}
        error = ValidationErrorDetail(
            field_name="test_field",
            field_path="test_field",
            error_type="value_error",
            error_message="Test error",
            invalid_value="invalid",
            context=context
        )

        assert error.context["user_id"] == "123"
        assert error.context["request_id"] == "req_456"


class TestValidationReport:
    """Test ValidationReport class."""

    def test_report_creation(self):
        """Test validation report creation."""
        report = ValidationReport(is_valid=True)
        assert report.is_valid
        assert len(report.errors) == 0
        assert len(report.warnings) == 0

    def test_adding_errors(self):
        """Test adding errors to report."""
        report = ValidationReport(is_valid=True)

        error = ValidationErrorDetail(
            field_name="test",
            field_path="test",
            error_type="value_error",
            error_message="Test error",
            invalid_value="invalid"
        )

        report.add_error(error)

        assert not report.is_valid
        assert len(report.errors) == 1
        assert report.errors[0] == error

    def test_adding_warnings(self):
        """Test adding warnings to report."""
        report = ValidationReport(is_valid=True)

        warning = ValidationErrorDetail(
            field_name="test",
            field_path="test",
            error_type="warning",
            error_message="Test warning",
            invalid_value="questionable",
            severity=ErrorSeverity.LOW
        )

        report.add_warning(warning)

        assert report.is_valid  # Warnings don't affect validity
        assert len(report.warnings) == 1

    def test_errors_by_severity(self):
        """Test filtering errors by severity."""
        report = ValidationReport(is_valid=False)

        high_error = ValidationErrorDetail(
            field_name="critical",
            field_path="critical",
            error_type="security_error",
            error_message="Security issue",
            invalid_value="malicious",
            severity=ErrorSeverity.HIGH
        )

        low_error = ValidationErrorDetail(
            field_name="format",
            field_path="format",
            error_type="format_error",
            error_message="Format issue",
            invalid_value="badly_formatted",
            severity=ErrorSeverity.LOW
        )

        report.add_error(high_error)
        report.add_error(low_error)

        high_errors = report.get_errors_by_severity(ErrorSeverity.HIGH)
        low_errors = report.get_errors_by_severity(ErrorSeverity.LOW)

        assert len(high_errors) == 1
        assert len(low_errors) == 1
        assert high_errors[0].severity == ErrorSeverity.HIGH

    def test_errors_by_category(self):
        """Test filtering errors by category."""
        report = ValidationReport(is_valid=False)

        type_error = ValidationErrorDetail(
            field_name="age",
            field_path="age",
            error_type="type_error",
            error_message="Type mismatch",
            invalid_value="not_a_number",
            category=ErrorCategory.TYPE_MISMATCH
        )

        value_error = ValidationErrorDetail(
            field_name="name",
            field_path="name",
            error_type="value_error",
            error_message="Invalid value",
            invalid_value="",
            category=ErrorCategory.VALUE_ERROR
        )

        report.add_error(type_error)
        report.add_error(value_error)

        type_errors = report.get_errors_by_category(ErrorCategory.TYPE_MISMATCH)
        value_errors = report.get_errors_by_category(ErrorCategory.VALUE_ERROR)

        assert len(type_errors) == 1
        assert len(value_errors) == 1

    def test_report_summary(self):
        """Test report summary generation."""
        report = ValidationReport(is_valid=False)

        # Add various errors and warnings
        report.add_error(ValidationErrorDetail(
            field_name="critical",
            field_path="critical",
            error_type="critical_error",
            error_message="Critical issue",
            invalid_value="bad",
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.SECURITY_VIOLATION
        ))

        report.add_error(ValidationErrorDetail(
            field_name="medium",
            field_path="medium",
            error_type="medium_error",
            error_message="Medium issue",
            invalid_value="questionable",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.VALUE_ERROR
        ))

        report.add_warning(ValidationErrorDetail(
            field_name="warning",
            field_path="warning",
            error_type="warning",
            error_message="Warning message",
            invalid_value="suspicious",
            severity=ErrorSeverity.LOW
        ))

        summary = report.get_summary()

        assert summary["is_valid"] == False
        assert summary["total_errors"] == 2
        assert summary["total_warnings"] == 1
        assert summary["error_breakdown"]["critical"] == 1
        assert summary["error_breakdown"]["medium"] == 1
        assert summary["category_breakdown"]["security_violation"] == 1

    def test_report_to_dict(self):
        """Test report dictionary conversion."""
        report = ValidationReport(
            is_valid=False,
            metadata={"test": "data"},
            execution_time_ms=150.5
        )

        error = ValidationErrorDetail(
            field_name="test",
            field_path="test",
            error_type="test_error",
            error_message="Test error",
            invalid_value="invalid"
        )
        report.add_error(error)

        report_dict = report.to_dict()

        assert isinstance(report_dict, dict)
        assert report_dict["is_valid"] == False
        assert len(report_dict["errors"]) == 1
        assert report_dict["metadata"]["test"] == "data"
        assert report_dict["execution_time_ms"] == 150.5
        assert "summary" in report_dict


class TestValidationErrorHandler:
    """Test ValidationErrorHandler class."""

    def test_handler_initialization(self):
        """Test error handler initialization."""
        handler = ValidationErrorHandler()
        assert handler.include_suggestions
        assert handler.include_context
        assert handler.localization == 'en'

        # Test custom initialization
        handler = ValidationErrorHandler(
            include_suggestions=False,
            localization='ru',
            max_error_details=50
        )
        assert not handler.include_suggestions
        assert handler.localization == 'ru'
        assert handler.max_error_details == 50

    def test_pydantic_error_handling(self):
        """Test Pydantic error handling."""
        handler = ValidationErrorHandler()

        # Create invalid data to trigger Pydantic errors
        invalid_data = {
            "name": "A",  # Too short
            "age": -5,    # Negative age
            "email": "not-an-email"  # Invalid email
        }

        try:
            TestModel(**invalid_data)
        except ValidationError as e:
            report = handler.handle_pydantic_error(e, invalid_data)

            assert not report.is_valid
            assert len(report.errors) >= 3  # At least 3 validation errors

            # Check that errors have proper structure
            for error in report.errors:
                assert error.field_name
                assert error.error_message
                assert error.invalid_value is not None

    def test_pydantic_error_with_context(self):
        """Test Pydantic error handling with context."""
        handler = ValidationErrorHandler(include_context=True)

        context = {"user_id": "123", "operation": "create_user"}

        try:
            TestModel(name="", age="not_a_number", email="invalid")
        except ValidationError as e:
            report = handler.handle_pydantic_error(e, context=context)

            # Check that context is included in errors
            for error in report.errors:
                if handler.include_context:
                    assert "user_id" in error.context
                    assert error.context["user_id"] == "123"

    def test_custom_error_handling(self):
        """Test custom error handling."""
        handler = ValidationErrorHandler()

        error = handler.handle_custom_error(
            field_name="custom_field",
            error_message="Custom validation failed",
            invalid_value="bad_value",
            error_type="custom_validation",
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.BUSINESS_LOGIC,
            expected_type="string",
            constraint_info={"min_length": 5},
            context={"custom": "context"}
        )

        assert error.field_name == "custom_field"
        assert error.error_message == "Custom validation failed"
        assert error.severity == ErrorSeverity.HIGH
        assert error.category == ErrorCategory.BUSINESS_LOGIC
        assert error.expected_type == "string"
        assert error.constraint_info["min_length"] == 5

    def test_error_severity_determination(self):
        """Test error severity determination."""
        handler = ValidationErrorHandler()

        # Test critical error detection
        severity = handler._determine_error_severity("security_violation", "injection detected")
        assert severity == ErrorSeverity.CRITICAL

        # Test high error detection
        severity = handler._determine_error_severity("missing_required", "field required")
        assert severity == ErrorSeverity.HIGH

        # Test low error detection
        severity = handler._determine_error_severity("format_issue", "whitespace problem")
        assert severity == ErrorSeverity.LOW

        # Test default medium severity
        severity = handler._determine_error_severity("unknown_error", "generic message")
        assert severity == ErrorSeverity.MEDIUM

    def test_error_category_determination(self):
        """Test error category determination."""
        handler = ValidationErrorHandler()

        # Test type mismatch
        category = handler._determine_error_category("type_error")
        assert category == ErrorCategory.TYPE_MISMATCH

        # Test value error
        category = handler._determine_error_category("value_error")
        assert category == ErrorCategory.VALUE_ERROR

        # Test constraint violation
        category = handler._determine_error_category("string_too_short")
        assert category == ErrorCategory.CONSTRAINT_VIOLATION

        # Test unknown category
        category = handler._determine_error_category("unknown_error_type")
        assert category == ErrorCategory.UNKNOWN

    def test_suggestion_generation(self):
        """Test suggestion generation."""
        handler = ValidationErrorHandler(include_suggestions=True)

        # Test type mismatch suggestions
        suggestions = handler._generate_suggestions(
            "type_error", "not_a_number", "int", None
        )
        assert len(suggestions) > 0
        assert any("convert" in s.lower() for s in suggestions)

        # Test constraint violation suggestions
        constraint_info = {"min_length": 5}
        suggestions = handler._generate_suggestions(
            "string_too_short", "abc", "str", constraint_info
        )
        assert len(suggestions) > 0
        assert any("5" in s for s in suggestions)

    def test_error_message_formatting(self):
        """Test error message formatting."""
        handler = ValidationErrorHandler()

        error = ValidationErrorDetail(
            field_name="test_field",
            field_path="test_field",
            error_type="value_error",
            error_message="Test error message",
            invalid_value="invalid",
            suggestions=["Fix suggestion 1", "Fix suggestion 2"]
        )

        # Test user-friendly formatting
        user_msg = handler.format_error_message(error, "user_friendly")
        assert "❌" in user_msg
        assert "test_field" in user_msg
        assert "💡" in user_msg  # Suggestions section

        # Test technical formatting
        tech_msg = handler.format_error_message(error, "technical")
        assert "[MEDIUM]" in tech_msg  # Severity
        assert "Type:" in tech_msg
        assert "Category:" in tech_msg

        # Test JSON formatting
        json_msg = handler.format_error_message(error, "json")
        assert json_msg.startswith("{")
        assert "field_name" in json_msg

    def test_validation_report_formatting(self):
        """Test validation report formatting."""
        handler = ValidationErrorHandler()

        report = ValidationReport(is_valid=False)
        error = ValidationErrorDetail(
            field_name="test",
            field_path="test",
            error_type="value_error",
            error_message="Test error",
            invalid_value="invalid"
        )
        report.add_error(error)

        # Test summary formatting
        summary = handler.format_validation_report(report, "summary")
        assert "❌ INVALID" in summary
        assert "Errors: 1" in summary

        # Test detailed formatting
        detailed = handler.format_validation_report(report, "detailed")
        assert "DETAILED ERRORS" in detailed

        # Test JSON formatting
        json_report = handler.format_validation_report(report, "json")
        assert json_report.startswith("{")

    def test_localization(self):
        """Test error message localization."""
        # Test Russian localization
        handler = ValidationErrorHandler(localization='ru')

        localized_msg = handler._localize_error_message("field required")
        assert "поле обязательно" in localized_msg

        localized_msg = handler._localize_error_message("invalid email format")
        assert "неверный формат email" in localized_msg

    def test_constraint_info_extraction(self):
        """Test constraint information extraction."""
        handler = ValidationErrorHandler()

        error_dict = {
            "type": "string_too_short",
            "loc": ("name",),
            "msg": "String too short",
            "input": "A",
            "ctx": {"min_length": 2}
        }

        constraint_info = handler._extract_constraint_info(error_dict)
        assert constraint_info is not None
        assert constraint_info["min_length"] == 2

    def test_max_error_details_limit(self):
        """Test maximum error details limit."""
        handler = ValidationErrorHandler(max_error_details=2)

        # Create a model that will generate many errors
        class ManyFieldsModel(BaseModel):
            field1: str = Field(..., min_length=10)
            field2: str = Field(..., min_length=10)
            field3: str = Field(..., min_length=10)
            field4: str = Field(..., min_length=10)

        try:
            ManyFieldsModel(field1="a", field2="b", field3="c", field4="d")
        except ValidationError as e:
            report = handler.handle_pydantic_error(e)

            # Should be limited to max_error_details
            assert len(report.errors) <= handler.max_error_details

    def test_error_processor_registration(self):
        """Test custom error processor registration."""
        handler = ValidationErrorHandler()

        def custom_processor(error_dict, original_data, context):
            return ValidationErrorDetail(
                field_name="custom",
                field_path="custom",
                error_type="custom_type",
                error_message="Custom processed error",
                invalid_value=error_dict.get("input")
            )

        handler.register_error_processor("custom_type", custom_processor)
        assert "custom_type" in handler._custom_processors


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_handle_validation_error(self):
        """Test handle_validation_error convenience function."""
        try:
            TestModel(name="", age=-1, email="invalid")
        except ValidationError as e:
            report = handle_validation_error(e)

            assert isinstance(report, ValidationReport)
            assert not report.is_valid
            assert len(report.errors) > 0

    def test_create_custom_error(self):
        """Test create_custom_error convenience function."""
        error = create_custom_error(
            field_name="test_field",
            error_message="Test error",
            invalid_value="bad_value",
            severity=ErrorSeverity.HIGH
        )

        assert isinstance(error, ValidationErrorDetail)
        assert error.field_name == "test_field"
        assert error.severity == ErrorSeverity.HIGH

    def test_format_error_for_user(self):
        """Test format_error_for_user convenience function."""
        error = ValidationErrorDetail(
            field_name="email",
            field_path="email",
            error_type="format_error",
            error_message="Invalid email format",
            invalid_value="not-an-email",
            suggestions=["Add @ symbol"]
        )

        formatted = format_error_for_user(error)

        assert "❌" in formatted
        assert "email" in formatted
        assert "💡" in formatted


class TestErrorHandlerIntegration:
    """Test error handler integration scenarios."""

    def test_complete_validation_workflow(self):
        """Test complete validation workflow."""
        handler = ValidationErrorHandler(
            include_suggestions=True,
            include_context=True,
            localization='en'
        )

        # Create a complex model with multiple validation rules
        class ComplexModel(BaseModel):
            user_id: str = Field(..., min_length=3, max_length=20)
            email: str
            age: int = Field(..., ge=0, le=120)
            tags: list = Field(default_factory=list, max_items=10)

        invalid_data = {
            "user_id": "ab",  # Too short
            "email": "not-an-email",  # Invalid format
            "age": 150,  # Too high
            "tags": ["tag"] * 15  # Too many items
        }

        context = {
            "request_id": "req_123",
            "user_agent": "test_agent",
            "timestamp": datetime.now().isoformat()
        }

        try:
            ComplexModel(**invalid_data)
        except ValidationError as e:
            report = handler.handle_pydantic_error(e, invalid_data, context)

            # Verify comprehensive error handling
            assert not report.is_valid
            assert len(report.errors) >= 4  # All fields should have errors

            # Check error details
            for error in report.errors:
                assert error.field_name
                assert error.error_message
                assert error.suggestions  # Should have suggestions
                assert error.context  # Should have context
                assert error.severity in ErrorSeverity
                assert error.category in ErrorCategory

            # Test report formatting
            summary = handler.format_validation_report(report, "summary")
            assert "INVALID" in summary

            detailed = handler.format_validation_report(report, "detailed")
            assert "DETAILED ERRORS" in detailed

    def test_multilingual_error_handling(self):
        """Test multilingual error handling."""
        # English handler
        en_handler = ValidationErrorHandler(localization='en')

        # Russian handler
        ru_handler = ValidationErrorHandler(localization='ru')

        try:
            TestModel(name="", age=-1, email="invalid")
        except ValidationError as e:
            en_report = en_handler.handle_pydantic_error(e)
            ru_report = ru_handler.handle_pydantic_error(e)

            # Both should have errors, but messages might be different
            assert len(en_report.errors) == len(ru_report.errors)

            # Check that Russian handler attempts localization
            for en_error, ru_error in zip(en_report.errors, ru_report.errors):
                # Error structure should be the same
                assert en_error.field_name == ru_error.field_name
                assert en_error.severity == ru_error.severity

    def test_performance_with_large_errors(self):
        """Test performance with large number of errors."""
        handler = ValidationErrorHandler(max_error_details=1000)

        # Create a model that could generate many errors
        class LargeModel(BaseModel):
            field1: str = Field(..., min_length=100)
            field2: str = Field(..., min_length=100)
            field3: str = Field(..., min_length=100)

        try:
            LargeModel(field1="short", field2="short", field3="short")
        except ValidationError as e:
            import time
            start_time = time.time()

            report = handler.handle_pydantic_error(e)

            end_time = time.time()
            processing_time = (end_time - start_time) * 1000  # Convert to ms

            # Should process reasonably quickly (< 100ms for simple cases)
            assert processing_time < 1000  # 1 second max
            assert not report.is_valid