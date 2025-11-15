import logging
from mcp.server.fastmcp import Context, FastMCP

from ..middleware.tenant import apply_tenant_from_meta
from .chat_room_summary import chat_room_summary as _chat_room_summary

logger = logging.getLogger(__name__)


def register_chat_room_summary_tool(mcp: FastMCP) -> None:
    @mcp.tool()
    async def ChatRoomSummary(recent_duration: int, ctx: Context) -> str:
        """微信群聊总结，当用户想总结群聊内容时，可以调用该工具。

        Args:
            recent_duration: 最近多久的聊天记录(秒)，例如最近一小时是3600秒，最近一天是86400秒
        """
        try:
            meta: dict | None = getattr(ctx.request_context, "meta", None)
            if meta:
                apply_tenant_from_meta(meta)
        except Exception as e:
            logger.error(f"应用租户上下文失败: {e}")

        result, data, error = await _chat_room_summary({"recent_duration": recent_duration})
        if error:
            raise Exception(f"错误: {error}")

        if isinstance(result, dict) and "content" in result:
            content_list = result["content"]
            if content_list and isinstance(content_list[0], dict):
                return content_list[0].get("text", str(result))
        return str(result)
