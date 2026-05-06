from db import get_connection


def write_log(action, order_id, detail):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO order_logs (action, order_id, detail) VALUES (%s, %s, %s)",
        (action, order_id, detail),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_logs(limit=200):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM order_logs ORDER BY created_at DESC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
