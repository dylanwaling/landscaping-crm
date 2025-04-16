import tkinter as tk

def create_admin_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Admin")
    tk.Label(tab, text="🛡️ Admin Tools Coming Soon", font=("Arial", 14)).pack(pady=20)
