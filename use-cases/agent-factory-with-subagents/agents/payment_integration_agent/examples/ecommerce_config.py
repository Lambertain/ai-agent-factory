"""
E-commerce Payment Integration Configuration Example.

Optimized configuration for online retail, product sales, and shopping platforms.
"""

from ..dependencies import PaymentAgentDependencies

def create_ecommerce_stripe_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "E-commerce Store"
) -> PaymentAgentDependencies:
    """
    Create Stripe configuration optimized for e-commerce.

    Best for: Online stores, product marketplaces, retail websites
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="ecommerce",

        # Payment methods for e-commerce
        payment_types=["card", "digital_wallet", "bank_transfer", "buy_now_pay_later"],

        # Multi-currency for international sales
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "CAD", "AUD"],
        multi_currency=True,
        currency_conversion=True,

        # E-commerce payment flow
        payment_flow="embedded",
        capture_method="automatic",
        confirmation_method="automatic",

        # Security optimizations for online retail
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,

        # E-commerce specific features
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        chargeback_protection=True,

        # Webhook configuration for order processing
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="immediate",
        retry_logic=True,

        # Analytics for conversion optimization
        analytics_enabled=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # Performance settings for high traffic
        api_timeout=30,
        retry_attempts=3,
        rate_limiting=True,
        caching_enabled=True,

        # Compliance for global sales
        gdpr_compliance=True,
        psd2_compliance=True,
        strong_customer_authentication=True,

        # Knowledge base configuration
        knowledge_tags=["ecommerce", "stripe", "payment-integration", "retail"],
        knowledge_domain="docs.stripe.com"
    )


def create_ecommerce_paypal_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "E-commerce Store"
) -> PaymentAgentDependencies:
    """
    Create PayPal configuration optimized for e-commerce.

    Best for: Consumer-focused stores, international sales, express checkout
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="paypal",
        business_model="ecommerce",

        # PayPal payment methods
        payment_types=["digital_wallet", "card", "bank_transfer", "buy_now_pay_later"],

        # Global currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF"],
        multi_currency=True,
        currency_conversion=True,

        # PayPal Express Checkout flow
        payment_flow="checkout",
        capture_method="automatic",
        confirmation_method="automatic",

        # Security configuration
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,

        # E-commerce features
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,

        # PayPal specific optimizations
        marketplace_support=False,  # For single merchant

        # Webhook configuration
        webhook_enabled=True,
        webhook_security="signature_verification",

        # Analytics
        analytics_enabled=True,
        revenue_analytics=True,

        # Performance
        api_timeout=45,  # PayPal can be slower
        retry_attempts=3,
        caching_enabled=True,

        # Knowledge base
        knowledge_tags=["ecommerce", "paypal", "payment-integration", "express-checkout"],
        knowledge_domain="developer.paypal.com"
    )


def create_ecommerce_square_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "E-commerce Store"
) -> PaymentAgentDependencies:
    """
    Create Square configuration optimized for e-commerce.

    Best for: Small-medium businesses, omnichannel retail, inventory integration
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="square",
        business_model="ecommerce",

        # Square payment methods
        payment_types=["card", "digital_wallet", "bank_transfer"],

        # Currency support (Square is more limited)
        default_currency="USD",
        supported_currencies=["USD", "CAD", "GBP", "AUD", "JPY"],
        multi_currency=False,  # Square handles this automatically

        # Square Web Payments SDK
        payment_flow="embedded",
        capture_method="automatic",

        # Security
        pci_compliance="pci_dss_saq_a",
        fraud_detection="basic",
        tokenization=True,

        # E-commerce features
        refund_support=True,
        partial_refunds=True,

        # Square specific features
        mobile_sdk=["ios", "android"],  # For omnichannel

        # Webhook configuration
        webhook_enabled=True,
        webhook_security="signature_verification",

        # Analytics
        analytics_enabled=True,
        revenue_analytics=True,

        # Performance
        api_timeout=30,
        retry_attempts=3,
        caching_enabled=True,

        # Knowledge base
        knowledge_tags=["ecommerce", "square", "payment-integration", "omnichannel"],
        knowledge_domain="developer.squareup.com"
    )


def create_ecommerce_multi_provider_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Multi-Provider E-commerce Store"
) -> PaymentAgentDependencies:
    """
    Create configuration supporting multiple payment providers.

    Best for: Large e-commerce platforms, international expansion, risk mitigation
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Start with Stripe as primary
        payment_provider="stripe",
        business_model="ecommerce",

        # Comprehensive payment method support
        payment_types=["card", "digital_wallet", "bank_transfer", "buy_now_pay_later", "crypto"],

        # Global currency support
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF",
            "SEK", "NOK", "DKK", "PLN", "CZK", "HUF"
        ],
        multi_currency=True,
        currency_conversion=True,

        # Flexible payment flow
        payment_flow="embedded",
        capture_method="automatic",
        confirmation_method="automatic",

        # Maximum security
        pci_compliance="pci_dss_saq_d",
        fraud_detection="machine_learning",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,
        risk_scoring=True,
        velocity_checks=True,
        geolocation_checks=True,
        blacklist_checks=True,

        # Comprehensive e-commerce features
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        chargeback_protection=True,
        automated_responses=True,

        # Advanced webhook processing
        webhook_enabled=True,
        webhook_security="both",  # Signature + IP whitelist
        event_processing="queued",  # For high volume
        retry_logic=True,
        dead_letter_queue=True,

        # Advanced analytics
        analytics_enabled=True,
        real_time_reporting=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # High performance configuration
        api_timeout=30,
        retry_attempts=5,
        rate_limiting=True,
        caching_enabled=True,
        load_balancing=True,

        # Full compliance
        gdpr_compliance=True,
        psd2_compliance=True,
        strong_customer_authentication=True,

        # Developer experience
        sandbox_mode=True,
        test_cards=True,
        webhook_testing=True,
        sdk_generation=True,

        # Knowledge base
        knowledge_tags=[
            "ecommerce", "multi-provider", "payment-integration",
            "enterprise", "global-payments"
        ],
        knowledge_domain="payments.universal.com"
    )


# Usage examples
if __name__ == "__main__":
    # Example 1: Small e-commerce store with Stripe
    stripe_config = create_ecommerce_stripe_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/ecommerce/project",
        project_name="My Online Store"
    )

    # Example 2: International store with PayPal
    paypal_config = create_ecommerce_paypal_config(
        api_key="your_paypal_client_id",
        project_path="/path/to/international/store",
        project_name="Global Marketplace"
    )

    # Example 3: Omnichannel business with Square
    square_config = create_ecommerce_square_config(
        api_key="your_square_access_token",
        project_path="/path/to/omnichannel/business",
        project_name="Retail Plus Online"
    )

    # Example 4: Enterprise multi-provider setup
    enterprise_config = create_ecommerce_multi_provider_config(
        api_key="your_primary_api_key",
        project_path="/path/to/enterprise/platform",
        project_name="Enterprise E-commerce Platform"
    )

    print("E-commerce payment configurations created successfully!")
    print(f"Stripe config: {stripe_config.payment_provider} - {stripe_config.business_model}")
    print(f"PayPal config: {paypal_config.payment_provider} - {paypal_config.business_model}")
    print(f"Square config: {square_config.payment_provider} - {square_config.business_model}")
    print(f"Enterprise config: {enterprise_config.payment_provider} - {enterprise_config.business_model}")