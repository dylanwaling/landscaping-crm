
import tkinter as tk
from tkinter import ttk
import datetime
from db import get_connection
from .dropdowns import create_dropdown
from .logic import refresh_job_list

def date_list():
    today = datetime.date.today()
    return [(today + datetime.timedelta(days=i)).isoformat() for i in range(90)]

def job_popup(job, job_listbox):
    def save():
        customer = customer_var.get()
        service = service_var.get()
        date_val = date_var.get()

        if not customer or not service or not date_val:
            return

        with get_connection() as conn:
            c = conn.cursor()
            if job:
                c.execute("""
                    UPDATE jobs SET customer_name=?, service=?, date=?, notes=?
                    WHERE id=?
                """, (
                    customer,
                    service,
                    date_val,
                    notes_text.get("1.0", tk.END).strip(),
                    job["id"]
                ))
            else:
                c.execute("""
                    INSERT INTO jobs (customer_name, service, date, notes)
                    VALUES (?, ?, ?, ?)
                """, (
                    customer,
                    service,
                    date_val,
                    notes_text.get("1.0", tk.END).strip()
                ))
            conn.commit()
            refresh_job_list(job_listbox)
            top.destroy()

    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM customers ORDER BY name")
        customer_list = [row["name"] for row in c.fetchall()]
        c.execute("SELECT name FROM services ORDER BY name")
        service_list = [row["name"] for row in c.fetchall()]

    top = tk.Toplevel()
    top.title("Edit Scheduled Job" if job else "Add Scheduled Job")

    customer_var = tk.StringVar(value=job["customer_name"] if job else "")
    customer_entry = tk.Entry(top, textvariable=customer_var, width=40)
    tk.Label(top, text="Customer").grid(row=0, column=0, sticky="e", pady=2)
    customer_entry.grid(row=0, column=1, pady=2)
    create_dropdown(top, customer_entry, customer_list, customer_var)

    service_var = tk.StringVar(value=job["service"] if job else "")
    service_entry = tk.Entry(top, textvariable=service_var, width=40)
    tk.Label(top, text="Service Type").grid(row=1, column=0, sticky="e", pady=2)
    service_entry.grid(row=1, column=1, pady=2)
    create_dropdown(top, service_entry, service_list, service_var)

    date_var = tk.StringVar(value=job["date"] if job else datetime.date.today().isoformat())
    date_entry = ttk.Combobox(top, textvariable=date_var, values=date_list(), width=37)
    tk.Label(top, text="Scheduled Date").grid(row=2, column=0, sticky="e", pady=2)
    date_entry.grid(row=2, column=1, pady=2)

    notes_text = tk.Text(top, width=40, height=5, wrap="word")
    tk.Label(top, text="Notes").grid(row=3, column=0, sticky="ne", pady=(10, 0))
    notes_text.grid(row=3, column=1, pady=(10, 0))
    if job:
        notes_text.insert(tk.END, job["notes"] or "")

    tk.Button(top, text="Save", command=save).grid(row=4, columnspan=2, pady=10)

def add_job_popup(job_listbox):
    job_popup(None, job_listbox)

def edit_job_popup(job_listbox):
    selected = job_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    job = job_listbox.jobs[index]
    job_popup(job, job_listbox)
