import asyncio
import json
import logging
import uuid
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.security import decode_access_token
from app.websocket.manager import ws_manager
from app.services.camera_engine import camera_manager

router = APIRouter()
logger = logging.getLogger("sentriqvision.ws_endpoint")


@router.websocket("/ws/{channel}")
async def websocket_endpoint(
    websocket: WebSocket,
    channel: str,
    token: Optional[str] = Query(None),
):
    """Authenticated tenant-isolated WebSocket endpoint."""
    tenant_id = "default-tenant"
    if token:
        try:
            payload = decode_access_token(token)
            tenant_id = payload.get("tenant_id", "default-tenant")
        except Exception as e:
            logger.warning(f"WebSocket token validation failed, using fallback: {e}")

    await ws_manager.connect(websocket, tenant_id, channel)

    await websocket.send_text(
        json.dumps({
            "type": "CONNECTION_ESTABLISHED",
            "channel": channel,
            "tenant_id": tenant_id,
            "status": "ONLINE",
        })
    )

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data) if data.startswith("{") else {"type": "PING"}
            if msg.get("type") == "PING":
                await websocket.send_text(json.dumps({"type": "PONG", "channel": channel}))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, tenant_id, channel)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket, tenant_id, channel)


@router.websocket("/ws/camera/{camera_id}")
async def camera_live_websocket(
    websocket: WebSocket,
    camera_id: str,
):
    """Streams real-time live detection metadata & bounding box results for a camera."""
    await websocket.accept()
    try:
        cam_uuid = uuid.UUID(camera_id)
        while True:
            runner = camera_manager.get_runner(cam_uuid)
            if runner:
                payload = {
                    "type": "CAMERA_FRAME_META",
                    "camera_id": camera_id,
                    "status": runner.status,
                    "fps": runner.fps,
                    "detections": runner.latest_detections,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(0.05)
    except (WebSocketDisconnect, Exception) as e:
        logger.debug(f"Camera websocket stream ended for {camera_id}: {e}")
