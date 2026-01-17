"""Unit tests for HumanSimulationService."""
import pytest

from src.application.services.human_simulation import HumanSimulationService


class TestHumanSimulationService:
    """Test cases for HumanSimulationService."""

    def test_random_quantity(self) -> None:
        """Test random quantity generation."""
        service = HumanSimulationService()

        for _ in range(10):
            qty = service.random_quantity(max_qty=4)
            assert 1 <= qty <= 4

    def test_random_scroll_amount(self) -> None:
        """Test random scroll generation."""
        service = HumanSimulationService()

        for _ in range(10):
            scroll = service.random_scroll_amount(max_scroll=1000)
            assert 100 <= scroll <= 1000

    @pytest.mark.asyncio
    async def test_delay_action(self) -> None:
        """Test action delay executes without error."""
        service = HumanSimulationService(action_delay_mean=0.1, action_delay_std=0.01)

        # Should complete without exception
        await service.delay_action()
        await service.delay_action(min_delay=0.05)

    @pytest.mark.asyncio
    async def test_delay_typing(self) -> None:
        """Test typing delay executes without error."""
        service = HumanSimulationService(typing_delay_min=1, typing_delay_max=5)

        # Should complete without exception
        await service.delay_typing()
