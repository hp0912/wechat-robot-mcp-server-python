"""
WeChat Robot MCP Server - Python Implementation
微信机器人 MCP 服务器主程序
"""
import logging
import sys
from typing import Any, Dict, List
import asyncio
from aiohttp import web
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from .config import config
from .middleware.tenant import TenantMiddleware
from .tools.chat_room_summary import chat_room_summary
from .webhook.wechat_messages import on_wechat_messages

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 版本信息
VERSION = "1.0.0"


async def serve() -> None:
    """启动 MCP 服务器"""
    logger.info(f"[MCP Server]启动 版本: {VERSION}")
    
    # 加载配置
    try:
        config.load_config()
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)
    
    # 创建 MCP 服务器
    server = Server("wechat-robot-mcp-server")
    
    # 注册工具
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        """列出可用的工具"""
        return [
            Tool(
                name="ChatRoomSummary",
                description="微信群聊总结，当用户想总结群聊内容时，可以调用该工具。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "recent_duration": {
                            "type": "integer",
                            "description": "最近多久的聊天记录(秒)，例如最近一小时是3600秒，最近一天是86400秒"
                        }
                    },
                    "required": ["recent_duration"]
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """处理工具调用"""
        if name == "ChatRoomSummary":
            result, data, error = await chat_room_summary(arguments)
            if error:
                return [TextContent(type="text", text=f"错误: {error}")]
            return [TextContent(type="text", text=str(result))]
        else:
            raise ValueError(f"未知工具: {name}")
    
    # 使用 stdio 传输运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


async def create_http_app() -> web.Application:
    """创建 HTTP 应用"""
    app = web.Application()
    
    # 注册路由
    app.router.add_post('/api/v1/messages', on_wechat_messages)
    
    return app


async def run_http_server() -> None:
    """运行 HTTP 服务器（用于 webhook）"""
    logger.info(f"[MCP Server]启动 版本: {VERSION}")
    
    # 加载配置
    try:
        config.load_config()
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)
    
    app = await create_http_app()
    
    # 启动服务器
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.mcp_server_port)
    
    logger.info(f"HTTP 服务器运行在端口 {config.mcp_server_port}")
    await site.start()
    
    # 保持运行
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("收到停止信号，关闭服务器...")
    finally:
        await runner.cleanup()


def run() -> None:
    """主入口函数"""
    # 根据参数决定运行模式
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        # HTTP 模式（用于接收 webhook）
        asyncio.run(run_http_server())
    else:
        # MCP stdio 模式（默认）
        asyncio.run(serve())


if __name__ == "__main__":
    run()
