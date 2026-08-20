import json
import logging
from typing import Dict, List, Set
from fastapi import WebSocket

logger = logging.getLogger("sentriqvision.websocket")


class ConnectionManager:
    def __init__(self):
        # Map: tenant_id -> channel -> set of active WebSockets
        self.active_connections: Dict[str, Dict[str, Set[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str, channel: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = {}
        if channel not in self.active_connections[tenant_id]:
            self.active_connections[tenant_id][channel] = set()
        self.active_connections[tenant_id][channel].add(websocket)
        logger.info(f"WebSocket connected for tenant {tenant_id} on channel {channel}")

    def disconnect(self, websocket: WebSocket, tenant_id: str, channel: str):
        if tenant_id in self.active_connections:
            if channel in self.active_connections[tenant_id]:
                self.active_connections[tenant_id][channel].discard(websocket)
                if not self.active_connections[tenant_id][channel]:
                    del self.active_connections[tenant_id][channel]
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]
        logger.info(f"WebSocket disconnected for tenant {tenant_id} on channel {channel}")

    async def broadcast_to_tenant(self, tenant_id: str, channel: str, message: dict):
        if tenant_id in self.active_connections and channel in self.active_connections[tenant_id]:
            dead_sockets = set()
            payload = json.dumps(message)
            for connection in self.active_connections[tenant_id][channel]:
                try:
                    await connection.send_text(payload)
                except Exception as e:
                    logger.warning(f"Failed to send to socket: {e}")
                    dead_sockets.add(connection)
            for dead in dead_sockets:
                self.disconnect(dead, tenant_id, channel)


ws_manager = ConnectionManager()
