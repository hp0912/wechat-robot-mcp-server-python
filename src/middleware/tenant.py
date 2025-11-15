"""
Tenant Middleware - 租户中间件

用于从请求中解析机器人上下文并设置数据库连接
"""
import logging
from typing import Any, Callable, Awaitable, Dict
from mcp.types import CallToolRequest

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


class TenantMiddleware:
    """租户中间件 - 处理机器人上下文和数据库连接"""
    
    def __init__(self, handler: Callable):
        self.handler = handler
    
    async def __call__(self, request: Any) -> Any:
        """中间件处理函数"""
        # 检查是否是 CallToolRequest
        if isinstance(request, CallToolRequest):
            if hasattr(request, 'params') and hasattr(request.params, 'meta'):
                meta = getattr(request.params, 'meta', None)
                if meta:
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
        
        # 调用下一个处理器
        return await self.handler(request)


def create_tenant_middleware(
    next_handler: Callable[[Any], Awaitable[Any]]
) -> Callable[[Any], Awaitable[Any]]:
    """创建租户中间件（函数式风格）"""
    
    async def middleware(request: Any) -> Any:
        # 检查是否是 CallToolRequest
        if isinstance(request, CallToolRequest):
            if hasattr(request, 'params') and hasattr(request.params, 'meta'):
                meta = getattr(request.params, 'meta', None)
                if meta:
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
        
        # 调用下一个处理器
        return await next_handler(request)
    
    return middleware
