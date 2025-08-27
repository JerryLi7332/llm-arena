#!/bin/bash

# DeepSeek API 后端集成部署脚本
# 使用方法: ./deploy_deepseek.sh

set -e

echo "🚀 开始部署 DeepSeek API 后端集成..."

# 检查Python环境
echo "📋 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先安装pip3"
    exit 1
fi

echo "✅ Python环境检查通过"

# 安装依赖
echo "📦 安装依赖包..."
pip3 install httpx>=0.24.0 pydantic>=2.0.0 pydantic-settings>=2.0.0

echo "✅ 依赖安装完成"

# 检查环境变量
echo "🔐 检查环境变量配置..."
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: DEEPSEEK_API_KEY 环境变量未设置"
    echo "请在 .env 文件中添加以下配置:"
    echo ""
    echo "DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here"
    echo "DEEPSEEK_API_BASE=https://api.deepseek.com/v1"
    echo "DEEPSEEK_DEFAULT_MODEL=deepseek-chat"
    echo "DEEPSEEK_MAX_TOKENS=4000"
    echo "DEEPSEEK_TEMPERATURE=0.7"
    echo "DEEPSEEK_REQUEST_TIMEOUT=30000"
    echo ""
    echo "或者设置环境变量:"
    echo "export DEEPSEEK_API_KEY='sk-your-api-key'"
    echo ""
else
    echo "✅ DEEPSEEK_API_KEY 已设置"
fi

# 检查文件是否存在
echo "📁 检查必要文件..."
required_files=(
    "src/settings/deepseek.py"
    "src/services/deepseek_service.py"
    "src/api/v1/deepseek.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 文件不存在: $file"
        exit 1
    fi
done

echo "✅ 所有必要文件存在"

# 检查路由配置
echo "🔗 检查路由配置..."
if ! grep -q "deepseek_router" "src/api/v1/__init__.py"; then
    echo "⚠️  警告: 路由配置可能未完成，请检查 src/api/v1/__init__.py"
fi

echo "✅ 路由配置检查完成"

# 测试导入
echo "🧪 测试模块导入..."
python3 -c "
try:
    from src.settings.deepseek import deepseek_settings
    from src.services.deepseek_service import deepseek_service
    from src.api.v1.deepseek import router
    print('✅ 所有模块导入成功')
except ImportError as e:
    print(f'❌ 模块导入失败: {e}')
    exit(1)
"

echo "✅ 模块导入测试通过"

# 启动服务
echo "🚀 启动FastAPI服务..."
echo "使用以下命令启动服务:"
echo ""
echo "uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "或者如果使用 start_server.py:"
echo "python3 start_server.py"
echo ""

# 测试API
echo "🧪 测试API端点..."
echo "服务启动后，可以使用以下命令测试:"
echo ""
echo "1. 检查API状态:"
echo "curl -X GET 'http://localhost:8000/api/v1/deepseek/status'"
echo ""
echo "2. 获取模型列表:"
echo "curl -X GET 'http://localhost:8000/api/v1/deepseek/models'"
echo ""
echo "3. 发送聊天消息:"
echo "curl -X POST 'http://localhost:8000/api/v1/deepseek/chat' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"messages\": [{\"role\": \"user\", \"content\": \"你好\"}]}'"
echo ""

echo "🎉 DeepSeek API 后端集成部署完成！"
echo ""
echo "📚 详细文档请查看: DEEPSEEK_DEPLOYMENT.md"
echo "🔧 如有问题，请检查日志文件或联系技术支持"
