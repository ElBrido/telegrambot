"""
Test payment gateway integration
"""
import os
import asyncio
from bot import BatmanWLBot

def test_payment_gateway_configuration():
    """Test that payment gateway can be configured"""
    print("Testing payment gateway configuration...")
    
    # Create test config with payment gateway
    with open('test_payment_config.ini', 'w') as f:
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
DB_NAME = test_payment.db

[PAYMENT_GATEWAY]
GATEWAY_TYPE = stripe
API_KEY = test_api_key
API_SECRET = test_api_secret
WEBHOOK_SECRET = test_webhook
TEST_MODE = true
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_payment_config.ini')
    
    # Check configuration loaded
    assert bot.gateway_type == 'stripe', "Gateway type should be 'stripe'"
    assert bot.gateway_api_key == 'test_api_key', "API key should be loaded"
    assert bot.gateway_test_mode == True, "Test mode should be True"
    
    print("✅ Payment gateway configuration loaded successfully")
    
    # Cleanup
    os.remove('test_payment_config.ini')
    if os.path.exists('test_payment.db'):
        os.remove('test_payment.db')
    
    print("✅ Payment gateway configuration test passed!")

async def test_payment_gateway_simulation():
    """Test payment gateway in simulation mode"""
    print("\nTesting payment gateway simulation mode...")
    
    # Create test config without payment gateway
    with open('test_sim_config.ini', 'w') as f:
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
DB_NAME = test_simulation.db

[PAYMENT_GATEWAY]
GATEWAY_TYPE = 
API_KEY = 
API_SECRET = 
TEST_MODE = true
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_sim_config.ini')
    
    # Test charge processing in simulation mode
    card_info = {
        'card': '4532015112830366',
        'month': 12,
        'year': 25,
        'cvv': '123',
        'is_valid': True
    }
    
    result = await bot.process_payment_gateway_charge(card_info)
    
    assert result['simulation'] == True, "Should be in simulation mode"
    assert result['gateway'] == 'simulation', "Gateway should be simulation"
    assert result['status'] in ['APPROVED', 'DECLINED'], "Status should be APPROVED or DECLINED"
    
    print(f"✅ Simulation result: {result['status']} - {result['message']}")
    
    # Cleanup
    os.remove('test_sim_config.ini')
    if os.path.exists('test_simulation.db'):
        os.remove('test_simulation.db')
    
    print("✅ Payment gateway simulation test passed!")

async def test_vbv_verification_simulation():
    """Test VBV/3D Secure verification in simulation mode"""
    print("\nTesting VBV verification simulation mode...")
    
    # Create test config without payment gateway
    with open('test_vbv_config.ini', 'w') as f:
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
DB_NAME = test_vbv.db

[PAYMENT_GATEWAY]
GATEWAY_TYPE = 
API_KEY = 
API_SECRET = 
TEST_MODE = true
""")
    
    # Initialize bot
    bot = BatmanWLBot('test_vbv_config.ini')
    
    # Test VBV verification without gateway (should return error)
    card_info = {
        'card': '4532015112830366',
        'month': 12,
        'year': 25,
        'cvv': '123',
        'is_valid': True
    }
    
    result = await bot.verify_vbv_3d_secure(card_info)
    
    assert result['simulation'] == True, "Should be in simulation mode"
    assert result['gateway'] == 'none', "Gateway should be none"
    assert result['error'] == True, "Should have error without gateway"
    assert 'requiere configurar' in result['message'], "Should mention configuration needed"
    
    print(f"✅ VBV simulation result: {result['message']}")
    
    # Cleanup
    os.remove('test_vbv_config.ini')
    if os.path.exists('test_vbv.db'):
        os.remove('test_vbv.db')
    
    print("✅ VBV verification simulation test passed!")

def test_cleanup_expired_keys():
    """Test cleanup of expired keys"""
    print("\nTesting expired keys cleanup...")
    
    from database import Database
    import secrets
    from datetime import datetime, timedelta
    import sqlite3
    
    # Create test database
    test_db = "test_cleanup.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = Database(test_db)
    
    # Add test users
    db.add_user(12345, "testuser", "Test", "User")
    db.add_user(67890, "validuser", "Valid", "User")
    
    # Create an expired key manually by setting expires_at in the past
    key_code1 = secrets.token_urlsafe(32)
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Insert expired key directly
    past_time = datetime.now() - timedelta(hours=1)
    cursor.execute("""
        INSERT INTO premium_keys (key_code, user_id, activated_at, expires_at, is_active, duration_hours)
        VALUES (?, ?, ?, ?, 1, 1)
    """, (key_code1, 12345, past_time, past_time))
    conn.commit()
    conn.close()
    
    print(f"Created expired key for user 12345")
    
    # Create a valid key (1 day)
    key_code2 = secrets.token_urlsafe(32)
    db.create_premium_key(key_code2, duration_hours=24)
    success, msg = db.activate_premium_key(67890, key_code2)
    print(f"Activated key 2: {msg}")
    
    # Check status before cleanup
    has_premium_before = db.has_premium(12345)
    print(f"User 12345 has premium before cleanup: {has_premium_before}")
    
    # Run cleanup
    count = db.cleanup_expired_keys()
    print(f"Cleaned up {count} expired keys")
    
    # Check that expired key is now inactive
    has_premium_expired = db.has_premium(12345)
    has_premium_valid = db.has_premium(67890)
    
    assert has_premium_expired == False, "Expired user should not have premium"
    assert has_premium_valid == True, "Valid user should still have premium"
    
    print("✅ Cleanup correctly deactivated expired keys")
    
    # Cleanup
    os.remove(test_db)
    
    print("✅ Expired keys cleanup test passed!")

def test_premium_info():
    """Test getting premium info"""
    print("\nTesting premium info retrieval...")
    
    from database import Database
    import secrets
    
    # Create test database
    test_db = "test_premium_info.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = Database(test_db)
    
    # Add test user
    db.add_user(12345, "testuser", "Test", "User")
    
    # User without premium
    info = db.get_premium_info(12345)
    assert info is None, "User without premium should have no info"
    print("✅ User without premium returns None")
    
    # Create and activate a key
    key_code = secrets.token_urlsafe(32)
    db.create_premium_key(key_code, duration_hours=48)
    success, msg = db.activate_premium_key(12345, key_code)
    
    # Get premium info
    info = db.get_premium_info(12345)
    assert info is not None, "User with premium should have info"
    assert 'expires_at' in info, "Info should contain expires_at"
    assert 'activated_at' in info, "Info should contain activated_at"
    assert info['duration_hours'] == 48, "Duration should be 48 hours"
    
    print(f"✅ Premium info retrieved: expires at {info['expires_at']}")
    
    # Cleanup
    os.remove(test_db)
    
    print("✅ Premium info test passed!")

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Payment Gateway & Premium Tests")
    print("=" * 60)
    
    test_payment_gateway_configuration()
    asyncio.run(test_payment_gateway_simulation())
    asyncio.run(test_vbv_verification_simulation())
    test_cleanup_expired_keys()
    test_premium_info()
    
    print("\n" + "=" * 60)
    print("✅ All payment gateway and premium tests passed!")
    print("=" * 60)
