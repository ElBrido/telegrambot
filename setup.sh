#!/bin/bash

echo "🎯 Supreme Card Checker Bot - Setup Script"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your BOT_TOKEN and ADMIN_IDS"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your bot token and admin IDs"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python bot.py"
echo ""
echo "🚀 Enjoy your Supreme Card Checker Bot!"
