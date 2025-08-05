#!/usr/bin/env python3
"""
FastAPI 应用启动脚本
支持前端HTML挂载和API服务
"""

import uvicorn
import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    # 配置参数
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 启动 FastAPI 应用...")
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"📚 API文档: http://{host}:{port}/docs")
    print(f"🎨 前端界面: http://{host}:{port}/")
    print(f"🔄 热重载: {'启用' if reload else '禁用'}")
    
    # 启动应用
    uvicorn.run(
        "src:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["src", "static"] if reload else None,
        log_level="info"
    ) 