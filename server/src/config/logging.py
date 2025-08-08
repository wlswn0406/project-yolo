import logging
import logging.handlers
from pathlib import Path

from .server_config import DEBUG



def setup_logging(log_level='INFO', log_dir='logs'):

    # 로그 디렉토리 생성
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # 파일 핸들러 (로테이션)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 루트 로거 설정
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler]
    )

    return logging.getLogger(__name__)

def get_logger(name):
    return logging.getLogger(name)