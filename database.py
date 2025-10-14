"""Database models and functions for BatmanWL Bot."""
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import secrets
import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    """User model."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    redeemed_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    def is_premium_active(self):
        """Check if user has active premium."""
        if not self.is_premium:
            return False
        if self.premium_until and self.premium_until < datetime.utcnow():
            return False
        return True
    
    def is_admin(self):
        """Check if user is admin."""
        return self.user_id == config.OWNER_ID or self.user_id in config.ADMIN_IDS
    
    def is_owner(self):
        """Check if user is owner."""
        return self.user_id == config.OWNER_ID


class PremiumKey(Base):
    """Premium key model."""
    __tablename__ = 'premium_keys'
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    max_uses = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    def can_redeem(self):
        """Check if key can be redeemed."""
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        return True
    
    def redeem(self, user):
        """Redeem the key for a user."""
        if not self.can_redeem():
            return False
        
        # Update user premium status
        user.is_premium = True
        user.premium_until = datetime.utcnow() + timedelta(hours=self.duration_hours)
        user.redeemed_key = self.key
        
        # Update key usage
        self.current_uses += 1
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            self.is_active = False
        
        return True


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)


def get_or_create_user(user_id, username=None, first_name=None):
    """Get or create a user."""
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name
            )
            session.add(user)
            session.commit()
        else:
            # Update user info
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            user.last_active = datetime.utcnow()
            session.commit()
        session.refresh(user)
        # Make user object independent of session
        session.expunge(user)
        return user
    finally:
        Session.remove()


def generate_key(duration_hours, max_uses, created_by):
    """Generate a new premium key."""
    session = Session()
    try:
        key = secrets.token_urlsafe(16)
        premium_key = PremiumKey(
            key=key,
            duration_hours=duration_hours,
            max_uses=max_uses,
            created_by=created_by
        )
        session.add(premium_key)
        session.commit()
        session.refresh(premium_key)
        session.expunge(premium_key)
        return premium_key
    finally:
        Session.remove()


def get_key(key_str):
    """Get a premium key by its string."""
    session = Session()
    try:
        return session.query(PremiumKey).filter_by(key=key_str).first()
    finally:
        Session.remove()


def redeem_key(user_id, key_str):
    """Redeem a premium key."""
    session = Session()
    try:
        key = session.query(PremiumKey).filter_by(key=key_str).first()
        if not key:
            return None, "Key not found"
        
        if not key.can_redeem():
            return None, "Key is no longer valid"
        
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return None, "User not found"
        
        if key.redeem(user):
            session.commit()
            session.refresh(user)
            session.expunge(user)
            return user, "Key redeemed successfully"
        else:
            return None, "Failed to redeem key"
    finally:
        Session.remove()


def get_all_keys():
    """Get all premium keys."""
    session = Session()
    try:
        return session.query(PremiumKey).order_by(PremiumKey.created_at.desc()).all()
    finally:
        Session.remove()


def deactivate_key(key_str):
    """Deactivate a premium key."""
    session = Session()
    try:
        key = session.query(PremiumKey).filter_by(key=key_str).first()
        if key:
            key.is_active = False
            session.commit()
            return True
        return False
    finally:
        Session.remove()
