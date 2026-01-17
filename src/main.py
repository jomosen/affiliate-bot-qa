"""Main entry point for the application."""
import asyncio
import sys

from loguru import logger

from src.infrastructure.config.settings import get_settings
from src.presentation.bot_orchestrator import BotOrchestrator
from src.presentation.cli import parse_args, setup_logging


async def main() -> int:
    """Main application entry point."""
    # Parse CLI arguments
    args = parse_args()

    # Load settings
    settings = get_settings()

    # Setup logging
    setup_logging(settings.log_level, settings.log_file)

    logger.info("=" * 60)
    logger.info("Affiliate Bot QA - E2E Testing Suite")
    logger.info("=" * 60)

    try:
        # Dry run - validate configuration
        if args.dry_run:
            logger.info("Configuration validation (dry run mode)")
            logger.info(f"Base URL: {settings.base_url}")
            logger.info(f"Max Concurrent Bots: {settings.max_concurrent_bots}")
            logger.info(
                f"Affiliate Links: {len(settings.get_affiliate_links_list())} configured"
            )
            logger.info(f"Coupon Codes: {len(settings.get_coupon_codes_list())} configured")
            logger.success("Configuration is valid!")
            return 0

        # Run bots
        bot_count = args.bots if args.bots else settings.max_concurrent_bots
        logger.info(f"Starting {bot_count} concurrent bots...")

        orchestrator = BotOrchestrator(settings)
        orders = await orchestrator.run_concurrent_bots(bot_count)

        logger.success(f"Execution completed! {len(orders)} orders processed.")

        # Print summary
        completed = len([o for o in orders if o.status.value == "completed"])
        failed = len([o for o in orders if o.status.value == "failed"])
        
        logger.info("=" * 60)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Orders: {len(orders)}")
        logger.success(f"Completed: {completed}")
        if failed > 0:
            logger.error(f"Failed: {failed}")
        logger.info("=" * 60)

        return 0

    except KeyboardInterrupt:
        logger.warning("Execution interrupted by user")
        return 130
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        return 1


def cli_entry() -> None:
    """CLI entry point wrapper."""
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


if __name__ == "__main__":
    cli_entry()
