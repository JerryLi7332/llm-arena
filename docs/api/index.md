# LLM Arena 后端 API 文档

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

### 6. 游戏系统

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
    "is_active": bool,
    "is_superuser": bool,
    "created_at": datetime,
    "updated_at": datetime,
    "last_login": datetime
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
