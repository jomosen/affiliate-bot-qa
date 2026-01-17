"""Factory for creating bot configurations."""
import random
from typing import Optional

from src.domain.models.bot_config import BotConfig


class BotConfigFactory:
    """Factory to create bot configurations with randomized behaviors."""

    def __init__(
        self,
        affiliate_links: list[str],
        coupon_codes: list[str],
        max_products: int = 3,
        max_quantity: int = 4,
    ):
        """Initialize factory with available options."""
        self.affiliate_links = affiliate_links
        self.coupon_codes = coupon_codes
        self.max_products = max_products
        self.max_quantity = max_quantity

    def create_random_bot(self, bot_id: int) -> BotConfig:
        """
        Create a bot with randomly selected entry method.
        50% affiliate link, 50% coupon code.
        """
        entry_method = random.choice(["affiliate_link", "coupon_code"])

        affiliate_link: Optional[str] = None
        coupon_code: Optional[str] = None

        if entry_method == "affiliate_link":
            affiliate_link = random.choice(self.affiliate_links)
        else:
            coupon_code = random.choice(self.coupon_codes)

        return BotConfig(
            bot_id=bot_id,
            entry_method=entry_method,
            affiliate_link=affiliate_link,
            coupon_code=coupon_code,
            target_product_count=random.randint(1, self.max_products),
            max_quantity_per_product=self.max_quantity,
        )

    def create_affiliate_bot(self, bot_id: int, affiliate_link: Optional[str] = None) -> BotConfig:
        """Create a bot configured to use affiliate link entry."""
        link = affiliate_link or random.choice(self.affiliate_links)
        return BotConfig(
            bot_id=bot_id,
            entry_method="affiliate_link",
            affiliate_link=link,
            target_product_count=random.randint(1, self.max_products),
            max_quantity_per_product=self.max_quantity,
        )

    def create_coupon_bot(self, bot_id: int, coupon_code: Optional[str] = None) -> BotConfig:
        """Create a bot configured to use coupon code entry."""
        code = coupon_code or random.choice(self.coupon_codes)
        return BotConfig(
            bot_id=bot_id,
            entry_method="coupon_code",
            coupon_code=code,
            target_product_count=random.randint(1, self.max_products),
            max_quantity_per_product=self.max_quantity,
        )
