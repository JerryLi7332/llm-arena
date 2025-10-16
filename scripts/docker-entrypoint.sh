#!/bin/bash
set -e

echo "============================================"
echo "🚀 LLM Arena - Docker 容器启动脚本"
echo "============================================"

# 等待数据库就绪
echo "⏳ 等待 PostgreSQL 数据库就绪..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  echo "   PostgreSQL 还未就绪，等待 2 秒..."
  sleep 2
done
echo "✅ PostgreSQL 已就绪"

# 等待 Redis 就绪（如果配置了）
if [ -n "$REDIS_HOST" ]; then
  echo "⏳ 等待 Redis 就绪..."
  until redis-cli -h "$REDIS_HOST" -p "${REDIS_PORT:-6379}" ping 2>/dev/null; do
    echo "   Redis 还未就绪，等待 2 秒..."
    sleep 2
  done
  echo "✅ Redis 已就绪"
fi

# 运行数据库迁移
echo "📦 运行数据库迁移..."
cd /app

# 检查是否已初始化 Aerich
if [ ! -f "aerich.ini" ]; then
  echo "   初始化 Aerich..."
  aerich init -t aerich_config.TORTOISE_ORM || true
fi

# 检查是否已初始化数据库
if [ ! -d "migrations/models" ]; then
  echo "   初始化数据库表..."
  aerich init-db
else
  echo "   应用数据库迁移..."
  aerich upgrade
fi

echo "✅ 数据库迁移完成"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p /app/uploads /app/logs /app/static
echo "✅ 目录创建完成"

# 启动应用
echo "============================================"
echo "🎉 启动 LLM Arena 应用..."
echo "============================================"

# 使用 uvicorn 启动应用
exec uvicorn src:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers ${WORKERS:-4} \
  --log-level ${LOG_LEVEL:-info} \
  --access-log \
  --use-colors
