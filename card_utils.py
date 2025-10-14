"""
Card utilities module for BatmanWL Bot
Handles BIN lookup, card generation, and validation
"""

import random
import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CardUtils:
    
    # Common BIN information (simplified database)
    BIN_DATABASE = {
        "4": {"type": "VISA", "network": "Visa"},
        "5": {"type": "MASTERCARD", "network": "Mastercard"},
        "3": {"type": "AMEX", "network": "American Express"},
        "6": {"type": "DISCOVER", "network": "Discover"},
    }
    
    @staticmethod
    def luhn_checksum(card_number: str) -> int:
        """Calculate Luhn checksum for card number"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        
        return checksum % 10
    
    @staticmethod
    def validate_card(card_number: str) -> bool:
        """Validate card number using Luhn algorithm"""
        # Remove spaces and dashes
        card_number = re.sub(r'[\s-]', '', card_number)
        
        # Check if it's all digits
        if not card_number.isdigit():
            return False
        
        # Check length (13-19 digits)
        if len(card_number) < 13 or len(card_number) > 19:
            return False
        
        return CardUtils.luhn_checksum(card_number) == 0
    
    @staticmethod
    def generate_card_number(bin_prefix: str, length: int = 16) -> str:
        """Generate a valid card number with given BIN prefix"""
        # Ensure bin_prefix is valid
        if not bin_prefix.isdigit():
            return None
        
        # Generate random digits for the middle part
        remaining_length = length - len(bin_prefix) - 1  # -1 for checksum
        
        if remaining_length < 0:
            return None
        
        card_base = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
        
        # Calculate checksum digit
        checksum = CardUtils.luhn_checksum(card_base + '0')
        check_digit = (10 - checksum) % 10
        
        return card_base + str(check_digit)
    
    @staticmethod
    def generate_multiple_cards(bin_prefix: str, count: int = 10, length: int = 16) -> List[str]:
        """Generate multiple valid card numbers"""
        cards = []
        for _ in range(count):
            card = CardUtils.generate_card_number(bin_prefix, length)
            if card:
                cards.append(card)
        return cards
    
    @staticmethod
    def get_bin_info(bin_number: str) -> Dict[str, str]:
        """Get BIN information (simplified version)"""
        if not bin_number or len(bin_number) < 1:
            return {"error": "BIN inválido"}
        
        first_digit = bin_number[0]
        
        if first_digit in CardUtils.BIN_DATABASE:
            info = CardUtils.BIN_DATABASE[first_digit].copy()
            info["bin"] = bin_number
            
            # Add more details based on BIN
            if first_digit == "4":
                info["issuer"] = "Banco emisor VISA"
                info["country"] = "Internacional"
            elif first_digit == "5":
                info["issuer"] = "Banco emisor MASTERCARD"
                info["country"] = "Internacional"
            elif first_digit == "3":
                info["issuer"] = "American Express"
                info["country"] = "USA"
            elif first_digit == "6":
                info["issuer"] = "Discover"
                info["country"] = "USA"
            
            return info
        
        return {
            "bin": bin_number,
            "type": "UNKNOWN",
            "network": "Desconocida",
            "issuer": "Desconocido",
            "country": "Desconocido"
        }
    
    @staticmethod
    def format_card_number(card_number: str) -> str:
        """Format card number with spaces"""
        card_number = re.sub(r'[\s-]', '', card_number)
        return ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
    
    @staticmethod
    def check_card_status(card_number: str) -> Dict[str, str]:
        """
        Simulate card status check (CCN check)
        In a real implementation, this would call an actual API
        """
        if not CardUtils.validate_card(card_number):
            return {
                "status": "INVALID",
                "message": "❌ Tarjeta inválida (no pasa validación Luhn)",
                "card": card_number
            }
        
        # Simulate random status for demonstration
        statuses = [
            {"status": "ACTIVE", "message": "✅ Tarjeta ACTIVA", "color": "🟢"},
            {"status": "INACTIVE", "message": "❌ Tarjeta INACTIVA", "color": "🔴"},
            {"status": "DECLINED", "message": "⚠️ Tarjeta DECLINADA", "color": "🟡"},
        ]
        
        result = random.choice(statuses)
        result["card"] = CardUtils.format_card_number(card_number)
        
        return result
    
    @staticmethod
    def generate_random_cvv() -> str:
        """Generate random CVV"""
        return str(random.randint(100, 999))
    
    @staticmethod
    def generate_random_expiry() -> str:
        """Generate random expiry date"""
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(25, 30))
        return f"{month}/{year}"
