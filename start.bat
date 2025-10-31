@echo off
REM Batch Installer - Start Script for Windows
REM Double-click this file to run the installer

echo ============================================================
echo  Batch Installer - ติดตั้งโปรแกรมรวมกัน
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ไม่ได้ติดตั้งในระบบ
    echo.
    echo กรุณาติดตั้ง Python 3.7 หรือสูงกว่าจาก:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python installed
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Installing required packages...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ❌ Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo ✓ All dependencies installed
echo.

REM Run the launcher
python run.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo ❌ An error occurred
    pause
)
