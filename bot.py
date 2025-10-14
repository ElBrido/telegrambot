"""Main Telegram bot module with comprehensive card checker functionality."""
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode
from dotenv import load_dotenv

from database import Database
from card_checker import CardChecker
from bin_checker import BINChecker
from group_manager import GroupManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]

# Initialize database
db = Database(os.getenv('DATABASE_PATH', 'bot_database.db'))


def is_admin(user_id: int) -> bool:
    """Check if user is an administrator."""
    return user_id in ADMIN_IDS


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with comprehensive panel."""
    user = update.effective_user
    chat = update.effective_chat
    
    # Add user to database
    await db.add_user(user.id, user.username, user.first_name, user.last_name)
    await db.update_last_seen(user.id)
    
    # Check if user is banned
    user_data = await db.get_user(user.id)
    if user_data and user_data['is_banned']:
        await update.message.reply_text(
            "❌ You are banned from using this bot. Contact an administrator."
        )
        return
    
    # Create welcome message with full panel
    welcome_text = f"""
🎯 **Welcome to Supreme Card Checker Bot** 🎯

👋 Hello {user.first_name}!

This is the most advanced card checking bot on Telegram with comprehensive features and admin controls.

━━━━━━━━━━━━━━━━━━━━
📋 **MAIN COMMANDS**
━━━━━━━━━━━━━━━━━━━━

💳 **Card Checking:**
/chk or .chk - Check a credit card
/mass or .mass - Mass check cards
/bin or .bin - Check BIN information

👤 **User Commands:**
/profile or .profile - View your profile
/stats or .stats - Your statistics
/credits or .credits - Check your credits
/help or .help - Show help menu

📊 **Information:**
/status or .status - Bot status
/plans or .plans - Premium plans
/info or .info - Bot information

━━━━━━━━━━━━━━━━━━━━
👥 **GROUP COMMANDS**
━━━━━━━━━━━━━━━━━━━━

/welcome - Set welcome message
/rules - Group rules
/link - Get group invite link

━━━━━━━━━━━━━━━━━━━━
"""
    
    # Add admin commands if user is admin
    if is_admin(user.id):
        welcome_text += """
🔐 **ADMIN COMMANDS**
━━━━━━━━━━━━━━━━━━━━

/broadcast or .broadcast - Send message to all users
/ban or .ban - Ban a user
/unban or .unban - Unban a user
/addcredits or .addcredits - Add credits to user
/stats_admin or .stats_admin - Global statistics
/users or .users - List all users
/logs or .logs - View admin logs

━━━━━━━━━━━━━━━━━━━━
"""
    
    welcome_text += """
💡 **TIP:** You can use commands with / or . prefix!
Example: /chk or .chk

🎁 **Current Credits:** {credits}
👑 **Status:** {status}

━━━━━━━━━━━━━━━━━━━━
🚀 **Ready to check cards? Use /chk to start!**
    """.format(
        credits=user_data['credits'] if user_data else 0,
        status='Premium ⭐' if user_data and user_data['is_premium'] else 'Free'
    )
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("💳 Check Card", callback_data='cmd_chk'),
            InlineKeyboardButton("📊 My Stats", callback_data='cmd_stats')
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data='cmd_help'),
            InlineKeyboardButton("💎 Premium Plans", callback_data='cmd_plans')
        ],
        [
            InlineKeyboardButton("🔔 Channel", url='https://t.me/your_channel'),
            InlineKeyboardButton("💬 Support", url='https://t.me/your_support')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def chk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /chk command for card checking."""
    user = update.effective_user
    
    # Check if user is banned
    user_data = await db.get_user(user.id)
    if user_data and user_data['is_banned']:
        await update.message.reply_text("❌ You are banned from using this bot.")
        return
    
    # Check if user has credits
    if not user_data or user_data['credits'] <= 0:
        await update.message.reply_text(
            "❌ You don't have enough credits!\n\n"
            "💎 Use /plans to get more credits or contact an admin."
        )
        return
    
    # Check if card info provided
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /chk or .chk <card_info>\n\n"
            "**Format:** card_number|month|year|cvv\n"
            "**Example:** /chk 4111111111111111|12|2025|123\n\n"
            "You can also use: card|mm|yyyy|cvv",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Parse card information
    card_input = ' '.join(context.args)
    card_info = CardChecker.parse_card(card_input)
    
    if not card_info:
        await update.message.reply_text(
            "❌ Invalid card format!\n\n"
            "**Please use:** card_number|month|year|cvv",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send checking message
    checking_msg = await update.message.reply_text(
        "🔄 **Checking card...**\n\n"
        f"💳 {card_info['card_number'][:4]}••••••••{card_info['card_number'][-4:]}\n"
        "⏳ Please wait...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Perform card check
    check_result = await CardChecker.check_card(card_info)
    
    # Use one credit
    await db.use_credit(user.id)
    
    # Log the check
    await db.log_card_check(user.id, card_info['card_number'], check_result['status'])
    
    # Format and send result
    result_text = CardChecker.format_check_result(card_info, check_result)
    result_text += f"\n\n👤 **Checked by:** @{user.username or user.first_name}"
    result_text += f"\n💰 **Credits Left:** {user_data['credits'] - 1}"
    
    await checking_msg.edit_text(
        result_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile."""
    user = update.effective_user
    user_data = await db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("❌ User not found. Use /start first.")
        return
    
    stats = await db.get_user_stats(user.id)
    
    profile_text = f"""
👤 **USER PROFILE**

**ID:** {user.id}
**Username:** @{user.username or 'N/A'}
**Name:** {user.first_name} {user.last_name or ''}
**Status:** {'👑 Premium' if user_data['is_premium'] else '🆓 Free'}
**Credits:** 💰 {user_data['credits']}

📊 **STATISTICS**
**Total Checks:** {stats['total_checks']}
**Approved:** ✅ {stats['approved_checks']}
**Declined:** ❌ {stats['total_checks'] - stats['approved_checks']}

**Joined:** {user_data['joined_date'][:10]}
**Last Seen:** {user_data['last_seen'][:10]}
"""
    
    await update.message.reply_text(profile_text, parse_mode=ParseMode.MARKDOWN)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics."""
    user = update.effective_user
    stats = await db.get_user_stats(user.id)
    
    stats_text = f"""
📊 **YOUR STATISTICS**

**Total Checks:** {stats['total_checks']}
**Approved Cards:** ✅ {stats['approved_checks']}
**Declined Cards:** ❌ {stats['total_checks'] - stats['approved_checks']}
**Success Rate:** {(stats['approved_checks'] / stats['total_checks'] * 100) if stats['total_checks'] > 0 else 0:.1f}%
"""
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message."""
    help_text = """
📚 **HELP & COMMANDS GUIDE**

━━━━━━━━━━━━━━━━━━━━
💳 **CARD CHECKING**
━━━━━━━━━━━━━━━━━━━━

**/chk** or **.chk** card|mm|yyyy|cvv
Check a single credit card

**/mass** or **.mass** [cards]
Check multiple cards at once

**/bin** or **.bin** [bin_number]
Get BIN information

━━━━━━━━━━━━━━━━━━━━
👤 **USER COMMANDS**
━━━━━━━━━━━━━━━━━━━━

**/profile** or **.profile**
View your profile and stats

**/stats** or **.stats**
View your checking statistics

**/credits** or **.credits**
Check your credit balance

━━━━━━━━━━━━━━━━━━━━
💎 **PREMIUM & PLANS**
━━━━━━━━━━━━━━━━━━━━

**/plans** or **.plans**
View premium plans

**/status** or **.status**
Check bot status

━━━━━━━━━━━━━━━━━━━━
💡 **TIPS**
━━━━━━━━━━━━━━━━━━━━

✓ Use / or . prefix for all commands
✓ Cards format: card|mm|yy|cvv
✓ Get free credits by inviting friends
✓ Premium users get unlimited checks

Need help? Contact: @your_support
"""
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def plans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show premium plans."""
    plans_text = """
💎 **PREMIUM PLANS**

━━━━━━━━━━━━━━━━━━━━
🥉 **BASIC PLAN**
━━━━━━━━━━━━━━━━━━━━
💰 100 Credits
⏱ Valid for 7 days
💵 $5 USD

━━━━━━━━━━━━━━━━━━━━
🥈 **STANDARD PLAN**
━━━━━━━━━━━━━━━━━━━━
💰 500 Credits
⏱ Valid for 30 days
💵 $20 USD
🎁 +50 Bonus Credits

━━━━━━━━━━━━━━━━━━━━
🥇 **PREMIUM PLAN**
━━━━━━━━━━━━━━━━━━━━
💰 Unlimited Credits
⏱ Valid for 30 days
💵 $50 USD
✨ Priority Support
🚀 Faster Checks
👑 Premium Badge

━━━━━━━━━━━━━━━━━━━━
**To purchase, contact:** @your_admin
**Payment methods:** PayPal, Crypto, Bank Transfer
"""
    
    keyboard = [
        [InlineKeyboardButton("💬 Contact Admin", url='https://t.me/your_admin')],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='cmd_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        plans_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot status."""
    stats = await db.get_stats()
    
    status_text = f"""
🤖 **BOT STATUS**

**Status:** 🟢 Online
**Uptime:** Active
**Version:** 2.0.0

📊 **STATISTICS**
**Total Users:** {stats['total_users']}
**Total Checks:** {stats['total_checks']}
**Banned Users:** {stats['banned_users']}

**Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)


async def bin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bin command for BIN information."""
    user = update.effective_user
    
    # Update last seen
    await db.update_last_seen(user.id)
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /bin or .bin <bin_number>\n\n"
            "**Example:** /bin 411111\n\n"
            "Provide the first 6 digits of a card number.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    bin_number = context.args[0]
    
    # Validate BIN
    if not bin_number.isdigit() or len(bin_number) < 4:
        await update.message.reply_text(
            "❌ Invalid BIN number!\n\n"
            "Please provide at least 4 digits.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get BIN information
    bin_info = BINChecker.get_bin_info(bin_number)
    result_text = BINChecker.format_bin_info(bin_number, bin_info)
    
    await update.message.reply_text(result_text, parse_mode=ParseMode.MARKDOWN)


async def mass_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mass command for mass card checking."""
    user = update.effective_user
    
    # Check if user is banned
    user_data = await db.get_user(user.id)
    if user_data and user_data['is_banned']:
        await update.message.reply_text("❌ You are banned from using this bot.")
        return
    
    # Check if user has credits
    if not user_data or user_data['credits'] < 5:
        await update.message.reply_text(
            "❌ You need at least 5 credits for mass checking!\n\n"
            "💎 Use /plans to get more credits or contact an admin."
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /mass or .mass <cards>\n\n"
            "**Format:** Provide multiple cards separated by new lines or commas\n"
            "**Example:**\n"
            "/mass 4111111111111111|12|2025|123\n"
            "5500000000000004|01|2026|456\n\n"
            "Or reply to this message with the cards to check (one per line).",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Parse multiple cards
    cards_input = ' '.join(context.args).replace(',', '\n')
    card_lines = [line.strip() for line in cards_input.split('\n') if line.strip()]
    
    if len(card_lines) > 10:
        await update.message.reply_text(
            "❌ Maximum 10 cards per mass check!\n\n"
            "Please reduce the number of cards."
        )
        return
    
    # Check if user has enough credits
    if user_data['credits'] < len(card_lines):
        await update.message.reply_text(
            f"❌ You need {len(card_lines)} credits but only have {user_data['credits']}!\n\n"
            "💎 Use /plans to get more credits."
        )
        return
    
    # Send checking message
    checking_msg = await update.message.reply_text(
        f"🔄 **Mass Checking {len(card_lines)} cards...**\n\n"
        "⏳ Please wait...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Check all cards
    results = []
    credits_used = 0
    
    for card_line in card_lines:
        card_info = CardChecker.parse_card(card_line)
        if card_info:
            check_result = await CardChecker.check_card(card_info)
            await db.log_card_check(user.id, card_info['card_number'], check_result['status'])
            await db.use_credit(user.id)
            credits_used += 1
            
            # Format result
            status_emoji = '✅' if check_result['status'] == 'APPROVED' else '❌'
            masked_card = f"{card_info['card_number'][:4]}••••{card_info['card_number'][-4:]}"
            results.append(
                f"{status_emoji} {masked_card} | {check_result['status']} | {check_result['reason']}"
            )
    
    # Format and send results
    result_text = f"""
📊 **MASS CHECK RESULTS**

**Total Cards:** {len(card_lines)}
**Checked:** {credits_used}
**Approved:** {sum(1 for r in results if '✅' in r)}
**Declined:** {sum(1 for r in results if '❌' in r)}

━━━━━━━━━━━━━━━━━━━━
**RESULTS:**

{chr(10).join(results)}

━━━━━━━━━━━━━━━━━━━━
👤 **Checked by:** @{user.username or user.first_name}
💰 **Credits Left:** {user_data['credits'] - credits_used}
"""
    
    await checking_msg.edit_text(result_text, parse_mode=ParseMode.MARKDOWN)


async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user credits."""
    user = update.effective_user
    user_data = await db.get_user(user.id)
    
    if not user_data:
        await update.message.reply_text("❌ User not found. Use /start first.")
        return
    
    credits_text = f"""
💰 **YOUR CREDITS**

**Current Balance:** {user_data['credits']} credits
**Status:** {'👑 Premium (Unlimited)' if user_data['is_premium'] else '🆓 Free User'}

━━━━━━━━━━━━━━━━━━━━
💡 **Need more credits?**

Use /plans to view premium plans and get more credits!
"""
    
    await update.message.reply_text(credits_text, parse_mode=ParseMode.MARKDOWN)


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot information."""
    info_text = """
ℹ️ **BOT INFORMATION**

**Name:** Supreme Card Checker Bot
**Version:** 2.0.0
**Developer:** @ElBrido

━━━━━━━━━━━━━━━━━━━━
**FEATURES**
━━━━━━━━━━━━━━━━━━━━

✅ Single & Mass Card Checking
✅ BIN Information Lookup
✅ User Credit System
✅ Premium Plans
✅ Admin Management Tools
✅ Detailed Statistics
✅ Dual Command Prefix (/ and .)
✅ Group Management
✅ User Banning System
✅ Broadcast Messages

━━━━━━━━━━━━━━━━━━━━
**SUPPORT**
━━━━━━━━━━━━━━━━━━━━

📢 Channel: @your_channel
💬 Support: @your_support
👨‍💻 Developer: @ElBrido

━━━━━━━━━━━━━━━━━━━━
🌟 **Thank you for using our bot!**
"""
    
    await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)


# GROUP COMMANDS

async def welcome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set welcome message for group."""
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if in group
    if chat.type == 'private':
        await update.message.reply_text(
            "❌ This command can only be used in groups!"
        )
        return
    
    # Check if user is admin
    if not await GroupManager.is_group_admin(update, context, user.id):
        await update.message.reply_text(
            "❌ This command is only for group administrators!"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /welcome <message>\n\n"
            "**Example:** /welcome Welcome to our group! Please read the rules.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    welcome_msg = ' '.join(context.args)
    GroupManager.set_welcome_message(chat.id, welcome_msg)
    
    await update.message.reply_text(
        f"✅ Welcome message updated!\n\n**Preview:**\n{welcome_msg}",
        parse_mode=ParseMode.MARKDOWN
    )


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show or set group rules."""
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if in group
    if chat.type == 'private':
        await update.message.reply_text(
            "❌ This command can only be used in groups!"
        )
        return
    
    # If no args, show rules
    if not context.args:
        rules = GroupManager.get_rules(chat.id)
        if rules:
            await update.message.reply_text(
                f"📜 **GROUP RULES**\n\n{rules}",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "📜 No rules set for this group.\n\n"
                "Admins can set rules with: /rules <rules_text>"
            )
        return
    
    # Check if user is admin to set rules
    if not await GroupManager.is_group_admin(update, context, user.id):
        await update.message.reply_text(
            "❌ Only administrators can set rules!"
        )
        return
    
    rules_text = ' '.join(context.args)
    GroupManager.set_rules(chat.id, rules_text)
    
    await update.message.reply_text(
        f"✅ Group rules updated!\n\n**Preview:**\n{rules_text}",
        parse_mode=ParseMode.MARKDOWN
    )


async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get group invite link."""
    chat = update.effective_chat
    user = update.effective_user
    
    # Check if in group
    if chat.type == 'private':
        await update.message.reply_text(
            "❌ This command can only be used in groups!"
        )
        return
    
    # Check if user is admin
    if not await GroupManager.is_group_admin(update, context, user.id):
        await update.message.reply_text(
            "❌ This command is only for group administrators!"
        )
        return
    
    try:
        invite_link = await context.bot.export_chat_invite_link(chat.id)
        await update.message.reply_text(
            f"🔗 **Group Invite Link:**\n\n{invite_link}",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(
            "❌ Failed to get invite link. Make sure the bot has admin rights."
        )


# ADMIN COMMANDS

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /broadcast <message>\n\n"
            "This will send the message to all users.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    message = ' '.join(context.args)
    
    # This is a simplified version. In production, you'd iterate through all users
    await update.message.reply_text(
        f"✅ Broadcast initiated!\n\n**Message:**\n{message}",
        parse_mode=ParseMode.MARKDOWN
    )


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /ban <user_id>\n\n"
            "Example: /ban 123456789",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        await db.ban_user(target_user_id, user.id)
        await update.message.reply_text(
            f"✅ User {target_user_id} has been banned.",
            parse_mode=ParseMode.MARKDOWN
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "❌ **Usage:** /unban <user_id>",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        await db.unban_user(target_user_id, user.id)
        await update.message.reply_text(
            f"✅ User {target_user_id} has been unbanned.",
            parse_mode=ParseMode.MARKDOWN
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")


async def addcredits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add credits to a user (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ **Usage:** /addcredits <user_id> <amount>\n\n"
            "Example: /addcredits 123456789 100",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        credits = int(context.args[1])
        await db.add_credits(target_user_id, credits, user.id)
        await update.message.reply_text(
            f"✅ Added {credits} credits to user {target_user_id}.",
            parse_mode=ParseMode.MARKDOWN
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID or credit amount.")


async def stats_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show global statistics (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    stats = await db.get_stats()
    
    stats_text = f"""
📊 **GLOBAL STATISTICS (ADMIN)**

**Total Users:** {stats['total_users']}
**Total Card Checks:** {stats['total_checks']}
**Banned Users:** {stats['banned_users']}
**Active Users:** {stats['total_users'] - stats['banned_users']}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)


async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all users (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    count = await db.get_all_users_count()
    
    users_text = f"""
👥 **USER LIST (ADMIN)**

**Total Users:** {count}

Use /ban <user_id> to ban a user
Use /unban <user_id> to unban a user
Use /addcredits <user_id> <amount> to add credits

**Note:** For detailed user list, use database query tools.
"""
    
    await update.message.reply_text(users_text, parse_mode=ParseMode.MARKDOWN)


async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View admin logs (admin only)."""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ This command is for admins only.")
        return
    
    logs_text = """
📋 **ADMIN LOGS**

Recent admin actions will be displayed here.

**Available Actions:**
• BAN - User banned
• UNBAN - User unbanned
• ADD_CREDITS - Credits added to user
• BROADCAST - Message broadcasted

Use database to view full logs history.
"""
    
    await update.message.reply_text(logs_text, parse_mode=ParseMode.MARKDOWN)


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'cmd_chk':
        await query.message.reply_text(
            "💳 **To check a card, use:**\n\n"
            "/chk card|mm|yyyy|cvv\n\n"
            "**Example:**\n"
            "/chk 4111111111111111|12|2025|123",
            parse_mode=ParseMode.MARKDOWN
        )
    elif data == 'cmd_stats':
        user = query.from_user
        stats = await db.get_user_stats(user.id)
        
        stats_text = f"""
📊 **YOUR STATISTICS**

**Total Checks:** {stats['total_checks']}
**Approved:** ✅ {stats['approved_checks']}
**Declined:** ❌ {stats['total_checks'] - stats['approved_checks']}
"""
        await query.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
    elif data == 'cmd_help':
        await help_command(update, context)
    elif data == 'cmd_plans':
        await plans_command(update, context)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages with dot prefix."""
    text = update.message.text
    
    if text.startswith('.'):
        # Convert dot command to slash command
        command = text[1:].split()[0]
        args = text.split()[1:] if len(text.split()) > 1 else []
        context.args = args
        
        # Route to appropriate command
        command_map = {
            'start': start_command,
            'chk': chk_command,
            'profile': profile_command,
            'stats': stats_command,
            'help': help_command,
            'plans': plans_command,
            'status': status_command,
            'bin': bin_command,
            'mass': mass_command,
            'credits': credits_command,
            'info': info_command,
            'welcome': welcome_command,
            'rules': rules_command,
            'link': link_command,
            'broadcast': broadcast_command,
            'ban': ban_command,
            'unban': unban_command,
            'addcredits': addcredits_command,
            'stats_admin': stats_admin_command,
            'users': users_command,
            'logs': logs_command,
        }
        
        if command in command_map:
            await command_map[command](update, context)


async def post_init(application: Application):
    """Initialize database after bot starts."""
    await db.init_db()
    logger.info("Database initialized")


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Register command handlers (slash commands)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("chk", chk_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("plans", plans_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("bin", bin_command))
    application.add_handler(CommandHandler("mass", mass_command))
    application.add_handler(CommandHandler("credits", credits_command))
    application.add_handler(CommandHandler("info", info_command))
    
    # Group commands
    application.add_handler(CommandHandler("welcome", welcome_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("link", link_command))
    
    # Admin commands
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("addcredits", addcredits_command))
    application.add_handler(CommandHandler("stats_admin", stats_admin_command))
    application.add_handler(CommandHandler("users", users_command))
    application.add_handler(CommandHandler("logs", logs_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    
    # Message handler for dot commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
