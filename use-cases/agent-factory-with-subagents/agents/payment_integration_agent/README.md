# 💳 Universal Payment Integration Agent

> Comprehensive AI agent for payment system integration supporting multiple providers and business models with adaptive prompts and universal configuration.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ai-agent-factory/payment-integration-agent)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://python.org)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-0.0.13+-orange.svg)](https://github.com/pydantic/pydantic-ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

### Universal Provider Support
- **8+ Payment Providers**: Stripe, PayPal, Square, Razorpay, Braintree, Adyen, Mollie, Checkout.com
- **Adaptive Configuration**: Auto-optimization based on provider capabilities
- **Zero Hardcoded Dependencies**: Fully configurable for any payment provider

### Business Model Optimization
- **7+ Business Models**: E-commerce, SaaS, Marketplace, Donation, Subscription, P2P, Gaming
- **Industry-Specific Features**: Tailored configurations for different use cases
- **Compliance Ready**: PCI DSS, GDPR, PSD2, KYC/AML support

### Advanced Capabilities
- **🤖 AI-Powered Integration**: Intelligent payment flow recommendations
- **🔒 Security First**: Advanced fraud detection and compliance handling
- **📊 Analytics Ready**: Revenue tracking and conversion optimization
- **🌍 Global Support**: Multi-currency and localization features
- **⚡ High Performance**: Async processing and webhook handling

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ai-agent-factory/payment-integration-agent
cd payment-integration-agent

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### Basic Configuration

```python
from payment_integration_agent import PaymentAgentDependencies, get_payment_integration_agent

# Create configuration
deps = PaymentAgentDependencies(
    api_key="your_stripe_secret_key",
    payment_provider="stripe",
    business_model="ecommerce",
    project_path="/path/to/your/project"
)

# Initialize agent
agent = get_payment_integration_agent(deps)

# Ask for help
response = await agent.run("How do I integrate Stripe for e-commerce payments?")
print(response.data)
```

### Environment Setup

```bash
# Required LLM Configuration
LLM_API_KEY=your_llm_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Payment Provider Keys
STRIPE_SECRET_KEY=sk_test_your_stripe_key
PAYPAL_CLIENT_ID=your_paypal_client_id
SQUARE_ACCESS_TOKEN=your_square_token

# Optional: Archon Knowledge Base
ARCHON_URL=http://localhost:3737
KNOWLEDGE_BASE_ENABLED=true
```

## 📖 Usage Examples

### E-commerce Integration

```python
from payment_integration_agent.examples import create_ecommerce_stripe_config

# Create e-commerce optimized configuration
config = create_ecommerce_stripe_config(
    api_key="sk_test_your_stripe_key",
    project_path="/path/to/ecommerce/project",
    project_name="My Online Store"
)

agent = get_payment_integration_agent(config)

# Get integration guidance
response = await agent.run("""
I need to integrate Stripe for my e-commerce store.
I want to support cards, Apple Pay, and bank transfers.
How should I implement the checkout flow?
""")
```

### SaaS Subscription Setup

```python
from payment_integration_agent.examples import create_saas_stripe_config

# Create SaaS optimized configuration
config = create_saas_stripe_config(
    api_key="sk_test_your_stripe_key",
    project_path="/path/to/saas/project",
    project_name="My SaaS Platform"
)

agent = get_payment_integration_agent(config)

# Get subscription guidance
response = await agent.run("""
I'm building a SaaS platform with multiple pricing tiers.
I need to handle trial periods, plan changes, and failed payments.
What's the best approach for subscription management?
""")
```

### Marketplace Platform

```python
from payment_integration_agent.examples import create_marketplace_stripe_config

# Create marketplace optimized configuration
config = create_marketplace_stripe_config(
    api_key="sk_test_your_stripe_key",
    project_path="/path/to/marketplace/project",
    project_name="Multi-Vendor Marketplace"
)

agent = get_payment_integration_agent(config)

# Get marketplace guidance
response = await agent.run("""
I'm building a marketplace where vendors sell products.
I need to split payments between vendors and collect platform fees.
How do I implement multi-party payments with Stripe Connect?
""")
```

### Direct Payment Processing

```python
# Process a payment directly
payment_result = await process_payment_request(
    amount=99.99,
    currency="USD",
    deps=config,
    customer_id="cus_123",
    description="Premium subscription"
)

print(f"Payment status: {payment_result['status']}")
print(f"Payment ID: {payment_result['payment_id']}")
```

### Webhook Validation

```python
# Validate incoming webhooks
webhook_result = await validate_webhook_event(
    payload=request.body,
    signature=request.headers.get("stripe-signature"),
    deps=config,
    webhook_secret="whsec_your_webhook_secret"
)

if webhook_result["verified"]:
    print("Webhook verified successfully")
    event_data = webhook_result["event"]
else:
    print("Webhook verification failed")
```

## 🏗️ Architecture

### Core Components

```
payment_integration_agent/
├── agent.py                 # Main agent implementation
├── dependencies.py          # Universal configuration system
├── prompts.py              # Adaptive prompts for different providers
├── tools.py                # Payment processing tools
├── settings.py             # Environment and model configuration
├── examples/               # Provider and business model examples
│   ├── ecommerce_config.py
│   ├── saas_config.py
│   └── marketplace_config.py
├── knowledge/              # Knowledge base for Archon integration
│   └── payment_integration_knowledge.md
└── __init__.py            # Package exports
```

### Universal Design Principles

#### ✅ Zero Hardcoded Dependencies
```python
# ❌ Bad: Hardcoded provider
def create_payment():
    return stripe.Payment.create(...)

# ✅ Good: Universal interface
def create_payment(provider, config):
    return provider_handlers[provider](config)
```

#### ✅ Adaptive Configuration
```python
# Configuration adapts based on provider and business model
deps = PaymentAgentDependencies(
    payment_provider="stripe",
    business_model="saas",
    # Auto-enables: subscription_support, dunning_management, churn_analytics
)
```

#### ✅ Multiple Domain Support
```python
# Same agent, different configurations
ecommerce_agent = create_ecommerce_payment_agent(api_key="...")
saas_agent = create_saas_payment_agent(api_key="...")
marketplace_agent = create_marketplace_payment_agent(api_key="...")
```

## 🔧 Configuration Options

### Payment Providers

| Provider | Business Models | Key Features |
|----------|----------------|--------------|
| **Stripe** | All | Payment Intents, Connect, Billing |
| **PayPal** | E-commerce, Marketplace | Express Checkout, Commerce Platform |
| **Square** | E-commerce, POS | Web Payments, In-Person, Omnichannel |
| **Razorpay** | E-commerce, SaaS | UPI, Net Banking, Payment Links |
| **Braintree** | All | Drop-in UI, Vault, PayPal Integration |
| **Adyen** | Enterprise | Global Methods, Platforms, Risk Management |

### Business Models

| Model | Key Features | Recommended Providers |
|-------|-------------|----------------------|
| **E-commerce** | Product sales, inventory sync, abandoned cart | Stripe, PayPal, Square |
| **SaaS** | Subscriptions, trials, usage billing, dunning | Stripe, Braintree |
| **Marketplace** | Split payments, vendor onboarding, escrow | Stripe, PayPal, Braintree |
| **Donation** | Recurring donations, tax receipts, campaigns | Stripe, PayPal |
| **Gaming** | Virtual currency, anti-fraud, chargebacks | Adyen, Braintree |
| **P2P** | KYC/AML, real-time transfers, limits | Stripe, Adyen |

### Security Levels

| Level | Description | Use Cases |
|-------|-------------|-----------|
| **PCI DSS SAQ-A** | Hosted payment pages | Most businesses |
| **PCI DSS SAQ-D** | Direct card handling | Enterprise, custom flows |
| **Advanced Fraud** | ML-based detection | High-risk industries |
| **Basic Fraud** | Rule-based screening | Low-risk businesses |

## 🛠️ Tools and Capabilities

### Available Tools

1. **`search_payment_knowledge`**: Search payment integration knowledge base
2. **`create_payment`**: Universal payment creation across providers
3. **`verify_webhook_signature`**: Secure webhook validation
4. **`process_refund`**: Handle payment refunds and disputes
5. **`validate_payment_configuration`**: Configuration analysis and recommendations

### Example Tool Usage

```python
# Search for integration patterns
knowledge = await search_payment_knowledge(
    ctx=context,
    query="Stripe subscription webhooks implementation"
)

# Create a payment
payment = await create_payment(
    ctx=context,
    amount=100.00,
    currency="USD",
    customer_id="cus_123"
)

# Validate configuration
analysis = await validate_payment_configuration(ctx=context)
print(f"Security score: {analysis['security_score']}")
print(f"Recommendations: {analysis['recommendations']}")
```

## 🎯 Use Cases

### 1. E-commerce Platform
```python
# Multi-provider e-commerce setup
config = create_ecommerce_multi_provider_config(
    api_key="primary_provider_key",
    project_name="Global E-commerce Platform"
)

# Features: Multi-currency, fraud detection, abandoned cart recovery
```

### 2. SaaS Subscription Service
```python
# Usage-based billing for API service
config = create_saas_usage_based_config(
    api_key="stripe_key",
    project_name="API Service Platform"
)

# Features: Metered billing, real-time reporting, dunning management
```

### 3. Marketplace Platform
```python
# Service marketplace with escrow
config = create_service_marketplace_config(
    api_key="stripe_key",
    project_name="Freelance Service Platform"
)

# Features: Split payments, escrow, vendor onboarding, dispute resolution
```

### 4. Enterprise B2B
```python
# High-value B2B transactions
config = create_enterprise_marketplace_config(
    api_key="stripe_live_key",
    project_name="B2B Enterprise Platform"
)

# Features: Enhanced security, compliance, manual approvals, audit logging
```

## 🧠 Knowledge Base Integration

### Archon Integration

The agent integrates with Archon Knowledge Base for enhanced expertise:

```python
# Enable knowledge base integration
deps = PaymentAgentDependencies(
    knowledge_base_enabled=True,
    archon_url="http://localhost:3737",
    knowledge_tags=["payment-integration", "stripe", "ecommerce"]
)
```

### Knowledge Base Setup

1. **Upload Knowledge File**:
   ```bash
   # Upload to Archon Knowledge Base
   curl -X POST http://localhost:3737/api/knowledge/upload \
     -F "file=@knowledge/payment_integration_knowledge.md" \
     -F "tags=payment-integration,agent-knowledge,pydantic-ai"
   ```

2. **Link to Project**:
   - Go to Archon UI: http://localhost:3737
   - Navigate to AI Agent Factory project
   - Link the payment integration knowledge source

### Available Knowledge

- **Provider Integration Patterns**: Best practices for each payment provider
- **Security Implementation**: PCI DSS, fraud detection, compliance patterns
- **Business Model Optimization**: Industry-specific configuration guides
- **Webhook Processing**: Event-driven architecture patterns
- **Testing Strategies**: Comprehensive testing approaches

## 🧪 Testing

### Test Configuration

```python
# Create test dependencies
test_deps = PaymentAgentDependencies(
    api_key="sk_test_stripe_key",
    payment_provider="stripe",
    business_model="ecommerce",
    sandbox_mode=True,
    test_cards=True
)

# Test payment creation
result = await process_payment_request(
    amount=10.00,
    currency="USD",
    deps=test_deps,
    customer_id="test_customer"
)
```

### Test Cards

```python
# Stripe test cards
TEST_CARDS = {
    "visa_success": "4242424242424242",
    "visa_declined": "4000000000000002",
    "mastercard_success": "5555555555554444",
    "amex_success": "378282246310005"
}
```

### Webhook Testing

```python
# Test webhook validation
test_payload = '{"id": "evt_test_webhook", "type": "payment_intent.succeeded"}'
test_signature = "t=1234567890,v1=test_signature"

result = await validate_webhook_event(
    payload=test_payload,
    signature=test_signature,
    deps=test_deps,
    webhook_secret="whsec_test_secret"
)
```

## 🔒 Security Best Practices

### PCI DSS Compliance

```python
# Automatic PCI compliance configuration
deps = PaymentAgentDependencies(
    pci_compliance="pci_dss_saq_a",  # Hosted payment pages
    encryption_at_rest=True,
    encryption_in_transit=True,
    tokenization=True
)
```

### Fraud Detection

```python
# Advanced fraud detection
deps = PaymentAgentDependencies(
    fraud_detection="machine_learning",
    risk_scoring=True,
    velocity_checks=True,
    geolocation_checks=True,
    blacklist_checks=True
)
```

### Webhook Security

```python
# Secure webhook processing
deps = PaymentAgentDependencies(
    webhook_security="both",  # Signature + IP whitelist
    webhook_enabled=True,
    retry_logic=True,
    dead_letter_queue=True
)
```

## 📊 Analytics and Monitoring

### Revenue Analytics

```python
# Enable comprehensive analytics
deps = PaymentAgentDependencies(
    analytics_enabled=True,
    real_time_reporting=True,
    revenue_analytics=True,
    fraud_analytics=True,
    churn_analytics=True  # For SaaS
)
```

### Performance Monitoring

```python
# Performance optimization
deps = PaymentAgentDependencies(
    api_timeout=30,
    retry_attempts=3,
    rate_limiting=True,
    caching_enabled=True,
    load_balancing=True  # For enterprise
)
```

## 🌍 Internationalization

### Multi-Currency Support

```python
# Global currency support
deps = PaymentAgentDependencies(
    default_currency="USD",
    supported_currencies=[
        "USD", "EUR", "GBP", "JPY", "CAD", "AUD",
        "CHF", "SEK", "NOK", "DKK", "PLN", "CZK"
    ],
    multi_currency=True,
    currency_conversion=True
)
```

### Regional Compliance

```python
# European operations
deps = PaymentAgentDependencies(
    gdpr_compliance=True,
    psd2_compliance=True,
    strong_customer_authentication=True
)

# Financial services
deps = PaymentAgentDependencies(
    kyc_requirements=True,
    aml_checks=True
)
```

## 🔄 Migration and Upgrades

### Provider Migration

```python
# Easy provider switching
old_config = PaymentAgentDependencies(payment_provider="paypal")
new_config = PaymentAgentDependencies(payment_provider="stripe")

# Agent automatically adapts to new provider capabilities
```

### Business Model Evolution

```python
# Evolve from e-commerce to marketplace
ecommerce_config = PaymentAgentDependencies(business_model="ecommerce")
marketplace_config = PaymentAgentDependencies(business_model="marketplace")

# Configuration automatically includes marketplace features
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/ai-agent-factory/payment-integration-agent
cd payment-integration-agent

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
black . && flake8 . && mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Full Documentation](https://docs.ai-agent-factory.com/payment-integration)
- **Issues**: [GitHub Issues](https://github.com/ai-agent-factory/payment-integration-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ai-agent-factory/payment-integration-agent/discussions)
- **Discord**: [AI Agent Factory Community](https://discord.gg/ai-agent-factory)

## 🙏 Acknowledgments

- **Pydantic AI**: Modern AI agent framework
- **Payment Providers**: Stripe, PayPal, Square, Razorpay, Braintree, Adyen
- **Community**: Contributors and users who make this project better

---

<div align="center">
<p><strong>Built with ❤️ by the AI Agent Factory Team</strong></p>
<p>
  <a href="https://github.com/ai-agent-factory">GitHub</a> •
  <a href="https://docs.ai-agent-factory.com">Documentation</a> •
  <a href="https://discord.gg/ai-agent-factory">Discord</a>
</p>
</div>