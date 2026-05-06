from db import get_connection


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_order_by_id(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_orders_by_customer(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE customer_name = %s", (name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_orders_by_status(status):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE status = %s", (status,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_order(data):
    """
    data: dict with keys customer_name, product, quantity, price, order_date, status
    Returns the new row's id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO orders (customer_name, product, quantity, price, order_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        data["customer_name"],
        data["product"],
        data["quantity"],
        data["price"],
        data["order_date"],
        data["status"],
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_order_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def delete_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected


def get_orders_by_date(date):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_date = %s", (date,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def update_order(order_id, fields):
    """
    fields: dict of column -> new value, e.g. {"quantity": 3, "price": 1500}
    Allowed columns: customer_name, product, quantity, price, order_date
    """
    allowed = {"customer_name", "product", "quantity", "price", "order_date"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return 0
    set_clause = ", ".join(f"{col} = %s" for col in updates)
    values = list(updates.values()) + [order_id]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE orders SET {set_clause} WHERE id = %s", values)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
