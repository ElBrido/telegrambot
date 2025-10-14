"""Card checker module for validating credit cards."""
import re
import random
from datetime import datetime


class CardChecker:
    """Credit card validation and checking."""
    
    @staticmethod
    def luhn_check(card_number):
        """Validate card number using Luhn algorithm."""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0
    
    @staticmethod
    def get_card_type(card_number):
        """Identify card type based on BIN."""
        card_str = str(card_number)
        
        if card_str.startswith('4'):
            return '💳 VISA'
        elif card_str.startswith(('51', '52', '53', '54', '55')):
            return '💳 MASTERCARD'
        elif card_str.startswith(('34', '37')):
            return '💳 AMEX'
        elif card_str.startswith('6011') or card_str.startswith(('644', '645', '646', '647', '648', '649', '65')):
            return '💳 DISCOVER'
        elif card_str.startswith(('300', '301', '302', '303', '304', '305', '36', '38')):
            return '💳 DINERS'
        elif card_str.startswith(('2131', '1800', '35')):
            return '💳 JCB'
        else:
            return '💳 UNKNOWN'
    
    @staticmethod
    def parse_card(card_input):
        """Parse card information from input string."""
        # Remove all non-digit and non-separator characters
        card_input = card_input.strip()
        
        # Try to extract card details
        patterns = [
            r'^(\d{13,19})[|\s]+(\d{2})[|\s/]*(\d{2,4})[|\s]+(\d{3,4})$',  # 4111111111111111|12|2025|123
            r'^(\d{13,19})[|\s]+(\d{2})[|\s/]*(\d{2,4})$',  # 4111111111111111|12|2025
            r'^(\d{13,19})$',  # Just card number
        ]
        
        for pattern in patterns:
            match = re.match(pattern, card_input)
            if match:
                groups = match.groups()
                card_number = groups[0]
                month = groups[1] if len(groups) > 1 else None
                year = groups[2] if len(groups) > 2 else None
                cvv = groups[3] if len(groups) > 3 else None
                
                return {
                    'card_number': card_number,
                    'month': month,
                    'year': year,
                    'cvv': cvv
                }
        
        return None
    
    @staticmethod
    async def check_card(card_info):
        """
        Check card validity.
        This is a simulation - in production, you'd integrate with real payment gateways.
        """
        card_number = card_info['card_number']
        
        # Validate using Luhn
        if not CardChecker.luhn_check(card_number):
            return {
                'status': 'DECLINED',
                'reason': 'Invalid card number (Luhn check failed)',
                'response_time': 0.5
            }
        
        # Get card type
        card_type = CardChecker.get_card_type(card_number)
        
        # Simulate various responses (in production, integrate with real gateway)
        responses = [
            {'status': 'APPROVED', 'reason': 'CVV Match', 'code': '1000'},
            {'status': 'DECLINED', 'reason': 'Insufficient Funds', 'code': '51'},
            {'status': 'DECLINED', 'reason': 'Invalid CVV', 'code': 'N7'},
            {'status': 'APPROVED', 'reason': 'Address Match', 'code': '1000'},
            {'status': 'DECLINED', 'reason': 'Card Expired', 'code': '54'},
            {'status': 'DECLINED', 'reason': 'Do Not Honor', 'code': '05'},
        ]
        
        # Simulate random response for testing
        # In production, you'd make actual API calls here
        result = random.choice(responses)
        result['card_type'] = card_type
        result['response_time'] = round(random.uniform(0.3, 1.5), 2)
        
        return result
    
    @staticmethod
    def format_check_result(card_info, check_result):
        """Format check result for display."""
        card_number = card_info['card_number']
        masked_card = f"{card_number[:4]}••••••••{card_number[-4:]}"
        
        status_emoji = '✅' if check_result['status'] == 'APPROVED' else '❌'
        
        result_text = f"""
{status_emoji} **CARD CHECK RESULT** {status_emoji}

💳 **Card:** {masked_card}
🏦 **Type:** {check_result.get('card_type', 'Unknown')}
📊 **Status:** {check_result['status']}
💬 **Response:** {check_result['reason']}
🔢 **Code:** {check_result.get('code', 'N/A')}
⏱ **Time:** {check_result.get('response_time', 0)}s

**Card Details:**
📅 Exp: {card_info.get('month', 'XX')}/{card_info.get('year', 'XXXX')}
🔐 CVV: {card_info.get('cvv', 'XXX')}
"""
        return result_text.strip()
