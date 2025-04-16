import tkinter as tk
from tkinter import ttk
from .service_types import create_service_types_tab
from .users import create_users_tab

def create_utilities_tab(main_notebook):
    tab = tk.Frame(main_notebook)
    main_notebook.add(tab, text="Utilities")

    util_tabs = ttk.Notebook(tab)
    util_tabs.pack(fill="both", expand=True, padx=10, pady=10)

    create_service_types_tab(util_tabs)
    create_users_tab(util_tabs)