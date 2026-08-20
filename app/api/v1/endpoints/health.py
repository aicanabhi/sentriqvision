import psutil
from fastapi import APIRouter, Depends
from sqlalchemy import text, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.schemas.response import ResponseEnvelope
from app.services.ai_engine.registry import global_ai_registry
from app.models.camera import Camera

router = APIRouter()


@router.get("/", response_model=ResponseEnvelope[dict])
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    # DB Check
    db_status = "HEALTHY"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    # Redis Check
    redis_status = "HEALTHY"
    try:
        r = await get_redis_client()
        await r.ping()
    except Exception as e:
        redis_status = f"UNHEALTHY: {str(e)}"

    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()

    return ResponseEnvelope(
        success=True,
        data={
            "status": "ONLINE",
            "services": {
                "database": db_status,
                "redis": redis_status,
            },
            "system_metrics": {
                "cpu_percent": cpu_usage,
                "ram_percent": ram.percent,
                "ram_used_mb": round(ram.used / (1024 * 1024), 2),
            },
        },
    )


@router.get("/database", response_model=ResponseEnvelope[dict])
async def get_database_health(db: AsyncSession = Depends(get_db)):
    """Returns database connection health, latency, and status."""
    import time
    start = time.time()
    try:
        await db.execute(text("SELECT 1"))
        latency_ms = round((time.time() - start) * 1000, 2)
        return ResponseEnvelope(
            success=True,
            data={
                "status": "HEALTHY",
                "latency_ms": latency_ms,
                "engine": "PostgreSQL / SQLite",
                "connected": True,
            },
        )
    except Exception as e:
        return ResponseEnvelope(
            success=False,
            error_code="DATABASE_UNHEALTHY",
            message=f"Database check failed: {str(e)}",
            data={"status": "UNHEALTHY", "connected": False, "error": str(e)},
        )


@router.get("/redis", response_model=ResponseEnvelope[dict])
async def get_redis_health():
    """Returns Redis connection health and status."""
    import time
    start = time.time()
    try:
        r = await get_redis_client()
        ping_ok = await r.ping()
        latency_ms = round((time.time() - start) * 1000, 2)
        return ResponseEnvelope(
            success=True,
            data={
                "status": "HEALTHY" if ping_ok else "UNHEALTHY",
                "latency_ms": latency_ms,
                "connected": bool(ping_ok),
            },
        )
    except Exception as e:
        return ResponseEnvelope(
            success=False,
            error_code="REDIS_UNHEALTHY",
            message=f"Redis check failed: {str(e)}",
            data={"status": "UNHEALTHY", "connected": False, "error": str(e)},
        )


@router.get("/gpu", response_model=ResponseEnvelope[dict])
async def get_gpu_health():
    """Returns actual GPU hardware telemetry or explicit GPU NOT AVAILABLE status."""
    gpu_available = False
    gpu_info = []

    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count > 0:
            gpu_available = True
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(name, bytes):
                    name = name.decode("utf-8")
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                try:
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Watts
                except Exception:
                    power = 0.0

                gpu_info.append({
                    "index": i,
                    "name": name,
                    "gpu_utilization_percent": util.gpu,
                    "memory_utilization_percent": util.memory,
                    "vram_total_mb": round(mem.total / (1024 * 1024), 2),
                    "vram_used_mb": round(mem.used / (1024 * 1024), 2),
                    "vram_free_mb": round(mem.free / (1024 * 1024), 2),
                    "temperature_celsius": temp,
                    "power_draw_watts": round(power, 2),
                })
        pynvml.nvmlShutdown()
    except Exception:
        # Fallback to PyTorch CUDA check if pynvml not installed or fails
        try:
            import torch
            if torch.cuda.is_available():
                gpu_available = True
                device_count = torch.cuda.device_count()
                for i in range(device_count):
                    gpu_info.append({
                        "index": i,
                        "name": torch.cuda.get_device_name(i),
                        "gpu_utilization_percent": 0.0,
                        "vram_total_mb": round(torch.cuda.get_device_properties(i).total_memory / (1024 * 1024), 2),
                        "vram_allocated_mb": round(torch.cuda.memory_allocated(i) / (1024 * 1024), 2),
                        "vram_reserved_mb": round(torch.cuda.memory_reserved(i) / (1024 * 1024), 2),
                        "temperature_celsius": 0,
                        "power_draw_watts": 0.0,
                    })
        except Exception:
            gpu_available = False

    if not gpu_available:
        return ResponseEnvelope(
            success=True,
            data={
                "status": "GPU NOT AVAILABLE",
                "available": False,
                "device_count": 0,
                "gpus": [],
                "message": "No CUDA GPU detected on system. Inference utilizing CPU acceleration.",
            },
        )

    return ResponseEnvelope(
        success=True,
        data={
            "status": "HEALTHY",
            "available": True,
            "device_count": len(gpu_info),
            "gpus": gpu_info,
        },
    )


@router.get("/models", response_model=ResponseEnvelope[dict])
async def get_models_health():
    """Returns AI model registry health status and installed weights summary."""
    health_data = global_ai_registry.get_all_capabilities_health()
    total_models = len(health_data)
    installed_count = sum(1 for m in health_data if m["is_installed"])
    model_required_count = sum(1 for m in health_data if m["status"] == "MODEL_REQUIRED")

    return ResponseEnvelope(
        success=True,
        data={
            "status": "HEALTHY" if installed_count > 0 else "MODEL_REQUIRED",
            "total_registered_models": total_models,
            "installed_models_count": installed_count,
            "missing_weights_count": model_required_count,
            "models": health_data,
        },
    )


@router.get("/cameras", response_model=ResponseEnvelope[dict])
async def get_cameras_health(db: AsyncSession = Depends(get_db)):
    """Returns real camera connectivity health and operational statuses."""
    result = await db.execute(select(Camera))
    cameras = result.scalars().all()

    total = len(cameras)
    online = sum(1 for c in cameras if c.status == "ONLINE")
    offline = sum(1 for c in cameras if c.status == "OFFLINE")
    error = sum(1 for c in cameras if c.status == "ERROR")
    connecting = sum(1 for c in cameras if c.status in ("CONNECTING", "RECONNECTING"))
    disabled = sum(1 for c in cameras if c.status == "DISABLED" or not c.is_active)

    return ResponseEnvelope(
        success=True,
        data={
            "total_cameras": total,
            "online_count": online,
            "offline_count": offline,
            "error_count": error,
            "connecting_count": connecting,
            "disabled_count": disabled,
            "cameras": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "status": c.status,
                    "is_active": c.is_active,
                    "last_frame_at": c.last_frame_at.isoformat() if c.last_frame_at else None,
                    "last_health_check": c.last_health_check.isoformat() if c.last_health_check else None,
                }
                for c in cameras
            ],
        },
    )


@router.get("/capabilities", response_model=ResponseEnvelope[list])
async def get_capabilities_health():
    """Returns detailed health, status, device, and latency metrics for all 54 canonical capabilities."""
    health_data = global_ai_registry.get_all_capabilities_health()
    return ResponseEnvelope(success=True, data=health_data)

