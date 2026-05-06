# CLAUDE.md — MySQL Python 學習專案指引

## 專案概覽

這是一個 MySQL 資料庫學習專案，使用 Python 透過 `mysql-connector-python` 連接本機 XAMPP 的 MySQL（MariaDB）伺服器，並對 `orders`（訂單）資料表進行 CRUD 操作。

---

## 環境設定

| 項目 | 設定值 |
|------|--------|
| 資料庫主機 | `127.0.0.1` |
| 埠號 | `3306` |
| 資料庫名稱 | `my_practice_20260505` |
| 資料表名稱 | `orders` |
| 使用者帳號 | `TestingProject0505`（或 `percy`） |
| 密碼 | 自行設定 |

> 連線設定統一寫在 `config.py`，所有其他檔案從這裡 import，不要在每個檔案重複寫連線資訊。

---

## 安裝依賴套件

```bash
pip install mysql-connector-python
```

---

## 專案結構

```
project/
├── CLAUDE.md         ← 本檔案，給 Claude Code 的指引
├── README.md         ← 給人類看的說明文件
├── config.py         ← 資料庫連線設定
├── db.py             ← 資料庫連線與基礎操作封裝
├── orders.py         ← orders 資料表的 CRUD 操作
└── main.py           ← 主程式入口，示範各功能
```

---

## 資料表結構：orders

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

### 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `id` | INT, AUTO_INCREMENT | 訂單唯一編號，自動遞增，不需手動填寫 |
| `customer_name` | VARCHAR(100) | 客戶姓名 |
| `product` | VARCHAR(100) | 商品名稱（筆記型電腦、滑鼠、鍵盤等） |
| `quantity` | INT | 購買數量 |
| `price` | INT | 單價（新台幣） |
| `order_date` | DATE | 訂單日期，格式 `YYYY-MM-DD` |
| `status` | VARCHAR(20) | 訂單狀態：`待處理` / `已出貨` / `已完成` |

---

## 各檔案職責

### config.py
存放資料庫連線參數，包含 host、port、user、password、database。修改連線資訊只需改這一個檔案。

### db.py
封裝 `mysql.connector` 的連線與關閉邏輯，提供 `get_connection()` 函式供其他模組使用。

### orders.py
針對 `orders` 資料表的所有操作：
- `get_all_orders()` — 取得所有訂單
- `get_order_by_id(id)` — 依 id 取得單筆訂單
- `get_orders_by_customer(name)` — 依客戶名稱查詢
- `get_orders_by_status(status)` — 依狀態篩選
- `insert_order(data)` — 新增訂單
- `update_order_status(id, status)` — 更新訂單狀態
- `delete_order(id)` — 刪除訂單

### main.py
示範呼叫各功能的主程式，執行 `python main.py` 即可測試所有操作。

---

## 注意事項

- 所有 SQL 操作使用參數化查詢（`%s` 佔位符），避免 SQL Injection
- 執行 INSERT / UPDATE / DELETE 後記得呼叫 `connection.commit()`
- 操作完畢後記得關閉 cursor 和 connection
- `order_date` 傳入格式為字串 `'YYYY-MM-DD'` 或 Python `datetime.date` 物件皆可
