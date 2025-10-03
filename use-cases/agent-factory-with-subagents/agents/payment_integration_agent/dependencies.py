"""
Universal Payment Integration Agent Dependencies.

Configurable dependencies supporting multiple payment providers and scenarios.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from decimal import Decimal


@dataclass
class PaymentAgentDependencies:
    """Universal dependencies for Payment Integration Agent."""

    # Core payment settings
    api_key: str
    agent_name: str = "payment_integration"  # For RAG protection
    project_path: str = ""
    project_name: str = ""

    # Universal payment configuration
    payment_provider: str = "stripe"  # stripe, paypal, square, razorpay, braintree, adyen, mollie, checkout
    payment_types: List[str] = field(default_factory=lambda: ["card", "bank_transfer"])  # card, bank_transfer, digital_wallet, crypto, buy_now_pay_later
    business_model: str = "ecommerce"  # ecommerce, saas, marketplace, donation, subscription, p2p, gaming

    # Payment flow configuration
    payment_flow: str = "checkout"  # checkout, hosted, embedded, mobile, api_only
    capture_method: str = "automatic"  # automatic, manual, delayed
    confirmation_method: str = "automatic"  # automatic, manual

    # Currency and localization
    default_currency: str = "USD"
    supported_currencies: List[str] = field(default_factory=lambda: ["USD", "EUR", "GBP"])
    multi_currency: bool = False
    currency_conversion: bool = False
    locale_support: List[str] = field(default_factory=lambda: ["en-US"])

    # Security and compliance
    pci_compliance: str = "pci_dss_saq_a"  # pci_dss_saq_a, pci_dss_saq_d, custom
    encryption_at_rest: bool = True
    encryption_in_transit: bool = True
    secure_card_storage: bool = True
    tokenization: bool = True

    # Fraud detection and risk management
    fraud_detection: str = "basic"  # basic, advanced, machine_learning, custom
    risk_scoring: bool = True
    velocity_checks: bool = True
    geolocation_checks: bool = True
    blacklist_checks: bool = True

    # Subscription and recurring payments
    subscription_support: bool = False
    recurring_billing: bool = False
    trial_periods: bool = False
    proration_handling: bool = False
    dunning_management: bool = False

    # Marketplace and multi-party payments
    marketplace_support: bool = False
    split_payments: bool = False
    platform_fees: bool = False
    escrow_support: bool = False
    vendor_onboarding: bool = False

    # Webhook and event handling
    webhook_enabled: bool = True
    webhook_security: str = "signature_verification"  # signature_verification, ip_whitelist, both
    event_processing: str = "immediate"  # immediate, queued, batch
    retry_logic: bool = True
    dead_letter_queue: bool = True

    # Payment analytics and reporting
    analytics_enabled: bool = True
    real_time_reporting: bool = False
    revenue_analytics: bool = True
    fraud_analytics: bool = True
    churn_analytics: bool = False

    # Refunds and disputes
    refund_support: bool = True
    partial_refunds: bool = True
    dispute_management: bool = True
    chargeback_protection: bool = False
    automated_responses: bool = False

    # Developer experience
    sandbox_mode: bool = True
    test_cards: bool = True
    webhook_testing: bool = True
    api_documentation: str = "openapi"  # openapi, postman, custom
    sdk_generation: bool = True

    # Integration settings
    framework_integration: str = "universal"  # universal, react, vue, angular, nodejs, python, php, ruby
    mobile_sdk: List[str] = field(default_factory=list)  # ios, android, react_native, flutter
    ecommerce_platform: str = "custom"  # custom, shopify, woocommerce, magento, bigcommerce

    # Performance and reliability
    api_timeout: int = 30
    retry_attempts: int = 3
    rate_limiting: bool = True
    caching_enabled: bool = True
    load_balancing: bool = False

    # Compliance and regulations
    gdpr_compliance: bool = True
    psd2_compliance: bool = False
    strong_customer_authentication: bool = False
    kyc_requirements: bool = False
    aml_checks: bool = False

    # Advanced features
    advanced_config: Dict[str, Any] = field(default_factory=dict)

    # RAG and knowledge integration
    knowledge_tags: List[str] = field(default_factory=lambda: ["payment-integration", "agent-knowledge", "pydantic-ai"])
    knowledge_domain: Optional[str] = None
    archon_project_id: Optional[str] = None

    # Session management
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization configuration."""
        # Auto-configure provider-specific settings
        self._configure_provider_defaults()
        self._set_business_model_optimizations()
        self._configure_compliance_requirements()

        # Set knowledge domain based on provider
        if not self.knowledge_domain:
            provider_domains = {
                "stripe": "docs.stripe.com",
                "paypal": "developer.paypal.com",
                "square": "developer.squareup.com",
                "razorpay": "razorpay.com/docs",
                "braintree": "developers.braintreepayments.com",
                "adyen": "docs.adyen.com"
            }
            self.knowledge_domain = provider_domains.get(self.payment_provider, "payments.universal.com")

    def _configure_provider_defaults(self):
        """Configure provider-specific default settings."""
        provider_configs = {
            "stripe": {
                "pci_compliance": "pci_dss_saq_a",
                "tokenization": True,
                "webhook_security": "signature_verification",
                "fraud_detection": "advanced",
                "subscription_support": True
            },
            "paypal": {
                "pci_compliance": "pci_dss_saq_a",
                "tokenization": True,
                "webhook_security": "signature_verification",
                "fraud_detection": "advanced",
                "marketplace_support": True
            },
            "square": {
                "pci_compliance": "pci_dss_saq_a",
                "tokenization": True,
                "webhook_security": "signature_verification",
                "fraud_detection": "basic",
                "mobile_sdk": ["ios", "android"]
            },
            "razorpay": {
                "pci_compliance": "pci_dss_saq_a",
                "tokenization": True,
                "supported_currencies": ["INR", "USD", "EUR"],
                "fraud_detection": "basic"
            },
            "braintree": {
                "pci_compliance": "pci_dss_saq_a",
                "tokenization": True,
                "fraud_detection": "advanced",
                "subscription_support": True,
                "marketplace_support": True
            },
            "adyen": {
                "pci_compliance": "pci_dss_saq_d",
                "tokenization": True,
                "fraud_detection": "machine_learning",
                "multi_currency": True,
                "supported_currencies": ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]
            }
        }

        config = provider_configs.get(self.payment_provider, {})
        for key, value in config.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Only override if current value is default/empty
                if (isinstance(current_value, list) and len(current_value) <= 2) or \
                   (isinstance(current_value, bool) and not current_value) or \
                   (isinstance(current_value, str) and current_value in ["basic", "stripe", "USD"]):
                    setattr(self, key, value)

    def _set_business_model_optimizations(self):
        """Set business model specific optimizations."""
        business_configs = {
            "ecommerce": {
                "payment_types": ["card", "digital_wallet", "bank_transfer"],
                "capture_method": "automatic",
                "refund_support": True,
                "fraud_detection": "advanced"
            },
            "saas": {
                "subscription_support": True,
                "recurring_billing": True,
                "trial_periods": True,
                "dunning_management": True,
                "churn_analytics": True
            },
            "marketplace": {
                "marketplace_support": True,
                "split_payments": True,
                "platform_fees": True,
                "vendor_onboarding": True,
                "escrow_support": True
            },
            "donation": {
                "payment_types": ["card", "bank_transfer", "digital_wallet"],
                "recurring_billing": True,
                "analytics_enabled": True,
                "fraud_detection": "basic"
            },
            "subscription": {
                "subscription_support": True,
                "recurring_billing": True,
                "trial_periods": True,
                "proration_handling": True,
                "dunning_management": True
            },
            "p2p": {
                "payment_types": ["digital_wallet", "bank_transfer"],
                "fraud_detection": "advanced",
                "kyc_requirements": True,
                "velocity_checks": True
            },
            "gaming": {
                "payment_types": ["card", "digital_wallet", "crypto"],
                "fraud_detection": "machine_learning",
                "velocity_checks": True,
                "chargeback_protection": True
            }
        }

        config = business_configs.get(self.business_model, {})
        for key, value in config.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Apply business model optimizations
                if isinstance(value, bool) and value:
                    setattr(self, key, value)
                elif isinstance(value, list) and len(value) > len(current_value or []):
                    setattr(self, key, value)

    def _configure_compliance_requirements(self):
        """Configure compliance based on business model and regions."""
        # European compliance
        if any("EUR" in curr for curr in self.supported_currencies):
            self.gdpr_compliance = True
            self.psd2_compliance = True
            self.strong_customer_authentication = True

        # Financial services compliance
        if self.business_model in ["p2p", "marketplace"]:
            self.kyc_requirements = True
            self.aml_checks = True

        # High-risk business compliance
        if self.business_model in ["gaming", "crypto"]:
            self.fraud_detection = "machine_learning"
            self.velocity_checks = True
            self.risk_scoring = True

    def get_provider_config(self) -> Dict[str, Any]:
        """Get provider-specific configuration."""
        return {
            "payment_provider": self.payment_provider,
            "payment_types": self.payment_types,
            "supported_currencies": self.supported_currencies,
            "multi_currency": self.multi_currency,
            "tokenization": self.tokenization,
            "fraud_detection": self.fraud_detection,
            **self.advanced_config
        }

    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration for payments."""
        return {
            "pci_compliance": self.pci_compliance,
            "encryption_at_rest": self.encryption_at_rest,
            "encryption_in_transit": self.encryption_in_transit,
            "secure_card_storage": self.secure_card_storage,
            "tokenization": self.tokenization,
            "fraud_detection": self.fraud_detection,
            "webhook_security": self.webhook_security
        }

    def get_business_config(self) -> Dict[str, Any]:
        """Get business model specific configuration."""
        return {
            "business_model": self.business_model,
            "subscription_support": self.subscription_support,
            "marketplace_support": self.marketplace_support,
            "refund_support": self.refund_support,
            "analytics_enabled": self.analytics_enabled,
            "compliance_requirements": {
                "gdpr": self.gdpr_compliance,
                "psd2": self.psd2_compliance,
                "kyc": self.kyc_requirements,
                "aml": self.aml_checks
            }
        }

    def get_supported_payment_methods(self) -> List[Dict[str, Any]]:
        """Get supported payment methods with provider capabilities."""
        methods = []

        for payment_type in self.payment_types:
            method_config = {
                "type": payment_type,
                "provider": self.payment_provider,
                "currencies": self.supported_currencies,
                "tokenization": self.tokenization
            }

            if payment_type == "card":
                method_config.update({
                    "brands": ["visa", "mastercard", "amex", "discover"],
                    "3ds_support": self.strong_customer_authentication,
                    "saved_cards": self.secure_card_storage
                })
            elif payment_type == "digital_wallet":
                method_config.update({
                    "wallets": ["apple_pay", "google_pay", "paypal"],
                    "mobile_optimized": True
                })
            elif payment_type == "bank_transfer":
                method_config.update({
                    "ach": True,
                    "sepa": "EUR" in self.supported_currencies,
                    "instant": False
                })

            methods.append(method_config)

        return methods

    def validate_configuration(self) -> List[str]:
        """Validate payment configuration and return warnings/errors."""
        issues = []

        # Provider validation
        supported_providers = ["stripe", "paypal", "square", "razorpay", "braintree", "adyen"]
        if self.payment_provider not in supported_providers:
            issues.append(f"Unsupported payment provider: {self.payment_provider}")

        # Currency validation
        if self.multi_currency and len(self.supported_currencies) < 2:
            issues.append("Multi-currency enabled but only one currency configured")

        # Compliance validation
        if self.business_model in ["p2p", "marketplace"] and not self.kyc_requirements:
            issues.append("KYC requirements recommended for P2P/marketplace payments")

        if "EUR" in self.supported_currencies and not self.psd2_compliance:
            issues.append("PSD2 compliance required for EUR payments")

        # Security validation
        if self.fraud_detection == "basic" and self.business_model in ["gaming", "crypto"]:
            issues.append("Advanced fraud detection recommended for high-risk business models")

        return issues