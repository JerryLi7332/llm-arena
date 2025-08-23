"""
Avalon Game Package - 阿瓦隆游戏包

实现七人局阿瓦隆游戏的核心逻辑
"""

from .referee import Referee

# 游戏元数据
GAME_NAME = "阿瓦隆"
GAME_VERSION = "1.0.0"
GAME_DESCRIPTION = "七人局阿瓦隆游戏，支持AI和玩家参与"

__all__ = [
    "Referee",
    "GAME_NAME",
    "GAME_VERSION",
    "GAME_DESCRIPTION"
]

