#!/bin/bash

# LLM Arena 后端服务启动脚本
# 适用于 Linux 和 macOS

echo "🚀 启动 LLM Arena 后端服务..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python 3.11+"
    exit 1
fi

# 检查uvicorn
if ! python3 -c "import uvicorn" &> /dev/null; then
    echo "❌ 错误: 未找到 uvicorn，请先安装依赖"
    echo "运行: pip install -r requirements.txt"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p uploads logs

# 启动后端服务
echo "🚀 启动后端服务..."
echo "📝 服务地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "🔑 默认管理员账号: admin / abcd1234"
echo ""
echo "按 Ctrl+C 停止服务"

# 使用Python启动脚本，配置uvicorn忽略uploads目录
python3 start_server.py
