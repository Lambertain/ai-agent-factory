"""
Tests for Payment Integration Agent.

Comprehensive test suite for payment integration functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from decimal import Decimal

from ..dependencies import PaymentAgentDependencies
from ..agent import (
    get_payment_integration_agent,
    run_payment_integration_agent,
    process_payment_request,
    validate_webhook_event,
    process_payment_refund
)
from ..tools import (
    search_payment_knowledge,
    create_payment,
    verify_webhook_signature,
    process_refund,
    validate_payment_configuration
)


class TestPaymentAgentDependencies:
    """Test payment agent dependencies configuration."""

    def test_default_configuration(self):
        """Test default dependency configuration."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            project_path="/test/path",
            project_name="Test Project"
        )

        assert deps.api_key == "test_key"
        assert deps.payment_provider == "stripe"
        assert deps.business_model == "ecommerce"
        assert deps.default_currency == "USD"
        assert deps.pci_compliance == "pci_dss_saq_a"

    def test_stripe_configuration_optimization(self):
        """Test Stripe-specific configuration optimization."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="stripe",
            business_model="ecommerce"
        )

        # Should auto-configure Stripe optimizations
        assert deps.fraud_detection == "advanced"
        assert deps.subscription_support == True
        assert deps.tokenization == True

    def test_saas_business_model_optimization(self):
        """Test SaaS business model optimization."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            business_model="saas"
        )

        # Should auto-configure SaaS features
        assert deps.subscription_support == True
        assert deps.recurring_billing == True
        assert deps.trial_periods == True
        assert deps.dunning_management == True
        assert deps.churn_analytics == True

    def test_marketplace_business_model_optimization(self):
        """Test marketplace business model optimization."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            business_model="marketplace"
        )

        # Should auto-configure marketplace features
        assert deps.marketplace_support == True
        assert deps.split_payments == True
        assert deps.platform_fees == True
        assert deps.vendor_onboarding == True

    def test_european_compliance_configuration(self):
        """Test European compliance auto-configuration."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            supported_currencies=["EUR", "GBP"]
        )

        # Should auto-enable European compliance
        assert deps.gdpr_compliance == True
        assert deps.psd2_compliance == True
        assert deps.strong_customer_authentication == True

    def test_configuration_validation(self):
        """Test configuration validation."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="unknown_provider"
        )

        issues = deps.validate_configuration()
        assert len(issues) > 0
        assert any("Unsupported payment provider" in issue for issue in issues)

    def test_supported_payment_methods(self):
        """Test supported payment methods generation."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_types=["card", "digital_wallet"],
            supported_currencies=["USD", "EUR"]
        )

        methods = deps.get_supported_payment_methods()
        assert len(methods) == 2

        card_method = next(m for m in methods if m["type"] == "card")
        assert "visa" in card_method["brands"]
        assert card_method["currencies"] == ["USD", "EUR"]

        wallet_method = next(m for m in methods if m["type"] == "digital_wallet")
        assert "apple_pay" in wallet_method["wallets"]


class TestPaymentTools:
    """Test payment processing tools."""

    @pytest.fixture
    def mock_deps(self):
        """Create mock dependencies for testing."""
        return PaymentAgentDependencies(
            api_key="test_stripe_key",
            payment_provider="stripe",
            business_model="ecommerce",
            project_path="/test/project"
        )

    @pytest.mark.asyncio
    async def test_search_payment_knowledge(self, mock_deps):
        """Test payment knowledge search."""
        from pydantic_ai import RunContext

        ctx = RunContext(deps=mock_deps, retry=0)
        result = await search_payment_knowledge(ctx, "stripe integration")

        assert "Stripe" in result
        assert "payment" in result.lower()
        assert len(result) > 100  # Should return substantial knowledge

    @pytest.mark.asyncio
    async def test_create_payment_stripe(self, mock_deps):
        """Test Stripe payment creation."""
        from pydantic_ai import RunContext

        ctx = RunContext(deps=mock_deps, retry=0)
        result = await create_payment(
            ctx=ctx,
            amount=99.99,
            currency="USD",
            customer_id="cus_test123",
            description="Test payment"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"
        assert result["amount"] == 99.99
        assert result["currency"] == "USD"
        assert "payment_id" in result

    @pytest.mark.asyncio
    async def test_create_payment_different_providers(self):
        """Test payment creation with different providers."""
        from pydantic_ai import RunContext

        providers = ["stripe", "paypal", "square", "razorpay"]

        for provider in providers:
            deps = PaymentAgentDependencies(
                api_key=f"test_{provider}_key",
                payment_provider=provider
            )
            ctx = RunContext(deps=deps, retry=0)

            result = await create_payment(
                ctx=ctx,
                amount=50.00,
                currency="USD"
            )

            assert result["success"] == True
            assert result["provider"] == provider

    @pytest.mark.asyncio
    async def test_verify_webhook_signature_stripe(self, mock_deps):
        """Test Stripe webhook signature verification."""
        from pydantic_ai import RunContext

        ctx = RunContext(deps=mock_deps, retry=0)
        test_payload = '{"id": "evt_test", "type": "payment_intent.succeeded"}'
        test_signature = "t=1234567890,v1=test_signature"

        result = await verify_webhook_signature(
            ctx=ctx,
            payload=test_payload,
            signature=test_signature,
            webhook_secret="whsec_test_secret"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"
        # Note: In real implementation, signature verification would be more complex

    @pytest.mark.asyncio
    async def test_process_refund(self, mock_deps):
        """Test refund processing."""
        from pydantic_ai import RunContext

        ctx = RunContext(deps=mock_deps, retry=0)
        result = await process_refund(
            ctx=ctx,
            payment_id="pi_test123",
            amount=25.00,
            reason="Customer request"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"
        assert "refund_id" in result

    @pytest.mark.asyncio
    async def test_validate_payment_configuration(self, mock_deps):
        """Test payment configuration validation."""
        from pydantic_ai import RunContext

        ctx = RunContext(deps=mock_deps, retry=0)
        result = await validate_payment_configuration(ctx)

        assert result["success"] == True
        assert result["provider"] == "stripe"
        assert result["business_model"] == "ecommerce"
        assert "security_score" in result
        assert "recommendations" in result
        assert "supported_payment_methods" in result


class TestPaymentAgent:
    """Test payment integration agent functionality."""

    @pytest.fixture
    def mock_deps(self):
        """Create mock dependencies for testing."""
        return PaymentAgentDependencies(
            api_key="test_stripe_key",
            payment_provider="stripe",
            business_model="ecommerce",
            project_path="/test/project"
        )

    def test_get_payment_integration_agent(self, mock_deps):
        """Test agent creation."""
        agent = get_payment_integration_agent(mock_deps)
        assert agent is not None
        assert hasattr(agent, 'run')

    @pytest.mark.asyncio
    async def test_run_payment_integration_agent(self, mock_deps):
        """Test agent execution."""
        response = await run_payment_integration_agent(
            "How do I integrate Stripe for e-commerce payments?",
            mock_deps
        )

        assert isinstance(response, str)
        assert len(response) > 0
        # Should contain relevant payment integration guidance

    @pytest.mark.asyncio
    async def test_process_payment_request(self, mock_deps):
        """Test payment request processing."""
        result = await process_payment_request(
            amount=99.99,
            currency="USD",
            deps=mock_deps,
            customer_id="cus_test123",
            description="Test payment"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"
        assert "payment_id" in result

    @pytest.mark.asyncio
    async def test_validate_webhook_event(self, mock_deps):
        """Test webhook event validation."""
        result = await validate_webhook_event(
            payload='{"id": "evt_test", "type": "payment_intent.succeeded"}',
            signature="t=1234567890,v1=test_signature",
            deps=mock_deps,
            webhook_secret="whsec_test_secret"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"

    @pytest.mark.asyncio
    async def test_process_payment_refund(self, mock_deps):
        """Test payment refund processing."""
        result = await process_payment_refund(
            payment_id="pi_test123",
            deps=mock_deps,
            amount=50.00,
            reason="Customer request"
        )

        assert result["success"] == True
        assert result["provider"] == "stripe"


class TestBusinessModelAgents:
    """Test business model specific agent creation."""

    @pytest.mark.asyncio
    async def test_create_ecommerce_payment_agent(self):
        """Test e-commerce agent creation."""
        from ..agent import create_ecommerce_payment_agent

        agent = await create_ecommerce_payment_agent(
            api_key="test_key",
            payment_provider="stripe",
            project_path="/test/ecommerce"
        )

        assert agent is not None

    @pytest.mark.asyncio
    async def test_create_saas_payment_agent(self):
        """Test SaaS agent creation."""
        from ..agent import create_saas_payment_agent

        agent = await create_saas_payment_agent(
            api_key="test_key",
            payment_provider="stripe",
            project_path="/test/saas"
        )

        assert agent is not None

    @pytest.mark.asyncio
    async def test_create_marketplace_payment_agent(self):
        """Test marketplace agent creation."""
        from ..agent import create_marketplace_payment_agent

        agent = await create_marketplace_payment_agent(
            api_key="test_key",
            payment_provider="stripe",
            project_path="/test/marketplace"
        )

        assert agent is not None

    @pytest.mark.asyncio
    async def test_create_donation_payment_agent(self):
        """Test donation agent creation."""
        from ..agent import create_donation_payment_agent

        agent = await create_donation_payment_agent(
            api_key="test_key",
            payment_provider="stripe",
            project_path="/test/donation"
        )

        assert agent is not None


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_invalid_provider_error(self):
        """Test handling of invalid payment provider."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="invalid_provider"
        )

        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps, retry=0)

        result = await create_payment(
            ctx=ctx,
            amount=100.00,
            currency="USD"
        )

        assert result["success"] == False
        assert "error" in result

    @pytest.mark.asyncio
    async def test_payment_failure_handling(self):
        """Test payment failure scenarios."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="stripe"
        )

        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps, retry=0)

        # Test with invalid amount
        result = await create_payment(
            ctx=ctx,
            amount=-100.00,  # Invalid negative amount
            currency="USD"
        )

        # Should handle gracefully
        assert "error" in result or result["success"] == False


class TestIntegrationScenarios:
    """Test real-world integration scenarios."""

    @pytest.mark.asyncio
    async def test_ecommerce_checkout_flow(self):
        """Test complete e-commerce checkout flow."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="stripe",
            business_model="ecommerce",
            payment_types=["card", "digital_wallet"]
        )

        # 1. Validate configuration
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps, retry=0)

        config_result = await validate_payment_configuration(ctx)
        assert config_result["success"] == True

        # 2. Create payment
        payment_result = await create_payment(
            ctx=ctx,
            amount=149.99,
            currency="USD",
            customer_id="cus_test_ecommerce",
            description="E-commerce order #12345"
        )
        assert payment_result["success"] == True

        # 3. Process webhook (simulate payment success)
        webhook_result = await verify_webhook_signature(
            ctx=ctx,
            payload='{"id": "evt_test", "type": "payment_intent.succeeded"}',
            signature="test_signature"
        )
        assert webhook_result["success"] == True

    @pytest.mark.asyncio
    async def test_saas_subscription_flow(self):
        """Test SaaS subscription flow."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="stripe",
            business_model="saas",
            subscription_support=True,
            trial_periods=True
        )

        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps, retry=0)

        # Validate SaaS configuration
        config_result = await validate_payment_configuration(ctx)
        assert config_result["success"] == True
        assert "subscription" in str(config_result.get("supported_payment_methods", []))

        # Create subscription payment
        payment_result = await create_payment(
            ctx=ctx,
            amount=29.99,
            currency="USD",
            customer_id="cus_test_saas",
            description="Monthly subscription"
        )
        assert payment_result["success"] == True

    @pytest.mark.asyncio
    async def test_marketplace_split_payment_flow(self):
        """Test marketplace split payment flow."""
        deps = PaymentAgentDependencies(
            api_key="test_key",
            payment_provider="stripe",
            business_model="marketplace",
            marketplace_support=True,
            split_payments=True,
            platform_fees=True
        )

        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps, retry=0)

        # Validate marketplace configuration
        config_result = await validate_payment_configuration(ctx)
        assert config_result["success"] == True

        # Create marketplace payment
        payment_result = await create_payment(
            ctx=ctx,
            amount=199.99,
            currency="USD",
            customer_id="cus_test_marketplace",
            description="Marketplace order with vendor split",
            metadata={
                "marketplace_order": True,
                "vendor_id": "vendor_123",
                "platform_fee": 19.99
            }
        )
        assert payment_result["success"] == True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])