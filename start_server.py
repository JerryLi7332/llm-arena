#!/usr/bin/env python3
"""
LLM Arena 后端服务启动脚本
配置uvicorn忽略uploads和logs目录，避免文件上传时触发重启
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """主函数"""
    print("🚀 启动 LLM Arena 后端服务...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    uploads_dir = project_root / "uploads"
    logs_dir = project_root / "logs"
    
    # 创建必要的目录
    print("📁 创建必要的目录...")
    uploads_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    
    # 配置uvicorn
    config = uvicorn.Config(
        "src:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[
            str(uploads_dir),
            str(logs_dir),
            "*/uploads/*",
            "*/logs/*"
        ],
        reload_dirs=[
            str(project_root / "src")
        ],
        log_level="info"
    )
    
    print("📝 服务地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("🔑 默认管理员账号: admin / abcd1234")
    print("📁 上传目录: uploads/")
    print("📁 日志目录: logs/")
    print("")
    print("按 Ctrl+C 停止服务")
    print("")
    
    # 启动服务
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    main()
