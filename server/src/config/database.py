from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .logging import setup_logging, get_logger
from .server_config import LOG_LEVEL, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD



setup_logging(log_level=LOG_LEVEL, log_dir='logs')
logger = get_logger(__name__)

# MySQL 데이터베이스 URL 구성
DATABASE_URL = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

# MySQL 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,           # 연결 상태 확인
    pool_recycle=300,             # 5분마다 연결 재생성
    pool_size=5,                  # 기본 연결 풀 크기
    max_overflow=10,              # 최대 추가 연결 수
    echo=(LOG_LEVEL == 'DEBUG'),  # 디버그 모드에서만 SQL 로깅
    pool_timeout=30,              # 연결 대기 시간 (초)
    connect_args={
        'charset': 'utf8mb4',
        'connect_timeout': 30,
        'read_timeout': 30,
        'write_timeout': 30
    }
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base 클래스 생성
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    '''
    FastAPI 의존성 주입용 데이터베이스 세션 생성
    '''
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f'Database session error: {e}')
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    '''
    데이터베이스 테이블 생성
    '''
    try:
        Base.metadata.create_all(bind=engine)
        logger.info('Database tables created successfully')
    except Exception as e:
        logger.error(f'Failed to create database tables: {e}')
        raise

def test_connection():
    '''
    데이터베이스 연결 테스트
    '''
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        logger.info(f'Database connection successful to {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
        return True
    except Exception as e:
        logger.error(f'Database connection failed: {e}')
        return False

async def check_database_health() -> dict:
    '''
    데이터베이스 헬스체크
    '''
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT VERSION() as version'))
            version = result.fetchone()[0]
            
            return {
                'status': 'healthy',
                'database_type': 'mysql',
                'version': version,
                'host': MYSQL_HOST,
                'port': MYSQL_PORT,
                'database': MYSQL_DATABASE,
                'connection_pool_size': engine.pool.size(),
                'checked_out_connections': engine.pool.checkedout(),
                'pool_checked_in': engine.pool.checkedin()
            }
    except Exception as e:
        logger.error(f'Database health check failed: {e}')
        return {
            'status': 'unhealthy',
            'error': str(e),
            'database_type': 'mysql',
            'host': MYSQL_HOST,
            'port': MYSQL_PORT,
            'database': MYSQL_DATABASE
        }

def get_database_info() -> dict:
    '''
    데이터베이스 연결 정보 반환 (민감정보 제외)
    '''
    return {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DATABASE,
        'user': MYSQL_USER,
        'charset': 'utf8mb4',
        'pool_size': engine.pool.size(),
        'max_overflow': 10,
        'pool_recycle': 300
    }

def init_database():
    '''데이터베이스 초기화'''
    logger.info('Initializing database connection...')
    if not test_connection():
        logger.error('Failed to connect to database. Please check configuration.')
        return False
    
    try:
        create_tables()
        return True
    except Exception as e:
        logger.error(f'Database initialization failed: {e}')
        return False