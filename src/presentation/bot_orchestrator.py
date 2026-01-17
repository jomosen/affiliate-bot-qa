"""Bot orchestration service for managing concurrent execution."""
import asyncio
import random
from typing import List

from loguru import logger

from src.application.factories.bot_config_factory import BotConfigFactory
from src.application.services.customer_data_generator import CustomerDataGenerator
from src.application.use_cases.execute_purchase_simulation import ExecutePurchaseSimulation
from src.domain.models.bot_config import BotConfig
from src.domain.models.order import Order
from src.infrastructure.config.settings import Settings
from src.infrastructure.web.playwright_automation import PlaywrightAutomation


class BotOrchestrator:
    """Orchestrates concurrent bot execution."""

    def __init__(self, settings: Settings):
        """Initialize orchestrator."""
        self.settings = settings
        self.bot_factory = BotConfigFactory(
            affiliate_links=settings.get_affiliate_links_list(),
            coupon_codes=settings.get_coupon_codes_list(),
        )

    async def run_single_bot(self, config: BotConfig) -> Order:
        """Run a single bot instance."""
        logger.info(f"Starting bot {config.bot_id}")

        # Create dependencies
        browser = PlaywrightAutomation(self.settings)
        await browser.initialize()

        customer_generator = CustomerDataGenerator(locale="es_ES")

        # Execute use case
        use_case = ExecutePurchaseSimulation(
            browser_automation=browser,
            customer_generator=customer_generator,
            base_url=self.settings.base_url,
        )

        order = await use_case.execute(config)

        return order

    async def run_concurrent_bots(self, bot_count: int) -> List[Order]:
        """Run multiple bots concurrently with semaphore control."""
        semaphore = asyncio.Semaphore(self.settings.max_concurrent_bots)

        async def run_with_semaphore(bot_id: int) -> Order:
            """Run bot with semaphore control."""
            async with semaphore:
                config = self.bot_factory.create_random_bot(bot_id)
                try:
                    return await self.run_single_bot(config)
                except Exception as e:
                    logger.error(f"Bot {bot_id} failed: {e}")
                    raise

        # Create tasks for all bots
        tasks = [run_with_semaphore(i) for i in range(1, bot_count + 1)]

        # Execute with delays between starts
        results = []
        for task in tasks:
            # Stagger bot starts
            await asyncio.sleep(
                random.uniform(
                    self.settings.bot_delay_min, self.settings.bot_delay_max
                )
            )
            results.append(asyncio.create_task(task))

        # Wait for all to complete
        completed_orders = await asyncio.gather(*results, return_exceptions=True)

        # Filter out exceptions
        successful_orders = [
            order for order in completed_orders if isinstance(order, Order)
        ]

        logger.info(
            f"Completed {len(successful_orders)} / {bot_count} bot executions successfully"
        )

        return successful_orders
