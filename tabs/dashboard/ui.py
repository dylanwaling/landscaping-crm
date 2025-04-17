import tkinter as tk
import datetime

def create_dashboard_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Dashboard")

    today = datetime.date.today().strftime('%A, %B %d, %Y')
    label = tk.Label(tab, text=f"Today: {today}", font=("Helvetica", 14, "bold"))
    label.pack(pady=20)

    summary = tk.Label(tab, text="Your current day overview will go here.")
    summary.pack()