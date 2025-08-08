# server/api/models.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


# 모델을 선택해 사용함


router = APIRouter(prefix="/api/models")

@router.get("/available")
async def get_available_models(db: Session = Depends(get_db)):
    """사용 가능한 모델 목록"""
    models = db.query(ModelRegistry).filter_by(status='production_ready').all()
    return [{"id": m.id, "name": m.model_name, "metrics": {"map50": m.map50}} for m in models]

@router.post("/select/{model_id}")
async def select_model(model_id: int, db: Session = Depends(get_db)):
    """모델 선택 및 로드"""
    model = db.query(ModelRegistry).filter_by(id=model_id).first()
    if not model:
        raise HTTPException(status_code=404, "Model not found")
    
    # 모델 배포
    model_manager = ModelManager(db)
    deployed_path = model_manager.deploy_to_server(model_id)
    
    # 감지 엔진 재시작
    await restart_detection_engine()
    
    return {"message": f"Model {model.model_name} deployed successfully"}

@router.get("/current")
async def get_current_model(db: Session = Depends(get_db)):
    """현재 사용 중인 모델 정보"""
    current = db.query(ModelRegistry).filter_by(is_active=True).first()
    return current