"""
Enterprise Logging Configuration
"""

from pathlib import Path
import sys

from loguru import logger

from app.core.settings import settings

# Create log directory

LOG_DIR = Path(settings.LOG_DIR)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 
# Remove default logger

logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# Application Logs

logger.add(
    LOG_DIR / "application.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
)

# Error Logs
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="5 MB",
    retention="60 days",
    compression="zip",
    enqueue=True,
)

# AI Logs


logger.add(
    LOG_DIR / "ai_engine.log",
    level="INFO",
    rotation="20 MB",
    retention="30 days",
    compression="zip",
    filter=lambda record: record["extra"].get("module") == "ai",
)

# Camera Logs
logger.add(
    LOG_DIR / "camera.log",
    level="INFO",
    rotation="20 MB",
    retention="30 days",
    compression="zip",
    filter=lambda record: record["extra"].get("module") == "camera",
)

# Authentication Logs

logger.add(
    LOG_DIR / "auth.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    filter=lambda record: record["extra"].get("module") == "auth",
)

# Database Logs

logger.add(
    LOG_DIR / "database.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    filter=lambda record: record["extra"].get("module") == "database",
)

# Helper Functions

def get_logger(name: str):
    """
    Returns logger instance.

    Example:
        logger = get_logger("camera")
    """
    return logger.bind(module=name)