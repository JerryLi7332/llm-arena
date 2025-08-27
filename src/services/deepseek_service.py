import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

import httpx
from fastapi import HTTPException

from settings.deepseek import deepseek_settings
from core.exceptions import CustomException

logger = logging.getLogger(__name__)


class DeepSeekService:
    """DeepSeek API服务"""
    
    def __init__(self):
        self.api_key = deepseek_settings.DEEPSEEK_API_KEY
        self.api_base = deepseek_settings.DEEPSEEK_API_BASE
        self.default_model = deepseek_settings.DEEPSEEK_DEFAULT_MODEL
        self.timeout = deepseek_settings.DEEPSEEK_REQUEST_TIMEOUT / 1000  # 转换为秒
        
        # 速率限制计数器
        self._request_count_minute = 0
        self._request_count_hour = 0
        self._last_minute_reset = datetime.now()
        self._last_hour_reset = datetime.now()
        
        # 成本统计
        self._daily_cost = 0.0
        self._last_cost_reset = datetime.now()
    
    def _check_rate_limit(self):
        """检查速率限制"""
        now = datetime.now()
        
        # 每分钟限制
        if now - self._last_minute_reset >= timedelta(minutes=1):
            self._request_count_minute = 0
            self._last_minute_reset = now
        
        if self._request_count_minute >= deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_MINUTE:
            raise CustomException(
                status_code=429,
                message="API调用频率超限，请稍后重试",
                details={"limit": "per_minute", "reset_time": self._last_minute_reset + timedelta(minutes=1)}
            )
        
        # 每小时限制
        if now - self._last_hour_reset >= timedelta(hours=1):
            self._request_count_hour = 0
            self._last_hour_reset = now
        
        if self._request_count_hour >= deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_HOUR:
            raise CustomException(
                status_code=429,
                message="API调用频率超限，请稍后重试",
                details={"limit": "per_hour", "reset_time": self._last_hour_reset + timedelta(hours=1)}
            )
    
    def _update_rate_limit_counters(self):
        """更新速率限制计数器"""
        self._request_count_minute += 1
        self._request_count_hour += 1
    
    def _check_cost_limit(self, estimated_cost: float):
        """检查成本限制"""
        now = datetime.now()
        
        # 每日成本重置
        if now - self._last_cost_reset >= timedelta(days=1):
            self._daily_cost = 0.0
            self._last_cost_reset = now
        
        # 单次请求成本限制
        if estimated_cost > deepseek_settings.DEEPSEEK_MAX_COST_PER_REQUEST:
            raise CustomException(
                status_code=400,
                message="预估成本超出单次请求限制",
                details={"estimated_cost": estimated_cost, "max_cost": deepseek_settings.DEEPSEEK_MAX_COST_PER_REQUEST}
            )
        
        # 每日成本限制
        if self._daily_cost + estimated_cost > deepseek_settings.DEEPSEEK_MAX_COST_PER_DAY:
            raise CustomException(
                status_code=400,
                message="预估成本超出每日限制",
                details={"daily_cost": self._daily_cost, "estimated_cost": estimated_cost, "max_daily": deepseek_settings.DEEPSEEK_MAX_COST_PER_DAY}
            )
    
    def _estimate_cost(self, input_tokens: int, output_tokens: int, model: str = None) -> float:
        """估算API调用成本"""
        # DeepSeek的定价（每1000 tokens）
        pricing = {
            "deepseek-chat": 0.001,
            "deepseek-coder": 0.001,
            "deepseek-chat-33b": 0.002
        }
        
        model = model or self.default_model
        cost_per_1k = pricing.get(model, 0.001)
        
        input_cost = (input_tokens / 1000) * cost_per_1k
        output_cost = (output_tokens / 1000) * cost_per_1k
        
        return input_cost + output_cost
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送HTTP请求到DeepSeek API"""
        url = f"{self.api_base}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 合并headers
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        
        # 设置超时
        kwargs["timeout"] = self.timeout
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, **kwargs)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise CustomException(
                        status_code=401,
                        message="DeepSeek API密钥无效",
                        details={"error": "unauthorized"}
                    )
                elif response.status_code == 429:
                    raise CustomException(
                        status_code=429,
                        message="DeepSeek API速率限制",
                        details={"error": "rate_limit"}
                    )
                elif response.status_code == 400:
                    error_data = response.json()
                    raise CustomException(
                        status_code=400,
                        message="DeepSeek API请求参数错误",
                        details=error_data
                    )
                else:
                    raise CustomException(
                        status_code=response.status_code,
                        message="DeepSeek API调用失败",
                        details={"status_code": response.status_code, "response": response.text}
                    )
                    
        except httpx.TimeoutException:
            raise CustomException(
                status_code=408,
                message="DeepSeek API请求超时",
                details={"timeout": self.timeout}
            )
        except httpx.RequestError as e:
            logger.error(f"DeepSeek API请求错误: {e}")
            raise CustomException(
                status_code=500,
                message="DeepSeek API网络错误",
                details={"error": str(e)}
            )
        except Exception as e:
            logger.error(f"DeepSeek API未知错误: {e}")
            raise CustomException(
                status_code=500,
                message="DeepSeek API调用失败",
                details={"error": str(e)}
            )
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """聊天完成接口"""
        # 检查速率限制
        self._check_rate_limit()
        
        # 估算成本
        estimated_input_tokens = sum(len(msg.get("content", "")) for msg in messages)
        estimated_output_tokens = max_tokens or 1000
        estimated_cost = self._estimate_cost(estimated_input_tokens, estimated_output_tokens, model)
        
        # 检查成本限制
        self._check_cost_limit(estimated_cost)
        
        # 准备请求数据
        request_data = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature or deepseek_settings.DEEPSEEK_TEMPERATURE,
            "max_tokens": max_tokens or deepseek_settings.DEEPSEEK_MAX_TOKENS,
            "stream": stream
        }
        
        try:
            # 发送请求
            response = await self._make_request(
                "POST",
                "/chat/completions",
                json=request_data
            )
            
            # 更新计数器
            self._update_rate_limit_counters()
            
            # 更新成本统计
            if "usage" in response:
                actual_cost = self._estimate_cost(
                    response["usage"].get("prompt_tokens", 0),
                    response["usage"].get("completion_tokens", 0),
                    model
                )
                self._daily_cost += actual_cost
            
            logger.info(f"DeepSeek API调用成功: {model}, 成本: ${estimated_cost:.6f}")
            return response
            
        except Exception as e:
            logger.error(f"DeepSeek API调用失败: {e}")
            raise
    
    async def get_models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        # 检查速率限制
        self._check_rate_limit()
        
        try:
            response = await self._make_request("GET", "/models")
            
            # 更新计数器
            self._update_rate_limit_counters()
            
            logger.info("DeepSeek API获取模型列表成功")
            return response
            
        except Exception as e:
            logger.error(f"DeepSeek API获取模型列表失败: {e}")
            raise
    
    async def check_status(self) -> Dict[str, Any]:
        """检查API状态"""
        try:
            # 使用获取模型列表来检查API状态
            await self.get_models()
            return {
                "status": "available",
                "message": "DeepSeek API运行正常",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"DeepSeek API状态检查失败: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """获取速率限制信息"""
        now = datetime.now()
        
        return {
            "minute_limit": deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_MINUTE,
            "minute_used": self._request_count_minute,
            "minute_remaining": max(0, deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_MINUTE - self._request_count_minute),
            "minute_reset": (self._last_minute_reset + timedelta(minutes=1)).isoformat(),
            
            "hour_limit": deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_HOUR,
            "hour_used": self._request_count_hour,
            "hour_remaining": max(0, deepseek_settings.DEEPSEEK_RATE_LIMIT_PER_HOUR - self._request_count_hour),
            "hour_reset": (self._last_hour_reset + timedelta(hours=1)).isoformat(),
            
            "daily_cost": round(self._daily_cost, 6),
            "max_daily_cost": deepseek_settings.DEEPSEEK_MAX_COST_PER_DAY,
            "cost_reset": (self._last_cost_reset + timedelta(days=1)).isoformat()
        }


# 创建全局服务实例
deepseek_service = DeepSeekService()
