
import tkinter as tk
from db import get_connection

def create_service_types_tab(parent):
    tab = tk.Frame(parent)
    parent.add(tab, text="Service Types")

    tk.Label(tab, text="Service Types:").pack(anchor="w", padx=10, pady=(10, 0))
    service_listbox = tk.Listbox(tab, width=50)
    service_listbox.pack(padx=10, pady=5)

    def refresh_services():
        service_listbox.delete(0, tk.END)
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM services ORDER BY name")
            for row in c.fetchall():
                service_listbox.insert(tk.END, row["name"])

    def add_service():
        name = entry.get().strip()
        if name:
            with get_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO services (name) VALUES (?)", (name,))
                conn.commit()
            entry.delete(0, tk.END)
            refresh_services()

    def delete_service():
        selected = service_listbox.curselection()
        if selected:
            name = service_listbox.get(selected[0])
            with get_connection() as conn:
                c = conn.cursor()
                c.execute("DELETE FROM services WHERE name = ?", (name,))
                conn.commit()
            refresh_services()

    entry = tk.Entry(tab, width=30)
    entry.pack(padx=10, pady=(5, 0))
    tk.Button(tab, text="Add Service", command=add_service).pack(padx=10, pady=2)
    tk.Button(tab, text="Delete Selected", command=delete_service).pack(padx=10, pady=2)

    refresh_services()
