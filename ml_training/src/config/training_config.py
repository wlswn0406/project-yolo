# ml-training/training_config.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from minio import Minio



load_dotenv()

# 프로젝트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 주요 디렉토리
SRC_DIR = PROJECT_ROOT / 'src'
DEPLOY_DIR = SRC_DIR / 'deployment'

# 데이터셋 다운로드 디렉토리
DOWNLOAD_DATASET_DIR = PROJECT_ROOT / 'download' / 'datasets'


YOLO11 = 'yolov11'

# roboflow
ROBOFLOW_API_KEY=os.getenv('ROBOFLOW_API_KEY')

# MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


# MINIO
minio_url = os.getenv('MINIO_URL')
minio_bucket_name = os.getenv('MINIO_BUCKET')

minio_client = Minio(
    minio_url,
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)


# 데이터셋 설정 파일 로드
# load_dataset_minio('v1')
# load_dataset_minio('current')
def load_dataset_minio(version='current'):
    file_path = f'datasets/labeled/{version}-data.yaml'

    try:
        response = minio_client.get_object(minio_bucket_name, file_path)
        config_content = response.read().decode('utf-8')
        return yaml.safe_load(config_content)
    
    except Exception as e:
        print(f'설정 파일 로드 실패: {e}')
        return None