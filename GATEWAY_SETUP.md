# 🌐 Payment Gateway Setup Guide

This guide explains how to configure and use the payment gateways in BatmanWL Bot.

## 📋 Table of Contents
- [Overview](#overview)
- [Gateway Types](#gateway-types)
- [Configuration](#configuration)
- [Gateway Details](#gateway-details)
- [CapSolver Setup](#capsolver-setup)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## Overview

BatmanWL Bot supports 10+ payment gateways for card validation, authorization, and charge testing. Gateways are categorized as:

- **🆓 FREE**: Available to all users for basic CCN validation
- **💎 PREMIUM**: Requires Premium membership for advanced features (Auth, VBV, Charge tests)

## Gateway Types

### 🆓 FREE Gateways

| Gateway | Command | Purpose | Features |
|---------|---------|---------|----------|
| **BluePay** | `/bluepay` | CCN Validation | Card number validation, AVS checking |
| **Exact** | `/exact` | CCN Check | Fast card number validation |
| **Sewin** | `/sewin` | CCN Validation | Fast CCN validation |
| **PayPal** | `/paypalgateway` | Basic Check | Global coverage, basic validation |

### 💎 PREMIUM Gateways

| Gateway | Command | Purpose | Features |
|---------|---------|---------|----------|
| **Adyen** | `/adyen` | Auth + VBV | Authorization, 3D Secure, global coverage |
| **Braintree** | `/braintree` | Auth + Fraud | PayPal-owned, fraud detection, strong 3DS |
| **Chase** | `/chase` | Full Check | Major bank processor, high trust score |
| **Payeezy** | `/payeezy` | Charge Test | Real charge capability ($1.00 test) |
| **Payflow** | `/payflow` | Charge Test | PayPal infrastructure charging |
| **Stripe** | `/stripegateway` | Auth + VBV | Industry standard, excellent 3DS support |

### 🤖 Additional Services

| Service | Purpose | Type |
|---------|---------|------|
| **CapSolver** | Captcha solving | PREMIUM |

## Configuration

### Basic Setup

1. **Copy example config:**
```bash
cp config.example.ini config.ini
```

2. **Edit `config.ini` and add your gateway credentials:**

### Example Configurations

#### Stripe Auth (Recommended for Beginners)

```ini
[STRIPE_AUTH]
API_KEY = sk_test_51xxxxx  # Get from https://dashboard.stripe.com
API_SECRET = 
TEST_MODE = true
```

**How to get Stripe API Key:**
1. Go to https://dashboard.stripe.com/register
2. Complete registration
3. Go to Developers → API keys
4. Copy the "Secret key" (starts with sk_test_ for test mode)

#### Adyen

```ini
[ADYEN]
API_KEY = your_api_key_here
API_SECRET = your_api_secret
MERCHANT_ACCOUNT = YourMerchantAccount
TEST_MODE = true
```

**How to get Adyen credentials:**
1. Sign up at https://www.adyen.com/
2. Go to Account → API credentials
3. Create new API credential
4. Copy API key and merchant account name

#### BluePay

```ini
[BLUEPAY]
ACCOUNT_ID = your_account_id
SECRET_KEY = your_secret_key
TEST_MODE = true
```

#### Braintree

```ini
[BRAINTREE]
PUBLIC_KEY = your_public_key
PRIVATE_KEY = your_private_key
MERCHANT_ID = your_merchant_id
TEST_MODE = true
```

**How to get Braintree credentials:**
1. Sign up at https://www.braintreepayments.com/
2. Go to Account → API
3. Copy Public Key, Private Key, and Merchant ID

#### Exact

```ini
[EXACT]
GATEWAY_ID = your_gateway_id
PASSWORD = your_password
TEST_MODE = true
```

#### Chase Paymentech

```ini
[CHASE]
MERCHANT_ID = your_merchant_id
API_KEY = your_api_key
API_SECRET = your_api_secret
TEST_MODE = true
```

#### Payeezy (First Data)

```ini
[PAYEEZY]
API_KEY = your_api_key
API_SECRET = your_api_secret
MERCHANT_TOKEN = your_merchant_token
TEST_MODE = true
```

**How to get Payeezy credentials:**
1. Sign up at https://developer.payeezy.com/
2. Create API credentials
3. Copy API Key, API Secret, and Merchant Token

#### PayPal Payflow

```ini
[PAYFLOW]
PARTNER = PayPal
VENDOR = your_vendor_login
USER = your_user_login
PASSWORD = your_password
TEST_MODE = true
```

#### PayPal Gateway

```ini
[PAYPAL]
CLIENT_ID = your_client_id
SECRET = your_secret
TEST_MODE = true
```

**How to get PayPal credentials:**
1. Go to https://developer.paypal.com/
2. Log in with your PayPal account
3. Go to Dashboard → My Apps & Credentials
4. Create a new app
5. Copy Client ID and Secret

#### Sewin Payment

```ini
[SEWIN]
API_KEY = your_api_key
API_SECRET = your_api_secret
TEST_MODE = true
```

## CapSolver Setup

CapSolver is used to automatically solve captchas that may appear during payment processing.

### Configuration

```ini
[CAPSOLVER]
API_KEY = CAP-xxxxxxxxxxxx
```

### Getting CapSolver API Key

1. Go to https://capsolver.com/
2. Sign up for an account
3. Go to Dashboard
4. Copy your API key
5. Add credits to your account (pay-per-use service)

### Supported Captcha Types

- reCAPTCHA v2
- reCAPTCHA v3
- hCaptcha
- FunCaptcha
- Image captchas

## Gateway Details

### Adyen Auth
**Type:** PREMIUM  
**Purpose:** Authorization and 3D Secure verification

**Features:**
- Global payment coverage (150+ currencies)
- Strong 3D Secure/VBV support
- Real-time authorization
- High success rates

**Best For:**
- International transactions
- High-security requirements
- 3D Secure verification

**Usage:**
```
/adyen 4532015112830366|12|25|123
```

---

### BluePay CCN
**Type:** FREE  
**Purpose:** Card number validation

**Features:**
- Basic CCN validation
- AVS (Address Verification System)
- Fast response times

**Best For:**
- Quick card validation
- Basic checking without charges

**Usage:**
```
/bluepay 4532015112830366|12|25|123
```

---

### Braintree Auth
**Type:** PREMIUM  
**Purpose:** Authorization with fraud detection

**Features:**
- PayPal owned and operated
- Advanced fraud detection
- Strong 3D Secure support
- Reliable infrastructure

**Best For:**
- Fraud prevention
- PayPal integration
- Trusted authorization

**Usage:**
```
/braintree 4532015112830366|12|25|123
```

---

### Exact CCN
**Type:** FREE  
**Purpose:** Fast card number validation

**Features:**
- Quick CCN check
- Basic card information
- Lightweight validation

**Best For:**
- Fast bulk checking
- Basic validation needs

**Usage:**
```
/exact 4532015112830366|12|25|123
```

---

### Chase Paymentech
**Type:** PREMIUM  
**Purpose:** Full card validation

**Features:**
- Major bank processor
- High trust score
- Complete validation
- Enterprise-grade

**Best For:**
- High-value transactions
- Bank-level validation
- Premium checking

**Usage:**
```
/chase 4532015112830366|12|25|123
```

---

### Payeezy Charged
**Type:** PREMIUM  
**Purpose:** Real charge testing

**Features:**
- Actual charge test ($1.00)
- First Data infrastructure
- Fraud detection
- Real-world validation

**Best For:**
- Testing actual charging capability
- Verifying card funds
- Real transaction simulation

**Usage:**
```
/payeezy 4532015112830366|12|25|123
```

**Note:** Tests with $1.00 charge

---

### Payflow Charged
**Type:** PREMIUM  
**Purpose:** Charge testing with PayPal

**Features:**
- PayPal infrastructure
- Real charge test ($1.00)
- Reliable processing
- High availability

**Best For:**
- PayPal ecosystem
- Reliable charge testing
- Production-grade validation

**Usage:**
```
/payflow 4532015112830366|12|25|123
```

**Note:** Tests with $1.00 charge

---

### PayPal Gateway
**Type:** FREE (basic) / PREMIUM (advanced)  
**Purpose:** Card validation

**Features:**
- Global coverage
- Buyer protection
- Trusted brand
- Multiple payment methods

**Best For:**
- International users
- Trusted validation
- General-purpose checking

**Usage:**
```
/paypalgateway 4532015112830366|12|25|123
```

---

### Sewin CCN
**Type:** FREE  
**Purpose:** Fast CCN validation

**Features:**
- Quick validation
- Card number check
- Lightweight

**Best For:**
- Fast checking
- Basic validation
- Bulk processing

**Usage:**
```
/sewin 4532015112830366|12|25|123
```

---

### Stripe Auth
**Type:** FREE (basic) / PREMIUM (VBV)  
**Purpose:** Authorization and 3D Secure

**Features:**
- Industry standard
- Excellent 3D Secure support
- Modern API
- Developer-friendly
- Great documentation

**Best For:**
- 3D Secure verification
- Modern applications
- Reliable authorization
- Recommended for most users

**Usage:**
```
/stripegateway 4532015112830366|12|25|123
```

**Recommended:** Best gateway for beginners due to excellent documentation and free tier

## Usage Examples

### Basic Card Check (Free)
```bash
# Check with BluePay
/bluepay 4532015112830366|12|25|123

# Check with Exact
/exact 4532015112830366|12|25|123

# Check with Sewin
/sewin 4532015112830366|12|25|123
```

### Advanced Authorization (Premium)
```bash
# Adyen Auth + VBV
/adyen 4532015112830366|12|25|123

# Stripe Auth
/stripegateway 4532015112830366|12|25|123

# Braintree Auth
/braintree 4532015112830366|12|25|123
```

### Charge Testing (Premium)
```bash
# Payeezy charge test
/payeezy 4532015112830366|12|25|123

# Payflow charge test
/payflow 4532015112830366|12|25|123
```

### Check Gateway Status
```bash
# View all gateways
/gateways

# View gateway help
/gatewayhelp

# View from admin panel
Click "🌐 Gateways" button in admin panel
```

## Response Format

All gateway commands return structured responses:

### Successful Check
```
🌐 STRIPE Check

💳 Tarjeta: 4532****0366
📅 Exp: 12/25

📊 Resultado:
Stripe: Card valid - VISA

🟢 LIVE
🔐 VBV: Enabled
```

### Failed Check
```
🌐 ADYEN Check

💳 Tarjeta: 4532****0366
📅 Exp: 12/25

📊 Resultado:
Adyen error: Invalid card number

🔴 DEAD
```

### Not Configured
```
❌ STRIPE no está configurado
Contacta al administrador
```

### Premium Required
```
❌ ADYEN requiere Premium
Usa /redeem <clave> para activar
```

## Troubleshooting

### Gateway Shows Offline

**Problem:** Gateway appears offline in `/gateways` command

**Solutions:**
1. Check `config.ini` has correct section name
2. Verify API keys are correct
3. Ensure `TEST_MODE = true` for testing
4. Check API key permissions in gateway dashboard

### API Key Errors

**Problem:** "Invalid API key" or similar errors

**Solutions:**
1. Double-check you copied the full API key
2. Verify you're using test keys when `TEST_MODE = true`
3. Check API key hasn't expired
4. Ensure API key has correct permissions

### Charge Commands Not Working

**Problem:** Charge tests fail or decline

**Solutions:**
1. Verify gateway supports test charges in test mode
2. Check merchant account has charge permissions
3. Use test card numbers from gateway documentation
4. Ensure sufficient balance for test charges

### CapSolver Not Working

**Problem:** Captchas not being solved

**Solutions:**
1. Verify CapSolver API key is correct
2. Check CapSolver account has credits
3. Ensure captcha type is supported
4. Check CapSolver service status

### Rate Limiting

**Problem:** "Too many requests" errors

**Solutions:**
1. Reduce check frequency
2. Upgrade to higher tier API plan
3. Implement delays between checks
4. Contact gateway support for rate limit increase

## Best Practices

### Security
- ✅ Always use test mode for development
- ✅ Never commit API keys to version control
- ✅ Use environment variables for sensitive data
- ✅ Rotate API keys regularly
- ✅ Monitor gateway usage

### Performance
- ✅ Use appropriate gateway for task (FREE for basic, PREMIUM for advanced)
- ✅ Implement caching for repeated checks
- ✅ Use batch processing when available
- ✅ Monitor response times

### Cost Optimization
- ✅ Use FREE gateways when possible
- ✅ Cache results to avoid duplicate checks
- ✅ Use test mode during development
- ✅ Monitor usage to avoid unexpected charges

## Support

### Gateway-Specific Support
- **Stripe:** https://support.stripe.com/
- **Adyen:** https://docs.adyen.com/
- **Braintree:** https://developers.braintreepayments.com/
- **PayPal:** https://developer.paypal.com/support/
- **Payeezy:** https://developer.payeezy.com/support
- **CapSolver:** https://docs.capsolver.com/

### Bot Support
- Check `/help` for bot commands
- Contact bot owner/admin
- See [README.md](README.md) for general help

## Additional Resources

- [COMMANDS.md](COMMANDS.md) - Complete command reference
- [README.md](README.md) - Bot setup guide
- [config.example.ini](config.example.ini) - Configuration examples
- [PAYMENT_GATEWAY_SETUP.md](PAYMENT_GATEWAY_SETUP.md) - Legacy gateway setup

## Updates and Maintenance

Gateways are regularly updated. Check for:
- API version updates
- New gateway additions
- Feature enhancements
- Security patches

Run `git pull` regularly to get the latest updates.

---

**Last Updated:** 2025-10-21  
**Version:** 2.0  
**Supported Gateways:** 10  
**Total Commands:** 12+ gateway commands
