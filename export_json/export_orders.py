import sys
import os
import json
import datetime

# 把上層目錄加入 Python 路徑，才能 import 上層的 orders / db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orders import get_all_orders


def serialize(obj):
    """讓 datetime.date / datetime.datetime 可以被 json.dumps 序列化"""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def export_orders_to_json(output_path: str = None):
    rows = get_all_orders()

    if output_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(output_dir, f"orders_{timestamp}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2, default=serialize)

    print(f"已匯出 {len(rows)} 筆訂單 → {output_path}")
    return output_path


if __name__ == "__main__":
    export_orders_to_json()


# ───────────────────────────────────────────────
# 情境：只匯出購買「滑鼠」的訂單
#
# 做法：
#   1. 一樣呼叫 get_all_orders() 抓全部資料
#   2. 用 Python 的 list comprehension 過濾出 product == "滑鼠" 的資料
#   3. 把過濾後的結果寫成 JSON，檔名加上 _mouse 方便辨識
#
# 執行方式：
#   cd "d:\user\桌面\練習\資料庫實作練習"
#   python export_json/export_orders.py
#   → 執行後會呼叫下方 export_mouse_orders_to_json()
# ───────────────────────────────────────────────

def export_mouse_orders_to_json(output_path: str = None):
    # 取得全部訂單
    all_rows = get_all_orders()

    # 只保留 product 欄位等於「滑鼠」的資料列
    mouse_rows = [row for row in all_rows if row["product"] == "滑鼠"]

    if output_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(output_dir, f"orders_mouse_{timestamp}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mouse_rows, f, ensure_ascii=False, indent=2, default=serialize)

    print(f"已匯出 {len(mouse_rows)} 筆滑鼠訂單 → {output_path}")
    return output_path


# 若想直接執行這個情境，把下方註解拿掉、把上方的 export_orders_to_json() 註解掉即可：
# if __name__ == "__main__":
#     export_mouse_orders_to_json()
