from app.dashboard.repository import DashboardRepository


class DashboardService:

    def __init__(self):
        self.repository = DashboardRepository()

    async def get_dashboard(self, db):
        return await self.repository.get_dashboard_counts(db)