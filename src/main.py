import tkinter as tk
from tkinter import messagebox

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "staff": {"password": "staff123", "role": "Staff"},
    "customer": {"password": "cust123", "role": "Customer"},
}

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Management System - Login")
        self.root.geometry("420x260")

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        print("Username:", username)
        print("Password:", password)

        if not username:
            messagebox.showwarning("Error", "Username is required")
            return

        if not password:
            messagebox.showwarning("Error", "Password is required")
            return

        if username not in USERS or USERS[username]["password"] != password:
            messagebox.showerror("Error", "Invalid credentials")
            return

        role = USERS[username]["role"]
        messagebox.showinfo("Success", f"Welcome {username} ({role})")
        self.open_dashboard(username, role)

    def open_dashboard(self, username, role):
        dashboard = tk.Toplevel(self.root)
        dashboard.title(f"{role} Dashboard")
        dashboard.geometry("350x180")

        tk.Label(
            dashboard,
            text=f"Welcome, {username}",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        tk.Label(
            dashboard,
            text=f"Role: {role}",
            font=("Arial", 12)
        ).pack(pady=5)

        if role == "Admin":
            msg = "You can manage inventory, users, and reports."
        elif role == "Staff":
            msg = "You can manage books and customer orders."
        else:
            msg = "You can browse books and manage purchases."

        tk.Label(
            dashboard,
            text=msg,
            wraplength=280,
            justify="center"
        ).pack(pady=10)

root = tk.Tk()
app = LoginApp(root)
root.mainloop()