# Module 04: Business Model Patterns

## E-commerce, SaaS, Marketplace - Payment Flow Implementations

Этот модуль содержит production-ready паттерны для различных бизнес-моделей: E-commerce, SaaS, и Marketplace.

---

## E-commerce Payment Flow

### Complete Checkout to Shipment Flow

```python
from typing import Dict, List, Optional
from decimal import Decimal
from enum import Enum

class OrderStatus(str, Enum):
    """Статусы заказа."""
    PENDING = 'pending'
    PAYMENT_PROCESSING = 'payment_processing'
    PAID = 'paid'
    PAYMENT_FAILED = 'payment_failed'
    INVENTORY_RESERVED = 'inventory_reserved'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class EcommercePaymentFlow:
    """
    Production-ready E-commerce payment flow.

    Этапы:
    1. Create order (cart → order)
    2. Reserve inventory
    3. Process payment
    4. Create shipment
    5. Update order status
    """

    def __init__(
        self,
        payment_service,
        inventory_service,
        shipment_service,
        db_session
    ):
        self.payment = payment_service
        self.inventory = inventory_service
        self.shipment = shipment_service
        self.db = db_session

    async def process_checkout(
        self,
        cart_items: List[Dict],
        customer_data: Dict,
        payment_method: Dict,
        shipping_address: Dict
    ) -> Dict:
        """
        Обработать полный checkout flow.

        Args:
            cart_items: Товары в корзине
            customer_data: Данные клиента
            payment_method: Платежный метод
            shipping_address: Адрес доставки

        Returns:
            Результат checkout с order_id и статусом

        Raises:
            CheckoutError: Ошибка на любом этапе checkout
        """
        # STEP 1: Создать заказ
        order = await self._create_order(
            cart_items=cart_items,
            customer_data=customer_data,
            shipping_address=shipping_address
        )

        order_id = order['id']

        try:
            # STEP 2: Зарезервировать inventory
            reservation = await self._reserve_inventory(
                order_id=order_id,
                cart_items=cart_items
            )

            await self._update_order_status(
                order_id,
                OrderStatus.INVENTORY_RESERVED
            )

            # STEP 3: Обработать платеж
            payment_result = await self._process_payment(
                order_id=order_id,
                amount=order['total_amount'],
                payment_method=payment_method,
                customer_data=customer_data
            )

            if payment_result['status'] != 'success':
                # Платеж не прошел - откатить резервацию
                await self._release_inventory(reservation['reservation_id'])

                await self._update_order_status(
                    order_id,
                    OrderStatus.PAYMENT_FAILED
                )

                raise CheckoutError(
                    code='payment_failed',
                    message=payment_result.get('error', 'Payment failed')
                )

            await self._update_order_status(
                order_id,
                OrderStatus.PAID
            )

            # STEP 4: Создать shipment
            shipment = await self._create_shipment(
                order_id=order_id,
                shipping_address=shipping_address,
                cart_items=cart_items
            )

            await self._update_order_status(
                order_id,
                OrderStatus.SHIPPED
            )

            # STEP 5: Отправить email подтверждение
            await self._send_order_confirmation_email(
                customer_email=customer_data['email'],
                order_id=order_id,
                tracking_number=shipment['tracking_number']
            )

            return {
                'success': True,
                'order_id': order_id,
                'payment_id': payment_result['payment_id'],
                'tracking_number': shipment['tracking_number'],
                'status': OrderStatus.SHIPPED
            }

        except Exception as e:
            # Откатить все изменения
            await self._rollback_checkout(order_id)

            raise CheckoutError(
                code='checkout_failed',
                message=f"Checkout failed: {str(e)}"
            )

    async def _create_order(
        self,
        cart_items: List[Dict],
        customer_data: Dict,
        shipping_address: Dict
    ) -> Dict:
        """
        Создать заказ в БД.

        Args:
            cart_items: Товары
            customer_data: Данные клиента
            shipping_address: Адрес доставки

        Returns:
            Созданный заказ
        """
        # Рассчитать total
        subtotal = sum(
            Decimal(item['price']) * item['quantity']
            for item in cart_items
        )

        tax = subtotal * Decimal('0.08')  # 8% tax
        shipping = Decimal('10.00')  # Фиксированная доставка
        total = subtotal + tax + shipping

        # Создать в БД
        order = await self.db.orders.create({
            'customer_id': customer_data['id'],
            'customer_email': customer_data['email'],
            'items': cart_items,
            'subtotal': float(subtotal),
            'tax': float(tax),
            'shipping': float(shipping),
            'total_amount': float(total),
            'shipping_address': shipping_address,
            'status': OrderStatus.PENDING
        })

        return order

    async def _reserve_inventory(
        self,
        order_id: str,
        cart_items: List[Dict]
    ) -> Dict:
        """
        Зарезервировать товары на складе.

        Args:
            order_id: ID заказа
            cart_items: Товары для резервации

        Returns:
            Результат резервации

        Raises:
            InventoryError: Недостаточно товара на складе
        """
        reservation_items = []

        for item in cart_items:
            product_id = item['product_id']
            quantity = item['quantity']

            # Проверить доступность
            available = await self.inventory.check_availability(
                product_id,
                quantity
            )

            if not available:
                # Откатить предыдущие резервации
                for reserved in reservation_items:
                    await self.inventory.release(reserved['reservation_id'])

                raise InventoryError(
                    code='insufficient_stock',
                    message=f"Недостаточно товара {product_id}"
                )

            # Зарезервировать
            reservation = await self.inventory.reserve(
                product_id=product_id,
                quantity=quantity,
                order_id=order_id,
                expires_in=900  # 15 минут
            )

            reservation_items.append(reservation)

        return {
            'reservation_id': order_id,
            'items': reservation_items,
            'expires_at': reservation_items[0]['expires_at']
        }

    async def _process_payment(
        self,
        order_id: str,
        amount: float,
        payment_method: Dict,
        customer_data: Dict
    ) -> Dict:
        """
        Обработать платеж.

        Args:
            order_id: ID заказа
            amount: Сумма платежа
            payment_method: Платежный метод
            customer_data: Данные клиента

        Returns:
            Результат платежа
        """
        try:
            payment_result = await self.payment.create_payment(
                amount=Decimal(str(amount)),
                currency='USD',
                payment_method_id=payment_method['id'],
                customer_id=customer_data.get('stripe_customer_id'),
                metadata={
                    'order_id': order_id,
                    'customer_email': customer_data['email']
                }
            )

            return {
                'status': 'success',
                'payment_id': payment_result['payment_id']
            }

        except PaymentError as e:
            return {
                'status': 'failed',
                'error': str(e)
            }

    async def _create_shipment(
        self,
        order_id: str,
        shipping_address: Dict,
        cart_items: List[Dict]
    ) -> Dict:
        """
        Создать shipment.

        Args:
            order_id: ID заказа
            shipping_address: Адрес доставки
            cart_items: Товары

        Returns:
            Созданный shipment
        """
        shipment = await self.shipment.create(
            order_id=order_id,
            address=shipping_address,
            items=cart_items,
            shipping_method='standard'
        )

        return {
            'shipment_id': shipment['id'],
            'tracking_number': shipment['tracking_number'],
            'estimated_delivery': shipment['estimated_delivery']
        }

    async def _update_order_status(
        self,
        order_id: str,
        status: OrderStatus
    ) -> None:
        """Обновить статус заказа."""
        await self.db.orders.update(
            order_id,
            {'status': status.value}
        )

    async def _release_inventory(self, reservation_id: str) -> None:
        """Освободить зарезервированный inventory."""
        await self.inventory.release(reservation_id)

    async def _rollback_checkout(self, order_id: str) -> None:
        """Откатить checkout при ошибке."""
        # Освободить inventory
        await self._release_inventory(order_id)

        # Обновить статус заказа
        await self._update_order_status(
            order_id,
            OrderStatus.CANCELLED
        )

    async def _send_order_confirmation_email(
        self,
        customer_email: str,
        order_id: str,
        tracking_number: str
    ) -> None:
        """Отправить email подтверждение заказа."""
        # Реализация отправки email
        pass
```

---

## SaaS Subscription Lifecycle Management

### Complete Subscription Flow with Dunning

```python
from datetime import datetime, timedelta

class SubscriptionStatus(str, Enum):
    """Статусы подписки."""
    ACTIVE = 'active'
    PAST_DUE = 'past_due'
    CANCELLED = 'cancelled'
    PAUSED = 'paused'

class SaaSSubscriptionFlow:
    """
    Production-ready SaaS subscription management.

    Функции:
    - Создание подписок
    - Plan changes с proration
    - Dunning management (retry logic для failed payments)
    - Usage-based billing
    """

    def __init__(
        self,
        payment_service,
        email_service,
        db_session
    ):
        self.payment = payment_service
        self.email = email_service
        self.db = db_session

        # Dunning configuration
        self.dunning_attempts = 3
        self.dunning_intervals = [3, 7, 14]  # days

    async def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_method_id: str,
        trial_days: Optional[int] = None
    ) -> Dict:
        """
        Создать новую подписку.

        Args:
            customer_id: ID клиента
            plan_id: ID плана подписки
            payment_method_id: ID платежного метода
            trial_days: Дни пробного периода (опционально)

        Returns:
            Созданная подписка
        """
        # Получить детали плана
        plan = await self.db.plans.get(plan_id)

        # Создать подписку через payment provider
        subscription = await self.payment.create_subscription(
            customer_id=customer_id,
            price_id=plan['stripe_price_id'],
            payment_method_id=payment_method_id,
            trial_period_days=trial_days
        )

        # Сохранить в БД
        db_subscription = await self.db.subscriptions.create({
            'customer_id': customer_id,
            'plan_id': plan_id,
            'stripe_subscription_id': subscription['id'],
            'status': SubscriptionStatus.ACTIVE,
            'current_period_start': subscription['current_period_start'],
            'current_period_end': subscription['current_period_end'],
            'trial_end': subscription.get('trial_end')
        })

        # Отправить welcome email
        await self.email.send_subscription_welcome(customer_id)

        return db_subscription

    async def change_plan(
        self,
        subscription_id: str,
        new_plan_id: str,
        prorate: bool = True
    ) -> Dict:
        """
        Изменить план подписки с proration.

        Args:
            subscription_id: ID подписки
            new_plan_id: ID нового плана
            prorate: Пропорциональное списание

        Returns:
            Обновленная подписка
        """
        # Получить текущую подписку
        subscription = await self.db.subscriptions.get(subscription_id)

        # Получить новый план
        new_plan = await self.db.plans.get(new_plan_id)

        # Обновить в payment provider
        updated_subscription = await self.payment.update_subscription(
            subscription_id=subscription['stripe_subscription_id'],
            new_price_id=new_plan['stripe_price_id'],
            proration_behavior='create_prorations' if prorate else 'none'
        )

        # Обновить в БД
        await self.db.subscriptions.update(subscription_id, {
            'plan_id': new_plan_id,
            'updated_at': datetime.utcnow()
        })

        # Отправить email о смене плана
        await self.email.send_plan_change_notification(
            subscription['customer_id'],
            new_plan['name']
        )

        return updated_subscription

    async def handle_payment_failed(
        self,
        subscription_id: str,
        payment_intent_id: str,
        error_message: str
    ) -> Dict:
        """
        Обработать неудачный платеж с dunning logic.

        Args:
            subscription_id: ID подписки
            payment_intent_id: ID неудачного payment intent
            error_message: Сообщение об ошибке

        Returns:
            Результат dunning процесса
        """
        # Получить подписку
        subscription = await self.db.subscriptions.get(subscription_id)

        # Получить dunning history
        dunning_attempts = await self.db.dunning.count(
            subscription_id=subscription_id,
            payment_intent_id=payment_intent_id
        )

        # Обновить статус подписки
        await self.db.subscriptions.update(subscription_id, {
            'status': SubscriptionStatus.PAST_DUE
        })

        # Отправить email о неудачном платеже
        await self.email.send_payment_failed_notification(
            customer_id=subscription['customer_id'],
            error_message=error_message,
            attempt=dunning_attempts + 1
        )

        # Запланировать retry если не превышен лимит
        if dunning_attempts < self.dunning_attempts:
            retry_date = datetime.utcnow() + timedelta(
                days=self.dunning_intervals[dunning_attempts]
            )

            # Создать dunning запись
            await self.db.dunning.create({
                'subscription_id': subscription_id,
                'payment_intent_id': payment_intent_id,
                'attempt_number': dunning_attempts + 1,
                'retry_date': retry_date,
                'status': 'scheduled'
            })

            return {
                'action': 'retry_scheduled',
                'retry_date': retry_date,
                'attempt': dunning_attempts + 1
            }

        else:
            # Превышен лимит попыток - отменить подписку
            await self.cancel_subscription(
                subscription_id,
                reason='payment_failed_max_attempts'
            )

            return {
                'action': 'subscription_cancelled',
                'reason': 'payment_failed_max_attempts'
            }

    async def retry_failed_payment(
        self,
        subscription_id: str,
        payment_intent_id: str
    ) -> Dict:
        """
        Повторить неудачный платеж (dunning retry).

        Args:
            subscription_id: ID подписки
            payment_intent_id: ID payment intent

        Returns:
            Результат повторной попытки
        """
        try:
            # Попытаться повторить платеж
            payment_result = await self.payment.retry_payment_intent(
                payment_intent_id
            )

            if payment_result['status'] == 'succeeded':
                # Платеж успешен - восстановить подписку
                await self.db.subscriptions.update(subscription_id, {
                    'status': SubscriptionStatus.ACTIVE
                })

                # Отметить dunning как успешный
                await self.db.dunning.update({
                    'subscription_id': subscription_id,
                    'payment_intent_id': payment_intent_id
                }, {
                    'status': 'succeeded',
                    'completed_at': datetime.utcnow()
                })

                # Отправить email о восстановлении
                subscription = await self.db.subscriptions.get(subscription_id)
                await self.email.send_subscription_restored_notification(
                    subscription['customer_id']
                )

                return {
                    'success': True,
                    'status': 'active'
                }

            else:
                # Платеж снова не прошел
                return await self.handle_payment_failed(
                    subscription_id,
                    payment_intent_id,
                    payment_result.get('error', 'Payment failed')
                )

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cancel_subscription(
        self,
        subscription_id: str,
        reason: Optional[str] = None,
        at_period_end: bool = False
    ) -> Dict:
        """
        Отменить подписку.

        Args:
            subscription_id: ID подписки
            reason: Причина отмены
            at_period_end: Отменить в конце периода

        Returns:
            Результат отмены
        """
        subscription = await self.db.subscriptions.get(subscription_id)

        # Отменить в payment provider
        cancelled = await self.payment.cancel_subscription(
            subscription_id=subscription['stripe_subscription_id'],
            at_period_end=at_period_end
        )

        # Обновить в БД
        update_data = {
            'status': SubscriptionStatus.CANCELLED,
            'cancelled_at': datetime.utcnow(),
            'cancellation_reason': reason
        }

        if at_period_end:
            update_data['cancel_at_period_end'] = True

        await self.db.subscriptions.update(subscription_id, update_data)

        # Отправить email о отмене
        await self.email.send_subscription_cancelled_notification(
            subscription['customer_id'],
            at_period_end
        )

        return {
            'success': True,
            'status': 'cancelled',
            'cancelled_at': update_data['cancelled_at']
        }

    async def track_usage(
        self,
        subscription_id: str,
        metric: str,
        quantity: int
    ) -> Dict:
        """
        Отслеживать usage для usage-based billing.

        Args:
            subscription_id: ID подписки
            metric: Метрика (например, 'api_calls', 'storage_gb')
            quantity: Количество использования

        Returns:
            Результат tracking
        """
        # Записать usage в БД
        usage = await self.db.usage.create({
            'subscription_id': subscription_id,
            'metric': metric,
            'quantity': quantity,
            'timestamp': datetime.utcnow()
        })

        # Отправить usage в Stripe для billing
        subscription = await self.db.subscriptions.get(subscription_id)

        await self.payment.report_usage(
            subscription_item_id=subscription['stripe_subscription_item_id'],
            quantity=quantity,
            timestamp=usage['timestamp']
        )

        return {
            'success': True,
            'usage_id': usage['id']
        }
```

---

## Marketplace Split Payments

### Platform Fee and Vendor Payouts

```python
class MarketplacePaymentFlow:
    """
    Production-ready Marketplace split payments.

    Используется Stripe Connect для:
    - Разделения платежей между platform и vendors
    - Управления vendor accounts
    - Автоматических выплат vendors
    """

    def __init__(
        self,
        stripe_service,
        db_session
    ):
        self.stripe = stripe_service
        self.db = db_session

        # Platform fee (например, 10%)
        self.platform_fee_percent = Decimal('0.10')

    async def onboard_vendor(
        self,
        vendor_data: Dict
    ) -> Dict:
        """
        Онбординг нового vendor через Stripe Connect.

        Args:
            vendor_data: Данные vendor (email, business details)

        Returns:
            Созданный Connected Account
        """
        # Создать Stripe Connected Account
        connected_account = await self.stripe.create_connected_account(
            type='express',  # или 'standard' для больше контроля vendor
            email=vendor_data['email'],
            country=vendor_data.get('country', 'US'),
            business_type=vendor_data.get('business_type', 'individual')
        )

        # Сохранить в БД
        vendor = await self.db.vendors.create({
            'email': vendor_data['email'],
            'stripe_account_id': connected_account['id'],
            'onboarding_complete': False,
            'created_at': datetime.utcnow()
        })

        # Создать onboarding link
        account_link = await self.stripe.create_account_link(
            account_id=connected_account['id'],
            refresh_url=vendor_data['refresh_url'],
            return_url=vendor_data['return_url'],
            type='account_onboarding'
        )

        return {
            'vendor_id': vendor['id'],
            'stripe_account_id': connected_account['id'],
            'onboarding_url': account_link['url']
        }

    async def process_marketplace_payment(
        self,
        order_id: str,
        vendor_id: str,
        total_amount: Decimal,
        payment_method_id: str,
        customer_id: str
    ) -> Dict:
        """
        Обработать marketplace платеж с split.

        Args:
            order_id: ID заказа
            vendor_id: ID vendor
            total_amount: Общая сумма
            payment_method_id: ID платежного метода
            customer_id: ID клиента

        Returns:
            Результат платежа с split информацией
        """
        # Получить vendor
        vendor = await self.db.vendors.get(vendor_id)

        # Рассчитать platform fee
        platform_fee = total_amount * self.platform_fee_percent
        vendor_amount = total_amount - platform_fee

        # Создать payment с destination charge
        payment = await self.stripe.create_payment_with_destination(
            amount=total_amount,
            currency='USD',
            payment_method_id=payment_method_id,
            customer_id=customer_id,
            destination_account=vendor['stripe_account_id'],
            application_fee_amount=platform_fee,
            metadata={
                'order_id': order_id,
                'vendor_id': vendor_id
            }
        )

        # Сохранить split в БД
        await self.db.payment_splits.create({
            'order_id': order_id,
            'payment_id': payment['id'],
            'vendor_id': vendor_id,
            'total_amount': float(total_amount),
            'platform_fee': float(platform_fee),
            'vendor_amount': float(vendor_amount),
            'created_at': datetime.utcnow()
        })

        return {
            'success': True,
            'payment_id': payment['id'],
            'total_amount': total_amount,
            'platform_fee': platform_fee,
            'vendor_amount': vendor_amount
        }
```

---

## Event-Driven Architecture

### Webhook Processing with Pub/Sub Pattern

```python
from typing import Callable, Dict, List

class PaymentEventBus:
    """
    Event-driven architecture для payment events.

    Используется pub/sub pattern для decoupling.
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(
        self,
        event_type: str,
        handler: Callable
    ) -> None:
        """
        Подписаться на тип события.

        Args:
            event_type: Тип события (например, 'payment.succeeded')
            handler: Функция-обработчик
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(handler)

    async def publish(
        self,
        event_type: str,
        event_data: Dict
    ) -> None:
        """
        Опубликовать событие всем подписчикам.

        Args:
            event_type: Тип события
            event_data: Данные события
        """
        handlers = self.subscribers.get(event_type, [])

        for handler in handlers:
            try:
                await handler(event_data)
            except Exception as e:
                # Логировать ошибку но продолжить обработку
                print(f"Handler error for {event_type}: {str(e)}")

# Пример использования
event_bus = PaymentEventBus()

# Подписка на события
async def send_confirmation_email(event_data):
    """Отправить email после успешного платежа."""
    customer_email = event_data['customer_email']
    order_id = event_data['order_id']
    # Send email...

async def update_inventory(event_data):
    """Обновить inventory после платежа."""
    order_id = event_data['order_id']
    # Update inventory...

event_bus.subscribe('payment.succeeded', send_confirmation_email)
event_bus.subscribe('payment.succeeded', update_inventory)

# Публикация события
await event_bus.publish('payment.succeeded', {
    'order_id': '123',
    'customer_email': 'customer@example.com'
})
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Implementation Engineer
