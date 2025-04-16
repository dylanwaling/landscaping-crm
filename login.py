import tkinter as tk
from tkinter import messagebox
from db import get_connection, init_db
import subprocess
import sys

DEV_MODE = True  # ✅ Turn this off when going live

def try_login(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return c.fetchone()

def main():
    init_db()

    if DEV_MODE:
        print("🔧 DEV MODE ACTIVE - Skipping login...")
        subprocess.run([sys.executable, "main.py", "--from-login"])
        return

    root = tk.Tk()
    root.title("Login")
    root.geometry("300x210")

    if DEV_MODE:
        label = tk.Label(root, text="DEV MODE ACTIVE", fg="red")
        label.pack(pady=(10, 0))

    tk.Label(root, text="Username").pack(pady=(20 if not DEV_MODE else 10), padx=10)
    user_entry = tk.Entry(root)
    user_entry.pack()

    tk.Label(root, text="Password").pack(pady=5)
    pass_entry = tk.Entry(root)
    pass_entry.pack()

    def login_action():
        user = user_entry.get().strip()
        pw = pass_entry.get().strip()
        if not user or not pw:
            messagebox.showerror("Error", "Enter both fields.")
            return
        user_data = try_login(user, pw)
        if user_data:
            root.destroy()
            subprocess.run([sys.executable, "main.py", "--from-login"])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(root, text="Login", command=login_action).pack(pady=15)
    root.mainloop()

if __name__ == "__main__":
    main()