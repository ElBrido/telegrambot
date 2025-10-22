# 🌐 Gateway System Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TELEGRAM BOT                            │
│                      (bot.py)                               │
└──────────────┬──────────────────────────────────────────────┘
               │
               │ User Commands
               │ /adyen, /bluepay, /stripe, etc.
               ▼
┌─────────────────────────────────────────────────────────────┐
│              COMMAND HANDLERS                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ _gateway_check() / _gateway_charge()                │   │
│  │ - Premium validation                                │   │
│  │ - Card parsing                                      │   │
│  │ - Gateway availability check                        │   │
│  └──────────────┬──────────────────────────────────────┘   │
└─────────────────┼──────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              GATEWAY MANAGER                                │
│              (payment_gateways.py)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  get_gateway(name)                                   │  │
│  │  is_gateway_available(name)                          │  │
│  │  get_online_gateways()                               │  │
│  └────────────┬─────────────────────────────────────────┘  │
└───────────────┼────────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬───────────┬──────────────┐
    │           │           │           │              │
    ▼           ▼           ▼           ▼              ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     ┌──────────┐
│ Adyen  │ │BluePay │ │Stripe  │ │Payeezy │ ... │CapSolver │
│  Auth  │ │  CCN   │ │  Auth  │ │Charged │     │ (Captcha)│
└────────┘ └────────┘ └────────┘ └────────┘     └──────────┘
    │           │           │           │              │
    │ API Call  │ API Call  │ API Call  │ API Call     │ API Call
    ▼           ▼           ▼           ▼              ▼
┌────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES                             │
│  Adyen API  BluePay API  Stripe API  Payeezy API  CapSolver│
└────────────────────────────────────────────────────────────┘
```

## Gateway Flow

```
User sends: /adyen 4532015112830366|12|25|123
                    │
                    ▼
            ┌───────────────┐
            │ Premium Check │
            └───────┬───────┘
                    │ ✓ Premium/Admin
                    ▼
            ┌───────────────┐
            │  Parse Card   │
            └───────┬───────┘
                    │ card_info = {card, month, year, cvv}
                    ▼
            ┌───────────────────┐
            │ Gateway Available?│
            └───────┬───────────┘
                    │ ✓ Configured
                    ▼
            ┌───────────────────┐
            │   AdyenAuth       │
            │  .check_card()    │
            └───────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    ✓ Success              ✗ Error
        │                       │
        ▼                       ▼
┌──────────────┐       ┌──────────────┐
│ GatewayResult│       │ GatewayResult│
│ status: LIVE │       │ status: ERROR│
│ is_live: true│       │ error: true  │
│ vbv: true    │       │ message: ... │
└──────┬───────┘       └──────┬───────┘
       │                      │
       └──────────┬───────────┘
                  ▼
          ┌──────────────┐
          │ Format       │
          │ Response     │
          └──────┬───────┘
                 ▼
          ┌──────────────┐
          │ Send to User │
          └──────────────┘
```

## Gateway Types

```
┌──────────────────────────────────────────────────────────────┐
│                   FREE GATEWAYS 🆓                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ BluePay  │  │  Exact   │  │  Sewin   │  │  PayPal  │   │
│  │   CCN    │  │   CCN    │  │   CCN    │  │  Basic   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  Purpose: Basic card number validation                      │
│  Access: All users                                           │
│  Features: CCN check, Luhn validation                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                 PREMIUM GATEWAYS 💎                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Adyen   │  │Braintree │  │  Chase   │                  │
│  │Auth + VBV│  │Auth+Fraud│  │   Full   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Payeezy  │  │ Payflow  │  │  Stripe  │                  │
│  │ Charged  │  │ Charged  │  │Auth + VBV│                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│                                                              │
│  Purpose: Authorization, VBV, Charge testing                 │
│  Access: Premium members + Admins                            │
│  Features: 3DS, fraud detection, real charges                │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              ADDITIONAL SERVICES 🤖                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              CapSolver                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │ reCAPTCHA  │  │  hCaptcha  │  │ FunCaptcha │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  Purpose: Automatic captcha solving                          │
│  Access: Premium                                             │
│  Type: Pay-per-use                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Data Models

```
┌──────────────────────────────────────┐
│        GatewayResult                 │
├──────────────────────────────────────┤
│ - status: str                        │
│ - message: str                       │
│ - gateway: str                       │
│ - is_live: bool                      │
│ - charged: bool                      │
│ - vbv_enabled: bool                  │
│ - error: bool                        │
│ - details: dict                      │
├──────────────────────────────────────┤
│ + to_dict() -> dict                  │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        BaseGateway                   │
├──────────────────────────────────────┤
│ - api_key: str                       │
│ - api_secret: str                    │
│ - test_mode: bool                    │
│ - gateway_name: str                  │
├──────────────────────────────────────┤
│ + is_configured() -> bool            │
│ + check_card(card_info) -> Result    │
│ + charge_card(card_info) -> Result   │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│      GatewayManager                  │
├──────────────────────────────────────┤
│ - gateways: dict                     │
│ - capsolver: CapSolver               │
├──────────────────────────────────────┤
│ + get_gateway(name) -> Gateway       │
│ + get_online_gateways() -> list      │
│ + is_gateway_available(name) -> bool │
└──────────────────────────────────────┘
```

## Configuration Structure

```
config.ini
│
├── [BOT]
│   ├── TOKEN
│   ├── ADMIN_IDS
│   └── OWNER_ID
│
├── [PAYMENT_GATEWAY]  (Legacy)
│   ├── GATEWAY_TYPE
│   ├── API_KEY
│   └── TEST_MODE
│
├── [ADYEN] 💎
│   ├── API_KEY
│   ├── API_SECRET
│   ├── MERCHANT_ACCOUNT
│   └── TEST_MODE
│
├── [BLUEPAY] 🆓
│   ├── ACCOUNT_ID
│   ├── SECRET_KEY
│   └── TEST_MODE
│
├── [BRAINTREE] 💎
│   ├── PUBLIC_KEY
│   ├── PRIVATE_KEY
│   ├── MERCHANT_ID
│   └── TEST_MODE
│
├── [EXACT] 🆓
│   ├── GATEWAY_ID
│   ├── PASSWORD
│   └── TEST_MODE
│
├── [CHASE] 💎
│   ├── MERCHANT_ID
│   ├── API_KEY
│   ├── API_SECRET
│   └── TEST_MODE
│
├── [PAYEEZY] 💎
│   ├── API_KEY
│   ├── API_SECRET
│   ├── MERCHANT_TOKEN
│   └── TEST_MODE
│
├── [PAYFLOW] 💎
│   ├── PARTNER
│   ├── VENDOR
│   ├── USER
│   ├── PASSWORD
│   └── TEST_MODE
│
├── [PAYPAL] 🆓/💎
│   ├── CLIENT_ID
│   ├── SECRET
│   └── TEST_MODE
│
├── [SEWIN] 🆓
│   ├── API_KEY
│   ├── API_SECRET
│   └── TEST_MODE
│
├── [STRIPE_AUTH] 🆓/💎
│   ├── API_KEY
│   ├── API_SECRET
│   └── TEST_MODE
│
└── [CAPSOLVER] 💎
    └── API_KEY
```

## Command Hierarchy

```
Gateway Commands
│
├── Information Commands
│   ├── /gatewayhelp - Show help
│   └── /gateways - Show status
│
├── FREE Commands (🆓 All Users)
│   ├── /bluepay - BluePay CCN
│   ├── /exact - Exact CCN
│   ├── /sewin - Sewin CCN
│   └── /paypalgateway - PayPal Basic
│
└── PREMIUM Commands (💎 Premium/Admin)
    ├── Authorization
    │   ├── /adyen - Adyen Auth + VBV
    │   ├── /braintree - Braintree Auth
    │   ├── /chase - Chase Full
    │   └── /stripegateway - Stripe Auth + VBV
    │
    └── Charge Testing
        ├── /payeezy - Payeezy $1 charge
        └── /payflow - Payflow $1 charge
```

## User Interface

```
Main Menu
│
├── ✅ Verificar Tarjeta (CCN)
├── 🔍 Buscar BIN
├── 💳 Generar Tarjetas (Premium)
├── 🔑 Activar Clave Premium
├── 📊 Mis Estadísticas
│
└── Admin Only
    ├── ⚙️ Panel Admin
    │   ├── Gestión de Claves
    │   ├── Gestión de Usuarios
    │   ├── Comunicación
    │   └── Estadísticas
    │
    └── 🌐 Gateways  ← NEW
        ├── Status Overview
        ├── Online/Offline Indicators
        ├── FREE vs PREMIUM Markers
        ├── Feature Descriptions
        └── Available Commands
```

## Response Examples

### Successful Check
```
┌────────────────────────────────┐
│ 🌐 STRIPE Check               │
├────────────────────────────────┤
│ 💳 Tarjeta: 4532****0366      │
│ 📅 Exp: 12/25                 │
│                                │
│ 📊 Resultado:                 │
│ Stripe: Card valid - VISA     │
│                                │
│ 🟢 LIVE                       │
│ 🔐 VBV: Enabled               │
└────────────────────────────────┘
```

### Charge Test
```
┌────────────────────────────────┐
│ 💰 PAYEEZY Charge Test        │
├────────────────────────────────┤
│ 💳 Tarjeta: 4532****0366      │
│ 📅 Exp: 12/25                 │
│ 💵 Monto: $1.00               │
│                                │
│ 📊 Resultado:                 │
│ Payeezy: Charged successfully │
│                                │
│ ✅ CHARGED                    │
│ 🟢 Card LIVE                  │
└────────────────────────────────┘
```

### Error Response
```
┌────────────────────────────────┐
│ 🌐 ADYEN Check                │
├────────────────────────────────┤
│ 💳 Tarjeta: 4532****0366      │
│ 📅 Exp: 12/25                 │
│                                │
│ 📊 Resultado:                 │
│ Adyen error: Invalid card     │
│                                │
│ 🔴 DEAD                       │
└────────────────────────────────┘
```

### Not Configured
```
┌────────────────────────────────┐
│ ❌ STRIPE no está configurado │
│ Contacta al administrador     │
└────────────────────────────────┘
```

### Premium Required
```
┌────────────────────────────────┐
│ ❌ ADYEN requiere Premium     │
│ Usa /redeem <clave> para      │
│ activar                       │
└────────────────────────────────┘
```

## Statistics

```
Implementation Statistics
├── Total Gateways: 10
├── FREE Gateways: 4
├── PREMIUM Gateways: 6
├── Additional Services: 1 (CapSolver)
├── Total Commands: 12
├── Lines of Code: ~2,500
├── Test Cases: 20
└── Documentation Files: 4
```

## Security Flow

```
API Keys Storage
     │
     ├── config.ini (NOT in git)
     │   └── .gitignore excludes it
     │
     ├── Environment Variables (Production)
     │   └── Recommended for deployment
     │
     └── Secure Configuration
         ├── Test mode for development
         ├── API key validation
         └── Error sanitization
```
