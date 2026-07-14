
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None


async def get_database() -> AsyncIOMotorDatabase:
    global client
    try:
        if not client:
            client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=2000)
            # Try a quick ping to check connection
            await client.admin.command('ping')
            logger.info("Connected to MongoDB successfully!")
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}")
        # Still create a client but it will fail when actually used
        if not client:
            client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=2000)
    return client[settings.MONGO_DB_NAME]


async def close_database_connection():
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed.")
