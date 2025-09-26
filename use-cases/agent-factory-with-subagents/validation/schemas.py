"""
JSON schemas and regular expressions for comprehensive data validation.
"""

import re
from typing import Dict, Any, Pattern

# Regular expression patterns for common validation tasks
REGEX_PATTERNS: Dict[str, Pattern[str]] = {
    # Email patterns
    'email_basic': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'email_strict': re.compile(r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'),

    # URL patterns
    'url_http': re.compile(r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'),
    'url_any_scheme': re.compile(r'^[a-zA-Z][a-zA-Z\d+\-.]*://[^\s/$.?#].[^\s]*$'),

    # Phone patterns
    'phone_international': re.compile(r'^\+?[1-9]\d{1,14}$'),
    'phone_us': re.compile(r'^(\+1-?)?([0-9]{3})?[-.]?([0-9]{3})[-.]?([0-9]{4})$'),
    'phone_ru': re.compile(r'^(\+7|8)?[-.\s]?(\([0-9]{3}\)|[0-9]{3})[-.\s]?[0-9]{3}[-.\s]?[0-9]{2}[-.\s]?[0-9]{2}$'),

    # ID patterns
    'uuid4': re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'),
    'session_id': re.compile(r'^[a-zA-Z0-9_-]{8,64}$'),
    'user_id': re.compile(r'^[a-zA-Z0-9_.-]{1,100}$'),

    # Security patterns
    'no_script_tags': re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
    'no_javascript': re.compile(r'javascript:', re.IGNORECASE),
    'no_event_handlers': re.compile(r'on\w+\s*=', re.IGNORECASE),
    'no_sql_injection': re.compile(r'(union|select|insert|update|delete|drop|create|alter|exec|execute)\s+', re.IGNORECASE),

    # Content patterns
    'safe_filename': re.compile(r'^[a-zA-Z0-9_.-]+$'),
    'safe_path': re.compile(r'^[a-zA-Z0-9_./\\-]+$'),
    'tool_name': re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$'),
    'version': re.compile(r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)*$'),

    # Text cleaning patterns
    'normalize_whitespace': re.compile(r'\s+'),
    'strip_html': re.compile(r'<[^>]+>'),
    'clean_unicode': re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]'),

    # Data format patterns
    'iso_datetime': re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:\d{2})$'),
    'hex_color': re.compile(r'^#[0-9a-fA-F]{6}$'),
    'base64': re.compile(r'^[A-Za-z0-9+/]*={0,2}$'),

    # API patterns
    'openai_api_key': re.compile(r'^sk-[a-zA-Z0-9]{48}$'),
    'anthropic_api_key': re.compile(r'^sk-ant-[a-zA-Z0-9\-]{95}$'),
    'jwt_token': re.compile(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')
}

# JSON schemas for comprehensive validation
JSON_SCHEMAS: Dict[str, Dict[str, Any]] = {

    # Search request schema
    'search_request': {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000,
                "pattern": "^(?!.*<script).*$"  # No script tags
            },
            "search_type": {
                "type": "string",
                "enum": ["semantic", "keyword", "hybrid"]
            },
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
            },
            "filters": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 20
            }
        },
        "required": ["query"],
        "additionalProperties": False
    },

    # Document schema
    'document': {
        "type": "object",
        "properties": {
            "id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_-]+$"
            },
            "title": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
            },
            "content": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000000
            },
            "source": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
            },
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 50
            },
            "created_at": {
                "type": ["string", "null"],
                "format": "date-time"
            },
            "updated_at": {
                "type": ["string", "null"],
                "format": "date-time"
            }
        },
        "required": ["title", "content", "source"],
        "additionalProperties": False
    },

    # Chunk schema
    'chunk': {
        "type": "object",
        "properties": {
            "id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_-]+$"
            },
            "document_id": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9_-]+$"
            },
            "content": {
                "type": "string",
                "minLength": 1,
                "maxLength": 50000
            },
            "embedding": {
                "type": ["array", "null"],
                "items": {
                    "type": "number"
                },
                "minItems": 384,
                "maxItems": 4096
            },
            "chunk_index": {
                "type": "integer",
                "minimum": 0
            },
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 20
            },
            "token_count": {
                "type": ["integer", "null"],
                "minimum": 0
            },
            "created_at": {
                "type": ["string", "null"],
                "format": "date-time"
            }
        },
        "required": ["document_id", "content", "chunk_index"],
        "additionalProperties": False
    },

    # Session schema
    'session': {
        "type": "object",
        "properties": {
            "id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_-]{8,64}$"
            },
            "user_id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_.-]{1,100}$"
            },
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 50
            },
            "created_at": {
                "type": ["string", "null"],
                "format": "date-time"
            },
            "updated_at": {
                "type": ["string", "null"],
                "format": "date-time"
            },
            "expires_at": {
                "type": ["string", "null"],
                "format": "date-time"
            }
        },
        "additionalProperties": False
    },

    # Message schema
    'message': {
        "type": "object",
        "properties": {
            "id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_-]+$"
            },
            "session_id": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9_-]{8,64}$"
            },
            "role": {
                "type": "string",
                "enum": ["user", "assistant", "system", "tool"]
            },
            "content": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100000
            },
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 20
            },
            "created_at": {
                "type": ["string", "null"],
                "format": "date-time"
            }
        },
        "required": ["session_id", "role", "content"],
        "additionalProperties": False
    },

    # Tool call schema
    'tool_call': {
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "pattern": "^[a-zA-Z][a-zA-Z0-9_]*$",
                "maxLength": 100
            },
            "args": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 50
            },
            "tool_call_id": {
                "type": ["string", "null"],
                "pattern": "^[a-zA-Z0-9_-]{1,100}$"
            }
        },
        "required": ["tool_name"],
        "additionalProperties": False
    },

    # Agent dependencies schema
    'agent_dependencies': {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9_-]{8,64}$"
            },
            "database_url": {
                "type": ["string", "null"],
                "pattern": "^(postgresql|sqlite|mysql|mongodb)://.*"
            },
            "openai_api_key": {
                "type": ["string", "null"],
                "pattern": "^sk-[a-zA-Z0-9]{48}$"
            }
        },
        "required": ["session_id"],
        "additionalProperties": False
    },

    # Agent context schema
    'agent_context': {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9_-]{8,64}$"
            },
            "messages": {
                "type": "array",
                "items": {"$ref": "#/definitions/message"},
                "maxItems": 1000
            },
            "tool_calls": {
                "type": "array",
                "items": {"$ref": "#/definitions/tool_call"},
                "maxItems": 100
            },
            "search_results": {
                "type": "array",
                "items": {"$ref": "#/definitions/chunk_result"},
                "maxItems": 100
            },
            "metadata": {
                "type": "object",
                "additionalProperties": True,
                "maxProperties": 50
            }
        },
        "required": ["session_id"],
        "additionalProperties": False,
        "definitions": {
            "message": {"$ref": "#/message"},
            "tool_call": {"$ref": "#/tool_call"},
            "chunk_result": {
                "type": "object",
                "properties": {
                    "chunk_id": {"type": "string"},
                    "document_id": {"type": "string"},
                    "content": {"type": "string"},
                    "score": {"type": "number", "minimum": 0, "maximum": 1},
                    "metadata": {"type": "object"},
                    "document_title": {"type": "string"},
                    "document_source": {"type": "string"}
                },
                "required": ["chunk_id", "document_id", "content", "score", "document_title", "document_source"]
            }
        }
    },

    # Ingestion config schema
    'ingestion_config': {
        "type": "object",
        "properties": {
            "chunk_size": {
                "type": "integer",
                "minimum": 100,
                "maximum": 50000
            },
            "chunk_overlap": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10000
            },
            "max_chunk_size": {
                "type": "integer",
                "minimum": 500,
                "maximum": 100000
            },
            "use_semantic_chunking": {
                "type": "boolean"
            }
        },
        "required": ["chunk_size", "chunk_overlap", "max_chunk_size"],
        "additionalProperties": False
    },

    # Email validation schema
    'email': {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email",
                "maxLength": 254
            }
        },
        "required": ["email"],
        "additionalProperties": False
    },

    # URL validation schema
    'url': {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "format": "uri",
                "maxLength": 2048
            },
            "allowed_schemes": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["http", "https"]
            }
        },
        "required": ["url"],
        "additionalProperties": False
    },

    # Phone validation schema
    'phone': {
        "type": "object",
        "properties": {
            "phone": {
                "type": "string",
                "pattern": "^[\\d\\s\\-\\(\\)\\+]{7,20}$"
            },
            "country_code": {
                "type": ["string", "null"],
                "pattern": "^[A-Z]{2}$"
            }
        },
        "required": ["phone"],
        "additionalProperties": False
    },

    # Text validation schema
    'text': {
        "type": "object",
        "properties": {
            "text": {
                "type": "string"
            },
            "min_length": {
                "type": "integer",
                "minimum": 0,
                "default": 1
            },
            "max_length": {
                "type": "integer",
                "minimum": 1,
                "default": 10000
            },
            "allow_empty": {
                "type": "boolean",
                "default": False
            },
            "forbidden_patterns": {
                "type": "array",
                "items": {"type": "string"},
                "default": []
            },
            "required_patterns": {
                "type": "array",
                "items": {"type": "string"},
                "default": []
            }
        },
        "required": ["text"],
        "additionalProperties": False
    },

    # Numeric validation schema
    'numeric': {
        "type": "object",
        "properties": {
            "value": {
                "type": "number"
            },
            "min_value": {
                "type": ["number", "null"]
            },
            "max_value": {
                "type": ["number", "null"]
            },
            "allow_negative": {
                "type": "boolean",
                "default": True
            },
            "precision": {
                "type": ["integer", "null"],
                "minimum": 0
            }
        },
        "required": ["value"],
        "additionalProperties": False
    },

    # DateTime validation schema
    'datetime': {
        "type": "object",
        "properties": {
            "datetime_value": {
                "type": "string",
                "format": "date-time"
            },
            "require_timezone": {
                "type": "boolean",
                "default": True
            },
            "min_datetime": {
                "type": ["string", "null"],
                "format": "date-time"
            },
            "max_datetime": {
                "type": ["string", "null"],
                "format": "date-time"
            }
        },
        "required": ["datetime_value"],
        "additionalProperties": False
    },

    # Research query schema (from main_agent_reference)
    'research_query': {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
            },
            "max_results": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 10
            },
            "include_summary": {
                "type": "boolean",
                "default": True
            }
        },
        "required": ["query"],
        "additionalProperties": False
    },

    # Email draft schema
    'email_draft': {
        "type": "object",
        "properties": {
            "to": {
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "email"
                },
                "minItems": 1,
                "maxItems": 50
            },
            "subject": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
            },
            "body": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100000
            },
            "cc": {
                "type": ["array", "null"],
                "items": {
                    "type": "string",
                    "format": "email"
                },
                "maxItems": 50
            },
            "bcc": {
                "type": ["array", "null"],
                "items": {
                    "type": "string",
                    "format": "email"
                },
                "maxItems": 50
            }
        },
        "required": ["to", "subject", "body"],
        "additionalProperties": False
    },

    # Agent response schema
    'agent_response': {
        "type": "object",
        "properties": {
            "success": {
                "type": "boolean"
            },
            "data": {
                "type": ["object", "null"],
                "additionalProperties": True
            },
            "error": {
                "type": ["string", "null"],
                "maxLength": 1000
            },
            "tools_used": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 100
            }
        },
        "required": ["success"],
        "additionalProperties": False
    }
}

# Security validation patterns
SECURITY_PATTERNS = {
    'sql_injection': [
        r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bCREATE\b|\bALTER\b|\bEXEC\b|\bEXECUTE\b)',
        r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
        r'([\'\";].*[\'\";])',
        r'(/\*.*\*/|--.*$|#.*$)'
    ],
    'xss': [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>'
    ],
    'path_traversal': [
        r'\.\./+',
        r'\.\.\\+',
        r'%2e%2e%2f',
        r'%2e%2e\\',
        r'\.\.%2f',
        r'\.\.%5c'
    ],
    'command_injection': [
        r'[;&|`$]',
        r'\$\(',
        r'`.*`',
        r'\|\|',
        r'&&',
        r'>/dev/null'
    ]
}

# Content normalization patterns
NORMALIZATION_PATTERNS = {
    'whitespace': re.compile(r'\s+'),
    'html_tags': re.compile(r'<[^>]+>'),
    'unicode_control': re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]'),
    'multiple_newlines': re.compile(r'\n{3,}'),
    'trailing_spaces': re.compile(r'[ \t]+$', re.MULTILINE),
    'leading_spaces': re.compile(r'^[ \t]+', re.MULTILINE)
}

# Common data type validation functions
def is_valid_email(email: str) -> bool:
    """Check if email format is valid."""
    return bool(REGEX_PATTERNS['email_basic'].match(email))

def is_valid_url(url: str) -> bool:
    """Check if URL format is valid."""
    return bool(REGEX_PATTERNS['url_http'].match(url))

def is_valid_uuid(uuid: str) -> bool:
    """Check if UUID format is valid."""
    return bool(REGEX_PATTERNS['uuid4'].match(uuid))

def is_valid_session_id(session_id: str) -> bool:
    """Check if session ID format is valid."""
    return bool(REGEX_PATTERNS['session_id'].match(session_id))

def contains_security_threats(text: str) -> tuple[bool, list[str]]:
    """Check for common security threats in text."""
    threats = []

    for threat_type, patterns in SECURITY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                threats.append(threat_type)
                break

    return bool(threats), threats

def normalize_text(text: str) -> str:
    """Normalize text content."""
    # Remove control characters
    text = NORMALIZATION_PATTERNS['unicode_control'].sub('', text)

    # Normalize whitespace
    text = NORMALIZATION_PATTERNS['whitespace'].sub(' ', text)

    # Remove excessive newlines
    text = NORMALIZATION_PATTERNS['multiple_newlines'].sub('\n\n', text)

    # Clean up line spacing
    text = NORMALIZATION_PATTERNS['trailing_spaces'].sub('', text)
    text = NORMALIZATION_PATTERNS['leading_spaces'].sub('', text)

    return text.strip()

def strip_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    return NORMALIZATION_PATTERNS['html_tags'].sub('', text)

# Export all schemas and patterns
__all__ = [
    'REGEX_PATTERNS',
    'JSON_SCHEMAS',
    'SECURITY_PATTERNS',
    'NORMALIZATION_PATTERNS',
    'is_valid_email',
    'is_valid_url',
    'is_valid_uuid',
    'is_valid_session_id',
    'contains_security_threats',
    'normalize_text',
    'strip_html_tags'
]