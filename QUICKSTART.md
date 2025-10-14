# 🚀 Quick Start Guide

Get your Supreme Card Checker Bot up and running in 5 minutes!

## Step 1: Get Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your User ID

1. Search for [@userinfobot](https://t.me/userinfobot) in Telegram
2. Start the bot
3. It will show your user ID (e.g., `123456789`)

## Step 3: Install

### Option A: Using Setup Script (Recommended)

```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
bash setup.sh
```

### Option B: Manual Installation

```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Step 4: Configure

Edit `.env` file:

```bash
nano .env
```

Add your bot token and user ID:

```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS=123456789
```

Save and exit (Ctrl+X, then Y, then Enter)

## Step 5: Run

```bash
source venv/bin/activate
python bot.py
```

Or simply:
```bash
bash run.sh
```

## Step 6: Test

1. Open Telegram and search for your bot
2. Send `/start` command
3. You should see the welcome panel with all features!

## 🎉 That's it!

Your bot is now running. Try these commands:

- `/chk 4111111111111111|12|2025|123` - Check a card
- `/bin 411111` - Get BIN info
- `/profile` - View your profile
- `/help` - See all commands

## Troubleshooting

**Bot not responding?**
- Check if bot is running: `ps aux | grep bot.py`
- Check for errors in terminal
- Verify bot token is correct

**Permission errors?**
- Run: `chmod +x setup.sh run.sh`

**Module not found?**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Next Steps

- Read [README.md](README.md) for full feature list
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Need Help?

- 📢 Channel: @your_channel
- 💬 Support: @your_support
- 🐛 Issues: [GitHub Issues](https://github.com/ElBrido/telegrambot/issues)

---

Enjoy your Supreme Card Checker Bot! 🎯
