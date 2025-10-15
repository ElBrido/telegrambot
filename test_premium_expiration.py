"""Test premium expiration"""
import os
import time
from database import Database
from datetime import datetime, timedelta

# Create test database
test_db = "test_expiration.db"
if os.path.exists(test_db):
    os.remove(test_db)

db = Database(test_db)

# Add test user
db.add_user(12345, "testuser", "Test", "User")

# Create and activate a key with 1 minute duration (0.0167 hours)
import secrets
key_code = secrets.token_urlsafe(32)
db.create_premium_key(key_code, duration_hours=0.0167)  # 1 minute

# Activate the key
success, msg = db.activate_premium_key(12345, key_code)
print(f"Key activation: {msg}")

# Check premium status immediately
has_premium = db.has_premium(12345)
print(f"Premium status immediately after activation: {has_premium}")

# Check the expiration time
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute("SELECT expires_at FROM premium_keys WHERE user_id = ?", (12345,))
result = cursor.fetchone()
expires_at = result['expires_at']
print(f"Expires at: {expires_at}")
print(f"Current time: {datetime.now()}")
conn.close()

# Wait 65 seconds
print("Waiting 65 seconds...")
time.sleep(65)

# Check premium status after 1 minute
has_premium_after = db.has_premium(12345)
print(f"Premium status after 65 seconds: {has_premium_after}")

# Check database directly
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute("SELECT expires_at, datetime('now') as now FROM premium_keys WHERE user_id = ?", (12345,))
result = cursor.fetchone()
print(f"Expires at: {result['expires_at']}, Current DB time: {result['now']}")
print(f"Comparison: expires_at > now = {result['expires_at'] > result['now']}")
conn.close()

# Cleanup
os.remove(test_db)
print("\n✅ Test completed!")
