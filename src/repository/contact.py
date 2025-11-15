"""
Contact repository for database operations
"""

from typing import Optional
from sqlalchemy.orm import Session

from ..model.contact import Contact


class ContactRepository:
    """联系人仓库"""
    
    def __init__(self, db: Session):
        """
        初始化联系人仓库
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_contact_by_wechat_id(self, wechat_id: str) -> Optional[Contact]:
        """
        根据微信ID获取联系人
        
        Args:
            wechat_id: 微信ID
            
        Returns:
            联系人对象，如果不存在返回 None
        """
        return self.db.query(Contact).filter(
            Contact.wechat_id == wechat_id
        ).first()
