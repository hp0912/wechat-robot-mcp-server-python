"""
Robot Context Module - 机器人上下文管理

使用 contextvars 实现线程安全的上下文传递
"""
from contextvars import ContextVar
from typing import Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session


@dataclass
class RobotContext:
    """机器人上下文信息"""
    we_chat_client_port: str = ""
    robot_id: int = 0
    robot_code: str = ""
    robot_redis_db: int = 0
    robot_wx_id: str = ""
    from_wx_id: str = ""
    sender_wx_id: str = ""
    message_id: int = 0
    ref_message_id: int = 0


# 上下文变量
_robot_context_var: ContextVar[Optional[RobotContext]] = ContextVar(
    'robot_context', default=None
)
_db_var: ContextVar[Optional[Session]] = ContextVar(
    'robot_db', default=None
)


def set_robot_context(rc: RobotContext) -> None:
    """设置机器人上下文"""
    _robot_context_var.set(rc)


def get_robot_context() -> Optional[RobotContext]:
    """获取机器人上下文"""
    return _robot_context_var.get()


def set_db(db: Session) -> None:
    """设置数据库会话"""
    _db_var.set(db)


def get_db() -> Optional[Session]:
    """获取数据库会话"""
    return _db_var.get()


def get_sql_db():
    """
    获取底层 SQL 连接（用于健康检查等）
    返回 SQLAlchemy 的 Connection 对象
    """
    db = get_db()
    if db is None:
        return None
    
    try:
        return db.connection()
    except Exception:
        return None
