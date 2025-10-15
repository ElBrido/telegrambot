"""Test button handler code for syntax errors"""
import sys
try:
    from bot import BatmanWLBot
    print("✅ Bot module loads successfully")
    
    # Check if button_handler method exists
    bot = BatmanWLBot('config.example.ini')
    print("✅ Bot instantiates successfully")
    
    # Check if all methods exist
    methods = ['button_handler', 'charge_command', 'genkey_command', 'redeem_command']
    for method in methods:
        if hasattr(bot, method):
            print(f"✅ Method {method} exists")
        else:
            print(f"❌ Method {method} NOT found")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
