# 🤖 机器人 AI - AnkiConnect API 使用指南

## 📋 概述

Railway 部署的 Anki 服务器通过 **AnkiConnect** 插件暴露 HTTP API，你可以通过这个 API 添加、查询、管理 Anki 卡片。

---

## 🔗 连接信息

- **API 地址**: `https://你的railway域名.railway.app` (部署后获得)
- **端口**: `8765` (Railway 会自动映射)
- **协议**: HTTP POST
- **数据格式**: JSON

---

## 🛠️ API 基础

所有 API 请求的格式：

```json
{
  "action": "动作名称",
  "version": 6,
  "params": {
    // 参数对象
  }
}
```

响应格式：

```json
{
  "result": "结果数据",
  "error": null
}
```

---

## 🎴 常用操作

### 1️⃣ 测试连接

**动作**: `version`

```json
POST https://你的域名.railway.app
{
  "action": "version",
  "version": 6
}
```

**响应**:
```json
{
  "result": 6,
  "error": null
}
```

---

### 2️⃣ 获取所有牌组

**动作**: `deckNames`

```json
{
  "action": "deckNames",
  "version": 6
}
```

**响应**:
```json
{
  "result": ["Default", "编程", "英语"],
  "error": null
}
```

---

### 3️⃣ 创建牌组

**动作**: `createDeck`

```json
{
  "action": "createDeck",
  "version": 6,
  "params": {
    "deck": "AI学习卡片"
  }
}
```

**响应**:
```json
{
  "result": 1234567890123,  // 牌组 ID
  "error": null
}
```

---

### 4️⃣ 添加单张卡片（最常用）

**动作**: `addNote`

**基础示例 - 问答卡**:
```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "AI学习卡片",
      "modelName": "Basic",
      "fields": {
        "Front": "什么是 Transformer？",
        "Back": "Transformer 是一种基于注意力机制的神经网络架构，由 Vaswani 等人在 2017 年提出。"
      },
      "tags": ["AI", "机器学习"],
      "options": {
        "allowDuplicate": false
      }
    }
  }
}
```

**响应**:
```json
{
  "result": 9876543210987,  // 卡片 ID
  "error": null
}
```

**高级示例 - 带图片的卡片**:
```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "编程",
      "modelName": "Basic",
      "fields": {
        "Front": "Python 列表推导式",
        "Back": "[x**2 for x in range(10)]"
      },
      "tags": ["Python", "语法"],
      "audio": [],
      "picture": []
    }
  }
}
```

---

### 5️⃣ 批量添加卡片

**动作**: `addNotes`

```json
{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "英语",
        "modelName": "Basic",
        "fields": {
          "Front": "apple",
          "Back": "苹果"
        },
        "tags": ["词汇"]
      },
      {
        "deckName": "英语",
        "modelName": "Basic",
        "fields": {
          "Front": "banana",
          "Back": "香蕉"
        },
        "tags": ["词汇"]
      }
    ]
  }
}
```

**响应**:
```json
{
  "result": [1111111111111, 2222222222222],  // 卡片 ID 数组
  "error": null
}
```

---

### 6️⃣ 查询卡片

**动作**: `findNotes`

```json
{
  "action": "findNotes",
  "version": 6,
  "params": {
    "query": "deck:AI学习卡片 tag:机器学习"
  }
}
```

**查询语法**:
- `deck:牌组名` - 指定牌组
- `tag:标签` - 指定标签
- `front:关键词` - 搜索正面内容
- `*关键词*` - 全文搜索

**响应**:
```json
{
  "result": [1234567890, 9876543210],  // 卡片 ID 列表
  "error": null
}
```

---

### 7️⃣ 获取卡片详情

**动作**: `notesInfo`

```json
{
  "action": "notesInfo",
  "version": 6,
  "params": {
    "notes": [1234567890, 9876543210]
  }
}
```

**响应**:
```json
{
  "result": [
    {
      "noteId": 1234567890,
      "modelName": "Basic",
      "tags": ["AI"],
      "fields": {
        "Front": {"value": "什么是 Transformer？", "order": 0},
        "Back": {"value": "一种神经网络架构", "order": 1}
      }
    }
  ],
  "error": null
}
```

---

### 8️⃣ 更新卡片

**动作**: `updateNoteFields`

```json
{
  "action": "updateNoteFields",
  "version": 6,
  "params": {
    "note": {
      "id": 1234567890,
      "fields": {
        "Back": "更新后的答案内容"
      }
    }
  }
}
```

---

### 9️⃣ 删除卡片

**动作**: `deleteNotes`

```json
{
  "action": "deleteNotes",
  "version": 6,
  "params": {
    "notes": [1234567890, 9876543210]
  }
}
```

---

### 🔟 手动触发同步

**动作**: `sync`

```json
{
  "action": "sync",
  "version": 6
}
```

**说明**: 虽然服务器有自动同步（默认 5 分钟），但你可以在添加重要卡片后立即触发同步。

---

## 📚 卡片类型 (modelName)

常用模板：

| 模板名 | 字段 | 用途 |
|--------|------|------|
| `Basic` | Front, Back | 基础问答卡 |
| `Basic (and reversed card)` | Front, Back | 双向卡片（自动创建反向） |
| `Cloze` | Text, Extra | 填空题 |

**示例 - 填空卡**:
```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "编程",
      "modelName": "Cloze",
      "fields": {
        "Text": "Python 的 {{c1::列表推导式}} 可以快速生成列表",
        "Extra": "语法糖"
      },
      "tags": ["Python"]
    }
  }
}
```

---

## 🐍 Python 示例代码

```python
import requests
import json

ANKI_URL = "https://你的域名.railway.app"

def add_card(front, back, deck="Default", tags=None):
    """添加一张 Anki 卡片"""
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": tags or [],
                "options": {
                    "allowDuplicate": False
                }
            }
        }
    }

    response = requests.post(ANKI_URL, json=payload)
    result = response.json()

    if result.get("error"):
        print(f"❌ 错误: {result['error']}")
        return None

    print(f"✅ 卡片已添加，ID: {result['result']}")
    return result["result"]

# 使用示例
add_card(
    front="什么是 Docker？",
    back="Docker 是一个容器化平台",
    deck="技术学习",
    tags=["DevOps", "容器"]
)
```

---

## 🔍 查询语法速查

| 查询 | 说明 |
|------|------|
| `deck:编程` | 搜索"编程"牌组 |
| `tag:Python` | 搜索标签为 Python |
| `is:new` | 新卡片 |
| `is:due` | 到期需要复习 |
| `added:1` | 最近 1 天添加 |
| `front:*Docker*` | 正面包含 Docker |
| `deck:编程 tag:Python` | 组合查询 |

---

## ⚠️ 常见错误处理

### 错误: "deck was not found"
```json
{
  "result": null,
  "error": "deck was not found"
}
```
**解决**: 先调用 `createDeck` 创建牌组

### 错误: "model was not found"
```json
{
  "result": null,
  "error": "model was not found"
}
```
**解决**: 使用正确的 modelName，如 `Basic`（区分大小写）

### 错误: "cannot create note because it is a duplicate"
**解决**: 设置 `"allowDuplicate": true` 或修改卡片内容

---

## 🚀 最佳实践

### 1. 智能批量添加
当你需要添加多张卡片时，使用 `addNotes`（批量）而不是多次调用 `addNote`：

```python
def add_vocabulary_batch(words):
    """批量添加词汇卡片"""
    notes = [
        {
            "deckName": "英语词汇",
            "modelName": "Basic",
            "fields": {"Front": word, "Back": translation},
            "tags": ["vocabulary"]
        }
        for word, translation in words
    ]

    payload = {
        "action": "addNotes",
        "version": 6,
        "params": {"notes": notes}
    }

    return requests.post(ANKI_URL, json=payload).json()
```

### 2. 添加后立即同步
对于重要卡片：
```python
add_card(front, back, deck)
requests.post(ANKI_URL, json={"action": "sync", "version": 6})
```

### 3. 检查牌组是否存在
```python
def ensure_deck_exists(deck_name):
    """确保牌组存在，不存在则创建"""
    # 获取所有牌组
    payload = {"action": "deckNames", "version": 6}
    response = requests.post(ANKI_URL, json=payload).json()
    decks = response.get("result", [])

    # 如果不存在则创建
    if deck_name not in decks:
        create_payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name}
        }
        requests.post(ANKI_URL, json=create_payload)
```

---

## 📞 调试技巧

### 1. 使用 curl 测试
```bash
curl -X POST https://你的域名.railway.app \
  -H "Content-Type: application/json" \
  -d '{
    "action": "version",
    "version": 6
  }'
```

### 2. 查看日志
在 Railway 控制台查看容器日志，自动同步脚本会输出详细日志。

### 3. 健康检查
定期调用 `version` 确保服务可用：
```python
def is_anki_available():
    try:
        response = requests.post(
            ANKI_URL,
            json={"action": "version", "version": 6},
            timeout=5
        )
        return response.json().get("result") == 6
    except:
        return False
```

---

## 🔗 完整 API 文档

AnkiConnect 支持 70+ 个操作，完整文档：
https://github.com/FooSoft/anki-connect#supported-actions

常用分类：
- **笔记操作**: addNote, addNotes, updateNoteFields, deleteNotes
- **卡片操作**: findCards, cardsInfo, suspend, unsuspend
- **牌组操作**: deckNames, createDeck, changeDeck
- **查询**: findNotes, notesInfo
- **同步**: sync
- **媒体**: storeMediaFile, retrieveMediaFile

---

## 🎯 快速开始

1. **测试连接**：
```bash
curl -X POST https://你的域名.railway.app \
  -d '{"action":"version","version":6}'
```

2. **创建牌组**：
```bash
curl -X POST https://你的域名.railway.app \
  -d '{"action":"createDeck","version":6,"params":{"deck":"机器人卡片"}}'
```

3. **添加第一张卡片**：
```bash
curl -X POST https://你的域名.railway.app \
  -d '{
    "action":"addNote",
    "version":6,
    "params":{
      "note":{
        "deckName":"机器人卡片",
        "modelName":"Basic",
        "fields":{"Front":"测试问题","Back":"测试答案"},
        "tags":["test"]
      }
    }
  }'
```

---

## 💡 集成到你的 Skill

建议创建一个 `AnkiClient` 类封装所有操作：

```python
class AnkiClient:
    def __init__(self, url):
        self.url = url

    def _request(self, action, params=None):
        payload = {"action": action, "version": 6}
        if params:
            payload["params"] = params
        response = requests.post(self.url, json=payload)
        return response.json()

    def add_card(self, front, back, deck="Default", tags=None):
        return self._request("addNote", {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {"Front": front, "Back": back},
                "tags": tags or []
            }
        })

    def get_decks(self):
        return self._request("deckNames")

    def sync(self):
        return self._request("sync")

# 使用
anki = AnkiClient("https://你的域名.railway.app")
anki.add_card("问题", "答案", deck="AI学习")
anki.sync()
```

---

## ✅ 完成

现在你可以：
1. ✅ 通过 HTTP API 添加卡片
2. ✅ 数据自动同步到 AnkiWeb 官方服务器（每 5 分钟）
3. ✅ 用户从官方 Anki 客户端拉取你添加的卡片
4. ✅ 多端数据一致

祝你构建 Skill 顺利！🚀
