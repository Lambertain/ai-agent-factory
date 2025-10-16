# Module 01: Stripe Integration

## Полная интеграция Stripe API для платежных систем

Этот модуль содержит production-ready паттерны для интеграции Stripe: Payment Intent, Setup Intent, webhooks, subscriptions.

---

## Payment Intent Pattern (Современный подход)

### Создание Payment Intent

```python
import stripe
from typing import Dict, Optional, List
from decimal import Decimal

class StripePaymentService:
    """
    Production-ready сервис для работы с Stripe Payment Intent API.

    Использует современный Payment Intent flow вместо устаревших Charges API.
    """

    def __init__(self, api_key: str):
        """
        Инициализация сервиса Stripe.

        Args:
            api_key: Stripe API ключ (секретный)
        """
        stripe.api_key = api_key
        self.supported_payment_methods = [
            'card',
            'us_bank_account',
            'sepa_debit',
            'ideal',
            'sofort'
        ]

    async def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = 'usd',
        customer_id: Optional[str] = None,
        payment_method_types: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
        description: Optional[str] = None,
        statement_descriptor: Optional[str] = None
    ) -> stripe.PaymentIntent:
        """
        Создать Payment Intent для одноразового платежа.

        Args:
            amount: Сумма платежа в основной валюте (например, 10.00 для $10.00)
            currency: Валюта платежа (ISO код)
            customer_id: ID существующего Stripe клиента (опционально)
            payment_method_types: Типы платежей (по умолчанию ['card'])
            metadata: Дополнительные данные для хранения
            description: Описание платежа
            statement_descriptor: Текст в выписке клиента (макс 22 символа)

        Returns:
            Созданный PaymentIntent объект

        Raises:
            stripe.error.CardError: Проблема с картой
            stripe.error.InvalidRequestError: Неверные параметры
        """
        # Конвертация суммы в центы
        amount_in_cents = int(amount * 100)

        # Параметры по умолчанию
        if payment_method_types is None:
            payment_method_types = ['card']

        # Создание Payment Intent
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency=currency.lower(),
                payment_method_types=payment_method_types,
                confirmation_method='automatic',
                capture_method='automatic',
                customer=customer_id,
                metadata=metadata or {},
                description=description,
                statement_descriptor=statement_descriptor
            )

            return payment_intent

        except stripe.error.CardError as e:
            # Проблема с картой (недостаточно средств, карта отклонена и т.д.)
            raise PaymentError(
                code='card_declined',
                message=f"Карта отклонена: {e.user_message}",
                details=e.json_body
            )

        except stripe.error.InvalidRequestError as e:
            # Неверные параметры запроса
            raise PaymentError(
                code='invalid_request',
                message=f"Неверный запрос: {str(e)}",
                details=e.json_body
            )

    async def confirm_payment_intent(
        self,
        payment_intent_id: str,
        payment_method_id: Optional[str] = None
    ) -> stripe.PaymentIntent:
        """
        Подтвердить Payment Intent после получения payment method от клиента.

        Args:
            payment_intent_id: ID Payment Intent
            payment_method_id: ID payment method от клиента (опционально)

        Returns:
            Обновленный PaymentIntent
        """
        try:
            payment_intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method_id
            )

            return payment_intent

        except stripe.error.CardError as e:
            raise PaymentError(
                code='confirmation_failed',
                message=f"Не удалось подтвердить платеж: {e.user_message}"
            )

    async def capture_payment_intent(
        self,
        payment_intent_id: str,
        amount_to_capture: Optional[int] = None
    ) -> stripe.PaymentIntent:
        """
        Захватить платеж (для manual capture method).

        Args:
            payment_intent_id: ID Payment Intent
            amount_to_capture: Сумма для захвата в центах (опционально)

        Returns:
            Обновленный PaymentIntent
        """
        try:
            payment_intent = stripe.PaymentIntent.capture(
                payment_intent_id,
                amount_to_capture=amount_to_capture
            )

            return payment_intent

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='capture_failed',
                message=f"Не удалось захватить платеж: {str(e)}"
            )

    async def cancel_payment_intent(
        self,
        payment_intent_id: str,
        cancellation_reason: Optional[str] = None
    ) -> stripe.PaymentIntent:
        """
        Отменить Payment Intent.

        Args:
            payment_intent_id: ID Payment Intent
            cancellation_reason: Причина отмены

        Returns:
            Отмененный PaymentIntent
        """
        try:
            payment_intent = stripe.PaymentIntent.cancel(
                payment_intent_id,
                cancellation_reason=cancellation_reason
            )

            return payment_intent

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='cancellation_failed',
                message=f"Не удалось отменить платеж: {str(e)}"
            )
```

---

## Setup Intent Pattern (Сохранение платежных методов)

### Создание Setup Intent для сохранения карты

```python
class StripeSetupService:
    """
    Сервис для сохранения платежных методов без списания средств.

    Используется для:
    - Сохранения карты для будущих платежей
    - Верификации карты без списания
    - Создания подписок с отложенным списанием
    """

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    async def create_setup_intent(
        self,
        customer_id: str,
        payment_method_types: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
        usage: str = 'off_session'
    ) -> stripe.SetupIntent:
        """
        Создать Setup Intent для сохранения платежного метода.

        Args:
            customer_id: ID Stripe клиента
            payment_method_types: Типы платежей (по умолчанию ['card'])
            metadata: Дополнительные данные
            usage: Когда будет использован метод ('on_session' или 'off_session')

        Returns:
            Созданный SetupIntent объект
        """
        if payment_method_types is None:
            payment_method_types = ['card']

        try:
            setup_intent = stripe.SetupIntent.create(
                customer=customer_id,
                payment_method_types=payment_method_types,
                usage=usage,
                metadata=metadata or {}
            )

            return setup_intent

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='setup_intent_failed',
                message=f"Не удалось создать Setup Intent: {str(e)}"
            )

    async def confirm_setup_intent(
        self,
        setup_intent_id: str,
        payment_method_id: str
    ) -> stripe.SetupIntent:
        """
        Подтвердить Setup Intent с payment method от клиента.

        Args:
            setup_intent_id: ID Setup Intent
            payment_method_id: ID payment method

        Returns:
            Подтвержденный SetupIntent
        """
        try:
            setup_intent = stripe.SetupIntent.confirm(
                setup_intent_id,
                payment_method=payment_method_id
            )

            return setup_intent

        except stripe.error.CardError as e:
            raise PaymentError(
                code='setup_confirmation_failed',
                message=f"Не удалось подтвердить Setup Intent: {e.user_message}"
            )

    async def attach_payment_method(
        self,
        payment_method_id: str,
        customer_id: str
    ) -> stripe.PaymentMethod:
        """
        Привязать payment method к клиенту.

        Args:
            payment_method_id: ID payment method
            customer_id: ID Stripe клиента

        Returns:
            Привязанный PaymentMethod
        """
        try:
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )

            return payment_method

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='attach_failed',
                message=f"Не удалось привязать payment method: {str(e)}"
            )

    async def set_default_payment_method(
        self,
        customer_id: str,
        payment_method_id: str
    ) -> stripe.Customer:
        """
        Установить payment method как дефолтный для клиента.

        Args:
            customer_id: ID Stripe клиента
            payment_method_id: ID payment method

        Returns:
            Обновленный Customer объект
        """
        try:
            customer = stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )

            return customer

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='default_payment_method_failed',
                message=f"Не удалось установить дефолтный payment method: {str(e)}"
            )
```

---

## Webhook Signature Verification

### Верификация и обработка Stripe webhooks

```python
import hmac
import hashlib
import json
from typing import Dict, Optional

class StripeWebhookHandler:
    """
    Безопасная обработка Stripe webhooks с верификацией подписи.

    Предотвращает:
    - Replay attacks
    - Man-in-the-middle attacks
    - Фальшивые webhook события
    """

    def __init__(self, webhook_secret: str):
        """
        Инициализация обработчика webhooks.

        Args:
            webhook_secret: Webhook signing secret из Stripe Dashboard
        """
        self.webhook_secret = webhook_secret
        self.tolerance = 300  # 5 минут tolerance для timestamp

    async def verify_signature(
        self,
        payload: bytes,
        signature_header: str
    ) -> Optional[stripe.Event]:
        """
        Верифицировать Stripe webhook signature.

        Args:
            payload: Сырое тело запроса (bytes)
            signature_header: Значение заголовка Stripe-Signature

        Returns:
            Провалидированный Stripe Event объект или None

        Raises:
            WebhookSignatureError: Неверная подпись
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature_header,
                self.webhook_secret
            )

            return event

        except ValueError as e:
            # Неверный payload
            raise WebhookSignatureError(
                code='invalid_payload',
                message=f"Неверный webhook payload: {str(e)}"
            )

        except stripe.error.SignatureVerificationError as e:
            # Неверная подпись
            raise WebhookSignatureError(
                code='invalid_signature',
                message=f"Неверная webhook подпись: {str(e)}"
            )

    async def process_event(
        self,
        event: stripe.Event,
        handlers: Dict[str, callable]
    ) -> Dict:
        """
        Обработать webhook event с соответствующим handler.

        Args:
            event: Провалидированный Stripe Event
            handlers: Словарь {event_type: handler_function}

        Returns:
            Результат обработки
        """
        event_type = event['type']
        event_data = event['data']['object']

        # Найти соответствующий handler
        handler = handlers.get(event_type)

        if handler is None:
            # Нет handler для этого типа события
            return {
                'status': 'unhandled',
                'event_type': event_type,
                'message': f"Нет handler для события {event_type}"
            }

        try:
            # Вызвать handler
            result = await handler(event_data, event)

            return {
                'status': 'success',
                'event_type': event_type,
                'result': result
            }

        except Exception as e:
            # Ошибка при обработке
            return {
                'status': 'error',
                'event_type': event_type,
                'error': str(e)
            }

# Примеры handlers для различных событий
async def handle_payment_succeeded(payment_intent: Dict, event: stripe.Event) -> Dict:
    """
    Обработать успешный платеж.

    Args:
        payment_intent: PaymentIntent объект
        event: Полный Stripe Event

    Returns:
        Результат обработки
    """
    customer_id = payment_intent.get('customer')
    amount = payment_intent.get('amount')

    # Обновить статус заказа
    await update_order_status(
        payment_intent_id=payment_intent['id'],
        status='paid',
        amount=amount / 100  # Конвертация из центов
    )

    # Отправить email подтверждение
    await send_payment_confirmation_email(customer_id)

    return {
        'order_updated': True,
        'email_sent': True
    }

async def handle_payment_failed(payment_intent: Dict, event: stripe.Event) -> Dict:
    """
    Обработать неудачный платеж.

    Args:
        payment_intent: PaymentIntent объект
        event: Полный Stripe Event

    Returns:
        Результат обработки
    """
    customer_id = payment_intent.get('customer')
    error_message = payment_intent.get('last_payment_error', {}).get('message')

    # Обновить статус заказа
    await update_order_status(
        payment_intent_id=payment_intent['id'],
        status='payment_failed',
        error=error_message
    )

    # Уведомить клиента
    await send_payment_failed_notification(customer_id, error_message)

    return {
        'order_updated': True,
        'notification_sent': True
    }

async def handle_customer_created(customer: Dict, event: stripe.Event) -> Dict:
    """
    Обработать создание нового клиента.

    Args:
        customer: Customer объект
        event: Полный Stripe Event

    Returns:
        Результат обработки
    """
    # Синхронизировать с локальной БД
    await sync_customer_to_database(
        stripe_customer_id=customer['id'],
        email=customer.get('email'),
        metadata=customer.get('metadata', {})
    )

    return {
        'customer_synced': True
    }
```

---

## Customer Management

### Создание и управление Stripe клиентами

```python
class StripeCustomerService:
    """
    Управление Stripe клиентами.

    Функции:
    - Создание клиентов
    - Обновление данных
    - Привязка платежных методов
    - Управление метаданными
    """

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    async def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict] = None,
        payment_method_id: Optional[str] = None
    ) -> stripe.Customer:
        """
        Создать нового Stripe клиента.

        Args:
            email: Email клиента
            name: Имя клиента
            phone: Телефон клиента
            metadata: Дополнительные данные (макс 50 ключей)
            payment_method_id: ID payment method для привязки

        Returns:
            Созданный Customer объект
        """
        try:
            customer_params = {
                'email': email,
                'metadata': metadata or {}
            }

            if name:
                customer_params['name'] = name

            if phone:
                customer_params['phone'] = phone

            if payment_method_id:
                customer_params['payment_method'] = payment_method_id
                customer_params['invoice_settings'] = {
                    'default_payment_method': payment_method_id
                }

            customer = stripe.Customer.create(**customer_params)

            return customer

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='customer_creation_failed',
                message=f"Не удалось создать клиента: {str(e)}"
            )

    async def update_customer(
        self,
        customer_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> stripe.Customer:
        """
        Обновить данные Stripe клиента.

        Args:
            customer_id: ID Stripe клиента
            email: Новый email (опционально)
            name: Новое имя (опционально)
            phone: Новый телефон (опционально)
            metadata: Обновленные метаданные (опционально)

        Returns:
            Обновленный Customer объект
        """
        update_params = {}

        if email is not None:
            update_params['email'] = email

        if name is not None:
            update_params['name'] = name

        if phone is not None:
            update_params['phone'] = phone

        if metadata is not None:
            update_params['metadata'] = metadata

        try:
            customer = stripe.Customer.modify(customer_id, **update_params)

            return customer

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='customer_update_failed',
                message=f"Не удалось обновить клиента: {str(e)}"
            )

    async def delete_customer(self, customer_id: str) -> Dict:
        """
        Удалить Stripe клиента.

        Args:
            customer_id: ID Stripe клиента

        Returns:
            Результат удаления
        """
        try:
            result = stripe.Customer.delete(customer_id)

            return {
                'deleted': result.get('deleted', False),
                'customer_id': customer_id
            }

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='customer_deletion_failed',
                message=f"Не удалось удалить клиента: {str(e)}"
            )
```

---

## Subscription Creation

### Создание и управление подписками

```python
class StripeSubscriptionService:
    """
    Управление Stripe подписками.

    Поддержка:
    - Создание подписок
    - Обновление планов
    - Отмена подписок
    - Пробные периоды
    """

    def __init__(self, api_key: str):
        stripe.api_key = api_key

    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        payment_method_id: Optional[str] = None,
        trial_period_days: Optional[int] = None,
        metadata: Optional[Dict] = None,
        proration_behavior: str = 'create_prorations'
    ) -> stripe.Subscription:
        """
        Создать новую подписку для клиента.

        Args:
            customer_id: ID Stripe клиента
            price_id: ID Stripe Price (план подписки)
            payment_method_id: ID payment method (опционально)
            trial_period_days: Количество дней пробного периода
            metadata: Дополнительные данные
            proration_behavior: Поведение пропорции ('create_prorations', 'none', 'always_invoice')

        Returns:
            Созданная Subscription
        """
        subscription_params = {
            'customer': customer_id,
            'items': [{'price': price_id}],
            'metadata': metadata or {},
            'proration_behavior': proration_behavior
        }

        if payment_method_id:
            subscription_params['default_payment_method'] = payment_method_id

        if trial_period_days is not None:
            subscription_params['trial_period_days'] = trial_period_days

        try:
            subscription = stripe.Subscription.create(**subscription_params)

            return subscription

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='subscription_creation_failed',
                message=f"Не удалось создать подписку: {str(e)}"
            )

    async def update_subscription(
        self,
        subscription_id: str,
        new_price_id: Optional[str] = None,
        proration_behavior: str = 'create_prorations',
        metadata: Optional[Dict] = None
    ) -> stripe.Subscription:
        """
        Обновить существующую подписку.

        Args:
            subscription_id: ID подписки
            new_price_id: Новый план подписки (опционально)
            proration_behavior: Поведение пропорции
            metadata: Обновленные метаданные

        Returns:
            Обновленная Subscription
        """
        update_params = {
            'proration_behavior': proration_behavior
        }

        if new_price_id:
            # Получить текущую подписку
            subscription = stripe.Subscription.retrieve(subscription_id)

            update_params['items'] = [{
                'id': subscription['items']['data'][0].id,
                'price': new_price_id
            }]

        if metadata:
            update_params['metadata'] = metadata

        try:
            subscription = stripe.Subscription.modify(subscription_id, **update_params)

            return subscription

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='subscription_update_failed',
                message=f"Не удалось обновить подписку: {str(e)}"
            )

    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> stripe.Subscription:
        """
        Отменить подписку.

        Args:
            subscription_id: ID подписки
            at_period_end: Отменить в конце периода (True) или немедленно (False)

        Returns:
            Отмененная Subscription
        """
        try:
            if at_period_end:
                # Отмена в конце периода
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                # Немедленная отмена
                subscription = stripe.Subscription.delete(subscription_id)

            return subscription

        except stripe.error.InvalidRequestError as e:
            raise PaymentError(
                code='subscription_cancellation_failed',
                message=f"Не удалось отменить подписку: {str(e)}"
            )
```

---

## Error Handling

### Custom exceptions для Stripe операций

```python
class PaymentError(Exception):
    """Базовый класс для ошибок платежей."""

    def __init__(self, code: str, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class WebhookSignatureError(Exception):
    """Ошибка верификации webhook подписи."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Implementation Engineer
