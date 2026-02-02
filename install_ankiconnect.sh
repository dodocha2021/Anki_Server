#!/bin/bash

set -e

ANKI_ADDONS_DIR="/root/.local/share/Anki2/addons21"
ANKICONNECT_ID="2055492159"

echo "创建插件目录..."
mkdir -p "$ANKI_ADDONS_DIR/$ANKICONNECT_ID"

echo "下载 AnkiConnect..."
cd /tmp
wget -O ankiconnect.zip https://github.com/FooSoft/anki-connect/archive/refs/heads/master.zip
unzip -q ankiconnect.zip

echo "安装 AnkiConnect..."
cp -r anki-connect-master/plugin/* "$ANKI_ADDONS_DIR/$ANKICONNECT_ID/"

# 创建配置文件，允许所有来源访问
cat > "$ANKI_ADDONS_DIR/$ANKICONNECT_ID/config.json" <<EOF
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "0.0.0.0",
    "webBindPort": 8765,
    "webCorsOriginList": ["*"]
}
EOF

echo "清理临时文件..."
rm -rf /tmp/anki-connect-master /tmp/ankiconnect.zip

echo "AnkiConnect 安装完成！"
