"""
Base Repository
Common CRUD database operations
"""

from typing import Generic, Type, TypeVar, Optional, List

from sqlalchemy.orm import Session

from app.models.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base
)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType]
    ):
        self.model = model


    # -----------------------------
    # Create
    # -----------------------------

    def create(
        self,
        db: Session,
        obj: ModelType
    ) -> ModelType:

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj



    # -----------------------------
    # Get By ID
    # -----------------------------

    def get_by_id(
        self,
        db: Session,
        id
    ) -> Optional[ModelType]:

        return (
            db.query(self.model)
            .filter(
                self.model.id == id
            )
            .first()
        )



    # -----------------------------
    # Get All
    # -----------------------------

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[ModelType]:

        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )



    # -----------------------------
    # Update
    # -----------------------------

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_data: dict
    ) -> ModelType:


        for field,value in obj_data.items():

            if hasattr(db_obj,field):

                setattr(
                    db_obj,
                    field,
                    value
                )


        db.commit()
        db.refresh(db_obj)

        return db_obj



    # -----------------------------
    # Delete
    # -----------------------------

    def delete(
        self,
        db: Session,
        db_obj: ModelType
    ):


        db.delete(db_obj)

        db.commit()

        return True



    # -----------------------------
    # Count
    # -----------------------------

    def count(
        self,
        db: Session
    ) -> int:

        return (
            db.query(self.model)
            .count()
        )