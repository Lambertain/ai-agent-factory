"""
Marketplace Payment Integration Configuration Example.

Optimized configuration for multi-vendor platforms and marketplace businesses.
"""

from ..dependencies import PaymentAgentDependencies

def create_marketplace_stripe_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Marketplace Platform"
) -> PaymentAgentDependencies:
    """
    Create Stripe configuration optimized for marketplace businesses.

    Best for: Multi-vendor platforms, service marketplaces, platform businesses
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="marketplace",

        # Marketplace payment methods
        payment_types=["card", "digital_wallet", "bank_transfer"],

        # Global marketplace currencies
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF",
            "SEK", "NOK", "DKK", "PLN", "CZK", "SGD", "HKD"
        ],
        multi_currency=True,
        currency_conversion=True,

        # Marketplace payment flow
        payment_flow="embedded",
        capture_method="manual",  # For marketplace approval workflows
        confirmation_method="automatic",

        # Security for marketplace
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,
        risk_scoring=True,
        velocity_checks=True,

        # Marketplace-specific features
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        escrow_support=True,
        vendor_onboarding=True,

        # Refund handling for marketplace disputes
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        automated_responses=True,

        # Webhook configuration for marketplace events
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="queued",  # Handle high volume
        retry_logic=True,
        dead_letter_queue=True,

        # Marketplace analytics
        analytics_enabled=True,
        real_time_reporting=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # Performance for marketplace scale
        api_timeout=45,
        retry_attempts=3,
        rate_limiting=True,
        caching_enabled=True,
        load_balancing=True,

        # Compliance for marketplace operations
        gdpr_compliance=True,
        psd2_compliance=True,
        kyc_requirements=True,  # For vendor onboarding
        aml_checks=True,

        # Developer experience
        sandbox_mode=True,
        webhook_testing=True,
        api_documentation="openapi",

        # Knowledge base
        knowledge_tags=["marketplace", "stripe", "connect", "split-payments"],
        knowledge_domain="docs.stripe.com"
    )


def create_marketplace_paypal_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Marketplace Platform"
) -> PaymentAgentDependencies:
    """
    Create PayPal configuration optimized for marketplace businesses.

    Best for: Consumer marketplaces, international platforms, PayPal-heavy regions
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="paypal",
        business_model="marketplace",

        # PayPal marketplace payment methods
        payment_types=["digital_wallet", "card", "bank_transfer"],

        # PayPal global currency support
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF",
            "SEK", "NOK", "DKK", "PLN", "CZK", "HKD", "SGD",
            "BRL", "MXN", "TWD", "NZD"
        ],
        multi_currency=True,
        currency_conversion=True,

        # PayPal Commerce Platform flow
        payment_flow="checkout",
        capture_method="manual",
        confirmation_method="automatic",

        # Security
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,

        # PayPal marketplace features
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        vendor_onboarding=True,
        escrow_support=False,  # PayPal handles this differently

        # Refunds
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,

        # Webhooks
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="immediate",

        # Analytics
        analytics_enabled=True,
        revenue_analytics=True,

        # Performance
        api_timeout=60,  # PayPal can be slower
        retry_attempts=3,
        caching_enabled=True,

        # Compliance
        gdpr_compliance=True,
        kyc_requirements=True,
        aml_checks=True,

        # Knowledge base
        knowledge_tags=["marketplace", "paypal", "commerce-platform", "split-payments"],
        knowledge_domain="developer.paypal.com"
    )


def create_service_marketplace_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Service Marketplace"
) -> PaymentAgentDependencies:
    """
    Create configuration for service-based marketplaces.

    Best for: Freelance platforms, service booking, gig economy
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="marketplace",

        # Service marketplace payment methods
        payment_types=["card", "digital_wallet", "bank_transfer"],

        # Currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "CAD", "AUD"],
        multi_currency=True,

        # Service marketplace flow
        payment_flow="embedded",
        capture_method="manual",  # Hold payment until service completion
        confirmation_method="automatic",

        # Security for service transactions
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,
        risk_scoring=True,

        # Service marketplace features
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        escrow_support=True,  # Critical for service completion
        vendor_onboarding=True,

        # Refund handling for service disputes
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        automated_responses=False,  # Manual review for services

        # Webhooks for service workflow
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="immediate",
        retry_logic=True,

        # Service analytics
        analytics_enabled=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # Performance
        api_timeout=30,
        retry_attempts=3,
        caching_enabled=True,

        # Compliance for service providers
        gdpr_compliance=True,
        kyc_requirements=True,
        aml_checks=True,

        # Knowledge base
        knowledge_tags=["service-marketplace", "escrow", "freelance", "gig-economy"],
        knowledge_domain="docs.stripe.com"
    )


def create_product_marketplace_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Product Marketplace"
) -> PaymentAgentDependencies:
    """
    Create configuration for product-based marketplaces.

    Best for: Multi-vendor retail, product platforms, Amazon-like marketplaces
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="marketplace",

        # Product marketplace payment methods
        payment_types=["card", "digital_wallet", "bank_transfer", "buy_now_pay_later"],

        # Global product marketplace currencies
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "CAD", "AUD", "JPY",
            "CHF", "SEK", "NOK", "DKK", "PLN", "CZK"
        ],
        multi_currency=True,
        currency_conversion=True,

        # Product marketplace flow
        payment_flow="embedded",
        capture_method="automatic",  # Immediate for physical products
        confirmation_method="automatic",

        # Security for product sales
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,
        risk_scoring=True,
        velocity_checks=True,
        chargeback_protection=True,

        # Product marketplace features
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        vendor_onboarding=True,
        escrow_support=False,  # Not typical for products

        # Refund handling for products
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        chargeback_protection=True,

        # Webhook configuration
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="queued",
        retry_logic=True,

        # Product marketplace analytics
        analytics_enabled=True,
        real_time_reporting=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # Performance for high volume
        api_timeout=30,
        retry_attempts=3,
        rate_limiting=True,
        caching_enabled=True,
        load_balancing=True,

        # Compliance
        gdpr_compliance=True,
        psd2_compliance=True,
        kyc_requirements=True,

        # Knowledge base
        knowledge_tags=["product-marketplace", "multi-vendor", "retail-platform"],
        knowledge_domain="docs.stripe.com"
    )


def create_enterprise_marketplace_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Enterprise Marketplace"
) -> PaymentAgentDependencies:
    """
    Create configuration for enterprise marketplace platforms.

    Best for: B2B marketplaces, enterprise procurement, high-value transactions
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="marketplace",

        # Enterprise payment methods
        payment_types=["card", "bank_transfer"],  # Focus on enterprise methods

        # Enterprise global currencies
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF",
            "SEK", "NOK", "DKK", "SGD", "HKD", "CNY"
        ],
        multi_currency=True,
        currency_conversion=True,

        # Enterprise marketplace flow
        payment_flow="api_only",  # Often integrated into enterprise systems
        capture_method="manual",  # Approval workflows
        confirmation_method="manual",

        # Enhanced security for enterprise
        pci_compliance="pci_dss_saq_d",
        fraud_detection="machine_learning",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,
        secure_card_storage=True,
        risk_scoring=True,
        velocity_checks=True,
        geolocation_checks=True,
        blacklist_checks=True,

        # Enterprise marketplace features
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        escrow_support=True,  # For high-value B2B transactions
        vendor_onboarding=True,

        # Enterprise refund handling
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,
        automated_responses=False,  # Manual review for enterprise

        # Enterprise webhook processing
        webhook_enabled=True,
        webhook_security="both",  # Signature + IP whitelist
        event_processing="queued",
        retry_logic=True,
        dead_letter_queue=True,

        # Enterprise analytics
        analytics_enabled=True,
        real_time_reporting=True,
        revenue_analytics=True,
        fraud_analytics=True,

        # Enterprise performance requirements
        api_timeout=120,  # Longer for complex B2B transactions
        retry_attempts=5,
        rate_limiting=True,
        caching_enabled=True,
        load_balancing=True,

        # Enhanced compliance for enterprise
        gdpr_compliance=True,
        psd2_compliance=True,
        strong_customer_authentication=True,
        kyc_requirements=True,
        aml_checks=True,

        # Enterprise features
        api_documentation="openapi",
        sdk_generation=True,

        # Knowledge base
        knowledge_tags=[
            "enterprise-marketplace", "b2b", "high-value-transactions",
            "procurement", "enterprise-payments"
        ],
        knowledge_domain="docs.stripe.com"
    )


# Usage examples
if __name__ == "__main__":
    # Example 1: Standard marketplace with Stripe
    marketplace_stripe = create_marketplace_stripe_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/marketplace/project",
        project_name="Multi-Vendor Marketplace"
    )

    # Example 2: Marketplace with PayPal support
    marketplace_paypal = create_marketplace_paypal_config(
        api_key="your_paypal_client_id",
        project_path="/path/to/marketplace/project",
        project_name="PayPal Marketplace"
    )

    # Example 3: Service marketplace
    service_marketplace = create_service_marketplace_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/service/platform",
        project_name="Freelance Service Platform"
    )

    # Example 4: Product marketplace
    product_marketplace = create_product_marketplace_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/product/marketplace",
        project_name="Multi-Vendor Product Platform"
    )

    # Example 5: Enterprise marketplace
    enterprise_marketplace = create_enterprise_marketplace_config(
        api_key="sk_live_your_stripe_key",
        project_path="/path/to/enterprise/marketplace",
        project_name="B2B Enterprise Marketplace"
    )

    print("Marketplace payment configurations created successfully!")
    print(f"Stripe marketplace: {marketplace_stripe.marketplace_support} - {marketplace_stripe.split_payments}")
    print(f"PayPal marketplace: {marketplace_paypal.payment_provider} - {marketplace_paypal.platform_fees}")
    print(f"Service marketplace: {service_marketplace.escrow_support} - {service_marketplace.capture_method}")
    print(f"Product marketplace: {product_marketplace.chargeback_protection} - {product_marketplace.load_balancing}")
    print(f"Enterprise marketplace: {enterprise_marketplace.pci_compliance} - {enterprise_marketplace.aml_checks}")