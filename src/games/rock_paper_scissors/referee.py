"""
Rock Paper Scissors Game Referee - 石头剪刀布游戏裁判

负责：
- 游戏规则验证
- 胜负判定
- 结果计算
"""

import logging
import random
from typing import Dict, List, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class Move(Enum):
    """游戏动作枚举"""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class GameResult(Enum):
    """游戏结果枚举"""
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
    ERROR = "error"


class Referee:
    """石头剪刀布游戏裁判"""

    def __init__(self):
        """初始化裁判"""
        self.valid_moves = [move.value for move in Move]
        self.win_conditions = {
            Move.ROCK.value: Move.SCISSORS.value,      # 石头胜剪刀
            Move.PAPER.value: Move.ROCK.value,         # 布胜石头
            Move.SCISSORS.value: Move.PAPER.value      # 剪刀胜布
        }

    def validate_move(self, move: str) -> bool:
        """
        验证玩家动作是否有效

        Args:
            move: 玩家动作

        Returns:
            bool: 是否有效
        """
        return move in self.valid_moves

    def determine_winner(self, move1: str, move2: str) -> Tuple[GameResult, GameResult]:
        """
        判定两个玩家之间的胜负

        Args:
            move1: 玩家1的动作
            move2: 玩家2的动作

        Returns:
            Tuple[GameResult, GameResult]: (玩家1结果, 玩家2结果)
        """
        try:
            # 验证动作
            if not self.validate_move(move1) or not self.validate_move(move2):
                logger.error(f"无效的动作: {move1} vs {move2}")
                return GameResult.ERROR, GameResult.ERROR

            # 平局
            if move1 == move2:
                return GameResult.DRAW, GameResult.DRAW

            # 判定胜负
            if self.win_conditions[move1] == move2:
                # 玩家1获胜
                return GameResult.WIN, GameResult.LOSS
            else:
                # 玩家2获胜
                return GameResult.LOSS, GameResult.WIN

        except Exception as e:
            logger.error(f"判定胜负时出错: {e}")
            return GameResult.ERROR, GameResult.ERROR

    def start_match(self, player1_move: str, player2_move: str) -> Dict[str, any]:
        """
        开始一场比赛

        Args:
            player1_move: 玩家1的动作
            player2_move: 玩家2的动作

        Returns:
            Dict: 比赛结果
        """
        try:
            logger.info(f"开始比赛: {player1_move} vs {player2_move}")

            # 判定胜负
            result1, result2 = self.determine_winner(
                player1_move, player2_move)

            if result1 == GameResult.ERROR:
                return {
                    "success": False,
                    "error": "无效的动作",
                    "player1_result": None,
                    "player2_result": None
                }

            # 构建结果
            match_result = {
                "success": True,
                "player1_move": player1_move,
                "player2_move": player2_move,
                "player1_result": result1.value,
                "player2_result": result2.value,
                "winner": None,
                "is_draw": result1 == GameResult.DRAW
            }

            # 确定获胜者
            if result1 == GameResult.WIN:
                match_result["winner"] = "player1"
            elif result2 == GameResult.WIN:
                match_result["winner"] = "player2"

            logger.info(f"比赛结果: {match_result}")
            return match_result

        except Exception as e:
            logger.error(f"开始比赛时出错: {e}")
            return {
                "success": False,
                "error": str(e),
                "player1_result": None,
                "player2_result": None
            }

    def generate_random_move(self) -> str:
        """
        生成随机动作（用于AI或测试）

        Returns:
            str: 随机动作
        """
        return random.choice(self.valid_moves)

    def get_move_name(self, move: str) -> str:
        """
        获取动作的中文名称

        Args:
            move: 动作值

        Returns:
            str: 中文名称
        """
        move_names = {
            Move.ROCK.value: "石头",
            Move.PAPER.value: "布",
            Move.SCISSORS.value: "剪刀"
        }
        return move_names.get(move, "未知")

    def get_result_description(self, result: GameResult) -> str:
        """
        获取结果的中文描述

        Args:
            result: 游戏结果

        Returns:
            str: 中文描述
        """
        result_descriptions = {
            GameResult.WIN: "胜利",
            GameResult.LOSS: "失败",
            GameResult.DRAW: "平局",
            GameResult.ERROR: "错误"
        }
        return result_descriptions.get(result, "未知")

    def log_match_summary(self, match_result: Dict[str, any]):
        """
        记录比赛摘要

        Args:
            match_result: 比赛结果
        """
        if not match_result.get("success"):
            logger.warning(f"比赛失败: {match_result.get('error', '未知错误')}")
            return

        p1_move = self.get_move_name(match_result["player1_move"])
        p2_move = self.get_move_name(match_result["player2_move"])
        p1_result = self.get_result_description(
            GameResult(match_result["player1_result"]))
        p2_result = self.get_result_description(
            GameResult(match_result["player2_result"]))

        if match_result["is_draw"]:
            logger.info(f"比赛结束: {p1_move} vs {p2_move} = 平局")
        else:
            winner = "玩家1" if match_result["winner"] == "player1" else "玩家2"
            logger.info(f"比赛结束: {p1_move} vs {p2_move} = {winner}获胜")
