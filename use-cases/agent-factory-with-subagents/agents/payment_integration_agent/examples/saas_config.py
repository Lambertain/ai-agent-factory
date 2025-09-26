"""
SaaS Payment Integration Configuration Example.

Optimized configuration for Software as a Service platforms with subscription management.
"""

from ..dependencies import PaymentAgentDependencies

def create_saas_stripe_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "SaaS Platform"
) -> PaymentAgentDependencies:
    """
    Create Stripe configuration optimized for SaaS businesses.

    Best for: Subscription software, SaaS platforms, usage-based billing
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="saas",

        # SaaS payment methods (focus on recurring)
        payment_types=["card", "bank_transfer", "digital_wallet"],

        # Global SaaS currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "CAD", "AUD", "JPY"],
        multi_currency=True,
        currency_conversion=True,

        # Subscription-focused payment flow
        payment_flow="embedded",
        capture_method="automatic",
        confirmation_method="automatic",

        # Security for SaaS
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,
        secure_card_storage=True,  # For subscription renewals

        # SaaS-specific subscription features
        subscription_support=True,
        recurring_billing=True,
        trial_periods=True,
        proration_handling=True,
        dunning_management=True,

        # Refund support for SaaS
        refund_support=True,
        partial_refunds=True,  # For mid-cycle cancellations

        # Webhook configuration for subscription events
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="immediate",
        retry_logic=True,
        dead_letter_queue=True,

        # SaaS analytics
        analytics_enabled=True,
        revenue_analytics=True,
        churn_analytics=True,
        fraud_analytics=True,

        # Performance for subscription processing
        api_timeout=30,
        retry_attempts=3,
        rate_limiting=True,
        caching_enabled=True,

        # Compliance for global SaaS
        gdpr_compliance=True,
        psd2_compliance=True,

        # Developer experience
        sandbox_mode=True,
        test_cards=True,
        webhook_testing=True,

        # Knowledge base
        knowledge_tags=["saas", "stripe", "subscriptions", "recurring-billing"],
        knowledge_domain="docs.stripe.com"
    )


def create_saas_braintree_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "SaaS Platform"
) -> PaymentAgentDependencies:
    """
    Create Braintree configuration optimized for SaaS businesses.

    Best for: SaaS with PayPal integration, international subscriptions
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="braintree",
        business_model="saas",

        # Braintree payment methods
        payment_types=["card", "digital_wallet", "bank_transfer"],

        # Currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "AUD", "CAD"],
        multi_currency=True,

        # Braintree flow
        payment_flow="embedded",
        capture_method="automatic",

        # Security
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,
        secure_card_storage=True,

        # Subscription features
        subscription_support=True,
        recurring_billing=True,
        trial_periods=True,
        proration_handling=True,
        dunning_management=True,

        # Refunds
        refund_support=True,
        partial_refunds=True,

        # Webhooks
        webhook_enabled=True,
        webhook_security="signature_verification",

        # Analytics
        analytics_enabled=True,
        revenue_analytics=True,
        churn_analytics=True,

        # Performance
        api_timeout=30,
        retry_attempts=3,
        caching_enabled=True,

        # Compliance
        gdpr_compliance=True,

        # Knowledge base
        knowledge_tags=["saas", "braintree", "subscriptions", "paypal"],
        knowledge_domain="developers.braintreepayments.com"
    )


def create_saas_usage_based_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Usage-Based SaaS"
) -> PaymentAgentDependencies:
    """
    Create configuration for usage-based SaaS billing.

    Best for: API services, metered usage, pay-as-you-go models
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="saas",

        # Payment methods
        payment_types=["card", "bank_transfer"],

        # Currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP"],
        multi_currency=True,

        # Payment flow
        payment_flow="api_only",  # Automated billing
        capture_method="automatic",
        confirmation_method="automatic",

        # Security
        pci_compliance="pci_dss_saq_a",
        fraud_detection="advanced",
        tokenization=True,
        secure_card_storage=True,

        # Usage-based billing features
        subscription_support=True,
        recurring_billing=True,
        trial_periods=False,  # Not typical for usage-based
        proration_handling=True,  # Important for usage billing
        dunning_management=True,

        # Refunds (rare for usage-based)
        refund_support=True,
        partial_refunds=True,

        # Webhook configuration (critical for usage billing)
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="queued",  # Handle high volume
        retry_logic=True,
        dead_letter_queue=True,

        # Analytics for usage tracking
        analytics_enabled=True,
        real_time_reporting=True,  # Important for usage billing
        revenue_analytics=True,
        churn_analytics=True,

        # Performance for high-frequency billing
        api_timeout=30,
        retry_attempts=5,
        rate_limiting=True,
        caching_enabled=True,

        # Compliance
        gdpr_compliance=True,

        # Knowledge base
        knowledge_tags=["saas", "usage-based", "metered-billing", "api-services"],
        knowledge_domain="docs.stripe.com"
    )


def create_saas_freemium_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Freemium SaaS"
) -> PaymentAgentDependencies:
    """
    Create configuration for freemium SaaS model.

    Best for: Freemium services, trial conversions, tiered pricing
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="saas",

        # Payment methods for conversion
        payment_types=["card", "digital_wallet", "bank_transfer"],

        # Currency support
        default_currency="USD",
        supported_currencies=["USD", "EUR", "GBP", "CAD", "AUD"],
        multi_currency=True,

        # Conversion-optimized flow
        payment_flow="embedded",
        capture_method="automatic",
        confirmation_method="automatic",

        # Security
        pci_compliance="pci_dss_saq_a",
        fraud_detection="basic",  # Lower friction for conversions
        tokenization=True,

        # Freemium features
        subscription_support=True,
        recurring_billing=True,
        trial_periods=True,  # Critical for freemium
        proration_handling=True,
        dunning_management=True,

        # Refunds for early cancellations
        refund_support=True,
        partial_refunds=True,

        # Webhooks for conversion tracking
        webhook_enabled=True,
        webhook_security="signature_verification",
        event_processing="immediate",

        # Conversion analytics
        analytics_enabled=True,
        revenue_analytics=True,
        churn_analytics=True,

        # Performance
        api_timeout=30,
        retry_attempts=3,
        caching_enabled=True,

        # Compliance
        gdpr_compliance=True,

        # Knowledge base
        knowledge_tags=["saas", "freemium", "trial-conversion", "tiered-pricing"],
        knowledge_domain="docs.stripe.com"
    )


def create_enterprise_saas_config(
    api_key: str,
    project_path: str = "",
    project_name: str = "Enterprise SaaS Platform"
) -> PaymentAgentDependencies:
    """
    Create configuration for enterprise SaaS platforms.

    Best for: B2B SaaS, enterprise software, high-value subscriptions
    """
    return PaymentAgentDependencies(
        # Core settings
        api_key=api_key,
        project_path=project_path,
        project_name=project_name,

        # Payment provider configuration
        payment_provider="stripe",
        business_model="saas",

        # Enterprise payment methods
        payment_types=["card", "bank_transfer"],  # Focus on ACH/wire transfers

        # Global enterprise currencies
        default_currency="USD",
        supported_currencies=[
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF",
            "SEK", "NOK", "DKK", "SGD", "HKD"
        ],
        multi_currency=True,
        currency_conversion=True,

        # Enterprise payment flow
        payment_flow="api_only",  # Often automated
        capture_method="manual",  # For approval workflows
        confirmation_method="manual",

        # Enhanced security for enterprise
        pci_compliance="pci_dss_saq_d",
        fraud_detection="machine_learning",
        encryption_at_rest=True,
        encryption_in_transit=True,
        tokenization=True,
        secure_card_storage=True,
        risk_scoring=True,

        # Enterprise subscription features
        subscription_support=True,
        recurring_billing=True,
        trial_periods=True,
        proration_handling=True,
        dunning_management=True,

        # Enterprise refund handling
        refund_support=True,
        partial_refunds=True,
        dispute_management=True,

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
        churn_analytics=True,
        fraud_analytics=True,

        # Enterprise performance requirements
        api_timeout=60,  # Longer for complex transactions
        retry_attempts=5,
        rate_limiting=True,
        caching_enabled=True,
        load_balancing=True,

        # Enterprise compliance
        gdpr_compliance=True,
        psd2_compliance=True,
        strong_customer_authentication=True,
        kyc_requirements=True,  # For high-value transactions

        # Advanced features
        api_documentation="openapi",
        sdk_generation=True,

        # Knowledge base
        knowledge_tags=[
            "saas", "enterprise", "b2b", "high-value-subscriptions",
            "enterprise-billing", "complex-pricing"
        ],
        knowledge_domain="docs.stripe.com"
    )


# Usage examples
if __name__ == "__main__":
    # Example 1: Standard SaaS with Stripe
    saas_stripe = create_saas_stripe_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/saas/project",
        project_name="My SaaS Platform"
    )

    # Example 2: SaaS with PayPal support via Braintree
    saas_braintree = create_saas_braintree_config(
        api_key="your_braintree_private_key",
        project_path="/path/to/saas/project",
        project_name="SaaS with PayPal"
    )

    # Example 3: Usage-based SaaS
    usage_based = create_saas_usage_based_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/api/service",
        project_name="API Service Platform"
    )

    # Example 4: Freemium SaaS
    freemium = create_saas_freemium_config(
        api_key="sk_test_your_stripe_key",
        project_path="/path/to/freemium/app",
        project_name="Freemium SaaS App"
    )

    # Example 5: Enterprise SaaS
    enterprise = create_enterprise_saas_config(
        api_key="sk_live_your_stripe_key",
        project_path="/path/to/enterprise/platform",
        project_name="Enterprise SaaS Platform"
    )

    print("SaaS payment configurations created successfully!")
    print(f"Standard SaaS: {saas_stripe.business_model} - {saas_stripe.subscription_support}")
    print(f"Braintree SaaS: {saas_braintree.payment_provider} - {saas_braintree.subscription_support}")
    print(f"Usage-based: {usage_based.real_time_reporting} - {usage_based.proration_handling}")
    print(f"Freemium: {freemium.trial_periods} - {freemium.churn_analytics}")
    print(f"Enterprise: {enterprise.pci_compliance} - {enterprise.load_balancing}")