@echo off
chcp 65001 >nul
REM Batch Installer - Start Script for Windows
REM Double-click this file to run the installer

echo ============================================================
echo  Batch Installer - Program Installer
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
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo [OK] All dependencies installed
echo.

REM Run the launcher
%PYTHON_CMD% run.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred
    pause
)
