"""
API Dependencies

Shared dependencies for FastAPI routes.
"""

from fastapi import (
    Depends,
    HTTPException,
    Query,
    
    status,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db


# ==========================================================
# OAuth2 JWT Scheme
# ==========================================================

security = HTTPBearer()


# ==========================================================
# Pagination
# ==========================================================

def pagination_params(
    page: int = Query(
        default=1,
        ge=1
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100
    ),
):
    return {
        "page": page,
        "per_page": per_page,
        "skip": (page - 1) * per_page,
    }


# ==========================================================
# Database Dependency
# ==========================================================

async def get_session() -> AsyncSession:
    async for session in get_db():
        yield session



# ==========================================================
# Authentication
# ==========================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing",
        )

    # TODO: Verify JWT token here

    return {
        "id": 1,
        "email": "admin@sentriqvision.com",
        "role": "super_admin",
        "token": token,
    }
# ==========================================================
# Active User
# ==========================================================

async def get_current_active_user(
    current_user=Depends(get_current_user)
):

    """
    Check active user.
    """

    return current_user



# ==========================================================
# Super Admin
# ==========================================================

async def get_current_super_admin(
    current_user=Depends(get_current_active_user)
):

    if current_user["role"] != "super_admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required",
        )


    return current_user



# ==========================================================
# Organization Admin
# ==========================================================

async def get_current_org_admin(
    current_user=Depends(get_current_active_user)
):

    allowed_roles = [
        "super_admin",
        "organization_admin",
    ]


    if current_user["role"] not in allowed_roles:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization admin access required",
        )


    return current_user



# ==========================================================
# Permission Dependency
# ==========================================================

def require_permission(permission_name: str):

    async def checker(
        current_user=Depends(get_current_active_user)
    ):

        # TODO:
        # Check permission table

        return current_user


    return checker