
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.application.schemas.common import APIResponse
from app.application.services.team_service import TeamService
from app.infrastructure.utils.dependencies import get_db, get_organization_admin

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=APIResponse[TeamResponse])
async def create_team(
    request: TeamCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = TeamService(db)
    team = await service.create_team(
        current_user["organization_id"],
        request,
        current_user["id"]
    )
    return APIResponse(success=True, data=team)


@router.get("", response_model=APIResponse[List[TeamResponse]])
async def get_all_teams(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = TeamService(db)
    teams = await service.get_all_teams(current_user["organization_id"])
    return APIResponse(success=True, data=teams)


@router.get("/{team_id}", response_model=APIResponse[TeamResponse])
async def get_team(
    team_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = TeamService(db)
    team = await service.get_team_by_id(team_id, current_user["organization_id"])
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=team)


@router.put("/{team_id}", response_model=APIResponse[TeamResponse])
async def update_team(
    team_id: str,
    request: TeamUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = TeamService(db)
    team = await service.update_team(
        team_id,
        current_user["organization_id"],
        request,
        current_user["id"]
    )
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, data=team)


@router.delete("/{team_id}")
async def delete_team(
    team_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user = Depends(get_organization_admin)
):
    if current_user["role"] == "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    service = TeamService(db)
    success = await service.delete_team(team_id, current_user["organization_id"])
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return APIResponse(success=True, message="Team deleted")
