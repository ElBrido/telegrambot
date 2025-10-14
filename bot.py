#!/usr/bin/env python3
"""
Professional Telegram Credit Card Verification Bot
Features: CCN Checker, BIN Lookup, VBV Checker, Mass Card Generation, Admin Management
"""

import json
import logging
import random
import re
from datetime import datetime
from typing import List, Dict, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import requests

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load configuration
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {
        "bot_token": "",
        "welcome_gif_url": "",
        "owners": [],
        "admins": []
    }
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)

BOT_TOKEN = config.get('bot_token', '')
WELCOME_GIF = config.get('welcome_gif_url', '')
OWNERS = set(config.get('owners', []))
ADMINS = set(config.get('admins', []))


# Helper functions
def save_config():
    """Save configuration to file"""
    config_data = {
        "bot_token": BOT_TOKEN,
        "welcome_gif_url": WELCOME_GIF,
        "owners": list(OWNERS),
        "admins": list(ADMINS)
    }
    with open('config.json', 'w') as f:
        json.dump(config_data, f, indent=2)


def is_owner(user_id: int) -> bool:
    """Check if user is owner"""
    return user_id in OWNERS


def is_admin(user_id: int) -> bool:
    """Check if user is admin or owner"""
    return user_id in ADMINS or user_id in OWNERS


def validate_card_number(card_number: str) -> bool:
    """Validate card number using Luhn algorithm"""
    card_number = re.sub(r'\D', '', card_number)
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    return luhn_checksum(card_number) == 0


def get_card_brand(card_number: str) -> str:
    """Identify card brand from card number"""
    card_number = re.sub(r'\D', '', card_number)
    
    if len(card_number) < 3:
        return 'UNKNOWN'
    
    if card_number.startswith('4'):
        return 'VISA'
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        return 'MASTERCARD'
    elif len(card_number) >= 4 and (2221 <= int(card_number[:4]) <= 2720):
        return 'MASTERCARD'
    elif card_number.startswith(('34', '37')):
        return 'AMEX'
    elif card_number.startswith(('6011', '65')):
        return 'DISCOVER'
    elif len(card_number) >= 3 and (644 <= int(card_number[:3]) <= 649):
        return 'DISCOVER'
    elif len(card_number) >= 4 and card_number.startswith(('3528', '3589')):
        return 'JCB'
    elif len(card_number) >= 4 and (3528 <= int(card_number[:4]) <= 3589):
        return 'JCB'
    else:
        return 'UNKNOWN'


def generate_card(bin_number: str, quantity: int = 1) -> List[str]:
    """Generate valid card numbers from BIN"""
    cards = []
    bin_clean = re.sub(r'\D', '', bin_number)
    
    if len(bin_clean) < 6:
        return []
    
    for _ in range(quantity):
        # Generate random digits to complete the card number (excluding last digit for checksum)
        card_base = bin_clean + ''.join([str(random.randint(0, 9)) for _ in range(15 - len(bin_clean))])
        
        # Calculate Luhn check digit
        def calculate_luhn_digit(card_num):
            """Calculate the Luhn check digit for a card number"""
            digits = [int(d) for d in card_num]
            # Double every second digit from right to left (starting from the second-to-last position)
            # Since we're adding a check digit at the end, we double positions 0, 2, 4, etc. from the right
            for i in range(len(digits) - 1, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
            
            # Calculate check digit to make total divisible by 10
            total = sum(digits)
            check_digit = (10 - (total % 10)) % 10
            return str(check_digit)
        
        check_digit = calculate_luhn_digit(card_base)
        full_card = card_base + check_digit
        
        # Generate expiry date and CVV
        month = random.randint(1, 12)
        year = random.randint(25, 30)
        cvv = random.randint(100, 999)
        
        cards.append(f"{full_card}|{month:02d}|{year}|{cvv}")
    
    return cards


# Bot command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    welcome_text = f"""
🔐 *PROFESSIONAL CC VERIFICATION BOT* 🔐

Welcome {user.first_name}! 👋

This bot provides professional credit card verification services.

*Available Features:*
✅ CCN Checker - Verify card numbers
✅ CCN Charge - Test card charging
✅ BIN Lookup - Get BIN information
✅ VBV Checker - Verify by Visa check
✅ Card Status - Active/Inactive verification
✅ Mass Generator - Generate multiple cards

*Quick Commands:*
/help - View all available commands
/cmds - List all functionalities
/status - Check your access level

*Credits:* @YourChannel
"""
    
    keyboard = [
        [InlineKeyboardButton("📋 Commands", callback_data='show_commands')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='show_help')],
        [InlineKeyboardButton("👤 My Status", callback_data='show_status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send GIF if configured
    if WELCOME_GIF:
        try:
            await context.bot.send_animation(
                chat_id=update.effective_chat.id,
                animation=WELCOME_GIF,
                caption=welcome_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Error sending GIF: {e}")
            await update.message.reply_text(
                welcome_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    else:
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📚 *HELP - COMMAND GUIDE* 📚

*Card Verification Commands:*
`.chk <card>` - Check if card is valid (CCN Checker)
`.ch <card>` - Charge verification (CCN CH)
`.bin <bin>` - BIN lookup information
`.vbv <card>` - Verify by Visa checker
`.status <card>` - Check if card is active/inactive

*Card Generation Commands:*
`.gen <bin> <quantity>` - Generate cards from BIN
`.mass <bin>` - Generate 10 cards from BIN

*Admin Commands:*
`/addadmin <user_id>` - Add admin (Owner only)
`/removeadmin <user_id>` - Remove admin (Owner only)
`/addowner <user_id>` - Add owner (Owner only)
`/listadmins` - List all admins

*Info Commands:*
`/start` - Show main menu
`/help` or `/cmds` - Show this help
`/status` - Check your access level

*Card Format:*
`1234567890123456|MM|YY|CVV`
or
`1234567890123456|MM|YYYY|CVV`

*Note:* All verification commands require admin access.
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def cmds_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cmds command - alias for help"""
    await help_command(update, context)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = update.effective_user.id
    
    if is_owner(user_id):
        role = "👑 Owner"
    elif is_admin(user_id):
        role = "⚡ Admin"
    else:
        role = "👤 User"
    
    status_text = f"""
📊 *YOUR STATUS* 📊

User ID: `{user_id}`
Role: {role}
Name: {update.effective_user.first_name}

*Permissions:*
"""
    
    if is_owner(user_id):
        status_text += "✅ All Commands\n✅ Admin Management\n✅ Card Verification\n✅ Card Generation"
    elif is_admin(user_id):
        status_text += "✅ Card Verification\n✅ Card Generation\n❌ Admin Management"
    else:
        status_text += "❌ Limited Access\n\nContact an admin for access."
    
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def addadmin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add admin (owner only)"""
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owners can add admins.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /addadmin <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        ADMINS.add(user_id)
        save_config()
        await update.message.reply_text(f"✅ User {user_id} added as admin.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")


async def removeadmin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove admin (owner only)"""
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owners can remove admins.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /removeadmin <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        if user_id in ADMINS:
            ADMINS.remove(user_id)
            save_config()
            await update.message.reply_text(f"✅ User {user_id} removed from admins.")
        else:
            await update.message.reply_text("❌ User is not an admin.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")


async def addowner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add owner (owner only)"""
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Only owners can add other owners.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /addowner <user_id>")
        return
    
    try:
        user_id = int(context.args[0])
        OWNERS.add(user_id)
        save_config()
        await update.message.reply_text(f"✅ User {user_id} added as owner.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID.")


async def listadmins_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all admins"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You don't have permission to view admins.")
        return
    
    admin_list = "👑 *OWNERS:*\n"
    if OWNERS:
        for owner_id in OWNERS:
            admin_list += f"• `{owner_id}`\n"
    else:
        admin_list += "None\n"
    
    admin_list += "\n⚡ *ADMINS:*\n"
    if ADMINS:
        for admin_id in ADMINS:
            admin_list += f"• `{admin_id}`\n"
    else:
        admin_list += "None\n"
    
    await update.message.reply_text(admin_list, parse_mode='Markdown')


async def handle_dot_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle commands starting with dot (.)"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You need admin access to use verification commands.")
        return
    
    message_text = update.message.text.strip()
    
    # Parse command
    parts = message_text.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    # Card check command
    if command == '.chk':
        await check_card(update, args)
    
    # Charge command
    elif command == '.ch':
        await charge_card(update, args)
    
    # BIN lookup command
    elif command == '.bin':
        await bin_lookup(update, args)
    
    # VBV checker command
    elif command == '.vbv':
        await vbv_check(update, args)
    
    # Status check command
    elif command == '.status':
        await status_check(update, args)
    
    # Generate cards command
    elif command == '.gen':
        await generate_cards(update, args)
    
    # Mass generate command
    elif command == '.mass':
        await mass_generate(update, args)


async def check_card(update: Update, card_info: str):
    """Check card validity (CCN Checker)"""
    if not card_info:
        await update.message.reply_text("Usage: .chk <card>|<mm>|<yy>|<cvv>")
        return
    
    processing_msg = await update.message.reply_text("🔄 Checking card...")
    
    try:
        parts = card_info.split('|')
        if len(parts) < 4:
            await processing_msg.edit_text("❌ Invalid format. Use: card|mm|yy|cvv")
            return
        
        card_number = re.sub(r'\D', '', parts[0])
        month = parts[1]
        year = parts[2]
        cvv = parts[3]
        
        # Validate card number
        is_valid = validate_card_number(card_number)
        brand = get_card_brand(card_number)
        
        result = f"""
🔍 *CCN CHECKER RESULT*

Card: `{card_number[:4]}****{card_number[-4:]}`
Brand: {brand}
Expiry: {month}/{year}
CVV: {cvv}

Validation: {'✅ VALID' if is_valid else '❌ INVALID'}
Luhn Check: {'✅ Passed' if is_valid else '❌ Failed'}

Status: {'🟢 LIVE' if is_valid else '🔴 DEAD'}

*Note:* This is a simulated check. Real card verification requires payment gateway integration.
"""
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def charge_card(update: Update, card_info: str):
    """Charge verification (CCN CH)"""
    if not card_info:
        await update.message.reply_text("Usage: .ch <card>|<mm>|<yy>|<cvv>")
        return
    
    processing_msg = await update.message.reply_text("🔄 Testing charge...")
    
    try:
        parts = card_info.split('|')
        if len(parts) < 4:
            await processing_msg.edit_text("❌ Invalid format. Use: card|mm|yy|cvv")
            return
        
        card_number = re.sub(r'\D', '', parts[0])
        month = parts[1]
        year = parts[2]
        cvv = parts[3]
        
        is_valid = validate_card_number(card_number)
        brand = get_card_brand(card_number)
        
        # Simulate charge test
        charge_status = "APPROVED" if is_valid and random.random() > 0.3 else "DECLINED"
        
        result = f"""
💳 *CHARGE TEST RESULT*

Card: `{card_number[:4]}****{card_number[-4:]}`
Brand: {brand}
Expiry: {month}/{year}

Test Amount: $1.00
Result: {'✅ ' + charge_status if charge_status == 'APPROVED' else '❌ ' + charge_status}
Response: {'Approved - CVV Match' if charge_status == 'APPROVED' else 'Insufficient Funds'}

*Note:* This is a simulated test. Real charging requires payment gateway integration.
"""
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def bin_lookup(update: Update, bin_number: str):
    """BIN lookup information"""
    if not bin_number:
        await update.message.reply_text("Usage: .bin <bin_number>")
        return
    
    processing_msg = await update.message.reply_text("🔄 Looking up BIN...")
    
    try:
        bin_clean = re.sub(r'\D', '', bin_number)[:6]
        
        if len(bin_clean) < 6:
            await processing_msg.edit_text("❌ BIN must be at least 6 digits.")
            return
        
        # Try to get BIN info from API
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_clean}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                result = f"""
🔎 *BIN LOOKUP RESULT*

BIN: `{bin_clean}`
Brand: {data.get('scheme', 'Unknown').upper()}
Type: {data.get('type', 'Unknown').upper()}
Category: {data.get('category', 'Unknown').upper()}

Bank: {data.get('bank', {}).get('name', 'Unknown')}
Country: {data.get('country', {}).get('name', 'Unknown')} {data.get('country', {}).get('emoji', '')}

"""
                await processing_msg.edit_text(result, parse_mode='Markdown')
                return
        except Exception as e:
            logger.error(f"BIN API error: {e}")
        
        # Fallback to basic info
        brand = get_card_brand(bin_clean + "0" * 10)
        
        result = f"""
🔎 *BIN LOOKUP RESULT*

BIN: `{bin_clean}`
Brand: {brand}
Type: DEBIT/CREDIT
Category: UNKNOWN

*Note:* Limited info available. API integration required for full details.
"""
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def vbv_check(update: Update, card_info: str):
    """VBV (Verified by Visa) checker"""
    if not card_info:
        await update.message.reply_text("Usage: .vbv <card>|<mm>|<yy>|<cvv>")
        return
    
    processing_msg = await update.message.reply_text("🔄 Checking VBV status...")
    
    try:
        parts = card_info.split('|')
        if len(parts) < 4:
            await processing_msg.edit_text("❌ Invalid format. Use: card|mm|yy|cvv")
            return
        
        card_number = re.sub(r'\D', '', parts[0])
        brand = get_card_brand(card_number)
        is_valid = validate_card_number(card_number)
        
        # Simulate VBV check
        vbv_enabled = random.choice([True, False]) if is_valid else False
        
        result = f"""
🔐 *VBV CHECKER RESULT*

Card: `{card_number[:4]}****{card_number[-4:]}`
Brand: {brand}

VBV Status: {'✅ ENABLED' if vbv_enabled else '❌ DISABLED'}
3D Secure: {'✅ Active' if vbv_enabled else '❌ Inactive'}

Security Level: {'🔒 High' if vbv_enabled else '🔓 Low'}

*Note:* This is a simulated check. Real VBV verification requires 3D Secure integration.
"""
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def status_check(update: Update, card_info: str):
    """Check if card is active or inactive"""
    if not card_info:
        await update.message.reply_text("Usage: .status <card>|<mm>|<yy>|<cvv>")
        return
    
    processing_msg = await update.message.reply_text("🔄 Checking card status...")
    
    try:
        parts = card_info.split('|')
        if len(parts) < 4:
            await processing_msg.edit_text("❌ Invalid format. Use: card|mm|yy|cvv")
            return
        
        card_number = re.sub(r'\D', '', parts[0])
        month = parts[1]
        year = parts[2]
        
        is_valid = validate_card_number(card_number)
        brand = get_card_brand(card_number)
        
        # Simulate status check
        is_active = random.choice([True, False]) if is_valid else False
        
        result = f"""
📊 *CARD STATUS CHECK*

Card: `{card_number[:4]}****{card_number[-4:]}`
Brand: {brand}
Expiry: {month}/{year}

Validation: {'✅ Valid Format' if is_valid else '❌ Invalid Format'}
Status: {'🟢 ACTIVE' if is_active else '🔴 INACTIVE'}
Balance: {'Available' if is_active else 'Unavailable'}

*Note:* This is a simulated check. Real status requires issuer API integration.
"""
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def generate_cards(update: Update, args: str):
    """Generate cards from BIN"""
    if not args:
        await update.message.reply_text("Usage: .gen <bin> <quantity>")
        return
    
    parts = args.split()
    if len(parts) < 1:
        await update.message.reply_text("Usage: .gen <bin> <quantity>")
        return
    
    bin_number = parts[0]
    quantity = int(parts[1]) if len(parts) > 1 else 10
    
    if quantity > 50:
        await update.message.reply_text("❌ Maximum 50 cards per generation.")
        return
    
    processing_msg = await update.message.reply_text(f"🔄 Generating {quantity} cards...")
    
    try:
        cards = generate_card(bin_number, quantity)
        
        if not cards:
            await processing_msg.edit_text("❌ Invalid BIN number.")
            return
        
        result = f"💳 *CARD GENERATOR*\n\nBIN: `{bin_number}`\nQuantity: {len(cards)}\n\n*Generated Cards:*\n\n"
        
        for i, card in enumerate(cards, 1):
            result += f"`{card}`\n"
        
        result += f"\n✅ Generation completed!"
        
        await processing_msg.edit_text(result, parse_mode='Markdown')
    
    except Exception as e:
        await processing_msg.edit_text(f"❌ Error: {str(e)}")


async def mass_generate(update: Update, bin_number: str):
    """Mass generate 10 cards from BIN"""
    if not bin_number:
        await update.message.reply_text("Usage: .mass <bin>")
        return
    
    await generate_cards(update, f"{bin_number} 10")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'show_commands':
        await query.message.reply_text("""
📋 *AVAILABLE COMMANDS*

*Verification:*
.chk - Card checker
.ch - Charge test
.bin - BIN lookup
.vbv - VBV checker
.status - Card status

*Generation:*
.gen - Generate cards
.mass - Mass generate

*Admin:*
/addadmin - Add admin
/removeadmin - Remove admin
/listadmins - List admins
""", parse_mode='Markdown')
    
    elif query.data == 'show_help':
        await help_command(query, context)
    
    elif query.data == 'show_status':
        user_id = query.from_user.id
        if is_owner(user_id):
            role = "👑 Owner"
        elif is_admin(user_id):
            role = "⚡ Admin"
        else:
            role = "👤 User"
        
        await query.message.reply_text(f"*Your Role:* {role}\n*User ID:* `{user_id}`", parse_mode='Markdown')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not set in config.json")
        print("Please add your bot token to config.json")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cmds", cmds_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("addadmin", addadmin_command))
    application.add_handler(CommandHandler("removeadmin", removeadmin_command))
    application.add_handler(CommandHandler("addowner", addowner_command))
    application.add_handler(CommandHandler("listadmins", listadmins_command))
    
    # Dot command handler
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r'^\.'), 
        handle_dot_commands
    ))
    
    # Button callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    print("Bot started successfully!")
    print("Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
