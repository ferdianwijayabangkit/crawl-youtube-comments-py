@echo off
echo.
echo ===============================================
echo     YouTube Comments Crawler - Run Script
echo     by Ferdian Bangkit Wijaya (UNTIRTA)
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python tidak ditemukan!
    echo Silakan jalankan setup.bat terlebih dahulu
    pause
    exit /b 1
)

REM Check if main script exists
if not exist youtube_comments_crawler.py (
    echo ❌ ERROR: youtube_comments_crawler.py tidak ditemukan!
    echo Pastikan Anda berada di folder yang benar
    pause
    exit /b 1
)

echo 🚀 Starting YouTube Comments Crawler...
echo.

REM Run the crawler
python youtube_comments_crawler.py %*

echo.
echo 👋 Crawler finished. Press any key to exit...
pause >nul
