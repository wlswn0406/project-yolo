@echo off
REM filepath: ai-door-system\ml_training\scripts\dataset_download_pipeline.bat

echo ========================================
echo AI Door System - Dataset Download
echo ========================================

REM 스크립트 디렉토리로 이동
cd /d "%~dp0\.."

REM Roboflow 다운로드
echo [1/1] Downloading from Roboflow...
python src\storage\dataset_download_roboflow.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Roboflow download failed
    pause
    exit /b 1
)

echo ========================================
echo Dataset download completed successfully!
echo ========================================
pause