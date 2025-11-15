"""
Chat Room Summary Tool - 群聊总结工具

将群聊记录总结成结构化的报告
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import httpx
from openai import OpenAI

from ..robot_context.context import get_robot_context, get_db
from ..repository.global_settings import GlobalSettingsRepository
from ..repository.chatroom_settings import ChatRoomSettingsRepository
from ..repository.contact import ContactRepository
from ..repository.message import MessageRepository
from ..utils.utils import normalize_ai_base_url, call_tool_result_error

logger = logging.getLogger(__name__)


class ChatRoomSummaryInput:
    """群聊总结输入参数"""
    
    def __init__(self, recent_duration: int):
        """
        初始化
        
        Args:
            recent_duration: 最近多久的聊天记录(秒)，例如最近一小时是3600秒，最近一天是86400秒
        """
        self.recent_duration = recent_duration


async def chat_room_summary(
    params: Dict[str, Any]
) -> Tuple[Dict[str, Any], Any, Optional[Exception]]:
    """
    群聊总结工具
    
    Args:
        params: 参数字典，包含 recent_duration
        
    Returns:
        包含结果的元组 (result, data, error)
    """
    try:
        # 解析参数
        recent_duration = params.get('recent_duration', 0)
        if not recent_duration or recent_duration <= 0:
            return call_tool_result_error("请指定有效的时间范围(秒)")
        
        if recent_duration > 24 * 3600:
            return call_tool_result_error("最多只能总结最近24小时内的聊天记录")
        
        # 获取机器人上下文
        rc = get_robot_context()
        if rc is None:
            return call_tool_result_error("获取机器人上下文失败")
        
        # 获取数据库连接
        db = get_db()
        if db is None:
            return call_tool_result_error("获取数据库连接失败")
        
        # 创建仓库实例
        global_settings_repo = GlobalSettingsRepository(db)
        chatroom_settings_repo = ChatRoomSettingsRepository(db)
        contact_repo = ContactRepository(db)
        message_repo = MessageRepository(db)
        
        # 获取全局设置
        global_settings = global_settings_repo.get_global_settings()
        if global_settings is None:
            return call_tool_result_error("获取全局设置失败")
        
        chat_ai_enabled = getattr(global_settings, 'chat_ai_enabled', False)
        chat_api_key = getattr(global_settings, 'chat_api_key', '')
        chat_base_url = getattr(global_settings, 'chat_base_url', '')
        
        if not chat_ai_enabled or not chat_api_key or not chat_base_url:
            return call_tool_result_error("全局配置群聊总结未开启")
        
        # 获取群聊设置
        chatroom_settings = chatroom_settings_repo.get_chatroom_settings(rc.from_wx_id)
        if chatroom_settings is None:
            return call_tool_result_error("获取群聊设置失败")
        
        chat_room_summary_enabled = getattr(chatroom_settings, 'chat_room_summary_enabled', None)
        if not chat_room_summary_enabled:
            return call_tool_result_error("群聊总结未开启")
        
        # 获取群聊名称
        chat_room_name = rc.from_wx_id
        chat_room = contact_repo.get_contact_by_wechat_id(rc.from_wx_id)
        if chat_room:
            nickname = getattr(chat_room, 'nickname', None)
            if nickname:
                chat_room_name = nickname
        
        # 获取聊天记录
        end_time = datetime.now()
        start_time = end_time - timedelta(seconds=recent_duration)
        
        messages = message_repo.get_messages_by_time_range(
            rc.robot_wx_id,
            rc.from_wx_id,
            int(start_time.timestamp()),
            int(end_time.timestamp())
        )
        
        if len(messages) < 100:
            return call_tool_result_error("聊天记录不足100条，不需要总结")
        
        # 组装对话记录为字符串
        content_lines = []
        for message in messages:
            # 格式化时间
            time_str = datetime.fromtimestamp(message.created_at).strftime("%Y-%m-%d %H:%M:%S")
            # 替换换行符
            msg_content = message.message.replace("\n", "。。")
            content_lines.append(f'[{time_str}] {{"{message.nickname}": "{msg_content}"}}--end--')
        
        # 构建提示词
        prompt = """你是一个中文的群聊总结的助手，你可以为一个微信的群聊记录，提取并总结每个时间段大家在重点讨论的话题内容。

每一行代表一个人的发言，每一行的的格式为： {"[time] {nickname}": "{content}"}--end--

请帮我将给出的群聊内容总结成一个今日的群聊报告，包含不多于10个的话题的总结（如果还有更多话题，可以在后面简单补充）。每个话题包含以下内容：
- 话题名(50字以内，带序号1️⃣2️⃣3️⃣，同时附带热度，以🔥数量表示）
- 参与者(不超过5个人，将重复的人名去重)
- 时间段(从几点到几点)
- 过程(50到200字左右）
- 评价(50字以下)
- 分割线： ------------

另外有以下要求：
1. 每个话题结束使用 ------------ 分割
2. 使用中文冒号
3. 无需大标题
4. 开始给出本群讨论风格的整体评价，例如活跃、太水、太黄、太暴力、话题不集中、无聊诸如此类
"""
        
        msg = f"群名称: {chat_room_name}\n聊天记录如下:\n" + "\n".join(content_lines)
        
        # 配置AI客户端
        ai_api_key = chat_api_key
        chatroom_api_key = getattr(chatroom_settings, 'chat_api_key', None)
        if chatroom_api_key:
            ai_api_key = chatroom_api_key
        
        ai_base_url = chat_base_url.rstrip("/")
        chatroom_base_url = getattr(chatroom_settings, 'chat_base_url', None)
        if chatroom_base_url:
            ai_base_url = chatroom_base_url.rstrip("/")
        
        ai_base_url = normalize_ai_base_url(ai_base_url)
        
        ai_model = getattr(global_settings, 'chat_room_summary_model', None) or "gpt-3.5-turbo"
        chatroom_model = getattr(chatroom_settings, 'chat_room_summary_model', None)
        if chatroom_model:
            ai_model = chatroom_model
        
        # 创建OpenAI客户端
        client = OpenAI(
            api_key=ai_api_key,
            base_url=ai_base_url
        )
        
        # 调用AI进行总结
        try:
            response = client.chat.completions.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": msg}
                ],
                stream=False,
                max_tokens=2000
            )
            
            if not response.choices or len(response.choices) == 0 or not response.choices[0].message.content:
                return call_tool_result_error("AI 总结失败，返回了空内容")
            
            summary_content = response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI 总结失败: {e}")
            return call_tool_result_error(f"AI 总结失败: {str(e)}")
        
        # 构建回复消息
        reply_msg = f"#消息总结\n让我们一起来看看群友们都聊了什么有趣的话题吧~\n\n{summary_content}"
        
        # 发送总结消息
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"http://client_{rc.robot_code}:{rc.we_chat_client_port}/api/v1/robot/message/send/longtext",
                    json={
                        "to_wxid": rc.from_wx_id,
                        "content": reply_msg
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code != 200:
                    return call_tool_result_error(
                        f"发送聊天总结失败，返回状态码不是 200: {response.status_code}"
                    )
                
                resp_data = response.json()
                if resp_data.get("code") != 200:
                    return call_tool_result_error(
                        f"发送聊天总结失败，返回状态码不是 200: {resp_data.get('message', '未知错误')}"
                    )
                
        except Exception as e:
            logger.error(f"发送聊天总结失败: {e}")
            return call_tool_result_error(f"发送聊天总结失败: {str(e)}")
        
        # 返回成功结果
        result = {
            "content": [
                {
                    "type": "text",
                    "text": "聊天总结发送成功"
                }
            ]
        }
        
        return result, None, None
        
    except Exception as e:
        logger.error(f"群聊总结工具执行失败: {e}")
        return call_tool_result_error(f"群聊总结工具执行失败: {str(e)}")
