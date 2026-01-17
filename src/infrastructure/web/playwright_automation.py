"""Playwright browser automation implementation."""
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from src.application.services.customer_data_generator import CustomerDataGenerator
from src.application.services.human_simulation import HumanSimulationService
from src.domain.models.order import CustomerInfo, OrderItem
from src.infrastructure.config.settings import Settings
from src.infrastructure.web.pages.cart_page import CartPage
from src.infrastructure.web.pages.checkout_page import CheckoutPage
from src.infrastructure.web.pages.home_page import HomePage
from src.infrastructure.web.pages.product_page import ProductPage


class PlaywrightAutomation:
    """Playwright implementation of browser automation."""

    def __init__(self, settings: Settings):
        """Initialize with settings."""
        self.settings = settings
        self.playwright = None
        self.browser: Browser = None  # type: ignore
        self.context: BrowserContext = None  # type: ignore
        self.page: Page = None  # type: ignore
        self.human_sim = HumanSimulationService(
            action_delay_mean=settings.action_delay_mean,
            action_delay_std=settings.action_delay_std,
            typing_delay_min=settings.typing_delay_min,
            typing_delay_max=settings.typing_delay_max,
        )

    async def initialize(self) -> None:
        """Initialize Playwright browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.settings.headless,
            slow_mo=self.settings.slow_mo,
        )
        self.context = await self.browser.new_context(
            viewport={
                "width": self.settings.viewport_width,
                "height": self.settings.viewport_height,
            },
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )
        self.page = await self.context.new_page()

    async def navigate(self, url: str) -> None:
        """Navigate to URL."""
        home_page = HomePage(self.page, self.human_sim, self.settings)
        await home_page.navigate(url)

    async def add_products_to_cart(self, count: int) -> list[OrderItem]:
        """Add random products to cart."""
        items = []
        home_page = HomePage(self.page, self.human_sim, self.settings)

        for i in range(count):
            # Add product directly from listing page
            product_name, price = await home_page.add_random_product_to_cart()
            
            item = OrderItem(
                product_id=f"PROD-{i+1}",
                product_name=product_name,
                quantity=1,
                unit_price=price,
                total_price=price,
            )
            items.append(item)
            
            # If we need more products, go back to listing
            if i < count - 1:
                await home_page.go_to_home()

        return items

    async def update_cart_quantities(self, max_qty: int) -> None:
        """Update quantities in cart."""
        # Navigate to cart
        await self.page.goto(f"{self.settings.base_url}/cart")
        cart_page = CartPage(self.page, self.human_sim, self.settings)
        await cart_page.update_quantities(max_qty)

    async def apply_coupon(self, code: str) -> float:
        """Apply coupon and return discount amount."""
        checkout_page = CheckoutPage(self.page, self.human_sim, self.settings)
        return await checkout_page.apply_coupon(code)

    async def proceed_to_checkout(self) -> None:
        """Navigate to checkout page."""
        cart_page = CartPage(self.page, self.human_sim, self.settings)
        await cart_page.proceed_to_checkout()

    async def fill_checkout_form(self, customer: CustomerInfo) -> None:
        """Fill checkout form with customer data."""
        checkout_page = CheckoutPage(self.page, self.human_sim, self.settings)
        await checkout_page.fill_billing_details(customer)

    async def select_cash_on_delivery(self) -> None:
        """Select COD payment method."""
        checkout_page = CheckoutPage(self.page, self.human_sim, self.settings)
        await checkout_page.select_cash_on_delivery()

    async def accept_terms(self) -> None:
        """Accept terms and conditions."""
        checkout_page = CheckoutPage(self.page, self.human_sim, self.settings)
        await checkout_page.accept_terms()

    async def place_order(self) -> str:
        """Submit order and return order number."""
        checkout_page = CheckoutPage(self.page, self.human_sim, self.settings)
        return await checkout_page.place_order()

    async def close(self) -> None:
        """Close browser context."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
