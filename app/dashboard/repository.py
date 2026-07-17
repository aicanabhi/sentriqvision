from motor.motor_asyncio import AsyncIOMotorDatabase


class DashboardRepository:

    async def get_dashboard_counts(self, db: AsyncIOMotorDatabase):

        return {
            "organizations": await db.organizations.count_documents({}),
            "organization_admins": await db.users.count_documents(
                {"role": "organization_admin"}
            ),
            "teams": await db.teams.count_documents({}),
            "users": await db.users.count_documents({}),
            "cameras": await db.cameras.count_documents({}),
            "active_cameras": await db.cameras.count_documents(
                {"status": "active"}
            ),
            "detections_today": await db.detections.count_documents({}),
            "alerts_today": await db.alerts.count_documents({})
        }