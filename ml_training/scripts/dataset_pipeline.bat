@echo off
REM filepath: ai-door-system\ml_training\scripts\dataset_pipeline.bat

echo ========================================
echo AI Door System - Dataset Pipeline
echo ========================================

REM 스크립트 디렉토리로 이동
cd /d "%~dp0\.."

REM 1. Roboflow 다운로드 및 폴더명 받기
echo [1/3] Downloading from Roboflow...
for /f "delims=" %%i in ('python src\storage\dataset_download_roboflow.py') do set DATASET_PATH=%%i
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Roboflow download failed
    pause
    exit /b 1
)

echo Downloaded dataset folder: %DATASET_PATH%

REM 2. MinIO 업로드
echo [2/3] Uploading to MinIO...
python src\storage\dataset_upload_minio.py %DATASET_PATH%
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: MinIO upload failed
    pause
    exit /b 1
)

REM 3. 정리
echo [3/3] Cleaning up...
rmdir /s /q %DATASET_PATH%

echo ========================================
echo Data pipeline completed successfully!
echo ========================================
pause