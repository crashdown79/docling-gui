@echo off
REM Run script for Docling GUI (Windows)

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found.
    echo Please run setup.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main.py
