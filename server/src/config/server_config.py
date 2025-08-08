# server/server_config.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from minio import Minio



load_dotenv()

# 프로젝트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 주요 디렉토리
STATIC_FOLDER = PROJECT_ROOT / 'static'
SRC_DIR = PROJECT_ROOT / 'src'


ENVIRONMENT = os.getenv('ENVIRONMENT')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DEBUG = os.getenv('DEBUG')
LOG_LEVEL = os.getenv('LOG_LEVEL')

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

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
    