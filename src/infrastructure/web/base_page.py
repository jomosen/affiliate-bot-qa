"""Page Object Model base class."""
from typing import Optional

from playwright.async_api import Page

from src.application.services.human_simulation import HumanSimulationService


class BasePage:
    """Base class for Page Object Model pattern."""

    def __init__(self, page: Page, human_sim: HumanSimulationService):
        """Initialize with Playwright page and human simulation service."""
        self.page = page
        self.human_sim = human_sim

    async def navigate(self, url: str) -> None:
        """Navigate to URL with human delay."""
        await self.page.goto(url)
        await self.human_sim.delay_action()

    async def click(self, selector: str, timeout: int = 30000) -> None:
        """Click element with human delay."""
        await self.human_sim.delay_action()
        await self.page.click(selector, timeout=timeout)
        await self.human_sim.delay_action()

    async def fill(self, selector: str, text: str, timeout: int = 30000) -> None:
        """Fill input field with human-like typing."""
        await self.human_sim.delay_action()
        await self.page.fill(selector, "", timeout=timeout)  # Clear first
        
        # Type character by character with delays
        for char in text:
            await self.page.type(selector, char)
            await self.human_sim.delay_typing()
        
        await self.human_sim.delay_action()

    async def select_option(self, selector: str, value: str, timeout: int = 30000) -> None:
        """Select option from dropdown with delay."""
        await self.human_sim.delay_action()
        await self.page.select_option(selector, value, timeout=timeout)
        await self.human_sim.delay_action()

    async def check(self, selector: str, timeout: int = 30000) -> None:
        """Check checkbox with delay."""
        await self.human_sim.delay_action()
        await self.page.check(selector, timeout=timeout)
        await self.human_sim.delay_action()

    async def get_text(self, selector: str, timeout: int = 30000) -> str:
        """Get text content of element."""
        element = await self.page.wait_for_selector(selector, timeout=timeout)
        return await element.inner_text() if element else ""

    async def wait_for_selector(
        self, selector: str, state: str = "visible", timeout: int = 30000
    ) -> None:
        """Wait for selector to reach specified state."""
        await self.page.wait_for_selector(selector, state=state, timeout=timeout)  # type: ignore

    async def scroll_randomly(self) -> None:
        """Scroll page randomly to simulate browsing."""
        scroll_amount = self.human_sim.random_scroll_amount()
        await self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        await self.human_sim.delay_action()
