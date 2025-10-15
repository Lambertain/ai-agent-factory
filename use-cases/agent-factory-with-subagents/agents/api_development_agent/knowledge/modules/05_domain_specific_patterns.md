# Module 05: Domain-Specific Patterns

## API паттерны для специфических доменов

Этот модуль содержит production-ready паттерны для различных доменов: E-commerce, Fintech, и Healthcare.

---

## E-commerce API Patterns

### Shopping Cart Management

```python
from datetime import datetime
from typing import List, Dict
import redis
import json

class ShoppingCartService:
    """
    Production-ready shopping cart service with Redis.
    """

    def __init__(self, redis_client: redis.Redis, db_session):
        self.redis = redis_client
        self.db = db_session

    async def add_to_cart(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ) -> Dict:
        """
        Add product to shopping cart.

        Args:
            user_id: User identifier
            product_id: Product to add
            quantity: Quantity to add

        Returns:
            Updated cart summary
        """
        # Validate product availability
        product = await self.db.get_product(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        if product.stock < quantity:
            raise HTTPException(
                400,
                f"Insufficient stock. Available: {product.stock}"
            )

        # Update cart in Redis
        cart_key = f"cart:{user_id}"
        cart_item = {
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity,
            "price": float(product.price),
            "added_at": datetime.utcnow().isoformat()
        }

        self.redis.hset(cart_key, str(product_id), json.dumps(cart_item))
        self.redis.expire(cart_key, 3600 * 24 * 7)  # 7 days expiry

        return {
            "success": True,
            "cart_total": await self.calculate_total(user_id)
        }

    async def remove_from_cart(self, user_id: int, product_id: int):
        """Remove product from cart."""
        cart_key = f"cart:{user_id}"
        self.redis.hdel(cart_key, str(product_id))

        return {"success": True}

    async def get_cart_items(self, user_id: int) -> List[Dict]:
        """Get all items in cart."""
        cart_key = f"cart:{user_id}"
        cart_data = self.redis.hgetall(cart_key)

        items = []
        for product_id, item_json in cart_data.items():
            item = json.loads(item_json)
            items.append(item)

        return items

    async def calculate_total(
        self,
        user_id: int,
        tax_rate: float = 0.08,
        shipping: float = 0
    ) -> Dict:
        """
        Calculate cart total with tax and shipping.

        Args:
            user_id: User identifier
            tax_rate: Tax rate (default: 8%)
            shipping: Shipping cost

        Returns:
            Total breakdown
        """
        cart_items = await self.get_cart_items(user_id)

        subtotal = sum(
            item["price"] * item["quantity"]
            for item in cart_items
        )

        tax = subtotal * tax_rate
        total = subtotal + tax + shipping

        return {
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "shipping": round(shipping, 2),
            "total": round(total, 2),
            "items_count": len(cart_items)
        }

    async def checkout(self, user_id: int, payment_method: str) -> Dict:
        """
        Process checkout.

        Args:
            user_id: User identifier
            payment_method: Payment method

        Returns:
            Order details
        """
        # Get cart items
        cart_items = await self.get_cart_items(user_id)

        if not cart_items:
            raise HTTPException(400, "Cart is empty")

        # Calculate total
        totals = await self.calculate_total(user_id)

        # Create order in database
        order = await self.db.create_order(
            user_id=user_id,
            items=cart_items,
            total=totals["total"],
            payment_method=payment_method
        )

        # Clear cart after successful checkout
        cart_key = f"cart:{user_id}"
        self.redis.delete(cart_key)

        return {
            "order_id": order.id,
            "status": "pending",
            "total": totals["total"]
        }
```

---

## Fintech Security Patterns

### PCI DSS Compliant Payment Processing

```python
import uuid
from datetime import datetime
from typing import Dict

class PaymentProcessor:
    """
    PCI DSS compliant payment processor.
    Handles sensitive card data securely.
    """

    def __init__(self, encryption_service, payment_gateway, audit_logger):
        self.encryption = encryption_service
        self.gateway = payment_gateway
        self.audit = audit_logger

    async def process_payment(self, payment_data: Dict) -> Dict:
        """
        Process payment with full audit trail.

        Args:
            payment_data: Payment information

        Returns:
            Payment result
        """
        # Validate and sanitize input
        validated_data = self.validate_payment_data(payment_data)

        # Generate transaction ID
        transaction_id = str(uuid.uuid4())

        # Encrypt sensitive card data (PCI DSS requirement)
        encrypted_card = self.encryption.encrypt_card_data(
            validated_data["card_number"]
        )

        # Create comprehensive audit trail
        audit_entry = {
            "transaction_id": transaction_id,
            "user_id": validated_data["user_id"],
            "amount": validated_data["amount"],
            "currency": validated_data.get("currency", "USD"),
            "timestamp": datetime.utcnow(),
            "ip_address": self.get_client_ip(),
            "encrypted_card_last4": encrypted_card[-4:],
            "merchant_id": validated_data.get("merchant_id")
        }

        # Log audit entry before processing
        await self.audit.log_payment_attempt(audit_entry)

        # Process with payment gateway
        try:
            result = await self.gateway.charge(
                amount=validated_data["amount"],
                card_token=encrypted_card,
                metadata=audit_entry,
                idempotency_key=transaction_id  # Prevent duplicate charges
            )

            # Log successful payment
            await self.audit.log_payment_success({
                **audit_entry,
                "gateway_transaction_id": result["id"],
                "status": "success"
            })

            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway_transaction_id": result["id"],
                "status": "approved"
            }

        except PaymentException as e:
            # Log failed payment
            await self.audit.log_payment_failure({
                **audit_entry,
                "error": str(e),
                "status": "failed"
            })

            raise HTTPException(
                status_code=402,
                detail=f"Payment failed: {str(e)}"
            )

    def validate_payment_data(self, data: Dict) -> Dict:
        """
        Validate payment data (PCI DSS requirement).

        Args:
            data: Payment information

        Returns:
            Validated data

        Raises:
            ValueError: If validation fails
        """
        required_fields = ["user_id", "amount", "card_number", "cvv", "expiry"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate card number (Luhn algorithm)
        if not self._validate_luhn(data["card_number"]):
            raise ValueError("Invalid card number")

        # Validate amount
        if data["amount"] <= 0:
            raise ValueError("Amount must be positive")

        return data

    def _validate_luhn(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm."""
        digits = [int(d) for d in str(card_number)]
        checksum = 0

        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit

        return checksum % 10 == 0

    async def refund_payment(
        self,
        transaction_id: str,
        amount: float,
        reason: str
    ) -> Dict:
        """
        Process refund with audit trail.

        Args:
            transaction_id: Original transaction ID
            amount: Refund amount
            reason: Refund reason

        Returns:
            Refund result
        """
        # Get original transaction
        original_tx = await self.audit.get_transaction(transaction_id)

        if not original_tx:
            raise HTTPException(404, "Transaction not found")

        # Validate refund amount
        if amount > original_tx["amount"]:
            raise HTTPException(400, "Refund amount exceeds original")

        # Process refund
        refund_id = str(uuid.uuid4())

        try:
            result = await self.gateway.refund(
                original_transaction_id=original_tx["gateway_transaction_id"],
                amount=amount,
                metadata={"refund_id": refund_id, "reason": reason}
            )

            # Log refund
            await self.audit.log_refund({
                "refund_id": refund_id,
                "original_transaction_id": transaction_id,
                "amount": amount,
                "reason": reason,
                "timestamp": datetime.utcnow(),
                "status": "success"
            })

            return {
                "success": True,
                "refund_id": refund_id,
                "status": "approved"
            }

        except Exception as e:
            await self.audit.log_refund_failure({
                "refund_id": refund_id,
                "error": str(e)
            })
            raise
```

---

## Healthcare HIPAA Compliance

### HIPAA-Compliant Patient Data Handling

```python
from datetime import datetime
from typing import Dict, List

class PatientDataService:
    """
    HIPAA-compliant patient data service.
    Implements minimum necessary principle and audit logging.
    """

    def __init__(self, encryption_service, audit_service, db_session):
        self.encryption = encryption_service
        self.audit = audit_service
        self.db = db_session

    async def get_patient_record(
        self,
        patient_id: int,
        requesting_user: User
    ) -> Dict:
        """
        Retrieve patient record with HIPAA compliance.

        Args:
            patient_id: Patient identifier
            requesting_user: User requesting the data

        Returns:
            Filtered patient record based on user role

        Raises:
            HTTPException: If access denied
        """
        # Check authorization (HIPAA requirement)
        if not self.can_access_patient_data(requesting_user, patient_id):
            # Log unauthorized access attempt
            await self.audit.log_unauthorized_access(
                user_id=requesting_user.id,
                patient_id=patient_id,
                timestamp=datetime.utcnow(),
                ip_address=self.get_client_ip()
            )

            raise HTTPException(403, "Access denied to patient data")

        # Log authorized PHI access (HIPAA requirement)
        await self.audit.log_phi_access(
            user_id=requesting_user.id,
            patient_id=patient_id,
            access_type="read",
            purpose="patient_care",
            timestamp=datetime.utcnow()
        )

        # Retrieve encrypted patient record
        encrypted_record = await self.db.get_patient_record(patient_id)

        if not encrypted_record:
            raise HTTPException(404, "Patient not found")

        # Decrypt PHI (Protected Health Information)
        decrypted_record = self.encryption.decrypt_phi(encrypted_record)

        # Apply minimum necessary principle (HIPAA requirement)
        filtered_record = self.filter_phi_by_role(
            decrypted_record,
            requesting_user.role
        )

        return filtered_record

    def can_access_patient_data(self, user: User, patient_id: int) -> bool:
        """
        Check if user can access patient data.

        Args:
            user: User requesting access
            patient_id: Patient identifier

        Returns:
            True if access allowed
        """
        # Role-based access control
        if user.role in ["doctor", "nurse"]:
            # Check if user is assigned to patient's care team
            return self.db.check_patient_assignment(user.id, patient_id)

        elif user.role == "admin":
            # Admins have access but limited data
            return True

        elif user.role == "patient" and user.patient_id == patient_id:
            # Patients can access their own records
            return True

        else:
            return False

    def filter_phi_by_role(self, record: Dict, role: str) -> Dict:
        """
        Filter PHI based on minimum necessary principle.

        Args:
            record: Full patient record
            role: User role

        Returns:
            Filtered record with only necessary information
        """
        if role == "doctor":
            # Doctors see full medical information
            return record

        elif role == "nurse":
            # Nurses see care-relevant information
            return {
                "patient_id": record["patient_id"],
                "name": record["name"],
                "dob": record["dob"],
                "allergies": record["allergies"],
                "current_medications": record["current_medications"],
                "vital_signs": record["vital_signs"],
                "care_plan": record["care_plan"]
            }

        elif role == "admin":
            # Admins see demographic and administrative info only
            return {
                "patient_id": record["patient_id"],
                "name": record["name"],
                "dob": record["dob"],
                "insurance": record["insurance"],
                "contact": record["contact"]
            }

        elif role == "patient":
            # Patients see their own data
            return record

        else:
            return {}

    async def update_patient_record(
        self,
        patient_id: int,
        updates: Dict,
        requesting_user: User
    ) -> Dict:
        """
        Update patient record with audit trail.

        Args:
            patient_id: Patient identifier
            updates: Fields to update
            requesting_user: User making the update

        Returns:
            Updated record
        """
        # Check write permission
        if not self.can_modify_patient_data(requesting_user, patient_id):
            raise HTTPException(403, "No permission to modify patient data")

        # Log PHI modification
        await self.audit.log_phi_modification(
            user_id=requesting_user.id,
            patient_id=patient_id,
            modified_fields=list(updates.keys()),
            timestamp=datetime.utcnow()
        )

        # Encrypt updated data
        encrypted_updates = self.encryption.encrypt_phi(updates)

        # Update in database
        updated_record = await self.db.update_patient_record(
            patient_id,
            encrypted_updates
        )

        return self.filter_phi_by_role(updated_record, requesting_user.role)

    def can_modify_patient_data(self, user: User, patient_id: int) -> bool:
        """Check if user can modify patient data."""
        return user.role in ["doctor", "nurse"] and \
               self.db.check_patient_assignment(user.id, patient_id)
```

---

**Версия:** 1.0
**Дата создания:** 2025-10-15
**Автор:** Archon Blueprint Architect
