from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AICodeBase(BaseModel):
    """AI代码基础模型"""
    name: str = Field(..., description="AI代码名称", max_length=100)
    description: Optional[str] = Field(None, description="AI代码描述")
    game_type: str = Field(..., description="游戏类型", max_length=50)
    version: int = Field(default=1, description="版本号")
    is_active: bool = Field(default=False, description="是否激活")
    is_public: bool = Field(default=False, description="是否公开")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    config: Optional[Dict[str, Any]] = Field(None, description="配置参数")


class AICodeCreate(AICodeBase):
    """创建AI代码模型"""
    user_id: int = Field(..., description="用户ID")
    file_path: str = Field(..., description="AI代码文件路径", max_length=500)
    file_name: str = Field(..., description="原始文件名", max_length=255)
    file_size: int = Field(..., description="文件大小（字节）")
    file_hash: Optional[str] = Field(None, description="文件哈希值", max_length=64)


class AICodeUpdate(BaseModel):
    """更新AI代码模型"""
    name: Optional[str] = Field(None, description="AI代码名称", max_length=100)
    description: Optional[str] = Field(None, description="AI代码描述")
    is_public: Optional[bool] = Field(None, description="是否公开")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    config: Optional[Dict[str, Any]] = Field(None, description="配置参数")


class AICodeResponse(AICodeBase):
    """AI代码响应模型"""
    id: int = Field(..., description="AI代码ID")
    user_id: int = Field(..., description="用户ID")
    file_path: str = Field(..., description="AI代码文件路径")
    file_name: str = Field(..., description="原始文件名")
    file_size: int = Field(..., description="文件大小（字节）")
    file_hash: Optional[str] = Field(None, description="文件哈希值")
    last_used: Optional[datetime] = Field(None, description="最后使用时间")
    win_count: int = Field(default=0, description="胜利次数")
    loss_count: int = Field(default=0, description="失败次数")
    draw_count: int = Field(default=0, description="平局次数")
    total_games: int = Field(default=0, description="总游戏次数")
    win_rate: float = Field(default=0.0, description="胜率")
    elo_score: int = Field(default=1200, description="ELO评分")
    download_count: int = Field(default=0, description="下载次数")
    rating: float = Field(default=0.0, description="评分")
    review_count: int = Field(default=0, description="评论数量")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class AICodeListResponse(BaseModel):
    """AI代码列表响应模型"""
    total: int = Field(..., description="总数")
    items: List[AICodeResponse] = Field(..., description="AI代码列表")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")


class GameStatsBase(BaseModel):
    """游戏统计基础模型"""
    user_id: int = Field(..., description="用户ID")
    game_type: str = Field(..., description="游戏类型", max_length=50)
    ranking_id: int = Field(default=0, description="排行榜ID")
    elo_score: int = Field(default=1200, description="ELO评分")
    wins: int = Field(default=0, description="胜利场次")
    losses: int = Field(default=0, description="失败场次")
    draws: int = Field(default=0, description="平局场次")
    games_played: int = Field(default=0, description="总游戏场次")
    win_rate: float = Field(default=0.0, description="胜率")


class GameStatsResponse(GameStatsBase):
    """游戏统计响应模型"""
    id: int = Field(..., description="游戏统计ID")
    cancelled_games: int = Field(default=0, description="取消的游戏场次")
    best_elo: int = Field(default=1200, description="最高ELO分数")
    current_streak: int = Field(default=0, description="当前连胜/连败")
    longest_win_streak: int = Field(default=0, description="最长连胜")
    longest_lose_streak: int = Field(default=0, description="最长连败")
    last_game_at: Optional[datetime] = Field(None, description="最后游戏时间")
    total_play_time: int = Field(default=0, description="总游戏时间（秒）")
    average_game_time: float = Field(default=0.0, description="平均游戏时间（秒）")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class BattleBase(BaseModel):
    """对战基础模型"""
    status: str = Field(default="waiting", description="对战状态", max_length=20)
    ranking_id: int = Field(default=0, description="排行榜ID")
    battle_type: str = Field(default="standard", description="对战类型", max_length=50)
    is_elo_exempt: bool = Field(default=False, description="是否ELO豁免")


class BattleCreate(BattleBase):
    """创建对战模型"""
    pass


class BattleResponse(BattleBase):
    """对战响应模型"""
    id: int = Field(..., description="对战ID")
    started_at: Optional[datetime] = Field(None, description="开始时间")
    ended_at: Optional[datetime] = Field(None, description="结束时间")
    results: Optional[Dict[str, Any]] = Field(None, description="对战结果")
    game_log_uuid: Optional[str] = Field(None, description="游戏日志UUID", max_length=100)
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class BattlePlayerBase(BaseModel):
    """对战参与者基础模型"""
    battle_id: int = Field(..., description="对战ID")
    user_id: int = Field(..., description="用户ID")
    selected_ai_code_id: Optional[int] = Field(None, description="选择的AI代码ID")
    position: int = Field(..., description="玩家位置(1-7)")
    initial_elo: Optional[int] = Field(None, description="初始ELO分数")
    elo_change: int = Field(default=0, description="ELO变化")
    outcome: Optional[str] = Field(None, description="对战结果", max_length=20)


class BattlePlayerCreate(BattlePlayerBase):
    """创建对战参与者模型"""
    pass


class BattlePlayerResponse(BattlePlayerBase):
    """对战参与者响应模型"""
    id: int = Field(..., description="对战参与者ID")
    join_time: datetime = Field(..., description="加入时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class AICodeReviewBase(BaseModel):
    """AI代码评论基础模型"""
    ai_code_id: int = Field(..., description="AI代码ID")
    user_id: int = Field(..., description="评论用户ID")
    rating: int = Field(..., description="评分(1-5)", ge=1, le=5)
    comment: str = Field(..., description="评论内容")
    is_helpful: bool = Field(default=False, description="是否有帮助")
    reply_to: Optional[int] = Field(None, description="回复的评论ID")


class AICodeReviewCreate(AICodeReviewBase):
    """创建AI代码评论模型"""
    pass


class AICodeReviewResponse(AICodeReviewBase):
    """AI代码评论响应模型"""
    id: int = Field(..., description="评论ID")
    helpful_count: int = Field(default=0, description="有帮助的数量")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class AICodeTagBase(BaseModel):
    """AI代码标签基础模型"""
    name: str = Field(..., description="标签名称", max_length=50)
    description: Optional[str] = Field(None, description="标签描述")
    color: str = Field(default="#666666", description="标签颜色", max_length=7)
    is_system: bool = Field(default=False, description="是否系统标签")


class AICodeTagCreate(AICodeTagBase):
    """创建AI代码标签模型"""
    pass


class AICodeTagResponse(AICodeTagBase):
    """AI代码标签响应模型"""
    id: int = Field(..., description="标签ID")
    usage_count: int = Field(default=0, description="使用次数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class AICodeVersionBase(BaseModel):
    """AI代码版本基础模型"""
    ai_code_id: int = Field(..., description="AI代码ID")
    version_number: int = Field(..., description="版本号")
    file_path: str = Field(..., description="文件路径", max_length=500)
    file_name: str = Field(..., description="文件名", max_length=255)
    file_size: int = Field(..., description="文件大小")
    file_hash: str = Field(..., description="文件哈希", max_length=64)
    changelog: Optional[str] = Field(None, description="更新日志")
    is_stable: bool = Field(default=True, description="是否稳定版本")


class AICodeVersionCreate(AICodeVersionBase):
    """创建AI代码版本模型"""
    pass


class AICodeVersionResponse(AICodeVersionBase):
    """AI代码版本响应模型"""
    id: int = Field(..., description="版本ID")
    download_count: int = Field(default=0, description="下载次数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class AICodeDownloadBase(BaseModel):
    """AI代码下载记录基础模型"""
    ai_code_id: int = Field(..., description="AI代码ID")
    user_id: int = Field(..., description="下载用户ID")
    ip_address: Optional[str] = Field(None, description="IP地址", max_length=45)
    user_agent: Optional[str] = Field(None, description="用户代理")
    download_type: str = Field(default="direct", description="下载类型", max_length=20)


class AICodeDownloadCreate(AICodeDownloadBase):
    """创建AI代码下载记录模型"""
    pass


class AICodeDownloadResponse(AICodeDownloadBase):
    """AI代码下载记录响应模型"""
    id: int = Field(..., description="下载记录ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


# 游戏类型枚举
from enum import Enum

class GameType(str, Enum):
    """游戏类型枚举"""
    ROCK_PAPER_SCISSORS = "rock_paper_scissors"
    AVALON = "avalon"


# 对战状态枚举
class BattleStatus(str, Enum):
    """对战状态枚举"""
    WAITING = "waiting"
    STARTING = "starting"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    ERROR = "error"


# 对战结果枚举
class BattleOutcome(str, Enum):
    """对战结果枚举"""
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
    CANCELLED = "cancelled"
    ERROR = "error"
