
import tkinter as tk

def create_dropdown(top, entry_widget, values_list, text_var):
    dropdown = tk.Toplevel(top)
    dropdown.withdraw()
    dropdown.overrideredirect(True)
    dropdown.attributes("-topmost", True)

    listbox = tk.Listbox(dropdown, width=40, height=5)
    listbox.pack()

    just_selected = {"value": False}

    def show_dropdown():
        if not dropdown.winfo_viewable():
            x = entry_widget.winfo_rootx()
            y = entry_widget.winfo_rooty() + entry_widget.winfo_height()
            dropdown.geometry(f"+{x}+{y}")
            dropdown.deiconify()

    def hide_dropdown():
        dropdown.withdraw()

    def update_dropdown(event=None):
        if just_selected["value"]:
            return
        typed = text_var.get().lower()
        listbox.delete(0, tk.END)
        matches = [val for val in values_list if typed in val.lower()]
        for val in matches:
            listbox.insert(tk.END, val)
        if matches:
            show_dropdown()
        else:
            hide_dropdown()

    def fill_selection(event=None):
        if listbox.curselection():
            selection = listbox.get(listbox.curselection()[0])
            text_var.set(selection)
            just_selected["value"] = True
            hide_dropdown()
            top.after(200, lambda: just_selected.update({"value": False}))

    entry_widget.bind("<KeyRelease>", update_dropdown)
    entry_widget.bind("<FocusIn>", update_dropdown)
    listbox.bind("<ButtonRelease-1>", fill_selection)
