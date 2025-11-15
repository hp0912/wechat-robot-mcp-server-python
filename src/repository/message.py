"""
Message repository for database operations
"""

from typing import List, Optional, Dict, Any, cast
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from ..model.message import Message


class TextMessageItem:
    """文本消息项"""
    
    def __init__(self, nickname: str, message: str, created_at: int):
        self.nickname = nickname
        self.message = message
        self.created_at = created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "nickname": self.nickname,
            "message": self.message,
            "created_at": self.created_at
        }


class MessageRepository:
    """消息仓库"""
    
    def __init__(self, db: Session):
        """
        初始化消息仓库
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_messages_by_time_range(
        self,
        self_wxid: str,
        chat_room_id: str,
        start_time: int,
        end_time: int
    ) -> List[TextMessageItem]:
        """
        根据时间范围获取消息列表
        
        Args:
            self_wxid: 自己的微信ID
            chat_room_id: 群聊ID
            start_time: 开始时间戳
            end_time: 结束时间戳
            
        Returns:
            消息列表
        """
        # APP消息类型
        app_msg_list = ['57', '4', '5', '6']
        
        # 构建查询
        # 由于 SQLAlchemy 不支持 MySQL 的 EXTRACTVALUE，我们需要在 Python 中处理 XML
        query = self.db.query(Message).filter(
            and_(
                Message.from_wxid == chat_room_id,
                or_(
                    Message.type == 1,  # 文本消息
                    and_(
                        Message.type == 49,  # APP消息
                        # 这里我们先查出来，再在 Python 中过滤
                    )
                ),
                Message.sender_wxid != self_wxid,
                Message.created_at >= start_time,
                Message.created_at < end_time
            )
        ).order_by(Message.created_at.asc())
        
        messages = query.all()
        
        # 处理结果
        result = []
        for msg in messages:
            # 获取发送者昵称（需要联表查询 chat_room_members）
            # 这里简化处理，直接使用 sender_wxid
            # 实际应该联表查询 chat_room_members 获取 remark 或 nickname
            nickname = str(msg.sender_wxid or "")
            
            # 处理消息内容
            message_content = self._extract_message_content(msg, app_msg_list)
            
            if message_content is not None:
                result.append(TextMessageItem(
                    nickname=nickname,
                    message=message_content,
                    created_at=cast(int, msg.created_at) if msg.created_at is not None else 0
                ))
        
        return result
    
    def _extract_message_content(self, msg: Message, app_msg_list: List[str]) -> Optional[str]:
        """
        提取消息内容
        
        Args:
            msg: 消息对象
            app_msg_list: APP消息类型列表
            
        Returns:
            消息内容，如果不符合条件返回 None
        """
        msg_type = cast(int, msg.type) if msg.type is not None else 0
        
        # 文本消息
        if msg_type == 1:
            return str(msg.content or "")
        
        # APP消息
        if msg_type == 49:
            try:
                content = str(msg.content or "")
                if not content:
                    return None
                    
                # 解析 XML
                root = etree.fromstring(content.encode('utf-8'))
                
                # 获取 appmsg/type
                appmsg_type_elem = root.find('.//appmsg/type')
                if appmsg_type_elem is None:
                    return None
                
                appmsg_type = appmsg_type_elem.text
                
                # 检查是否在允许的类型列表中
                if appmsg_type not in app_msg_list:
                    return None
                
                # 根据类型提取内容
                if appmsg_type == '57':  # 引用消息
                    title_elem = root.find('.//appmsg/title')
                    return title_elem.text if title_elem is not None else ""
                
                elif appmsg_type == '5' or appmsg_type == '4':  # 网页分享消息
                    title_elem = root.find('.//appmsg/title')
                    des_elem = root.find('.//appmsg/des')
                    title = title_elem.text if title_elem is not None else ""
                    des = des_elem.text if des_elem is not None else ""
                    return f"网页分享消息，标题: {title}，描述：{des}"
                
                elif appmsg_type == '6':  # 文件消息
                    title_elem = root.find('.//appmsg/title')
                    title = title_elem.text if title_elem is not None else ""
                    return f"文件消息，文件名: {title}"
                
                else:
                    des_elem = root.find('.//appmsg/des')
                    return des_elem.text if des_elem is not None else ""
                    
            except Exception:
                # XML 解析失败，返回原始内容
                return str(msg.content or "")
        
        return None
