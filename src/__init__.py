from contextlib import asynccontextmanager
import os
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
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

    # 挂载静态文件
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """服务前端HTML文件"""
        index_path = static_dir / "index.html"
        if index_path.exists():
            # 注意：FileResponse 需要传递 str 路径，否则部分环境下会报错
            return FileResponse(str(index_path), media_type="text/html")
        else:
            return JSONResponse({"message": "前端文件未找到，请确保 static/index.html 文件存在"}, status_code=404)

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
