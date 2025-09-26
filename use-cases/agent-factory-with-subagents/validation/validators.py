"""
Enhanced Pydantic validators with comprehensive validation rules.
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timezone
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, field_validator, model_validator
from urllib.parse import urlparse
import phonenumbers
from phonenumbers import NumberParseException


class EmailValidator(BaseModel):
    """Enhanced email validation with normalization."""

    email: str = Field(..., description="Email address to validate")

    @field_validator('email')
    @classmethod
    def validate_email_address(cls, v: str) -> str:
        """Validate and normalize email address."""
        if not v or not isinstance(v, str):
            raise ValueError("Email must be a non-empty string")

        # Remove whitespace
        v = v.strip()

        if not v:
            raise ValueError("Email cannot be empty or whitespace only")

        # Check basic email pattern first
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError(f"Invalid email format: {v}")

        # Use email-validator for comprehensive validation
        try:
            validation = validate_email(v)
            return validation.email  # Returns normalized email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")


class URLValidator(BaseModel):
    """Enhanced URL validation with scheme and domain checks."""

    url: str = Field(..., description="URL to validate")
    allowed_schemes: List[str] = Field(default=['http', 'https'], description="Allowed URL schemes")
    require_tld: bool = Field(default=True, description="Require top-level domain")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate and normalize URL."""
        if not v or not isinstance(v, str):
            raise ValueError("URL must be a non-empty string")

        # Remove whitespace
        v = v.strip()

        if not v:
            raise ValueError("URL cannot be empty or whitespace only")

        # Add scheme if missing
        if not v.startswith(('http://', 'https://')):
            v = f'https://{v}'

        try:
            parsed = urlparse(v)
        except Exception as e:
            raise ValueError(f"Invalid URL format: {str(e)}")

        if not parsed.scheme:
            raise ValueError("URL must have a scheme")

        if not parsed.netloc:
            raise ValueError("URL must have a domain")

        # Check domain format
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?(\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?)*$'
        if not re.match(domain_pattern, parsed.netloc.split(':')[0]):
            raise ValueError(f"Invalid domain format: {parsed.netloc}")

        return v

    @model_validator(mode='after')
    def validate_scheme(self) -> 'URLValidator':
        """Validate URL scheme against allowed schemes."""
        parsed = urlparse(self.url)
        if parsed.scheme not in self.allowed_schemes:
            raise ValueError(f"URL scheme '{parsed.scheme}' not allowed. Allowed schemes: {self.allowed_schemes}")
        return self


class PhoneValidator(BaseModel):
    """International phone number validation."""

    phone: str = Field(..., description="Phone number to validate")
    country_code: Optional[str] = Field(default=None, description="Default country code (e.g., 'US', 'RU')")

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate and normalize phone number."""
        if not v or not isinstance(v, str):
            raise ValueError("Phone number must be a non-empty string")

        # Remove whitespace and common separators
        v = re.sub(r'[\s\-\(\)\+]', '', v.strip())

        if not v:
            raise ValueError("Phone number cannot be empty after cleaning")

        # Basic digit check
        if not re.match(r'^[\d\+]+$', v):
            raise ValueError("Phone number can only contain digits and + sign")

        return v

    @model_validator(mode='after')
    def validate_phone_format(self) -> 'PhoneValidator':
        """Validate phone number format using phonenumbers library."""
        try:
            parsed_number = phonenumbers.parse(self.phone, self.country_code)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError(f"Invalid phone number: {self.phone}")

            # Normalize to international format
            self.phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        except NumberParseException as e:
            raise ValueError(f"Phone number parsing error: {str(e)}")

        return self


class TextValidator(BaseModel):
    """Enhanced text validation with content filtering and normalization."""

    text: str = Field(..., description="Text to validate")
    min_length: int = Field(default=1, ge=0, description="Minimum text length")
    max_length: int = Field(default=10000, ge=1, description="Maximum text length")
    allow_empty: bool = Field(default=False, description="Allow empty strings")
    strip_whitespace: bool = Field(default=True, description="Strip leading/trailing whitespace")
    normalize_whitespace: bool = Field(default=True, description="Normalize internal whitespace")
    forbidden_patterns: List[str] = Field(default_factory=list, description="Forbidden regex patterns")
    required_patterns: List[str] = Field(default_factory=list, description="Required regex patterns")

    @field_validator('text')
    @classmethod
    def validate_text_content(cls, v: str) -> str:
        """Validate and normalize text content."""
        if not isinstance(v, str):
            raise ValueError("Text must be a string")

        return v

    @model_validator(mode='after')
    def validate_text_rules(self) -> 'TextValidator':
        """Apply text validation rules."""
        text = self.text

        # Strip whitespace if requested
        if self.strip_whitespace:
            text = text.strip()

        # Check if empty and if allowed
        if not text and not self.allow_empty:
            raise ValueError("Text cannot be empty")

        # Normalize internal whitespace
        if self.normalize_whitespace:
            text = re.sub(r'\s+', ' ', text)

        # Check length constraints
        if len(text) < self.min_length:
            raise ValueError(f"Text too short. Minimum length: {self.min_length}, got: {len(text)}")

        if len(text) > self.max_length:
            raise ValueError(f"Text too long. Maximum length: {self.max_length}, got: {len(text)}")

        # Check forbidden patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                raise ValueError(f"Text contains forbidden pattern: {pattern}")

        # Check required patterns
        for pattern in self.required_patterns:
            if not re.search(pattern, text, re.IGNORECASE):
                raise ValueError(f"Text missing required pattern: {pattern}")

        self.text = text
        return self


class NumericValidator(BaseModel):
    """Enhanced numeric validation with range checks and normalization."""

    value: Union[int, float] = Field(..., description="Numeric value to validate")
    min_value: Optional[Union[int, float]] = Field(default=None, description="Minimum allowed value")
    max_value: Optional[Union[int, float]] = Field(default=None, description="Maximum allowed value")
    allow_negative: bool = Field(default=True, description="Allow negative values")
    precision: Optional[int] = Field(default=None, ge=0, description="Decimal precision for floats")

    @field_validator('value')
    @classmethod
    def validate_numeric_value(cls, v: Union[int, float]) -> Union[int, float]:
        """Validate numeric value."""
        if not isinstance(v, (int, float)):
            raise ValueError("Value must be a number")

        if not isinstance(v, (int, float)) or (isinstance(v, float) and (v != v)):  # NaN check
            raise ValueError("Value must be a valid number (not NaN or infinity)")

        return v

    @model_validator(mode='after')
    def validate_numeric_constraints(self) -> 'NumericValidator':
        """Apply numeric validation constraints."""
        value = self.value

        # Check negative values
        if not self.allow_negative and value < 0:
            raise ValueError(f"Negative values not allowed: {value}")

        # Check range constraints
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value below minimum: {value} < {self.min_value}")

        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value above maximum: {value} > {self.max_value}")

        # Apply precision for floats
        if self.precision is not None and isinstance(value, float):
            self.value = round(value, self.precision)

        return self


class DateTimeValidator(BaseModel):
    """Enhanced datetime validation with timezone handling."""

    datetime_value: datetime = Field(..., description="Datetime value to validate")
    require_timezone: bool = Field(default=True, description="Require timezone information")
    min_datetime: Optional[datetime] = Field(default=None, description="Minimum allowed datetime")
    max_datetime: Optional[datetime] = Field(default=None, description="Maximum allowed datetime")

    @field_validator('datetime_value')
    @classmethod
    def validate_datetime(cls, v: datetime) -> datetime:
        """Validate datetime value."""
        if not isinstance(v, datetime):
            raise ValueError("Value must be a datetime object")

        return v

    @model_validator(mode='after')
    def validate_datetime_constraints(self) -> 'DateTimeValidator':
        """Apply datetime validation constraints."""
        dt = self.datetime_value

        # Check timezone requirement
        if self.require_timezone and dt.tzinfo is None:
            raise ValueError("Datetime must include timezone information")

        # Normalize to UTC if timezone is present
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
            self.datetime_value = dt

        # Check range constraints
        if self.min_datetime is not None:
            min_dt = self.min_datetime
            if min_dt.tzinfo is None and dt.tzinfo is not None:
                min_dt = min_dt.replace(tzinfo=timezone.utc)
            elif min_dt.tzinfo is not None and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            if dt < min_dt:
                raise ValueError(f"Datetime before minimum: {dt} < {min_dt}")

        if self.max_datetime is not None:
            max_dt = self.max_datetime
            if max_dt.tzinfo is None and dt.tzinfo is not None:
                max_dt = max_dt.replace(tzinfo=timezone.utc)
            elif max_dt.tzinfo is not None and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            if dt > max_dt:
                raise ValueError(f"Datetime after maximum: {dt} > {max_dt}")

        return self


# Application-specific validators

class AgentInputValidator(BaseModel):
    """Validator for general agent input parameters."""

    input_data: Dict[str, Any] = Field(..., description="Agent input data")
    required_fields: List[str] = Field(default_factory=list, description="Required fields")
    optional_fields: List[str] = Field(default_factory=list, description="Optional fields")
    field_validators: Dict[str, Callable] = Field(default_factory=dict, description="Custom field validators")

    @model_validator(mode='after')
    def validate_agent_input(self) -> 'AgentInputValidator':
        """Validate agent input structure and fields."""
        data = self.input_data

        # Check required fields
        missing_fields = []
        for field in self.required_fields:
            if field not in data:
                missing_fields.append(field)

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Check for unexpected fields
        allowed_fields = set(self.required_fields + self.optional_fields)
        unexpected_fields = set(data.keys()) - allowed_fields

        if unexpected_fields:
            raise ValueError(f"Unexpected fields: {list(unexpected_fields)}")

        # Apply custom field validators
        for field, validator in self.field_validators.items():
            if field in data:
                try:
                    data[field] = validator(data[field])
                except Exception as e:
                    raise ValueError(f"Validation failed for field '{field}': {str(e)}")

        return self


class SearchRequestValidator(BaseModel):
    """Enhanced validator for search requests."""

    query: str = Field(..., description="Search query")
    search_type: str = Field(default="semantic", description="Search type")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Search filters")

    @field_validator('query')
    @classmethod
    def validate_search_query(cls, v: str) -> str:
        """Validate search query."""
        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=1000,
            strip_whitespace=True,
            normalize_whitespace=True,
            forbidden_patterns=[r'<script.*?>', r'javascript:', r'on\w+\s*=']
        )
        return text_validator.text

    @field_validator('search_type')
    @classmethod
    def validate_search_type(cls, v: str) -> str:
        """Validate search type."""
        allowed_types = ['semantic', 'keyword', 'hybrid']
        if v not in allowed_types:
            raise ValueError(f"Invalid search type: {v}. Allowed: {allowed_types}")
        return v


class DocumentValidator(BaseModel):
    """Enhanced validator for document data."""

    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Document source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate document title."""
        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=500,
            strip_whitespace=True,
            normalize_whitespace=True,
            forbidden_patterns=[r'<[^>]+>', r'javascript:', r'on\w+\s*=']
        )
        return text_validator.text

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate document content."""
        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=1000000,  # 1MB of text
            strip_whitespace=True,
            normalize_whitespace=False  # Preserve formatting in content
        )
        return text_validator.text

    @field_validator('source')
    @classmethod
    def validate_source(cls, v: str) -> str:
        """Validate document source."""
        # Check if it's a URL or file path
        if v.startswith(('http://', 'https://')):
            url_validator = URLValidator(url=v)
            return url_validator.url
        else:
            # Validate as file path or identifier
            text_validator = TextValidator(
                text=v,
                min_length=1,
                max_length=1000,
                strip_whitespace=True,
                forbidden_patterns=[r'[<>"|*?]', r'\.\./', r'\\\\']
            )
            return text_validator.text


class ChunkValidator(BaseModel):
    """Enhanced validator for document chunks."""

    content: str = Field(..., description="Chunk content")
    chunk_index: int = Field(..., ge=0, description="Chunk index")
    token_count: Optional[int] = Field(default=None, ge=0, description="Token count")
    embedding: Optional[List[float]] = Field(default=None, description="Embedding vector")

    @field_validator('content')
    @classmethod
    def validate_chunk_content(cls, v: str) -> str:
        """Validate chunk content."""
        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=50000,  # 50k characters max per chunk
            strip_whitespace=True,
            normalize_whitespace=False
        )
        return text_validator.text

    @field_validator('embedding')
    @classmethod
    def validate_embedding(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """Validate embedding vector."""
        if v is None:
            return v

        if not isinstance(v, list):
            raise ValueError("Embedding must be a list of floats")

        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError("All embedding values must be numeric")

        # Check for common embedding dimensions
        valid_dimensions = [384, 512, 768, 1024, 1536, 2048, 3072, 4096]
        if len(v) not in valid_dimensions:
            raise ValueError(f"Unusual embedding dimension: {len(v)}. Common dimensions: {valid_dimensions}")

        return v


class SessionValidator(BaseModel):
    """Enhanced validator for session data."""

    session_id: str = Field(..., description="Session ID")
    user_id: Optional[str] = Field(default=None, description="User ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID format."""
        # UUID pattern or custom format
        uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        custom_pattern = r'^[a-zA-Z0-9_-]{8,64}$'

        if not (re.match(uuid_pattern, v) or re.match(custom_pattern, v)):
            raise ValueError(f"Invalid session ID format: {v}")

        return v

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate user ID format."""
        if v is None:
            return v

        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=100,
            strip_whitespace=True,
            forbidden_patterns=[r'[<>"|*?\\]', r'javascript:', r'on\w+\s*=']
        )
        return text_validator.text


class MessageValidator(BaseModel):
    """Enhanced validator for message data."""

    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role")
    session_id: str = Field(..., description="Session ID")

    @field_validator('content')
    @classmethod
    def validate_message_content(cls, v: str) -> str:
        """Validate message content."""
        text_validator = TextValidator(
            text=v,
            min_length=1,
            max_length=100000,  # 100k characters max per message
            strip_whitespace=True,
            normalize_whitespace=True
        )
        return text_validator.text

    @field_validator('role')
    @classmethod
    def validate_message_role(cls, v: str) -> str:
        """Validate message role."""
        allowed_roles = ['user', 'assistant', 'system', 'tool']
        if v.lower() not in allowed_roles:
            raise ValueError(f"Invalid message role: {v}. Allowed: {allowed_roles}")
        return v.lower()

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID."""
        session_validator = SessionValidator(session_id=v)
        return session_validator.session_id


class ToolCallValidator(BaseModel):
    """Enhanced validator for tool call data."""

    tool_name: str = Field(..., description="Tool name")
    args: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")
    tool_call_id: Optional[str] = Field(default=None, description="Tool call ID")

    @field_validator('tool_name')
    @classmethod
    def validate_tool_name(cls, v: str) -> str:
        """Validate tool name."""
        # Tool names should be valid Python identifiers
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', v):
            raise ValueError(f"Invalid tool name format: {v}")

        return v

    @field_validator('tool_call_id')
    @classmethod
    def validate_tool_call_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate tool call ID."""
        if v is None:
            return v

        # Should be a valid identifier
        if not re.match(r'^[a-zA-Z0-9_-]{1,100}$', v):
            raise ValueError(f"Invalid tool call ID format: {v}")

        return v


class IngestionConfigValidator(BaseModel):
    """Enhanced validator for ingestion configuration."""

    chunk_size: int = Field(..., ge=100, le=50000, description="Chunk size")
    chunk_overlap: int = Field(..., ge=0, description="Chunk overlap")
    max_chunk_size: int = Field(..., ge=500, description="Maximum chunk size")
    use_semantic_chunking: bool = Field(default=True, description="Use semantic chunking")

    @model_validator(mode='after')
    def validate_chunk_config(self) -> 'IngestionConfigValidator':
        """Validate chunk configuration consistency."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(f"Chunk overlap ({self.chunk_overlap}) must be less than chunk size ({self.chunk_size})")

        if self.max_chunk_size < self.chunk_size:
            raise ValueError(f"Max chunk size ({self.max_chunk_size}) must be >= chunk size ({self.chunk_size})")

        return self


class AgentDependenciesValidator(BaseModel):
    """Enhanced validator for agent dependencies."""

    session_id: str = Field(..., description="Session ID")
    database_url: Optional[str] = Field(default=None, description="Database URL")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID."""
        session_validator = SessionValidator(session_id=v)
        return session_validator.session_id

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate database URL."""
        if v is None:
            return v

        # Common database URL patterns
        db_patterns = [
            r'^postgresql://.*',
            r'^sqlite://.*',
            r'^mysql://.*',
            r'^mongodb://.*'
        ]

        if not any(re.match(pattern, v) for pattern in db_patterns):
            raise ValueError(f"Invalid database URL format: {v}")

        return v

    @field_validator('openai_api_key')
    @classmethod
    def validate_api_key(cls, v: Optional[str]) -> Optional[str]:
        """Validate OpenAI API key format."""
        if v is None:
            return v

        # OpenAI API key format: sk-...
        if not re.match(r'^sk-[a-zA-Z0-9]{48}$', v):
            raise ValueError("Invalid OpenAI API key format")

        return v


class AgentContextValidator(BaseModel):
    """Enhanced validator for agent context."""

    session_id: str = Field(..., description="Session ID")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Messages")
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list, description="Tool calls")
    search_results: List[Dict[str, Any]] = Field(default_factory=list, description="Search results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Context metadata")

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID."""
        session_validator = SessionValidator(session_id=v)
        return session_validator.session_id

    @field_validator('messages')
    @classmethod
    def validate_messages(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate messages list."""
        validated_messages = []
        for i, msg in enumerate(v):
            try:
                # Validate each message
                if 'content' not in msg or 'role' not in msg:
                    raise ValueError(f"Message {i} missing required fields")

                msg_validator = MessageValidator(
                    content=msg['content'],
                    role=msg['role'],
                    session_id="temp"  # We'll use the context session_id
                )
                validated_messages.append(msg)
            except Exception as e:
                raise ValueError(f"Invalid message at index {i}: {str(e)}")

        return validated_messages

    @field_validator('tool_calls')
    @classmethod
    def validate_tool_calls(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate tool calls list."""
        validated_calls = []
        for i, call in enumerate(v):
            try:
                if 'tool_name' not in call:
                    raise ValueError(f"Tool call {i} missing tool_name")

                tool_validator = ToolCallValidator(
                    tool_name=call['tool_name'],
                    args=call.get('args', {}),
                    tool_call_id=call.get('tool_call_id')
                )
                validated_calls.append(call)
            except Exception as e:
                raise ValueError(f"Invalid tool call at index {i}: {str(e)}")

        return validated_calls