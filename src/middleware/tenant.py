"""
Tenant Middleware - 租户中间件

用于从请求中解析机器人上下文并设置数据库连接
"""
import logging
from typing import Any, Dict

from ..config import config
from ..robot_context import RobotContext, set_robot_context, set_db

logger = logging.getLogger(__name__)


def parse_robot_context(meta: Dict[str, Any]) -> RobotContext:
    """从 meta 数据解析机器人上下文"""
    try:
        # 字段名映射：从 Go 的 JSON tag 到 Python 的 snake_case
        field_map = {
            'WeChatClientPort': 'we_chat_client_port',
            'RobotID': 'robot_id',
            'RobotCode': 'robot_code',
            'RobotRedisDB': 'robot_redis_db',
            'RobotWxID': 'robot_wx_id',
            'FromWxID': 'from_wx_id',
            'SenderWxID': 'sender_wx_id',
            'MessageID': 'message_id',
            'RefMessageID': 'ref_message_id',
        }
        
        # 转换字段名
        kwargs = {}
        for go_name, py_name in field_map.items():
            if go_name in meta:
                kwargs[py_name] = meta[go_name]
        
        return RobotContext(**kwargs)
    except Exception as e:
        logger.error(f"解析 RobotContext 失败: {e}")
        return RobotContext()

def apply_tenant_from_meta(meta: Dict[str, Any]) -> None:
    """根据 MCP 请求中的 meta 设置机器人上下文和数据库连接"""
    if not meta:
        return

    # 解析机器人上下文
    rc = parse_robot_context(meta)
    set_robot_context(rc)

    # 如果有 RobotCode，设置数据库连接
    if rc.robot_code:
        try:
            db = config.get_db_by_robot_code(rc.robot_code)
            set_db(db)
        except Exception as e:
            logger.error(
                f"获取数据库连接失败(RobotCode:{rc.robot_code}): {e}"
            )
