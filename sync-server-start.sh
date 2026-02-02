#!/bin/bash

set -e

echo "========================================"
echo "🚀 Anki Sync Server"
echo "========================================"

# 配置检查
if [ -z "$ANKIWEB_USERNAME" ] || [ -z "$ANKIWEB_PASSWORD" ]; then
    echo "⚠️  警告: 未设置 ANKIWEB_USERNAME 或 ANKIWEB_PASSWORD"
    echo "   这不影响同步服务器运行，但无法自动同步到 AnkiWeb"
fi

# 创建必要的目录
mkdir -p /data/collections

echo "📂 数据目录: /data"
echo "🌐 监听地址: ${SYNC_HOST}:${SYNC_PORT}"
echo "========================================"

# 启动 Anki 同步服务器
echo "🎴 启动 Anki 同步服务器..."

python -m anki.syncserver \
    --host "${SYNC_HOST}" \
    --port "${SYNC_PORT}" \
    --base "${SYNC_BASE}"
