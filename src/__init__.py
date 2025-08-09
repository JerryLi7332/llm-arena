from contextlib import asynccontextmanager
import os
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, JSONResponse
from tortoise import Tortoise

from core.dependency import get_current_username
from core.exceptions import SettingNotFound
from core.init_app import (
    init_data,
    make_middlewares,
    register_exceptions,
    register_routers,
)

import sys
import locale


# 强制使用 UTF-8 编码
if sys.platform.startswith("win"):
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    if locale.getpreferredencoding().lower() != "utf-8":
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 或其他支持 UTF-8 的地区


try:
    from settings.config import settings
except ImportError as e:
    raise SettingNotFound("Can not import settings") from e


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    yield
    await Tortoise.close_connections()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        lifespan=lifespan,
    )

    # Vue前端构建目录
    vue_dist_dir = Path(__file__).parent.parent / "frontend" / "dist"
    
    # 检查Vue构建文件是否存在
    index_path = vue_dist_dir / "index.html"
    
    # Vue前端路由支持 - 所有前端路由都返回index.html
    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """服务前端HTML文件"""
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
        else:
            return JSONResponse({
                "message": "前端文件未找到，请先构建Vue项目",
                "build_command": "cd frontend && npm run build"
            }, status_code=404)

    # 静态资源支持（CSS、JS、图片等）
    @app.get("/assets/{path:path}", include_in_schema=False)
    async def serve_assets(path: str):
        """服务Vue构建的静态资源"""
        asset_path = vue_dist_dir / "assets" / path
        if asset_path.exists() and asset_path.is_file():
            return FileResponse(str(asset_path))
        else:
            return JSONResponse({"message": "静态资源未找到"}, status_code=404)

    # Vue路由支持 - 所有前端路由都返回index.html
    @app.get("/{path:path}", include_in_schema=False)
    async def serve_vue_routes(path: str):
        """支持Vue前端路由"""
        # 排除API路由
        if path.startswith("api/"):
            return JSONResponse({"message": "API路由不存在"}, status_code=404)
        
        # 排除文档路由
        if path in ["docs", "openapi.json", "redoc"]:
            return JSONResponse({"message": "文档路由不存在"}, status_code=404)
        
        # 排除静态资源路由
        if path.startswith("assets/"):
            return JSONResponse({"message": "静态资源路由不存在"}, status_code=404)
        
        # 所有其他路由都返回index.html，让Vue Router处理
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
        else:
            return JSONResponse({
                "message": "前端文件未找到，请先构建Vue项目",
                "build_command": "cd frontend && npm run build"
            }, status_code=404)

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(
        username: str = Depends(get_current_username),
    ):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html(username: str = Depends(get_current_username)):
        return get_redoc_html(
            openapi_url="/openapi.json",
            title=app.title + " - ReDoc",
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint(
        username: str = Depends(get_current_username),
    ):
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        return openapi_schema

    register_exceptions(app)
    register_routers(app, prefix="/api")
    return app


app = create_app()
