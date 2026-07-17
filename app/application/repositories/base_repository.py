
from typing import Optional, List, Dict, Any
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from datetime import datetime


class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.collection: AsyncIOMotorCollection = db[collection_name]

    async def create(self, data: Dict[str, Any]) -> str:
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        print("=" * 50)
        print("Searching Collection:", self.collection.name)
        print("Searching ID:", id)

        try:
            document = await self.collection.find_one(
                {"_id": ObjectId(id)}
            )

            print("Mongo Result:", document)

            if document:
                document["id"] = str(document["_id"])
                del document["_id"]

            return document

        except Exception as e:
            print("Mongo Error:", e)
            return None

    async def get_by_field(self, field: str, value: Any) -> Optional[Dict[str, Any]]:
        document = await self.collection.find_one({field: value})
        if document:
            document["id"] = str(document["_id"])
            del document["_id"]
            return document
        return None

    async def get_all(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = filter_query or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)

        if sort:
            cursor = cursor.sort(sort)

        documents = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            documents.append(doc)

        return documents

    async def count(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        query = filter_query or {}
        return await self.collection.count_documents(query)

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        if result.matched_count:
            return await self.get_by_id(id)

        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one(
            {"_id": ObjectId(id)}
        )
        return result.deleted_count > 0