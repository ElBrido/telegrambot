# 🚀 Quick Start Guide for BatmanWL Bot

This guide will help you get your BatmanWL bot up and running in under 5 minutes!

## Prerequisites

- **Python 3.8+** installed on your system
- **pip3** (Python package manager)
- A **Telegram account**

## Step-by-Step Installation

### 1. Get Your Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` to BotFather
3. Follow the instructions to create your bot
4. Name it **BatmanWL** or **𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot**
5. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your User ID

1. Search for **@userinfobot** on Telegram
2. Start a chat and send any message
3. Copy your user ID (a number like: `123456789`)

### 3. Install the Bot

```bash
# Clone the repository
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot

# Install dependencies
./install_dependencies.sh

# Configure the bot
./setup.sh
```

When prompted:
- Enter your **bot token** from step 1
- Enter your **user ID** from step 2
- (Optional) Enter admin user IDs separated by commas

### 4. Start the Bot

```bash
# Activate the virtual environment
source venv/bin/activate

# Start the bot
python3 bot.py
```

You should see:
```
INFO - Database initialized
INFO - Starting 𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot...
```

### 5. Test the Bot

1. Open Telegram and search for your bot
2. Send `/start` to begin
3. Send `/status` to check your role (you should be Owner)

## First Steps as Owner

### Generate Your First Premium Key

```
/genkey 24 1
```

This creates a key that:
- Lasts for 24 hours
- Can be redeemed once

Share this key with a user, and they can redeem it with:
```
/redeem YOUR_KEY_HERE
```

### Common Key Examples

```bash
/genkey 24 1        # 1 day, single use
/genkey 168 10      # 7 days, 10 uses
/genkey 720 -1      # 30 days, unlimited uses
```

### Manage Keys

```bash
/listkeys           # View all generated keys
/deactivate <key>   # Disable a specific key
/stats              # View bot statistics
```

## Available Commands

### For All Users
- `/start` - Welcome message and bot info
- `/help` - Show help message
- `/status` - Check your premium status
- `/weather <city>` - Get weather info
- `/calc <expression>` - Calculate math

### Premium Features
- `/genimage <prompt>` - Generate AI images
- `/search <query>` - Advanced web search
- `/translate <lang> <text>` - Translate text
- `/convert <format>` - Convert files

### Admin Commands
- `/genkey <hours> <uses>` - Generate premium keys
- `/listkeys` - List all keys
- `/deactivate <key>` - Deactivate a key
- `/stats` - View statistics

## Roles Explained

- **👑 Owner**: You! Full access to everything
- **⚡ Admin**: Other users you designate (edit ADMIN_IDS in .env)
- **⭐ Premium**: Users who redeemed a valid key
- **🆓 Free**: Regular users with basic access

## Troubleshooting

### Bot won't start?

1. Check your bot token:
   ```bash
   cat .env | grep BOT_TOKEN
   ```

2. Make sure dependencies are installed:
   ```bash
   source venv/bin/activate
   pip list | grep telegram
   ```

3. Check for errors in the output

### Key won't redeem?

1. Check if the key is still active:
   ```bash
   /listkeys
   ```

2. Make sure it hasn't been fully used (check usage count)

3. Verify the key string is correct (no extra spaces)

## Next Steps

1. **Customize Premium Features**: Edit `features.py` to add real API integrations
2. **Add More Admins**: Edit `.env` and restart the bot
3. **Share Keys**: Generate and distribute keys to your users
4. **Monitor Usage**: Use `/stats` to track bot usage

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the code in `bot.py` to understand the commands
- Open an issue on GitHub if you find bugs

---

**Enjoy your BatmanWL Bot! 🦇**
