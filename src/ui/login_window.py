import tkinter as tk
from tkinter import messagebox, ttk


class LoginWindow(ttk.Frame):
    def __init__(self, master, auth_service, on_login_success):
        super().__init__(master, padding=24)
        self.auth_service = auth_service
        self.on_login_success = on_login_success

        self.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            self,
            text="Bookstore Management System",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        subtitle_label = ttk.Label(
            self,
            text="Sign in with a staff or customer account to continue.",
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 18))

        form_frame = ttk.Frame(self)
        form_frame.grid(row=2, column=0, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Username").grid(
            row=0, column=0, sticky="w", padx=(0, 12), pady=6
        )
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(form_frame, text="Password").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=6
        )
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=6)

        demo_label = ttk.Label(
            self,
            text="Demo users: manager / securepass, staff1 / books123, customer1 / reader123",
        )
        demo_label.grid(row=3, column=0, sticky="w", pady=(0, 8))

        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self, textvariable=self.status_var, foreground="#b42318")
        self.status_label.grid(row=4, column=0, sticky="w", pady=(12, 6))

        login_button = ttk.Button(self, text="Login", command=self.capture_credentials)
        login_button.grid(row=5, column=0, sticky="ew", pady=(8, 0))

        self.username_entry.focus_set()
        self.password_entry.bind("<Return>", lambda _event: self.capture_credentials())

    def capture_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        is_valid, message, user = self.auth_service.authenticate(username, password)

        if not is_valid:
            self.status_var.set(message)
            messagebox.showwarning("Login Error", message)
            return

        self.status_var.set("")
        print("Captured Username:", user["username"])
        print("Captured Password:", password)
        print("Assigned Role:", user["role"])
        messagebox.showinfo(
            "Login Submitted",
            f"Username: {user['username']}\nRole: {user['role']}\nCredentials captured successfully.",
        )
        self.on_login_success(user)
