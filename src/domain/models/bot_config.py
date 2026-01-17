"""Bot configuration domain model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class BotConfig:
    """Configuration for a single bot instance."""

    bot_id: int
    entry_method: str
    affiliate_link: Optional[str] = None
    coupon_code: Optional[str] = None
    target_product_count: int = 1
    max_quantity_per_product: int = 4

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.entry_method == "affiliate_link" and not self.affiliate_link:
            raise ValueError("Affiliate link required for affiliate entry method")
        if self.entry_method == "coupon_code" and not self.coupon_code:
            raise ValueError("Coupon code required for coupon entry method")
