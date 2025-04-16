
import tkinter as tk
from .logic import fetch_customers, preview_notes, delete_customer
from .popup import add_customer_popup, edit_customer_popup

customers = []
customer_listbox = None
customer_notes = None
search_var = None

def create_customers_tab(notebook):
    global customer_listbox, customer_notes, search_var, customers

    tab = tk.Frame(notebook)
    notebook.add(tab, text="Customers")

    search_var = tk.StringVar()
    search_var.trace_add("write", lambda *args: refresh_customer_list(search_var.get()))

    tk.Label(tab, text="Search:").pack(anchor="w", padx=10, pady=(10, 0))
    tk.Entry(tab, textvariable=search_var, width=50).pack(anchor="w", padx=10)

    customer_listbox = tk.Listbox(tab, width=140)
    customer_listbox.pack(padx=10, pady=(5, 0))
    customer_listbox.bind("<<ListboxSelect>>", on_customer_select)

    tk.Label(tab, text="Full Notes:").pack(anchor="w", padx=10, pady=(10, 0))
    customer_notes = tk.Text(tab, height=5, width=140, wrap="word")
    customer_notes.pack(padx=10, pady=5)
    customer_notes.config(state="disabled")

    buttons = tk.Frame(tab)
    buttons.pack(pady=5)
    tk.Button(buttons, text="Add", width=12, command=lambda: add_customer_popup(refresh_customer_list)).grid(row=0, column=0, padx=5)
    tk.Button(buttons, text="Edit", width=12, command=lambda: edit_customer_popup(customer_listbox, refresh_customer_list)).grid(row=0, column=1, padx=5)
    tk.Button(buttons, text="Delete", width=12, command=lambda: delete_customer(customer_listbox, refresh_customer_list)).grid(row=0, column=2, padx=5)
    tk.Button(buttons, text="Refresh", width=12, command=lambda: refresh_customer_list()).grid(row=0, column=3, padx=5)

    refresh_customer_list()

def refresh_customer_list(filter_text=""):
    global customers, customer_listbox
    customers = fetch_customers(filter_text)
    customer_listbox.delete(0, tk.END)
    for c in customers:
        preview = preview_notes(c["notes"])
        display = f"{c['name']} | {c['phone']} | {c['email']} | {c['address']} | Gate: {c['gate_code']} | {preview}"
        customer_listbox.insert(tk.END, display)
    customer_listbox.customers = customers

def on_customer_select(event):
    global customers, customer_listbox, customer_notes
    selected = customer_listbox.curselection()
    if not selected:
        customer_notes.config(state="normal")
        customer_notes.delete("1.0", tk.END)
        customer_notes.config(state="disabled")
        return

    index = selected[0]
    full_notes = customers[index]["notes"] or ""
    customer_notes.config(state="normal")
    customer_notes.delete("1.0", tk.END)
    customer_notes.insert(tk.END, full_notes)
    customer_notes.config(state="disabled")
