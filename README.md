# line-bot
# 🍰 LINE Bot 點心訂購系統

這是一個使用 **Flask** 搭配 **LINE Messaging API** 所建構的甜點訂購 LINE 機器人，支援使用者透過 LINE 輸入格式化文字來下訂單，並儲存在 SQLite 資料庫中。

---

## 🚀 專案功能 Features

* ✅ 使用者透過 LINE 輸入格式化文字下訂單
* ✅ 自動解析品項、數量、付款方式與面交資訊
* ✅ 訂單自動儲存進 SQLite 資料庫
* ✅ 管理者可輸入指令查看最新訂單紀錄
* ✅ 提供甜點圖片、訂購方式說明、當月製作時間表
* ✅ 使用 Flex Message 展示甜點資訊

---

## 📁 專案結構 Project Structure

```
.
├── app.py               # 主應用：處理 LINE 訊息與訂單邏輯
├── model.py             # 資料庫初始化與儲存邏輯
├── requirements.txt     # 套件需求列表
├── .gitignore           # 忽略資料庫與 pycache 等
└── Procfile             # 部署設定（Heroku 等用）
```

---

## ⚙️ 安裝與執行方式

### 1. 安裝環境

建議使用處理處處處處處處處處處

```bash
pip install -r requirements.txt
```

### 2. 設定 `.env` 環境變數

建立 `.env` 檔案並加入 LINE bot 金鑰資訊：

```
LINE_CHANNEL_ACCESS_TOKEN=你的 Access Token
LINE_CHANNEL_SECRET=你的 Channel Secret
```

### 3. 執行應用（本地測試）

```bash
python app.py
```

---

## 💡 使用方式（LINE 端）

使用者可透過以下格式下單：

```
原味購諾雪*2
法芟娜可可購諾雪*1
麵茶購諾雪*3
舒胡布丁*2
付款方式:現金
日期:5/25
時間:14:30
面交地點:台南7-11忠忠門店
```

### 可使用指令

| 指令        | 說明                      |
| --------- | ----------------------- |
| `購諾雪`     | 顯示 FlexMessage 的甜點圖片與說明 |
| `舒胡布丁`    | 顯示商品介紹                  |
| `巴斯克`     | 顯示商品介紹                  |
| `菜單`      | 顯示甜點圖片菜單                |
| `訂購方式`    | 顯示訂購流程與付款 QRcode        |
| `當月製作時間表` | 顯示製作日曆                  |
| `查看訂單`    | 僅限管理者帳號查詢最近 5 筆訂單       |

---

## 🛠️ 技術梯

* Python 3.x
* Flask
* LINE Messaging API SDK (`line-bot-sdk`)
* SQLite
* dotenv（管理環境變數）
* Gunicorn（部署用）

---

## 📈 資料庫結構（SQLite）

```sql
orders (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    user_name TEXT,
    cheese_cake INTEGER,
    financier_original INTEGER,
    financier_choco INTEGER,
    financier_tea INTEGER,
    pudding INTEGER,
    payment_method TEXT,
    pickup_date TEXT,
    pickup_time TEXT,
    pickup_location TEXT,
    timestamp DATETIME
)
```

---

## ☁️ 可部署平台（選擇其一）

* Heroku（使用 `Procfile` 和 `gunicorn`）
* Render / Railway / Fly.io
* 本機測試可用 ngrok 反向代理接收 LINE webhook

---

## 📉 作者建議

* 若你打算擴充成後台系統，可考慮接入 Firestore、Supabase 等雲端資料庫
* 可新增「圖片點選下單」功能或使用 LINE LIFF 擴充

---

## 📞 聯絡方式

如需協助整合、似項目部署或改寫本系統，歡迎私訊閦娟 😁

---
