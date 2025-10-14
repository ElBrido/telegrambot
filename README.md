# 🎯 Supreme Card Checker Telegram Bot

A comprehensive, feature-rich Telegram bot for credit card validation and checking. This bot is designed to be superior to other card checkers with a complete set of features, admin controls, and user management.

## ✨ Features

### 💳 Card Checking
- **Single Card Check**: Validate individual credit cards with detailed response
- **Mass Card Check**: Check multiple cards at once
- **BIN Information**: Get detailed BIN (Bank Identification Number) data
- **Luhn Algorithm**: Validates card numbers using industry-standard algorithm
- **Support Multiple Card Types**: VISA, Mastercard, AMEX, Discover, Diners, JCB

### 👤 User Features
- **User Profiles**: Complete user profile with statistics
- **Credit System**: Track and manage user credits
- **Statistics**: Detailed checking history and success rates
- **Premium Plans**: Multiple subscription tiers
- **Dual Command Support**: Use both `/` and `.` prefixes for all commands

### 🔐 Admin Features
- **User Management**: Ban/unban users
- **Credit Management**: Add or remove credits from users
- **Broadcast System**: Send messages to all users
- **Global Statistics**: View bot-wide statistics
- **Admin Logs**: Track all admin actions
- **User Monitoring**: View user activity and history

### 👥 Group Features
- **Welcome Messages**: Customizable welcome for new members
- **Group Rules**: Set and display group rules
- **Invite Links**: Generate and manage group invite links

### 🛡️ Security & Performance
- **Database Integration**: SQLite for persistent data storage
- **Rate Limiting**: Prevent abuse with credit system
- **User Banning**: Block malicious users
- **Input Validation**: Secure card data handling
- **Logging System**: Track all operations

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` file and add your configuration:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
DATABASE_PATH=bot_database.db
```

4. **Run the bot**
```bash
python bot.py
```

## 📋 Commands Reference

### User Commands (Available to all users)

| Command | Alternative | Description |
|---------|-------------|-------------|
| `/start` | `.start` | Show welcome panel with all features |
| `/chk` | `.chk` | Check a credit card |
| `/mass` | `.mass` | Mass check multiple cards |
| `/bin` | `.bin` | Get BIN information |
| `/profile` | `.profile` | View your profile |
| `/stats` | `.stats` | View your statistics |
| `/credits` | `.credits` | Check credit balance |
| `/help` | `.help` | Show help menu |
| `/plans` | `.plans` | View premium plans |
| `/status` | `.status` | Check bot status |
| `/info` | `.info` | Bot information |

### Group Commands

| Command | Description |
|---------|-------------|
| `/welcome` | Set welcome message |
| `/rules` | Display group rules |
| `/link` | Get group invite link |

### Admin Commands (Restricted to administrators)

| Command | Alternative | Description |
|---------|-------------|-------------|
| `/broadcast` | `.broadcast` | Send message to all users |
| `/ban` | `.ban` | Ban a user |
| `/unban` | `.unban` | Unban a user |
| `/addcredits` | `.addcredits` | Add credits to user |
| `/stats_admin` | `.stats_admin` | View global statistics |
| `/users` | `.users` | List all users |
| `/logs` | `.logs` | View admin action logs |

## 💡 Usage Examples

### Checking a Card
```
/chk 4111111111111111|12|2025|123
.chk 5500000000000004|01|2026|456
```

### Admin Operations
```
/ban 123456789
/addcredits 123456789 100
/broadcast Welcome to the new version!
```

## 🏗️ Project Structure

```
telegrambot/
├── bot.py              # Main bot application
├── database.py         # Database management
├── card_checker.py     # Card validation logic
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## 🔧 Configuration

### Environment Variables

- `BOT_TOKEN`: Your Telegram bot token from BotFather
- `ADMIN_IDS`: Comma-separated list of admin user IDs
- `DATABASE_PATH`: Path to SQLite database file

### Adding Administrators

Add admin user IDs to the `.env` file:
```env
ADMIN_IDS=123456789,987654321,555555555
```

## 📊 Database Schema

The bot uses SQLite with the following tables:

- **users**: User information and settings
- **card_checks**: History of card validations
- **admin_logs**: Admin action tracking

## 🛠️ Development

### Running in Development Mode

```bash
python bot.py
```

### Database Management

The database is automatically created on first run. To reset:
```bash
rm bot_database.db
python bot.py
```

## 🔒 Security Notes

- Never commit your `.env` file
- Keep your bot token secure
- Regularly backup your database
- Monitor admin logs for suspicious activity
- Update dependencies regularly

## 📈 Premium Plans

The bot includes a credit system with premium plans:

- **Basic**: 100 credits, 7 days
- **Standard**: 500 credits + 50 bonus, 30 days
- **Premium**: Unlimited credits, 30 days, priority support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Telegram: @your_support
- Channel: @your_channel

## ⚠️ Disclaimer

This bot is for educational purposes only. Always comply with local laws and regulations regarding financial data handling. The bot simulates card checking and should not be used with real card validation services without proper authorization and compliance with payment card industry standards.

## 🎯 Why This Bot is Superior

1. **Complete Feature Set**: All features fully implemented and working
2. **Dual Command Support**: Use `/` or `.` prefix for convenience
3. **Professional Admin Panel**: Comprehensive admin tools
4. **User Management**: Complete user tracking and statistics
5. **Security First**: Built-in protections and logging
6. **Clean Code**: Well-organized and documented
7. **Database Powered**: Persistent data storage
8. **Scalable Design**: Ready for production use
9. **Active Development**: Regular updates and improvements
10. **Beautiful UI**: Attractive inline keyboards and formatting

---

Made with ❤️ by ElBrido