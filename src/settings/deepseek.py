import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeekSettings(BaseSettings):
    """DeepSeek API配置"""
    
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # 忽略额外的环境变量
        env_ignore_empty=True,
    )
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    DEEPSEEK_DEFAULT_MODEL: str = "deepseek-chat"
    
    # 可选配置
    DEEPSEEK_MAX_TOKENS: int = 4000
    DEEPSEEK_TEMPERATURE: float = 0.7
    DEEPSEEK_REQUEST_TIMEOUT: int = 30000
    
    # 速率限制配置
    DEEPSEEK_RATE_LIMIT_PER_MINUTE: int = 60
    DEEPSEEK_RATE_LIMIT_PER_HOUR: int = 1000
    
    # 成本控制
    DEEPSEEK_MAX_COST_PER_REQUEST: float = 0.01  # 美元
    DEEPSEEK_MAX_COST_PER_DAY: float = 1.0  # 美元
    
    @field_validator("DEEPSEEK_API_KEY")
    @classmethod
    def validate_api_key(cls, v):
        """验证API密钥"""
        if not v:
            raise ValueError("DEEPSEEK_API_KEY必须设置")
        if not v.startswith("sk-"):
            raise ValueError("DeepSeek API密钥格式错误，应以'sk-'开头")
        if len(v) < 20:
            raise ValueError("DeepSeek API密钥长度不足")
        return v
    
    @field_validator("DEEPSEEK_TEMPERATURE")
    @classmethod
    def validate_temperature(cls, v):
        """验证温度值"""
        if not 0 <= v <= 2:
            raise ValueError("温度值必须在0-2之间")
        return v
    
    @field_validator("DEEPSEEK_MAX_TOKENS")
    @classmethod
    def validate_max_tokens(cls, v):
        """验证最大token数"""
        if not 100 <= v <= 32768:
            raise ValueError("最大token数必须在100-32768之间")
        return v
    
    @field_validator("DEEPSEEK_REQUEST_TIMEOUT")
    @classmethod
    def validate_timeout(cls, v):
        """验证超时时间"""
        if not 5000 <= v <= 120000:
            raise ValueError("请求超时时间必须在5-120秒之间")
        return v


# 创建全局配置实例
deepseek_settings = DeepSeekSettings()
