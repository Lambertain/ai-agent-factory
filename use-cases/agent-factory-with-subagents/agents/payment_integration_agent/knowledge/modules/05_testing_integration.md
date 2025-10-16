# Module 05: Testing & Integration Patterns

## Обзор модуля

Этот модуль содержит полные production-ready примеры для:
- **Multi-Currency Support** - конвертация валют, локализация, округление
- **Test Cards and Sandbox** - тестовые карты Stripe/PayPal/Square для различных сценариев
- **Error Handling Patterns** - маппинг ошибок, пользовательские сообщения, логирование
- **Performance Optimization** - Redis caching, circuit breakers, batch processing
- **Framework Integration** - FastAPI и Express.js примеры

---

## 1. Multi-Currency Support

### 1.1 Currency Service с конвертацией и локализацией

```python
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional
import httpx
from datetime import datetime, timedelta
from enum import Enum

class CurrencyCode(str, Enum):
    """Supported currency codes (ISO 4217)."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"
    INR = "INR"
    BRL = "BRL"
    KRW = "KRW"
    BHD = "BHD"  # 3 decimal places
    CLF = "CLF"  # 4 decimal places

class CurrencyService:
    """
    Сервис для multi-currency операций.

    Features:
    - Currency conversion с кэшированием exchange rates
    - Правильное округление для разных валют (0, 2, 3, 4 decimal places)
    - Locale-based formatting
    - Exchange rate refresh каждые 1 час
    """

    # Decimal places для каждой валюты
    CURRENCY_DECIMALS = {
        CurrencyCode.JPY: 0,  # Японская йена - целые числа
        CurrencyCode.KRW: 0,  # Корейская вона - целые числа
        CurrencyCode.BHD: 3,  # Бахрейнский динар - 3 знака
        CurrencyCode.CLF: 4,  # Унидад де фоменто - 4 знака
    }

    # Символы валют для форматирования
    CURRENCY_SYMBOLS = {
        CurrencyCode.USD: "$",
        CurrencyCode.EUR: "€",
        CurrencyCode.GBP: "£",
        CurrencyCode.JPY: "¥",
        CurrencyCode.CNY: "¥",
        CurrencyCode.INR: "₹",
        CurrencyCode.BRL: "R$",
        CurrencyCode.KRW: "₩",
    }

    def __init__(
        self,
        redis_client,
        exchange_rate_api_key: str,
        cache_ttl: int = 3600  # 1 hour
    ):
        self.redis = redis_client
        self.api_key = exchange_rate_api_key
        self.cache_ttl = cache_ttl
        self.base_currency = CurrencyCode.USD

    async def get_exchange_rate(
        self,
        from_currency: CurrencyCode,
        to_currency: CurrencyCode
    ) -> Decimal:
        """
        Получить exchange rate с кэшированием.
        """
        if from_currency == to_currency:
            return Decimal("1.0")

        # Проверка кэша
        cache_key = f"exchange_rate:{from_currency}:{to_currency}"
        cached_rate = await self.redis.get(cache_key)

        if cached_rate:
            return Decimal(cached_rate)

        # Fetch from API (example: exchangerate-api.com)
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency}/{to_currency}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        rate = Decimal(str(data['conversion_rate']))

        # Кэшируем rate
        await self.redis.setex(cache_key, self.cache_ttl, str(rate))

        return rate

    async def convert_amount(
        self,
        amount: Decimal,
        from_currency: CurrencyCode,
        to_currency: CurrencyCode
    ) -> Decimal:
        """
        Конвертировать сумму между валютами.
        """
        rate = await self.get_exchange_rate(from_currency, to_currency)
        converted = amount * rate

        # Правильное округление для целевой валюты
        decimal_places = self.CURRENCY_DECIMALS.get(to_currency, 2)

        if decimal_places == 0:
            # Округление до целого числа (JPY, KRW)
            return converted.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        else:
            # Округление до N знаков после запятой
            quantize_value = Decimal(10) ** -decimal_places
            return converted.quantize(quantize_value, rounding=ROUND_HALF_UP)

    def format_currency(
        self,
        amount: Decimal,
        currency: CurrencyCode,
        locale: str = 'en_US'
    ) -> str:
        """
        Форматировать сумму согласно валюте и локали.

        Examples:
            USD: $1,234.56
            EUR: €1.234,56 (de_DE locale)
            JPY: ¥1,235 (no decimals)
        """
        decimal_places = self.CURRENCY_DECIMALS.get(currency, 2)
        symbol = self.CURRENCY_SYMBOLS.get(currency, currency.value)

        # Locale-specific formatting
        if locale.startswith('de'):
            # German locale: 1.234,56
            thousands_sep = '.'
            decimal_sep = ','
        elif locale.startswith('fr'):
            # French locale: 1 234,56
            thousands_sep = ' '
            decimal_sep = ','
        else:
            # Default (en_US): 1,234.56
            thousands_sep = ','
            decimal_sep = '.'

        # Format number
        if decimal_places == 0:
            formatted_number = f"{int(amount):,}".replace(',', thousands_sep)
        else:
            # Split на целую и дробную части
            integer_part = int(amount)
            decimal_part = amount - integer_part

            formatted_integer = f"{integer_part:,}".replace(',', thousands_sep)
            formatted_decimal = str(decimal_part)[2:2+decimal_places].ljust(decimal_places, '0')

            formatted_number = f"{formatted_integer}{decimal_sep}{formatted_decimal}"

        return f"{symbol}{formatted_number}"

    async def convert_to_cents(
        self,
        amount: Decimal,
        currency: CurrencyCode
    ) -> int:
        """
        Конвертировать в минимальные единицы (cents для USD, kobo для NGN, etc).

        Stripe требует суммы в минимальных единицах:
        - USD: $10.50 → 1050 cents
        - JPY: ¥100 → 100 (no decimals)
        - BHD: 10.500 → 10500 fils (3 decimals)
        """
        decimal_places = self.CURRENCY_DECIMALS.get(currency, 2)
        multiplier = Decimal(10) ** decimal_places

        cents = int(amount * multiplier)
        return cents

    async def convert_from_cents(
        self,
        cents: int,
        currency: CurrencyCode
    ) -> Decimal:
        """
        Конвертировать из минимальных единиц обратно в основную валюту.
        """
        decimal_places = self.CURRENCY_DECIMALS.get(currency, 2)
        divisor = Decimal(10) ** decimal_places

        amount = Decimal(cents) / divisor
        return amount


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
async def example_multi_currency():
    """Пример multi-currency операций."""
    import redis.asyncio as aioredis

    redis_client = await aioredis.from_url("redis://localhost")
    currency_service = CurrencyService(
        redis_client=redis_client,
        exchange_rate_api_key="your_api_key"
    )

    # Конвертация USD → EUR
    usd_amount = Decimal("100.00")
    eur_amount = await currency_service.convert_amount(
        amount=usd_amount,
        from_currency=CurrencyCode.USD,
        to_currency=CurrencyCode.EUR
    )
    print(f"$100.00 USD = €{eur_amount} EUR")

    # Форматирование для разных локалей
    formatted_usd = currency_service.format_currency(usd_amount, CurrencyCode.USD, 'en_US')
    formatted_eur = currency_service.format_currency(eur_amount, CurrencyCode.EUR, 'de_DE')

    print(f"US format: {formatted_usd}")  # $100.00
    print(f"DE format: {formatted_eur}")  # €92,50

    # Конвертация в cents для Stripe
    cents = await currency_service.convert_to_cents(usd_amount, CurrencyCode.USD)
    print(f"$100.00 = {cents} cents")  # 10000

    # JPY (no decimals)
    jpy_amount = Decimal("1000")
    jpy_cents = await currency_service.convert_to_cents(jpy_amount, CurrencyCode.JPY)
    print(f"¥1000 = {jpy_cents} (no conversion)")  # 1000
```

---

## 2. Test Cards and Sandbox Environments

### 2.1 Stripe Test Cards

```python
from typing import Dict, List
from enum import Enum

class StripeTestScenario(str, Enum):
    """Stripe test card scenarios."""
    SUCCESS = "success"
    DECLINED_GENERIC = "declined_generic"
    DECLINED_INSUFFICIENT_FUNDS = "declined_insufficient_funds"
    DECLINED_LOST_CARD = "declined_lost_card"
    DECLINED_STOLEN_CARD = "declined_stolen_card"
    EXPIRED_CARD = "expired_card"
    INCORRECT_CVC = "incorrect_cvc"
    PROCESSING_ERROR = "processing_error"
    INCORRECT_NUMBER = "incorrect_number"
    REQUIRE_3DS = "require_3ds"
    CHARGE_DISPUTES = "charge_disputes"

class StripeTestCards:
    """
    Stripe test card numbers для различных сценариев.

    Документация: https://stripe.com/docs/testing
    """

    CARDS: Dict[StripeTestScenario, Dict] = {
        # Успешные платежи
        StripeTestScenario.SUCCESS: {
            "number": "4242424242424242",
            "brand": "Visa",
            "description": "Любые CVC, любая будущая дата истечения",
            "outcome": "Payment succeeds"
        },

        # Отклонения карты
        StripeTestScenario.DECLINED_GENERIC: {
            "number": "4000000000000002",
            "brand": "Visa",
            "description": "Generic decline",
            "outcome": "Payment fails with generic_decline code"
        },
        StripeTestScenario.DECLINED_INSUFFICIENT_FUNDS: {
            "number": "4000000000009995",
            "brand": "Visa",
            "description": "Insufficient funds",
            "outcome": "Payment fails with insufficient_funds code"
        },
        StripeTestScenario.DECLINED_LOST_CARD: {
            "number": "4000000000009987",
            "brand": "Visa",
            "description": "Lost card",
            "outcome": "Payment fails with lost_card code"
        },
        StripeTestScenario.DECLINED_STOLEN_CARD: {
            "number": "4000000000009979",
            "brand": "Visa",
            "description": "Stolen card",
            "outcome": "Payment fails with stolen_card code"
        },

        # Ошибки валидации
        StripeTestScenario.EXPIRED_CARD: {
            "number": "4000000000000069",
            "brand": "Visa",
            "description": "Expired card",
            "outcome": "Payment fails with expired_card code"
        },
        StripeTestScenario.INCORRECT_CVC: {
            "number": "4000000000000127",
            "brand": "Visa",
            "description": "Incorrect CVC",
            "outcome": "Payment fails with incorrect_cvc code"
        },

        # Ошибки обработки
        StripeTestScenario.PROCESSING_ERROR: {
            "number": "4000000000000119",
            "brand": "Visa",
            "description": "Processing error",
            "outcome": "Payment fails with processing_error code"
        },

        # 3D Secure
        StripeTestScenario.REQUIRE_3DS: {
            "number": "4000002500003155",
            "brand": "Visa",
            "description": "Requires 3D Secure authentication",
            "outcome": "Payment requires authentication"
        },

        # Disputes
        StripeTestScenario.CHARGE_DISPUTES: {
            "number": "4000000000000259",
            "brand": "Visa",
            "description": "Charge will be disputed",
            "outcome": "Payment succeeds but will be disputed as fraudulent"
        }
    }

    # Card brands для тестирования
    CARD_BRANDS = {
        "visa": "4242424242424242",
        "mastercard": "5555555555554444",
        "amex": "378282246310005",
        "discover": "6011111111111117",
        "diners": "3056930009020004",
        "jcb": "3566002020360505",
        "unionpay": "6200000000000005"
    }

    @classmethod
    def get_card(cls, scenario: StripeTestScenario) -> Dict:
        """Получить test card для сценария."""
        return cls.CARDS[scenario]

    @classmethod
    def get_card_by_brand(cls, brand: str) -> str:
        """Получить test card number для бренда."""
        return cls.CARD_BRANDS.get(brand.lower())


# ПРИМЕР ИСПОЛЬЗОВАНИЯ В ТЕСТАХ
async def test_stripe_declined_insufficient_funds():
    """Test Stripe payment с insufficient funds card."""
    test_card = StripeTestCards.get_card(
        StripeTestScenario.DECLINED_INSUFFICIENT_FUNDS
    )

    # Create payment intent с test card
    try:
        payment_intent = await stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            payment_method_data={
                'type': 'card',
                'card': {
                    'number': test_card['number'],
                    'exp_month': 12,
                    'exp_year': 2025,
                    'cvc': '123'
                }
            },
            confirm=True
        )
        assert False, "Payment should have failed"
    except stripe.error.CardError as e:
        # Expected behavior
        assert e.code == 'insufficient_funds'
        print(f"✓ Test passed: {e.user_message}")
```

### 2.2 PayPal Sandbox Configuration

```python
from typing import Dict
import os

class PayPalSandboxConfig:
    """
    PayPal Sandbox configuration для тестирования.

    Документация: https://developer.paypal.com/tools/sandbox/
    """

    # Sandbox API endpoints
    SANDBOX_API_URL = "https://api-m.sandbox.paypal.com"
    SANDBOX_WEB_URL = "https://www.sandbox.paypal.com"

    # Test accounts credentials (создай на developer.paypal.com)
    TEST_BUYER_CREDENTIALS = {
        "email": os.getenv("PAYPAL_SANDBOX_BUYER_EMAIL", "buyer@example.com"),
        "password": os.getenv("PAYPAL_SANDBOX_BUYER_PASSWORD", "test123")
    }

    TEST_SELLER_CREDENTIALS = {
        "email": os.getenv("PAYPAL_SANDBOX_SELLER_EMAIL", "seller@example.com"),
        "password": os.getenv("PAYPAL_SANDBOX_SELLER_PASSWORD", "test123")
    }

    # Test credit card numbers (в sandbox режиме)
    TEST_CREDIT_CARDS = {
        "visa": {
            "number": "4032039963220896",
            "cvv": "123",
            "exp_month": "12",
            "exp_year": "2025",
            "type": "visa"
        },
        "mastercard": {
            "number": "5425233430109903",
            "cvv": "123",
            "exp_month": "12",
            "exp_year": "2025",
            "type": "mastercard"
        }
    }

    @classmethod
    def get_sandbox_config(cls) -> Dict:
        """Get sandbox configuration."""
        return {
            "client_id": os.getenv("PAYPAL_SANDBOX_CLIENT_ID"),
            "client_secret": os.getenv("PAYPAL_SANDBOX_CLIENT_SECRET"),
            "mode": "sandbox",  # Important!
            "api_url": cls.SANDBOX_API_URL
        }

    @classmethod
    def is_sandbox_mode(cls) -> bool:
        """Check if running in sandbox mode."""
        return os.getenv("PAYPAL_MODE", "sandbox") == "sandbox"


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
async def test_paypal_sandbox_order():
    """Test PayPal order creation в sandbox."""
    config = PayPalSandboxConfig.get_sandbox_config()

    # Create PayPal service в sandbox режиме
    paypal = PayPalPaymentService(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        mode='sandbox'
    )

    # Create order
    order = await paypal.create_order(
        amount=Decimal("10.00"),
        currency='USD'
    )

    print(f"Sandbox order created: {order['order_id']}")
    print(f"Approval URL: {order['approval_url']}")

    # В тестах можно автоматически approve через API
    # или manually через approval_url с test buyer account
```

### 2.3 Square Sandbox Setup

```python
from typing import Dict
import os

class SquareSandboxConfig:
    """
    Square Sandbox configuration для тестирования.

    Документация: https://developer.squareup.com/docs/testing/test-values
    """

    # Sandbox API endpoint
    SANDBOX_API_URL = "https://connect.squareupsandbox.com"

    # Test credit card numbers (nonce tokens для sandbox)
    TEST_CARD_NONCES = {
        "visa_success": "cnon:card-nonce-ok",
        "mastercard_success": "cnon:card-nonce-ok",
        "declined": "cnon:card-nonce-declined",
        "errors": "cnon:card-nonce-errors",
        "address_verification_fail": "cnon:card-nonce-address-verification-failed",
        "cvv_fail": "cnon:card-nonce-cvv-failure"
    }

    # Test amounts для различных сценариев (в cents)
    TEST_AMOUNTS = {
        "success": 100,  # $1.00 - success
        "card_declined": 200,  # $2.00 - card declined
        "invalid_expiration": 300,  # $3.00 - invalid expiration
        "invalid_cvv": 400,  # $4.00 - CVV failure
        "avs_failure": 500,  # $5.00 - AVS failure
        "processor_declined": 5001  # $50.01 - processor declined
    }

    @classmethod
    def get_sandbox_config(cls) -> Dict:
        """Get sandbox configuration."""
        return {
            "access_token": os.getenv("SQUARE_SANDBOX_ACCESS_TOKEN"),
            "location_id": os.getenv("SQUARE_SANDBOX_LOCATION_ID"),
            "environment": "sandbox",
            "api_url": cls.SANDBOX_API_URL
        }

    @classmethod
    def get_test_card_nonce(cls, scenario: str) -> str:
        """Get test card nonce для сценария."""
        return cls.TEST_CARD_NONCES.get(scenario, cls.TEST_CARD_NONCES['visa_success'])


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
async def test_square_sandbox_payment():
    """Test Square payment в sandbox с test nonce."""
    config = SquareSandboxConfig.get_sandbox_config()

    square = SquarePaymentService(
        access_token=config['access_token'],
        location_id=config['location_id'],
        environment='sandbox'
    )

    # Test successful payment
    nonce = SquareSandboxConfig.get_test_card_nonce('visa_success')

    payment = await square.create_payment(
        amount=Decimal("10.00"),
        currency='USD',
        source_id=nonce  # Test nonce вместо реальной карты
    )

    print(f"Sandbox payment created: {payment['id']}")
    assert payment['status'] == 'COMPLETED'
```

---

## 3. Error Handling Patterns

### 3.1 Unified Error Handler с user-friendly messages

```python
from typing import Dict, Optional
import logging
from enum import Enum

class PaymentErrorCode(str, Enum):
    """Unified payment error codes."""
    # Card errors
    CARD_DECLINED = "card_declined"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    EXPIRED_CARD = "expired_card"
    INCORRECT_CVC = "incorrect_cvc"
    INCORRECT_ZIP = "incorrect_zip"
    LOST_CARD = "lost_card"
    STOLEN_CARD = "stolen_card"

    # Processing errors
    PROCESSING_ERROR = "processing_error"
    RATE_LIMIT = "rate_limit"
    API_ERROR = "api_error"

    # Validation errors
    INVALID_AMOUNT = "invalid_amount"
    INVALID_CURRENCY = "invalid_currency"
    MISSING_PAYMENT_METHOD = "missing_payment_method"

    # Authentication errors
    AUTHENTICATION_REQUIRED = "authentication_required"
    AUTHENTICATION_FAILED = "authentication_failed"

class PaymentErrorHandler:
    """
    Unified error handler для всех payment providers.

    Конвертирует provider-specific errors в unified error codes
    и user-friendly messages.
    """

    # Маппинг Stripe error codes → unified codes
    STRIPE_ERROR_MAPPING = {
        "card_declined": PaymentErrorCode.CARD_DECLINED,
        "insufficient_funds": PaymentErrorCode.INSUFFICIENT_FUNDS,
        "expired_card": PaymentErrorCode.EXPIRED_CARD,
        "incorrect_cvc": PaymentErrorCode.INCORRECT_CVC,
        "incorrect_zip": PaymentErrorCode.INCORRECT_ZIP,
        "lost_card": PaymentErrorCode.LOST_CARD,
        "stolen_card": PaymentErrorCode.STOLEN_CARD,
        "processing_error": PaymentErrorCode.PROCESSING_ERROR,
        "rate_limit": PaymentErrorCode.RATE_LIMIT
    }

    # Маппинг PayPal error names → unified codes
    PAYPAL_ERROR_MAPPING = {
        "INSTRUMENT_DECLINED": PaymentErrorCode.CARD_DECLINED,
        "INSUFFICIENT_FUNDS": PaymentErrorCode.INSUFFICIENT_FUNDS,
        "INVALID_RESOURCE_ID": PaymentErrorCode.API_ERROR,
        "UNPROCESSABLE_ENTITY": PaymentErrorCode.PROCESSING_ERROR
    }

    # User-friendly messages для каждого error code
    USER_MESSAGES = {
        PaymentErrorCode.CARD_DECLINED: "Ваша карта была отклонена. Пожалуйста, попробуйте другую карту или свяжитесь с банком.",
        PaymentErrorCode.INSUFFICIENT_FUNDS: "На карте недостаточно средств. Пожалуйста, используйте другую карту.",
        PaymentErrorCode.EXPIRED_CARD: "Срок действия карты истек. Пожалуйста, используйте другую карту.",
        PaymentErrorCode.INCORRECT_CVC: "Неверный код безопасности (CVC/CVV). Проверьте данные и попробуйте снова.",
        PaymentErrorCode.INCORRECT_ZIP: "Неверный почтовый индекс. Проверьте данные и попробуйте снова.",
        PaymentErrorCode.LOST_CARD: "Эта карта была заявлена как утерянная. Пожалуйста, используйте другую карту.",
        PaymentErrorCode.STOLEN_CARD: "Эта карта была заявлена как украденная. Пожалуйста, используйте другую карту.",
        PaymentErrorCode.PROCESSING_ERROR: "Произошла ошибка при обработке платежа. Попробуйте еще раз через несколько минут.",
        PaymentErrorCode.RATE_LIMIT: "Слишком много попыток. Пожалуйста, подождите несколько минут и попробуйте снова.",
        PaymentErrorCode.API_ERROR: "Временная ошибка сервиса. Мы уже работаем над решением. Попробуйте позже.",
        PaymentErrorCode.AUTHENTICATION_REQUIRED: "Требуется дополнительная аутентификация (3D Secure). Следуйте инструкциям.",
        PaymentErrorCode.AUTHENTICATION_FAILED: "Аутентификация не удалась. Проверьте данные или используйте другую карту."
    }

    # Technical messages для логов (detailed)
    TECHNICAL_MESSAGES = {
        PaymentErrorCode.CARD_DECLINED: "Card declined by issuer. Decline code: {decline_code}",
        PaymentErrorCode.INSUFFICIENT_FUNDS: "Insufficient funds on card",
        PaymentErrorCode.PROCESSING_ERROR: "Payment processing error: {details}",
        PaymentErrorCode.API_ERROR: "API error from {provider}: {error_message}"
    }

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def handle_stripe_error(self, error: Exception) -> Dict:
        """
        Обработать Stripe error.
        """
        import stripe

        if isinstance(error, stripe.error.CardError):
            # Card was declined
            code = error.code
            unified_code = self.STRIPE_ERROR_MAPPING.get(code, PaymentErrorCode.CARD_DECLINED)

            # Логируем technical details
            self.logger.error(
                f"Stripe CardError: {code}",
                extra={
                    "decline_code": error.decline_code,
                    "charge_id": error.json_body.get('error', {}).get('charge')
                }
            )

            return {
                "error_code": unified_code,
                "user_message": self.USER_MESSAGES[unified_code],
                "provider": "stripe",
                "provider_code": code,
                "decline_code": error.decline_code
            }

        elif isinstance(error, stripe.error.RateLimitError):
            self.logger.warning("Stripe rate limit exceeded")
            return {
                "error_code": PaymentErrorCode.RATE_LIMIT,
                "user_message": self.USER_MESSAGES[PaymentErrorCode.RATE_LIMIT],
                "provider": "stripe"
            }

        elif isinstance(error, stripe.error.InvalidRequestError):
            self.logger.error(f"Stripe invalid request: {error.user_message}")
            return {
                "error_code": PaymentErrorCode.API_ERROR,
                "user_message": "Ошибка в параметрах платежа. Свяжитесь с поддержкой.",
                "provider": "stripe",
                "details": str(error)
            }

        else:
            # Generic Stripe error
            self.logger.error(f"Stripe error: {str(error)}")
            return {
                "error_code": PaymentErrorCode.PROCESSING_ERROR,
                "user_message": self.USER_MESSAGES[PaymentErrorCode.PROCESSING_ERROR],
                "provider": "stripe",
                "details": str(error)
            }

    def handle_paypal_error(self, error: Dict) -> Dict:
        """
        Обработать PayPal error response.

        PayPal errors structure:
        {
            "name": "UNPROCESSABLE_ENTITY",
            "details": [...],
            "message": "..."
        }
        """
        error_name = error.get('name', 'UNKNOWN_ERROR')
        unified_code = self.PAYPAL_ERROR_MAPPING.get(
            error_name,
            PaymentErrorCode.PROCESSING_ERROR
        )

        # Логируем technical details
        self.logger.error(
            f"PayPal error: {error_name}",
            extra={"details": error.get('details', [])}
        )

        return {
            "error_code": unified_code,
            "user_message": self.USER_MESSAGES[unified_code],
            "provider": "paypal",
            "provider_error_name": error_name,
            "details": error.get('message')
        }

    def handle_generic_error(self, error: Exception, provider: str) -> Dict:
        """
        Обработать generic error.
        """
        self.logger.error(
            f"Payment error from {provider}: {str(error)}",
            exc_info=True
        )

        return {
            "error_code": PaymentErrorCode.PROCESSING_ERROR,
            "user_message": self.USER_MESSAGES[PaymentErrorCode.PROCESSING_ERROR],
            "provider": provider,
            "details": str(error)
        }


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
async def process_payment_with_error_handling(
    payment_service,
    amount: Decimal,
    currency: str,
    payment_method: str
):
    """Пример payment processing с unified error handling."""
    error_handler = PaymentErrorHandler()

    try:
        result = await payment_service.create_payment(
            amount=amount,
            currency=currency,
            payment_method_id=payment_method
        )
        return {"success": True, "payment_id": result['id']}

    except Exception as error:
        # Determine provider type
        provider = payment_service.__class__.__name__.lower()

        if 'stripe' in provider:
            error_info = error_handler.handle_stripe_error(error)
        elif 'paypal' in provider:
            error_info = error_handler.handle_paypal_error(error.response.json())
        else:
            error_info = error_handler.handle_generic_error(error, provider)

        # Возвращаем user-friendly error
        return {
            "success": False,
            "error": error_info
        }
```

---

## 4. Performance Optimization

### 4.1 Redis Caching для exchange rates и payment metadata

```python
from typing import Optional, Dict, Any
import json
from functools import wraps
import hashlib

class PaymentCacheService:
    """
    Redis caching service для payment operations.

    Кэширует:
    - Exchange rates (TTL: 1 hour)
    - Customer data (TTL: 5 minutes)
    - Payment metadata (TTL: 10 minutes)
    """

    def __init__(self, redis_client, default_ttl: int = 300):
        self.redis = redis_client
        self.default_ttl = default_ttl

    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from prefix and parameters."""
        params_str = json.dumps(kwargs, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
        return f"{prefix}:{params_hash}"

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached value with TTL."""
        ttl = ttl or self.default_ttl
        await self.redis.setex(key, ttl, json.dumps(value))

    async def invalidate(self, pattern: str):
        """Invalidate all keys matching pattern."""
        cursor = 0
        while True:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)
            if keys:
                await self.redis.delete(*keys)
            if cursor == 0:
                break


def cache_payment_result(ttl: int = 300):
    """
    Decorator для кэширования payment results.

    Usage:
        @cache_payment_result(ttl=600)
        async def get_customer_payment_methods(customer_id: str):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Generate cache key
            cache_key = f"payment:{func.__name__}:{args}:{kwargs}"

            # Check cache
            if hasattr(self, 'cache'):
                cached_result = await self.cache.get(cache_key)
                if cached_result:
                    return cached_result

            # Execute function
            result = await func(self, *args, **kwargs)

            # Store in cache
            if hasattr(self, 'cache'):
                await self.cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
class CachedPaymentService:
    """Payment service с Redis caching."""

    def __init__(self, redis_client, stripe_service):
        self.cache = PaymentCacheService(redis_client)
        self.stripe = stripe_service

    @cache_payment_result(ttl=300)
    async def get_customer_payment_methods(self, customer_id: str) -> List[Dict]:
        """
        Получить payment methods клиента с кэшированием.

        Cache TTL: 5 minutes
        """
        payment_methods = await self.stripe.list_customer_payment_methods(customer_id)
        return payment_methods

    async def invalidate_customer_cache(self, customer_id: str):
        """Invalidate cache при добавлении/удалении payment method."""
        await self.cache.invalidate(f"payment:get_customer_payment_methods:*{customer_id}*")
```

### 4.2 Circuit Breaker для external payment APIs

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import asyncio

class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker pattern для payment APIs.

    Предотвращает cascade failures при недоступности payment provider.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests blocked immediately
    - HALF_OPEN: Testing recovery, limited requests allowed
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # seconds
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        """
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout passed
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception(f"Circuit breaker is OPEN. Service unavailable.")

        try:
            result = await func(*args, **kwargs)

            # Success - reset circuit
            if self.state == CircuitState.HALF_OPEN:
                self._reset()

            return result

        except self.expected_exception as e:
            # Failure - record and potentially open circuit
            self._record_failure()
            raise e

    def _record_failure(self):
        """Record failure and open circuit if threshold exceeded."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if enough time passed to attempt recovery."""
        if not self.last_failure_time:
            return False

        time_since_failure = datetime.utcnow() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout

    def _reset(self):
        """Reset circuit to CLOSED state."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
class ResilientPaymentService:
    """Payment service с circuit breaker protection."""

    def __init__(self, stripe_service):
        self.stripe = stripe_service
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
            expected_exception=Exception
        )

    async def create_payment_with_protection(
        self,
        amount: Decimal,
        currency: str,
        payment_method_id: str
    ) -> Dict:
        """
        Create payment с circuit breaker protection.
        """
        try:
            result = await self.circuit_breaker.call(
                self.stripe.create_payment_intent,
                amount=amount,
                currency=currency,
                payment_method_id=payment_method_id
            )
            return {"success": True, "payment": result}

        except Exception as e:
            if "Circuit breaker is OPEN" in str(e):
                # Fallback to alternative provider
                return await self._fallback_payment_provider(amount, currency, payment_method_id)
            raise e

    async def _fallback_payment_provider(self, amount, currency, payment_method_id):
        """Fallback to alternative provider when Stripe is down."""
        # Implement PayPal/Square fallback
        pass
```

### 4.3 Batch Processing для webhooks

```python
from typing import List, Dict
import asyncio
from collections import defaultdict

class WebhookBatchProcessor:
    """
    Batch processing для payment webhooks.

    Группирует webhooks по типу и обрабатывает batch-ами
    для уменьшения DB queries.
    """

    def __init__(
        self,
        batch_size: int = 50,
        flush_interval: int = 5  # seconds
    ):
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        # Группировка webhooks по типу события
        self.batches: Dict[str, List[Dict]] = defaultdict(list)

        # Background task для auto-flush
        self._flush_task = None

    async def add_webhook(self, event_type: str, webhook_data: Dict):
        """
        Добавить webhook в batch.
        """
        self.batches[event_type].append(webhook_data)

        # Flush если batch заполнен
        if len(self.batches[event_type]) >= self.batch_size:
            await self._flush_batch(event_type)

    async def _flush_batch(self, event_type: str):
        """
        Обработать batch webhooks определенного типа.
        """
        if not self.batches[event_type]:
            return

        batch = self.batches[event_type]
        self.batches[event_type] = []

        # Batch processing based on event type
        if event_type == 'payment_intent.succeeded':
            await self._process_successful_payments_batch(batch)
        elif event_type == 'payment_intent.payment_failed':
            await self._process_failed_payments_batch(batch)
        elif event_type == 'customer.subscription.updated':
            await self._process_subscription_updates_batch(batch)

    async def _process_successful_payments_batch(self, batch: List[Dict]):
        """
        Обработать batch успешных платежей.

        Single DB query для всех payment_intent_ids.
        """
        payment_intent_ids = [event['data']['object']['id'] for event in batch]

        # Bulk update в БД (1 query вместо N)
        await self.db.payments.bulk_update_status(
            payment_intent_ids=payment_intent_ids,
            status='succeeded'
        )

        # Bulk email notifications
        customer_emails = [event['data']['object']['receipt_email'] for event in batch]
        await self.email_service.send_bulk_receipts(customer_emails, batch)

    async def _process_failed_payments_batch(self, batch: List[Dict]):
        """Batch processing неудачных платежей."""
        payment_intent_ids = [event['data']['object']['id'] for event in batch]

        await self.db.payments.bulk_update_status(
            payment_intent_ids=payment_intent_ids,
            status='failed'
        )

        # Bulk dunning notifications
        await self.dunning_service.schedule_retries_batch(batch)

    async def _process_subscription_updates_batch(self, batch: List[Dict]):
        """Batch processing subscription updates."""
        subscription_ids = [event['data']['object']['id'] for event in batch]

        await self.db.subscriptions.bulk_sync_from_stripe(subscription_ids)

    async def start_auto_flush(self):
        """Start background task для периодического flush."""
        async def auto_flush_loop():
            while True:
                await asyncio.sleep(self.flush_interval)
                for event_type in list(self.batches.keys()):
                    await self._flush_batch(event_type)

        self._flush_task = asyncio.create_task(auto_flush_loop())

    async def stop_auto_flush(self):
        """Stop background task."""
        if self._flush_task:
            self._flush_task.cancel()


# ПРИМЕР ИСПОЛЬЗОВАНИЯ
webhook_processor = WebhookBatchProcessor(batch_size=50, flush_interval=5)
await webhook_processor.start_auto_flush()

# При получении webhook
await webhook_processor.add_webhook(
    event_type='payment_intent.succeeded',
    webhook_data=stripe_event
)
```

---

## 5. Framework Integration Examples

### 5.1 FastAPI Integration

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
import stripe

app = FastAPI(title="Payment API", version="1.0.0")

# Pydantic models
class CreatePaymentRequest(BaseModel):
    """Request model для создания платежа."""
    amount: Decimal = Field(..., gt=0, description="Amount in main currency units")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code")
    payment_method_id: str = Field(..., description="Stripe payment method ID")
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict] = Field(default_factory=dict)

class CreatePaymentResponse(BaseModel):
    """Response model для создания платежа."""
    success: bool
    payment_intent_id: str
    status: str
    client_secret: Optional[str] = None

# Dependency для Stripe service
def get_stripe_service() -> StripePaymentService:
    """Dependency injection для Stripe service."""
    return StripePaymentService(api_key=os.getenv("STRIPE_SECRET_KEY"))

# Exception handler для payment errors
@app.exception_handler(PaymentError)
async def payment_error_handler(request, exc: PaymentError):
    """Global handler для payment errors."""
    error_handler = PaymentErrorHandler()
    error_info = error_handler.handle_stripe_error(exc)

    return JSONResponse(
        status_code=400,
        content={
            "error": error_info['error_code'],
            "message": error_info['user_message']
        }
    )

# Endpoints
@app.post("/payments", response_model=CreatePaymentResponse)
async def create_payment(
    request: CreatePaymentRequest,
    stripe_service: StripePaymentService = Depends(get_stripe_service)
):
    """
    Создать новый платеж.

    Requires:
    - amount: Сумма в основных единицах валюты (напр. 10.50 для $10.50)
    - currency: ISO 4217 код валюты (USD, EUR, etc)
    - payment_method_id: Stripe payment method ID (получен через Stripe.js)
    """
    try:
        payment_intent = await stripe_service.create_payment_intent(
            amount=request.amount,
            currency=request.currency,
            payment_method_id=request.payment_method_id,
            description=request.description,
            metadata=request.metadata
        )

        return CreatePaymentResponse(
            success=True,
            payment_intent_id=payment_intent.id,
            status=payment_intent.status,
            client_secret=payment_intent.client_secret
        )

    except PaymentError as e:
        # Handled by global exception handler
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/webhooks/stripe")
async def stripe_webhook(
    payload: bytes = Body(...),
    stripe_signature: str = Header(..., alias="Stripe-Signature"),
    webhook_handler: StripeWebhookHandler = Depends(get_webhook_handler)
):
    """
    Stripe webhook endpoint.

    Обрабатывает события от Stripe:
    - payment_intent.succeeded
    - payment_intent.payment_failed
    - customer.subscription.updated
    - etc.
    """
    try:
        # Verify signature
        event = await webhook_handler.verify_signature(payload, stripe_signature)

        # Process event
        result = await webhook_handler.handle_event(event)

        return {"received": True}

    except WebhookSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Webhook processing error")

# Healthcheck
@app.get("/health")
async def health_check():
    """Healthcheck endpoint."""
    return {"status": "healthy", "service": "payment-api"}
```

### 5.2 Express.js Integration (TypeScript)

```typescript
import express, { Request, Response, NextFunction } from 'express';
import Stripe from 'stripe';
import { body, validationResult } from 'express-validator';

const app = express();
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16'
});

// Middleware для JSON body parsing
app.use(express.json());

// Middleware для error handling
interface PaymentError extends Error {
  code?: string;
  statusCode?: number;
}

const errorHandler = (
  err: PaymentError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error('Payment error:', err);

  if (err.code === 'card_declined') {
    return res.status(400).json({
      error: 'card_declined',
      message: 'Ваша карта была отклонена. Попробуйте другую карту.'
    });
  }

  res.status(err.statusCode || 500).json({
    error: 'payment_error',
    message: 'Произошла ошибка при обработке платежа.'
  });
};

// Routes
app.post(
  '/api/payments',
  [
    body('amount').isFloat({ gt: 0 }),
    body('currency').isLength({ min: 3, max: 3 }),
    body('payment_method_id').notEmpty()
  ],
  async (req: Request, res: Response, next: NextFunction) => {
    // Validation
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { amount, currency, payment_method_id } = req.body;

    try {
      // Create payment intent
      const paymentIntent = await stripe.paymentIntents.create({
        amount: Math.round(amount * 100), // Convert to cents
        currency: currency.toLowerCase(),
        payment_method: payment_method_id,
        confirm: true,
        automatic_payment_methods: {
          enabled: true,
          allow_redirects: 'never'
        }
      });

      res.json({
        success: true,
        payment_intent_id: paymentIntent.id,
        status: paymentIntent.status
      });
    } catch (error) {
      next(error);
    }
  }
);

// Stripe webhook endpoint
app.post(
  '/api/webhooks/stripe',
  express.raw({ type: 'application/json' }),
  async (req: Request, res: Response, next: NextFunction) => {
    const sig = req.headers['stripe-signature'] as string;
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

    let event: Stripe.Event;

    try {
      // Verify signature
      event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
    } catch (err) {
      console.error('Webhook signature verification failed:', err);
      return res.status(400).send('Webhook signature verification failed');
    }

    // Handle event
    switch (event.type) {
      case 'payment_intent.succeeded':
        const paymentIntent = event.data.object as Stripe.PaymentIntent;
        console.log(`Payment succeeded: ${paymentIntent.id}`);
        // Update database, send receipt email, etc.
        break;

      case 'payment_intent.payment_failed':
        const failedPayment = event.data.object as Stripe.PaymentIntent;
        console.error(`Payment failed: ${failedPayment.id}`);
        // Handle dunning, notify customer, etc.
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    res.json({ received: true });
  }
);

// Error handling middleware (должен быть последним)
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Payment API running on port ${PORT}`);
});
```

---

## Итоговая архитектура Integration Layer

```
┌─────────────────────────────────────────────────────────┐
│              Frontend (React/Vue/Angular)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Stripe.js   │  │  PayPal SDK  │  │  Square SDK  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 Backend API (FastAPI)                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Payment Router (Multi-Provider)          │  │
│  │   ┌────────┐  ┌────────┐  ┌────────┐             │  │
│  │   │ Stripe │  │ PayPal │  │ Square │             │  │
│  │   └────────┘  └────────┘  └────────┘             │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Error Handler (Unified Errors)           │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Currency Service (Multi-Currency)           │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Circuit Breaker (Resilience Protection)        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Redis Cache Layer                      │
│  • Exchange rates (TTL: 1h)                             │
│  • Customer data (TTL: 5m)                              │
│  • Payment metadata (TTL: 10m)                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Database (PostgreSQL)                     │
│  • Payments                                             │
│  • Customers                                            │
│  • Subscriptions                                        │
│  • Payment methods                                      │
└─────────────────────────────────────────────────────────┘
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Implementation Engineer
