# 📱 BatmanWL Bot - Example Interactions

This document shows example interactions with the BatmanWL bot to help you understand how it works.

## 🎬 Getting Started

### First Interaction - User Starts Bot

**User:** `/start`

**Bot:**
```
🦇 Welcome to 𝑩𝒂𝒕𝒎𝒂𝒏𝑾𝑳|Bot! 🦇

I'm your advanced Telegram bot with premium features.

📋 Free Commands:
/start - Start the bot
/help - Show this help message
/status - Check your premium status
/weather <city> - Get weather information
/calc <expression> - Calculate math expressions

⭐ Premium Commands:
/genimage <prompt> - Generate AI images
/convert <format> - Convert files to different formats
/search <query> - Advanced web search
/translate <lang> <text> - Translate text

🔑 Key Management:
/redeem <key> - Redeem a premium key

👑 Admin Commands:
/genkey <hours> <uses> - Generate premium keys
/listkeys - List all premium keys
/deactivate <key> - Deactivate a key
/stats - View bot statistics

Use /help for more information!

[Buttons: 📊 My Status | ❓ Help]
```

## 👤 Regular User Journey

### Checking Status (Free User)

**User:** `/status`

**Bot:**
```
👤 User Status

Name: John Doe
Username: @johndoe
User ID: 555555555

🆓 Role: Free User
❌ Premium: Not Active

Use /redeem <key> to activate premium!
```

### Trying Premium Feature Without Key

**User:** `/genimage a beautiful sunset`

**Bot:**
```
⚠️ This feature is premium only!

Use /redeem <key> to activate premium access.
Contact an admin to get a premium key.
```

### Using Free Feature

**User:** `/calc 25 * 4 + 10`

**Bot:**
```
🔢 Calculator

25*4+10 = 110
```

**User:** `/weather New York`

**Bot:**
```
🌤 Weather Information

City: New York

⚠️ This is a demo feature. To enable actual weather data:
1. Get API access to OpenWeatherMap or similar
2. Add the API key to your .env file
3. Implement the integration in features.py

Current weather conditions would be displayed here!
```

### Redeeming a Premium Key

**User:** `/redeem ABC123XYZ789`

**Bot:**
```
✅ Key redeemed successfully

🎉 Premium activated!
⏱ Valid until: 2025-10-15 18:30:00 UTC

Enjoy your premium features! 🦇
```

### Using Premium Features

**User:** `/genimage a futuristic cyberpunk city at night`

**Bot:**
```
🎨 Generating image for: a futuristic cyberpunk city at night...

🎨 Image Generation

Prompt: a futuristic cyberpunk city at night

⚠️ This is a demo feature. To enable actual image generation:
1. Get API access to an AI image service (DALL-E, Stable Diffusion, etc.)
2. Add the API key to your .env file
3. Implement the integration in features.py

The image would be generated and sent to you!
```

**User:** `/search best programming practices 2024`

**Bot:**
```
🔍 Searching for: best programming practices 2024...

🔍 Advanced Search Results

Query: best programming practices 2024

⚠️ This is a demo feature. To enable actual search:
1. Get API access to a search service (Google Custom Search, etc.)
2. Add the API key to your .env file
3. Implement the integration in features.py

Top results would be displayed here!
```

**User:** `/translate es Hello, how are you today?`

**Bot:**
```
🌐 Translation

Original: Hello, how are you today?
Target language: es

⚠️ This is a demo feature. To enable actual translation:
1. Get API access to a translation service
2. Add the API key to your .env file
3. Implement the integration in features.py

Translated text would appear here!
```

### Checking Status (Premium User)

**User:** `/status`

**Bot:**
```
👤 User Status

Name: John Doe
Username: @johndoe
User ID: 555555555

⭐ Role: Premium User
✅ Premium Active Until: 2025-10-15 18:30:00 UTC
⏱ Time Remaining: 23h 45m
```

## 👑 Admin/Owner Journey

### Owner Checking Status

**User (Owner):** `/status`

**Bot:**
```
👤 User Status

Name: Batman
Username: @batman
User ID: 123456789

👑 Role: Owner
✅ Access: All Features (Unlimited)
```

### Generating Keys

**Owner:** `/genkey 24 1`

**Bot:**
```
✅ Key generated successfully!

🔑 Key: Wjn1yJyfTg8qbqQUvUdE0A
⏱ Duration: 24 hours (1 days)
👥 Max uses: 1

Share this key with users to grant them premium access!
```

**Owner:** `/genkey 168 10`

**Bot:**
```
✅ Key generated successfully!

🔑 Key: Ct2Z2yGgACQv5inEctxLCw
⏱ Duration: 168 hours (7 days)
👥 Max uses: 10

Share this key with users to grant them premium access!
```

**Owner:** `/genkey 720 -1`

**Bot:**
```
✅ Key generated successfully!

🔑 Key: _cdnxOSS9gQ3bpkNHIc41w
⏱ Duration: 720 hours (30 days)
👥 Max uses: unlimited

Share this key with users to grant them premium access!
```

### Listing Keys

**Owner:** `/listkeys`

**Bot:**
```
🔑 Premium Keys

`Wjn1yJyfTg8qbqQUvUdE0A`
Status: ❌ Inactive | Uses: 1/1 | Duration: 24h

`Ct2Z2yGgACQv5inEctxLCw`
Status: ✅ Active | Uses: 3/10 | Duration: 168h

`_cdnxOSS9gQ3bpkNHIc41w`
Status: ✅ Active | Uses: 5/∞ | Duration: 720h

`AbCdEfGhIjKlMnOpQrStUv`
Status: ✅ Active | Uses: 0/1 | Duration: 24h
```

### Deactivating a Key

**Owner:** `/deactivate AbCdEfGhIjKlMnOpQrStUv`

**Bot:**
```
✅ Key `AbCdEfGhIjKlMnOpQrStUv` has been deactivated!
```

### Viewing Statistics

**Owner:** `/stats`

**Bot:**
```
📊 Bot Statistics

👥 Total Users: 47
⭐ Premium Users: 12
🔑 Total Keys: 15
✅ Active Keys: 8
```

### Using Features (Admin Bypass)

Even without an active premium key, admins and owners can use all features:

**Owner:** `/genimage a cosmic nebula`

**Bot:**
```
🎨 Generating image for: a cosmic nebula...

🎨 Image Generation

Prompt: a cosmic nebula

⚠️ This is a demo feature. To enable actual image generation:
[... feature response ...]
```

## 🚫 Error Scenarios

### Invalid Key Redemption

**User:** `/redeem INVALID_KEY`

**Bot:**
```
❌ Key not found
```

### Expired Key

**User:** `/redeem OLD_EXPIRED_KEY`

**Bot:**
```
❌ Key is no longer valid
```

### Command Without Arguments

**User:** `/genkey`

**Bot:**
```
❌ Usage: /genkey <hours> <max_uses>

Examples:
/genkey 24 1 - 24 hours, single use
/genkey 168 10 - 1 week, 10 uses
/genkey 720 -1 - 30 days, unlimited uses
```

**User:** `/calc`

**Bot:**
```
❌ Usage: /calc <expression>

Example: /calc 2 + 2 * 3
```

### Non-Admin Trying Admin Command

**Regular User:** `/genkey 24 1`

**Bot:**
```
⚠️ This command is for admins only!
```

### Invalid Calculator Expression

**User:** `/calc rm -rf /`

**Bot:**
```
❌ Invalid expression. Only use numbers and +, -, *, /, (, )
```

**User:** `/calc 10 / 0`

**Bot:**
```
❌ Error: Division by zero
```

## 💡 Pro Tips

1. **For Owners/Admins:**
   - Generate keys in batches for events
   - Use unlimited keys for VIP members
   - Use single-use keys for trials
   - Monitor statistics regularly

2. **For Users:**
   - Check your premium status before it expires
   - Redeem keys immediately to start using premium features
   - Report any issues to admins

3. **Key Best Practices:**
   - Short duration (24h) for trials
   - Medium duration (7 days) for regular users
   - Long duration (30+ days) for subscribers
   - Single-use for one-time access
   - Multi-use for groups or families
   - Unlimited use for permanent access

---

**Ready to start? Follow the [QUICKSTART.md](QUICKSTART.md) guide!** 🦇
