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

import calendar
import datetime
from .popup import open_job_editor
from .logic import get_jobs_for_day

def create_calendar_view(parent):
    now = datetime.datetime.now()
    year, month = now.year, now.month
    cal = calendar.Calendar()

    header = tk.Label(parent, text=f"{calendar.month_name[month]} {year}", font=("Helvetica", 14, "bold"))
    header.grid(row=7, column=0, columnspan=7, pady=10)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(weekdays):
        tk.Label(parent, text=day).grid(row=8, column=i)

    row = 9
    for week in cal.monthdayscalendar(year, month):
        for col, day in enumerate(week):
            if day == 0:
                continue

            frame = tk.Frame(parent, borderwidth=1, relief="solid", width=80, height=60)
            frame.grid_propagate(False)
            frame.grid(row=row, column=col, padx=1, pady=1)

            def make_clickable(widget, y=year, m=month, d=day):
                widget.bind("<Button-1>", lambda e: open_job_editor(y, m, d))

            day_label = tk.Label(frame, text=str(day), anchor="nw")
            day_label.pack(anchor="nw")
            make_clickable(frame)
            make_clickable(day_label)

            jobs = get_jobs_for_day(year, month, day)
            if jobs:
                job_preview = tk.Label(frame, text=f"{len(jobs)} job(s)", fg="blue", font=("Arial", 8))
                job_preview.pack()
                make_clickable(job_preview)
        row += 1