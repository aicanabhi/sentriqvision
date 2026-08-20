from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse
from app.schemas.response import ResponseEnvelope
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=ResponseEnvelope[TokenResponse])
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    tokens = await service.authenticate_user(login_data)
    return ResponseEnvelope(success=True, data=tokens)


@router.post("/refresh", response_model=ResponseEnvelope[TokenResponse])
async def refresh(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    tokens = await service.refresh_access_token(refresh_data.refresh_token)
    return ResponseEnvelope(success=True, data=tokens)


@router.post("/seed", response_model=ResponseEnvelope[dict])
async def seed_data(
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    await service.seed_initial_data()
    return ResponseEnvelope(success=True, data={"message": "Initial seed completed successfully"})
