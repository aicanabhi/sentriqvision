"""Application lifecycle events."""

from app.core.logger import get_logger

logger = get_logger(__name__)


async def on_startup() -> None:
    logger.info("SentriqVision platform starting up...")


async def on_shutdown() -> None:
    logger.info("SentriqVision platform shutting down...")
