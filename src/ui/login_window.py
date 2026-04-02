import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore Management System - Login")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # Title label
        self.title_label = tk.Label(
            root,
            text="Bookstore Management System",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=15)

        # Username label and entry
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        # Password label and entry
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(
            root,
            text="Login",
            width=15,
            command=self.capture_credentials
        )
        self.login_button.pack(pady=15)

    def capture_credentials(self):
        """
        Capture the username and password entered by the user.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # For now, just show that credentials were captured
        if username and password:
            messagebox.showinfo(
                "Login Submitted",
                f"Username: {username}\nPassword captured successfully."
            )
            print("Captured Username:", username)
            print("Captured Password:", password)
        else:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both username and password."
            )