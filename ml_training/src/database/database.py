# ml-training/src/database/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelRegistry(Base):
    __tablename__ = 'model_registry'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String, unique=True, nullable=False)
    model_path = Column(String, nullable=False)
    model_url = Column(String)  # 웹에서 접근 가능한 URL
    base_model = Column(String, nullable=False)  # yolov8n, yolov8s, etc.
    
    # 메트릭
    map50 = Column(Float)
    map50_95 = Column(Float) 
    precision = Column(Float)
    recall = Column(Float)
    
    # 메타데이터
    parameters = Column(JSON)  # 모델 파라미터 정보
    config = Column(JSON)      # 학습 설정
    created_at = Column(DateTime)
    
    # 상태
    status = Column(String, default='trained')  # trained, validated, deployed
    is_active = Column(Boolean, default=False)  # 현재 사용 중인 모델
    
    # 파일 정보
    file_size = Column(Integer)
    checksum = Column(String)