"""Product page object."""
import random

from src.domain.models.order import OrderItem
from src.infrastructure.config.settings import Settings
from src.infrastructure.web.base_page import BasePage


class ProductPage(BasePage):
    """Page Object for product detail pages."""

    def __init__(self, page, human_sim, settings: Settings):
        """Initialize with settings for selectors."""
        super().__init__(page, human_sim)
        self.settings = settings

    async def add_to_cart(self) -> OrderItem:
        """Add product to cart and return order item details."""
        # Get product information (this is simplified - adapt to actual store)
        product_name = await self.get_text("h1.product_title, .product-title")
        
        # Extract price (simplified)
        price_text = await self.get_text(".price .amount, .product-price")
        price = self._parse_price(price_text)

        # Click add to cart
        selectors = self.settings.selector_add_to_cart_button.split(",")
        for selector in selectors:
            try:
                await self.click(selector.strip(), timeout=5000)
                break
            except Exception:
                continue

        # Wait for cart update
        await self.human_sim.delay_action(min_delay=2.0)

        return OrderItem(
            product_id=f"PROD-{random.randint(1000, 9999)}",
            product_name=product_name or "Unknown Product",
            quantity=1,
            unit_price=price,
            total_price=price,
        )

    def _parse_price(self, price_text: str) -> float:
        """Parse price from text string."""
        # Remove currency symbols and convert to float
        import re

        numbers = re.findall(r"[\d,]+\.?\d*", price_text.replace(",", ""))
        return float(numbers[0]) if numbers else 10.0
