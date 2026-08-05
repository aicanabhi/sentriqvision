"""
API Dependencies

Shared dependencies for FastAPI routes.
"""

from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db



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
# Authentication
# ==========================================================

async def get_current_user(
    authorization: str | None = Header(
        default=None,
        alias="Authorization"
    )
):

    """
    Get logged in user from JWT.
    """

    if not authorization:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing"
        )


    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )


    token = authorization.split(" ")[1]


    # TODO:
    # Decode JWT
    # Fetch user from database

    return {
        "id": 1,
        "email": "admin@sentriqvision.com",
        "role": "super_admin",
        "token": token
    }



# ==========================================================
# Active User
# ==========================================================

async def get_current_active_user(
    current_user = Depends(get_current_user)
):

    """
    Check user status.
    """

    # TODO:
    # Check is_active from database

    return current_user



# ==========================================================
# Super Admin
# ==========================================================

async def get_current_super_admin(
    current_user = Depends(get_current_active_user)
):

    """
    Super Admin access.
    """

    if current_user["role"] != "super_admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required"
        )


    return current_user



# ==========================================================
# Organization Admin
# ==========================================================

async def get_current_org_admin(
    current_user = Depends(get_current_active_user)
):

    allowed_roles = [
        "super_admin",
        "organization_admin"
    ]


    if current_user["role"] not in allowed_roles:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization admin access required"
        )


    return current_user



# ==========================================================
# Permission Dependency
# ==========================================================

def require_permission(permission_name: str):

    async def checker(
        current_user = Depends(get_current_active_user)
    ):

        # TODO:
        # Check permission table

        return current_user


    return checker