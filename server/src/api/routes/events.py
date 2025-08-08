from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from config.logging import get_logger



logger = get_logger(__name__)
events_router = APIRouter(prefix='/events', tags=['events'])



class EventInfo(BaseModel):
    id: int
    event_type: str
    detection_id: Optional[int] = None
    timestamp: str
    status: str
    description: str

class EventImage(BaseModel):
    id: int
    event_id: int
    image_path: str
    image_type: str
    file_size: int
    created_at: str

class EventListResponse(BaseModel):
    events: List[EventInfo]
    total: int
    page: int
    limit: int

class UnclassifiedImage(BaseModel):
    id: int
    image_path: str
    file_size: int
    created_at: str
    confidence: Optional[float] = None

class CompressRequest(BaseModel):
    quality: int



@events_router.get('/', response_model=EventListResponse)
async def get_events(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    event_type: Optional[str] = Query(None, alias="type"),
    date_range: Optional[str] = Query(None)
):
    pass

@events_router.get('/{event_id}', response_model=EventInfo)
async def get_event(event_id: int):
    pass

@events_router.get('/{event_id}/images', response_model=List[EventImage])
async def get_event_images(event_id: int):
    pass

@events_router.get('/images/unclassified', response_model=List[UnclassifiedImage])
async def get_unclassified_images(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    pass

@events_router.put('/images/compress')
async def update_image_compression(compress_config: CompressRequest):
    pass