@echo off
chcp 65001 >nul
REM Batch Installer - Web UI (Direct Start)
REM Double-click to start Web UI directly

echo ============================================================
echo  Batch Installer - Web UI
echo ============================================================
echo.

REM Check if Python is installed - try multiple commands
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Python not found
echo [ERROR] Python is not installed or not in PATH
echo.
echo Please install Python 3.7 or higher from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check "Add Python to PATH"
echo.
pause
exit /b 1

:python_found
echo [OK] Python found: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Check if requirements are installed
echo Checking dependencies...
%PYTHON_CMD% -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Installing required packages...
    echo.
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
    echo.
)

echo [OK] All dependencies ready
echo.
echo Starting Web Server...
echo Browser will open automatically at http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

%PYTHON_CMD% batch_installer_web.py

echo.
echo ============================================================
echo  Server stopped
echo ============================================================
pause
