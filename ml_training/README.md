# ML Training

현관 방문자 감지 시스템의 AI 모델 학습 및 관리 모듈


**개요**  
현관 모니터링 시스템에서 수집된 데이터를 기반으로 YOLO 객체 감지 모델을 지속적으로 학습하고 개선하는 파이프라인입니다. 미분류 이미지의 자동 라벨링부터 모델 배포까지 전체 생명주기를 관리합니다.



## 주요 기능

[TODO] 검토

**모델 학습**
- [ ] YOLOv11 기반 커스텀 모델 학습 환경 구축
- [ ] 하이퍼파라미터 자동 튜닝 (Hyperparameter Optimization)
- [ ] 실험 추적 시스템 (MLflow/Weights & Biases)
- [ ] 학습 결과 비교 및 분석
- [ ] 성능 평가 자동화 (mAP, Precision, Recall)
- [ ] 교차 검증 (Cross-validation) 구현
- [ ] 조기 종료 (Early Stopping) 로직
- [ ] 학습 재시작 및 체크포인트 관리

**모델 관리**
- [ ] 모델별 저장소 구성 (Model Registry)
- [ ] 버전별 모델 저장 및 태깅
- [ ] 모델 메타데이터 관리 (성능 지표, 학습 정보)
- [ ] 데이터베이스 연동 (모델 정보 기록)
- [ ] 모델 검색 및 필터링 기능

**모델 배포 및 교체**
- [ ] 모델 학습 후 생성된 모델을 지정된 모델 폴더로 복사
- [ ] 모델 버전, 경로, 평가 정보, 파라미터를 데이터베이스에 저장
- [ ] 대시보드에서 설정을 통해 원하는 모델로 교체하여 사용

**데이터 처리**
- [ ] 외부 데이터셋 관리 (Roboflow)
- [ ] MinIO에서 미분류 이미지 자동 수집
- [ ] 이미지 품질 검증 및 필터링
- [ ] 자동 라벨링 시스템 구축
- [ ] 수동 검토 워크플로우 구성
- [ ] YOLO 형식 데이터셋 자동 변환
- [ ] 데이터셋 버전 관리
- [ ] 데이터 증강(Augmentation) 파이프라인
- [ ] 데이터 검증 및 무결성 체크

**API 서비스**
- [ ] REST API 서버 구축
- [ ] 모델 추론 API 엔드포인트
- [ ] 인증 및 권한 관리
- [ ] API 버전 관리
- [ ] 요청/응답 로깅
- [ ] API 문서 자동 생성 (Swagger/OpenAPI)
- [ ] 헬스체크 엔드포인트

**모니터링 및 관찰성**
- [ ] 학습 과정 실시간 추적
- [ ] 성능 지표 대시보드 구축
- [ ] 모델 성능 지속적 모니터링
- [ ] 추론 지연시간 모니터링
- [ ] 오류율 및 경고 시스템
- [ ] 리소스 사용량 모니터링 (CPU, GPU, 메모리)



## 구조

```bash
ml-training/
├── Dockerfile
├── requirements.txt
├── src/
│   ├── config/
│   ├── data/                   # 데이터 처리
│   │   ├── collector.py        # MinIO에서 미분류 데이터 수집
│   │   ├── preprocessor.py     # 이미지 전처리
│   │   ├── labeler.py          # 자동/수동 라벨링
│   │   └── dataset_builder.py  # YOLO 데이터셋 구성
│   ├── training/               # 학습 관련
│   │   ├── trainer.py          # YOLO 모델 학습
│   │   ├── validator.py        # 모델 검증
│   │   └── metrics.py          # 평가 지표 계산
│   ├── models/                 # 모델 관리
│   │   ├── manager.py          # 모델 버전 관리
│   │   ├── optimizer.py        # 모델 최적화
│   │   └── converter.py        # 모델 형식 변환
│   ├── storage/                # MinIO 클라이언트
│   │   ├── minio_client.py     # MinIO 연결/업로드/다운로드
│   │   └── file_manager.py     # 파일 시스템 관리
│   └── utils/
│       ├── logger.py           # 로깅 설정
│       ├── config_loader.py    # 설정 파일 로더
│       └── visualization.py    # 결과 시각화
├── scripts/                    # 스크립트
└── notebooks/                  # 실험/분석용
```



## 구성

**사전 요구사항**
- Git
- Docker & Docker Compose
- Python 3.11
- CUDA 11.8+


**로컬 환경 설정**
```bash
# 가상 환경 생성
conda activate project

# 패키지 설치
pip install python-dotenv pyyaml minio
pip install ultralytics torch torchvision
pip install matplotlib seaborn pandas
pip install labelimg roboflow

# 데이터 증강 albumentations
# 학습 과정 시각화 tensorboard
# 실시간 추적 wandb
```