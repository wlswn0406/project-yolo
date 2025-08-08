from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.logging import get_logger



logger = get_logger(__name__)
detection_process_router = APIRouter(prefix='/detection', tags=['detection'])

class ProcessStatus(BaseModel):
    status: str
    pid: Optional[int] = None
    uptime: Optional[str] = None
    last_detection: Optional[str] = None

class ProcessConfig(BaseModel):
    detection_interval: int = 1
    confidence_threshold: float = 0.5
    auto_restart: bool = True
    max_retries: int = 3



@detection_process_router.get('/', response_model=ProcessStatus)
async def get_detection_process():
    pass

@detection_process_router.post('/{action}')
async def set_detection_process():
    # start, stop, restart 
    pass

@detection_process_router.put('/config')
async def set_detection_config():
    pass