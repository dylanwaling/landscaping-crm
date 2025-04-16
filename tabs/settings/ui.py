import tkinter as tk
from tkinter import ttk

def create_settings_tab(main_notebook):
    tab = tk.Frame(main_notebook)
    main_notebook.add(tab, text="Settings")

    settings_tabs = ttk.Notebook(tab)
    settings_tabs.pack(fill="both", expand=True, padx=10, pady=10)

    # No tabs currently (future: preferences, integrations, etc.)