"""
Pytest configuration and fixtures for validation tests.
"""

import pytest
from datetime import datetime, timezone
from typing import Dict, Any

from ..validators import EmailValidator, SearchRequestValidator
from ..normalizers import DataNormalizer
from ..error_handler import ValidationErrorHandler, ValidationErrorDetail, ErrorSeverity, ErrorCategory


@pytest.fixture
def sample_email_validator():
    """Fixture providing a sample email validator."""
    return EmailValidator(email="test@example.com")


@pytest.fixture
def sample_search_request():
    """Fixture providing a sample search request validator."""
    return SearchRequestValidator(
        query="test search query",
        search_type="semantic",
        limit=10,
        filters={"category": "documents"}
    )


@pytest.fixture
def data_normalizer():
    """Fixture providing a data normalizer instance."""
    return DataNormalizer(
        strict_mode=False,
        auto_fix_errors=True,
        preserve_formatting=False
    )


@pytest.fixture
def strict_data_normalizer():
    """Fixture providing a strict data normalizer instance."""
    return DataNormalizer(
        strict_mode=True,
        auto_fix_errors=False,
        preserve_formatting=False
    )


@pytest.fixture
def error_handler():
    """Fixture providing an error handler instance."""
    return ValidationErrorHandler(
        include_suggestions=True,
        include_context=True,
        localization='en',
        max_error_details=100
    )


@pytest.fixture
def russian_error_handler():
    """Fixture providing a Russian localized error handler."""
    return ValidationErrorHandler(
        include_suggestions=True,
        include_context=True,
        localization='ru',
        max_error_details=100
    )


@pytest.fixture
def sample_validation_error():
    """Fixture providing a sample validation error detail."""
    return ValidationErrorDetail(
        field_name="test_field",
        field_path="root.test_field",
        error_type="value_error",
        error_message="Sample validation error",
        invalid_value="invalid_data",
        expected_type="string",
        constraint_info={"min_length": 5, "max_length": 50},
        suggestions=["Check the input format", "Ensure minimum length"],
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.VALUE_ERROR,
        context={"request_id": "test_req_123", "user_id": "test_user"}
    )


@pytest.fixture
def sample_invalid_data():
    """Fixture providing sample invalid data for testing."""
    return {
        "email": "not-an-email",
        "age": "not_a_number",
        "name": "",
        "url": "not-a-url",
        "phone": "123",
        "text_with_html": "<script>alert('xss')</script>",
        "negative_number": -5,
        "future_date": "2025-12-31",
        "past_date": "1900-01-01"
    }


@pytest.fixture
def sample_valid_data():
    """Fixture providing sample valid data for testing."""
    return {
        "email": "user@example.com",
        "age": 25,
        "name": "John Doe",
        "url": "https://example.com",
        "phone": "+1234567890",
        "text": "Valid text content",
        "positive_number": 42,
        "current_date": datetime.now(timezone.utc).isoformat()
    }


@pytest.fixture
def sample_batch_data():
    """Fixture providing sample batch data for testing."""
    return [
        {
            "id": 1,
            "email": "USER1@EXAMPLE.COM",
            "age": "25",
            "name": "  John Doe  ",
            "tags": ["python", "ai", "python"]  # Has duplicate
        },
        {
            "id": 2,
            "email": "user2@example.com",
            "age": "30",
            "name": "Jane Smith",
            "tags": ["javascript", "web"]
        },
        {
            "id": 3,
            "email": "INVALID-EMAIL",
            "age": "invalid_age",
            "name": "",
            "tags": []
        }
    ]


@pytest.fixture
def field_type_mapping():
    """Fixture providing field type mapping for batch processing."""
    return {
        "email": "email",
        "age": "numeric",
        "name": "text",
        "tags": "list"
    }


@pytest.fixture
def field_options_mapping():
    """Fixture providing field options for batch processing."""
    return {
        "name": {
            "min_length": 2,
            "max_length": 100,
            "strip_whitespace": True
        },
        "age": {
            "min_value": 0,
            "max_value": 150
        },
        "tags": {
            "remove_duplicates": True,
            "remove_empty": True,
            "max_size": 10
        }
    }


@pytest.fixture
def complex_nested_data():
    """Fixture providing complex nested data structure."""
    return {
        "user": {
            "personal": {
                "name": "  John DOE  ",
                "email": "JOHN@EXAMPLE.COM",
                "age": "25"
            },
            "contact": {
                "phone": "(555) 123-4567",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zip": "12345"
                }
            }
        },
        "preferences": {
            "notifications": True,
            "theme": "dark",
            "languages": ["en", "es", "en"]  # Duplicate
        },
        "metadata": {
            "created_at": "2023-01-15T10:30:00Z",
            "last_login": "2023-12-01 14:22:33",
            "session_count": "42"
        }
    }


@pytest.fixture
def security_test_inputs():
    """Fixture providing inputs for security testing."""
    return {
        "xss_attempts": [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "<iframe src='javascript:alert(\"xss\")'></iframe>"
        ],
        "sql_injection_attempts": [
            "'; DROP TABLE users; --",
            "admin' OR '1'='1",
            "1 UNION SELECT * FROM passwords",
            "1; DELETE FROM users WHERE 1=1; --"
        ],
        "path_traversal_attempts": [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ],
        "command_injection_attempts": [
            "; rm -rf /",
            "| cat /etc/passwd",
            "`whoami`",
            "$(ls -la)"
        ]
    }


@pytest.fixture
def performance_test_data():
    """Fixture providing data for performance testing."""
    return {
        "large_text": "A" * 10000,  # 10KB text
        "large_list": list(range(1000)),  # 1000 items
        "large_dict": {f"key_{i}": f"value_{i}" for i in range(500)},  # 500 key-value pairs
        "deeply_nested": {
            f"level_{i}": {
                f"sublevel_{j}": f"value_{i}_{j}"
                for j in range(10)
            }
            for i in range(10)
        }
    }


@pytest.fixture
def multilingual_test_data():
    """Fixture providing multilingual test data."""
    return {
        "english": {
            "text": "Hello World",
            "error_message": "field required",
            "validation_failed": "Validation failed"
        },
        "russian": {
            "text": "Привет Мир",
            "error_message": "поле обязательно",
            "validation_failed": "Ошибка валидации"
        },
        "chinese": {
            "text": "你好世界",
            "error_message": "字段必需",
            "validation_failed": "验证失败"
        },
        "arabic": {
            "text": "مرحبا بالعالم",
            "error_message": "الحقل مطلوب",
            "validation_failed": "فشل التحقق"
        },
        "emoji": {
            "text": "Hello 🌍 World 🚀",
            "error_message": "Invalid format 😞",
            "validation_failed": "Failed ❌"
        }
    }


# Helper functions for tests
@pytest.fixture
def create_test_error():
    """Fixture providing a function to create test errors."""
    def _create_error(
        field_name: str = "test_field",
        error_type: str = "value_error",
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.VALUE_ERROR,
        **kwargs
    ) -> ValidationErrorDetail:
        defaults = {
            "field_path": field_name,
            "error_message": f"Test error for {field_name}",
            "invalid_value": "test_invalid_value",
            "suggestions": [f"Fix {field_name}"],
            "context": {"test": True}
        }
        defaults.update(kwargs)

        return ValidationErrorDetail(
            field_name=field_name,
            error_type=error_type,
            severity=severity,
            category=category,
            **defaults
        )

    return _create_error


@pytest.fixture
def validation_test_cases():
    """Fixture providing common validation test cases."""
    return {
        "email_tests": {
            "valid": [
                "user@example.com",
                "test.email@domain.co.uk",
                "user+tag@subdomain.example.org"
            ],
            "invalid": [
                "not-an-email",
                "@domain.com",
                "user@",
                "user space@domain.com"
            ]
        },
        "url_tests": {
            "valid": [
                "https://example.com",
                "http://subdomain.example.org/path",
                "https://example.com:8080/path?query=value"
            ],
            "invalid": [
                "not-a-url",
                "ftp://example.com",  # If not in allowed schemes
                "just-text"
            ]
        },
        "phone_tests": {
            "valid": [
                "+1234567890",
                "+79991234567",
                "(555) 123-4567"
            ],
            "invalid": [
                "not-a-phone",
                "123",
                "abcdefghij"
            ]
        },
        "numeric_tests": {
            "valid": [
                42,
                3.14159,
                "123",
                "45.67"
            ],
            "invalid": [
                "not-a-number",
                "12.34.56",
                "infinity"
            ]
        }
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security-related"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance-related"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add slow marker to tests that might be slow
        if "performance" in item.name or "large" in item.name:
            item.add_marker(pytest.mark.slow)

        # Add security marker to security tests
        if "security" in item.name or "xss" in item.name or "injection" in item.name:
            item.add_marker(pytest.mark.security)

        # Add integration marker to integration tests
        if "integration" in item.name or "workflow" in item.name:
            item.add_marker(pytest.mark.integration)