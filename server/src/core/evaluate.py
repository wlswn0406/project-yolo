import os
from yolo2.config.config import PROJECT_ROOT, LATEST_MODEL_PATH
from ultralytics import YOLO



'''
모델 검증
'''

# 데이터 경로
data_yaml_path = os.path.join(PROJECT_ROOT, 'data.yaml')

# 모델 경로 확인
if LATEST_MODEL_PATH and os.path.exists(LATEST_MODEL_PATH):
    print(f'사용할 모델: {LATEST_MODEL_PATH}')
    
    # 훈련된 모델 로드
    model = YOLO(LATEST_MODEL_PATH)

    # 모델 성능 평가
    metrics = model.val(data=data_yaml_path)

    print(f'>> mAP50: {metrics.box.map50}')
    print(f'>> mAP50-95: {metrics.box.map}')
    
else:
    print('훈련된 모델을 찾을 수 없습니다.')