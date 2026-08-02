import logging
import torch

try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False

logger = logging.getLogger(__name__)

class DeviceManager:
    """
    Automatically detects and selects the best available AI execution hardware.
    Priority: CUDA -> TensorRT -> ONNX GPU -> CPU
    """

    @staticmethod
    def get_best_device() -> str:
        """Returns the best available device for PyTorch."""
        if torch.cuda.is_available():
            logger.info("GPU Available: Running on CUDA")
            return "cuda"
        
        # We can add MPS for Mac here if needed, but the prompt asks for CPU/NVIDIA
        logger.info("GPU Not Available: Running on CPU")
        return "cpu"

    @staticmethod
    def get_onnx_providers() -> list[str]:
        """Returns the best execution providers for ONNX Runtime."""
        if not HAS_ONNX:
            logger.warning("ONNX Runtime is not installed. CPU will be used as fallback.")
            return ["CPUExecutionProvider"]

        available_providers = ort.get_available_providers()
        
        providers = []
        if "TensorrtExecutionProvider" in available_providers and torch.cuda.is_available():
            logger.info("ONNX: Using TensorRT Execution Provider")
            providers.append("TensorrtExecutionProvider")
            
        if "CUDAExecutionProvider" in available_providers and torch.cuda.is_available():
            if "TensorrtExecutionProvider" not in providers:
                logger.info("ONNX: Using CUDA Execution Provider")
            providers.append("CUDAExecutionProvider")
            
        providers.append("CPUExecutionProvider")
        
        if len(providers) == 1:
            logger.info("ONNX: Running on CPU")
            
        return providers

    @staticmethod
    def get_device_info() -> dict:
        """Returns comprehensive information about the current execution environment."""
        info = {
            "pytorch_device": DeviceManager.get_best_device(),
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
            "onnx_providers": DeviceManager.get_onnx_providers()
        }
        return info

device_manager = DeviceManager()
