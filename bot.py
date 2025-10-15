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
        
        # Payment gateway configuration
        self.gateway_type = self.config.get('PAYMENT_GATEWAY', 'GATEWAY_TYPE', fallback='')
        self.gateway_api_key = self.config.get('PAYMENT_GATEWAY', 'API_KEY', fallback='')
        self.gateway_api_secret = self.config.get('PAYMENT_GATEWAY', 'API_SECRET', fallback='')
        self.gateway_test_mode = self.config.getboolean('PAYMENT_GATEWAY', 'TEST_MODE', fallback=True)
        
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

    async def process_payment_gateway_charge(self, card_info: dict) -> dict:
        """Process charge through configured payment gateway
        Returns dict with status, message, and details"""
        
        if not self.gateway_type or not self.gateway_api_key:
            # No gateway configured - use simulation
            import random
            is_approved = card_info.get('is_valid', False) and random.random() > 0.3
            return {
                'status': 'APPROVED' if is_approved else 'DECLINED',
                'message': 'Aprobado - CVV Match' if is_approved else 'Fondos Insuficientes',
                'simulation': True,
                'gateway': 'simulation'
            }
        
        # Real payment gateway processing
        gateway_result = {
            'status': 'ERROR',
            'message': 'Gateway configuration error',
            'simulation': False,
            'gateway': self.gateway_type
        }
        
        try:
            if self.gateway_type.lower() == 'stripe':
                # Stripe integration
                try:
                    import stripe
                    stripe.api_key = self.gateway_api_key
                    
                    # Create a payment method with the card
                    payment_method = stripe.PaymentMethod.create(
                        type="card",
                        card={
                            "number": card_info['card'],
                            "exp_month": card_info.get('month', 12),
                            "exp_year": card_info.get('year', 25),
                            "cvc": card_info.get('cvv', '123'),
                        },
                    )
                    
                    # Create payment intent
                    intent = stripe.PaymentIntent.create(
                        amount=100,  # $1.00 in cents
                        currency='usd',
                        payment_method=payment_method.id,
                        confirm=True,
                        return_url='https://example.com/return'
                    )
                    
                    gateway_result['status'] = 'APPROVED' if intent.status == 'succeeded' else 'DECLINED'
                    gateway_result['message'] = f"Stripe: {intent.status}"
                    gateway_result['transaction_id'] = intent.id
                    
                except ImportError:
                    gateway_result['message'] = '❌ Stripe library not installed. Run: pip install stripe'
                except Exception as e:
                    gateway_result['message'] = f'Stripe error: {str(e)}'
                    
            elif self.gateway_type.lower() == 'paypal':
                # PayPal integration placeholder
                gateway_result['message'] = '⚠️ PayPal integration requires PayPal SDK. Contact admin for setup.'
                
            elif self.gateway_type.lower() == 'mercadopago':
                # MercadoPago integration placeholder
                gateway_result['message'] = '⚠️ MercadoPago integration requires SDK. Contact admin for setup.'
                
            else:
                gateway_result['message'] = f'⚠️ Gateway type "{self.gateway_type}" not supported yet'
                
        except Exception as e:
            gateway_result['message'] = f'Gateway error: {str(e)}'
            logger.error(f"Payment gateway error: {e}")
        
        return gateway_result


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        # Register user
        self.db.add_user(user.id, user.username, user.first_name, user.last_name)
        
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
                "Formatos aceptados:\n"
                "• /ccn 4532015112830366\n"
                "• /ccn 4532015112830366|12|28|123"
            )
            return
        
        input_str = ''.join(context.args)
        user_id = update.effective_user.id
        
        # Parse input to extract card and optional details
        parsed = self.card_utils.parse_card_input(input_str)
        card_number = parsed['card']
        
        if not card_number:
            await update.message.reply_text("❌ Número de tarjeta inválido")
            return
        
        # Check card
        result = self.card_utils.check_card_status(card_number)
        
        # Log to database
        self.db.add_card_check(user_id, card_number, result['status'])
        
        # Build response with extra details if provided
        extra_info = ""
        if parsed['month'] or parsed['year']:
            expiry = self.card_utils.format_expiry(parsed['month'], parsed['year'])
            if expiry:
                extra_info += f"📅 Exp: {expiry}\n"
        if parsed['cvv']:
            extra_info += f"🔐 CVV: {parsed['cvv']}\n"
        
        response = f"""
🔍 **Verificación de Tarjeta**

💳 Tarjeta: `{result['card']}`
{extra_info}{result['message']}

Estado: {result['status']}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def charge_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ch or ..ch command - Charge test verification"""
        user_id = update.effective_user.id
        
        if not (self.db.is_admin(user_id) or self.db.has_premium(user_id)):
            await update.message.reply_text("❌ Este comando requiere Premium o Admin")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /ch <tarjeta>|<mm>|<aa>|<cvv>\n"
                "Ejemplo: /ch 4532015112830366|12|25|123"
            )
            return
        
        input_str = ''.join(context.args)
        processing_msg = await update.message.reply_text("🔄 Probando cargo...")
        
        try:
            parsed = self.card_utils.parse_card_input(input_str)
            card_number = parsed['card']
            
            if not card_number:
                await processing_msg.edit_text("❌ Número de tarjeta inválido")
                return
            
            result = self.card_utils.check_card_status(card_number)
            
            # Prepare card info for gateway
            card_info = {
                'card': result['card'],
                'month': parsed.get('month'),
                'year': parsed.get('year'),
                'cvv': parsed.get('cvv'),
                'is_valid': result['is_valid']
            }
            
            # Process through payment gateway
            gateway_result = await self.process_payment_gateway_charge(card_info)
            
            expiry = self.card_utils.format_expiry(parsed['month'], parsed['year']) if parsed['month'] else "N/A"
            
            # Build response
            gateway_indicator = ""
            if gateway_result.get('simulation'):
                gateway_indicator = "\n⚠️ **Modo Simulación** - Configure PAYMENT_GATEWAY en config.ini para cargos reales"
            else:
                gateway_indicator = f"\n✅ **Gateway Real:** {gateway_result['gateway']}"
                if self.gateway_test_mode:
                    gateway_indicator += " (Modo Test)"
            
            response = f"""
💳 **PRUEBA DE CARGO**

💳 Tarjeta: `{result['card']}`
🏦 Tipo: {result.get('type', 'N/A')}
📅 Exp: {expiry}
🔐 CVV: {parsed['cvv'] or 'N/A'}

💰 Monto: $1.00 USD
Estado: {'✅ ' + gateway_result['status'] if gateway_result['status'] == 'APPROVED' else '❌ ' + gateway_result['status']}
Respuesta: {gateway_result['message']}{gateway_indicator}
            """
            
            if gateway_result.get('transaction_id'):
                response += f"\n🔖 ID Transacción: `{gateway_result['transaction_id']}`"
            
            await processing_msg.edit_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ Error: {str(e)}")

    async def vbv_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vbv or ..vbv command - VBV/3D Secure verification"""
        user_id = update.effective_user.id
        
        if not (self.db.is_admin(user_id) or self.db.has_premium(user_id)):
            await update.message.reply_text("❌ Este comando requiere Premium o Admin")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /vbv <tarjeta>|<mm>|<aa>|<cvv>\n"
                "Ejemplo: /vbv 4532015112830366|12|25|123"
            )
            return
        
        input_str = ''.join(context.args)
        processing_msg = await update.message.reply_text("🔄 Verificando VBV...")
        
        try:
            parsed = self.card_utils.parse_card_input(input_str)
            card_number = parsed['card']
            
            if not card_number:
                await processing_msg.edit_text("❌ Número de tarjeta inválido")
                return
            
            result = self.card_utils.check_card_status(card_number)
            
            # Simulate VBV check
            import random
            vbv_enabled = random.choice([True, False]) if result['is_valid'] else False
            
            response = f"""
🔐 **VERIFICADOR VBV**

💳 Tarjeta: `{result['card']}`
🏦 Tipo: {result.get('type', 'N/A')}

Estado VBV: {'✅ HABILITADO' if vbv_enabled else '❌ DESHABILITADO'}
3D Secure: {'✅ Activo' if vbv_enabled else '❌ Inactivo'}

Nivel de Seguridad: {'🔒 Alto' if vbv_enabled else '🔓 Bajo'}

⚠️ **Nota:** Esta es una verificación simulada. La verificación VBV real requiere integración con 3D Secure.
            """
            
            await processing_msg.edit_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ Error: {str(e)}")

    async def card_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cardstatus or ..cardstatus command - Check if card is active"""
        user_id = update.effective_user.id
        
        if not (self.db.is_admin(user_id) or self.db.has_premium(user_id)):
            await update.message.reply_text("❌ Este comando requiere Premium o Admin")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /cardstatus <tarjeta>|<mm>|<aa>|<cvv>\n"
                "Ejemplo: /cardstatus 4532015112830366|12|25|123"
            )
            return
        
        input_str = ''.join(context.args)
        processing_msg = await update.message.reply_text("🔄 Verificando estado...")
        
        try:
            parsed = self.card_utils.parse_card_input(input_str)
            card_number = parsed['card']
            
            if not card_number:
                await processing_msg.edit_text("❌ Número de tarjeta inválido")
                return
            
            result = self.card_utils.check_card_status(card_number)
            expiry = self.card_utils.format_expiry(parsed['month'], parsed['year']) if parsed['month'] else "N/A"
            
            # Simulate active/inactive status
            import random
            is_active = random.choice([True, False]) if result['is_valid'] else False
            
            response = f"""
📊 **ESTADO DE TARJETA**

💳 Tarjeta: `{result['card']}`
🏦 Tipo: {result.get('type', 'N/A')}
📅 Exp: {expiry}

Validación: {'✅ Formato Válido' if result['is_valid'] else '❌ Formato Inválido'}
Estado: {'🟢 ACTIVA' if is_active else '🔴 INACTIVA'}
Saldo: {'Disponible' if is_active else 'No Disponible'}

⚠️ **Nota:** Esta es una verificación simulada. El estado real requiere integración con API del emisor.
            """
            
            await processing_msg.edit_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ Error: {str(e)}")

    async def bin_lookup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bin or ..bin command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /bin <bin_número>\n"
                "Formatos aceptados:\n"
                "• /bin 453201\n"
                "• /bin 453201|12|28"
            )
            return
        
        input_str = ''.join(context.args)
        
        # Parse input to extract BIN and optional expiry
        parsed = self.card_utils.parse_card_input(input_str)
        bin_number = parsed['card']
        
        if not bin_number:
            await update.message.reply_text("❌ BIN inválido")
            return
        
        bin_info = self.card_utils.get_bin_info(bin_number)
        
        if "error" in bin_info:
            await update.message.reply_text(f"❌ {bin_info['error']}")
            return
        
        # Add expiry info if provided
        extra_info = ""
        if parsed['month'] or parsed['year']:
            expiry = self.card_utils.format_expiry(parsed['month'], parsed['year'])
            if expiry:
                extra_info = f"📅 Exp sugerida: {expiry}\n"
        
        response = f"""
🔍 **Información BIN**

📊 BIN: `{bin_info['bin']}`
🏦 Tipo: {bin_info['type']}
🌐 Red: {bin_info['network']}
🏢 Emisor: {bin_info.get('issuer', 'N/A')}
🌍 País: {bin_info.get('country', 'N/A')}
{extra_info}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def generate_cards_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gen or ..gen command"""
        user_id = update.effective_user.id
        
        # Check if user has permission
        if not (self.db.has_premium(user_id) or self.db.is_admin(user_id)):
            await update.message.reply_text(
                "❌ Esta función requiere **Premium**\n"
                "Usa /redeem <clave> para activar premium",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) < 1:
            await update.message.reply_text(
                "❌ Uso: /gen <bin> [cantidad]\n"
                "Formatos aceptados:\n"
                "• /gen 453201 10\n"
                "• /gen 453201|12|28 10"
            )
            return
        
        # Parse first argument to extract BIN and optional expiry
        parsed = self.card_utils.parse_card_input(context.args[0])
        bin_prefix = parsed['card']
        custom_expiry = self.card_utils.format_expiry(parsed['month'], parsed['year'])
        
        if not bin_prefix:
            await update.message.reply_text("❌ BIN inválido")
            return
        
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
            # Use custom expiry if provided, otherwise generate random
            expiry = custom_expiry if custom_expiry else self.card_utils.generate_random_expiry()
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
        """Handle /redeem or ..redeem command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /redeem <clave_premium>\n"
                "Ejemplo: /redeem ABC123XYZ"
            )
            return
        
        key_code = context.args[0]
        user_id = update.effective_user.id
        
        success, message = self.db.activate_premium_key(user_id, key_code)
        
        await update.message.reply_text(message)

    async def genkey_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /genkey command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        # Parse arguments: count and duration
        count = 1
        duration_hours = 720  # Default 30 days
        
        if context.args:
            try:
                count = int(context.args[0])
                count = min(count, 20)  # Limit to 20 keys
                
                # Check if duration is specified
                if len(context.args) > 1:
                    duration_str = context.args[1]
                    # Parse duration with unit (e.g., "5h", "30m", "3600s", "1d")
                    if duration_str.endswith('s'):
                        duration_hours = float(duration_str[:-1]) / 3600.0
                    elif duration_str.endswith('m'):
                        duration_hours = float(duration_str[:-1]) / 60.0
                    elif duration_str.endswith('h'):
                        duration_hours = float(duration_str[:-1])
                    elif duration_str.endswith('d'):
                        duration_hours = float(duration_str[:-1]) * 24.0
                    else:
                        # Default to hours if no unit specified
                        duration_hours = float(duration_str)
            except (ValueError, IndexError):
                await update.message.reply_text(
                    "❌ Uso: /genkey [cantidad] [duración]\n"
                    "Ejemplos:\n"
                    "• /genkey 5 24h - 5 claves de 24 horas\n"
                    "• /genkey 3 30m - 3 claves de 30 minutos\n"
                    "• /genkey 10 3600s - 10 claves de 3600 segundos\n"
                    "• /genkey 2 7d - 2 claves de 7 días"
                )
                return
        
        keys = []
        for _ in range(count):
            key_code = secrets.token_urlsafe(32)  # Increased from 12 to 32 for better security
            if self.db.create_premium_key(key_code, int(duration_hours)):
                keys.append(f"`{key_code}`")
        
        # Format duration for display
        if duration_hours >= 24:
            duration_display = f"{duration_hours/24:.1f} días"
        elif duration_hours >= 1:
            duration_display = f"{duration_hours:.1f} horas"
        else:
            duration_display = f"{duration_hours*60:.0f} minutos"
        
        response = f"""
🔑 **Claves Premium Generadas**

Cantidad: {len(keys)}

{chr(10).join(keys)}

Duración: {duration_display}
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
        user_id = update.effective_user.id
        is_admin = self.db.is_admin(user_id)
        
        help_text = """
🦇 **BatmanWL - Ayuda** 🦇

**Comandos disponibles:**

**Comandos básicos:**
• `/start` - Iniciar bot y ver menú
• `/menu` o `.menu` - Mostrar menú principal
• `/help` o `.help` - Mostrar esta ayuda

**Verificación de Tarjetas:**
• `/ccn <tarjeta>` o `.chk <tarjeta>` - Verificar tarjeta
  Ejemplos:
  `/ccn 4532015112830366`
  `/ccn 4532015112830366|12|28|123`
  `.chk 4532015112830366|12|25|123`

• `/ch <tarjeta>` o `.ch <tarjeta>` - Prueba de cargo (Premium/Admin)
  Ejemplo: `/ch 4532015112830366|12|25|123`

• `/vbv <tarjeta>` o `.vbv <tarjeta>` - Verificar VBV/3D Secure (Premium/Admin)
  Ejemplo: `/vbv 4532015112830366|12|25|123`

• `/cardstatus <tarjeta>` o `.cardstatus <tarjeta>` - Estado activo/inactivo (Premium/Admin)
  Ejemplo: `/cardstatus 4532015112830366|12|25|123`
  
• `/bin <bin>` o `.bin <bin>` - Buscar información BIN
  Ejemplos:
  `/bin 453201`
  `.bin 453201|12|28`

**Premium:**
• `/gen <bin> [cant]` o `.gen <bin> [cant]` - Generar tarjetas (Premium)
  Ejemplos:
  `/gen 453201 10`
  `.gen 453201|12|28 10`
  `.mass 453201` - Genera 10 tarjetas
  
• `/redeem <clave>` - Activar clave premium
• `/stats` - Ver tus estadísticas
"""

        if is_admin:
            help_text += """
**Comandos de Administración:**
• `/genkey [cantidad] [duración]` - Generar claves premium
  Ejemplos: /genkey 5 24h, /genkey 3 30m, /genkey 2 7d
• `/ban <user_id>` - Banear usuario
• `/unban <user_id>` - Desbanear usuario
• `/addcredits <user_id> <cantidad>` - Agregar créditos
• `/broadcast <mensaje>` - Enviar mensaje a todos
• `/statsadmin` - Ver estadísticas globales
"""

        help_text += """
💡 **Formato profesional:**
Usa el formato `tarjeta|mes|año|cvv` para inputs completos
Ejemplo: `4532015112830366|04|31|123`

💡 **Tip:** Puedes usar `/` o `.` o `..` antes de cualquier comando
Ejemplos: `/ccn`, `.chk`, `..ccn` funcionan igual
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
                "Ejemplos:\n"
                "• /ccn 4532015112830366\n"
                "• /ccn 4532015112830366|12|28|123",
                parse_mode='Markdown'
            )
        elif query.data == 'bin_lookup':
            await query.message.reply_text(
                "🔍 **Buscar BIN**\n\n"
                "Usa: /bin <bin_número>\n"
                "Ejemplos:\n"
                "• /bin 453201\n"
                "• /bin 453201|12|28",
                parse_mode='Markdown'
            )
        elif query.data == 'gen_cards':
            if not (self.db.has_premium(user_id) or self.db.is_admin(user_id)):
                await query.message.reply_text(
                    "❌ Esta función requiere **Premium**\n"
                    "Usa /redeem <clave> para activar premium",
                    parse_mode='Markdown'
                )
            else:
                await query.message.reply_text(
                    "💳 **Generar Tarjetas**\n\n"
                    "Usa: /gen <bin> [cantidad]\n"
                    "Ejemplos:\n"
                    "• /gen 453201 10\n"
                    "• /gen 453201|12|28 10",
                    parse_mode='Markdown'
                )
        elif query.data == 'activate_key':
            await query.message.reply_text(
                "🔑 **Activar Clave Premium**\n\n"
                "Usa: /redeem <clave_premium>\n"
                "Ejemplo: /redeem ABC123XYZ",
                parse_mode='Markdown'
            )
        elif query.data == 'stats':
            user = self.db.get_user(user_id)
            stats = self.db.get_user_stats(user_id)
            has_premium = self.db.has_premium(user_id)
            premium_info = self.db.get_premium_info(user_id)
            
            response = f"""
📊 **Tus Estadísticas**

👤 Usuario: @{query.from_user.username or query.from_user.first_name}
🆔 ID: {user_id}
🎭 Rol: {user['role']}
⭐ Premium: {'✅ Activo' if has_premium else '❌ Inactivo'}
"""
            
            if premium_info:
                from datetime import datetime
                expires_at = datetime.fromisoformat(premium_info['expires_at'])
                response += f"📅 Expira: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            response += f"\n📈 Verificaciones: {stats['total_checks']}\n"
            
            await query.message.reply_text(response, parse_mode='Markdown')
        elif query.data == 'admin_panel':
            if not self.db.is_admin(user_id):
                await query.message.reply_text("❌ No tienes permiso")
            else:
                await query.message.reply_text(
                    "⚙️ **Panel de Administración Completo**\n\n"
                    "**Gestión de Claves:**\n"
                    "• /genkey [cantidad] [duración] - Generar claves premium\n"
                    "  Ejemplos: /genkey 5 24h, /genkey 3 30m, /genkey 2 7d\n\n"
                    "**Gestión de Usuarios:**\n"
                    "• /ban <user_id> - Banear usuario\n"
                    "• /unban <user_id> - Desbanear usuario\n"
                    "• /addcredits <user_id> <cantidad> - Agregar créditos\n\n"
                    "**Comunicación:**\n"
                    "• /broadcast <mensaje> - Mensaje a todos los usuarios\n\n"
                    "**Estadísticas:**\n"
                    "• /statsadmin - Ver estadísticas globales\n",
                    parse_mode='Markdown'
                )
        elif query.data == 'help':
            is_admin = self.db.is_admin(user_id)
            
            help_text = """
🦇 **BatmanWL - Ayuda** 🦇

**Comandos disponibles:**

**Comandos básicos:**
• `/start` - Iniciar bot y ver menú
• `/menu` o `.menu` - Mostrar menú principal
• `/help` o `.help` - Mostrar esta ayuda

**Verificación de Tarjetas:**
• `/ccn <tarjeta>` o `.chk <tarjeta>` - Verificar tarjeta
  Ejemplos:
  `/ccn 4532015112830366`
  `/ccn 4532015112830366|12|28|123`
  `.chk 4532015112830366|12|25|123`

• `/ch <tarjeta>` o `.ch <tarjeta>` - Prueba de cargo (Premium/Admin)
  Ejemplo: `/ch 4532015112830366|12|25|123`

• `/vbv <tarjeta>` o `.vbv <tarjeta>` - Verificar VBV/3D Secure (Premium/Admin)
  Ejemplo: `/vbv 4532015112830366|12|25|123`

• `/cardstatus <tarjeta>` o `.cardstatus <tarjeta>` - Estado activo/inactivo (Premium/Admin)
  Ejemplo: `/cardstatus 4532015112830366|12|25|123`
  
• `/bin <bin>` o `.bin <bin>` - Buscar información BIN
  Ejemplos:
  `/bin 453201`
  `.bin 453201|12|28`

**Premium:**
• `/gen <bin> [cant]` o `.gen <bin> [cant]` - Generar tarjetas (Premium)
  Ejemplos:
  `/gen 453201 10`
  `.gen 453201|12|28 10`
  `.mass 453201` - Genera 10 tarjetas
  
• `/key <clave>` - Activar clave premium
• `/stats` - Ver tus estadísticas
"""

            if is_admin:
                help_text += """
**Comandos de Administración:**
• `/genkey [cantidad] [duración]` - Generar claves premium
  Ejemplos: /genkey 5 24h, /genkey 3 30m, /genkey 2 7d
• `/ban <user_id>` - Banear usuario
• `/unban <user_id>` - Desbanear usuario
• `/addcredits <user_id> <cantidad>` - Agregar créditos
• `/broadcast <mensaje>` - Enviar mensaje a todos
• `/statsadmin` - Ver estadísticas globales
"""

            help_text += """
💡 **Formato profesional:**
Usa el formato `tarjeta|mes|año|cvv` para inputs completos
Ejemplo: `4532015112830366|04|31|123`

💡 **Tip:** Puedes usar `/` o `.` o `..` antes de cualquier comando
Ejemplos: `/ccn`, `.chk`, `..ccn` funcionan igual
            """
            
            await query.message.reply_text(help_text, parse_mode='Markdown')

    # Admin panel commands
    async def ban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ban command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /ban <user_id>\n"
                "Ejemplo: /ban 123456789"
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            self.db.ban_user(target_user_id, user_id)
            await update.message.reply_text(f"✅ Usuario {target_user_id} baneado correctamente")
        except ValueError:
            await update.message.reply_text("❌ ID de usuario inválido")
    
    async def unban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /unban command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /unban <user_id>\n"
                "Ejemplo: /unban 123456789"
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            self.db.unban_user(target_user_id, user_id)
            await update.message.reply_text(f"✅ Usuario {target_user_id} desbaneado correctamente")
        except ValueError:
            await update.message.reply_text("❌ ID de usuario inválido")
    
    async def addcredits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /addcredits command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ Uso: /addcredits <user_id> <cantidad>\n"
                "Ejemplo: /addcredits 123456789 100"
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            credits = int(context.args[1])
            self.db.add_credits(target_user_id, credits, user_id)
            await update.message.reply_text(
                f"✅ Se agregaron {credits} créditos al usuario {target_user_id}"
            )
        except ValueError:
            await update.message.reply_text("❌ Valores inválidos")
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /broadcast <mensaje>\n"
                "Ejemplo: /broadcast Hola a todos!"
            )
            return
        
        message = ' '.join(context.args)
        await update.message.reply_text(
            f"📢 **Mensaje de Broadcast**\n\n{message}\n\n"
            "✅ Mensaje enviado a todos los usuarios (simulado)",
            parse_mode='Markdown'
        )
    
    async def stats_admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /statsadmin command (admin only)"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permiso para usar este comando")
            return
        
        stats = self.db.get_stats()
        
        response = f"""
📊 **Estadísticas Globales (Admin)**

👥 Total Usuarios: {stats['total_users']}
📈 Total Verificaciones: {stats['total_checks']}
🚫 Usuarios Baneados: {stats['banned_users']}
✅ Usuarios Activos: {stats['total_users'] - stats['banned_users']}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')

    async def handle_dot_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle commands starting with '..' or '.'"""
        text = update.message.text
        
        # Handle both .. and . prefixes
        if text.startswith('..'):
            command = text[2:].split()[0]
            args = text.split()[1:]
        elif text.startswith('.'):
            command = text[1:].split()[0]
            args = text.split()[1:]
        else:
            return
        
        # Simulate command
        if command == 'menu':
            await self.menu(update, context)
        elif command == 'ccn' or command == 'chk':
            context.args = args
            await self.ccn_check_command(update, context)
        elif command == 'ch':
            context.args = args
            await self.charge_command(update, context)
        elif command == 'vbv':
            context.args = args
            await self.vbv_command(update, context)
        elif command == 'cardstatus':
            context.args = args
            await self.card_status_command(update, context)
        elif command == 'bin':
            context.args = args
            await self.bin_lookup_command(update, context)
        elif command == 'gen' or command == 'mass':
            context.args = args
            await self.generate_cards_command(update, context)
        elif command == 'key' or command == 'redeem':
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
        
        # Add basic command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("menu", self.menu))
        application.add_handler(CommandHandler("ccn", self.ccn_check_command))
        application.add_handler(CommandHandler("chk", self.ccn_check_command))  # Alias
        application.add_handler(CommandHandler("ch", self.charge_command))  # Charge test
        application.add_handler(CommandHandler("vbv", self.vbv_command))  # VBV checker
        application.add_handler(CommandHandler("cardstatus", self.card_status_command))  # Card status
        application.add_handler(CommandHandler("bin", self.bin_lookup_command))
        application.add_handler(CommandHandler("gen", self.generate_cards_command))
        application.add_handler(CommandHandler("key", self.activate_key_command))  # Legacy support
        application.add_handler(CommandHandler("redeem", self.activate_key_command))  # New command
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Admin command handlers
        application.add_handler(CommandHandler("genkey", self.genkey_command))
        application.add_handler(CommandHandler("ban", self.ban_command))
        application.add_handler(CommandHandler("unban", self.unban_command))
        application.add_handler(CommandHandler("addcredits", self.addcredits_command))
        application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        application.add_handler(CommandHandler("statsadmin", self.stats_admin_command))
        
        # Button handler
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Handle '.' and '..' commands
        application.add_handler(MessageHandler(
            filters.TEXT & filters.Regex(r'^\.'),
            self.handle_dot_commands
        ))
        
        # Schedule periodic cleanup of expired keys (every hour)
        job_queue = application.job_queue
        job_queue.run_repeating(self.cleanup_expired_keys_job, interval=3600, first=10)
        
        logger.info("🦇 BatmanWL Bot iniciado!")
        logger.info(f"💳 Payment Gateway: {self.gateway_type if self.gateway_type else 'Simulation Mode'}")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def cleanup_expired_keys_job(self, context: ContextTypes.DEFAULT_TYPE):
        """Job to clean up expired premium keys periodically"""
        count = self.db.cleanup_expired_keys()
        if count > 0:
            logger.info(f"🧹 Cleaned up {count} expired premium keys")


def main():
    """Main entry point"""
    bot = BatmanWLBot('config.ini')
    bot.run()


if __name__ == '__main__':
    main()
