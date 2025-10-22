"""
Test payment gateway integrations
"""

import unittest
import configparser
from payment_gateways import (
    GatewayManager, AdyenAuth, BluePayCCN, BraintreeAuth,
    ExactCCN, ChasePaymentGateway, PayeezyCharged, PayflowCharged,
    PayPalGateway, SewinCCN, StripeAuth, CapSolver
)


class TestGatewayClasses(unittest.TestCase):
    """Test individual gateway classes"""
    
    def test_adyen_init(self):
        """Test Adyen gateway initialization"""
        gateway = AdyenAuth(test_mode=True)
        self.assertFalse(gateway.is_configured())  # No api_key
        
        gateway = AdyenAuth(api_key="test_key", api_secret="test_secret", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_bluepay_init(self):
        """Test BluePay gateway initialization"""
        gateway = BluePayCCN(api_key="test_id", api_secret="test_key", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_braintree_init(self):
        """Test Braintree gateway initialization"""
        gateway = BraintreeAuth(api_key="test_public", api_secret="test_private", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_exact_init(self):
        """Test Exact gateway initialization"""
        gateway = ExactCCN(api_key="test_gateway_id", api_secret="test_password", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_chase_init(self):
        """Test Chase gateway initialization"""
        gateway = ChasePaymentGateway(api_key="test_merchant_id", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_payeezy_init(self):
        """Test Payeezy gateway initialization"""
        gateway = PayeezyCharged(api_key="test_key", api_secret="test_secret", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_payflow_init(self):
        """Test Payflow gateway initialization"""
        gateway = PayflowCharged(api_key="test_partner", api_secret="test_vendor", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_paypal_init(self):
        """Test PayPal gateway initialization"""
        gateway = PayPalGateway(api_key="test_client_id", api_secret="test_secret", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_sewin_init(self):
        """Test Sewin gateway initialization"""
        gateway = SewinCCN(api_key="test_key", api_secret="test_secret", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_stripe_init(self):
        """Test Stripe gateway initialization"""
        gateway = StripeAuth(api_key="sk_test_xxxxx", test_mode=True)
        self.assertTrue(gateway.is_configured())
    
    def test_gateway_not_configured(self):
        """Test gateway without configuration"""
        gateway = AdyenAuth()
        self.assertFalse(gateway.is_configured())


class TestCapSolver(unittest.TestCase):
    """Test CapSolver integration"""
    
    def test_capsolver_init(self):
        """Test CapSolver initialization"""
        solver = CapSolver(api_key="test_key")
        self.assertTrue(solver.is_configured())
    
    def test_capsolver_not_configured(self):
        """Test CapSolver without API key"""
        solver = CapSolver()
        self.assertFalse(solver.is_configured())


class TestGatewayManager(unittest.TestCase):
    """Test GatewayManager"""
    
    def setUp(self):
        """Set up test config"""
        self.config = configparser.ConfigParser()
        
        # Add test gateway config
        self.config.add_section('STRIPE_AUTH')
        self.config.set('STRIPE_AUTH', 'API_KEY', 'sk_test_xxxxx')
        self.config.set('STRIPE_AUTH', 'TEST_MODE', 'true')
        
        self.config.add_section('BLUEPAY')
        self.config.set('BLUEPAY', 'ACCOUNT_ID', 'test_account')
        self.config.set('BLUEPAY', 'SECRET_KEY', 'test_secret')
        self.config.set('BLUEPAY', 'TEST_MODE', 'true')
        
        self.config.add_section('CAPSOLVER')
        self.config.set('CAPSOLVER', 'API_KEY', 'test_capsolver_key')
    
    def test_gateway_manager_init(self):
        """Test GatewayManager initialization"""
        manager = GatewayManager(self.config)
        self.assertIsNotNone(manager)
        self.assertIsInstance(manager.gateways, dict)
    
    def test_get_gateway(self):
        """Test getting a gateway"""
        manager = GatewayManager(self.config)
        
        # Should have stripe
        stripe = manager.get_gateway('stripe')
        self.assertIsNotNone(stripe)
        self.assertIsInstance(stripe, StripeAuth)
        
        # Should have bluepay
        bluepay = manager.get_gateway('bluepay')
        self.assertIsNotNone(bluepay)
        self.assertIsInstance(bluepay, BluePayCCN)
    
    def test_get_nonexistent_gateway(self):
        """Test getting a gateway that doesn't exist"""
        manager = GatewayManager(self.config)
        gateway = manager.get_gateway('nonexistent')
        self.assertIsNone(gateway)
    
    def test_get_online_gateways(self):
        """Test getting online gateways"""
        manager = GatewayManager(self.config)
        online = manager.get_online_gateways()
        
        self.assertIsInstance(online, list)
        self.assertGreater(len(online), 0)
        
        # Check structure
        for gw in online:
            self.assertIn('name', gw)
            self.assertIn('configured', gw)
            self.assertIn('class', gw)
    
    def test_is_gateway_available(self):
        """Test checking if gateway is available"""
        manager = GatewayManager(self.config)
        
        # Stripe should be available
        self.assertTrue(manager.is_gateway_available('stripe'))
        
        # BluePay should be available
        self.assertTrue(manager.is_gateway_available('bluepay'))
        
        # Adyen should not be available (not configured)
        self.assertFalse(manager.is_gateway_available('adyen'))
    
    def test_capsolver_initialization(self):
        """Test CapSolver initialization in manager"""
        manager = GatewayManager(self.config)
        
        self.assertIsNotNone(manager.capsolver)
        self.assertTrue(manager.capsolver.is_configured())


class TestGatewayResponses(unittest.TestCase):
    """Test gateway response handling"""
    
    def test_gateway_result_to_dict(self):
        """Test GatewayResult to_dict method"""
        from payment_gateways import GatewayResult
        
        result = GatewayResult(
            status='LIVE',
            message='Card is valid',
            gateway='stripe',
            is_live=True,
            charged=False,
            vbv_enabled=True,
            error=False
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['status'], 'LIVE')
        self.assertEqual(result_dict['message'], 'Card is valid')
        self.assertEqual(result_dict['gateway'], 'stripe')
        self.assertTrue(result_dict['is_live'])
        self.assertFalse(result_dict['charged'])
        self.assertTrue(result_dict['vbv_enabled'])
        self.assertFalse(result_dict['error'])


if __name__ == '__main__':
    unittest.main()
