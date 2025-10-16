# Module 03: Payment Security & Compliance

## PCI DSS Compliance, Fraud Detection и Security Best Practices

Этот модуль содержит production-ready паттерны для безопасности платежей, PCI DSS compliance и fraud detection.

---

## PCI DSS Compliance Implementation

### Разница между SAQ-A и SAQ-D

```python
from enum import Enum
from typing import Dict, Optional
import hashlib
import secrets

class PCIComplianceLevel(str, Enum):
    """
    Уровни PCI DSS compliance.

    SAQ-A: Самый простой - используются внешние токенизаторы
    SAQ-D: Самый сложный - обработка карт на своих серверах
    """
    SAQ_A = 'SAQ-A'  # E-commerce only, no card data storage
    SAQ_D = 'SAQ-D'  # Full merchant processing

class PCIComplianceService:
    """
    Сервис для обеспечения PCI DSS compliance.

    Функции:
    - Определение уровня compliance
    - Токенизация карт
    - Безопасное хранение данных
    - Audit logging
    """

    def __init__(self, compliance_level: PCIComplianceLevel):
        """
        Инициализация PCI compliance сервиса.

        Args:
            compliance_level: Уровень compliance (SAQ-A или SAQ-D)
        """
        self.compliance_level = compliance_level

    async def tokenize_card(
        self,
        card_number: str,
        provider: str = 'stripe'
    ) -> Dict:
        """
        Токенизировать карту через внешнего провайдера (SAQ-A подход).

        Args:
            card_number: Номер карты (только для передачи провайдеру)
            provider: Провайдер токенизации ('stripe', 'paypal', 'square')

        Returns:
            Token карты для использования в платежах

        Note:
            При SAQ-A подходе карта НЕ должна касаться ваших серверов.
            Используйте Stripe.js, PayPal SDK или Square Payment Form.
        """
        if self.compliance_level == PCIComplianceLevel.SAQ_A:
            # SAQ-A: Используем внешнюю токенизацию
            # Карта токенизируется на клиенте, мы получаем только token

            return {
                'token_type': 'external',
                'provider': provider,
                'message': 'Используйте клиентскую токенизацию (Stripe.js, PayPal SDK)',
                'compliance': 'SAQ-A'
            }

        else:
            # SAQ-D: Можем обрабатывать карты на сервере
            # НО требуется полное PCI DSS compliance

            raise NotImplementedError(
                "SAQ-D требует полную PCI DSS инфраструктуру. "
                "Рекомендуется использовать SAQ-A с внешней токенизацией."
            )

    async def encrypt_sensitive_data(
        self,
        data: str,
        encryption_key: bytes
    ) -> str:
        """
        Зашифровать чувствительные данные (PCI DSS requirement).

        Args:
            data: Данные для шифрования
            encryption_key: 256-bit AES ключ

        Returns:
            Зашифрованные данные (base64)

        Note:
            Используется только для SAQ-D уровня.
            При SAQ-A данные карт НЕ должны попадать на сервер.
        """
        from cryptography.fernet import Fernet

        if self.compliance_level != PCIComplianceLevel.SAQ_D:
            raise ValueError(
                "Шифрование карт разрешено только при SAQ-D compliance"
            )

        # Создать Fernet шифратор
        f = Fernet(encryption_key)

        # Зашифровать данные
        encrypted_data = f.encrypt(data.encode())

        return encrypted_data.decode()

    async def decrypt_sensitive_data(
        self,
        encrypted_data: str,
        encryption_key: bytes
    ) -> str:
        """
        Расшифровать чувствительные данные.

        Args:
            encrypted_data: Зашифрованные данные (base64)
            encryption_key: 256-bit AES ключ

        Returns:
            Расшифрованные данные
        """
        from cryptography.fernet import Fernet

        if self.compliance_level != PCIComplianceLevel.SAQ_D:
            raise ValueError(
                "Доступ к зашифрованным картам разрешен только при SAQ-D"
            )

        f = Fernet(encryption_key)
        decrypted_data = f.decrypt(encrypted_data.encode())

        return decrypted_data.decode()

    async def mask_card_number(self, card_number: str) -> str:
        """
        Замаскировать номер карты для логирования и отображения.

        Args:
            card_number: Полный номер карты

        Returns:
            Замаскированный номер (например, "**** **** **** 1234")

        Note:
            Даже при SAQ-D нужно маскировать карты в логах и UI.
        """
        # Оставить только последние 4 цифры
        last_four = card_number[-4:]

        # Замаскировать остальное
        masked = f"**** **** **** {last_four}"

        return masked

    async def log_pci_event(
        self,
        event_type: str,
        user_id: str,
        details: Dict,
        ip_address: str
    ) -> None:
        """
        Логировать PCI-релевантное событие для audit trail.

        Args:
            event_type: Тип события ('card_tokenized', 'payment_processed', etc.)
            user_id: ID пользователя
            details: Детали события (без чувствительных данных)
            ip_address: IP адрес запроса

        Note:
            PCI DSS требует audit trail для всех платежных операций.
        """
        import datetime

        # Создать audit log entry
        audit_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip_address,
            'details': details,
            'compliance_level': self.compliance_level.value
        }

        # Сохранить в secure audit log
        # (должен быть защищен от модификации и удаления)
        await self._save_to_audit_log(audit_entry)

    async def _save_to_audit_log(self, entry: Dict) -> None:
        """
        Сохранить запись в immutable audit log.

        Args:
            entry: Audit log entry
        """
        # Реализация зависит от инфраструктуры
        # Можно использовать:
        # - AWS CloudTrail
        # - Azure Monitor
        # - Elasticsearch с WORM storage
        # - Blockchain-based audit log

        pass  # Заглушка для примера
```

---

## Fraud Detection Engine

### Multi-Level Risk Scoring System

```python
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timedelta

class FraudDetectionLevel(str, Enum):
    """Уровни fraud detection."""
    BASIC = 'basic'
    ADVANCED = 'advanced'
    MACHINE_LEARNING = 'machine_learning'

class FraudDetectionEngine:
    """
    Многоуровневый fraud detection engine.

    Уровни защиты:
    - Basic: Velocity limits, blacklists, geolocation
    - Advanced: Device fingerprinting, behavioral analysis, network graph
    - ML: Machine learning модели для предсказания fraud
    """

    def __init__(
        self,
        detection_level: FraudDetectionLevel,
        redis_client=None,
        ml_model=None
    ):
        """
        Инициализация fraud detection engine.

        Args:
            detection_level: Уровень защиты
            redis_client: Redis для хранения метрик (опционально)
            ml_model: ML модель для fraud detection (опционально)
        """
        self.detection_level = detection_level
        self.redis = redis_client
        self.ml_model = ml_model

        # Пороговые значения
        self.velocity_limits = {
            'payments_per_hour': 10,
            'payments_per_day': 50,
            'max_amount_per_hour': Decimal('5000'),
            'max_amount_per_day': Decimal('20000')
        }

    async def analyze_payment(
        self,
        payment_data: Dict
    ) -> Dict:
        """
        Анализировать платеж на fraud.

        Args:
            payment_data: Данные платежа для анализа

        Returns:
            Результат анализа с риск-скором и рекомендацией
        """
        risk_score = 0
        fraud_signals = []

        # BASIC LEVEL CHECKS
        if self.detection_level in [
            FraudDetectionLevel.BASIC,
            FraudDetectionLevel.ADVANCED,
            FraudDetectionLevel.MACHINE_LEARNING
        ]:
            # Check 1: Velocity limits
            velocity_risk = await self.check_velocity_limits(payment_data)
            risk_score += velocity_risk['score']
            if velocity_risk['signals']:
                fraud_signals.extend(velocity_risk['signals'])

            # Check 2: Geolocation anomalies
            geo_risk = await self.check_geolocation(payment_data)
            risk_score += geo_risk['score']
            if geo_risk['signals']:
                fraud_signals.extend(geo_risk['signals'])

            # Check 3: Blacklist check
            blacklist_risk = await self.check_blacklist(payment_data)
            risk_score += blacklist_risk['score']
            if blacklist_risk['signals']:
                fraud_signals.extend(blacklist_risk['signals'])

        # ADVANCED LEVEL CHECKS
        if self.detection_level in [
            FraudDetectionLevel.ADVANCED,
            FraudDetectionLevel.MACHINE_LEARNING
        ]:
            # Check 4: Device fingerprinting
            device_risk = await self.check_device_fingerprint(payment_data)
            risk_score += device_risk['score']
            if device_risk['signals']:
                fraud_signals.extend(device_risk['signals'])

            # Check 5: Behavioral patterns
            behavior_risk = await self.check_behavioral_patterns(payment_data)
            risk_score += behavior_risk['score']
            if behavior_risk['signals']:
                fraud_signals.extend(behavior_risk['signals'])

            # Check 6: Network analysis
            network_risk = await self.check_network_analysis(payment_data)
            risk_score += network_risk['score']
            if network_risk['signals']:
                fraud_signals.extend(network_risk['signals'])

        # MACHINE LEARNING LEVEL
        if self.detection_level == FraudDetectionLevel.MACHINE_LEARNING:
            if self.ml_model:
                ml_score = await self.ml_model.predict(payment_data)
                # Усреднить ML score с rule-based score
                risk_score = (risk_score + ml_score) / 2

                fraud_signals.append(f"ML fraud probability: {ml_score:.2f}")

        # Принять решение на основе риск-скора
        decision = self.make_fraud_decision(risk_score)

        return {
            'risk_score': risk_score,
            'decision': decision,
            'fraud_signals': fraud_signals,
            'detection_level': self.detection_level.value
        }

    async def check_velocity_limits(self, payment_data: Dict) -> Dict:
        """
        Проверить velocity limits (количество платежей за период).

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        user_id = payment_data.get('user_id')
        amount = payment_data.get('amount', Decimal('0'))

        if not self.redis or not user_id:
            return {'score': 0, 'signals': []}

        signals = []
        risk_score = 0

        # Получить количество платежей за час
        hour_key = f'payments:hour:{user_id}:{datetime.utcnow().strftime("%Y%m%d%H")}'
        payments_this_hour = int(self.redis.get(hour_key) or 0)

        if payments_this_hour >= self.velocity_limits['payments_per_hour']:
            risk_score += 20
            signals.append(
                f"Превышен лимит платежей в час: {payments_this_hour}/{self.velocity_limits['payments_per_hour']}"
            )

        # Получить сумму платежей за час
        amount_hour_key = f'amount:hour:{user_id}:{datetime.utcnow().strftime("%Y%m%d%H")}'
        amount_this_hour = Decimal(self.redis.get(amount_hour_key) or '0')

        if amount_this_hour >= self.velocity_limits['max_amount_per_hour']:
            risk_score += 25
            signals.append(
                f"Превышен лимит суммы в час: ${amount_this_hour}/${self.velocity_limits['max_amount_per_hour']}"
            )

        # Обновить счетчики
        self.redis.incr(hour_key)
        self.redis.expire(hour_key, 3600)  # 1 час

        new_amount = amount_this_hour + amount
        self.redis.set(amount_hour_key, str(new_amount), ex=3600)

        return {
            'score': risk_score,
            'signals': signals
        }

    async def check_geolocation(self, payment_data: Dict) -> Dict:
        """
        Проверить геолокацию на аномалии.

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        ip_address = payment_data.get('ip_address')
        user_id = payment_data.get('user_id')

        if not ip_address or not user_id:
            return {'score': 0, 'signals': []}

        signals = []
        risk_score = 0

        # Получить страну из IP
        country = await self._get_country_from_ip(ip_address)

        # Получить обычную страну пользователя
        if self.redis:
            usual_country_key = f'user:country:{user_id}'
            usual_country = self.redis.get(usual_country_key)

            if usual_country and usual_country.decode() != country:
                risk_score += 15
                signals.append(
                    f"Необычная страна: {country} (обычно {usual_country.decode()})"
                )
            elif not usual_country:
                # Сохранить страну как обычную
                self.redis.set(usual_country_key, country)

        # Проверить high-risk страны
        high_risk_countries = ['NG', 'RO', 'BG', 'CN']  # Примеры
        if country in high_risk_countries:
            risk_score += 10
            signals.append(f"High-risk страна: {country}")

        return {
            'score': risk_score,
            'signals': signals
        }

    async def check_blacklist(self, payment_data: Dict) -> Dict:
        """
        Проверить по blacklist (email, IP, карта).

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        email = payment_data.get('email')
        ip_address = payment_data.get('ip_address')
        card_hash = payment_data.get('card_hash')  # Hash последних 4 цифр

        signals = []
        risk_score = 0

        if not self.redis:
            return {'score': 0, 'signals': []}

        # Проверить email blacklist
        if email and self.redis.sismember('blacklist:email', email):
            risk_score += 50
            signals.append(f"Email в blacklist: {email}")

        # Проверить IP blacklist
        if ip_address and self.redis.sismember('blacklist:ip', ip_address):
            risk_score += 40
            signals.append(f"IP в blacklist: {ip_address}")

        # Проверить card blacklist
        if card_hash and self.redis.sismember('blacklist:card', card_hash):
            risk_score += 60
            signals.append(f"Карта в blacklist")

        return {
            'score': risk_score,
            'signals': signals
        }

    async def check_device_fingerprint(self, payment_data: Dict) -> Dict:
        """
        Проверить device fingerprint на аномалии.

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        device_id = payment_data.get('device_id')
        user_id = payment_data.get('user_id')

        if not device_id or not user_id or not self.redis:
            return {'score': 0, 'signals': []}

        signals = []
        risk_score = 0

        # Получить обычные устройства пользователя
        devices_key = f'user:devices:{user_id}'
        known_devices = self.redis.smembers(devices_key)

        if known_devices and device_id not in [d.decode() for d in known_devices]:
            risk_score += 10
            signals.append("Новое устройство")

        # Добавить устройство в список известных
        self.redis.sadd(devices_key, device_id)

        # Проверить сколько разных устройств за последний час
        devices_hour_key = f'devices:hour:{datetime.utcnow().strftime("%Y%m%d%H")}'
        devices_this_hour = self.redis.scard(devices_hour_key)

        if devices_this_hour > 5:
            risk_score += 15
            signals.append(f"Много разных устройств за час: {devices_this_hour}")

        return {
            'score': risk_score,
            'signals': signals
        }

    async def check_behavioral_patterns(self, payment_data: Dict) -> Dict:
        """
        Анализировать поведенческие паттерны.

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        user_id = payment_data.get('user_id')
        amount = payment_data.get('amount', Decimal('0'))

        if not user_id or not self.redis:
            return {'score': 0, 'signals': []}

        signals = []
        risk_score = 0

        # Получить среднюю сумму платежей пользователя
        amounts_key = f'user:amounts:{user_id}'
        amounts = self.redis.lrange(amounts_key, 0, -1)

        if amounts:
            avg_amount = sum(Decimal(a.decode()) for a in amounts) / len(amounts)

            # Если сумма сильно выше средней
            if amount > avg_amount * 3:
                risk_score += 15
                signals.append(
                    f"Необычно большая сумма: ${amount} (средняя ${avg_amount:.2f})"
                )

        # Сохранить текущую сумму в историю
        self.redis.rpush(amounts_key, str(amount))
        self.redis.ltrim(amounts_key, -50, -1)  # Хранить последние 50

        return {
            'score': risk_score,
            'signals': signals
        }

    async def check_network_analysis(self, payment_data: Dict) -> Dict:
        """
        Анализировать network graph (связи между пользователями).

        Args:
            payment_data: Данные платежа

        Returns:
            Риск-скор и сигналы
        """
        # Упрощенный пример network analysis
        # В production можно использовать graph database (Neo4j)

        user_id = payment_data.get('user_id')
        email = payment_data.get('email')
        ip_address = payment_data.get('ip_address')

        if not self.redis:
            return {'score': 0, 'signals': []}

        signals = []
        risk_score = 0

        # Проверить сколько пользователей с того же IP
        if ip_address:
            users_same_ip_key = f'ip:users:{ip_address}'
            users_count = self.redis.scard(users_same_ip_key)

            if users_count > 3:
                risk_score += 20
                signals.append(
                    f"Много пользователей с одного IP: {users_count}"
                )

            self.redis.sadd(users_same_ip_key, user_id)

        return {
            'score': risk_score,
            'signals': signals
        }

    def make_fraud_decision(self, risk_score: float) -> Dict:
        """
        Принять решение на основе риск-скора.

        Args:
            risk_score: Итоговый риск-скор (0-100)

        Returns:
            Решение и рекомендация
        """
        if risk_score < 30:
            return {
                'action': 'approve',
                'risk': 'low',
                'message': 'Платеж одобрен автоматически'
            }
        elif risk_score < 70:
            return {
                'action': 'review',
                'risk': 'medium',
                'message': 'Платеж требует ручной проверки'
            }
        else:
            return {
                'action': 'decline',
                'risk': 'high',
                'message': 'Платеж отклонен из-за высокого риска fraud'
            }

    async def _get_country_from_ip(self, ip_address: str) -> str:
        """
        Получить страну из IP адреса.

        Args:
            ip_address: IP адрес

        Returns:
            ISO код страны
        """
        # Можно использовать:
        # - MaxMind GeoIP2
        # - IP2Location
        # - ipapi.co API

        # Заглушка для примера
        return 'US'

    async def add_to_blacklist(
        self,
        blacklist_type: str,
        value: str,
        reason: str
    ) -> None:
        """
        Добавить в blacklist.

        Args:
            blacklist_type: Тип ('email', 'ip', 'card')
            value: Значение для blacklist
            reason: Причина добавления
        """
        if not self.redis:
            raise ValueError("Redis required for blacklist")

        blacklist_key = f'blacklist:{blacklist_type}'
        self.redis.sadd(blacklist_key, value)

        # Логировать причину
        reason_key = f'blacklist:reason:{blacklist_type}:{value}'
        self.redis.set(reason_key, reason)
```

---

## Card Data Encryption

### AES-256 шифрование для SAQ-D уровня

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class CardEncryptionService:
    """
    Сервис для шифрования карт (только для SAQ-D).

    Note:
        Рекомендуется использовать SAQ-A подход с внешней токенизацией.
        Шифрование карт на своих серверах требует full PCI DSS compliance.
    """

    def __init__(self, master_key: bytes):
        """
        Инициализация с master encryption key.

        Args:
            master_key: 256-bit master key для шифрования
        """
        self.master_key = master_key

    def generate_encryption_key(self, salt: bytes = None) -> bytes:
        """
        Сгенерировать encryption key из master key.

        Args:
            salt: Salt для key derivation (опционально)

        Returns:
            256-bit Fernet key
        """
        if salt is None:
            salt = os.urandom(16)

        # Derive key using PBKDF2
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))

        return key

    async def encrypt_card(
        self,
        card_number: str,
        encryption_key: bytes
    ) -> str:
        """
        Зашифровать номер карты.

        Args:
            card_number: Номер карты (plain text)
            encryption_key: Fernet encryption key

        Returns:
            Зашифрованный номер карты (base64)
        """
        f = Fernet(encryption_key)
        encrypted = f.encrypt(card_number.encode())

        return encrypted.decode()

    async def decrypt_card(
        self,
        encrypted_card: str,
        encryption_key: bytes
    ) -> str:
        """
        Расшифровать номер карты.

        Args:
            encrypted_card: Зашифрованный номер (base64)
            encryption_key: Fernet encryption key

        Returns:
            Номер карты (plain text)
        """
        f = Fernet(encryption_key)
        decrypted = f.decrypt(encrypted_card.encode())

        return decrypted.decode()
```

---

## Compliance Requirements

### GDPR, PSD2, KYC/AML Implementation

```python
class ComplianceService:
    """
    Сервис для обеспечения regulatory compliance.

    Поддержка:
    - GDPR (право на забвение, data export)
    - PSD2 (Strong Customer Authentication)
    - KYC/AML (проверка личности, мониторинг транзакций)
    """

    async def process_gdpr_deletion_request(
        self,
        user_id: str
    ) -> Dict:
        """
        Обработать GDPR запрос на удаление данных.

        Args:
            user_id: ID пользователя

        Returns:
            Результат удаления
        """
        # Удалить или анонимизировать PII (Personally Identifiable Information)
        # Сохранить только необходимые для compliance данные

        steps_completed = []

        # 1. Анонимизировать платежные данные
        await self._anonymize_payment_history(user_id)
        steps_completed.append('payment_history_anonymized')

        # 2. Удалить сохраненные платежные методы
        await self._delete_payment_methods(user_id)
        steps_completed.append('payment_methods_deleted')

        # 3. Экспортировать данные перед удалением (если запрошено)
        # ...

        return {
            'user_id': user_id,
            'status': 'completed',
            'steps': steps_completed
        }

    async def _anonymize_payment_history(self, user_id: str) -> None:
        """Анонимизировать историю платежей."""
        # Заменить user_id на anonymous ID
        # Удалить email, имя, адрес
        # Сохранить только aggregated данные для финансовой отчетности
        pass

    async def _delete_payment_methods(self, user_id: str) -> None:
        """Удалить сохраненные платежные методы."""
        # Удалить tokens из Stripe/PayPal/Square
        # Удалить из локальной БД
        pass
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Implementation Engineer
