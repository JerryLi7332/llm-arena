# LLM Arena 后端 API 文档

---

- [基础API](#基础API)

- [游戏使用API](#游戏使用API)

---

# 基础API

## 概述

LLM Arena 是一个基于 FastAPI 构建的现代化后端服务，提供完整的用户管理、权限控制、文件管理和游戏系统功能。本文档详细描述了所有可用的 API 端点。

## 基本信息

- **项目名称**: LLM Arena
- **版本**: 0.1.0
- **框架**: FastAPI
- **数据库**: PostgreSQL (支持 SQLite 作为开发环境)
- **认证方式**: JWT Token
- **API 版本**: v1

## 基础配置

### 服务器信息
- **开发环境**: http://localhost:8000
- **API 前缀**: `/v1`
- **文档地址**: `/docs` (Swagger UI)
- **健康检查**: `/v1/base/health`

### 认证配置
- **JWT 算法**: HS256
- **访问令牌过期时间**: 4 小时
- **刷新令牌过期时间**: 7 天
- **限流策略**: 默认 200 次/天，50 次/小时

## API 端点总览

### 1. 基础模块 (`/v1/base`)

#### 认证相关

| 端点 | 方法 | 描述 | 权限要求 | 限流 |
|------|------|------|----------|------|
| `/auth/access_token` | POST | 用户登录获取 token | 无 | 5次/分钟 |
| `/refresh_token` | POST | 刷新访问令牌 | 无 | 10次/分钟 |
| `/auth/register` | POST | 用户注册 | 无 | 3次/分钟 |

#### 用户信息

| 端点 | 方法 | 描述 | 权限要求 | 限流 |
|------|------|------|----------|------|
| `/userinfo` | GET | 获取当前用户信息 | 需要认证 | 无 |
| `/health` | GET | 系统健康检查 | 无 | 无 |
| `/version` | GET | 获取API版本信息 | 无 | 无 |

### 2. 用户管理模块 (`/v1/users`)

| 端点 | 方法 | 描述 | 权限要求 | 参数 |
|------|------|------|----------|------|
| `/list` | GET | 获取用户列表 | 需要权限 | page, page_size, username, email, dept_id |
| `/get` | GET | 获取用户详情 | 需要权限 | user_id |
| `/create` | POST | 创建新用户 | 需要权限 | UserCreate |
| `/update` | POST | 更新用户信息 | 需要权限 | UserUpdate |
| `/delete` | DELETE | 删除用户 | 需要权限 | user_id |
| `/reset_password` | POST | 重置用户密码 | 需要权限 | user_id |
| `/upload_avatar` | POST | 上传用户头像 | 需要认证 | file (UploadFile) |
| `/profile` | PUT | 更新个人资料 | 需要认证 | ProfileUpdate |
| `/password` | PUT | 修改密码 | 需要认证 | UpdatePassword |
| `/avatar` | DELETE | 删除用户头像 | 需要认证 | 无 |

### 3. 角色管理模块 (`/v1/role`)

| 端点 | 方法 | 描述 | 权限要求 | 参数 |
|------|------|------|----------|------|
| `/list` | GET | 获取角色列表 | 需要权限 | page, page_size, role_name |
| `/get` | GET | 获取角色详情 | 需要权限 | role_id |
| `/create` | POST | 创建新角色 | 需要权限 | RoleCreate |
| `/update` | POST | 更新角色信息 | 需要权限 | RoleUpdate |
| `/delete` | DELETE | 删除角色 | 需要权限 | role_id |
| `/authorized` | GET | 查看角色权限 | 需要权限 | id |
| `/authorized` | POST | 更新角色权限 | 需要权限 | RoleUpdateMenusApis |

### 4. API 管理模块 (`/v1/api`)

| 端点 | 方法 | 描述 | 权限要求 | 参数 |
|------|------|------|----------|------|
| `/list` | GET | 获取API列表 | 需要权限 | page, page_size, path, summary, tags |
| `/get` | GET | 获取API详情 | 需要权限 | id |
| `/create` | POST | 创建新API | 需要权限 | ApiCreate |
| `/update` | POST | 更新API信息 | 需要权限 | ApiUpdate |
| `/delete` | DELETE | 删除API | 需要权限 | api_id |
| `/refresh` | POST | 刷新API列表 | 需要权限 | 无 |

### 5. 文件管理模块 (`/v1/files`)

| 端点 | 方法 | 描述 | 权限要求 | 参数 |
|------|------|------|----------|------|
| `/upload` | POST | 上传文件 | 需要认证 | file (UploadFile) |

### 6. 用户头像管理

#### 头像上传限制
- **支持格式**: JPG、PNG、GIF、WebP
- **文件大小**: 最大 2MB
- **权限要求**: 需要用户认证
- **返回信息**: 头像URL和成功消息

#### 个人资料更新
- **支持字段**: username、email、nickname、avatar
- **权限要求**: 需要用户认证
- **验证规则**: 遵循用户模型验证规则

### 7. 游戏系统

#### 石头剪刀布游戏
- **游戏ID**: `rock_paper_scissors`
- **版本**: 1.0.0
- **描述**: 经典的石头剪刀布游戏

#### 阿瓦隆游戏
- **游戏ID**: `avalon`
- **版本**: 1.0.0
- **描述**: 阿瓦隆桌游的在线版本

## 数据模型

### 用户模型 (User)
```python
{
    "id": int,
    "username": str,
    "email": str,
    "nickname": str,
    "avatar": str,
    "is_active": bool,
    "is_superuser": bool,
    "created_at": datetime,
    "updated_at": datetime,
    "last_login": datetime,
    "roles": list
}
```

### 用户创建模型 (UserCreate)
```python
{
    "email": str,
    "username": str,
    "password": str,
    "nickname": str,
    "avatar": str,
    "is_active": bool,
    "is_superuser": bool,
    "role_ids": list[int],
    "dept_id": int
}
```

### 用户更新模型 (UserUpdate)
```python
{
    "id": int,
    "email": str,
    "username": str,
    "nickname": str,
    "avatar": str,
    "password": str,
    "is_active": bool,
    "is_superuser": bool,
    "role_ids": list[int],
    "dept_id": int
}
```

### 头像上传响应模型 (AvatarUpload)
```python
{
    "avatar_url": str,
    "message": str
}
```

### 个人资料更新模型 (ProfileUpdate)
```python
{
    "username": str,
    "email": str,
    "nickname": str,
    "avatar": str
}
```

### 密码更新模型 (UpdatePassword)
```python
{
    "old_password": str,
    "new_password": str
}
```

### 角色模型 (Role)
```python
{
    "id": int,
    "name": str,
    "description": str,
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

### API模型 (Api)
```python
{
    "id": int,
    "path": str,
    "method": str,
    "summary": str,
    "tags": str,
    "is_active": bool
}
```

## 认证与权限

### JWT Token 结构
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "username": "用户名",
    "expires_in": 14400
}
```

### 权限依赖
- `DependAuth`: 基础认证依赖，验证用户是否已登录
- `DependPermisson`: 权限验证依赖，检查用户是否有访问特定端点的权限

### 限流策略
- **登录**: 5次/分钟
- **注册**: 3次/分钟
- **刷新令牌**: 10次/分钟
- **其他API**: 200次/天，50次/小时

## 响应格式

### 成功响应
```json
{
    "code": 200,
    "msg": "操作成功",
    "data": {...}
}
```

### 分页响应
```json
{
    "code": 200,
    "msg": "操作成功",
    "data": [...],
    "total": 100,
    "page": 1,
    "page_size": 10
}
```

### 错误响应
```json
{
    "code": 400,
    "msg": "错误信息"
}
```

## 错误代码

| 代码 | 描述 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 使用示例

### 1. 用户登录
```bash
curl -X POST "http://localhost:8000/v1/base/auth/access_token" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
```

### 2. 获取用户列表
```bash
curl -X GET "http://localhost:8000/v1/users/list?page=1&page_size=10" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. 上传文件
```bash
curl -X POST "http://localhost:8000/v1/files/upload" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -F "file=@/path/to/file.txt"
```

### 4. 上传用户头像
```bash
curl -X POST "http://localhost:8000/v1/users/upload_avatar" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -F "file=@/path/to/avatar.jpg"
```

### 5. 更新个人资料
```bash
curl -X PUT "http://localhost:8000/v1/users/profile" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "new_username",
       "email": "new_email@example.com",
       "nickname": "新昵称"
     }'
```

### 6. 删除用户头像
```bash
curl -X DELETE "http://localhost:8000/v1/users/avatar" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 开发环境设置

### 环境变量
```bash
# 数据库配置
DB_ENGINE=postgres  # 或 sqlite
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=fastapi_backend

# JWT配置
SECRET_KEY=your_secret_key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# 应用配置
APP_ENV=development
DEBUG=true
```

### 启动服务
```bash
# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
aerich upgrade

# 启动服务
uv run uvicorn src:app --reload --host 0.0.0.0 --port 8000
```

## 测试

项目包含完整的测试套件，支持以下测试类型：
- 认证测试
- API功能测试
- 数据库操作测试
- 权限验证测试

运行测试：
```bash
pytest tests/
```

## 部署

### Docker 部署
```bash
# 构建镜像
docker build -t llm-arena-backend .

# 运行容器
docker run -d -p 8000:8000 llm-arena-backend
```

### 生产环境配置
- 设置 `APP_ENV=production`
- 配置生产数据库
- 设置强密码和密钥
- 配置反向代理 (Nginx)
- 启用HTTPS

---

# 游戏使用API

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

---

# DeepSeek API

## 概述

本文档说明如何在现有FastAPI后端中集成DeepSeek API，实现AI聊天功能。

## 新增文件

### 1. 配置文件
- `src/settings/deepseek.py` - DeepSeek API配置管理

### 2. 服务层
- `src/services/deepseek_service.py` - DeepSeek API服务实现

### 3. API路由
- `src/api/v1/deepseek.py` - DeepSeek API端点

### 4. 依赖文件
- `requirements_deepseek.txt` - 新增依赖列表

## 环境变量配置

在您的 `.env` 文件中添加以下配置：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_DEFAULT_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4000
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_REQUEST_TIMEOUT=30000
DEEPSEEK_RATE_LIMIT_PER_MINUTE=60
DEEPSEEK_RATE_LIMIT_PER_HOUR=1000
DEEPSEEK_MAX_COST_PER_REQUEST=0.01
DEEPSEEK_MAX_COST_PER_DAY=1.0
```

## 安装依赖

```bash
# 安装新增依赖
pip install -r requirements_deepseek.txt

# 或者单独安装主要依赖
pip install httpx>=0.24.0
```

## API端点

集成后，您将拥有以下新的API端点：

### 1. 聊天完成
- **POST** `/api/v1/deepseek/chat`
- 功能：发送消息给DeepSeek AI并获取回复

### 2. 获取模型列表
- **GET** `/api/v1/deepseek/models`
- 功能：获取可用的DeepSeek模型

### 3. 检查API状态
- **GET** `/api/v1/deepseek/status`
- 功能：检查DeepSeek API运行状态

### 4. 获取速率限制信息
- **GET** `/api/v1/deepseek/rate-limit`
- 功能：查看当前API使用限制和成本统计

### 5. 获取配置信息
- **GET** `/api/v1/deepseek/config`
- 功能：查看当前配置（不包含敏感信息）

## 使用示例

### 1. 发送聊天消息

```bash
curl -X POST "http://localhost:8000/api/v1/deepseek/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好，请介绍一下自己"}
    ],
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### 2. 获取模型列表

```bash
curl -X GET "http://localhost:8000/api/v1/deepseek/models" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. 检查API状态

```bash
curl -X GET "http://localhost:8000/api/v1/deepseek/status" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 安全特性

### 1. 用户认证
- 所有API端点都需要有效的JWT令牌
- 使用现有的 `DependAuth` 依赖

### 2. 速率限制
- 每分钟限制：60次请求
- 每小时限制：1000次请求
- 可配置的限制参数

### 3. 成本控制
- 单次请求最大成本：$0.01
- 每日最大成本：$1.0
- 实时成本统计和限制

### 4. 输入验证
- 消息格式验证
- 参数范围验证
- 模型名称验证

## 错误处理

### 1. 自定义异常
- 使用 `CustomException` 统一错误格式
- 详细的错误信息和状态码

### 2. 常见错误
- 401: API密钥无效
- 429: 速率限制超限
- 400: 请求参数错误
- 408: 请求超时
- 500: 服务器内部错误

## 监控和日志

### 1. 日志记录
- API调用成功/失败日志
- 成本统计日志
- 错误详情日志

### 2. 性能监控
- 请求响应时间
- 速率限制使用情况
- 成本消耗统计

## 部署步骤

### 1. 代码部署
```bash
# 1. 复制新增文件到对应目录
cp src/settings/deepseek.py /path/to/your/project/src/settings/
cp src/services/deepseek_service.py /path/to/your/project/src/services/
cp src/api/v1/deepseek.py /path/to/your/project/src/api/v1/

# 2. 更新路由配置
# 编辑 src/api/v1/__init__.py 文件

# 3. 安装依赖
pip install -r requirements_deepseek.txt
```

### 2. 环境配置
```bash
# 1. 设置环境变量
export DEEPSEEK_API_KEY="sk-your-api-key"

# 2. 或者添加到 .env 文件
echo "DEEPSEEK_API_KEY=sk-your-api-key" >> .env
```

### 3. 重启服务
```bash
# 重启FastAPI服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 测试验证

### 1. 健康检查
```bash
# 检查API状态
curl -X GET "http://localhost:8000/api/v1/deepseek/status" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. 功能测试
```bash
# 测试聊天功能
curl -X POST "http://localhost:8000/api/v1/deepseek/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "测试消息"}]}'
```

### 3. 错误测试
```bash
# 测试无效令牌
curl -X GET "http://localhost:8000/api/v1/deepseek/status" \
  -H "Authorization: Bearer invalid-token"
```

## 故障排除

### 1. 常见问题

#### API密钥错误
```
错误：DeepSeek API密钥无效
解决：检查 DEEPSEEK_API_KEY 环境变量是否正确设置
```

#### 网络连接问题
```
错误：DeepSeek API网络错误
解决：检查网络连接和防火墙设置
```

#### 速率限制
```
错误：API调用频率超限
解决：等待限制重置或调整配置参数
```

### 2. 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

### 3. 配置验证
```bash
# 检查配置信息
curl -X GET "http://localhost:8000/api/v1/deepseek/config" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 性能优化

### 1. 连接池
- 使用 httpx 异步客户端
- 配置合适的超时时间

### 2. 缓存策略
- 模型列表缓存
- 状态检查缓存

### 3. 异步处理
- 所有API调用都是异步的
- 支持并发请求处理

## 扩展功能

### 1. 流式输出
- 支持 `stream=true` 参数
- 实时返回AI回复

### 2. 多模型支持
- 自动模型选择
- 模型性能对比

### 3. 成本分析
- 详细的成本统计
- 使用趋势分析

## 维护和更新

### 1. 定期检查
- API密钥有效期
- 使用量统计
- 成本控制

### 2. 版本更新
- 关注DeepSeek API更新
- 及时更新依赖包
- 测试新功能

### 3. 监控告警
- 设置成本超限告警
- 监控API可用性
- 错误率监控

## 联系支持

如果在部署过程中遇到问题，请：

1. 检查日志文件获取详细错误信息
2. 验证环境变量配置
3. 确认网络连接正常
4. 查看DeepSeek官方文档
5. 联系技术支持团队
