"""
Group manager module for Telegram group management
"""

from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes


class GroupManager:
    # In-memory storage for group settings (in production, use database)
    _group_settings = {}
    
    @staticmethod
    def set_welcome_message(chat_id: int, message: str):
        """Set welcome message for a group.
        
        Args:
            chat_id: Telegram chat ID
            message: Welcome message text
        """
        if chat_id not in GroupManager._group_settings:
            GroupManager._group_settings[chat_id] = {}
        GroupManager._group_settings[chat_id]['welcome'] = message
    
    @staticmethod
    def get_welcome_message(chat_id: int) -> Optional[str]:
        """Get welcome message for a group.
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            Welcome message or None
        """
        if chat_id in GroupManager._group_settings:
            return GroupManager._group_settings[chat_id].get('welcome')
        return None
    
    @staticmethod
    def set_rules(chat_id: int, rules: str):
        """Set rules for a group.
        
        Args:
            chat_id: Telegram chat ID
            rules: Group rules text
        """
        if chat_id not in GroupManager._group_settings:
            GroupManager._group_settings[chat_id] = {}
        GroupManager._group_settings[chat_id]['rules'] = rules
    
    @staticmethod
    def get_rules(chat_id: int) -> Optional[str]:
        """Get rules for a group.
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            Group rules or None
        """
        if chat_id in GroupManager._group_settings:
            return GroupManager._group_settings[chat_id].get('rules')
        return None
    
    @staticmethod
    async def is_group_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
        """Check if user is admin in the group.
        
        Args:
            update: Telegram update
            context: Bot context
            user_id: User ID to check
            
        Returns:
            True if user is admin, False otherwise
        """
        try:
            chat = update.effective_chat
            member = await context.bot.get_chat_member(chat.id, user_id)
            return member.status in ['creator', 'administrator']
        except Exception:
            return False
