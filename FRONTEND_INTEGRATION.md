# 前端集成部署指南

本项目已成功将前端HTML界面集成到FastAPI后端中，实现了完整的全栈应用。

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 pip 安装
pip install -e .

# 或使用 uv 安装（推荐）
uv sync
```

### 2. 配置环境

创建 `.env` 文件：

```env
# 数据库配置
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=fastapi_backend

# JWT配置
SECRET_KEY=your_secret_key_here

# 应用配置
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### 3. 启动应用

```bash
# 使用启动脚本
python run.py

# 或直接使用 uvicorn
uvicorn src:app --host 0.0.0.0 --port 8000 --reload
```

## 📱 访问地址

启动后，您可以通过以下地址访问：

- **前端界面**: http://localhost:8000/
- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **API端点**: http://localhost:8000/api/

## 🎨 前端功能

### 主要功能模块

1. **用户认证**
   - 登录/登出
   - JWT Token 管理
   - 自动刷新 Token

2. **用户管理**
   - 用户列表查看
   - 创建新用户
   - 编辑用户信息
   - 删除用户

3. **角色管理**
   - 角色列表查看
   - 角色权限管理

4. **API管理**
   - API列表查看
   - API状态监控

5. **文件上传**
   - 拖拽上传
   - 文件预览
   - 上传进度显示

### 技术特性

- **响应式设计**: 适配桌面和移动设备
- **现代化UI**: 使用CSS变量和现代设计语言
- **实时通知**: 操作结果实时反馈
- **数据缓存**: 智能缓存减少请求
- **错误处理**: 完善的错误处理机制

## 🔧 开发指南

### 前端文件结构

```
static/
└── index.html          # 主前端文件
```

### 自定义前端

1. **修改样式**: 编辑 `static/index.html` 中的 `<style>` 部分
2. **添加功能**: 在 JavaScript 部分添加新的功能模块
3. **API集成**: 在 `API_URLS` 对象中添加新的API端点

### 添加新的API端点

1. 在 `src/api/v1/` 目录下创建新的API模块
2. 在 `src/__init__.py` 中注册路由
3. 在前端 `API_URLS` 中添加对应的端点

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t fastapi-frontend .
```

### 运行容器

```bash
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -e DB_HOST=your_db_host \
  -e DB_PASSWORD=your_password \
  fastapi-frontend
```

## 🔒 安全配置

### 生产环境配置

1. **修改默认密码**:
   ```env
   SWAGGER_UI_USERNAME=admin
   SWAGGER_UI_PASSWORD=your_secure_password
   ```

2. **配置HTTPS**:
   ```bash
   # 使用 nginx 反向代理
   # 或配置 uvicorn SSL
   uvicorn src:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
   ```

3. **环境变量**:
   ```env
   APP_ENV=production
   DEBUG=false
   ```

## 📊 监控和日志

### 日志配置

应用使用 `loguru` 进行日志管理，日志文件位于 `app/logs/` 目录。

### 性能监控

- 使用 `slowapi` 进行限流
- Redis 缓存支持
- 数据库连接池优化

## 🛠️ 故障排除

### 常见问题

1. **前端无法访问**
   - 检查 `static/index.html` 文件是否存在
   - 确认静态文件挂载配置正确

2. **API请求失败**
   - 检查数据库连接
   - 确认JWT Token配置
   - 查看应用日志

3. **文件上传失败**
   - 检查文件上传目录权限
   - 确认文件大小限制

### 调试模式

```bash
# 启用详细日志
export LOG_LEVEL=DEBUG
python run.py
```

## 📝 更新日志

### v1.0.0
- ✅ 集成前端HTML界面
- ✅ 实现用户认证系统
- ✅ 添加文件上传功能
- ✅ 完善错误处理机制
- ✅ 支持响应式设计

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。 