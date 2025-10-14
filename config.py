"""Configuration module for the bot."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration class."""
    
    # Bot settings
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')
    
    # Credit settings
    DEFAULT_CREDITS = int(os.getenv('DEFAULT_CREDITS', '5'))
    MASS_CHECK_MIN_CREDITS = int(os.getenv('MASS_CHECK_MIN_CREDITS', '5'))
    MAX_MASS_CHECK_CARDS = int(os.getenv('MAX_MASS_CHECK_CARDS', '10'))
    
    # Premium settings
    PREMIUM_UNLIMITED = os.getenv('PREMIUM_UNLIMITED', 'true').lower() == 'true'
    
    # Bot information
    BOT_NAME = os.getenv('BOT_NAME', 'Supreme Card Checker Bot')
    BOT_VERSION = os.getenv('BOT_VERSION', '2.0.0')
    CHANNEL_URL = os.getenv('CHANNEL_URL', 'https://t.me/your_channel')
    SUPPORT_URL = os.getenv('SUPPORT_URL', 'https://t.me/your_support')
    ADMIN_URL = os.getenv('ADMIN_URL', 'https://t.me/your_admin')
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in environment variables")
        
        if not cls.ADMIN_IDS:
            raise ValueError("At least one ADMIN_ID is required")
        
        return True


# Validate configuration on import
Config.validate()
