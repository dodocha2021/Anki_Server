#!/usr/bin/env python3
"""
Anki 初始化脚本 - 使用官方 API
使用 Anki 的 Collection API 来正确初始化数据库
"""

import os
import sys

print("========================================")
print("🔧 初始化 Anki 配置")
print("========================================")

ANKI_BASE = "/root/.local/share/Anki2"
PROFILE_NAME = "User 1"
PROFILE_PATH = os.path.join(ANKI_BASE, PROFILE_NAME)
COLLECTION_PATH = os.path.join(PROFILE_PATH, "collection.anki2")

# 创建必要的目录
print(f"📁 创建目录: {PROFILE_PATH}")
os.makedirs(PROFILE_PATH, exist_ok=True)

# 检查是否已经初始化
if os.path.exists(COLLECTION_PATH):
    print(f"✅ Collection 已存在: {COLLECTION_PATH}")
    print("========================================")
    print("✅ Anki 已经初始化")
    print("========================================")
    sys.exit(0)

# 使用 Anki 官方 API 初始化
print("📝 使用 Anki API 初始化 collection...")

try:
    # 导入 Anki
    from anki.collection import Collection
    
    print(f"🔨 创建 Collection: {COLLECTION_PATH}")
    
    # 创建 Collection - Anki 会自动创建正确的数据库结构
    col = Collection(COLLECTION_PATH)
    
    print("✅ Collection 创建成功")
    
    # 关闭 collection
    col.close()
    
    print("✅ Collection 已关闭")
    
    # 验证文件存在
    if os.path.exists(COLLECTION_PATH):
        size = os.path.getsize(COLLECTION_PATH)
        print(f"✅ Collection 文件已创建 ({size} bytes)")
    else:
        print("❌ 错误: Collection 文件未创建")
        sys.exit(1)
    
    print("========================================")
    print("✅ Anki 初始化完成")
    print("   Anki will complete setup on first run")
    print("========================================")
    
except Exception as e:
    print(f"❌ 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
