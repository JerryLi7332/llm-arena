from tortoise import fields
from .base import BaseModel, TimestampMixin


# class AICode(BaseModel, TimestampMixin):
#     """AI代码模型"""
#     user_id = fields.BigIntField(description="用户ID", index=True)
#     name = fields.CharField(max_length=100, description="AI代码名称")
#     code_path = fields.CharField(max_length=500, description="AI代码文件路径")
#     game_type = fields.CharField(max_length=50, description="游戏类型", index=True)
#     description = fields.TextField(null=True, description="AI代码描述")
#     version = fields.IntField(default=1, description="版本号")
#     is_active = fields.BooleanField(default=False, description="是否激活", index=True)
    
#     class Meta:
#         table = "ai_code"


# class GameStats(BaseModel, TimestampMixin):
#     """游戏统计模型"""
#     user_id = fields.BigIntField(description="用户ID", index=True)
#     ranking_id = fields.IntField(default=0, description="排行榜ID", index=True)
#     elo_score = fields.IntField(default=1200, description="ELO评分")
#     wins = fields.IntField(default=0, description="胜利场次")
#     losses = fields.IntField(default=0, description="失败场次")
#     draws = fields.IntField(default=0, description="平局场次")
#     games_played = fields.IntField(default=0, description="总游戏场次")
#     cancelled_games = fields.IntField(default=0, description="取消的游戏场次")
    
#     class Meta:
#         table = "game_stats"
#         unique_together = (("user_id", "ranking_id"),)


class Battle(BaseModel, TimestampMixin):
    """对战模型"""
    status = fields.CharField(max_length=20, default="waiting", description="对战状态", index=True)
    ranking_id = fields.IntField(default=0, description="排行榜ID", index=True)
    started_at = fields.DatetimeField(null=True, description="开始时间")
    ended_at = fields.DatetimeField(null=True, description="结束时间")
    results = fields.JSONField(null=True, description="对战结果")
    game_log_uuid = fields.CharField(max_length=100, null=True, description="游戏日志UUID")
    battle_type = fields.CharField(max_length=50, default="standard", description="对战类型")
    is_elo_exempt = fields.BooleanField(default=False, description="是否ELO豁免")
    
    class Meta:
        table = "battle"


class BattlePlayer(BaseModel, TimestampMixin):
    """对战参与者模型"""
    battle_id = fields.BigIntField(description="对战ID", index=True)
    user_id = fields.BigIntField(description="用户ID", index=True)
    selected_ai_code_id = fields.BigIntField(null=True, description="选择的AI代码ID")
    position = fields.IntField(description="玩家位置(1-7)")
    initial_elo = fields.IntField(null=True, description="初始ELO分数")
    elo_change = fields.IntField(default=0, description="ELO变化")
    outcome = fields.CharField(max_length=20, null=True, description="对战结果")
    join_time = fields.DatetimeField(auto_now_add=True, description="加入时间")
    
    class Meta:
        table = "battle_player"
        unique_together = (("battle_id", "position"), ("battle_id", "user_id"))
