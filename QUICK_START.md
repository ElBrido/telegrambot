# 🚀 Quick Start Guide

Get your Telegram CC Verification Bot running in 5 minutes!

## ⚡ Fast Setup

### 1. Get Your Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your User ID
1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Start the bot
3. Copy your user ID (a number like `123456789`)

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Setup (Recommended)
```bash
python setup.py
```
Follow the interactive prompts to configure your bot.

**OR** Manual Configuration:
1. Copy `config.example.json` to `config.json`
2. Edit `config.json` with your bot token and user ID

### 5. Start the Bot
```bash
python bot.py
```

You should see: `Bot started successfully!`

### 6. Test Your Bot
1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. You should see the welcome panel!

## 📱 First Commands to Try

### Check Your Status
```
/status
```
You should see "👑 Owner" as your role.

### Add an Admin (Optional)
```
/addadmin 987654321
```
Replace `987654321` with a friend's user ID.

### Test Card Checking
```
.chk 4532015112830366|12|25|123
```

### Test BIN Lookup
```
.bin 453201
```

### Generate Cards
```
.gen 453201 10
```

## ❓ Troubleshooting

### "Bot token not set"
- Make sure you edited `config.json` with your real bot token
- Check that the file is named exactly `config.json` (not `config.json.txt`)

### "Commands not working"
- Make sure you added your user ID to the `owners` array
- Restart the bot after making config changes
- Check that you're using the correct command format

### "Module not found"
- Run: `pip install -r requirements.txt`
- Make sure you have Python 3.8 or higher

## 🎯 Next Steps

1. **Add a Welcome GIF**: Edit `welcome_gif_url` in `config.json`
2. **Add Admins**: Use `/addadmin <user_id>` to add trusted users
3. **Customize**: Edit `bot.py` to add your own features
4. **Deploy**: Consider hosting on a server for 24/7 operation

## 📚 Learn More

- Read the full [README.md](README.md) for all features
- Check `/help` command in the bot for command list
- Join our community for support

---

**Ready to go?** Start with `/start` in your bot! 🎉
