

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import settings

from app.application.repositories.super_admin_repository import (
    SuperAdminRepository
)

from app.application.repositories.organization_admin_repository import (
    OrganizationAdminRepository
)

from app.application.repositories.refresh_token_repository import (
    RefreshTokenRepository
)

from app.infrastructure.security.hash import (
    get_password_hash,
    verify_password,
)

from app.infrastructure.security.jwt import (
    create_access_token,
    create_refresh_token,
)

from app.application.schemas.auth import (
    Role,
    TokenResponse,
)


class AuthService:


    def __init__(
        self,
        db: Optional[AsyncIOMotorDatabase] = None
    ):
        self.db = db



    # ==================================
    # CREATE SUPER ADMIN
    # ==================================

    async def create_super_admin(self):

        if not self.db:

            from app.infrastructure.database.mongodb import (
                get_database
            )

            self.db = await get_database()


        repo = SuperAdminRepository(self.db)


        existing = await repo.get_by_email(
            settings.SUPER_ADMIN_EMAIL
        )


        if existing:

            print(
                "Super Admin already exists!"
            )

            return



        hashed_password = get_password_hash(
            settings.SUPER_ADMIN_PASSWORD
        )


        await repo.create({

            "email":
                settings.SUPER_ADMIN_EMAIL,

            "password":
                hashed_password,

            "name":
                "Super Admin",

            "role":
                Role.SUPER_ADMIN.value

        })


        print(
            "Super Admin created successfully!"
        )



    # ==================================
    # SUPER ADMIN LOGIN
    # ==================================

    async def login_super_admin(
        self,
        email: str,
        password: str,
        db: AsyncIOMotorDatabase
    ):


        repo = SuperAdminRepository(db)


        user = await repo.get_by_email(email)


        print(
            "LOGIN USER:",
            user
        )


        if not user:

            raise ValueError(
                "Invalid credentials"
            )



        if not verify_password(
            password,
            user["password"]
        ):

            raise ValueError(
                "Invalid credentials"
            )



        access_token = create_access_token(

            data={

                "sub":
                    str(user["id"]),

                "role":
                    Role.SUPER_ADMIN.value

            }

        )



        refresh_token = create_refresh_token(

            data={

                "sub":
                    str(user["id"]),

                "role":
                    Role.SUPER_ADMIN.value

            }

        )



        refresh_repo = RefreshTokenRepository(db)


        await refresh_repo.create({

            "token":
                refresh_token,

            "user_id":
                str(user["id"]),

            "role":
                Role.SUPER_ADMIN.value,

            "revoked":
                False

        })



        return TokenResponse(

            access_token=
                access_token,

            refresh_token=
                refresh_token,

            token_type=
                "bearer"

        )




    # ==================================
    # ORGANIZATION ADMIN LOGIN
    # ==================================

    async def login_organization_admin(
        self,
        email: str,
        password: str,
        db: AsyncIOMotorDatabase
    ):


        repo = OrganizationAdminRepository(db)


        user = await repo.get_by_email(email)



        if not user:

            raise ValueError(
                "Invalid credentials"
            )



        if not verify_password(
            password,
            user["password"]
        ):

            raise ValueError(
                "Invalid credentials"
            )



        access_token = create_access_token(

            data={

                "sub":
                    str(user["id"]),

                "role":
                    Role.ORGANIZATION_ADMIN.value,

                "organization_id":
                    user["organization_id"]

            }

        )



        return TokenResponse(

            access_token=
                access_token,

            token_type=
                "bearer"

        )




    # ==================================
    # CHANGE PASSWORD
    # ==================================

    async def change_password(
        self,
        user_id: str,
        role: str,
        old_password: str,
        new_password: str,
        db: AsyncIOMotorDatabase
    ):



        if role == Role.SUPER_ADMIN.value:

            repo = SuperAdminRepository(db)


        else:

            repo = OrganizationAdminRepository(db)



        user = await repo.get_by_id(
            user_id
        )


        if not user:

            raise ValueError(
                "User not found"
            )



        if not verify_password(
            old_password,
            user["password"]
        ):

            raise ValueError(
                "Old password incorrect"
            )



        new_hash = get_password_hash(
            new_password
        )



        await repo.update(

            user_id,

            {

                "password":
                    new_hash

            }

        )



        return {

            "message":
                "Password changed successfully"

        }




    # ==================================
    # LOGOUT
    # ==================================

    async def logout(self):

        return {

            "message":
                "Logout successful"

        }