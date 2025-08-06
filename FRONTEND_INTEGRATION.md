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
        """服务前端HTML文件"""
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
        else:
            return JSONResponse({"message": "前端文件未找到"}, status_code=404)
    
    @app.get("/admin", include_in_schema=False)
    async def serve_admin():
        """服务管理后台页面"""
        admin_path = static_dir / "admin.html"
        if admin_path.exists():
            return FileResponse(str(admin_path), media_type="text/html")
        else:
            return JSONResponse({"message": "管理页面未找到"}, status_code=404)
    
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
],
```

### 3. 目录结构建议

```
static/          # 主要静态文件
├── index.html
├── css/
├── js/
├── images/
├── icons/
└── fonts/

uploads/         # 上传文件目录
├── images/
└── documents/
```

### 4. 常见问题排查

1. **404 错误**：检查文件路径和目录是否存在
2. **权限错误**：确保应用有读取静态文件目录的权限
3. **中间件错误**：确认路径已添加到排除列表
4. **MIME 类型错误**：确保返回正确的 `media_type`

### 5. 测试验证

可以通过浏览器访问或创建测试脚本验证挂载是否成功。
