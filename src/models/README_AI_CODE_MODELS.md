# AI代码相关模型说明

## 概述

本文档说明了LLM Arena项目中AI代码相关的数据模型设计。这些模型支持用户上传、管理和使用AI代码，以及相关的统计、评论、标签等功能。

## 核心模型

### 1. AICode - AI代码主模型

**功能**: 存储用户上传的AI代码的基本信息

**主要字段**:
- `user_id`: 用户ID，关联到用户表
- `name`: AI代码名称
- `file_path`: 文件存储路径
- `file_name`: 原始文件名
- `file_size`: 文件大小（字节）
- `file_hash`: 文件哈希值，用于文件完整性验证
- `game_type`: 游戏类型（如：rock_paper_scissors, avalon）
- `description`: 代码描述
- `version`: 版本号
- `is_active`: 是否激活状态
- `last_used`: 最后使用时间
- `win_count/loss_count/draw_count`: 胜负平次数
- `total_games`: 总游戏次数
- `win_rate`: 胜率
- `elo_score`: ELO评分
- `tags`: 标签列表（JSON格式）
- `config`: 配置参数（JSON格式）
- `is_public`: 是否公开
- `download_count`: 下载次数
- `rating`: 评分
- `review_count`: 评论数量

**辅助方法**:
- `update_win_rate()`: 更新胜率
- `add_game_result(result)`: 添加游戏结果
- `get_file_extension()`: 获取文件扩展名
- `is_code_file()`: 判断是否为代码文件
- `is_archive_file()`: 判断是否为压缩文件
- `get_file_size_display()`: 获取文件大小的可读显示
- `can_be_activated()`: 判断是否可以激活
- `get_status_display()`: 获取状态显示

**索引**:
- 用户ID + 游戏类型
- 游戏类型 + 激活状态
- 游戏类型 + ELO评分
- 公开状态 + 评分

### 2. GameStats - 游戏统计模型

**功能**: 记录用户在特定游戏中的统计数据

**主要字段**:
- `user_id`: 用户ID
- `game_type`: 游戏类型
- `ranking_id`: 排行榜ID
- `elo_score`: ELO评分
- `wins/losses/draws`: 胜负平次数
- `games_played`: 总游戏次数
- `cancelled_games`: 取消的游戏次数
- `win_rate`: 胜率
- `best_elo`: 最高ELO分数
- `current_streak`: 当前连胜/连败
- `longest_win_streak`: 最长连胜
- `longest_lose_streak`: 最长连败
- `last_game_at`: 最后游戏时间
- `total_play_time`: 总游戏时间（秒）
- `average_game_time`: 平均游戏时间（秒）

**索引**:
- 游戏类型 + ELO评分
- 游戏类型 + 胜率
- 用户ID + 游戏类型

### 3. AICodeReview - AI代码评论模型

**功能**: 存储用户对AI代码的评论和评分

**主要字段**:
- `ai_code_id`: AI代码ID
- `user_id`: 评论用户ID
- `rating`: 评分(1-5)
- `comment`: 评论内容
- `is_helpful`: 是否有帮助
- `helpful_count`: 有帮助的数量
- `reply_to`: 回复的评论ID（支持嵌套评论）

**索引**:
- AI代码ID + 评分
- 用户ID + 创建时间

### 4. AICodeTag - AI代码标签模型

**功能**: 管理AI代码的标签系统

**主要字段**:
- `name`: 标签名称（唯一）
- `description`: 标签描述
- `color`: 标签颜色（十六进制）
- `usage_count`: 使用次数
- `is_system`: 是否系统标签

### 5. AICodeTagRelation - 标签关系模型

**功能**: 建立AI代码和标签的多对多关系

**主要字段**:
- `ai_code_id`: AI代码ID
- `tag_id`: 标签ID

**约束**: 唯一约束确保不会重复关联

### 6. AICodeVersion - AI代码版本模型

**功能**: 管理AI代码的版本历史

**主要字段**:
- `ai_code_id`: AI代码ID
- `version_number`: 版本号
- `file_path`: 文件路径
- `file_name`: 文件名
- `file_size`: 文件大小
- `file_hash`: 文件哈希
- `changelog`: 更新日志
- `is_stable`: 是否稳定版本
- `download_count`: 下载次数

**约束**: AI代码ID + 版本号的唯一约束

### 7. AICodeDownload - 下载记录模型

**功能**: 记录AI代码的下载历史

**主要字段**:
- `ai_code_id`: AI代码ID
- `user_id`: 下载用户ID
- `ip_address`: IP地址
- `user_agent`: 用户代理
- `download_type`: 下载类型（direct, api等）

## 设计特点

### 1. 性能优化
- 合理的索引设计，支持常用查询场景
- 复合索引优化多字段查询
- 统计字段预计算，减少实时计算开销

### 2. 扩展性
- JSON字段支持灵活的配置和标签
- 版本管理支持代码迭代
- 标签系统支持分类和搜索

### 3. 数据完整性
- 外键约束确保数据一致性
- 唯一约束防止重复数据
- 文件哈希验证文件完整性

### 4. 用户体验
- 详细的统计信息
- 评分和评论系统
- 下载历史追踪

## 使用场景

### 1. AI代码管理
- 用户上传AI代码
- 版本控制和更新
- 激活/停用管理

### 2. 游戏对战
- 选择AI代码参与对战
- 记录对战结果
- 更新ELO评分和统计

### 3. 社区功能
- 代码分享和下载
- 评分和评论
- 标签分类

### 4. 数据分析
- 用户行为分析
- 代码质量评估
- 游戏平衡性分析

## 注意事项

1. **文件存储**: 文件路径需要根据实际存储方案调整
2. **哈希算法**: 文件哈希建议使用SHA-256等安全算法
3. **JSON字段**: 需要验证JSON数据的格式和大小
4. **索引维护**: 定期分析索引使用情况，优化查询性能
5. **数据清理**: 考虑数据归档和清理策略

## 未来扩展

1. **AI代码测试**: 添加自动化测试功能
2. **代码分析**: 集成代码质量分析工具
3. **性能监控**: 添加AI代码性能指标
4. **协作功能**: 支持多人协作开发
5. **API接口**: 提供标准化的AI代码接口
