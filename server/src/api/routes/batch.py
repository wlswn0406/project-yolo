from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel

from config.logging import get_logger

logger = get_logger(__name__)
batch_router = APIRouter(prefix='/batch', tags=['batch'])

class BatchJob(BaseModel):
    id: int
    job_type: str
    job_name: str
    status: str
    priority: int
    progress_percentage: int
    current_step: Optional[str] = None
    total_steps: Optional[int] = None
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None

class BatchJobList(BaseModel):
    jobs: List[BatchJob]
    total: int

class TriggerRequest(BaseModel):
    job_type: str



@batch_router.get('/jobs', response_model=BatchJobList)
async def get_batch_jobs(
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200)
):
    pass

@batch_router.post('/trigger')
async def trigger_batch_job(trigger_request: TriggerRequest, background_tasks: BackgroundTasks):
    pass

@batch_router.get('/jobs/{job_id}', response_model=BatchJob)
async def get_batch_job(job_id: int):
    pass

@batch_router.delete('/jobs/{job_id}')
async def cancel_batch_job(job_id: int):
    pass