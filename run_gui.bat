@echo off
echo ==========================================
echo Starting Job Portal GUI...
echo ==========================================

cd /d "%~dp0"

if not exist venv (
    echo Error: Virtual environment not found!
    echo Please run 'run_backend.bat' first to set up the project.
    pause
    exit /b
)

call venv\Scripts\activate

echo Launching GUI...
python -m src.gui.main
pause
