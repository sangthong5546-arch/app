@echo off
chcp 65001 >nul
REM Install Python Dependencies with multiple fallback options
REM This script tries different methods to install required packages

echo ============================================================
echo  Installing Python Dependencies
echo ============================================================
echo.

REM Detect Python
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    ) else (
        echo [ERROR] Python not found!
        pause
        exit /b 1
    )
)

echo [OK] Using: %PYTHON_CMD%
echo.

REM Check if already installed
%PYTHON_CMD% -c "import requests" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Dependencies already installed!
    echo.
    pause
    exit /b 0
)

echo [INFO] Installing 'requests' library...
echo.
echo Trying different installation methods...
echo.

REM Method 1: Standard PyPI with increased timeout
echo ============================================================
echo Method 1: PyPI.org (Standard - with longer timeout)
echo ============================================================
%PYTHON_CMD% -m pip install --timeout 60 requests
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Installed via PyPI.org
    goto :success
)

echo [FAILED] PyPI.org timed out
echo.

REM Method 2: Use Aliyun mirror (faster for Asia)
echo ============================================================
echo Method 2: Aliyun Mirror (Faster for Asia/Thailand)
echo ============================================================
%PYTHON_CMD% -m pip install -i https://mirrors.aliyun.com/pypi/simple/ requests
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Installed via Aliyun mirror
    goto :success
)

echo [FAILED] Aliyun mirror failed
echo.

REM Method 3: Use Tencent mirror
echo ============================================================
echo Method 3: Tencent Mirror (Alternative Asia mirror)
echo ============================================================
%PYTHON_CMD% -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple requests
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Installed via Tencent mirror
    goto :success
)

echo [FAILED] Tencent mirror failed
echo.

REM Method 4: Douban mirror
echo ============================================================
echo Method 4: Douban Mirror (Another alternative)
echo ============================================================
%PYTHON_CMD% -m pip install -i https://pypi.douban.com/simple requests
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Installed via Douban mirror
    goto :success
)

echo [FAILED] Douban mirror failed
echo.

REM All methods failed
echo ============================================================
echo [ERROR] All installation methods failed!
echo ============================================================
echo.
echo Possible solutions:
echo 1. Check your internet connection
echo 2. Disable firewall/antivirus temporarily
echo 3. Use VPN if PyPI is blocked
echo 4. Manual installation:
echo    - Download: https://files.pythonhosted.org/packages/requests-2.31.0.tar.gz
echo    - Extract and run: python setup.py install
echo.
pause
exit /b 1

:success
echo.
echo ============================================================
echo [SUCCESS] All dependencies installed!
echo ============================================================
echo.
echo You can now run: start-web.bat
echo.
pause
exit /b 0
