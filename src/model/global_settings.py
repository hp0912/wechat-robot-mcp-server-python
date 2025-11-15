from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, BigInteger, String, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class WelcomeType(str, Enum):
    """欢迎方式枚举"""
    TEXT = "text"    # 文本
    EMOJI = "emoji"  # 表情
    IMAGE = "image"  # 图片
    URL = "url"      # 链接


class PatType(str, Enum):
    """拍一拍方式枚举"""
    TEXT = "text"    # 文本
    VOICE = "voice"  # 语音


class NewsType(str, Enum):
    """早报类型枚举"""
    NONE = ""
    TEXT = "text"    # 文本
    IMAGE = "image"  # 图片


class ImageModel(str, Enum):
    """图像模型枚举"""
    DOUBAO = "doubao"                    # 豆包模型
    JIMENG = "jimeng"                    # 即梦模型
    GLM = "glm"                          # 智谱模型
    HUNYUAN = "hunyuan"                  # 腾讯混元模型
    STABLE_DIFFUSION = "stable-diffusion" # Stable Diffusion 模型
    MIDJOURNEY = "midjourney"            # Midjourney 模型
    OPENAI = "openai"                    # OpenAI 模型


class GlobalSettings(Base):
    """全局设置模型"""
    __tablename__ = "global_settings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="公共配置表主键ID")
    chat_ai_enabled = Column(Boolean, default=False, comment="是否启用AI聊天功能")
    chat_ai_trigger = Column(String(20), default="", comment="触发聊天AI的关键词")
    chat_base_url = Column(String(255), default="", comment="聊天AI的基础URL地址")
    chat_api_key = Column(String(255), default="", comment="聊天AI的API密钥")
    workflow_model = Column(String(100), default="", comment="聊天AI使用的模型名称")
    chat_model = Column(String(100), default="", comment="聊天AI使用的模型名称")
    image_recognition_model = Column(String(100), default="", comment="图像识别AI使用的模型名称")
    chat_prompt = Column(Text, comment="聊天AI系统提示词")
    max_completion_tokens = Column(BigInteger, default=0, comment="最大回复")
    image_ai_enabled = Column(Boolean, default=False, comment="是否启用AI绘图功能")
    image_model = Column(String(255), default="", comment="绘图AI模型")
    image_ai_settings = Column(JSON, comment="绘图AI配置项")
    tts_enabled = Column(Boolean, default=False, comment="是否启用AI文本转语音功能")
    tts_settings = Column(JSON, comment="文本转语音配置项")
    ltts_settings = Column(JSON, comment="长文本转语音配置项")
    pat_enabled = Column(Boolean, default=False, comment="是否启用拍一拍功能")
    pat_type = Column(String(10), default="text", comment="拍一拍方式：text-文本，voice-语音")
    pat_text = Column(String(255), default="", comment="拍一拍的文本")
    pat_voice_timbre = Column(String(255), default="", comment="拍一拍的音色")
    welcome_enabled = Column(Boolean, default=False, comment="是否启用新成员加群欢迎功能")
    welcome_type = Column(String(10), default="text", comment="欢迎方式：text-文本，emoji-表情，image-图片，url-链接")
    welcome_text = Column(String(255), default="", comment="欢迎新成员的文本")
    welcome_emoji_md5 = Column(String(64), default="", comment="欢迎新成员的表情MD5")
    welcome_emoji_len = Column(BigInteger, default=0, comment="欢迎新成员的表情MD5长度")
    welcome_image_url = Column(String(255), default="", comment="欢迎新成员的图片URL")
    welcome_url = Column(String(255), default="", comment="欢迎新成员的URL")
    leave_chat_room_alert_enabled = Column(Boolean, default=False, comment="是否启用离开群聊提醒功能")
    leave_chat_room_alert_text = Column(String(255), default="", comment="离开群聊提醒文本")
    chat_room_ranking_enabled = Column(Boolean, default=False, comment="是否启用群聊排行榜功能")
    chat_room_ranking_daily_cron = Column(String(255), default="", comment="每日定时任务表达式")
    chat_room_ranking_weekly_cron = Column(String(255), nullable=True, comment="每周定时任务表达式")
    chat_room_ranking_month_cron = Column(String(255), nullable=True, comment="每月定时任务表达式")
    chat_room_summary_enabled = Column(Boolean, default=False, comment="是否启用聊天记录总结功能")
    chat_room_summary_model = Column(String(100), default="", comment="聊天总结使用的AI模型名称")
    chat_room_summary_cron = Column(String(100), default="", comment="群聊总结的定时任务表达式")
    news_enabled = Column(Boolean, default=False, comment="是否启用每日早报功能")
    news_type = Column(String(10), default="text", comment="是否启用每日早报功能")
    news_cron = Column(String(100), default="", comment="每日早报的定时任务表达式")
    morning_enabled = Column(Boolean, default=False, comment="是否启用早安问候功能")
    morning_cron = Column(String(100), default="", comment="早安问候的定时任务表达式")
    friend_sync_cron = Column(String(100), default="", comment="好友同步的定时任务表达式")


class GlobalSettingsSchema(BaseModel):
    """全局设置Pydantic模型"""
    id: int = Field(..., description="公共配置表主键ID")
    chat_ai_enabled: Optional[bool] = Field(False, description="是否启用AI聊天功能")
    chat_ai_trigger: Optional[str] = Field("", description="触发聊天AI的关键词")
    chat_base_url: str = Field("", description="聊天AI的基础URL地址")
    chat_api_key: str = Field("", description="聊天AI的API密钥")
    workflow_model: str = Field("", description="聊天AI使用的模型名称")
    chat_model: str = Field("", description="聊天AI使用的模型名称")
    image_recognition_model: str = Field("", description="图像识别AI使用的模型名称")
    chat_prompt: str = Field("", description="聊天AI系统提示词")
    max_completion_tokens: Optional[int] = Field(0, description="最大回复")
    image_ai_enabled: Optional[bool] = Field(False, description="是否启用AI绘图功能")
    image_model: ImageModel = Field(ImageModel.DOUBAO, description="绘图AI模型")
    image_ai_settings: Optional[Dict[str, Any]] = Field(None, description="绘图AI配置项")
    tts_enabled: Optional[bool] = Field(False, description="是否启用AI文本转语音功能")
    tts_settings: Optional[Dict[str, Any]] = Field(None, description="文本转语音配置项")
    ltts_settings: Optional[Dict[str, Any]] = Field(None, description="长文本转语音配置项")
    pat_enabled: Optional[bool] = Field(False, description="是否启用拍一拍功能")
    pat_type: PatType = Field(PatType.TEXT, description="拍一拍方式：text-文本，voice-语音")
    pat_text: str = Field("", description="拍一拍的文本")
    pat_voice_timbre: str = Field("", description="拍一拍的音色")
    welcome_enabled: Optional[bool] = Field(False, description="是否启用新成员加群欢迎功能")
    welcome_type: WelcomeType = Field(WelcomeType.TEXT, description="欢迎方式")
    welcome_text: str = Field("", description="欢迎新成员的文本")
    welcome_emoji_md5: str = Field("", description="欢迎新成员的表情MD5")
    welcome_emoji_len: int = Field(0, description="欢迎新成员的表情MD5长度")
    welcome_image_url: str = Field("", description="欢迎新成员的图片URL")
    welcome_url: str = Field("", description="欢迎新成员的URL")
    leave_chat_room_alert_enabled: Optional[bool] = Field(False, description="是否启用离开群聊提醒功能")
    leave_chat_room_alert_text: str = Field("", description="离开群聊提醒文本")
    chat_room_ranking_enabled: Optional[bool] = Field(False, description="是否启用群聊排行榜功能")
    chat_room_ranking_daily_cron: str = Field("", description="每日定时任务表达式")
    chat_room_ranking_weekly_cron: Optional[str] = Field(None, description="每周定时任务表达式")
    chat_room_ranking_month_cron: Optional[str] = Field(None, description="每月定时任务表达式")
    chat_room_summary_enabled: Optional[bool] = Field(False, description="是否启用聊天记录总结功能")
    chat_room_summary_model: str = Field("", description="聊天总结使用的AI模型名称")
    chat_room_summary_cron: str = Field("", description="群聊总结的定时任务表达式")
    news_enabled: Optional[bool] = Field(False, description="是否启用每日早报功能")
    news_type: NewsType = Field(NewsType.TEXT, description="早报类型")
    news_cron: str = Field("", description="每日早报的定时任务表达式")
    morning_enabled: Optional[bool] = Field(False, description="是否启用早安问候功能")
    morning_cron: str = Field("", description="早安问候的定时任务表达式")
    friend_sync_cron: str = Field("", description="好友同步的定时任务表达式")
    
    class Config:
        from_attributes = True
