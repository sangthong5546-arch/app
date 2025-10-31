@echo off
REM Batch Installer - Web UI (Direct Start)
REM Double-click to start Web UI directly

echo ============================================================
echo  Batch Installer - Web UI
echo ============================================================
echo.
echo Starting Web Server...
echo Browser will open automatically at http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python batch_installer_web.py

echo.
echo ============================================================
echo  Server stopped
echo ============================================================
pause
