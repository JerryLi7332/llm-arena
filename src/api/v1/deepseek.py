from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.dependency import DependAuth
from services.deepseek_service import deepseek_service
from core.exceptions import CustomException

router = APIRouter()


# 请求和响应模型
class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色: user 或 assistant")
    content: str = Field(..., description="消息内容")


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="对话消息列表")
    model: Optional[str] = Field(None, description="使用的模型")
    temperature: Optional[float] = Field(None, ge=0, le=2, description="创造性参数 (0-2)")
    max_tokens: Optional[int] = Field(None, ge=100, le=32768, description="最大输出长度")
    stream: bool = Field(False, description="是否流式输出")


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[dict]
    usage: Optional[dict] = None


class ModelsResponse(BaseModel):
    data: List[dict]


class StatusResponse(BaseModel):
    status: str
    message: str
    timestamp: str


class RateLimitResponse(BaseModel):
    minute_limit: int
    minute_used: int
    minute_remaining: int
    minute_reset: str
    hour_limit: int
    hour_used: int
    hour_remaining: int
    hour_reset: str
    daily_cost: float
    max_daily_cost: float
    cost_reset: str


@router.post("/chat", response_model=ChatCompletionResponse, tags=["DeepSeek API"])
async def chat_completion(
    request: ChatCompletionRequest,
    current_user: dict = DependAuth
):
    """
    DeepSeek 聊天完成接口
    
    - **messages**: 对话消息列表
    - **model**: 使用的模型 (可选，默认使用配置的模型)
    - **temperature**: 创造性参数 (可选，默认0.7)
    - **max_tokens**: 最大输出长度 (可选，默认1000)
    - **stream**: 是否流式输出 (可选，默认False)
    """
    try:
        # 验证消息格式
        if not request.messages:
            raise CustomException(
                status_code=400,
                message="消息列表不能为空"
            )
        
        # 验证最后一条消息是用户消息
        if request.messages[-1].role != "user":
            raise CustomException(
                status_code=400,
                message="最后一条消息必须是用户消息"
            )
        
        # 调用DeepSeek服务
        response = await deepseek_service.chat_completion(
            messages=[msg.dict() for msg in request.messages],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        return response
        
    except CustomException:
        raise
    except Exception as e:
        raise CustomException(
            status_code=500,
            message="聊天完成失败",
            details={"error": str(e)}
        )


@router.get("/models", response_model=ModelsResponse, tags=["DeepSeek API"])
async def get_models(current_user: dict = DependAuth):
    """
    获取可用的DeepSeek模型列表
    """
    try:
        response = await deepseek_service.get_models()
        return response
        
    except CustomException:
        raise
    except Exception as e:
        raise CustomException(
            status_code=500,
            message="获取模型列表失败",
            details={"error": str(e)}
        )


@router.get("/status", response_model=StatusResponse, tags=["DeepSeek API"])
async def check_status(current_user: dict = DependAuth):
    """
    检查DeepSeek API状态
    """
    try:
        response = await deepseek_service.check_status()
        return response
        
    except CustomException:
        raise
    except Exception as e:
        raise CustomException(
            status_code=500,
            message="检查API状态失败",
            details={"error": str(e)}
        )


@router.get("/rate-limit", response_model=RateLimitResponse, tags=["DeepSeek API"])
async def get_rate_limit_info(current_user: dict = DependAuth):
    """
    获取DeepSeek API速率限制信息
    """
    try:
        response = deepseek_service.get_rate_limit_info()
        return response
        
    except Exception as e:
        raise CustomException(
            status_code=500,
            message="获取速率限制信息失败",
            details={"error": str(e)}
        )


@router.get("/config", tags=["DeepSeek API"])
async def get_config(current_user: dict = DependAuth):
    """
    获取DeepSeek API配置信息（不包含敏感信息）
    """
    try:
        from settings.deepseek import deepseek_settings
        
        config = {
            "api_base": deepseek_settings.DEEPSEEK_API_BASE,
            "default_model": deepseek_settings.DEEPSEEK_DEFAULT_MODEL,
            "max_tokens": deepseek_settings.DEEPSEEK_MAX_TOKENS,
            "temperature": deepseek_settings.DEEPSEEK_TEMPERATURE,
            "request_timeout": deepseek_settings.DEEPSEEK_REQUEST_TIMEOUT,
            "rate_limit_per_minute": deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_MINUTE,
            "rate_limit_per_hour": deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_HOUR,
            "max_cost_per_request": deepseek_settings.DEEPSEEK_MAX_COST_PER_REQUEST,
            "max_cost_per_day": deepseek_settings.DEEPSEEK_MAX_COST_PER_DAY
        }
        
        return {
            "config": config,
            "message": "配置信息获取成功"
        }
        
    except Exception as e:
        raise CustomException(
            status_code=500,
            message="获取配置信息失败",
            details={"error": str(e)}
        )
