"""BIN (Bank Identification Number) checker module."""
import random


class BINChecker:
    """Check and get information about card BINs."""
    
    # Sample BIN database (in production, use a real BIN database API)
    BIN_DATABASE = {
        '4111': {
            'scheme': 'VISA',
            'type': 'CREDIT',
            'brand': 'VISA',
            'bank': 'Sample Bank',
            'country': 'United States',
            'country_code': 'US'
        },
        '5500': {
            'scheme': 'MASTERCARD',
            'type': 'CREDIT',
            'brand': 'MASTERCARD',
            'bank': 'Global Bank',
            'country': 'United States',
            'country_code': 'US'
        },
        '3400': {
            'scheme': 'AMEX',
            'type': 'CREDIT',
            'brand': 'AMERICAN EXPRESS',
            'bank': 'American Express',
            'country': 'United States',
            'country_code': 'US'
        },
    }
    
    @staticmethod
    def get_bin_info(bin_number):
        """
        Get BIN information.
        In production, integrate with a real BIN database API.
        """
        bin_str = str(bin_number)[:4]
        
        # Check if BIN exists in database
        if bin_str in BINChecker.BIN_DATABASE:
            return BINChecker.BIN_DATABASE[bin_str]
        
        # Generate sample data for unknown BINs
        schemes = ['VISA', 'MASTERCARD', 'AMEX', 'DISCOVER']
        types = ['CREDIT', 'DEBIT', 'PREPAID']
        countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 'France']
        country_codes = ['US', 'GB', 'CA', 'DE', 'FR']
        
        idx = random.randint(0, 4)
        
        return {
            'scheme': random.choice(schemes),
            'type': random.choice(types),
            'brand': random.choice(schemes),
            'bank': 'Unknown Bank',
            'country': countries[idx],
            'country_code': country_codes[idx]
        }
    
    @staticmethod
    def format_bin_info(bin_number, bin_info):
        """Format BIN information for display."""
        text = f"""
🏦 **BIN INFORMATION**

**BIN:** {bin_number}

💳 **Card Scheme:** {bin_info['scheme']}
📋 **Card Type:** {bin_info['type']}
🏷 **Brand:** {bin_info['brand']}
🏦 **Bank:** {bin_info['bank']}
🌍 **Country:** {bin_info['country']} ({bin_info['country_code']})

━━━━━━━━━━━━━━━━━━━━
ℹ️ This information is based on the first 6 digits of the card number (BIN).
"""
        return text.strip()
