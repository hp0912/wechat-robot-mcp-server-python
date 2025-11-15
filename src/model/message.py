from enum import IntEnum
from sqlalchemy import Column, BigInteger, String, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class MessageType(IntEnum):
    """PC微信所有的官方消息类型"""
    TEXT = 1              # 文本消息
    IMAGE = 3             # 图片消息
    VOICE = 34            # 语音消息
    VERIFY = 37           # 认证消息
    POSSIBLE_FRIEND = 40  # 好友推荐消息
    SHARE_CARD = 42       # 名片消息
    VIDEO = 43            # 视频消息
    EMOTICON = 47         # 表情消息
    LOCATION = 48         # 地理位置消息
    APP = 49              # APP消息
    VOIP = 50             # VOIP消息
    INIT = 51             # 微信初始化消息
    VOIP_NOTIFY = 52      # VOIP结束消息
    VOIP_INVITE = 53      # VOIP邀请
    MICRO_VIDEO = 62      # 小视频消息
    UNKNOW = 9999         # 未知消息
    PROMPT = 10000        # 系统消息
    SYSTEM = 10002        # 消息撤回


class AppMessageType(IntEnum):
    """PC微信所有的官方App消息类型"""
    TEXT = 1                      # 文本消息
    IMG = 2                       # 图片消息
    AUDIO = 3                     # 语音消息
    VIDEO = 4                     # 视频消息
    URL = 5                       # 文章消息
    ATTACH = 6                    # 附件消息
    OPEN = 7                      # Open
    EMOJI = 8                     # 表情消息
    VOICE_REMIND = 9              # VoiceRemind
    SCAN_GOOD = 10                # ScanGood
    GOOD = 13                     # Good
    EMOTION = 15                  # Emotion
    CARD_TICKET = 16              # 名片消息
    REALTIME_SHARE_LOCATION = 17  # 地理位置消息
    QUOTE = 57                    # 引用消息
    ATTACH_UPLOADING = 74         # 附件上传中
    TRANSFERS = 2000              # 转账消息
    RED_ENVELOPES = 2001          # 红包消息
    READER_TYPE = 100001          # 自定义的消息


class Message(Base):
    """消息模型"""
    __tablename__ = "messages"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    msg_id = Column(BigInteger, index=True, comment="消息Id")
    client_msg_id = Column(BigInteger, index=True, comment="客户端消息Id")
    is_chat_room = Column(Boolean, default=False, comment="消息是否来自群聊")
    is_at_me = Column(Boolean, default=False, comment="消息是否艾特我")
    is_ai_context = Column(Boolean, default=False, comment="消息是否是AI上下文")
    is_recalled = Column(Boolean, default=False, comment="消息是否已经撤回")
    type = Column(BigInteger, nullable=False, comment="消息类型")
    app_msg_type = Column(BigInteger, nullable=False, comment="消息子类型")
    content = Column(String(4000), default="", comment="内容")
    display_full_content = Column(String(4000), default="", comment="显示的完整内容")
    message_source = Column(String(1000), default="", comment="消息源")
    from_wxid = Column(String(64), default="", comment="消息来源")
    sender_wxid = Column(String(64), default="", comment="消息发送者")
    reply_wxid = Column(String(64), default="", comment="AI回复的人")
    to_wxid = Column(String(64), default="", comment="接收者")
    attachment_url = Column(String(255), default="", comment="文件地址")
    created_at = Column(BigInteger, nullable=False, comment="创建时间")
    updated_at = Column(BigInteger, nullable=False, comment="更新时间")


class MessageSchema(BaseModel):
    """消息Pydantic模型"""
    id: int
    msg_id: int = Field(..., description="消息Id")
    client_msg_id: int = Field(..., description="客户端消息Id")
    is_chat_room: bool = Field(False, description="消息是否来自群聊")
    is_at_me: bool = Field(False, description="消息是否艾特我")
    is_ai_context: bool = Field(False, description="消息是否是AI上下文")
    is_recalled: bool = Field(False, description="消息是否已经撤回")
    type: MessageType = Field(..., description="消息类型")
    app_msg_type: AppMessageType = Field(..., description="消息子类型")
    content: str = Field("", description="内容")
    display_full_content: str = Field("", description="显示的完整内容")
    message_source: str = Field("", description="消息源")
    from_wxid: str = Field("", description="消息来源")
    sender_wxid: str = Field("", description="消息发送者")
    reply_wxid: str = Field("", description="AI回复的人")
    to_wxid: str = Field("", description="接收者")
    attachment_url: str = Field("", description="文件地址")
    created_at: int = Field(..., description="创建时间")
    updated_at: int = Field(..., description="更新时间")
    # 额外字段，通过联表查询填充
    sender_nickname: str = Field("", description="发送者昵称")
    sender_avatar: str = Field("", description="发送者头像")
    
    class Config:
        from_attributes = True
