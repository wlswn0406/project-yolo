import os
import sys
from pathlib import Path
from roboflow import Roboflow

try:
    from config.training_config import DOWNLOAD_DATASET_DIR, YOLO11, ROBOFLOW_API_KEY
except ImportError:
    current_file = Path(__file__)
    src_dir = current_file.parent.parent
    sys.path.insert(0, str(src_dir))
    from config.training_config import DOWNLOAD_DATASET_DIR, YOLO11, ROBOFLOW_API_KEY



def download_dataset_from_roboflow(workspace, project_name):
    '''
    Roboflow에서 데이터셋 다운로드
    /download/dataset/에 저장하고 저장된 폴더명 반환
    '''

    # 다운로드 디렉토리
    download_dir = DOWNLOAD_DATASET_DIR
    download_dir.mkdir(parents=True, exist_ok=True)

    # 작업 디렉토리 변경
    original_cwd = os.getcwd()
    os.chdir(download_dir)

    try:
        rf = Roboflow(ROBOFLOW_API_KEY)
        project = rf.workspace(workspace).project(project_name)
        dataset = project.version(1).download(YOLO11)
        download_path = download_dir / dataset.location
        print(f'Dataset downloaded to: {download_path}')
        return str(download_path)
    finally:
        # 원래 작업 디렉토리로 복원
        os.chdir(original_cwd)

if __name__ == '__main__':
    try:
        dataset_path = download_dataset_from_roboflow('test-yykc5', 'packages-dataset-ri1xs')
        print('SUCCESS: Dataset downloaded to')
        print(dataset_path)
    except Exception as e:
        print(f'ERROR: Download failed - {e}')
        exit(1)