# 🦇 BatmanWL Bot - Premium Telegram Bot 🦇

**BatmanWL** (𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot) is a feature-rich Telegram bot with a premium key system, allowing administrators to grant time-limited access to exclusive features.

## ✨ Features

### 🎯 Key System
- **Time-Limited Keys**: Create keys with specific durations (e.g., 24 hours, 7 days, 30 days)
- **Usage Limits**: Keys can be single-use or multi-use (or unlimited)
- **Easy Redemption**: Users can redeem keys with a simple command
- **Automatic Expiration**: Premium access expires automatically after the specified time

### 👑 Role-Based Access
- **Owner**: Full access to all features without restrictions
- **Admins**: Full access to all features and key management
- **Premium Users**: Access to premium features while their key is active
- **Free Users**: Access to basic features only

### ⭐ Premium Features
- **AI Image Generation** (`/genimage`) - Generate images from text prompts
- **File Conversion** (`/convert`) - Convert files between different formats
- **Advanced Search** (`/search`) - Powerful web search capabilities
- **Text Translation** (`/translate`) - Translate text to different languages

### 🆓 Free Features
- **Weather Information** (`/weather`) - Get weather data for any city
- **Calculator** (`/calc`) - Perform mathematical calculations
- **Status Check** (`/status`) - View your premium status and role

### 🔧 Admin Features
- **Key Generation** (`/genkey`) - Create premium keys with custom duration and usage limits
- **Key Management** (`/listkeys`) - View all generated keys
- **Key Deactivation** (`/deactivate`) - Disable specific keys
- **Statistics** (`/stats`) - View bot usage statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip3
- A Telegram account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ElBrido/telegrambot.git
   cd telegrambot
   ```

2. **Install dependencies**
   ```bash
   ./install_dependencies.sh
   ```
   This script will:
   - Check for Python and pip
   - Create a virtual environment
   - Install all required packages

3. **Configure the bot**
   ```bash
   ./setup.sh
   ```
   This script will ask you for:
   - Bot token (get it from [@BotFather](https://t.me/BotFather))
   - Your Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot))
   - Admin user IDs (optional)

4. **Start the bot**
   ```bash
   source venv/bin/activate
   python3 bot.py
   ```

### Manual Configuration

If you prefer to configure manually, copy `.env.example` to `.env` and edit it:

```bash
cp .env.example .env
nano .env
```

Fill in the required values:
- `BOT_TOKEN`: Your bot token from @BotFather
- `OWNER_ID`: Your Telegram user ID
- `ADMIN_IDS`: Comma-separated list of admin user IDs (optional)

## 📖 Usage

### For Users

1. **Start the bot**
   ```
   /start
   ```

2. **Check your status**
   ```
   /status
   ```

3. **Redeem a premium key**
   ```
   /redeem YOUR_KEY_HERE
   ```

4. **Use premium features**
   ```
   /genimage a beautiful sunset over mountains
   /search best programming practices
   /translate es Hello, how are you?
   ```

5. **Use free features**
   ```
   /weather London
   /calc 2 + 2 * 3
   ```

### For Admins

1. **Generate a premium key**
   ```
   /genkey 24 1        # 24 hours, single use
   /genkey 168 10      # 7 days, 10 uses
   /genkey 720 -1      # 30 days, unlimited uses
   ```

2. **List all keys**
   ```
   /listkeys
   ```

3. **Deactivate a key**
   ```
   /deactivate KEY_STRING
   ```

4. **View statistics**
   ```
   /stats
   ```

## 🔑 Key System Details

### Key Duration
Keys can be created with any duration in hours:
- 24 hours = 1 day
- 168 hours = 7 days
- 720 hours = 30 days
- Custom durations as needed

### Usage Limits
- **Single use** (`max_uses = 1`): Key can only be redeemed once
- **Multi-use** (`max_uses = N`): Key can be redeemed N times
- **Unlimited** (`max_uses = -1`): Key can be redeemed unlimited times

### Key Features
- Keys are automatically deactivated when usage limit is reached
- Premium access expires automatically after the specified duration
- Users can check their remaining premium time with `/status`
- Admins can manually deactivate keys at any time

## 📁 Project Structure

```
telegrambot/
├── bot.py                    # Main bot file
├── config.py                 # Configuration management
├── database.py              # Database models and functions
├── features.py              # Premium and free features
├── requirements.txt         # Python dependencies
├── setup.sh                 # Quick setup script
├── install_dependencies.sh  # Dependency installation script
├── .env.example            # Example environment file
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔒 Security

- Bot token and sensitive data are stored in `.env` file (not committed to git)
- Database file is excluded from version control
- Keys are generated using cryptographically secure random tokens
- Admin and owner roles are strictly enforced

## 🛠 Customization

### Adding New Premium Features

1. Open `features.py`
2. Add your new feature function
3. Open `bot.py`
4. Add a command handler with the `@require_premium` decorator

Example:
```python
# In features.py
def my_new_feature(param):
    # Your feature logic here
    return "Result"

# In bot.py
@require_premium
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    result = my_new_feature(context.args[0])
    await update.message.reply_text(result)

# Register in main()
application.add_handler(CommandHandler("mycommand", my_command))
```

### Implementing Real API Integrations

The bot includes placeholder implementations for premium features. To enable real functionality:

1. **Image Generation**: Integrate with DALL-E, Stable Diffusion, or similar
2. **File Conversion**: Use Pillow, ffmpeg, or similar tools
3. **Advanced Search**: Integrate with Google Custom Search, Bing API, etc.
4. **Weather**: Use OpenWeatherMap or similar weather API
5. **Translation**: Use Google Translate API, DeepL, or similar

Add your API keys to `.env` and implement the integrations in `features.py`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📝 License

This project is open source and available for personal and commercial use.

## 👨‍💻 Author

Created by ElBrido

## 🆘 Support

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Contact the bot owner through Telegram

## 🎉 Acknowledgments

Inspired by various Telegram bot projects and premium bot systems.

---

**Enjoy your BatmanWL Bot! 🦇**