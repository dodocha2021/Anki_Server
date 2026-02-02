#!/usr/bin/env python3
"""
Initialize Anki profile to prevent startup crashes
"""
import os
import sqlite3
import json

ANKI_BASE = "/root/.local/share/Anki2"

def init_prefs_db():
    """Create the preferences database"""
    db_path = os.path.join(ANKI_BASE, "prefs21.db")
    
    if os.path.exists(db_path):
        print(f"✅ prefs21.db already exists")
        return
    
    print("📝 Creating prefs21.db...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the config table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Insert default preferences
    default_prefs = {
        "numBackups": "50",
        "curDeck": "1",
        "sortType": "noteFld",
        "sortBackwards": "False",
        "addToCur": "True",
        "collapseTime": "1200",
        "estTimes": "True",
        "dueCounts": "True",
        "curModel": "null",
        "nextPos": "1",
        "schedVer": "2"
    }
    
    for key, value in default_prefs.items():
        cursor.execute('INSERT OR REPLACE INTO config VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()
    print("✅ prefs21.db created")

def init_meta_json():
    """Create the meta.json file"""
    meta_path = os.path.join(ANKI_BASE, "meta.json")
    
    if os.path.exists(meta_path):
        print(f"✅ meta.json already exists")
        return
    
    print("📝 Creating meta.json...")
    
    meta = {
        "firstRun": False,
        "defaultLang": "en",
        "last_addon_update_check": 0
    }
    
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print("✅ meta.json created")

def init_user_profile():
    """Create a default user profile"""
    user_dir = os.path.join(ANKI_BASE, "User 1")
    os.makedirs(user_dir, exist_ok=True)
    
    collection_path = os.path.join(user_dir, "collection.anki2")
    
    if os.path.exists(collection_path):
        print(f"✅ User profile already exists")
        return
    
    print("📝 Creating default user profile...")
    
    # Create minimal collection database
    conn = sqlite3.connect(collection_path)
    cursor = conn.cursor()
    
    # Collection table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS col (
            id integer primary key,
            crt integer not null,
            mod integer not null,
            scm integer not null,
            ver integer not null,
            dty integer not null,
            usn integer not null,
            ls integer not null,
            conf text not null,
            models text not null,
            decks text not null,
            dconf text not null,
            tags text not null
        )
    ''')
    
    # Insert default collection
    import time
    now = int(time.time())
    
    cursor.execute('''
        INSERT INTO col VALUES (
            1, ?, ?, ?, 11, 0, 0, 0,
            '{"nextPos":1,"estTimes":true,"activeDecks":[1]}',
            '{}',
            '{"1":{"id":1,"name":"Default","desc":"","mod":0}}',
            '{"1":{"id":1,"name":"Default","maxTaken":60}}',
            '{}'
        )
    ''', (now, now, now))
    
    # Notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id integer primary key,
            guid text not null,
            mid integer not null,
            mod integer not null,
            usn integer not null,
            tags text not null,
            flds text not null,
            sfld text not null,
            csum integer not null,
            flags integer not null,
            data text not null
        )
    ''')
    
    # Cards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id integer primary key,
            nid integer not null,
            did integer not null,
            ord integer not null,
            mod integer not null,
            usn integer not null,
            type integer not null,
            queue integer not null,
            due integer not null,
            ivl integer not null,
            factor integer not null,
            reps integer not null,
            lapses integer not null,
            left integer not null,
            odue integer not null,
            odid integer not null,
            flags integer not null,
            data text not null
        )
    ''')
    
    # Revlog table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revlog (
            id integer primary key,
            cid integer not null,
            usn integer not null,
            ease integer not null,
            ivl integer not null,
            lastIvl integer not null,
            factor integer not null,
            time integer not null,
            type integer not null
        )
    ''')
    
    # Graves table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS graves (
            usn integer not null,
            oid integer not null,
            type integer not null
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ User profile created")

def main():
    print("========================================")
    print("🔧 初始化 Anki 配置")
    print("========================================")
    
    os.makedirs(ANKI_BASE, exist_ok=True)
    
    init_prefs_db()
    init_meta_json()
    init_user_profile()
    
    print("========================================")
    print("✅ Anki 配置初始化完成")
    print("========================================")

if __name__ == "__main__":
    main()
