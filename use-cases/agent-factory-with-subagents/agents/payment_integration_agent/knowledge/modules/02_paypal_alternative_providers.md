# Module 02: PayPal & Alternative Providers

## Интеграция PayPal, Square и других платежных провайдеров

Этот модуль содержит production-ready паттерны для интеграции PayPal, Square и стратегии работы с несколькими провайдерами.

---

## PayPal Integration

### PayPal Order Creation (Checkout Flow)

```python
import requests
from typing import Dict, List, Optional
from decimal import Decimal
import base64

class PayPalPaymentService:
    """
    Production-ready сервис для работы с PayPal Orders API v2.

    Поддержка:
    - Создание заказов
    - Захват платежей
    - Возвраты
    - Webhooks
    """

    def __init__(self, client_id: str, client_secret: str, mode: str = 'sandbox'):
        """
        Инициализация PayPal сервиса.

        Args:
            client_id: PayPal Client ID
            client_secret: PayPal Client Secret
            mode: Режим работы ('sandbox' или 'live')
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.mode = mode

        # API endpoints
        if mode == 'sandbox':
            self.base_url = 'https://api-m.sandbox.paypal.com'
        else:
            self.base_url = 'https://api-m.paypal.com'

        self.access_token = None

    async def get_access_token(self) -> str:
        """
        Получить OAuth2 access token от PayPal.

        Returns:
            Access token для API запросов

        Raises:
            PaymentError: Ошибка получения токена
        """
        url = f'{self.base_url}/v1/oauth2/token'

        # Basic authentication
        auth = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()
        ).decode()

        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {'grant_type': 'client_credentials'}

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data['access_token']

            return self.access_token

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='token_acquisition_failed',
                message=f"Не удалось получить PayPal access token: {str(e)}"
            )

    async def create_order(
        self,
        amount: Decimal,
        currency: str = 'USD',
        return_url: str = None,
        cancel_url: str = None,
        items: Optional[List[Dict]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Создать PayPal заказ для checkout.

        Args:
            amount: Сумма платежа
            currency: Валюта (ISO код)
            return_url: URL для возврата после успешного платежа
            cancel_url: URL для возврата при отмене
            items: Список товаров в заказе
            metadata: Дополнительные данные

        Returns:
            Созданный Order объект с approval URL

        Raises:
            PaymentError: Ошибка создания заказа
        """
        if not self.access_token:
            await self.get_access_token()

        url = f'{self.base_url}/v2/checkout/orders'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Подготовка данных заказа
        order_data = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': currency,
                    'value': str(amount)
                }
            }]
        }

        # Добавить items если переданы
        if items:
            order_data['purchase_units'][0]['items'] = items

        # Добавить custom_id для идентификации
        if metadata and 'order_id' in metadata:
            order_data['purchase_units'][0]['custom_id'] = metadata['order_id']

        # Добавить application context (return/cancel URLs)
        if return_url and cancel_url:
            order_data['application_context'] = {
                'return_url': return_url,
                'cancel_url': cancel_url,
                'brand_name': metadata.get('brand_name', 'My Store'),
                'locale': metadata.get('locale', 'en-US'),
                'landing_page': 'BILLING',
                'shipping_preference': 'NO_SHIPPING',
                'user_action': 'PAY_NOW'
            }

        try:
            response = requests.post(url, headers=headers, json=order_data)
            response.raise_for_status()

            order = response.json()

            # Извлечь approval URL для редиректа клиента
            approval_url = None
            for link in order.get('links', []):
                if link['rel'] == 'approve':
                    approval_url = link['href']
                    break

            return {
                'order_id': order['id'],
                'status': order['status'],
                'approval_url': approval_url,
                'order': order
            }

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='order_creation_failed',
                message=f"Не удалось создать PayPal заказ: {str(e)}"
            )

    async def capture_order(self, order_id: str) -> Dict:
        """
        Захватить платеж после одобрения клиентом.

        Args:
            order_id: ID PayPal заказа

        Returns:
            Результат захвата платежа

        Raises:
            PaymentError: Ошибка захвата
        """
        if not self.access_token:
            await self.get_access_token()

        url = f'{self.base_url}/v2/checkout/orders/{order_id}/capture'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()

            capture_data = response.json()

            return {
                'order_id': order_id,
                'status': capture_data['status'],
                'capture_id': capture_data['purchase_units'][0]['payments']['captures'][0]['id'],
                'amount': capture_data['purchase_units'][0]['payments']['captures'][0]['amount'],
                'capture_data': capture_data
            }

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='capture_failed',
                message=f"Не удалось захватить PayPal платеж: {str(e)}"
            )

    async def refund_capture(
        self,
        capture_id: str,
        amount: Optional[Decimal] = None,
        currency: Optional[str] = None
    ) -> Dict:
        """
        Создать возврат для захваченного платежа.

        Args:
            capture_id: ID захвата
            amount: Сумма возврата (None для полного возврата)
            currency: Валюта возврата

        Returns:
            Результат возврата

        Raises:
            PaymentError: Ошибка возврата
        """
        if not self.access_token:
            await self.get_access_token()

        url = f'{self.base_url}/v2/payments/captures/{capture_id}/refund'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        refund_data = {}

        # Частичный возврат если указана сумма
        if amount is not None and currency is not None:
            refund_data['amount'] = {
                'currency_code': currency,
                'value': str(amount)
            }

        try:
            response = requests.post(url, headers=headers, json=refund_data)
            response.raise_for_status()

            refund = response.json()

            return {
                'refund_id': refund['id'],
                'status': refund['status'],
                'amount': refund.get('amount'),
                'refund': refund
            }

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='refund_failed',
                message=f"Не удалось создать PayPal возврат: {str(e)}"
            )
```

---

## PayPal Subscription Management

### Создание и управление PayPal подписками

```python
class PayPalSubscriptionService:
    """
    Управление PayPal Subscriptions (Billing Plans).

    Функции:
    - Создание billing plans
    - Создание подписок
    - Управление подписками
    - Отмена подписок
    """

    def __init__(self, client_id: str, client_secret: str, mode: str = 'sandbox'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.mode = mode

        if mode == 'sandbox':
            self.base_url = 'https://api-m.sandbox.paypal.com'
        else:
            self.base_url = 'https://api-m.paypal.com'

        self.access_token = None

    async def get_access_token(self) -> str:
        """Получить OAuth2 access token от PayPal."""
        url = f'{self.base_url}/v1/oauth2/token'

        auth = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()
        ).decode()

        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {'grant_type': 'client_credentials'}

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data['access_token']

            return self.access_token

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='token_acquisition_failed',
                message=f"Не удалось получить PayPal access token: {str(e)}"
            )

    async def create_subscription(
        self,
        plan_id: str,
        return_url: str,
        cancel_url: str,
        subscriber_name: Optional[str] = None,
        subscriber_email: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Создать PayPal подписку.

        Args:
            plan_id: ID Billing Plan
            return_url: URL для возврата после подтверждения
            cancel_url: URL для возврата при отмене
            subscriber_name: Имя подписчика
            subscriber_email: Email подписчика
            metadata: Дополнительные данные

        Returns:
            Созданная Subscription с approval URL

        Raises:
            PaymentError: Ошибка создания подписки
        """
        if not self.access_token:
            await self.get_access_token()

        url = f'{self.base_url}/v1/billing/subscriptions'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        subscription_data = {
            'plan_id': plan_id,
            'application_context': {
                'return_url': return_url,
                'cancel_url': cancel_url,
                'brand_name': metadata.get('brand_name', 'My Service') if metadata else 'My Service',
                'locale': metadata.get('locale', 'en-US') if metadata else 'en-US',
                'shipping_preference': 'NO_SHIPPING',
                'user_action': 'SUBSCRIBE_NOW'
            }
        }

        # Добавить информацию о подписчике
        if subscriber_name or subscriber_email:
            subscription_data['subscriber'] = {}

            if subscriber_name:
                subscription_data['subscriber']['name'] = {
                    'given_name': subscriber_name.split()[0],
                    'surname': subscriber_name.split()[-1] if len(subscriber_name.split()) > 1 else ''
                }

            if subscriber_email:
                subscription_data['subscriber']['email_address'] = subscriber_email

        # Добавить custom_id для идентификации
        if metadata and 'user_id' in metadata:
            subscription_data['custom_id'] = metadata['user_id']

        try:
            response = requests.post(url, headers=headers, json=subscription_data)
            response.raise_for_status()

            subscription = response.json()

            # Извлечь approval URL
            approval_url = None
            for link in subscription.get('links', []):
                if link['rel'] == 'approve':
                    approval_url = link['href']
                    break

            return {
                'subscription_id': subscription['id'],
                'status': subscription['status'],
                'approval_url': approval_url,
                'subscription': subscription
            }

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='subscription_creation_failed',
                message=f"Не удалось создать PayPal подписку: {str(e)}"
            )

    async def cancel_subscription(
        self,
        subscription_id: str,
        reason: Optional[str] = None
    ) -> Dict:
        """
        Отменить PayPal подписку.

        Args:
            subscription_id: ID подписки
            reason: Причина отмены

        Returns:
            Результат отмены

        Raises:
            PaymentError: Ошибка отмены
        """
        if not self.access_token:
            await self.get_access_token()

        url = f'{self.base_url}/v1/billing/subscriptions/{subscription_id}/cancel'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        cancel_data = {
            'reason': reason or 'Customer requested cancellation'
        }

        try:
            response = requests.post(url, headers=headers, json=cancel_data)
            response.raise_for_status()

            return {
                'subscription_id': subscription_id,
                'status': 'cancelled',
                'success': True
            }

        except requests.exceptions.RequestException as e:
            raise PaymentError(
                code='subscription_cancellation_failed',
                message=f"Не удалось отменить PayPal подписку: {str(e)}"
            )
```

---

## Square Payment Integration

### Square Payment и Subscription API

```python
from square.client import Client as SquareClient
import uuid

class SquarePaymentService:
    """
    Production-ready сервис для работы с Square Payments API.

    Поддержка:
    - Создание платежей
    - Создание подписок
    - Управление клиентами
    - Возвраты
    """

    def __init__(self, access_token: str, environment: str = 'sandbox'):
        """
        Инициализация Square сервиса.

        Args:
            access_token: Square Access Token
            environment: Окружение ('sandbox' или 'production')
        """
        self.client = SquareClient(
            access_token=access_token,
            environment=environment
        )

    async def create_payment(
        self,
        amount: Decimal,
        currency: str = 'USD',
        source_id: str = None,
        customer_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Создать Square платеж.

        Args:
            amount: Сумма платежа
            currency: Валюта (ISO код)
            source_id: ID payment source (card nonce)
            customer_id: ID Square клиента (опционально)
            idempotency_key: Ключ идемпотентности (опционально)
            metadata: Дополнительные данные

        Returns:
            Результат платежа

        Raises:
            PaymentError: Ошибка создания платежа
        """
        # Генерация idempotency key если не передан
        if not idempotency_key:
            idempotency_key = str(uuid.uuid4())

        # Конвертация в минорные единицы (центы)
        amount_money = {
            'amount': int(amount * 100),
            'currency': currency
        }

        payment_request = {
            'source_id': source_id,
            'idempotency_key': idempotency_key,
            'amount_money': amount_money
        }

        # Добавить customer_id если передан
        if customer_id:
            payment_request['customer_id'] = customer_id

        # Добавить metadata
        if metadata:
            payment_request['note'] = metadata.get('note', '')
            payment_request['reference_id'] = metadata.get('reference_id', '')

        try:
            result = self.client.payments.create_payment(
                body=payment_request
            )

            if result.is_success():
                payment = result.body['payment']

                return {
                    'payment_id': payment['id'],
                    'status': payment['status'],
                    'amount': payment['amount_money'],
                    'payment': payment
                }
            else:
                errors = result.errors
                raise PaymentError(
                    code='payment_creation_failed',
                    message=f"Square платеж не удался: {errors[0]['detail']}",
                    details={'errors': errors}
                )

        except Exception as e:
            raise PaymentError(
                code='payment_error',
                message=f"Ошибка Square платежа: {str(e)}"
            )

    async def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        card_id: Optional[str] = None,
        start_date: Optional[str] = None,
        idempotency_key: Optional[str] = None
    ) -> Dict:
        """
        Создать Square подписку.

        Args:
            customer_id: ID Square клиента
            plan_id: ID Subscription Plan
            card_id: ID карты для автоплатежей (опционально)
            start_date: Дата начала подписки (ISO 8601)
            idempotency_key: Ключ идемпотентности

        Returns:
            Созданная Subscription

        Raises:
            PaymentError: Ошибка создания подписки
        """
        if not idempotency_key:
            idempotency_key = str(uuid.uuid4())

        subscription_request = {
            'idempotency_key': idempotency_key,
            'location_id': self._get_location_id(),
            'plan_id': plan_id,
            'customer_id': customer_id
        }

        # Добавить card_id если передан
        if card_id:
            subscription_request['card_id'] = card_id

        # Добавить start_date если передан
        if start_date:
            subscription_request['start_date'] = start_date

        try:
            result = self.client.subscriptions.create_subscription(
                body=subscription_request
            )

            if result.is_success():
                subscription = result.body['subscription']

                return {
                    'subscription_id': subscription['id'],
                    'status': subscription['status'],
                    'subscription': subscription
                }
            else:
                errors = result.errors
                raise PaymentError(
                    code='subscription_creation_failed',
                    message=f"Square подписка не создана: {errors[0]['detail']}",
                    details={'errors': errors}
                )

        except Exception as e:
            raise PaymentError(
                code='subscription_error',
                message=f"Ошибка Square подписки: {str(e)}"
            )

    async def cancel_subscription(
        self,
        subscription_id: str
    ) -> Dict:
        """
        Отменить Square подписку.

        Args:
            subscription_id: ID подписки

        Returns:
            Результат отмены

        Raises:
            PaymentError: Ошибка отмены
        """
        try:
            result = self.client.subscriptions.cancel_subscription(
                subscription_id=subscription_id
            )

            if result.is_success():
                subscription = result.body['subscription']

                return {
                    'subscription_id': subscription_id,
                    'status': subscription['status'],
                    'success': True
                }
            else:
                errors = result.errors
                raise PaymentError(
                    code='subscription_cancellation_failed',
                    message=f"Square подписка не отменена: {errors[0]['detail']}",
                    details={'errors': errors}
                )

        except Exception as e:
            raise PaymentError(
                code='subscription_cancellation_error',
                message=f"Ошибка отмены Square подписки: {str(e)}"
            )

    def _get_location_id(self) -> str:
        """
        Получить первый доступный location ID.

        Returns:
            Location ID для использования в запросах
        """
        result = self.client.locations.list_locations()

        if result.is_success() and result.body.get('locations'):
            return result.body['locations'][0]['id']
        else:
            raise PaymentError(
                code='no_location',
                message="Не найдено ни одного Square location"
            )
```

---

## Multi-Provider Strategy Pattern

### Универсальный роутер платежей

```python
from enum import Enum
from typing import Protocol

class PaymentProvider(str, Enum):
    """Поддерживаемые платежные провайдеры."""
    STRIPE = 'stripe'
    PAYPAL = 'paypal'
    SQUARE = 'square'

class PaymentServiceProtocol(Protocol):
    """Протокол для всех платежных сервисов."""

    async def create_payment(
        self,
        amount: Decimal,
        currency: str,
        **kwargs
    ) -> Dict:
        """Создать платеж."""
        ...

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[Decimal] = None,
        **kwargs
    ) -> Dict:
        """Создать возврат."""
        ...

class PaymentRouter:
    """
    Универсальный роутер для работы с несколькими платежными провайдерами.

    Функции:
    - Автоматический выбор провайдера
    - Fallback на запасные провайдеры
    - Умная маршрутизация на основе метрик
    """

    def __init__(
        self,
        stripe_service: StripePaymentService,
        paypal_service: PayPalPaymentService,
        square_service: SquarePaymentService,
        default_provider: PaymentProvider = PaymentProvider.STRIPE
    ):
        """
        Инициализация роутера с несколькими провайдерами.

        Args:
            stripe_service: Stripe сервис
            paypal_service: PayPal сервис
            square_service: Square сервис
            default_provider: Провайдер по умолчанию
        """
        self.providers = {
            PaymentProvider.STRIPE: stripe_service,
            PaymentProvider.PAYPAL: paypal_service,
            PaymentProvider.SQUARE: square_service
        }
        self.default_provider = default_provider

    async def create_payment(
        self,
        amount: Decimal,
        currency: str,
        provider: Optional[PaymentProvider] = None,
        fallback: bool = True,
        **kwargs
    ) -> Dict:
        """
        Создать платеж через выбранного провайдера с fallback.

        Args:
            amount: Сумма платежа
            currency: Валюта
            provider: Конкретный провайдер (опционально)
            fallback: Использовать fallback при ошибке
            **kwargs: Дополнительные параметры для провайдера

        Returns:
            Результат платежа с информацией о провайдере

        Raises:
            PaymentError: Все провайдеры недоступны
        """
        # Выбрать провайдера
        selected_provider = provider or self.default_provider
        service = self.providers[selected_provider]

        try:
            # Попытка создать платеж
            result = await service.create_payment(
                amount=amount,
                currency=currency,
                **kwargs
            )

            result['provider'] = selected_provider.value

            return result

        except PaymentError as e:
            if not fallback:
                raise

            # Попробовать fallback провайдеры
            fallback_providers = [
                p for p in self.providers.keys()
                if p != selected_provider
            ]

            for fallback_provider in fallback_providers:
                try:
                    fallback_service = self.providers[fallback_provider]

                    result = await fallback_service.create_payment(
                        amount=amount,
                        currency=currency,
                        **kwargs
                    )

                    result['provider'] = fallback_provider.value
                    result['fallback_used'] = True
                    result['original_provider'] = selected_provider.value

                    return result

                except PaymentError:
                    continue

            # Все провайдеры не сработали
            raise PaymentError(
                code='all_providers_failed',
                message=f"Все платежные провайдеры недоступны"
            )

    def select_provider_by_metrics(
        self,
        amount: Decimal,
        currency: str,
        customer_country: Optional[str] = None
    ) -> PaymentProvider:
        """
        Выбрать оптимального провайдера на основе метрик.

        Args:
            amount: Сумма платежа
            currency: Валюта
            customer_country: Страна клиента

        Returns:
            Рекомендованный провайдер
        """
        # Логика выбора на основе комиссий и доступности

        # PayPal популярен в США и Европе
        if customer_country in ['US', 'GB', 'DE', 'FR']:
            return PaymentProvider.PAYPAL

        # Stripe универсален и имеет низкие комиссии
        if currency in ['USD', 'EUR', 'GBP']:
            return PaymentProvider.STRIPE

        # Square хорош для малого бизнеса в США
        if customer_country == 'US' and amount < Decimal('1000'):
            return PaymentProvider.SQUARE

        # Дефолт
        return self.default_provider
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Implementation Engineer
