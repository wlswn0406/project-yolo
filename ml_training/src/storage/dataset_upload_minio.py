import os
import sys
from pathlib import Path

try:
    from config.training_config import minio_bucket_name, minio_client
except ImportError:
    current_file = Path(__file__)
    src_dir = current_file.parent.parent
    sys.path.insert(0, str(src_dir))
    from config.training_config import minio_bucket_name, minio_client



def upload_dataset_to_minio(local_path, minio_prefix='datasets'):
    '''
    MinIO에 로컬 데이터셋 업로드
    local_path: 로컬 파일 경로
    minio_prefix: MinIO 버킷 내의 경로 접두사
    '''

    local_path = Path(local_path)
    if not local_path.exists():
        raise FileNotFoundError(f'Dataset path not found: {local_path}')

    uploaded_files = []
    folder_name = local_path.name

    try:

        # MINIO 버킷 확인
        if not minio_client.bucket_exists(minio_bucket_name):
            minio_client.make_bucket(minio_bucket_name)

        # [TODO] 단일 파일 처리

        # 폴더 전체 업로드
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_path)
                minio_path = f'{minio_prefix}/{folder_name}/{relative_path}'.replace('\\', '/')

                minio_client.fput_object(
                    bucket_name=minio_bucket_name,
                    object_name=minio_path,
                    file_path=str(file_path)
                )
                uploaded_files.append(minio_path)
                print(f'Uploaded: {minio_path}')
        
        print(f'SUCCESS: {local_path} uploaded to {minio_path}')
        return uploaded_files
    
    except Exception as e:
        print(f'ERROR: Upload failed - {e}')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python minio_upload.py <dataset_path>')
        exit(1)
    
    dataset_path = sys.argv[1]
    try:
        upload_dataset_to_minio(dataset_path)
        print('SUCCESS: Dataset uploaded to MinIO')
    except Exception as e:
        print(f'ERROR: Upload failed - {e}')
        exit(1)