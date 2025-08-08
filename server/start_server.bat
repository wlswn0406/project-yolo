@echo off
REM Smart Doorbell System 개발 서버 시작 스크립트

echo Starting Smart Doorbell System Development Server...
echo.

REM Python 경로 설정
set PYTHONPATH=c:\Users\SBA\ex-github\ai-door-system\server\src

REM src 디렉토리로 이동
cd /d c:\Users\SBA\ex-github\ai-door-system\server\src

REM 환경 변수 확인 (디버깅용)
echo PYTHONPATH: %PYTHONPATH%
echo Current Directory: %CD%
echo.

REM uvicorn으로 FastAPI 서버 시작
uvicorn main:app --reload

pause