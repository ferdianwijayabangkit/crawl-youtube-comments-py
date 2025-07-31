@echo off
echo.
echo ===============================================
echo   YouTube Comments Crawler - Setup Script
echo   by Ferdian Bangkit Wijaya (UNTIRTA)
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu dari https://python.org
    pause
    exit /b 1
)

echo ✅ Python ditemukan:
python --version

echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Error installing dependencies!
    echo Silakan cek koneksi internet dan coba lagi.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies berhasil diinstall!
echo.
echo 🔧 Checking optional dependencies...

REM Check optional dependencies
python -c "import textblob; print('✅ TextBlob available (sentiment analysis)')" 2>nul || echo "⚠️ TextBlob not available (sentiment analysis disabled)"
python -c "import requests; print('✅ Requests available (IP detection)')" 2>nul || echo "⚠️ Requests not available (IP detection disabled)"

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo    1. Get YouTube Data API v3 key from Google Cloud Console
echo    2. Run: python youtube_comments_crawler.py
echo.
echo 💡 For help: python youtube_comments_crawler.py --help
echo.
pause
