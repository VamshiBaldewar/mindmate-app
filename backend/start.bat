@echo off
REM GathaFeed Backend Startup Script for Windows

echo 🚀 Starting GathaFeed Backend Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Set environment variables
set FLASK_ENV=development
set SECRET_KEY=gathafeed-secret-key-2024
set GOOGLE_API_KEY=AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs
set PROJECT_ID=gathafeed-ai
set REGION=us-central1

REM Start the Flask application
echo 🌟 Starting Flask application...
echo 📍 Server will be available at: http://localhost:5000
echo 🔗 API endpoints available at: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
