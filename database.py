"""Database module for managing user data and bot state."""
import aiosqlite
import os
from datetime import datetime


class Database:
    def __init__(self, db_path='bot_database.db'):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database tables."""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_banned INTEGER DEFAULT 0,
                    is_premium INTEGER DEFAULT 0,
                    credits INTEGER DEFAULT 0,
                    joined_date TEXT,
                    last_seen TEXT
                )
            ''')
            
            # Card checks history
            await db.execute('''
                CREATE TABLE IF NOT EXISTS card_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    card_number TEXT,
                    status TEXT,
                    check_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Admin actions log
            await db.execute('''
                CREATE TABLE IF NOT EXISTS admin_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER,
                    action TEXT,
                    target_user_id INTEGER,
                    timestamp TEXT
                )
            ''')
            
            await db.commit()
    
    async def add_user(self, user_id, username=None, first_name=None, last_name=None):
        """Add a new user to the database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, joined_date, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, datetime.now().isoformat(), datetime.now().isoformat()))
            await db.commit()
    
    async def update_last_seen(self, user_id):
        """Update user's last seen timestamp."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE users SET last_seen = ? WHERE user_id = ?
            ''', (datetime.now().isoformat(), user_id))
            await db.commit()
    
    async def get_user(self, user_id):
        """Get user information."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return await cursor.fetchone()
    
    async def ban_user(self, user_id, admin_id):
        """Ban a user."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
            await db.execute('''
                INSERT INTO admin_logs (admin_id, action, target_user_id, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (admin_id, 'BAN', user_id, datetime.now().isoformat()))
            await db.commit()
    
    async def unban_user(self, user_id, admin_id):
        """Unban a user."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
            await db.execute('''
                INSERT INTO admin_logs (admin_id, action, target_user_id, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (admin_id, 'UNBAN', user_id, datetime.now().isoformat()))
            await db.commit()
    
    async def add_credits(self, user_id, credits, admin_id=None):
        """Add credits to a user."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (credits, user_id))
            if admin_id:
                await db.execute('''
                    INSERT INTO admin_logs (admin_id, action, target_user_id, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (admin_id, f'ADD_CREDITS_{credits}', user_id, datetime.now().isoformat()))
            await db.commit()
    
    async def use_credit(self, user_id):
        """Use one credit from user."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT credits FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            if row and row[0] > 0:
                await db.execute('UPDATE users SET credits = credits - 1 WHERE user_id = ?', (user_id,))
                await db.commit()
                return True
            return False
    
    async def log_card_check(self, user_id, card_number, status):
        """Log a card check."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO card_checks (user_id, card_number, status, check_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, card_number[-4:], status, datetime.now().isoformat()))  # Only store last 4 digits
            await db.commit()
    
    async def get_user_stats(self, user_id):
        """Get user statistics."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT COUNT(*) FROM card_checks WHERE user_id = ?
            ''', (user_id,))
            total_checks = (await cursor.fetchone())[0]
            
            cursor = await db.execute('''
                SELECT COUNT(*) FROM card_checks WHERE user_id = ? AND status = 'APPROVED'
            ''', (user_id,))
            approved_checks = (await cursor.fetchone())[0]
            
            return {
                'total_checks': total_checks,
                'approved_checks': approved_checks
            }
    
    async def get_all_users_count(self):
        """Get total number of users."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT COUNT(*) FROM users')
            return (await cursor.fetchone())[0]
    
    async def get_stats(self):
        """Get global statistics."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT COUNT(*) FROM users')
            total_users = (await cursor.fetchone())[0]
            
            cursor = await db.execute('SELECT COUNT(*) FROM card_checks')
            total_checks = (await cursor.fetchone())[0]
            
            cursor = await db.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
            banned_users = (await cursor.fetchone())[0]
            
            return {
                'total_users': total_users,
                'total_checks': total_checks,
                'banned_users': banned_users
            }
