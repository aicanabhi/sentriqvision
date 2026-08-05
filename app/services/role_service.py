"""
Role Service
"""

from sqlalchemy.orm import Session

from app.models.role import Role


class RoleService:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Role).all()

    def get_by_id(self, role_id):
        return (
            self.db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )

    def create(self, data):
        role = Role(**data)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, role_id, data):
        role = self.get_by_id(role_id)

        if not role:
            return None

        for key, value in data.items():
            setattr(role, key, value)

        self.db.commit()
        self.db.refresh(role)

        return role

    def delete(self, role_id):
        role = self.get_by_id(role_id)

        if not role:
            return False

        self.db.delete(role)
        self.db.commit()

        return True