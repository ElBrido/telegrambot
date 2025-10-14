"""
Card checker module for advanced card validation
Provides card parsing and status checking functionality
"""

import re
import random
from typing import Dict, Optional


class CardChecker:
    @staticmethod
    def parse_card(card_input: str) -> Optional[Dict[str, str]]:
        """Parse card information from input string.
        
        Args:
            card_input: Card info in format card|mm|yyyy|cvv or card|mm|yy|cvv
            
        Returns:
            Dictionary with card_number, month, year, cvv or None if invalid
        """
        # Remove extra spaces
        card_input = card_input.strip()
        
        # Split by pipe
        parts = card_input.split('|')
        
        if len(parts) < 1:
            return None
        
        # Extract card number (remove non-digits)
        card_number = re.sub(r'\D', '', parts[0])
        
        if not card_number or len(card_number) < 13:
            return None
        
        result = {
            'card_number': card_number,
            'month': parts[1] if len(parts) > 1 else None,
            'year': parts[2] if len(parts) > 2 else None,
            'cvv': parts[3] if len(parts) > 3 else None
        }
        
        return result
    
    @staticmethod
    async def check_card(card_info: Dict[str, str]) -> Dict[str, str]:
        """Simulate card checking.
        
        Args:
            card_info: Dictionary with card details
            
        Returns:
            Dictionary with status and reason
        """
        # Validate card using Luhn
        card_number = card_info['card_number']
        
        # Simple Luhn validation
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            checksum = 0
            for i in range(len(digits) - 1, -1, -2):
                checksum += digits[i]
            for i in range(len(digits) - 2, -1, -2):
                doubled = digits[i] * 2
                checksum += doubled if doubled < 10 else doubled - 9
            return checksum % 10 == 0
        
        if not luhn_check(card_number):
            return {
                'status': 'DECLINED',
                'reason': 'Invalid Card Number (Luhn Failed)'
            }
        
        # Simulate different statuses
        status_options = [
            ('APPROVED', 'CVV Match - Card Active'),
            ('APPROVED', 'Authorized - Sufficient Funds'),
            ('DECLINED', 'Insufficient Funds'),
            ('DECLINED', 'Card Declined'),
            ('DECLINED', 'Do Not Honor'),
        ]
        
        # Use card number last digit for consistency
        last_digit = int(card_number[-1])
        if last_digit % 2 == 0:
            status, reason = status_options[0]
        else:
            status, reason = random.choice(status_options)
        
        return {
            'status': status,
            'reason': reason
        }
    
    @staticmethod
    def format_check_result(card_info: Dict[str, str], check_result: Dict[str, str]) -> str:
        """Format card check result for display.
        
        Args:
            card_info: Card information dictionary
            check_result: Check result dictionary
            
        Returns:
            Formatted string for Telegram message
        """
        card_number = card_info['card_number']
        masked_card = f"{card_number[:4]}••••••••{card_number[-4:]}"
        
        status_emoji = '✅' if check_result['status'] == 'APPROVED' else '❌'
        
        result = f"""
{status_emoji} **CARD CHECK RESULT**

**Card:** `{masked_card}`
**Status:** {check_result['status']}
**Response:** {check_result['reason']}
"""
        
        if card_info.get('month') and card_info.get('year'):
            result += f"**Expiry:** {card_info['month']}/{card_info['year']}\n"
        
        if card_info.get('cvv'):
            result += f"**CVV:** {card_info['cvv']}\n"
        
        return result
