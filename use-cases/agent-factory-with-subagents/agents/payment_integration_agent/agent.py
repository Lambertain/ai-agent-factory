"""
Universal Payment Integration Agent for Pydantic AI.

Comprehensive AI agent for payment system integration supporting multiple providers
and business models with adaptive prompts and universal configuration.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from pydantic_ai import Agent, RunContext

from .dependencies import PaymentAgentDependencies
from ..common import check_pm_switch
from .prompts import get_system_prompt
from .settings import get_llm_model
from ..common.pydantic_ai_decorators import (
    create_universal_pydantic_agent,
    with_integrations,
    register_agent
)
from .tools import (
    create_payment,
    verify_webhook_signature,
    process_refund,
    validate_payment_configuration
)

logger = logging.getLogger(__name__)

# Create universal payment integration agent with decorators
payment_integration_agent = create_universal_pydantic_agent(
    model=get_llm_model(),
    deps_type=PaymentAgentDependencies,
    system_prompt=lambda deps: get_system_prompt(deps),
    agent_type="payment_integration",
    knowledge_tags=["payment", "integration", "agent-knowledge", "pydantic-ai"],
    knowledge_domain="payment.integration.com",
    with_collective_tools=True,
    with_knowledge_tool=True
)

# Register agent in global registry
register_agent("payment_integration", payment_integration_agent, agent_type="payment_integration")

# Register payment integration tools
payment_integration_agent.tool(create_payment)
payment_integration_agent.tool(verify_webhook_signature)
payment_integration_agent.tool(process_refund)
payment_integration_agent.tool(validate_payment_configuration)

# Collective work tools and knowledge search now added automatically via decorators


def get_payment_integration_agent(deps: Optional[PaymentAgentDependencies] = None) -> Agent[PaymentAgentDependencies, str]:
    """
    Get payment integration agent instance.

    Args:
        deps: Optional payment dependencies (not used, kept for compatibility)

    Returns:
        Configured payment integration agent
    """
    # Return global agent instance created with decorators
    return payment_integration_agent


async def run_payment_integration_agent(
    user_input: str,
    deps: Optional[PaymentAgentDependencies] = None,
    **kwargs
) -> str:
    """
    Run payment integration agent with user input.

    Args:
        user_input: User query or request for payment integration
        deps: Payment agent dependencies
        **kwargs: Additional arguments for agent execution

    Returns:
        Agent response with payment integration guidance
    """
    try:
        # Use global agent instance with provided deps
        if deps is None:
            deps = PaymentAgentDependencies(api_key="demo")

        result = await payment_integration_agent.run(user_input, deps=deps)

        logger.info(f"Payment integration request completed: {user_input[:100]}...")
        return result.data

    except Exception as e:
        logger.error(f"Payment integration agent error: {e}")
        return f"Ошибка выполнения агента платежной интеграции: {e}"


async def process_payment_request(
    amount: float,
    currency: str,
    deps: PaymentAgentDependencies,
    customer_id: Optional[str] = None,
    payment_method_id: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Process payment request through the agent.

    Args:
        amount: Payment amount
        currency: Currency code
        deps: Payment agent dependencies
        customer_id: Customer identifier
        payment_method_id: Saved payment method ID
        description: Payment description
        **kwargs: Additional payment parameters

    Returns:
        Payment processing result
    """
    try:
        agent = get_payment_integration_agent(deps)

        # Create payment through agent tools
        with agent.override(deps=deps):
            payment_result = await create_payment(
                ctx=RunContext(deps=deps, retry=0),
                amount=amount,
                currency=currency,
                customer_id=customer_id,
                payment_method_id=payment_method_id,
                description=description,
                metadata=kwargs
            )

        logger.info(f"Payment processed: {payment_result.get('payment_id')}")
        return payment_result

    except Exception as e:
        logger.error(f"Payment processing error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": deps.payment_provider
        }


async def validate_webhook_event(
    payload: str,
    signature: str,
    deps: PaymentAgentDependencies,
    webhook_secret: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate webhook event through the agent.

    Args:
        payload: Webhook payload
        signature: Webhook signature
        deps: Payment agent dependencies
        webhook_secret: Webhook signing secret

    Returns:
        Webhook validation result
    """
    try:
        agent = get_payment_integration_agent(deps)

        # Verify webhook through agent tools
        with agent.override(deps=deps):
            verification_result = await verify_webhook_signature(
                ctx=RunContext(deps=deps, retry=0),
                payload=payload,
                signature=signature,
                webhook_secret=webhook_secret
            )

        logger.info(f"Webhook validated: {verification_result.get('verified')}")
        return verification_result

    except Exception as e:
        logger.error(f"Webhook validation error: {e}")
        return {
            "success": False,
            "verified": False,
            "error": str(e),
            "provider": deps.payment_provider
        }


async def process_payment_refund(
    payment_id: str,
    deps: PaymentAgentDependencies,
    amount: Optional[float] = None,
    reason: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Process payment refund through the agent.

    Args:
        payment_id: Payment identifier
        deps: Payment agent dependencies
        amount: Refund amount (None for full refund)
        reason: Refund reason
        **kwargs: Additional refund parameters

    Returns:
        Refund processing result
    """
    try:
        agent = get_payment_integration_agent(deps)

        # Process refund through agent tools
        with agent.override(deps=deps):
            refund_result = await process_refund(
                ctx=RunContext(deps=deps, retry=0),
                payment_id=payment_id,
                amount=amount,
                reason=reason,
                metadata=kwargs
            )

        logger.info(f"Refund processed: {refund_result.get('refund_id')}")
        return refund_result

    except Exception as e:
        logger.error(f"Refund processing error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": deps.payment_provider
        }


async def get_payment_configuration_analysis(
    deps: PaymentAgentDependencies
) -> Dict[str, Any]:
    """
    Get comprehensive payment configuration analysis.

    Args:
        deps: Payment agent dependencies

    Returns:
        Configuration analysis and recommendations
    """
    try:
        agent = get_payment_integration_agent(deps)

        # Validate configuration through agent tools
        with agent.override(deps=deps):
            analysis_result = await validate_payment_configuration(
                ctx=RunContext(deps=deps, retry=0)
            )

        logger.info(f"Configuration analyzed for {deps.payment_provider}")
        return analysis_result

    except Exception as e:
        logger.error(f"Configuration analysis error: {e}")
        return {
            "success": False,
            "error": str(e),
            "provider": deps.payment_provider
        }


# Convenience functions for different business models

def create_ecommerce_payment_deps(
    api_key: str,
    payment_provider: str = "stripe",
    project_path: str = "",
    **kwargs
) -> PaymentAgentDependencies:
    """Create payment dependencies optimized for e-commerce."""
    return PaymentAgentDependencies(
        api_key=api_key,
        project_path=project_path,
        payment_provider=payment_provider,
        business_model="ecommerce",
        payment_types=["card", "digital_wallet", "bank_transfer"],
        fraud_detection="advanced",
        refund_support=True,
        **kwargs
    )


def create_saas_payment_deps(
    api_key: str,
    payment_provider: str = "stripe",
    project_path: str = "",
    **kwargs
) -> PaymentAgentDependencies:
    """Create payment dependencies optimized for SaaS."""
    return PaymentAgentDependencies(
        api_key=api_key,
        project_path=project_path,
        payment_provider=payment_provider,
        business_model="saas",
        subscription_support=True,
        recurring_billing=True,
        trial_periods=True,
        dunning_management=True,
        churn_analytics=True,
        **kwargs
    )


def create_marketplace_payment_deps(
    api_key: str,
    payment_provider: str = "stripe",
    project_path: str = "",
    **kwargs
) -> PaymentAgentDependencies:
    """Create payment dependencies optimized for marketplaces."""
    return PaymentAgentDependencies(
        api_key=api_key,
        project_path=project_path,
        payment_provider=payment_provider,
        business_model="marketplace",
        marketplace_support=True,
        split_payments=True,
        platform_fees=True,
        vendor_onboarding=True,
        escrow_support=True,
        **kwargs
    )


def create_donation_payment_deps(
    api_key: str,
    payment_provider: str = "stripe",
    project_path: str = "",
    **kwargs
) -> PaymentAgentDependencies:
    """Create payment dependencies optimized for donations."""
    return PaymentAgentDependencies(
        api_key=api_key,
        project_path=project_path,
        payment_provider=payment_provider,
        business_model="donation",
        payment_types=["card", "bank_transfer", "digital_wallet"],
        recurring_billing=True,
        analytics_enabled=True,
        fraud_detection="basic",
        **kwargs
    )


# Main execution function
async def main():
    """
    Main execution function for testing the payment integration agent.
    """
    # Create test dependencies
    deps = PaymentAgentDependencies(
        api_key="test_api_key",
        project_path="/path/to/project",
        project_name="Test Payment Project",
        payment_provider="stripe",
        business_model="ecommerce"
    )

    # Test payment agent (using global instance)
    # Test queries
    test_queries = [
        "Как интегрировать Stripe для e-commerce платежей?",
        "Настроить webhook для обработки платежей",
        "Реализовать возвраты для failed платежей",
        "Добавить поддержку подписок",
        "Настроить fraud detection"
    ]

    print(f"🔄 Тестирование Payment Integration Agent ({deps.payment_provider} - {deps.business_model})")
    print("=" * 80)

    for query in test_queries:
        print(f"\n💬 Запрос: {query}")
        print("-" * 40)

        try:
            response = await run_payment_integration_agent(query, deps)
            print(f"🤖 Ответ: {response[:200]}...")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    # Test payment processing
    print(f"\n💳 Тестирование создания платежа...")
    payment_result = await process_payment_request(
        amount=99.99,
        currency="USD",
        deps=deps,
        description="Test payment"
    )
    print(f"Результат: {payment_result}")

    # Test configuration validation
    print(f"\n⚙️ Тестирование валидации конфигурации...")
    config_result = await get_payment_configuration_analysis(deps)
    print(f"Конфигурация: {config_result.get('configuration_valid')}")
    print(f"Рекомендации: {len(config_result.get('recommendations', []))}")


if __name__ == "__main__":
    asyncio.run(main())