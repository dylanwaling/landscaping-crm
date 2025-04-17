import tkinter as tk
from .logic import save_job_for_day

def open_job_editor(year, month, day):
    top = tk.Toplevel()
    top.title(f"Add Job for {year}-{month:02d}-{day:02d}")

    tk.Label(top, text="Job description:").pack(pady=5)
    text = tk.Text(top, width=40, height=5)
    text.pack(padx=10)

    def save():
        job = text.get("1.0", "end").strip()
        if job:
            save_job_for_day(year, month, day, job)
        top.destroy()

    tk.Button(top, text="Save", command=save).pack(pady=10)