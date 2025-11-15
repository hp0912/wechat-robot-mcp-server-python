from typing import Any, Optional
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int = Field(..., description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
