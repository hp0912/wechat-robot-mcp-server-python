from mcp.server.fastmcp import FastMCP

from .mcp_chat_room_summary import register_chat_room_summary_tool


def register_tools(mcp: FastMCP) -> None:
    """注册所有 MCP 工具。

    新增工具时，只需要在这里调用对应的 register_xxx_tool 即可。
    """

    register_chat_room_summary_tool(mcp)
