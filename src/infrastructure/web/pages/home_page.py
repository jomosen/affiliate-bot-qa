"""Home page object."""
import random

from src.infrastructure.config.settings import Settings
from src.infrastructure.web.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the store's home page."""

    def __init__(self, page, human_sim, settings: Settings):
        """Initialize with settings for selectors."""
        super().__init__(page, human_sim)
        self.settings = settings

    async def go_to_home(self) -> None:
        """Navigate to the home page."""
        await self.navigate(self.settings.base_url)

    async def browse_products(self) -> None:
        """Simulate browsing by scrolling and random delays."""
        await self.scroll_randomly()
        await self.human_sim.delay_action(min_delay=2.0)
        await self.scroll_randomly()

    async def add_random_product_to_cart(self) -> tuple[str, float]:
        """Click add to cart button on a random product from listing and return product info."""
        # Wait for page to load
        await self.page.wait_for_load_state("networkidle", timeout=60000)
        
        # Try multiple selectors (comma-separated in settings)
        selectors = [s.strip() for s in self.settings.selector_add_to_cart_button.split(",")]
        add_to_cart_buttons = []
        
        for selector in selectors:
            buttons = await self.page.query_selector_all(selector)
            if buttons:
                add_to_cart_buttons.extend(buttons)
                break
        
        if not add_to_cart_buttons:
            raise Exception(
                f"No 'Add to cart' buttons found with any selector: {self.settings.selector_add_to_cart_button}"
            )
        
        # Select a random product's add to cart button
        button = random.choice(add_to_cart_buttons)
        
        # Get product name and price from the product container
        try:
            # Find parent product container
            product_container = await button.evaluate_handle("btn => btn.closest('li.product, .product-item, .product')")
            
            # Extract product name
            name_element = await product_container.query_selector("h2, .product-title, .woocommerce-loop-product__title")
            product_name = await name_element.inner_text() if name_element else "Unknown Product"
            
            # Extract price
            price_element = await product_container.query_selector(".price .amount, .price ins .amount, .price")
            price_text = await price_element.inner_text() if price_element else "0"
            price = self._parse_price(price_text)
        except Exception:
            product_name = "Unknown Product"
            price = 10.0
        
        # Click add to cart button
        await self.human_sim.delay_action()
        await button.click()
        
        # Wait for cart notification or redirect
        await self.human_sim.delay_action(min_delay=2.0)
        
        return product_name, price
    
    def _parse_price(self, price_text: str) -> float:
        """Parse price from text string."""
        import re
        # Remove currency symbols and extract numbers
        numbers = re.findall(r"[\d,]+\.?\d*", price_text.replace(",", ""))
        return float(numbers[0]) if numbers else 10.0
