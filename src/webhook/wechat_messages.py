"""
微信消息 Webhook 处理器
处理从微信接收的消息
"""
import json
import logging
from typing import Any, Optional
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
from aiohttp import web

logger = logging.getLogger(__name__)


@dataclass
class WeChatMessageResponse:
    """微信消息响应"""
    code: int
    message: str
    data: Optional[Any] = None

    def to_dict(self):
        """转换为字典"""
        result = {
            "code": self.code,
            "message": self.message
        }
        if self.data is not None:
            result["data"] = self.data
        return result


class WeChatMessageHandler(BaseHTTPRequestHandler):
    """微信消息处理器"""
    
    def _send_json_response(self, response: WeChatMessageResponse):
        """发送 JSON 响应"""
        self.send_response(response.code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response.to_dict()).encode('utf-8'))
    
    def do_POST(self):
        """处理 POST 请求"""
        # 读取请求体
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                response = WeChatMessageResponse(
                    code=400,
                    message="empty request body"
                )
                self._send_json_response(response)
                return
            
            body = self.rfile.read(content_length)
        except Exception as e:
            logger.error(f"Failed to read request body: {e}")
            response = WeChatMessageResponse(
                code=400,
                message="failed to read request body"
            )
            self._send_json_response(response)
            return
        
        # 解析 JSON
        try:
            req = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON body: {e}")
            response = WeChatMessageResponse(
                code=400,
                message="invalid JSON body"
            )
            self._send_json_response(response)
            return
        
        # TODO: 在这里继续处理解析后的 req（如入库、业务逻辑等）
        logger.info(f"Received WeChat message: {req}")
        
        # 返回成功响应
        response = WeChatMessageResponse(
            code=200,
            message="ok"
        )
        self._send_json_response(response)
    
    def do_GET(self):
        """处理其他方法的请求"""
        self._handle_method_not_allowed()
    
    def do_PUT(self):
        """处理其他方法的请求"""
        self._handle_method_not_allowed()
    
    def do_DELETE(self):
        """处理其他方法的请求"""
        self._handle_method_not_allowed()
    
    def _handle_method_not_allowed(self):
        """处理不允许的方法"""
        response = WeChatMessageResponse(
            code=405,
            message="method not allowed, only POST is supported"
        )
        self._send_json_response(response)
    
    def log_message(self, format, *args):
        """重写日志方法，使用 Python logging"""
        logger.info("%s - - %s" % (self.address_string(), format % args))


async def on_wechat_messages(request: web.Request) -> web.Response:
    """
    处理微信消息的 aiohttp 处理器
    
    Args:
        request: aiohttp Request 对象
        
    Returns:
        web.Response: HTTP 响应
    """
    # 只接受 POST 请求
    if request.method != 'POST':
        response = WeChatMessageResponse(
            code=405,
            message="method not allowed, only POST is supported"
        )
        return web.json_response(response.to_dict(), status=405)
    
    # 读取请求体
    try:
        body = await request.read()
    except Exception as e:
        logger.error(f"Failed to read request body: {e}")
        response = WeChatMessageResponse(
            code=400,
            message="failed to read request body"
        )
        return web.json_response(response.to_dict(), status=400)
    
    # 检查请求体是否为空
    if not body or len(body) == 0:
        response = WeChatMessageResponse(
            code=400,
            message="empty request body"
        )
        return web.json_response(response.to_dict(), status=400)
    
    # 解析 JSON
    try:
        req = json.loads(body)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON body: {e}")
        response = WeChatMessageResponse(
            code=400,
            message="invalid JSON body"
        )
        return web.json_response(response.to_dict(), status=400)
    
    # TODO: 在这里继续处理解析后的 req（如入库、业务逻辑等）
    logger.info(f"Received WeChat message: {req}")
    
    # 返回成功响应
    response = WeChatMessageResponse(
        code=200,
        message="ok"
    )
    return web.json_response(response.to_dict(), status=200)
