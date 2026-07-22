@echo off
REM ============================================================
REM  Start Benchmark Web UI (Measurement Lab)
REM
REM  Usage: double-click start-web.bat or run from cmd
REM  Prereq: Python 3.12+ in PATH, pip deps installed
REM          (run setup-bench.bat first if not)
REM
REM  Opens http://127.0.0.1:8765 in default browser
REM ============================================================

cd /d "%~dp0"

echo ============================================
echo   Measurement Lab - Benchmark Web UI
echo ============================================
echo.

REM Check python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo         Install Python 3.12+ and add to PATH.
    pause
    exit /b 1
)

REM Check deps
python -c "import yaml, anthropic" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Missing deps. Installing...
    python -m pip install -r eval\requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
)

echo Starting server at http://127.0.0.1:8765
echo Press Ctrl+C to stop.
echo.

REM Open browser after 2 seconds (server needs time to start)
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8765"

REM Start server (blocks until Ctrl+C)
python -m eval.server --port 8765
