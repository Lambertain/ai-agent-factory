"""
Advanced type checking and boundary validation system.
Provides comprehensive type verification and constraint validation.
"""

import sys
import math
import inspect
from typing import (
    Any, Dict, List, Tuple, Union, Optional, Type, get_origin, get_args,
    Literal, Callable, TypeVar, Generic, ForwardRef
)
from datetime import datetime, date, time, timedelta
from decimal import Decimal, InvalidOperation
from uuid import UUID
from pathlib import Path
import re
from enum import Enum


class ValidationConstraint:
    """Base class for validation constraints."""

    def __init__(self, error_message: Optional[str] = None):
        self.error_message = error_message

    def validate(self, value: Any) -> bool:
        """Validate the value against this constraint."""
        raise NotImplementedError

    def get_error_message(self, value: Any) -> str:
        """Get error message for failed validation."""
        return self.error_message or f"Constraint validation failed for value: {value}"


class RangeConstraint(ValidationConstraint):
    """Numeric range constraint validator."""

    def __init__(self,
                 min_value: Optional[Union[int, float]] = None,
                 max_value: Optional[Union[int, float]] = None,
                 inclusive_min: bool = True,
                 inclusive_max: bool = True,
                 error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_value = min_value
        self.max_value = max_value
        self.inclusive_min = inclusive_min
        self.inclusive_max = inclusive_max

    def validate(self, value: Any) -> bool:
        """Validate numeric range constraints."""
        if not isinstance(value, (int, float, Decimal)):
            return False

        if self.min_value is not None:
            if self.inclusive_min:
                if value < self.min_value:
                    return False
            else:
                if value <= self.min_value:
                    return False

        if self.max_value is not None:
            if self.inclusive_max:
                if value > self.max_value:
                    return False
            else:
                if value >= self.max_value:
                    return False

        return True

    def get_error_message(self, value: Any) -> str:
        if self.error_message:
            return self.error_message

        parts = []
        if self.min_value is not None:
            op = ">=" if self.inclusive_min else ">"
            parts.append(f"value {op} {self.min_value}")

        if self.max_value is not None:
            op = "<=" if self.inclusive_max else "<"
            parts.append(f"value {op} {self.max_value}")

        constraint_desc = " and ".join(parts)
        return f"Value {value} violates constraint: {constraint_desc}"


class LengthConstraint(ValidationConstraint):
    """String/collection length constraint validator."""

    def __init__(self,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 exact_length: Optional[int] = None,
                 error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_length = min_length
        self.max_length = max_length
        self.exact_length = exact_length

    def validate(self, value: Any) -> bool:
        """Validate length constraints."""
        try:
            length = len(value)
        except TypeError:
            return False

        if self.exact_length is not None:
            return length == self.exact_length

        if self.min_length is not None and length < self.min_length:
            return False

        if self.max_length is not None and length > self.max_length:
            return False

        return True

    def get_error_message(self, value: Any) -> str:
        if self.error_message:
            return self.error_message

        try:
            actual_length = len(value)
        except TypeError:
            return f"Value {value} does not have a length"

        if self.exact_length is not None:
            return f"Length must be exactly {self.exact_length}, got {actual_length}"

        parts = []
        if self.min_length is not None:
            parts.append(f"min {self.min_length}")
        if self.max_length is not None:
            parts.append(f"max {self.max_length}")

        constraint_desc = ", ".join(parts)
        return f"Length {actual_length} violates constraint: {constraint_desc}"


class PatternConstraint(ValidationConstraint):
    """Regular expression pattern constraint validator."""

    def __init__(self,
                 pattern: Union[str, re.Pattern],
                 flags: int = 0,
                 must_match: bool = True,
                 error_message: Optional[str] = None):
        super().__init__(error_message)
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern, flags)
        else:
            self.pattern = pattern
        self.must_match = must_match

    def validate(self, value: Any) -> bool:
        """Validate pattern constraint."""
        if not isinstance(value, str):
            return False

        match = self.pattern.search(value)
        return bool(match) if self.must_match else not bool(match)

    def get_error_message(self, value: Any) -> str:
        if self.error_message:
            return self.error_message

        match_type = "match" if self.must_match else "not match"
        return f"Value '{value}' must {match_type} pattern: {self.pattern.pattern}"


class ChoiceConstraint(ValidationConstraint):
    """Choice/enumeration constraint validator."""

    def __init__(self,
                 choices: Union[List[Any], Tuple[Any, ...], set],
                 case_sensitive: bool = True,
                 error_message: Optional[str] = None):
        super().__init__(error_message)
        self.choices = set(choices)
        self.case_sensitive = case_sensitive

        if not case_sensitive:
            # Create lowercase mapping for string choices
            self.lowercase_choices = {
                str(choice).lower(): choice
                for choice in choices
                if isinstance(choice, str)
            }

    def validate(self, value: Any) -> bool:
        """Validate choice constraint."""
        if value in self.choices:
            return True

        if not self.case_sensitive and isinstance(value, str):
            return value.lower() in self.lowercase_choices

        return False

    def get_error_message(self, value: Any) -> str:
        if self.error_message:
            return self.error_message

        choices_str = ", ".join(str(c) for c in sorted(self.choices))
        return f"Value '{value}' not in allowed choices: [{choices_str}]"


class TypeChecker:
    """
    Advanced type checking system with comprehensive validation capabilities.
    """

    def __init__(self,
                 strict_mode: bool = False,
                 auto_convert: bool = True,
                 raise_on_error: bool = False):
        """
        Initialize the type checker.

        Args:
            strict_mode: Enable strict type checking
            auto_convert: Attempt automatic type conversion
            raise_on_error: Raise exceptions on validation errors
        """
        self.strict_mode = strict_mode
        self.auto_convert = auto_convert
        self.raise_on_error = raise_on_error

        # Type conversion functions
        self._converters: Dict[Type, Callable] = {
            int: self._convert_to_int,
            float: self._convert_to_float,
            str: self._convert_to_str,
            bool: self._convert_to_bool,
            list: self._convert_to_list,
            dict: self._convert_to_dict,
            datetime: self._convert_to_datetime,
            UUID: self._convert_to_uuid,
            Decimal: self._convert_to_decimal,
        }

        # Custom type validators
        self._validators: Dict[str, Callable] = {}

    def register_validator(self, type_name: str, validator: Callable):
        """Register a custom type validator."""
        self._validators[type_name] = validator

    def check_type(self,
                   value: Any,
                   expected_type: Type,
                   constraints: Optional[List[ValidationConstraint]] = None,
                   convert: Optional[bool] = None) -> Tuple[bool, Any, List[str]]:
        """
        Check if value matches expected type with optional constraints.

        Args:
            value: Value to check
            expected_type: Expected type
            constraints: List of validation constraints
            convert: Override auto_convert setting

        Returns:
            Tuple of (is_valid, converted_value, error_messages)
        """
        errors = []
        converted_value = value
        should_convert = convert if convert is not None else self.auto_convert

        try:
            # Handle special typing constructs
            origin = get_origin(expected_type)
            args = get_args(expected_type)

            if origin is Union:
                return self._check_union_type(value, args, constraints, should_convert)
            elif origin is list or origin is List:
                return self._check_list_type(value, args, constraints, should_convert)
            elif origin is dict or origin is Dict:
                return self._check_dict_type(value, args, constraints, should_convert)
            elif origin is tuple or origin is Tuple:
                return self._check_tuple_type(value, args, constraints, should_convert)
            elif origin is Literal:
                return self._check_literal_type(value, args, constraints)

            # Handle basic types
            if not self._is_instance_of_type(value, expected_type):
                if should_convert:
                    try:
                        converted_value = self._convert_value(value, expected_type)
                    except Exception as e:
                        errors.append(f"Type conversion failed: {str(e)}")
                        if self.raise_on_error:
                            raise ValueError(f"Cannot convert {type(value)} to {expected_type}")
                        return False, value, errors
                else:
                    errors.append(f"Expected {expected_type}, got {type(value)}")
                    if self.raise_on_error:
                        raise TypeError(f"Expected {expected_type}, got {type(value)}")
                    return False, value, errors

            # Apply constraints
            if constraints:
                constraint_errors = self._validate_constraints(converted_value, constraints)
                errors.extend(constraint_errors)

            is_valid = len(errors) == 0
            return is_valid, converted_value, errors

        except Exception as e:
            error_msg = f"Type checking error: {str(e)}"
            errors.append(error_msg)
            if self.raise_on_error:
                raise
            return False, value, errors

    def validate_boundaries(self,
                           value: Any,
                           data_type: str,
                           **kwargs) -> Tuple[bool, List[str]]:
        """
        Validate value against boundary conditions.

        Args:
            value: Value to validate
            data_type: Type of data for boundary checking
            **kwargs: Boundary parameters

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        try:
            if data_type == 'numeric':
                errors.extend(self._validate_numeric_boundaries(value, **kwargs))
            elif data_type == 'string':
                errors.extend(self._validate_string_boundaries(value, **kwargs))
            elif data_type == 'collection':
                errors.extend(self._validate_collection_boundaries(value, **kwargs))
            elif data_type == 'datetime':
                errors.extend(self._validate_datetime_boundaries(value, **kwargs))
            elif data_type in self._validators:
                custom_errors = self._validators[data_type](value, **kwargs)
                if isinstance(custom_errors, list):
                    errors.extend(custom_errors)
                elif custom_errors:
                    errors.append(str(custom_errors))

            return len(errors) == 0, errors

        except Exception as e:
            errors.append(f"Boundary validation error: {str(e)}")
            return False, errors

    def _is_instance_of_type(self, value: Any, expected_type: Type) -> bool:
        """Check if value is instance of expected type."""
        try:
            return isinstance(value, expected_type)
        except TypeError:
            # Handle cases where isinstance fails (e.g., with some generic types)
            return type(value) == expected_type

    def _convert_value(self, value: Any, target_type: Type) -> Any:
        """Convert value to target type."""
        if target_type in self._converters:
            return self._converters[target_type](value)

        # Try direct conversion
        try:
            return target_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert {value} to {target_type}: {str(e)}")

    def _convert_to_int(self, value: Any) -> int:
        """Convert value to integer."""
        if isinstance(value, bool):
            return int(value)
        elif isinstance(value, str):
            # Handle common string formats
            value = value.strip().replace(',', '').replace(' ', '')
            if value.lower() in ('true', 'yes', 'on', '1'):
                return 1
            elif value.lower() in ('false', 'no', 'off', '0'):
                return 0
            return int(float(value))  # Handle "123.0" format
        elif isinstance(value, float):
            if value.is_integer():
                return int(value)
            raise ValueError(f"Float {value} cannot be converted to int without precision loss")
        return int(value)

    def _convert_to_float(self, value: Any) -> float:
        """Convert value to float."""
        if isinstance(value, str):
            value = value.strip().replace(',', '').replace(' ', '')
        return float(value)

    def _convert_to_str(self, value: Any) -> str:
        """Convert value to string."""
        if value is None:
            return ""
        return str(value)

    def _convert_to_bool(self, value: Any) -> bool:
        """Convert value to boolean."""
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ('true', 'yes', 'on', '1', 'y', 't'):
                return True
            elif value in ('false', 'no', 'off', '0', 'n', 'f', ''):
                return False
            raise ValueError(f"Cannot convert string '{value}' to bool")
        return bool(value)

    def _convert_to_list(self, value: Any) -> list:
        """Convert value to list."""
        if isinstance(value, (tuple, set)):
            return list(value)
        elif isinstance(value, str):
            # Try JSON parsing first
            try:
                import json
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except:
                pass
            # Split by common delimiters
            return [item.strip() for item in re.split(r'[,;|\n]', value) if item.strip()]
        elif hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
            return list(value)
        return [value]

    def _convert_to_dict(self, value: Any) -> dict:
        """Convert value to dictionary."""
        if isinstance(value, str):
            import json
            return json.loads(value)
        elif hasattr(value, '_asdict'):  # namedtuple
            return value._asdict()
        elif hasattr(value, '__dict__'):
            return vars(value)
        return dict(value)

    def _convert_to_datetime(self, value: Any) -> datetime:
        """Convert value to datetime."""
        if isinstance(value, str):
            # Try common datetime formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d.%m.%Y',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%SZ',
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            # Try ISO format with timezone
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                pass
        elif isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        elif isinstance(value, date):
            return datetime.combine(value, time())

        raise ValueError(f"Cannot convert {value} to datetime")

    def _convert_to_uuid(self, value: Any) -> UUID:
        """Convert value to UUID."""
        if isinstance(value, str):
            return UUID(value)
        return UUID(str(value))

    def _convert_to_decimal(self, value: Any) -> Decimal:
        """Convert value to Decimal."""
        if isinstance(value, str):
            value = value.strip().replace(',', '')
        try:
            return Decimal(str(value))
        except InvalidOperation as e:
            raise ValueError(f"Cannot convert {value} to Decimal: {str(e)}")

    def _check_union_type(self,
                         value: Any,
                         union_args: Tuple,
                         constraints: Optional[List[ValidationConstraint]],
                         should_convert: bool) -> Tuple[bool, Any, List[str]]:
        """Check Union type (e.g., Union[int, str])."""
        errors = []

        for arg_type in union_args:
            is_valid, converted_value, type_errors = self.check_type(
                value, arg_type, constraints, should_convert
            )
            if is_valid:
                return True, converted_value, []
            errors.extend(type_errors)

        return False, value, [f"Value does not match any type in Union: {union_args}"]

    def _check_list_type(self,
                        value: Any,
                        list_args: Tuple,
                        constraints: Optional[List[ValidationConstraint]],
                        should_convert: bool) -> Tuple[bool, Any, List[str]]:
        """Check List type with element type checking."""
        errors = []

        # Convert to list if needed
        if not isinstance(value, list):
            if should_convert:
                try:
                    value = self._convert_to_list(value)
                except Exception as e:
                    errors.append(f"Cannot convert to list: {str(e)}")
                    return False, value, errors
            else:
                errors.append(f"Expected list, got {type(value)}")
                return False, value, errors

        # Check element types if specified
        if list_args:
            element_type = list_args[0]
            validated_items = []

            for i, item in enumerate(value):
                is_valid, converted_item, item_errors = self.check_type(
                    item, element_type, None, should_convert
                )
                if not is_valid:
                    errors.extend([f"Item {i}: {error}" for error in item_errors])
                validated_items.append(converted_item)

            value = validated_items

        # Apply constraints
        if constraints:
            constraint_errors = self._validate_constraints(value, constraints)
            errors.extend(constraint_errors)

        return len(errors) == 0, value, errors

    def _check_dict_type(self,
                        value: Any,
                        dict_args: Tuple,
                        constraints: Optional[List[ValidationConstraint]],
                        should_convert: bool) -> Tuple[bool, Any, List[str]]:
        """Check Dict type with key/value type checking."""
        errors = []

        # Convert to dict if needed
        if not isinstance(value, dict):
            if should_convert:
                try:
                    value = self._convert_to_dict(value)
                except Exception as e:
                    errors.append(f"Cannot convert to dict: {str(e)}")
                    return False, value, errors
            else:
                errors.append(f"Expected dict, got {type(value)}")
                return False, value, errors

        # Check key/value types if specified
        if len(dict_args) >= 2:
            key_type, value_type = dict_args[0], dict_args[1]
            validated_dict = {}

            for k, v in value.items():
                # Check key type
                key_valid, converted_key, key_errors = self.check_type(
                    k, key_type, None, should_convert
                )
                if not key_valid:
                    errors.extend([f"Key '{k}': {error}" for error in key_errors])

                # Check value type
                val_valid, converted_val, val_errors = self.check_type(
                    v, value_type, None, should_convert
                )
                if not val_valid:
                    errors.extend([f"Value for key '{k}': {error}" for error in val_errors])

                validated_dict[converted_key] = converted_val

            value = validated_dict

        # Apply constraints
        if constraints:
            constraint_errors = self._validate_constraints(value, constraints)
            errors.extend(constraint_errors)

        return len(errors) == 0, value, errors

    def _check_tuple_type(self,
                         value: Any,
                         tuple_args: Tuple,
                         constraints: Optional[List[ValidationConstraint]],
                         should_convert: bool) -> Tuple[bool, Any, List[str]]:
        """Check Tuple type with element type checking."""
        errors = []

        # Convert to tuple if needed
        if not isinstance(value, tuple):
            if should_convert:
                try:
                    if isinstance(value, (list, set)):
                        value = tuple(value)
                    else:
                        value = (value,)
                except Exception as e:
                    errors.append(f"Cannot convert to tuple: {str(e)}")
                    return False, value, errors
            else:
                errors.append(f"Expected tuple, got {type(value)}")
                return False, value, errors

        # Check element types if specified
        if tuple_args:
            if len(tuple_args) == len(value):
                validated_items = []
                for i, (item, expected_type) in enumerate(zip(value, tuple_args)):
                    is_valid, converted_item, item_errors = self.check_type(
                        item, expected_type, None, should_convert
                    )
                    if not is_valid:
                        errors.extend([f"Item {i}: {error}" for error in item_errors])
                    validated_items.append(converted_item)
                value = tuple(validated_items)
            else:
                errors.append(f"Tuple length mismatch: expected {len(tuple_args)}, got {len(value)}")

        # Apply constraints
        if constraints:
            constraint_errors = self._validate_constraints(value, constraints)
            errors.extend(constraint_errors)

        return len(errors) == 0, value, errors

    def _check_literal_type(self,
                           value: Any,
                           literal_args: Tuple,
                           constraints: Optional[List[ValidationConstraint]]) -> Tuple[bool, Any, List[str]]:
        """Check Literal type."""
        if value in literal_args:
            # Apply constraints
            errors = []
            if constraints:
                errors = self._validate_constraints(value, constraints)
            return len(errors) == 0, value, errors
        else:
            allowed_values = ", ".join(str(v) for v in literal_args)
            return False, value, [f"Value must be one of: {allowed_values}"]

    def _validate_constraints(self,
                             value: Any,
                             constraints: List[ValidationConstraint]) -> List[str]:
        """Validate value against constraints."""
        errors = []

        for constraint in constraints:
            try:
                if not constraint.validate(value):
                    errors.append(constraint.get_error_message(value))
            except Exception as e:
                errors.append(f"Constraint validation error: {str(e)}")

        return errors

    def _validate_numeric_boundaries(self, value: Any, **kwargs) -> List[str]:
        """Validate numeric boundary conditions."""
        errors = []

        if not isinstance(value, (int, float, Decimal)):
            errors.append(f"Expected numeric type, got {type(value)}")
            return errors

        # Check basic range
        min_val = kwargs.get('min_value')
        max_val = kwargs.get('max_value')
        if min_val is not None and value < min_val:
            errors.append(f"Value {value} below minimum {min_val}")
        if max_val is not None and value > max_val:
            errors.append(f"Value {value} above maximum {max_val}")

        # Check special numeric conditions
        if kwargs.get('positive_only', False) and value <= 0:
            errors.append(f"Value must be positive, got {value}")

        if kwargs.get('non_negative', False) and value < 0:
            errors.append(f"Value must be non-negative, got {value}")

        if kwargs.get('finite_only', True) and isinstance(value, float):
            if math.isinf(value):
                errors.append("Value cannot be infinite")
            if math.isnan(value):
                errors.append("Value cannot be NaN")

        # Check decimal precision
        precision = kwargs.get('decimal_precision')
        if precision is not None and isinstance(value, float):
            if len(str(value).split('.')[-1]) > precision:
                errors.append(f"Value has too many decimal places (max {precision})")

        return errors

    def _validate_string_boundaries(self, value: Any, **kwargs) -> List[str]:
        """Validate string boundary conditions."""
        errors = []

        if not isinstance(value, str):
            errors.append(f"Expected string type, got {type(value)}")
            return errors

        # Length constraints
        min_len = kwargs.get('min_length')
        max_len = kwargs.get('max_length')
        if min_len is not None and len(value) < min_len:
            errors.append(f"String too short: {len(value)} < {min_len}")
        if max_len is not None and len(value) > max_len:
            errors.append(f"String too long: {len(value)} > {max_len}")

        # Pattern constraints
        required_patterns = kwargs.get('required_patterns', [])
        for pattern in required_patterns:
            if not re.search(pattern, value):
                errors.append(f"String missing required pattern: {pattern}")

        forbidden_patterns = kwargs.get('forbidden_patterns', [])
        for pattern in forbidden_patterns:
            if re.search(pattern, value):
                errors.append(f"String contains forbidden pattern: {pattern}")

        # Character constraints
        if kwargs.get('ascii_only', False) and not value.isascii():
            errors.append("String must contain only ASCII characters")

        if kwargs.get('alphanumeric_only', False) and not value.isalnum():
            errors.append("String must contain only alphanumeric characters")

        return errors

    def _validate_collection_boundaries(self, value: Any, **kwargs) -> List[str]:
        """Validate collection boundary conditions."""
        errors = []

        try:
            length = len(value)
        except TypeError:
            errors.append(f"Value {value} does not have a length")
            return errors

        # Size constraints
        min_size = kwargs.get('min_size')
        max_size = kwargs.get('max_size')
        if min_size is not None and length < min_size:
            errors.append(f"Collection too small: {length} < {min_size}")
        if max_size is not None and length > max_size:
            errors.append(f"Collection too large: {length} > {max_size}")

        # Content constraints
        if kwargs.get('no_duplicates', False) and isinstance(value, (list, tuple)):
            if len(value) != len(set(str(item) for item in value)):
                errors.append("Collection contains duplicate items")

        if kwargs.get('no_empty_items', False) and hasattr(value, '__iter__'):
            empty_items = [i for i, item in enumerate(value) if not item]
            if empty_items:
                errors.append(f"Collection contains empty items at indices: {empty_items}")

        return errors

    def _validate_datetime_boundaries(self, value: Any, **kwargs) -> List[str]:
        """Validate datetime boundary conditions."""
        errors = []

        if not isinstance(value, (datetime, date)):
            errors.append(f"Expected datetime/date type, got {type(value)}")
            return errors

        # Range constraints
        min_date = kwargs.get('min_date')
        max_date = kwargs.get('max_date')
        if min_date is not None and value < min_date:
            errors.append(f"Date {value} before minimum {min_date}")
        if max_date is not None and value > max_date:
            errors.append(f"Date {value} after maximum {max_date}")

        # Timezone constraints
        if kwargs.get('require_timezone', False) and isinstance(value, datetime):
            if value.tzinfo is None:
                errors.append("Datetime must include timezone information")

        # Future/past constraints
        now = datetime.now()
        if kwargs.get('future_only', False) and value <= now:
            errors.append(f"Date must be in the future, got {value}")
        if kwargs.get('past_only', False) and value >= now:
            errors.append(f"Date must be in the past, got {value}")

        return errors


# Convenience functions for common type checking scenarios
def check_numeric_range(value: Union[int, float],
                       min_value: Optional[float] = None,
                       max_value: Optional[float] = None) -> Tuple[bool, List[str]]:
    """Quick numeric range validation."""
    checker = TypeChecker()
    constraint = RangeConstraint(min_value, max_value)
    is_valid, _, errors = checker.check_type(value, type(value), [constraint])
    return is_valid, errors


def check_string_length(value: str,
                       min_length: Optional[int] = None,
                       max_length: Optional[int] = None) -> Tuple[bool, List[str]]:
    """Quick string length validation."""
    checker = TypeChecker()
    constraint = LengthConstraint(min_length, max_length)
    is_valid, _, errors = checker.check_type(value, str, [constraint])
    return is_valid, errors


def check_pattern_match(value: str, pattern: str) -> Tuple[bool, List[str]]:
    """Quick pattern matching validation."""
    checker = TypeChecker()
    constraint = PatternConstraint(pattern)
    is_valid, _, errors = checker.check_type(value, str, [constraint])
    return is_valid, errors


def check_choices(value: Any, choices: List[Any]) -> Tuple[bool, List[str]]:
    """Quick choice validation."""
    checker = TypeChecker()
    constraint = ChoiceConstraint(choices)
    is_valid, _, errors = checker.check_type(value, type(value), [constraint])
    return is_valid, errors


# Export main classes and functions
__all__ = [
    'ValidationConstraint',
    'RangeConstraint',
    'LengthConstraint',
    'PatternConstraint',
    'ChoiceConstraint',
    'TypeChecker',
    'check_numeric_range',
    'check_string_length',
    'check_pattern_match',
    'check_choices'
]