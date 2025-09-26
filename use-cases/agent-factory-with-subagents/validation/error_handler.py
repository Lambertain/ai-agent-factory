"""
Comprehensive error handling and detailed validation error messaging system.
"""

import json
import traceback
from typing import Any, Dict, List, Optional, Union, Type, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from pydantic import ValidationError, BaseModel
import logging


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    TYPE_MISMATCH = "type_mismatch"
    VALUE_ERROR = "value_error"
    CONSTRAINT_VIOLATION = "constraint_violation"
    FORMAT_ERROR = "format_error"
    SECURITY_VIOLATION = "security_violation"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM_ERROR = "system_error"
    UNKNOWN = "unknown"


@dataclass
class ValidationErrorDetail:
    """Detailed validation error information."""
    field_name: str
    field_path: str
    error_type: str
    error_message: str
    invalid_value: Any
    expected_type: Optional[str] = None
    constraint_info: Optional[Dict[str, Any]] = None
    suggestions: List[str] = field(default_factory=list)
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.VALUE_ERROR
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'field_name': self.field_name,
            'field_path': self.field_path,
            'error_type': self.error_type,
            'error_message': self.error_message,
            'invalid_value': str(self.invalid_value)[:100],  # Truncate long values
            'expected_type': self.expected_type,
            'constraint_info': self.constraint_info,
            'suggestions': self.suggestions,
            'severity': self.severity.value,
            'category': self.category.value,
            'context': self.context,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    is_valid: bool
    errors: List[ValidationErrorDetail] = field(default_factory=list)
    warnings: List[ValidationErrorDetail] = field(default_factory=list)
    corrected_data: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: Optional[float] = None

    def add_error(self, error: ValidationErrorDetail):
        """Add validation error."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: ValidationErrorDetail):
        """Add validation warning."""
        self.warnings.append(warning)

    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ValidationErrorDetail]:
        """Get errors filtered by severity."""
        return [error for error in self.errors if error.severity == severity]

    def get_errors_by_category(self, category: ErrorCategory) -> List[ValidationErrorDetail]:
        """Get errors filtered by category."""
        return [error for error in self.errors if error.category == category]

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        return {
            'is_valid': self.is_valid,
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'error_breakdown': {
                'critical': len(self.get_errors_by_severity(ErrorSeverity.CRITICAL)),
                'high': len(self.get_errors_by_severity(ErrorSeverity.HIGH)),
                'medium': len(self.get_errors_by_severity(ErrorSeverity.MEDIUM)),
                'low': len(self.get_errors_by_severity(ErrorSeverity.LOW))
            },
            'category_breakdown': {
                category.value: len(self.get_errors_by_category(category))
                for category in ErrorCategory
            },
            'execution_time_ms': self.execution_time_ms,
            'metadata': self.metadata
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'is_valid': self.is_valid,
            'errors': [error.to_dict() for error in self.errors],
            'warnings': [warning.to_dict() for warning in self.warnings],
            'corrected_data': self.corrected_data,
            'metadata': self.metadata,
            'execution_time_ms': self.execution_time_ms,
            'summary': self.get_summary()
        }


class ValidationErrorHandler:
    """
    Comprehensive validation error handler with detailed error messaging,
    suggestions, and integration capabilities.
    """

    def __init__(self,
                 include_suggestions: bool = True,
                 include_context: bool = True,
                 localization: str = 'en',
                 max_error_details: int = 100,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize the error handler.

        Args:
            include_suggestions: Include fix suggestions in error messages
            include_context: Include context information in errors
            localization: Language for error messages ('en', 'ru', etc.)
            max_error_details: Maximum number of error details to collect
            logger: Logger instance for error logging
        """
        self.include_suggestions = include_suggestions
        self.include_context = include_context
        self.localization = localization
        self.max_error_details = max_error_details
        self.logger = logger or logging.getLogger(__name__)

        # Error message templates
        self._error_templates = self._load_error_templates()

        # Suggestion generators
        self._suggestion_generators: Dict[str, Callable] = {
            'type_mismatch': self._generate_type_suggestions,
            'value_error': self._generate_value_suggestions,
            'constraint_violation': self._generate_constraint_suggestions,
            'format_error': self._generate_format_suggestions,
            'security_violation': self._generate_security_suggestions
        }

        # Custom error processors
        self._custom_processors: Dict[str, Callable] = {}

    def register_error_processor(self, error_type: str, processor: Callable):
        """Register custom error processor."""
        self._custom_processors[error_type] = processor

    def handle_pydantic_error(self,
                             pydantic_error: ValidationError,
                             original_data: Optional[Any] = None,
                             context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """
        Handle Pydantic validation errors with detailed analysis.

        Args:
            pydantic_error: Pydantic ValidationError
            original_data: Original data that caused the error
            context: Additional context information

        Returns:
            Detailed validation report
        """
        report = ValidationReport(is_valid=False)
        context = context or {}

        try:
            for error_dict in pydantic_error.errors():
                error_detail = self._process_pydantic_error_dict(
                    error_dict, original_data, context
                )
                report.add_error(error_detail)

                # Limit number of errors to prevent memory issues
                if len(report.errors) >= self.max_error_details:
                    break

        except Exception as e:
            self.logger.error(f"Error processing Pydantic validation error: {str(e)}")
            # Add fallback error
            fallback_error = ValidationErrorDetail(
                field_name="unknown",
                field_path="unknown",
                error_type="system_error",
                error_message=f"Error processing validation: {str(e)}",
                invalid_value=original_data,
                severity=ErrorSeverity.HIGH,
                category=ErrorCategory.SYSTEM_ERROR
            )
            report.add_error(fallback_error)

        return report

    def handle_custom_error(self,
                           field_name: str,
                           error_message: str,
                           invalid_value: Any,
                           error_type: str = "custom_error",
                           severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                           category: ErrorCategory = ErrorCategory.VALUE_ERROR,
                           expected_type: Optional[str] = None,
                           constraint_info: Optional[Dict[str, Any]] = None,
                           context: Optional[Dict[str, Any]] = None) -> ValidationErrorDetail:
        """
        Handle custom validation errors.

        Args:
            field_name: Name of the field that failed validation
            error_message: Error message
            invalid_value: Value that caused the error
            error_type: Type of error
            severity: Error severity
            category: Error category
            expected_type: Expected data type
            constraint_info: Information about constraint that was violated
            context: Additional context

        Returns:
            Detailed validation error
        """
        context = context or {}

        # Generate suggestions if enabled
        suggestions = []
        if self.include_suggestions:
            suggestions = self._generate_suggestions(
                error_type, invalid_value, expected_type, constraint_info
            )

        # Create detailed error
        error_detail = ValidationErrorDetail(
            field_name=field_name,
            field_path=field_name,
            error_type=error_type,
            error_message=self._localize_error_message(error_message),
            invalid_value=invalid_value,
            expected_type=expected_type,
            constraint_info=constraint_info,
            suggestions=suggestions,
            severity=severity,
            category=category,
            context=context if self.include_context else {}
        )

        return error_detail

    def create_validation_report(self,
                                errors: List[ValidationErrorDetail],
                                warnings: Optional[List[ValidationErrorDetail]] = None,
                                corrected_data: Optional[Any] = None,
                                metadata: Optional[Dict[str, Any]] = None,
                                execution_time_ms: Optional[float] = None) -> ValidationReport:
        """
        Create a comprehensive validation report.

        Args:
            errors: List of validation errors
            warnings: List of validation warnings
            corrected_data: Data after correction (if any)
            metadata: Additional metadata
            execution_time_ms: Execution time in milliseconds

        Returns:
            Validation report
        """
        report = ValidationReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings or [],
            corrected_data=corrected_data,
            metadata=metadata or {},
            execution_time_ms=execution_time_ms
        )

        return report

    def format_error_message(self,
                            error: ValidationErrorDetail,
                            format_type: str = "user_friendly") -> str:
        """
        Format error message for different audiences.

        Args:
            error: Validation error detail
            format_type: Type of formatting ('user_friendly', 'technical', 'json')

        Returns:
            Formatted error message
        """
        if format_type == "user_friendly":
            return self._format_user_friendly_message(error)
        elif format_type == "technical":
            return self._format_technical_message(error)
        elif format_type == "json":
            return json.dumps(error.to_dict(), indent=2, ensure_ascii=False)
        else:
            return error.error_message

    def format_validation_report(self,
                                report: ValidationReport,
                                format_type: str = "summary",
                                include_suggestions: bool = True) -> str:
        """
        Format validation report for display.

        Args:
            report: Validation report
            format_type: Type of formatting ('summary', 'detailed', 'json')
            include_suggestions: Include suggestions in output

        Returns:
            Formatted report
        """
        if format_type == "json":
            return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
        elif format_type == "summary":
            return self._format_summary_report(report)
        elif format_type == "detailed":
            return self._format_detailed_report(report, include_suggestions)
        else:
            return str(report.get_summary())

    def _process_pydantic_error_dict(self,
                                    error_dict: Dict[str, Any],
                                    original_data: Optional[Any],
                                    context: Dict[str, Any]) -> ValidationErrorDetail:
        """Process individual Pydantic error dictionary."""
        # Extract error information
        field_path = ".".join(str(loc) for loc in error_dict.get('loc', []))
        field_name = str(error_dict.get('loc', ['unknown'])[-1])
        error_type = error_dict.get('type', 'unknown')
        error_message = error_dict.get('msg', 'Validation failed')
        invalid_value = error_dict.get('input')

        # Determine severity and category
        severity = self._determine_error_severity(error_type, error_message)
        category = self._determine_error_category(error_type)

        # Extract constraint information
        constraint_info = self._extract_constraint_info(error_dict)

        # Generate suggestions
        suggestions = []
        if self.include_suggestions:
            suggestions = self._generate_suggestions(
                error_type, invalid_value, None, constraint_info
            )

        # Add context
        error_context = context.copy() if self.include_context else {}
        error_context.update({
            'original_data_type': type(original_data).__name__ if original_data else None,
            'pydantic_error_type': error_type
        })

        return ValidationErrorDetail(
            field_name=field_name,
            field_path=field_path,
            error_type=error_type,
            error_message=self._localize_error_message(error_message),
            invalid_value=invalid_value,
            constraint_info=constraint_info,
            suggestions=suggestions,
            severity=severity,
            category=category,
            context=error_context
        )

    def _determine_error_severity(self, error_type: str, error_message: str) -> ErrorSeverity:
        """Determine error severity based on type and message."""
        critical_patterns = ['security', 'injection', 'overflow', 'critical']
        high_patterns = ['required', 'missing', 'invalid_type', 'constraint']
        low_patterns = ['format', 'whitespace', 'case']

        error_text = f"{error_type} {error_message}".lower()

        if any(pattern in error_text for pattern in critical_patterns):
            return ErrorSeverity.CRITICAL
        elif any(pattern in error_text for pattern in high_patterns):
            return ErrorSeverity.HIGH
        elif any(pattern in error_text for pattern in low_patterns):
            return ErrorSeverity.LOW
        else:
            return ErrorSeverity.MEDIUM

    def _determine_error_category(self, error_type: str) -> ErrorCategory:
        """Determine error category based on type."""
        category_mapping = {
            'type_error': ErrorCategory.TYPE_MISMATCH,
            'value_error': ErrorCategory.VALUE_ERROR,
            'assertion_error': ErrorCategory.CONSTRAINT_VIOLATION,
            'json_invalid': ErrorCategory.FORMAT_ERROR,
            'string_type': ErrorCategory.TYPE_MISMATCH,
            'int_type': ErrorCategory.TYPE_MISMATCH,
            'float_type': ErrorCategory.TYPE_MISMATCH,
            'bool_type': ErrorCategory.TYPE_MISMATCH,
            'missing': ErrorCategory.VALUE_ERROR,
            'extra_forbidden': ErrorCategory.CONSTRAINT_VIOLATION,
            'string_too_short': ErrorCategory.CONSTRAINT_VIOLATION,
            'string_too_long': ErrorCategory.CONSTRAINT_VIOLATION,
            'too_small': ErrorCategory.CONSTRAINT_VIOLATION,
            'too_large': ErrorCategory.CONSTRAINT_VIOLATION,
        }

        return category_mapping.get(error_type, ErrorCategory.UNKNOWN)

    def _extract_constraint_info(self, error_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract constraint information from error dictionary."""
        constraint_info = {}

        # Extract limit information
        if 'ctx' in error_dict:
            ctx = error_dict['ctx']
            for key in ['limit_value', 'min_length', 'max_length', 'ge', 'le', 'gt', 'lt']:
                if key in ctx:
                    constraint_info[key] = ctx[key]

        return constraint_info if constraint_info else None

    def _generate_suggestions(self,
                             error_type: str,
                             invalid_value: Any,
                             expected_type: Optional[str],
                             constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for fixing the error."""
        suggestions = []

        # Use registered suggestion generator
        category = self._determine_error_category(error_type).value
        if category in self._suggestion_generators:
            try:
                suggestions = self._suggestion_generators[category](
                    invalid_value, expected_type, constraint_info
                )
            except Exception as e:
                self.logger.warning(f"Error generating suggestions: {str(e)}")

        return suggestions

    def _generate_type_suggestions(self,
                                  invalid_value: Any,
                                  expected_type: Optional[str],
                                  constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for type mismatch errors."""
        suggestions = []
        value_type = type(invalid_value).__name__

        if expected_type:
            suggestions.append(f"Convert {value_type} to {expected_type}")

            # Type-specific suggestions
            if expected_type == 'int' and isinstance(invalid_value, str):
                suggestions.append("Remove non-numeric characters and convert to integer")
            elif expected_type == 'float' and isinstance(invalid_value, str):
                suggestions.append("Ensure string represents a valid decimal number")
            elif expected_type == 'str':
                suggestions.append(f"Convert {value_type} to string using str() function")
            elif expected_type == 'bool':
                suggestions.append("Use true/false, 1/0, or yes/no values")

        return suggestions

    def _generate_value_suggestions(self,
                                   invalid_value: Any,
                                   expected_type: Optional[str],
                                   constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for value errors."""
        suggestions = []

        if isinstance(invalid_value, str):
            if not invalid_value.strip():
                suggestions.append("Provide a non-empty value")
            else:
                suggestions.append("Check for spelling errors or invalid characters")

        if constraint_info:
            if 'min_length' in constraint_info:
                min_len = constraint_info['min_length']
                current_len = len(str(invalid_value)) if invalid_value else 0
                suggestions.append(f"Value must be at least {min_len} characters long (current: {current_len})")

        return suggestions

    def _generate_constraint_suggestions(self,
                                        invalid_value: Any,
                                        expected_type: Optional[str],
                                        constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for constraint violations."""
        suggestions = []

        if constraint_info:
            if 'limit_value' in constraint_info:
                limit = constraint_info['limit_value']
                suggestions.append(f"Value must not exceed {limit}")

            if 'min_length' in constraint_info:
                min_len = constraint_info['min_length']
                suggestions.append(f"Add more characters to reach minimum length of {min_len}")

            if 'max_length' in constraint_info:
                max_len = constraint_info['max_length']
                current_len = len(str(invalid_value)) if invalid_value else 0
                if current_len > max_len:
                    suggestions.append(f"Remove {current_len - max_len} characters to meet maximum length of {max_len}")

        return suggestions

    def _generate_format_suggestions(self,
                                    invalid_value: Any,
                                    expected_type: Optional[str],
                                    constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for format errors."""
        suggestions = []

        if isinstance(invalid_value, str):
            # Email format suggestions
            if '@' in str(invalid_value) and '.' not in str(invalid_value).split('@')[-1]:
                suggestions.append("Add a valid domain extension (e.g., .com, .org)")

            # URL format suggestions
            if 'http' in str(invalid_value).lower() and not str(invalid_value).startswith(('http://', 'https://')):
                suggestions.append("Ensure URL starts with http:// or https://")

            # Date format suggestions
            if any(char.isdigit() for char in str(invalid_value)) and len(str(invalid_value)) > 6:
                suggestions.append("Use ISO format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")

        return suggestions

    def _generate_security_suggestions(self,
                                      invalid_value: Any,
                                      expected_type: Optional[str],
                                      constraint_info: Optional[Dict[str, Any]]) -> List[str]:
        """Generate suggestions for security violations."""
        suggestions = [
            "Remove potentially dangerous characters or patterns",
            "Use only alphanumeric characters and safe symbols",
            "Avoid script tags, SQL keywords, and command injection patterns"
        ]
        return suggestions

    def _load_error_templates(self) -> Dict[str, str]:
        """Load localized error message templates."""
        templates = {
            'en': {
                'type_mismatch': "Expected {expected_type}, but received {actual_type}",
                'value_error': "Invalid value: {value}",
                'constraint_violation': "Value violates constraint: {constraint}",
                'format_error': "Invalid format for {field_name}",
                'security_violation': "Security violation detected in {field_name}",
                'missing_field': "Required field {field_name} is missing",
                'unknown_error': "An unknown validation error occurred"
            },
            'ru': {
                'type_mismatch': "Ожидался {expected_type}, но получен {actual_type}",
                'value_error': "Недопустимое значение: {value}",
                'constraint_violation': "Значение нарушает ограничение: {constraint}",
                'format_error': "Неверный формат для {field_name}",
                'security_violation': "Обнаружено нарушение безопасности в {field_name}",
                'missing_field': "Обязательное поле {field_name} отсутствует",
                'unknown_error': "Произошла неизвестная ошибка валидации"
            }
        }
        return templates.get(self.localization, templates['en'])

    def _localize_error_message(self, message: str) -> str:
        """Localize error message if translation is available."""
        # Simple localization - in real implementation, use proper i18n library
        if self.localization == 'ru':
            translations = {
                'field required': 'поле обязательно',
                'value is not a valid': 'значение не является допустимым',
                'string too short': 'строка слишком короткая',
                'string too long': 'строка слишком длинная',
                'value is not a valid integer': 'значение не является допустимым целым числом',
                'value is not a valid float': 'значение не является допустимым числом с плавающей точкой',
                'invalid email format': 'неверный формат email',
                'invalid url format': 'неверный формат URL'
            }
            for en_text, ru_text in translations.items():
                if en_text in message.lower():
                    message = message.lower().replace(en_text, ru_text)

        return message

    def _format_user_friendly_message(self, error: ValidationErrorDetail) -> str:
        """Format error message for end users."""
        message = f"❌ {error.field_name}: {error.error_message}"

        if error.suggestions:
            message += "\n💡 Suggestions:"
            for suggestion in error.suggestions[:3]:  # Limit to top 3 suggestions
                message += f"\n  • {suggestion}"

        return message

    def _format_technical_message(self, error: ValidationErrorDetail) -> str:
        """Format error message for developers."""
        message = f"[{error.severity.value.upper()}] {error.field_path}: {error.error_message}"
        message += f"\n  Type: {error.error_type}"
        message += f"\n  Category: {error.category.value}"
        message += f"\n  Invalid Value: {error.invalid_value}"

        if error.expected_type:
            message += f"\n  Expected Type: {error.expected_type}"

        if error.constraint_info:
            message += f"\n  Constraint Info: {error.constraint_info}"

        if error.suggestions:
            message += f"\n  Suggestions: {', '.join(error.suggestions)}"

        return message

    def _format_summary_report(self, report: ValidationReport) -> str:
        """Format validation report summary."""
        summary = report.get_summary()

        message = f"Validation Result: {'✅ VALID' if report.is_valid else '❌ INVALID'}\n"
        message += f"Errors: {summary['total_errors']}, Warnings: {summary['total_warnings']}\n"

        if summary['total_errors'] > 0:
            message += "\nError Breakdown:\n"
            for severity, count in summary['error_breakdown'].items():
                if count > 0:
                    message += f"  {severity.upper()}: {count}\n"

        if summary['execution_time_ms']:
            message += f"\nExecution Time: {summary['execution_time_ms']:.2f}ms"

        return message

    def _format_detailed_report(self, report: ValidationReport, include_suggestions: bool) -> str:
        """Format detailed validation report."""
        message = self._format_summary_report(report)

        if report.errors:
            message += "\n\n📋 DETAILED ERRORS:\n"
            for i, error in enumerate(report.errors, 1):
                message += f"\n{i}. {self._format_user_friendly_message(error)}\n"

        if report.warnings:
            message += "\n\n⚠️  WARNINGS:\n"
            for i, warning in enumerate(report.warnings, 1):
                message += f"\n{i}. {self._format_user_friendly_message(warning)}\n"

        return message


# Convenience functions
def handle_validation_error(error: ValidationError,
                           original_data: Optional[Any] = None,
                           context: Optional[Dict[str, Any]] = None) -> ValidationReport:
    """Quick validation error handling."""
    handler = ValidationErrorHandler()
    return handler.handle_pydantic_error(error, original_data, context)


def create_custom_error(field_name: str,
                       error_message: str,
                       invalid_value: Any,
                       **kwargs) -> ValidationErrorDetail:
    """Quick custom error creation."""
    handler = ValidationErrorHandler()
    return handler.handle_custom_error(field_name, error_message, invalid_value, **kwargs)


def format_error_for_user(error: ValidationErrorDetail) -> str:
    """Quick user-friendly error formatting."""
    handler = ValidationErrorHandler()
    return handler.format_error_message(error, "user_friendly")


# Export main classes and functions
__all__ = [
    'ErrorSeverity',
    'ErrorCategory',
    'ValidationErrorDetail',
    'ValidationReport',
    'ValidationErrorHandler',
    'handle_validation_error',
    'create_custom_error',
    'format_error_for_user'
]