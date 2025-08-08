# ml-training/src/model_trainer.py
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import torch
from ultralytics import YOLO
import json

@dataclass
class ModelConfig:
    model_name: str
    base_model: str  # 'yolov8n', 'yolov8s', etc.
    epochs: int
    batch_size: int
    learning_rate: float
    image_size: int
    dataset_path: str
    
class ModelTrainer:
    def __init__(self, config: ModelConfig, db_manager):
        self.config = config
        self.db_manager = db_manager
        self.model = None
        self.training_results = None
        
    def prepare_dataset(self):
        """데이터셋 준비 및 검증"""
        pass
        
    def train(self):
        """모델 학습 실행"""
        # YOLO 모델 초기화
        self.model = YOLO(self.config.base_model)
        
        # 학습 실행
        self.training_results = self.model.train(
            data=self.config.dataset_path,
            epochs=self.config.epochs,
            batch=self.config.batch_size,
            lr0=self.config.learning_rate,
            imgsz=self.config.image_size,
            project='runs/train',
            name=self.config.model_name
        )
        
        return self.training_results
    
    def evaluate(self):
        """모델 평가"""
        metrics = self.model.val()
        return {
            'map50': metrics.box.map50,
            'map50_95': metrics.box.map,
            'precision': metrics.box.mp,
            'recall': metrics.box.mr
        }
    
    def save_model_info(self, model_path: str, metrics: dict):
        """모델 정보를 데이터베이스에 저장"""
        model_info = {
            'model_name': self.config.model_name,
            'model_path': model_path,
            'base_model': self.config.base_model,
            'created_at': datetime.now(),
            'metrics': metrics,
            'parameters': self.get_model_parameters(),
            'config': self.config.__dict__
        }
        
        return self.db_manager.save_model_info(model_info)