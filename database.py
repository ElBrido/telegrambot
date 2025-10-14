"""
Database module for BatmanWL Bot
Manages users, roles, and premium access keys
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_name: str = "batmanwl.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table with enhanced fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'user',
                is_banned INTEGER DEFAULT 0,
                credits INTEGER DEFAULT 0,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Premium keys table with max uses support
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS premium_keys (
                key_code TEXT PRIMARY KEY,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activated_at TIMESTAMP,
                expires_at TIMESTAMP,
                is_active INTEGER DEFAULT 0,
                duration_hours INTEGER DEFAULT 720,
                max_uses INTEGER DEFAULT 1,
                current_uses INTEGER DEFAULT 0,
                created_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        """)

        # Card checks history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS card_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                card_number TEXT,
                status TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Admin logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                action TEXT,
                target_user_id INTEGER,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES users(user_id),
                FOREIGN KEY (target_user_id) REFERENCES users(user_id)
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None, role: str = "user"):
        """Add or update user in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update existing user
            cursor.execute("""
                UPDATE users SET username = ?, first_name = ?, last_name = ?, last_seen = datetime('now')
                WHERE user_id = ?
            """, (username, first_name, last_name, user_id))
        else:
            # Insert new user with default credits
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, role, credits)
                VALUES (?, ?, ?, ?, ?, 10)
            """, (user_id, username, first_name, last_name, role))
        
        conn.commit()
        conn.close()

    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None

    def get_user_role(self, user_id: int) -> str:
        """Get user role"""
        user = self.get_user(user_id)
        return user['role'] if user else 'user'

    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin or owner"""
        role = self.get_user_role(user_id)
        return role in ['admin', 'owner']

    def is_owner(self, user_id: int) -> bool:
        """Check if user is owner"""
        role = self.get_user_role(user_id)
        return role == 'owner'

    def create_premium_key(self, key_code: str) -> bool:
        """Create a new premium key"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO premium_keys (key_code)
                VALUES (?)
            """, (key_code,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def activate_premium_key(self, user_id: int, key_code: str, duration_days: int = 30) -> Tuple[bool, str]:
        """Activate premium key for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if key exists and is not activated
        cursor.execute("""
            SELECT * FROM premium_keys WHERE key_code = ?
        """, (key_code,))
        
        key = cursor.fetchone()
        
        if not key:
            conn.close()
            return False, "❌ Clave no válida"
        
        if key['is_active']:
            conn.close()
            return False, "❌ Esta clave ya ha sido utilizada"
        
        # Activate key
        now = datetime.now()
        expires_at = now + timedelta(days=duration_days)
        
        cursor.execute("""
            UPDATE premium_keys
            SET user_id = ?, activated_at = ?, expires_at = ?, is_active = 1
            WHERE key_code = ?
        """, (user_id, now, expires_at, key_code))
        
        conn.commit()
        conn.close()
        
        return True, f"✅ Clave activada! Premium hasta: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def has_premium(self, user_id: int) -> bool:
        """Check if user has active premium"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM premium_keys
            WHERE user_id = ? AND is_active = 1 AND expires_at > datetime('now')
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None

    def add_card_check(self, user_id: int, card_number: str, status: str):
        """Log a card check"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO card_checks (user_id, card_number, status)
            VALUES (?, ?, ?)
        """, (user_id, card_number, status))
        
        conn.commit()
        conn.close()

    def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) as total_checks
            FROM card_checks
            WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {'total_checks': result['total_checks'] if result else 0}
    
    # Enhanced admin features
    def ban_user(self, user_id: int, admin_id: int):
        """Ban a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET is_banned = 1 WHERE user_id = ?
        """, (user_id,))
        
        # Log action
        cursor.execute("""
            INSERT INTO admin_logs (admin_id, action, target_user_id, details)
            VALUES (?, 'BAN', ?, 'User banned')
        """, (admin_id, user_id))
        
        conn.commit()
        conn.close()
    
    def unban_user(self, user_id: int, admin_id: int):
        """Unban a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET is_banned = 0 WHERE user_id = ?
        """, (user_id,))
        
        # Log action
        cursor.execute("""
            INSERT INTO admin_logs (admin_id, action, target_user_id, details)
            VALUES (?, 'UNBAN', ?, 'User unbanned')
        """, (admin_id, user_id))
        
        conn.commit()
        conn.close()
    
    def add_credits(self, user_id: int, credits: int, admin_id: int):
        """Add credits to user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET credits = credits + ? WHERE user_id = ?
        """, (credits, user_id))
        
        # Log action
        cursor.execute("""
            INSERT INTO admin_logs (admin_id, action, target_user_id, details)
            VALUES (?, 'ADD_CREDITS', ?, ?)
        """, (admin_id, user_id, f"Added {credits} credits"))
        
        conn.commit()
        conn.close()
    
    def use_credit(self, user_id: int):
        """Use one credit"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET credits = MAX(0, credits - 1) WHERE user_id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def update_last_seen(self, user_id: int):
        """Update user's last seen timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET last_seen = datetime('now') WHERE user_id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> dict:
        """Get global statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        cursor.execute("SELECT COUNT(*) as total_checks FROM card_checks")
        total_checks = cursor.fetchone()['total_checks']
        
        cursor.execute("SELECT COUNT(*) as banned_users FROM users WHERE is_banned = 1")
        banned_users = cursor.fetchone()['banned_users']
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_checks': total_checks,
            'banned_users': banned_users
        }
    
    def get_all_users_count(self) -> int:
        """Get total number of users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] if result else 0
