"""Execute purchase simulation use case."""
import asyncio
import random
from typing import Protocol

from loguru import logger

from src.domain.models.bot_config import BotConfig
from src.domain.models.order import CustomerInfo, EntryMethod, Order, OrderItem


class IBrowserAutomation(Protocol):
    """Protocol for browser automation operations."""

    async def navigate(self, url: str) -> None:
        """Navigate to a URL."""
        ...

    async def add_products_to_cart(self, count: int) -> list[OrderItem]:
        """Add random products to cart."""
        ...

    async def update_cart_quantities(self, max_qty: int) -> None:
        """Update quantities in cart."""
        ...

    async def apply_coupon(self, code: str) -> float:
        """Apply coupon and return discount amount."""
        ...

    async def proceed_to_checkout(self) -> None:
        """Navigate to checkout page."""
        ...

    async def fill_checkout_form(self, customer: CustomerInfo) -> None:
        """Fill checkout form with customer data."""
        ...

    async def select_cash_on_delivery(self) -> None:
        """Select COD payment method."""
        ...

    async def accept_terms(self) -> None:
        """Accept terms and conditions."""
        ...

    async def place_order(self) -> str:
        """Submit order and return order number."""
        ...

    async def close(self) -> None:
        """Close browser context."""
        ...


class ICustomerDataGenerator(Protocol):
    """Protocol for generating fake customer data."""

    def generate_customer_info(self) -> CustomerInfo:
        """Generate realistic fake customer information."""
        ...


class ExecutePurchaseSimulation:
    """Use case for executing a complete purchase simulation."""

    def __init__(
        self,
        browser_automation: IBrowserAutomation,
        customer_generator: ICustomerDataGenerator,
        base_url: str,
    ):
        """Initialize the use case with dependencies."""
        self.browser = browser_automation
        self.customer_generator = customer_generator
        self.base_url = base_url

    async def execute(self, config: BotConfig) -> Order:
        """Execute the purchase simulation according to the bot configuration."""
        order = Order()
        order.id = config.bot_id  # type: ignore

        try:
            logger.info(f"Bot {config.bot_id}: Starting purchase simulation")

            # Step 1: Navigate to store
            if config.entry_method == "affiliate_link":
                logger.info(f"Bot {config.bot_id}: Entering via affiliate link")
                order.entry_method = EntryMethod.AFFILIATE_LINK
                order.affiliate_link = config.affiliate_link
                await self.browser.navigate(config.affiliate_link)  # type: ignore
            else:
                logger.info(f"Bot {config.bot_id}: Entering via homepage with coupon")
                order.entry_method = EntryMethod.COUPON_CODE
                order.coupon_code = config.coupon_code
                await self.browser.navigate(self.base_url)

            # Step 2: Browse and add products to cart
            logger.info(f"Bot {config.bot_id}: Adding products to cart")
            items = await self.browser.add_products_to_cart(config.target_product_count)
            for item in items:
                order.add_item(item)

            # Step 3: Randomize quantities
            logger.info(f"Bot {config.bot_id}: Updating cart quantities")
            await self.browser.update_cart_quantities(config.max_quantity_per_product)

            # Step 4: Apply coupon if using coupon entry method (BEFORE checkout)
            if config.entry_method == "coupon_code":
                logger.info(f"Bot {config.bot_id}: Applying coupon {config.coupon_code}")
                discount = await self.browser.apply_coupon(config.coupon_code)  # type: ignore
                order.apply_discount(discount)

            # Step 5: Proceed to checkout
            await self.browser.proceed_to_checkout()

            # Step 6: Fill checkout form with fake data
            logger.info(f"Bot {config.bot_id}: Filling checkout form")
            customer = self.customer_generator.generate_customer_info()
            order.customer_info = customer
            await self.browser.fill_checkout_form(customer)

            # Step 7: Select Cash on Delivery payment
            logger.info(f"Bot {config.bot_id}: Selecting COD payment")
            await self.browser.select_cash_on_delivery()

            # Step 8: Accept terms and place order
            await self.browser.accept_terms()
            logger.info(f"Bot {config.bot_id}: Placing order")
            order_number = await self.browser.place_order()

            # Step 9: Mark order as completed
            order.mark_completed(order_number)
            logger.success(f"Bot {config.bot_id}: Order {order_number} completed successfully")

        except Exception as e:
            logger.error(f"Bot {config.bot_id}: Purchase failed - {str(e)}")
            order.mark_failed(str(e))
            raise

        finally:
            await self.browser.close()

        return order
