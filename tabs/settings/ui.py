import tkinter as tk
from tkinter import ttk
import os
import json

def create_settings_tab(main_notebook):
    tab = tk.Frame(main_notebook)
    main_notebook.add(tab, text="Settings")

    settings_tabs = ttk.Notebook(tab)
    settings_tabs.pack(fill="both", expand=True, padx=10, pady=10)

    create_google_tab(settings_tabs)

def create_google_tab(parent):
    tab = ttk.Frame(parent)
    parent.add(tab, text="Google Calendar")

    status_label = ttk.Label(tab, text="")
    status_label.pack(pady=(10, 5))

    def get_account_info():
        if os.path.exists("token.json"):
            try:
                with open("token.json") as f:
                    data = json.load(f)
                    email = data.get("email", None)
                    return f"Signed in" if email is None else f"Signed in as: {email}"
            except:
                return "Signed in (email unavailable)"
        return "Not signed in"

    def update_status():
        status_label.config(text=get_account_info())

    def sign_in():
        from tabs.dashboard.calendar import get_upcoming_events
        get_upcoming_events(1)
        update_status()

    def sign_out():
        try:
            os.remove("token.json")
        except FileNotFoundError:
            pass
        update_status()

    update_status()

    ttk.Button(tab, text="Sign In with Google", command=sign_in).pack(pady=5)
    ttk.Button(tab, text="Sign Out", command=sign_out).pack(pady=5)