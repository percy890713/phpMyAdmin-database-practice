# 訂單管理系統 — MySQL + Python

本系統使用 Python 連接本機 XAMPP MySQL，對 `orders` 資料表進行 CRUD 操作。
提供兩種操作介面：**終端機選單** 與 **網頁介面（FastAPI）**。

> 初次使用請先閱讀 [新手手冊.md](新手手冊.md)，了解環境安裝與基礎 SQL 語法。

---

## 快速啟動

### 前置條件

1. 確認 XAMPP 的 MySQL 已啟動（Port 3306）
2. 在 [config.py](config.py) 填入正確的帳號密碼

### 方式一：終端機選單

```bash
python main.py
```

### 方式二：網頁介面（FastAPI）

安裝套件（只需執行一次）：

```bash
pip install fastapi uvicorn
```

啟動伺服器：

```bash
uvicorn api:app --reload
```

開啟瀏覽器輸入：`http://127.0.0.1:8000`

> `uvicorn api:app --reload` 的意思：
> - `api` → 執行 `api.py`
> - `app` → 該檔案裡名為 `app` 的 FastAPI 物件
> - `--reload` → 程式碼變動時自動重啟（開發用）

---

## 檔案結構

```
project/
├── README.md              ← 本檔案，系統操作說明
├── 新手手冊.md             ← 環境安裝、SQL 語法入門
├── config.py              ← 資料庫連線設定（host、user、password、database）
├── db.py                  ← 資料庫連線封裝，提供 get_connection()
├── orders.py              ← orders 資料表的所有 CRUD 操作函式
├── logs.py                ← order_logs 資料表的寫入與查詢
├── main.py                ← 終端機互動式選單
├── api.py                 ← FastAPI 後端，提供 REST API 路由
└── static/
    └── index.html         ← 網頁前端，透過 api.py 操作資料庫
```

---

## 資料庫與資料表

| 項目 | 值 |
|------|-----|
| 資料庫 | `my_practice_20260505` |
| 資料表 | `orders`、`order_logs` |

### orders 資料表結構

```sql
CREATE TABLE orders (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    product       VARCHAR(100),
    quantity      INT,
    price         INT,
    order_date    DATE,
    status        VARCHAR(20)
);
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| `id` | INT, AUTO_INCREMENT | 自動產生，不需手動填寫 |
| `customer_name` | VARCHAR(100) | 客戶姓名 |
| `product` | VARCHAR(100) | 商品名稱 |
| `quantity` | INT | 購買數量 |
| `price` | INT | 單價（新台幣） |
| `order_date` | DATE | 格式 `YYYY-MM-DD` |
| `status` | VARCHAR(20) | `待處理` / `已出貨` / `已完成` |

### order_logs 資料表結構

記錄每一次新增、更新、刪除操作，需在 phpMyAdmin 手動建立。

```sql
CREATE TABLE order_logs (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    action     VARCHAR(20),
    order_id   INT,
    detail     TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| `id` | INT, AUTO_INCREMENT | 紀錄編號，自動產生 |
| `action` | VARCHAR(20) | 操作類型：`新增` / `更新狀態` / `更改訂單` / `刪除` |
| `order_id` | INT | 被操作的訂單 id |
| `detail` | TEXT | 操作詳細說明 |
| `created_at` | DATETIME | 操作時間，自動記錄 |

### 商品與價格

| 商品 | 單價 |
|------|------|
| 筆記型電腦 | 25,000 元 |
| 手機 | 18,000 元 |
| 平板 | 12,000 元 |
| 螢幕 | 8,000 元 |
| 耳機 | 2,200 元 |
| 鍵盤 | 1,200 元 |
| 滑鼠 | 500 元 |

---

## 功能說明

兩種介面提供相同的 7 項功能：

| 功能 | 說明 |
|------|------|
| 1. 查詢所有訂單 | 列出全部訂單 |
| 2. 查詢訂單（依條件） | 依客戶姓名、狀態或日期篩選 |
| 3. 新增訂單 | 建立一筆新訂單 |
| 4. 更新訂單狀態 | 只修改 `status` 欄位 |
| 5. 刪除訂單 | 依 id 刪除，需確認 |
| 6. 更改訂單 | 修改客戶姓名、商品、數量、單價、日期 |
| 7. 修改紀錄 | 查看所有操作紀錄（新增 / 更新 / 更改 / 刪除） |

---

## 終端機選單操作說明

執行 `python main.py` 後進入選單，輸入數字選擇功能，輸入 `0` 離開。

### 2. 查詢訂單（依條件）

```
查詢條件：
  1. 客戶姓名
  2. 訂單狀態
  3. 日期
請選擇：1
請輸入客戶姓名：王小明
```

### 3. 新增訂單

以逗號分隔輸入 6 個欄位：

```
格式：客戶姓名,商品,數量,單價,日期,狀態
> 王大明,手機,1,18000,2024-03-03,待處理
```

### 4. 更新訂單狀態

```
請輸入要更新的訂單 id：5
請輸入新狀態：已出貨
```

### 5. 刪除訂單

```
請輸入要刪除的訂單 id：10
確認刪除？（y/n）：y
```

### 6. 更改訂單

```
請輸入要更改的訂單 id：5
  可修改的欄位：
    1. 客戶姓名  2. 商品  3. 數量  4. 單價  5. 日期
  請選擇要修改的欄位：3
  請輸入新的數量：3
```

### 7. 修改紀錄

直接列出最新 200 筆操作紀錄，格式如下：

```
[2026-05-06 14:30:22] 新增     | 訂單 id=51 | 客戶：王大明，商品：手機 x1，單價：18000 元，狀態：待處理
[2026-05-06 14:31:05] 更新狀態 | 訂單 id=51 | 狀態改為：已出貨
[2026-05-06 14:32:10] 刪除     | 訂單 id=51 | 客戶：王大明，商品：手機
```

---

## 網頁介面說明

啟動後開啟 `http://127.0.0.1:8000`，7 個功能對應上方頁籤。

- 狀態欄位統一使用下拉選單選擇
- 日期欄位使用瀏覽器內建日期選擇器
- 「更改訂單」頁籤需先點「載入訂單資料」，確認後再修改送出
- 操作結果即時顯示在頁面上（成功綠色、失敗紅色）
- 「修改紀錄」頁籤點「載入紀錄」顯示操作歷史，最新的排最上面

---

## API 路由一覽（FastAPI）

| 方法 | 路徑 | 功能 |
|------|------|------|
| GET | `/orders` | 查詢所有訂單 |
| GET | `/orders/{id}` | 查詢單筆訂單 |
| GET | `/orders/search?by=customer&value=王小明` | 依條件查詢 |
| POST | `/orders` | 新增訂單 |
| PATCH | `/orders/{id}/status` | 更新訂單狀態 |
| PATCH | `/orders/{id}` | 更改訂單欄位 |
| DELETE | `/orders/{id}` | 刪除訂單 |
| GET | `/logs` | 查詢所有修改紀錄 |

> FastAPI 自動產生互動式 API 文件，啟動後可至 `http://127.0.0.1:8000/docs` 查看。

---

## 常見問題

**Q：啟動 MySQL 失敗，Port 3306 被占用？**
開啟工作管理員，找到並結束 `mysqld.exe` 程序，再重新啟動 XAMPP 的 MySQL。

**Q：Python 連線時出現 Access Denied？**
確認 `config.py` 裡的帳號密碼是否正確，可先在 phpMyAdmin 用同樣帳號密碼登入測試。

**Q：為什麼 id 中間有跳號？**
id 跳號代表曾有資料被刪除，屬於正常現象。id 只需「唯一」，不需「連續」。

**Q：網頁顯示但操作沒有回應？**
確認 `uvicorn api:app --reload` 有正常執行，且 XAMPP MySQL 是啟動狀態。

---

## Git 操作指令

### 第一次 clone 下來（換電腦或給別人用）

```bash
git clone https://github.com/percy890713/phpMyAdmin-database-practice.git
cd phpMyAdmin-database-practice

# 複製設定範本，填入自己的帳號密碼
cp config.example.py config.py
```

然後編輯 `config.py`，把 `your_username` / `your_password` 換成實際的資料庫帳密。

---

### 日常更新推上 GitHub

```bash
# 查看哪些檔案有變動
git status

# 加入要推的檔案（指定檔名，避免誤推敏感資料）
git add db.py orders.py main.py api.py logs.py static/index.html README.md

# 寫 commit 訊息
git commit -m "說明這次改了什麼"

# 推上 GitHub
git push
```

> `config.py` 已加入 `.gitignore`，每次 `git add` 都不會把它包進去，不用擔心密碼外洩。

---

*建立日期：2026-05-05*
