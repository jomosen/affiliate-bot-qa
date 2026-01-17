"""Checkout page object."""
from src.domain.models.order import CustomerInfo
from src.infrastructure.config.settings import Settings
from src.infrastructure.web.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for the checkout page."""

    def __init__(self, page, human_sim, settings: Settings):
        """Initialize with settings for selectors."""
        super().__init__(page, human_sim)
        self.settings = settings

    async def apply_coupon(self, coupon_code: str) -> float:
        """Apply coupon code and return discount amount."""
        try:
            await self.fill(self.settings.selector_coupon_code_input, coupon_code)
            await self.click(self.settings.selector_apply_coupon_button)
            await self.human_sim.delay_action(min_delay=3.0)

            # Try to get discount amount (simplified)
            discount_text = await self.get_text(".cart-discount, .coupon-discount")
            return self._parse_discount(discount_text)
        except Exception:
            return 0.0

    async def fill_billing_details(self, customer: CustomerInfo) -> None:
        """Fill all billing form fields with customer information."""
        await self.fill(self.settings.selector_billing_first_name, customer.first_name)
        await self.fill(self.settings.selector_billing_last_name, customer.last_name)
        await self.fill(self.settings.selector_billing_email, customer.email)
        await self.fill(self.settings.selector_billing_phone, customer.phone)
        await self.fill(self.settings.selector_billing_address, customer.address)
        await self.fill(self.settings.selector_billing_city, customer.city)
        await self.fill(self.settings.selector_billing_postcode, customer.postcode)

    async def select_cash_on_delivery(self) -> None:
        """Select COD payment method."""
        await self.click(self.settings.selector_payment_method_cod)
        await self.human_sim.delay_action()

    async def accept_terms(self) -> None:
        """Check terms and conditions checkbox."""
        try:
            await self.check(self.settings.selector_terms_checkbox)
        except Exception:
            pass  # Terms checkbox might not always be present

    async def place_order(self) -> str:
        """Click place order button and extract order number."""
        await self.click(self.settings.selector_place_order_button)
        await self.human_sim.delay_action(min_delay=5.0)

        # Wait for order received page
        await self.wait_for_selector(self.settings.selector_order_received, timeout=30000)

        # Extract order number (simplified)
        order_text = await self.get_text(
            ".woocommerce-order-number, .order-number, strong"
        )
        return self._extract_order_number(order_text)

    def _parse_discount(self, discount_text: str) -> float:
        """Parse discount amount from text."""
        import re

        numbers = re.findall(r"[\d,]+\.?\d*", discount_text.replace(",", ""))
        return float(numbers[0]) if numbers else 0.0

    def _extract_order_number(self, text: str) -> str:
        """Extract order number from text."""
        import re

        match = re.search(r"#?(\d+)", text)
        return match.group(1) if match else f"ORD-{id(text) % 10000}"
