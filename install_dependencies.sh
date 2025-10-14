#!/bin/bash
# Install dependencies for BatmanWL Bot

echo "🦇 BatmanWL Bot - Installing Dependencies 🦇"
echo "============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📥 Installing Python packages..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================="
    echo "✅ All dependencies installed successfully!"
    echo "============================================="
    echo ""
    echo "Next steps:"
    echo "1. Run ./setup.sh to configure the bot"
    echo "2. Activate the virtual environment: source venv/bin/activate"
    echo "3. Start the bot: python3 bot.py"
else
    echo ""
    echo "❌ Failed to install dependencies!"
    echo "Please check the error messages above."
    exit 1
fi
