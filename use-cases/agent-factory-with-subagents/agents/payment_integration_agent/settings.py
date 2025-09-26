"""
Universal Payment Integration Agent Settings.

Configurable settings supporting multiple providers and environments.
"""

import os
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class PaymentAgentSettings(BaseSettings):
    """Universal settings for Payment Integration Agent."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ===== CORE LLM CONFIGURATION =====
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="LLM API key")
    llm_model: str = Field(default="qwen2.5-coder-32b-instruct", description="LLM model name")
    llm_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="LLM API base URL"
    )

    # ===== COST-OPTIMIZED MODEL CONFIGURATION =====
    # Payment analysis and complex financial logic - Premium Qwen
    llm_payment_analysis_model: str = Field(
        default="qwen2.5-72b-instruct",
        description="Model for payment analysis and complex financial logic"
    )

    # Payment integration code generation - Qwen Coder
    llm_payment_coding_model: str = Field(
        default="qwen2.5-coder-32b-instruct",
        description="Model for payment integration code generation"
    )

    # Documentation and validation - Ultra-cheap Gemini
    llm_payment_docs_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Model for payment documentation and validation"
    )

    # Webhook processing and event handling - Fast Qwen Coder
    llm_webhook_model: str = Field(
        default="qwen2.5-coder-7b-instruct",
        description="Model for webhook processing and event handling"
    )

    # Alternative API keys
    gemini_api_key: str = Field(..., description="Google Gemini API key")

    # ===== PAYMENT AGENT CONFIGURATION =====
    agent_name: str = Field(default="Payment Integration Agent", description="Agent name")
    agent_version: str = Field(default="1.0.0", description="Agent version")

    # Default payment provider settings
    default_payment_provider: str = Field(default="stripe", description="Default payment provider")
    default_business_model: str = Field(default="ecommerce", description="Default business model")
    default_currency: str = Field(default="USD", description="Default currency")

    # ===== KNOWLEDGE BASE & RAG =====
    archon_url: str = Field(default="http://localhost:3737", description="Archon Knowledge Base URL")
    knowledge_base_enabled: bool = Field(default=True, description="Enable knowledge base integration")

    # Knowledge base configuration
    default_knowledge_tags: list[str] = Field(
        default_factory=lambda: ["payment-integration", "agent-knowledge", "pydantic-ai"],
        description="Default knowledge base tags"
    )

    # ===== PERFORMANCE SETTINGS =====
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout_seconds: int = Field(default=60, description="Request timeout in seconds")
    enable_caching: bool = Field(default=True, description="Enable response caching")

    # Rate limiting
    max_requests_per_minute: int = Field(default=60, description="Max requests per minute")
    max_requests_per_hour: int = Field(default=1000, description="Max requests per hour")

    # ===== DEVELOPMENT SETTINGS =====
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    enable_verbose_logging: bool = Field(default=False, description="Enable verbose logging")

    # Development features
    hot_reload: bool = Field(default=True, description="Enable hot reload")
    auto_save: bool = Field(default=True, description="Enable auto save")

    # ===== SECURITY SETTINGS =====
    enable_input_validation: bool = Field(default=True, description="Enable input validation")
    max_input_length: int = Field(default=10000, description="Maximum input length")
    sanitize_inputs: bool = Field(default=True, description="Sanitize user inputs")

    # Security defaults
    default_encryption_level: str = Field(default="tls_1_2", description="Default encryption level")
    enable_audit_logging: bool = Field(default=True, description="Enable audit logging")

    # ===== PAYMENT PROVIDER DEFAULTS =====
    # Stripe
    stripe_api_version: str = Field(default="2024-06-20", description="Stripe API version")
    stripe_webhook_tolerance: int = Field(default=300, description="Stripe webhook tolerance (seconds)")

    # PayPal
    paypal_api_version: str = Field(default="v2", description="PayPal API version")
    paypal_sandbox_mode: bool = Field(default=True, description="PayPal sandbox mode")

    # Square
    square_api_version: str = Field(default="2024-06-04", description="Square API version")
    square_environment: str = Field(default="sandbox", description="Square environment")

    # Razorpay
    razorpay_api_version: str = Field(default="v1", description="Razorpay API version")

    # Braintree
    braintree_environment: str = Field(default="sandbox", description="Braintree environment")

    # Adyen
    adyen_api_version: str = Field(default="71", description="Adyen API version")
    adyen_environment: str = Field(default="test", description="Adyen environment")

    # ===== BUSINESS MODEL DEFAULTS =====
    # E-commerce
    ecommerce_tax_calculation: bool = Field(default=True, description="Enable tax calculation for e-commerce")
    ecommerce_inventory_sync: bool = Field(default=True, description="Enable inventory sync")
    ecommerce_abandoned_cart: bool = Field(default=True, description="Enable abandoned cart recovery")

    # SaaS
    saas_subscription_management: bool = Field(default=True, description="Enable subscription management")
    saas_usage_tracking: bool = Field(default=True, description="Enable usage tracking")
    saas_dunning_management: bool = Field(default=True, description="Enable dunning management")

    # Marketplace
    marketplace_split_payments: bool = Field(default=True, description="Enable split payments")
    marketplace_vendor_onboarding: bool = Field(default=True, description="Enable vendor onboarding")
    marketplace_escrow: bool = Field(default=False, description="Enable escrow payments")

    # Donation
    donation_recurring_setup: bool = Field(default=True, description="Enable recurring donations")
    donation_tax_receipts: bool = Field(default=True, description="Enable tax receipts")
    donation_anonymous_support: bool = Field(default=True, description="Enable anonymous donations")

    # Gaming
    gaming_virtual_currency: bool = Field(default=True, description="Enable virtual currency")
    gaming_anti_fraud: bool = Field(default=True, description="Enable gaming anti-fraud")
    gaming_chargeback_protection: bool = Field(default=True, description="Enable chargeback protection")

    # P2P
    p2p_kyc_verification: bool = Field(default=True, description="Enable KYC verification")
    p2p_transaction_limits: bool = Field(default=True, description="Enable transaction limits")
    p2p_real_time_processing: bool = Field(default=True, description="Enable real-time processing")

    # ===== COMPLIANCE DEFAULTS =====
    # PCI DSS
    pci_dss_level: str = Field(default="saq_a", description="PCI DSS compliance level")
    enable_pci_scanning: bool = Field(default=True, description="Enable PCI vulnerability scanning")

    # GDPR
    gdpr_data_retention_days: int = Field(default=2555, description="GDPR data retention period (7 years)")
    gdpr_anonymization: bool = Field(default=True, description="Enable GDPR data anonymization")

    # PSD2
    psd2_sca_exemptions: bool = Field(default=True, description="Enable PSD2 SCA exemptions")
    psd2_transaction_risk_analysis: bool = Field(default=True, description="Enable transaction risk analysis")

    # KYC/AML
    kyc_verification_level: str = Field(default="standard", description="KYC verification level")
    aml_screening_enabled: bool = Field(default=False, description="Enable AML screening")

    # ===== MONITORING & OBSERVABILITY =====
    # Metrics
    metrics_provider: str = Field(default="prometheus", description="Metrics provider")
    enable_custom_metrics: bool = Field(default=True, description="Enable custom metrics")

    # Logging
    log_format: str = Field(default="json", description="Log format")
    enable_structured_logging: bool = Field(default=True, description="Enable structured logging")

    # Alerting
    alert_webhook_url: Optional[str] = Field(default=None, description="Alert webhook URL")
    alert_on_failed_payments: bool = Field(default=True, description="Alert on failed payments")
    alert_on_high_decline_rate: bool = Field(default=True, description="Alert on high decline rate")

    # ===== TESTING CONFIGURATION =====
    enable_test_mode: bool = Field(default=True, description="Enable test mode")
    test_card_numbers: list[str] = Field(
        default_factory=lambda: [
            "4242424242424242",  # Visa
            "5555555555554444",  # Mastercard
            "378282246310005",   # Amex
        ],
        description="Test card numbers"
    )

    # Testing features
    enable_webhook_testing: bool = Field(default=True, description="Enable webhook testing")
    webhook_test_endpoint: str = Field(default="https://webhook.site", description="Webhook test endpoint")

    # ===== ADVANCED CONFIGURATION =====
    # Experimental features
    enable_experimental_features: bool = Field(default=False, description="Enable experimental features")
    enable_ai_fraud_detection: bool = Field(default=True, description="Enable AI fraud detection")
    enable_smart_routing: bool = Field(default=False, description="Enable smart payment routing")

    # Performance optimization
    enable_payment_optimization: bool = Field(default=True, description="Enable payment optimization")
    enable_conversion_tracking: bool = Field(default=True, description="Enable conversion tracking")
    enable_a_b_testing: bool = Field(default=False, description="Enable A/B testing")

    # Integration settings
    webhook_signature_verification: bool = Field(default=True, description="Enable webhook signature verification")
    api_versioning_strategy: str = Field(default="header", description="API versioning strategy")
    enable_idempotency: bool = Field(default=True, description="Enable idempotency keys")

    # ===== ENVIRONMENT PATHS =====
    project_root: str = Field(default=".", description="Project root directory")
    output_directory: str = Field(default="./generated", description="Output directory")
    backup_directory: str = Field(default="./backups", description="Backup directory")
    logs_directory: str = Field(default="./logs", description="Logs directory")


def load_settings() -> PaymentAgentSettings:
    """
    Load payment agent settings from environment variables and .env file.

    Returns:
        Configured PaymentAgentSettings instance

    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    try:
        settings = PaymentAgentSettings()

        # Validate critical settings
        if not settings.llm_api_key or settings.llm_api_key == "your_api_key_here":
            raise ValueError(
                "LLM_API_KEY is required. Please set it in your .env file or environment variables."
            )

        if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is required for cost optimization. Please set it in your .env file."
            )

        return settings

    except Exception as e:
        error_msg = f"Failed to load payment agent settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\n\nPlease ensure LLM_API_KEY is set in your .env file:"
            error_msg += "\nLLM_API_KEY=your_actual_api_key_here"
        raise ValueError(error_msg) from e


def get_llm_model(task_type: str = "default") -> OpenAIModel:
    """
    Get cost-optimized LLM model based on task type.

    Args:
        task_type: Type of task (default, analysis, coding, docs, webhook)

    Returns:
        Configured OpenAI model instance
    """
    settings = load_settings()

    # Select model based on task type for cost optimization
    model_map = {
        "default": settings.llm_model,
        "analysis": settings.llm_payment_analysis_model,
        "coding": settings.llm_payment_coding_model,
        "docs": settings.llm_payment_docs_model,
        "webhook": settings.llm_webhook_model,
    }

    model_name = model_map.get(task_type, settings.llm_model)

    # Configure provider based on model
    if model_name.startswith("gemini"):
        # Use Gemini for cost-effective tasks
        provider = OpenAIProvider(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.gemini_api_key
        )
    else:
        # Use Qwen for specialized tasks
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )

    return OpenAIModel(model_name, provider=provider)


def get_provider_specific_settings(provider: str) -> Dict[str, Any]:
    """
    Get provider-specific configuration settings.

    Args:
        provider: Payment provider name

    Returns:
        Provider-specific settings dictionary
    """
    settings = load_settings()

    provider_settings = {
        "stripe": {
            "api_version": settings.stripe_api_version,
            "webhook_tolerance": settings.stripe_webhook_tolerance,
            "endpoint_secret_required": True,
            "supports_payment_intents": True,
            "supports_setup_intents": True,
            "supports_connect": True
        },
        "paypal": {
            "api_version": settings.paypal_api_version,
            "sandbox_mode": settings.paypal_sandbox_mode,
            "supports_orders_api": True,
            "supports_subscriptions": True,
            "supports_marketplace": True
        },
        "square": {
            "api_version": settings.square_api_version,
            "environment": settings.square_environment,
            "supports_web_payments": True,
            "supports_in_person": True,
            "supports_invoices": True
        },
        "razorpay": {
            "api_version": settings.razorpay_api_version,
            "supports_payment_links": True,
            "supports_subscriptions": True,
            "supports_smart_collect": True,
            "supports_route": True
        },
        "braintree": {
            "environment": settings.braintree_environment,
            "supports_drop_in": True,
            "supports_hosted_fields": True,
            "supports_vault": True,
            "supports_marketplace": True
        },
        "adyen": {
            "api_version": settings.adyen_api_version,
            "environment": settings.adyen_environment,
            "supports_checkout": True,
            "supports_platforms": True,
            "supports_local_methods": True
        }
    }

    return provider_settings.get(provider, {})


def get_business_model_settings(business_model: str) -> Dict[str, Any]:
    """
    Get business model specific configuration settings.

    Args:
        business_model: Business model name

    Returns:
        Business model specific settings dictionary
    """
    settings = load_settings()

    business_settings = {
        "ecommerce": {
            "tax_calculation": settings.ecommerce_tax_calculation,
            "inventory_sync": settings.ecommerce_inventory_sync,
            "abandoned_cart": settings.ecommerce_abandoned_cart,
            "recommended_providers": ["stripe", "paypal", "square"],
            "required_features": ["refunds", "webhooks", "fraud_detection"]
        },
        "saas": {
            "subscription_management": settings.saas_subscription_management,
            "usage_tracking": settings.saas_usage_tracking,
            "dunning_management": settings.saas_dunning_management,
            "recommended_providers": ["stripe", "braintree"],
            "required_features": ["subscriptions", "trials", "proration"]
        },
        "marketplace": {
            "split_payments": settings.marketplace_split_payments,
            "vendor_onboarding": settings.marketplace_vendor_onboarding,
            "escrow": settings.marketplace_escrow,
            "recommended_providers": ["stripe", "paypal", "braintree"],
            "required_features": ["connect", "split_payments", "kyc"]
        },
        "donation": {
            "recurring_setup": settings.donation_recurring_setup,
            "tax_receipts": settings.donation_tax_receipts,
            "anonymous_support": settings.donation_anonymous_support,
            "recommended_providers": ["stripe", "paypal"],
            "required_features": ["recurring", "reporting", "low_fees"]
        },
        "gaming": {
            "virtual_currency": settings.gaming_virtual_currency,
            "anti_fraud": settings.gaming_anti_fraud,
            "chargeback_protection": settings.gaming_chargeback_protection,
            "recommended_providers": ["adyen", "braintree"],
            "required_features": ["fraud_detection", "chargeback_protection"]
        },
        "p2p": {
            "kyc_verification": settings.p2p_kyc_verification,
            "transaction_limits": settings.p2p_transaction_limits,
            "real_time_processing": settings.p2p_real_time_processing,
            "recommended_providers": ["stripe", "adyen"],
            "required_features": ["kyc", "aml", "instant_transfers"]
        }
    }

    return business_settings.get(business_model, {})


def get_compliance_settings(regions: list[str]) -> Dict[str, Any]:
    """
    Get compliance settings based on operating regions.

    Args:
        regions: List of operating regions/countries

    Returns:
        Compliance settings dictionary
    """
    settings = load_settings()

    compliance_config = {
        "pci_dss": {
            "level": settings.pci_dss_level,
            "scanning_enabled": settings.enable_pci_scanning
        },
        "gdpr": {
            "applicable": any(region in ["EU", "UK"] for region in regions),
            "data_retention_days": settings.gdpr_data_retention_days,
            "anonymization": settings.gdpr_anonymization
        },
        "psd2": {
            "applicable": "EU" in regions,
            "sca_exemptions": settings.psd2_sca_exemptions,
            "risk_analysis": settings.psd2_transaction_risk_analysis
        },
        "kyc_aml": {
            "verification_level": settings.kyc_verification_level,
            "screening_enabled": settings.aml_screening_enabled
        }
    }

    return compliance_config


# Convenience function to get settings
def get_settings() -> PaymentAgentSettings:
    """Get payment agent settings instance."""
    return load_settings()