"""Configuration management using pydantic-settings."""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Store Configuration
    base_url: str = Field(default="https://example-store.com")
    store_name: str = Field(default="Example Store")

    # Concurrency Settings
    max_concurrent_bots: int = Field(default=5, ge=1, le=50)
    bot_delay_min: int = Field(default=2)
    bot_delay_max: int = Field(default=8)

    # Affiliate and Coupon Configuration
    affiliate_links: str = Field(default="")
    coupon_codes: str = Field(default="")

    # Browser Configuration
    headless: bool = Field(default=False)
    slow_mo: int = Field(default=100)
    viewport_width: int = Field(default=1920)
    viewport_height: int = Field(default=1080)

    # Human Simulation Settings
    action_delay_mean: float = Field(default=1.5)
    action_delay_std: float = Field(default=0.5)
    typing_delay_min: int = Field(default=50)
    typing_delay_max: int = Field(default=150)

    # Timeouts (milliseconds)
    page_load_timeout: int = Field(default=60000)
    element_timeout: int = Field(default=30000)

    # CSS Selectors Hub
    selector_product_link: str = Field(default="a.product, .product-link, .woocommerce-LoopProduct-link")
    selector_add_to_cart_button: str = Field(default="button.add-to-cart")
    selector_cart_quantity_input: str = Field(default="input.qty")
    selector_proceed_to_checkout: str = Field(default="a.checkout-button")
    selector_billing_first_name: str = Field(default="#billing_first_name")
    selector_billing_last_name: str = Field(default="#billing_last_name")
    selector_billing_email: str = Field(default="#billing_email")
    selector_billing_phone: str = Field(default="#billing_phone")
    selector_billing_address: str = Field(default="#billing_address_1")
    selector_billing_city: str = Field(default="#billing_city")
    selector_billing_postcode: str = Field(default="#billing_postcode")
    selector_coupon_code_input: str = Field(default="#coupon_code")
    selector_apply_coupon_button: str = Field(default='button[name="apply_coupon"]')
    selector_payment_method_cod: str = Field(default="#payment_method_cod")
    selector_terms_checkbox: str = Field(default="#terms")
    selector_place_order_button: str = Field(default="#place_order")
    selector_order_received: str = Field(default=".woocommerce-order-received")

    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/bot_execution.log")

    def get_affiliate_links_list(self) -> List[str]:
        """Parse affiliate links from comma-separated string."""
        if not self.affiliate_links:
            return []
        return [link.strip() for link in self.affiliate_links.split(",") if link.strip()]

    def get_coupon_codes_list(self) -> List[str]:
        """Parse coupon codes from comma-separated string."""
        if not self.coupon_codes:
            return []
        return [code.strip() for code in self.coupon_codes.split(",") if code.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
