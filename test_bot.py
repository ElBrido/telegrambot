"""Test suite for the Telegram bot."""
import asyncio
import unittest
from card_checker import CardChecker
from bin_checker import BINChecker


class TestCardChecker(unittest.TestCase):
    """Test card checking functionality."""
    
    def test_luhn_check_valid(self):
        """Test Luhn algorithm with valid card."""
        # Valid test card numbers
        valid_cards = [
            '4111111111111111',  # VISA
            '5500000000000004',  # Mastercard
            '340000000000009',   # AMEX
        ]
        
        for card in valid_cards:
            self.assertTrue(CardChecker.luhn_check(card))
    
    def test_luhn_check_invalid(self):
        """Test Luhn algorithm with invalid card."""
        invalid_cards = [
            '4111111111111112',
            '1234567890123456',
        ]
        
        for card in invalid_cards:
            self.assertFalse(CardChecker.luhn_check(card))
    
    def test_get_card_type(self):
        """Test card type identification."""
        self.assertEqual(CardChecker.get_card_type('4111111111111111'), '💳 VISA')
        self.assertEqual(CardChecker.get_card_type('5500000000000004'), '💳 MASTERCARD')
        self.assertEqual(CardChecker.get_card_type('340000000000009'), '💳 AMEX')
    
    def test_parse_card_full(self):
        """Test card parsing with full information."""
        card_input = '4111111111111111|12|2025|123'
        result = CardChecker.parse_card(card_input)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['card_number'], '4111111111111111')
        self.assertEqual(result['month'], '12')
        self.assertEqual(result['year'], '2025')
        self.assertEqual(result['cvv'], '123')
    
    def test_parse_card_partial(self):
        """Test card parsing with partial information."""
        card_input = '4111111111111111|12|2025'
        result = CardChecker.parse_card(card_input)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['card_number'], '4111111111111111')
        self.assertEqual(result['month'], '12')
        self.assertEqual(result['year'], '2025')
        self.assertIsNone(result['cvv'])
    
    def test_parse_card_only_number(self):
        """Test card parsing with only card number."""
        card_input = '4111111111111111'
        result = CardChecker.parse_card(card_input)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['card_number'], '4111111111111111')


class TestBINChecker(unittest.TestCase):
    """Test BIN checking functionality."""
    
    def test_get_bin_info(self):
        """Test BIN information retrieval."""
        bin_info = BINChecker.get_bin_info('411111')
        
        self.assertIsNotNone(bin_info)
        self.assertIn('scheme', bin_info)
        self.assertIn('type', bin_info)
        self.assertIn('bank', bin_info)
        self.assertIn('country', bin_info)
    
    def test_format_bin_info(self):
        """Test BIN information formatting."""
        bin_info = {
            'scheme': 'VISA',
            'type': 'CREDIT',
            'brand': 'VISA',
            'bank': 'Test Bank',
            'country': 'United States',
            'country_code': 'US'
        }
        
        result = BINChecker.format_bin_info('411111', bin_info)
        
        self.assertIn('411111', result)
        self.assertIn('VISA', result)
        self.assertIn('CREDIT', result)


class TestAsyncFunctions(unittest.IsolatedAsyncioTestCase):
    """Test async functions."""
    
    async def test_check_card(self):
        """Test card checking."""
        card_info = {
            'card_number': '4111111111111111',
            'month': '12',
            'year': '2025',
            'cvv': '123'
        }
        
        result = await CardChecker.check_card(card_info)
        
        self.assertIsNotNone(result)
        self.assertIn('status', result)
        self.assertIn('reason', result)
        self.assertIn('card_type', result)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCardChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestBINChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestAsyncFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
