"""
BatmanWL Telegram Bot
Professional bot for credit card verification
"""

import logging
import configparser
import secrets
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from database import Database
from card_utils import CardUtils

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BatmanWLBot:
    def __init__(self, config_file='config.ini'):
        """Initialize the bot"""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        self.token = self.config.get('BOT', 'TOKEN')
        self.admin_ids = [int(x.strip()) for x in self.config.get('BOT', 'ADMIN_IDS').split(',')]
        self.owner_id = int(self.config.get('BOT', 'OWNER_ID'))
        self.gif_url = self.config.get('WELCOME', 'GIF_URL')
        self.welcome_msg = self.config.get('WELCOME', 'MESSAGE')
        self.key_duration = int(self.config.get('PREMIUM', 'KEY_DURATION_DAYS'))
        
        self.db = Database(self.config.get('DATABASE', 'DB_NAME'))
        self.card_utils = CardUtils()
        
        # Register owner in database
        self.db.add_user(self.owner_id, role='owner')
        for admin_id in self.admin_ids:
            if admin_id != self.owner_id:
                self.db.add_user(admin_id, role='admin')

    def build_main_menu(self, user_id: int) -> InlineKeyboardMarkup:
        """Build main menu keyboard"""
        is_premium = self.db.has_premium(user_id)
        is_admin = self.db.is_admin(user_id)
        
        keyboard = [
            [InlineKeyboardButton("✅ Verificar Tarjeta (CCN)", callback_data='ccn_check')],
            [InlineKeyboardButton("🔍 Buscar BIN", callback_data='bin_lookup')],
        ]
        
        if is_premium or is_admin:
            keyboard.append([InlineKeyboardButton("💳 Generar Tarjetas", callback_data='gen_cards')])
        
        keyboard.extend([
            [InlineKeyboardButton("🔑 Activar Clave Premium", callback_data='activate_key')],
            [InlineKeyboardButton("📊 Mis Estadísticas", callback_data='stats')],
        ])
        
        if is_admin:
            keyboard.append([InlineKeyboardButton("⚙️ Panel Admin", callback_data='admin_panel')])
        
        keyboard.append([InlineKeyboardButton("ℹ️ Ayuda", callback_data='help')])
        
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Register user
        self.db.add_user(user.id, user.username)
        
        welcome_text = f"""
{self.welcome_msg}

👤 Usuario: @{user.username or user.first_name}
🆔 ID: {user.id}

🦇 **BatmanWL** es tu bot profesional para:
• Verificación de tarjetas (CCN Check)
• Búsqueda de información BIN
• Generación masiva de tarjetas
• Sistema de roles y premium

Usa los botones del menú o comandos con / o ..
        """
        
        # Send GIF
        try:
            await context.bot.send_animation(
                chat_id=update.effective_chat.id,
                animation=self.gif_url,
                caption=welcome_text,
                parse_mode='Markdown',
                reply_markup=self.build_main_menu(user.id)
            )
        except Exception as e:
            logger.error(f"Error sending GIF: {e}")
            await update.message.reply_text(
                welcome_text,
                parse_mode='Markdown',
                reply_markup=self.build_main_menu(user.id)
            )

    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu or ..menu command"""
        user = update.effective_user
        
        menu_text = "🦇 **Menú Principal - BatmanWL** 🦇\n\nSelecciona una opción:"
        
        await update.message.reply_text(
            menu_text,
            parse_mode='Markdown',
            reply_markup=self.build_main_menu(user.id)
        )

    async def ccn_check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ccn or ..ccn command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /ccn <número_de_tarjeta>\n"
                "Ejemplo: /ccn 4532015112830366"
            )
            return
        
        card_number = ''.join(context.args)
        user_id = update.effective_user.id
        
        # Check card
        result = self.card_utils.check_card_status(card_number)
        
        # Log to database
        self.db.add_card_check(user_id, card_number, result['status'])
        
        response = f"""
🔍 **Verificación de Tarjeta**

💳 Tarjeta: `{result['card']}`
{result['message']}

Estado: {result['status']}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def bin_lookup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bin or ..bin command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /bin <bin_número>\n"
                "Ejemplo: /bin 453201"
            )
            return
        
        bin_number = context.args[0]
        bin_info = self.card_utils.get_bin_info(bin_number)
        
        if "error" in bin_info:
            await update.message.reply_text(f"❌ {bin_info['error']}")
            return
        
        response = f"""
🔍 **Información BIN**

📊 BIN: `{bin_info['bin']}`
🏦 Tipo: {bin_info['type']}
🌐 Red: {bin_info['network']}
🏢 Emisor: {bin_info.get('issuer', 'N/A')}
🌍 País: {bin_info.get('country', 'N/A')}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def generate_cards_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gen or ..gen command"""
        user_id = update.effective_user.id
        
        # Check if user has permission
        if not (self.db.has_premium(user_id) or self.db.is_admin(user_id)):
            await update.message.reply_text(
                "❌ Esta función requiere **Premium**\n"
                "Usa /key <clave> para activar premium",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) < 1:
            await update.message.reply_text(
                "❌ Uso: /gen <bin> [cantidad]\n"
                "Ejemplo: /gen 453201 10"
            )
            return
        
        bin_prefix = context.args[0]
        count = int(context.args[1]) if len(context.args) > 1 else 10
        
        # Limit count
        count = min(count, 50)
        
        cards = self.card_utils.generate_multiple_cards(bin_prefix, count)
        
        if not cards:
            await update.message.reply_text("❌ No se pudieron generar tarjetas con ese BIN")
            return
        
        # Format cards with CVV and expiry
        formatted_cards = []
        for card in cards:
            cvv = self.card_utils.generate_random_cvv()
            expiry = self.card_utils.generate_random_expiry()
            formatted_cards.append(f"`{self.card_utils.format_card_number(card)}|{expiry}|{cvv}`")
        
        response = f"""
💳 **Tarjetas Generadas**

🔢 BIN: {bin_prefix}
📊 Cantidad: {len(cards)}

{chr(10).join(formatted_cards)}

✅ Todas las tarjetas pasan validación Luhn
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def activate_key_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /key or ..key command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /key <clave_premium>\n"
                "Ejemplo: /key ABC123XYZ"
            )
            return
        
        key_code = context.args[0]
        user_id = update.effective_user.id
        
        success, message = self.db.activate_premium_key(user_id, key_code, self.key_duration)
        
        await update.message.reply_text(message)

    async def genkey_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /genkey command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        count = int(context.args[0]) if context.args else 1
        count = min(count, 20)  # Limit to 20 keys
        
        keys = []
        for _ in range(count):
            key_code = secrets.token_urlsafe(12)
            if self.db.create_premium_key(key_code):
                keys.append(f"`{key_code}`")
        
        response = f"""
🔑 **Claves Premium Generadas**

Cantidad: {len(keys)}

{chr(10).join(keys)}

Duración: {self.key_duration} días
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats or ..stats command"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        stats = self.db.get_user_stats(user_id)
        has_premium = self.db.has_premium(user_id)
        
        response = f"""
📊 **Tus Estadísticas**

👤 Usuario: @{update.effective_user.username or update.effective_user.first_name}
🆔 ID: {user_id}
🎭 Rol: {user['role']}
⭐ Premium: {'✅ Activo' if has_premium else '❌ Inactivo'}

📈 Verificaciones: {stats['total_checks']}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help or ..help command"""
        help_text = """
🦇 **BatmanWL - Ayuda** 🦇

**Comandos disponibles:**

**Comandos básicos:**
• `/start` - Iniciar bot y ver menú
• `/menu` o `..menu` - Mostrar menú principal
• `/help` o `..help` - Mostrar esta ayuda

**Verificación:**
• `/ccn <tarjeta>` - Verificar tarjeta
• `/bin <bin>` - Buscar información BIN

**Premium:**
• `/gen <bin> [cant]` - Generar tarjetas (Premium)
• `/key <clave>` - Activar clave premium
• `/stats` - Ver tus estadísticas

**Admin:**
• `/genkey [cant]` - Generar claves premium

💡 **Tip:** Puedes usar `/` o `..` antes de cualquier comando
Ejemplo: `/menu` o `..menu`
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == 'ccn_check':
            await query.message.reply_text(
                "💳 **Verificar Tarjeta**\n\n"
                "Usa: /ccn <número_de_tarjeta>\n"
                "Ejemplo: /ccn 4532015112830366",
                parse_mode='Markdown'
            )
        elif query.data == 'bin_lookup':
            await query.message.reply_text(
                "🔍 **Buscar BIN**\n\n"
                "Usa: /bin <bin_número>\n"
                "Ejemplo: /bin 453201",
                parse_mode='Markdown'
            )
        elif query.data == 'gen_cards':
            if not (self.db.has_premium(user_id) or self.db.is_admin(user_id)):
                await query.message.reply_text(
                    "❌ Esta función requiere **Premium**\n"
                    "Usa /key <clave> para activar premium",
                    parse_mode='Markdown'
                )
            else:
                await query.message.reply_text(
                    "💳 **Generar Tarjetas**\n\n"
                    "Usa: /gen <bin> [cantidad]\n"
                    "Ejemplo: /gen 453201 10",
                    parse_mode='Markdown'
                )
        elif query.data == 'activate_key':
            await query.message.reply_text(
                "🔑 **Activar Clave Premium**\n\n"
                "Usa: /key <clave_premium>\n"
                "Ejemplo: /key ABC123XYZ",
                parse_mode='Markdown'
            )
        elif query.data == 'stats':
            await self.stats_command(update, context)
        elif query.data == 'admin_panel':
            if not self.db.is_admin(user_id):
                await query.message.reply_text("❌ No tienes permiso")
            else:
                await query.message.reply_text(
                    "⚙️ **Panel de Administración**\n\n"
                    "**Comandos disponibles:**\n"
                    "• /genkey [cantidad] - Generar claves premium\n",
                    parse_mode='Markdown'
                )
        elif query.data == 'help':
            await self.help_command(update, context)

    async def handle_dot_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle commands starting with '..'"""
        text = update.message.text
        
        if text.startswith('..'):
            # Convert ..command to /command
            command = text[2:].split()[0]
            args = text.split()[1:]
            
            # Simulate command
            if command == 'menu':
                await self.menu(update, context)
            elif command == 'ccn':
                context.args = args
                await self.ccn_check_command(update, context)
            elif command == 'bin':
                context.args = args
                await self.bin_lookup_command(update, context)
            elif command == 'gen':
                context.args = args
                await self.generate_cards_command(update, context)
            elif command == 'key':
                context.args = args
                await self.activate_key_command(update, context)
            elif command == 'stats':
                await self.stats_command(update, context)
            elif command == 'help':
                await self.help_command(update, context)
            else:
                await update.message.reply_text(
                    f"❌ Comando desconocido: {command}\n"
                    "Usa /help para ver comandos disponibles"
                )

    def run(self):
        """Start the bot"""
        application = Application.builder().token(self.token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("menu", self.menu))
        application.add_handler(CommandHandler("ccn", self.ccn_check_command))
        application.add_handler(CommandHandler("bin", self.bin_lookup_command))
        application.add_handler(CommandHandler("gen", self.generate_cards_command))
        application.add_handler(CommandHandler("key", self.activate_key_command))
        application.add_handler(CommandHandler("genkey", self.genkey_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Button handler
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Handle '..' commands
        application.add_handler(MessageHandler(
            filters.TEXT & filters.Regex(r'^\.\.'),
            self.handle_dot_commands
        ))
        
        logger.info("🦇 BatmanWL Bot iniciado!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""
    bot = BatmanWLBot('config.ini')
    bot.run()


if __name__ == '__main__':
    main()
