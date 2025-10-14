"""Configuration management for BatmanWL Bot."""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME', '𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot')

# Owner and admin configuration
OWNER_ID = int(os.getenv('OWNER_ID', 0))
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///batmanwl.db')

# Validate required configuration
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required in .env file")
if OWNER_ID == 0:
    raise ValueError("OWNER_ID is required in .env file")
