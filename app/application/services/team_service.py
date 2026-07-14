
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.application.repositories.team_repository import TeamRepository
from app.application.schemas.team import TeamCreate, TeamUpdate, TeamResponse


class TeamService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = TeamRepository(db)

    async def create_team(self, organization_id: str, data: TeamCreate, created_by: str) -> TeamResponse:
        team_id = await self.repo.create({
            **data.model_dump(),
            "organization_id": organization_id,
            "created_by": created_by,
            "updated_by": created_by
        })
        team = await self.repo.get_by_id(team_id)
        return TeamResponse(**team)

    async def get_all_teams(self, organization_id: str, skip: int = 0, limit: int = 100) -> List[TeamResponse]:
        teams = await self.repo.get_all(
            filter_query={"organization_id": organization_id},
            skip=skip,
            limit=limit
        )
        return [TeamResponse(**team) for team in teams]

    async def get_team_by_id(self, team_id: str, organization_id: str) -> Optional[TeamResponse]:
        team = await self.repo.get_by_id(team_id)
        if team and team["organization_id"] == organization_id:
            return TeamResponse(**team)
        return None

    async def update_team(self, team_id: str, organization_id: str, data: TeamUpdate, updated_by: str) -> Optional[TeamResponse]:
        team = await self.repo.get_by_id(team_id)
        if not team or team["organization_id"] != organization_id:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = updated_by
        updated_team = await self.repo.update(team_id, update_data)
        return TeamResponse(**updated_team)

    async def delete_team(self, team_id: str, organization_id: str) -> bool:
        team = await self.repo.get_by_id(team_id)
        if not team or team["organization_id"] != organization_id:
            return False
        return await self.repo.delete(team_id)
