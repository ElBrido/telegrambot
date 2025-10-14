# 🚀 Deployment Guide

This guide covers various deployment options for the Supreme Card Checker Bot.

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Admin User IDs

## Method 1: Local Deployment

### Step 1: Setup

```bash
# Clone the repository
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot

# Run setup script
bash setup.sh
```

### Step 2: Configuration

Edit `.env` file with your credentials:

```bash
nano .env
```

Add your configuration:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
```

### Step 3: Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot
python bot.py
```

Or simply:
```bash
bash run.sh
```

## Method 2: Docker Deployment

### Using Docker Compose (Recommended)

1. **Create `.env` file:**
```bash
cp .env.example .env
nano .env
```

2. **Build and run:**
```bash
docker-compose up -d
```

3. **View logs:**
```bash
docker-compose logs -f
```

4. **Stop the bot:**
```bash
docker-compose down
```

### Using Docker directly

1. **Build the image:**
```bash
docker build -t supreme-card-checker-bot .
```

2. **Run the container:**
```bash
docker run -d \
  --name card-checker-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  supreme-card-checker-bot
```

## Method 3: VPS Deployment

### Using systemd (Linux)

1. **Create service file:**
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

2. **Add configuration:**
```ini
[Unit]
Description=Supreme Card Checker Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegrambot
ExecStart=/path/to/telegrambot/venv/bin/python /path/to/telegrambot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

4. **Check status:**
```bash
sudo systemctl status telegram-bot
```

## Method 4: Heroku Deployment

1. **Create Procfile:**
```
worker: python bot.py
```

2. **Create runtime.txt:**
```
python-3.11.0
```

3. **Deploy:**
```bash
heroku create your-bot-name
heroku config:set BOT_TOKEN=your_token_here
heroku config:set ADMIN_IDS=123456789,987654321
git push heroku main
heroku ps:scale worker=1
```

## Method 5: Cloud Platforms

### AWS EC2

1. Launch an EC2 instance (Ubuntu 20.04 or later)
2. SSH into the instance
3. Follow "Local Deployment" steps
4. Use systemd for auto-restart (see VPS deployment)

### Google Cloud Platform

1. Create a Compute Engine instance
2. SSH into the instance
3. Follow "Local Deployment" steps
4. Configure firewall rules if needed

### DigitalOcean Droplet

1. Create a droplet (Ubuntu)
2. SSH into the droplet
3. Follow "Local Deployment" steps
4. Use systemd for persistence

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_TOKEN` | Yes | - | Telegram bot token from BotFather |
| `ADMIN_IDS` | Yes | - | Comma-separated admin user IDs |
| `DATABASE_PATH` | No | `bot_database.db` | Path to SQLite database |
| `DEFAULT_CREDITS` | No | `5` | Default credits for new users |
| `MASS_CHECK_MIN_CREDITS` | No | `5` | Minimum credits for mass check |
| `MAX_MASS_CHECK_CARDS` | No | `10` | Maximum cards per mass check |
| `PREMIUM_UNLIMITED` | No | `true` | Enable unlimited for premium users |
| `BOT_NAME` | No | `Supreme Card Checker Bot` | Bot display name |
| `BOT_VERSION` | No | `2.0.0` | Bot version |
| `CHANNEL_URL` | No | - | Your Telegram channel URL |
| `SUPPORT_URL` | No | - | Support contact URL |
| `ADMIN_URL` | No | - | Admin contact URL |

## Monitoring

### View Logs

**Local:**
```bash
tail -f logs/bot.log
```

**Docker:**
```bash
docker logs -f supreme-card-checker-bot
```

**Systemd:**
```bash
journalctl -u telegram-bot -f
```

### Database Backup

**Manual backup:**
```bash
cp bot_database.db bot_database_backup_$(date +%Y%m%d).db
```

**Automated backup (cron):**
```bash
# Add to crontab
0 2 * * * cp /path/to/bot_database.db /path/to/backups/bot_db_$(date +\%Y\%m\%d).db
```

## Troubleshooting

### Bot not responding

1. Check if bot is running:
```bash
ps aux | grep bot.py
```

2. Check logs for errors
3. Verify bot token is correct
4. Ensure network connectivity

### Database errors

1. Check database file permissions
2. Verify database path in `.env`
3. Try removing and recreating database (will lose data)

### Import errors

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Check Python version (3.8+)

## Security Recommendations

1. **Never commit `.env` file** - Always use `.env.example`
2. **Keep bot token secure** - Don't share publicly
3. **Regular backups** - Backup database regularly
4. **Update dependencies** - Keep packages up to date
5. **Monitor admin actions** - Check logs regularly
6. **Use HTTPS** - For webhook mode (if used)
7. **Restrict admin access** - Only add trusted admins

## Scaling

### For High Traffic

1. **Use Redis** for session storage instead of in-memory
2. **Database optimization** - Consider PostgreSQL for production
3. **Load balancing** - Deploy multiple instances behind load balancer
4. **Caching** - Implement caching for BIN lookups
5. **Async optimization** - Use connection pooling

### Multiple Instances

If running multiple instances, ensure:
- Shared database (PostgreSQL/MySQL)
- Shared session storage (Redis)
- Message queue for broadcasts

## Maintenance

### Updating the Bot

1. **Backup database:**
```bash
cp bot_database.db bot_database.backup
```

2. **Pull latest changes:**
```bash
git pull origin main
```

3. **Update dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

4. **Restart bot:**
```bash
sudo systemctl restart telegram-bot
```

### Database Maintenance

```bash
# Check database integrity
sqlite3 bot_database.db "PRAGMA integrity_check;"

# Optimize database
sqlite3 bot_database.db "VACUUM;"
```

## Support

For deployment issues:
- Check GitHub Issues
- Contact support: @your_support
- Review logs for error messages

---

Happy deploying! 🚀
