from orders import (
    get_all_orders,
    get_order_by_id,
    get_orders_by_customer,
    get_orders_by_status,
    get_orders_by_date,
    insert_order,
    update_order_status,
    update_order,
    delete_order,
)
from logs import write_log, get_all_logs

VALID_STATUSES = {"待處理", "已出貨", "已完成"}

FIELD_MAP = {
    "1": ("customer_name", "客戶姓名", str),
    "2": ("product",       "商品",     str),
    "3": ("quantity",      "數量",     int),
    "4": ("price",         "單價",     int),
    "5": ("order_date",    "日期",     str),
}


def print_orders(orders):
    if not orders:
        print("  （無符合資料）")
        return
    for o in orders:
        print(
            f"  [{o['id']}] {o['customer_name']} | {o['product']} x{o['quantity']} "
            f"@ {o['price']}元 | {o['order_date']} | {o['status']}"
        )


def input_int(prompt):
    raw = input(prompt).strip()
    if raw.isdigit():
        return int(raw)
    return None


def resolve_order(prompt):
    """輸入 ID（數字）或客戶姓名，回傳對應的訂單 dict，找不到回傳 None。"""
    raw = input(prompt).strip()
    if not raw:
        print("  ✗ 不能為空")
        return None

    if raw.isdigit():
        order = get_order_by_id(int(raw))
        if not order:
            print(f"  ✗ 找不到 id={raw} 的訂單")
        return order

    orders = get_orders_by_customer(raw)
    if not orders:
        print(f"  ✗ 找不到客戶「{raw}」的訂單")
        return None
    if len(orders) == 1:
        return orders[0]

    print(f"  找到 {len(orders)} 筆訂單，請選擇要操作的：")
    print_orders(orders)
    order_id = input_int("  請輸入訂單 id：")
    if order_id is None:
        print("  ✗ id 必須是整數")
        return None
    matched = next((o for o in orders if o["id"] == order_id), None)
    if not matched:
        print(f"  ✗ id={order_id} 不在上方列表中")
        return None
    return matched


# ── 選項處理函式 ────────────────────────────────────────────

def handle_query_all():
    print("\n=== 所有訂單 ===")
    print_orders(get_all_orders())


def handle_query_by_condition():
    print("\n查詢條件：")
    print("  1. 客戶姓名")
    print("  2. 訂單狀態")
    print("  3. 日期")
    choice = input("請選擇：").strip()

    if choice == "1":
        name = input("請輸入客戶姓名：").strip()
        if not name:
            print("  ✗ 姓名不能為空")
            return
        print_orders(get_orders_by_customer(name))

    elif choice == "2":
        print("  狀態選項：待處理 / 已出貨 / 已完成")
        status = input("請輸入狀態：").strip()
        if status not in VALID_STATUSES:
            print(f"  ✗ 無效狀態「{status}」")
            return
        print_orders(get_orders_by_status(status))

    elif choice == "3":
        date = input("請輸入日期（YYYY-MM-DD）：").strip()
        print_orders(get_orders_by_date(date))

    else:
        print("  ✗ 無效選項")


def handle_insert():
    print("\n請輸入訂單資料（以逗號分隔）：")
    print("  格式：客戶姓名,商品,數量,單價,日期,狀態")
    raw = input("> ").strip()
    parts = [p.strip() for p in raw.split(",")]

    if len(parts) != 6:
        print(f"  ✗ 需要 6 個欄位，目前輸入了 {len(parts)} 個")
        return

    customer_name, product, qty_str, price_str, order_date, status = parts

    if not qty_str.isdigit():
        print(f"  ✗ 數量必須是整數，收到「{qty_str}」")
        return
    if not price_str.isdigit():
        print(f"  ✗ 單價必須是整數，收到「{price_str}」")
        return
    if status not in VALID_STATUSES:
        print(f"  ✗ 無效狀態「{status}」，請使用：待處理 / 已出貨 / 已完成")
        return

    data = {
        "customer_name": customer_name,
        "product": product,
        "quantity": int(qty_str),
        "price": int(price_str),
        "order_date": order_date,
        "status": status,
    }
    new_id = insert_order(data)
    write_log("新增", new_id,
              f"客戶：{customer_name}，商品：{product} x{qty_str}，單價：{price_str} 元，狀態：{status}")
    print(f"  ✓ 新增成功，訂單 id = {new_id}")
    print_orders([get_order_by_id(new_id)])


def handle_update_status():
    order = resolve_order("\n請輸入訂單 id 或客戶姓名：")
    if not order:
        return
    order_id = order["id"]
    print("  目前訂單：", end="")
    print_orders([order])

    print("  狀態選項：待處理 / 已出貨 / 已完成")
    status = input("請輸入新狀態：").strip()
    if status not in VALID_STATUSES:
        print(f"  ✗ 無效狀態「{status}」")
        return

    update_order_status(order_id, status)
    write_log("更新狀態", order_id, f"狀態改為：{status}")
    print("  ✓ 更新成功")
    print_orders([get_order_by_id(order_id)])


def handle_delete():
    order = resolve_order("\n請輸入訂單 id 或客戶姓名：")
    if not order:
        return
    order_id = order["id"]
    print("  即將刪除：", end="")
    print_orders([order])

    confirm = input("  確認刪除？（y/n）：").strip().lower()
    if confirm != "y":
        print("  已取消")
        return

    delete_order(order_id)
    write_log("刪除", order_id,
              f"客戶：{order['customer_name']}，商品：{order['product']}")
    print("  ✓ 刪除成功")


def handle_update_order():
    order = resolve_order("\n請輸入訂單 id 或客戶姓名：")
    if not order:
        return
    order_id = order["id"]
    print("  目前訂單：", end="")
    print_orders([order])

    print("\n  可修改的欄位：")
    for key, (_, label, _) in FIELD_MAP.items():
        print(f"    {key}. {label}")

    choice = input("  請選擇要修改的欄位：").strip()
    if choice not in FIELD_MAP:
        print("  ✗ 無效選項")
        return

    col, label, cast = FIELD_MAP[choice]
    new_val_str = input(f"  請輸入新的{label}：").strip()

    if cast == int:
        if not new_val_str.isdigit():
            print(f"  ✗ {label}必須是整數")
            return
        new_val = int(new_val_str)
    else:
        if not new_val_str:
            print(f"  ✗ {label}不能為空")
            return
        new_val = new_val_str

    update_order(order_id, {col: new_val})
    write_log("更改訂單", order_id, f"{label} 改為：{new_val}")
    print("  ✓ 更改成功")
    print_orders([get_order_by_id(order_id)])


def handle_view_logs():
    print("\n=== 修改紀錄（最新 200 筆）===")
    logs = get_all_logs()
    if not logs:
        print("  （尚無紀錄）")
        return
    for log in logs:
        print(f"  [{log['created_at']}] {log['action']} | 訂單 id={log['order_id']} | {log['detail']}")


# ── 主程式 ──────────────────────────────────────────────────

MENU = """
==== 訂單管理系統 ====
1. 查詢所有訂單
2. 查詢訂單（依條件）
3. 新增訂單
4. 更新訂單狀態
5. 刪除訂單
6. 更改訂單
7. 修改紀錄
0. 離開
請選擇功能："""

HANDLERS = {
    "1": handle_query_all,
    "2": handle_query_by_condition,
    "3": handle_insert,
    "4": handle_update_status,
    "5": handle_delete,
    "6": handle_update_order,
    "7": handle_view_logs,
}


def main():
    while True:
        choice = input(MENU).strip()
        if choice == "0":
            print("掰掰！")
            break
        handler = HANDLERS.get(choice)
        if handler:
            handler()
        else:
            print("  ✗ 無效選項，請輸入 0–7")


if __name__ == "__main__":
    main()
