"""模型包初始化文件"""

from .base import BaseResponse
from .contact import Contact, ContactType, ContactSchema
from .message import Message, MessageType, AppMessageType, MessageSchema
from .global_settings import (
    GlobalSettings, 
    GlobalSettingsSchema,
    WelcomeType, 
    PatType, 
    NewsType, 
    ImageModel
)
from .chatroom_settings import ChatRoomSettings, ChatRoomSettingsSchema

__all__ = [
    # base
    "BaseResponse",
    
    # contact
    "Contact",
    "ContactType",
    "ContactSchema",
    
    # message
    "Message",
    "MessageType",
    "AppMessageType",
    "MessageSchema",
    
    # global_settings
    "GlobalSettings",
    "GlobalSettingsSchema",
    "WelcomeType",
    "PatType",
    "NewsType",
    "ImageModel",
    
    # chatroom_settings
    "ChatRoomSettings",
    "ChatRoomSettingsSchema",
]
