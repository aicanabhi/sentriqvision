from app.application.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    async def get_dashboard(self):
        return await self.repository.get_dashboard_summary()