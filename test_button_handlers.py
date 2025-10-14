"""
Test suite for button handlers
Validates that callback query handlers work correctly
"""

import sys
import os
import asyncio
from unittest.mock import Mock, AsyncMock
from bot import BatmanWLBot


def test_button_handler_stats():
    """Test stats button handler with callback query"""
    print("Testing stats button handler...")
    
    # Create test database
    test_db = "test_button_db.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create mock config
    with open('test_config.ini', 'w') as f:
        f.write("""[BOT]
TOKEN = test_token_123
ADMIN_IDS = 12345
OWNER_ID = 12345

[WELCOME]
GIF_URL = https://example.com/test.gif
MESSAGE = Test Welcome

[PREMIUM]
KEY_DURATION_DAYS = 30

[DATABASE]
DB_NAME = test_button_db.db
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_config.ini')
    
    # Create test user
    bot.db.add_user(67890, "testuser", "Test", "User", "user")
    bot.db.add_card_check(67890, "4532015112830366", "ACTIVE")
    
    # Create mock update and context for callback query
    update = Mock()
    context = Mock()
    
    # Mock callback query
    query = Mock()
    query.data = 'stats'
    query.from_user = Mock()
    query.from_user.id = 67890
    query.from_user.username = "testuser"
    query.from_user.first_name = "Test"
    query.message = Mock()
    
    # Mock async methods
    query.answer = AsyncMock()
    query.message.reply_text = AsyncMock()
    
    update.callback_query = query
    
    # Test the button handler
    asyncio.run(bot.button_handler(update, context))
    
    # Verify query.answer() was called
    assert query.answer.called, "query.answer() should be called"
    
    # Verify reply_text was called
    assert query.message.reply_text.called, "query.message.reply_text should be called"
    
    # Get the response text
    call_args = query.message.reply_text.call_args
    response_text = call_args[0][0] if call_args[0] else call_args.kwargs.get('text', '')
    
    # Verify response contains expected content
    assert "Tus Estadísticas" in response_text, "Response should contain stats title"
    assert "testuser" in response_text or "Test" in response_text, "Response should contain username"
    assert "67890" in response_text, "Response should contain user ID"
    assert "Verificaciones:" in response_text, "Response should contain checks count"
    
    print("  ✅ Stats button handler works correctly")
    print(f"  ✅ Response contains user info and statistics")
    
    # Cleanup
    os.remove(test_db)
    os.remove('test_config.ini')
    
    print("✅ Stats button handler test passed!\n")


def test_button_handler_help():
    """Test help button handler with callback query"""
    print("Testing help button handler...")
    
    # Create test database
    test_db = "test_button_help_db.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create mock config
    with open('test_config.ini', 'w') as f:
        f.write("""[BOT]
TOKEN = test_token_123
ADMIN_IDS = 12345
OWNER_ID = 12345

[WELCOME]
GIF_URL = https://example.com/test.gif
MESSAGE = Test Welcome

[PREMIUM]
KEY_DURATION_DAYS = 30

[DATABASE]
DB_NAME = test_button_help_db.db
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_config.ini')
    
    # Create test user (regular user)
    bot.db.add_user(67890, "testuser", "Test", "User", "user")
    
    # Create mock update and context for callback query
    update = Mock()
    context = Mock()
    
    # Mock callback query
    query = Mock()
    query.data = 'help'
    query.from_user = Mock()
    query.from_user.id = 67890
    query.from_user.username = "testuser"
    query.message = Mock()
    
    # Mock async methods
    query.answer = AsyncMock()
    query.message.reply_text = AsyncMock()
    
    update.callback_query = query
    
    import asyncio
    asyncio.run(bot.button_handler(update, context))
    
    # Verify query.answer() was called
    assert query.answer.called, "query.answer() should be called"
    
    # Verify reply_text was called
    assert query.message.reply_text.called, "query.message.reply_text should be called"
    
    # Get the response text
    call_args = query.message.reply_text.call_args
    response_text = call_args[0][0] if call_args[0] else call_args.kwargs.get('text', '')
    
    # Verify response contains expected content
    assert "BatmanWL - Ayuda" in response_text, "Response should contain help title"
    assert "/ccn" in response_text, "Response should contain /ccn command"
    assert "/bin" in response_text, "Response should contain /bin command"
    assert "/gen" in response_text, "Response should contain /gen command"
    assert "/key" in response_text, "Response should contain /key command"
    
    # Should NOT contain admin commands for regular user
    assert "/genkey" not in response_text, "Regular user should not see admin commands"
    
    print("  ✅ Help button handler works correctly for regular user")
    print(f"  ✅ Response contains expected commands")
    print(f"  ✅ Admin commands properly hidden from regular user")
    
    # Test with admin user
    bot.db.add_user(12345, "adminuser", "Admin", "User", "admin")
    query.from_user.id = 12345
    query.message.reply_text = AsyncMock()  # Reset mock
    
    asyncio.run(bot.button_handler(update, context))
    
    # Get the response text for admin
    call_args = query.message.reply_text.call_args
    admin_response = call_args[0][0] if call_args[0] else call_args.kwargs.get('text', '')
    
    # Verify admin sees admin commands
    assert "/genkey" in admin_response, "Admin user should see admin commands"
    assert "/ban" in admin_response, "Admin user should see /ban command"
    assert "/broadcast" in admin_response, "Admin user should see /broadcast command"
    
    print("  ✅ Help button handler shows admin commands to admin users")
    
    # Cleanup
    os.remove(test_db)
    os.remove('test_config.ini')
    
    print("✅ Help button handler test passed!\n")


def test_all_button_handlers():
    """Test all button handlers respond correctly"""
    print("Testing all button handlers...")
    
    # Create test database
    test_db = "test_all_buttons_db.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create mock config
    with open('test_config.ini', 'w') as f:
        f.write("""[BOT]
TOKEN = test_token_123
ADMIN_IDS = 12345
OWNER_ID = 12345

[WELCOME]
GIF_URL = https://example.com/test.gif
MESSAGE = Test Welcome

[PREMIUM]
KEY_DURATION_DAYS = 30

[DATABASE]
DB_NAME = test_all_buttons_db.db
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_config.ini')
    
    # Create test user
    bot.db.add_user(67890, "testuser", "Test", "User", "user")
    
    # Test all button types
    button_tests = [
        ('ccn_check', 'Verificar Tarjeta'),
        ('bin_lookup', 'Buscar BIN'),
        ('gen_cards', 'Premium'),  # Should show premium required
        ('activate_key', 'Activar Clave Premium'),
        ('stats', 'Tus Estadísticas'),
        ('help', 'BatmanWL - Ayuda'),
    ]
    
    for button_data, expected_text in button_tests:
        # Create mock update and context
        update = Mock()
        context = Mock()
        query = Mock()
        query.data = button_data
        query.from_user = Mock()
        query.from_user.id = 67890
        query.from_user.username = "testuser"
        query.from_user.first_name = "Test"
        query.message = Mock()
        query.answer = AsyncMock()
        query.message.reply_text = AsyncMock()
        update.callback_query = query
        
        # Test the button
        asyncio.run(bot.button_handler(update, context))
        
        # Verify response
        assert query.answer.called, f"Button {button_data} should call query.answer()"
        assert query.message.reply_text.called, f"Button {button_data} should send a message"
        
        call_args = query.message.reply_text.call_args
        response = call_args[0][0] if call_args[0] else call_args.kwargs.get('text', '')
        assert expected_text in response, f"Button {button_data} should contain '{expected_text}' in response"
        
        print(f"  ✅ Button '{button_data}' works correctly")
    
    # Cleanup
    os.remove(test_db)
    os.remove('test_config.ini')
    
    print("✅ All button handlers test passed!\n")


def run_all_tests():
    """Run all button handler tests"""
    print("=" * 50)
    print("🦇 BatmanWL Bot - Button Handler Tests 🦇")
    print("=" * 50)
    print()
    
    try:
        test_button_handler_stats()
        test_button_handler_help()
        test_all_button_handlers()
        
        print("=" * 50)
        print("✅ ALL BUTTON HANDLER TESTS PASSED!")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
