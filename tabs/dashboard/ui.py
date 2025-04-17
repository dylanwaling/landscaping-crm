import tkinter as tk
import calendar
import datetime
from .popup import open_job_editor
from .logic import get_jobs_for_day

def create_dashboard_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Dashboard")

    now = datetime.datetime.now()
    year, month = now.year, now.month
    cal = calendar.Calendar()

    header = tk.Label(tab, text=f"{calendar.month_name[month]} {year}", font=("Helvetica", 14, "bold"))
    header.grid(row=0, column=0, columnspan=7, pady=10)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(weekdays):
        tk.Label(tab, text=day).grid(row=1, column=i)

    row = 2
    for week in cal.monthdayscalendar(year, month):
        for col, day in enumerate(week):
            if day == 0:
                continue

            frame = tk.Frame(tab, borderwidth=1, relief="solid", width=80, height=60)
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