@echo off
:: Define encoding to UTF-8
chcp 65001 > nul

cd /d "C:\Users\alexj\PycharmProjects\DailyDigest"

:: Add current directory to PYTHONPATH so 'src' module can be found
set PYTHONPATH=%cd%

call .venv\Scripts\activate

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



