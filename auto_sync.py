#!/usr/bin/env python3
"""
自动同步脚本
定期将本地 Anki 数据同步到 AnkiWeb 官方服务器
"""

import os
import time
import json
import requests
from datetime import datetime

ANKICONNECT_URL = "http://localhost:8765"
SYNC_INTERVAL = int(os.environ.get("SYNC_INTERVAL", "300"))  # 默认 5 分钟
USERNAME = os.environ.get("ANKIWEB_USERNAME")
PASSWORD = os.environ.get("ANKIWEB_PASSWORD")


def log(message):
    """打印带时间戳的日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def call_ankiconnect(action, params=None):
    """调用 AnkiConnect API"""
    payload = {
        "action": action,
        "version": 6
    }
    if params:
        payload["params"] = params

    try:
        response = requests.post(ANKICONNECT_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("error"):
            log(f"❌ AnkiConnect 错误: {result['error']}")
            return None

        return result.get("result")
    except requests.exceptions.RequestException as e:
        log(f"❌ 网络错误: {e}")
        return None


def perform_sync():
    """执行同步操作"""
    log("🔄 开始同步到 AnkiWeb...")

    # 方法1: 使用 sync 动作 (推荐)
    result = call_ankiconnect("sync")

    if result is not None:
        log(f"✅ 同步成功: {result}")
        return True
    else:
        log("❌ 同步失败")
        return False


def wait_for_ankiconnect():
    """等待 AnkiConnect 准备就绪"""
    log("⏳ 等待 AnkiConnect 就绪...")
    for i in range(30):
        try:
            result = call_ankiconnect("version")
            if result:
                log(f"✅ AnkiConnect 版本: {result}")
                return True
        except:
            pass
        time.sleep(2)

    log("❌ AnkiConnect 未就绪")
    return False


def main():
    """主循环"""
    log("========================================")
    log("🚀 自动同步脚本启动")
    log(f"   同步间隔: {SYNC_INTERVAL} 秒")
    log(f"   AnkiWeb 账号: {USERNAME}")
    log("========================================")

    if not USERNAME or not PASSWORD:
        log("❌ 错误: 未设置 ANKIWEB_USERNAME 或 ANKIWEB_PASSWORD")
        return

    # 等待 AnkiConnect 启动
    if not wait_for_ankiconnect():
        log("❌ 无法连接到 AnkiConnect，退出")
        return

    # 首次同步前等待 30 秒（给 Anki 启动留时间）
    log(f"⏳ 等待 30 秒后开始首次同步...")
    time.sleep(30)

    # 主循环
    sync_count = 0
    while True:
        try:
            sync_count += 1
            log(f"📊 第 {sync_count} 次同步")

            if perform_sync():
                log(f"✅ 同步完成，下次同步: {SYNC_INTERVAL}秒后")
            else:
                log(f"⚠️  同步失败，{SYNC_INTERVAL}秒后重试")

            time.sleep(SYNC_INTERVAL)

        except KeyboardInterrupt:
            log("🛑 收到停止信号，退出自动同步")
            break
        except Exception as e:
            log(f"❌ 未知错误: {e}")
            log(f"⏳ {SYNC_INTERVAL}秒后重试...")
            time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    main()
