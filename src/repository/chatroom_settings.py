"""
ChatRoom settings repository for database operations
"""

from typing import Optional
from sqlalchemy.orm import Session

from ..model.chatroom_settings import ChatRoomSettings


class ChatRoomSettingsRepository:
    """群聊设置仓库"""
    
    def __init__(self, db: Session):
        """
        初始化群聊设置仓库
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_chatroom_settings(self, chat_room_id: str) -> Optional[ChatRoomSettings]:
        """
        根据群聊ID获取群聊设置
        
        Args:
            chat_room_id: 群聊ID
            
        Returns:
            群聊设置对象，如果不存在返回 None
        """
        return self.db.query(ChatRoomSettings).filter(
            ChatRoomSettings.chat_room_id == chat_room_id
        ).first()
