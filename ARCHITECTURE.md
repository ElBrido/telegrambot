# 🏗️ BatmanWL Bot - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM PLATFORM                        │
│                   (User Interface Layer)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Bot API Requests/Responses
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   BOT.PY (Main Engine)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Command Handlers                                   │   │
│  │  • /start, /menu, /help                            │   │
│  │  • /ccn, /bin, /gen                                │   │
│  │  • /key, /genkey, /stats                           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Message Handlers                                   │   │
│  │  • Callback queries (buttons)                       │   │
│  │  • .. commands (alternative syntax)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Business Logic                                      │   │
│  │  • Authentication & Authorization                    │   │
│  │  • Premium verification                              │   │
│  │  • Response formatting                               │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────┬────────────────────────────┬─────────────────┘
               │                            │
               │                            │
┌──────────────▼────────────┐   ┌──────────▼───────────────┐
│   DATABASE.PY             │   │   CARD_UTILS.PY          │
│   (Data Layer)            │   │   (Logic Layer)          │
├───────────────────────────┤   ├──────────────────────────┤
│ • User Management         │   │ • Luhn Validation        │
│ • Role System             │   │ • Card Generation        │
│ • Premium Keys            │   │ • BIN Lookup             │
│ • Card Check History      │   │ • CVV/Expiry Generation  │
│ • Statistics              │   │ • Formatting             │
└──────────────┬────────────┘   └──────────────────────────┘
               │
               │
┌──────────────▼────────────┐
│   BATMANWL.DB             │
│   (SQLite Database)       │
├───────────────────────────┤
│ • users                   │
│ • premium_keys            │
│ • card_checks             │
└───────────────────────────┘
```

## Component Breakdown

### 1. Telegram Platform Layer
- **Purpose**: User interaction interface
- **Technology**: Telegram Bot API
- **Features**:
  - Text messages
  - Inline keyboards
  - Animations (GIF)
  - Markdown formatting

### 2. Bot Engine (bot.py)

#### Command Handlers
```python
/start          → Welcome panel with GIF
/menu           → Main menu with buttons
/ccn <card>     → Verify card status
/bin <bin>      → Lookup BIN information
/gen <bin> [n]  → Generate cards (Premium)
/key <code>     → Activate premium
/genkey [n]     → Generate keys (Admin)
/stats          → User statistics
/help           → Help message
```

#### Alternative Syntax
All commands support `..` prefix:
```
..menu, ..ccn, ..bin, ..gen, etc.
```

#### Button Handlers
- CCN Check button → Instructions
- BIN Lookup button → Instructions
- Generate Cards button → Instructions (or permission check)
- Activate Key button → Instructions
- Stats button → Show statistics
- Admin Panel button → Admin commands
- Help button → Help message

### 3. Database Module (database.py)

#### Class: Database

**Methods:**
```python
__init__(db_name)                    # Initialize database
init_database()                      # Create tables
add_user(user_id, username, role)    # Add/update user
get_user(user_id)                    # Retrieve user
get_user_role(user_id)               # Get user role
is_admin(user_id)                    # Check admin status
is_owner(user_id)                    # Check owner status
create_premium_key(key_code)         # Create premium key
activate_premium_key(user_id, key)   # Activate key
has_premium(user_id)                 # Check premium status
add_card_check(user_id, card, status) # Log card check
get_user_stats(user_id)              # Get statistics
```

#### Database Tables

**users**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    role TEXT DEFAULT 'user',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**premium_keys**
```sql
CREATE TABLE premium_keys (
    key_code TEXT PRIMARY KEY,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activated_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_active INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

**card_checks**
```sql
CREATE TABLE card_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    card_number TEXT,
    status TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

### 4. Card Utilities Module (card_utils.py)

#### Class: CardUtils

**Static Methods:**
```python
luhn_checksum(card_number)              # Calculate Luhn checksum
validate_card(card_number)              # Validate using Luhn
generate_card_number(bin, length)       # Generate valid card
generate_multiple_cards(bin, count)     # Generate multiple cards
get_bin_info(bin_number)                # Lookup BIN information
format_card_number(card_number)         # Format with spaces
check_card_status(card_number)          # Simulate card check
generate_random_cvv()                   # Generate CVV
generate_random_expiry()                # Generate expiry date
```

**BIN Database** (Simplified):
```python
BIN_DATABASE = {
    "4": {"type": "VISA", "network": "Visa"},
    "5": {"type": "MASTERCARD", "network": "Mastercard"},
    "3": {"type": "AMEX", "network": "American Express"},
    "6": {"type": "DISCOVER", "network": "Discover"},
}
```

## Data Flow Diagrams

### User Registration Flow
```
User sends /start
       ↓
Bot checks if user exists
       ↓
    No │ Yes
       ↓      ↓
   Register  Retrieve
   new user  existing user
       ↓      ↓
       └──────┘
          ↓
   Show welcome panel
          ↓
   Display menu based on role
```

### Card Verification Flow
```
User sends /ccn 4532015112830366
       ↓
Bot extracts card number
       ↓
CardUtils.validate_card()
       ↓
    Valid? ───No──→ Return "Invalid card"
       │
      Yes
       ↓
CardUtils.check_card_status()
       ↓
Random status: ACTIVE/INACTIVE/DECLINED
       ↓
Database.add_card_check()
       ↓
Format response with status
       ↓
Send to user
```

### Card Generation Flow
```
User sends /gen 453201 10
       ↓
Check if user has premium/admin
       ↓
    No │ Yes
       ↓      ↓
   Deny    Continue
   access     ↓
          Extract BIN and count
              ↓
          Limit count to 50
              ↓
      CardUtils.generate_multiple_cards()
              ↓
          For each card:
          • Generate valid number (Luhn)
          • Generate random CVV
          • Generate random expiry
              ↓
          Format with backticks
              ↓
          Send to user
```

### Premium Key Activation Flow
```
User sends /key ABC123XYZ
       ↓
Extract key code
       ↓
Database.activate_premium_key()
       ↓
Check if key exists
       ↓
    No │ Yes
       ↓      ↓
  Invalid  Check if
   key     already used
              ↓
           No │ Yes
              ↓      ↓
          Activate  Already
          key       used
              ↓
     Set expiry (30 days)
              ↓
     Update database
              ↓
     Send success message
```

### Admin Key Generation Flow
```
Admin sends /genkey 5
       ↓
Check if user is admin
       ↓
    No │ Yes
       ↓      ↓
   Deny   Continue
   access    ↓
        For each key (max 20):
             ↓
        Generate secure token
        (secrets.token_urlsafe)
             ↓
        Database.create_premium_key()
             ↓
        Format with backticks
             ↓
        Send keys to admin
```

## Security Architecture

### Access Control Layers

```
┌─────────────────────────────────────┐
│         Owner Level                 │
│  • All admin permissions            │
│  • System configuration             │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│         Admin Level                 │
│  • Generate premium keys            │
│  • Access all features              │
│  • View all commands                │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│       Premium User Level            │
│  • Generate cards                   │
│  • All basic features               │
│  • Time-limited access              │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│       Regular User Level            │
│  • Card verification                │
│  • BIN lookup                       │
│  • View statistics                  │
└─────────────────────────────────────┘
```

### Permission Matrix

| Feature | User | Premium | Admin | Owner |
|---------|------|---------|-------|-------|
| Card Verification | ✅ | ✅ | ✅ | ✅ |
| BIN Lookup | ✅ | ✅ | ✅ | ✅ |
| Statistics | ✅ | ✅ | ✅ | ✅ |
| Card Generation | ❌ | ✅ | ✅ | ✅ |
| Generate Keys | ❌ | ❌ | ✅ | ✅ |
| System Config | ❌ | ❌ | ❌ | ✅ |

## Configuration Architecture

### Config File Structure
```ini
[BOT]
TOKEN = <telegram_bot_token>
ADMIN_IDS = <comma_separated_ids>
OWNER_ID = <owner_user_id>

[WELCOME]
GIF_URL = <welcome_gif_url>
MESSAGE = <welcome_message>

[PREMIUM]
KEY_DURATION_DAYS = <days>

[DATABASE]
DB_NAME = <database_filename>
```

### Environment Setup
```
1. Virtual Environment (venv/)
   ├── Python interpreter
   ├── Installed packages
   └── Isolated dependencies

2. Configuration (config.ini)
   ├── Bot credentials
   ├── Admin settings
   └── Feature settings

3. Database (batmanwl.db)
   ├── User data
   ├── Premium keys
   └── History logs

4. Application Files
   ├── bot.py
   ├── database.py
   └── card_utils.py
```

## Deployment Architecture

### Development Environment
```
Developer Machine
├── Clone repository
├── Create config.ini
├── Run install.sh
├── Run start.sh
└── Bot runs locally
```

### Production Environment
```
Server (VPS/Cloud)
├── Clone repository
├── Configure firewall
├── Create config.ini
├── Setup systemd service (optional)
├── Run install.sh
├── Run start.sh
└── Bot runs 24/7
```

### Scaling Considerations

**Single Instance** (Current Implementation)
- Handles 100-1000 users
- Single database file
- Single process

**Future Scaling Options**
- Multiple bot instances
- Shared database server
- Load balancing
- Redis caching
- Queue system for heavy operations

## Error Handling Architecture

### Error Levels

```
┌─────────────────────────────────────┐
│     User Input Validation           │
│  • Invalid card format              │
│  • Missing parameters               │
│  • Out of range values              │
└────────────────┬────────────────────┘
                 │ Handle gracefully
                 ↓
┌─────────────────────────────────────┐
│     Business Logic Errors           │
│  • Permission denied                │
│  • Premium expired                  │
│  • Invalid key code                 │
└────────────────┬────────────────────┘
                 │ Log and notify user
                 ↓
┌─────────────────────────────────────┐
│     System Errors                   │
│  • Database errors                  │
│  • API failures                     │
│  • Network issues                   │
└────────────────┬────────────────────┘
                 │ Log, notify admin
                 ↓
┌─────────────────────────────────────┐
│     Critical Errors                 │
│  • Bot crash                        │
│  • Configuration error              │
│  • Dependency missing               │
└─────────────────────────────────────┘
  Stop and require intervention
```

## Testing Architecture

### Test Coverage

```
test_bot.py
├── Unit Tests
│   ├── Card validation (Luhn algorithm)
│   ├── Card generation (valid cards)
│   ├── BIN lookup (database queries)
│   ├── Database operations (CRUD)
│   └── Card formatting (string manipulation)
│
├── Integration Tests
│   ├── Database + User operations
│   ├── Premium key system
│   └── Statistics calculation
│
└── Validation Tests
    ├── File existence
    ├── Python syntax
    ├── Script permissions
    └── Config structure
```

## Logging Architecture

### Log Levels
```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

**Log Categories:**
- `INFO`: Normal operations (bot start, user registration)
- `WARNING`: Unusual but handled (invalid input)
- `ERROR`: Errors that can be recovered (database timeout)
- `CRITICAL`: Errors requiring immediate attention (bot crash)

## Performance Architecture

### Optimization Strategies

1. **Database Indexing**
   - Primary keys on user_id
   - Index on premium_keys.user_id
   - Index on card_checks.user_id

2. **Caching** (Future)
   - User role cache
   - Premium status cache
   - BIN info cache

3. **Async Operations**
   - Telegram API calls are async
   - Database operations are sync (SQLite limitation)

4. **Rate Limiting** (Future)
   - Limit requests per user
   - Prevent spam
   - Protect resources

## Maintenance Architecture

### Regular Tasks
```
Daily:
  └── Monitor logs for errors

Weekly:
  ├── Check database size
  └── Review user statistics

Monthly:
  ├── Backup database
  ├── Update dependencies
  └── Review premium keys

Quarterly:
  ├── Security audit
  ├── Performance review
  └── Feature planning
```

## Summary

BatmanWL Bot uses a clean, modular architecture with:
- **Clear separation of concerns** (UI, Logic, Data)
- **Secure authentication** (role-based access)
- **Scalable design** (can grow with demand)
- **Maintainable code** (documented and tested)
- **User-friendly** (easy to deploy and use)

The architecture supports current requirements and allows for future enhancements without major refactoring.
