# 🔐 Professional Telegram Credit Card Verification Bot

A comprehensive Telegram bot for professional credit card verification with advanced features including CCN checking, BIN lookup, VBV verification, and mass card generation.

## ✨ Features

### 🔍 Card Verification
- **CCN Checker** - Validate credit card numbers using Luhn algorithm
- **CCN Charge** - Test card charging capabilities
- **BIN Lookup** - Get detailed BIN information
- **VBV Checker** - Verify by Visa (3D Secure) status checking
- **Card Status** - Check if cards are active or inactive

### 🎲 Card Generation
- **Mass Generator** - Generate valid card numbers from BIN
- **Custom Quantity** - Generate up to 50 cards at once
- **Format Support** - Generates cards with expiry and CVV

### 👥 Admin Management
- **Owner System** - Full control over bot permissions
- **Admin System** - Delegated access for trusted users
- **Access Control** - Commands restricted by role

### 🎨 User Interface
- **Interactive Panels** - Beautiful inline keyboard menus
- **GIF Support** - Customizable welcome GIF
- **Status Display** - Real-time user role information
- **Help System** - Comprehensive command documentation

## 📋 Commands

### General Commands
- `/start` - Show welcome panel with all features
- `/help` or `/cmds` - Display all available commands
- `/status` - Check your access level and permissions

### Verification Commands (Admin Only)
- `.chk <card>|<mm>|<yy>|<cvv>` - Check card validity (CCN Checker)
- `.ch <card>|<mm>|<yy>|<cvv>` - Charge verification (CCN CH)
- `.bin <bin_number>` - BIN lookup information
- `.vbv <card>|<mm>|<yy>|<cvv>` - Verify by Visa checker
- `.status <card>|<mm>|<yy>|<cvv>` - Check if card is active/inactive

### Generation Commands (Admin Only)
- `.gen <bin> <quantity>` - Generate cards from BIN (max 50)
- `.mass <bin>` - Generate 10 cards from BIN

### Admin Commands (Owner Only)
- `/addadmin <user_id>` - Add a new admin
- `/removeadmin <user_id>` - Remove an admin
- `/addowner <user_id>` - Add a new owner
- `/listadmins` - List all admins and owners

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure the Bot
Edit `config.json` and add your credentials:
```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "welcome_gif_url": "YOUR_GIF_URL_HERE",
  "owners": [123456789],
  "admins": []
}
```

**Configuration Options:**
- `bot_token` - Your Telegram bot token from BotFather (required)
- `welcome_gif_url` - URL to a GIF for the welcome message (optional)
- `owners` - List of Telegram user IDs with full access (required)
- `admins` - List of Telegram user IDs with verification access (optional)

### Step 4: Get Your User ID
1. Start a chat with [@userinfobot](https://t.me/userinfobot)
2. Copy your user ID
3. Add it to the `owners` array in `config.json`

### Step 5: Run the Bot
```bash
python bot.py
```

The bot should now be running and responding to commands!

## 📖 Usage Examples

### Checking a Card
```
.chk 4532015112830366|12|25|123
```

### BIN Lookup
```
.bin 453201
```

### Generating Cards
```
.gen 453201 10
```

### Mass Generate
```
.mass 453201
```

### Adding an Admin
```
/addadmin 987654321
```

## 🔒 Security Features

- **Role-based Access Control** - Commands restricted by user role
- **Owner-only Admin Management** - Only owners can modify permissions
- **User ID Verification** - All actions tied to Telegram user IDs
- **Persistent Configuration** - Settings saved across restarts

## ⚠️ Important Notes

### Legal Disclaimer
This bot is for **educational and testing purposes only**. The verification features are simulated and do not perform real credit card transactions. 

**DO NOT:**
- Use this bot for illegal activities
- Test cards you don't own
- Attempt real financial fraud
- Share sensitive card information

**Legal Use Cases:**
- Testing payment integration systems
- Educational purposes
- Security research with proper authorization
- Development and QA testing

### Security Warning
- Keep your `config.json` file private
- Never commit your bot token to public repositories
- Use `.gitignore` to exclude sensitive files
- Regularly rotate your bot token

## 🛠️ Technical Details

### Architecture
- **Framework:** python-telegram-bot 20.7
- **Language:** Python 3.8+
- **Card Validation:** Luhn algorithm implementation
- **BIN Lookup:** Integration with BINList API
- **Storage:** JSON-based configuration

### Card Validation
The bot uses the Luhn algorithm (mod 10) to validate card numbers:
1. Double every second digit from right to left
2. Subtract 9 from digits greater than 9
3. Sum all digits
4. Valid if sum is divisible by 10

### Card Generation
Cards are generated with:
- Valid Luhn checksum
- Random digits completing the BIN
- Realistic expiry dates (25-30)
- Random CVV codes (100-999)

## 🔧 Troubleshooting

### Bot Not Starting
- Verify bot token is correct in `config.json`
- Check Python version: `python --version` (must be 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Commands Not Working
- Ensure you're added as an owner in `config.json`
- Restart the bot after configuration changes
- Check bot logs for error messages

### BIN Lookup Failing
- The bot uses a free API that may have rate limits
- Check your internet connection
- The bot will fallback to basic info if API fails

## 📝 Development

### Adding New Features
The bot is designed to be easily extensible. To add new commands:

1. Create a new handler function
2. Register it in the `main()` function
3. Add documentation to help text
4. Test thoroughly before deployment

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is provided as-is for educational purposes. Use responsibly and in compliance with all applicable laws and regulations.

## 👤 Credits

Developed by @YourChannel

For support or questions, contact the repository owner.

## 🔗 Links

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Library](https://python-telegram-bot.org/)
- [BotFather - Create Telegram Bots](https://t.me/BotFather)

---

**Remember:** This is a simulation tool. Never use it for illegal activities or with real financial data without proper authorization.