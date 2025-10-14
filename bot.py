"""BatmanWL Telegram Bot - Main bot file."""
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
import config
import database
from features import (
    generate_image, convert_file, advanced_search,
    get_weather, translate_text, calculate_expression
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def require_premium(func):
    """Decorator to require premium access for a command."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user = database.get_or_create_user(
            user_id,
            update.effective_user.username,
            update.effective_user.first_name
        )
        
        # Admins and owners bypass premium requirement
        if user.is_admin() or user.is_owner():
            return await func(update, context, user)
        
        # Check if user has active premium
        if not user.is_premium_active():
            await update.message.reply_text(
                "⚠️ This feature is premium only!\n\n"
                "Use /redeem <key> to activate premium access.\n"
                "Contact an admin to get a premium key."
            )
            return
        
        return await func(update, context, user)
    return wrapper


def require_admin(func):
    """Decorator to require admin access for a command."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user = database.get_or_create_user(
            user_id,
            update.effective_user.username,
            update.effective_user.first_name
        )
        
        if not (user.is_admin() or user.is_owner()):
            await update.message.reply_text("⚠️ This command is for admins only!")
            return
        
        return await func(update, context, user)
    return wrapper


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler."""
    user = database.get_or_create_user(
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name
    )
    
    welcome_text = f"""
🦇 Welcome to {config.BOT_NAME}! 🦇

I'm your advanced Telegram bot with premium features.

📋 *Free Commands:*
/start - Start the bot
/help - Show this help message
/status - Check your premium status
/weather <city> - Get weather information
/calc <expression> - Calculate math expressions

⭐ *Premium Commands:*
/genimage <prompt> - Generate AI images
/convert <format> - Convert files to different formats
/search <query> - Advanced web search
/translate <lang> <text> - Translate text

🔑 *Key Management:*
/redeem <key> - Redeem a premium key

👑 *Admin Commands:*
/genkey <hours> <uses> - Generate premium keys
/listkeys - List all premium keys
/deactivate <key> - Deactivate a key
/stats - View bot statistics

Use /help for more information!
"""
    
    keyboard = [
        [InlineKeyboardButton("📊 My Status", callback_data="status")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler."""
    await start(update, context)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status command handler."""
    user = database.get_or_create_user(
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name
    )
    
    status_text = f"""
👤 *User Status*

Name: {user.first_name or 'Unknown'}
Username: @{user.username or 'None'}
User ID: `{user.user_id}`

"""
    
    if user.is_owner():
        status_text += "👑 *Role:* Owner\n"
        status_text += "✅ *Access:* All Features (Unlimited)\n"
    elif user.is_admin():
        status_text += "⚡ *Role:* Administrator\n"
        status_text += "✅ *Access:* All Features (Unlimited)\n"
    elif user.is_premium_active():
        time_left = user.premium_until - datetime.utcnow()
        hours = int(time_left.total_seconds() / 3600)
        minutes = int((time_left.total_seconds() % 3600) / 60)
        status_text += "⭐ *Role:* Premium User\n"
        status_text += f"✅ *Premium Active Until:* {user.premium_until.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        status_text += f"⏱ *Time Remaining:* {hours}h {minutes}m\n"
    else:
        status_text += "🆓 *Role:* Free User\n"
        status_text += "❌ *Premium:* Not Active\n"
        status_text += "\nUse /redeem <key> to activate premium!\n"
    
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Redeem command handler."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /redeem <key>\n\n"
            "Example: /redeem ABC123XYZ"
        )
        return
    
    key_str = context.args[0]
    user_id = update.effective_user.id
    
    user, message = database.redeem_key(user_id, key_str)
    
    if user:
        time_until = user.premium_until.strftime('%Y-%m-%d %H:%M:%S')
        await update.message.reply_text(
            f"✅ {message}\n\n"
            f"🎉 Premium activated!\n"
            f"⏱ Valid until: {time_until} UTC\n\n"
            f"Enjoy your premium features! 🦇"
        )
    else:
        await update.message.reply_text(f"❌ {message}")


@require_admin
async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Generate key command handler (admin only)."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /genkey <hours> <max_uses>\n\n"
            "Examples:\n"
            "/genkey 24 1 - 24 hours, single use\n"
            "/genkey 168 10 - 1 week, 10 uses\n"
            "/genkey 720 -1 - 30 days, unlimited uses"
        )
        return
    
    try:
        hours = int(context.args[0])
        max_uses = int(context.args[1])
        
        if hours <= 0:
            await update.message.reply_text("❌ Hours must be positive!")
            return
        
        if max_uses == 0 or max_uses < -1:
            await update.message.reply_text("❌ Max uses must be -1 (unlimited) or positive!")
            return
        
        key = database.generate_key(hours, max_uses, user.user_id)
        
        uses_text = "unlimited" if max_uses == -1 else str(max_uses)
        await update.message.reply_text(
            f"✅ Key generated successfully!\n\n"
            f"🔑 Key: `{key.key}`\n"
            f"⏱ Duration: {hours} hours ({hours//24} days)\n"
            f"👥 Max uses: {uses_text}\n\n"
            f"Share this key with users to grant them premium access!"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid numbers provided!")


@require_admin
async def listkeys(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """List keys command handler (admin only)."""
    keys = database.get_all_keys()
    
    if not keys:
        await update.message.reply_text("No keys have been generated yet.")
        return
    
    text = "🔑 *Premium Keys*\n\n"
    
    for key in keys[:20]:  # Show first 20 keys
        status = "✅ Active" if key.is_active and key.can_redeem() else "❌ Inactive"
        uses = f"{key.current_uses}/{key.max_uses}" if key.max_uses > 0 else f"{key.current_uses}/∞"
        text += f"`{key.key}`\n"
        text += f"Status: {status} | Uses: {uses} | Duration: {key.duration_hours}h\n\n"
    
    if len(keys) > 20:
        text += f"\n_... and {len(keys) - 20} more keys_"
    
    await update.message.reply_text(text, parse_mode='Markdown')


@require_admin
async def deactivate(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Deactivate key command handler (admin only)."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /deactivate <key>\n\n"
            "Example: /deactivate ABC123XYZ"
        )
        return
    
    key_str = context.args[0]
    
    if database.deactivate_key(key_str):
        await update.message.reply_text(f"✅ Key `{key_str}` has been deactivated!")
    else:
        await update.message.reply_text(f"❌ Key not found!")


@require_admin
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Stats command handler (admin only)."""
    session = database.Session()
    try:
        total_users = session.query(database.User).count()
        premium_users = session.query(database.User).filter(
            database.User.is_premium == True
        ).count()
        total_keys = session.query(database.PremiumKey).count()
        active_keys = session.query(database.PremiumKey).filter(
            database.PremiumKey.is_active == True
        ).count()
        
        text = f"""
📊 *Bot Statistics*

👥 Total Users: {total_users}
⭐ Premium Users: {premium_users}
🔑 Total Keys: {total_keys}
✅ Active Keys: {active_keys}
"""
        
        await update.message.reply_text(text, parse_mode='Markdown')
    finally:
        database.Session.remove()


# Premium feature handlers
@require_premium
async def genimage_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Generate image command handler (premium only)."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /genimage <prompt>\n\n"
            "Example: /genimage a futuristic city at sunset"
        )
        return
    
    prompt = ' '.join(context.args)
    await update.message.reply_text(f"🎨 Generating image for: {prompt}...")
    
    result = generate_image(prompt)
    await update.message.reply_text(result)


@require_premium
async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Convert file command handler (premium only)."""
    await update.message.reply_text(
        "📄 File Conversion Feature\n\n"
        "This feature allows you to convert files between different formats.\n"
        "Send me a file and specify the target format!"
    )


@require_premium
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Search command handler (premium only)."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /search <query>\n\n"
            "Example: /search best programming languages 2024"
        )
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(f"🔍 Searching for: {query}...")
    
    result = advanced_search(query)
    await update.message.reply_text(result)


# Free feature handlers
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Weather command handler (free)."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /weather <city>\n\n"
            "Example: /weather London"
        )
        return
    
    city = ' '.join(context.args)
    result = get_weather(city)
    await update.message.reply_text(result)


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculator command handler (free)."""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /calc <expression>\n\n"
            "Example: /calc 2 + 2 * 3"
        )
        return
    
    expression = ' '.join(context.args)
    result = calculate_expression(expression)
    await update.message.reply_text(result)


@require_premium
async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
    """Translate command handler (premium only)."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /translate <language> <text>\n\n"
            "Example: /translate es Hello, how are you?"
        )
        return
    
    target_lang = context.args[0]
    text = ' '.join(context.args[1:])
    result = translate_text(text, target_lang)
    await update.message.reply_text(result)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "status":
        user = database.get_or_create_user(
            query.from_user.id,
            query.from_user.username,
            query.from_user.first_name
        )
        
        status_text = f"👤 *Your Status*\n\n"
        
        if user.is_owner():
            status_text += "👑 Owner - Full Access"
        elif user.is_admin():
            status_text += "⚡ Admin - Full Access"
        elif user.is_premium_active():
            time_left = user.premium_until - datetime.utcnow()
            hours = int(time_left.total_seconds() / 3600)
            status_text += f"⭐ Premium - {hours}h remaining"
        else:
            status_text += "🆓 Free User"
        
        await query.edit_message_text(status_text, parse_mode='Markdown')
    
    elif query.data == "help":
        await query.edit_message_text("Use /help to see all commands!")


def main():
    """Start the bot."""
    # Initialize database
    database.init_db()
    logger.info("Database initialized")
    
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("redeem", redeem))
    
    # Admin commands
    application.add_handler(CommandHandler("genkey", genkey))
    application.add_handler(CommandHandler("listkeys", listkeys))
    application.add_handler(CommandHandler("deactivate", deactivate))
    application.add_handler(CommandHandler("stats", stats))
    
    # Premium commands
    application.add_handler(CommandHandler("genimage", genimage_command))
    application.add_handler(CommandHandler("convert", convert_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("translate", translate_command))
    
    # Free commands
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("calc", calc_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    logger.info(f"Starting {config.BOT_NAME}...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
