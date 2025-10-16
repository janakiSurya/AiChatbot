#!/bin/bash

# Boku AI Assistant Deployment Script

set -e

echo "🚀 Deploying Boku AI Assistant..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy env.example to .env and configure it."
    exit 1
fi

# Check if HF_API_KEY is set
if ! grep -q "HF_API_KEY=" .env || grep -q "HF_API_KEY=your_huggingface_api_key_here" .env; then
    echo "❌ Please set your HF_API_KEY in the .env file."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python test_complete_system.py

# Start the application
echo "🎉 Starting Boku AI Assistant..."
echo "📱 Access the application at: http://localhost:7871"
python app.py
