"""
Global settings repository for database operations
"""

from typing import Optional
from sqlalchemy.orm import Session

from ..model.global_settings import GlobalSettings


class GlobalSettingsRepository:
    """全局设置仓库"""
    
    def __init__(self, db: Session):
        """
        初始化全局设置仓库
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_global_settings(self) -> Optional[GlobalSettings]:
        """
        获取全局设置
        
        Returns:
            全局设置对象，如果不存在返回 None
        """
        return self.db.query(GlobalSettings).first()
