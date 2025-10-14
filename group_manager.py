"""Group management module for Telegram bot."""
from telegram import ChatMemberAdministrator, ChatMemberOwner


class GroupManager:
    """Manage group settings and features."""
    
    # Store group settings (in production, use database)
    group_settings = {}
    
    @staticmethod
    async def is_group_admin(update, context, user_id):
        """Check if user is group admin."""
        chat = update.effective_chat
        if chat.type in ['private']:
            return False
        
        try:
            member = await context.bot.get_chat_member(chat.id, user_id)
            return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))
        except:
            return False
    
    @staticmethod
    def set_welcome_message(chat_id, message):
        """Set welcome message for a group."""
        if chat_id not in GroupManager.group_settings:
            GroupManager.group_settings[chat_id] = {}
        GroupManager.group_settings[chat_id]['welcome_message'] = message
    
    @staticmethod
    def get_welcome_message(chat_id):
        """Get welcome message for a group."""
        if chat_id in GroupManager.group_settings:
            return GroupManager.group_settings[chat_id].get('welcome_message')
        return None
    
    @staticmethod
    def set_rules(chat_id, rules):
        """Set rules for a group."""
        if chat_id not in GroupManager.group_settings:
            GroupManager.group_settings[chat_id] = {}
        GroupManager.group_settings[chat_id]['rules'] = rules
    
    @staticmethod
    def get_rules(chat_id):
        """Get rules for a group."""
        if chat_id in GroupManager.group_settings:
            return GroupManager.group_settings[chat_id].get('rules')
        return None
