"""
Permission Service
"""

from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionService:

    def __init__(self, db: Session):
        self.db = db


    def get_all_permissions(self):
        return (
            self.db.query(Permission)
            .all()
        )


    def get_permission_by_id(self, permission_id: str):
        return (
            self.db.query(Permission)
            .filter(
                Permission.id == permission_id
            )
            .first()
        )


    def create_permission(self, permission_data):
        permission = Permission(
            **permission_data
        )

        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)

        return permission


    def update_permission(
        self,
        permission_id: str,
        permission_data: dict
    ):
        permission = self.get_permission_by_id(
            permission_id
        )

        if not permission:
            return None

        for key, value in permission_data.items():
            setattr(
                permission,
                key,
                value
            )

        self.db.commit()
        self.db.refresh(permission)

        return permission


    def delete_permission(
        self,
        permission_id: str
    ):
        permission = self.get_permission_by_id(
            permission_id
        )

        if not permission:
            return False

        self.db.delete(permission)
        self.db.commit()

        return True