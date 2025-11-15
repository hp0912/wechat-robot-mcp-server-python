"""
WeChat Robot MCP Server - Python Implementation
微信机器人 MCP 服务器主程序
"""
import logging
import sys
from typing import List
import asyncio
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from mcp.server.fastmcp import FastMCP

from .config import config
from .tools.registry import register_tools
from .webhook.wechat_messages import on_wechat_messages

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 版本信息
VERSION = "1.0.0"

# 创建 FastMCP 服务器并注册工具
mcp = FastMCP("wechat-robot-mcp-server")
register_tools(mcp)


async def webhook_handler(request):
    """处理 webhook 请求"""
    result = await on_wechat_messages(request)
    return JSONResponse(content=result, status_code=result.get("code", 200))


def run() -> None:
    """主入口函数 - 同时支持 MCP 和 Webhook"""
    logger.info(f"[MCP Server]启动 版本: {VERSION}")
    
    # 加载配置
    try:
        config.load_config()
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)
    
    # 创建 Starlette 应用，同时支持 MCP 和 Webhook
    app = Starlette(
        routes=[
            # MCP Streamable HTTP 端点
            Mount("/mcp", app=mcp.streamable_http_app()),
            # Webhook 端点
            Route("/api/v1/messages", webhook_handler, methods=["POST"]),
        ]
    )
    
    # 运行服务器
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.mcp_server_port)


if __name__ == "__main__":
    run()
