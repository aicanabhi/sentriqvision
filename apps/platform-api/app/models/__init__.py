from .base import Base
from .organization import Organization
from .site import Site
from .zone import Zone
from .camera import Camera
from .module import Module
from .camera_module import CameraModule
from .module_config import ModuleConfig
from .event import Event
from .event_evidence import EventEvidence
from .account import Account

__all__ = [
    "Base",
    "Organization",
    "Site",
    "Zone",
    "Camera",
    "Module",
    "CameraModule",
    "ModuleConfig",
    "Event",
    "EventEvidence",
]

"""
Organization
     │
     └── Site
          │
          └── Zone
               │
               └── Camera
                    │
                    └── CameraModule
                           │
                           ├── Module
                           │    ├── PPE
                           │    ├── FIRE
                           │    └── SMART_PARKING
                           │
                           └── ModuleConfig
For example:
Site: Mumbai Plant
   │
   └── Zone: Production
         │
         └── Camera: CAM-001
               │
               ├── PPE
               │    └── {
               │          helmet_required: true,
               │          vest_required: true
               │       }
               │
               └── FIRE
                    └── {
                          confidence_threshold: 0.85
                       }                           
"""