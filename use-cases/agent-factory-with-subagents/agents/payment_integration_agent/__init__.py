"""
Universal Payment Integration Agent for Pydantic AI.

Comprehensive AI agent for payment system integration supporting multiple providers
and business models including Stripe, PayPal, Square, Razorpay, Braintree, and Adyen.

Features:
- Universal payment provider support (8+ providers)
- Adaptive prompts for different business models
- Comprehensive security and compliance configuration
- Business model optimizations (e-commerce, SaaS, marketplace, etc.)
- Webhook processing and event handling
- Fraud detection and risk management
- Multi-currency and localization support
- Subscription and recurring payment management
"""

from .agent import (
    payment_integration_agent,
    get_payment_integration_agent,
    run_payment_integration_agent,
    process_payment_request,
    validate_webhook_event,
    process_payment_refund,
    get_payment_configuration_analysis,
    create_ecommerce_payment_agent,
    create_saas_payment_agent,
    create_marketplace_payment_agent,
    create_donation_payment_agent
)
from .dependencies import PaymentAgentDependencies
from .settings import (
    PaymentAgentSettings,
    load_settings,
    get_settings,
    get_llm_model,
    get_provider_specific_settings,
    get_business_model_settings,
    get_compliance_settings
)
from .tools import (
    search_payment_knowledge,
    create_payment,
    verify_webhook_signature,
    process_refund,
    validate_payment_configuration,
    PaymentRequest,
    PaymentResponse,
    RefundRequest,
    WebhookEvent
)

__version__ = "1.0.0"
__author__ = "AI Agent Factory"
__license__ = "MIT"

# Supported payment providers
SUPPORTED_PROVIDERS = [
    "stripe",
    "paypal",
    "square",
    "razorpay",
    "braintree",
    "adyen",
    "mollie",
    "checkout"
]

# Supported business models
SUPPORTED_BUSINESS_MODELS = [
    "ecommerce",
    "saas",
    "marketplace",
    "donation",
    "subscription",
    "p2p",
    "gaming"
]

# Supported payment types
SUPPORTED_PAYMENT_TYPES = [
    "card",
    "bank_transfer",
    "digital_wallet",
    "crypto",
    "buy_now_pay_later"
]

__all__ = [
    # Agent functions
    "payment_integration_agent",
    "get_payment_integration_agent",
    "run_payment_integration_agent",
    "process_payment_request",
    "validate_webhook_event",
    "process_payment_refund",
    "get_payment_configuration_analysis",

    # Business model specific agents
    "create_ecommerce_payment_agent",
    "create_saas_payment_agent",
    "create_marketplace_payment_agent",
    "create_donation_payment_agent",

    # Dependencies and settings
    "PaymentAgentDependencies",
    "PaymentAgentSettings",
    "load_settings",
    "get_settings",
    "get_llm_model",
    "get_provider_specific_settings",
    "get_business_model_settings",
    "get_compliance_settings",

    # Tools and models
    "search_payment_knowledge",
    "create_payment",
    "verify_webhook_signature",
    "process_refund",
    "validate_payment_configuration",
    "PaymentRequest",
    "PaymentResponse",
    "RefundRequest",
    "WebhookEvent",

    # Constants
    "SUPPORTED_PROVIDERS",
    "SUPPORTED_BUSINESS_MODELS",
    "SUPPORTED_PAYMENT_TYPES"
]