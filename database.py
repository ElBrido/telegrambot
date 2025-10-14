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

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                role TEXT DEFAULT 'user',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Premium keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS premium_keys (
                key_code TEXT PRIMARY KEY,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activated_at TIMESTAMP,
                expires_at TIMESTAMP,
                is_active INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
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

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def add_user(self, user_id: int, username: str = None, role: str = "user"):
        """Add or update user in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, username, role)
            VALUES (?, ?, ?)
        """, (user_id, username, role))
        
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
