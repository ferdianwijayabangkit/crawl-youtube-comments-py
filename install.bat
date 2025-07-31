@echo off
title YouTube Comments Crawler - Auto Installer
color 0A

echo.
echo ===============================================
echo   YouTube Comments Crawler - Auto Installer
echo   by Ferdian Bangkit Wijaya (UNTIRTA)
echo ===============================================
echo.
echo 🚀 This installer will set up everything you need!
echo 👨‍💻 Developed by Ferdian Bangkit Wijaya
echo 🏫 Universitas Sultan Ageng Tirtayasa
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
) else (
    echo ⚠️ Running without administrator privileges
    echo   Some features may not work properly
)

echo.
echo 📋 INSTALLATION STEPS:
echo    1. Check Python installation
echo    2. Install Python dependencies
echo    3. Verify system setup
echo    4. Create shortcuts (optional)
echo    5. Download example files
echo.

pause

REM Step 1: Check Python
echo.
echo ==========================================
echo 📍 STEP 1: Checking Python Installation
echo ==========================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo 📥 DOWNLOADING PYTHON...
    echo Please visit: https://python.org/downloads
    echo.
    echo After installing Python:
    echo 1. Restart this installer
    echo 2. Or run setup.bat manually
    echo.
    pause
    start https://python.org/downloads
    exit /b 1
) else (
    echo ✅ Python found:
    python --version
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 📊 Python version: %PYTHON_VERSION%

REM Step 2: Install dependencies
echo.
echo ==========================================
echo 📍 STEP 2: Installing Dependencies
echo ==========================================

if exist requirements.txt (
    echo 📦 Installing from requirements.txt...
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo ❌ Failed to install some dependencies
        echo 🔧 Trying alternative installation...
        
        echo Installing core dependencies...
        pip install google-api-python-client
        pip install pandas
        pip install openpyxl
        
        echo Installing optional dependencies...
        pip install textblob requests
    ) else (
        echo ✅ All dependencies installed successfully!
    )
) else (
    echo ⚠️ requirements.txt not found, installing manually...
    
    echo Installing core dependencies...
    pip install google-api-python-client pandas openpyxl
    
    echo Installing optional dependencies...
    pip install textblob requests
)

REM Step 3: Verify setup
echo.
echo ==========================================
echo 📍 STEP 3: Verifying System Setup
echo ==========================================

if exist test_system.py (
    echo 🧪 Running system verification...
    python test_system.py
) else (
    echo ⚠️ test_system.py not found, skipping verification
)

REM Step 4: Create shortcuts
echo.
echo ==========================================
echo 📍 STEP 4: Creating Shortcuts (Optional)
echo ==========================================

set /p CREATE_SHORTCUTS="Create desktop shortcuts? (y/n): "
if /i "%CREATE_SHORTCUTS%"=="y" (
    echo 🔗 Creating shortcuts...
    
    REM Create desktop shortcut for main crawler
    set DESKTOP=%USERPROFILE%\Desktop
    set CURRENT_DIR=%CD%
    
    echo @echo off > "%DESKTOP%\YouTube Comments Crawler.bat"
    echo cd /d "%CURRENT_DIR%" >> "%DESKTOP%\YouTube Comments Crawler.bat"
    echo python youtube_comments_crawler.py >> "%DESKTOP%\YouTube Comments Crawler.bat"
    echo pause >> "%DESKTOP%\YouTube Comments Crawler.bat"
    
    REM Create shortcut for system test
    echo @echo off > "%DESKTOP%\Test YouTube Crawler System.bat"
    echo cd /d "%CURRENT_DIR%" >> "%DESKTOP%\Test YouTube Crawler System.bat"
    echo python test_system.py >> "%DESKTOP%\Test YouTube Crawler System.bat"
    
    echo ✅ Desktop shortcuts created!
) else (
    echo ⏭️ Skipping shortcut creation
)

REM Step 5: Setup templates
echo.
echo ==========================================
echo 📍 STEP 5: Setting Up Templates
echo ==========================================

if exist create_template.py (
    echo 📊 Creating Excel template...
    python create_template.py
) else (
    echo ⚠️ create_template.py not found
)

REM Check if templates exist
if exist youtube_urls_template.xlsx (
    echo ✅ Excel template ready
) else (
    echo ⚠️ Excel template not created
)

if exist youtube_urls_template.txt (
    echo ✅ Text template ready
) else (
    echo ⚠️ Text template not created
)

REM Final check
echo.
echo ==========================================
echo 📍 INSTALLATION COMPLETE!
echo ==========================================

echo.
echo ✅ SYSTEM STATUS:
echo.

REM Check main files
if exist youtube_comments_crawler.py (
    echo ✅ Main crawler script: Ready
) else (
    echo ❌ Main crawler script: Missing
)

if exist README.md (
    echo ✅ Documentation: Available
) else (
    echo ⚠️ Documentation: Missing
)

if exist requirements.txt (
    echo ✅ Dependencies list: Available
) else (
    echo ⚠️ Dependencies list: Missing
)

echo.
echo 🎯 NEXT STEPS:
echo.
echo 1. 📖 Read the documentation:
echo    - README.md (complete guide)
echo    - QUICK_START.md (5-minute setup)
echo.
echo 2. 🔑 Get YouTube API Key:
echo    - Visit: https://console.cloud.google.com
echo    - Enable YouTube Data API v3
echo    - Create credentials (API Key)
echo.
echo 3. 🚀 Start crawling:
echo    - Double-click: YouTube Comments Crawler.bat (if shortcut created)
echo    - Or run: python youtube_comments_crawler.py
echo    - Or use: run.bat
echo.
echo 4. 🧪 Test system (if needed):
echo    - Run: python test_system.py
echo    - Or double-click: Test YouTube Crawler System.bat
echo.

echo 💡 HELPFUL FILES:
echo    📊 youtube_urls_template.xlsx - Excel template for URLs
echo    📄 youtube_urls_template.txt  - Text template for URLs
echo    ⚙️ config_template.ini        - Configuration template
echo.

echo 🎓 FOR ACADEMIC RESEARCH:
echo    - Use Excel template for organized URL lists
echo    - Enable sentiment analysis in configuration
echo    - Export results to Excel for statistical analysis
echo    - Follow ethical research guidelines
echo.

echo 🆘 NEED HELP?
echo    - Check README.md for detailed instructions
echo    - Check QUICK_START.md for fast setup
echo    - Visit GitHub issues for community support
echo.

echo 🎉 Happy researching!
echo.

set /p OPEN_DOCS="Open documentation now? (y/n): "
if /i "%OPEN_DOCS%"=="y" (
    if exist README.md (
        start README.md
    )
    if exist QUICK_START.md (
        start QUICK_START.md
    )
)

set /p RUN_NOW="Run YouTube Comments Crawler now? (y/n): "
if /i "%RUN_NOW%"=="y" (
    echo.
    echo 🚀 Starting YouTube Comments Crawler...
    echo.
    python youtube_comments_crawler.py
)

echo.
echo 👋 Installation complete! Press any key to exit...
pause >nul
