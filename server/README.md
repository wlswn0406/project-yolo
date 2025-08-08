# Server

실시간 영상 수신, YOLO 객체 탐지, 이미지 저장 및 알림을 처리하는 핵심 서버

**개요**  
카메라로부터 실시간 영상을 수신하여 YOLO 모델로 객체를 감지하고, 감지 결과를 데이터베이스에 저장하며 텔레그램을 통한 실시간 알림을 제공합니다. 웹 대시보드와의 API 통신 및 모델 학습 트리거 기능을 담당합니다.


## 기능

- 실시간 카메라 영상 수신 및 YOLO 객체 탐지
- 감지된 객체 이미지를 MinIO에 저장
- 감지 결과를 MySQL 데이터베이스에 기록
- 텔레그램을 통한 실시간 알림 전송
- 모델 버전 관리 및 학습 트리거
- 웹 대시보드용 API 제공



## 구조

```bash
├── server/                            
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                         
│   ├── static/
│   ├── src/             
│   │   ├── config/                      # 설정
│   │   ├── api/                         # API 라우터
│   │   ├── core/                        # 비즈니스 로직
│   │   ├── database/                    # 데이터베이스
│   │   └── utils/                      
│   └── tests/ 
```



## 구성

**테스트**
```bash
# MySQL
docker run -d \
  --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=password123 \
  -e MYSQL_DATABASE=testdb \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=testpass \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0


# 가상 환경
conda create -n project python=3.11
conda activate project

# 패키지 설치
pip install python-dotenv pyyaml torch torchvision ultralytics websockets fastapi uvicorn opencv-python-headless pillow python-telegram-bot pydantic python-multipart minio sqlalchemy pymysql alembic cryptography pytest 
```



## API 엔드포인트

**Detection Process API**  
: 영상 수신 + 객체 탐지 + 알림 통합 프로세스  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/detection` | 통합 감지 시스템 정보 조회 (현재 모델 종류 등) | - |
| POST | `/api/detection/{type}` | 통합 감지 시스템 시작, 중지, 재시작 | `type`: start, stop, restart |
| PUT | `/api/detection/config` | 통합 시스템 설정 변경 | // ?세팅에도 존재함? |

```json
{
  "status": "running|stopped|error",
  "camera_status": "connected|disconnected",
  "model_loaded": true,
  "notification_ready": true,
  "uptime": 3600,
  "fps": 30,
  "detection_count": 45
}
```


**Stream API**  
: 영상 스트림 조회  

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stream/status` | 스트림 상태 확인 |
| GET | `/api/stream/viewer` | 실시간 객체 탐지 뷰어 (html 반환) |


**Detection API**  
: 객체 감지 결과 조회  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| POST | `/api/detections/{id?}` | 수동 객체 감지 (테스트용) | `image`: 이미지 파일 |
| GET | `/api/detections/{id}` | 특정 이벤트 상세 조회 | - |
| GET | `/api/detections` | 감지 이력 조회 | `page`, `limit`, `start_date`, `end_date`, `type` |
| GET | `/api/detections/recent` | 최근 감지 이벤트 | `limit`(기본값 10) |
| GET | `/api/detections/types` | 감지 가능한 객체 유형 목록 | - |
| PUT | `/api/detections/{id}/classify` | 미분류 객체 재분류 (수동 라벨링) | - |

type
- person - 사람
- package - 택배/패키지
- delivery_food - 배달음식
- mail - 우편물
- unclassified - 미분류

* 미분류 객체 재분류 : 미분류로 감지된 객체를 사용자가 수동으로 올바른 유형으로 재분류


**Model API**  
: YOLO 모델 정보 확인, 재학습, 데이터셋 설정 및 확인 등  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/models/current` | 현재 사용 모델 정보 |
| GET | `/api/models/versions` | 모델 버전 목록 |
| GET | `/api/models/{id}/info` | 특정 모델 정보 (성능 포함) |
| POST | `/api/models/{id}/deploy` | 특정 모델 배포 |
| POST | `/api/models/train` | 새 모델 학습 시작 | `dataset_id`, `epochs`, `batch_size`, `confidence_threshold`, `sensitivity` |
| POST | `/api/models/{id}/update` | 특정 모델 재학습/업데이트 | `dataset_id`, `epochs`, `batch_size`, `confidence_threshold`, `sensitivity` |
| GET | `/api/models/train/status` | 학습 진행 상태 | - |
| DELETE | `/api/models/train/cancel` | 학습 취소 | - |

```json
{
  "model_id": "yolo_v1.2",
  "accuracy": 0.95,
  "inference_time": "15ms",
  "dataset_id": "packages_v2.1",
  "data_yaml_path": "/datasets/packages_v2.1/data.yaml",
  "training_date": "2025-08-01T10:00:00Z",
  "training_params": {
    "epochs": 100,
    "batch_size": 16,
    "confidence_threshold": 0.5,
    "sensitivity": "medium"
  }
}
```

**Dataset API**  
: 데이터셋 관리  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/datasets` | 데이터셋 목록 조회 | - |
| GET | `/api/datasets/{id}` | 특정 데이터셋 정보 | - |
| POST | `/api/datasets/create` | 새 데이터셋 생성 | `name`, `description` |
| PUT | `/api/datasets/{id}/update` | 데이터셋 버전 업데이트 | `version`, `images` |
| POST | `/api/datasets/auto-collect` | 미분류 데이터를 데이터셋에 자동 추가 | `dataset_id`, `auto_label` |
| POST | `/api/datasets/roboflow/sync` | Roboflow 데이터셋 동기화 (배치) | `project_name`, `version` |


minio  
http://172.21.147.11:9001/browser/ai-door-system/datasets%2FPackages-1%2F


**DataYaml API**
| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/datasets/{id}/yaml` | 현재 활성 data.yaml 내용 조회 | - |
| POST | `/api/datasets/{id}/yaml` | 새로운 data.yaml 생성/업로드 | `yaml_content`, `version` |
| PUT | `/api/datasets/{id}/yaml/{yaml_id}` | data.yaml 수정 | `yaml_content` |
| GET | `/api/datasets/{id}/yaml/versions` | data.yaml 버전 이력 | - |
| POST | `/api/datasets/{id}/yaml/{yaml_id}/activate` | 특정 yaml 버전을 활성화 | - |
| GET | `/api/datasets/{id}/yaml/validate` | yaml 파일 유효성 검증 | `yaml_content` |
| GET | `/api/datasets/{id}/yaml/changes/{yaml_id}` | yaml 변경 이력 상세 | - |



**Event API**  
: 이벤트 및 이미지 관리  

이벤트 = 객체가 탐지되어 ID가 붙은 이미지  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/events` | 전체 이벤트 조회  | `page`, `limit`, `type`, `date_range` |
| GET | `/api/events/{id}` | 특정 이벤트 상세 | - |
| GET | `/api/events/{id}/images` | 이벤트의 캡처 이미지들 | - |
| GET | `/api/events/images/unclassified` | 미분류 이미지 목록 | `page`, `limit` |
| PUT | `/api/events/images/compress` | 이미지 압축 설정 변경 | `quality`(1-100) |


**Notification API**  
: 알림 설정, 조회 용도, 알림 발송은 테스트 용도  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/notifications/settings` | 알림 설정 조회 | - |
| PUT | `/api/notifications/settings` | 알림 설정 변경 | `enabled`, `sensitivity`, `types` |
| POST | `/api/notifications/send` | 테스트 알림 전송 | `text` |
| GET | `/api/notifications/history` | 알림 전송 이력 | `page`, `limit` | // 파라미터 사용 가능한지? 

알림 메시지
- `TEXT_0`: "미분류 객체가 감지되었습니다."
- `TEXT_1`: "사람이 감지되었습니다"  
- `TEXT_2`: "택배가 도착했습니다"
- `TEXT_3`: "배달음식이 도착했습니다"
- `TEXT_4`: "우편물이 도착했습니다"

알림 설정
- `enabled`: 알림 활성화/비활성화
- `sensitivity`: 감지 민감도 ("low", "medium", "high")  
- `types`: 알림 받을 객체 유형 배열


**Settings API**  
: 시스템 설정 및 관리  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/settings` | 전체 설정 조회 | - |
| PUT | `/api/settings` | 전체 설정 업데이트 | 설정 JSON 객체 |
| GET | `/api/settings/camera` | 카메라 설정 조회 | - |
| PUT | `/api/settings/camera` | 카메라 설정 변경 | `resolution`, `fps`, `brightness`, `contrast` |
| GET | `/api/settings/storage` | 스토리지 설정 조회 | - |
| PUT | `/api/settings/storage` | 스토리지 설정 변경 | `max_days`, `auto_cleanup`, `max_size_gb` |
| GET | `/api/settings/detection` | 감지 설정 조회 | - |
| PUT | `/api/settings/detection` | 감지 설정 변경 | `confidence_threshold`, `capture_interval`, `capture_count` |

// ++ 카메라 설정은 확인 필요함
// ++ 스토리지 설정은 확인 필요함

Camera Settings
- `resolution`: "1920x1080", "1280x720", "640x480"
- `fps`: 10-60
- `brightness`: -100 to 100
- `contrast`: -100 to 100

Storage Settings
- `max_days`: 보관 기간 (일)
- `auto_cleanup`: 자동 정리 활성화
- `max_size_gb`: 최대 저장 공간 (GB)

Detection Settings
- `confidence_threshold`: 0.1-1.0 (감지 신뢰도 임계값)
- `capture_interval`: 캡처 간격 (초)
- `capture_count`: 연속 캡처 장수



**System API**  
: 시스템 상태 및 모니터링  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/system/health` | 시스템 헬스체크 |
| GET | `/api/system/status` | 시스템 상태 |
| GET | `/api/system/logs` | 시스템 로그 조회 | `level`, `limit`, `date_range` |
| GET | `/api/system/storage` | 스토리지 사용량 | - |
| GET | `/api/system/performance` | 성능 모니터링 | - |
| POST | `/api/system/cleanup` | 시스템 정리 | `type`: "images", "logs", "temp" |
| POST | `/api/system/restart` | 시스템 재시작 | `service`: "camera", "detection", "all" |


**Batch API**  
: 배치 관리  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/batch/jobs` | 배치 작업 목록 | `status`, `limit` |
| POST | `/api/batch/trigger` | 배치 작업 트리거 | `job_type` |
| GET | `/api/batch/jobs/{id}` | 특정 작업 상태 | - |
| DELETE | `/api/batch/jobs/{id}` | 작업 취소 | - |


**Analytics API**  
: 이벤트 분석 및 패턴 인식  

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/analytics/patterns` | 방문 패턴 분석 | `period`: "day", "week", "month" |
| GET | `/api/analytics/frequent-visitors` | 자주 오는 방문자 분석 | `days`: 분석 일수 |
| GET | `/api/analytics/anomalies` | 비정상 행동 감지 | `sensitivity`: "low", "medium", "high" |
| GET | `/api/analytics/tracking` | 현재 추적 중인 객체 (SORT/DeepSORT) | - |
| GET | `/api/analytics/reports` | 분석 리포트 생성 | `type`, `period`, `format` |
| GET | `/api/analytics/statistics` | 감지 통계 | `period`, `group_by` |

**분석 리포트 유형:**
- `daily_summary`: 일일 요약
- `weekly_pattern`: 주간 패턴  
- `visitor_analysis`: 방문자 분석
- `security_report`: 보안 리포트



### 응답 형식

**성공**
```json
{
  "success": true|false,
  "message": "응답 메시지",
  "data": { ... },
  "timestamp": "2025-08-07T10:30:00Z",
}
```

**오류**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { ... }
  }
}
```




## 데이터베이스 스키마

// 로그인 생략

```sql
--사용자
CREATE TABLE users (
    id SERIAL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100),
    password VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(20) DEFAULT 'user',
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--텔레그램
CREATE TABLE telegrams (
    id SERIAL PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    chat_id VARCHAR(50) UNIQUE NOT NULL,
    bot_token VARCHAR(200) NOT NULL,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--객체 유형
CREATE TABLE object_types (
    id SERIAL PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL, -- person, package, delivery_food, mail, unclassified
    name VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--이벤트
CREATE TABLE detection_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path VARCHAR(255),
    object_type_id INTEGER REFERENCES object_types(id),
    model_version VARCHAR(50),

    --이하 정리 필요
    fps INTEGER,
    processing_time INTEGER; -- 처리 시간 (ms)
    confidence_score FLOAT,        -- 감지 신뢰도
    bbox_coordinates TEXT,         -- 바운딩 박스 좌표 JSON
    notification_sent BOOLEAN,
    user_verified BOOLEAN,         -- 사용자 검증 여부
    is_false_positive BOOLEAN      -- 오탐지 여부
    status VARCHAR(20) DEFAULT 'active', -- active, archived

   -- 재분류 (사용자가 분류를 수정하는 경우)
    original_type_id INTEGER REFERENCES object_types(id),
    reclassified_by INTEGER REFERENCES users(id),
    reclassified_at TIMESTAMP,

    -- 객체 추적 관련 (SORT/DeepSORT)
    tracking_id INTEGER,
    tracking_duration INTEGER, -- 추적 지속 시간 (초)


    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--이벤트 이미지(각 이벤트당 연속 캡처된 이미지들)
CREATE TABLE event_images (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES detection_events(id) ON DELETE CASCADE,
    image_path VARCHAR(500) NOT NULL, -- MinIO 저장 경로
    image_url VARCHAR(500), -- 접근 가능한 URL
    sequence_number INTEGER NOT NULL, -- 1~5 (2초 간격 연속 캡처)
    compression_quality INTEGER DEFAULT 85, -- 1-100
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(event_id, sequence_number)
);

-- 모델 관리
CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(50) UNIQUE NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    model_path VARCHAR(500) NOT NULL, -- MinIO 저장 경로
    model_size INTEGER, -- bytes
    version VARCHAR(20) NOT NULL,
    accuracy DECIMAL(5,4), -- 0.0000 ~ 1.0000
    inference_time INTEGER, -- milliseconds
    is_current BOOLEAN DEFAULT false, -- 현재 사용 중인 모델
    status VARCHAR(20) DEFAULT 'ready', -- training, ready, deployed, deprecated
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--모델 학습
CREATE TABLE model_training (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES models(id),
    dataset_id INTEGER, -- datasets 테이블 참조
    job_name VARCHAR(100) NOT NULL,
    job_type VARCHAR(20) NOT NULL, -- train, retrain, update
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    
    -- 학습 파라미터
    epochs INTEGER DEFAULT 100,
    batch_size INTEGER DEFAULT 16,
    confidence_threshold DECIMAL(3,2) DEFAULT 0.50,
    sensitivity VARCHAR(10) DEFAULT 'medium', -- low, medium, high
    
    -- 학습 결과
    final_accuracy DECIMAL(5,4),
    training_loss DECIMAL(10,6),
    validation_loss DECIMAL(10,6),
    training_time INTEGER, -- seconds
    
    -- 진행 상태
    current_epoch INTEGER DEFAULT 0,
    progress_percentage INTEGER DEFAULT 0,
    log_path VARCHAR(500), -- 학습 로그 파일 경로
    
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--데이터셋
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    dataset_id VARCHAR(50) UNIQUE NOT NULL, -- packages_v2.1
    name VARCHAR(100) NOT NULL,
    description TEXT,
    version VARCHAR(20) NOT NULL,
    
    -- MinIO 저장 경로
    storage_path VARCHAR(500) NOT NULL, -- /ai-door-system/datasets/packages_v2.1/
    yaml_path VARCHAR(500) NOT NULL, -- data.yaml 파일 경로
    
    -- 통계 정보
    total_images INTEGER DEFAULT 0,
    total_labels INTEGER DEFAULT 0,
    class_distribution JSONB, -- 클래스별 이미지 수
    
    -- Roboflow 연동 정보
    roboflow_project VARCHAR(100),
    roboflow_version VARCHAR(20),
    last_sync_at TIMESTAMP,
    
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 데이터셋 버전 히스토리
CREATE TABLE dataset_versions (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    changes TEXT,
    image_count INTEGER DEFAULT 0,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- data.yaml 설정 관리
CREATE TABLE data_yaml (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    dataset_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    yaml_content TEXT NOT NULL, -- YAML 파일 전체 내용
    
    -- YAML 파싱된 주요 정보
    train_path VARCHAR(500),
    val_path VARCHAR(500),
    test_path VARCHAR(500),
    nc INTEGER NOT NULL, -- number of classes
    names JSONB NOT NULL, -- class names array
    
    -- 추가 설정
    download_url VARCHAR(500),
    yaml_version VARCHAR(20),
    
    -- 메타데이터
    file_hash VARCHAR(64), -- YAML 파일 SHA256 해시 (변경 감지용)
    is_active BOOLEAN DEFAULT true,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 데이터셋당 하나의 활성 YAML만 존재
    UNIQUE KEY unique_active_yaml (dataset_id, is_active)
);


-- YAML 변경 이력
CREATE TABLE data_yaml_history (
    id SERIAL PRIMARY KEY,
    yaml_config_id INTEGER REFERENCES data_yaml(id) ON DELETE CASCADE,
    change_type VARCHAR(20) NOT NULL, -- created, updated, activated, deactivated
    old_content TEXT,
    new_content TEXT,
    changes_summary JSONB, -- 변경된 필드들의 요약
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 알림 메시지 템플릿
CREATE TABLE notification_templates (
    id SERIAL PRIMARY KEY,
    template_key VARCHAR(20) UNIQUE NOT NULL, -- TEXT_0, TEXT_1, TEXT_2, TEXT_3, TEXT_4
    object_type_id INTEGER REFERENCES object_types(id),
    message_text TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 알림 전송 이력
CREATE TABLE notification_history (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    telegram_user_id INTEGER REFERENCES telegrams(id),
    template_id INTEGER REFERENCES notification_templates(id),
    message_text TEXT NOT NULL,
    send_status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed
    sent_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 시스템 설정
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- camera, storage, detection, general
    setting_key VARCHAR(100) NOT NULL,
    setting_value TEXT NOT NULL,
    data_type VARCHAR(20) DEFAULT 'string', -- string, integer, float, boolean, json
    description TEXT,
    is_encrypted BOOLEAN DEFAULT false,
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(category, setting_key)
);

-- 시스템 상태 로그
CREATE TABLE system_status_logs (
    id SERIAL PRIMARY KEY,
    component VARCHAR(50) NOT NULL, -- camera, detection, notification, storage
    status VARCHAR(20) NOT NULL, -- running, stopped, error
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    gpu_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    fps INTEGER,
    error_message TEXT,
    metadata JSONB,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 시스템 로그
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(10) NOT NULL, -- DEBUG, INFO, WARNING, ERROR, CRITICAL
    component VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 배치 작업
CREATE TABLE batch_jobs (
    id SERIAL PRIMARY KEY,
    job_type VARCHAR(50) NOT NULL, -- dataset_update, model_retrain, storage_cleanup, log_archive
    job_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    priority INTEGER DEFAULT 5, -- 1-10 (1=highest)
    
    -- 작업 파라미터
    parameters JSONB,
    
    -- 실행 정보
    progress_percentage INTEGER DEFAULT 0,
    current_step VARCHAR(100),
    total_steps INTEGER,
    
    -- 결과
    result JSONB,
    error_message TEXT,
    
    -- 스케줄링
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 분석, 패턴 추가 ++


CREATE INDEX idx_detection_events_detected_at ON detection_events(detected_at DESC);
CREATE INDEX idx_detection_events_object_type ON detection_events(object_type_id);
CREATE INDEX idx_detection_events_status ON detection_events(status);
CREATE INDEX idx_detection_events_tracking_id ON detection_events(tracking_id);

CREATE INDEX idx_event_images_event_id ON event_images(event_id);
CREATE INDEX idx_event_images_captured_at ON event_images(captured_at DESC);

CREATE INDEX idx_notification_history_sent_at ON notification_history(sent_at DESC);
CREATE INDEX idx_notification_history_send_status ON notification_history(send_status);

CREATE INDEX idx_system_logs_created_at ON system_logs(created_at DESC);
CREATE INDEX idx_system_logs_level ON system_logs(level);
CREATE INDEX idx_system_logs_component ON system_logs(component);

CREATE INDEX idx_batch_jobs_status ON batch_jobs(status);
CREATE INDEX idx_batch_jobs_created_at ON batch_jobs(created_at DESC);
```