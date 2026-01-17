"""Unit tests for BotConfigFactory."""
import pytest

from src.application.factories.bot_config_factory import BotConfigFactory


class TestBotConfigFactory:
    """Test cases for BotConfigFactory."""

    def test_create_random_bot(self) -> None:
        """Test random bot creation."""
        factory = BotConfigFactory(
            affiliate_links=["http://example.com?ref=1", "http://example.com?ref=2"],
            coupon_codes=["CODE1", "CODE2"],
        )

        config = factory.create_random_bot(bot_id=1)

        assert config.bot_id == 1
        assert config.entry_method in ["affiliate_link", "coupon_code"]
        assert config.target_product_count >= 1

    def test_create_affiliate_bot(self) -> None:
        """Test affiliate bot creation."""
        factory = BotConfigFactory(
            affiliate_links=["http://example.com?ref=1"],
            coupon_codes=["CODE1"],
        )

        config = factory.create_affiliate_bot(bot_id=1)

        assert config.bot_id == 1
        assert config.entry_method == "affiliate_link"
        assert config.affiliate_link is not None
        assert config.coupon_code is None

    def test_create_coupon_bot(self) -> None:
        """Test coupon bot creation."""
        factory = BotConfigFactory(
            affiliate_links=["http://example.com?ref=1"],
            coupon_codes=["CODE1"],
        )

        config = factory.create_coupon_bot(bot_id=1)

        assert config.bot_id == 1
        assert config.entry_method == "coupon_code"
        assert config.coupon_code is not None
        assert config.affiliate_link is None
