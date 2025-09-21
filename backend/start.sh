#!/bin/bash

# GathaFeed Backend Startup Script

echo "🚀 Starting GathaFeed Backend Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export SECRET_KEY="gathafeed-secret-key-2024"
export GOOGLE_API_KEY="AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs"
export PROJECT_ID="gathafeed-ai"
export REGION="us-central1"

# Start the Flask application
echo "🌟 Starting Flask application..."
echo "📍 Server will be available at: http://localhost:5000"
echo "🔗 API endpoints available at: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
