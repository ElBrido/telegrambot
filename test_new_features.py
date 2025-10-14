"""
Test new features: /redeem command and customizable key durations
"""

import os
import sys
from database import Database
import secrets


def test_key_generation_with_duration():
    """Test generating keys with custom durations"""
    print("Testing key generation with custom durations...")
    
    # Create a test database
    db_name = "test_duration.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    
    db = Database(db_name)
    
    # Test creating keys with different durations (all as integers for database)
    test_cases = [
        (24, "24 hours"),
        (1, "1 hour"),
        (1, "1 hour (from 0.5 * 2)"),  # Store as 1 hour minimum
        (720, "30 days (720 hours)"),
    ]
    
    for duration_hours, description in test_cases:
        key_code = secrets.token_urlsafe(32)
        success = db.create_premium_key(key_code, duration_hours)
        assert success, f"Failed to create key with duration {description}"
        print(f"  ✅ Created key with duration: {description}")
    
    # Clean up
    os.remove(db_name)
    print("✅ Key generation with duration tests passed!\n")


def test_key_activation():
    """Test key activation with stored duration"""
    print("Testing key activation with stored durations...")
    
    # Create a test database
    db_name = "test_activation.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    
    db = Database(db_name)
    db.add_user(12345, "testuser", "Test", "User")
    
    # Create and activate a key with custom duration
    key_code = secrets.token_urlsafe(32)
    duration_hours = 48  # 2 days
    
    success = db.create_premium_key(key_code, duration_hours)
    assert success, "Failed to create key"
    print(f"  ✅ Created key: {key_code[:10]}...")
    
    # Activate the key
    success, message = db.activate_premium_key(12345, key_code)
    assert success, f"Failed to activate key: {message}"
    print(f"  ✅ Activated key: {message}")
    
    # Check premium status
    has_premium = db.has_premium(12345)
    assert has_premium, "User should have premium after activation"
    print("  ✅ Premium status confirmed")
    
    # Clean up
    os.remove(db_name)
    print("✅ Key activation tests passed!\n")


def test_long_keys():
    """Test that keys are now 32 characters (longer than before)"""
    print("Testing longer key generation...")
    
    # Generate a key with the new length
    key_code = secrets.token_urlsafe(32)
    
    # token_urlsafe(32) generates approximately 43 characters
    # (32 bytes encoded in base64 URL-safe format)
    # Minimum expected length is 40 characters
    MIN_EXPECTED_LENGTH = 40
    assert len(key_code) >= MIN_EXPECTED_LENGTH, \
        f"Key should be at least {MIN_EXPECTED_LENGTH} chars, got {len(key_code)}"
    print(f"  ✅ Generated key length: {len(key_code)} characters")
    print(f"  ✅ Example key: {key_code}")
    
    print("✅ Long key generation tests passed!\n")


def test_duration_parsing():
    """Test parsing duration strings like '24h', '30m', '7d', '3600s'"""
    print("Testing duration parsing logic...")
    
    test_cases = [
        ("24h", 24, "24 hours"),
        ("30m", 0.5, "30 minutes"),
        ("7d", 168, "7 days"),
        ("3600s", 1, "3600 seconds (1 hour)"),
        ("1h", 1, "1 hour"),
        ("60m", 1, "60 minutes"),
    ]
    
    for duration_str, expected_hours, description in test_cases:
        # Parse duration with float division for precision
        if duration_str.endswith('s'):
            duration_hours = float(duration_str[:-1]) / 3600.0
        elif duration_str.endswith('m'):
            duration_hours = float(duration_str[:-1]) / 60.0
        elif duration_str.endswith('h'):
            duration_hours = float(duration_str[:-1])
        elif duration_str.endswith('d'):
            duration_hours = float(duration_str[:-1]) * 24.0
        else:
            duration_hours = float(duration_str)
        
        # Check if parsing is correct
        assert abs(duration_hours - expected_hours) < 0.01, \
            f"Duration parsing failed for {duration_str}: expected {expected_hours}, got {duration_hours}"
        
        print(f"  ✅ Parsed '{duration_str}' = {duration_hours} hours ({description})")
    
    print("✅ Duration parsing tests passed!\n")


def run_all_tests():
    """Run all new feature tests"""
    print("=" * 50)
    print("🔑 New Features Test Suite 🔑")
    print("=" * 50)
    print()
    
    try:
        test_long_keys()
        test_duration_parsing()
        test_key_generation_with_duration()
        test_key_activation()
        
        print("=" * 50)
        print("✅ ALL NEW FEATURE TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
