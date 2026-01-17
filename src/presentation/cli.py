"""CLI interface for bot execution."""
import argparse
import sys
from pathlib import Path

from loguru import logger


def setup_logging(log_level: str, log_file: str) -> None:
    """Configure loguru logging."""
    logger.remove()  # Remove default handler
    
    # Console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    
    # File handler
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="7 days",
    )


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Affiliate Bot QA - E2E Purchase Simulation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--bots",
        type=int,
        help="Number of concurrent bots to run (overrides .env)",
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without executing bots",
    )
    
    return parser


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = create_parser()
    return parser.parse_args()
