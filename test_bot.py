#!/usr/bin/env python3
"""Test script to verify BatmanWL Bot installation and functionality."""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    try:
        import telegram
        print("   ✅ python-telegram-bot")
        
        import sqlalchemy
        print("   ✅ sqlalchemy")
        
        import dotenv
        print("   ✅ python-dotenv")
        
        import requests
        print("   ✅ requests")
        
        from PIL import Image
        print("   ✅ Pillow")
        
        import cryptography
        print("   ✅ cryptography")
        
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\n🧪 Testing configuration...")
    try:
        # Check if .env exists
        if not os.path.exists('.env'):
            print("   ⚠️  .env file not found")
            print("   Run ./setup.sh to create it")
            return False
        
        import config
        print(f"   ✅ Bot name: {config.BOT_NAME}")
        print(f"   ✅ Owner ID: {config.OWNER_ID}")
        print(f"   ✅ Admin IDs: {config.ADMIN_IDS}")
        print(f"   ✅ Database: {config.DATABASE_URL}")
        
        return True
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\n🧪 Testing database...")
    try:
        import database
        
        # Initialize database
        database.init_db()
        print("   ✅ Database initialized")
        
        # Test user creation
        user = database.get_or_create_user(999999999, "testuser", "Test User")
        print(f"   ✅ User created: {user.first_name}")
        
        # Test key generation
        key = database.generate_key(24, 1, 999999999)
        print(f"   ✅ Key generated: {key.key[:10]}...")
        
        # Test key redemption
        result_user, message = database.redeem_key(999999999, key.key)
        if result_user:
            print(f"   ✅ Key redeemed: {message}")
        else:
            print(f"   ❌ Key redemption failed: {message}")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_features():
    """Test feature functions."""
    print("\n🧪 Testing features...")
    try:
        import features
        
        # Test calculator
        result = features.calculate_expression("2 + 2")
        if "4" in result:
            print("   ✅ Calculator working")
        else:
            print(f"   ❌ Calculator failed: {result}")
            return False
        
        # Test other features exist
        features.generate_image("test")
        print("   ✅ Image generation function exists")
        
        features.get_weather("test")
        print("   ✅ Weather function exists")
        
        features.advanced_search("test")
        print("   ✅ Search function exists")
        
        features.translate_text("test", "es")
        print("   ✅ Translation function exists")
        
        return True
    except Exception as e:
        print(f"   ❌ Features error: {e}")
        return False

def test_bot():
    """Test bot can be imported."""
    print("\n🧪 Testing bot module...")
    try:
        import bot
        print("   ✅ Bot module imports successfully")
        
        # Check main function exists
        if hasattr(bot, 'main'):
            print("   ✅ Main function exists")
        else:
            print("   ❌ Main function not found")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Bot error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🦇 BatmanWL Bot - Test Suite 🦇")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Database", test_database()))
    results.append(("Features", test_features()))
    results.append(("Bot Module", test_bot()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your bot is ready to run!")
        print("\nTo start the bot:")
        print("  source venv/bin/activate")
        print("  python3 bot.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
