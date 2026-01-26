@echo off
:: Define encoding to UTF-8
chcp 65001 > nul

:: Get the directory where the script is located
cd /d "%~dp0"

:: Add current directory to PYTHONPATH so 'src' module can be found
set PYTHONPATH=%cd%

:: Activate virtual environment
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo [ERROR] Virtual environment not found (.venv).
    echo Please follow the setup instructions in README.md.
    pause
    exit /b
)

echo.
echo =========================================
echo Initializing Daily Digest Script...
echo =========================================
python src\main\main.py

echo.
echo =========================================
echo Daily Digest Script Completed.
echo =========================================

:: Wait so user can read output
timeout /t 5



