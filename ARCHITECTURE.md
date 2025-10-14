# 🏗️ BatmanWL Bot - Architecture

This document describes the technical architecture of the BatmanWL bot.

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Telegram Platform                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS/Long Polling
                     │
┌────────────────────▼────────────────────────────────────┐
│                     bot.py                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Telegram Bot Application                  │  │
│  │  - Command Handlers                               │  │
│  │  - Message Handlers                               │  │
│  │  - Callback Query Handlers                        │  │
│  │  - Decorators (@require_premium, @require_admin)  │  │
│  └──────────────────────────────────────────────────┘  │
└──────────┬──────────────────────────────────┬──────────┘
           │                                  │
           │                                  │
┌──────────▼──────────────┐      ┌───────────▼──────────┐
│      config.py          │      │     features.py      │
│  - Environment vars     │      │  - Image generation  │
│  - Bot token           │      │  - File conversion   │
│  - Owner/Admin IDs     │      │  - Search            │
│  - Database URL        │      │  - Translation       │
└─────────────────────────┘      │  - Weather           │
                                 │  - Calculator        │
                                 └──────────────────────┘
           │
           │
┌──────────▼──────────────────────────────────────────────┐
│                    database.py                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │              SQLAlchemy Models                      │ │
│  │  ┌─────────────┐         ┌──────────────┐         │ │
│  │  │    User     │         │  PremiumKey  │         │ │
│  │  │             │         │              │         │ │
│  │  │ - user_id   │         │ - key        │         │ │
│  │  │ - username  │         │ - duration   │         │ │
│  │  │ - is_premium│         │ - max_uses   │         │ │
│  │  │ - premium_  │         │ - current_   │         │ │
│  │  │   until     │         │   uses       │         │ │
│  │  └─────────────┘         │ - is_active  │         │ │
│  │                          └──────────────┘         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Database Functions                     │ │
│  │  - get_or_create_user()                            │ │
│  │  - generate_key()                                  │ │
│  │  - redeem_key()                                    │ │
│  │  - get_all_keys()                                  │ │
│  │  - deactivate_key()                                │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────┘
                           │
                           │
                ┌──────────▼──────────┐
                │   SQLite Database   │
                │   (batmanwl.db)     │
                │                     │
                │  - users table      │
                │  - premium_keys     │
                │    table            │
                └─────────────────────┘
```

## 🔐 Authentication & Authorization Flow

```
┌────────────┐
│   User     │
│  Message   │
└──────┬─────┘
       │
       ▼
┌─────────────────────────┐
│  Get or Create User     │
│  (database.py)          │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Check User Role        │
│  - is_owner()?          │
│  - is_admin()?          │
│  - is_premium_active()? │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Command Handler        │
│  - @require_admin       │
│  - @require_premium     │
│  - No decorator (free)  │
└──────┬──────────────────┘
       │
       ├──── Owner/Admin ────────┐
       │                          │
       ├──── Premium User ────────┤
       │                          │
       └──── Free User ───────────┤
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Execute        │
                         │  Command        │
                         └─────────────────┘
```

## 🔑 Key System Flow

### Key Generation (Admin)

```
Admin: /genkey 24 1
       │
       ▼
┌─────────────────────┐
│  Check is_admin()   │
└──────┬──────────────┘
       │ ✅ Admin
       ▼
┌─────────────────────┐
│  Generate secure    │
│  token (secrets)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Create PremiumKey  │
│  - key: random      │
│  - duration: 24h    │
│  - max_uses: 1      │
│  - is_active: true  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Save to database   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Return key to      │
│  admin              │
└─────────────────────┘
```

### Key Redemption (User)

```
User: /redeem KEY123
       │
       ▼
┌─────────────────────┐
│  Get key from DB    │
└──────┬──────────────┘
       │
       ├─── Not found ───────► Error: Key not found
       │
       ▼
┌─────────────────────┐
│  Check can_redeem() │
│  - is_active?       │
│  - not expired?     │
│  - uses available?  │
└──────┬──────────────┘
       │
       ├─── Invalid ─────────► Error: Key invalid
       │
       ▼ ✅ Valid
┌─────────────────────┐
│  Update User        │
│  - is_premium=true  │
│  - premium_until=   │
│    now + duration   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Update Key         │
│  - current_uses++   │
│  - deactivate if    │
│    max uses reached │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Success message    │
└─────────────────────┘
```

## 📦 Module Dependencies

```
bot.py
├── config.py
│   └── python-dotenv
├── database.py
│   ├── sqlalchemy
│   ├── config.py
│   └── secrets (stdlib)
└── features.py
    ├── re (stdlib)
    ├── requests (optional)
    ├── Pillow (optional)
    └── [other APIs]

test_bot.py
├── bot.py
├── config.py
├── database.py
└── features.py
```

## 🔄 Data Flow

### User Registration

```
New User Message
      │
      ▼
get_or_create_user()
      │
      ├─── User exists ──► Update last_active
      │                    Return user
      │
      └─── New user ─────► Create User record
                           Save to database
                           Return user
```

### Premium Access Check

```
Command Execution
      │
      ▼
@require_premium
      │
      ▼
Get user from database
      │
      ▼
is_admin() or is_owner()?
      │
      ├─── Yes ──────────► Allow access
      │
      └─── No ───────────► is_premium_active()?
                                │
                                ├─── Yes ──► Allow access
                                │
                                └─── No ───► Deny access
                                             Show message
```

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username VARCHAR,
    first_name VARCHAR,
    is_premium BOOLEAN DEFAULT FALSE,
    premium_until DATETIME,
    redeemed_key VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_active DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Premium Keys Table

```sql
CREATE TABLE premium_keys (
    id INTEGER PRIMARY KEY,
    key VARCHAR UNIQUE NOT NULL,
    duration_hours INTEGER NOT NULL,
    max_uses INTEGER DEFAULT 1,
    current_uses INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME
);
```

## 🎯 Key Design Decisions

### 1. **Session Management**
- Scoped sessions for thread safety
- Expunge objects after commit to avoid detached instance errors
- Proper cleanup with Session.remove()

### 2. **Role-Based Access**
- Three roles: Owner, Admin, Premium, Free
- Decorators for clean access control
- Owner and Admin bypass all restrictions

### 3. **Key System**
- Cryptographically secure tokens (secrets.token_urlsafe)
- Flexible duration and usage limits
- Automatic deactivation when limits reached
- Time-based expiration checked on redemption

### 4. **Modularity**
- Separate modules for concerns
- Easy to extend with new features
- Placeholder implementations for demo
- Clear interfaces for API integration

### 5. **Configuration**
- Environment variables for security
- No secrets in code
- Easy deployment configuration

## 🔌 Extension Points

To extend the bot:

1. **Add New Commands**: Create handler in bot.py, register in main()
2. **Add Premium Features**: Create function in features.py, add command with @require_premium
3. **Add Database Models**: Add class to database.py, create helper functions
4. **Add API Integrations**: Implement in features.py, add API keys to .env
5. **Custom Access Control**: Create new decorators like @require_admin

## 🚀 Deployment Considerations

- **Database**: SQLite for small deployments, PostgreSQL for production
- **Scaling**: Consider using webhooks instead of polling for high traffic
- **Monitoring**: Add logging and error tracking
- **Backups**: Regular database backups for user data
- **Rate Limiting**: Implement rate limiting for premium features

## 📈 Future Enhancements

- Payment integration for key purchases
- User dashboard/statistics
- Feature usage analytics
- Group chat support
- Webhook mode for better performance
- Redis caching for session data
- Admin web panel
- Scheduled tasks (key cleanup, reminder notifications)

---

For implementation details, see the source code in each module.
