#!/usr/bin/env python3
"""
Setup script for Telegram CC Verification Bot
Helps configure the bot on first run
"""

import json
import os
import sys

def setup_config():
    """Interactive setup for config.json"""
    print("=" * 60)
    print("  Telegram CC Verification Bot - Setup")
    print("=" * 60)
    print()
    
    # Check if config already exists
    if os.path.exists('config.json'):
        print("⚠️  config.json already exists!")
        response = input("Do you want to reconfigure? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Setup cancelled.")
            return
        print()
    
    # Get bot token
    print("Step 1: Bot Token")
    print("-" * 40)
    print("Get your bot token from @BotFather on Telegram")
    print("Example: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
    bot_token = input("\nEnter your bot token: ").strip()
    
    if not bot_token or ':' not in bot_token:
        print("❌ Invalid bot token format!")
        return
    
    print("✅ Bot token saved")
    print()
    
    # Get user ID
    print("Step 2: Owner User ID")
    print("-" * 40)
    print("Get your Telegram user ID from @userinfobot")
    print("You need to add at least one owner to use the bot")
    owner_id = input("\nEnter your Telegram user ID: ").strip()
    
    try:
        owner_id = int(owner_id)
    except ValueError:
        print("❌ Invalid user ID! Must be a number.")
        return
    
    print("✅ Owner ID saved")
    print()
    
    # Get GIF URL (optional)
    print("Step 3: Welcome GIF (Optional)")
    print("-" * 40)
    print("Enter a URL to a GIF for the welcome message")
    print("Press Enter to skip")
    gif_url = input("\nEnter GIF URL (or press Enter): ").strip()
    
    if gif_url:
        print("✅ GIF URL saved")
    else:
        print("⚠️  No GIF URL provided (using text only)")
    print()
    
    # Create config
    config = {
        "bot_token": bot_token,
        "welcome_gif_url": gif_url,
        "owners": [owner_id],
        "admins": []
    }
    
    # Save config
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("=" * 60)
        print("✅ Configuration saved successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the bot: python bot.py")
        print()
        print("Your bot is ready to use!")
        print()
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return


def main():
    """Main setup function"""
    try:
        setup_config()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
