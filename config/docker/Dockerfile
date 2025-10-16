# 使用官方 Python 3.11 slim 镜像作为基础镜像
# 使用国内镜像加速
FROM docker.m.daocloud.io/library/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    TZ=Asia/Shanghai

# 更换为国内镜像源以加速
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
COPY config/docker/requirements-minimal.txt ./requirements-minimal.txt

# 分阶段安装依赖，减少内存压力
# 第一步：安装最基础的包
RUN python -m pip install --no-cache-dir -r requirements-minimal.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 第二步：尝试安装其余依赖（如果失败，至少基础功能可用）
RUN python -m pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple || echo "Some packages failed to install, continuing with basic setup"

# 复制项目文件
COPY . .

# 复制并设置启动脚本权限
COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 创建必要的目录
RUN mkdir -p /app/logs /app/static /app/migrations

# 注意：为了避免权限问题，暂时以 root 用户运行
# 在生产环境中建议配置适当的用户权限

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# 启动命令
CMD ["/docker-entrypoint.sh"]
