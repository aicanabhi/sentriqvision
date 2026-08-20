import pytest
from httpx import AsyncClient
from app.services.parameter_service import CANONICAL_54_SERVICES


@pytest.mark.asyncio
async def test_54_capabilities_uniqueness():
    """Verify that all 54 canonical capabilities are unique in key and service number."""
    assert len(CANONICAL_54_SERVICES) == 54
    codes = [item[1] for item in CANONICAL_54_SERVICES]
    numbers = [item[0] for item in CANONICAL_54_SERVICES]
    names = [item[2] for item in CANONICAL_54_SERVICES]

    assert len(set(codes)) == 54, "Duplicate capability code key found!"
    assert len(set(numbers)) == 54, "Duplicate capability service number found!"
    assert len(set(names)) == 54, "Duplicate capability name found!"
    assert min(numbers) == 1 and max(numbers) == 54


@pytest.mark.asyncio
async def test_organization_capability_filtering(client: AsyncClient):
    """Test login, parameters listing, and enabled capabilities filtering endpoint."""
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Fetch full 54 parameter list for organization
    params_resp = await client.get("/api/v1/parameters/", headers=headers)
    assert params_resp.status_code == 200
    params = params_resp.json()["data"]
    assert len(params) == 54, f"Expected 54 capabilities, got {len(params)}"

    # 2. Fetch enabled organization capabilities filter endpoint
    entitlements_resp = await client.get("/api/v1/parameters/organization-entitlements", headers=headers)
    assert entitlements_resp.status_code == 200
    enabled = entitlements_resp.json()["data"]
    assert isinstance(enabled, list)
    for cap in enabled:
        assert cap["enabled"] is True
        assert cap["status"] == "ACTIVE"
