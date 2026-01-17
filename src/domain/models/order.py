"""Order domain model representing a purchase transaction."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EntryMethod(str, Enum):
    """Method used to enter the store."""

    AFFILIATE_LINK = "affiliate_link"
    COUPON_CODE = "coupon_code"
    DIRECT = "direct"


@dataclass
class OrderItem:
    """Individual item within an order."""

    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


@dataclass
class CustomerInfo:
    """Customer information for an order."""

    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    postcode: str


@dataclass
class Order:
    """Domain model representing a complete order."""

    id: UUID = field(default_factory=uuid4)
    order_number: Optional[str] = None
    customer_info: Optional[CustomerInfo] = None
    items: list[OrderItem] = field(default_factory=list)
    subtotal: float = 0.0
    discount: float = 0.0
    total: float = 0.0
    entry_method: EntryMethod = EntryMethod.DIRECT
    affiliate_link: Optional[str] = None
    coupon_code: Optional[str] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order and recalculate total."""
        self.items.append(item)
        self.subtotal += item.total_price
        self._recalculate_total()

    def apply_discount(self, discount: float) -> None:
        """Apply a discount and recalculate total."""
        self.discount = discount
        self._recalculate_total()

    def _recalculate_total(self) -> None:
        """Recalculate order total after changes."""
        self.total = max(0.0, self.subtotal - self.discount)

    def mark_completed(self, order_number: str) -> None:
        """Mark order as completed with the store's order number."""
        self.order_number = order_number
        self.status = OrderStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def mark_failed(self, error: str) -> None:
        """Mark order as failed with error message."""
        self.status = OrderStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.utcnow()
