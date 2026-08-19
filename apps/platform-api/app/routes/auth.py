"""
Authentication API routes.

Provides the login endpoint used to exchange valid account
credentials for a JWT access token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.repositories.account import AccountRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import AuthService
from app.security.dependencies import get_current_account
from app.auth import AccountRole
from app.security.authorization import require_roles
from app.schemas.account import AccountCreate, AccountResponse
from app.services.account import AccountService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_db)):
    repository = AccountRepository(session)
    service = AuthService(repository)

    token = await service.authenticate(email=data.email, password=data.password)

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me")
async def get_me(account = Depends(get_current_account)):
    return {
        "id": account.id,
        "email": account.email,
        "role": account.role,
        "organization_id": account.organization_id,
        "is_active": account.is_active,
    }

@router.get("/admin-test")
async def admin_test(
        account = Depends(require_roles(AccountRole.SUPER_ADMIN, AccountRole.ADMIN)),
):
    return {
        "message": "Admin authorization successful",
        "account_id": account.id,
        "role": account.role,
    }

@router.post("/accounts/admin", response_model=AccountResponse)
async def create_organization_admin(
        data: AccountCreate,
        account = Depends(require_roles(AccountRole.SUPER_ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    repository = AccountRepository(session)
    service = AccountService(repository)

    if data.role != AccountRole.ADMIN:
        raise HTTPException(
            status_code=400,
            detail="This endpoint only creates ADMIN accounts."
        )

    try:
        new_account = await service.create(
            email=data.email,
            password=data.password,
            role=data.role,
            organization_id=data.organization_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    await session.commit()
    await session.refresh(new_account)

    return new_account

@router.get("/super-admin-test")
async def super_admin_test(
        account=Depends(require_roles(AccountRole.SUPER_ADMIN)),
):
    return {
        "message": "Super admin authorization successful",
        "account_id": account.id,
        "role": account.role,
    }

@router.post("/accounts/organization", response_model=AccountResponse)
async def create_organization_account(
        data: AccountCreate,
        account = Depends(require_roles(AccountRole.ADMIN)),
        session: AsyncSession = Depends(get_db),
):
    if data.role not in {
        AccountRole.OPERATOR,
        AccountRole.AUTHORIZED_VIEWER,
    }:
        raise HTTPException(
            status_code=400,
            detail="Only OPERATOR or AUTHORIZED_VIEWER accounts can be created"
        )

    if data.organization_id != account.organization_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot create an account outside your organization"
        )

    repository = AccountRepository(session)
    service = AccountService(repository)

    try:
        new_account = await service.create(
            email=data.email,
            password=data.password,
            role=data.role,
            organization_id=data.organization_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    await session.commit()
    await session.refresh(new_account)
    return new_account