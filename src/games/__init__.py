"""
Games Package - 游戏逻辑包

包含各种游戏的具体实现，如：
- 石头剪刀布
- 阿瓦隆
- 其他游戏类型

此包提供统一的游戏接口和自动发现机制
"""

import os
import importlib
from typing import Dict, Type, Any

# 游戏注册表
GAME_REGISTRY: Dict[str, Dict[str, Any]] = {}

def _discover_games():
    """自动发现并注册所有游戏"""
    current_dir = os.path.dirname(__file__)
    
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        
        # 检查是否是目录且包含__init__.py文件
        if (os.path.isdir(item_path) and 
            os.path.exists(os.path.join(item_path, "__init__.py")) and
            not item.startswith("_")):
            
            try:
                # 动态导入游戏模块
                module = importlib.import_module(f".{item}", package=__name__)
                
                # 获取游戏信息
                game_name = getattr(module, "GAME_NAME", item)
                game_version = getattr(module, "GAME_VERSION", "1.0.0")
                game_description = getattr(module, "GAME_DESCRIPTION", "")
                referee_class = getattr(module, "Referee", None)
                
                # 注册游戏
                GAME_REGISTRY[item] = {
                    "name": game_name,
                    "version": game_version,
                    "description": game_description,
                    "referee": referee_class,
                    "module": module
                }
                
            except ImportError as e:
                print(f"警告: 无法导入游戏模块 {item}: {e}")
            except Exception as e:
                print(f"警告: 游戏模块 {item} 注册失败: {e}")

# 自动发现游戏
_discover_games()

def get_game(game_id: str) -> Dict[str, Any]:
    """获取指定游戏的信息"""
    return GAME_REGISTRY.get(game_id)

def get_all_games() -> Dict[str, Dict[str, Any]]:
    """获取所有已注册游戏的信息"""
    return GAME_REGISTRY.copy()

def get_game_referee(game_id: str):
    """获取指定游戏的裁判类"""
    game_info = GAME_REGISTRY.get(game_id)
    return game_info.get("referee") if game_info else None

def list_available_games() -> list:
    """列出所有可用的游戏ID"""
    return list(GAME_REGISTRY.keys())

# 为了向后兼容，仍然导出Referee类
# 但建议使用get_game_referee()函数来获取特定游戏的裁判类
try:
    from .rock_paper_scissors.referee import Referee as RockPaperScissorsReferee
    from .avalon.referee import Referee as AvalonReferee
except ImportError:
    RockPaperScissorsReferee = None
    AvalonReferee = None

__all__ = [
    # 游戏注册系统
    "GAME_REGISTRY",
    "get_game",
    "get_all_games", 
    "get_game_referee",
    "list_available_games",
    
    # 向后兼容的导出
    "RockPaperScissorsReferee",
    "AvalonReferee",
]

