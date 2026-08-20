import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_org_ai_capability_data_isolation(client: AsyncClient):
    """
    Data Isolation Test:
    Verify that toggling AI capability for Organization A does NOT affect Organization B.
    """
    # 1. Login Super Admin
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get list of organizations
    orgs_resp = await client.get("/api/v1/superadmin/organizations", headers=headers)
    assert orgs_resp.status_code == 200
    orgs = orgs_resp.json()["data"]
    assert len(orgs) >= 1

    org_a_id = orgs[0]["id"]

    # Create a second organization Org B
    create_b = await client.post(
        "/api/v1/superadmin/organizations",
        headers=headers,
        json={"name": "Org B Test Corp", "slug": "org-b-test"},
    )
    assert create_b.status_code == 200
    org_b_id = create_b.json()["data"]["id"]

    # 3. Fetch 54 capabilities for Org A and Org B
    caps_a_resp = await client.get(f"/api/v1/parameters/organization/{org_a_id}", headers=headers)
    assert caps_a_resp.status_code == 200
    caps_a = caps_a_resp.json()["data"]
    assert len(caps_a) == 54

    caps_b_resp = await client.get(f"/api/v1/parameters/organization/{org_b_id}", headers=headers)
    assert caps_b_resp.status_code == 200
    caps_b = caps_b_resp.json()["data"]
    assert len(caps_b) == 54

    # Pick a specific capability (e.g. #30 / index 29)
    target_cap = caps_a[29]
    param_id = target_cap["parameter_id"]

    # Ensure Org B target cap is currently disabled
    cap_b_before = next(c for c in caps_b if c["parameter_id"] == param_id)

    # 4. Toggle capability FOR ORG A ONLY to enabled=True
    toggle_a_resp = await client.patch(
        f"/api/v1/parameters/{param_id}/toggle",
        headers=headers,
        json={"organization_id": org_a_id, "enabled": True},
    )
    assert toggle_a_resp.status_code == 200
    assert toggle_a_resp.json()["data"]["enabled"] is True

    # 5. VERIFY ORG B IS STILL DISABLED (ISOLATION CHECK)
    caps_b_after = (await client.get(f"/api/v1/parameters/organization/{org_b_id}", headers=headers)).json()["data"]
    cap_b_after = next(c for c in caps_b_after if c["parameter_id"] == param_id)
    assert cap_b_after["enabled"] is False, "CRITICAL FAILURE: Org B capability state changed when Org A was toggled!"

    # 6. Toggle Org B to enabled=True as well
    toggle_b_resp = await client.patch(
        f"/api/v1/parameters/{param_id}/toggle",
        headers=headers,
        json={"organization_id": org_b_id, "enabled": True},
    )
    assert toggle_b_resp.status_code == 200

    # Verify Org A remains enabled and Org B is now enabled
    caps_a_final = (await client.get(f"/api/v1/parameters/organization/{org_a_id}", headers=headers)).json()["data"]
    caps_b_final = (await client.get(f"/api/v1/parameters/organization/{org_b_id}", headers=headers)).json()["data"]

    cap_a_final = next(c for c in caps_a_final if c["parameter_id"] == param_id)
    cap_b_final = next(c for c in caps_b_final if c["parameter_id"] == param_id)

    assert cap_a_final["enabled"] is True
    assert cap_b_final["enabled"] is True


@pytest.mark.asyncio
async def test_org_ai_capability_validation_and_errors(client: AsyncClient):
    """
    Validation Test:
    - Invalid organization UUID format returns 400.
    - Non-existent organization UUID returns 404.
    - Invalid FPS / Confidence thresholds return 400.
    - Assigning unowned camera returns 400.
    """
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Invalid UUID format -> 400
    inv_uuid_resp = await client.get("/api/v1/parameters/organization/not-a-valid-uuid", headers=headers)
    assert inv_uuid_resp.status_code == 400

    # 2. Non-existent UUID -> 404
    fake_uuid = str(uuid.uuid4())
    non_exist_resp = await client.get(f"/api/v1/parameters/organization/{fake_uuid}", headers=headers)
    assert non_exist_resp.status_code == 404

    # 3. Invalid FPS (>60) -> 422/400
    caps_resp = await client.get("/api/v1/parameters/", headers=headers)
    assert caps_resp.status_code == 200
    param_id = caps_resp.json()["data"][0]["parameter_id"]

    inv_fps_resp = await client.put(
        f"/api/v1/parameters/{param_id}/configure",
        headers=headers,
        json={"sampling_fps": 120.0},
    )
    assert inv_fps_resp.status_code in [400, 422]

    # 4. Invalid confidence (>1.0) -> 422/400
    inv_conf_resp = await client.put(
        f"/api/v1/parameters/{param_id}/configure",
        headers=headers,
        json={"confidence_threshold": 2.5},
    )
    assert inv_conf_resp.status_code in [400, 422]

    # 5. Assign fake unowned camera ID -> 400
    unowned_cam_id = str(uuid.uuid4())
    inv_cam_resp = await client.put(
        f"/api/v1/parameters/{param_id}/configure",
        headers=headers,
        json={"camera_ids": [unowned_cam_id]},
    )
    assert inv_cam_resp.status_code == 400
    assert "does not belong" in inv_cam_resp.json()["detail"].lower() or "camera" in inv_cam_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_catalog_is_global_and_entitlement_endpoint(client: AsyncClient):
    """
    Test that GET /catalog is global and PATCH /{param_id}/entitlement updates entitlement state.
    """
    auth_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert auth_resp.status_code == 200
    token = auth_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Catalog API returns exactly 54 items
    cat_resp = await client.get("/api/v1/parameters/catalog", headers=headers)
    assert cat_resp.status_code == 200
    catalog_data = cat_resp.json()["data"]
    assert len(catalog_data) == 54

    # 2. Test explicit entitlement PATCH endpoint
    orgs_resp = await client.get("/api/v1/superadmin/organizations", headers=headers)
    assert orgs_resp.status_code == 200
    org_id = orgs_resp.json()["data"][0]["id"]
    param_id = catalog_data[0]["id"]

    entitle_resp = await client.patch(
        f"/api/v1/parameters/{param_id}/entitlement",
        headers=headers,
        json={"organization_id": org_id, "entitled": True},
    )
    assert entitle_resp.status_code == 200
    assert entitle_resp.json()["data"]["entitled"] is True

