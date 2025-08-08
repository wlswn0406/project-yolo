from typing import Optional, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from config.logging import get_logger



logger = get_logger(__name__)
data_yaml_router = APIRouter(prefix='/datasets', tags=['data-yaml'])



class YamlContent(BaseModel):
    id: int
    dataset_id: int
    version: str
    content: str
    is_active: bool
    created_at: str

class CreateYamlRequest(BaseModel):
    yaml_content: str
    version: str

class UpdateYamlRequest(BaseModel):
    yaml_content: str

class ValidateYamlRequest(BaseModel):
    yaml_content: str

class YamlVersion(BaseModel):
    id: int
    version: str
    created_at: str
    is_active: bool

class YamlChanges(BaseModel):
    id: int
    version: str
    changes: List[str]
    created_at: str



@data_yaml_router.get('/{dataset_id}/yaml', response_model=YamlContent)
async def get_active_yaml(dataset_id: int):
    pass

@data_yaml_router.post('/{dataset_id}/yaml')
async def create_yaml(dataset_id: int, yaml_config: CreateYamlRequest):
    pass

@data_yaml_router.put('/{dataset_id}/yaml/{yaml_id}')
async def update_yaml(dataset_id: int, yaml_id: int, yaml_config: UpdateYamlRequest):
    pass

@data_yaml_router.get('/{dataset_id}/yaml/versions', response_model=List[YamlVersion])
async def get_yaml_versions(dataset_id: int):
    pass

@data_yaml_router.post('/{dataset_id}/yaml/{yaml_id}/activate')
async def activate_yaml(dataset_id: int, yaml_id: int):
    pass

@data_yaml_router.get('/{dataset_id}/yaml/validate')
async def validate_yaml(dataset_id: int, yaml_config: ValidateYamlRequest):
    pass

@data_yaml_router.get('/{dataset_id}/yaml/changes/{yaml_id}', response_model=YamlChanges)
async def get_yaml_changes(dataset_id: int, yaml_id: int):
    pass