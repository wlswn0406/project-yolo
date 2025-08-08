from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel

from config.logging import get_logger



logger = get_logger(__name__)
stream_router = APIRouter(prefix='/stream', tags=['stream'])



@stream_router.get('/live')
async def stream_live():
    pass

# static > html 반환
@stream_router.get('/viewer')
async def stream_viewer():
    pass