import tkinter as tk

def create_accounting_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Accounting")
    tk.Label(tab, text="💵 Accounting Coming Soon", font=("Arial", 14)).pack(pady=20)
