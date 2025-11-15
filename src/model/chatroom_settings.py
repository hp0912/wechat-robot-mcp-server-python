from typing import Optional, Dict, Any
from sqlalchemy import Column, BigInteger, String, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from .global_settings import WelcomeType, PatType, NewsType, ImageModel

Base = declarative_base()


class ChatRoomSettings(Base):
    """群聊设置模型"""
    __tablename__ = "chat_room_settings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="公共配置表主键ID")
    chat_room_id = Column(String(64), default="", comment="群聊ID")
    chat_ai_enabled = Column(Boolean, nullable=True, comment="是否启用AI聊天功能")
    chat_ai_trigger = Column(String(20), nullable=True, comment="触发聊天AI的关键词")
    chat_base_url = Column(String(255), nullable=True, comment="聊天AI的基础URL地址")
    chat_api_key = Column(String(255), nullable=True, comment="聊天AI的API密钥")
    workflow_model = Column(String(100), nullable=True, comment="聊天AI使用的模型名称")
    chat_model = Column(String(100), nullable=True, comment="聊天AI使用的模型名称")
    image_recognition_model = Column(String(100), nullable=True, comment="图像识别AI使用的模型名称")
    chat_prompt = Column(Text, nullable=True, comment="聊天AI系统提示词")
    max_completion_tokens = Column(BigInteger, nullable=True, comment="最大回复")
    image_ai_enabled = Column(Boolean, nullable=True, comment="是否启用AI绘图功能")
    image_model = Column(String(255), nullable=True, comment="绘图AI模型")
    image_ai_settings = Column(JSON, comment="绘图AI配置项")
    tts_enabled = Column(Boolean, nullable=True, comment="是否启用AI文本转语音功能")
    tts_settings = Column(JSON, comment="文本转语音配置项")
    ltts_settings = Column(JSON, comment="长文本转语音配置项")
    pat_enabled = Column(Boolean, nullable=True, comment="是否启用拍一拍功能")
    pat_type = Column(String(10), default="text", comment="拍一拍方式：text-文本，voice-语音")
    pat_text = Column(String(255), default="", comment="拍一拍的文本")
    pat_voice_timbre = Column(String(255), default="", comment="拍一拍的音色")
    welcome_enabled = Column(Boolean, nullable=True, comment="是否启用新成员加群欢迎功能")
    welcome_type = Column(String(10), default="text", comment="欢迎方式：text-文本，emoji-表情，image-图片，url-链接")
    welcome_text = Column(String(255), default="", comment="欢迎新成员的文本")
    welcome_emoji_md5 = Column(String(64), default="", comment="欢迎新成员的表情MD5")
    welcome_emoji_len = Column(BigInteger, default=0, comment="欢迎新成员的表情MD5长度")
    welcome_image_url = Column(String(255), default="", comment="欢迎新成员的图片URL")
    welcome_url = Column(String(255), default="", comment="欢迎新成员的URL")
    leave_chat_room_alert_enabled = Column(Boolean, nullable=True, comment="是否启用离开群聊提醒功能")
    leave_chat_room_alert_text = Column(String(255), default="", comment="离开群聊提醒文本")
    chat_room_ranking_enabled = Column(Boolean, nullable=True, comment="是否启用群聊排行榜功能")
    chat_room_summary_enabled = Column(Boolean, nullable=True, comment="是否启用聊天记录总结功能")
    chat_room_summary_model = Column(String(100), nullable=True, comment="聊天总结使用的AI模型名称")
    news_enabled = Column(Boolean, nullable=True, comment="是否启用每日早报功能")
    news_type = Column(String(10), nullable=True, comment="是否启用每日早报功能")
    morning_enabled = Column(Boolean, nullable=True, comment="是否启用早安问候功能")


class ChatRoomSettingsSchema(BaseModel):
    """群聊设置Pydantic模型"""
    id: int = Field(..., description="公共配置表主键ID")
    chat_room_id: str = Field("", description="群聊ID")
    chat_ai_enabled: Optional[bool] = Field(None, description="是否启用AI聊天功能")
    chat_ai_trigger: Optional[str] = Field(None, description="触发聊天AI的关键词")
    chat_base_url: Optional[str] = Field(None, description="聊天AI的基础URL地址")
    chat_api_key: Optional[str] = Field(None, description="聊天AI的API密钥")
    workflow_model: Optional[str] = Field(None, description="聊天AI使用的模型名称")
    chat_model: Optional[str] = Field(None, description="聊天AI使用的模型名称")
    image_recognition_model: Optional[str] = Field(None, description="图像识别AI使用的模型名称")
    chat_prompt: Optional[str] = Field(None, description="聊天AI系统提示词")
    max_completion_tokens: Optional[int] = Field(None, description="最大回复")
    image_ai_enabled: Optional[bool] = Field(None, description="是否启用AI绘图功能")
    image_model: Optional[ImageModel] = Field(None, description="绘图AI模型")
    image_ai_settings: Optional[Dict[str, Any]] = Field(None, description="绘图AI配置项")
    tts_enabled: Optional[bool] = Field(None, description="是否启用AI文本转语音功能")
    tts_settings: Optional[Dict[str, Any]] = Field(None, description="文本转语音配置项")
    ltts_settings: Optional[Dict[str, Any]] = Field(None, description="长文本转语音配置项")
    pat_enabled: Optional[bool] = Field(None, description="是否启用拍一拍功能")
    pat_type: PatType = Field(PatType.TEXT, description="拍一拍方式")
    pat_text: str = Field("", description="拍一拍的文本")
    pat_voice_timbre: str = Field("", description="拍一拍的音色")
    welcome_enabled: Optional[bool] = Field(None, description="是否启用新成员加群欢迎功能")
    welcome_type: WelcomeType = Field(WelcomeType.TEXT, description="欢迎方式")
    welcome_text: str = Field("", description="欢迎新成员的文本")
    welcome_emoji_md5: str = Field("", description="欢迎新成员的表情MD5")
    welcome_emoji_len: int = Field(0, description="欢迎新成员的表情MD5长度")
    welcome_image_url: str = Field("", description="欢迎新成员的图片URL")
    welcome_url: str = Field("", description="欢迎新成员的URL")
    leave_chat_room_alert_enabled: Optional[bool] = Field(None, description="是否启用离开群聊提醒功能")
    leave_chat_room_alert_text: str = Field("", description="离开群聊提醒文本")
    chat_room_ranking_enabled: Optional[bool] = Field(None, description="是否启用群聊排行榜功能")
    chat_room_summary_enabled: Optional[bool] = Field(None, description="是否启用聊天记录总结功能")
    chat_room_summary_model: Optional[str] = Field(None, description="聊天总结使用的AI模型名称")
    news_enabled: Optional[bool] = Field(None, description="是否启用每日早报功能")
    news_type: Optional[NewsType] = Field(None, description="早报类型")
    morning_enabled: Optional[bool] = Field(None, description="是否启用早安问候功能")
    
    class Config:
        from_attributes = True
