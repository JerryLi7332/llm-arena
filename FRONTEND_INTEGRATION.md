# 前端集成部署指南

——FastAPI 静态文件挂载与前端路由生成

## 概述

本指南介绍如何在 FastAPI 项目中正确挂载静态文件，避免审计日志中间件错误。

## 问题背景

当访问根路径 `/` 或其他静态文件路径时，可能会遇到以下错误：
```
ValueError: summary is non nullable field, but null was passed
```

这是因为审计日志中间件尝试为静态文件请求创建日志记录，但静态文件路由没有对应的 API 路由信息。

## 挂载方法

### 1. 修改中间件配置

在 `src/core/init_app.py` 中的 `make_middlewares()` 函数里，将静态文件路径添加到排除列表（见下）

### 2. 挂载新的静态文件

#### 2.1 在 `src/__init__.py` 中添加新的挂载点（前端路由 + 静态文件组合）

```python
def create_app() -> FastAPI:
    app = FastAPI(...)
    
    # 挂载静态文件目录
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # 挂载上传文件目录
    uploads_dir = Path(__file__).parent.parent / "uploads"
    if uploads_dir.exists():
        app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
    
    # 添加新的路由处理
    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """服务主页 - LLM Arena介绍页面"""
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
        else:
            return JSONResponse({"message": "前端文件未找到"}, status_code=404)
    
    @app.get("/admin", include_in_schema=False)
    async def serve_admin():
        """服务管理后台页面 - 仅管理员可访问"""
        admin_path = static_dir / "admin.html"
        if admin_path.exists():
            return FileResponse(str(admin_path), media_type="text/html")
        else:
            return JSONResponse({"message": "管理后台页面未找到"}, status_code=404)
    
    @app.get("/dashboard", include_in_schema=False)
    async def serve_dashboard():
        """服务用户仪表板页面 - 普通用户可访问"""
        dashboard_path = static_dir / "dashboard.html"
        if dashboard_path.exists():
            return FileResponse(str(dashboard_path), media_type="text/html")
        else:
            return JSONResponse({"message": "用户仪表板页面未找到"}, status_code=404)
    
    return app
```

#### 2.2 更新排除路径配置

在 `src/core/init_app.py` 中添加新的排除路径：

```python
EXCLUDE_PATHS = [
    "/api/v1/base/access_token",
    "/docs",
    "/openapi.json",
    "/",
    "/redoc",
    "/static",
    "/assets",      # 新增
    "/uploads",     # 新增
    "/admin",       # 新增
    "/dashboard",   # 新增
],
```
```

### 3. 新的路由结构

#### 3.1 页面路由说明

- **`/`** - 主页：LLM Arena介绍页面，包含产品特性和注册/登录引导
- **`/admin`** - 管理后台：仅管理员可访问，包含用户管理、角色管理等功能
- **`/dashboard`** - 用户仪表板：普通用户可访问，包含用户信息和基本功能
- **`/auth/login`** - 登录页面：用户登录界面
- **`/auth/register`** - 注册页面：用户注册界面

#### 3.2 权限控制

- 管理后台 (`/admin`) 需要管理员权限，非管理员用户访问时会显示权限拒绝页面
- 用户仪表板 (`/dashboard`) 需要登录权限，未登录用户会显示登录页面
- 主页 (`/`) 无需权限，所有用户都可访问

### 4. 目录结构建议

```
static/          # 主要静态文件
├── index.html   # 主页 - LLM Arena介绍
├── admin.html   # 管理后台 - 仅管理员
├── dashboard.html # 用户仪表板 - 普通用户
├── login.html   # 登录页面
├── register.html # 注册页面
├── css/
├── js/
├── images/
├── icons/
└── fonts/

uploads/         # 上传文件目录
├── images/
└── documents/
```

### 5. 常见问题排查

1. **404 错误**：检查文件路径和目录是否存在
2. **权限错误**：确保应用有读取静态文件目录的权限
3. **中间件错误**：确认路径已添加到排除列表
4. **MIME 类型错误**：确保返回正确的 `media_type`
5. **权限拒绝错误**：检查用户角色是否为管理员（访问 `/admin` 时）

### 6. 测试验证

可以通过浏览器访问或创建测试脚本验证挂载是否成功：

- 访问 `/` 应该显示LLM Arena介绍页面
- 访问 `/admin` 需要管理员权限
- 访问 `/dashboard` 需要登录权限
- 访问 `/auth/login` 和 `/auth/register` 应该显示相应的登录/注册页面
