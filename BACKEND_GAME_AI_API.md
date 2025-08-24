# 后端游戏AI API 实现说明

## 概述

本文档描述了为LLM Arena项目新创建的游戏AI代码管理API的实现细节。这些API允许用户为不同的游戏上传、管理和使用AI代码。

## 新增的API接口

### 1. 游戏AI代码管理

#### 获取AI代码列表
- **接口**: `GET /api/v1/games/ai-codes/{game_type}`
- **功能**: 获取指定游戏类型的AI代码列表
- **参数**: 
  - `game_type`: 游戏类型 (rock_paper_scissors, avalon)
- **认证**: 需要用户登录
- **返回**: AI代码列表

#### 上传AI代码
- **接口**: `POST /api/v1/games/ai-codes/{game_type}/upload`
- **功能**: 上传游戏AI代码
- **参数**: 
  - `game_type`: 游戏类型
  - `name`: AI代码名称
  - `description`: AI代码描述（可选）
  - `file`: 代码文件
- **认证**: 需要用户登录
- **返回**: 上传成功的AI代码信息

#### 激活AI代码
- **接口**: `POST /api/v1/games/ai-codes/{ai_code_id}/activate`
- **功能**: 激活指定的AI代码
- **参数**: 
  - `ai_code_id`: AI代码ID
- **认证**: 需要用户登录
- **返回**: 激活后的AI代码信息

#### 下载AI代码
- **接口**: `GET /api/v1/games/ai-codes/{ai_code_id}/download`
- **功能**: 下载AI代码文件
- **参数**: 
  - `ai_code_id`: AI代码ID
- **认证**: 需要用户登录
- **返回**: 文件内容

#### 获取AI代码详情
- **接口**: `GET /api/v1/games/ai-codes/{ai_code_id}`
- **功能**: 获取AI代码详情
- **参数**: 
  - `ai_code_id`: AI代码ID
- **认证**: 需要用户登录
- **返回**: AI代码详情

#### 更新AI代码信息
- **接口**: `PUT /api/v1/games/ai-codes/{ai_code_id}`
- **功能**: 更新AI代码信息
- **参数**: 
  - `ai_code_id`: AI代码ID
  - `ai_code_update`: 更新的AI代码信息
- **认证**: 需要用户登录
- **返回**: 更新后的AI代码信息

#### 删除AI代码
- **接口**: `DELETE /api/v1/games/ai-codes/{ai_code_id}`
- **功能**: 删除AI代码
- **参数**: 
  - `ai_code_id`: AI代码ID
- **认证**: 需要用户登录
- **返回**: 删除结果

## 新增的文件和模块

### 1. API路由文件

#### `src/api/v1/games/__init__.py`
- 游戏模块的初始化文件
- 注册AI代码管理路由

#### `src/api/v1/games/ai_codes.py`
- AI代码管理的核心API实现
- 包含所有CRUD操作
- 文件上传、下载、删除等操作

### 2. 数据模型

#### `src/models/games.py`
- 已存在的游戏相关模型
- 包含AICode、GameStats、Battle等模型
- 支持AI代码的完整生命周期管理

### 3. 数据Schema

#### `src/schemas/games.py`
- 游戏相关的Pydantic schema
- 用于API请求和响应的数据验证
- 包含所有必要的字段和验证规则

### 4. 服务层

#### `src/services/file_service.py`
- 扩展了文件服务
- 新增了`download_file`和`delete_file`方法
- 支持AI代码文件的完整管理

### 5. 核心CRUD操作

#### `src/core/crud.py`
- 扩展了CRUD基类
- 新增了`get_multi`、`update_multi`等方法
- 支持批量操作和复杂查询

## 技术实现细节

### 1. 文件上传处理

```python
# 文件类型验证
allowed_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.zip', '.rar']
file_ext = os.path.splitext(file.filename)[1].lower()
if file_ext not in allowed_extensions:
    raise HTTPException(status_code=400, detail="不支持的文件类型")

# 文件大小验证 (10MB)
max_size = 10 * 1024 * 1024
if file.size > max_size:
    raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
```

### 2. 权限控制

```python
# 验证所有权
if ai_code.user_id != current_user_id:
    raise HTTPException(status_code=403, detail="无权限操作此AI代码")
```

### 3. 激活逻辑

```python
# 先停用同游戏类型的其他AI代码
await CRUD(AICode).update_multi(
    {"user_id": current_user_id, "game_type": ai_code.game_type},
    {"is_active": False}
)

# 激活当前AI代码
updated_ai_code = await CRUD(AICode).update(
    ai_code_id,
    {"is_active": True}
)
```

## 数据库模型说明

### AICode模型字段

- `user_id`: 用户ID
- `name`: AI代码名称
- `file_path`: 文件路径
- `file_name`: 原始文件名
- `file_size`: 文件大小
- `file_hash`: 文件哈希值
- `game_type`: 游戏类型
- `description`: 描述
- `version`: 版本号
- `is_active`: 是否激活
- `last_used`: 最后使用时间
- `win_count`: 胜利次数
- `loss_count`: 失败次数
- `draw_count`: 平局次数
- `total_games`: 总游戏次数
- `win_rate`: 胜率
- `elo_score`: ELO评分
- `tags`: 标签列表
- `config`: 配置参数
- `is_public`: 是否公开
- `download_count`: 下载次数
- `rating`: 评分
- `review_count`: 评论数量

## 安全特性

### 1. 文件安全
- 文件类型白名单验证
- 文件大小限制
- 危险文件类型检测
- 安全的文件名生成

### 2. 权限控制
- 用户认证验证
- 资源所有权验证
- 操作权限检查

### 3. 数据验证
- 输入参数验证
- 文件内容验证
- 业务逻辑验证

## 使用示例

### 1. 上传AI代码

```bash
curl -X POST "http://localhost:8000/api/v1/games/ai-codes/rock_paper_scissors/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "name=智能石头剪刀布AI" \
  -F "description=基于机器学习的AI策略" \
  -F "file=@ai_code.py"
```

### 2. 获取AI代码列表

```bash
curl -X GET "http://localhost:8000/api/v1/games/ai-codes/rock_paper_scissors" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. 激活AI代码

```bash
curl -X POST "http://localhost:8000/api/v1/games/ai-codes/1/activate" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 测试

### 1. 运行测试脚本

```bash
python test_game_ai_api.py
```

### 2. 测试覆盖范围

- 用户认证
- 文件上传
- 文件下载
- 文件删除
- AI代码管理
- 权限验证

## 部署注意事项

### 1. 文件存储
- 确保uploads目录有写入权限
- 配置适当的文件大小限制
- 考虑使用云存储服务

### 2. 数据库
- 运行数据库迁移
- 创建必要的索引
- 配置适当的连接池

### 3. 安全配置
- 配置JWT密钥
- 设置CORS策略
- 配置防火墙规则

## 未来扩展

### 1. 功能扩展
- AI代码版本管理
- 代码执行环境
- 性能测试功能
- 排行榜系统

### 2. 技术改进
- 异步文件处理
- 缓存机制
- 监控和日志
- 性能优化

## 故障排除

### 1. 常见问题

#### 文件上传失败
- 检查文件大小限制
- 验证文件类型
- 确认存储权限

#### 认证失败
- 检查JWT配置
- 验证用户凭据
- 确认token有效期

#### 数据库错误
- 检查数据库连接
- 验证模型定义
- 确认迁移状态

### 2. 日志查看

```bash
# 查看应用日志
tail -f logs/backend_*.log

# 查看错误日志
tail -f logs/backend_error_*.log
```

## 总结

新创建的游戏AI API提供了完整的AI代码管理功能，包括：

1. **完整的CRUD操作**: 创建、读取、更新、删除AI代码
2. **文件管理**: 上传、下载、删除代码文件
3. **权限控制**: 用户认证和资源所有权验证
4. **安全特性**: 文件类型验证、大小限制、危险文件检测
5. **业务逻辑**: 激活/停用逻辑、游戏类型管理

这些API为前端提供了强大的后端支持，使用户能够轻松管理他们的游戏AI代码。
