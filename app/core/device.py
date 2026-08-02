"""
Device Detection & Management

Automatically detects the best available device
(CPU / CUDA GPU) for AI inference.
"""

from dataclasses import dataclass
import os
import platform
import multiprocessing

from loguru import logger

# ---------------------------------------------------------
# Optional Imports
# ---------------------------------------------------------

try:
    import torch
except Exception:
    torch = None

try:
    import onnxruntime as ort
except Exception:
    ort = None


# ---------------------------------------------------------
# Device Information
# ---------------------------------------------------------


@dataclass
class DeviceInfo:
    device: str
    provider: str
    gpu_name: str | None
    cpu_count: int
    cuda_available: bool
    onnx_providers: list[str]
    total_memory_gb: float | None


# ---------------------------------------------------------
# Device Manager
# ---------------------------------------------------------


class DeviceManager:

    def __init__(self):
        self.device_info = self.detect()

    # -----------------------------------------------------

    def detect(self) -> DeviceInfo:

        cpu_count = multiprocessing.cpu_count()

        gpu_name = None

        cuda_available = False

        provider = "CPUExecutionProvider"

        providers = []

        memory = None

        # ------------------------------
        # ONNX Providers
        # ------------------------------

        if ort is not None:

            try:
                providers = ort.get_available_providers()
            except Exception:
                providers = []

      
        # CUDA

        if torch is not None:

            if torch.cuda.is_available():

                cuda_available = True

                gpu_name = torch.cuda.get_device_name(0)

                provider = "CUDAExecutionProvider"

                memory = round(
                    torch.cuda.get_device_properties(0).total_memory
                    / 1024
                    / 1024
                    / 1024,
                    2,
                )

                device = "cuda"

            else:

                device = "cpu"

        else:

            device = "cpu"

        logger.info("===================================")
        logger.info("Device Detection")
        logger.info("===================================")

        logger.info(f"OS               : {platform.system()}")
        logger