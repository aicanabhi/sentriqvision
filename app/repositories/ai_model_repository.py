"""
Base Repository

Common database operations
used by all repositories.
"""

from typing import Generic, Type, TypeVar, Optional, List

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar(
    "ModelType"
)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
        db: AsyncSession,
    ):
        self.model = model
        self.db = db


    # ======================================================
    # CREATE
    # ======================================================

    async def create(
        self,
        obj: ModelType,
    ) -> ModelType:

        self.db.add(obj)

        await self.db.commit()

        await self.db.refresh(obj)

        return obj



    # ======================================================
    # GET BY ID
    # ======================================================

    async def get_by_id(
        self,
        id,
    ) -> Optional[ModelType]:

        result = await self.db.execute(
            select(self.model)
            .where(
                self.model.id == id
            )
        )

        return result.scalar_one_or_none()



    # ======================================================
    # GET ALL
    # ======================================================

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:

        result = await self.db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )



    # ======================================================
    # UPDATE
    # ======================================================

    async def update(
        self,
        id,
        data: dict,
    ) -> Optional[ModelType]:

        await self.db.execute(
            update(self.model)
            .where(
                self.model.id == id
            )
            .values(**data)
        )

        await self.db.commit()


        return await self.get_by_id(id)



    # ======================================================
    # DELETE
    # ======================================================

    async def delete(
        self,
        id,
    ) -> bool:


        result = await self.db.execute(
            delete(self.model)
            .where(
                self.model.id == id
            )
        )


        await self.db.commit()


        return result.rowcount > 0



    # ======================================================
    # EXISTS
    # ======================================================

    async def exists(
        self,
        id,
    ) -> bool:


        result = await self.db.execute(
            select(self.model.id)
            .where(
                self.model.id == id
            )
        )


        return result.scalar_one_or_none() is not None