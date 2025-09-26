"""
Tests for the enhanced Pydantic validators.
"""

import pytest
from datetime import datetime, timezone
from typing import List
from pydantic import ValidationError

from ..validators import (
    EmailValidator, URLValidator, PhoneValidator, TextValidator,
    NumericValidator, DateTimeValidator, SearchRequestValidator,
    DocumentValidator, ChunkValidator, SessionValidator,
    MessageValidator, ToolCallValidator
)


class TestEmailValidator:
    """Test email validation."""

    def test_valid_emails(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@subdomain.example.org",
            "123@numbers.com"
        ]

        for email in valid_emails:
            validator = EmailValidator(email=email)
            assert validator.email in [email, email.lower()]

    def test_invalid_emails(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "not-an-email",
            "@domain.com",
            "user@",
            "user@domain",
            "user space@domain.com",
            ""
        ]

        for email in invalid_emails:
            with pytest.raises(ValidationError):
                EmailValidator(email=email)

    def test_email_normalization(self):
        """Test email normalization."""
        validator = EmailValidator(email="  Test@EXAMPLE.COM  ")
        assert validator.email == "test@example.com"


class TestURLValidator:
    """Test URL validation."""

    def test_valid_urls(self):
        """Test valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://subdomain.example.org/path",
            "https://example.com:8080/path?query=value#fragment"
        ]

        for url in valid_urls:
            validator = URLValidator(url=url)
            assert validator.url == url

    def test_url_scheme_addition(self):
        """Test automatic scheme addition."""
        validator = URLValidator(url="example.com")
        assert validator.url == "https://example.com"

    def test_invalid_urls(self):
        """Test invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "ftp://invalid-scheme.com",  # Not in allowed schemes
            "",
            "just-text"
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError):
                URLValidator(url=url, allowed_schemes=['http', 'https'])

    def test_custom_allowed_schemes(self):
        """Test custom allowed schemes."""
        validator = URLValidator(url="ftp://example.com", allowed_schemes=['ftp', 'http'])
        assert validator.url == "ftp://example.com"


class TestPhoneValidator:
    """Test phone number validation."""

    def test_valid_phone_numbers(self):
        """Test valid phone numbers."""
        valid_phones = [
            ("+1234567890", "US"),
            ("+79991234567", "RU"),
            ("1234567890", "US")
        ]

        for phone, country in valid_phones:
            validator = PhoneValidator(phone=phone, country_code=country)
            assert validator.phone.startswith('+')

    def test_phone_normalization(self):
        """Test phone number normalization."""
        validator = PhoneValidator(phone="(123) 456-7890", country_code="US")
        assert validator.phone == "+11234567890"

    def test_invalid_phone_numbers(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            "not-a-phone",
            "123",
            "+invalid",
            ""
        ]

        for phone in invalid_phones:
            with pytest.raises(ValidationError):
                PhoneValidator(phone=phone)


class TestTextValidator:
    """Test text validation."""

    def test_basic_text_validation(self):
        """Test basic text validation."""
        validator = TextValidator(text="  Hello World  ")
        assert validator.text == "Hello World"

    def test_length_constraints(self):
        """Test text length constraints."""
        # Valid length
        validator = TextValidator(text="Hello", min_length=3, max_length=10)
        assert validator.text == "Hello"

        # Too short
        with pytest.raises(ValidationError):
            TextValidator(text="Hi", min_length=5)

        # Too long
        with pytest.raises(ValidationError):
            TextValidator(text="Very long text", max_length=5)

    def test_forbidden_patterns(self):
        """Test forbidden patterns."""
        with pytest.raises(ValidationError):
            TextValidator(
                text="<script>alert('xss')</script>",
                forbidden_patterns=[r'<script.*?>']
            )

    def test_required_patterns(self):
        """Test required patterns."""
        with pytest.raises(ValidationError):
            TextValidator(
                text="No numbers here",
                required_patterns=[r'\d+']
            )

        # Valid case
        validator = TextValidator(
            text="Has 123 numbers",
            required_patterns=[r'\d+']
        )
        assert "123" in validator.text


class TestNumericValidator:
    """Test numeric validation."""

    def test_valid_numbers(self):
        """Test valid numeric values."""
        validator = NumericValidator(value=42.5)
        assert validator.value == 42.5

    def test_range_constraints(self):
        """Test numeric range constraints."""
        # Valid range
        validator = NumericValidator(value=50, min_value=0, max_value=100)
        assert validator.value == 50

        # Below minimum
        with pytest.raises(ValidationError):
            NumericValidator(value=-10, min_value=0)

        # Above maximum
        with pytest.raises(ValidationError):
            NumericValidator(value=150, max_value=100)

    def test_negative_values(self):
        """Test negative value handling."""
        with pytest.raises(ValidationError):
            NumericValidator(value=-5, allow_negative=False)

    def test_precision_handling(self):
        """Test decimal precision."""
        validator = NumericValidator(value=3.14159, precision=2)
        assert validator.value == 3.14


class TestDateTimeValidator:
    """Test datetime validation."""

    def test_valid_datetime(self):
        """Test valid datetime values."""
        dt = datetime.now(timezone.utc)
        validator = DateTimeValidator(datetime_value=dt)
        assert validator.datetime_value == dt

    def test_timezone_requirement(self):
        """Test timezone requirement."""
        dt_without_tz = datetime.now()
        with pytest.raises(ValidationError):
            DateTimeValidator(datetime_value=dt_without_tz, require_timezone=True)

    def test_datetime_range(self):
        """Test datetime range constraints."""
        dt = datetime.now(timezone.utc)
        min_dt = dt.replace(year=2020)
        max_dt = dt.replace(year=2030)

        # Valid range
        validator = DateTimeValidator(
            datetime_value=dt,
            min_datetime=min_dt,
            max_datetime=max_dt
        )
        assert validator.datetime_value == dt

        # Before minimum
        with pytest.raises(ValidationError):
            DateTimeValidator(
                datetime_value=dt.replace(year=2019),
                min_datetime=min_dt
            )


class TestSearchRequestValidator:
    """Test search request validation."""

    def test_valid_search_request(self):
        """Test valid search request."""
        validator = SearchRequestValidator(
            query="test search",
            search_type="semantic",
            limit=10
        )
        assert validator.query == "test search"
        assert validator.search_type == "semantic"
        assert validator.limit == 10

    def test_invalid_search_type(self):
        """Test invalid search type."""
        with pytest.raises(ValidationError):
            SearchRequestValidator(
                query="test",
                search_type="invalid_type"
            )

    def test_query_security(self):
        """Test query security validation."""
        with pytest.raises(ValidationError):
            SearchRequestValidator(query="<script>alert('xss')</script>")


class TestDocumentValidator:
    """Test document validation."""

    def test_valid_document(self):
        """Test valid document."""
        validator = DocumentValidator(
            title="Test Document",
            content="This is test content.",
            source="https://example.com/doc.pdf"
        )
        assert validator.title == "Test Document"
        assert validator.content == "This is test content."
        assert validator.source == "https://example.com/doc.pdf"

    def test_document_html_filtering(self):
        """Test HTML filtering in title."""
        with pytest.raises(ValidationError):
            DocumentValidator(
                title="<h1>Title</h1>",
                content="Content",
                source="file.txt"
            )

    def test_large_content(self):
        """Test large content handling."""
        large_content = "x" * 2000000  # 2MB
        with pytest.raises(ValidationError):
            DocumentValidator(
                title="Large Doc",
                content=large_content,
                source="file.txt"
            )


class TestChunkValidator:
    """Test chunk validation."""

    def test_valid_chunk(self):
        """Test valid chunk."""
        validator = ChunkValidator(
            content="This is chunk content.",
            chunk_index=0,
            token_count=5
        )
        assert validator.content == "This is chunk content."
        assert validator.chunk_index == 0
        assert validator.token_count == 5

    def test_embedding_validation(self):
        """Test embedding validation."""
        # Valid embedding
        embedding = [0.1] * 1536  # OpenAI embedding size
        validator = ChunkValidator(
            content="Content",
            chunk_index=0,
            embedding=embedding
        )
        assert len(validator.embedding) == 1536

        # Invalid embedding size
        with pytest.raises(ValidationError):
            ChunkValidator(
                content="Content",
                chunk_index=0,
                embedding=[0.1] * 100  # Wrong size
            )


class TestSessionValidator:
    """Test session validation."""

    def test_valid_session(self):
        """Test valid session."""
        validator = SessionValidator(
            session_id="sess_1234567890abcdef",
            user_id="user123"
        )
        assert validator.session_id == "sess_1234567890abcdef"
        assert validator.user_id == "user123"

    def test_invalid_session_id(self):
        """Test invalid session ID."""
        invalid_ids = [
            "short",
            "contains spaces",
            "contains@symbols",
            ""
        ]

        for session_id in invalid_ids:
            with pytest.raises(ValidationError):
                SessionValidator(session_id=session_id)


class TestMessageValidator:
    """Test message validation."""

    def test_valid_message(self):
        """Test valid message."""
        validator = MessageValidator(
            content="Hello, world!",
            role="user",
            session_id="sess_1234567890abcdef"
        )
        assert validator.content == "Hello, world!"
        assert validator.role == "user"

    def test_invalid_role(self):
        """Test invalid message role."""
        with pytest.raises(ValidationError):
            MessageValidator(
                content="Content",
                role="invalid_role",
                session_id="sess_1234567890abcdef"
            )

    def test_large_message(self):
        """Test large message handling."""
        large_content = "x" * 200000  # 200k characters
        with pytest.raises(ValidationError):
            MessageValidator(
                content=large_content,
                role="user",
                session_id="sess_1234567890abcdef"
            )


class TestToolCallValidator:
    """Test tool call validation."""

    def test_valid_tool_call(self):
        """Test valid tool call."""
        validator = ToolCallValidator(
            tool_name="search_documents",
            args={"query": "test", "limit": 10},
            tool_call_id="call_123"
        )
        assert validator.tool_name == "search_documents"
        assert validator.args == {"query": "test", "limit": 10}
        assert validator.tool_call_id == "call_123"

    def test_invalid_tool_name(self):
        """Test invalid tool name."""
        invalid_names = [
            "123invalid",  # Can't start with number
            "tool-name",   # Can't contain hyphens
            "tool name",   # Can't contain spaces
            ""
        ]

        for tool_name in invalid_names:
            with pytest.raises(ValidationError):
                ToolCallValidator(tool_name=tool_name)

    def test_optional_tool_call_id(self):
        """Test optional tool call ID."""
        validator = ToolCallValidator(
            tool_name="test_tool",
            args={}
        )
        assert validator.tool_call_id is None


# Integration tests
class TestValidatorIntegration:
    """Test validator integration scenarios."""

    def test_complete_agent_input(self):
        """Test complete agent input validation."""
        # This would test a complete workflow with multiple validators
        session_validator = SessionValidator(session_id="sess_abc123def456")
        message_validator = MessageValidator(
            content="Search for AI research papers",
            role="user",
            session_id=session_validator.session_id
        )
        search_validator = SearchRequestValidator(
            query="AI research papers",
            search_type="semantic",
            limit=20
        )

        assert session_validator.session_id == "sess_abc123def456"
        assert message_validator.content == "Search for AI research papers"
        assert search_validator.query == "AI research papers"

    def test_document_processing_pipeline(self):
        """Test document processing pipeline validation."""
        document_validator = DocumentValidator(
            title="Research Paper",
            content="This is a research paper about AI.",
            source="https://arxiv.org/abs/2301.12345"
        )

        chunk_validator = ChunkValidator(
            content="This is a research paper about AI.",
            chunk_index=0,
            token_count=8
        )

        assert document_validator.title == "Research Paper"
        assert chunk_validator.content == document_validator.content
        assert chunk_validator.chunk_index == 0

    def test_error_accumulation(self):
        """Test error accumulation across multiple validators."""
        errors = []

        try:
            EmailValidator(email="invalid-email")
        except ValidationError as e:
            errors.extend(e.errors())

        try:
            URLValidator(url="not-a-url")
        except ValidationError as e:
            errors.extend(e.errors())

        try:
            PhoneValidator(phone="123")
        except ValidationError as e:
            errors.extend(e.errors())

        assert len(errors) >= 3  # At least one error from each validator