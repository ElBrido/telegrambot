"""
BIN checker module for BIN lookup functionality
"""

from typing import Dict


class BINChecker:
    # Extended BIN database
    BIN_DATABASE = {
        "4": {
            "type": "VISA",
            "network": "Visa",
            "country": "Various",
            "bank": "Multiple Issuers"
        },
        "5": {
            "type": "MASTERCARD",
            "network": "Mastercard",
            "country": "Various",
            "bank": "Multiple Issuers"
        },
        "3": {
            "type": "AMEX",
            "network": "American Express",
            "country": "USA",
            "bank": "American Express"
        },
        "6": {
            "type": "DISCOVER",
            "network": "Discover",
            "country": "USA",
            "bank": "Discover Financial"
        },
    }
    
    @staticmethod
    def get_bin_info(bin_number: str) -> Dict[str, str]:
        """Get BIN information from database.
        
        Args:
            bin_number: First 4-6 digits of card
            
        Returns:
            Dictionary with BIN information
        """
        if not bin_number or len(bin_number) < 1:
            return {"error": "Invalid BIN"}
        
        # Get first digit
        first_digit = bin_number[0]
        
        if first_digit in BINChecker.BIN_DATABASE:
            info = BINChecker.BIN_DATABASE[first_digit].copy()
            info['bin'] = bin_number
            return info
        
        return {
            'bin': bin_number,
            'type': 'UNKNOWN',
            'network': 'Unknown',
            'country': 'N/A',
            'bank': 'N/A'
        }
    
    @staticmethod
    def format_bin_info(bin_number: str, bin_info: Dict[str, str]) -> str:
        """Format BIN information for display.
        
        Args:
            bin_number: BIN number
            bin_info: BIN information dictionary
            
        Returns:
            Formatted string for Telegram message
        """
        if 'error' in bin_info:
            return f"❌ {bin_info['error']}"
        
        result = f"""
🔍 **BIN LOOKUP**

**BIN:** `{bin_number}`
**Type:** {bin_info.get('type', 'Unknown')}
**Network:** {bin_info.get('network', 'Unknown')}
**Country:** {bin_info.get('country', 'N/A')}
**Bank:** {bin_info.get('bank', 'N/A')}
"""
        return result
