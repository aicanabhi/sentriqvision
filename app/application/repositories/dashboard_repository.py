from motor.motor_asyncio import AsyncIOMotorDatabase


class DashboardRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_dashboard_summary(self):
        return {
            "total_organizations": await self.db["organization"].count_documents({}),
            "total_organization_admins": await self.db["organization_admin"].count_documents({}),
            "total_users": await self.db["users"].count_documents({}),
            "total_teams": await self.db["teams"].count_documents({}),
            "total_cameras": await self.db["cameras"].count_documents({}),
            "active_cameras": await self.db["cameras"].count_documents(
                {"status": "active"}
            ),
            "total_alerts": await self.db["alerts"].count_documents({}),
            "today_alerts": await self.db["alerts"].count_documents({})
        }