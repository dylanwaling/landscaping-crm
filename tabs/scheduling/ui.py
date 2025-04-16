
import tkinter as tk
from .logic import fetch_jobs, delete_job
from .job_popup import add_job_popup, edit_job_popup
from .logic import refresh_job_list

jobs = []
job_listbox = None

def create_scheduling_tab(notebook):
    global job_listbox

    tab = tk.Frame(notebook)
    notebook.add(tab, text="Scheduling")

    job_listbox = tk.Listbox(tab, width=100)
    job_listbox.pack(padx=10, pady=(10, 5))

    buttons = tk.Frame(tab)
    buttons.pack(pady=5)

    tk.Button(buttons, text="Add Job", width=12, command=lambda: add_job_popup(job_listbox)).grid(row=0, column=0, padx=5)
    tk.Button(buttons, text="Edit Job", width=12, command=lambda: edit_job_popup(job_listbox)).grid(row=0, column=1, padx=5)
    tk.Button(buttons, text="Delete Job", width=12, command=lambda: delete_job(job_listbox)).grid(row=0, column=2, padx=5)
    tk.Button(buttons, text="Refresh", width=12, command=lambda: refresh_job_list(job_listbox)).grid(row=0, column=3, padx=5)

    refresh_job_list(job_listbox)
