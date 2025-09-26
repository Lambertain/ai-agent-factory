"""
Tests for the data normalization system.
"""

import pytest
from datetime import datetime, timezone
from decimal import Decimal

from ..normalizers import (
    DataNormalizer, quick_normalize_text, quick_normalize_email,
    quick_normalize_url, quick_normalize_phone
)


class TestDataNormalizer:
    """Test the main DataNormalizer class."""

    def test_initialization(self):
        """Test normalizer initialization."""
        normalizer = DataNormalizer()
        assert not normalizer.strict_mode
        assert normalizer.auto_fix_errors

        strict_normalizer = DataNormalizer(strict_mode=True)
        assert strict_normalizer.strict_mode

    def test_custom_normalizer_registration(self):
        """Test custom normalizer registration."""
        normalizer = DataNormalizer()

        def custom_validator(value):
            return str(value).upper()

        normalizer.register_normalizer("uppercase", custom_validator)
        assert "uppercase" in normalizer._custom_normalizers


class TestTextNormalization:
    """Test text normalization functions."""

    def test_basic_text_normalization(self):
        """Test basic text cleaning."""
        normalizer = DataNormalizer()

        # Test whitespace normalization
        result = normalizer.normalize_text("  Hello   World  \n\n\n")
        assert result == "Hello World"

        # Test HTML removal
        result = normalizer.normalize_text("<p>Hello <b>World</b></p>", remove_html=True)
        assert result == "Hello World"

        # Test control character removal
        result = normalizer.normalize_text("Hello\x00\x01World")
        assert result == "HelloWorld"

    def test_text_length_limits(self):
        """Test text length limiting."""
        normalizer = DataNormalizer()

        # Test truncation
        long_text = "a" * 1000
        result = normalizer.normalize_text(long_text, max_length=10)
        assert len(result) == 10

        # Test strict mode
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_text(long_text, max_length=10)

    def test_preserve_formatting(self):
        """Test formatting preservation."""
        normalizer = DataNormalizer(preserve_formatting=True)
        text = "Line 1\n  Line 2\n    Line 3"
        result = normalizer.normalize_text(text, normalize_whitespace=False)
        assert "\n" in result

    def test_quick_normalize_text(self):
        """Test quick text normalization function."""
        result = quick_normalize_text("  <p>Hello World</p>  ")
        assert result == "Hello World"


class TestEmailNormalization:
    """Test email normalization functions."""

    def test_valid_email_normalization(self):
        """Test valid email normalization."""
        normalizer = DataNormalizer()

        # Test case normalization
        result = normalizer.normalize_email("USER@EXAMPLE.COM")
        assert result == "user@example.com"

        # Test whitespace removal
        result = normalizer.normalize_email("  user@example.com  ")
        assert result == "user@example.com"

    def test_invalid_email_handling(self):
        """Test invalid email handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return original on failure
        result = normalizer.normalize_email("not-an-email")
        assert result == "not-an-email"

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_email("not-an-email")

    def test_email_auto_fix(self):
        """Test email auto-fixing."""
        normalizer = DataNormalizer(auto_fix_errors=True)

        # Test double dot fixing
        result = normalizer.normalize_email("user..name@example.com")
        # Should attempt to fix common issues

    def test_quick_normalize_email(self):
        """Test quick email normalization function."""
        result = quick_normalize_email("  USER@EXAMPLE.COM  ")
        assert result == "user@example.com"


class TestURLNormalization:
    """Test URL normalization functions."""

    def test_scheme_addition(self):
        """Test automatic scheme addition."""
        normalizer = DataNormalizer()

        result = normalizer.normalize_url("example.com")
        assert result == "https://example.com"

        result = normalizer.normalize_url("example.com", default_scheme="http")
        assert result == "http://example.com"

    def test_url_path_normalization(self):
        """Test URL path normalization."""
        normalizer = DataNormalizer()

        # Test double slash removal
        result = normalizer.normalize_url("https://example.com//path//to//file")
        assert "//path" not in result

        # Test trailing slash removal
        result = normalizer.normalize_url("https://example.com/path/")
        assert result == "https://example.com/path"

    def test_url_case_normalization(self):
        """Test URL case normalization."""
        normalizer = DataNormalizer()

        result = normalizer.normalize_url("HTTPS://EXAMPLE.COM/Path")
        assert result.startswith("https://example.com")

    def test_invalid_url_handling(self):
        """Test invalid URL handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return original on failure
        result = normalizer.normalize_url("not-a-url")
        assert "not-a-url" in result

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_url("not-a-url")

    def test_quick_normalize_url(self):
        """Test quick URL normalization function."""
        result = quick_normalize_url("example.com")
        assert result == "https://example.com"


class TestPhoneNormalization:
    """Test phone number normalization functions."""

    def test_phone_formatting(self):
        """Test phone number formatting."""
        normalizer = DataNormalizer()

        # Test E164 format (default)
        result = normalizer.normalize_phone("+1 (555) 123-4567", "US")
        assert result.startswith("+1")
        assert "(" not in result
        assert ")" not in result
        assert "-" not in result

        # Test international format
        result = normalizer.normalize_phone(
            "+1 555 123 4567", "US", format_style="INTERNATIONAL"
        )
        assert result.startswith("+1")

    def test_country_code_handling(self):
        """Test country code handling."""
        normalizer = DataNormalizer()

        # Test with country code
        result = normalizer.normalize_phone("5551234567", "US")
        assert result.startswith("+1")

        # Test Russian phone
        result = normalizer.normalize_phone("9991234567", "RU")
        assert result.startswith("+7")

    def test_invalid_phone_handling(self):
        """Test invalid phone handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return original
        result = normalizer.normalize_phone("not-a-phone")
        assert result == "not-a-phone"

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_phone("not-a-phone")

    def test_quick_normalize_phone(self):
        """Test quick phone normalization function."""
        result = quick_normalize_phone("(555) 123-4567")
        assert result.startswith("+1")


class TestDateTimeNormalization:
    """Test datetime normalization functions."""

    def test_datetime_string_parsing(self):
        """Test datetime string parsing."""
        normalizer = DataNormalizer()

        # Test ISO format
        result = normalizer.normalize_datetime("2023-01-15T10:30:00Z")
        assert isinstance(result, str)
        assert "2023-01-15" in result

        # Test various formats
        formats_to_test = [
            "2023-01-15 10:30:00",
            "2023-01-15",
            "01/15/2023",
            "15.01.2023"
        ]

        for date_str in formats_to_test:
            result = normalizer.normalize_datetime(date_str)
            assert result is not None

    def test_datetime_timezone_handling(self):
        """Test timezone handling."""
        normalizer = DataNormalizer()

        # Test UTC conversion
        dt = datetime.now()
        result = normalizer.normalize_datetime(dt, target_timezone="UTC")
        assert isinstance(result, str)

    def test_datetime_object_handling(self):
        """Test datetime object handling."""
        normalizer = DataNormalizer()

        dt = datetime.now(timezone.utc)
        result = normalizer.normalize_datetime(dt, iso_format=True)
        assert isinstance(result, str)
        assert "T" in result

        result = normalizer.normalize_datetime(dt, iso_format=False)
        assert isinstance(result, datetime)

    def test_invalid_datetime_handling(self):
        """Test invalid datetime handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return original
        result = normalizer.normalize_datetime("not-a-date")
        assert result == "not-a-date"

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_datetime("not-a-date")


class TestNumericNormalization:
    """Test numeric normalization functions."""

    def test_string_to_numeric_conversion(self):
        """Test string to numeric conversion."""
        normalizer = DataNormalizer()

        # Test integer conversion
        result = normalizer.normalize_numeric("123")
        assert result == 123
        assert isinstance(result, int)

        # Test float conversion
        result = normalizer.normalize_numeric("123.45")
        assert result == 123.45
        assert isinstance(result, float)

        # Test with thousand separators
        result = normalizer.normalize_numeric("1,234.56")
        assert result == 1234.56

    def test_numeric_boundary_checking(self):
        """Test numeric boundary checking."""
        normalizer = DataNormalizer()

        # Test within bounds
        result = normalizer.normalize_numeric(50, min_value=0, max_value=100)
        assert result == 50

        # Test below minimum (non-strict)
        result = normalizer.normalize_numeric(-10, min_value=0)
        assert result == 0  # Should be clamped to minimum

        # Test above maximum (non-strict)
        result = normalizer.normalize_numeric(150, max_value=100)
        assert result == 100  # Should be clamped to maximum

    def test_decimal_precision(self):
        """Test decimal precision handling."""
        normalizer = DataNormalizer()

        result = normalizer.normalize_numeric(3.14159, decimal_places=2)
        assert result == 3.14

    def test_boolean_to_numeric(self):
        """Test boolean to numeric conversion."""
        normalizer = DataNormalizer()

        result = normalizer.normalize_numeric(True)
        assert result == 1

        result = normalizer.normalize_numeric(False)
        assert result == 0

    def test_invalid_numeric_handling(self):
        """Test invalid numeric handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return 0 or try to extract
        result = normalizer.normalize_numeric("not-a-number")
        assert result == 0

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_numeric("not-a-number")


class TestJSONNormalization:
    """Test JSON normalization functions."""

    def test_json_string_parsing(self):
        """Test JSON string parsing."""
        normalizer = DataNormalizer()

        json_str = '{"key": "value", "number": 123}'
        result = normalizer.normalize_json(json_str)
        assert '"key"' in result
        assert '"value"' in result

    def test_json_object_serialization(self):
        """Test JSON object serialization."""
        normalizer = DataNormalizer()

        data = {"key": "value", "number": 123}
        result = normalizer.normalize_json(data, sort_keys=True)
        assert '"key"' in result
        assert '"number"' in result

    def test_json_formatting(self):
        """Test JSON formatting options."""
        normalizer = DataNormalizer()

        data = {"b": 2, "a": 1}

        # Test sorted keys
        result = normalizer.normalize_json(data, sort_keys=True)
        assert result.index('"a"') < result.index('"b"')

        # Test pretty printing
        result = normalizer.normalize_json(data, indent=2)
        assert "\n" in result

    def test_invalid_json_handling(self):
        """Test invalid JSON handling."""
        normalizer = DataNormalizer()

        # Non-strict mode should return original
        result = normalizer.normalize_json("invalid json")
        assert result == "invalid json"

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.normalize_json("invalid json")


class TestCollectionNormalization:
    """Test collection normalization functions."""

    def test_list_normalization(self):
        """Test list normalization."""
        normalizer = DataNormalizer()

        # Test duplicate removal
        result = normalizer.normalize_list([1, 2, 2, 3], remove_duplicates=True)
        assert result == [1, 2, 3]

        # Test empty item removal
        result = normalizer.normalize_list([1, "", None, 2], remove_empty=True)
        assert result == [1, 2]

        # Test sorting
        result = normalizer.normalize_list([3, 1, 2], sort_items=True)
        assert result == [1, 2, 3]

    def test_list_item_normalization(self):
        """Test individual item normalization in lists."""
        normalizer = DataNormalizer()

        def item_normalizer(item):
            return str(item).upper()

        result = normalizer.normalize_list(
            ["hello", "world"], item_normalizer=item_normalizer
        )
        assert result == ["HELLO", "WORLD"]

    def test_dict_normalization(self):
        """Test dictionary normalization."""
        normalizer = DataNormalizer()

        # Test key normalization
        data = {"Key One": "value1", "Key Two": "value2"}
        result = normalizer.normalize_dict(data, normalize_keys=True)

        # Keys should be normalized (lowercase, underscores)
        assert "key_one" in result
        assert "key_two" in result

        # Test null value removal
        data = {"key1": "value", "key2": None, "key3": ""}
        result = normalizer.normalize_dict(data, remove_null_values=True)
        assert "key2" not in result
        assert "key3" not in result

    def test_dict_value_normalization(self):
        """Test dictionary value normalization."""
        normalizer = DataNormalizer()

        def value_normalizer(value):
            return str(value).upper() if value else value

        data = {"key1": "hello", "key2": "world"}
        result = normalizer.normalize_dict(
            data, value_normalizer=value_normalizer
        )
        assert result["key1"] == "HELLO"
        assert result["key2"] == "WORLD"


class TestUniversalDataNormalization:
    """Test universal data normalization."""

    def test_auto_type_detection(self):
        """Test automatic type detection."""
        normalizer = DataNormalizer()

        # Test email detection
        result = normalizer.normalize_data("user@example.com")
        assert result == "user@example.com"

        # Test URL detection
        result = normalizer.normalize_data("http://example.com")
        assert result == "http://example.com"

        # Test phone detection
        result = normalizer.normalize_data("+1234567890")
        assert result.startswith("+")

    def test_explicit_type_specification(self):
        """Test explicit type specification."""
        normalizer = DataNormalizer()

        # Test explicit email type
        result = normalizer.normalize_data("USER@EXAMPLE.COM", data_type="email")
        assert result == "user@example.com"

        # Test explicit numeric type
        result = normalizer.normalize_data("123.45", data_type="numeric")
        assert result == 123.45

    def test_custom_options(self):
        """Test custom normalization options."""
        normalizer = DataNormalizer()

        options = {"min_length": 5, "max_length": 10}
        result = normalizer.normalize_data(
            "Hello World", data_type="text", custom_options=options
        )
        assert len(result) <= 10


class TestBatchNormalization:
    """Test batch normalization functions."""

    def test_batch_normalization(self):
        """Test batch data normalization."""
        normalizer = DataNormalizer()

        data_batch = [
            {"email": "USER@EXAMPLE.COM", "age": "25"},
            {"email": "test@test.com", "age": "30"}
        ]

        field_types = {"email": "email", "age": "numeric"}

        result = normalizer.batch_normalize(data_batch, field_types)

        assert len(result) == 2
        assert result[0]["email"] == "user@example.com"
        assert result[0]["age"] == 25
        assert result[1]["age"] == 30

    def test_batch_with_field_options(self):
        """Test batch normalization with field options."""
        normalizer = DataNormalizer()

        data_batch = [
            {"text": "  Hello World  ", "number": "123.456"}
        ]

        field_types = {"text": "text", "number": "numeric"}
        field_options = {
            "text": {"max_length": 5},
            "number": {"decimal_places": 1}
        }

        result = normalizer.batch_normalize(
            data_batch, field_types, field_options
        )

        assert len(result[0]["text"]) <= 5
        assert result[0]["number"] == 123.5

    def test_batch_error_handling(self):
        """Test batch normalization error handling."""
        normalizer = DataNormalizer()

        data_batch = [
            {"field": "valid_value"},
            "invalid_item",  # Not a dict
            {"field": "another_value"}
        ]

        # Non-strict mode should skip invalid items
        result = normalizer.batch_normalize(data_batch)
        assert len(result) == 2

        # Strict mode should raise error
        strict_normalizer = DataNormalizer(strict_mode=True)
        with pytest.raises(ValueError):
            strict_normalizer.batch_normalize(data_batch)


class TestNormalizationReporting:
    """Test normalization reporting functions."""

    def test_normalization_report(self):
        """Test normalization report generation."""
        normalizer = DataNormalizer()

        original = "  HELLO WORLD  "
        normalized = normalizer.normalize_text(original)

        report = normalizer.get_normalization_report(original, normalized)

        assert "original_type" in report
        assert "normalized_type" in report
        assert "changes_detected" in report
        assert report["changes_detected"] == True

    def test_string_specific_report(self):
        """Test string-specific report details."""
        normalizer = DataNormalizer()

        original = "  Hello   World  "
        normalized = normalizer.normalize_text(original)

        report = normalizer.get_normalization_report(original, normalized)

        assert "details" in report
        assert "length_change" in report["details"]
        assert "whitespace_normalized" in report["details"]

    def test_list_specific_report(self):
        """Test list-specific report details."""
        normalizer = DataNormalizer()

        original = [1, 2, 2, 3]
        normalized = normalizer.normalize_list(original, remove_duplicates=True)

        report = normalizer.get_normalization_report(original, normalized)

        assert "details" in report
        assert "count_change" in report["details"]

    def test_dict_specific_report(self):
        """Test dict-specific report details."""
        normalizer = DataNormalizer()

        original = {"Key One": "value", "key_two": None}
        normalized = normalizer.normalize_dict(original, remove_null_values=True)

        report = normalizer.get_normalization_report(original, normalized)

        assert "details" in report
        assert "keys_change" in report["details"]