import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_tenant_isolation_security(client: AsyncClient):
    """
    Critical Security Test:
    1. Authenticate as Org A user (admin@sentriqvision.com).
    2. Retrieve cameras for Org A.
    3. Verify that accessing a non-existent or other org's camera returns 404/403.
    """
    # 1. Login Super Admin / Tenant Admin
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. List cameras for tenant
    cams_resp = await client.get("/api/v1/cameras/", headers=headers)
    assert cams_resp.status_code == 200
    cams = cams_resp.json()["data"]
    assert isinstance(cams, list)

    # 3. Attempt to access unowned/invalid camera ID
    fake_cam_id = "00000000-0000-0000-0000-000000000000"
    forbidden_resp = await client.post(f"/api/v1/cameras/{fake_cam_id}/restart", headers=headers)
    assert forbidden_resp.status_code in [403, 404]


@pytest.mark.asyncio
async def test_superadmin_capabilities_and_health(client: AsyncClient):
    """Verifies Super Admin system health and organizations management endpoints."""
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    health_resp = await client.get("/api/v1/superadmin/system-health", headers=headers)
    assert health_resp.status_code == 200
    health_data = health_resp.json()["data"]
    assert "cpu_percent" in health_data
    assert "ram_used_gb" in health_data
    assert health_data["system_health"] == "HEALTHY"

    orgs_resp = await client.get("/api/v1/superadmin/organizations", headers=headers)
    assert orgs_resp.status_code == 200
    assert isinstance(orgs_resp.json()["data"], list)
