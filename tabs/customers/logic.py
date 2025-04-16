
from db import get_connection

def fetch_customers(keyword=""):
    with get_connection() as conn:
        c = conn.cursor()
        like = f"%{keyword}%"
        c.execute("""
            SELECT * FROM customers
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR notes LIKE ? OR gate_code LIKE ?
        """, (like, like, like, like, like, like))
        return c.fetchall()

def preview_notes(text, word_limit=30):
    if not text:
        return ""
    words = text.split()
    return " ".join(words[:word_limit]) + ("..." if len(words) > word_limit else "")

def delete_customer(listbox, refresh_callback):
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    customer_id = listbox.customers[index]["id"]

    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
    refresh_callback()
