from enum import Enum
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()


class ContactType(str, Enum):
    """联系人类型枚举"""
    FRIEND = "friend"
    CHAT_ROOM = "chat_room"
    OFFICIAL_ACCOUNT = "official_account"


class Contact(Base):
    """微信联系人模型，包括好友和群组"""
    __tablename__ = "contacts"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wechat_id = Column(String(64), nullable=False, index=True, comment="微信号")
    alias = Column(String(64), default="", comment="微信号别名")
    nickname = Column(String(64), nullable=True, comment="昵称")
    avatar = Column(String(255), default="", comment="头像")
    type = Column(String(20), nullable=False, comment="联系人类型")
    remark = Column(String(64), default="", comment="备注")
    pyinitial = Column(String(64), nullable=True, comment="昵称拼音首字母大写")
    quan_pin = Column(String(128), nullable=True, comment="昵称拼音全拼小写")
    sex = Column(Integer, default=0, comment="性别 0：未知 1：男 2：女")
    country = Column(String(64), default="", comment="国家")
    province = Column(String(64), default="", comment="省份")
    city = Column(String(64), default="", comment="城市")
    signature = Column(String(255), default="", comment="个性签名")
    sns_background = Column(String(255), nullable=True, comment="朋友圈背景图")
    chat_room_owner = Column(String(64), default="", comment="群主微信号")
    created_at = Column(BigInteger, nullable=False, comment="创建时间")
    last_active_at = Column(BigInteger, nullable=False, comment="最近活跃时间")
    updated_at = Column(BigInteger, nullable=False, comment="更新时间")
    deleted_at = Column(BigInteger, nullable=True, index=True, comment="删除时间")
    
    __table_args__ = (
        Index('idx_wechat_id_deleted', 'wechat_id', 'deleted_at', unique=True),
    )
    
    def is_chat_room(self) -> bool:
        """判断联系人是否为群组"""
        return str(self.type) == ContactType.CHAT_ROOM.value


class ContactSchema(BaseModel):
    """联系人Pydantic模型"""
    id: int
    wechat_id: str = Field(..., description="微信号")
    alias: str = Field(default="", description="微信号别名")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: str = Field(default="", description="头像")
    type: ContactType = Field(..., description="联系人类型")
    remark: str = Field(default="", description="备注")
    pyinitial: Optional[str] = Field(None, description="昵称拼音首字母大写")
    quan_pin: Optional[str] = Field(None, description="昵称拼音全拼小写")
    sex: int = Field(default=0, description="性别 0：未知 1：男 2：女")
    country: str = Field(default="", description="国家")
    province: str = Field(default="", description="省份")
    city: str = Field(default="", description="城市")
    signature: str = Field(default="", description="个性签名")
    sns_background: Optional[str] = Field(None, description="朋友圈背景图")
    chat_room_owner: str = Field(default="", description="群主微信号")
    created_at: int = Field(..., description="创建时间")
    last_active_at: int = Field(..., description="最近活跃时间")
    updated_at: int = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
