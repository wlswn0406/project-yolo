import os
from yolo2.config.config import PROJECT_ROOT, LATEST_MODEL_PATH, IMG_DIR, OUTPUT_DIR
from ultralytics import YOLO



# 데이터셋 경로
data_yaml_path = os.path.join(PROJECT_ROOT, 'data.yaml')

# 테스트 이미지 경로
test_image_path = os.path.join(IMG_DIR, 'test.png')

# 결과 출력 함수
def results_print(results):
    for result in results:
        # 결과 표시 및 저장
        result.show()
        result.save(os.path.join(OUTPUT_DIR, 'output-test.jpg'))
        
        # 탐지된 객체 정보 출력
        boxes = result.boxes
        if boxes is not None:
            print(f'탐지된 객체 수: {len(boxes)}')
            for box in boxes:
                # Tensor 값을 Python 값으로 변환
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                print(f'클래스: {result.names[class_id]}, 신뢰도: {confidence:.2f}')
        else:
            print('탐지된 객체가 없습니다.')

# 모델 로드 및 예측
if LATEST_MODEL_PATH and os.path.exists(LATEST_MODEL_PATH):
    print(f'사용할 모델: {LATEST_MODEL_PATH}')
    
    # 훈련된 모델 로드
    model = YOLO(LATEST_MODEL_PATH)

    # 단일 이미지 예측
    results = model(test_image_path)
    results_print(results)
    
else:
    print('훈련된 모델을 찾을 수 없습니다.')
