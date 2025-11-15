"""
微信消息 Webhook 处理器
处理从微信接收的消息
"""
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class WeChatMessageResponse:
    """微信消息响应"""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result: Dict[str, Any] = {
            "code": self.code,
            "message": self.message
        }
        if self.data is not None:
            result["data"] = self.data
        return result


async def on_wechat_messages(request) -> Dict[str, Any]:
    """
    处理微信消息的处理器 - 支持 aiohttp 和 starlette
    
    Args:
        request: Request 对象
        
    Returns:
        Dict: 响应字典
    """
    # 检测是 starlette 还是 aiohttp 的 request
    try:
        from starlette.requests import Request as StarletteRequest
        is_starlette = isinstance(request, StarletteRequest)
    except ImportError:
        is_starlette = False
    
    # 只接受 POST 请求
    method = request.method if is_starlette else request.method
    if method != 'POST':
        return WeChatMessageResponse(
            code=405,
            message="method not allowed, only POST is supported"
        ).to_dict()
    
    # 读取请求体
    try:
        if is_starlette:
            body = await request.body()
        else:
            body = await request.read()
    except Exception as e:
        logger.error(f"Failed to read request body: {e}")
        return WeChatMessageResponse(
            code=400,
            message="failed to read request body"
        ).to_dict()
    
    # 检查请求体是否为空
    if not body or len(body) == 0:
        return WeChatMessageResponse(
            code=400,
            message="empty request body"
        ).to_dict()
    
    # 解析 JSON
    try:
        req = json.loads(body)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON body: {e}")
        return WeChatMessageResponse(
            code=400,
            message="invalid JSON body"
        ).to_dict()
    
    # TODO: 在这里继续处理解析后的 req（如入库、业务逻辑等）
    logger.info(f"Received WeChat message: {req}")
    
    # 返回成功响应
    return WeChatMessageResponse(
        code=200,
        message="ok"
    ).to_dict()
