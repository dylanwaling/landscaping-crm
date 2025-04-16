
import tkinter as tk
from db import get_connection

def add_customer_popup(refresh_callback):
    def save():
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO customers (name, phone, email, address, gate_code, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name_entry.get(),
                phone_entry.get(),
                email_entry.get(),
                address_entry.get(),
                gate_code_entry.get(),
                notes_text.get("1.0", tk.END).strip()
            ))
            conn.commit()
            refresh_callback()
            top.destroy()

    top = tk.Toplevel()
    top.title("Add Customer")

    labels = ["Name", "Phone", "Email", "Address", "Gate Code"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(top, text=label).grid(row=i, column=0, sticky="e", pady=2)
        entry = tk.Entry(top, width=40)
        entry.grid(row=i, column=1, pady=2)
        entries.append(entry)

    name_entry, phone_entry, email_entry, address_entry, gate_code_entry = entries

    tk.Label(top, text="Notes").grid(row=len(labels), column=0, sticky="ne", pady=(10, 0))
    notes_text = tk.Text(top, width=40, height=5, wrap="word")
    notes_text.grid(row=len(labels), column=1, pady=(10, 0))

    tk.Button(top, text="Save", command=save).grid(row=len(labels)+1, columnspan=2, pady=10)

def edit_customer_popup(listbox, refresh_callback):
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    customer = listbox.customers[index]

    def save():
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE customers SET name=?, phone=?, email=?, address=?, gate_code=?, notes=?
                WHERE id=?
            """, (
                name_entry.get(),
                phone_entry.get(),
                email_entry.get(),
                address_entry.get(),
                gate_code_entry.get(),
                notes_text.get("1.0", tk.END).strip(),
                customer["id"]
            ))
            conn.commit()
            refresh_callback()
            top.destroy()

    top = tk.Toplevel()
    top.title("Edit Customer")

    labels = ["Name", "Phone", "Email", "Address", "Gate Code"]
    values = [
        customer["name"],
        customer["phone"],
        customer["email"],
        customer["address"],
        customer["gate_code"] or ""
    ]
    entries = []

    for i, (label, value) in enumerate(zip(labels, values)):
        tk.Label(top, text=label).grid(row=i, column=0, sticky="e", pady=2)
        entry = tk.Entry(top, width=40)
        entry.insert(0, value)
        entry.grid(row=i, column=1, pady=2)
        entries.append(entry)

    name_entry, phone_entry, email_entry, address_entry, gate_code_entry = entries

    tk.Label(top, text="Notes").grid(row=len(labels), column=0, sticky="ne", pady=(10, 0))
    notes_text = tk.Text(top, width=40, height=5, wrap="word")
    notes_text.insert(tk.END, customer["notes"] or "")
    notes_text.grid(row=len(labels), column=1, pady=(10, 0))

    tk.Button(top, text="Save Changes", command=save).grid(row=len(labels)+1, columnspan=2, pady=10)
