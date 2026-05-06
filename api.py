from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

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

app = FastAPI(title="訂單管理系統")

VALID_STATUSES = {"待處理", "已出貨", "已完成"}


def serialize(obj):
    """將 datetime.date / datetime.datetime 轉成字串，確保 JSON 序列化正常。"""
    if isinstance(obj, list):
        return [serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in obj.items()}
    return obj


class NewOrder(BaseModel):
    customer_name: str
    product: str
    quantity: int
    price: int
    order_date: str
    status: str


class StatusUpdate(BaseModel):
    status: str


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[int] = None
    order_date: Optional[str] = None


# ── 查詢 ────────────────────────────────────────────────────

@app.get("/orders")
def api_get_all():
    return serialize(get_all_orders())


@app.get("/orders/search")
def api_search(by: str, value: str):
    if by == "customer":
        return serialize(get_orders_by_customer(value))
    if by == "status":
        if value not in VALID_STATUSES:
            raise HTTPException(400, f"無效狀態：{value}")
        return serialize(get_orders_by_status(value))
    if by == "date":
        return serialize(get_orders_by_date(value))
    raise HTTPException(400, f"無效的查詢條件：{by}")


@app.get("/orders/{order_id}")
def api_get_one(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(404, "找不到該訂單")
    return serialize(order)


# ── 新增 ────────────────────────────────────────────────────

@app.post("/orders", status_code=201)
def api_insert(order: NewOrder):
    if order.status not in VALID_STATUSES:
        raise HTTPException(400, f"無效狀態：{order.status}")
    new_id = insert_order(order.dict())
    write_log("新增", new_id,
              f"客戶：{order.customer_name}，商品：{order.product} x{order.quantity}，"
              f"單價：{order.price} 元，狀態：{order.status}")
    return {"id": new_id}


# ── 更新狀態 ─────────────────────────────────────────────────

@app.patch("/orders/{order_id}/status")
def api_update_status(order_id: int, body: StatusUpdate):
    if body.status not in VALID_STATUSES:
        raise HTTPException(400, f"無效狀態：{body.status}")
    if not get_order_by_id(order_id):
        raise HTTPException(404, "找不到該訂單")
    update_order_status(order_id, body.status)
    write_log("更新狀態", order_id, f"狀態改為：{body.status}")
    return serialize(get_order_by_id(order_id))


# ── 更改欄位 ─────────────────────────────────────────────────

@app.patch("/orders/{order_id}")
def api_update_fields(order_id: int, body: OrderUpdate):
    if not get_order_by_id(order_id):
        raise HTTPException(404, "找不到該訂單")
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(400, "至少需要修改一個欄位")
    update_order(order_id, fields)
    detail = "，".join(f"{k} 改為 {v}" for k, v in fields.items())
    write_log("更改訂單", order_id, detail)
    return serialize(get_order_by_id(order_id))


# ── 刪除 ────────────────────────────────────────────────────

@app.delete("/orders/{order_id}")
def api_delete(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(404, "找不到該訂單")
    delete_order(order_id)
    write_log("刪除", order_id,
              f"客戶：{order['customer_name']}，商品：{order['product']}")
    return {"message": "刪除成功"}


# ── 修改紀錄 ─────────────────────────────────────────────────

@app.get("/logs")
def api_get_logs():
    return serialize(get_all_logs())


# ── 靜態檔案（前端）放最後，避免攔截 API 路由 ─────────────────

app.mount("/", StaticFiles(directory="static", html=True), name="static")
