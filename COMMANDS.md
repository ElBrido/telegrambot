# 📋 Commands Reference

Complete list of all available bot commands. All commands support both `/` and `.` prefixes.

## 💳 Card Checking Commands

### /chk or .chk
**Check a single credit card**

**Usage:**
```
/chk <card>|<month>|<year>|<cvv>
.chk 4111111111111111|12|2025|123
```

**Features:**
- Validates using Luhn algorithm
- Identifies card type (VISA, Mastercard, etc.)
- Returns detailed check result
- Deducts 1 credit per check

---

### /mass or .mass
**Check multiple cards at once**

**Usage:**
```
/mass <cards separated by new lines or commas>
.mass 4111111111111111|12|2025|123,5500000000000004|01|2026|456
```

**Features:**
- Check up to 10 cards simultaneously
- Requires minimum 5 credits
- Shows summary of results
- Faster than individual checks

---

### /bin or .bin
**Get Bank Identification Number information**

**Usage:**
```
/bin <first_6_digits>
.bin 411111
```

**Features:**
- Shows card scheme (VISA, Mastercard, etc.)
- Displays card type (Credit, Debit, Prepaid)
- Shows issuing bank
- Displays country information
- Free to use (no credits required)

---

## 👤 User Commands

### /start or .start
**Show welcome panel and bot features**

**Usage:** `/start`

**Features:**
- Displays complete feature panel
- Shows your credit balance
- Interactive inline keyboard
- Lists all available commands

---

### /profile or .profile
**View your user profile**

**Usage:** `/profile`

**Shows:**
- User ID and username
- Account status (Free/Premium)
- Credit balance
- Total checks performed
- Success rate statistics
- Join date and last seen

---

### /stats or .stats
**View your checking statistics**

**Usage:** `/stats`

**Shows:**
- Total checks performed
- Approved cards count
- Declined cards count
- Success rate percentage

---

### /credits or .credits
**Check your credit balance**

**Usage:** `/credits`

**Shows:**
- Current credit balance
- Account status
- How to get more credits

---

### /help or .help
**Show help and commands guide**

**Usage:** `/help`

**Features:**
- Complete command list
- Usage examples
- Tips and tricks
- Support contact information

---

### /plans or .plans
**View premium subscription plans**

**Usage:** `/plans`

**Shows:**
- Available premium plans
- Pricing and features
- How to purchase
- Payment methods

---

### /status or .status
**Check bot status and statistics**

**Usage:** `/status`

**Shows:**
- Bot online status
- Version information
- Total users
- Total checks performed
- Last update time

---

### /info or .info
**Show bot information**

**Usage:** `/info`

**Shows:**
- Bot name and version
- Developer information
- Feature list
- Support channels
- Links to resources

---

## 👥 Group Commands

### /welcome
**Set custom welcome message for group (Admin Only)**

**Usage:**
```
/welcome <message>
/welcome Welcome to our group! Please check the rules.
```

**Requirements:**
- Must be used in a group
- User must be group admin
- Bot must have appropriate permissions

---

### /rules
**Show or set group rules**

**Usage:**
```
/rules                    # Show current rules
/rules <rules_text>       # Set rules (Admin only)
```

**Features:**
- Display group rules to all members
- Admins can update rules
- Supports markdown formatting

---

### /link
**Get group invite link (Admin Only)**

**Usage:** `/link`

**Requirements:**
- Must be used in a group
- User must be group admin
- Bot must have admin permissions

---

## 🔐 Admin Commands

### /broadcast or .broadcast
**Send message to all users**

**Usage:**
```
/broadcast <message>
.broadcast Important announcement: Bot maintenance tonight!
```

**Features:**
- Sends message to all registered users
- Admin only
- Shows confirmation before sending

---

### /ban or .ban
**Ban a user from using the bot**

**Usage:**
```
/ban <user_id>
.ban 123456789
```

**Features:**
- Prevents user from using bot
- Logged in admin logs
- Reversible with /unban

---

### /unban or .unban
**Remove ban from a user**

**Usage:**
```
/unban <user_id>
.unban 123456789
```

**Features:**
- Restores user access
- Logged in admin logs

---

### /addcredits or .addcredits
**Add credits to a user's account**

**Usage:**
```
/addcredits <user_id> <amount>
.addcredits 123456789 100
```

**Features:**
- Add any amount of credits
- Logged in admin logs
- Immediate effect

---

### /stats_admin or .stats_admin
**View global bot statistics**

**Usage:** `/stats_admin`

**Shows:**
- Total users
- Total checks performed
- Banned users count
- Active users count
- Timestamp of report

---

### /users or .users
**List all users**

**Usage:** `/users`

**Shows:**
- Total user count
- Quick admin action reference

---

### /logs or .logs
**View admin action logs**

**Usage:** `/logs`

**Shows:**
- Recent admin actions
- Action types
- Target users
- Timestamps

---

## 💡 Command Tips

### Using Both Prefixes
All commands work with both `/` and `.` prefixes:
```
/chk 4111111111111111|12|2025|123
.chk 4111111111111111|12|2025|123
```

### Batch Operations
Some commands support batch operations:
```
.mass card1|mm|yy|cvv
card2|mm|yy|cvv
card3|mm|yy|cvv
```

### Quick Access
Use the inline keyboard buttons in `/start` for quick access to common commands.

### Getting Help
- Use `/help` for general guidance
- Each command shows usage hints if called incorrectly
- Contact support for specific issues

---

## 📊 Command Categories Summary

| Category | Commands | Description |
|----------|----------|-------------|
| Card Checking | `/chk` `/mass` `/bin` | Card validation and checking |
| User | `/start` `/profile` `/stats` `/credits` `/help` | User account management |
| Information | `/plans` `/status` `/info` | Bot information and plans |
| Group | `/welcome` `/rules` `/link` | Group management |
| Admin | `/broadcast` `/ban` `/unban` `/addcredits` `/stats_admin` `/users` `/logs` | Bot administration |

---

## 🎯 Examples

### Basic Card Check
```
.chk 4111111111111111|12|2025|123
```

### Mass Check
```
.mass 4111111111111111|12|2025|123
5500000000000004|01|2026|456
3400000000000009|08|2027|1234
```

### BIN Lookup
```
.bin 411111
```

### Admin Operations
```
.ban 123456789
.addcredits 123456789 100
.broadcast New feature released!
```

---

Need more help? Use `/help` in the bot or contact support!
