import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import PlatformException
from app.core.logging import logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.organization import Organization
from app.models.tenant import Tenant
from app.models.user import Permission, Role, User
from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, login_data: LoginRequest) -> TokenResponse:
        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == login_data.email)
        )
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(login_data.password, user.password_hash):
            raise PlatformException(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                status_code=401,
            )

        if not user.is_active:
            raise PlatformException(
                code="USER_INACTIVE",
                message="User account is deactivated",
                status_code=403,
            )

        # Get user tenant's org
        tenant_query = select(Tenant).where(Tenant.id == user.tenant_id)
        tenant_res = await self.db.execute(tenant_query)
        tenant = tenant_res.scalar_one_or_none()
        org_id = str(tenant.organization_id) if tenant else str(uuid.uuid4())

        role_names = [role.name for role in user.roles]
        access_token = create_access_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
            org_id=org_id,
            roles=role_names,
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user_id=str(user.id),
            tenant_id=str(user.tenant_id),
            org_id=org_id,
            email=user.email,
            full_name=user.full_name,
            roles=role_names,
        )

    async def refresh_access_token(self, refresh_token_str: str) -> TokenResponse:
        try:
            payload = decode_refresh_token(refresh_token_str)
            user_id = payload.get("sub")
        except Exception:
            raise PlatformException(
                code="INVALID_REFRESH_TOKEN",
                message="Invalid or expired refresh token",
                status_code=401,
            )

        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == uuid.UUID(user_id))
        )
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise PlatformException(
                code="USER_NOT_FOUND",
                message="User associated with token not found or inactive",
                status_code=401,
            )

        tenant_query = select(Tenant).where(Tenant.id == user.tenant_id)
        tenant_res = await self.db.execute(tenant_query)
        tenant = tenant_res.scalar_one_or_none()
        org_id = str(tenant.organization_id) if tenant else str(uuid.uuid4())

        role_names = [role.name for role in user.roles]
        new_access_token = create_access_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
            org_id=org_id,
            roles=role_names,
        )
        new_refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            user_id=str(user.id),
            tenant_id=str(user.tenant_id),
            org_id=org_id,
            email=user.email,
            full_name=user.full_name,
            roles=role_names,
        )

    async def seed_initial_data(self):
        """Seeds default Organization, Tenant, Roles, Permissions, and Admin User if DB is empty."""
        org_check = await self.db.execute(select(Organization))
        if org_check.first():
            return  # Already seeded

        logger.info("Seeding initial database entities (Org, Tenant, Roles, Superadmin)...")

        # 1. Org & Tenant
        org = Organization(name="Default Security Corp", slug="default-corp")
        self.db.add(org)
        await self.db.flush()

        tenant = Tenant(
            organization_id=org.id,
            name="HQ Security Campus",
            code="hq-campus",
            config={"max_cameras": 100, "ai_features": ["FACE", "YOLO", "OCR", "ENHANCE"]},
        )
        self.db.add(tenant)
        await self.db.flush()

        # 2. Roles
        admin_role = Role(name="SUPER_ADMIN", description="System Super Admin", is_system=True)
        op_role = Role(name="OPERATOR", description="Security Command Center Operator", is_system=True)
        self.db.add_all([admin_role, op_role])
        await self.db.flush()

        # 3. Superuser
        admin_user = User(
            tenant_id=tenant.id,
            email="admin@sentriqvision.com",
            password_hash=get_password_hash("Admin123!"),
            full_name="System Administrator",
            is_superuser=True,
            is_active=True,
        )
        admin_user.roles.append(admin_role)
        self.db.add(admin_user)

        await self.db.commit()
        logger.info("Initial data successfully seeded. Admin login: admin@sentriqvision.com / Admin123!")

        # 4. Seed 54 AI parameters catalog & entitlements
        from app.services.parameter_service import ParameterService
        param_service = ParameterService(self.db)
        await param_service.seed_catalog_and_org_entitlements(org.id)

