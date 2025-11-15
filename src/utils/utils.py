import re
import logging
from typing import Tuple, Dict, Any, Optional


def normalize_ai_base_url(base_url: str) -> str:
    """
    规范化AI BaseURL，确保以/v+数字结尾，如果没有则添加/v1
    
    Args:
        base_url: 原始的base URL
        
    Returns:
        规范化后的base URL
    """
    base_url = base_url.rstrip("/")
    version_regex = re.compile(r'/v\d+$')
    if not version_regex.search(base_url):
        base_url += "/v1"
    return base_url


def call_tool_result_error(errmsg: str) -> Tuple[Dict[str, Any], None, None]:
    """
    创建工具调用错误结果
    
    Args:
        errmsg: 错误消息
        
    Returns:
        包含错误信息的结果元组
    """
    logging.error(errmsg)
    
    result: Dict[str, Any] = {
        "isError": True,
        "content": [
            {
                "type": "text",
                "text": errmsg
            }
        ]
    }
    return result, None, None
