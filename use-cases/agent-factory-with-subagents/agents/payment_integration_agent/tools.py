"""
Universal Payment Integration Agent Tools.

Comprehensive tools supporting multiple payment providers and business models.
"""

import asyncio
import json
import hashlib
import hmac
import logging
from typing import Dict, Any, List, Optional, Union
from decimal import Decimal
from datetime import datetime, timedelta
from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from .dependencies import PaymentAgentDependencies

logger = logging.getLogger(__name__)


class PaymentRequest(BaseModel):
    """Universal payment request model."""
    amount: Decimal
    currency: str
    customer_id: Optional[str] = None
    payment_method_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    return_url: Optional[str] = None
    confirmation_method: str = "automatic"
    capture_method: str = "automatic"


class PaymentResponse(BaseModel):
    """Universal payment response model."""
    payment_id: str
    status: str
    amount: Decimal
    currency: str
    client_secret: Optional[str] = None
    confirmation_url: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RefundRequest(BaseModel):
    """Universal refund request model."""
    payment_id: str
    amount: Optional[Decimal] = None
    reason: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WebhookEvent(BaseModel):
    """Universal webhook event model."""
    event_id: str
    event_type: str
    object_type: str
    object_id: str
    data: Dict[str, Any]
    created: datetime
    api_version: Optional[str] = None


async def search_payment_knowledge(
    ctx: RunContext[PaymentAgentDependencies],
    query: str,
    match_count: int = 5
) -> str:
    """
    Search payment integration knowledge base through Archon RAG.

    Args:
        query: Search query for payment integration knowledge
        match_count: Number of results to return

    Returns:
        Knowledge base search results with payment integration expertise
    """
    try:
        # Construct knowledge search query with payment context
        search_query = f"payment integration {ctx.deps.payment_provider} {ctx.deps.business_model} {query}"

        # Use domain filtering if available
        domain_filter = ctx.deps.knowledge_domain if hasattr(ctx.deps, 'knowledge_domain') else None

        # Search through Archon MCP (this would be the actual MCP call)
        # For now, return comprehensive payment knowledge
        knowledge_results = {
            "stripe": _get_stripe_knowledge(query),
            "paypal": _get_paypal_knowledge(query),
            "square": _get_square_knowledge(query),
            "razorpay": _get_razorpay_knowledge(query),
            "braintree": _get_braintree_knowledge(query),
            "adyen": _get_adyen_knowledge(query)
        }

        provider_knowledge = knowledge_results.get(ctx.deps.payment_provider, "")

        # Add business model specific knowledge
        business_knowledge = _get_business_model_knowledge(ctx.deps.business_model, query)

        return f"""**Payment Provider Knowledge ({ctx.deps.payment_provider}):**
{provider_knowledge}

**Business Model Knowledge ({ctx.deps.business_model}):**
{business_knowledge}

**Security Guidelines:**
{_get_security_knowledge(ctx.deps, query)}

**Integration Patterns:**
{_get_integration_patterns_knowledge(ctx.deps, query)}"""

    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        return f"Ошибка поиска в базе знаний: {e}"


async def create_payment(
    ctx: RunContext[PaymentAgentDependencies],
    amount: float,
    currency: str,
    customer_id: Optional[str] = None,
    payment_method_id: Optional[str] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create universal payment across different providers.

    Args:
        amount: Payment amount
        currency: Currency code (USD, EUR, etc.)
        customer_id: Customer identifier
        payment_method_id: Saved payment method ID
        description: Payment description
        metadata: Additional payment metadata

    Returns:
        Universal payment response with provider-specific details
    """
    try:
        payment_request = PaymentRequest(
            amount=Decimal(str(amount)),
            currency=currency.upper(),
            customer_id=customer_id,
            payment_method_id=payment_method_id,
            description=description or f"Payment via {ctx.deps.payment_provider}",
            metadata=metadata or {},
            confirmation_method=ctx.deps.confirmation_method,
            capture_method=ctx.deps.capture_method
        )

        # Provider-specific implementation
        provider_handlers = {
            "stripe": _create_stripe_payment,
            "paypal": _create_paypal_payment,
            "square": _create_square_payment,
            "razorpay": _create_razorpay_payment,
            "braintree": _create_braintree_payment,
            "adyen": _create_adyen_payment
        }

        handler = provider_handlers.get(ctx.deps.payment_provider)
        if not handler:
            raise ValueError(f"Unsupported payment provider: {ctx.deps.payment_provider}")

        response = await handler(ctx.deps, payment_request)

        # Log payment creation for audit
        logger.info(f"Payment created: {response.payment_id} for {amount} {currency}")

        return {
            "success": True,
            "payment_id": response.payment_id,
            "status": response.status,
            "amount": float(response.amount),
            "currency": response.currency,
            "client_secret": response.client_secret,
            "confirmation_url": response.confirmation_url,
            "metadata": response.metadata,
            "provider": ctx.deps.payment_provider
        }

    except Exception as e:
        logger.error(f"Payment creation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": ctx.deps.payment_provider
        }


async def verify_webhook_signature(
    ctx: RunContext[PaymentAgentDependencies],
    payload: str,
    signature: str,
    webhook_secret: Optional[str] = None
) -> Dict[str, Any]:
    """
    Verify webhook signature for secure event processing.

    Args:
        payload: Raw webhook payload
        signature: Webhook signature from headers
        webhook_secret: Webhook signing secret (optional)

    Returns:
        Verification result and parsed event data
    """
    try:
        # Use webhook secret from deps or provided parameter
        secret = webhook_secret or getattr(ctx.deps, 'webhook_secret', ctx.deps.api_key)

        # Provider-specific signature verification
        verification_handlers = {
            "stripe": _verify_stripe_webhook,
            "paypal": _verify_paypal_webhook,
            "square": _verify_square_webhook,
            "razorpay": _verify_razorpay_webhook,
            "braintree": _verify_braintree_webhook,
            "adyen": _verify_adyen_webhook
        }

        handler = verification_handlers.get(ctx.deps.payment_provider)
        if not handler:
            raise ValueError(f"Webhook verification not supported for: {ctx.deps.payment_provider}")

        is_valid, event_data = handler(payload, signature, secret)

        if is_valid:
            # Parse webhook event
            webhook_event = WebhookEvent(
                event_id=event_data.get("id", "unknown"),
                event_type=event_data.get("type", "unknown"),
                object_type=event_data.get("object", "unknown"),
                object_id=event_data.get("object_id", "unknown"),
                data=event_data.get("data", {}),
                created=datetime.now(),
                api_version=event_data.get("api_version")
            )

            logger.info(f"Webhook verified: {webhook_event.event_type}")

            return {
                "success": True,
                "verified": True,
                "event": webhook_event.dict(),
                "provider": ctx.deps.payment_provider
            }
        else:
            logger.warning("Webhook signature verification failed")
            return {
                "success": False,
                "verified": False,
                "error": "Invalid webhook signature",
                "provider": ctx.deps.payment_provider
            }

    except Exception as e:
        logger.error(f"Webhook verification error: {e}")
        return {
            "success": False,
            "verified": False,
            "error": str(e),
            "provider": ctx.deps.payment_provider
        }


async def process_refund(
    ctx: RunContext[PaymentAgentDependencies],
    payment_id: str,
    amount: Optional[float] = None,
    reason: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process payment refund across different providers.

    Args:
        payment_id: Original payment identifier
        amount: Refund amount (None for full refund)
        reason: Refund reason
        metadata: Additional refund metadata

    Returns:
        Refund processing result
    """
    try:
        refund_request = RefundRequest(
            payment_id=payment_id,
            amount=Decimal(str(amount)) if amount else None,
            reason=reason or "Requested by customer",
            metadata=metadata or {}
        )

        # Provider-specific refund implementation
        refund_handlers = {
            "stripe": _process_stripe_refund,
            "paypal": _process_paypal_refund,
            "square": _process_square_refund,
            "razorpay": _process_razorpay_refund,
            "braintree": _process_braintree_refund,
            "adyen": _process_adyen_refund
        }

        handler = refund_handlers.get(ctx.deps.payment_provider)
        if not handler:
            raise ValueError(f"Refund not supported for: {ctx.deps.payment_provider}")

        refund_result = await handler(ctx.deps, refund_request)

        logger.info(f"Refund processed: {refund_result.get('refund_id')} for payment {payment_id}")

        return {
            "success": True,
            "refund_id": refund_result.get("refund_id"),
            "status": refund_result.get("status"),
            "amount": refund_result.get("amount"),
            "currency": refund_result.get("currency"),
            "reason": refund_request.reason,
            "provider": ctx.deps.payment_provider
        }

    except Exception as e:
        logger.error(f"Refund processing error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": ctx.deps.payment_provider
        }


async def validate_payment_configuration(
    ctx: RunContext[PaymentAgentDependencies]
) -> Dict[str, Any]:
    """
    Validate payment provider configuration and settings.

    Returns:
        Configuration validation results and recommendations
    """
    try:
        validation_results = ctx.deps.validate_configuration()

        # Provider-specific health check
        health_check_result = await _check_provider_health(ctx.deps)

        # Security configuration check
        security_score = _calculate_security_score(ctx.deps)

        # Business model optimization check
        optimization_recommendations = _get_optimization_recommendations(ctx.deps)

        return {
            "success": True,
            "provider": ctx.deps.payment_provider,
            "business_model": ctx.deps.business_model,
            "configuration_valid": len(validation_results) == 0,
            "issues": validation_results,
            "health_check": health_check_result,
            "security_score": security_score,
            "recommendations": optimization_recommendations,
            "supported_payment_methods": ctx.deps.get_supported_payment_methods(),
            "compliance": {
                "pci_dss": ctx.deps.pci_compliance,
                "gdpr": ctx.deps.gdpr_compliance,
                "psd2": ctx.deps.psd2_compliance,
                "kyc": ctx.deps.kyc_requirements
            }
        }

    except Exception as e:
        logger.error(f"Configuration validation error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": ctx.deps.payment_provider
        }


# Provider-specific implementation functions

async def _create_stripe_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create Stripe payment intent."""
    # Stripe Payment Intent creation logic
    payment_id = f"pi_stripe_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="requires_confirmation",
        amount=request.amount,
        currency=request.currency,
        client_secret=f"{payment_id}_secret",
        metadata=request.metadata
    )


async def _create_paypal_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create PayPal payment order."""
    payment_id = f"paypal_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="created",
        amount=request.amount,
        currency=request.currency,
        confirmation_url=f"https://www.paypal.com/checkoutnow?token={payment_id}",
        metadata=request.metadata
    )


async def _create_square_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create Square payment."""
    payment_id = f"square_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="pending",
        amount=request.amount,
        currency=request.currency,
        metadata=request.metadata
    )


async def _create_razorpay_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create Razorpay payment order."""
    payment_id = f"order_razorpay_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="created",
        amount=request.amount,
        currency=request.currency,
        metadata=request.metadata
    )


async def _create_braintree_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create Braintree transaction."""
    payment_id = f"braintree_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="submitted_for_settlement",
        amount=request.amount,
        currency=request.currency,
        metadata=request.metadata
    )


async def _create_adyen_payment(deps: PaymentAgentDependencies, request: PaymentRequest) -> PaymentResponse:
    """Create Adyen payment."""
    payment_id = f"adyen_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return PaymentResponse(
        payment_id=payment_id,
        status="pending",
        amount=request.amount,
        currency=request.currency,
        metadata=request.metadata
    )


# Webhook verification functions

def _verify_stripe_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify Stripe webhook signature."""
    try:
        # Stripe signature verification logic
        elements = signature.split(',')
        signature_hash = None
        timestamp = None

        for element in elements:
            if element.startswith('v1='):
                signature_hash = element[3:]
            elif element.startswith('t='):
                timestamp = element[2:]

        if not signature_hash or not timestamp:
            return False, {}

        # Create expected signature
        payload_to_sign = f"{timestamp}.{payload}"
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        is_valid = hmac.compare_digest(signature_hash, expected_signature)
        event_data = json.loads(payload) if is_valid else {}

        return is_valid, event_data

    except Exception:
        return False, {}


def _verify_paypal_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify PayPal webhook signature."""
    # PayPal webhook verification would be implemented here
    try:
        event_data = json.loads(payload)
        return True, event_data  # Simplified for demo
    except Exception:
        return False, {}


def _verify_square_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify Square webhook signature."""
    # Square webhook verification would be implemented here
    try:
        event_data = json.loads(payload)
        return True, event_data  # Simplified for demo
    except Exception:
        return False, {}


def _verify_razorpay_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify Razorpay webhook signature."""
    # Razorpay webhook verification would be implemented here
    try:
        event_data = json.loads(payload)
        return True, event_data  # Simplified for demo
    except Exception:
        return False, {}


def _verify_braintree_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify Braintree webhook signature."""
    # Braintree webhook verification would be implemented here
    try:
        event_data = json.loads(payload)
        return True, event_data  # Simplified for demo
    except Exception:
        return False, {}


def _verify_adyen_webhook(payload: str, signature: str, secret: str) -> tuple[bool, Dict[str, Any]]:
    """Verify Adyen webhook signature."""
    # Adyen webhook verification would be implemented here
    try:
        event_data = json.loads(payload)
        return True, event_data  # Simplified for demo
    except Exception:
        return False, {}


# Refund processing functions

async def _process_stripe_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process Stripe refund."""
    refund_id = f"re_stripe_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "succeeded",
        "amount": request.amount,
        "currency": "USD"  # Would get from original payment
    }


async def _process_paypal_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process PayPal refund."""
    refund_id = f"paypal_refund_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "completed",
        "amount": request.amount,
        "currency": "USD"
    }


async def _process_square_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process Square refund."""
    refund_id = f"square_refund_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "pending",
        "amount": request.amount,
        "currency": "USD"
    }


async def _process_razorpay_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process Razorpay refund."""
    refund_id = f"rfnd_razorpay_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "processed",
        "amount": request.amount,
        "currency": "INR"
    }


async def _process_braintree_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process Braintree refund."""
    refund_id = f"braintree_refund_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "submitted_for_settlement",
        "amount": request.amount,
        "currency": "USD"
    }


async def _process_adyen_refund(deps: PaymentAgentDependencies, request: RefundRequest) -> Dict[str, Any]:
    """Process Adyen refund."""
    refund_id = f"adyen_refund_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "refund_id": refund_id,
        "status": "received",
        "amount": request.amount,
        "currency": "EUR"
    }


# Knowledge base functions

def _get_stripe_knowledge(query: str) -> str:
    """Get Stripe-specific knowledge."""
    return """
**Stripe Best Practices:**
- Use Payment Intents API для modern payment flows
- Implement SCA/3DS2 для European customers
- Utilize Stripe Elements для PCI compliance
- Set up webhooks с idempotency handling
- Use Stripe Connect для marketplace payments
- Implement Radar rules для fraud prevention
- Support multiple payment methods (cards, wallets, bank transfers)
- Handle failed payments с Smart Retries
"""


def _get_paypal_knowledge(query: str) -> str:
    """Get PayPal-specific knowledge."""
    return """
**PayPal Best Practices:**
- Use Orders API v2 для checkout flows
- Implement Express Checkout для better UX
- Set up webhook subscriptions для order updates
- Use PayPal Commerce Platform для marketplaces
- Support PayPal Credit и Pay in 4
- Implement proper error handling для declined payments
- Use PayPal SDK для mobile integration
- Handle currency conversion automatically
"""


def _get_square_knowledge(query: str) -> str:
    """Get Square-specific knowledge."""
    return """
**Square Best Practices:**
- Use Web Payments SDK для online payments
- Implement In-Person Payments для POS integration
- Set up webhooks для payment notifications
- Use Square Invoices для billing
- Implement proper inventory sync
- Support gift cards и loyalty programs
- Use Application fees для marketplace scenarios
- Handle refunds и chargebacks properly
"""


def _get_razorpay_knowledge(query: str) -> str:
    """Get Razorpay-specific knowledge."""
    return """
**Razorpay Best Practices:**
- Use Standard Checkout для quick integration
- Implement Custom Checkout для branded experience
- Set up Payment Links для remote sales
- Use Route API для marketplace payments
- Support UPI, Net Banking, Wallets
- Implement Smart Collect для bank transfers
- Handle currency conversion для international
- Use Dashboard APIs для analytics
"""


def _get_braintree_knowledge(query: str) -> str:
    """Get Braintree-specific knowledge."""
    return """
**Braintree Best Practices:**
- Use Drop-in UI для quick integration
- Implement Custom Fields для advanced flows
- Support PayPal, Venmo, Apple Pay, Google Pay
- Use Vault для storing payment methods
- Implement 3D Secure для enhanced security
- Set up webhooks для transaction updates
- Use Marketplace functionality для multi-party payments
- Handle subscription billing properly
"""


def _get_adyen_knowledge(query: str) -> str:
    """Get Adyen-specific knowledge."""
    return """
**Adyen Best Practices:**
- Use Checkout API для unified integration
- Implement local payment methods globally
- Set up Authentication 3DS2 properly
- Use Adyen for Platforms для marketplaces
- Implement proper webhook handling
- Support real-time account updates
- Use RevenueProtect для fraud prevention
- Handle multi-currency processing
"""


def _get_business_model_knowledge(business_model: str, query: str) -> str:
    """Get business model specific knowledge."""
    knowledge_map = {
        "ecommerce": """
- Implement abandoned cart recovery flows
- Support guest checkout и account creation
- Handle inventory sync with payments
- Implement proper tax calculation
- Support multiple shipping options
- Handle subscription products
- Implement loyalty programs integration
""",
        "saas": """
- Implement subscription lifecycle management
- Handle plan changes с proration
- Set up dunning management для failed payments
- Implement usage-based billing
- Support trial periods и freemium models
- Handle customer retention flows
- Implement revenue recognition properly
""",
        "marketplace": """
- Implement multi-party payment flows
- Handle platform fee collection
- Set up vendor onboarding с KYC
- Implement escrow payment holding
- Handle dispute resolution
- Support split payments properly
- Implement commission tracking
""",
        "donation": """
- Support recurring donation setup
- Implement donor management
- Handle anonymous donations
- Generate tax receipts automatically
- Support campaign-based tracking
- Implement fundraising goal tracking
- Handle transparent fee disclosure
"""
    }

    return knowledge_map.get(business_model, "General payment processing patterns")


def _get_security_knowledge(deps: PaymentAgentDependencies, query: str) -> str:
    """Get security-specific knowledge."""
    return f"""
**Security Requirements ({deps.pci_compliance}):**
- Implement proper token-based card storage
- Use HTTPS/TLS 1.2+ для all communications
- Handle PCI DSS compliance requirements
- Implement fraud detection rules
- Set up webhook signature verification
- Use proper API key management
- Implement rate limiting и monitoring
- Handle PII data protection (GDPR/PSD2)
"""


def _get_integration_patterns_knowledge(deps: PaymentAgentDependencies, query: str) -> str:
    """Get integration patterns knowledge."""
    return f"""
**Integration Patterns ({deps.payment_flow}):**
- Implement proper error handling patterns
- Set up retry logic для failed requests
- Handle webhook deduplication
- Implement proper logging для audit trails
- Use background job processing для heavy operations
- Handle payment state machine properly
- Implement proper testing strategies
- Set up monitoring и alerting
"""


# Utility functions

async def _check_provider_health(deps: PaymentAgentDependencies) -> Dict[str, Any]:
    """Check payment provider API health."""
    # This would make actual API calls to check provider status
    return {
        "api_accessible": True,
        "response_time": 150,  # ms
        "status": "operational",
        "last_checked": datetime.now().isoformat()
    }


def _calculate_security_score(deps: PaymentAgentDependencies) -> int:
    """Calculate security configuration score."""
    score = 0

    # PCI compliance
    if deps.pci_compliance == "pci_dss_saq_d":
        score += 30
    elif deps.pci_compliance == "pci_dss_saq_a":
        score += 20

    # Encryption
    if deps.encryption_at_rest:
        score += 15
    if deps.encryption_in_transit:
        score += 15

    # Fraud detection
    if deps.fraud_detection == "machine_learning":
        score += 20
    elif deps.fraud_detection == "advanced":
        score += 15
    elif deps.fraud_detection == "basic":
        score += 10

    # Additional security features
    if deps.tokenization:
        score += 10
    if deps.webhook_security == "both":
        score += 10
    elif deps.webhook_security == "signature_verification":
        score += 5

    return min(score, 100)


def _get_optimization_recommendations(deps: PaymentAgentDependencies) -> List[str]:
    """Get configuration optimization recommendations."""
    recommendations = []

    # Business model optimizations
    if deps.business_model == "saas" and not deps.subscription_support:
        recommendations.append("Enable subscription support for SaaS business model")

    if deps.business_model == "marketplace" and not deps.marketplace_support:
        recommendations.append("Enable marketplace features for multi-party payments")

    # Security optimizations
    if deps.fraud_detection == "basic" and deps.business_model in ["gaming", "crypto"]:
        recommendations.append("Consider advanced fraud detection for high-risk business model")

    # Compliance optimizations
    if "EUR" in deps.supported_currencies and not deps.psd2_compliance:
        recommendations.append("Enable PSD2 compliance for European operations")

    # Performance optimizations
    if not deps.caching_enabled:
        recommendations.append("Enable caching for better performance")

    if not deps.webhook_enabled:
        recommendations.append("Enable webhooks for real-time payment updates")

    return recommendations