@echo off
REM Setup script for Docling GUI (Windows)
REM This script sets up the virtual environment and installs dependencies

echo ================================================
echo Docling GUI - Setup Script (Windows)
echo ================================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9 or later.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Verify Docling installation
echo Verifying Docling installation...
python -c "import docling; print('Docling', docling.__version__, 'installed successfully')" 2>nul
if errorlevel 1 (
    echo WARNING: Could not verify Docling installation
) else (
    echo Docling installation verified
)
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo To run the application:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo   2. Run the application:
echo      python main.py
echo.
echo For more information, see README.md or QUICKSTART.md
echo.
pause
