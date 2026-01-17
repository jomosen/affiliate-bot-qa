"""Unit tests for Order domain model."""
import pytest
from datetime import datetime

from src.domain.models.order import (
    CustomerInfo,
    EntryMethod,
    Order,
    OrderItem,
    OrderStatus,
)


class TestOrder:
    """Test cases for Order domain model."""

    def test_order_creation_defaults(self) -> None:
        """Test order is created with correct defaults."""
        order = Order()

        assert order.id is not None
        assert order.order_number is None
        assert order.status == OrderStatus.PENDING
        assert order.entry_method == EntryMethod.DIRECT
        assert order.subtotal == 0.0
        assert order.discount == 0.0
        assert order.total == 0.0
        assert len(order.items) == 0

    def test_add_item_updates_totals(self) -> None:
        """Test adding items correctly updates order totals."""
        order = Order()
        item = OrderItem(
            product_id="P1",
            product_name="Test Product",
            quantity=2,
            unit_price=10.0,
            total_price=20.0,
        )

        order.add_item(item)

        assert len(order.items) == 1
        assert order.subtotal == 20.0
        assert order.total == 20.0

    def test_apply_discount(self) -> None:
        """Test discount application recalculates total."""
        order = Order()
        item = OrderItem(
            product_id="P1",
            product_name="Test Product",
            quantity=1,
            unit_price=100.0,
            total_price=100.0,
        )
        order.add_item(item)

        order.apply_discount(25.0)

        assert order.discount == 25.0
        assert order.total == 75.0

    def test_mark_completed(self) -> None:
        """Test marking order as completed."""
        order = Order()
        order_number = "ORD-12345"

        order.mark_completed(order_number)

        assert order.status == OrderStatus.COMPLETED
        assert order.order_number == order_number
        assert order.completed_at is not None

    def test_mark_failed(self) -> None:
        """Test marking order as failed."""
        order = Order()
        error_msg = "Payment failed"

        order.mark_failed(error_msg)

        assert order.status == OrderStatus.FAILED
        assert order.error_message == error_msg
        assert order.completed_at is not None
