"""Human simulation service for realistic delays and interactions."""
import asyncio
import random
from typing import Optional


class HumanSimulationService:
    """Service to simulate human-like behavior with realistic delays."""

    def __init__(
        self,
        action_delay_mean: float = 1.5,
        action_delay_std: float = 0.5,
        typing_delay_min: int = 50,
        typing_delay_max: int = 150,
    ):
        """Initialize with delay parameters."""
        self.action_delay_mean = action_delay_mean
        self.action_delay_std = action_delay_std
        self.typing_delay_min = typing_delay_min
        self.typing_delay_max = typing_delay_max

    async def delay_action(self, min_delay: Optional[float] = None) -> None:
        """Add realistic delay between actions using Gaussian distribution."""
        if min_delay is not None:
            delay = max(min_delay, random.gauss(self.action_delay_mean, self.action_delay_std))
        else:
            delay = max(0.5, random.gauss(self.action_delay_mean, self.action_delay_std))

        await asyncio.sleep(delay)

    async def delay_typing(self) -> None:
        """Add realistic delay for typing a single character."""
        delay = random.randint(self.typing_delay_min, self.typing_delay_max) / 1000.0
        await asyncio.sleep(delay)

    async def type_text_humanly(self, text: str) -> list[str]:
        """
        Return list of characters with delays for human-like typing.
        Returns characters to be typed with delays applied.
        """
        chars = []
        for char in text:
            await self.delay_typing()
            chars.append(char)
        return chars

    def random_quantity(self, max_qty: int = 4) -> int:
        """Generate random quantity between 1 and max_qty."""
        return random.randint(1, max_qty)

    def random_scroll_amount(self, max_scroll: int = 1000) -> int:
        """Generate random scroll amount for browsing simulation."""
        return random.randint(100, max_scroll)
