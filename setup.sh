#!/bin/bash
# Setup script for BatmanWL Bot

echo "🦇 BatmanWL Bot - Setup Wizard 🦇"
echo "================================="
echo ""

# Check if .env file exists
if [ -f ".env" ]; then
    echo "⚠️  Warning: .env file already exists!"
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Using existing .env file."
        exit 0
    fi
fi

echo "Let's configure your bot!"
echo ""

# Get bot token
echo "📝 Step 1: Bot Token"
echo "Get your bot token from @BotFather on Telegram"
read -p "Enter your bot token: " BOT_TOKEN
echo ""

# Get owner ID
echo "📝 Step 2: Owner ID"
echo "Get your Telegram user ID from @userinfobot"
read -p "Enter your user ID: " OWNER_ID
echo ""

# Get admin IDs
echo "📝 Step 3: Admin IDs (optional)"
echo "Enter admin user IDs separated by commas (or press Enter to skip)"
read -p "Admin IDs: " ADMIN_IDS
echo ""

# Create .env file
echo "💾 Creating .env file..."
cat > .env << EOF
# Telegram Bot Token from @BotFather
BOT_TOKEN=$BOT_TOKEN

# Owner Telegram ID (your user ID)
OWNER_ID=$OWNER_ID

# Admin IDs (comma-separated list)
ADMIN_IDS=$ADMIN_IDS

# Database path
DATABASE_URL=sqlite:///batmanwl.db

# Bot name
BOT_NAME=𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot
EOF

echo "✅ Configuration saved to .env"
echo ""

# Check if dependencies are installed
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Run ./install_dependencies.sh first to install dependencies."
    echo ""
fi

echo "================================="
echo "✅ Setup complete!"
echo "================================="
echo ""
echo "To start the bot:"
echo "1. Make sure dependencies are installed: ./install_dependencies.sh"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start the bot: python3 bot.py"
echo ""
echo "Enjoy your BatmanWL Bot! 🦇"
