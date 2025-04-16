import sys
import tkinter as tk
from tkinter import ttk
from db import init_db
from tabs.dashboard import create_dashboard_tab
from tabs.scheduling import create_scheduling_tab
from tabs.customers import create_customers_tab
from tabs.accounting import create_accounting_tab
from tabs.utilities import create_utilities_tab
from tabs.settings import create_settings_tab
from tabs.admin import create_admin_tab

# Block direct access unless launched with the flag
if "--from-login" not in sys.argv:
    print("Access Denied. Please run login.py.")
    sys.exit()

DEV_MODE = True  # Toggle manually

def main():
    init_db()

    root = tk.Tk()
    title = "Landscaping CRM"
    if DEV_MODE:
        title += "  —  DEV MODE ON"
    root.title(title)

    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True)

    create_dashboard_tab(tabs)
    create_scheduling_tab(tabs)
    create_customers_tab(tabs)
    create_accounting_tab(tabs)
    create_utilities_tab(tabs)
    create_settings_tab(tabs)
    create_admin_tab(tabs)

    root.mainloop()

if __name__ == "__main__":
    main()