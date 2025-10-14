# ❓ Frequently Asked Questions (FAQ)

## General Questions

### What is this bot?
This is a comprehensive Telegram bot for credit card validation and checking. It uses industry-standard algorithms (Luhn) to validate card numbers and provides detailed information about cards and BINs.

### Is this bot free?
The bot operates on a credit system. New users receive free credits to start. Additional credits can be obtained through premium plans or admin grants.

### Is it safe to use?
The bot is designed with security in mind. However, note that this is a simulation for educational purposes. Only the last 4 digits of card numbers are stored in the database for privacy.

### How does the card checking work?
The bot validates cards using the Luhn algorithm and simulates gateway responses. In production environments, you would integrate with actual payment gateways.

---

## Getting Started

### How do I start using the bot?
1. Search for the bot in Telegram
2. Send `/start` command
3. You'll receive welcome credits
4. Use `/chk` to check your first card

### How do I get my first credits?
New users automatically receive default credits (usually 5) when they first use `/start`.

### What commands can I use?
Send `/help` to see all available commands. You can use both `/` and `.` prefixes for all commands.

### Can I use commands with a dot (.) instead of slash (/)?
Yes! All commands support both prefixes. For example, both `/chk` and `.chk` work the same way.

---

## Card Checking

### What format should I use for card checking?
Use this format: `card_number|month|year|cvv`

Example: `/chk 4111111111111111|12|2025|123`

### How many cards can I check at once?
- Single check: 1 card (costs 1 credit)
- Mass check: Up to 10 cards at once (costs 1 credit per card, minimum 5 credits required)

### What card types are supported?
The bot supports:
- VISA
- Mastercard
- American Express (AMEX)
- Discover
- Diners Club
- JCB

### What does "APPROVED" or "DECLINED" mean?
These are simulated responses. In production:
- **APPROVED**: Card passed validation checks
- **DECLINED**: Card failed validation (various reasons)

### Why does the bot show different response codes?
Different codes indicate different reasons for approval or decline (e.g., CVV match, insufficient funds, expired card, etc.)

### Does the bot store my card numbers?
Only the last 4 digits are stored in the database for statistical purposes. Full card numbers are never stored.

---

## Credits System

### What are credits?
Credits are the currency used in the bot. Each card check costs 1 credit.

### How do I check my credit balance?
Use the `/credits` command to see your current balance.

### How can I get more credits?
1. Purchase premium plans (see `/plans`)
2. Contact an admin for credit grants
3. Wait for promotional offers

### Do credits expire?
Credits don't expire for free users. Premium plans have validity periods as specified in each plan.

### What happens if I run out of credits?
You won't be able to check cards until you get more credits. Use `/plans` to see options.

---

## Premium Plans

### What are premium plans?
Premium plans offer more credits and additional features like unlimited checks, priority support, and faster processing.

### How do I purchase a premium plan?
1. Use `/plans` to see available plans
2. Contact the admin via the provided link
3. Follow payment instructions
4. Your account will be upgraded once payment is confirmed

### What payment methods are accepted?
Common payment methods include PayPal, cryptocurrency, and bank transfers. Contact admin for current options.

### Can I get a refund?
Refund policies depend on the plan. Contact admin for details.

---

## Admin & Group Features

### How do I become an admin?
Admin status is controlled by the bot owner. Contact them if you need admin access.

### What can admins do?
Admins can:
- Ban/unban users
- Add credits to any user
- Broadcast messages to all users
- View global statistics
- Access admin logs

### Can I use this bot in groups?
Yes! The bot has special group features like welcome messages, rules, and invite link generation.

### How do I add the bot to my group?
1. Add the bot to your group as a member
2. Promote it to admin (for full features)
3. Use group commands like `/welcome` and `/rules`

### What permissions does the bot need in groups?
For full functionality, the bot needs:
- Send messages
- Delete messages (for cleanup)
- Manage invite links (for `/link` command)

---

## Troubleshooting

### The bot is not responding
**Check:**
1. Is the bot online? Use `/status` from another chat
2. Are you banned? Contact an admin
3. Is Telegram having issues? Check telegram status

### I get "Invalid format" error
Make sure you're using the correct format: `card|mm|yyyy|cvv`

Example: `4111111111111111|12|2025|123`

### "You don't have enough credits" message
You need to get more credits. Use `/credits` to check your balance and `/plans` to see options.

### My card shows as "DECLINED" but I know it's valid
The bot simulates responses for testing. Real-world integration would give actual results from payment gateways.

### Commands don't work in group
Some commands are private-only (like `/chk`). Use them in a private chat with the bot.

### I was banned by mistake
Contact an admin immediately. They can review and unban your account.

---

## Technical Questions

### What technology is used?
- **Language**: Python 3.8+
- **Framework**: python-telegram-bot
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Deployment**: Docker, systemd, or direct Python

### Can I run my own instance?
Yes! The bot is open source. Follow the setup guide in [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md).

### How do I report bugs?
Open an issue on GitHub or contact support via Telegram.

### Can I contribute to development?
Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Is the source code available?
Yes, the project is open source on GitHub: https://github.com/ElBrido/telegrambot

### Can I customize the bot?
Yes! You can modify any aspect of the bot. Check the configuration in `config.py` and `.env`.

---

## Security & Privacy

### Is my data safe?
- Only last 4 digits of cards are stored
- User IDs and statistics are stored
- No sensitive information is logged in plain text
- Database is local to your instance

### Does the bot share my information?
No. All data stays in your local database. No information is shared with third parties.

### What should I do if I suspect a security issue?
Contact the admin immediately or report it on GitHub (for responsible disclosure).

### Can admins see my card numbers?
No. Card numbers are never stored in full. Only last 4 digits are logged.

---

## Premium Features

### What's the difference between free and premium?
**Free:**
- Limited credits
- Standard check speed
- Basic support

**Premium:**
- Unlimited credits (on premium plans)
- Priority support
- Premium badge
- Faster checks

### How long does premium last?
Each plan has its own validity period (7, 30, or 90 days depending on the plan).

### What happens when premium expires?
You revert to free tier with remaining credits. You won't lose your data or statistics.

### Can I upgrade my plan?
Yes, contact admin to upgrade to a higher tier plan.

---

## Contact & Support

### How do I get help?
1. Read this FAQ
2. Use `/help` command in bot
3. Contact support via links in `/info`
4. Open issue on GitHub

### Where can I find updates?
Follow the official channel (link in `/info` command) for updates and announcements.

### Who maintains this bot?
Created and maintained by @ElBrido and the open source community.

### How do I report inappropriate behavior?
Contact an admin immediately with details (user ID, screenshot if possible).

---

## Still have questions?

- 📚 Check [README.md](README.md) for detailed information
- 📋 See [COMMANDS.md](COMMANDS.md) for command reference
- 🚀 Read [QUICKSTART.md](QUICKSTART.md) for quick setup
- 💬 Contact support: @your_support
- 📢 Join channel: @your_channel

---

*Last updated: 2024*
