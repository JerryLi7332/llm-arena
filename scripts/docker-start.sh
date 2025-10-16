#!/bin/bash
# ============================================
# LLM Arena - Linux/Mac Docker 一键启动脚本
# ============================================

set -e

# 切换到项目根目录（脚本所在目录的上级）
cd "$(dirname "$0")/.."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}🚀 LLM Arena Docker 部署脚本${NC}"
echo -e "${BLUE}============================================${NC}"
echo
echo -e "${BLUE}📁 工作目录: $(pwd)${NC}"
echo

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ 错误: 未检测到 Docker${NC}"
    echo "   请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ 错误: 未检测到 docker-compose${NC}"
    echo "   请先安装 docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker 环境检查通过${NC}"
echo

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  警告: 未找到 .env 文件${NC}"
    if [ -f "config/docker/.env.docker" ]; then
        echo "   正在从 config/docker/.env.docker 复制..."
        cp config/docker/.env.docker .env
    elif [ -f ".env.example" ]; then
        echo "   正在从 .env.example 复制..."
        cp .env.example .env
    else
        echo -e "${RED}   ❌ 错误: 找不到任何环境配置模板${NC}"
        exit 1
    fi
    echo
    echo -e "${YELLOW}⚠️  请编辑 .env 文件，配置以下项目：${NC}"
    echo "   - SECRET_KEY (必须修改)"
    echo "   - DEEPSEEK_API_KEY (必须配置)"
    echo "   - DB_PASSWORD (建议修改)"
    echo
    read -p "按回车继续..."
fi

# 显示菜单
show_menu() {
    echo "请选择操作:"
    echo "[1] 首次部署 (构建镜像 + 启动服务)"
    echo "[2] 启动服务 (使用现有镜像)"
    echo "[3] 重新构建并启动"
    echo "[4] 停止服务"
    echo "[5] 查看日志"
    echo "[6] 清理所有数据 (危险操作)"
    echo "[0] 退出"
    echo
}

# 显示成功信息
show_success() {
    echo
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}✅ 操作成功！${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo
    echo -e "${BLUE}📊 服务状态:${NC}"
    docker-compose -f config/docker/docker-compose.yml ps
    echo
    echo -e "${BLUE}🌐 访问地址:${NC}"
    echo "   - 后端 API:      http://localhost:8000"
    echo "   - API 文档:      http://localhost:8000/docs"
    echo "   - 前端页面:      http://localhost (如果启用了 nginx)"
    echo
    echo -e "${BLUE}💡 常用命令:${NC}"
    echo "   查看日志:        docker-compose -f config/docker/docker-compose.yml logs -f"
    echo "   进入容器:        docker-compose -f config/docker/docker-compose.yml exec backend bash"
    echo "   重启服务:        docker-compose -f config/docker/docker-compose.yml restart"
    echo "   停止服务:        docker-compose -f config/docker/docker-compose.yml down"
    echo
}

# 主循环
while true; do
    show_menu
    read -p "请输入选项 [0-6]: " choice
    
    case $choice in
        1)
            echo
            echo -e "${BLUE}🔨 首次部署: 构建镜像并启动服务...${NC}"
            echo
            docker-compose -f config/docker/docker-compose.yml build --no-cache
            docker-compose -f config/docker/docker-compose.yml up -d
            show_success
            ;;
        2)
            echo
            echo -e "${BLUE}🚀 启动服务...${NC}"
            echo
            docker-compose -f config/docker/docker-compose.yml up -d
            show_success
            ;;
        3)
            echo
            echo -e "${BLUE}🔨 重新构建镜像并启动...${NC}"
            echo
            docker-compose -f config/docker/docker-compose.yml down
            docker-compose -f config/docker/docker-compose.yml build --no-cache
            docker-compose -f config/docker/docker-compose.yml up -d
            show_success
            ;;
        4)
            echo
            echo -e "${BLUE}🛑 停止服务...${NC}"
            echo
            docker-compose -f config/docker/docker-compose.yml down
            echo -e "${GREEN}✅ 服务已停止${NC}"
            ;;
        5)
            echo
            echo -e "${BLUE}📋 查看实时日志 (Ctrl+C 退出)...${NC}"
            echo
            docker-compose -f config/docker/docker-compose.yml logs -f
            ;;
        6)
            echo
            echo -e "${RED}⚠️  警告: 此操作将删除所有容器、镜像和数据卷！${NC}"
            echo "   数据库数据将会丢失，请谨慎操作！"
            echo
            read -p "确认清理? [y/N]: " confirm
            if [ "$confirm" == "y" ] || [ "$confirm" == "Y" ]; then
                echo
                echo -e "${BLUE}🗑️  清理中...${NC}"
                docker-compose -f config/docker/docker-compose.yml down -v
                docker rmi llm-arena-backend 2>/dev/null || true
                echo -e "${GREEN}✅ 清理完成${NC}"
            else
                echo "操作已取消"
            fi
            ;;
        0)
            echo "再见！"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 无效选项${NC}"
            ;;
    esac
    
    echo
    read -p "按回车继续..."
    clear
done
