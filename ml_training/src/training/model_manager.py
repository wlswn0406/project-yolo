# ml-training/src/model_manager.py
import shutil
import hashlib
from pathlib import Path

class ModelManager:
    def __init__(self, db_session):
        self.db = db_session
        self.models_dir = Path("models")
        self.runs_dir = Path("runs/train")
        
    def register_trained_model(self, run_name: str, model_name: str = None):
        """학습 완료된 모델을 등록"""
        run_path = self.runs_dir / run_name
        best_model_path = run_path / "weights" / "best.pt"
        
        if not best_model_path.exists():
            raise FileNotFoundError(f"Model not found: {best_model_path}")
        
        # 모델 이름 생성 (미제공시)
        if not model_name:
            model_name = f"{run_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 모델을 관리 디렉토리로 복사
        managed_path = self.models_dir / "experiments" / f"{model_name}.pt"
        managed_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_model_path, managed_path)
        
        # 모델 평가
        metrics = self.evaluate_model(managed_path)
        
        # DB에 등록
        model_record = ModelRegistry(
            model_name=model_name,
            model_path=str(managed_path),
            model_url=f"/api/models/download/{model_name}",
            **metrics,
            parameters=self.get_model_info(managed_path),
            file_size=managed_path.stat().st_size,
            checksum=self.calculate_checksum(managed_path)
        )
        
        self.db.add(model_record)
        self.db.commit()
        
        return model_record.id
    
    def promote_to_production(self, model_id: int):
        """모델을 프로덕션으로 승격"""
        model = self.db.query(ModelRegistry).filter_by(id=model_id).first()
        
        # 프로덕션 디렉토리로 복사
        prod_path = self.models_dir / "production" / f"{model.model_name}.pt"
        shutil.copy2(model.model_path, prod_path)
        
        # 상태 업데이트
        model.status = 'production_ready'
        self.db.commit()
        
        return prod_path
    
    def deploy_to_server(self, model_id: int):
        """서버로 모델 배포"""
        model = self.db.query(ModelRegistry).filter_by(id=model_id).first()
        
        # 서버 모델 디렉토리로 복사
        server_path = Path("../server/models/current/model.pt")
        shutil.copy2(model.model_path, server_path)
        
        # 이전 활성 모델 비활성화
        self.db.query(ModelRegistry).filter_by(is_active=True).update({'is_active': False})
        
        # 현재 모델 활성화
        model.is_active = True
        model.status = 'deployed'
        self.db.commit()
        
        return server_path