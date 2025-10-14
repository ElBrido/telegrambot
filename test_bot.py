"""
Test suite for BatmanWL Bot
Simple tests to validate core functionality
"""

import os
import sys
from card_utils import CardUtils
from database import Database


def test_card_validation():
    """Test card validation using Luhn algorithm"""
    print("Testing card validation...")
    
    # Valid cards
    valid_cards = [
        "4532015112830366",
        "5425233430109903",
        "378282246310005",
        "6011111111111117",
    ]
    
    for card in valid_cards:
        assert CardUtils.validate_card(card), f"Valid card {card} failed validation"
        print(f"  ✅ {card} - Valid")
    
    # Invalid cards
    invalid_cards = [
        "1234567890123456",
        "0000000000000000",
        "9999999999999999",
    ]
    
    for card in invalid_cards:
        assert not CardUtils.validate_card(card), f"Invalid card {card} passed validation"
        print(f"  ✅ {card} - Invalid (as expected)")
    
    print("✅ Card validation tests passed!\n")


def test_card_generation():
    """Test card generation"""
    print("Testing card generation...")
    
    bin_prefix = "453201"
    cards = CardUtils.generate_multiple_cards(bin_prefix, 10)
    
    assert len(cards) == 10, f"Expected 10 cards, got {len(cards)}"
    print(f"  ✅ Generated {len(cards)} cards")
    
    for card in cards:
        assert card.startswith(bin_prefix), f"Card {card} doesn't start with {bin_prefix}"
        assert CardUtils.validate_card(card), f"Generated card {card} is invalid"
    
    print(f"  ✅ All generated cards are valid")
    print("✅ Card generation tests passed!\n")


def test_bin_lookup():
    """Test BIN lookup"""
    print("Testing BIN lookup...")
    
    test_bins = {
        "4": {"type": "VISA", "network": "Visa"},
        "5": {"type": "MASTERCARD", "network": "Mastercard"},
        "3": {"type": "AMEX", "network": "American Express"},
        "6": {"type": "DISCOVER", "network": "Discover"},
    }
    
    for bin_num, expected in test_bins.items():
        result = CardUtils.get_bin_info(bin_num)
        assert result["type"] == expected["type"], f"BIN {bin_num} type mismatch"
        assert result["network"] == expected["network"], f"BIN {bin_num} network mismatch"
        print(f"  ✅ BIN {bin_num} - {result['type']}")
    
    print("✅ BIN lookup tests passed!\n")


def test_database_operations():
    """Test database operations"""
    print("Testing database operations...")
    
    # Use temporary database
    test_db = "test_database.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = Database(test_db)
    
    # Test user operations
    db.add_user(12345, "testuser", "Test", "User", "user")
    user = db.get_user(12345)
    assert user is not None, "User not found"
    assert user["username"] == "testuser", "Username mismatch"
    assert user["role"] == "user", "Role mismatch"
    print("  ✅ User operations work")
    
    # Test role system
    db.add_user(67890, "adminuser", "Admin", "User", "admin")
    assert db.is_admin(67890), "Admin check failed"
    assert not db.is_owner(67890), "Owner check failed"
    print("  ✅ Role system works")
    
    # Test premium keys
    key_code = "TEST123KEY"
    assert db.create_premium_key(key_code), "Key creation failed"
    
    success, msg = db.activate_premium_key(12345, key_code, 30)
    assert success, f"Key activation failed: {msg}"
    
    assert db.has_premium(12345), "Premium check failed"
    print("  ✅ Premium key system works")
    
    # Test card checks
    db.add_card_check(12345, "4532015112830366", "ACTIVE")
    stats = db.get_user_stats(12345)
    assert stats["total_checks"] == 1, "Card check logging failed"
    print("  ✅ Card check logging works")
    
    # Cleanup
    os.remove(test_db)
    print("✅ Database tests passed!\n")


def test_card_formatting():
    """Test card number formatting"""
    print("Testing card formatting...")
    
    card = "4532015112830366"
    formatted = CardUtils.format_card_number(card)
    expected = "4532 0151 1283 0366"
    
    assert formatted == expected, f"Expected {expected}, got {formatted}"
    print(f"  ✅ {card} → {formatted}")
    print("✅ Card formatting tests passed!\n")


def test_input_parsing():
    """Test pipe-delimited input parsing"""
    print("Testing input parsing...")
    
    # Test full format: card|mm|yy|cvv
    test_cases = [
        {
            "input": "4532015112830366|12|28|123",
            "expected": {
                "card": "4532015112830366",
                "month": "12",
                "year": "28",
                "cvv": "123"
            }
        },
        {
            "input": "515462002002|04|31",
            "expected": {
                "card": "515462002002",
                "month": "04",
                "year": "31",
                "cvv": None
            }
        },
        {
            "input": "111111|0|0|",
            "expected": {
                "card": "111111",
                "month": None,  # 0 is invalid month
                "year": "00",
                "cvv": None
            }
        },
        {
            "input": "453201|12|28",
            "expected": {
                "card": "453201",
                "month": "12",
                "year": "28",
                "cvv": None
            }
        },
        {
            "input": "4532015112830366",
            "expected": {
                "card": "4532015112830366",
                "month": None,
                "year": None,
                "cvv": None
            }
        },
        {
            "input": "453201|4|2031|456",
            "expected": {
                "card": "453201",
                "month": "04",  # Should pad to 2 digits
                "year": "31",   # Should take last 2 digits from 2031
                "cvv": "456"
            }
        }
    ]
    
    for test in test_cases:
        result = CardUtils.parse_card_input(test["input"])
        expected = test["expected"]
        
        assert result["card"] == expected["card"], \
            f"Card mismatch for '{test['input']}': expected {expected['card']}, got {result['card']}"
        assert result["month"] == expected["month"], \
            f"Month mismatch for '{test['input']}': expected {expected['month']}, got {result['month']}"
        assert result["year"] == expected["year"], \
            f"Year mismatch for '{test['input']}': expected {expected['year']}, got {result['year']}"
        assert result["cvv"] == expected["cvv"], \
            f"CVV mismatch for '{test['input']}': expected {expected['cvv']}, got {result['cvv']}"
        
        print(f"  ✅ {test['input']} → parsed correctly")
    
    print("✅ Input parsing tests passed!\n")


def test_expiry_formatting():
    """Test expiry date formatting"""
    print("Testing expiry formatting...")
    
    test_cases = [
        {"month": "12", "year": "28", "expected": "12/28"},
        {"month": "04", "year": "31", "expected": "04/31"},
        {"month": None, "year": "28", "expected": None},
        {"month": "12", "year": None, "expected": None},
        {"month": None, "year": None, "expected": None},
    ]
    
    for test in test_cases:
        result = CardUtils.format_expiry(test["month"], test["year"])
        expected = test["expected"]
        
        assert result == expected, \
            f"Expiry format mismatch: expected {expected}, got {result}"
        
        print(f"  ✅ ({test['month']}, {test['year']}) → {result}")
    
    print("✅ Expiry formatting tests passed!\n")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("🦇 BatmanWL Bot - Test Suite 🦇")
    print("=" * 50)
    print()
    
    try:
        test_card_validation()
        test_card_generation()
        test_bin_lookup()
        test_database_operations()
        test_card_formatting()
        test_input_parsing()
        test_expiry_formatting()
        
        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
