import tkinter as tk
from .calendar import get_upcoming_events

def create_dashboard_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Dashboard")

    label = tk.Label(tab, text="Upcoming Google Calendar Events", font=("Helvetica", 12, "bold"))
    label.pack(pady=10)

    event_box = tk.Text(tab, height=10, width=80)
    event_box.pack(padx=10, pady=5)

    events = get_upcoming_events()
    if not events:
        event_box.insert(tk.END, "No upcoming events found.")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            event_box.insert(tk.END, f"{start} - {summary}\n")

    event_box.config(state="disabled")