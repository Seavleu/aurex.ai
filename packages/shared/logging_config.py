"""
AUREX.AI - Shared Logging Configuration.

Centralized logging setup using loguru.
"""

import sys
from pathlib import Path

from loguru import logger


def setup_logging(
    service_name: str,
    log_level: str = "INFO",
    log_file: str | None = None,
) -> None:
    """
    Configure logging for a service.

    Args:
        service_name: Name of the service (e.g., 'backend', 'pipeline')
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Remove default handler
    logger.remove()

    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        f"<cyan>{service_name}</cyan> | "
        "<level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            f"{service_name} | {{message}}",
            level=log_level,
            rotation="100 MB",
            retention="30 days",
            compression="zip",
        )

    logger.info(f"{service_name} logging initialized at {log_level} level")


def get_logger() -> logger:
    """
    Get configured logger instance.

    Returns:
        Configured logger instance
    """
    return logger

