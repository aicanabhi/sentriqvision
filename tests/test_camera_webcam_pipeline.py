import pytest
import uuid
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_detect_available_webcams(client: AsyncClient):
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/cameras/webcams", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_create_and_start_webcam(client: AsyncClient):
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@sentriqvision.com", "password": "Admin123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "Front Desk Webcam",
        "location": "Lobby",
        "rtsp_url": "webcam://0",
        "camera_type": "WEBCAM",
        "device_index": 0
    }

    # 1. Create Webcam Camera
    res = await client.post("/api/v1/cameras/connect", json=payload, headers=headers)
    assert res.status_code == 200
    cam_data = res.json()["data"]
    cam_id = cam_data["id"]
    assert cam_data["camera_type"] == "WEBCAM"
    assert cam_data["device_index"] == 0

    # 2. Start Camera Runner
    start_res = await client.post(f"/api/v1/cameras/{cam_id}/start", headers=headers)
    assert start_res.status_code == 200
    start_data = start_res.json()["data"]
    assert start_data["is_running"] is True
    assert start_data["status"] == "ONLINE"

    # 3. Stop Camera Runner
    stop_res = await client.post(f"/api/v1/cameras/{cam_id}/stop", headers=headers)
    assert stop_res.status_code == 200
    stop_data = stop_res.json()["data"]
    assert stop_data["is_running"] is False
    assert stop_data["status"] == "OFFLINE"

    # 4. Clean up test camera
    del_res = await client.delete(f"/api/v1/cameras/{cam_id}", headers=headers)
    assert del_res.status_code == 200
