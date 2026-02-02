#!/bin/bash

set -e

echo "========================================"
echo "🚀 启动 Anki 同步服务器"
echo "========================================"

# 检查必需的环境变量
if [ -z "$ANKIWEB_USERNAME" ] || [ -z "$ANKIWEB_PASSWORD" ]; then
    echo "⚠️  警告: ANKIWEB_USERNAME 或 ANKIWEB_PASSWORD 未设置"
    echo "   自动同步功能将被禁用"
    AUTO_SYNC_ENABLED=false
else
    AUTO_SYNC_ENABLED=true
    echo "✅ 检测到 AnkiWeb 凭据"
fi

# 清理可能残留的 Xvfb 锁文件
if [ -f /tmp/.X99-lock ]; then
    echo "🧹 清理旧的 Xvfb 锁文件..."
    rm -f /tmp/.X99-lock
fi

# 启动 Xvfb (虚拟显示)
echo "🖥️  启动虚拟显示 (Xvfb)..."
Xvfb :99 -screen 0 1024x768x16 &
XVFB_PID=$!
sleep 2

# 检查 AnkiConnect 是否已安装（Volume 持久化检测）
ANKICONNECT_DIR="/root/.local/share/Anki2/addons21/2055492159"
PREFS_FILE="/root/.local/share/Anki2/prefs21.db"

if [ ! -d "$ANKICONNECT_DIR" ]; then
    echo "📦 首次运行，安装 AnkiConnect..."
    /app/install_ankiconnect.sh
else
    echo "✅ AnkiConnect 已安装 (从 Volume 加载)"
fi

# 创建基础配置目录并设置权限
echo "📁 初始化 Anki 数据目录..."
ANKI_BASE="/root/.local/share/Anki2"
mkdir -p "$ANKI_BASE"
chmod -R 755 "$ANKI_BASE"

# 初始化最小配置（仅在首次运行时）
if [ ! -f "$PREFS_FILE" ]; then
    echo "🔧 首次运行，初始化 Anki 配置..."
    python3 /app/init_anki.py
else
    echo "✅ Anki 配置已存在 (从 Volume 加载)"
fi

# 启动 Anki 并捕获错误输出
echo "🎴 启动 Anki..."

# 设置环境变量强制无头模式
export QT_QPA_PLATFORM=offscreen
export QT_LOGGING_RULES="*.debug=false;qt.qpa.*=false"
export QTWEBENGINE_DISABLE_SANDBOX=1

# 尝试使用 --profile 参数避免 GUI 初始化对话框
# 启动 Anki 时指定一个默认配置文件
echo "User 1" > "$ANKI_BASE/profile"

anki --no-sandbox \
  --base "$ANKI_BASE" \
  --profile "User 1" \
  2>&1 | tee /tmp/anki.log &
ANKI_PID=$!
sleep 5

# 检查 Anki 是否还在运行
if ! kill -0 $ANKI_PID 2>/dev/null; then
    echo "❌ Anki 启动失败！查看错误日志："
    cat /tmp/anki.log
    exit 1
fi

# 等待 AnkiConnect 就绪
echo "⏳ 等待 AnkiConnect 启动..."
for i in {1..30}; do
    if curl -s http://localhost:8765 > /dev/null 2>&1; then
        echo "✅ AnkiConnect 已就绪！"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ AnkiConnect 启动超时"
        exit 1
    fi
    sleep 2
done

# 测试 AnkiConnect
echo "🧪 测试 AnkiConnect..."
RESPONSE=$(curl -s -X POST http://localhost:8765 -d '{
    "action": "version",
    "version": 6
}')
echo "   响应: $RESPONSE"

# 启动自动同步脚本（如果启用）
if [ "$AUTO_SYNC_ENABLED" = true ]; then
    SYNC_INTERVAL=${SYNC_INTERVAL:-300}  # 默认 5 分钟
    echo "🔄 启动自动同步 (间隔: ${SYNC_INTERVAL}秒)..."
    python3 /app/auto_sync.py &
    SYNC_PID=$!
fi

echo "========================================"
echo "✅ Anki 服务器已启动！"
echo "   AnkiConnect API: http://0.0.0.0:8765"
echo "   自动同步: $([ "$AUTO_SYNC_ENABLED" = true ] && echo "已启用" || echo "已禁用")"
echo "========================================"

# 保持容器运行
trap "echo '🛑 收到停止信号...'; kill $ANKI_PID $XVFB_PID $([ -n \"$SYNC_PID\" ] && echo \"$SYNC_PID\"); exit 0" SIGTERM SIGINT

wait $ANKI_PID
