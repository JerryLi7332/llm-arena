# 前端集成指南

本文档说明如何完善后端和Vue前端的联系，以及如何正确配置和运行项目。

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- Node.js (版本 16+)
- Python (版本 3.8+)
- PostgreSQL 或 SQLite

### 2. 前端构建

#### 方法一：使用构建脚本（推荐）

**Linux/macOS:**
```bash
cd frontend
chmod +x build-for-backend.sh
./build-for-backend.sh
```

**Windows:**
```cmd
cd frontend
build-for-backend.bat
```

#### 方法二：手动构建

```bash
cd frontend
npm install
npm run build
```

### 3. 启动后端服务

```bash
# 安装Python依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn src:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问应用

构建完成后，访问 `http://localhost:8000` 即可看到前端应用。

## 🔧 配置说明

### 环境变量配置

在 `frontend/` 目录下创建 `.env` 文件：

```env
# API配置
VITE_API_BASE_URL=http://localhost:8000

# 应用配置
VITE_APP_TITLE=Vue FastAPI Admin
VITE_APP_DESCRIPTION=基于Vue3和FastAPI的管理系统

# 开发环境配置
VITE_DEV_SERVER_PORT=3000
VITE_DEV_SERVER_HOST=0.0.0.0

# 调试配置
VITE_ENABLE_DEBUG=true
VITE_ENABLE_DEVTOOLS=false
```

### CORS配置

后端已配置CORS支持，允许以下源访问：
- `http://localhost:3000`
- `http://localhost:8080`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8080`

如需添加其他源，请修改 `src/settings/config.py` 中的 `CORS_ORIGINS` 配置。

## 📁 项目结构

```
llm-arena/
├── frontend/                 # Vue前端项目
│   ├── src/                 # 源代码
│   ├── dist/                # 构建输出目录
│   ├── build-for-backend.sh # Linux构建脚本
│   └── build-for-backend.bat # Windows构建脚本
├── src/                     # FastAPI后端
│   ├── __init__.py          # 应用入口
│   ├── api/                 # API路由
│   └── settings/            # 配置文件
└── static/                  # 静态文件目录（已移除）
```

## 🔄 开发模式

### 前端开发

```bash
cd frontend
npm run dev
```

前端开发服务器将在 `http://localhost:3000` 启动，并自动代理API请求到后端。

### 后端开发

```bash
uvicorn src:app --host 0.0.0.0 --port 8000 --reload
```

后端API服务器将在 `http://localhost:8000` 启动。

## 🌐 路由处理

### 前端路由

后端已配置支持Vue Router的History模式：

- `/` - 首页
- `/login` - 登录页
- `/dashboard` - 仪表板
- `/admin` - 管理页面
- 其他前端路由都会返回 `index.html`

### API路由

所有API请求都以 `/api` 开头：

- `/api/v1/base/auth/login` - 登录
- `/api/v1/base/auth/register` - 注册
- `/api/v1/users/` - 用户管理
- `/api/v1/roles/` - 角色管理

## 🔐 认证机制

### JWT Token

前端使用JWT Token进行身份验证：

1. 用户登录后获取 `access_token` 和 `refresh_token`
2. 所有API请求自动携带 `Authorization: Bearer <token>` 头
3. Token过期时自动刷新
4. 刷新失败时自动跳转到登录页

### 错误处理

前端已配置完善的错误处理机制：

- 401: 未授权，自动刷新token或跳转登录
- 403: 权限不足
- 404: 资源不存在
- 422: 请求参数错误
- 429: 请求过于频繁
- 500: 服务器内部错误

## 🚀 部署说明

### 生产环境部署

1. **构建前端**
   ```bash
   cd frontend
   npm run build
   ```

2. **配置环境变量**
   - 设置 `CORS_ORIGINS` 为生产域名
   - 配置数据库连接
   - 设置 `SECRET_KEY`

3. **启动后端服务**
   ```bash
   uvicorn src:app --host 0.0.0.0 --port 8000
   ```

### Docker部署

```dockerfile
# 构建前端
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# 运行后端
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
EXPOSE 8000
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 故障排除

### 常见问题

1. **前端无法访问后端API**
   - 检查CORS配置
   - 确认后端服务正在运行
   - 检查网络连接

2. **构建失败**
   - 确保Node.js版本正确
   - 清理 `node_modules` 重新安装
   - 检查磁盘空间

3. **路由404错误**
   - 确保前端已正确构建
   - 检查 `frontend/dist/index.html` 是否存在
   - 确认后端路由配置正确

### 调试技巧

1. **前端调试**
   - 使用浏览器开发者工具
   - 检查网络请求
   - 查看控制台错误

2. **后端调试**
   - 查看服务器日志
   - 使用 `/docs` 访问API文档
   - 检查数据库连接

## 📞 技术支持

如遇到问题，请检查：

1. 项目依赖是否正确安装
2. 环境变量是否正确配置
3. 网络连接是否正常
4. 端口是否被占用

更多信息请参考项目文档或提交Issue。
