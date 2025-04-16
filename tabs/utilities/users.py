import tkinter as tk
from tkinter import ttk
from db import get_connection
from tkinter import messagebox

def create_users_tab(parent):
    tab = ttk.Frame(parent)
    parent.add(tab, text="Users")

    ttk.Label(tab, text="Manage Application Users").pack(pady=(10, 5), anchor="w", padx=10)

    user_listbox = tk.Listbox(tab, width=40)
    user_listbox.pack(padx=10, pady=(0, 5))

    username_entry = ttk.Entry(tab, width=30)
    password_entry = ttk.Entry(tab, width=30)
    username_entry.pack(padx=10, pady=(5, 0))
    password_entry.pack(padx=10, pady=(2, 5))

    def refresh_users():
        user_listbox.delete(0, tk.END)
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            for row in c.execute("SELECT username FROM users ORDER BY username"):
                user_listbox.insert(tk.END, row["username"])

    def add_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Missing Info", "Username and password are required.")
            return
        with get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                refresh_users()
            except Exception as e:
                messagebox.showerror("Error", f"User not added: {e}")

    def delete_user():
        selected = user_listbox.curselection()
        if not selected:
            return
        username = user_listbox.get(selected[0])
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
        refresh_users()

    def edit_user_popup():
        selected = user_listbox.curselection()
        if not selected:
            return
        username = user_listbox.get(selected[0])

        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if not user:
                return

        def save_changes():
            new_user = user_entry.get().strip()
            new_pass = pass_entry.get().strip()
            if not new_user or not new_pass:
                messagebox.showerror("Missing Info", "Both fields are required.")
                return
            with get_connection() as conn:
                c = conn.cursor()
                try:
                    c.execute("UPDATE users SET username=?, password=? WHERE id=?", (new_user, new_pass, user["id"]))
                    conn.commit()
                    edit_win.destroy()
                    refresh_users()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        edit_win = tk.Toplevel()
        edit_win.title("Edit User")
        ttk.Label(edit_win, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        user_entry = ttk.Entry(edit_win, width=30)
        user_entry.insert(0, user["username"])
        user_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(edit_win, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        pass_entry = ttk.Entry(edit_win, width=30)
        pass_entry.insert(0, user["password"])
        pass_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(edit_win, text="Save", command=save_changes).grid(row=2, columnspan=2, pady=10)

    ttk.Button(tab, text="Add User", command=add_user).pack(padx=10, pady=(2, 5))
    ttk.Button(tab, text="Edit Selected", command=edit_user_popup).pack(padx=10, pady=2)
    ttk.Button(tab, text="Delete Selected", command=delete_user).pack(padx=10, pady=(0, 10))

    refresh_users()