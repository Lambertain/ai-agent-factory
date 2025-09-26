"""
Automatic data normalization system for AI Agent Factory.
Provides comprehensive data cleaning, formatting, and standardization.
"""

import re
import json
import unicodedata
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException

from .schemas import NORMALIZATION_PATTERNS, REGEX_PATTERNS


class DataNormalizer:
    """
    Comprehensive data normalization system.
    Automatically cleans, formats, and standardizes various data types.
    """

    def __init__(self,
                 strict_mode: bool = False,
                 preserve_formatting: bool = False,
                 auto_fix_errors: bool = True):
        """
        Initialize the data normalizer.

        Args:
            strict_mode: If True, raises errors on invalid data instead of attempting fixes
            preserve_formatting: If True, preserves original formatting where possible
            auto_fix_errors: If True, attempts to automatically fix common data issues
        """
        self.strict_mode = strict_mode
        self.preserve_formatting = preserve_formatting
        self.auto_fix_errors = auto_fix_errors

        # Custom normalizers registry
        self._custom_normalizers: Dict[str, Callable] = {}

    def register_normalizer(self, data_type: str, normalizer: Callable):
        """Register a custom normalizer for a specific data type."""
        self._custom_normalizers[data_type] = normalizer

    def normalize_text(self,
                      text: str,
                      remove_html: bool = True,
                      normalize_whitespace: bool = True,
                      remove_control_chars: bool = True,
                      strip_edges: bool = True,
                      max_length: Optional[int] = None) -> str:
        """
        Normalize text content with various cleaning options.

        Args:
            text: Input text to normalize
            remove_html: Remove HTML tags
            normalize_whitespace: Normalize whitespace characters
            remove_control_chars: Remove Unicode control characters
            strip_edges: Strip leading/trailing whitespace
            max_length: Maximum allowed length (truncates if exceeded)

        Returns:
            Normalized text string
        """
        if not isinstance(text, str):
            if self.strict_mode:
                raise ValueError(f"Expected string, got {type(text)}")
            text = str(text)

        # Remove HTML tags
        if remove_html:
            text = NORMALIZATION_PATTERNS['html_tags'].sub('', text)

        # Remove control characters
        if remove_control_chars:
            text = NORMALIZATION_PATTERNS['unicode_control'].sub('', text)

        # Normalize Unicode
        text = unicodedata.normalize('NFKC', text)

        # Normalize whitespace
        if normalize_whitespace:
            text = NORMALIZATION_PATTERNS['whitespace'].sub(' ', text)
            text = NORMALIZATION_PATTERNS['multiple_newlines'].sub('\n\n', text)

        # Clean line spacing
        text = NORMALIZATION_PATTERNS['trailing_spaces'].sub('', text)

        # Strip edges
        if strip_edges:
            text = text.strip()

        # Truncate if necessary
        if max_length and len(text) > max_length:
            if self.strict_mode:
                raise ValueError(f"Text length {len(text)} exceeds maximum {max_length}")
            text = text[:max_length].rstrip()

        return text

    def normalize_email(self, email: str) -> str:
        """
        Normalize email address with comprehensive validation and cleanup.

        Args:
            email: Email address to normalize

        Returns:
            Normalized email address

        Raises:
            ValueError: If email format is invalid in strict mode
        """
        if not isinstance(email, str):
            if self.strict_mode:
                raise ValueError(f"Expected string, got {type(email)}")
            email = str(email)

        # Basic cleanup
        email = email.strip().lower()

        if not email:
            if self.strict_mode:
                raise ValueError("Email cannot be empty")
            return ""

        try:
            # Use email-validator for comprehensive normalization
            validation = validate_email(email)
            return validation.email
        except EmailNotValidError as e:
            if self.strict_mode:
                raise ValueError(f"Invalid email: {str(e)}")

            # Attempt basic fixes if auto_fix_errors is enabled
            if self.auto_fix_errors:
                # Fix common issues
                email = re.sub(r'\s+', '', email)  # Remove all whitespace
                email = re.sub(r'\.{2,}', '.', email)  # Fix multiple dots
                email = re.sub(r'^\.+|\.+$', '', email)  # Remove leading/trailing dots

                # Try validation again
                try:
                    validation = validate_email(email)
                    return validation.email
                except EmailNotValidError:
                    pass

            # Return original if can't fix
            return email

    def normalize_url(self,
                     url: str,
                     add_scheme: bool = True,
                     default_scheme: str = 'https',
                     normalize_path: bool = True) -> str:
        """
        Normalize URL with scheme handling and path cleanup.

        Args:
            url: URL to normalize
            add_scheme: Add default scheme if missing
            default_scheme: Default scheme to add
            normalize_path: Normalize URL path

        Returns:
            Normalized URL string
        """
        if not isinstance(url, str):
            if self.strict_mode:
                raise ValueError(f"Expected string, got {type(url)}")
            url = str(url)

        # Basic cleanup
        url = url.strip()

        if not url:
            if self.strict_mode:
                raise ValueError("URL cannot be empty")
            return ""

        # Add scheme if missing
        if add_scheme and not re.match(r'^[a-zA-Z][a-zA-Z\d+\-.]*://', url):
            url = f'{default_scheme}://{url}'

        try:
            parsed = urlparse(url)

            # Normalize components
            scheme = parsed.scheme.lower() if parsed.scheme else default_scheme
            netloc = parsed.netloc.lower() if parsed.netloc else ''
            path = parsed.path

            # Normalize path
            if normalize_path and path:
                # Remove double slashes
                path = re.sub(r'/+', '/', path)
                # Remove trailing slash for non-root paths
                if path != '/' and path.endswith('/'):
                    path = path.rstrip('/')

            # Reconstruct URL
            normalized = urlunparse((
                scheme,
                netloc,
                path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))

            return normalized

        except Exception as e:
            if self.strict_mode:
                raise ValueError(f"URL normalization failed: {str(e)}")
            return url

    def normalize_phone(self,
                       phone: str,
                       country_code: Optional[str] = None,
                       format_style: str = 'E164') -> str:
        """
        Normalize phone number to international format.

        Args:
            phone: Phone number to normalize
            country_code: Default country code (e.g., 'US', 'RU')
            format_style: Output format ('E164', 'INTERNATIONAL', 'NATIONAL')

        Returns:
            Normalized phone number string
        """
        if not isinstance(phone, str):
            if self.strict_mode:
                raise ValueError(f"Expected string, got {type(phone)}")
            phone = str(phone)

        # Basic cleanup
        phone = re.sub(r'[\s\-\(\)\.]+', '', phone.strip())

        if not phone:
            if self.strict_mode:
                raise ValueError("Phone number cannot be empty")
            return ""

        try:
            parsed_number = phonenumbers.parse(phone, country_code)

            if not phonenumbers.is_valid_number(parsed_number):
                if self.strict_mode:
                    raise ValueError(f"Invalid phone number: {phone}")
                return phone

            # Format based on style
            format_map = {
                'E164': phonenumbers.PhoneNumberFormat.E164,
                'INTERNATIONAL': phonenumbers.PhoneNumberFormat.INTERNATIONAL,
                'NATIONAL': phonenumbers.PhoneNumberFormat.NATIONAL
            }

            format_enum = format_map.get(format_style, phonenumbers.PhoneNumberFormat.E164)
            return phonenumbers.format_number(parsed_number, format_enum)

        except NumberParseException as e:
            if self.strict_mode:
                raise ValueError(f"Phone parsing error: {str(e)}")

            # Attempt basic fixes if auto_fix_errors is enabled
            if self.auto_fix_errors:
                # Add country code if missing and looks like a valid number
                if country_code and len(phone) >= 7 and phone.isdigit():
                    country_info = phonenumbers.country_code_for_region(country_code)
                    if country_info:
                        fixed_phone = f'+{country_info}{phone}'
                        try:
                            parsed = phonenumbers.parse(fixed_phone, None)
                            if phonenumbers.is_valid_number(parsed):
                                return phonenumbers.format_number(
                                    parsed, phonenumbers.PhoneNumberFormat.E164
                                )
                        except NumberParseException:
                            pass

            return phone

    def normalize_datetime(self,
                          dt_value: Union[str, datetime],
                          target_timezone: Optional[str] = 'UTC',
                          iso_format: bool = True) -> Union[str, datetime]:
        """
        Normalize datetime to consistent format and timezone.

        Args:
            dt_value: Datetime value to normalize
            target_timezone: Target timezone (default: UTC)
            iso_format: Return as ISO format string

        Returns:
            Normalized datetime string or object
        """
        if isinstance(dt_value, str):
            try:
                # Parse ISO format datetime
                if 'T' in dt_value:
                    dt_value = datetime.fromisoformat(dt_value.replace('Z', '+00:00'))
                else:
                    # Try common formats
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y', '%d.%m.%Y']:
                        try:
                            dt_value = datetime.strptime(dt_value, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        if self.strict_mode:
                            raise ValueError(f"Cannot parse datetime: {dt_value}")
                        return dt_value
            except Exception as e:
                if self.strict_mode:
                    raise ValueError(f"Datetime parsing error: {str(e)}")
                return dt_value

        elif not isinstance(dt_value, datetime):
            if self.strict_mode:
                raise ValueError(f"Expected datetime or string, got {type(dt_value)}")
            return str(dt_value)

        # Add timezone if missing
        if dt_value.tzinfo is None:
            dt_value = dt_value.replace(tzinfo=timezone.utc)

        # Convert to target timezone
        if target_timezone and target_timezone.upper() == 'UTC':
            dt_value = dt_value.astimezone(timezone.utc)

        # Return in requested format
        if iso_format:
            return dt_value.isoformat()
        else:
            return dt_value

    def normalize_numeric(self,
                         value: Union[str, int, float],
                         decimal_places: Optional[int] = None,
                         min_value: Optional[float] = None,
                         max_value: Optional[float] = None) -> Union[int, float]:
        """
        Normalize numeric values with bounds checking and precision control.

        Args:
            value: Numeric value to normalize
            decimal_places: Number of decimal places to round to
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Returns:
            Normalized numeric value
        """
        if isinstance(value, str):
            # Clean string for numeric conversion
            value = value.strip()
            # Remove common thousand separators
            value = value.replace(',', '').replace(' ', '')

            try:
                # Try integer first
                if '.' not in value and 'e' not in value.lower():
                    value = int(value)
                else:
                    value = float(value)
            except ValueError as e:
                if self.strict_mode:
                    raise ValueError(f"Cannot convert to number: {value}")

                # Attempt to extract numeric value
                if self.auto_fix_errors:
                    numeric_match = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', str(value))
                    if numeric_match:
                        try:
                            value = float(numeric_match.group())
                        except ValueError:
                            return 0 if not self.strict_mode else raise e
                    else:
                        return 0 if not self.strict_mode else raise e
                else:
                    return value

        elif not isinstance(value, (int, float)):
            if self.strict_mode:
                raise ValueError(f"Expected numeric type, got {type(value)}")
            try:
                value = float(value)
            except (ValueError, TypeError):
                return 0

        # Check bounds
        if min_value is not None and value < min_value:
            if self.strict_mode:
                raise ValueError(f"Value {value} below minimum {min_value}")
            value = min_value

        if max_value is not None and value > max_value:
            if self.strict_mode:
                raise ValueError(f"Value {value} above maximum {max_value}")
            value = max_value

        # Apply decimal precision
        if decimal_places is not None and isinstance(value, float):
            value = round(value, decimal_places)

        return value

    def normalize_json(self,
                      json_data: Union[str, Dict, List],
                      sort_keys: bool = True,
                      indent: Optional[int] = None) -> str:
        """
        Normalize JSON data to consistent format.

        Args:
            json_data: JSON data to normalize
            sort_keys: Sort object keys
            indent: Indentation level for pretty printing

        Returns:
            Normalized JSON string
        """
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                if self.strict_mode:
                    raise ValueError(f"Invalid JSON: {str(e)}")
                return json_data

        try:
            return json.dumps(
                json_data,
                sort_keys=sort_keys,
                indent=indent,
                ensure_ascii=False,
                separators=(',', ': ') if indent else (',', ':')
            )
        except (TypeError, ValueError) as e:
            if self.strict_mode:
                raise ValueError(f"JSON serialization error: {str(e)}")
            return str(json_data)

    def normalize_list(self,
                      lst: List[Any],
                      remove_duplicates: bool = True,
                      remove_empty: bool = True,
                      sort_items: bool = False,
                      item_normalizer: Optional[Callable] = None) -> List[Any]:
        """
        Normalize list data with various cleanup options.

        Args:
            lst: List to normalize
            remove_duplicates: Remove duplicate items
            remove_empty: Remove empty/null items
            sort_items: Sort list items
            item_normalizer: Function to normalize individual items

        Returns:
            Normalized list
        """
        if not isinstance(lst, list):
            if self.strict_mode:
                raise ValueError(f"Expected list, got {type(lst)}")
            try:
                lst = list(lst)
            except TypeError:
                return []

        result = []

        for item in lst:
            # Apply item normalizer if provided
            if item_normalizer:
                try:
                    item = item_normalizer(item)
                except Exception as e:
                    if self.strict_mode:
                        raise ValueError(f"Item normalization failed: {str(e)}")
                    continue

            # Remove empty items if requested
            if remove_empty and not item:
                continue

            # Add to result
            result.append(item)

        # Remove duplicates
        if remove_duplicates:
            seen = set()
            deduped = []
            for item in result:
                # Handle unhashable types
                try:
                    if item not in seen:
                        seen.add(item)
                        deduped.append(item)
                except TypeError:
                    # For unhashable types, check manually
                    if item not in deduped:
                        deduped.append(item)
            result = deduped

        # Sort if requested
        if sort_items:
            try:
                result.sort()
            except TypeError:
                # Handle mixed types or non-comparable items
                result.sort(key=str)

        return result

    def normalize_dict(self,
                      dct: Dict[str, Any],
                      normalize_keys: bool = True,
                      remove_null_values: bool = True,
                      key_normalizer: Optional[Callable] = None,
                      value_normalizer: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Normalize dictionary data with key/value processing.

        Args:
            dct: Dictionary to normalize
            normalize_keys: Normalize dictionary keys
            remove_null_values: Remove null/empty values
            key_normalizer: Function to normalize keys
            value_normalizer: Function to normalize values

        Returns:
            Normalized dictionary
        """
        if not isinstance(dct, dict):
            if self.strict_mode:
                raise ValueError(f"Expected dict, got {type(dct)}")
            try:
                dct = dict(dct)
            except (TypeError, ValueError):
                return {}

        result = {}

        for key, value in dct.items():
            # Normalize key
            if normalize_keys:
                if key_normalizer:
                    try:
                        key = key_normalizer(key)
                    except Exception as e:
                        if self.strict_mode:
                            raise ValueError(f"Key normalization failed: {str(e)}")
                        continue
                else:
                    # Default key normalization
                    key = str(key).strip().lower().replace(' ', '_')

            # Normalize value
            if value_normalizer:
                try:
                    value = value_normalizer(value)
                except Exception as e:
                    if self.strict_mode:
                        raise ValueError(f"Value normalization failed: {str(e)}")
                    continue

            # Remove null values if requested
            if remove_null_values and value in (None, '', [], {}):
                continue

            result[key] = value

        return result

    def normalize_data(self,
                      data: Any,
                      data_type: Optional[str] = None,
                      custom_options: Optional[Dict[str, Any]] = None) -> Any:
        """
        Universal data normalization function that automatically detects type.

        Args:
            data: Data to normalize
            data_type: Explicit data type hint
            custom_options: Custom normalization options

        Returns:
            Normalized data
        """
        options = custom_options or {}

        # Use custom normalizer if registered
        if data_type and data_type in self._custom_normalizers:
            return self._custom_normalizers[data_type](data)

        # Auto-detect type and normalize
        if data_type == 'email' or (isinstance(data, str) and '@' in data and '.' in data):
            return self.normalize_email(data)

        elif data_type == 'url' or (isinstance(data, str) and ('http' in data or 'www.' in data)):
            return self.normalize_url(data, **options)

        elif data_type == 'phone' or (isinstance(data, str) and re.match(r'^[\d\s\-\(\)\+]{7,}$', data)):
            return self.normalize_phone(data, **options)

        elif data_type == 'datetime' or isinstance(data, datetime):
            return self.normalize_datetime(data, **options)

        elif data_type == 'numeric' or isinstance(data, (int, float)):
            return self.normalize_numeric(data, **options)

        elif data_type == 'json' or (isinstance(data, str) and data.strip().startswith(('{', '['))):
            return self.normalize_json(data, **options)

        elif isinstance(data, list):
            return self.normalize_list(data, **options)

        elif isinstance(data, dict):
            return self.normalize_dict(data, **options)

        elif isinstance(data, str):
            return self.normalize_text(data, **options)

        else:
            # Return as-is for unknown types
            return data

    def batch_normalize(self,
                       data_batch: List[Dict[str, Any]],
                       field_types: Optional[Dict[str, str]] = None,
                       field_options: Optional[Dict[str, Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Batch normalize multiple data objects.

        Args:
            data_batch: List of data objects to normalize
            field_types: Type hints for specific fields
            field_options: Custom options for specific fields

        Returns:
            List of normalized data objects
        """
        field_types = field_types or {}
        field_options = field_options or {}

        normalized_batch = []

        for item in data_batch:
            if not isinstance(item, dict):
                if self.strict_mode:
                    raise ValueError(f"Expected dict in batch, got {type(item)}")
                continue

            normalized_item = {}

            for field, value in item.items():
                try:
                    data_type = field_types.get(field)
                    options = field_options.get(field, {})

                    normalized_value = self.normalize_data(value, data_type, options)
                    normalized_item[field] = normalized_value

                except Exception as e:
                    if self.strict_mode:
                        raise ValueError(f"Normalization failed for field '{field}': {str(e)}")
                    # Keep original value if normalization fails
                    normalized_item[field] = value

            normalized_batch.append(normalized_item)

        return normalized_batch

    def get_normalization_report(self,
                               original_data: Any,
                               normalized_data: Any) -> Dict[str, Any]:
        """
        Generate a report comparing original and normalized data.

        Args:
            original_data: Original data before normalization
            normalized_data: Data after normalization

        Returns:
            Normalization report with statistics and changes
        """
        report = {
            'original_type': type(original_data).__name__,
            'normalized_type': type(normalized_data).__name__,
            'size_change': 0,
            'changes_detected': False,
            'details': {}
        }

        # Calculate size changes
        try:
            original_size = len(str(original_data))
            normalized_size = len(str(normalized_data))
            report['size_change'] = normalized_size - original_size
        except:
            pass

        # Detect changes
        try:
            report['changes_detected'] = original_data != normalized_data
        except:
            report['changes_detected'] = True

        # Type-specific details
        if isinstance(original_data, str) and isinstance(normalized_data, str):
            report['details'] = {
                'length_change': len(normalized_data) - len(original_data),
                'whitespace_normalized': len(original_data.split()) != len(normalized_data.split()),
                'case_changed': original_data.lower() != normalized_data.lower()
            }

        elif isinstance(original_data, list) and isinstance(normalized_data, list):
            report['details'] = {
                'count_change': len(normalized_data) - len(original_data),
                'items_removed': len(original_data) - len(normalized_data),
                'duplicates_removed': len(original_data) - len(set(map(str, original_data)))
            }

        elif isinstance(original_data, dict) and isinstance(normalized_data, dict):
            report['details'] = {
                'keys_change': len(normalized_data) - len(original_data),
                'keys_added': set(normalized_data.keys()) - set(original_data.keys()),
                'keys_removed': set(original_data.keys()) - set(normalized_data.keys())
            }

        return report


# Convenience functions for common normalization tasks
def quick_normalize_text(text: str) -> str:
    """Quick text normalization with default settings."""
    normalizer = DataNormalizer()
    return normalizer.normalize_text(text)

def quick_normalize_email(email: str) -> str:
    """Quick email normalization with default settings."""
    normalizer = DataNormalizer()
    return normalizer.normalize_email(email)

def quick_normalize_url(url: str) -> str:
    """Quick URL normalization with default settings."""
    normalizer = DataNormalizer()
    return normalizer.normalize_url(url)

def quick_normalize_phone(phone: str, country: str = 'US') -> str:
    """Quick phone normalization with default settings."""
    normalizer = DataNormalizer()
    return normalizer.normalize_phone(phone, country)

# Export main classes and functions
__all__ = [
    'DataNormalizer',
    'quick_normalize_text',
    'quick_normalize_email',
    'quick_normalize_url',
    'quick_normalize_phone'
]