import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class AIServiceManager:
    """
    Manages the lifecycle (enable, disable, pause, restart) of AI services.
    Every service runs independently and only enabled services execute.
    """
    
    def __init__(self):
        # Maps service_id or service_name to its execution pipeline state
        self.active_services: Dict[str, Dict[str, Any]] = {}
        self.lock = asyncio.Lock()

    async def enable_service(self, organization_id: str, camera_id: str, service_name: str, config: dict):
        """Enables and starts a specific AI service for a given camera."""
        service_key = f"{organization_id}_{camera_id}_{service_name}"
        
        async with self.lock:
            if service_key in self.active_services and self.active_services[service_key]["status"] == "running":
                logger.info(f"Service {service_name} is already running for camera {camera_id}")
                return
            
            logger.info(f"Enabling AI Service: {service_name} on Camera: {camera_id}")
            # In a full implementation, this would instantiate the specific pipeline class (e.g., ParkingDetectionPipeline)
            self.active_services[service_key] = {
                "organization_id": organization_id,
                "camera_id": camera_id,
                "service_name": service_name,
                "status": "running",
                "config": config,
                "pipeline": None # Placeholder for actual pipeline object
            }

    async def disable_service(self, organization_id: str, camera_id: str, service_name: str):
        """Disables and completely stops an AI service."""
        service_key = f"{organization_id}_{camera_id}_{service_name}"
        
        async with self.lock:
            if service_key in self.active_services:
                logger.info(f"Disabling AI Service: {service_name} on Camera: {camera_id}")
                self.active_services[service_key]["status"] = "disabled"
                del self.active_services[service_key]

    async def pause_service(self, organization_id: str, camera_id: str, service_name: str):
        """Pauses a running AI service (keeps memory footprint but halts inference)."""
        service_key = f"{organization_id}_{camera_id}_{service_name}"
        
        async with self.lock:
            if service_key in self.active_services and self.active_services[service_key]["status"] == "running":
                logger.info(f"Pausing AI Service: {service_name} on Camera: {camera_id}")
                self.active_services[service_key]["status"] = "paused"

    async def restart_service(self, organization_id: str, camera_id: str, service_name: str, config: dict):
        """Restarts a service, pulling new configurations if provided."""
        logger.info(f"Restarting AI Service: {service_name} on Camera: {camera_id}")
        await self.disable_service(organization_id, camera_id, service_name)
        await self.enable_service(organization_id, camera_id, service_name, config)

    async def execute_frame(self, organization_id: str, camera_id: str, frame: Any):
        """Routes a camera frame to all running AI services associated with it."""
        # Find all services running on this camera
        services_to_run = []
        for key, service in self.active_services.items():
            if service["camera_id"] == camera_id and service["status"] == "running":
                services_to_run.append(service)
                
        if not services_to_run:
            return
            
        # Here we would normally fan out the frame to multiple pipelines asynchronously
        # For example: await asyncio.gather(*[srv["pipeline"].process(frame) for srv in services_to_run])
        pass

service_manager = AIServiceManager()
