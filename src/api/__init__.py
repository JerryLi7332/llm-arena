from fastapi import APIRouter

from .v1 import v1_router

import sys
import locale


# 强制使用 UTF-8 编码
if sys.platform.startswith("win"):
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    if locale.getpreferredencoding().lower() != "utf-8":
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 或其他支持 UTF-8 的地区


api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")


__all__ = ["api_router"]
