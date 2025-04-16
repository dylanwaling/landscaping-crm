import tkinter as tk

def create_dashboard_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Dashboard")
    tk.Label(tab, text="📊 Dashboard Coming Soon", font=("Arial", 14)).pack(pady=20)
