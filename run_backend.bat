@echo off
echo ==========================================
echo Setting up Job Portal Project...
echo ==========================================

cd /d "%~dp0"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

if not exist instance\job_portal.db (
    echo Initializing database...
    python -c "from src.db import db; from src.app import create_app; app = create_app(); with app.app_context(): db.create_all()"
)

echo.
echo ==========================================
echo Starting Backend Server...
echo ==========================================
echo The server is running at http://localhost:5000
echo Keep this window open!
echo.
python -m src.app
pause
