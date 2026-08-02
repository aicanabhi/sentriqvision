"""
Application Startup Utilities

Responsible for:

- Folder initialization
- CPU/GPU Detection
- Startup Banner
- Environment Validation
- Future Database Initialization
"""

from pathlib import Path

from app.core.device import get_device_info
from app.core.logging import logger
from app.core.settings import settings


# ==========================================================
# Required Directories
# ==========================================================

REQUIRED_DIRECTORIES = [
    "logs",
    "uploads",
    "uploads/images",
    "uploads/videos",
    "uploads/snapshots",
    "uploads/thumbnails",
    "uploads/temp",
    "reports",
    "reports/pdf",
    "reports/excel",
    "storage",
    "storage/events",
    "storage/clips",
    "storage/frames",
    "models",
    "models/yolo",
    "models/face",
    "models/ocr",
    "models/anpr",
    "models/ppe",
    "cache",
]


# ==========================================================
# Create Directories
# ==========================================================

def create_directories() -> None:
    """
    Create all required project directories.
    """

    for folder in REQUIRED_DIRECTORIES:
        path = Path(folder)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {folder}")


# ==========================================================
# Validate Environment
# ==========================================================

def validate_environment() -> None:
    """
    Validate application settings.
    """

    if not settings.SECRET_KEY:
        raise RuntimeError("SECRET_KEY is missing.")

    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing.")

    logger.info("Environment validation successful.")


# ==========================================================
# Startup Banner
# ==========================================================

def print_banner() -> None:
    """
    Display startup banner.
    """

    device = get_device_info()

    banner = f"""

===========================================================
                 SENTRIQVISION AI PLATFORM
===========================================================

Application : {settings.APP_NAME}
Environment : {settings.APP_ENV}
Version     : {settings.APP_VERSION}

Host        : {settings.HOST}
Port        : {settings.PORT}

Device      : {device['device']}
GPU         : {device['gpu_name']}
CUDA        : {device['cuda_available']}

===========================================================

"""

    logger.info(banner)


# ==========================================================
# Initialize Application
# ==========================================================

def initialize_application() -> None:
    """
    Execute all startup tasks.
    """

    logger.info("Initializing SentriqVision...")

    validate_environment()

    create_directories()

    print_banner()

    logger.info("Application initialized successfully.")