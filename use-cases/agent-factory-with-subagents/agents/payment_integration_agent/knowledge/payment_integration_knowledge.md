# Payment Integration Agent Knowledge Base

## Системный промпт

Ты специализированный AI-агент для интеграции платежных систем с экспертизой в современных payment провайдерах и финтех решениях. Твоя задача - предоставлять комплексную помощь в интеграции, настройке и оптимизации платежных решений для различных бизнес-моделей.

### Экспертиза охватывает:
- **8+ платежных провайдеров**: Stripe, PayPal, Square, Razorpay, Braintree, Adyen, Mollie, Checkout.com
- **7+ бизнес-моделей**: E-commerce, SaaS, Marketplace, Donation, Subscription, P2P, Gaming
- **Универсальная интеграция**: Адаптивные решения под любой проект и технологический стек
- **Безопасность и комплаенс**: PCI DSS, GDPR, PSD2, KYC/AML требования
- **Современные паттерны**: Webhook обработка, fraud detection, multi-currency поддержка

## Ключевые паттерны интеграции

### 1. Universal Payment Provider Integration

#### Stripe Integration Patterns
```python
# Payment Intent для современного flow
payment_intent = stripe.PaymentIntent.create(
    amount=amount_in_cents,
    currency='usd',
    payment_method_types=['card', 'us_bank_account'],
    confirmation_method='automatic',
    capture_method='automatic'
)

# Setup Intent для сохранения методов
setup_intent = stripe.SetupIntent.create(
    customer=customer_id,
    payment_method_types=['card'],
    usage='off_session'
)

# Webhook signature verification
def verify_stripe_webhook(payload, sig_header, endpoint_secret):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return True, event
    except stripe.error.SignatureVerificationError:
        return False, None
```

#### PayPal Integration Patterns
```python
# PayPal Order creation
order_request = {
    "intent": "CAPTURE",
    "purchase_units": [{
        "amount": {
            "currency_code": "USD",
            "value": str(amount)
        }
    }],
    "payment_source": {
        "paypal": {
            "experience_context": {
                "return_url": return_url,
                "cancel_url": cancel_url
            }
        }
    }
}

# PayPal subscription creation
subscription_request = {
    "plan_id": plan_id,
    "subscriber": {
        "email_address": customer_email
    },
    "application_context": {
        "return_url": return_url,
        "cancel_url": cancel_url
    }
}
```

#### Square Integration Patterns
```python
# Square payment creation
payment_request = {
    "source_id": source_id,
    "amount_money": {
        "amount": amount_in_cents,
        "currency": "USD"
    },
    "idempotency_key": str(uuid.uuid4())
}

# Square subscription creation
subscription_request = {
    "card_id": card_id,
    "plan_id": plan_id,
    "start_date": start_date
}
```

### 2. Business Model Specific Patterns

#### E-commerce Payment Flow
```python
class EcommercePaymentFlow:
    def __init__(self, provider_config):
        self.provider = provider_config

    async def create_checkout_session(self, cart_items, customer):
        # Calculate total including tax and shipping
        total = self.calculate_total(cart_items)

        # Create payment with inventory hold
        payment = await self.provider.create_payment(
            amount=total.amount,
            currency=total.currency,
            metadata={
                "order_id": cart_items.order_id,
                "customer_id": customer.id,
                "items": json.dumps(cart_items.items)
            }
        )

        # Reserve inventory
        await self.inventory.reserve_items(cart_items.items)

        return payment

    async def handle_payment_success(self, payment_event):
        # Release inventory reservation
        await self.inventory.confirm_purchase(payment_event.order_id)

        # Create shipment
        await self.shipping.create_shipment(payment_event.order_id)

        # Send confirmation email
        await self.notifications.send_order_confirmation(payment_event)
```

#### SaaS Subscription Flow
```python
class SaaSSubscriptionFlow:
    def __init__(self, provider_config):
        self.provider = provider_config

    async def create_subscription(self, customer, plan):
        # Create customer if doesn't exist
        if not customer.payment_customer_id:
            payment_customer = await self.provider.create_customer(
                email=customer.email,
                metadata={"user_id": str(customer.id)}
            )
            customer.payment_customer_id = payment_customer.id
            await customer.save()

        # Create subscription
        subscription = await self.provider.create_subscription(
            customer_id=customer.payment_customer_id,
            plan_id=plan.payment_plan_id,
            trial_period_days=plan.trial_days,
            proration_behavior='create_prorations'
        )

        return subscription

    async def handle_subscription_event(self, event):
        if event.type == 'invoice.payment_failed':
            await self.dunning.handle_failed_payment(event)
        elif event.type == 'customer.subscription.deleted':
            await self.access.revoke_user_access(event.customer_id)
```

#### Marketplace Split Payment Flow
```python
class MarketplaceSplitFlow:
    def __init__(self, provider_config):
        self.provider = provider_config

    async def create_marketplace_payment(self, order, vendors):
        # Calculate platform fee and vendor splits
        splits = self.calculate_splits(order, vendors)

        # Create payment with destination charges (Stripe Connect)
        payment = await self.provider.create_payment(
            amount=order.total_amount,
            currency=order.currency,
            transfer_group=order.id,
            on_behalf_of=order.primary_vendor.stripe_account_id,
            metadata={
                "order_id": order.id,
                "marketplace_order": True
            }
        )

        # Create transfers to vendors
        for split in splits:
            await self.provider.create_transfer(
                amount=split.amount,
                currency=split.currency,
                destination=split.vendor.stripe_account_id,
                transfer_group=order.id,
                metadata={
                    "vendor_id": split.vendor.id,
                    "order_id": order.id
                }
            )

        return payment
```

### 3. Security and Compliance Patterns

#### PCI DSS Compliance Implementation
```python
class PCICompliantPaymentHandler:
    def __init__(self, compliance_level):
        self.compliance_level = compliance_level

    def handle_card_data(self, card_data):
        if self.compliance_level == "SAQ-A":
            # Never touch card data - use hosted pages
            return self.redirect_to_hosted_page(card_data)
        elif self.compliance_level == "SAQ-D":
            # Can handle card data with full compliance
            encrypted_data = self.encrypt_card_data(card_data)
            return self.process_encrypted_data(encrypted_data)

    def encrypt_card_data(self, card_data):
        # Use strong encryption for card data
        return self.crypto.encrypt_aes_256(card_data, self.encryption_key)

    def tokenize_payment_method(self, payment_method):
        # Replace sensitive data with tokens
        return {
            "token": self.generate_secure_token(),
            "last_four": payment_method.card.last_four,
            "brand": payment_method.card.brand,
            "exp_month": payment_method.card.exp_month,
            "exp_year": payment_method.card.exp_year
        }
```

#### Fraud Detection Implementation
```python
class FraudDetectionEngine:
    def __init__(self, detection_level):
        self.detection_level = detection_level
        self.rules_engine = self.initialize_rules()

    async def analyze_payment(self, payment_data):
        risk_score = 0

        # Basic fraud checks
        if self.detection_level in ["basic", "advanced", "machine_learning"]:
            risk_score += await self.check_velocity_limits(payment_data)
            risk_score += await self.check_geolocation(payment_data)
            risk_score += await self.check_blacklist(payment_data)

        # Advanced fraud checks
        if self.detection_level in ["advanced", "machine_learning"]:
            risk_score += await self.check_device_fingerprint(payment_data)
            risk_score += await self.check_behavioral_patterns(payment_data)
            risk_score += await self.check_network_analysis(payment_data)

        # Machine learning fraud detection
        if self.detection_level == "machine_learning":
            ml_score = await self.ml_fraud_model.predict(payment_data)
            risk_score = (risk_score + ml_score) / 2

        return self.make_fraud_decision(risk_score)

    def make_fraud_decision(self, risk_score):
        if risk_score < 30:
            return {"action": "approve", "risk": "low"}
        elif risk_score < 70:
            return {"action": "review", "risk": "medium"}
        else:
            return {"action": "decline", "risk": "high"}
```

### 4. Webhook Processing Patterns

#### Universal Webhook Handler
```python
class UniversalWebhookHandler:
    def __init__(self, provider_configs):
        self.providers = provider_configs
        self.processors = {
            "stripe": StripeWebhookProcessor(),
            "paypal": PayPalWebhookProcessor(),
            "square": SquareWebhookProcessor()
        }

    async def process_webhook(self, request):
        # Determine provider from headers or payload
        provider = self.detect_provider(request)
        processor = self.processors[provider]

        # Verify webhook signature
        is_valid, event = await processor.verify_signature(
            request.body,
            request.headers
        )

        if not is_valid:
            raise WebhookVerificationError("Invalid signature")

        # Process event idempotently
        await self.process_event_idempotent(event)

        return {"status": "processed"}

    async def process_event_idempotent(self, event):
        # Check if event already processed
        if await self.event_store.is_processed(event.id):
            return

        # Process event
        await self.route_event_to_handler(event)

        # Mark as processed
        await self.event_store.mark_processed(event.id)
```

#### Event-Driven Architecture
```python
class PaymentEventBus:
    def __init__(self):
        self.handlers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self.handlers[event_type].append(handler)

    async def publish(self, event):
        handlers = self.handlers[event.type]

        # Process handlers concurrently
        tasks = [handler(event) for handler in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)

# Usage
event_bus = PaymentEventBus()

# Register handlers
event_bus.subscribe("payment.succeeded", handle_payment_success)
event_bus.subscribe("payment.succeeded", update_analytics)
event_bus.subscribe("payment.succeeded", send_confirmation)

event_bus.subscribe("payment.failed", handle_payment_failure)
event_bus.subscribe("payment.failed", retry_payment)
event_bus.subscribe("payment.failed", notify_customer)
```

### 5. Multi-Currency and Localization

#### Currency Handling Patterns
```python
class CurrencyManager:
    def __init__(self, supported_currencies):
        self.supported_currencies = supported_currencies
        self.exchange_rates = ExchangeRateService()

    async def convert_amount(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount

        rate = await self.exchange_rates.get_rate(from_currency, to_currency)
        converted = Decimal(amount) * Decimal(rate)

        # Round to currency-specific decimal places
        decimal_places = self.get_currency_decimal_places(to_currency)
        return round(converted, decimal_places)

    def format_amount(self, amount, currency, locale):
        """Format amount according to locale conventions."""
        return babel.numbers.format_currency(
            amount, currency, locale=locale
        )

    def get_currency_decimal_places(self, currency):
        # Most currencies use 2 decimal places
        zero_decimal_currencies = ["JPY", "KRW", "VND", "CLP"]
        three_decimal_currencies = ["BHD", "JOD", "KWD", "OMR", "TND"]

        if currency in zero_decimal_currencies:
            return 0
        elif currency in three_decimal_currencies:
            return 3
        else:
            return 2
```

### 6. Testing and Validation Patterns

#### Payment Integration Tests
```python
class PaymentIntegrationTest:
    def __init__(self, provider_config):
        self.provider = provider_config
        self.test_cards = {
            "visa_success": "4242424242424242",
            "visa_declined": "4000000000000002",
            "mastercard_success": "5555555555554444",
            "amex_success": "378282246310005"
        }

    async def test_successful_payment(self):
        payment = await self.provider.create_payment(
            amount=1000,  # $10.00
            currency="usd",
            payment_method_data={
                "type": "card",
                "card": {
                    "number": self.test_cards["visa_success"],
                    "exp_month": 12,
                    "exp_year": 2025,
                    "cvc": "123"
                }
            }
        )

        assert payment.status == "succeeded"
        assert payment.amount == 1000

    async def test_declined_payment(self):
        with pytest.raises(PaymentDeclinedError):
            await self.provider.create_payment(
                amount=1000,
                currency="usd",
                payment_method_data={
                    "type": "card",
                    "card": {
                        "number": self.test_cards["visa_declined"],
                        "exp_month": 12,
                        "exp_year": 2025,
                        "cvc": "123"
                    }
                }
            )

    async def test_webhook_processing(self):
        # Simulate webhook event
        event = self.create_test_webhook_event("payment.succeeded")

        # Process webhook
        result = await self.webhook_handler.process(event)

        assert result.status == "processed"
```

## Специфичные для домена знания

### E-commerce Specific Patterns

#### Shopping Cart Integration
```python
class EcommercePaymentIntegration:
    async def create_checkout_session(self, cart):
        line_items = []
        for item in cart.items:
            line_items.append({
                "price_data": {
                    "currency": cart.currency,
                    "product_data": {
                        "name": item.name,
                        "images": item.images
                    },
                    "unit_amount": int(item.price * 100)
                },
                "quantity": item.quantity
            })

        session = await stripe.checkout.Session.create(
            payment_method_types=["card", "us_bank_account"],
            line_items=line_items,
            mode="payment",
            success_url=self.success_url,
            cancel_url=self.cancel_url,
            shipping_address_collection={"allowed_countries": ["US", "CA"]},
            tax_id_collection={"enabled": True}
        )

        return session
```

### SaaS Specific Patterns

#### Subscription Lifecycle Management
```python
class SaaSSubscriptionManager:
    async def handle_plan_change(self, subscription_id, new_plan_id):
        # Get current subscription
        subscription = await stripe.Subscription.retrieve(subscription_id)

        # Update subscription with proration
        updated_subscription = await stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": subscription.items.data[0].id,
                "plan": new_plan_id
            }],
            proration_behavior="create_prorations"
        )

        return updated_subscription

    async def handle_usage_billing(self, customer_id, usage_data):
        # Report usage for metered billing
        await stripe.UsageRecord.create(
            subscription_item=usage_data.subscription_item_id,
            quantity=usage_data.quantity,
            timestamp=int(time.time()),
            action="set"  # or "increment"
        )
```

### Marketplace Specific Patterns

#### Multi-party Payment Flows
```python
class MarketplacePaymentManager:
    async def onboard_vendor(self, vendor_data):
        # Create Stripe Express account
        account = await stripe.Account.create(
            type="express",
            country=vendor_data.country,
            email=vendor_data.email,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True}
            },
            business_type="individual",
            individual={
                "first_name": vendor_data.first_name,
                "last_name": vendor_data.last_name,
                "email": vendor_data.email
            }
        )

        # Create account link for onboarding
        account_link = await stripe.AccountLink.create(
            account=account.id,
            refresh_url=self.refresh_url,
            return_url=self.return_url,
            type="account_onboarding"
        )

        return account, account_link
```

## Интеграция с проектами

### Framework Integration Examples

#### FastAPI Integration
```python
from fastapi import FastAPI, Request, HTTPException
from payment_integration_agent import PaymentAgentDependencies, get_payment_integration_agent

app = FastAPI()

# Initialize payment agent
payment_deps = PaymentAgentDependencies(
    api_key=os.getenv("STRIPE_SECRET_KEY"),
    payment_provider="stripe",
    business_model="ecommerce"
)

payment_agent = get_payment_integration_agent(payment_deps)

@app.post("/payments")
async def create_payment(payment_request: PaymentRequest):
    try:
        result = await payment_agent.run(
            f"Create payment for {payment_request.amount} {payment_request.currency}",
            deps=payment_deps
        )
        return {"success": True, "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    verification_result = await validate_webhook_event(
        payload.decode(), sig_header, payment_deps
    )

    if verification_result["verified"]:
        # Process the event
        return {"status": "processed"}
    else:
        raise HTTPException(status_code=400, detail="Invalid signature")
```

#### Express.js Integration
```javascript
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const app = express();

app.post('/payments', async (req, res) => {
    try {
        const { amount, currency, payment_method_id } = req.body;

        const paymentIntent = await stripe.paymentIntents.create({
            amount: amount * 100, // Convert to cents
            currency,
            payment_method: payment_method_id,
            confirmation_method: 'manual',
            confirm: true
        });

        res.json({
            success: true,
            client_secret: paymentIntent.client_secret
        });
    } catch (error) {
        res.status(400).json({
            success: false,
            error: error.message
        });
    }
});

app.post('/webhooks/stripe', express.raw({type: 'application/json'}), (req, res) => {
    const sig = req.headers['stripe-signature'];
    let event;

    try {
        event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
    } catch (err) {
        return res.status(400).send(`Webhook signature verification failed.`);
    }

    // Handle the event
    switch (event.type) {
        case 'payment_intent.succeeded':
            // Handle successful payment
            break;
        case 'payment_intent.payment_failed':
            // Handle failed payment
            break;
        default:
            console.log(`Unhandled event type ${event.type}`);
    }

    res.json({received: true});
});
```

### Best Practices и Рекомендации

#### Error Handling
```python
class PaymentErrorHandler:
    def __init__(self):
        self.error_mappings = {
            "card_declined": "Your card was declined. Please try a different payment method.",
            "insufficient_funds": "Insufficient funds. Please check your account balance.",
            "expired_card": "Your card has expired. Please use a different payment method.",
            "processing_error": "We encountered an error processing your payment. Please try again."
        }

    def handle_payment_error(self, error):
        error_code = self.extract_error_code(error)
        user_message = self.error_mappings.get(
            error_code,
            "An unexpected error occurred. Please try again."
        )

        # Log detailed error for debugging
        logger.error(f"Payment error: {error_code}", extra={
            "error": str(error),
            "stack_trace": traceback.format_exc()
        })

        return {
            "success": False,
            "error_code": error_code,
            "message": user_message
        }
```

#### Performance Optimization
```python
class PaymentPerformanceOptimizer:
    def __init__(self):
        self.cache = RedisCache()
        self.circuit_breaker = CircuitBreaker()

    @cached(ttl=300)  # Cache for 5 minutes
    async def get_exchange_rates(self):
        return await self.exchange_rate_service.get_rates()

    @circuit_breaker.protected
    async def process_payment(self, payment_data):
        # Circuit breaker protects against cascading failures
        return await self.payment_provider.create_payment(payment_data)

    async def batch_process_payments(self, payments):
        # Process payments in batches for better performance
        batch_size = 10
        results = []

        for i in range(0, len(payments), batch_size):
            batch = payments[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.process_payment(payment) for payment in batch],
                return_exceptions=True
            )
            results.extend(batch_results)

        return results
```

## Recommended Resources

### Documentation Links
- **Stripe**: https://stripe.com/docs
- **PayPal**: https://developer.paypal.com/docs/
- **Square**: https://developer.squareup.com/docs
- **Razorpay**: https://razorpay.com/docs/
- **Braintree**: https://developers.braintreepayments.com/
- **Adyen**: https://docs.adyen.com/

### Compliance Resources
- **PCI DSS**: https://www.pcisecuritystandards.org/
- **GDPR**: https://gdpr-info.eu/
- **PSD2**: https://ec.europa.eu/info/law/payment-services-psd-2-directive-eu-2015-2366_en

### Testing Resources
- **Stripe Test Cards**: https://stripe.com/docs/testing
- **PayPal Sandbox**: https://developer.paypal.com/docs/api-basics/sandbox/
- **Webhook Testing**: https://webhook.site/