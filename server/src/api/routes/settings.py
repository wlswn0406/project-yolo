from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.logging import get_logger



logger = get_logger(__name__)
settings_router = APIRouter(prefix='/settings', tags=['settings'])



class GlobalSettings(BaseModel):
    camera: Dict[str, Any]
    storage: Dict[str, Any]
    detection: Dict[str, Any]
    notifications: Dict[str, Any]

class CameraSettings(BaseModel):
    resolution: str
    fps: int
    brightness: int
    contrast: int

class StorageSettings(BaseModel):
    max_days: int
    auto_cleanup: bool
    max_size_gb: int

class DetectionSettings(BaseModel):
    confidence_threshold: float
    capture_interval: int
    capture_count: int



@settings_router.get('/', response_model=GlobalSettings)
async def get_all_settings():
    pass

@settings_router.put('/')
async def update_all_settings(settings: GlobalSettings):
    pass

@settings_router.get('/camera', response_model=CameraSettings)
async def get_camera_settings():
    pass

@settings_router.put('/camera')
async def update_camera_settings(camera_settings: CameraSettings):
    pass

@settings_router.get('/storage', response_model=StorageSettings)
async def get_storage_settings():
    pass

@settings_router.put('/storage')
async def update_storage_settings(storage_settings: StorageSettings):
    pass

@settings_router.get('/detection', response_model=DetectionSettings)
async def get_detection_settings():
    pass

@settings_router.put('/detection')
async def update_detection_settings(detection_settings: DetectionSettings):
    pass