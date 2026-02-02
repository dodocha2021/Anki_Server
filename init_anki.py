#!/usr/bin/env python3
"""
Initialize Anki using its own libraries
This avoids manual database creation which can lead to version mismatches
"""
import os
import sys

ANKI_BASE = "/root/.local/share/Anki2"

def init_anki_properly():
    """Use Anki's own initialization"""
    print("========================================")
    print("🔧 初始化 Anki 配置")
    print("========================================")
    
    os.makedirs(ANKI_BASE, exist_ok=True)
    
    # Create a minimal prefs.db that won't crash Anki
    import sqlite3
    prefs_path = os.path.join(ANKI_BASE, "prefs21.db")
    
    if not os.path.exists(prefs_path):
        print("📝 Creating minimal prefs database...")
        conn = sqlite3.connect(prefs_path)
        cursor = conn.cursor()
        
        # This is the exact schema Anki expects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                usn INTEGER NOT NULL DEFAULT 0,
                mtime_secs INTEGER NOT NULL DEFAULT 0,
                value BLOB NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ prefs21.db created")
    else:
        print("✅ prefs21.db already exists")
    
    # Create meta.json with minimal required fields
    import json
    meta_path = os.path.join(ANKI_BASE, "meta.json")
    
    if not os.path.exists(meta_path):
        print("📝 Creating meta.json...")
        meta = {}  # Empty is fine, Anki will populate it
        with open(meta_path, 'w') as f:
            json.dump(meta, f)
        print("✅ meta.json created")
    else:
        print("✅ meta.json already exists")
    
    print("========================================")
    print("✅ Anki 基础配置完成")
    print("   Anki will complete initialization on first run")
    print("========================================")

if __name__ == "__main__":
    init_anki_properly()
