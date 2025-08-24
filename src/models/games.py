from tortoise import fields
from .base import BaseModel, TimestampMixin


class GameStats(BaseModel, TimestampMixin):
    """游戏统计模型"""
    user_id = fields.IntField(description="用户ID", index=True)
    game_type = fields.CharField(max_length=50, description="游戏类型", index=True)
    ranking_id = fields.IntField(default=0, description="排行榜ID", index=True)
    elo_score = fields.IntField(default=1200, description="ELO评分")
    wins = fields.IntField(default=0, description="胜利场次")
    losses = fields.IntField(default=0, description="失败场次")
    draws = fields.IntField(default=0, description="平局场次")
    games_played = fields.IntField(default=0, description="总游戏场次")
    cancelled_games = fields.IntField(default=0, description="取消的游戏场次")
    win_rate = fields.FloatField(default=0.0, description="胜率")
    best_elo = fields.IntField(default=1200, description="最高ELO分数")
    current_streak = fields.IntField(default=0, description="当前连胜/连败")
    longest_win_streak = fields.IntField(default=0, description="最长连胜")
    longest_lose_streak = fields.IntField(default=0, description="最长连败")
    last_game_at = fields.DatetimeField(null=True, description="最后游戏时间")
    total_play_time = fields.IntField(default=0, description="总游戏时间（秒）")
    average_game_time = fields.FloatField(default=0.0, description="平均游戏时间（秒）")
    
    class Meta:
        table = "game_stats"
        unique_together = (("user_id", "game_type", "ranking_id"),)
        indexes = [
            ("game_type", "elo_score"),
            ("game_type", "win_rate"),
            ("user_id", "game_type"),
        ]


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
    battle_id = fields.IntField(description="对战ID", index=True)
    user_id = fields.IntField(description="用户ID", index=True)
    selected_ai_code_id = fields.IntField(null=True, description="选择的AI代码ID")
    position = fields.IntField(description="玩家位置(1-7)")
    initial_elo = fields.IntField(null=True, description="初始ELO分数")
    elo_change = fields.IntField(default=0, description="ELO变化")
    outcome = fields.CharField(max_length=20, null=True, description="对战结果")
    join_time = fields.DatetimeField(auto_now_add=True, description="加入时间")
    
    class Meta:
        table = "battle_player"
        unique_together = (("battle_id", "position"), ("battle_id", "user_id"))


class AICodeReview(BaseModel, TimestampMixin):
    """AI代码评论模型"""
    ai_code_id = fields.IntField(description="AI代码ID", index=True)
    user_id = fields.IntField(description="评论用户ID", index=True)
    rating = fields.IntField(description="评分(1-5)")
    comment = fields.TextField(description="评论内容")
    is_helpful = fields.BooleanField(default=False, description="是否有帮助")
    helpful_count = fields.IntField(default=0, description="有帮助的数量")
    reply_to = fields.IntField(null=True, description="回复的评论ID")
    
    class Meta:
        table = "ai_code_review"
        indexes = [
            ("ai_code_id", "rating"),
            ("user_id", "created_at"),
        ]


class AICodeTag(BaseModel, TimestampMixin):
    """AI代码标签模型"""
    name = fields.CharField(max_length=50, description="标签名称", unique=True)
    description = fields.TextField(null=True, description="标签描述")
    color = fields.CharField(max_length=7, description="标签颜色", default="#666666")
    usage_count = fields.IntField(default=0, description="使用次数")
    is_system = fields.BooleanField(default=False, description="是否系统标签")
    
    class Meta:
        table = "ai_code_tag"


class AICodeTagRelation(BaseModel, TimestampMixin):
    """AI代码标签关系模型"""
    ai_code_id = fields.IntField(description="AI代码ID", index=True)
    tag_id = fields.IntField(description="标签ID", index=True)
    
    class Meta:
        table = "ai_code_tag_relation"
        unique_together = (("ai_code_id", "tag_id"),)


class AICodeVersion(BaseModel, TimestampMixin):
    """AI代码版本模型"""
    ai_code_id = fields.IntField(description="AI代码ID", index=True)
    version_number = fields.IntField(description="版本号")
    file_path = fields.CharField(max_length=500, description="文件路径")
    file_name = fields.CharField(max_length=255, description="文件名")
    file_size = fields.IntField(description="文件大小")
    file_hash = fields.CharField(max_length=64, description="文件哈希")
    changelog = fields.TextField(null=True, description="更新日志")
    is_stable = fields.BooleanField(default=True, description="是否稳定版本")
    download_count = fields.IntField(default=0, description="下载次数")
    
    class Meta:
        table = "ai_code_version"
        unique_together = (("ai_code_id", "version_number"),)
        indexes = [
            ("ai_code_id", "created_at"),
        ]


class AICodeDownload(BaseModel, TimestampMixin):
    """AI代码下载记录模型"""
    ai_code_id = fields.IntField(description="AI代码ID", index=True)
    user_id = fields.IntField(description="下载用户ID", index=True)
    ip_address = fields.CharField(max_length=45, description="IP地址", null=True)
    user_agent = fields.TextField(null=True, description="用户代理")
    download_type = fields.CharField(max_length=20, description="下载类型", default="direct")
    
    class Meta:
        table = "ai_code_download"
        indexes = [
            ("ai_code_id", "created_at"),
            ("user_id", "created_at"),
        ]


class AICode(BaseModel, TimestampMixin):
    """AI代码模型"""
    user_id = fields.IntField(description="用户ID", index=True)
    name = fields.CharField(max_length=100, description="AI代码名称")
    file_path = fields.CharField(max_length=500, description="AI代码文件路径")
    file_name = fields.CharField(max_length=255, description="原始文件名")
    file_size = fields.IntField(description="文件大小（字节）")
    file_hash = fields.CharField(max_length=64, description="文件哈希值", null=True)
    game_type = fields.CharField(max_length=50, description="游戏类型", index=True)
    description = fields.TextField(null=True, description="AI代码描述")
    version = fields.IntField(default=1, description="版本号")
    is_active = fields.BooleanField(default=False, description="是否激活", index=True)
    last_used = fields.DatetimeField(null=True, description="最后使用时间")
    win_count = fields.IntField(default=0, description="胜利次数")
    loss_count = fields.IntField(default=0, description="失败次数")
    draw_count = fields.IntField(default=0, description="平局次数")
    total_games = fields.IntField(default=0, description="总游戏次数")
    win_rate = fields.FloatField(default=0.0, description="胜率")
    elo_score = fields.IntField(default=1200, description="ELO评分")
    tags = fields.JSONField(null=True, description="标签列表")
    config = fields.JSONField(null=True, description="配置参数")
    is_public = fields.BooleanField(default=False, description="是否公开")
    download_count = fields.IntField(default=0, description="下载次数")
    rating = fields.FloatField(default=0.0, description="评分")
    review_count = fields.IntField(default=0, description="评论数量")
    
    class Meta:
        table = "ai_code"
        indexes = [
            ("user_id", "game_type"),
            ("game_type", "is_active"),
            ("game_type", "elo_score"),
            ("is_public", "rating"),
        ]
    
    def update_win_rate(self):
        """更新胜率"""
        if self.total_games > 0:
            self.win_rate = round(self.win_count / self.total_games, 4)
        else:
            self.win_rate = 0.0
    
    def add_game_result(self, result):
        """添加游戏结果"""
        self.total_games += 1
        if result == "win":
            self.win_count += 1
        elif result == "loss":
            self.loss_count += 1
        elif result == "draw":
            self.draw_count += 1
        self.update_win_rate()
    
    def get_file_extension(self):
        """获取文件扩展名"""
        if self.file_name:
            return self.file_name.split('.')[-1].lower()
        return ""
    
    def is_code_file(self):
        """判断是否为代码文件"""
        code_extensions = ['py', 'js', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'php', 'rb']
        return self.get_file_extension() in code_extensions
    
    def is_archive_file(self):
        """判断是否为压缩文件"""
        archive_extensions = ['zip', 'rar', '7z', 'tar', 'gz', 'bz2']
        return self.get_file_extension() in archive_extensions
    
    def get_file_size_display(self):
        """获取文件大小的可读显示"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def can_be_activated(self):
        """判断是否可以激活"""
        return self.is_code_file() or self.is_archive_file()
    
    def get_status_display(self):
        """获取状态显示"""
        if self.is_active:
            return "已激活"
        elif self.can_be_activated():
            return "可激活"
        else:
            return "不可激活"
