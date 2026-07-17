from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_organizations: int
    total_organization_admins: int
    total_users: int
    total_teams: int
    total_cameras: int
    active_cameras: int
    total_alerts: int
    today_alerts: int