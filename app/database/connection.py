from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.MONGO_DB_NAME]


def get_db() -> AsyncIOMotorDatabase:
    return database