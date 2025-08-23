"""
Rock Paper Scissors Game Package - 石头剪刀布游戏包

实现石头剪刀布游戏的核心逻辑
"""

from .referee import Referee

# 游戏元数据
GAME_NAME = "石头剪刀布"
GAME_VERSION = "1.0.0"
GAME_DESCRIPTION = "经典的石头剪刀布游戏，支持AI对战和玩家对战"

__all__ = [
    "Referee",
    "GAME_NAME",
    "GAME_VERSION", 
    "GAME_DESCRIPTION"
]

