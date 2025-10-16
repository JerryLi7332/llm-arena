# 🐳 Docker 部署指南

> LLM Arena 项目的 Docker 容器化部署方案

## 📋 目录

- [快速开始](#快速开始)
- [架构说明](#架构说明)
- [配置说明](#配置说明)
- [启动脚本](#启动脚本)
- [常见问题](#常见问题)
- [高级配置](#高级配置)

---

## 🚀 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 2GB+ 可用内存

### 三步部署

#### 1. 配置环境变量

```bash
# Windows
copy config\docker\.env.docker .env

# Linux/Mac
cp config/docker/.env.docker .env
```

编辑 `.env` 文件，**必须修改**以下配置：

```bash
SECRET_KEY=your_generated_secret_key_here  # 使用 openssl rand -hex 32 生成
DEEPSEEK_API_KEY=sk-your-api-key          # DeepSeek API 密钥
DB_PASSWORD=your_secure_password           # 数据库密码
```

#### 2. 启动服务

```bash
# Windows
.\scripts\docker-start.bat

# Linux/Mac
chmod +x scripts/docker-start.sh
./scripts/docker-start.sh
```

选择 **[1] 首次部署**

#### 3. 访问应用

- 🌐 后端 API: <http://localhost:8000>
- 📚 API 文档: <http://localhost:8000/docs>
- 🎨 前端页面: <http://localhost> (如果启用 Nginx)

---

## 🏗️ 架构说明

### 服务组成

```text
┌─────────────────────────────────────┐
│         Docker Network              │
│                                     │
│  ┌─────────┐    ┌──────────┐      │
│  │  Nginx  │───▶│ Backend  │      │
│  │  (80)   │    │  (8000)  │      │
│  └─────────┘    └─────┬────┘      │
│                       │            │
│           ┌───────────┴───────┐   │
│           │                   │   │
│      ┌────▼────┐      ┌──────▼───┐│
│      │Postgres │      │  Redis   ││
│      │ (5432)  │      │  (6379)  ││
│      └─────────┘      └──────────┘│
└─────────────────────────────────────┘
```

### 服务说明

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| backend | 本地构建 | 8000 | FastAPI 后端 |
| postgres | postgres:15-alpine | 5432 | PostgreSQL 数据库 |
| redis | redis:7-alpine | 6379 | Redis 缓存 |
| nginx | nginx:alpine | 80, 443 | 反向代理 (可选) |

### 数据持久化

- `postgres_data` - 数据库数据
- `redis_data` - Redis 数据
- `./uploads` - 用户上传文件
- `./logs` - 应用日志

---

## ⚙️ 配置说明

### 目录结构

```text
config/
├── docker/
│   ├── docker-compose.yml  # 服务编排配置
│   ├── Dockerfile          # 后端镜像构建
│   ├── .dockerignore       # Docker 忽略文件
│   └── .env.docker         # 环境配置模板
└── nginx/
    ├── nginx.conf          # Nginx 主配置
    └── conf.d/
        └── default.conf    # 反向代理配置
```

### 环境变量配置

#### 必须配置

```bash
# 应用安全
SECRET_KEY=                  # JWT 密钥，使用 openssl rand -hex 32 生成

# AI 服务
DEEPSEEK_API_KEY=           # DeepSeek API 密钥

# 数据库
DB_PASSWORD=                # PostgreSQL 密码
```

#### 可选配置

```bash
# 数据库
DB_USER=postgres            # 数据库用户名
DB_NAME=llm_arena          # 数据库名称
DB_PORT=5432               # 数据库端口

# Redis
REDIS_PASSWORD=            # Redis 密码（留空则不设密码）
REDIS_PORT=6379            # Redis 端口

# 服务端口
BACKEND_PORT=8000          # 后端端口
NGINX_PORT=80              # Nginx HTTP 端口
NGINX_SSL_PORT=443         # Nginx HTTPS 端口

# 应用配置
DEBUG=false                # 调试模式
LOG_LEVEL=INFO            # 日志级别
WORKERS=4                  # Uvicorn 工作进程数
```

---

## 🎮 启动脚本

### 功能菜单

启动脚本提供 6 个功能选项：

1. **首次部署** - 构建镜像 + 启动服务
2. **启动服务** - 使用现有镜像启动
3. **重新构建** - 重建镜像并启动
4. **停止服务** - 停止所有容器
5. **查看日志** - 实时日志查看
6. **清理数据** - 清理容器和数据卷 (⚠️ 危险操作)

### 手动命令

如果不使用启动脚本，可以直接使用 docker-compose：

```bash
# 构建并启动
docker-compose -f config/docker/docker-compose.yml up -d --build

# 启动服务
docker-compose -f config/docker/docker-compose.yml up -d

# 停止服务
docker-compose -f config/docker/docker-compose.yml down

# 查看日志
docker-compose -f config/docker/docker-compose.yml logs -f

# 查看状态
docker-compose -f config/docker/docker-compose.yml ps

# 重启服务
docker-compose -f config/docker/docker-compose.yml restart

# 进入容器
docker-compose -f config/docker/docker-compose.yml exec backend bash
```

---

## ❓ 常见问题

### Q1: 端口被占用

**问题**: `Error: bind: address already in use`

**解决方案**: 修改 `.env` 中的端口配置

```bash
BACKEND_PORT=8001
DB_PORT=5433
REDIS_PORT=6380
NGINX_PORT=8080
```

### Q2: 数据库连接失败

**问题**: `could not connect to server`

**检查步骤**:

1. 确认容器运行: `docker ps`
2. 查看日志: `docker-compose -f config/docker/docker-compose.yml logs postgres`
3. 检查健康状态: `docker inspect llm-arena-postgres`

### Q3: 镜像构建失败

**可能原因**:

- 网络问题 (已配置国内镜像源)
- 磁盘空间不足
- Docker 版本过低

**解决方案**:

```bash
# 清理 Docker 缓存
docker system prune -a

# 检查磁盘空间
docker system df

# 重新构建
docker-compose -f config/docker/docker-compose.yml build --no-cache
```

### Q4: 容器启动后自动退出

**检查步骤**:

1. 查看容器日志
2. 检查 `.env` 配置是否正确
3. 确认依赖服务 (postgres, redis) 是否健康

```bash
# 查看退出原因
docker logs llm-arena-backend

# 检查服务健康状态
docker-compose -f config/docker/docker-compose.yml ps
```

### Q5: Nginx 无法访问

**问题**: 访问 localhost 无响应

**解决方案**:

- Nginx 是可选服务，可以直接访问 `localhost:8000`
- 检查 Nginx 日志: `docker logs llm-arena-nginx`
- 确认前端已构建: `frontend/dist` 目录是否存在

---

## 🔧 高级配置

### 禁用 Nginx (仅后端)

如果只需要后端 API，可以禁用 Nginx：

编辑 `config/docker/docker-compose.yml`，注释掉 nginx 服务：

```yaml
# nginx:
#   image: nginx:alpine
#   ...
```

然后直接访问 `http://localhost:8000`

### 开发模式

开发时挂载源代码，实现热重载：

编辑 `config/docker/docker-compose.yml`，取消注释：

```yaml
volumes:
  - ../../src:/app/src  # 挂载源代码
```

### 配置 SSL/HTTPS

1. 准备 SSL 证书文件 (`.crt`, `.key`)
2. 放置到 `config/nginx/certs/` 目录
3. 修改 `config/nginx/conf.d/default.conf`

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/certs/your_cert.crt;
    ssl_certificate_key /etc/nginx/certs/your_key.key;
    # ...
}
```

4. 取消 docker-compose.yml 中的证书挂载注释

### 数据库备份与恢复

```bash
# 备份数据库
docker-compose -f config/docker/docker-compose.yml exec postgres \
  pg_dump -U postgres llm_arena > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker-compose -f config/docker/docker-compose.yml exec -T postgres \
  psql -U postgres llm_arena < backup_20250116.sql
```

### 性能优化

#### 调整 Uvicorn 工作进程

编辑 `.env`:

```bash
WORKERS=8  # 根据 CPU 核心数调整，建议为 (2 * CPU核心数) + 1
```

#### 增加 PostgreSQL 连接池

编辑 `.env`:

```bash
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
```

#### 配置资源限制

编辑 `config/docker/docker-compose.yml`:

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 512M
```

---

## 📊 监控与日志

### 查看日志

```bash
# 所有服务
docker-compose -f config/docker/docker-compose.yml logs -f

# 特定服务
docker-compose -f config/docker/docker-compose.yml logs -f backend
docker-compose -f config/docker/docker-compose.yml logs -f postgres

# 最近 100 行
docker-compose -f config/docker/docker-compose.yml logs --tail=100
```

### 资源监控

```bash
# 查看资源使用
docker stats

# 查看容器状态
docker-compose -f config/docker/docker-compose.yml ps

# 查看网络
docker network ls
docker network inspect llm-arena-network
```

---

## 🔐 生产环境清单

部署到生产环境前，请确保：

- [ ] 修改所有默认密码
- [ ] 生成强随机 SECRET_KEY
- [ ] 配置 SSL/HTTPS 证书
- [ ] 限制数据库端口仅监听 127.0.0.1
- [ ] 配置防火墙规则
- [ ] 启用日志轮转
- [ ] 设置资源限制
- [ ] 配置自动备份策略
- [ ] 设置监控和告警
- [ ] 禁用 DEBUG 模式
- [ ] 关闭 Swagger UI 或加密码保护

---

## 📚 相关文档

- [项目主文档](../README.md)
- [环境配置说明](./ENV_CONFIG.md)
- [前端集成指南](../FRONTEND_INTEGRATION.md)
- [贡献指南](../CONTRIBUTING.md)

---

## 🆘 获取帮助

- 📖 查看文档: [docs/](../docs/)
- 🐛 报告问题: [GitHub Issues](https://github.com/pkulab409/llm-arena/issues)
- 💬 社区讨论: [GitHub Discussions](https://github.com/pkulab409/llm-arena/discussions)

---

**部署成功！祝你使用愉快！🎉**
