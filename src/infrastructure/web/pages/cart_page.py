"""Cart page object."""
from src.infrastructure.config.settings import Settings
from src.infrastructure.web.base_page import BasePage


class CartPage(BasePage):
    """Page Object for the shopping cart page."""

    def __init__(self, page, human_sim, settings: Settings):
        """Initialize with settings for selectors."""
        super().__init__(page, human_sim)
        self.settings = settings

    async def update_quantities(self, max_qty: int) -> None:
        """Update cart item quantities randomly."""
        quantity_inputs = await self.page.query_selector_all(
            self.settings.selector_cart_quantity_input
        )

        for input_field in quantity_inputs:
            new_qty = self.human_sim.random_quantity(max_qty)
            await self.human_sim.delay_action()
            await input_field.fill(str(new_qty))

        # Click update cart button if it exists
        try:
            await self.click('button[name="update_cart"]', timeout=3000)
        except Exception:
            pass  # Some stores auto-update

        await self.human_sim.delay_action(min_delay=2.0)

    async def proceed_to_checkout(self) -> None:
        """Click proceed to checkout button."""
        selectors = self.settings.selector_proceed_to_checkout.split(",")
        for selector in selectors:
            try:
                await self.click(selector.strip(), timeout=5000)
                break
            except Exception:
                continue

        await self.human_sim.delay_action(min_delay=2.0)
